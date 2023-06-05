import pygame
import sys
import math
from Cutscenes import *
import time
from pygame.locals import *

pygame.init()
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
bg_image = pygame.image.load("C:/Users/Juliana/PycharmProjects/Protoytpe 2 for Unit 2/background/Favela part 1.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height - 150))
bg_width = bg_image.get_width()
bg_rect = bg_image.get_rect()
tiles = math.ceil(screen_width / bg_width) + 1
bg_image_2 = pygame.image.load("C:/Users/Juliana/PycharmProjects/Protoytpe 2 for Unit 2/background/roadforgame.jpg")
bg_image_2 = pygame.transform.scale(bg_image_2, (screen_width, screen_height - 550))
bg_width_2 = bg_image_2.get_width()
bg_rect_2 = bg_image_2.get_rect()
tiles_2 = math.ceil(screen_width / bg_width_2) + 1
print(tiles_2)
print(tiles)
scroll = 0
button_width = 200
button_height = 100
blue = (12, 10, 225)
white = (225, 225, 225)
start_button_clicked = False
start_button_visible = True
passed_jump_pad = False

# Define player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(bottomleft=(0, 650))
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.gravity = pygame.math.Vector2(0, 2)
        self.freeze_timer = 0

    def update(self, cut_scene_manager):
        global up
        if self.rect.centerx > 1100:
            cut_scene_manager.start_cut_scene(CutSceneOne(self))
            value = counter
            up = False
            print(value)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= screen_height - 150:
            self.rect.top = screen_height - 150
        if self.rect.bottom >= screen_height - 0:
            self.rect.bottom = screen_height - 0

        if cut_scene_manager.cut_scene is None and not passed_jump_pad and self.freeze_timer <= 0:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.rect.x -= 5
            if pressed[pygame.K_RIGHT]:
                self.rect.x += 5
            if pressed[pygame.K_UP]:
                self.rect.y -= 5
            if pressed[pygame.K_DOWN]:
                self.rect.y += 5

        self.velocity += self.acceleration
        self.rect.move_ip(self.velocity.x, self.velocity.y)

        if self.freeze_timer > 0:
            self.freeze_timer -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


class Jumppad(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 60
        self.height = 100
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 225, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (300, 550)
        self.jump_force = pygame.math.Vector2(10, -10)


    def bike_jump(self, player):
        player.velocity.y += self.jump_force.y
        player.velocity.x = self.jump_force.x
        global passed_jump_pad
        passed_jump_pad = True


class IceBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.freeze_duration = 60

    def freeze_player(self, player):
        if player.freeze_timer <= 0:
            player.freeze_timer = self.freeze_duration

# Create player, cut scene manager, jump pad, and ice block
player = Player()
cut_scene_manager = CutSceneManager(screen)
jump_pad = Jumppad(400, 300)
ice_block = IceBlock(600, 600)

up = True

# spritegroups
all_sprites = pygame.sprite.Group()
all_sprites.add(player, jump_pad, ice_block)

# timer
counter = 0
current_time = 0
button_press_time = 0

# set ground level
ground_level_min = 550
ground_level_max = 700

# Game loop
while True:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if start_button_visible and not start_button_clicked:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    handle_button_click()

    for i in range(0, tiles):
        screen.blit(bg_image, (i * bg_width + scroll, 0))
        bg_rect.x = i * bg_width + scroll

    if abs(scroll) > bg_width:
        scroll = 0

    for i in range(0, tiles_2):
        screen.blit(bg_image_2, (i * bg_width_2 + scroll, 565))
        bg_rect.x = i * bg_width_2 + scroll

    if abs(scroll) > bg_width_2:
        scroll = 0

    if start_button_visible:
        draw_start_button()

    if player.rect.x >= 700:
        player.velocity.x = 0
        player.rect.y = 700

    if passed_jump_pad:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player.rect.x -= 5
        if pressed[pygame.K_RIGHT]:
            player.rect.x += 5
        if pressed[pygame.K_UP]:
            player.rect.y -= 5
        if pressed[pygame.K_DOWN]:
            player.rect.y += 5

    if start_button_clicked:
        if up:
            start_button_visible = False
            counter += 1
            if counter > 180:
                pass
            scroll -= 5
        else:
            counter = counter
            break

    # Update objects
    player.update(cut_scene_manager)
    cut_scene_manager.update()

    if player.rect.colliderect(jump_pad.rect):
        jump_pad.bike_jump(player)

    if player.rect.colliderect(ice_block.rect):
        ice_block.freeze_player(player)

    # Draw objects
    all_sprites.draw(screen)
    cut_scene_manager.draw()
    draw_start_button()

    # Update display
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    pygame.display.update()
    pygame.display.flip()

