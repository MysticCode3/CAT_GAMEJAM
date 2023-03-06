import pygame
import math
from bullet import Bullet


class Cat:
    def __init__(self, pos, dimensions, vel):
        self.pos = pos
        self.dimensions = dimensions
        self.vel = vel
        self.x_vel = 0
        self.y_vel = 0
        self.is_grounded = False
        self.is_falling_timer = 0
        self.ground_floor = 0
        self.jump_power = 300
        self.bullet_list = []
        self.shoot_cooldown = 0
        self.shoot_cooldown_charge = 0.9
        self.health = 8
        self.orignal_health = self.health
        self.img = pygame.image.load("assets/cat_img.png")
        self.img = pygame.transform.scale(self.img, (self.dimensions))
        self.bullet_img = pygame.image.load("assets/bullet_img.png")
        self.bullet_img = pygame.transform.scale(self.bullet_img, (16, 16))
        self.bullet_dmg = 1

    def rect(self):
        return pygame.Rect(self.pos, self.dimensions)

    def draw(self, screen):
        screen.blit(self.img, (self.rect().x, self.rect().y))
        for bullet in self.bullet_list:
            screen.blit(self.bullet_img, (bullet.rect().x, bullet.rect().y))
        pygame.draw.rect(screen, (255, 255, 255), ((10, 10), (150, 30)), 2, 10)
        if self.health >= 0:
            pygame.draw.rect(
                screen,
                (212, 113, 93),
                (
                    (10, 10),
                    ((150/self.orignal_health) * self.health, 30)
                ),
                0,
                10
            )

    def update(self, dt, floors, enemy_bullets):
        keys = pygame.key.get_pressed()
        self.shoot_cooldown -= dt
        self.is_falling_timer -= dt

        if keys[pygame.K_a]:
            self.x_vel -= self.vel * dt
            self.is_grounded = False

        # qwerty or dvorak
        if keys[pygame.K_d] or keys[pygame.K_e]:
            self.x_vel += self.vel * dt
            self.is_grounded = False

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

        if (keys[pygame.K_w] or keys[pygame.K_COMMA]) and self.is_grounded:
            self.y_vel -= self.jump_power
            self.is_grounded = False

        if not self.ground_floor == 0 \
            and (keys[pygame.K_s] or keys[pygame.K_o]) \
                and self.is_grounded:
            self.pos[1] = self.ground_floor.pos[1] - \
                self.ground_floor.dimensions[1]/2
            self.is_falling_timer = 0.2
            self.y_vel += self.jump_power
            self.is_grounded = False
            self.ground_floor = 0

        if self.pos[1] > 676:
            self.pos[1] = 676
            self.y_vel = 0

        if not self.is_grounded:
            self.y_vel += 350 * dt
        self.pos[1] += self.y_vel * dt

        for enemy_bullet in enemy_bullets:
            if enemy_bullet.rect().colliderect(self.rect()):
                self.health -= enemy_bullet.damage
                enemy_bullet.timer = 0
                enemy_bullet.x = -50000

        for bullet in self.bullet_list:
            if bullet.timer <= 0:
                self.bullet_list.remove(bullet)

            bullet.update(floors, dt)

    def shoot(self, cursor_pos):
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = self.shoot_cooldown_charge
        self.bullet_list.append(
            Bullet(
                self.pos[0] + self.dimensions[0] / 2,
                self.pos[1] + self.dimensions[1] / 2,
                cursor_pos[0], cursor_pos[1],
                500,
                self.bullet_dmg
            )
        )