import pygame
import math
# Подключаем все необходимые библиотеки для работы программы

pygame.init()
fps = 60        # Частота кадров в нашей игре
timer = pygame.time.Clock()
font = pygame.font.Font('assets/font/myFont.ttf', 25)  # Шрифт в игре
bigfont = pygame.font.Font('assets/font/myFont.ttf', 55)  # Шрифт для окна с окончанием игры
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
gameover_im = pygame.image.load(f'assets/menus/gameOver.png')
pause_im = pygame.image.load(f'assets/menus/pause.png')
for i in range(1, 4):      # Загружаем изображения для 3-х уровней
    background.append(pygame.image.load(f'assets/backgrounds/{i}.png'))  # Фоны
    gameinfo.append(pygame.image.load(f'assets/gameinfo/{i}.png'))  # Меню во время игры
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{i}.png'), (100, 100)))  # Пистолеты
    if i < 3:  # Загружаем изображения для 1 и 2-го уровней
        for j in range(1, 4):   # Уменьшаем противников в зависимости от уровня и дальности
            target_im[i - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 13))))
    else:
        for j in range(1, 5):  # Загружаем изображения для 3-го уровня
            target_im[i - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j * 18), 80 - (j * 13))))
pygame.mixer.music.load('assets/sounds/background_music.mp3')   # Загружаем музыкальные составляющие игры
plate_sound = pygame.mixer.Sound('assets/sounds/skelet.mp3')
plate_sound.set_volume(.5)
bird_sound = pygame.mixer.Sound('assets/sounds/Duck.mp3')
bird_sound.set_volume(.3)
laser_sound = pygame.mixer.Sound('assets/sounds/Laser Gun.wav')
laser_sound.set_volume(.5)
pygame.mixer.music.play()


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
                if level == 1:   # При попадании проигрывается характерный звук
                    bird_sound.play()
                elif level == 2:
                    plate_sound.play()
                elif level == 3:
                    laser_sound.play()

    return coords


def draw_score():  # Функция, отвечающая за оформление игрового меню
    point_text = font.render(f'Очки: {points}', True, 'black')
    screen.blit(point_text, (320, 660))
    shot_text = font.render(f'Выстрелы: {total_got}', True, 'black')
    screen.blit(shot_text, (320, 688))
    time_text = font.render(f'Время: {time1}', True, 'black')
    screen.blit(time_text, (320, 714))
    if mode == 0:  # Оформление игрового меню зависит от типа игры, который мы выбирали
        mode_text = font.render(f'Свободный режим', True, 'black')
    if mode == 1:
        mode_text = font.render(f'Осталось патронов: {ammo}', True, 'black')
    if mode == 2:
        mode_text = font.render(f'Осталось времени: {time2}', True, 'black')
    screen.blit(mode_text, (320, 741))


def draw_menu():   # Функция для стартового меню
    global game_over, pause, mode, level, menu, time1, time2, total_got, points, ammo, clicked, new_coords
    game_over = False
    pause = False
    screen.blit(menu_im, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    mode0_button = pygame.rect.Rect((170, 524), (260, 100))   # Реализуем рабочие кнопки
    mode1_button = pygame.rect.Rect((475, 524), (260, 100))
    mode2_button = pygame.rect.Rect((310, 661), (260, 100))
    if mode0_button.collidepoint(mouse_pos) and clicks[0] and not clicked:  # Считывая нажатие на конкретную кнопку
        # Запускаем конкретный режим игры. Задаём нужные начальные параметры
        mode = 0
        level = 1
        menu = False
        time1 = 0
        total_got = 0
        points = 0
        clicked = True
        new_coords = False
    if mode1_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 1
        level = 1
        menu = False
        time1 = 0
        ammo = 82
        total_got = 0
        points = 0
        clicked = True
        new_coords = False
    if mode2_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 2
        level = 1
        menu = False
        time2 = 35
        time1 = 0
        total_got = 0
        points = 0
        clicked = True
        new_coords = False


def draw_gameover():
    global clicked, level, pause, menu, game_over, points, time1, time2, total_got
    passed_score = points
    screen.blit(gameover_im, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    stop_button = pygame.rect.Rect((170, 661), (260, 100))  # Реализуем рабочие кнопки
    reset_button = pygame.rect.Rect((475, 661), (260, 100))
    screen.blit(bigfont.render(f'{passed_score}', True, 'white'), (615, 480))
    if reset_button.collidepoint(mouse_pos) and clicks[0] and not clicked:  # На экране окончания игры две кнопки.
        # Одна возвращает нас в меню, вторая выключает программу
        clicked = True
        level = 0
        pause = False
        game_over = False
        menu = True
        points = 0
        total_got = 0
        time1 = 0
        time2 = 0
    if stop_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        global run
        run = False


def draw_pause():  # Функция окна паузы
    global level, pause, menu, points, total_got, time1, time2, clicked, new_coords
    screen.blit(pause_im, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    countin_button = pygame.rect.Rect((170, 661), (260, 100))  # Реализуем рабочие кнопки
    reset_button = pygame.rect.Rect((475, 661), (260, 100))
    if countin_button.collidepoint(mouse_pos) and clicks[0] and not clicked:  # У нас есть две кнопки,
        # одна возвращает в игру, вторая в меню, аннулируя результаты
        level = temp_level
        pause = False
    if reset_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = 0
        pause = False
        menu = True
        points = 0
        total_got = 0
        time1 = 0
        time2 = 0
        clicked = True
        new_coords = False
        pygame.mixer.music.play()


run = True
while run:  # Цикл запуска
    timer.tick(fps)
    if level != 0:  # Запускаем таймер в игре
        if vrem < 60:
            vrem += 1
        else:
            vrem = 1
            time1 += 1
            if mode == 2:
                time2 -= 1
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
    if menu:  # Запуск меню
        level = 0
        draw_menu()
    if game_over:  # Запуск экрана окончания игры
        level = 0
        draw_gameover()
    if pause:  # Запуск экрана паузы
        level = 0
        draw_pause()
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
    if level > 0:  # Если мы не в стартовом меню, то запускаем пистолет и счёт очков
        draw_gun()
        draw_score()
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
            if (670 < mouse_posit[0] < 860) and (660 < mouse_posit[1] < 725):
                temp_level = level
                pause = True
                clicked = True
            if (670 < mouse_posit[0] < 860) and (715 < mouse_posit[1] < 760):
                menu = True
                clicked = True
                new_coords = False
                pygame.mixer.music.play()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked:
            clicked = False
    if level > 0:  # Реализация перехода на следующий уровень при зачистке предыдущего
        if target_box == [[], [], []] and level < 3:
            level += 1
        if (level == 3 and target_box == [[], [], [], []]) or (mode == 1 and ammo == 0) or (mode == 2 and time2 == 0):
            # Условия при котором мы перезапускаем игру, возвращаясь в меню
            new_coords = False
            game_over = True
            pygame.mixer.music.play()
            level = 0
    pygame.display.flip()
pygame.quit()