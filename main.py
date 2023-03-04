import pygame
import sys
import cat
import floor as f
import enemy as e
import time
import math
import random

DIMENSIONS = [1080, 720]

cx, cy = 0, 0
last_time = time.time()
dt = 0

player = cat.Cat([DIMENSIONS[0]/2, 200], [35, 35], 875)

floors = [
    f.Floor([200, 100], [200, 30]),
    f.Floor([300, 200], [150, 30]),
    f.Floor([500, 200], [400, 30]),
    f.Floor([100, 300], [400, 30]),
    f.Floor([200, 300], [400, 30]),
    f.Floor([000, 400], [980, 30]),
    f.Floor([100, 500], [980, 30]),
    f.Floor([500, 600], [500, 30]),
    f.Floor([100, 600], [300, 30]),
    f.Floor((0, DIMENSIONS[1] - 10), [DIMENSIONS[0], 30])
]

enemies = [
    e.Enemy([DIMENSIONS[0], 500], e.TYPES["fast"]),
    e.Enemy([0, 500], e.TYPES["fat"]),
]

def random_enemy():
    return random.randint(0, 1)

pygame.init()
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 50)
shoot_cool_down_charge = 0.9
shoot_cool_down = 0
enemy_spawn_time = 8
enemy_spawn_timer = 8

while True:
    if player.health <= 0:
        pygame.quit()
        sys.exit()

    dt = time.time() - last_time
    last_time = time.time()
    shoot_cool_down -= dt
    enemy_spawn_timer -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            if event.button == 1 and shoot_cool_down <= 0:
                shoot_cool_down = shoot_cool_down_charge
                player.shoot([cx, cy])

    keys = pygame.key.get_pressed()

    screen.fill((255, 195, 150))
    for floor in floors:
        floor.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)

    for enemy in enemies:
        enemy.update(min(0.16, dt), floors, player, player.bullet_list)
        if enemy.health <= 0:
            enemies.remove(enemy)
    
    if enemy_spawn_timer <= 0:
        shoot_cool_down_charge *= 0.925
        enemy_spawn_time *= 0.95
        enemy_spawn_timer = enemy_spawn_time
        enemies.append(
            e.Enemy(
                [random.randint(0, DIMENSIONS[1] - 25),
                 random.randint(0, DIMENSIONS[1] - 25)],
                random_enemy()
            )
        )

    player.update(min(0.16, dt), floors)
    pygame.display.update()
    clock.tick(60)
