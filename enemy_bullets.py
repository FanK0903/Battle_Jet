import pygame
from pygame.sprite import Sprite

class EnemyAmmo(Sprite):
    def __init__(self, settings, screen, start_pos, vy):
    #setting enemy ammo
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.color = settings.enemy_bullet_color

        self.rect = pygame.Rect(0, 0, settings.enemy_bullet_width, settings.enemy_bullet_height)
        self.rect.midtop = start_pos
        self.y = float(self.rect.y)
        self.vy = float(vy)

    def update(self):
        self.y += self.vy
        self.rect.y = int(self.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=2)
