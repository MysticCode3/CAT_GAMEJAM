import pygame
import sys
import cat
import floor as f
import enemy as e
import time
import random
import button

DIMENSIONS = [1080, 720]
cx, cy = 0, 0

pygame.init()
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()
font = pygame.font.Font("PressStart2P-Regular.ttf", 80)
font_small = pygame.font.Font("PressStart2P-Regular.ttf", 50)
font_extra_small = pygame.font.Font("PressStart2P-Regular.ttf", 35)


def random_enemy():
    return random.randint(0, 2)


DIFFICULTIES = {
    "easy": 0,
    "normal": 1,
    "hard": 2
}


def endless_mode(difficulty, high_score):
    global cx, cy
    last_time = time.time()
    dt = 0

    player = cat.Cat([DIMENSIONS[0]/2 - 17.5, 200], [35, 35], 925)

    if difficulty == DIFFICULTIES["easy"]:
        player.orignal_health = 12
        player.health = 12
        player.vel += 100
        player.bullet_dmg = 2
    elif difficulty == DIFFICULTIES["hard"]:
        player.orignal_health = 5
        player.health = 5
        player.vel -= 50
        player.bullet_dmg = 0.75

    floors = [
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

    def spawn_enemy():
        enemies.append(
            e.Enemy(
                [random.randint(0, DIMENSIONS[1] - 25),
                 random.randint(0, DIMENSIONS[1] - 25)],
                random_enemy()
            )
        )

    enemy_spawn_time = 8
    enemy_spawn_timer = 8
    mouse_down = False
    score = 0

    while True:
        if player.health <= 0 \
            or player.pos[0] + player.dimensions[0] < 0 \
                or player.pos[0] > DIMENSIONS[0]:
            return score

        dt = time.time() - last_time
        last_time = time.time()
        enemy_spawn_timer -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                cx, cy = pygame.mouse.get_pos()

        if mouse_down:
            player.shoot([cx, cy])

        screen.fill((255, 195, 150))
        for floor in floors:
            floor.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        score_txt = font_extra_small.render(f"Score: {score}", True, (212, 113, 93))
        screen.blit(score_txt, (10, 45))

        high_score_txt = font_extra_small.render(f"High Score: {score}", True, (212, 113, 93))
        if high_score >= score:
            high_score_txt = font_extra_small.render(f"High Score: {high_score}", True, (212, 113, 93))

        screen.blit(high_score_txt, (10, 80))

        pygame.display.update()

        for enemy in enemies:
            enemy.update(min(0.16, dt), floors, player)
            if enemy.health <= 0 \
                or enemy.pos[0] + enemy.dimensions[0] < 0 \
                    or enemy.pos[0] > DIMENSIONS[0]:
                enemies.remove(enemy)
                score += 1

        if enemy_spawn_timer <= 0:
            player.shoot_cooldown_charge *= 0.965
            enemy_spawn_time *= 0.995
            enemy_spawn_timer = enemy_spawn_time
            spawn_enemy()
            if score > 50 and difficulty >= DIFFICULTIES["easy"]:
                spawn_enemy()
            if score > 100 and difficulty >= DIFFICULTIES["normal"]:
                spawn_enemy()
            if score > 250 and difficulty >= DIFFICULTIES["hard"]:
                spawn_enemy()
            if score > 500 and difficulty >= DIFFICULTIES["hard"]:
                spawn_enemy()

        player.update(
            min(0.16, dt),
            floors,
            [bullet for enemy in enemies for bullet in enemy.bullet_list]
        )

        clock.tick(60)

def main_menu(high_score):
    global cx, cy
    difficulty_button = button.Button(
        [(243, 180, 134), (255, 200, 150), (239, 235, 234)],
        DIMENSIONS[0]/2-200, 400,
        400, 100
    )
    start_button = button.Button(
        [(243, 180, 134), (255, 200, 150), (239, 235, 234)],
        DIMENSIONS[0]/2-200, 550,
        400, 100
    )
    current_difficulty = 1
    mouse_down = False

    def difficulty_as_string(difficulty_number):
        for a,b in DIFFICULTIES.items():
            if b == difficulty_number:
                return a
        
        return None

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                difficulty_button.update(cx, cy, mouse_down, False)
                start_button.update(cx, cy, mouse_down, False)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                difficulty_button.update(cx, cy, mouse_down, True)
                start_button.update(cx, cy, mouse_down, True)
            elif event.type == pygame.MOUSEMOTION:
                cx, cy = pygame.mouse.get_pos()
                difficulty_button.update(cx, cy, mouse_down, False)
                start_button.update(cx, cy, mouse_down, False)
        
        if difficulty_button.is_clicked:
            current_difficulty += 1
            if current_difficulty > 2:
                current_difficulty = 0
            difficulty_button.is_clicked = False
        
        if start_button.is_clicked:
            return current_difficulty

        screen.fill((255, 195, 150))

        title_txt_1 = font.render("Cat", True, (212, 113, 93))
        title_txt_2 = font.render("Ball", True, (212, 113, 93))

        if high_score != 0:
            high_score_txt = font_extra_small.render(f"High Score: {high_score}", True, (212, 113, 93))
            screen.blit(high_score_txt, (DIMENSIONS[0]/2-high_score_txt.get_width()/2, DIMENSIONS[1] / 2 - 35))

        screen.blit(title_txt_1, (DIMENSIONS[0]/2-title_txt_1.get_width()/2 - 50, 100))
        screen.blit(title_txt_2, (DIMENSIONS[0]/2-title_txt_1.get_width()/2 + 50, 220))

        difficulty_button_txt = font_small.render(f"{difficulty_as_string(current_difficulty)}", True, (212, 113, 93)) 
        difficulty_button.draw(screen)
        screen.blit(difficulty_button_txt, (DIMENSIONS[0]/2-difficulty_button_txt.get_width()/2 + 3, 420)) 

        start_button_txt = font_small.render("start", True, (212, 113, 93)) 
        start_button.draw(screen)
        screen.blit(start_button_txt, (DIMENSIONS[0]/2-start_button_txt.get_width()/2 + 3, 570)) 
        
        clock.tick(60)
        pygame.display.update()

difficulty = 0
high_score = 0

if __name__ == "__main__":
    while True:
        difficulty = main_menu(high_score)
        high_score = endless_mode(difficulty, high_score)
