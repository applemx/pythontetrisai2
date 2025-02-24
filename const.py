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
DOUBLE = -100
TRIPLE = -100
TETRIS = 500
ILIMIT = 10


#weight
WEIGHTAGG = -0.3532094402994673
WEIGHTHOLES = 2.6718670094062587
WEIGHTBUMP = 1.1335454293812393
WEIGHTQUAD = 1.0403058682028303
WEIGHTLINES = 0.9877719121956348
WEIGHTSINGLE = 4.532751185724388
WEIGHTDOUBLE = 2.30685472904432
WEIGHTTRIPLE = 2.2342213833061417
WEIGHTILIMIT = 0.910767174047026
WEIGHTTETRIS = 4.120129202054855

