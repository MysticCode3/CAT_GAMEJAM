import pygame
import math

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
        self.x_vel = 0
        self.y_vel = 0
        self.is_grounded = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_jumping = False
        self.is_falling = False
        self.is_falling_timer = 0
        self.ground_floor = 0
        self.attack_timer = 0

        # CHANGABLE CHARACTERISTICS
        self.dimensions = [0, 0]
        self.vel = 0
        self.jump_power = 0
        self.health = 0
        self.damage = 0
        self.attack_charge = 0
        self.image = None

        if self.type == TYPES["fast"]:
            self.dimensions = [30, 30]
            self.vel = 975
            self.jump_power = 350
            self.health = 2
            self.damage = 1
            self.attack_charge = 0.5
            self.attack_timer = 4
            self.img = pygame.image.load("assets/fast_enemy.png")
            self.img = pygame.transform.scale(self.img, (self.dimensions))
        if self.type == TYPES["fat"]:
            self.dimensions = [45, 45]
            self.vel = 595
            self.jump_power = 310
            self.health = 4
            self.damage = 3
            self.attack_charge = 2
            self.attack_timer = 5
            self.img = pygame.image.load("assets/fat_enemy.png")
            self.img = pygame.transform.scale(self.img, (self.dimensions))

    def rect(self):
        return pygame.Rect(self.pos, self.dimensions)

    def draw(self, screen):
        if (self.type == TYPES["fast"]):
            # pygame.draw.rect(screen, (50, 90, 150), self.rect())
            screen.blit(self.img, (self.rect().x, self.rect().y))
        if (self.type == TYPES["fat"]):
            # pygame.draw.rect(screen, (150, 90, 50), self.rect())
            screen.blit(self.img, (self.rect().x, self.rect().y))
        if (self.type == TYPES["shooter"]):
            pass  # same size as player

    def update(self, dt, floors, player, player_bullets):
        self.is_falling_timer -= dt

        if self.is_moving_left:
            self.x_vel -= self.vel * dt

        if self.is_moving_right:
            self.x_vel += self.vel * dt

        self.pos[0] += self.x_vel * dt
        self.x_vel *= math.pow(0.1, dt)
        if abs(self.x_vel) < 10:
            self.x_vel = 0
        else:
            self.is_grounded = False

        if self.is_falling_timer <= 0:
            for floor in floors:
                if (floor.rect().colliderect(self.rect())
                    and (self.pos[1] + self.dimensions[1]/2)
                    <= (floor.pos[1] + floor.dimensions[1]/2)
                        and self.y_vel >= 0):
                    self.is_grounded = True
                    self.ground_floor = floor
                    self.y_vel = 0
                    self.pos[1] = floor.pos[1] - self.dimensions[1] + 1

        if self.is_jumping and self.is_grounded:
            self.y_vel -= self.jump_power
            self.is_grounded = False

        if not self.ground_floor == 0 \
            and self.is_falling \
                and self.is_grounded:
            self.is_falling_timer = 0.2
            self.pos[1] = self.ground_floor.pos[1] - \
                self.ground_floor.dimensions[1]/2
            self.y_vel += self.jump_power
            self.is_grounded = False
            self.ground_floor = 0


        if not self.is_grounded:
            self.y_vel += 350 * dt
        self.pos[1] += self.y_vel * dt

        if self.type == TYPES["fast"] or self.type == TYPES["fat"]:
            self.homingAi(dt, player)

        for player_bullet in player_bullets:
            if player_bullet.rect().colliderect(self.rect()):
                self.health -= player_bullet.damage
                player_bullet.timer = 0
                player_bullet.x = -50000
        
    def homingAi(self, dt, player):
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_jumping = False
        self.is_falling = False

        if abs(player.pos[0]-self.pos[0]) > 5:
            if player.pos[0] > self.pos[0]:
                self.is_moving_right = True
                self.is_moving_left = False
            elif player.pos[0] < self.pos[0]:
                self.is_moving_left = True
                self.is_moving_right = False

        if self.ground_floor != 0 \
            and self.is_grounded \
                and self.pos[1] > player.pos[1] \
                and abs(self.pos[1] - player.pos[1]) > 50:
            self.is_jumping = True
        

        if self.ground_floor != 0 \
            and self.is_grounded \
                and self.pos[1] < player.pos[1] \
                and abs(self.pos[1] - player.pos[1]) > 50:
            self.is_falling = True

        self.attack_timer -= dt
        if self.attack_timer <= 0 \
            and self.rect().colliderect(player.rect()):
            self.attack_timer = self.attack_charge
            player.health -= self.damage
