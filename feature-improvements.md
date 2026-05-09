# Feature Improvements

Gameplay and UX features the game is currently missing. Ordered roughly from highest to lowest impact.

## Core Gameplay

### 1. Score system
Track points per asteroid destroyed (more points for smaller asteroids since they're harder to hit). Render the score in the top-left corner with `pygame.font`. Persist a high score to a local JSON file.

### 2. Lives & game-over screen
Currently a single collision calls `sys.exit()`. Replace with:
- Player starts with 3 lives.
- On hit: brief invulnerability window, respawn at center, play a hit effect.
- Game-over screen with final score, "Press R to restart / Q to quit".

### 3. Screen wraparound
The player can sail off-screen indefinitely. Asteroids and the ship should wrap edges (classic Asteroids behavior). Shots should despawn at the edge or after a max lifetime.

### 4. Shot lifetime
Bullets currently fly forever. Add a `lifetime` field (e.g. 1.0 second) and `kill()` when expired. Caps simultaneous shots and matches arcade feel.

### 5. Thrust physics (momentum)
`W`/`S` currently set position directly via velocity-like math but drop momentum the instant the key releases. Replace with acceleration: `W` adds to `velocity`, no key = drift. Add a small drag coefficient. Feels much more like the original.

### 6. Levels / waves
Increase `ASTEROID_SPAWN_RATE_SECONDS` difficulty over time, or spawn waves: clear all asteroids → short pause → next wave with N+1 starting asteroids.

## Visuals & Feel

### 7. Polygon asteroids
Asteroids are currently outlined circles. Generate an irregular polygon per asteroid (random radii around N vertices) for visual variety.

### 8. Particle effects
- Explosion particles on asteroid destruction.
- Thrust flame triangle behind the ship while `W` is held.
- Brief flash + debris on player death.

### 9. Sound
- Shot fire SFX
- Asteroid hit/split SFX
- Player death SFX
- Optional ambient music

### 10. Screen shake
Small camera shake on player death and large-asteroid destruction. Cheap to implement, big payoff.

### 11. HUD
Score (top-left), lives (top-right, drawn as small ship icons), wave number (top-center).

## Meta & Polish

### 12. Pause menu
`Esc` toggles pause. Show "PAUSED — press Esc to resume / Q to quit".

### 13. Main menu
Title screen on launch with "Start", "High Scores", "Quit". Avoids the game starting in media res.

### 14. Configurable controls
Let players remap keys via a settings file rather than hardcoded `K_w`/`K_a`/`K_s`/`K_d`.

### 15. Power-ups
Occasional drops from destroyed asteroids: rapid fire, triple shot, shield, slow-motion.

### 16. UFO / enemy ship
Periodic enemy that crosses the screen and shoots back. Classic Asteroids feature.

### 17. Hyperspace
Panic button (e.g. `Shift`) that teleports the player to a random location. Small risk of self-destruction. Adds a strategic layer.

## Quality-of-Life

### 18. Restart without quitting
Currently the only way to retry is to relaunch. Tied to the game-over screen item above.

### 19. FPS / debug overlay
Toggleable overlay (`F3`?) showing FPS, sprite counts, and player position. Useful for tuning.

### 20. Replay from logs
The logger already writes JSONL state snapshots. A small `replay.py` could read them and re-render the run. Cool feature for sharing best runs.
