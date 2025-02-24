import random
import const
import main   # ここで main.py の run_one_game() を呼び出す想定

# ---------------------------
# GA(遺伝的アルゴリズム)のパラメータ
# ---------------------------
POP_SIZE = 20               # 集団(個体)数
NUM_GENERATIONS = 6        # 世代数
ELITE_SIZE = 4              # エリート選択で残す個体数
MUTATE_RATE = 0.3           # 突然変異率(突然変異を起こす確率)
MUTATE_SCALE_INITIAL = 3.0  # 初期の変異幅(大きめ)
MUTATE_SCALE_MIN = 0.2      # 最終的に近づけたい最小変異幅(小さめ)

def random_individual():
    """
    個体 = [WEIGHTAGG, WEIGHTHOLES, WEIGHTBUMP, WEIGHTQUAD, WEIGHTLINES,
            WEIGHTSINGLE, WEIGHTDOUBLE, WEIGHTTRIPLE, WEIGHTILIMIT, WEIGHTTETRIS]
    の10次元ベクトルにする。
    
    例: 初期値を多少ランダムにしているが、実際には試行錯誤しながら調整可能。
    """
    return [
        random.uniform(-2, 2),  # WEIGHTAGG
        random.uniform(-2, 2),  # WEIGHTHOLES
        random.uniform(-2, 2),  # WEIGHTBUMP
        random.uniform(0,  5),  # WEIGHTQUAD
        random.uniform(0,  5),  # WEIGHTLINES 
        random.uniform(2,  10),  # WEIGHTSINGLE
        random.uniform(2,  10),  # WEIGHTDOUBLE
        random.uniform(0,  7),  # WEIGHTTRIPLE
        random.uniform(0,  2),  # WEIGHTILIMIT
        random.uniform(0,  10),  # WEIGHTTETRIS
    ]


def set_individual_to_const(ind):
    """
    個体(リスト)の値を const.py に反映させる
    """
    const.WEIGHTAGG    = ind[0]
    const.WEIGHTHOLES  = ind[1]
    const.WEIGHTBUMP   = ind[2]
    const.WEIGHTQUAD   = ind[3]
    const.WEIGHTLINES  = ind[4]

    const.WEIGHTSINGLE = ind[5]
    const.WEIGHTDOUBLE = ind[6]
    const.WEIGHTTRIPLE = ind[7]
    const.WEIGHTILIMIT = ind[8]
    const.WEIGHTTETRIS = ind[9]

def evaluate_fitness(ind):
    """
    1個体の重みでテトリスをプレイし、最終スコアを返す。
    """
    # 重みを反映
    set_individual_to_const(ind)

    # ---- 自動プレイを実行 ----
    # main.py の run_one_game() を呼び出して、最終スコアを取得
    final_score = main.run_one_game("mino.txt",1)
    return final_score

def crossover(ind1, ind2):
    """
    2個体 ind1, ind2 を交叉して子個体を1つ作る (ここでは単純にランダム比率)
    """
    child = []
    for i in range(len(ind1)):
        alpha = random.random()
        gene = alpha*ind1[i] + (1-alpha)*ind2[i]
        child.append(gene)
    return child

def mutate(ind, mutate_scale):
    """
    突然変異 (アダプティブ変異幅)
    """
    new_ind = []
    for gene in ind:
        if random.random() < MUTATE_RATE:
            mutation = random.uniform(-mutate_scale, mutate_scale)
            gene += mutation
        new_ind.append(gene)
    return new_ind

def get_mutate_scale(gen):
    """
    世代が進むほど変異幅を小さくする例
      - gen=0            -> MUTATE_SCALE_INITIAL
      - gen=NUM_GENERATIONS -> MUTATE_SCALE_MIN
    """
    ratio = gen / float(NUM_GENERATIONS)
    scale = (1 - ratio) * MUTATE_SCALE_INITIAL + ratio * MUTATE_SCALE_MIN
    return scale

def main_ga():
    # 初期集団
    population = [random_individual() for _ in range(POP_SIZE)]

    for gen in range(NUM_GENERATIONS):
        print(f"[Generation {gen}/{NUM_GENERATIONS}]")
        mutate_scale_current = get_mutate_scale(gen)

        # (個体, スコア) のペアを作成
        scored_population = []
        for ind in population:
            score = evaluate_fitness(ind)
            scored_population.append((ind, score))

        # スコアでソート (降順)
        scored_population.sort(key=lambda x: x[1], reverse=True)

        # エリート (上位 ELITE_SIZE)
        elites = scored_population[:ELITE_SIZE]
        best_ind, best_score = elites[0]
        print(f"  Best Score: {best_score:.1f}, Ind={best_ind}")

        # 次世代を作成
        new_population = [elem[0] for elem in elites]  # エリートをコピー
        while len(new_population) < POP_SIZE:
            # 親を上位10以内などから選ぶ (ルーレット選択などでもOK)
            parent1 = random.choice(scored_population[:10])[0]
            parent2 = random.choice(scored_population[:10])[0]

            child = crossover(parent1, parent2)
            child = mutate(child, mutate_scale_current)
            new_population.append(child)

        # 世代交代
        population = new_population

    print("Training Finished!")

if __name__ == "__main__":
    main_ga()
