import pygame
from math import floor
from random import randint
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((800, 800), vsync = True)
font = pygame.font.Font("assets\\monofont.ttf", 80)
clock = pygame.time.Clock()
size = 10
running = True
time = 0
first_render = True

def load(path):
    img = pygame.image.load(f"assets\\{path}").convert_alpha()
    return pygame.transform.scale(img, (screen.get_width() / size, screen.get_height() / size))

flag = load("flag.png")
unknown = load("unclear.png")
mine = load("mine.png")
nums = {}
for n in range(9):
    nums[n] = load(f"{n}.png")

class State(Enum):
    FLAGGED = 1
    REVEALED = 2
    UNKNOWN = 3

class Mode(Enum):
    MINE = 1
    CLEAR = 2

class Tile:
    def __init__(self, is_mine):
        if is_mine: self.mode = Mode.MINE
        else: self.mode = Mode.CLEAR
        self.state = State.UNKNOWN
        self.adjacent = 0

class Board:
    def __init__(self, size):
        self.won = False
        self.size = size
        self.num_tiles = self.size**2
        self.mine_density = 0.15
        self.grid = [Tile(False) for _ in range(self.num_tiles)]
        self.tile_size = int(screen.get_width() / self.size)
        for _ in range(int(self.num_tiles * self.mine_density)):
            self.grid[randint(0, self.num_tiles - 1)].mode = Mode.MINE
        for idx in range(self.num_tiles):
            for col in range(-1, 2):
                for row in range(-1, 2):
                    if col == 0 and row == 0:
                        continue
                    adjacent_idx = idx + col + row * self.size
                    if adjacent_idx < 0 or adjacent_idx >= self.num_tiles:
                        continue
                    if col + (idx % self.size) < 0 or col + (idx % self.size) >= self.size:
                        continue
                    if self.grid[adjacent_idx].mode == Mode.MINE:
                        self.grid[idx].adjacent += 1
        for idx in range(self.num_tiles):
            if self.grid[idx].mode == Mode.CLEAR and self.grid[idx].adjacent == 0:
                self.click((idx % size) * self.tile_size, floor(idx / size) * self.tile_size)
                break
    
    def render(self, all=False):
        for idx in range(self.num_tiles):
            if self.grid[idx].state == State.REVEALED or all:
                if self.grid[idx].mode == Mode.CLEAR:
                    screen.blit(nums[self.grid[idx].adjacent], ((idx % self.size) * self.tile_size, floor(idx / self.size) * self.tile_size))
                else:
                    screen.blit(mine, ((idx % self.size) * self.tile_size, floor(idx / self.size) * self.tile_size))
            elif self.grid[idx].state == State.UNKNOWN:
                screen.blit(unknown, ((idx % self.size) * self.tile_size, floor(idx / self.size) * self.tile_size))
            elif self.grid[idx].state == State.FLAGGED:
                screen.blit(flag, ((idx % self.size) * self.tile_size, floor(idx / self.size) * self.tile_size))

    def click(self, mx, my):
        x = floor(mx / self.tile_size)
        y = floor(my / self.tile_size)
        idx = x + y * self.size
        if self.grid[idx].mode == Mode.MINE and self.grid[idx].state == State.UNKNOWN:
            return False
        if self.grid[idx].state == State.FLAGGED:
            self.grid[idx].state = State.UNKNOWN
            return True
        if self.grid[idx].mode == Mode.MINE:
            return False
        if self.grid[idx].mode == Mode.CLEAR:
            self.grid[idx].state = State.REVEALED
        if self.grid[idx].adjacent == 0:
            for col in range(-1, 2):
                for row in range(-1, 2):
                    if col == 0 and row == 0:
                        continue
                    adjacent_idx = idx + col + row * self.size
                    if adjacent_idx < 0 or adjacent_idx >= self.num_tiles:
                        continue
                    if col + (idx % self.size) < 0 or col + (idx % self.size) >= self.size:
                        continue
                    if self.grid[adjacent_idx].state != State.REVEALED:
                        self.grid[adjacent_idx].state = State.REVEALED
                        if self.grid[adjacent_idx].adjacent == 0:
                            self.click((adjacent_idx % size) * self.tile_size, floor(adjacent_idx / size) * self.tile_size)
        return True

    def checkwin(self):
        won = True
        for idx in range(self.num_tiles):
            if self.grid[idx].state == State.FLAGGED and self.grid[idx].mode != Mode.MINE:
                won = False
                break
            if self.grid[idx].state != State.FLAGGED and self.grid[idx].mode == Mode.MINE:
                won = False
                break
            if self.grid[idx].state != State.REVEALED and self.grid[idx].mode == Mode.CLEAR:
                won = False
                break
        self.won = won
        return not self.won

    def flag(self, mx, my):
        x = floor(mx / self.tile_size)
        y = floor(my / self.tile_size)
        idx = x + y * self.size
        self.grid[idx].state = State.FLAGGED
            
g = Board(size)

while running:
    dt = clock.tick(10)
    time += dt
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                running = g.click(mx, my)
                if running: running = g.checkwin()
            elif event.button == 3:
                g.flag(mx, my)
                running = g.checkwin()
                
    screen.fill((255,255,255))
    g.render()
    pygame.display.update()

running = True

while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    g.render(all=True)
    if g.won:
        screen.blit(font.render(f"VICTORY! Time: {round(time / 1000, 1)}", False, (0, 0, 0)), (10, 10))
    else:
        screen.blit(font.render("FAILURE!", False, (0, 0, 0)), (10, 10))
    pygame.display.update()
pygame.quit()
