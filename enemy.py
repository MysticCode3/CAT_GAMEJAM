import pygame

TYPES = {
    "fast": 0,
    "fat": 1,
    "shooter": 2,
}

class Enemy:
    def __init__(self, pos, type):
        """`type` - int"""
        self.pos = pos
        self.type = type
        self.yVel = 0
        self.isGrounded = False
        self.isMovingLeft = False
        self.isMovingRight = False
        self.isJumping = False
        self.isAttack = False
        self.touchingFloor = 0

        # CHANGABLE CHARACTERISTICS
        self.dimensions = [25, 25]
        self.vel = 350
        self.jumpPower = 0;
    
    def rect(self):
        return pygame.Rect(self.pos, self.dimensions)

    def draw(self, screen):
        if (self.type == TYPES["fast"]):
            pygame.draw.rect(screen, (50, 90, 150), self.rect())
        if (self.type == TYPES["fat"]):
            pass #small
        if (self.type == TYPES["shooter"]):
            pass #small

    def update(self, dt, floors, player):
        if self.isMovingLeft:
            self.pos[0] -= self.vel * dt
            self.isGrounded = False
        
        if self.isMovingRight:
            self.pos[0] += self.vel * dt
            self.isGrounded = False

        for floor in floors:
            if (floor.rect().colliderect(self.rect())
            and (self.pos[1] + self.dimensions[1]/2) <= (floor.pos[1] + floor.dimensions[1]/2)
            and self.yVel >= 0):
                self.isGrounded = True
                self.touchingFloor = floor
                self.yVel = 0
                self.pos[1] = floor.pos[1] - self.dimensions[1] + 1

        if self.isJumping and self.isGrounded:
            self.yVel -= 300
            self.isGrounded = False

        if not self.isGrounded: self.yVel += 350 * dt
        self.pos[1] += self.yVel * dt

        if (self.type == TYPES["fast"]):
            self.fastAi(player, floors)
    
    def fastAi(self, player, floors):
        self.isJumping = False

        if abs(player.pos[0]-self.pos[0]) > 5:
            if player.pos[0] > self.pos[0]:
                self.isMovingRight = True
                self.isMovingLeft = False
            elif player.pos[0] < self.pos[0]:
                self.isMovingLeft = True
                self.isMovingRight = False
        else:
            self.isMovingLeft = False
            self.isMovingRight = False

        if self.touchingFloor != 0 and self.isGrounded:
            if self.pos[0] < self.touchingFloor.pos[0] + 10 or self.pos[0] > self.touchingFloor.pos[0] + self.touchingFloor.dimensions[0] - 10:
                self.isJumping = True