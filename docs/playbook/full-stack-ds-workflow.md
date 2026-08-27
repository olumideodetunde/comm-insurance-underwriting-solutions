# Full-stack data scientist workflow

This is the day-to-day workflow the M0 engineering scaffold (`Makefile`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`) is built for, mapped to the actual files in this repo.

## 1. One-time setup

```bash
git clone https://github.com/olumideodetunde/comm-insurance-underwriting-solutions.git
cd comm-insurance-underwriting-solutions
pip install uv
make install          # uv sync inside project/, creates project/.venv
cd project && uv run pre-commit install   # hooks run automatically on every commit
databricks auth login --host https://dbc-07bd4965-8a3a.cloud.databricks.com   # once, for bundle deploy/run
```

## 2. Explore the data first

Exploration and production code are deliberately separated (`project/src/project_etl/README.md` spells this out):
- Ad-hoc EDA goes in `project/src/project_etl/explorations/` (e.g. `sample_exploration.ipynb`). Open it in the Databricks workspace or run it locally against a real cluster via Databricks Connect (`uv run jupyter` picks up the `spark` fixture pattern from `conftest.py`).
- Nothing you write here is tested or deployed - it's throwaway/investigative.

## 3. Write a transformation

Once you know what a dataset should look like, add a file under `project/src/project_etl/transformations/` - one dataset per file, decorated with `@dp.table` (Lakeflow Declarative Pipelines syntax, `sample_trips_project.py` is the template to copy). `spark` and `dbutils` are injected by the pipeline runtime, not imported - that's why `pyproject.toml` lists them as ruff `builtins` instead of flagging them as undefined.

Preview a single transformation without deploying the whole pipeline:

```bash
databricks bundle run project_etl --refresh sample_trips_project
```

## 4. Write the test alongside it

Add a test in `project/tests/`. Two flavors:
- **Pure logic** (parsing, feature math, config validation) -> plain pytest, like `tests/test_smoke.py`. No cluster needed.
- **Anything that touches Spark** -> request the `spark` fixture from `conftest.py`. It lazily opens a Databricks Connect session only when a test actually asks for it, so it doesn't block the rest of the suite when you're offline.

## 5. Run the local gate before committing

```bash
make lint      # ruff check
make format    # ruff format
make test      # pytest, with coverage
```

`git commit` runs the same lint/format + the fast smoke test automatically via pre-commit (`.pre-commit-config.yaml`) - it fails fast on staged files if something's off, before you even push.

## 6. Push and open a PR

CI (`.github/workflows/ci.yml`) reruns `uv run ruff check` + `uv run pytest` on every PR into `main` - this is the merge gate. A separate `validate-bundle` job runs `databricks bundle validate` too, once `DATABRICKS_HOST`/`DATABRICKS_TOKEN` are configured as repo variables/secrets.

## 7. Deploy to your personal dev workspace

```bash
databricks bundle deploy -t dev
```

`databricks.yml`'s `dev` target uses `mode: development`, so everything gets prefixed `[dev your_username]` and job schedules are paused - safe to iterate against without touching anyone else's resources or prod data.

## 8. Wire it into a job (orchestration)

`resources/sample_job.job.yml` shows the pattern: a scheduled job that chains a notebook task -> the `project` wheel's `main` entry point -> a `refresh_pipeline` task that reruns `project_etl`. This is where model training/scoring steps get hung once modeling work starts (see `docs/roadmap/Underwriting Quadrant Roadmap.html`).

## 9. Ship to prod

Merge to `main` -> CI's `deploy` job runs `databricks bundle deploy -t prod` automatically (gated the same way, on `DATABRICKS_HOST` being set). `prod` in `databricks.yml` pins a single deploy location and `mode: production`, so nothing gets duplicated per-user.