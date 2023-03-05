import pygame
import sys
import cat
import floor as f
import enemy as e
import time
import random

DIMENSIONS = [1080, 720]
cx, cy = 0, 0

pygame.init()
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 50)


def random_enemy():
    return random.randint(0, 2)


def endless_mode():
    global cx, cy
    last_time = time.time()
    dt = 0

    player = cat.Cat([DIMENSIONS[0]/2 - 17.5, 200], [35, 35], 925)

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
        e.Enemy([DIMENSIONS[0]/2 - 25, 500], e.TYPES["shooter"]),
    ]

    enemy_spawn_time = 8
    enemy_spawn_timer = 8
    mouse_down = False
    is_running = True
    score = 0

    while is_running:
        if player.health <= 0 \
            or player.pos[0] + player.dimensions[0] < 0 \
                or player.pos[0] > DIMENSIONS[0]:
            is_running = False
        dt = time.time() - last_time
        last_time = time.time()
        enemy_spawn_timer -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Score: " + str(score))
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            if event.type == pygame.MOUSEMOTION:
                cx, cy = pygame.mouse.get_pos()

        if mouse_down:
            player.shoot([cx, cy])
        screen.fill((255, 195, 150))
        for floor in floors:
            floor.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        for enemy in enemies:
            enemy.update(min(0.16, dt), floors, player)
            if enemy.health <= 0 \
                or enemy.pos[0] + enemy.dimensions[0] < 0 \
                    or enemy.pos[0] > DIMENSIONS[0]:
                enemies.remove(enemy)
                score += 1

        if enemy_spawn_timer <= 0:
            player.shoot_cooldown_charge *= 0.925
            enemy_spawn_time *= 0.96
            enemy_spawn_timer = enemy_spawn_time
            enemies.append(
                e.Enemy(
                    [random.randint(0, DIMENSIONS[1] - 25),
                     random.randint(0, DIMENSIONS[1] - 25)],
                    random_enemy()
                )
            )

        player.update(
            min(0.16, dt),
            floors,
            [bullet for enemy in enemies for bullet in enemy.bullet_list]
        )
        pygame.display.update()
        clock.tick(60)

    print("Score: " + str(score))


if __name__ == "__main__":
    endless_mode()
