# Changelog

All notable changes to this project are listed here, following [Keep a Changelog](https://keepachangelog.com/). The project is a **prototype**;
versions below 1.0 may change the data model without migration.

## [0.2.0] - 2026-10-09

### Changed
- **Relicensed under the MIT License** (was a custom source-available license). The project is now open source.

### Added
- Code of Conduct, pull request template, expanded contributing guide.

## [0.1.1] - 2026-10-09

### Security
- Lead website links are only rendered as links when they use `http`/`https`. A `javascript:` URL
  saved by a lead-search job could otherwise run script on the dashboard when clicked.

### Fixed
- Phone-width layout: the top navigation no longer stretches to fill the screen, and the leads
  table scrolls inside its card instead of overflowing the page.
- A job that has never run shows "never" instead of "never · -".

## [0.1.0] - 2026-10-09

### Added
- Local web dashboard: pipeline board, leads table, clients page, Claude page.
- Scheduled lead-search jobs that run Claude Code headless with a restricted tool allow-list.
- Per-lead Claude steps: site research, pitch email, onboarding email, project brief.
- Delivery checklist, price / paid / deadline tracking, `mailto:` drafts.
- `leadgen.py add` / `list` command line.
- `LEADGEN_DB`, `LEADGEN_CLAUDE`, `LEADGEN_MODEL` environment settings.
- CSRF and DNS-rebinding protection, test suite, CI.
