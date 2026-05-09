# Logging

`logger.py` writes two JSONL files per run:
- `game_state.jsonl` — position/velocity/radius snapshots (first 16s, 1/sec), uses `inspect.currentframe()` to read caller locals
- `game_events.jsonl` — discrete events: `player_hit`, `asteroid_shot`, `asteroid_split`

Both overwritten on each run. Timestamped copies also saved (e.g. `game_state_20260509_120036.jsonl`).
