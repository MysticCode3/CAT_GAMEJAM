import pygame
import math


class Bullet:
    def __init__(self, x, y, target_x, target_y, speed, damage=1):
        self.x = x
        self.y = y
        self.damage = damage
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.timer = 5  # time in seconds
        self.gravity = 350
        self.size = 16

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, floors, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dy += self.gravity * dt
        self.timer -= dt
        for floor in floors:
            if self.rect().colliderect(floor.rect()):
                self.dy *= -1.1
                self.dx *= 1.1
                if self.y > floor.rect().y:
                    self.y = floor.rect().y + floor.rect().h
                else:
                    self.y = floor.rect().y - self.size
