install:
	uv sync

run:
	uv run database

lint:
	uv run ruff check .
