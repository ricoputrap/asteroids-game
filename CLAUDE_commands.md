# Commands

```bash
# Run game
uv run main.py

# Run tests
uv run pytest

# Run single test
uv run pytest tests/test_game.py::TestAsteroidSplit::test_split_produces_two_children

# Lint
uv run ruff check .
uv run ruff format .
```
