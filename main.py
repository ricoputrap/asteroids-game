import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
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
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asterodid_field = AsteroidField()
    

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)

        for asteroid in asteroids:
            is_colliding_with_player = asteroid.collides_with(player)

            if is_colliding_with_player:
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for shot in shots:
                is_asteroid_shot = asteroid.collides_with(shot)

                if is_asteroid_shot:
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.kill()


        for drawable_item in drawable:
            drawable_item.draw(screen)
        
        pygame.display.flip()

        # pause the game loop until 1/60th of a second has passed
        dt = clock.tick(60) / 1000 # ms to second


if __name__ == "__main__":
    main()
