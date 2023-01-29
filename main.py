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
    if i < 3:  # Загружаем изображения для 1 и 2-го уровней
        for j in range(1, 4):  # Уменьшаем противников в зависимости от уровня и дальности
            target_im[i - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 13))))
    else:
        for j in range(1, 5):  # Загружаем изображения для 3-го уровня
            target_im[i - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 13))))


def draw_gun():  # Функция для пистолета
    mouse_pos = pygame.mouse.get_pos()
    gun_point = (WIDTH / 2, HEIGHT - 200)
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
    else:
        slope = -100000
    angle = math.atan(slope)    # Считаем угол наклона в радианах
    rotation = math.degrees(angle)  # Переводим в градусы
    if mouse_pos[0] < WIDTH / 2:    # Если наш курсор находится в левой части экрана
        gun = pygame.transform.flip(guns[level - 1], True, False)  # Мы должны перевернуть изображение пистолета
        if mouse_pos[1] < 600:  # Если наш курсор находится в игровом меню, то пистолет стрелять не должен
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH / 2 - 90, HEIGHT - 250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)   # Рисуем "след" от выстрела
    else:   # Если наш курсор находится в правой части экрана, то ничего переворачивать не надо
        gun = guns[level - 1]
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (WIDTH / 2 - 30, HEIGHT - 250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)


def drew_level(coords):    # Рисуем противников на поле
    if level == 1 or level == 2:
        target_rect = [[], [], []]   # Список списков для каждого типа противника
    else:
        target_rect = [[], [], [], []]
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            target_rect[i].append(pygame.rect.Rect((coords[i][j][0] + 15, coords[i][j][1]),
                                  (60 - (i * 13), 60 - (i * 13))))  # 'Хитбокс' врагов
            screen.blit(target_im[level - 1][i], coords[i][j])
    return target_rect


def move_level(coords):  # Функция для движения противников
    if level == 1 or level == 2:
        max_quant = 3
    else:
        max_quant = 4
    for i in range(max_quant):
        for j in range(len(coords[i])):
            crds = coords[i][j]
            if crds[0] < -150:
                coords[i][j] = (WIDTH, crds[1])   # Двигаем нижние объекты по длине экрана
            else:
                coords[i][j] = (crds[0] - (2**i), crds[1])  # Чем выше объект, тем быстрее он передвигается
    return coords


def shot(targets, coords):  # Функция, отвечающая за выстрел
    global points
    mouse_pos = pygame.mouse.get_pos()
    for i in range(len(targets)):
        for j in range(len(targets[i])):
            if targets[i][j].collidepoint(mouse_pos):
                coords[i].pop(j)  # При попадании противник исчезает
                points += 10 + (10 * (i ** 2))  # За каждого врага мы получаем очки. Чем выше враг - тем больше
    return coords


run = True
while run:  # Цикл запуска
    if not new_coords:
        one_coords = [[], [], []]  # Создаём отдельные списки для координат для каждого типа врагов и уровня
        two_coords = [[], [], []]
        three_coords = [[], [], [], []]
        for i in range(3):
            lst = targets[1]  # Обращаемся к нашему словарю с количеством противников
            for j in range(lst[i]):
                one_coords[i].append((WIDTH // (lst[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
                # Каждый новый тип врага располагается выше над прошлым
        for i in range(3):
            lst = targets[2]
            for j in range(lst[i]):
                two_coords[i].append((WIDTH // (lst[i]) * j, 300 - (i * 150) + 30 * (j % 2)))
        for i in range(4):
            lst = targets[3]
            for j in range(lst[i]):
                three_coords[i].append((WIDTH // (lst[i]) * j, 300 - (i * 100) + 30 * (j % 2)))
        new_coords = True
    screen.fill('Black')
    screen.blit(background[level - 1], (0, 0))  # Добавляем фон
    screen.blit(gameinfo[level - 1], (0, HEIGHT - 200))  # Располагаем на экране таблицу, где будет наш счёт
    if level > 0:  # Если мы не в стартовом меню, то запускаем пистолет и счёт очков
        draw_gun()
    if level == 1:   # В зависимости от уровня загружаем противников, их координаты и проверяем, попали ли мы в них
        target_box = drew_level(one_coords)
        one_coords = move_level(one_coords)
        if got:
            one_coords = shot(target_box, one_coords)
            got = False
            # После того как мы попали в противника, необходимо снова занулить значение,
            # иначе мы сможем просто водить мышью по экрану и, наводя на противника, засчитывать очки
    elif level == 2:
        target_box = drew_level(two_coords)
        two_coords = move_level(two_coords)
        if got:
            two_coords = shot(target_box, two_coords)
            got = False
    elif level == 3:
        target_box = drew_level(three_coords)
        three_coords = move_level(three_coords)
        if got:
            three_coords = shot(target_box, three_coords)
            got = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Если мы нажали на врага именно правой кнопкой
            mouse_posit = pygame.mouse.get_pos()
            if (0 < mouse_posit[0] < WIDTH) and (0 < mouse_posit[1] < HEIGHT - 200):
                # Также игра активирует стрельбу только в пределах экрана с противниками
                got = True
                total_got += 1
                if mode == 1:  # При типе игры, где ограниченное количество патронов, мы должны их уменьшать
                    ammo -= 1
    if level > 0:  # Реализация перехода на следующий уровень при зачистке предыдущего
        if target_box == [[], [], []] and level < 3:
            level += 1
    pygame.display.flip()
pygame.quit()