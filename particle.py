import math
import random

import pygame

from constants import PARTICLE_LENGTH, PARTICLE_LIFETIME, PARTICLE_SPEED


class Particle(pygame.sprite.Sprite):
    containers: tuple

    def __init__(self, x: float, y: float) -> None:
        super().__init__(self.containers)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * PARTICLE_SPEED
        self.position = pygame.Vector2(x, y)
        self.lifetime = PARTICLE_LIFETIME

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        ratio = max(0.0, self.lifetime / PARTICLE_LIFETIME)
        grey = int(255 * ratio)
        end = self.position + self.velocity.normalize() * PARTICLE_LENGTH
        pygame.draw.line(
            screen,
            (grey, grey, grey),
            (int(self.position.x), int(self.position.y)),
            (int(end.x), int(end.y)),
            2,
        )
