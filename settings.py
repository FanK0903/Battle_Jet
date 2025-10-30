class Initialize:
    def __init__(self):

    #screen setting and fps setting
        self.screen_width = 900
        self.screen_height = 650
        self.bg_color = (16, 16, 24)
        self.fps = 60

    #player setting
        self.jet_speed = 4.2
        self.jet_width = 60
        self.jet_height = 40
        self.jet_color = (90, 200, 255)
        self.player_max_hp = 4

    #player ammo setting
        self.bullet_speed = 9.0
        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_color = (245, 245, 245)
        self.bullets_allowed = 6
        self.fire_cooldown_ms = 120

    #The level up score requirement
        self.level_thresholds = [500, 1000, 2000]

    #Enemy setting, 3 types enemy with different damage, hp and destoryed score
        self.enemy_width = 48
        self.enemy_height = 34
        self.enemy_colors = {
            "basic": (120, 250, 120),
            "elite": (255, 200, 90),
            "boss":  (255, 110, 110)
        }

        self.enemy_base_vy = {
            "basic": 0.9,
            "elite": 1.05,
            "boss":  1.2
        }
        self.enemy_base_vx = {
            "basic": 0.6,
            "elite": 0.8,
            "boss":  1.0
        }
        self.enemy_wobble_max = 0.6
        self.enemy_ai_change_ms = 900

        self.enemy_bullet_speed = {
            "basic": 4.6,
            "elite": 5.4,
            "boss":  6.2
        }
        self.enemy_bullet_width = 4
        self.enemy_bullet_height = 12
        self.enemy_bullet_color = (255, 90, 90)

        self.enemy_fire_cd_range = {
            "basic": (1300, 1900),
            "elite": (900, 1400),
            "boss":  (650, 1100)
        }

    #The max enemy, different level have different quantity and different appearance percentage
        self.max_enemies_by_lvl = {1: 6, 2: 9, 3: 12}
        self.spawn_interval_ms_by_lvl = {1: 900, 2: 650, 3: 500}
        self.spawn_weights_by_lvl = {
            1: {"basic": 0.65, "elite": 0.28, "boss": 0.07},
            2: {"basic": 0.45, "elite": 0.40, "boss": 0.15},
            3: {"basic": 0.30, "elite": 0.45, "boss": 0.25},
        }

        self.enemy_hp = {"basic": 2, "elite": 4, "boss": 7}
        self.enemy_points = {"basic": 10, "elite": 20, "boss": 30}
