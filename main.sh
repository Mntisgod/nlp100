# poplura-names.txtを入力として受け取る
# そのファイルを読み込み、行数を数える

# ファイルのパスを受け取る
# 以下を関数にする

function count_lines() {
  # ファイルの行数を数える
  wc -l $1
}

function replace (){
    # ファイルの中身を置換する
    # tabをスペースに置換
    sed -i -e 's/\t/ /g' $1
}

# 特定の列を抽出
function extract_column() {
    # スペースで区切られたファイルの1列目を抽出
    cut -d ' ' -f 1 $1 > column1.txt
    # ファイルの2列目を抽出
    cut -d ' ' -f 2 $1 > column2.txt
}

function concat_column() {
    # 2つのファイルを連結
    paste $1 $2 > concat_column.txt
}

function show_head(){
    # ファイルの先頭n行を表示、nは引数で指定
    head -n $1 popular-names.txt
}

function show_tail(){
    # ファイルの末尾n行を表示、nは引数で指定
    tail -n $1 popular-names.txt
}

function split_file(){
    # ファイルをn行ごとに分割
    split -l $1 popular-names.txt
}

function calc_set_1(){
    # 一列目の文字列の種類を数える
    cut -d ' ' -f 1 $1 | sort | uniq > set1.txt
}

function sort_value_by_third_column(){
    sort -k 3 -n -r $1
}

# 出現頻度の高い単語を抽出
function sort_by_frequency_of_first_column(){
    cut -d ' ' -f 1 $1 | sort | uniq -c | sort -r > frequency.txt
}

sort_by_frequency_of_first_column $1

