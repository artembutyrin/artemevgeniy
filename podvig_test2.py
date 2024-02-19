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
             load_image("static_img/heart.png")]

    def __init__(self, group, x_pos, y_pos, nom):
        super().__init__(group, all_sprites)
        self.image = StaticImg.image[nom]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self, *args):
        pass


class Level(pygame.sprite.Sprite):
    background = [load_image("background_3.jpg"),
                  load_image("background_2.jpg")]

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
    
    def testcollide(self, group, kill_self):
        is_kill = pygame.sprite.spritecollideany(self, group)
        pygame.sprite.spritecollide(self, group, True)
        if is_kill and kill_self:
            self.kill()
            
    def update(self, *args):
        self.rect = self.rect.move(3, 0)
 
    
class MonsterBullit(FlyObj):
    image = load_image("static_img/heart.png")
    def __init__(self, group, pos_x, pos_y):
        super().__init__(bullit_m_sprite, all_sprites)
        self.image = MonsterBullit.image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    
    def update(self, *args):
        self.rect = self.rect.move(-6, 0)
        self.testcollide(hero_sprites, True)        
        
        
class HeroBullit(FlyObj):
    image = load_image("static_img/heart.png")
    def __init__(self, group, pos_x, pos_y):
        super().__init__(bullit_sprite, all_sprites)
        self.image = HeroBullit.image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    
    def update(self, *args):
        self.rect = self.rect.move(3, 0)
        self.testcollide(monsters_sprites, True)
       
        
class HeroBullitSuper(HeroBullit):
    image = load_image("static_img/heart.png")
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
    image = load_image("static_img/tornado.png")
    def __init__(self, group, pos_x, pos_y):
        super().__init__(tornado_sprite, all_sprites)
        self.image = HeroBullitTornado.image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    
    def update(self, *args):
        #self.rect = self.rect.move(3, 0)
        self.testcollide(monsters_sprites, False)
        

class Portal(pygame.sprite.Sprite):
    image = load_image("static_img/portal.png")

    def __init__(self):
        super().__init__(portal_sprite, all_sprites)
        self.image = Portal.image
        self.rect = self.image.get_rect()
        self.rect.x = 1600
        self.rect.y = 450
        
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
            magic_hero.HP -= 1
            for spr in heart_sprites:
                spr.kill()
            for i in range(magic_hero.HP):
                StaticImg(heart_sprites, 25 * i + 10, 50, 1)
            self.kill()
                
        
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
            
        
class MonsterNew(Monsters):
    
    new_monster = [load_image("fish_monster/fish_monster_1.png"),
                    load_image("fish_monster/fish_monster_2.png"),
                    load_image("fish_monster/fish_monster_3.png"),
                    load_image("fish_monster/fish_monster_4.png"),
                    load_image("fish_monster/fish_monster_5.png"),
                    load_image("fish_monster/fish_monster_6.png")]

    def __init__(self, group, y_pos):
        super().__init__(group, y_pos)
        self.image = MonsterNew.new_monster[0]
        
    def update(self, *args):
        self.image = MonsterNew.new_monster[anim_counter_fish]
        #anim_counter_fish сделать свой
        self.rect.x = 1530
        #self.rect = self.rect.move(0, 0)
        self.testcollide()
    
    def gun(self):
        MonsterBullit(bullit_m_sprite, self.rect.x - 100, self.rect.y + 30)
        
        
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
                 
        self.life_update()
        
    def move(self):
        if self.loser:
            return
        
        if self.condition == "hide":
            return
        
        if self.condition == "passiv":
            hero_move_x = 0 
            hero_move_y = 0
                
        if self.condition == "left":
            hero_move_x = -1 * self.speed
            hero_move_y = 0
            
        if self.condition == "right":
            hero_move_x = 1 * self.speed
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


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    
    hero_move_speed = 1
    
    anim_counter_fish = 0
    anim_counter_hero = 0
    
    hero_timer_anim = pygame.USEREVENT
    fish_timer_create = pygame.USEREVENT + 1
    fish_timer_anim = pygame.USEREVENT + 2
    portal_timer_create = pygame.USEREVENT + 3
    tornado_life_timer = pygame.USEREVENT + 4
    
    pygame.time.set_timer(hero_timer_anim, 150)
    pygame.time.set_timer(fish_timer_anim, 100)
    pygame.time.set_timer(fish_timer_create, 4000)
    pygame.time.set_timer(tornado_life_timer, 3000)
    
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
                mmmm = MonsterNew(fish_sprites, 100)
                print("mmmm")
                pygame.time.set_timer(portal_timer_create, 5000)
                portal_not_exist = True

        
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
                    HeroBullit(bullit_sprite, magic_hero.rect.x + 100, magic_hero.rect.y + 70)
                if event.key == pygame.K_q:
                    HeroBullitTornado(tornado_sprite, 750, 200)
                    #запуск по позиции мышки
                if event.key == pygame.K_e:
                    for b in range(1, 4):
                        HeroBullitSuper(bullit_sprite, magic_hero.rect.x + 100, magic_hero.rect.y + 70, b)
                if event.key == pygame.K_a:
                    magic_hero.condition = "left"
                if event.key == pygame.K_d:
                    magic_hero.condition = "right"
                if event.key == pygame.K_LSHIFT:
                    magic_hero.speed = 15
                if event.key == pygame.K_SPACE:
                    if not magic_hero.jump_flg:
                        magic_hero.jump() 
                if event.key == pygame.K_f:
                    StaticImg(images, 600, 50, 0)
                    pygame.time.set_timer(fish_timer_create, 500)
                if event.key == pygame.K_n:
                    if magic_hero.loser:
                        #old level picture: you are LOSER? press "n"
                        Nomer_Level -= 1
                        end_of_level = True
                    
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
                    
            if event.type == tornado_life_timer:
                ###
                if Nomer_Level == 1:
                    mmmm.gun()
                ###
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
            load_game = True
            end_of_level = False
            for spr in all_sprites:
                spr.kill()
        
        clock.tick(50)
        pygame.display.flip()
        
    pygame.quit()