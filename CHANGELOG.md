# Changelog

All notable changes to this project are listed here. The project is a **prototype**;
versions below 1.0 may change the data model without migration.

## [0.1.0] - 2026-10-09

### Added
- Local web dashboard: pipeline board, leads table, clients page, Claude page.
- Scheduled lead-search jobs that run Claude Code headless with a restricted tool allow-list.
- Per-lead Claude steps: site research, pitch email, onboarding email, project brief.
- Delivery checklist, price / paid / deadline tracking, `mailto:` drafts.
- `leadgen.py add` / `list` command line.
- `LEADGEN_DB`, `LEADGEN_CLAUDE`, `LEADGEN_MODEL` environment settings.
- CSRF and DNS-rebinding protection, test suite, CI.
