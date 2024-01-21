import pygame
import sys
import os
from datetime import datetime, timedelta
from random import choice
import sqlite3

pygame.init()

RED = pygame.Color("red")
GREEN = pygame.Color("#00FF00")
BLUE = pygame.Color(0, 0, 225)
BLACK = pygame.Color("#000000")
WHILE = pygame.Color(255, 255, 255)
SIZE = W, H = (1000, 600)
screen = pygame.display.set_mode(SIZE)
all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, size_x, size_y, flag, parent=None):
        super().__init__(all_sprites)
        self.columns = columns
        self.rows = rows
        self.flag = flag
        self.count_click = 0

        self.size_x, self.size_y = size_x, size_y
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.parent = parent

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, self.size_x,
                                self.size_y)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.flag and self.columns * self.rows != self.count_click + 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count_click += 1
            if self in load_script.arr_indicators:
                self.parent.check()
        elif not self.flag:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


class AnimatedSpriteIndicator(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, size_x, size_y, flag):
        super().__init__(sheet, columns, rows, x, y, size_x, size_y, flag, self)
        self.count_indicator = 0

    def check(self):
        load_script.arr_indicators[self] = True
        if all(list(load_script.arr_indicators.values())):
            check_winner.control_check()
            load_script.ending = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'fon_menu': pygame.transform.scale(load_image('fon_menu.png'), (1000, 600)),
    'bomb': pygame.transform.scale(load_image('bomb_3_lvl.png'), (900, 500)),
    'fon_easy_level': pygame.transform.scale(load_image('fon2.png'), (1000, 600)),
    'bomb_medium_level': pygame.transform.scale(load_image('bomb_medium.png'), (900, 500)),
    'bomb_hard_level': pygame.transform.scale(load_image('bomb_hard.png'), (900, 500))
}
DICT_COMPLEXITY = {"easy_level": "Легкая", 'medium_level': "Средняя", 'hard_level': "Сложная"}


def terminate():
    manage_data_base.close()
    pygame.quit()
    sys.exit()


def generate_level(complexity):
    Fon_Game()
    BombDraw(complexity)


def level_selection_menu():
    fon = pygame.transform.scale(load_image('fon_menu.png'), (W, H))
    screen.blit(fon, (0, 0))
    Fon()
    button_back = AnimatedSprite(pygame.transform.scale(load_image('back_button.png'), (600, 150)),
                                 2, 1, 10, 10, 300,
                                 150, False)
    easy_level_button = AnimatedSprite(pygame.transform.scale(load_image('easy_level_button.png'), (600, 150)),
                                       2, 1, 500, 10, 300,
                                       150, False)
    medium_level_button = AnimatedSprite(pygame.transform.scale(load_image('medium_level_button.png'), (600, 150)),
                                         2, 1, 500, 225, 300,
                                         150, False)
    hard_level_button = AnimatedSprite(pygame.transform.scale(load_image('hard_level_button.png'), (600, 150)),
                                       2, 1, 500, 440, 300,
                                       150, False)
    flag_button_back = True
    flag_button_easy_level = True
    flag_medium_level_button = True
    flag_hard_level_button = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 10 < x < 310 and 10 < y < 160 and flag_button_back:
                    flag_button_back = False
                    button_back.update()
                elif (not 10 < x < 310 or not 10 < y < 160) and not flag_button_back:
                    button_back.update()
                    flag_button_back = True
                if 500 < x < 800 and 10 < y < 150 and flag_button_easy_level:
                    easy_level_button.update()
                    flag_button_easy_level = False
                elif (not 500 < x < 800 or not 10 < y < 150) and not flag_button_easy_level:
                    easy_level_button.update()
                    flag_button_easy_level = True
                if 500 < x < 800 and 230 < y < 390 and flag_medium_level_button:
                    medium_level_button.update()
                    flag_medium_level_button = False
                elif (not 500 < x < 800 or not 230 < y < 390) and not flag_medium_level_button:
                    medium_level_button.update()
                    flag_medium_level_button = True
                if 500 < x < 800 and 441 < y < 590 and flag_hard_level_button:
                    hard_level_button.update()
                    flag_hard_level_button = False
                elif (not 500 < x < 800 or not 441 < y < 590) and not flag_hard_level_button:
                    hard_level_button.update()
                    flag_hard_level_button = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x, y)
                if 10 < x < 390 and 10 < y < 160:
                    return "main_menu"
                if 500 < x < 800 and 10 < y < 150:
                    return "easy_level"
                if 500 < x < 800 and 230 < y < 390:
                    return "medium_level"
                if 500 < x < 800 and 441 < y < 590:
                    return "hard_level"
        all_sprites.draw(screen)
        pygame.display.flip()


