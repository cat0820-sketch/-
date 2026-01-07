import pygame
import os
from settings import TILE, IMAGE_DIR
from flame import Flame

class Bomb:
    def __init__(self, col, row, owner="player"):
        self.col = col
        self.row = row
        self.owner = owner
        self.timer = 60
        self.exploded = False
        self.solid = True

        image_path = os.path.join(IMAGE_DIR, "bomb.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE, TILE))
        else:
            self.image = pygame.Surface((TILE, TILE))
            self.image.fill((200, 200, 0))

    def update(self, game_map):
        self.timer -= 1
        if self.timer > 0:
            return []

        self.exploded = True
        self.solid = False

        flames = [Flame(self.col, self.row)]

        for dc, dr in [(1,0), (-1,0), (0,1), (0,-1)]:
            nc = self.col + dc
            nr = self.row + dr
            if game_map.is_inside(nc, nr) and not game_map.is_wall(nc, nr):
                flames.append(Flame(nc, nr))

        return flames

    def draw(self, screen):
        screen.blit(self.image, (self.col * TILE, self.row * TILE))
