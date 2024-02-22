import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 430

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("История игры и персонажа")
background_image = pygame.image.load("background_image.jpg")
background_rect = background_image.get_rect()

character_image = pygame.image.load("2024-02-22 21.43.26.png")
character_rect = character_image.get_rect()
character_rect.left = 20
character_rect.top = 120

font = pygame.font.SysFont("Arial", 20)

with open('game_story.txt', 'r') as file:
    game_story = file.readlines()

with open('character_description.txt', 'r') as file:
    character_story = file.readlines()


def draw_text(text_list, x, y):
    for i, line in enumerate(text_list):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (x, y + i * 25))


running = True
while running:
    screen.fill(WHITE)
    screen.blit(background_image, background_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_text(game_story, 10, 10)

    screen.blit(character_image, character_rect)

    draw_text(character_story, 10, SCREEN_HEIGHT - 230)

    pygame.display.flip()

pygame.quit()
sys.exit()