def start_screen():
    fon = pygame.transform.scale(load_image('fon_menu.png'), (W, H))
    screen.blit(fon, (0, 0))
    Fon()
    button_start = AnimatedSprite(pygame.transform.scale(load_image('button_menu_1.png'), (600, 150)), 2, 1, 350,
                                  200,
                                  300,
                                  150, False)
    flag_button_start = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 349 < x < 659 and 202 < y < 346:
                    result = level_selection_menu()
                    if result != "main_menu":
                        return result
                    else:
                        fon = pygame.transform.scale(load_image('fon_menu.png'), (W, H))
                        screen.blit(fon, (0, 0))
                        Fon()
                        button_start = AnimatedSprite(
                            pygame.transform.scale(load_image('button_menu_1.png'), (600, 150)), 2, 1, 350,
                            200,
                            300,
                            150, False)
                        flag_button_start = True
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 349 < x < 659 and 202 < y < 346 and flag_button_start:
                    button_start.update()
                    flag_button_start = False
                elif (not 349 < x < 659 or not 202 < y < 346) and not flag_button_start:
                    button_start.update()
                    flag_button_start = True
        all_sprites.draw(screen)
        pygame.display.flip()


def finish_menu(time, complexity):
    fon_finish_menu = AnimatedSprite(pygame.transform.scale(load_image('fon_win.png'), (2000, 600)), 2, 1,
                                     0, 0, 1000,
                                     600, False)
    if manage_data_base.return_data_base()[0][0] < time:
        manage_data_base.changing_a_cell(time)
    time_sun = datetime.now()
    manage_data_base.changing_a_cell("win")
    complexity_text = pygame.font.SysFont('serif', 28)
    complexity_text = complexity_text.render(DICT_COMPLEXITY[complexity], False,
                                             (0, 0, 0))
    record_time_text = pygame.font.SysFont('serif', 28)
    record_time_text = record_time_text.render(str(manage_data_base.return_data_base()[0][0]), False,
                                               (0, 0, 0))
    time_text = pygame.font.SysFont('serif', 28)
    time_text = time_text.render(str(time), False,
                                 (0, 0, 0))
    win_count_text = pygame.font.SysFont('serif', 28)
    win_count_text = win_count_text.render(str(manage_data_base.return_data_base()[0][1]), False,
                                           (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        if time_sun.second != datetime.now().second:
            time_sun = datetime.now()
            fon_finish_menu.update()
        all_sprites.draw(screen)
        screen.blit(complexity_text, (215, 103))
        screen.blit(record_time_text, (315, 340))
        screen.blit(time_text, (315, 225))
        screen.blit(win_count_text, (280, 498))
        pygame.display.flip()


def push_button(pos):
    load_script.sorted_coordinates(pos)


def down_button(pos):
    load_script.down_button(pos)


class Fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = tile_images['fon_menu']
        self.rect = self.image.get_rect().move(
            0, 0)


class Fon_Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = tile_images['fon_easy_level']
        self.rect = self.image.get_rect().move(
            0, 0)


class BombDraw(pygame.sprite.Sprite):
    def __init__(self, complexity):
        super().__init__(all_sprites)
        self.image = tile_images[complexity]
        self.rect = self.image.get_rect().move(
            50, 50)


class LoadEasyScript:
    def __init__(self, wire, button_click, serial_number):
        self.ending = False
        self.wire = wire
        self.button_click = button_click
        self.count_button_click = 0
        self.serial_number = serial_number
        self.dict_serial_numbers = {'number_EA500.png': 2, "number_22081921.png": 3, "number_517B.png": 4,
                                    "number_3A3CC9.png": 7}
        self.arr_coordinates = [((459, 290), (585, 383)), ((81, 193), (110, 269)), ((139, 190), (170, 268)),
                                ((200, 191), (230, 268)), ((104, 84), (250, 130)), ((673, 334), (715, 381))]

        self.button = AnimatedSprite(pygame.transform.scale(load_image('button.png'), (544, 200)), 2, 1, 380, 240, 272,
                                     200, False)
        self.red_wire = AnimatedSprite(pygame.transform.scale(load_image('red_wire.png'), (60, 80)), 2, 1, 80, 190, 30,
                                       80, True)
        self.blue_wire = AnimatedSprite(pygame.transform.scale(load_image('blue_wire.png'), (60, 80)), 2, 1, 140, 190,
                                        30,
                                        80, True)
        self.green_wire = AnimatedSprite(pygame.transform.scale(load_image('green_wire.png'), (60, 80)), 2, 1, 200, 190,
                                         30,
                                         80, True)
        self.indicator_wire = AnimatedSpriteIndicator(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2,
                                                      1, 246,
                                                      155,
                                                      40, 40, True)
        self.indicator_button = AnimatedSpriteIndicator(
            pygame.transform.scale(load_image('indicator_metal.png'), (80, 40)),
            2, 1, 670,
            220,
            40, 40, True)
        self.serial_number_sprite = AnimatedSprite(
            pygame.transform.scale(load_image(serial_number), (510, 54 * self.dict_serial_numbers[serial_number])), 2,
            self.dict_serial_numbers[serial_number], 60,
            80,
            255, 54, True)
        self.mini_button = AnimatedSprite(pygame.transform.scale(load_image('mini_button.png'), (204, 324)), 4,
                                          2, 669,
                                          330,
                                          51, 54, False)
        self.arr_indicators = {self.indicator_wire: False, self.indicator_button: False}

    def wire_script(self, wire):
        if wire != self.wire:
            check_winner.control_check()
        else:
            self.indicator_wire.update()

    def func_button_click(self, button_count):
        if button_count != self.button_click:
            check_winner.control_check()
        else:
            self.indicator_button.update()

    def down_button(self, pos):
        x, y = pos
        arr_coordinates = self.arr_coordinates
        if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < \
                arr_coordinates[0][1][
                    1]:
            self.sorted_coordinates(pos)
            self.count_button_click += 1
        elif arr_coordinates[5][0][0] < x < arr_coordinates[5][1][0] and arr_coordinates[5][0][1] < y < \
                arr_coordinates[5][1][
                    1]:
            self.func_button_click(self.count_button_click)

    def sorted_coordinates(self, pos):
        x, y = pos
        arr_coordinates = self.arr_coordinates
        if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < \
                arr_coordinates[0][1][
                    1]:
            self.button.update()
            self.mini_button.update()
        elif arr_coordinates[1][0][0] < x < arr_coordinates[1][1][0] and arr_coordinates[1][0][1] < y < \
                arr_coordinates[1][1][
                    1]:
            self.red_wire.update()
            self.wire_script("red")
        elif arr_coordinates[2][0][0] < x < arr_coordinates[2][1][0] and arr_coordinates[2][0][1] < y < \
                arr_coordinates[2][1][
                    1]:
            self.blue_wire.update()
            self.wire_script("blue")
        elif arr_coordinates[3][0][0] < x < arr_coordinates[3][1][0] and arr_coordinates[3][0][1] < y < \
                arr_coordinates[3][1][
                    1]:
            self.green_wire.update()
            self.wire_script("green")
        elif arr_coordinates[4][0][0] < x < arr_coordinates[4][1][0] and arr_coordinates[4][0][1] < y < \
                arr_coordinates[4][1][
                    1]:
            load_script.serial_number_sprite.update()


class LoadMediumScript:
    def __init__(self, wire, sequence, serial_number):
        self.ending = False
        self.click = False
        self.wire = wire
        self.sequence = sequence
        self.sequence_count = 0
        self.count_button_click = 0
        self.serial_number = serial_number
        self.arr_coordinates = [((60, 191), (89, 268)),
                                ((110, 191), (138, 267)),
                                ((163, 192), (188, 268)),
                                ((211, 191), (236, 266)),

                                ((651, 231), (718, 300)),
                                ((730, 233), (796, 296)),
                                ((652, 312), (717, 375)),
                                ((733, 313), (797, 375)),
                                ((344, 475), (404, 517))
                                ]

        self.red_wire = AnimatedSprite(pygame.transform.scale(load_image('red_wire.png'), (60, 80)), 2, 1, 60, 190, 30,
                                       80, True)
        self.blue_wire = AnimatedSprite(pygame.transform.scale(load_image('blue_wire.png'), (60, 80)), 2, 1, 110, 190,
                                        30,
                                        80, True)
        self.green_wire = AnimatedSprite(pygame.transform.scale(load_image('green_wire.png'), (60, 80)), 2, 1, 160, 190,
                                         30,
                                         80, True)
        self.people_wire = AnimatedSprite(pygame.transform.scale(load_image('people_wire.png'), (60, 80)), 2, 1, 210,
                                          190,
                                          30,
                                          80, True)
        self.pazzle_conjugate_operator = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_conjugate_operator.png'), (140, 70)), 2, 1, 650,
            230,
            70,
            70, True)
        self.pazzle_transposition_matrix = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_transposition_matrix.png'), (140, 70)), 2, 1, 730,
            230,
            70,
            70, True)
        self.pazzle_tensor_product = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_tensor_product.png'), (140, 70)), 2, 1, 730,
            310,
            70,
            70, True)
        self.pazzle_matrix_unit = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_matrix_unit.png'), (140, 70)), 2, 1, 650,
            310,
            70,
            70, True)
        self.indicator_wire = AnimatedSpriteIndicator(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2,
                                                      1, 246,
                                                      155,
                                                      40, 40, True)
        self.indicator_pazzle = AnimatedSpriteIndicator(
            pygame.transform.scale(load_image('indicator_metal.png'), (80, 40)), 2,
            1, 850,
            190,
            40, 40, True)
        self.code_number = AnimatedSpriteIndicator(pygame.transform.scale(load_image(serial_number), (380, 54)), 2,
                                                   1, 340,
                                                   470,
                                                   190, 54, False)
        self.arr_indicators = {self.indicator_wire: False, self.indicator_pazzle: False}

    def wire_script(self, wire):
        if wire != self.wire:
            check_winner.control_check()
        else:
            self.indicator_wire.update()

    def sequence_fun(self, symbol):
        if not self.arr_indicators[self.indicator_pazzle]:
            if symbol == self.sequence[self.sequence_count]:
                self.sequence_count += 1
            else:
                check_winner.control_check()
            if self.sequence_count == 4:
                self.indicator_pazzle.update()

    def down_button(self, pos):
        x, y = pos
        arr_coordinates = load_script.arr_coordinates
        print(x, y)
        if arr_coordinates[8][0][0] < x < arr_coordinates[8][1][0] and arr_coordinates[8][0][1] < y < \
                arr_coordinates[8][1][
                    1]:
            self.code_number.update()

    def sorted_coordinates(self, pos):
        x, y = pos
        arr_coordinates = load_script.arr_coordinates
        if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < \
                arr_coordinates[0][1][
                    1]:
            self.red_wire.update()
            self.wire_script("red")
        elif arr_coordinates[1][0][0] < x < arr_coordinates[1][1][0] and arr_coordinates[1][0][1] < y < \
                arr_coordinates[1][1][
                    1]:
            self.blue_wire.update()
            self.wire_script("blue")
        elif arr_coordinates[2][0][0] < x < arr_coordinates[2][1][0] and arr_coordinates[2][0][1] < y < \
                arr_coordinates[2][1][
                    1]:
            self.green_wire.update()
            self.wire_script("green")
        elif arr_coordinates[3][0][0] < x < arr_coordinates[3][1][0] and arr_coordinates[3][0][1] < y < \
                arr_coordinates[3][1][
                    1]:
            self.people_wire.update()
            self.wire_script("people")
        elif arr_coordinates[4][0][0] < x < arr_coordinates[4][1][0] and arr_coordinates[4][0][1] < y < \
                arr_coordinates[4][1][
                    1]:
            self.pazzle_conjugate_operator.update()
            self.sequence_fun("pazzle_conjugate_operator")
        elif arr_coordinates[5][0][0] < x < arr_coordinates[5][1][0] and arr_coordinates[5][0][1] < y < \
                arr_coordinates[5][1][
                    1]:
            self.pazzle_transposition_matrix.update()
            self.sequence_fun("pazzle_transposition_matrix")
        elif arr_coordinates[6][0][0] < x < arr_coordinates[6][1][0] and arr_coordinates[6][0][1] < y < \
                arr_coordinates[6][1][
                    1]:
            self.pazzle_matrix_unit.update()
            self.sequence_fun("pazzle_matrix_unit")
        elif arr_coordinates[7][0][0] < x < arr_coordinates[7][1][0] and arr_coordinates[7][0][1] < y < \
                arr_coordinates[7][1][
                    1]:
            self.pazzle_tensor_product.update()
            self.sequence_fun("pazzle_tensor_product")
        elif arr_coordinates[8][0][0] < x < arr_coordinates[8][1][0] and arr_coordinates[8][0][1] < y < \
                arr_coordinates[8][1][
                    1]:
            self.code_number.update()


