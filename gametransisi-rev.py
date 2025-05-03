import pygame
import sys

import subtitle
from subtitle import Subtitle

class Button:
    TEXT_COLOR = (255, 255, 255)

    def __init__(self, text, x, y, width, height, color, hover_color, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.action = action
        self.is_hovered = False
        self.text_surf = self.font.render(self.text, True, self.TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                if self.action:
                    self.action()
                    return True
        return False

class Game:
    # Konstanta dan State Game
    BG_COLOR = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    BUTTON_COLOR = (50, 50, 50)
    BUTTON_HOVER_COLOR = (70, 70, 70)
    TITLE_COLOR = (10, 10, 50)
    FONT_SIZE_LARGE = 60
    FONT_SIZE_MEDIUM = 30
    FONT_SIZE_SMALL = 20
    STATE_MAIN_MENU = "main_menu"
    STATE_PLAYING = "playing"
    PLAYER_SPEED = 5

    def __init__(self):
        pygame.init()

        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Journey to Find a Leader')
        self.clock = pygame.time.Clock()

        self.subtitle =  Subtitle(self.screen)

        self._load_fonts()
        self._load_images()

        self.game_state = self.STATE_MAIN_MENU
        self.current_bg = self.menu_bg

        # Variabel untuk state transisi
        self.transition_duration = 1200
        self.transition_timer = 0
        self.transition_active = False
        self.transition_alpha = 0
        self.next_stage_name = ""

        # Setup Player
        if self.player_img:
            self.player_rect = self.player_img.get_rect()
        else:
            self.player_rect = pygame.Rect(0, 0, 50, 50)
        self.player_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.movement = {'up': False, 'down': False, 'left': False, 'right': False}

        # Buat tombol-tombol
        self._create_buttons()

    def _load_fonts(self):
            self.large_font = pygame.font.Font(None, self.FONT_SIZE_LARGE)
            self.medium_font = pygame.font.Font(None, self.FONT_SIZE_MEDIUM)
            self.small_font = pygame.font.Font(None, self.FONT_SIZE_SMALL)
            self.title_font = pygame.font.Font(None, self.FONT_SIZE_LARGE + 10)

    def _load_images(self):
        # Fungsi helper internal untuk load gambar
        def load_image(path):
            try:
                return pygame.image.load(path).convert_alpha()
            except pygame.error as e:
                print(f"Error loading image '{path}': {e}")
                return None

        # === Player Image ===
        player_path = "data/images/entities/bimas.png"
        self.player_img = load_image(player_path)

        # === Menu Background ===
        menu_bg_path = "data/images/entities/maps.png"
        loaded_menu_bg = load_image(menu_bg_path)
        self.menu_bg = pygame.transform.scale(loaded_menu_bg,
                                              (self.screen_width, self.screen_height)) if loaded_menu_bg else None

        # === Title Image ===
        title_image_path = "data/images/entities/TITLE.png"
        loaded_title_image = load_image(title_image_path)
        self.title_image = pygame.transform.scale(loaded_title_image, (self.screen_width,
                                                                       self.screen_height)) if loaded_title_image else None

        # === Prolog Background ===
        prolog_bg_path = "data/images/entities/Prolog-Background-Dialog.png"
        loaded_prolog_bg = load_image(prolog_bg_path)
        self.prolog_bg_image = pygame.transform.scale(loaded_prolog_bg, (self.screen_width,
                                                                         self.screen_height)) if loaded_prolog_bg else None

        # === Dialog Box ===
        dialog_box_path = "data/images/entities/Dialog-Box.png"
        loaded_dialog_box = load_image(dialog_box_path)
        self.dialog_box_image = pygame.transform.scale(loaded_dialog_box, (self.screen_width,
                                                                           self.screen_height)) if loaded_dialog_box else None

        # === King Image ===
        king_img_path = "data/images/entities/DIALOGKING.png"
        loaded_king_img = load_image(king_img_path)
        self.king_img = pygame.transform.scale(loaded_king_img,
                                               (self.screen_width, self.screen_height)) if loaded_king_img else None

        # === Set default playing background (misalnya pakai prolog) ===
        self.playing_bg_image = self.prolog_bg_image  # Atau king_img, tergantung logika game kamu

    def _create_buttons(self):
        # Pengaturan layout tombol
        btn_width = 200
        btn_height = 50
        btn_spacing = 20
        total_btn_height = (btn_height * 2) + btn_spacing
        start_y = (self.screen_height - total_btn_height) // 2 + 50
        btn_x = (self.screen_width - btn_width) // 2

        # Membuat instance tombol
        self.play_button = Button("Play Game", btn_x, start_y, btn_width, btn_height,
                                  self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR, self.medium_font,
                                  self.initiate_transition_to_play) # Action: mulai transisi
        self.exitButton = Button("Exit", btn_x, start_y + btn_height + btn_spacing, btn_width, btn_height,
                                 self.BUTTON_COLOR, self.BUTTON_HOVER_COLOR, self.medium_font,
                                 self.quit_game)

        self.mainMenu_btn = [self.play_button, self.exitButton]

    # Memulai proses transisi ke state playing


    def initiate_transition_to_play(self):
        if not self.transition_active:
            self.transition_active = True
            self.transition_timer = 0
            self.transition_alpha = 0
            self.next_stage_name = self.STATE_PLAYING

    # Logika yang dijalankan SETELAH transisi selesai
    def start_game_logic(self):
        self.game_state = self.STATE_PLAYING
        self.current_bg = self.playing_bg_image # Ganti background
        self.player_rect.center = (self.screen_width // 2, self.screen_height // 2) # Reset posisi player
        self.movement = {'up': False, 'down': False, 'left': False, 'right': False} # Reset movement
        self.subtitle.show(
            "Aku bukan raja, bukan pemimpin besar… \nAku hanya seorang kesatria yang mencari arti kepemimpinan sejati.")

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        # Proses event hanya jika tidak sedang transisi
        process_game_events = not self.transition_active

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            # Event handling untuk menu utama
            if self.game_state == self.STATE_MAIN_MENU and process_game_events:
                for button in self.mainMenu_btn:
                    button.handle_event(event)
            # Event handling untuk state playing
            elif self.game_state == self.STATE_PLAYING and process_game_events:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP): self.movement['up'] = True
                    if event.key in (pygame.K_s, pygame.K_DOWN): self.movement['down'] = True
                    if event.key in (pygame.K_a, pygame.K_LEFT): self.movement['left'] = True
                    if event.key in (pygame.K_d, pygame.K_RIGHT): self.movement['right'] = True
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_w, pygame.K_UP): self.movement['up'] = False
                    if event.key in (pygame.K_s, pygame.K_DOWN): self.movement['down'] = False
                    if event.key in (pygame.K_a, pygame.K_LEFT): self.movement['left'] = False
                    if event.key in (pygame.K_d, pygame.K_RIGHT): self.movement['right'] = False

    def _update(self, dt):
        if self.transition_active:
            # Update timer dan alpha transisi
            self.transition_timer += dt
            progress = min(1.0, self.transition_timer / self.transition_duration)
            self.transition_alpha = int(progress * 255)

            # Cek jika transisi selesai
            if self.transition_timer >= self.transition_duration:
                self.transition_active = False
                self.transition_timer = 0
                # Jalankan logika untuk state baru
                if self.next_stage_name == self.STATE_PLAYING:
                    self.start_game_logic()
                self.next_stage_name = ""
        else:
            #Update logika game normal berdasarkan state
            if hasattr(self, "subtitle"):
                    self.subtitle.update()
            if self.game_state == self.STATE_PLAYING:
                # Update pergerakan player
                posisi_x = (self.movement['right'] - self.movement['left']) * self.PLAYER_SPEED
                posisi_y = (self.movement['down'] - self.movement['up']) * self.PLAYER_SPEED
                self.player_rect.move_ip(posisi_x, posisi_y)

                # Batasi pergerakan player di dalam layar
                self.player_rect.left = max(0, self.player_rect.left)
                self.player_rect.right = min(self.screen_width, self.player_rect.right)
                self.player_rect.top = max(0, self.player_rect.top)
                self.player_rect.bottom = min(self.screen_height, self.player_rect.bottom)


            elif self.game_state == self.STATE_MAIN_MENU:
                pass # Tidak ada update khusus untuk menu saat ini

    def _draw(self):
        # Gambar background sesuai state (atau state sebelum transisi)
        bg_to_draw = self.menu_bg if self.game_state == self.STATE_MAIN_MENU or self.transition_active else self.playing_bg_image
        if bg_to_draw:
            self.screen.blit(bg_to_draw, (0, 0))
        else:
            self.screen.fill(self.BG_COLOR) # Fallback warna solid

        # Gambar elemen spesifik state
        if self.game_state == self.STATE_MAIN_MENU:
            # Gambar judul
            max_title_width = int(self.screen_width * 0.7)
            title_ratio = self.title_image.get_height() / self.title_image.get_width()
            title_width = max_title_width
            title_height = int(title_width * title_ratio)

            # Resize gambar title
            overlay_resized = pygame.transform.scale(self.title_image, (title_width, title_height))

            # Posisikan di tengah atas (misal 100px dari atas)
            title_rect = overlay_resized.get_rect(midtop=(self.screen_width // 2, -25))
            self.screen.blit(overlay_resized, title_rect)
            # Gambar tombol
            for button in self.mainMenu_btn:
                button.draw(self.screen)

        elif self.game_state == self.STATE_PLAYING:
            # Subtitle
            # Gambar player
            if self.player_img:
                self.screen.blit(self.player_img, self.player_rect)
            else:
                pygame.draw.rect(self.screen, self.GRAY, self.player_rect)

        # Gambar efek transisi (jika aktif) di paling atas
        if self.transition_active:
            fade_surface = pygame.Surface((self.screen_width, self.screen_height))
            fade_surface.fill(self.BLACK)
            fade_surface.set_alpha(self.transition_alpha)
            self.screen.blit(fade_surface, (0, 0))

        if hasattr(self, "subtitle"):
            self.subtitle.draw()

        pygame.display.flip()

    def run(self):
        # Game loop utama
        while True:
            dt = self.clock.tick(60) # Dapatkan delta time
            self._handle_events()    # Proses input
            self._update(dt)         # Update state game
            self._draw()             # Gambar ke layar
            self.subtitle.update()

if __name__ == '__main__':
    game = Game()
    game.run()