import pygame
import sys
import random
import os
from datetime import datetime

pygame.init()

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Exploit')

background_image = pygame.image.load('background_image.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

start_button_image = pygame.image.load('start_button_image.jpg')
start_button_image = pygame.transform.scale(start_button_image, (200, 50))

settings_button_image = pygame.image.load('settings_button_image.jpg')
settings_button_image = pygame.transform.scale(settings_button_image, (200, 50))

exit_button_image = pygame.image.load('exit_button_image.jpg')
exit_button_image = pygame.transform.scale(exit_button_image, (200, 50))

history_button_image = pygame.image.load('history_button_image.png')
history_button_image = pygame.transform.scale(history_button_image, (200, 50))

font = pygame.font.Font(None, 36)

graphics_options = ['Low', 'Low', 'Low']
selected_graphics_option = 0

sound_options = ['On', 'Off']
selected_sound_option = 0

def run_game():
    # Ваш код игры здесь
    def load_image(name, colorkey=None):
        fullname = os.path.join('images', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image

    class StaticImg(pygame.sprite.Sprite):
        image = [load_image("static_img/sword.png"),
                 load_image("static_img/hp_full.png")]

        def __init__(self, group, x_pos, y_pos, nom):
            super().__init__(group, all_sprites)
            self.image = StaticImg.image[nom]
            self.rect = self.image.get_rect()
            self.rect.x = x_pos
            self.rect.y = y_pos

    class Level(pygame.sprite.Sprite):
        background = [load_image("backgrounds/under_water.jpg"),
                      load_image("backgrounds/defolt_forest.jpg"),
                      load_image("backgrounds/night_water.png")]

        def __init__(self, group, x_pos, nomer):
            super().__init__(group, all_sprites)
            self.image = Level.background[nomer]
            self.rect = self.image.get_rect()
            self.rect.x = x_pos
            self.rect.y = 0

        def update(self, *args):
            self.rect = self.rect.move(-1, 0)
            if self.rect.x == -1700:
                self.rect.x = 1700

    class FlyObj(pygame.sprite.Sprite):

        def update(self, *args):
            self.rect = self.rect.move(3, 0)

    class MonsterBullit(FlyObj):
        image = load_image("attack/ball_1.png")
        images = [load_image("guardian/attack/guard_attk_1.png"), load_image("guardian/attack/guard_attk_2.png"),
                  load_image("guardian/attack/guard_attk_3.png"), load_image("guardian/attack/guard_attk_4.png")]

        def __init__(self, group, pos_x, pos_y):
            super().__init__(bullit_m_sprite, all_sprites)
            self.image = MonsterBullit.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def update(self, *args):
            self.rect = self.rect.move(-6, 0)
            # self.testcollide(hero_sprites, True)

    class HeroBullit(FlyObj):
        image = load_image("attack/ball_1.png")

        def __init__(self, group, pos_x, pos_y):
            super().__init__(bullit_sprite, all_sprites)
            self.image = HeroBullit.image
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def update(self, *args):
            self.rect = self.rect.move(3, 0)
            # self.testcollide(monsters_sprites, True)

    class HeroBullitSuper(HeroBullit):
        image = load_image("attack/ball_1.png")

        def __init__(self, group, pos_x, pos_y, nom):
            super().__init__(group, pos_x, pos_y)
            self.image = HeroBullitSuper.image
            self.nom = nom

        def update(self, *args):
            if self.nom == 1:
                self.rect = self.rect.move(3, 1)
            if self.nom == 2:
                self.rect = self.rect.move(3, -1)
            if self.nom == 3:
                self.rect = self.rect.move(3, 0)
            super().update()

    class HeroBullitTornado(FlyObj):
        tornado = [load_image("tornado/tornado_2.png"),
                   load_image("tornado/tornado_3.png"), load_image("tornado/tornado_4.png"),
                   load_image("tornado/tornado_5.png"), load_image("tornado/tornado_6.png"),
                   load_image("tornado/tornado_7.png"), load_image("tornado/tornado_8.png")]

        def __init__(self, group, pos_x, pos_y):
            super().__init__(group, all_sprites)
            self.image = HeroBullitTornado.tornado[0]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def testcollide(self, group, kill_self):
            is_kill = pygame.sprite.spritecollideany(self, group)
            pygame.sprite.spritecollide(self, group, True)
            if is_kill and kill_self:
                self.kill()

        def update(self, *args):
            # self.rect = self.rect.move(3, 0)
            self.image = HeroBullitTornado.tornado[anim_counter_tornado]
            self.testcollide(monsters_sprites, True)

    class Portal(pygame.sprite.Sprite):
        image = load_image("static_img/portal.png")

        def __init__(self):
            super().__init__(portal_sprite, all_sprites)
            self.image = Portal.image
            self.rect = self.image.get_rect()
            self.rect.x = 1520
            self.rect.y = 350

    class Monsters(pygame.sprite.Sprite):
        image = load_image("static_img/portal.png")

        def __init__(self, group, y_pos):
            super().__init__(group, monsters_sprites, all_sprites)
            self.rect = self.image.get_rect()
            self.rect.x = 1730
            self.rect.y = y_pos

        def testcollide(self):
            is_kill = pygame.sprite.spritecollideany(self, hero_sprites)
            if is_kill:
                magic_hero.HP_minus()
                if magic_hero.HP == 0:
                    s_HP_0.play()
                else:
                    s_HP_minus.play()
                self.kill()

        def bullitcollide(self, group):
            is_kill = pygame.sprite.spritecollideany(self, group)
            pygame.sprite.spritecollide(self, group, True)
            if is_kill:
                self.kill()
                return True
            return False

    class MonsterFish(Monsters):
        fish_monster = [load_image("fish_monster/fish_monster_1.png"),
                        load_image("fish_monster/fish_monster_2.png"),
                        load_image("fish_monster/fish_monster_3.png"),
                        load_image("fish_monster/fish_monster_4.png"),
                        load_image("fish_monster/fish_monster_5.png"),
                        load_image("fish_monster/fish_monster_6.png")]

        def __init__(self, group, y_pos):
            super().__init__(group, y_pos)
            self.image = MonsterFish.fish_monster[0]

        def update(self, *args):
            self.image = MonsterFish.fish_monster[anim_counter_fish]
            self.rect = self.rect.move(-2, 0)
            self.testcollide()
            self.bullitcollide(bullit_sprite)

    class Guardian(Monsters):
        guardian = [load_image("guardian/guardian_1.png"),
                    load_image("guardian/guardian_2.png"),
                    load_image("guardian/guardian_3.png"),
                    load_image("guardian/guardian_4.png"),
                    load_image("guardian/guardian_5.png")]

        def __init__(self, group, x_pos, y_pos):
            super().__init__(group, y_pos)
            self.image = Guardian.guardian[0]
            self.rect.x = x_pos

        def update(self, *args):
            self.image = Guardian.guardian[anim_counter_guardian]

        def gun(self):
            MonsterBullit(bullit_m_sprite, self.rect.x - 100, self.rect.y + 30)
            s_fire_bullit.play()

    class FirePrinc(Monsters):
        burst_attack = [load_image("fire_princ/burst_attack/burst_attack_1.png"),
                        load_image("fire_princ/burst_attack/burst_attack_2.png"),
                        load_image("fire_princ/burst_attack/burst_attack_3.png"),
                        load_image("fire_princ/burst_attack/burst_attack_4.png"),
                        load_image("fire_princ/burst_attack/burst_attack_5.png"),
                        load_image("fire_princ/burst_attack/burst_attack_6.png"),
                        load_image("fire_princ/burst_attack/burst_attack_7.png")]

        chopping_attack = [load_image("fire_princ/chopping_attack/chopping_attack_1.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_2.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_3.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_4.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_5.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_6.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_7.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_8.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_9.png"),
                           load_image("fire_princ/chopping_attack/chopping_attack_10.png")]

        fire_knife = [load_image("fire_princ/fire_knife/fire_knife_1.png"),
                      load_image("fire_princ/fire_knife/fire_knife_2.png"),
                      load_image("fire_princ/fire_knife/fire_knife_3.png"),
                      load_image("fire_princ/fire_knife/fire_knife_4.png"),
                      load_image("fire_princ/fire_knife/fire_knife_5.png"),
                      load_image("fire_princ/fire_knife/fire_knife_6.png"),
                      load_image("fire_princ/fire_knife/fire_knife_7.png"),
                      load_image("fire_princ/fire_knife/fire_knife_8.png"),
                      load_image("fire_princ/fire_knife/fire_knife_9.png"),
                      load_image("fire_princ/fire_knife/fire_knife_10.png"),
                      load_image("fire_princ/fire_knife/fire_knife_11.png"),
                      load_image("fire_princ/fire_knife/fire_knife_12.png"),
                      load_image("fire_princ/fire_knife/fire_knife_13.png"),
                      load_image("fire_princ/fire_knife/fire_knife_14.png"),
                      load_image("fire_princ/fire_knife/fire_knife_15.png"),
                      load_image("fire_princ/fire_knife/fire_knife_16.png")
                      ]

        princ_walk = [load_image("fire_princ/princ_walk/walk_2.png"),
                      load_image("fire_princ/princ_walk/walk_3.png"),
                      load_image("fire_princ/princ_walk/walk_4.png"),
                      load_image("fire_princ/princ_walk/walk_5.png"),
                      load_image("fire_princ/princ_walk/walk_6.png"),
                      load_image("fire_princ/princ_walk/walk_7.png"),
                      load_image("fire_princ/princ_walk/walk_8.png")]

        def __init__(self, group, pos_x, pos_y):
            super().__init__(group, pos_y)
            self.image = FirePrinc.princ_walk[0]
            self.anim_count = 0
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.not_action = True
            self.random_action = 1

        def testcollide(self):
            is_kill = pygame.sprite.spritecollideany(self, hero_sprites)
            if is_kill:
                magic_hero.HP_minus()
                if magic_hero.HP == 0:
                    s_HP_0.play()
                else:
                    s_HP_minus.play()

        def update(self):
            if 1 <= self.random_action <= 4:
                self.anim_count = self.anim_count % 7
                self.image = FirePrinc.princ_walk[self.anim_count]
                if self.random_action <= 2:
                    dx = 3
                else:
                    dx = -3
                self.rect.x += dx
                if self.anim_count == 6:
                    self.not_action = True
                    self.anim_count = 0

            if self.random_action == 5:
                self.anim_count = self.anim_count % 16
                self.image = FirePrinc.fire_knife[self.anim_count]
                if self.anim_count == 15:
                    self.testcollide()
                    self.not_action = True
                    self.anim_count = 0

            if self.random_action == 6:
                self.anim_count = self.anim_count % 10
                self.image = FirePrinc.chopping_attack[self.anim_count]
                if self.anim_count == 9:
                    self.testcollide()
                    self.not_action = True
                    self.anim_count = 0

            if self.random_action == 7:
                self.anim_count = self.anim_count % 7
                self.image = FirePrinc.burst_attack[self.anim_count]
                if self.anim_count == 6:
                    self.testcollide()
                    self.not_action = True
                    self.anim_count = 0

    class WaterEmpress(Monsters):
        attack = [load_image("water_empress/attack/attack_1.png"),
                  load_image("water_empress/attack/attack_2.png"),
                  load_image("water_empress/attack/attack_3.png"),
                  load_image("water_empress/attack/attack_4.png"),
                  load_image("water_empress/attack/attack_5.png"),
                  load_image("water_empress/attack/attack_6.png"),
                  load_image("water_empress/attack/attack_7.png")]

        drop = [load_image("water_empress/drop/drop_1.png"),
                load_image("water_empress/drop/drop_2.png"),
                load_image("water_empress/drop/drop_3.png"),
                load_image("water_empress/drop/drop_4.png"),
                load_image("water_empress/drop/drop_5.png"),
                load_image("water_empress/drop/drop_6.png"),
                load_image("water_empress/drop/drop_7.png"),
                load_image("water_empress/drop/drop_8.png"),
                load_image("water_empress/drop/drop_9.png"),
                load_image("water_empress/drop/drop_10.png"),
                load_image("water_empress/drop/drop_11.png"),
                load_image("water_empress/drop/drop_12.png"),
                load_image("water_empress/drop/drop_13.png"),
                load_image("water_empress/drop/drop_14.png"),
                load_image("water_empress/drop/drop_15.png"),
                load_image("water_empress/drop/drop_16.png"),
                load_image("water_empress/drop/drop_17.png"),
                load_image("water_empress/drop/drop_18.png"),
                load_image("water_empress/drop/drop_19.png"),
                load_image("water_empress/drop/drop_20.png"),
                load_image("water_empress/drop/drop_21.png"),
                load_image("water_empress/drop/drop_22.png")]

        wave = [load_image("water_empress/wave/wave_1.png"),
                load_image("water_empress/wave/wave_2.png"),
                load_image("water_empress/wave/wave_3.png"),
                load_image("water_empress/wave/wave_4.png"),
                load_image("water_empress/wave/wave_5.png"),
                load_image("water_empress/wave/wave_6.png"),
                load_image("water_empress/wave/wave_7.png"),
                load_image("water_empress/wave/wave_8.png"),
                load_image("water_empress/wave/wave_9.png"),
                load_image("water_empress/wave/wave_10.png"),
                load_image("water_empress/wave/wave_11.png"),
                load_image("water_empress/wave/wave_12.png"),
                load_image("water_empress/wave/wave_13.png"),
                load_image("water_empress/wave/wave_14.png")]

        enpress_walk = [load_image("water_empress/walk/walk_2.png"),
                        load_image("water_empress/walk/walk_3.png"),
                        load_image("water_empress/walk/walk_4.png"),
                        load_image("water_empress/walk/walk_5.png"),
                        load_image("water_empress/walk/walk_6.png"),
                        load_image("water_empress/walk/walk_7.png"),
                        load_image("water_empress/walk/walk_8.png"),
                        load_image("water_empress/walk/walk_9.png"),
                        load_image("water_empress/walk/walk_10.png")]

        def __init__(self, group, pos_x, pos_y):
            super().__init__(group, pos_y)
            self.image = WaterEmpress.enpress_walk[0]
            self.anim_count = 0
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.not_action = True
            self.random_action = 1

        def testcollide(self):
            is_kill = pygame.sprite.spritecollideany(self, hero_sprites)
            if is_kill:
                magic_hero.HP_minus()
                if magic_hero.HP == 0:
                    s_HP_0.play()
                else:
                    s_HP_minus.play()

        def update(self):
            if 1 <= self.random_action <= 4:
                self.anim_count = self.anim_count % 9
                self.image = WaterEmpress.enpress_walk[self.anim_count]
                if self.random_action <= 2:
                    dx = 3
                else:
                    dx = -3
                self.rect.x += dx
                if self.anim_count == 8:
                    self.not_action = True
                    self.anim_count = 0

            if self.random_action == 5:
                self.anim_count = self.anim_count % 14
                self.image = WaterEmpress.wave[self.anim_count]
                if self.anim_count >= 9:
                    self.testcollide()
                if self.anim_count == 13:
                    self.not_action = True
                    self.anim_count = 0

            if self.random_action == 6:
                self.anim_count = self.anim_count % 22
                self.image = WaterEmpress.drop[self.anim_count]
                if self.anim_count >= 18:
                    self.testcollide()
                if self.anim_count == 21:
                    self.testcollide()
                    self.not_action = True
                    self.anim_count = 0

            if self.random_action == 7:
                self.anim_count = self.anim_count % 7
                self.image = WaterEmpress.attack[self.anim_count]
                if self.anim_count >= 5:
                    self.testcollide()
                if self.anim_count == 6:
                    self.testcollide()
                    self.not_action = True
                    self.anim_count = 0

    class Hero(pygame.sprite.Sprite):
        hero_pasiv = [load_image("pasiv/pasivv_1.png"),
                      load_image("pasiv/pasivv_2.png"),
                      load_image("pasiv/pasivv_3.png"),
                      load_image("pasiv/pasivv_4.png"),
                      load_image("pasiv/pasivv_5.png"),
                      load_image("pasiv/pasivv_6.png")]

        right_walk = [load_image("right_walk/right_walk_1.png"),
                      load_image("right_walk/right_walk_2.png"),
                      load_image("right_walk/right_walk_3.png"),
                      load_image("right_walk/right_walk_4.png")]

        left_walk = [load_image("left_walk/left_walk_1.png"),
                     load_image("left_walk/left_walk_2.png"),
                     load_image("left_walk/left_walk_3.png"),
                     load_image("left_walk/left_walk_4.png")]

        lose = [load_image("lose/lose_1.png"),
                load_image("lose/lose_2.png"),
                load_image("lose/lose_3.png"),
                load_image("lose/lose_4.png"),
                load_image("lose/lose_5.png"),
                load_image("lose/lose_6.png"),
                load_image("lose/lose_7.png"),
                load_image("lose/lose_8.png")]

        run_right = [load_image("right_run/right_run_1.png"),
                     load_image("right_run/right_run_2.png"),
                     load_image("right_run/right_run_3.png"),
                     load_image("right_run/right_run_4.png"),
                     load_image("right_run/right_run_5.png"),
                     load_image("right_run/right_run_6.png"),
                     load_image("right_run/right_run_7.png"),
                     load_image("right_run/right_run_8.png")]

        hide = [load_image("hide/hide_4.png"),
                load_image("hide/hide_3.png"),
                load_image("hide/hide_2.png"),
                load_image("hide/hide_1.png")]

        def __init__(self, x_pos, y_pos):
            super().__init__(hero_sprites, all_sprites)
            self.image = Hero.hero_pasiv[0]
            self.rect = self.image.get_rect()
            self.rect.x = x_pos
            self.rect.y = y_pos
            self.y_start = y_pos
            self.anim_count = 0
            self.condition = "hide"
            self.speed = 1
            self.jump_flg = False
            self.jump_size = 0
            self.HP = 3
            self.loser = False

        def update(self, *args):
            if self.condition == "hide":
                a_c = self.anim_count % 4
                self.image = Hero.hide[a_c]
                if self.anim_count == 8:
                    s_portal.play()
                    self.condition = "passiv"

            if self.condition == "passiv":
                self.anim_count = self.anim_count % 6
                self.image = Hero.hero_pasiv[self.anim_count]

            if self.condition == "left":
                self.anim_count = self.anim_count % 4
                self.image = Hero.left_walk[self.anim_count]

            if self.condition == "right":
                self.anim_count = self.anim_count % 8
                self.image = Hero.run_right[self.anim_count]

            if self.condition == "lose":
                if self.anim_count < 8:
                    self.image = Hero.lose[self.anim_count]

            if magic_hero.bullitcollide(bullit_m_sprite):
                magic_hero.HP_minus()
                if magic_hero.HP == 0:
                    s_HP_0.play()
                else:
                    s_HP_minus.play()
            self.life_update()

        def move(self):
            global hero_move_x, hero_move_y
            if self.loser:
                return

            if self.condition == "hide":
                return

            if self.condition == "passiv":
                hero_move_x = 0
                hero_move_y = 0

            if self.condition == "left":

                hero_move_x = -1 * self.speed
                if self.rect.x < 10:
                    hero_move_x = 0
                hero_move_y = 0

            if self.condition == "right":
                hero_move_x = 1 * self.speed
                if self.rect.x > 1550:
                    hero_move_x = 0
                hero_move_y = 0

            if self.jump_flg:
                self.speed = 15
                if self.jump_size > 0:
                    hero_move_y = (self.jump_size ** 2) // 2
                else:
                    hero_move_y = -1 * (self.jump_size ** 2) // 2

                self.jump_size += 1
                if self.jump_size == 12:
                    self.jump_flg = False
                    self.speed = 1
                    self.rect.y = self.y_start
                    hero_move_y = 0

            self.rect = self.rect.move(hero_move_x, hero_move_y)

        def jump(self):
            self.jump_flg = True
            self.jump_size = -12

        def life_update(self):
            if self.HP == 0:
                self.condition = "lose"
                self.loser = True

        def portal_collide(self):
            is_portal = pygame.sprite.spritecollideany(self, portal_sprite)
            if is_portal:
                StaticImg(images, 600, 50, 1)
                return True
            return False

        def bullitcollide(self, group):
            is_kill = pygame.sprite.spritecollideany(self, group)
            pygame.sprite.spritecollide(self, group, True)
            if is_kill:
                return True
            return False

        def HP_minus(self):
            self.HP -= 1
            for spr in heart_sprites:
                spr.kill()
            for i in range(self.HP):
                StaticImg(heart_sprites, 25 * i + 10, 50, 1)

    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height):
            super().__init__()
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class DeathWindow:
        def __init__(self):
            self.font = pygame.font.SysFont(None, 48)
            self.screen = pygame.display.set_mode((1700, 620))
            self.clock = pygame.time.Clock()

        def show(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return

                self.screen.fill((0, 0, 0))
                death_text = self.font.render("Вы проиграли!", True, (255, 255, 255))
                self.screen.blit(death_text, (150, 250))

                pygame.display.flip()
                self.clock.tick(30)

    platform1 = Platform(300, 400, 200, 20)
    platform2 = Platform(500, 300, 150, 20)
    platform3 = Platform(800, 200, 200, 20)
    platform4 = Platform(1100, 150, 150, 20)

    if __name__ == '__main__':
        pygame.init()
        clock = pygame.time.Clock()

        hero_move_speed = 1

        anim_counter_fish = 0
        anim_counter_hero = 0
        anim_counter_tornado = 0
        anim_counter_guardian = 0
        anim_counter_princ = 0
        Kolvo_level = 2

        s_kaplya = pygame.mixer.Sound('sound/effect/kaplya.wav')
        s_kaplya3 = pygame.mixer.Sound('sound/effect/kaplya3.wav')
        s_fire_bullit = pygame.mixer.Sound('sound/effect/fire_bullit.wav')
        s_HP_0 = pygame.mixer.Sound('sound/effect/HP_0.wav')
        s_HP_minus = pygame.mixer.Sound('sound/effect/HP_minus.wav')
        s_kvak = pygame.mixer.Sound('sound/effect/kvak.wav')
        s_portal = pygame.mixer.Sound('sound/effect/portal.wav')
        s_prygok = pygame.mixer.Sound('sound/effect/prygok.wav')
        s_veter = pygame.mixer.Sound('sound/effect/veter.wav')
        s_berserk = pygame.mixer.Sound('sound/effect/berserk.wav')

        hero_timer_anim = pygame.USEREVENT
        fish_timer_create = pygame.USEREVENT + 1
        fish_timer_anim = pygame.USEREVENT + 2
        portal_timer_create = pygame.USEREVENT + 3
        tornado_life_timer = pygame.USEREVENT + 4
        guardian_timer_anim = pygame.USEREVENT + 5
        tornado_life_anim = pygame.USEREVENT + 6
        fireprinc_attac_kd = pygame.USEREVENT + 7
        fireprinc_timer_anim = pygame.USEREVENT + 8
        waterEmpress_attac_kd = pygame.USEREVENT + 9
        waterEmpress_timer_anim = pygame.USEREVENT + 10
        # superr_kd = pygame.USEREVENT + 9

        pygame.time.set_timer(hero_timer_anim, 150)
        pygame.time.set_timer(fish_timer_anim, 100)
        pygame.time.set_timer(fish_timer_create, 4000)
        pygame.time.set_timer(tornado_life_timer, 7000)
        pygame.time.set_timer(tornado_life_anim, 100)
        pygame.time.set_timer(guardian_timer_anim, 100)
        pygame.time.set_timer(fireprinc_timer_anim, 100)
        pygame.time.set_timer(fireprinc_attac_kd, 1000)
        pygame.time.set_timer(waterEmpress_attac_kd, 1000)
        pygame.time.set_timer(waterEmpress_timer_anim, 100)
        # pygame.time.set_timer(superr_kd, 500)

        size = width, height = 1700, 620
        screen = pygame.display.set_mode(size)
        all_sprites = pygame.sprite.Group()
        background_sprite = pygame.sprite.Group()
        fish_sprites = pygame.sprite.Group()
        monsters_sprites = pygame.sprite.Group()
        hero_sprites = pygame.sprite.Group()
        images = pygame.sprite.Group()
        heart_sprites = pygame.sprite.Group()
        portal_sprite = pygame.sprite.Group()
        bullit_sprite = pygame.sprite.Group()
        bullit_m_sprite = pygame.sprite.Group()
        tornado_sprite = pygame.sprite.Group()
        platform_sprites = pygame.sprite.Group()
        platform_sprites.add(platform1, platform2, platform3, platform4)

        Nomer_Level = 0
        load_game = True
        end_of_level = False
        portal_not_exist = True

        running = True
        death_window = DeathWindow()
        while running:

            if load_game:
                Level(background_sprite, 0, Nomer_Level)
                Level(background_sprite, 1700, Nomer_Level)
                magic_hero = Hero(50, 400)
                for i in range(magic_hero.HP):
                    StaticImg(heart_sprites, 25 * i + 10, 50, 1)
                load_game = False

                if Nomer_Level == 0:
                    pygame.mixer.music.load('sound/musik/fish.mp3')
                    pygame.mixer.music.play(-1)
                    MonsterFish(fish_sprites, 350)
                    pygame.time.set_timer(portal_timer_create, 500)
                    portal_not_exist = True

                if Nomer_Level == 1:
                    pygame.mixer.music.load('sound/musik/prince.mp3')
                    pygame.mixer.music.play(-1)
                    Guardian_monster1 = Guardian(monsters_sprites, 1500, 50)
                    Guardian_monster2 = Guardian(monsters_sprites, 1400, 25)
                    Guardian_monster3 = Guardian(monsters_sprites, 1300, 400)
                    FirePrinc_monster = FirePrinc(monsters_sprites, 400, 280)
                    pygame.time.set_timer(portal_timer_create, 10000)
                    portal_not_exist = True

                if Nomer_Level == 2:
                    pygame.mixer.music.load('sound/musik/waterEmpress.mp3')
                    pygame.mixer.music.play(-1)
                    waterEmpress_monster = WaterEmpress(monsters_sprites, 400, 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    magic_hero.speed = 1
                    if not magic_hero.loser:
                        if magic_hero.condition != "hide":
                            magic_hero.condition = "passiv"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if not magic_hero.loser:
                            s_kaplya.play()
                            HeroBullit(bullit_sprite, magic_hero.rect.x + 100, magic_hero.rect.y + 70)

                    if event.key == pygame.K_q:
                        if not magic_hero.loser:
                            s_veter.play()
                            HeroBullitTornado(tornado_sprite, random.randint(100, 1500), 200)

                    if event.key == pygame.K_e:
                        # if event.type != superr_kd:
                        if not magic_hero.loser:
                            s_kaplya3.play()
                            for b in range(1, 4):
                                HeroBullitSuper(bullit_sprite, magic_hero.rect.x + 100, magic_hero.rect.y + 70, b)

                    if event.key == pygame.K_a:
                        magic_hero.condition = "left"

                    if event.key == pygame.K_d:
                        magic_hero.condition = "right"

                    if event.key == pygame.K_LSHIFT:
                        # crazy run 25 -  norm 3
                        magic_hero.speed = 25

                    if event.key == pygame.K_SPACE:
                        s_prygok.play()
                        if not magic_hero.jump_flg:
                            magic_hero.jump()

                    if event.key == pygame.K_f:
                        s_berserk.play()
                        StaticImg(images, 600, 50, 0)
                        pygame.time.set_timer(fish_timer_create, 500)

                    if event.key == pygame.K_n:
                        if magic_hero.loser:
                            # old level picture: you are LOSER? press "n"
                            Nomer_Level -= 1
                            end_of_level = True

                if event.type == tornado_life_anim:
                    anim_counter_tornado += 1
                    if anim_counter_tornado == 6:
                        anim_counter_tornado = 0

                if event.type == hero_timer_anim:
                    magic_hero.anim_count += 1
                    if magic_hero.anim_count == 30:
                        magic_hero.anim_count = 0
                        if magic_hero.loser:
                            magic_hero.anim_count = 8

                if event.type == fish_timer_anim:
                    anim_counter_fish += 1
                    if anim_counter_fish == 5:
                        anim_counter_fish = 0

                if Nomer_Level == 1:
                    if event.type == guardian_timer_anim:
                        anim_counter_guardian += 1
                        if anim_counter_guardian == 4:
                            anim_counter_guardian = 0

                    if event.type == fireprinc_timer_anim:
                        FirePrinc_monster.anim_count += 1
                        if FirePrinc_monster.anim_count == 30:
                            FirePrinc_monster.anim_count = 0

                    if event.type == fish_timer_create:  # время стрельбы такое же как рыбы
                        Guardian_monster1.gun()
                        Guardian_monster2.gun()
                        Guardian_monster3.gun()

                    if FirePrinc_monster.not_action:
                        FirePrinc_monster.random_action = random.randint(1, 7)
                        FirePrinc_monster.not_action = False

                if Nomer_Level == 2:
                    if event.type == waterEmpress_timer_anim:
                        waterEmpress_monster.anim_count += 1
                        if waterEmpress_monster.anim_count == 30:
                            waterEmpress_monster.anim_count = 0

                    if waterEmpress_monster.not_action:
                        waterEmpress_monster.random_action = random.randint(1, 7)
                        print(waterEmpress_monster.random_action)
                        waterEmpress_monster.not_action = False

                if event.type == tornado_life_timer:
                    for spr in tornado_sprite:
                        spr.kill()

                if event.type == portal_timer_create:
                    if portal_not_exist:
                        portal = Portal()
                        portal_not_exist = False

                if Nomer_Level == 0:
                    if event.type == fish_timer_create:
                        s_kvak.play()
                        fish_y = random.randint(50, 500)
                        MonsterFish(fish_sprites, fish_y)

            magic_hero.move()
            if not end_of_level:
                end_of_level = magic_hero.portal_collide()

            all_sprites.update()
            all_sprites.draw(screen)

            if end_of_level:
                magic_hero.condition = "hide"
                Nomer_Level += 1
                if Nomer_Level > Kolvo_level:
                    print("the end")
                    pygame.quit()
                load_game = True
                end_of_level = False
                for spr in all_sprites:
                    spr.kill()

            for platform in platform_sprites:
                screen.blit(platform.image, platform.rect)

            if magic_hero.HP == 0:  # Проверка смерти персонажа
                death_window.show()


            clock.tick(50)
            pygame.display.flip()


        pygame.quit()
    print("Игра запущена")

def show_settings_window():
    global selected_graphics_option, selected_sound_option

    while True:
        window.blit(background_image, (0, 0))

        settings_title = font.render('Settings', True, BLACK)
        settings_title_rect = settings_title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        window.blit(settings_title, settings_title_rect)

        graphics_label = font.render('Graphics Settings:', True, BLACK)
        graphics_label_rect = graphics_label.get_rect(topleft=(100, 100))
        window.blit(graphics_label, graphics_label_rect)

        option_rects = []
        for i, option in enumerate(graphics_options):
            option_label = font.render(option, True, BLACK)
            option_rect = option_label.get_rect(topleft=(120, 150 + i * 50))
            window.blit(option_label, option_rect.topleft)
            option_rects.append(option_rect)
            if i == selected_graphics_option:
                pygame.draw.rect(window, BLACK, option_rect, 2)

        sound_label = font.render('Sound Settings:', True, BLACK)
        sound_label_rect = sound_label.get_rect(topleft=(100, 300))
        window.blit(sound_label, sound_label_rect)

        sound_option_label = font.render(sound_options[selected_sound_option], True, BLACK)
        sound_option_rect = sound_option_label.get_rect(topleft=(120, 350))
        window.blit(sound_option_label, sound_option_rect.topleft)

        current_time = datetime.now().strftime("%H:%M:%S")
        time_label = font.render('Local Time: ' + current_time, True, BLACK)
        time_label_rect = time_label.get_rect(topleft=(100, 500))
        window.blit(time_label, time_label_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, option_rect in enumerate(option_rects):
                    if option_rect.collidepoint(event.pos):
                        selected_graphics_option = i

                if sound_option_rect.collidepoint(event.pos):
                    selected_sound_option = (selected_sound_option + 1) % len(sound_options)

        pygame.display.flip()


def show_character_history_window():
    global window

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    SCREEN_WIDTH = 750
    SCREEN_HEIGHT = 470

    character_window = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    character_window.fill(WHITE)

    background_image = pygame.image.load("background_image.jpg")
    character_window.blit(background_image, (0, 0))

    character_image = pygame.image.load("2024-02-22 21.43.26.png")
    character_window.blit(character_image, (20, 120))
    character_image = pygame.image.load("2024-02-27 18.48.34.png")
    character_window.blit(character_image, (90, 120))
    character_image = pygame.image.load("2024-02-27 18.51.38.png")
    character_window.blit(character_image, (160, 120))
    character_image = pygame.image.load("2024-02-27 18.52.29.png")
    character_window.blit(character_image, (230, 120))
    character_image = pygame.image.load("2024-02-27 18.53.40.png")
    character_window.blit(character_image, (300, 120))
    character_image = pygame.image.load("2024-02-27 18.54.16.png")
    character_window.blit(character_image, (370, 120))

    font = pygame.font.SysFont("Arial", 20)

    with open('game_story.txt', 'r') as file:
        game_story = file.readlines()

    with open('character_description.txt', 'r') as file:
        character_story = file.readlines()

    def draw_text(text_list, x, y):
        for i, line in enumerate(text_list):
            text_surface = font.render(line.strip(), True, BLACK)
            character_window.blit(text_surface, (x, y + i * 25))

    draw_text(game_story, 10, 10)
    draw_text(character_story, 10, SCREEN_HEIGHT - 280)

    window.blit(character_window, (25, 25))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


while True:
    window.blit(background_image, (0, 0))

    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render('Exploit', True, BLACK)
    title_text_shadow = title_font.render('Exploit', True, (50, 50, 50))

    title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    title_text_shadow_rect = title_text_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 3, 53))

    window.blit(title_text_shadow, title_text_shadow_rect)
    window.blit(title_text, title_text_rect)

    start_button = pygame.Rect(300, 200, 200, 50)
    settings_button = pygame.Rect(300, 300, 200, 50)
    exit_button = pygame.Rect(300, 400, 200, 50)
    history_button = pygame.Rect(300, 500, 200, 50)

    window.blit(start_button_image, (300, 200))
    window.blit(settings_button_image, (300, 300))
    window.blit(exit_button_image, (300, 400))
    window.blit(history_button_image, (300, 500))

    start_text = font.render('Start', True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button.center)
    window.blit(start_text, start_text_rect)

    settings_text = font.render('Settings', True, BLACK)
    settings_text_rect = settings_text.get_rect(center=settings_button.center)
    window.blit(settings_text, settings_text_rect)

    exit_text = font.render('Exit', True, BLACK)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    window.blit(exit_text, exit_text_rect)

    history_text = font.render('History', True, BLACK)
    history_text_rect = history_text.get_rect(center=history_button.center)
    window.blit(history_text, history_text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                print("Start button clicked")
                run_game()
            elif settings_button.collidepoint(event.pos):
                print("Settings button clicked")
                show_settings_window()
            elif exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif history_button.collidepoint(event.pos):
                print("History button clicked")
                show_character_history_window()

    pygame.display.flip()