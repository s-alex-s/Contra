import pygame
from random import randint
from load_pictures import *


def start_screen():
    def text_render():
        fon = pygame.transform.scale(load_image('start_screen.jpg', name='screens'), (420, 400))
        screen.blit(fon, (0, 0))
        text_coord = 200
        text_image = load_image('contra_logo.png', name='screens', n_scale_divided=2)
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 100
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        screen.blit(sounds_mode_txt, (20, 360))
        screen.blit(text_image, (20, 20))

    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '450,330'
    font = pygame.font.Font(None, 30)
    size = a, b = 420, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Contra')
    clock = pygame.time.Clock()
    FPS = 60
    character = "Bill"
    sounds_mode = 'Standard'
    start_sound = pygame.mixer.Sound('data/sounds/start_level.wav')
    start_sound.set_volume(0.06)
    pygame.mixer.music.load('data/sounds/main_menu.wav')
    pygame.mixer.music.set_volume(0.07)
    pygame.mixer.music.play()
    sounds_mode_txt = font.render('Звуки: Стандартные', True, pygame.Color('white'))
    intro_text = ["       Выбор персонажа",
                  "        -> Bill Rizer",
                  "           Lance Bean"]
    text_render()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused():
                    pygame.mouse.set_visible(False)
                else:
                    pygame.mouse.set_visible(True)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro_text = ["       Выбор персонажа",
                                  "           Bill Rizer",
                                  "        -> Lance Bean"]
                    text_render()
                    character = "Lance"
                elif event.key == pygame.K_w:
                    intro_text = ["       Выбор персонажа",
                                  "        -> Bill Rizer",
                                  "           Lance Bean"]
                    text_render()
                    character = "Bill"
                elif event.key == pygame.K_a:
                    sounds_mode_txt = font.render('Звуки: Стандартные', True, pygame.Color('white'))
                    if sounds_mode != 'Standard':
                        pygame.mixer.music.load('data/sounds/main_menu.wav')
                        pygame.mixer.music.set_volume(0.07)
                        pygame.mixer.music.play()
                    start_sound = pygame.mixer.Sound('data/sounds/start_level.wav')
                    start_sound.set_volume(0.06)
                    sounds_mode = 'Standard'
                    text_render()
                elif event.key == pygame.K_d:
                    sounds_mode_txt = font.render('Звуки: DOOM', True, pygame.Color('white'))
                    if sounds_mode != 'DOOM':
                        random_music_num = randint(1, 2)
                        if random_music_num == 1:
                            pygame.mixer.music.load('data/sounds/main_menu_DOOM.wav')
                            pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play()
                        elif random_music_num == 2:
                            pygame.mixer.music.load('data/sounds/main_menu_OLD_DOOM.mp3')
                            pygame.mixer.music.set_volume(0.06)
                            pygame.mixer.music.play()
                    start_sound = pygame.mixer.Sound('data/sounds/start_level_DOOM.wav')
                    start_sound.set_volume(0.06)
                    sounds_mode = 'DOOM'
                    text_render()
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    start_sound.play()
                    return character, sounds_mode
        pygame.display.flip()
        clock.tick(FPS)


def you_win_screen():
    fon = pygame.transform.scale(load_image('start_screen.jpg', name='screens'), (1000, 352))
    text = load_image('you_win_text.png', name='screens')
    size = x, y = 1000, 352
    screen = pygame.display.set_mode(size)
    screen.blit(fon, (0, 0))
    screen.blit(text, (400, 170))
    clock = pygame.time.Clock()

    pygame.mixer.music.stop()
    if sounds_mode == 'Standard':
        win_music = pygame.mixer.Sound('data/sounds/win.wav')
    elif sounds_mode == 'DOOM':
        win_music = pygame.mixer.Sound('data/sounds/win_and_lose_DOOM.wav')

    win_music.set_volume(0.04)
    win_music.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
        pygame.display.flip()


def game_over_screen():
    fon = pygame.transform.scale(load_image('start_screen.jpg', name='screens'), (1000, 352))
    text = load_image('game_over.png', name='screens')
    size = x, y = 1000, 352
    screen = pygame.display.set_mode(size)
    screen.blit(fon, (0, 0))
    screen.blit(text, (350, 150))
    clock = pygame.time.Clock()

    pygame.mixer.music.stop()
    if sounds_mode == 'Standard':
        game_over_music = pygame.mixer.Sound('data/sounds/game_over.wav')
    elif sounds_mode == 'DOOM':
        game_over_music = pygame.mixer.Sound('data/sounds/win_and_lose_DOOM.wav')

    game_over_music.set_volume(0.04)
    game_over_music.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
        pygame.display.flip()


class Animation(pygame.sprite.Sprite):

    def change_anim(self, img, columns, rows, rever=False):
        self.frames = []
        self.cut_sheet(img, columns, rows, self.rect.x, self.rect.y, rever)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows, x, y, rever=False):
        self.rect = pygame.Rect(x, y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        if rever is not False:
            self.frames = self.frames[::-1]


class Hp_count(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(1100, 20)

    def update_hp(self, pos, hp):
        self.rect.x = pos[0] - 460
        self.rect.y = 20
        if hp == 1:
            self.image = load_image('2_hp.png', name='Bill', n_scale_multiply=2)
        if hp == 2:
            self.image = load_image('1_hp.png', name='Bill', n_scale_multiply=2)


class Bill(Animation):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.xv = 0
        self.yv = 0
        self.x = 0
        self.onGround = False
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.count_iter = 0
        self.current_animation = 'stand'
        self.damage = 0
        self.isDamage = False

    def collide(self, xv, yv):
        for p in platform_group:
            if pygame.sprite.collide_rect(self, p):
                if xv > 0:
                    self.rect.right -= MOVE_SPEED
                    self.x -= MOVE_SPEED
                if xv < 0:
                    self.rect.left += MOVE_SPEED
                    self.x += MOVE_SPEED
                if yv > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yv = 0
                if yv < 0:
                    self.rect.top = p.rect.bottom
                    self.yv = 0

        for p in bridge_group:
            if pygame.sprite.collide_rect(self, p):
                if yv > 0:
                    self.rect.bottom = p.rect.top + 1
                    self.onGround = True
                    self.yv = 0

        if pygame.sprite.spritecollideany(self, water_group):
            game_over_screen()

    def get_pos(self):
        return self.rect.x, self.rect.y, self.x

    def get_hp(self):
        return self.damage

    def take_damage(self):
        self.isDamage = False
        for bullet in enemy_bullet_group:
            if pygame.sprite.collide_rect(self, bullet):
                self.damage += 1
                bullet.kill()
                if self.damage == 3:
                    game_over_screen()
                    self.kill()
                self.isDamage = True

    def update(self, left, right, up):
        global player
        global player_image

        if up:
            if self.onGround:
                self.yv = -JUMP_POWER
                if self.current_animation != 'jump' and self.onGround:
                    player_image = load_image('Bill_jumping.png', name=person)
                    player.change_anim(player_image, 4, 1)
                    self.current_animation = 'jump'
        if left and not right:
            self.xv = -MOVE_SPEED
            if up:
                if self.current_animation != 'jump':
                    player_image = load_image('Bill_jumping.png', name=person, flip=True)
                    player.change_anim(player_image, 4, 1, rever=True)
                    self.current_animation = 'jump'
            elif self.current_animation != 'left':
                player_image = load_image('Bill_walking.png', name=person, flip=True)
                player.change_anim(player_image, 6, 1, rever=True)
                self.current_animation = 'left'
        if right and not left:
            self.xv = MOVE_SPEED
            if up:
                if self.current_animation != 'jump':
                    player_image = load_image('Bill_jumping.png', name=person)
                    player.change_anim(player_image, 4, 1)
                    self.current_animation = 'jump'
            elif self.current_animation != 'right':
                player_image = load_image('Bill_walking.png', name=person)
                player.change_anim(player_image, 6, 1)
                self.current_animation = 'right'
        if (not (left or right)) or (left and right):
            self.xv = 0
            if self.current_animation != 'stand':
                self.current_animation = 'stand'

        if self.count_iter == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count_iter = 0
        self.count_iter += 1

        if not self.onGround:
            self.yv += GRAVITY
        self.onGround = False
        self.rect.y += self.yv
        self.collide(0, self.yv)

        self.rect.x += self.xv
        self.x += self.xv
        self.collide(self.xv, 0)
        self.take_damage()


class Gromaides(Animation):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        if sounds_mode == 'Standard':
            self.shoot_sound = pygame.mixer.Sound('data/sounds/boss_shoot.wav')
            self.boss_crashed_sound = pygame.mixer.Sound('data/sounds/boss_crashed.wav')
        else:
            self.shoot_sound = pygame.mixer.Sound('data/sounds/boss_shoot_DOOM.wav')
            self.boss_crashed_sound = pygame.mixer.Sound('data/sounds/boss_crashed_DOOM.wav')
        self.shoot_sound.set_volume(0.06)
        self.boss_crashed_sound.set_volume(0.06)
        self.count_iter = 0
        self.count_iter2 = 0
        self.attack = False
        self.close_mouth = True
        self.start = False
        self.anim_is_change = False
        self.damage = 0
        self.isDamage = False
        self.isDead = False

    def get_pos(self):
        return self.rect.x, self.rect.y

    def boss_is_dead(self):
        return self.isDead

    def lets_attack(self):
        self.start = True
        self.attack = True

    def take_damage(self):
        self.isDamage = False
        for bullet in bullet_group:
            if (self.rect.x + 150 <= bullet.rect.x <= self.rect.x + 240) and (self.rect.y + 90 >= bullet.rect.y) \
                    and not self.isDead:
                self.damage += 1
                bullet.kill()
                if self.damage == 15:
                    self.isDead = True
                    self.start = False
                    self.attack = False
                    pygame.mixer.music.stop()
                    self.boss_crashed_sound.play()
                    self.change_anim(load_image('crashed.png', name='Gromaides_BOSS', n_scale_plus=96, n_plus_wide=53),
                                     1, 1)

                    n = 0
                    for boom in range(4):
                        Explosion(load_image('boom.png', name='Explosions', n_scale_multiply=3), 3, 1,
                                  self.rect.x + 128, self.rect.y + n, 30)
                        n += 60
                    n = 0
                    for boom in range(4):
                        Explosion(load_image('boom.png', name='Explosions', n_scale_multiply=3), 3, 1,
                                  self.rect.x + 228, self.rect.y + n, 30)
                        n += 60

                self.isDamage = True

    def closed_mouth(self):
        if not self.anim_is_change:
            self.change_anim(load_image('Gromaides.png', name='Gromaides_BOSS', n_scale_plus=300), 2, 3, rever=True)
            self.anim_is_change = True
        if self.count_iter2 == 6:
            if self.cur_frame == len(self.frames) - 1:
                self.change_anim(load_image('closed_mouth.png', name='Gromaides_BOSS', n_scale_plus=96,
                                            n_plus_wide=53), 1, 1)
                self.attack = True
                self.anim_is_change = False
                if self.attack:
                    Boss_bullet(load_image('boss_boom.png', name='Gromaides_BOSS', n_scale_multiply=2), 4, 1,
                                self.rect.x + 115,
                                self.rect.y + 95, 4, 3)
                    Boss_bullet(load_image('boss_boom.png', name='Gromaides_BOSS', n_scale_multiply=2), 4, 1,
                                self.rect.x + 265,
                                self.rect.y + 95, -4, 3)
            if not self.attack:
                self.cur_frame = self.cur_frame + 1
                self.image = self.frames[self.cur_frame]
            self.count_iter2 = 0
        self.count_iter2 += 1

    def shooting(self):
        if not self.anim_is_change:
            self.change_anim(load_image('Gromaides.png', name='Gromaides_BOSS', n_scale_plus=300), 2, 3)
            self.anim_is_change = True

        if self.count_iter == 6:
            if self.cur_frame == len(self.frames) - 1:
                Boss_bullet(load_image('boss_boom.png', name='Gromaides_BOSS', n_scale_multiply=2), 4, 1,
                            self.rect.x + 188,
                            self.rect.y + 60, -3, 3)
                Boss_bullet(load_image('boss_boom.png', name='Gromaides_BOSS', n_scale_multiply=2), 4, 1,
                            self.rect.x + 188,
                            self.rect.y + 60, 0, 3)
                Boss_bullet(load_image('boss_boom.png', name='Gromaides_BOSS', n_scale_multiply=2), 4, 1,
                            self.rect.x + 188,
                            self.rect.y + 60, 3, 3)
                self.shoot_sound.play()
                self.attack = False
                self.anim_is_change = False
            if self.attack:
                self.cur_frame = self.cur_frame + 1
                self.image = self.frames[self.cur_frame]
            self.count_iter = 0
        self.count_iter += 1

    def update(self, left, right, up):
        self.take_damage()
        if self.attack:
            self.shooting()
        elif self.start:
            self.closed_mouth()


class Boss_bullet(Animation):
    def __init__(self, sheet, columns, rows, x, y, xv, yv):
        super().__init__(all_sprites, enemy_bullet_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.count_iter = 0
        self.xv = xv
        self.yv = yv

    def update(self, left, right, up):
        self.rect.x += self.xv
        self.rect.y += self.yv
        if self.count_iter == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count_iter = 0
        self.count_iter += 1
        if self.rect.y > 352:
            self.kill()


class Helicopter(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def get_pos(self):
        return self.rect.x

    def update_helicopter(self):
        self.rect.x += 5


soldiers = [[50 * 32, 5 * 32, 5 * 32 - 10, "alive"],
            [70 * 32, 5 * 32, 5 * 32 - 10, "alive"],
            [86 * 32, 4 * 32, 7 * 32 - 10, "alive"],
            [117 * 32, 5 * 32, 5 * 32 - 10, "alive"]]
snipers = [[60 * 32, 2 * 32, "alive"], [71 * 32, 2 * 32, "alive"],
           [42 * 32, 7 * 32, "alive"], [96 * 32, 7 * 32, "alive"],
           [126 * 32, 8 * 32, "alive"], [137 * 32, 8 * 32, "alive"]]
alien_egg = [[62 * 32, 2 * 32], [81 * 32, 5 * 32],
             [108 * 32, 5 * 32], [94 * 32, 5 * 32],
             [122 * 32, 6 * 32], [133 * 32, 5 * 32]]
aliens = [[59 * 32, 2 * 32, 5 * 32 - 10], [81 * 32, 5 * 32, 2 * 32 - 10],
          [108 * 32, 5 * 32, 2 * 32 - 10], [94 * 32, 5 * 32, 4 * 32 - 10],
          [122 * 32, 6 * 32, 3 * 32 - 10], [133 * 32, 5 * 32, 3 * 32 - 10]]


class Soldier(Animation):
    def __init__(self, image, columns, rows, x_pos, y_pos, count, number):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(image, columns, rows, x_pos, y_pos)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x_pos, y_pos)
        self.change = 0
        self.count = count
        self.side = "right"
        self.move = True
        self.wait = 20
        self.kil = False
        self.damage = 0
        self.current_animation = 'right'
        self.count_iter = 0
        self.count_iter1 = 0
        self.number = number

    def wait_bullet(self, left, top, center=False):
        self.move = False
        self.wait -= 1
        if self.wait == 0 and self.kil is False:
            self.attack(left, top, center)
            self.wait = 15

    def attack(self, left, top, center=False):
        self.move = False
        enemy_bullets.append(BulletEnemy(tile_images["bullet"], self.rect.x, self.rect.y, left, top, center))

    def update_soldier(self):
        global soldiers
        global enemy_bullets
        global soldier_image

        if self.change >= self.count:
            self.change = 0
            if self.side == "right":
                self.side = "left"
            else:
                self.side = "right"
        if self.side == "right" and self.move is True:
            self.rect.x += 3
            self.change += 3
            if self.current_animation != 'right':
                soldier_image = load_image('soldier_go.png', name="Soldier", flip=True)
                self.change_anim(soldier_image, 6, 1, rever=True)
                self.current_animation = 'right'
        elif self.side == "left" and self.move is True:
            self.rect.x -= 3
            self.change += 3
            if self.current_animation != 'left':
                soldier_image = load_image('soldier_go.png', name="Soldier")
                self.change_anim(soldier_image, 6, 1)
                self.current_animation = 'left'
        if -128 <= self.rect.x - player.rect.x <= 128 and -128 <= self.rect.y - player.rect.y <= 128:
            if self.rect.x > player.rect.x and (self.rect.y - 3 == player.rect.y or self.rect.y - 5 == player.rect.y):
                self.wait_bullet(True, False, True)
                soldier_image = load_image('shoot_stand.png', name="Soldier")
                self.change_anim(soldier_image, 1, 1)
            elif self.rect.x < player.rect.x and (self.rect.y - 3 == player.rect.y or self.rect.y - 5 == player.rect.y):
                self.wait_bullet(False, False, True)
                soldier_image = load_image('shoot_stand.png', name="Soldier", flip=True)
                self.change_anim(soldier_image, 1, 1, rever=True)
        else:
            self.move = True
        self.take_damage()
        if self.count_iter == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count_iter = 0
        self.count_iter += 1
        return False

    def take_damage(self):
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(self, bullet) and self.kil is False:
                self.damage += 1
                bullet.kill()
            if self.damage == 3:
                self.kil = True
                soldiers[self.number] = "dead"
                if self.count_iter1 == 9:
                    enemy_dead_sound.play()
                    self.kill()
                if self.count_iter1 == 6:
                    self.image = load_image('3_boom.png', name="Explosions")
                if self.count_iter1 == 3:
                    self.image = load_image('2_boom.png', name="Explosions")
                if self.count_iter1 == 1:
                    self.image = load_image('1_boom.png', name="Explosions")
                self.count_iter1 += 1


class Sniper(Animation):
    def __init__(self, image, columns, rows, x_pos, y_pos, number):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(image, columns, rows, x_pos, y_pos)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x_pos, y_pos)
        self.wait = 20
        self.kil = False
        self.damage = 0
        self.change = False
        self.last = "left"
        self.count_iter = 0
        self.number = number

    def wait_bullet(self, left, top, center=False):
        self.move = False
        self.wait -= 1
        if self.wait == 0 and self.kil is False:
            self.attack(left, top, center)
            self.wait = 15

    def attack(self, left, top, center=False):
        enemy_bullets.append(BulletEnemy(tile_images["bullet"], self.rect.x, self.rect.y, left, top, center))

    def update_sniper(self):
        global snipers
        global enemy_bullets
        global sniper_image
        global sniper

        if self.change is True:
            self.change = False
            self.rect.y += 8
        if -128 <= self.rect.x - player.rect.x <= 128 and -128 <= self.rect.y - player.rect.y <= 128:
            if self.rect.x > player.rect.x and (self.rect.y - 3 == player.rect.y or self.rect.y - 5 == player.rect.y):
                self.wait_bullet(True, False, True)
                self.last = "left"
                sniper_image = load_image('shoot_center.png', name="Sniper")
                self.change_anim(sniper_image, 1, 1)
            elif self.rect.x < player.rect.x and (self.rect.y - 3 == player.rect.y or self.rect.y - 5 == player.rect.y):
                self.wait_bullet(False, False, True)
                self.last = "right"
                sniper_image = load_image('shoot_center.png', name="Sniper", flip=True)
                self.change_anim(sniper_image, 1, 1, rever=True)
            elif self.rect.x > player.rect.x and self.rect.y < player.rect.y:
                self.wait_bullet(True, False)
                self.last = "left"
                sniper_image = load_image('shooting_down.png', name="Sniper")
                self.change_anim(sniper_image, 1, 1)
            elif self.rect.x < player.rect.x and self.rect.y < player.rect.y:
                self.wait_bullet(False, False)
                self.last = "right"
                sniper_image = load_image('shooting_down.png', name="Sniper", flip=True)
                self.change_anim(sniper_image, 1, 1, rever=True)
            elif self.rect.x > player.rect.x and self.rect.y > player.rect.y:
                self.wait_bullet(True, True)
                self.last = "left"
                self.rect.y -= 8
                self.change = True
                sniper_image = load_image('shoot_up.png', name="Sniper")
                self.change_anim(sniper_image, 1, 1)
            elif self.rect.x < player.rect.x and self.rect.y > player.rect.y:
                self.wait_bullet(False, True)
                self.last = "right"
                self.rect.y -= 8
                self.change = True
                sniper_image = load_image('shoot_up.png', name="Sniper", flip=True)
                self.change_anim(sniper_image, 1, 1, rever=True)
        else:
            if self.last == "right":
                sniper_image = load_image('shoot_center.png', name="Sniper", flip=True)
                self.change_anim(sniper_image, 1, 1, rever=True)
            else:
                sniper_image = load_image('shoot_center.png', name="Sniper")
                self.change_anim(sniper_image, 1, 1)
        self.take_damage()

    def take_damage(self):
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(self, bullet) and self.kil is False:
                self.damage += 1
                bullet.kill()
        if self.damage == 3:
            self.kil = True
            snipers[self.number] = "dead"
            if self.count_iter == 9:
                enemy_dead_sound.play()
                self.kill()
            if self.count_iter == 6:
                self.image = load_image('3_boom.png', name="Explosions")
            if self.count_iter == 3:
                self.image = load_image('2_boom.png', name="Explosions")
            if self.count_iter == 1:
                self.image = load_image('1_boom.png', name="Explosions")
            self.count_iter += 1


class AlienEgg(Animation):

    def __init__(self, image, columns, rows, x_pos, y_pos, number):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(image, columns, rows, x_pos, y_pos)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x_pos, y_pos)
        self.x = x_pos
        self.y = y_pos
        self.number = number
        self.alive = 0
        self.stage = 1
        self.count_iter = 0

    def update_egg(self):
        global alien_egg
        global egg_image
        global BORN

        for i in soldiers:
            if i[3] == "alive":
                self.alive += 1
        for i in snipers:
            if i[2] == "alive":
                self.alive += 1
        if self.alive == 4 and self.stage == 1:
            egg_image = load_image('2_stage.png', name="Egg")
            self.change_anim(egg_image, 1, 1)
            self.stage = 2
        if self.alive == 3 and self.stage == 2:
            egg_image = load_image('3_stage.png', name="Egg")
            self.change_anim(egg_image, 4, 1)
            self.stage = 3
            BORN = False
        if self.count_iter == 12 and self.cur_frame < len(self.frames) - 1 and self.stage == 3:
            self.cur_frame = self.cur_frame + 1
            self.image = self.frames[self.cur_frame]
            self.count_iter = 0
        self.alive = 0
        if self.stage == 3:
            self.count_iter += 1
            return True
        return False


class Aliens(Animation):

    def __init__(self, image, columns, rows, x_pos, y_pos, count, number):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(image, columns, rows, x_pos, y_pos + 5)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x_pos, y_pos + 5)
        self.change = 0
        self.count = count
        self.side = "right"
        self.wait = 40
        self.kil = False
        self.damage = 0
        self.current_animation = 'right'
        self.count_iter = 0
        self.count_iter1 = 0
        self.number = number
        self.move = True

    def update_alien(self, upd_alien):
        global aliens
        global enemy_bullets
        global alien_image

        if upd_alien is True:
            if self.change >= self.count:
                self.change = 0
                if self.side == "right":
                    self.side = "left"
                else:
                    self.side = "right"
            if self.side == "right" and self.move is True:
                self.rect.x += 3
                self.change += 3
                if self.current_animation != 'right':
                    alien_image = load_image('run.png', name="Alien")
                    self.change_anim(alien_image, 4, 1)
                    self.current_animation = 'right'
            elif self.side == "left" and self.move is True:
                self.rect.x -= 3
                self.change += 3
                if self.current_animation != 'left':
                    alien_image = load_image('run.png', name="Alien", flip=True)
                    self.change_anim(alien_image, 4, 1, rever=True)
                    self.current_animation = 'left'
            if -128 <= self.rect.x - player.rect.x <= 128 and -128 <= self.rect.y - player.rect.y <= 128:
                if self.rect.x > player.rect.x and (
                        self.rect.y - 8 == player.rect.y or self.rect.y - 10 == player.rect.y):
                    self.wait_bullet(True, False, True)
                    alien_image = load_image('attack.png', name="Alien", flip=True)
                    self.change_anim(alien_image, 1, 1, rever=True)
                elif self.rect.x < player.rect.x and (
                        self.rect.y - 8 == player.rect.y or self.rect.y - 10 == player.rect.y):
                    self.wait_bullet(False, False, True)
                    alien_image = load_image('attack.png', name="Alien")
                    self.change_anim(alien_image, 1, 1)
            else:
                self.move = True
            self.take_damage()
            if self.count_iter == 7:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.count_iter = 0
            self.count_iter += 1

    def take_damage(self):
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(self, bullet) and self.kil is False:
                self.damage += 1
                bullet.kill()
            if self.damage == 5:
                self.kil = True
                aliens[self.number] = "dead"
                if self.count_iter1 == 9:
                    enemy_dead_sound.play()
                    self.kill()
                if self.count_iter1 == 6:
                    self.image = load_image('3_boom.png', name="Explosions")
                if self.count_iter1 == 3:
                    self.image = load_image('2_boom.png', name="Explosions")
                if self.count_iter1 == 1:
                    self.image = load_image('1_boom.png', name="Explosions")
                self.count_iter1 += 1

    def wait_bullet(self, left, top, center=False):
        self.move = False
        self.wait -= 1
        if self.wait == 0 and self.kil is False:
            self.attack(left, top, center)
            self.wait = 40

    def attack(self, left, top, center=False):
        self.move = False
        enemy_bullets.append(BulletEnemy(tile_images["1_stage_bullet"], self.rect.x + 30, self.rect.y, left, top,
                                         center, type="Alien"))


class BulletEnemy(Animation):

    def __init__(self, image, x, y, left, top, center=False, type="Soldier"):
        super().__init__(all_sprites, enemy_bullet_group)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.change = 0
        self.left = left
        self.top = top
        self.center = center
        self.type = type

    def update_bullet(self):
        global tile_images
        if self.type == "Soldier":
            if self.center is True:
                if self.left is True:
                    self.rect.x -= 2
                elif self.left is False:
                    self.rect.x += 2
            elif self.top is False:
                if self.left is True:
                    self.rect.x -= 2
                    self.rect.y += 2
                elif self.left is False:
                    self.rect.x += 2
                    self.rect.y += 2
            elif self.top is True:
                if self.left is True:
                    self.rect.x -= 2
                    self.rect.y -= 2
                elif self.left is False:
                    self.rect.x += 2
                    self.rect.y -= 2
            self.change += 1
            if self.change == 64:
                self.kill()
            if self.rect.x == player.rect.x and self.rect.y == player.rect.y:
                self.kill()
        else:
            if self.left is True:
                self.rect.x -= 2
            elif self.left is False:
                self.rect.x += 2
            if self.change == 24:
                self.image = tile_images["2_stage_bullet"]
            self.change += 1
            if self.change == 48:
                self.kill()
            if self.rect.x == player.rect.x and self.rect.y == player.rect.y:
                self.kill()


