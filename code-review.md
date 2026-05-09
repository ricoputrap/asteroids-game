# Code Review

Code-quality issues, bugs, and refactoring opportunities. Severity tags: 🔴 bug, 🟡 smell, 🟢 nice-to-have.

## Bugs

### 🔴 `main.py:28` — `AsteroidField.containers` is not a tuple
```python
AsteroidField.containers = (updatable)
```
`(updatable)` is just `updatable` in parentheses — not a 1-tuple. Compare with the other lines, which are real tuples. It happens to work because pygame's `Sprite.__init__` accepts either a single `Group` or an iterable of groups, but the inconsistency is a footgun. Fix:
```python
AsteroidField.containers = (updatable,)
```

### 🔴 `player.py:65` — `Shot` constructed with `Vector2` instead of `x, y` floats
```python
shot = Shot(self.position, self.position)
```
`Shot.__init__(self, x, y)` then calls `super().__init__(x, y, SHOT_RADIUS)`, which calls `pygame.Vector2(x, y)`. Passing two `Vector2` objects here is a type misuse — pygame may silently coerce or raise depending on version. Should be:
```python
shot = Shot(self.position.x, self.position.y)
```
Also: the shot spawns at the ship's *center*, not the nose of the triangle. Spawning at the nose looks better:
```python
nose = self.position + pygame.Vector2(0, 1).rotate(self.rotation) * self.radius
shot = Shot(nose.x, nose.y)
```

### 🔴 `main.py:31` — typo `asterodid_field`
Currently unreferenced, so it doesn't break anything, but rename to `asteroid_field` before it spreads.

### 🟡 `main.py:51` — `sys.exit()` from inside the game loop
Hard exit on player death prevents cleanup (logs flushed via context manager, fine here, but generally bad). Returning from `main()` and breaking the loop is cleaner and enables a future game-over screen.

## Code Smells

### 🟡 `asteroidfield.py:4` — `from constants import *`
Wildcard imports obscure dependencies and break tooling (linters, IDE jump-to-def). Import the names explicitly:
```python
from constants import (
    ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS, ASTEROID_KINDS,
    ASTEROID_SPAWN_RATE_SECONDS, SCREEN_HEIGHT, SCREEN_WIDTH,
)
```

### 🟡 `main.py` — main loop does too much
The `while True` block mixes input, update, collision, and render. Extract:
- `handle_events()` → returns `running: bool`
- `check_collisions(player, asteroids, shots)` → returns event list
- `render(screen, drawable)`

Easier to test, easier to add pause/menu states later.

### 🟡 `asteroid.py:28-35` — magic numbers in `split()`
```python
new_radius = self.radius - ASTEROID_MIN_RADIUS
changed_direction_angle = random.uniform(20, 50)
new_asteroid1.velocity = self.velocity.rotate(changed_direction_angle) * 1.2
```
The split-angle range and `1.2` speed multiplier should live in `constants.py` (e.g. `ASTEROID_SPLIT_ANGLE_MIN`, `ASTEROID_SPLIT_ANGLE_MAX`, `ASTEROID_SPLIT_SPEED_MULTIPLIER`).

### 🟡 `player.py:54-58` — `move()` arithmetic split across three lines
```python
unit_vector = pygame.Vector2(0, 1)
rotated_vector = unit_vector.rotate(self.rotation)
rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
self.position += rotated_with_speed_vector
```
One line is clearer:
```python
self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt
```
Or even better, share a `forward_vector()` helper with `triangle()` and `shoot()` which all compute the same thing.

### 🟡 `circleshape.py:20-22` — `update()` should raise, not pass
```python
def update(self, dt):
    # must override
    pass
```
A subclass that forgets to override silently does nothing. Use `raise NotImplementedError` (or make `CircleShape` an `abc.ABC`).

### 🟡 `logger.py` — frame introspection is fragile
`log_state()` walks `frame.f_back.f_locals` to discover state. This breaks the moment you refactor `main()` (e.g. extracting helpers — locals disappear). It's also implicit: nothing in `main.py` says what gets logged. Pass state explicitly:
```python
log_state(screen, player, asteroids, shots, ...)
```

### 🟡 `logger.py:111` — file opened on every snapshot
Each call opens, writes, closes the file. Fine at 1Hz, but consider a single open file handle (or the `logging` module) if log frequency increases.

### 🟢 `logger.py` — log files overwritten each run
`mode = "w" if not _state_log_initialized else "a"` resets logs at process start. For replay-from-logs (see feature list), prefer timestamped filenames: `game_state_{ts}.jsonl`.

### 🟢 `pyproject.toml:4` — placeholder description
`description = "Add your description here"` — fill it in.

## Architecture / Design

### 🟢 No tests
Pure functions are easy to unit-test: `CircleShape.collides_with`, asteroid split math, vector math. Add `pytest` to `pyproject.toml` and start with a `tests/` directory.

### 🟢 No type hints
The codebase is small enough that hints would meaningfully document intent (`def update(self, dt: float) -> None`, `def collides_with(self, other: "CircleShape") -> bool`). Pair with `mypy` or `pyright` in CI.

### 🟢 No linter / formatter config
Add `ruff` (lint + format) to `pyproject.toml`. Catches the wildcard import, unused variables, etc., automatically.

### 🟢 `containers` class-attribute pattern
Setting `Player.containers = (...)` from outside the class works but is implicit and hard to follow. An alternative is to pass groups into the constructor, but the current pattern is idiomatic for small pygame projects — acceptable. Document it in `circleshape.py` so newcomers understand the magic.

### 🟢 Collision loop is O(asteroids × shots)
Fine at current scale. If asteroid + shot counts grow, look at `pygame.sprite.groupcollide(asteroids, shots, False, True, collided=...)` with a custom `collided` callback using the existing radius logic.

## Suggested Refactor Order

1. Fix the two 🔴 bugs (containers tuple, Shot constructor).
2. Extract `handle_events`, `check_collisions`, `render` from `main.py`.
3. Replace `from constants import *` with explicit imports.
4. Move asteroid-split magic numbers to `constants.py`.
5. Add `ruff` + a basic `tests/` directory.
6. Make logger explicit (drop frame introspection).
