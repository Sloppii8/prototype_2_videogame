import pygame
import sys
from Cutscenes import CutSceneManager, CutSceneOne
import math
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
        self.jumping = False
        self.max_launch_distance_x = 100  # Maximum distance to launch in x-coordinate
        self.launch_distance_x = 0

    def update(self, cut_scene_manager, jump_pads):
        if self.rect.centerx > 1100:
            cut_scene_manager.start_cut_scene(CutSceneOne(self))
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= screen_height - 150:
            self.rect.top = screen_height - 150
        if self.rect.bottom >= screen_height - 0:
            self.rect.bottom = screen_height - 0

        if cut_scene_manager.cut_scene is None:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.rect.x -= 5
            if pressed[pygame.K_RIGHT]:
                self.rect.x += 5
            if pressed[pygame.K_UP] and not self.jumping:
                self.velocity.y = -20
                self.jumping = True

        if self.jumping:
            self.velocity += self.acceleration
            self.rect.move_ip(self.velocity.x, self.velocity.y)
            self.launch_distance_x += abs(self.velocity.x)

            if self.launch_distance_x >= self.max_launch_distance_x:
                self.velocity.x = 0
                self.launch_distance_x = 0
                self.jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)




class JumpPad(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.power = -15

    def activate(self, player):
        player.velocity.y = self.power
        player.launching = True
        player.launch_distance_traveled_x = 0

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def draw_start_button():
    global button_x, button_y
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height) // 2
    pygame.draw.rect(screen, blue, (button_x, button_y, button_width, button_height))
    font = pygame.font.SysFont(None, 48)
    text = font.render("Start", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)


def handle_button_click():
    global start_button_clicked
    start_button_clicked = True
    # Add your desired logic to execute when the button is clicked
    print("Start button clicked!")
    countdown()


def countdown():
    global counter, scroll
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        text = font.render(str(i), True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(1)


# Create player, cut scene manager, and jump pad
player = Player()
cut_scene_manager = CutSceneManager(screen)
jump_pad = JumpPad(500, 630)
jump_pads = [jump_pad]  # Add the jump pad to a list


# sprite groups
all_sprites = pygame.sprite.Group()

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

    if start_button_clicked:
        start_button_visible = False  # Hide the button after it's clicked
        counter += 1
        if counter > 180:
            pass
        scroll -= 5


    for jump_pad in jump_pads:
        jump_pad.update()

    player.update(cut_scene_manager, jump_pads)

    # Update objects
    player.update(cut_scene_manager, jump_pad)
    cut_scene_manager.update()
    jump_pad.update()

    # Check collision between player and jump pad
    if player.rect.colliderect(jump_pad.rect) and not player.launching:
        jump_pad.activate(player)

    # Draw objects
    all_sprites.add(player)  # Add the player sprite to the all_sprites group
    all_sprites.draw(screen)
    cut_scene_manager.draw()
    jump_pad.draw(screen)
    draw_start_button()

    # Update display
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    pygame.display.update()
    pygame.display.flip()
