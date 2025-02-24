import curses

import game_loop
import const
import input
import board_logic
import draw

import evaluate
import finder
import pcfinder

def main():
    """
    1) input.py でミノ順を読み込み
    2) 空盤面を作成
    3) 現在の盤面と、次の depth_limit 個のミノを対象に beam_search_solve を実行し、
       その中から最初の手 (piece, x, rotation) を取り出して盤面に反映する
    4) 盤面更新後、ライン消去とスコア加算、描画を行う
    5) これを全ミノ分繰り返し、最終スコアを表示する
    """
    # 入力読み込み
    N, mino_seq = input.read_input_from_file("mino.txt")
    board = board_logic.create_empty_board()
    total_score = 0

    # 今後のミノが残っている間ループ
    index = 0
    while index < len(mino_seq):
        # 今回は depth_limit 手先まで先読みする
        # ただし残りのミノが depth_limit 未満ならそれに合わせる
        subseq = mino_seq[index : index + const.DEPTH_LIMIT]
        
        # beam_search_solve は (final_board, cum_score, move_sequence) を返す
        final_board, cum_score, move_sequence = finder.beam_search_solve(board, subseq)
        
        if not move_sequence:
            print("探索に失敗。これ以上配置できません。")
            break

        # 最初の手を取り出す
        first_move = move_sequence[0]  # (mino_type, x, rotation)
        piece, best_x, best_rot = first_move
        
        # 実際にその手を現在の盤面に適用
        mino_idx = const.MINO_TYPE_TO_INDEX[piece]
        rotated_mino = board_logic.rotate_mino(const.MINOS[mino_idx], best_rot)
        board_logic.drop_mino(board, rotated_mino, best_x)
        
        # ライン消去＆得点計算
        line_score, board , _= board_logic.clear_lines_and_get_score(board)
        total_score += line_score

        # 実際の評価値を表示(デバッグ用)
        eval_score = evaluate.evaluate_board(board)

        # 結果を表示
        print(f"Placed {piece} at x={best_x}, rot={best_rot}, line_score={line_score} ,eval_score={eval_score}")
        draw.draw_board(board)
        print("----")
        
        # 次のミノへ進む (今回は 1 手適用したので index を1 増やす)
        index += 1

    print(f"Total Score = {total_score}")
if __name__ == "__main__":
    main()
