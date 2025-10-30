import pygame

class Jet:
    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings


    #player jet initial place, hp and movement
        self.color = settings.jet_color
        self.rect = pygame.Rect(0, 0, settings.jet_width, settings.jet_height)
        self.rect.midbottom = (settings.screen_width // 2, settings.screen_height - 12)
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

        self.max_hp = settings.player_max_hp
        self.hp = self.max_hp

    def reset_hp(self):
        self.hp = self.max_hp

    def update(self):

    #update place setting
        if self.moving_right and self.rect.right < self.settings.screen_width:
            self.x += self.settings.jet_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.jet_speed
        self.rect.x = int(self.x)

    def draw(self):

    #player jet model
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=8)
        nose = [
            (self.rect.centerx, self.rect.top - 14),
            (self.rect.left + 10, self.rect.top + 6),
            (self.rect.right - 10, self.rect.top + 6),
        ]
        pygame.draw.polygon(self.screen, self.color, nose)
