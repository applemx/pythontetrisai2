import random

def read_input_from_file(filename):
    """
    テキストファイルから
      1行目 : ミノの個数 N
      2行目以降 : ミノの種類( i, t, l, j, o, s, z )
    を読み込む関数。
    
    Returns:
        N   (int): ミノの個数
        mino_sequence (list[str]): ミノの種類のリスト
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    N = int(lines[0])
    mino_sequence = lines[1:]

    if N != len(mino_sequence):
        raise ValueError("ミノの個数が一致しません")
    
    return N, mino_sequence

def generate_random_mino_sequence(num_pieces=100):
    """学習用にランダムなミノシーケンスを生成"""
    mino_sequence = []
    MINO_TYPES = ['I', 'T', 'L', 'J', 'O', 'S', 'Z']
    for _ in range(num_pieces):
        mino_sequence.append(random.choice(MINO_TYPES))
    
    return mino_sequence
