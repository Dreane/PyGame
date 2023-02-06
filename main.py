import time
import sys
import pygame
import mapping
import lander_machine

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 17)
state_font = pygame.font.SysFont('Comic Sans MS', 30)

fuel = 1000
attempt = 1
is_win = None
high_score = ''

map_complete = 0

all_sprites = pygame.sprite.Group()

map = mapping.Map(WIDTH, HEIGHT)

lander = lander_machine.Lander(map.width_proportion * 1.25, fuel)
land_rect = lander.image.get_rect()
fire = lander_machine.Fire(map.get_proportion() * 1.5, lander.rect.centerx, lander.rect.centery, lander.angle)
all_sprites.add(lander)
map_sprites = map.map_sprites
state_sprites = map.state_spites
all_sprites.add(*map_sprites)
state_game_text = my_font.render(f'', False, (255, 255, 255))


def start_screen():
    global map_complete, high_score,fuel
    intro_font = pygame.font.SysFont('Comic Sans MS', 25)

    intro_text = ["Добро пожаловать на борт!",
                  "Нажмите Enter, чтобы начать играть", "", "Правила игры:", "Управление стрелками на клавиатуре:",
                  "вправо,влево - поворот угла,", "вверх-запуск двигателя",
                  "Приземлитесь на платформы, выделенные жирной линией","и облетайте остальные препятствия","При приземлении погрешность угла может составлять 7 градусов","а скорость 10"]
    screen.fill((0, 0, 0))
    text_coord = 50
    for line in intro_text:
        string_rendered = intro_font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH / 2 - string_rendered.get_width() / 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        map_complete = 0
        high_score = open('resources/high_score.txt').read()
        fuel = 1000
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    first_start()
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


def out_border():
    global state_game_text, is_win
    if lander.rect.x > WIDTH or -60 > lander.rect.x:
        state_game_text = state_font.render(f'Game over!', False, (255, 255, 255))
        is_win = False
        return True


def lander_collider():
    global state_game_text, is_win, map_complete
    is_collide_state = pygame.sprite.spritecollideany(lander, state_sprites)
    is_collide = pygame.sprite.spritecollideany(lander, map_sprites)
    if is_collide:
        if is_collide_state and (0 <= lander.angle <= 7 or 353 <= lander.angle <= 360) and lander.speed_y <= 10:
            print(lander.speed_y)
            state_game_text = state_font.render(f'Map complete: {map_complete + 1}', False, (255, 255, 255))
            is_win = True
            print('Win')
        else:
            print(attempt)
            if attempt == 2:
                state_game_text = state_font.render(f'Game over', False, (255, 255, 255))
            else:
                state_game_text = state_font.render(f'Try again', False, (255, 255, 255))
            is_win = False

        return True
    return False


def clear_group():
    all_sprites.empty()
    map_sprites.empty()
    state_sprites.empty()


def first_start():
    global fuel, lander, attempt, state_sprites, map, map_sprites, all_sprites
    attempt = 1
    clear_group()
    print(len(map_sprites))
    map = mapping.Map(WIDTH, HEIGHT)
    lander.kill()
    lander = lander_machine.Lander(map.width_proportion, fuel)
    state_sprites = map.state_spites
    map_sprites = map.map_sprites
    all_sprites.add(*map_sprites)
    all_sprites.add(lander)


def repeat_map():
    global lander
    lander.kill()
    lander = lander_machine.Lander(map.width_proportion, fuel)
    all_sprites.add(lander)


start_screen()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and lander.fuel:
        screen.blit(fire.image, fire.rect)

    lander.move(pressed)
    lander.start_engine(pressed)
    all_sprites.update()
    all_sprites.draw(screen)
    fire.update_pos(lander.rect.centerx, lander.rect.centery, lander.angle,
                    lander.image.get_height() - lander.image.get_height() / 2)
    lander_collider()
    lander.update_speed()
    speed_x_text = my_font.render(f'Horizontal speed: {round(lander.speed_x, 3)}', False, (255, 255, 255))
    speed_y_text = my_font.render(f'Vertical speed: {round(lander.speed_y, 3)}', False, (255, 255, 255))
    complete_text = my_font.render(f'High score: {map_complete}/{high_score}', False, (255, 255, 255))
    fuel_text = my_font.render(f'Fuel: {lander.fuel}', False, (255, 255, 255))

    screen.blit(speed_x_text, (WIDTH - 200, 50))
    screen.blit(speed_y_text, (WIDTH - 200, 75))

    screen.blit(complete_text, (15, 50))
    screen.blit(fuel_text, (15, 70))

    out_border()

    clock.tick(60)
    pygame.display.update()
    if lander_collider() or out_border():
        lander.speed_y = 0
        lander.speed_x = 0
        lander.g = 0
        lander.a = 0
        lander.x0 = 0
        lander.y0 = 0
        screen.blit(state_game_text,
                    (WIDTH // 2 - state_game_text.get_width() // 2, HEIGHT // 2 - state_game_text.get_height()))
        pygame.display.flip()
        time.sleep(3)
        if is_win:
            fuel = lander.fuel
            map_complete += 1
            first_start()
            print('Win')
        elif not is_win:
            print('Lose')
            attempt += 1
            if attempt == 3:
                if int(high_score) < map_complete:
                    open('resources/high_score.txt', 'w').write(str(map_complete))
                start_screen()
            else:
                fuel = lander.fuel
                repeat_map()
