import pygame
import pytest

from asteroid import Asteroid
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_SPEED_MULTIPLIER


@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


class ConcreteShape(CircleShape):
    def draw(self, screen):
        pass

    def update(self, dt):
        pass


class TestCollidesWith:
    def test_overlapping(self):
        a = ConcreteShape(0, 0, 10)
        b = ConcreteShape(5, 0, 10)
        assert a.collides_with(b)

    def test_touching(self):
        a = ConcreteShape(0, 0, 10)
        b = ConcreteShape(20, 0, 10)
        assert a.collides_with(b)

    def test_separate(self):
        a = ConcreteShape(0, 0, 10)
        b = ConcreteShape(30, 0, 10)
        assert not a.collides_with(b)


class TestAsteroidSplit:
    def setup_method(self):
        self.group = pygame.sprite.Group()
        Asteroid.containers = self.group

    def test_split_produces_two_children(self):
        radius = ASTEROID_MIN_RADIUS * 2
        a = Asteroid(0, 0, radius)
        a.velocity = pygame.Vector2(100, 0)
        a.split()
        assert len(self.group) == 2

    def test_split_child_radius(self):
        radius = ASTEROID_MIN_RADIUS * 2
        a = Asteroid(0, 0, radius)
        a.velocity = pygame.Vector2(100, 0)
        a.split()
        for child in self.group:
            assert child.radius == radius - ASTEROID_MIN_RADIUS

    def test_split_speed_increase(self):
        radius = ASTEROID_MIN_RADIUS * 2
        a = Asteroid(0, 0, radius)
        a.velocity = pygame.Vector2(100, 0)
        original_speed = a.velocity.length()
        a.split()
        for child in self.group:
            expected = original_speed * ASTEROID_SPLIT_SPEED_MULTIPLIER
            assert abs(child.velocity.length() - expected) < 0.01

    def test_small_asteroid_no_children(self):
        a = Asteroid(0, 0, ASTEROID_MIN_RADIUS)
        a.velocity = pygame.Vector2(100, 0)
        a.split()
        assert len(self.group) == 0
