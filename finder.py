import board_logic
import evaluate
import const
from copy import deepcopy

def beam_search_solve(initial_board, mino_sequence):
    # 初期状態
    initial_state = (deepcopy(initial_board), 0, [])
    beam = [initial_state]
    max_depth = min(const.DEPTH_LIMIT, len(mino_sequence))
    
    for d in range(max_depth):
        piece = mino_sequence[d]
        new_beam = []
        for state in beam:
            board, cum_score, moves = state
            mino_idx = const.MINO_TYPE_TO_INDEX[piece]
            base_mino = const.MINOS[mino_idx]
            # 試す回転は 0～3
            for rotation in [0, 1, 2, 3]:
                rotated = board_logic.rotate_mino(base_mino, rotation)
                mino_width = len(rotated[0])
                # x の範囲は 0～(WIDTH - mino_width)
                for x in range(const.WIDTH - mino_width + 1):
                    # まず、現在の盤面の上部に配置可能かチェック (衝突しないか)
                    if not board_logic.can_place_mino(board, rotated, 0, x):
                        continue
                    # 盤面のコピーを作り、ミノを落下させる
                    temp_board = deepcopy(board)
                    board_logic.drop_mino(temp_board, rotated, x)
                    # ライン消去＆スコア更新
                    line_score, after_board , cleared = board_logic.clear_lines_and_get_score(temp_board)
                    # 盤面評価
                    eval_value = evaluate.evaluate_board(after_board,cleared,mino_sequence[d:])
                    # 合計スコア: これまでのスコア + 消去スコア + 評価値
                    new_score = cum_score + line_score + eval_value
                    new_moves = moves + [(piece, x, rotation)]
                    new_state = (after_board, new_score, new_moves)
                    new_beam.append(new_state)
        # ビーム幅で上位を選択 (scoreが高いほど良い)
        new_beam.sort(key=lambda s: s[1], reverse=True)
        beam = new_beam[:const.BEAM_WIDTH]
        # もしビームが空なら探索打ち切り
        if not beam:
            break
    # ビーム内で最もスコアが高い状態を選ぶ
    best_state = max(beam, key=lambda s: s[1]) if beam else initial_state
    return best_state