class LoadHardScript:
    def __init__(self, wire, sequence, code_number, serial_number, button_click):
        self.ending = False
        self.click = False
        self.wire = wire
        self.button_click = button_click
        self.sequence = sequence
        self.sequence_count = 0
        self.count_button_click = 0
        self.serial_number = serial_number
        self.dict_serial_numbers = {'number_EA500.png': 2, "number_22081921.png": 3, "number_517B.png": 4,
                                    "number_3A3CC9.png": 7}
        self.arr_coordinates = [
            ((60, 202), (89, 278)),
            ((100, 201), (129, 279)),
            ((140, 202), (168, 278)),
            ((180, 202), (209, 279)),
            ((221, 202), (246, 276)),
            ((313, 434), (363, 467)),
            ((311, 492), (562, 541)),
            ((377, 243), (515, 351)),
            ((555, 273), (583, 302)),

            ((671, 223), (736, 286)),
            ((750, 221), (817, 286)),
            ((672, 301), (740, 366)),
            ((750, 300), (819, 366))

        ]

        self.red_wire = AnimatedSprite(pygame.transform.scale(load_image('red_wire.png'), (60, 80)), 2, 1, 60, 200, 30,
                                       80, True)
        self.blue_wire = AnimatedSprite(pygame.transform.scale(load_image('blue_wire.png'), (60, 80)), 2, 1, 100, 200,
                                        30,
                                        80, True)
        self.green_wire = AnimatedSprite(pygame.transform.scale(load_image('green_wire.png'), (60, 80)), 2, 1, 140, 200,
                                         30,
                                         80, True)
        self.people_wire = AnimatedSprite(pygame.transform.scale(load_image('people_wire.png'), (60, 80)), 2, 1, 180,
                                          200,
                                          30,
                                          80, True)
        self.yellow_wire = AnimatedSprite(pygame.transform.scale(load_image('yellow_wire.png'), (60, 80)), 2, 1, 220,
                                          200,
                                          30,
                                          80, True)
        self.pazzle_conjugate_operator = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_conjugate_operator.png'), (140, 70)), 2, 1, 670,
            220,
            70,
            70, True)
        self.pazzle_transposition_matrix = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_transposition_matrix.png'), (140, 70)), 2, 1, 750,
            220,
            70,
            70, True)
        self.pazzle_tensor_product = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_tensor_product.png'), (140, 70)), 2, 1, 750,
            300,
            70,
            70, True)
        self.pazzle_matrix_unit = AnimatedSprite(
            pygame.transform.scale(load_image('pazzle_matrix_unit.png'), (140, 70)), 2, 1, 670,
            300,
            70,
            70, True)
        self.indicator_button = AnimatedSpriteIndicator(
            pygame.transform.scale(load_image('indicator_metal.png'), (80, 40)),
            2, 1, 545,
            150,
            40, 40, True)
        self.indicator_wire = AnimatedSpriteIndicator(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2,
                                                      1, 246,
                                                      155,
                                                      40, 40, True)
        self.indicator_pazzle = AnimatedSpriteIndicator(
            pygame.transform.scale(load_image('indicator_metal.png'), (80, 40)), 2,
            1, 860,
            150,
            40, 40, True)
        self.button = AnimatedSprite(pygame.transform.scale(load_image('button.png'), (400, 150)), 2, 1, 345, 220, 200,
                                     150, False)
        self.mini_button = AnimatedSprite(pygame.transform.scale(load_image('mini_button.png'), (140, 210)), 4,
                                          2, 552,
                                          270,
                                          35, 35, False)
        self.code_number = AnimatedSpriteIndicator(pygame.transform.scale(load_image(code_number), (300, 40)), 2,
                                                   1, 310,
                                                   430,
                                                   150, 40, False)
        self.serial_number_sprite = AnimatedSprite(
            pygame.transform.scale(load_image(serial_number), (510, 54 * self.dict_serial_numbers[serial_number])), 2,
            self.dict_serial_numbers[serial_number], 310,
            490,
            255, 54, True)

        self.arr_indicators = {self.indicator_wire: False, self.indicator_pazzle: False}

    def wire_script(self, wire):
        pass
        if wire != self.wire:
            check_winner.control_check()
        else:
            self.indicator_wire.update()

    def func_button_click(self, button_count):
        if button_count != self.button_click:
            check_winner.control_check()
        else:
            self.indicator_button.update()

    def sequence_fun(self, symbol):
        pass
        if not self.arr_indicators[self.indicator_pazzle]:
            if symbol == self.sequence[self.sequence_count]:
                self.sequence_count += 1
            else:
                check_winner.control_check()
            if self.sequence_count == 4:
                self.indicator_pazzle.update()

    def down_button(self, pos):
        x, y = pos
        arr_coordinates = load_script.arr_coordinates
        print(x, y)
        if arr_coordinates[5][0][0] < x < arr_coordinates[5][1][0] and arr_coordinates[5][0][1] < y < \
                arr_coordinates[5][1][
                    1]:
            self.code_number.update()
        elif arr_coordinates[7][0][0] < x < arr_coordinates[7][1][0] and arr_coordinates[7][0][1] < y < \
                arr_coordinates[7][1][
                    1]:
            self.count_button_click += 1
            self.mini_button.update()

    def sorted_coordinates(self, pos):
        x, y = pos
        arr_coordinates = load_script.arr_coordinates
        if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < \
                arr_coordinates[0][1][
                    1]:
            self.red_wire.update()
            self.wire_script("red")
        elif arr_coordinates[1][0][0] < x < arr_coordinates[1][1][0] and arr_coordinates[1][0][1] < y < \
                arr_coordinates[1][1][
                    1]:
            self.blue_wire.update()
            self.wire_script("blue")
        elif arr_coordinates[2][0][0] < x < arr_coordinates[2][1][0] and arr_coordinates[2][0][1] < y < \
                arr_coordinates[2][1][
                    1]:
            self.green_wire.update()
            self.wire_script("green")
        elif arr_coordinates[3][0][0] < x < arr_coordinates[3][1][0] and arr_coordinates[3][0][1] < y < \
                arr_coordinates[3][1][
                    1]:
            self.people_wire.update()
            self.wire_script("people")
        elif arr_coordinates[4][0][0] < x < arr_coordinates[4][1][0] and arr_coordinates[4][0][1] < y < \
                arr_coordinates[4][1][
                    1]:
            self.yellow_wire.update()
            self.wire_script("yellow")
        elif arr_coordinates[5][0][0] < x < arr_coordinates[5][1][0] and arr_coordinates[5][0][1] < y < \
                arr_coordinates[5][1][
                    1]:
            self.code_number.update()
        elif arr_coordinates[6][0][0] < x < arr_coordinates[6][1][0] and arr_coordinates[6][0][1] < y < \
                arr_coordinates[6][1][
                    1]:
            self.serial_number_sprite.update()
        elif arr_coordinates[7][0][0] < x < arr_coordinates[7][1][0] and arr_coordinates[7][0][1] < y < \
                arr_coordinates[7][1][
                    1]:
            self.button.update()
            self.mini_button.update()
        elif arr_coordinates[8][0][0] < x < arr_coordinates[8][1][0] and arr_coordinates[8][0][1] < y < \
                arr_coordinates[8][1][
                    1]:
            self.func_button_click(self.count_button_click)
        elif arr_coordinates[9][0][0] < x < arr_coordinates[9][1][0] and arr_coordinates[9][0][1] < y < \
                arr_coordinates[9][1][
                    1]:
            self.pazzle_conjugate_operator.update()
            self.sequence_fun("pazzle_conjugate_operator")
        elif arr_coordinates[10][0][0] < x < arr_coordinates[10][1][0] and arr_coordinates[10][0][1] < y < \
                arr_coordinates[10][1][
                    1]:
            self.pazzle_transposition_matrix.update()
            self.sequence_fun("pazzle_transposition_matrix")
        elif arr_coordinates[11][0][0] < x < arr_coordinates[11][1][0] and arr_coordinates[11][0][1] < y < \
                arr_coordinates[11][1][
                    1]:
            self.pazzle_matrix_unit.update()
            self.sequence_fun("pazzle_matrix_unit")
        elif arr_coordinates[12][0][0] < x < arr_coordinates[12][1][0] and arr_coordinates[12][0][1] < y < \
                arr_coordinates[12][1][
                    1]:
            self.pazzle_tensor_product.update()
            self.sequence_fun("pazzle_tensor_product")


