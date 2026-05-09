import random

import pygame

from circleshape import CircleShape
from constants import (
    ASTEROID_MIN_RADIUS,
    ASTEROID_SPLIT_ANGLE_MAX,
    ASTEROID_SPLIT_ANGLE_MIN,
    ASTEROID_SPLIT_SPEED_MULTIPLIER,
    LINE_WIDTH,
)
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        angle = random.uniform(ASTEROID_SPLIT_ANGLE_MIN, ASTEROID_SPLIT_ANGLE_MAX)
        new_asteroid1.velocity = self.velocity.rotate(angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER
        new_asteroid2.velocity = self.velocity.rotate(-angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER
