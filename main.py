import pygame
import sys

from buttons import Button
from assets import load_image
from transition import Transition
from entities import Player
from subtitle import Subtitle

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.state = "main_menu"
        self.transition = Transition(1000)
        self.subtitle = Subtitle(self.screen)

        self.font = pygame.font.Font(None, 30)
        self.title_img = load_image("data/images/entities/TITLE.png", self.screen.get_size())
        self.menu_bg = load_image("data/images/entities/maps.png", self.screen.get_size())
        self.playing_bg = load_image("data/images/entities/Prolog-Background-Dialog.png", self.screen.get_size())
        self.player = Player(load_image("data/images/entities/DIALOGBIMAS2.png"), self.screen_rect.center)
        self.dialog = load_image("data/images/entities/Dialog-Box.png", self.screen.get_size())
        self.king = load_image("data/images/entities/DIALOGKING.png", self.screen.get_size())

        self.buttons = {
            "main_menu" :[
            Button("Play", 400, 250, 200, 50, (50, 50, 50), (70, 70, 70), self.font, self.start_transition),
            Button("Exit", 400, 320, 200, 50, (50, 50, 50), (70, 70, 70), self.font, self.quit_game),
            ],
            "stage_prolog": [
            Button("Next", 400, 320, 150, 50, (50, 50, 50), (70, 70, 70), self.font, self.start_transition)

            ]
        }


    def start_transition(self):
        self.transition.start("stage_prolog")
        # self.transition.next_stage("next_stage")


    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.handle_events()
            self.update(dt)
            self.draw()

# Ini untuk rundown game, semua state disusun disini
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.state == "main_menu":
                for btn in self.buttons.get(self.state, []):
                    btn.handle_event(event)
            elif self.state == "stage_prolog":
                # self.player.handle_input(event)
                for btn in self.buttons.get(self.state, []):
                    btn.handle_event(event)
            # elif self.state == "stage1.1":

    def update(self, dt):
        next_state = self.transition.update(dt)
        if next_state:
            self.state = next_state
            if self.state == "stage_prolog":
                self.subtitle.show("Aku bukan raja... hanya kesatria...")
            if self.state == "stage1.1":
                self.subtitle.reset()
                self.subtitle.show("Aku sedang mencari arti kepemimpinan sejati")

        if self.state == "stage_prolog":
            self.player.update(self.screen.get_size())
        self.subtitle.update()

    def draw(self):
        if self.state == "main_menu":
            self.screen.blit(self.menu_bg, (0, 0))
            self.screen.blit(self.title_img, (0, 0))
            for btn in self.buttons.get(self.state, []):
                btn.draw(self.screen)
        elif self.state == "stage_prolog":
            self.screen.blit(self.playing_bg, (0, 0))
            self.player.draw(self.screen)
            dialog_ratio = self.dialog.get_height() / self.screen_width * 0.7
            dialog_height = 100
            overlay_resized = pygame.transform.scale(self. dialog, (self.screen_width * 0.7,dialog_height))
            dialog_rect = overlay_resized.get_rect(midbottom=(self.screen_width // 2, 600))
            self.screen.blit(overlay_resized,dialog_rect)
            for btn in self.buttons.get(self.state, []):
                btn.draw(self.screen)

        self.subtitle.draw()
        self.transition.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
