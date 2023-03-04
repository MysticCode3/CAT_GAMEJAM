import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed, damage=1):
        self.x = x
        self.y = y
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed * 2
        self.timer = 5 # time in seconds
        self.gravity = 350
        self.damage = 1

    def rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)

    def update(self, floors, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dy += self.gravity * dt
        self.timer -= dt
        for floor in floors:
            if self.rect().colliderect(floor.rect()):
                self.dy *= -0.9
