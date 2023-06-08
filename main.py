""" This is a race gaming code called seasons united, this game was made by Juliana silva costa."""

import pygame
import sys
from Cutscenes import *
import math
import time
import random
from pygame.locals import *

#Varibles
pygame.init()
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.mixer.music.load("C:/Users/Juliana/PycharmProjects/Protoytpe 2 for Unit 2/Music/DRIVE.mp3")
pygame.mixer.music.play(-1)
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
        self.freeze_timer = 0
        self.freeze_duration = 120

    def update(self, cut_scene_manager):
        global up
        if self.rect.centerx > 1100:
            cut_scene_manager.start_cut_scene(CutSceneOne(self))
            up = False
            value = counter
            print(value)
            # Render the text
            font = pygame.font.Font(None, 100)
            text_surface = font.render("Time: " + str(round(value/60,2)) + " Seconds", True, (255, 0, 0))

            # Get the rect of the rendered text
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

            # Draw the text on the screen
            screen.blit(text_surface, text_rect)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= screen_height - 150:
            self.rect.top = screen_height - 150
        if self.rect.bottom >= screen_height - 0:
            self.rect.bottom = screen_height - 0

        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            if self.freeze_timer == 0:
                # Unfreeze the player
                print("Player unfrozen!")

        if cut_scene_manager.cut_scene is None and self.freeze_timer <= 0:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.rect.x -= 5
            if pressed[pygame.K_RIGHT]:
                self.rect.x += 5
            if pressed[pygame.K_UP]:
                self.rect.y -= 5
            if pressed[pygame.K_DOWN]:
                self.rect.y += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


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
    #  logic to execute when the button is clicked
    print("Start button clicked!")
    countdown()


def countdown():
    global counter, scroll
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        text = font.render(str(i), True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect) #display the countdown text
        pygame.display.flip()
        time.sleep(1)


class IceBlock(pygame.sprite.Sprite):
    def __init__(self, ice_blocks):
        super().__init__()
        self.width = 50
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.generate_random_position(ice_blocks)
        self.freeze_duration = 60

    def freeze_player(self, player):
        if player.freeze_timer <= 0:
            player.freeze_timer = self.freeze_duration

    def generate_random_position(self, ice_blocks):
        # Define the area where the ice blocks can appear
        area_x = 200  # Starting x-coordinate of the area
        area_y = 600  # Starting y-coordinate of the area
        area_width = 700  # Width of the area
        area_height = 120  # Height of the area

        min_distance = 100  # Minimum distance between ice blocks

        while True:
            x = random.randint(area_x, area_x + area_width)
            y = random.randint(area_y, area_y + area_height)

            # Check if the new ice block is too close to any existing ice block
            too_close = False
            for block in ice_blocks:
                distance = math.sqrt((x - block.rect.centerx) ** 2 + (y - block.rect.centery) ** 2)
                if distance < min_distance:
                    too_close = True
                    break

            if not too_close:
                return x, y



# Create player, cut scene manager, and ice blocks
player = Player()
cut_scene_manager = CutSceneManager(screen)
num_ice_blocks = 4  # Set the choosen number of ice blocks
ice_blocks = pygame.sprite.Group()

for _ in range(num_ice_blocks):
    ice_block = IceBlock(ice_blocks)
    ice_blocks.add(ice_block)

up = True

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player, ice_blocks)

# Timer
counter = 0
current_time = 0
button_press_time = 0


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
        if up:
            start_button_visible = False  # Hide the button after it's clicked
            counter += 1
            if counter > 180:
                pass
            scroll -= 5
        else:
            if cut_scene_manager.cut_scene is None:
                counter += 1
                if counter > 180:
                    break

    # Update objects
    player.update(cut_scene_manager)
    cut_scene_manager.update()

    # Check for collision between player and ice blocks
    for ice_block in ice_blocks:
        if player.rect.colliderect(ice_block.rect):
            ice_block.freeze_player(player)

    # Draw objects
    all_sprites.draw(screen)
    cut_scene_manager.draw()
    draw_start_button()

    # Check if the cutscene is active and draw the text
    if cut_scene_manager.cut_scene is not None:
        cut_scene_manager.cut_scene.draw(screen)

    # Update display
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    pygame.display.update()
    pygame.display.flip()