class Bullet(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.change = 0
        self.side = "right"
        self.aiming = "forward"
        self.moving = False

    def right(self):
        self.side = "right"

    def left(self):
        self.side = "left"

    def MoveTrue(self):
        self.moving = True

    def MoveFalse(self):
        self.moving = False

    def aim_change(self, x):
        self.aiming = x

    def update_bullet(self):
        if self.aiming == "forward":
            if self.side == "right":
                self.rect.x += 6
            else:
                self.rect.x -= 6
        elif self.aiming == "up":
            if not self.moving:
                self.rect.y -= 6
            elif self.side == "right":
                self.rect.x += 6
                self.rect.y -= 2
            else:
                self.rect.x -= 6
                self.rect.y -= 2
        else:
            if self.side == "right":
                self.rect.x += 6
                self.rect.y += 2
            else:
                self.rect.x -= 6
                self.rect.y += 2
        self.change += 3
        if self.change == 240:
            self.kill()


class AreYouReady(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.alpha = 255

    def minus_transparency(self):
        self.image.set_alpha(self.alpha)
        self.alpha -= 5


class Explosion(Animation):
    def __init__(self, sheet, columns, rows, x, y, iter):
        super().__init__(all_sprites)
        self.frames = []
        self.x = 0
        self.onGround = False
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.count_iter = 0
        self.iter = iter

    def update(self, left, right, up):
        if self.count_iter == self.iter:
            self.cur_frame = self.cur_frame + 1
            if self.cur_frame != len(self.frames):
                self.image = self.frames[self.cur_frame]
            else:
                self.kill()
            self.count_iter = 0
        self.count_iter += 1


class Bridge(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, bridge_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 1)
        self.isBoom = False
        self.count_iter = 0

    def update(self, left, right, up):
        if pygame.sprite.collide_rect(self, player):
            self.isBoom = True
        if self.isBoom:
            if self.count_iter == 15:
                Explosion(load_image('boom.png', name='Explosions'), 3, 1, self.rect.x, self.rect.y, 5)
                self.kill()
            self.count_iter += 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                platform_group.add(Tile('grass', x, y))
            elif level[y][x] == '!':
                platform_group.add(Tile('ground', x, y))
            elif level[y][x] == '-':
                if y != 6:
                    Tile('center_trees', x, y)
                else:
                    Tile('empty', x, y)
                bridge_group.add(Bridge('center_brige', x, y))
            elif level[y][x] == 'F':
                Tile('forest', x, y)
            elif level[y][x] == '/':
                water_group.add(Tile('water', x, y))
            elif level[y][x] == '2':
                water_group.add(Tile('water_right', x, y))
            elif level[y][x] == '3':
                water_group.add(Tile('water_left', x, y))
            elif level[y][x] == '|':
                water_group.add(Tile('water_up', x, y))
            elif level[y][x] == '4':
                water_group.add(Tile('water_right-up', x, y))
            elif level[y][x] == '5':
                water_group.add(Tile('water_left-up', x, y))
            elif level[y][x] == '6':
                if y != 6:
                    Tile('center_trees', x, y)
                else:
                    Tile('empty', x, y)
                bridge_group.add(Bridge('start_brige', x, y))
            elif level[y][x] == '7':
                if y != 6:
                    Tile('center_trees', x, y)
                else:
                    Tile('empty', x, y)
                bridge_group.add(Bridge('end_brige', x, y))
            elif level[y][x] == '=':
                Tile('start_trees', x, y)
            elif level[y][x] == '*':
                Tile('center_trees', x, y)
            elif level[y][x] == '+':
                Tile('end_trees', x, y)
            elif level[y][x] == '1':
                platform_group.add(Tile('grass', x, y))


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


tile_images = {
    'grass': load_image('grass.jpg', name='map'),
    'ground': load_image('ground.jpg', name='map'),
    'center_brige': load_image('center_brige.png', name='map'),
    'water_up': load_image('water_up.jpg', name='map'),
    'empty': load_image('space.jpg', name='map'),
    'forest': load_image('forest.jpg', name='map'),
    'water_right': load_image('water_right.jpg', name='map'),
    'water_left': load_image('water_left.jpg', name='map'),
    'water': load_image('water.jpg', name='map'),
    'water_right-up': load_image('water_right-up.jpg', name='map'),
    'water_left-up': load_image('water_left-up.jpg', name='map'),
    'start_brige': load_image('start_brige.png', name='map'),
    'end_brige': load_image('end_brige.png', name='map'),
    'start_trees': load_image('start_trees.jpg', name='map'),
    'center_trees': load_image('center_trees.jpg', name='map'),
    'end_trees': load_image('end_trees.jpg', name='map'),
    'bullet': load_image('bullet.png', name='Bill'),
    '1_stage_bullet': load_image('1_stage.png', name='Alien'),
    '2_stage_bullet': load_image('2_stage.png', name='Alien')
}


def spawn(x, y):
    global player
    global player_image
    player.kill()
    player = Bill(player_image, 1, 1, x, y)
    return player


def who_alive():
    soldiers_is = False
    snipers_is = False
    aliens_is = False
    for i in soldiers:
        if i != 'dead':
            soldiers_is = True
            break
    for i in snipers:
        if i != 'dead':
            snipers_is = True
            break
    for i in aliens:
        if i != 'dead':
            aliens_is = True
            break
    if not soldiers_is and not snipers_is and not aliens_is:
        return False
    return True


all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

tile_width = tile_height = 32
sounds_and_person = start_screen()
person = sounds_and_person[0]
sounds_mode = sounds_and_person[1]
generate_level(load_level('map.txt'))
player_image = load_image('Bill_standing.png', name=person)
MOVE_SPEED = 3
JUMP_POWER = 12
GRAVITY = 1
helicopter_image = load_image('helicopter.png', name='vehicle', n_scale_divided=2)
player = Bill(player_image, 1, 1, 1100, 900)
helicopter = Helicopter(helicopter_image, -2000, 10)
txt = load_image('start_level_ready.png', name='texts')
start_text = AreYouReady(txt, 1100, 40)

enemy_bullets = []
soldier_image = load_image('soldier_stand.jpg', name="Soldier")
sniper_image = load_image('shoot_center.png', name="Sniper")
egg_image = load_image('1_stage.png', name="Egg")
alien_image = load_image('start.png', name="Alien")
gromaides_image = load_image('closed_mouth.png', name='Gromaides_BOSS', n_scale_plus=96, n_plus_wide=53)
boss_gromaides = Gromaides(gromaides_image, 1, 1, 7205, 415)
if sounds_mode == 'Standard':
    enemy_dead_sound = pygame.mixer.Sound('data/sounds/enemy_dead.wav')
else:
    enemy_dead_sound = pygame.mixer.Sound('data/sounds/enemy_dead_DOOM.wav')
enemy_dead_sound.set_volume(0.06)

hp_count = Hp_count(load_image('hp.png', name='Bill', n_scale_multiply=2))

soldiers_list = []
snipers_list = []
egg_list = []
alien_list = []
for i in range(4):
    soldiers_list.append(Soldier(soldier_image, 1, 1, soldiers[i][0], soldiers[i][1], soldiers[i][2], i))
for i in range(6):
    snipers_list.append(Sniper(sniper_image, 1, 1, snipers[i][0], snipers[i][1], i))
for i in range(6):
    egg_list.append(AlienEgg(egg_image, 1, 1, alien_egg[i][0], alien_egg[i][1], i))
for i in range(6):
    alien_list.append(Aliens(alien_image, 1, 1, aliens[i][0], aliens[i][1], aliens[i][2], i))
