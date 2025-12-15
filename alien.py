import pygame
import random

instruments = ["bass", "voice2", "voice1", "hihat", "drum"]


class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y, matrix_x, matrix_y):
        super().__init__()
        self.type = type
        self.matrix_x = matrix_x
        self.matrix_y = matrix_y
        self.event_assign()
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction

    def event_assign(self):
        self.instrument = instruments[self.matrix_y]
        self.beat_number = int(self.matrix_x / 3) + 1
        self.sound_event = self.matrix_x % 3
        self.block = int(f"{self.beat_number}{self.matrix_y}")
        pass


class MisteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("Graphics/mystery.png")

        x = random.choice(
            [self.offset / 2, screen_width + self.offset - self.image.get_width()]
        )
        if x == self.offset / 2:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft=(x, 70))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()

