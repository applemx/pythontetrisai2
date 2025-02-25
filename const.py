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

#ペナルティ得点
PENALTY_FOR_8 = 100
PENALTY_FOR_12 = 100

#weight
WEIGHTAGG = 0.7320263451068715
WEIGHTHOLES = 4.89755713938711
WEIGHTBUMP = 0.5606084730183616
WEIGHTQUAD = 1.493838374918443
WEIGHTLINES = 0.33291026718952527
WEIGHTSINGLE = 6.571687093979982
WEIGHTDOUBLE = 6.710410225840108
WEIGHTTRIPLE = 3.351174044558223
WEIGHTILIMIT = 2.009736461469682
WEIGHTTETRIS = 5.937961489680006
WEIGHTPENALTY_FOR_8 = -1.3714141417023236
WEIGHTPENALTY_FOR_12 = 2.454636711067569

