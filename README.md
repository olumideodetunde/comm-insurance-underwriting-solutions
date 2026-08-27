# comm-insurance-underwriting-solutions

Databricks-native commercial insurance underwriting and pricing solutions.
This repo hosts a [Databricks Asset Bundle](https://docs.databricks.com/dev-tools/bundles/index.html) project under `project/`.

## Setup

Requires Python (see `project/pyproject.toml` for the supported range) and [uv](https://docs.astral.sh/uv/).

```bash
pip install uv
make install
```

This runs `uv sync` inside `project/`, creating a `.venv` with all runtime and dev dependencies.

## Development

| Command | What it does |
|---|---|
| `make install` | Sync the environment (`uv sync`) |
| `make lint` | Run `ruff check` |
| `make format` | Run `ruff format` |
| `make test` | Run `pytest` (with coverage) |

Run any tool directly with `uv run <command>` from `project/` if you'd rather not go through `make`.

### Pre-commit hooks

This repo uses [pre-commit](https://pre-commit.com/) to run lint, format, and a smoke test before each commit.

```bash
cd project && uv run pre-commit install
```

After that, `git commit` automatically runs `ruff check --fix`, `ruff format`, and the smoke test suite (`project/tests/test_smoke.py`) against staged files.

## CI

`.github/workflows/ci.yml` runs `ruff check` and `pytest` on every pull request into `main` and blocks merge on failure. It also validates and deploys the Databricks bundle, but only once the `DATABRICKS_HOST` repo variable and `DATABRICKS_TOKEN` secret are configured.

## Tests

`project/tests/test_smoke.py` is a plain local test with no external dependencies. Tests that need a live Databricks cluster can request the `spark` fixture from `project/tests/conftest.py`, which connects lazily via Databricks Connect only when used.
