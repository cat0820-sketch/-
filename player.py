import pygame
from settings import TILE, IMAGE_DIR
from bomb import Bomb
import os
class Player:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.max_bombs = 1
        self.move_cooldown = 0
        self.move_interval = 12

        image_path = os.path.join(IMAGE_DIR, "player.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE, TILE))
        else:
            print(f"{image_path} が見つかりません。緑で代用します。")
            self.image = pygame.Surface((TILE, TILE))
            self.image.fill((0, 200, 0))

    def place_bomb(self, bombs):
        active = sum(1 for b in bombs if b.owner == "player")
        if active >= self.max_bombs: return
        if any(b.col == self.col and b.row == self.row for b in bombs): return
        bombs.append(Bomb(self.col, self.row, owner="player"))

    def move(self, keys, game_map, bombs):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return

        dc = dr = 0
        if keys[pygame.K_LEFT]: dc = -1
        elif keys[pygame.K_RIGHT]: dc = 1
        elif keys[pygame.K_UP]: dr = -1
        elif keys[pygame.K_DOWN]: dr = 1
        else: return

        nc, nr = self.col + dc, self.row + dr
        if game_map.can_move(nc, nr, bombs):
            self.col, self.row = nc, nr
            self.move_cooldown = self.move_interval

    def draw(self, screen):
        screen.blit(self.image, (self.col*TILE, self.row*TILE))
