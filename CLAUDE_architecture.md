# Architecture

Sprite groups are the core coordination mechanism — all game objects register into groups at construction via `containers` tuple set before instantiation:

- `updatable` — receives `update(dt)` each frame
- `drawable` — receives `draw(screen)` each frame
- `asteroids` — collision targets for shots and player
- `shots` — projectiles checked against asteroids

`CircleShape` is the base class for all game objects. Collision = distance check against summed radii. `Player`, `Asteroid`, `Shot` all inherit from it and auto-register into `containers` on `__init__`.

`main.py` owns the game loop: handle events → update → check collisions → render → tick. `AsteroidField` spawns asteroids on a timer from screen edges; it's updatable-only (no draw).

All tunable values (speeds, radii, cooldowns, spawn rates) live in `constants.py`.
