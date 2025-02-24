import const

def evaluate_board(board,cleared_lines=0):
    """
    テトリスの盤面を拡張評価し、浮動小数点のスコアを返す。
    高いほど「良い盤面」とみなす。
    """
    agg = aggregate_height(board)
    holes = count_holes(board)
    bump = bumpiness(board)
    lines = cleard_lines_eval(board,cleared_lines)
    

    # Perfect Clear ボーナス (pc_evaluate.py の関数を利用)
    #pc_bonus = perfect_clear_bonus(board, bonus=500)


    score = - const.WEIGHTAGG * agg - const.WEIGHTHOLES * holes - const.WEIGHTBUMP * bump + lines * const.WEIGHTLINES
    return score 

def cleard_lines_eval(board,cleared_lines):
    # ライン消去に対するボーナス／ペナルティ
    line_clear_bonus = 0
    if cleared_lines  == 1:
        line_clear_bonus += const.SINGLE
    elif cleared_lines == 2:
        line_clear_bonus += const.DOUBLE
    elif cleared_lines == 3:
        line_clear_bonus += const.TRIPLE
    elif cleared_lines == 4:
        line_clear_bonus += const.TETRIS  # Tetrisの場合ボーナス

    return line_clear_bonus

def aggregate_height(board):
    """
    各列の高さの合計を計算する。
    各列は、上(行0)から下に向かって最初にブロックが現れる位置から
    HEIGHTまでの距離とする。
    
    Args:
        board (list[list[int]]): 盤面
    
    Returns:
        int: 各列の高さの合計
    """
    width = const.WIDTH
    height = const.HEIGHT
    total = 0
    for c in range(width):
        col_height = 0
        for r in range(height):
            if board[r][c] == 1:
                col_height = height - r
                break
        total += col_height
    return total

def count_holes(board):
    """
    盤面の各列について、一度ブロックが現れた後の空セルの数を穴として数える。
    
    Args:
        board (list[list[int]]): 盤面
    
    Returns:
        int: 穴の総数
    """
    width = const.WIDTH
    height = const.HEIGHT
    holes = 0
    for c in range(width):
        block_found = False
        for r in range(height):
            if board[r][c] == 1:
                block_found = True
            else:
                if block_found:
                    holes += 1
    return holes

def bumpiness(board):
    """
    隣接する列間の高さの差の合計を計算する。
    
    Args:
        board (list[list[int]]): 盤面
    
    Returns:
        int: bumpiness の合計
    """
    width = const.WIDTH
    height = const.HEIGHT
    col_heights = [0] * width
    for c in range(width):
        for r in range(height):
            if board[r][c] == 1:
                col_heights[c] = height - r
                break
    bump = 0
    for i in range(width - 1):
        bump += abs(col_heights[i] - col_heights[i+1])
    return bump
