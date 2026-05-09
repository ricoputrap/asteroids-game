# Asteroids Game

A Python implementation of the classic arcade game **Asteroids**, built with `pygame`. This project is part of the [Boot.dev](https://www.boot.dev/) curriculum and serves as an exercise in object-oriented design, the game loop pattern, and 2D vector math.

## Gameplay

You pilot a triangular spaceship in the middle of the screen. Asteroids spawn from the edges and drift toward you. Shoot them to break them apart — large asteroids split into two smaller, faster ones; the smallest disappear when hit. Collide with any asteroid and it's game over.

## Controls

| Key      | Action                |
| -------- | --------------------- |
| `W`      | Thrust forward        |
| `S`      | Thrust backward       |
| `A`      | Rotate left           |
| `D`      | Rotate right          |
| `Space`  | Shoot (rate-limited)  |

## Requirements

- Python `>=3.13`
- `pygame==2.6.1`
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

## Setup & Run

Using `uv`:

```bash
uv sync
uv run main.py
```

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pygame==2.6.1
python main.py
```

## Project Structure

```
asteroids-game/
├── main.py             # Entry point + main game loop
├── constants.py        # Tunable game parameters (speeds, sizes, cooldowns)
├── circleshape.py      # Base sprite class with circle-based collision
├── player.py           # Player ship: input handling, movement, shooting
├── asteroid.py         # Asteroid sprite + split-on-hit behavior
├── asteroidfield.py    # Spawns asteroids from screen edges on a timer
├── shot.py             # Projectile fired by the player
├── logger.py           # Periodic state snapshots + event logs (JSONL)
├── pyproject.toml      # Project metadata + dependencies
└── game_state.jsonl    # Auto-generated state log (overwritten each run)
└── game_events.jsonl   # Auto-generated event log (overwritten each run)
```

## Architecture

The game is built around **pygame sprite groups** for batch update + draw:

- `updatable` — every sprite that needs `update(dt)` called per frame
- `drawable` — every sprite that needs `draw(screen)` called per frame
- `asteroids` — collision target group
- `shots` — projectiles checked against asteroids

`CircleShape` is the shared base class; collision is a simple distance check against summed radii. `Player`, `Asteroid`, and `Shot` all inherit from it. Sprites are auto-registered into their `containers` tuple at construction time, so the main loop never needs to track them manually.

## Logging

`logger.py` writes two JSONL files for post-run inspection:

- **`game_state.jsonl`** — one snapshot per second (first 16 seconds), capturing all sprite groups, their counts, and per-sprite position/velocity/radius/rotation. Uses frame introspection (`inspect.currentframe()`) to discover state from the caller's locals.
- **`game_events.jsonl`** — discrete events: `player_hit`, `asteroid_shot`, `asteroid_split`.

Both files are overwritten on each run.

## Status

Functional but minimal. No score, no lives, no menu, no sound. See [`feature-improvements.md`](./feature-improvements.md) and [`code-review.md`](./code-review.md) for the roadmap.
