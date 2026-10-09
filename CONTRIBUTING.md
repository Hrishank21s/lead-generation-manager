# Contributing

Thanks for your interest! This project is **source-available** under a custom
[license](LICENSE): you may use it, but not redistribute it or publish modified versions.

## Welcome

- **Bug reports** and **feature requests** through [issues](https://github.com/Hrishank21s/lead-generation-manager/issues/new/choose).
- **Pull requests** for fixes. Please open an issue first for anything larger than a small fix.
  By submitting a contribution you agree to the contribution terms in Section 7 of the LICENSE.

## Ground rules for code

- Python standard library only - no third-party dependencies.
- Keep it one file (`leadgen.py`) unless there is a strong reason not to.
- Run the tests before opening a PR:

  ```bash
  python3 -m unittest discover tests -v
  ```

- Never commit `data/` or any real lead data, and remove personal data from screenshots and logs.
