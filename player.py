import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_BLINK_RATE,
    PLAYER_INVULNERABILITY_DURATION,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.invulnerable: float = 0.0
        self._blink_timer: float = 0.0
        self._visible: bool = True

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if self._visible:
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def respawn(self, x: float, y: float) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable = PLAYER_INVULNERABILITY_DURATION
        self._blink_timer = PLAYER_BLINK_RATE
        self._visible = True

    def update(self, dt: float) -> None:
        if self.invulnerable > 0:
            self.invulnerable -= dt
            self._blink_timer -= dt
            if self._blink_timer <= 0:
                self._visible = not self._visible
                self._blink_timer = PLAYER_BLINK_RATE
            if self.invulnerable <= 0:
                self._visible = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.cooldown -= dt

    def move(self, dt: float) -> None:
        self.position += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SPEED * dt

    def shoot(self) -> None:
        if self.cooldown > 0:
            return

        nose = self.position + pygame.Vector2(0, 1).rotate(self.rotation) * self.radius
        shot = Shot(nose.x, nose.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
