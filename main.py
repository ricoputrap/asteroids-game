import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def check_collisions(
    player: Player,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
) -> bool:
    for asteroid in list(asteroids):
        if asteroid.collides_with(player):
            log_event("player_hit")
            return True
        for shot in list(shots):
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                shot.kill()
                asteroid.split()
    return False


def render(screen: pygame.Surface, drawable: pygame.sprite.Group) -> None:
    screen.fill("black")
    for item in drawable:
        item.draw(screen)
    pygame.display.flip()


def main() -> None:
    pygame.init()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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

    while True:
        log_state(screen, player, asteroids, shots)

        if not handle_events():
            return

        updatable.update(dt)

        if check_collisions(player, asteroids, shots):
            print("Game over!")
            return

        render(screen, drawable)
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