class CheckWinner:
    def __init__(self):
        self.running = True

    def check(self):
        return self.running

    def control_check(self):
        self.running = False


def lose_window():
    fon_lose_menu = AnimatedSprite(pygame.transform.scale(load_image('lose_main.png'), (2000, 600)), 2, 1, 0, 0, 1000,
                                   600, False)
    time = datetime.now()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        if time.second != datetime.now().second:
            print(time.second, datetime.now().second)
            time = datetime.now()
            fon_lose_menu.update()
        all_sprites.draw(screen)
        pygame.display.flip()


class ManageDataBase:
    def __init__(self):
        self.con = sqlite3.connect("data_base.sqlite")
        self.cur = self.con.cursor()

    def create_a_cell(self):
        self.cur.execute("""INSERT INTO statistic(record_time, count_win) VALUES(0, 0);""").fetchall()

    def changing_a_cell(self, parameter):
        if parameter == "win":
            self.cur.execute("""UPDATE statistic SET count_win = count_win + 1;""")
        else:
            update_query = "UPDATE statistic SET record_time = ?;"
            self.cur.execute(update_query, (parameter,))
        self.con.commit()

    def return_data_base(self):
        return self.cur.execute("""SELECT * FROM statistic""").fetchall()

    def close(self):
        self.con.close()


