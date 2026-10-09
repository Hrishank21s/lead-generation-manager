# Security Policy

Lead Generation Manager is a **local, single-user prototype**. It is designed to run on your own
machine and is not meant to be exposed to a network.

## Built-in protections

- The server binds to `127.0.0.1` only.
- Requests whose `Host` or `Origin` header is not the local server are rejected (CSRF and
  DNS-rebinding protection), so other websites cannot trigger Claude runs.
- Every Claude run uses `claude -p --permission-mode default` with an explicit tool allow-list.
  Lead-search jobs may only search and fetch web pages and call `leadgen.py add` / `list`.
  Writing steps get no tools at all.
- The tool contains no email-sending code. You send every message yourself.
- All page output is HTML-escaped. Lead data stays in `data/` and is git-ignored.

## Known limits

- No authentication: anyone with access to your machine's localhost can use it.
- Text from websites and client replies is passed to Claude as data. Prompt injection is
  mitigated by the tool allow-list, not eliminated.

## Reporting a vulnerability

Please **do not** open a public issue. Use
[GitHub private vulnerability reporting](https://github.com/Hrishank21s/lead-generation-manager/security/advisories/new).
You will get a response within 7 days.
