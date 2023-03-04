import pygame
import math


class Cat:
    def __init__(self, pos, dimensions, vel):
        self.pos = pos
        self.dimensions = dimensions
        self.vel = vel
        self.xVel = 0
        self.yVel = 0
        self.isGrounded = False
        self.touchingFloor = 0
        self.jumpPower = 300

    def rect(self):
        return pygame.Rect(self.pos, self.dimensions)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def update(self, dt, floors):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.xVel -= self.vel * dt
            self.isGrounded = False

        # qwerty or dvorak
        if keys[pygame.K_d] or keys[pygame.K_e]:
            self.xVel += self.vel * dt
            self.isGrounded = False

        self.pos[0] += self.xVel * dt
        self.xVel *= math.pow(0.1, dt)
        if abs(self.xVel) < 10:
            self.xVel = 0
        else:
            self.isGrounded = False

        for floor in floors:
            if (floor.rect().colliderect(self.rect())
                and (self.pos[1] + self.dimensions[1]/2)
                <= (floor.pos[1] + floor.dimensions[1]/2)
                    and self.yVel >= 0):
                self.isGrounded = True
                self.touchingFloor = floor
                self.yVel = 0
                self.pos[1] = floor.pos[1] - self.dimensions[1] + 1

        if (keys[pygame.K_w] or keys[pygame.K_COMMA]) and self.isGrounded:
            self.yVel -= self.jumpPower
            self.isGrounded = False

        if not self.touchingFloor == 0 \
            and (keys[pygame.K_s] or keys[pygame.K_o]) \
                and self.isGrounded:
            self.pos[1] = self.touchingFloor.pos[1] - \
                self.touchingFloor.dimensions[1]/2
            self.yVel += self.jumpPower
            self.isGrounded = False
            self.touchingFloor = 0

        if not self.isGrounded:
            self.yVel += 350 * dt
        self.pos[1] += self.yVel * dt
