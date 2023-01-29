import pygame
import math
# Подключаем все необходимые библиотеки для работы программы

pygame.init()
fps = 60        # Частота кадров в нашей игре
timer = pygame.time.Clock()
font = pygame.font.Font('assets/font/myFont.ttf', 25)  # Шрифт в игре
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Создаём окно игры
background = []
guns = []
gameinfo = []
target_im = [[], [], []]
targets = {1: [10, 5, 3],    # Количество врагов на экране
           2: [12, 8, 5],
           3: [15, 12, 8, 3]}  # В третьем уровне будут дополнительные мини-враги для усложнения
level = 1
points = 0
ammo = 0
mode = 0
total_got = 0
time1 = 0
time2 = 0
vrem = 1
new_coords = False
got = False
clicked = False
menu = True
game_over = False
game_pause = False
menu_im = pygame.image.load(f'assets/menus/mainMenu.png')
gameover_im = pygame.image.load(f'assets/menus/gameOver.png')
pause_im = pygame.image.load(f'assets/menus/pause.png')
for i in range(1, 4):      # Загружаем изображения для 3-х уровней
    background.append(pygame.image.load(f'assets/backgrounds/{i}.png'))  # Фоны
    gameinfo.append(pygame.image.load(f'assets/gameinfo/{i}.png'))  # Меню во время игры
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{i}.png'), (100, 100)))  # Пистолеты


run = True
while run:  # Цикл запуска
    screen.fill('Black')
    screen.blit(background[level - 1], (0, 0))  # Добавляем фон
    screen.blit(gameinfo[level - 1], (0, HEIGHT - 200))  # Располагаем на экране таблицу, где будет наш счёт
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
