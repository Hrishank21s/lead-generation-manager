"""Smoke tests: CLI, every page, lead save + checklist, mailto drafts, CSRF/rebinding guards.
Run: python3 -m unittest discover tests   (no Claude calls - LEADGEN_CLAUDE points at a missing binary)"""
import os, subprocess, sys, tempfile, threading, unittest, urllib.error, urllib.parse, urllib.request
from pathlib import Path

TMP = tempfile.mkdtemp()
os.environ["LEADGEN_DB"] = str(Path(TMP) / "test.db")
os.environ["LEADGEN_CLAUDE"] = str(Path(TMP) / "no-such-claude")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import leadgen  # noqa: E402


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a):
        return None


open_url = urllib.request.build_opener(NoRedirect).open


class LeadGenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        leadgen.init()
        cls.srv = leadgen.ThreadingHTTPServer(("127.0.0.1", 0), leadgen.H)
        cls.base = f"http://127.0.0.1:{cls.srv.server_port}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def req(self, path, data=None, origin="self", host=None):
        r = urllib.request.Request(self.base + path, data=urllib.parse.urlencode(data, doseq=True).encode() if data else None)
        if origin:
            r.add_header("Origin", self.base if origin == "self" else origin)
        if host:
            r.add_header("Host", host)
        try:
            with open_url(r) as resp:
                return resp.status, resp.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "leadgen.py"), *args], capture_output=True, text=True).stdout

    def test_cli_add_dedupes_and_lists(self):
        self.assertIn("added", self.cli("add", "--name", "Cli Co", "--url", "https://cli.example"))
        self.assertIn("exists", self.cli("add", "--name", "Cli Co", "--url", "https://cli.example"))
        self.assertIn("https://cli.example", self.cli("list", "new"))

    def test_pages_render(self):
        for path in ("/", "/leads", "/clients", "/claude", "/leads?status=won"):
            self.assertEqual(self.req(path, origin=None)[0], 200, path)
        self.assertEqual(self.req("/lead/99999", origin=None)[0], 404)

    def test_lead_lifecycle(self):
        self.assertEqual(self.req("/lead", {"name": "Acme", "url": "https://acme.example", "contact": "a@acme.example"})[0], 303)
        lid = leadgen.q("SELECT id FROM leads WHERE url='https://acme.example'")[0]["id"]
        code, _ = self.req("/lead", {"id": lid, "name": "Acme", "url": "https://acme.example", "contact": "a@acme.example",
                                     "status": "won", "value": "800", "paid": "400", "check": ["0", "3"],
                                     "pitch": "Subject: Hello there\n\nBody"})
        self.assertEqual(code, 303)
        r = leadgen.q("SELECT * FROM leads WHERE id=?", (lid,))[0]
        self.assertEqual((r["status"], r["value"], r["paid"], r["checklist"]), ("won", 800, 400, "0,3"))
        page = self.req(f"/lead/{lid}", origin=None)[1]
        self.assertIn("mailto:a%40acme.example?subject=Hello%20there", page)
        self.assertIn("2/7", self.req("/clients", origin=None)[1])

    def test_duplicate_url_rejected(self):
        self.req("/lead", {"name": "Dup", "url": "https://dup.example"})
        self.assertEqual(self.req("/lead", {"name": "Dup", "url": "https://dup.example"})[0], 409)

    def test_cross_site_and_rebinding_blocked(self):
        self.assertEqual(self.req("/job/run", {"id": 1}, origin="https://evil.example")[0], 403)
        self.assertEqual(self.req("/", origin=None, host="evil.example")[0], 403)

    def test_html_is_escaped(self):
        self.req("/lead", {"name": "<script>x</script>", "url": "https://xss.example"})
        self.assertNotIn("<script>x</script>", self.req("/leads", origin=None)[1])

    def test_javascript_url_never_linked(self):
        self.req("/lead", {"name": "Js", "url": "javascript:alert(1)"})
        lid = leadgen.q("SELECT id FROM leads WHERE name='Js'")[0]["id"]
        page = self.req(f"/lead/{lid}", origin=None)[1]
        self.assertNotRegex(page, r"href=[\"']javascript:")

    def test_missing_claude_is_recorded_not_fatal(self):
        status, out = leadgen.claude("hi", [])
        self.assertEqual(status, "error")
        self.assertIn("no-such-claude", out)

    def test_claude_runs_only_get_their_tools(self):
        seen = []
        real, leadgen.subprocess.run = leadgen.subprocess.run, lambda cmd, **kw: seen.append(cmd) or subprocess.CompletedProcess(cmd, 0, "", "")
        try:
            leadgen.claude("hi", leadgen.JOB_TOOLS)
            leadgen.claude("hi", [])
        finally:
            leadgen.subprocess.run = real
        job, pitch = seen
        self.assertIn("--safe-mode", job)
        self.assertEqual(job[job.index("--tools") + 1], "WebSearch,WebFetch,Bash")
        self.assertEqual(pitch[pitch.index("--tools") + 1], "")


if __name__ == "__main__":
    unittest.main()
