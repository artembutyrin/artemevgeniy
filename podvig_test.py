import os
import sys
import random
import pygame


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

    def update(self, *args):
        pass


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

    def update(self, *args):
        pass


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

    """left_run = [load_image("left_run/left_run_1.png"),
                load_image("left_run/left_run_2.png"),
                load_image("left_run/left_run_3.png"),
                load_image("left_run/left_run_4.png"),
                load_image("left_run/left_run_5.png"),
                load_image("left_run/left_run_6.png"),
                load_image("left_run/left_run_7.png"),
                load_image("left_run/left_run_8.png")]"""

    procast = [load_image("procast/procast_1.png"),
               load_image("procast/procast_2.png"),
               load_image("procast/procast_3.png"),
               load_image("procast/procast_4.png"),
               load_image("procast/procast_5.png"),
               load_image("procast/procast_6.png"),
               load_image("procast/procast_7.png"),
               load_image("procast/procast_8.png")]

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


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    hero_move_speed = 1

    anim_counter_fish = 0
    anim_counter_hero = 0
    anim_counter_tornado = 0
    anim_counter_guardian = 0
    anim_counter_princ = 0
    Kolvo_level = 1

    hero_timer_anim = pygame.USEREVENT
    fish_timer_create = pygame.USEREVENT + 1
    fish_timer_anim = pygame.USEREVENT + 2
    portal_timer_create = pygame.USEREVENT + 3
    tornado_life_timer = pygame.USEREVENT + 4
    guardian_timer_anim = pygame.USEREVENT + 5
    tornado_life_anim = pygame.USEREVENT + 6
    fireprinc_attac_kd = pygame.USEREVENT + 7
    fireprinc_timer_anim = pygame.USEREVENT + 8
    # superr_kd = pygame.USEREVENT + 9

    pygame.time.set_timer(hero_timer_anim, 150)
    pygame.time.set_timer(fish_timer_anim, 100)
    pygame.time.set_timer(fish_timer_create, 4000)
    pygame.time.set_timer(tornado_life_timer, 7000)
    pygame.time.set_timer(tornado_life_anim, 100)
    pygame.time.set_timer(guardian_timer_anim, 100)
    pygame.time.set_timer(fireprinc_timer_anim, 100)
    pygame.time.set_timer(fireprinc_attac_kd, 1000)
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

    Nomer_Level = 0
    load_game = True
    end_of_level = False
    portal_not_exist = True

    running = True
    while running:

        if load_game:
            Level(background_sprite, 0, Nomer_Level)
            Level(background_sprite, 1700, Nomer_Level)
            magic_hero = Hero(50, 400)
            for i in range(magic_hero.HP):
                StaticImg(heart_sprites, 25 * i + 10, 50, 1)
            load_game = False

            if Nomer_Level == 0:
                MonsterFish(fish_sprites, 350)
                pygame.time.set_timer(portal_timer_create, 500)
                portal_not_exist = True

            if Nomer_Level == 1:
                Guardian_monster1 = Guardian(monsters_sprites, 1500, 50)
                Guardian_monster2 = Guardian(monsters_sprites, 1400, 25)
                Guardian_monster3 = Guardian(monsters_sprites, 1300, 400)
                FirePrinc_monster = FirePrinc(monsters_sprites, 400, 280)
                pygame.time.set_timer(portal_timer_create, 10000)
                portal_not_exist = True

            if Nomer_Level == 2:
                pass

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
                        HeroBullit(bullit_sprite, magic_hero.rect.x + 100, magic_hero.rect.y + 70)

                if event.key == pygame.K_q:
                    if not magic_hero.loser:
                        HeroBullitTornado(tornado_sprite, random.randint(100, 1500), 200)

                if event.key == pygame.K_e:
                    # if event.type != superr_kd:
                    if not magic_hero.loser:
                        for b in range(1, 4):
                            HeroBullitSuper(bullit_sprite, magic_hero.rect.x + 100, magic_hero.rect.y + 70, b)
                if event.key == pygame.K_a:
                    magic_hero.condition = "left"

                if event.key == pygame.K_d:
                    magic_hero.condition = "right"

                if event.key == pygame.K_LSHIFT:
                    # crazy run 25 -  norm 3
                    magic_hero.speed = 3

                if event.key == pygame.K_SPACE:
                    if not magic_hero.jump_flg:
                        magic_hero.jump()
                if event.key == pygame.K_f:
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

                # if event.type == fireprinc_attac_kd:
                if FirePrinc_monster.not_action:
                    FirePrinc_monster.random_action = random.randint(1, 7)
                    FirePrinc_monster.not_action = False

            if event.type == tornado_life_timer:
                for spr in tornado_sprite:
                    spr.kill()

            if event.type == portal_timer_create:
                if portal_not_exist:
                    portal = Portal()
                    portal_not_exist = False

            if Nomer_Level == 0:
                if event.type == fish_timer_create:
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

        clock.tick(50)
        pygame.display.flip()

    pygame.quit()
