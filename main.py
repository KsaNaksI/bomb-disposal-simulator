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
arr_coordinates = [((459, 290), (585, 383))]


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
    x, y = pos
    if arr_coordinates[0][0][0] < x < arr_coordinates[0][1][0] and arr_coordinates[0][0][1] < y < arr_coordinates[0][1][1]:
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


clock = pygame.time.Clock()
pygame.display.set_caption("bomb disposal simulator")
running = True
start_screen()
FPS = 60
print(all_sprites)
generate_level()
button = AnimatedSprite(pygame.transform.scale(load_image('button.png'), (544, 200)), 2, 1, 380, 240, 272, 200)
while running:
    clock.tick(FPS)
    screen.fill(WHILE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            push_button(event.pos)
    all_sprites.draw(screen)
    pygame.display.flip()
terminate()
