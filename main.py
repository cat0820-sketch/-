import pygame
import sys
from settings import *
from map import GameMap
from player import Player
from enemy import Enemy
from flame import Flame
from bomb import Bomb

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ステージ番号管理
stage_number = 1

# ステージデータ
stages = {
    1: [
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,2,0,2,0,0,0,0,0,1],
        [1,0,1,0,1,2,0,0,1,0,1,0,1],
        [1,0,2,0,0,0,0,0,2,0,2,0,1],
        [1,2,1,2,1,2,0,2,1,2,1,2,1],
        [1,0,2,0,2,0,0,0,0,0,2,0,1],
        [1,2,1,2,1,2,1,2,1,2,1,2,1],
        [1,0,0,0,2,0,2,0,2,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
    2: [
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,2,1,2,1,2,1,0,1,2,1,2,1],
        [1,0,2,0,2,0,2,0,2,0,2,0,1],
        [1,2,1,2,1,0,1,0,1,0,1,2,1],
        [1,0,2,0,2,0,2,0,0,0,0,0,1],
        [1,2,1,2,1,0,1,2,1,0,1,2,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
}

# 初期マップ生成
game_map = GameMap(stages[stage_number])
player = Player(1, 1)

# 初期敵配置
enemies = [Enemy(7, 3)]
bombs = []
flames = []

while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.place_bomb(bombs)

    keys = pygame.key.get_pressed()
    player.move(keys, game_map, bombs)

    # 画面描画
    screen.fill(BLACK)
    game_map.draw(screen)

    # 💣 爆弾処理
    for bomb in bombs[:]:
        new_flames = bomb.update(game_map)
        if bomb.exploded:
            if bomb in bombs:
                bombs.remove(bomb)
            # 敵の持つ爆弾も解除
            for enemy in enemies:
                if bomb in enemy.my_bombs:
                    enemy.my_bombs.remove(bomb)
            flames.extend(new_flames)
        else:
            bomb.draw(screen)

    # 敵更新
    for enemy in enemies:
        enemy.update(game_map, player, bombs)
        enemy.draw(screen)

    # 🔥 炎処理 & 死亡判定
    for flame in flames[:]:
        if flame.update():
            flames.remove(flame)
            continue

        flame.draw(screen)
        game_map.destroy_block(flame.col, flame.row)

        if flame.col == player.col and flame.row == player.row:
            pygame.quit()
            sys.exit()

        for enemy in enemies:
            if flame.col == enemy.col and flame.row == enemy.row:
                enemy.dead = True

    enemies = [e for e in enemies if not e.dead]

    # 🏁 正しいステージクリア判定
    if len(enemies) == 0 and len(flames) == 0:
        stage_number += 1
        if stage_number in stages:
            game_map = GameMap(stages[stage_number])
            player.col, player.row = 1, 1
            # ステージごとの敵配置
            if stage_number == 2:
                enemies = [Enemy(7,3), Enemy(4,7)]
            else:
                enemies = []
            bombs.clear()
            flames.clear()
        else:
            print("全ステージクリア！")
            pygame.quit()
            sys.exit()

    player.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
