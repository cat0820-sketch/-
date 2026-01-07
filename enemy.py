import pygame
import os
import random
from settings import TILE, IMAGE_DIR
from bomb import Bomb

class Enemy:
    def __init__(self, col, row):
        self.col = col
        self.row = row

        self.dead = False
        self.my_bombs = []

        self.evading = False

        # ===== 移動クールダウン =====
        self.move_cooldown = 0
        self.move_interval = 24

        self.bomb_cooldown = 0
        self.bomb_interval = 120

        # ===== 役割（連携用）=====
        self.role = random.choice([
            "chaser_left",
            "chaser_right",
            "blocker"
        ])

        image_path = os.path.join(IMAGE_DIR, "enemy.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE, TILE))
        else:
            self.image = pygame.Surface((TILE, TILE))
            self.image.fill((150,150,150))

    # ==================================================
    # 更新処理
    # ==================================================
    def update(self, game_map, player, bombs):
        if self.dead:
            return

        # 移動クールダウン
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        self.move_cooldown = self.move_interval

        # 爆弾回避中
        if self.evading:
            self.escape_move(game_map, bombs)
            return

        # ===== 連携AI =====
        if self.role == "chaser_left":
            self.surround_player(player, game_map, bombs, side="left")
        elif self.role == "chaser_right":
            self.surround_player(player, game_map, bombs, side="right")
        else:
            self.block_player(player, game_map, bombs)

        self.normal_move(game_map, bombs, player)

    def draw(self, screen):
        screen.blit(self.image, (self.col * TILE, self.row * TILE))

    # ==================================================
    # 行動ロジック
    # ==================================================

    def normal_move(self, game_map, bombs, player):
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1

        if abs(self.col - player.col) + abs(self.row - player.row) <= 2:
            if self.can_place_bomb_safely(game_map, bombs):
                self.place_bomb(bombs)
                self.bomb_cooldown = self.bomb_interval

    def surround_player(self, player, game_map, bombs, side):
        dx = player.col - self.col
        dy = player.row - self.row

        if abs(dx) >= abs(dy):
            target_col = player.col
            target_row = player.row + (1 if side == "left" else -1)
        else:
            target_col = player.col + (1 if side == "left" else -1)
            target_row = player.row

        self.move_towards(target_col, target_row, game_map, bombs)

    def move_towards(self, tc, tr, game_map, bombs):
        best = None
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            nc = self.col + dc
            nr = self.row + dr
            if not game_map.can_move(nc, nr, bombs):
                continue
            dist = abs(nc - tc) + abs(nr - tr)
            if best is None or dist < best[0]:
                best = (dist, nc, nr)

        if best:
            self.col = best[1]
            self.row = best[2]

    def block_player(self, player, game_map, bombs):
        dx = player.col - self.col
        dy = player.row - self.row
        tc = player.col + (1 if dx > 0 else -1 if dx < 0 else 0)
        tr = player.row + (1 if dy > 0 else -1 if dy < 0 else 0)
        self.move_towards(tc, tr, game_map, bombs)

    # ==================================================
    # 爆弾回避（★ここが重要）
    # ==================================================
    def escape_move(self, game_map, bombs):
        # ----- 危険判定 -----
        danger = False
        for b in bombs:
            if abs(self.col - b.col) + abs(self.row - b.row) <= 2:
                danger = True
                break

        # もう安全なら回避終了
        if not danger:
            self.evading = False
            return

        # ----- 逃げる方向を探す -----
        best = None
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            nc = self.col + dc
            nr = self.row + dr
            if not game_map.can_move(nc, nr, bombs):
                continue

            score = 0
            for b in bombs:
                score += abs(nc - b.col) + abs(nr - b.row)

            if best is None or score > best[0]:
                best = (score, nc, nr)

        if best:
            self.col = best[1]
            self.row = best[2]

    # ==================================================
    # 爆弾
    # ==================================================
    def place_bomb(self, bombs):
        if any(b.owner == "enemy" for b in bombs):
            return
        bomb = Bomb(self.col, self.row, owner="enemy")
        bombs.append(bomb)
        self.my_bombs.append(bomb)
        self.evading = True

    def can_place_bomb_safely(self, game_map, bombs):
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            if game_map.can_move(self.col + dc, self.row + dr, bombs):
                return True
        return False
