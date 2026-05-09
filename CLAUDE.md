# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Before Starting Work

**Always ask clarifying questions until you fully understand what's needed.** Do not make assumptions about requirements, scope, or approach. Ask specifically about:
- What problem are you solving?
- What should the outcome look like?
- Are there edge cases or constraints?
- What's the priority or deadline?

Only proceed once you have concrete answers.

## Commands

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

## Architecture

Sprite groups are the core coordination mechanism — all game objects register into groups at construction via `containers` tuple set before instantiation:

- `updatable` — receives `update(dt)` each frame
- `drawable` — receives `draw(screen)` each frame
- `asteroids` — collision targets for shots and player
- `shots` — projectiles checked against asteroids

`CircleShape` is the base class for all game objects. Collision = distance check against summed radii. `Player`, `Asteroid`, `Shot` all inherit from it and auto-register into `containers` on `__init__`.

`main.py` owns the game loop: handle events → update → check collisions → render → tick. `AsteroidField` spawns asteroids on a timer from screen edges; it's updatable-only (no draw).

All tunable values (speeds, radii, cooldowns, spawn rates) live in `constants.py`.

## Logging

`logger.py` writes two JSONL files per run:
- `game_state.jsonl` — position/velocity/radius snapshots (first 16s, 1/sec), uses `inspect.currentframe()` to read caller locals
- `game_events.jsonl` — discrete events: `player_hit`, `asteroid_shot`, `asteroid_split`

Both overwritten on each run. Timestamped copies also saved (e.g. `game_state_20260509_120036.jsonl`).

## Testing

Tests require `pygame.init()` before instantiating any sprite. The `pygame_init` fixture handles this with `autouse=True`. When adding sprites in tests, set `ClassName.containers` to a group before instantiation.
