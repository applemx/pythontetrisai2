import const

def evaluate_board(board, cleared_lines=0, mino_sequence=[]):
    """
    テトリスの盤面を拡張評価し、浮動小数点のスコアを返す。
    高いほど「良い盤面」
    """
    agg = aggregate_height(board)
    holes = count_holes(board)
    bump = bumpiness(board)
    lines = cleard_lines_eval(board, cleared_lines)
    well_score = tetris_i_eval(board, mino_sequence)

    score = (
        - const.WEIGHTAGG * agg
        - const.WEIGHTHOLES * holes
        - const.WEIGHTBUMP * bump
        + lines * const.WEIGHTLINES
        + well_score * const.WEIGHTQUAD  #テトリス井戸の評価を加算
    )
    return score


def cleard_lines_eval(board, cleared_lines):
    """
    ライン消去に対するボーナス／ペナルティ
    """
    line_clear_bonus = 0
    if cleared_lines == 1:
        line_clear_bonus += const.SINGLE
    elif cleared_lines == 2:
        line_clear_bonus += const.DOUBLE
    elif cleared_lines == 3:
        line_clear_bonus += const.TRIPLE
    elif cleared_lines == 4:
        line_clear_bonus += const.TETRIS  # Tetrisの場合ボーナス
    return line_clear_bonus


def if_exits_i(mino_sequence):
    """
    15手以内にIミノが存在するかどうか
    存在すれば 1（True 相当）、なければ 0（False 相当）を返す
    """
    limit = 15 
    for i in range(min(limit, len(mino_sequence))):
        if mino_sequence[i] == 'I':
            return 1
    return 0


def tetris_i_eval(board, mino_sequence):
    """
    - Iミノが近々来るなら、テトリスを狙える井戸(1列だけの深い穴)があるかをチェック
    - その井戸にIミノを落としたときに最大何ライン消せそうかを判定し、スコア加算
    """
    # Iミノがしばらく来ないなら評価しない
    if not if_exits_i(mino_sequence):
        return 0

    width = const.WIDTH
    height = const.HEIGHT

    # 各列の高さを取得
    col_heights = [0]*width
    for c in range(width):
        for r in range(height):
            if board[r][c] == 1:
                col_heights[c] = height - r
                break

    # 最小高さを持つ列を探す
    min_height = min(col_heights)
    well_cols = [c for c in range(width) if col_heights[c] == min_height]

    # 「ちょうど1列」だけが最小の高さを持つ場合のみ、テトリス井戸候補とみなす
    if len(well_cols) != 1:
        return 0  # 井戸が1本でなければスコア加算しない（またはペナルティを付けてもOK）

    well_col = well_cols[0]

    # 実際に下から何ライン、他の列が埋まっていて、その井戸列(well_col)だけ空いているかを数える
    # 連続している行数をカウントする
    consecutive_lines = 0
    for row in range(height - 1, -1, -1):
        row_filled_except_well = True
        # まず、井戸列は空いている必要がある
        if board[row][well_col] == 1:
            # そこが埋まっていたら、そこで終了
            break
        # 井戸列以外がすべて埋まっているかチェック
        for c in range(width):
            if c == well_col:
                continue
            if board[row][c] == 0:
                row_filled_except_well = False
                break
        if row_filled_except_well:
            consecutive_lines += 1
        else:
            # 連続が途切れたら終了
            break

    # 最大4ラインが狙える (実際には4行より多く埋まっていても、Iミノで消せるのは最大4行)
    potential_clear = min(consecutive_lines, 4)

    # ここで、potential_clear 行のテトリスが狙えるときのボーナスを設定
    # 値は好きに調整してください（サンプル）
    # 例: 4ライン消去が期待できるなら +50, 3ラインなら +20, 2ラインなら +10, 1ラインなら +5
    well_score_table = {4: 50, 3: 20, 2: 10, 1: 5, 0: 0}
    # 下記のようにスコアを設定
    well_score = well_score_table.get(potential_clear, 0)

    return well_score


def aggregate_height(board):
    """
    各列の高さの合計を計算する。
    各列は、上(行0)から下に向かって最初にブロックが現れる位置から
    HEIGHTまでの距離とする。
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
    """
    width = const.WIDTH
    height = const.HEIGHT
    col_heights = [0]*width
    for c in range(width):
        for r in range(height):
            if board[r][c] == 1:
                col_heights[c] = height - r
                break
    bump = 0
    for i in range(width - 1):
        bump += abs(col_heights[i] - col_heights[i+1])
    return bump
