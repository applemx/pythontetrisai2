# board_logic.py

import const
from copy import deepcopy

def create_empty_board():
    """
    20x10の空盤面を作る
    """
    return [[0]*const.WIDTH for _ in range(const.HEIGHT)]

def rotate_mino(mino_2d, rotation):
    """
    rotation: 0,1,2,3 (回転回数)
    """
    if rotation == 0:
        rotated = mino_2d
    elif rotation == 1:
        # 90度(時計回り)
        rotated = list(zip(*mino_2d[::-1]))
    elif rotation == 2:
        # 180度
        rotated = [row[::-1] for row in mino_2d[::-1]]
    elif rotation == 3:
        # 270度
        rotated = list(zip(*mino_2d))[::-1]
    else:
        raise ValueError("rotation must be 0..3")

    # zip()の結果はタプルになるためリスト化
    rotated = [list(row) for row in rotated]
    # 左上に詰める(余分な0行・0列を除去)なら、ここで trim 処理を行う
    return trim_mino(rotated)

def trim_mino(mino):
    """
    ミノの2次元配列から先頭/末尾の空行・空列を取り除く(上左に詰める)
    """
    # 省略 or 実装例省略
    return mino

def can_place_mino(board, mino_2d, start_row, start_col):
    """
    board上にmino_2dを (start_row, start_col) に重ねて衝突しないかチェック
    """
    for r in range(len(mino_2d)):
        for c in range(len(mino_2d[r])):
            if mino_2d[r][c] == 1:
                R = start_row + r
                C = start_col + c
                # 範囲外 or 既存ブロック衝突
                if R < 0 or R >= const.HEIGHT or C < 0 or C >= const.WIDTH:
                    return False
                if board[R][C] == 1:
                    return False
    return True

def drop_mino(board, mino_2d, start_col):
    """
    回転済みのミノを、列 = start_col に落とし、固定する。
    最上段 row=0 付近から順に下へ衝突判定を行っていく簡易実装。
    boardを直接書き換えて固定し、最終的に着地したrowを返す。
    """
    row = 0
    while True:
        if can_place_mino(board, mino_2d, row+1, start_col):
            row += 1
        else:
            break
    # 固定
    for r in range(len(mino_2d)):
        for c in range(len(mino_2d[r])):
            if mino_2d[r][c] == 1:
                board[row+r][start_col+c] = 1
    return row

def clear_lines_and_get_score(board):
    """
    埋まった行を削除してスコアを返す。
    オールクリアも判定。
    Returns: (score, new_board)
    """
    new_board = deepcopy(board)
    full_lines = []
    for r in range(const.HEIGHT):
        if all(x==1 for x in new_board[r]):
            full_lines.append(r)
    cleared = len(full_lines)
    if cleared == 0:
        return 0, new_board , 0
    
    # 消去実行
    for r in reversed(full_lines):
        del new_board[r]
    for _ in range(cleared):
        new_board.insert(0, [0]*const.WIDTH)
    
    # スコア算出
    base_score = const.LINES_SCORE.get(cleared, 0)
    # オールクリア判定
    if all(all(cell==0 for cell in row) for row in new_board):
        # 全消しなら ALL_CLEAR_SCORE を適用
        base_score = const.ALL_CLEAR_SCORE.get(cleared, 0)

    return base_score, new_board, cleared
