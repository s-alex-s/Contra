import pygame
from load_pictures import *
from all_characters import *


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def apply_level(self, obj):
        obj.rect.y += self.dy

    def update_level(self, target):
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)


camera = Camera()

size = width, height = 1000, 352
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
bullets = []
FPS = 60

if sounds_mode == 'Standard':
    pygame.mixer.music.load('data/sounds/music_STANDARD.wav')
    shooting_sound = pygame.mixer.Sound('data/sounds/shoot.wav')
elif sounds_mode == 'DOOM':
    pygame.mixer.music.load('data/sounds/music_DOOM_start.wav')
    pygame.mixer.music.play()
    shooting_sound = pygame.mixer.Sound('data/sounds/shoot_DOOM.wav')
helicopter_sound = pygame.mixer.Sound('data/sounds/helicopter_sound.wav')

helicopter_sound.set_volume(0.07)
pygame.mixer.music.set_volume(0.04)
shooting_sound.set_volume(0.06)

k_left = False
k_right = False
k_down = False
k_up = False
last_key = "right"
aiming = "forward"
isJump = False
img_flip = False
control = False
start_txt_transp = False
new_level = False
new_level_music = False
bill_is_spawn = False
boss_attack = False
everyone_Dead = False
alien_upd = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)
        if control:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    aiming = "up"
                    k_up = True
                    player_image = load_image('shooting_up.png', name=person, flip=img_flip)
                    player.change_anim(player_image, 3, 1, rever=img_flip)
                if event.key == pygame.K_s:
                    aiming = "down"
                    k_down = True
                    player_image = load_image('shooting_down.png', name=person, flip=img_flip)
                    player.change_anim(player_image, 3, 1, rever=img_flip)
                if event.key == pygame.K_a:
                    k_left = True
                    img_flip = True
                    last_key = 'left'
                if event.key == pygame.K_d:
                    k_right = True
                    img_flip = False
                    last_key = 'right'
                if event.key == pygame.K_SPACE:
                    isJump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    k_left = False
                if event.key == pygame.K_d:
                    k_right = False
                if event.key == pygame.K_SPACE:
                    isJump = False
                if event.key == pygame.K_w:
                    k_up = False
                    if k_left or k_right:
                        player_image = load_image('Bill_walking.png', name=person, flip=img_flip)
                        player.change_anim(player_image, 6, 1, rever=img_flip)
                if event.key == pygame.K_s:
                    k_down = False
                    if k_left or k_right:
                        player_image = load_image('Bill_walking.png', name=person, flip=img_flip)
                        player.change_anim(player_image, 6, 1, rever=img_flip)
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    aiming = "forward"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = list(player.get_pos())
                    if last_key == 'right' and not (k_up or k_down):
                        pos[0] += 20
                        pos[1] += 5
                    elif last_key == 'left' and not (k_up or k_down):
                        pos[0] -= 13
                        pos[1] += 5
                    if k_right and k_up:
                        pos[0] += 10
                        pos[1] -= 8
                    elif k_left and k_up:
                        pos[0] -= 8
                        pos[1] -= 8
                    elif k_up and not (k_left and k_right):
                        if last_key == 'right':
                            pos[0] += 3
                            pos[1] -= 8
                        else:
                            pos[0] -= 5
                            pos[1] -= 8
                    if k_right and k_down:
                        pos[0] += 15
                        pos[1] += 14
                    elif k_left and k_down:
                        pos[0] -= 10
                        pos[1] += 15
                    elif k_down and not (k_left and k_right):
                        if last_key == 'right':
                            pos[0] += 20
                            pos[1] += 5
                        else:
                            pos[0] -= 12
                            pos[1] += 5

                    bullet = Bullet(tile_images["bullet"], pos[0], pos[1])
                    bullet_group.add(bullet)
                    bullet.aim_change(aiming)
                    if not k_left and not k_right:
                        bullet.MoveFalse()
                    else:
                        bullet.MoveTrue()
                    if last_key == "right":
                        bullet.right()
                    else:
                        bullet.left()
                    bullets.append(bullet)
                    if (k_left or k_right) and k_up:
                        player_image = load_image('shooting_up.png', name=person, flip=img_flip)
                        player.change_anim(player_image, 3, 1, rever=img_flip)
                    elif (k_left or k_right) and k_down:
                        player_image = load_image('shooting_down.png', name=person, flip=img_flip)
                        player.change_anim(player_image, 3, 1, rever=img_flip)
                    else:
                        player_image = load_image('shooting.png', name=person, flip=img_flip)
                        player.change_anim(player_image, 3, 1, rever=img_flip)

                    shooting_sound.play()

    if ((not k_left and not k_right) or (k_left and k_right)) and not isJump and not k_up:
        player_image = load_image('Bill_standing.png', name=person, flip=img_flip)
        player.change_anim(player_image, 1, 1, rever=img_flip)
    elif k_up and (not k_left and not k_right):
        player_image = load_image('shooting_up_stand.png', name=person, flip=img_flip)
        player.change_anim(player_image, 1, 1, rever=img_flip)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update(k_left, k_right, isJump)
    everyone_Dead = who_alive()
    hp_count.update_hp(player.get_pos(), player.get_hp())
    if bill_is_spawn and player.get_pos()[1] > 535 and not new_level:
        if everyone_Dead:
            game_over_screen()
        camera.update_level(player)
        for sprite in all_sprites:
            camera.apply_level(sprite)
        pygame.mixer.music.stop()
        new_level = True
    if player.get_pos()[1] > 600 and new_level:
        if boss_gromaides.boss_is_dead():
            you_win_screen()
        else:
            game_over_screen()
    if player.get_pos()[2] > 6096 and not boss_attack:
        boss_gromaides.lets_attack()
        boss_attack = True
    if player.get_pos()[2] > 5270 and not new_level_music:
        if sounds_mode == 'Standard':
            pygame.mixer.music.load('data/sounds/music_boss_fight.wav')
        else:
            pygame.mixer.music.load('data/sounds/music_boss_fight_DOOM.wav')
        pygame.mixer.music.set_volume(0.04)
        pygame.mixer.music.play(-1)
        new_level_music = True
    helicopter.update_helicopter()
    if helicopter.get_pos() == 383:
        bill_is_spawn = True
        player = spawn(480, 30)
        control = True
        if sounds_mode == 'DOOM':
            pygame.mixer.music.load('data/sounds/music_DOOM.wav')
        pygame.mixer.music.play(-1)
    if helicopter.get_pos() == 1001:
        helicopter.kill()
    for soldier in soldiers_list:
        soldier.update_soldier()
    for sniper in snipers_list:
        sniper.update_sniper()
    for egg in egg_list:
        alien_upd = egg.update_egg()
    for bullet in bullets:
        bullet.update_bullet()
    for enemy_bullet in enemy_bullets:
        enemy_bullet.update_bullet()
    if helicopter.get_pos() == -507:
        start_txt_transp = True
    if helicopter.get_pos() == -1272:
        helicopter_sound.play()
    if start_txt_transp:
        start_text.minus_transparency()
    for alien in alien_list:
        alien.update_alien(alien_upd)
    clock.tick(FPS)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    pygame.display.flip()
pygame.quit()
