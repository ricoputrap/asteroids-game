import atexit
import json
import math
from datetime import datetime

__all__ = ["log_state", "log_event"]

_FPS = 60
_MAX_SECONDS = 16
_SPRITE_SAMPLE_LIMIT = 10

_frame_count = 0
_start_time = datetime.now()
_ts = _start_time.strftime("%Y%m%d_%H%M%S")

_state_log_file = open(f"game_state_{_ts}.jsonl", "w")
_event_log_file = open(f"game_events_{_ts}.jsonl", "w")
atexit.register(_state_log_file.close)
atexit.register(_event_log_file.close)


def _sprite_info(sprite: object) -> dict:
    info: dict = {"type": sprite.__class__.__name__}
    if hasattr(sprite, "position"):
        info["pos"] = [round(sprite.position.x, 2), round(sprite.position.y, 2)]
    if hasattr(sprite, "velocity"):
        info["vel"] = [round(sprite.velocity.x, 2), round(sprite.velocity.y, 2)]
    if hasattr(sprite, "radius"):
        info["rad"] = sprite.radius
    if hasattr(sprite, "rotation"):
        info["rot"] = round(sprite.rotation, 2)
    return info


def _group_info(group) -> dict:
    sprites = [_sprite_info(s) for i, s in enumerate(group) if i < _SPRITE_SAMPLE_LIMIT]
    return {"count": len(group), "sprites": sprites}


def log_state(screen, player, asteroids, shots) -> None:
    global _frame_count

    if _frame_count > _FPS * _MAX_SECONDS:
        return

    _frame_count += 1
    if _frame_count % _FPS != 0:
        return

    now = datetime.now()
    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": list(screen.get_size()),
        "player": _sprite_info(player),
        "asteroids": _group_info(asteroids),
        "shots": _group_info(shots),
    }
    _state_log_file.write(json.dumps(entry) + "\n")
    _state_log_file.flush()


def log_event(event_type: str, **details) -> None:
    now = datetime.now()
    event = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }
    _event_log_file.write(json.dumps(event) + "\n")
    _event_log_file.flush()
