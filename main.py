import time

import pygame
import mapping
import lander_machine

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 17)
state_font = pygame.font.SysFont('Comic Sans MS', 35)

all_sprites = pygame.sprite.Group()

map = mapping.Map(WIDTH, HEIGHT)

lander = lander_machine.Lander(map.width_proportion * 1.25)
land_rect = lander.image.get_rect()
fire = lander_machine.Fire(map.get_proportion() * 1.5, lander.rect.centerx, lander.rect.centery, lander.angle)

all_sprites.add(lander)
map_sprites = map.map_sprites
state_sprites = map.state_spites
all_sprites.add(*map_sprites)
state_game_text = my_font.render(f'', False, (255, 255, 255))
fuel = 1000


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def out_border():
    global state_game_text
    if lander.rect.x > WIDTH or -60 > lander.rect.x:
        state_game_text = state_font.render(f'You Lose', False, (255, 255, 255))
        return True


def lander_collider():
    global state_game_text
    is_collide_state = pygame.sprite.spritecollideany(lander, state_sprites)
    is_collide = pygame.sprite.spritecollideany(lander, map_sprites)
    if is_collide:
        lander.speed_y = 0
        lander.speed_x = 0
        lander.g = 0
        lander.a = 0
        lander.x0 = 0
        lander.y0 = 0
        if is_collide_state and (0 <= lander.angle <= 7 or 353 <= lander.angle <= 360) and lander.speed_y <= 10:
            state_game_text = state_font.render(f'You Win', False, (255, 255, 255))
        else:
            state_game_text = state_font.render(f'You Lose', False, (255, 255, 255))
        return True
    return False


def start_game():
    global map, lander, all_sprites, map_sprites, state_sprites
    all_sprites.empty()
    map_sprites.empty()
    state_sprites.empty()
    map = mapping.Map(WIDTH, HEIGHT)
    lander = lander_machine.Lander(map.width_proportion * 1.25)
    all_sprites.add(lander)
    map_sprites = map.map_sprites
    state_sprites = map.state_spites
    all_sprites.add(*map_sprites)


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
    fuel_text = my_font.render(f'Fuel: {lander.fuel}', False, (255, 255, 255))

    screen.blit(speed_x_text, (WIDTH - 200, 50))
    screen.blit(speed_y_text, (WIDTH - 200, 75))

    screen.blit(fuel_text, (15, 50))

    out_border()

    clock.tick(60)
    pygame.display.update()
    if lander_collider() or out_border():
        screen.blit(state_game_text,
                    (WIDTH // 2 - state_game_text.get_width() // 2, HEIGHT // 2 - state_game_text.get_height()))
        pygame.display.flip()
        time.sleep(3)
        start_game()
