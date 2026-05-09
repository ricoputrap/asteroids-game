import json
import os
import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    HIGH_SCORE_PATH,
    SCORE_LARGE,
    SCORE_MEDIUM,
    SCORE_SMALL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from player import Player
from shot import Shot

_RADIUS_TO_SCORE = {
    ASTEROID_MIN_RADIUS: SCORE_SMALL,
    ASTEROID_MIN_RADIUS * 2: SCORE_MEDIUM,
    ASTEROID_MIN_RADIUS * 3: SCORE_LARGE,
}


def load_high_score() -> int:
    try:
        with open(HIGH_SCORE_PATH) as f:
            return json.load(f)["high_score"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return 0


def save_high_score(score: int) -> None:
    os.makedirs(os.path.dirname(HIGH_SCORE_PATH), exist_ok=True)
    with open(HIGH_SCORE_PATH, "w") as f:
        json.dump({"high_score": score}, f)


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def check_collisions(
    player: Player,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
) -> tuple[bool, int]:
    points_earned = 0
    for asteroid in list(asteroids):
        if asteroid.collides_with(player):
            log_event("player_hit")
            return True, points_earned
        for shot in list(shots):
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                shot.kill()
                points_earned += _RADIUS_TO_SCORE.get(asteroid.radius, 0)
                asteroid.split()
    return False, points_earned


def render(
    screen: pygame.Surface,
    drawable: pygame.sprite.Group,
    font: pygame.font.Font,
    score: int,
    high_score: int,
) -> None:
    screen.fill("black")
    for item in drawable:
        item.draw(screen)
    score_surf = font.render(f"SCORE: {score}", True, "white")
    screen.blit(score_surf, (10, 10))
    best_surf = font.render(f"BEST: {high_score}", True, "white")
    screen.blit(best_surf, (SCREEN_WIDTH - best_surf.get_width() - 10, 10))
    pygame.display.flip()


def main() -> None:
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    score = 0
    high_score = load_high_score()

    while True:
        log_state(screen, player, asteroids, shots)

        if not handle_events():
            save_high_score(max(score, high_score))
            return

        updatable.update(dt)

        game_over, points = check_collisions(player, asteroids, shots)
        score += points
        if score > high_score:
            high_score = score

        if game_over:
            save_high_score(high_score)
            print(f"Game over! Score: {score}")
            return

        render(screen, drawable, font, score, high_score)
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
