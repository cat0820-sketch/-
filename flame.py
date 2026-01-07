import pygame
from settings import TILE, RED

class Flame:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.timer = 30  # 表示フレーム数

        # 見た目（赤い四角）
        self.image = pygame.Surface((TILE, TILE))
        self.image.fill(RED)

    def update(self):
        self.timer -= 1
        return self.timer <= 0  # Trueなら消える

    def draw(self, screen):
        # 念のためマップ外ガード
        if self.col < 0 or self.row < 0:
            return

        screen.blit(
            self.image,
            (self.col * TILE, self.row * TILE)
        )
