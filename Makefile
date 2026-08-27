.PHONY: install lint format test

install:
	cd project && uv sync

lint:
	cd project && uv run ruff check .

format:
	cd project && uv run ruff format .

test:
	cd project && uv run pytest
