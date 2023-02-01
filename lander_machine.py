import math

import pygame


class Lander(pygame.sprite.Sprite):
    def __init__(self, proportion, fuel):
        super(Lander, self).__init__()
        self.image_not_scaled = pygame.transform.smoothscale(
            pygame.image.load("resources/img/lander_zoom.png").convert(), (proportion, proportion))
        self.image = self.image_not_scaled
        self.rect = self.image.get_rect(center=(0, 0))
        self.x0 = 0
        self.y0 = 0
        self.angle = 0
        self.change_angle = 0
        self.speed_y = 20
        self.speed_x = 50
        self.g = 3.5
        self.ax = 0
        self.a = 0
        self.angle = 45
        self.border = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.pos_x = -8
        self.pos_y = -8
        self.fuel = fuel

    def rot(self):
        self.image = pygame.transform.rotate(self.image_not_scaled, self.angle)
        self.angle += self.change_angle
        self.angle = self.angle % 360
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, li):
        self.change_angle = 0
        if li[pygame.K_LEFT]:
            self.change_angle = 4
        elif li[pygame.K_RIGHT]:
            self.change_angle = -4
        self.rot()

    def update(self, *args):
        self.pos_x += self.speed_x * (1 / 60)
        self.pos_y += self.speed_y * (1 / 60)
        self.rect.center = (self.pos_x, self.pos_y)

    #        pygame.draw.rect(self.image, (255, 255, 255), self.border, 1)

    def update_speed(self):
        self.ax = -self.a * math.sin(math.radians(self.angle))
        self.ay = self.g - self.a * math.cos(math.radians(self.angle))
        self.speed_x = self.speed_x + self.ax * (1 / 60)
        self.speed_y = self.speed_y + self.ay * (1 / 60)

    def start_engine(self, li):
        if li[pygame.K_UP] and self.fuel > 0:
            self.a = 40
            self.fuel -= 2
        else:
            self.a = 0


class Fire(pygame.sprite.Sprite):
    def __init__(self, proportion, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image_not_scaled = pygame.transform.smoothscale(
            pygame.image.load("resources/img/fire.png").convert_alpha(), (proportion, proportion))
        self.image = self.image_not_scaled
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.border = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())

    def update_pos(self, x, y, angle, l):
        self.image = pygame.transform.rotate(self.image_not_scaled, angle)
        self.rect.center = (x + l * math.sin(math.radians(angle)), y + l * math.cos(math.radians(angle)))
        # pygame.draw.rect(self.image, (255, 255, 255), self.border, 1)
