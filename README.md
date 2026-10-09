# Lead Manager

> [!WARNING]
> **Prototype, not a finished product.** This is an early working prototype built for one person's
> freelance web-dev pipeline. It runs only on your own machine, has no login, no test suite, and
> the data model may change without migration. Use it to try the idea, not to run a business on yet.

A local CRM where **Claude finds, researches, pitches and onboards clients - and you build.**

It is one Python file (`tools/crm.py`, standard library only) that serves a dashboard on
`http://127.0.0.1:8765` and runs [Claude Code](https://claude.com/claude-code) in headless mode
(`claude -p`) for the research and writing work.

![Dashboard](docs/dashboard.png)

## How it works

```
 Claude (scheduled job)        Claude (one click per lead)                      You
 ──────────────────────        ───────────────────────────────────────────      ─────────────────
 search the web for     ──▶    1 research their site  ──▶  2 draft pitch   ──▶  review + send it
 businesses with weak          (problems, fit, contact)    email                from your mail app
 websites, save leads                                                                  │
                                                                                client says yes
                                                                                       ▼
                               3 draft onboarding email  ◀──────────────────── mark "replied"
                                 (asks for requirements)  ──▶ you send it ──▶  client answers
                                                                                       │
                               5 write project brief  ◀── 4 you paste answers ◀────────┘
                                 (pages, features, assets,
                                  timeline, open questions)  ──▶  you build + deliver
```

The split is deliberate: **Claude does the searching, research and writing. It never contacts
anyone.** Every email opens in your own mail app (a `mailto:` link) so you read and send each one
yourself.

## Requirements

- macOS or Linux, **Python 3.11+** with SQLite 3.35+ (standard library only, nothing to `pip install`)
- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed and logged in - the `claude`
  command must work in your terminal. Claude runs use your own Claude plan / API usage.

## Quick start

```bash
git clone https://github.com/Hrishank21s/lead-manager.git
cd lead-manager
python3 tools/crm.py serve          # then open http://127.0.0.1:8765
```

On first start it creates `data/crm.db` (git-ignored) with default instructions and one disabled
lead-search job. The server must stay running for scheduled jobs to fire. Use another port with
`python3 tools/crm.py serve 9000`.

## Using it

### 1. Set your standing instructions (Claude page)

These are added to **every** task Claude runs. Say what you sell, who you target, what a good lead
looks like, and how to sign emails. The default:

> We sell website rebuilds ($600-900, 5 days) to small businesses and indie SaaS whose site is
> weak (slow, broken on mobile, dated, unclear offer). A good lead: real business, public site with
> visible problems, a findable contact. Skip big companies and agencies.

Change the price, the niche (e.g. "dentists in Pune"), and add your name - pitches are signed
`[Your name]` until you do.

### 2. Find leads (Claude page → jobs)

A job is a plain-English task plus an interval in hours. The built-in one is
*"Find 5 new leads matching the instructions"*, every 24 h, **off by default**.

- **Run now** runs it once. A run takes a few minutes; results show in *Run history*.
- **Run on schedule** makes it repeat while the server is up.
- Add more jobs for other niches or cities.

Jobs check the existing list first and skip duplicate URLs.

![Claude page](docs/claude.png)

### 3. Work a lead (lead page)

Open any lead. The right side is Claude's work, in order:

| Step | Button | What Claude writes |
|---|---|---|
| 1 Research | *Research their site* | What they sell, 3 concrete site problems with evidence, best contact, fit score 1-5 |
| 2 Pitch email | *Draft pitch* | A short personal email quoting those problems and offering a free homepage mockup |
| 3 Onboarding email | *Draft onboarding email* | Questions for goals, pages, copy, brand assets, reference sites, features, hosting, deadline, deposit |
| 4 Client's answers | *(you paste their reply)* | - |
| 5 Project brief | *Write project brief* | Pages and sections, features, assets have/missing, design direction, timeline, price, open questions |

Every field is editable. A button saves the page first, then starts Claude; the page refreshes on
its own until the result lands. **Open in mail** appears once there is a draft and an email contact.

![Lead page](docs/lead.png)

### 4. Move it through the pipeline

Set the status as things happen:
`new → qualified → mockup → pitched → replied → won → delivered` (or `lost`).

Leads at *replied*, *won* or *delivered* appear on the **Clients** page with the 7-step delivery
checklist (questionnaire sent → requirements received → brief approved → deposit paid → build
started → delivered → final payment), price, amount paid and deadline.

![Clients page](docs/clients.png)

The **Dashboard** shows the pipeline board, leads, pitched, reply rate, active clients, money booked
and money collected.

## Command line

Claude's jobs use these, and you can too:

```bash
python3 tools/crm.py add --name "Harbor Cafe" --url https://harbor-cafe.example \
    --contact hello@harbor-cafe.example --source manual --notes "menu is a PDF"
python3 tools/crm.py list            # all leads, tab-separated
python3 tools/crm.py list pitched    # one status
```

## Safety model

- **Claude's tools are locked down.** Every run is `claude -p --permission-mode default` with an
  explicit allow-list: lead-search jobs get web search, web fetch and `crm.py add/list` only;
  research gets web search + fetch; writing steps get no tools. Anything else is refused.
- **Nothing is sent automatically.** There is no mail code in this tool. You send every email.
- **Local only.** The server binds to `127.0.0.1`, and rejects requests whose `Host` or `Origin`
  is not this server, so other websites can't trigger Claude runs (CSRF / DNS rebinding).
- **Web content is treated as data.** Lead info and client replies are passed to Claude labelled as
  information, never instructions - but this is a prompt, not a guarantee, which is one more reason
  the tools are restricted.
- **Your data stays on disk** in `data/crm.db` and is git-ignored, since it holds people's emails.

## Known limitations (it's a prototype)

- Schedules are "every N hours", not fixed times; jobs only run while the server is up.
- Single user, no login - do not expose the port to a network.
- No client-facing intake form (that would need public hosting); you paste client replies in.
- No email sending, inbox sync or reply detection - status is updated by hand.
- Duplicate check is an exact URL match (`https://x.com` and `https://x.com/` count as two).
- No automated test suite yet; checked by hand against a live server.

## Roadmap ideas

Fixed-time schedules · inbox sync to auto-detect replies · client intake form · invoice/payment
links · export to CSV · per-niche instruction presets.
