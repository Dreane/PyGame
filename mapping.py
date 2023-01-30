import pygame
import math

pygame.init()


class Map:
    def __init__(self, width, height):
        self.txt = [i.strip('\n') for i in open('resources/land/land1.txt').readlines()]
        self.length_land = max(map(len, self.txt))
        print(self.length_land)
        self.width_proportion = width // self.length_land
        self.height_proportion = height // len(self.txt)
        print(math.degrees(math.atan(self.height_proportion // self.width_proportion)))
        self.map_sprites = pygame.sprite.Group()
        self.state_spites = pygame.sprite.Group()
        self.draw()

    def draw(self):
        pos_x = 0
        pos_y = 0
        for y in self.txt:
            for x in y:
                if x and x != ' ':
                    if x == '_':
                        line = Line('resources/img/line.png', pos_x, pos_y, self.width_proportion,
                                    self.height_proportion, 0)
                    elif x == '/':
                        line = Line('resources/img/line.png', pos_x, pos_y, self.width_proportion,
                                    self.height_proportion, 45)
                        #pygame.draw.rect(line.image, (255, 255, 255), line.border, 1)
                    elif x == '\\':
                        line = Line('resources/img/line.png', pos_x, pos_y, self.width_proportion,
                                    self.height_proportion, -45)
                    # elif x == '|':
                    #     pygame.draw.line(screen, (255, 255, 255), (pos_x, pos_y - self.height_proportion),
                    #                      (pos_x, pos_y))
                    elif x == '=':
                        line = State(pos_x, pos_y, self.width_proportion)
                        self.state_spites.add(line)
                    self.map_sprites.add(line)
                pos_x += self.width_proportion
            pos_y += self.height_proportion
            pos_x = 0

    def get_proportion(self):
        print(self.width_proportion)
        return self.width_proportion

    def get_group(self):
        return self.map_sprites


class Line(pygame.sprite.Sprite):
    def __init__(self, img, pos_x, pos_y, width_proportion, height_proportion, rotate):
        pygame.sprite.Sprite.__init__(self)

        self.image_not_scaled = pygame.image.load(img).convert_alpha()
        if rotate == 45:
            self.image_scaled = pygame.transform.scale(self.image_not_scaled,
                                                       (round(
                                                           (width_proportion ** 2 + height_proportion ** 2) ** (1 / 2)),
                                                        3))
            self.image = pygame.transform.rotate(self.image_scaled,
                                                 math.degrees(math.atan(height_proportion // width_proportion)))
            self.rect = self.image.get_rect(x=pos_x, y=pos_y - height_proportion)
        if rotate == -45:
            self.image_scaled = pygame.transform.scale(self.image_not_scaled,
                                                       (round(
                                                           (width_proportion ** 2 + height_proportion ** 2) ** (1 / 2)),
                                                        3))
            self.image = pygame.transform.rotate(self.image_scaled,
                                                 math.degrees(math.atan(-height_proportion // width_proportion)))
            self.rect = self.image.get_rect(x=pos_x, y=pos_y - height_proportion)
        if rotate == 0:
            self.image = pygame.transform.scale(self.image_not_scaled, (width_proportion, 3))
            self.rect = self.image.get_rect(x=pos_x, y=pos_y)

        self.border = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())

class State(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width_proportion):
        pygame.sprite.Sprite.__init__(self)
        self.image_not_scaled = pygame.image.load('resources/img/state.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_not_scaled, (width_proportion, 5))
        self.rect = self.image.get_rect(x=pos_x, y=pos_y-3)
