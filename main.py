import pygame
import sys
import cat
import floor as f
import enemy as e
import time

DIMENSIONS = [1080, 720]

cx, cy = 0, 0
last_time = time.time()
dt = 0

player = cat.Cat([DIMENSIONS[0]/2, 500], [25, 25], 875)

floors = [
    f.Floor([200, 100], [200, 10]),
    f.Floor([500, 600], [500, 10]),
    f.Floor([100, 600], [300, 10]),
    f.Floor([400, 500], [400, 10]),
    f.Floor((0, DIMENSIONS[1] - 10), [DIMENSIONS[0], 10])
]

enemies = [
    e.Enemy([DIMENSIONS[0], 500], e.TYPES["fast"])
]

pygame.init()
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 50)

while True:
    dt = time.time() - last_time
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            # print(cx, cy)

    keys = pygame.key.get_pressed()

    screen.fill((30, 30, 30))
    for floor in floors:
        floor.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)

    for enemy in enemies:
        enemy.update(min(0.16, dt), floors, player)
    player.update(min(0.16, dt), floors)
    pygame.display.update()
    clock.tick(60)
