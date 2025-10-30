import random
import pygame
from pygame.sprite import Sprite
#setting enemy attribute
class Enemy(Sprite):
    def __init__(self, settings, screen, level: str, x: int, y: int):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.level = level

        self.color = settings.enemy_colors[level]
        self.rect = pygame.Rect(x, y, settings.enemy_width, settings.enemy_height)

        self.max_hp = settings.enemy_hp[level]
        self.hp = self.max_hp
        self.points = settings.enemy_points[level]

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.base_vx = settings.enemy_base_vx[level]
        self.base_vy = settings.enemy_base_vy[level]
        self.vx = self.base_vx * (1 if random.random() < 0.5 else -1)
        self.vy = self.base_vy

        self.wobble_max = settings.enemy_wobble_max
        self.next_ai_change = pygame.time.get_ticks() + settings.enemy_ai_change_ms

        lo, hi = settings.enemy_fire_cd_range[level]
        self.next_fire_time = pygame.time.get_ticks() + random.randint(lo, hi)

    def update(self):
    # Randomly fine-tune the speed at regular intervals to avoid a pure straight line
        now = pygame.time.get_ticks()
        if now >= self.next_ai_change:
            self.vx = max(-self.base_vx - self.wobble_max,
                          min(self.base_vx + self.wobble_max,
                              self.vx + random.uniform(-0.6, 0.6)))
            self.vy = self.base_vy + random.uniform(-0.15, 0.25)
            self.next_ai_change = now + self.settings.enemy_ai_change_ms

    #boundary setting
        self.x += self.vx
        self.y += self.vy
        if self.rect.left <= 0 and self.vx < 0:
            self.vx *= -1
        if self.rect.right >= self.settings.screen_width and self.vx > 0:
            self.vx *= -1
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def ready_to_fire(self):
        return pygame.time.get_ticks() >= self.next_fire_time

    def schedule_next_fire(self):
        lo, hi = self.settings.enemy_fire_cd_range[self.level]
        self.next_fire_time = pygame.time.get_ticks() + random.randint(lo, hi)

    def draw(self):
    # draw the enemy jet and enemy hp display
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=6)
        bar_w = self.rect.width
        bar_h = 5
        hp_ratio = max(0.0, self.hp / self.max_hp)
        back = pygame.Rect(self.rect.left, self.rect.top - 8, bar_w, bar_h)
        hpw = int(bar_w * hp_ratio)
        front = pygame.Rect(self.rect.left, self.rect.top - 8, hpw, bar_h)
        pygame.draw.rect(self.screen, (40, 40, 48), back, border_radius=3)
        pygame.draw.rect(self.screen, (60, 255, 80), front, border_radius=3)
