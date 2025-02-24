import curses

import game_loop
import const
import input
import board_logic
import draw

import evaluate
import finder


def run_one_game(filename="mino.txt",mode=0):
    """
    1) mino.txt などからミノのシーケンスを読み込み
    2) 空盤面を作成
    3) 次の depth_limit 手を先読みしながら、ビームサーチで最適手を探す
    4) 各手を盤面に反映し、ライン消去スコアを加算
    5) 全ミノ分終わったら最終スコアを返す
    """
    # 入力読み込み(0=>通常1=>学習(ランダム))
    if mode == 0:
        N, mino_seq = input.read_input_from_file(filename)
    else:
        N = 100
        mino_seq = input.generate_random_mino_sequence(100)

    print(f"Loaded {N} minos: {mino_seq}")
    board = board_logic.create_empty_board()
    total_score = 0

    index = 0
    while index < len(mino_seq):
        # 次の depth_limit 分だけ先読み
        subseq = mino_seq[index : index + const.DEPTH_LIMIT]

        # ビームサーチで最適手を探索
        final_board, cum_score, move_sequence = finder.beam_search_solve(board, subseq)
        
        if not move_sequence:
            # これ以上配置できない(ビームが生成されず)場合は中断
            # その時点の total_score を返して終了
            # 実際にはゲームオーバー的な扱い
            break

        # 見つかった最適手(最初の1手)を適用
        piece, best_x, best_rot = move_sequence[0]  # (mino_type, x, rotation)

        # ミノを配置
        mino_idx = const.MINO_TYPE_TO_INDEX[piece]
        rotated_mino = board_logic.rotate_mino(const.MINOS[mino_idx], best_rot)
        board_logic.drop_mino(board, rotated_mino, best_x)

        # ライン消去
        line_score, board, _ = board_logic.clear_lines_and_get_score(board)
        total_score += line_score

        # デバッグ用に評価値を見たい場合
        eval_score = evaluate.evaluate_board(board, mino_seq[index:])
        print(f"Placed {piece} at x={best_x}, rot={best_rot}, line_score={line_score}, eval_score={eval_score}")

        # 盤面を出力
        draw.draw_board(board)
        print("----")

        # 次のミノへ
        index += 1

    return total_score


def main():
    """
    通常のエントリポイント:
    run_one_game を呼び出し、スコアを表示する
    """

    final_score = run_one_game("mino.txt",0)
    print(f"Final Score = {final_score}")



if __name__ == "__main__":
    main()
