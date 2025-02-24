import const 
import board_logic
import draw

def custom_tetris(piece_sequence_input):
    board = board_logic.create_empty_board()

    # サンプルでは、ミノを順番に: L, T, O, S, Z,... と出す(任意で変更)
    # もしくは好きな回数繰り返す、あるいはランダムにしても良い
    piece_sequence = piece_sequence_input
    seq_index = 0

    while True:
        if seq_index >= len(piece_sequence):
            print("All given pieces used. End.")
            break

        mino_type = piece_sequence[seq_index]
        seq_index += 1

        # スポーン
        rotation = 0
        x = const.MINOS_DEFAULT_X  # 真ん中あたりに出現
        y = 0
        mino_data = const.MINOS[const.MINO_TYPE_TO_INDEX[mino_type]]

        # もし最初から衝突ならゲームオーバー
        if not board_logic.can_place_mino(board, board_logic.rotate_mino(mino_data, rotation), y, x):
            print("Game Over! Cannot spawn piece.")
            break

        # --- 回転フェーズ ---
        while True:
            # 描画用
            temp_board = copy_board(board)
            place_temp(temp_board, board_logic.rotate_mino(mino_data, rotation), y, x)
            print_board(temp_board, f"Piece: {mino_type}  (Rotation Phase)")

            cmd = input("[Rotation Phase] (r=rotate, f=finish): ")

            if cmd == 'r':
                # 回転
                new_rot = (rotation + 1) % 4
                rotated_mino = board_logic.rotate_mino(mino_data, new_rot)
                if board_logic.can_place_mino(board, rotated_mino, y, x):
                    rotation = new_rot
            elif cmd == 'f':
                # 回転フェーズ終了
                break
            else:
                print("Unknown command. Use 'r' or 'f'.")

        # --- 移動フェーズ ---
        while True:
            temp_board = copy_board(board)
            place_temp(temp_board, board_logic.rotate_mino(mino_data, rotation), y, x)
            print_board(temp_board, f"Piece: {mino_type}  (Move Phase)")

            cmd = input("[Move Phase] (a=left, d=right, f=finish): ")

            if cmd == 'a':
                # 左移動
                if board_logic.can_place_mino(board, board_logic.rotate_mino(mino_data, rotation), y, x-1):
                    x -= 1
            elif cmd == 'd':
                # 右移動
                if board_logic.can_place_mino(board, board_logic.rotate_mino(mino_data, rotation), y, x+1):
                    x += 1
            elif cmd == 'f':
                # 移動フェーズ終了
                break
            else:
                print("Unknown command. Use 'a','d','f'.")

        # --- ハードドロップ ---
        # 衝突する直前までyを落とす
        # ここではユーザの操作なしで即座に落とす想定
        # もしユーザが "s" を押したタイミングで落としたいなら、別フェーズでループすればOK
        final_y = drop_to_bottom(board, board_logic.rotate_mino(mino_data, rotation), y, x)
        place_final(board, board_logic.rotate_mino(mino_data, rotation), final_y, x)

        # ライン消去
        score, new_board = board_logic.clear_lines_and_get_score(board)
        board = new_board
        if score > 0:
            print(f"Scored {score} points!")

    print("Game end. Final board:")
    print_board(board, "Final")

def copy_board(board):
    return [row[:] for row in board]

def print_board(board, title=""):
    if title:
        print(f"=== {title} ===")
    draw.draw_board(board)

def place_temp(temp_board, mino_2d, top, left):
    for r in range(len(mino_2d)):
        for c in range(len(mino_2d[r])):
            if mino_2d[r][c] == 1:
                temp_board[top + r][left + c] = 1

def place_final(board, mino_2d, top, left):
    for r in range(len(mino_2d)):
        for c in range(len(mino_2d[r])):
            if mino_2d[r][c] == 1:
                board[top + r][left + c] = 1

def drop_to_bottom(board, mino_2d, start_row, col):
    """
    衝突しない限り下げ続け、最終的に衝突する直前のrowを返す(ハードドロップ)
    """
    row = start_row
    while board_logic.can_place_mino(board, mino_2d, row+1, col):
        row += 1
    return row


if __name__ == "__main__":
    custom_tetris()
