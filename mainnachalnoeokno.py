import pygame
import sys
from datetime import datetime

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Exploit')

background_image = pygame.image.load('background_image.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

start_button_image = pygame.image.load('start_button_image.jpg')
start_button_image = pygame.transform.scale(start_button_image, (200, 50))

settings_button_image = pygame.image.load('settings_button_image.jpg')
settings_button_image = pygame.transform.scale(settings_button_image, (200, 50))

exit_button_image = pygame.image.load('exit_button_image.jpg')
exit_button_image = pygame.transform.scale(exit_button_image, (200, 50))

history_button_image = pygame.image.load('history_button_image.png')
history_button_image = pygame.transform.scale(history_button_image, (200, 50))

font = pygame.font.Font(None, 36)

graphics_options = ['Low', 'Low', 'Low']
selected_graphics_option = 0

sound_options = ['On', 'Off']
selected_sound_option = 0


def show_settings_window():
    global selected_graphics_option, selected_sound_option

    while True:
        window.blit(background_image, (0, 0))

        settings_title = font.render('Settings', True, BLACK)
        settings_title_rect = settings_title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        window.blit(settings_title, settings_title_rect)

        graphics_label = font.render('Graphics Settings:', True, BLACK)
        graphics_label_rect = graphics_label.get_rect(topleft=(100, 100))
        window.blit(graphics_label, graphics_label_rect)

        option_rects = []
        for i, option in enumerate(graphics_options):
            option_label = font.render(option, True, BLACK)
            option_rect = option_label.get_rect(topleft=(120, 150 + i * 50))
            window.blit(option_label, option_rect.topleft)
            option_rects.append(option_rect)
            if i == selected_graphics_option:
                pygame.draw.rect(window, BLACK, option_rect, 2)

        sound_label = font.render('Sound Settings:', True, BLACK)
        sound_label_rect = sound_label.get_rect(topleft=(100, 300))
        window.blit(sound_label, sound_label_rect)

        sound_option_label = font.render(sound_options[selected_sound_option], True, BLACK)
        sound_option_rect = sound_option_label.get_rect(topleft=(120, 350))
        window.blit(sound_option_label, sound_option_rect.topleft)

        current_time = datetime.now().strftime("%H:%M:%S")
        time_label = font.render('Local Time: ' + current_time, True, BLACK)
        time_label_rect = time_label.get_rect(topleft=(100, 500))
        window.blit(time_label, time_label_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, option_rect in enumerate(option_rects):
                    if option_rect.collidepoint(event.pos):
                        selected_graphics_option = i

                if sound_option_rect.collidepoint(event.pos):
                    selected_sound_option = (selected_sound_option + 1) % len(sound_options)

        pygame.display.flip()


def show_character_history_window():
    global window

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    SCREEN_WIDTH = 750
    SCREEN_HEIGHT = 470

    character_window = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  

    character_window.fill(WHITE)

    background_image = pygame.image.load("background_image.jpg")
    character_window.blit(background_image, (0, 0))

    character_image = pygame.image.load("2024-02-22 21.43.26.png")
    character_window.blit(character_image, (20, 120))
    character_image = pygame.image.load("2024-02-27 18.48.34.png")
    character_window.blit(character_image, (90, 120))
    character_image = pygame.image.load("2024-02-27 18.51.38.png")
    character_window.blit(character_image, (160, 120))
    character_image = pygame.image.load("2024-02-27 18.52.29.png")
    character_window.blit(character_image, (230, 120))
    character_image = pygame.image.load("2024-02-27 18.53.40.png")
    character_window.blit(character_image, (300, 120))
    character_image = pygame.image.load("2024-02-27 18.54.16.png")
    character_window.blit(character_image, (370, 120))

    font = pygame.font.SysFont("Arial", 20)

    with open('game_story.txt', 'r') as file:
        game_story = file.readlines()

    with open('character_description.txt', 'r') as file:
        character_story = file.readlines()

    def draw_text(text_list, x, y):
        for i, line in enumerate(text_list):
            text_surface = font.render(line.strip(), True, BLACK)
            character_window.blit(text_surface, (x, y + i * 25))

    draw_text(game_story, 10, 10) 
    draw_text(character_story, 10, SCREEN_HEIGHT - 280)

    window.blit(character_window, (25, 25))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


while True:
    window.blit(background_image, (0, 0))

    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render('Exploit', True, BLACK)
    title_text_shadow = title_font.render('Exploit', True, (50, 50, 50))

    title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    title_text_shadow_rect = title_text_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 3, 53))

    window.blit(title_text_shadow, title_text_shadow_rect)
    window.blit(title_text, title_text_rect)

    start_button = pygame.Rect(300, 200, 200, 50)
    settings_button = pygame.Rect(300, 300, 200, 50)
    exit_button = pygame.Rect(300, 400, 200, 50)
    history_button = pygame.Rect(300, 500, 200, 50)

    window.blit(start_button_image, (300, 200))
    window.blit(settings_button_image, (300, 300))
    window.blit(exit_button_image, (300, 400))
    window.blit(history_button_image, (300, 500))

    start_text = font.render('Start', True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button.center)
    window.blit(start_text, start_text_rect)

    settings_text = font.render('Settings', True, BLACK)
    settings_text_rect = settings_text.get_rect(center=settings_button.center)
    window.blit(settings_text, settings_text_rect)

    exit_text = font.render('Exit', True, BLACK)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    window.blit(exit_text, exit_text_rect)

    history_text = font.render('History', True, BLACK)
    history_text_rect = history_text.get_rect(center=history_button.center)
    window.blit(history_text, history_text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                print("Start button clicked")
            elif settings_button.collidepoint(event.pos):
                print("Settings button clicked")
                show_settings_window()
            elif exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif history_button.collidepoint(event.pos):
                print("History button clicked")
                show_character_history_window()

    pygame.display.flip()
