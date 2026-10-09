# Contributing

Thanks for helping! Lead Generation Manager is open source under the [MIT License](LICENSE).
Bug reports, ideas, docs fixes and code are all welcome.

## Ways to help

- **Report a bug** or **request a feature** - [open an issue](https://github.com/Hrishank21s/lead-generation-manager/issues/new/choose).
- **Improve the docs** - typos, unclear steps, missing screenshots.
- **Send code** - look for issues labelled `good first issue` or `help wanted`.

## Development setup

No dependencies to install - only Python 3.11+.

```bash
git clone https://github.com/Hrishank21s/lead-generation-manager.git
cd lead-generation-manager
python3 leadgen.py serve                     # http://127.0.0.1:8765
python3 -m unittest discover tests -v        # run the tests (no AI calls)
```

To try the UI without spending AI credits, add leads by hand or with `python3 leadgen.py add`.
Use a throwaway database with `LEADGEN_DB=/tmp/dev.db`.

## Pull requests

1. Fork the repo and create a branch from `main`.
2. Keep the change focused; open an issue first for anything large.
3. Add or update a test in `tests/` when you change behaviour.
4. Make sure `python3 -m unittest discover tests -v` passes.
5. Add a line under **Unreleased** in [CHANGELOG.md](CHANGELOG.md).
6. Open the PR and fill in the template.

## Design rules

- **Standard library only.** No third-party packages.
- **One file.** `leadgen.py` holds the app; split only with a strong reason.
- **The AI never sends anything.** Don't add code that emails or messages people automatically.
- **Keep Claude locked down.** Any change to an `--allowedTools` list is a security change - explain it in the PR.
- **No real data.** Never commit `data/`, real leads or personal emails; screenshots use `.example` domains.

By contributing, you agree that your contributions are licensed under the MIT License and that you
follow the [Code of Conduct](CODE_OF_CONDUCT.md).
