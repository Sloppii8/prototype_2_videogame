import pygame

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


class CutSceneOne:


    def __init__(self, player ):
        global counter_1
        # Variables
        self.name = 'test'
        self.step = 0
        self.timer = pygame.time.get_ticks()
        self.cut_scene_running = True

        # If we need to control the player while a cut scene running
        self.player = player

        # Dialogue
        self.text = {
            'one': "You have completed the level",
            'one.1': "Great job!",
            'one.2': "To play again press space bar",

            'two': "Let see if you can get a better time!"
        }
        self.text_counter = 0

    def update(self):

        pressed = pygame.key.get_pressed()
        space = pressed[pygame.K_SPACE]

        # First cut scene
        if self.step == 0:
            if int(self.text_counter) < len(self.text['one']):
                self.text_counter += 0.4
            else:
                if space:
                    self.step = 1

        # First cut scene
        if self.step == 0:
            if int(self.text_counter) < len(self.text['one.1']):
                self.text_counter += 0.4
            else:
                if space:
                    self.step = 1

                # First cut scene
        if self.step == 0:
            if int(self.text_counter) < len(self.text['one.2']):
                self.text_counter += 0.4
            else:
                if space:
                    self.step = 1

        # Second part
        if self.step == 1:
            if self.player.rect.centerx < 0:
                self.step = 2
                self.text_counter = 0
            else:
                self.player.rect.x -= 5

        # Third part (dialogue)
        if self.step == 2:
            if int(self.text_counter) < len(self.text['two']):
                self.text_counter += 0.4
            else:
                if space:
                    # Finish the cut scene
                    self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen):

        if self.step == 0:
            draw_text(
                screen,
                self.text['one'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                50,
                25
            )
        if self.step == 0:
            draw_text(
                screen,
                self.text['one.1'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                50,
                75
            )

        if self.step == 0:
            draw_text(
                screen,
                self.text['one.2'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                50,
                125
            )

        if self.step == 2:
            draw_text(
                screen,
                self.text['two'][0:int(self.text_counter)],
                50,
                (255, 255, 255),
                50,
                50
            )


class CutSceneManager:

    def __init__(self, screen):
        self.cut_scenes_complete = []
        self.cut_scene = None
        self.cut_scene_running = False

        # Drawing variables
        self.screen = screen
        self.window_size = 0

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_complete:
            self.cut_scenes_complete.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):

        if self.cut_scene_running:
            if self.window_size < self.screen.get_height() * 0.3: self.window_size += 2
            self.cut_scene_running = self.cut_scene.update()
        else:
            self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            # Draw rect generic to all cut scenes
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen.get_width(), self.window_size))
            # Draw specific cut scene details
            self.cut_scene.draw(self.screen)


