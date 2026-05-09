import json
import os
import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    HIGH_SCORE_PATH,
    PARTICLE_COUNT,
    PLAYER_MAX_LIVES,
    SCORE_LARGE,
    SCORE_MEDIUM,
    SCORE_SMALL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from particle import Particle
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
    player_hit = False
    for asteroid in list(asteroids):
        if not player_hit and player.invulnerable <= 0 and asteroid.collides_with(player):
            log_event("player_hit")
            player_hit = True
            continue
        for shot in list(shots):
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                shot.kill()
                points_earned += _RADIUS_TO_SCORE.get(asteroid.radius, 0)
                asteroid.split()
                break
    return player_hit, points_earned


def render(
    screen: pygame.Surface,
    drawable: pygame.sprite.Group,
    font: pygame.font.Font,
    score: int,
    high_score: int,
    lives: int,
) -> None:
    screen.fill("black")
    for item in drawable:
        item.draw(screen)
    score_surf = font.render(f"SCORE: {score}", True, "white")
    screen.blit(score_surf, (10, 10))
    lives_surf = font.render(f"LIVES: {lives}", True, "white")
    lives_x = SCREEN_WIDTH - lives_surf.get_width() - 10
    screen.blit(lives_surf, (lives_x, 10))
    best_surf = font.render(f"BEST: {high_score}", True, "white")
    best_x = SCREEN_WIDTH - best_surf.get_width() - 10
    screen.blit(best_surf, (best_x, 10 + lives_surf.get_height() + 4))
    pygame.display.flip()


def render_game_over(
    screen: pygame.Surface,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    score: int,
    high_score: int,
) -> None:
    screen.fill("black")
    cx = SCREEN_WIDTH // 2
    cy = SCREEN_HEIGHT // 2

    title_surf = big_font.render("GAME OVER", True, "white")
    screen.blit(title_surf, (cx - title_surf.get_width() // 2, cy - 120))

    score_surf = font.render(f"SCORE: {score}", True, "white")
    screen.blit(score_surf, (cx - score_surf.get_width() // 2, cy - 20))

    best_surf = font.render(f"BEST: {high_score}", True, "white")
    screen.blit(best_surf, (cx - best_surf.get_width() // 2, cy + 20))

    hint_surf = font.render("R  restart     Q  quit", True, "white")
    screen.blit(hint_surf, (cx - hint_surf.get_width() // 2, cy + 80))

    pygame.display.flip()


def _reset_game(
    updatable: pygame.sprite.Group,
    drawable: pygame.sprite.Group,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    particles: pygame.sprite.Group,
) -> Player:
    for group in (updatable, drawable, asteroids, shots, particles):
        group.empty()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()
    return player


def main() -> None:
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    score = 0
    lives = PLAYER_MAX_LIVES
    high_score = load_high_score()
    showing_game_over = False

    while True:
        dt = clock.tick(60) / 1000

        if showing_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                    if event.key == pygame.K_r:
                        score = 0
                        lives = PLAYER_MAX_LIVES
                        showing_game_over = False
                        player = _reset_game(updatable, drawable, asteroids, shots, particles)
            render_game_over(screen, font, big_font, score, high_score)
            continue

        log_state(screen, player, asteroids, shots)

        if not handle_events():
            save_high_score(max(score, high_score))
            return

        updatable.update(dt)

        player_hit, points = check_collisions(player, asteroids, shots)
        score += points
        if score > high_score:
            high_score = score

        if player_hit:
            lives -= 1
            for _ in range(PARTICLE_COUNT):
                Particle(player.position.x, player.position.y)
            if lives > 0:
                player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            else:
                high_score = max(score, high_score)
                save_high_score(high_score)
                showing_game_over = True

        render(screen, drawable, font, score, high_score, lives)


if __name__ == "__main__":
    main()
