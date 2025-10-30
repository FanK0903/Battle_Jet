import pygame
from pygame.sprite import Sprite

class Ammo(Sprite):
    def __init__(self, settings, screen, jet_rect, damage):

    #setting player bullet movement and damage swift
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.color = settings.bullet_color

        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.midbottom = (jet_rect.centerx, jet_rect.top)
        self.y = float(self.rect.y)

        self.damage = int(damage)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=2)