manage_data_base = ManageDataBase()
if not manage_data_base.return_data_base():
    manage_data_base.create_a_cell()

while True:
    all_sprites = pygame.sprite.Group()
    res = start_screen()
    if res == "easy_level":
        generate_level('bomb')
        easy_levels = [("blue", 1, "number_517B.png"),
                       ("green", 6, 'number_EA500.png'),
                       ("blue", 3, "number_22081921.png"),
                       ("red", 2, "number_3A3CC9.png")]
        level = choice(easy_levels)
        load_script = LoadEasyScript(*level)
    if res == "medium_level":
        medium_levels = [
            ("blue", (
                "pazzle_transposition_matrix", "pazzle_conjugate_operator", "pazzle_tensor_product",
                "pazzle_matrix_unit"),
             "code_1_1_1.png"),
            ("red", (
                'pazzle_transposition_matrix', 'pazzle_tensor_product', 'pazzle_conjugate_operator',
                'pazzle_matrix_unit'),
             "code_1_0_1.png"),
            ("green", (
                'pazzle_conjugate_operator', 'pazzle_matrix_unit', 'pazzle_tensor_product',
                'pazzle_transposition_matrix'),
             "code_0_1_1.png"),
            ("people", (
                'pazzle_matrix_unit', 'pazzle_conjugate_operator', 'pazzle_tensor_product',
                'pazzle_transposition_matrix'),
             "code_1_1_0.png")
        ]
        generate_level('bomb_medium_level')
        level = choice(medium_levels)
        load_script = LoadMediumScript(*level)
    if res == "hard_level":
        generate_level('bomb_hard_level')
        medium_levels = [
            ("blue", (
                "pazzle_transposition_matrix", "pazzle_conjugate_operator", "pazzle_tensor_product",
                "pazzle_matrix_unit"), "code_1_0_1.png", "number_517B.png", 3),
            ("red", (
                "pazzle_transposition_matrix", "pazzle_tensor_product",
                "pazzle_matrix_unit", "pazzle_conjugate_operator"),
             "code_1_1_1.png", "number_EA500.png", 4),
            ("green", (
                "pazzle_tensor_product", "pazzle_matrix_unit", "pazzle_conjugate_operator",
                "pazzle_transposition_matrix"),
             "code_1_1_0.png", "number_22081921.png", 7),
            ("people", (
                'pazzle_matrix_unit', 'pazzle_conjugate_operator', 'pazzle_tensor_product',
                'pazzle_transposition_matrix'),
             "code_1_1_0.png", "number_3A3CC9.png", 9),
            ("yellow", (
                'pazzle_matrix_unit', 'pazzle_tensor_product', 'pazzle_conjugate_operator',
                'pazzle_transposition_matrix'),
             "code_0_1_1.png", "number_22081921.png", 5)
        ]
        level = choice(medium_levels)
        load_script = LoadHardScript(*level)
    clock_in_half_hour = datetime.now() + timedelta(seconds=80)  # <== Тут можно менять время
    check_winner = CheckWinner()


    def main_cycle():
        clock = pygame.time.Clock()
        pygame.display.set_caption("bomb disposal simulator")
        FPS = 60
        f2 = pygame.font.SysFont('serif', 28)
        count_button = pygame.font.SysFont('serif', 28)
        pos = (0, 0)
        while check_winner.check():
            clock.tick(FPS)
            screen.fill(WHILE)
            time_new = datetime.now()
            if time_new.strftime('%H:%M %S') == clock_in_half_hour.strftime('%H:%M %S'):
                check_winner.control_check()
            all_sprites.draw(screen)
            time = clock_in_half_hour - time_new
            count_button_click = count_button.render(str(load_script.count_button_click), False,
                                                     (0, 0, 0))
            time_render = f2.render(str(time.seconds), False,
                                    (255, 0, 0))
            screen.blit(time_render, (155, 355))
            if res == "easy_level":
                screen.blit(count_button_click, (520, 165))
            elif res == "hard_level":
                screen.blit(count_button_click, (445, 158))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    check_winner.control_check()
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    down_button(pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    push_button(pos)
            pygame.display.flip()
        finish_menu(time.seconds, res) if load_script.ending else lose_window()


    main_cycle()
