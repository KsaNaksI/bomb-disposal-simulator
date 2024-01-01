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

# группа координат
#                  Кнопка                    красный провод           синий  провод             зелёный провод
arr_coordinates = [((459, 290), (585, 383)), ((81, 193), (110, 269)), ((139, 190), (170, 268)),
                   ((200, 191), (230, 268))]
dict_wire = {"blue": True, "red": True, "green": True}
first_script = ["red", ]



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
    'fon': pygame.transform.scale(load_image('fon2.png'), (1000, 600)),
    'bomb': pygame.transform.scale(load_image('bomb_3_lvl.png'), (900, 500))
}


def terminate():
    pygame.quit()
    sys.exit()


def generate_level():
    Fon()
    Bomb1LVLDraw(1, 1)


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), (W, H))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def push_button(pos):
    if True:
        sorted_coordinates(pos)


def sorted_coordinates(pos):
    x, y = pos
    print(x, y)
    if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < arr_coordinates[0][1][
        1]:
        return "button"
    elif arr_coordinates[1][0][0] < x < arr_coordinates[1][1][0] and arr_coordinates[1][0][1] < y < \
            arr_coordinates[1][1][
                1] and dict_wire["red"]:
        dict_wire["red"] = False
        red_wire.update()
        load_script.wire_script("red")
    elif arr_coordinates[2][0][0] < x < arr_coordinates[2][1][0] and arr_coordinates[2][0][1] < y < \
            arr_coordinates[2][1][
                1] and dict_wire["blue"]:
        dict_wire["blue"] = False
        blue_wire.update()
        load_script.wire_script("blue")
    elif arr_coordinates[3][0][0] < x < arr_coordinates[3][1][0] and arr_coordinates[3][0][1] < y < \
            arr_coordinates[3][1][
                1] and dict_wire["green"]:
        green_wire.update()
        dict_wire["green"] = False
        load_script.wire_script("green")


def down_button(pos):
    x, y = pos
    if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < arr_coordinates[0][1][
        1]:
        button.update()


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, size_x, size_y):
        super().__init__(all_sprites)
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
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

class LoadScript:
    def __init__(self, wire, button, serial_number, power):
        self.wire = wire
        self.button = button
        self.serial_number = serial_number
        self.power = power

    def wire_script(self, wire):
        if wire != self.wire:
            print("Ну всо")
        else:
            indicator_wire.update()


clock = pygame.time.Clock()
pygame.display.set_caption("bomb disposal simulator")
running = True
start_screen()
FPS = 60
print(all_sprites)
generate_level()
load_script = LoadScript("red", "click", "1212", "full")
button = AnimatedSprite(pygame.transform.scale(load_image('button.png'), (544, 200)), 2, 1, 380, 240, 272, 200)
red_wire = AnimatedSprite(pygame.transform.scale(load_image('red_wire.png'), (60, 80)), 2, 1, 80, 190, 30, 80)
blue_wire = AnimatedSprite(pygame.transform.scale(load_image('blue_wire.png'), (60, 80)), 2, 1, 140, 190, 30, 80)
green_wire = AnimatedSprite(pygame.transform.scale(load_image('green_wire.png'), (60, 80)), 2, 1, 200, 190, 30, 80)
indicator_wire = AnimatedSprite(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2, 1, 246, 155, 40, 40)
indicator_button = AnimatedSprite(pygame.transform.scale(load_image('indicator.png'), (80, 40)), 2, 1, 670, 220, 40, 40)
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
