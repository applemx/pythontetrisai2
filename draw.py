# draw.py

def draw_board(board):
    """
    テトリスの盤面(board)をASCIIで描画する。
    boardは [row=0 .. row=19] (上から下) の2次元リストを想定。
    ただし、人間が見るときは最上段が一番上に表示されるように、
    row=0 を上にして順番に描画するか、逆順にするか選ぶ。
    
    下記は「row=0 を上にしてそのまま描画」するバージョン。
    """

    height = len(board)
    width = len(board[0]) if height > 0 else 0

    # ヘッダー行 (列インデックス)を表示したいなら
    # print("   " + "".join(f"{c%10}" for c in range(width)))
    
    for r in range(height):
        row_str = ""
        for c in range(width):
            if board[r][c] == 1:
                row_str += "#"
            else:
                row_str += "."
        print(row_str)
