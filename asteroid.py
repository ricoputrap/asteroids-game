from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import pygame
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        # kill itself and (probably) spawn smaller ones
        self.kill()

        # small asteroid disappears when destroyed
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # instantiate new smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # set the new direction for each smaller asteroids
        changed_direction_angle = random.uniform(20, 50)
        new_asteroid1.velocity = self.velocity.rotate(changed_direction_angle) * 1.2 # move faster
        new_asteroid2.velocity = self.velocity.rotate(-changed_direction_angle) * 1.2 # opposite




