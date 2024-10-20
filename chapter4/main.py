import collections
import MeCab
import matplotlib.pyplot as plt
import japanize_matplotlib


def main():
    with open('neko.txt', 'r') as f:
        text = f.read()
        # MeCabのインスタンスを作成
        mecab = MeCab.Tagger()
        # 形態素解析を実行
        result = mecab.parse(text)
        # 結果をneko.txt.mecabに保存
        with open('neko.txt.mecab', 'w') as f:
            f.write(result)


def read_mecab():
    with open('neko.txt.mecab', 'r') as f:
        lines = f.readlines()
        list = []
        for line in lines:
            dic = {}
            surface = line.split('\t')
            if surface[0] == 'EOS\n':
                continue
            dic['surface'] = surface[0]
            # surfaceのlengthがそれぞれ異なるため、条件分岐
            if len(surface) == 1:
                continue
            base = surface[3]
            dic['base'] = base
            if len(surface[4].split('-')) == 1:
                pos = surface[4]
                dic['pos'] = pos
                dic['pos1'] = ''
                list.append(dic)
                continue
            pos = surface[4].split('-')[0]
            pos1 = surface[4].split('-')[1]
            dic['pos'] = pos
            dic['pos1'] = pos1
            list.append(dic)
        return list


def extract_verbs_surface(map: list):
    verb_surface_list = []
    for dict in map:
        if dict["pos"] == "動詞":
            verb_surface_list.append(dict["surface"])
    print(verb_surface_list)


def extract_verbs_base(map: list):
    verb_base_list = []
    for dict in map:
        if dict["pos"] == "動詞":
            verb_base_list.append(dict["base"])
    print(verb_base_list)


def extract_nouns_clause_a_of_b(map: list):
    nouns_clause_a_of_b = []
    for i, dict in enumerate(map):
        if dict["surface"] == "の" and map[i - 1]["pos"] == "名詞" and map[i + 1]["pos"] == "名詞":
            nouns_clause_a_of_b.append(map[i - 1]["surface"] + dict["surface"] + map[i + 1]["surface"])
    print(nouns_clause_a_of_b)


def extract_consecutive_nouns(map: list):
    consecutive_nouns_list = []
    tmp = ""
    count = 0
    for i, dict in enumerate(map):
        if tmp == "" and dict["pos"] == "名詞":
            tmp = dict["surface"]
            count = 1
        if dict["pos"] == "名詞" and map[i + 1]["pos"] == "名詞":
            tmp += map[i + 1]["surface"]
            count += 1
        else:
            if tmp != "" and count > 1:
                consecutive_nouns_list.append(tmp)
                tmp = ""
    print(consecutive_nouns_list)


def sort_word_frequency(map: list):
    word_frequency = {}
    for dict in map:
        if dict["surface"] in word_frequency:
            word_frequency[dict["surface"]] += 1
        else:
            word_frequency[dict["surface"]] = 1
    word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    with open('word_frequency.txt', 'w') as f:
        for word, frequency in word_frequency:
            f.write(f'{word}: {frequency}\n')
    
    for i in range(10):
        print(word_frequency[i])
        # 棒グラフ描画ライブラリを使ってグラフを描画
        plt.bar(word_frequency[i][0], word_frequency[i][1])
    plt.show()


def sort_co_occurred_frequency(map: list):
    co_occurred_frequency = {}
    for i, dict in enumerate(map):
        if dict["surface"] == "猫":
            if map[i - 1]["surface"] in co_occurred_frequency and i - 1 >= 0:
                co_occurred_frequency[map[i - 1]["surface"]] += 1
            elif i - 1 >= 0:
                co_occurred_frequency[map[i - 1]["surface"]] = 1
            if map[i + 1]["surface"] in co_occurred_frequency and i + 1 < len(map):
                co_occurred_frequency[map[i + 1]["surface"]] += 1
            elif i + 1 < len(map):
                co_occurred_frequency[map[i + 1]["surface"]] = 1

    co_occurred_frequency = sorted(co_occurred_frequency.items(), key=lambda x: x[1], reverse=True)
    with open('co_occurred_frequency.txt', 'w') as f:
        for word, frequency in co_occurred_frequency:
            f.write(f'{word}: {frequency}\n')

    for i in range(10):
        # 棒グラフ描画ライブラリを使ってグラフを描画
        # todo: 助詞、助動詞、記号を除外する
        plt.bar(co_occurred_frequency[i][0], co_occurred_frequency[i][1])
    plt.show()


def plot_word_frequency():
    with open('word_frequency.txt', 'r') as f:
        lines = f.readlines()
        word = []
        frequency = []
        for line in lines:
            word.append(line.split(': ')[0])
            frequency.append(int(line.split(': ')[1]))
        # 横軸を単語、縦軸を出現頻度とした棒グラフを描画
        plt.hist(frequency, range=(1,100))
        plt.xlabel('出現頻度')
        plt.ylabel('単語の種類数')
        # yを対数軸に設定
        plt.yscale('log')
        plt.show()


# 単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
def plot_word_frequency_log(map: list):

    word_list = []
    for dict in map:
        word_list.append(dict["surface"])
    data39 = collections.Counter(word_list)
    temp2 = sorted((data39.values()), reverse=True)
    plt.plot(temp2)
    plt.xlabel('出現頻度順位')
    plt.ylabel('出現頻度')
    ax = plt.gca()
    ax.set_yscale('log')  # メイン: y軸をlogスケールで描く
    ax.set_xscale('log')
    plt.show()


if __name__ == '__main__':
    # main()
    map = read_mecab()
    plot_word_frequency_log(map)