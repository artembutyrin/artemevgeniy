import sys
import requests
import pygame
import os

zoom = [2, 2]
crd = [83, 55]

maps = 'http://static-maps.yandex.ru/1.x/'
parrams = {
    'll': str(crd[0]) + ',' + str(crd[1]),
    'spn': str(zoom[0]) + ',' + str(zoom[1]),
    'l': 'map'}
resp = requests.get(maps, params=parrams)
with open('map.png', 'wb') as f:
    f.write(resp.content)
pic = pygame.image.load('map.png')
os.remove('map.png')
pygame.init()
screen = pygame.display.set_mode((600, 450))
flag = True
now = 0
while flag:
    screen.blit(pic, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
    pygame.display.flip()
pygame.quit()