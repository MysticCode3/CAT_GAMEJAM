import pygame

class Cat:
    def __init__(self, pos, dimensions, vel):
        self.pos = pos
        self.dimensions = dimensions
        self.vel = vel
        self.isGrounded = False
        self.jumpPower = 20
        self.yVel = 0

    def rect(self):
        return pygame.Rect(self.pos, self.dimensions)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def update(self, dt, floors):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.pos[0] -= self.vel * dt
            self.isGrounded = False
        
        if keys[pygame.K_d]:
            self.pos[0] += self.vel * dt
            self.isGrounded = False

        for floor in floors:
            if (floor.rect().colliderect(self.rect())
            and (self.pos[1] + self.dimensions[1]/2) <= (floor.pos[1] + floor.dimensions[1]/2)
            and self.yVel >= 0):
                self.isGrounded = True
                self.yVel = 0
                self.pos[1] = floor.pos[1] - self.dimensions[1] + 1

        if keys[pygame.K_w] and self.isGrounded:
            self.yVel -= 300
            self.isGrounded = False

        if not self.isGrounded: self.yVel += 350 * dt
        self.pos[1] += self.yVel * dt