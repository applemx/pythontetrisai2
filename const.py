# const.py

# --- 盤面関連の定数 ---
WIDTH = 10
HEIGHT = 20

# --- ミノの出現位置 ---
MINOS_DEFAULT_X= 3

# --- ミノ形状の定義(回転前) ---
MINOS = [
    [[1, 1, 1, 1]],         # I
    [[1, 1, 1],
     [0, 1, 0]],            # T
    [[1, 1, 1],
     [1, 0, 0]],            # L
    [[1, 1, 1],
     [0, 0, 1]],            # J
    [[1, 1],
     [1, 1]],               # O
    [[0, 1, 1],
     [1, 1, 0]],            # S
    [[1, 1, 0],
     [0, 1, 1]]             # Z
]

# ミノの種類(文字)をMINOS配列のインデックスに対応させる辞書
MINO_TYPE_TO_INDEX = {
    'I': 0,
    'T': 1,
    'L': 2,
    'J': 3,
    'O': 4,
    'S': 5,
    'Z': 6
}

# --- スコア表 ---
# 行数に応じた得点 (オールクリアでない場合)
LINES_SCORE = {
    1: 100,
    2: 300,
    3: 500,
    4: 800
}

# 行数 + オールクリア時の加点
ALL_CLEAR_SCORE = {
    1: 800,
    2: 1200,
    3: 1800,
    4: 2000
}

# 探索設定
DEPTH_LIMIT = 7
BEAM_WIDTH = 7

#evaluate

# --- ライン消去時の得点 ---　
SINGLE = -100
DOUBLE = -70
TRIPLE = -50
TETRIS = 1000
PC = 10000000

#weight
WEIGHTAGG = 1
WEIGHTHOLES = 4
WEIGHTBUMP = 2
WEIGHTQUAD = 10
WEIGHTLINES = 1 #多分これは固定