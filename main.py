import pygame
import sys
import os

pygame.init()

RED = pygame.Color("red")
GREEN = pygame.Color("#00FF00")
BLUE = pygame.Color(0, 0, 225)
BLACK = pygame.Color("#000000")
WHILE = pygame.Color(255, 255, 255)
rgb = (BLUE, GREEN, RED)
SIZE = W, H = (1000, 600)
screen = pygame.display.set_mode(SIZE)

# группы спрайтов
all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, size_x, size_y, flag):
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
        elif not self.flag:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


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
    'fon': pygame.transform.scale(load_image('fon_menu.png'), (1000, 600)),
    'bomb': pygame.transform.scale(load_image('bomb_3_lvl.png'), (900, 500))
}


def terminate():
    pygame.quit()
    sys.exit()


def generate_level():
    Fon()
    Bomb1LVLDraw(1, 1)


def main_menu():
    fon = pygame.transform.scale(load_image('fon_menu.png'), (W, H))
    screen.blit(fon, (0, 0))
    Fon()
    button_back = AnimatedSprite(pygame.transform.scale(load_image('back_button.png'), (600, 150)),
                                 2, 1, 10, 10, 300,
                                 150, False)
    easy_level_button = AnimatedSprite(pygame.transform.scale(load_image('easy_level_button.png'), (600, 150)),
                                       2, 1, 500, 10, 300,
                                       150, False)
    flag_button_back = True
    flag_button_easy_level = True
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x, y)
                if 10 < x < 390 and 10 < y < 160:
                    return "main_menu"
                if 500 < x < 800 and 10 < y < 150:
                    print(1)
                    return "easy_level"
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
    button_reg = AnimatedSprite(pygame.transform.scale(load_image('button_menu_games.png'), (800, 150)), 2, 1, 10,
                                10,
                                400,
                                150, False)
    flag_button_reg = True
    flag_button_start = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 349 < x < 659 and 202 < y < 346:
                    result = main_menu()
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
                        button_reg = AnimatedSprite(
                            pygame.transform.scale(load_image('button_menu_games.png'), (800, 150)), 2, 1, 10,
                            10,
                            400,
                            150, False)
                if 10 < x < 410 and 10 < y < 160:
                    print(1)
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if 349 < x < 659 and 202 < y < 346 and flag_button_start:
                    button_start.update()
                    flag_button_start = False
                elif (not 349 < x < 659 or not 202 < y < 346) and not flag_button_start:
                    button_start.update()
                    flag_button_start = True
                if 10 < x < 410 and 10 < y < 160 and flag_button_reg:
                    flag_button_reg = False
                    button_reg.update()
                elif (not 10 < x < 410 or not 10 < y < 160) and not flag_button_reg:
                    flag_button_reg = True
                    button_reg.update()
        all_sprites.draw(screen)
        pygame.display.flip()


def push_button(pos):
    if True:
        sorted_coordinates(pos)


def down_button(pos):
    x, y = pos
    arr_coordinates = load_script.arr_coordinates
    if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < arr_coordinates[0][1][
        1]:
        sorted_coordinates(pos)
        load_script.count_button_click += 1


def sorted_coordinates(pos):
    x, y = pos
    print(x, y)
    arr_coordinates = load_script.arr_coordinates
    if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < arr_coordinates[0][1][
        1]:
        load_script.button.update()
        load_script.mini_button.update()
    elif arr_coordinates[1][0][0] < x < arr_coordinates[1][1][0] and arr_coordinates[1][0][1] < y < \
            arr_coordinates[1][1][
                1]:
        load_script.red_wire.update()
        load_script.wire_script("red")
    elif arr_coordinates[2][0][0] < x < arr_coordinates[2][1][0] and arr_coordinates[2][0][1] < y < \
            arr_coordinates[2][1][
                1]:
        load_script.blue_wire.update()
        load_script.wire_script("blue")
    elif arr_coordinates[3][0][0] < x < arr_coordinates[3][1][0] and arr_coordinates[3][0][1] < y < \
            arr_coordinates[3][1][
                1]:
        load_script.green_wire.update()
        load_script.wire_script("green")
    elif arr_coordinates[4][0][0] < x < arr_coordinates[4][1][0] and arr_coordinates[4][0][1] < y < \
            arr_coordinates[4][1][
                1]:
        load_script.serial_number_sprite.update()
    elif arr_coordinates[5][0][0] < x < arr_coordinates[5][1][0] and arr_coordinates[5][0][1] < y < \
            arr_coordinates[5][1][
                1]:
        load_script.func_button_click(load_script.count_button_click)


class Fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = tile_images["fon"]
        self.rect = self.image.get_rect().move(
            0, 0)


class Bomb1LVLDraw(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images["bomb"]
        self.rect = self.image.get_rect().move(
            pos_x * 50, pos_y * 50)


class LoadEasyScript:
    def __init__(self, wire, button_click, serial_number):
        self.wire = wire
        self.button_click = button_click
        self.count_button_click = 0
        self.serial_number = serial_number
        self.arr_coordinates = [((459, 290), (585, 383)), ((81, 193), (110, 269)), ((139, 190), (170, 268)),
                                ((200, 191), (230, 268)), ((104, 84), (250, 130)), ((673, 334), (715, 381))]
        self.arr_wire = ["blue", "red", "green"]

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
        self.indicator_wire = AnimatedSprite(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2, 1, 246,
                                             155,
                                             40, 40, True)
        self.indicator_button = AnimatedSprite(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2, 1, 670,
                                               220,
                                               40, 40, True)
        self.serial_number_sprite = AnimatedSprite(pygame.transform.scale(load_image('number_517B.png'), (510, 216)), 2,
                                                   4, 60,
                                                   80,
                                                   255, 54, True)
        self.mini_button = AnimatedSprite(pygame.transform.scale(load_image('mini_button.png'), (204, 324)), 4,
                                          2, 669,
                                          330,
                                          51, 54, False)

    def wire_script(self, wire):
        if wire != self.wire:
            print("Ну всо")
        else:
            self.indicator_wire.update()

    def func_button_click(self, button_count):
        if button_count != self.button_click:
            print("Бах")
        else:
            self.indicator_button.update()
            print("оке")


clock = pygame.time.Clock()
pygame.display.set_caption("bomb disposal simulator")
running = True
FPS = 60
print(all_sprites)
if start_screen() == "easy_level":
    generate_level()
    load_script = LoadEasyScript("red", 3, "517B")
while running:
    clock.tick(FPS)
    screen.fill(WHILE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            push_button(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            down_button(event.pos)
    all_sprites.draw(screen)
    pygame.display.flip()
terminate()
