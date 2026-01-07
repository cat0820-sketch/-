import pygame
import os
from settings import TILE, IMAGE_DIR

class GameMap:
    def __init__(self, stage_data):
        # stage_data は必ず2次元リスト
        if not isinstance(stage_data, list) or not all(isinstance(row, list) for row in stage_data):
            raise ValueError("stage は 2次元リストで渡してください")
        self.stage = stage_data

        self.height = len(stage_data)
        self.width = len(stage_data[0])

        # 画像読み込み（ない場合は床画像を代用）
        try:
            self.wall_img = pygame.image.load(os.path.join(IMAGE_DIR, "wall.png"))
        except FileNotFoundError:
            print("wall.png がないため灰色で代用します")
            self.wall_img = pygame.Surface((TILE, TILE))
            self.wall_img.fill((100,100,100))

        try:
            self.breakable_img = pygame.image.load(os.path.join(IMAGE_DIR, "breakable.png"))
        except FileNotFoundError:
            print("breakable.png がないため黄色で代用します")
            self.breakable_img = pygame.Surface((TILE, TILE))
            self.breakable_img.fill((200,200,100))

        try:
            self.floor_img = pygame.image.load(os.path.join(IMAGE_DIR, "floor.png"))
        except FileNotFoundError:
            print("floor.png がないため灰色で代用します")
            self.floor_img = pygame.Surface((TILE, TILE))
            self.floor_img.fill((150,150,150))

        # サイズ調整
        self.wall_img = pygame.transform.scale(self.wall_img, (TILE, TILE))
        self.breakable_img = pygame.transform.scale(self.breakable_img, (TILE, TILE))
        self.floor_img = pygame.transform.scale(self.floor_img, (TILE, TILE))

    def draw(self, screen):
        """ステージを描画する"""
        for row_idx, row in enumerate(self.stage):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE
                y = row_idx * TILE
                screen.blit(self.floor_img, (x, y))
                if tile == 1:
                    screen.blit(self.wall_img, (x, y))
                elif tile == 2:
                    screen.blit(self.breakable_img, (x, y))

    def destroy_block(self, col, row):
        """壊せる壁を消す"""
        if 0 <= row < len(self.stage) and 0 <= col < len(self.stage[0]):
            if self.stage[row][col] == 2:
                self.stage[row][col] = 0

    def can_move(self, col, row, bombs):
        """
        指定マスが移動可能か判定する
        - 壁(1)・壊せる壁(2)は不可
        - 置かれている爆弾も不可
        """
        # マップ範囲チェック
        if row < 0 or row >= len(self.stage) or col < 0 or col >= len(self.stage[0]):
            return False

        # 壁・壊せる壁チェック
        if self.stage[row][col] in (1, 2):
            return False

        # 置かれている爆弾チェック
        for bomb in bombs:
            if bomb.col == col and bomb.row == row:
                return False

        return True

    def is_inside(self, col, row):
        return 0 <= col < self.width and 0 <= row < self.height

    def is_wall(self, col, row):
        if not self.is_inside(col, row):
            return True
        # 壁 or 壊せないブロック
        return self.stage[row][col] == 1
