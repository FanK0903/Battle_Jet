import sys
import random
import pygame

from settings import Initialize
from jet import Jet
from bullets import Ammo
from enemy_bullets import EnemyAmmo
from enemy import Enemy

class Battle_JET:
    def __init__(self):
        pygame.init()
        self.settings = Initialize()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Battle JET — Arcade Mode")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 26)
        self.big_font = pygame.font.SysFont(None, 34)

        self.jet = Jet(self.settings, self.screen)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.score = 0
        self.player_level = 1
        self.next_spawn_time = 0 #enemy refresh timer

    # The winning score, after 2000 score will pass the game
        self.state = 'menu'
        self.win_score=2000

    def start_new_game(self):
    #every new game setting, refresh all the parameter
        self.score = 0
        self.player_level = 1
        self.jet.reset_hp()
        self.enemies.empty()
        self.enemy_bullets.empty()
        self.bullets.empty()
        self.next_spawn_time = pygame.time.get_ticks() + 600
        self.state = 'playing'


    def compute_player_level(self):
    #player have 3 level, for every level the bullet damage will increase 1(initial as 1), and every time level up would refresh life
        s = self.score
        th = self.settings.level_thresholds
        if s < th[0]:
            return 1
        elif s < th[1]:
            return 2
        else:
            return 3

    def current_bullet_damage(self):
        return self.player_level

    def on_level_up(self, new_level):
        self.jet.reset_hp()
        for b in list(self.enemy_bullets)[:8]:
            self.enemy_bullets.remove(b)


    def pick_level_by_weights(self):
    # enemy generate
        weights = self.settings.spawn_weights_by_lvl[self.player_level]
        r = random.random()
        if r < weights["basic"]:
            return "basic"
        elif r < weights["basic"] + weights["elite"]:
            return "elite"
        else:
            return "boss"

    def spawn_enemy_if_due(self):
        now = pygame.time.get_ticks()
        if now < self.next_spawn_time:
            return

    # The max enemy quantity limit
        max_on = self.settings.max_enemies_by_lvl[self.player_level]
        if len(self.enemies) >= max_on:
            self.next_spawn_time = now + 120
            return

    #random generate enemy at top of the screen
        level = self.pick_level_by_weights()
        x = random.randint(24, self.settings.screen_width - self.settings.enemy_width - 24)
        y = -random.randint(20, 120)
        enemy = Enemy(self.settings, self.screen, level, x, y)
        self.enemies.add(enemy)

    #next enemy generate time
        interval = self.settings.spawn_interval_ms_by_lvl[self.player_level]
        self.next_spawn_time = now + int(interval * random.uniform(0.85, 1.15))

    def enemies_try_fire(self):
        for e in self.enemies:
            if e.ready_to_fire():
                vy = self.settings.enemy_bullet_speed[e.level]
                start = (e.rect.centerx, e.rect.bottom)
                self.enemy_bullets.add(EnemyAmmo(self.settings, self.screen, start, vy))
                e.schedule_next_fire()

    def handle_events(self):
    #press 'q' for quit, press 'enter' for start the game, press any key to return menu after lose the game, press 'enter' to back mene after win
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.state == 'playing':
                    self._keydown(event)
                elif self.state == 'menu':
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.start_new_game()
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit(); sys.exit()
                elif self.state == 'gameover':
                    self.state = 'menu'
                elif self.state=='win':
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.state='menu'
            elif event.type == pygame.KEYUP and self.state == 'playing':
                self._keyup(event)

    def _keydown(self, event):
    #press 'Esc' to quit game during play
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.jet.moving_right = True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.jet.moving_left = True
        elif event.key in (pygame.K_SPACE, pygame.K_k):
            self.fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self.state = 'menu'

    def _keyup(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.jet.moving_right = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.jet.moving_left = False

    def fire_bullet(self):
        now = pygame.time.get_ticks()
        if (now - getattr(self, "last_fire_time", 0)) < self.settings.fire_cooldown_ms:
            return
        if len(self.bullets) < self.settings.bullets_allowed:
            dmg = self.current_bullet_damage()
            self.bullets.add(Ammo(self.settings, self.screen, self.jet.rect, dmg))
            self.last_fire_time = now

    def update_bullets(self):
    # Clean the bullets when move out of screen
        self.bullets.update()
        for b in list(self.bullets):
            if b.rect.bottom <= 0:
                self.bullets.remove(b)

    #check if the bullet shoot the enemy and reduce enemy hp and update score
        for bullet in list(self.bullets):
            hit_list = [e for e in self.enemies if e.rect.colliderect(bullet.rect)]
            if hit_list:
                self.bullets.remove(bullet)
                damage = bullet.damage
                for enemy in hit_list:
                    enemy.hp -= damage
                    if enemy.hp <= 0:
                        self.score += enemy.points
                        self.enemies.remove(enemy)

    def update_enemy_bullets(self):
        self.enemy_bullets.update()
        for b in list(self.enemy_bullets):
            if b.rect.top >= self.settings.screen_height:
                self.enemy_bullets.remove(b)
            elif b.rect.colliderect(self.jet.rect):
                self.enemy_bullets.remove(b)
                self.player_take_hit()

    def player_take_hit(self):
    #gameover when player hp equal or less than 0
        self.jet.hp -= 1
        if self.jet.hp <= 0:
            self.enemies.empty()
            self.enemy_bullets.empty()
            self.bullets.empty()
            self.state = 'gameover'
            self.gameover_time = pygame.time.get_ticks()

    def check_collisions_and_bounds(self):
    # check the enemy jet crash player jet cause damage
        for e in list(self.enemies):
            if e.rect.colliderect(self.jet.rect):
                self.enemies.remove(e)
                self.player_take_hit()
            elif e.rect.top > self.settings.screen_height:
                self.enemies.remove(e)

    def draw_hud(self):
    # draw head up display, display current score and next level score requirement and player hp
        score_surf = self.big_font.render(f"Score: {self.score}", True, (235, 235, 255))
        score_rect = score_surf.get_rect(topright=(self.settings.screen_width - 14, 12))
        self.screen.blit(score_surf, score_rect)

        th = self.settings.level_thresholds
        lv = self.player_level
        if lv == 1:
            need = max(0, th[0] - self.score)
        elif lv == 2:
            need = max(0, th[1] - self.score)
        else:
            need = max(0, th[2] - self.score)
        hint = f"Lv.{lv} damage={self.current_bullet_damage()}  Next level: {need}" if lv < 3 else "Lv.3 弹伤=3 (MAX)"
        hint_surf = self.font.render(hint, True, (190, 220, 255))
        self.screen.blit(hint_surf, (14, 14))

        bar_x, bar_y = 14, 42
        bar_w, bar_h = 180, 10
        ratio = max(0.0, self.jet.hp / self.jet.max_hp)
        back = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
        front = pygame.Rect(bar_x, bar_y, int(bar_w * ratio), bar_h)
        pygame.draw.rect(self.screen, (60, 60, 80), back, border_radius=4)
        pygame.draw.rect(self.screen, (255, 90, 90), front, border_radius=4)
        hp_text = self.font.render(f"HP: {self.jet.hp}/{self.jet.max_hp}", True, (220,200,200))
        self.screen.blit(hp_text, (bar_x + bar_w + 10, bar_y - 4))

    def draw_all(self):
    # draw all, include background, hud and entity
        self.screen.fill(self.settings.bg_color)
        for b in self.bullets:
            b.draw()
        for eb in self.enemy_bullets:
            eb.draw()
        for e in self.enemies:
            e.draw()
        self.jet.draw()
        self.draw_hud()
        pygame.display.flip()

    def draw_center_text(self, lines, gap=12):
    #setting display detail when mene, win, loss
        self.screen.fill(self.settings.bg_color)
        surfaces = [self.big_font.render(t, True, (230,230,255)) for t in lines]
        total_h = sum(s.get_height() for s in surfaces) + gap*(len(surfaces)-1)
        y = (self.settings.screen_height - total_h)//2
        for s in surfaces:
            r = s.get_rect(center=(self.settings.screen_width//2, y + s.get_height()//2))
            self.screen.blit(s, r)
            y += s.get_height() + gap
        pygame.display.flip()

    def draw_menu(self):
        self.draw_center_text([
            "Battle JET",
            "",
            "[Enter] Start Game",
            "[Q] Quit"
        ])

    def draw_gameover(self):
        self.draw_center_text([
            "You lose",
            "",
            "[Any key] Back to Main Menu"
        ])

    def draw_win(self):
        self.draw_center_text([
            'You win!',
            '',
            '[Enter] back to Menu',
        ])


    def run_game(self): #The main loop
        while True:
            self.clock.tick(self.settings.fps)
            self.handle_events()

        #player level up checking, refresh player hp
            if self.state == 'playing':
                old_level = self.player_level
                self.player_level = self.compute_player_level()
                if self.player_level > old_level:
                    self.on_level_up(self.player_level)

        #enemy movement and enemy generate
                self.spawn_enemy_if_due()
                for e in self.enemies:
                    e.update()
                self.enemies_try_fire()

                self.jet.update()
                self.update_bullets()
                self.update_enemy_bullets()
                self.check_collisions_and_bounds()

            #judgement for winning
                if self.score>=self.win_score:
                    self.enemies.empty()
                    self.enemy_bullets.empty()
                    self.bullets.empty()
                    self.state='win'
                    continue

                self.draw_all()

            elif self.state == 'menu':
                self.draw_menu()

            elif self.state == 'gameover':
                self.draw_gameover()

            elif self.state=='win':
                self.draw_win()

if __name__ == "__main__":
    Battle_JET().run_game()
