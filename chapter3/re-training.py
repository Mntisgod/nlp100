# jawiki-country.json.gzを解凍

import re
import gzip
import json

import requests
import urllib


class RE:
    def __init__(self):
        pass

    def extract_UK(self):
        with gzip.open('jawiki-country.json.gz', 'rt') as f:
            for line in f:
                line = json.loads(line)
                if line['title'] == 'イギリス':
                    return line['text']
        raise ValueError('no article about UK')

    # 21. カテゴリ名を含む行を抽出
    def extract_lines_contains_category(self, text):
        pattern = re.compile(r'\[\[Category:.*\]\]')
        return pattern.findall(text)

    # 22. カテゴリ名を抽出
    def extract_category(self, text):
        pattern = re.compile(r'\[\[Category:(.*?)(?:\|.*)?\]\]')
        return pattern.findall(text)

    # 23. セクション構造
    # == == で囲まれた文字列と、=の数に合わせたレベルを表示
    def extract_section_level(self, text):
        pattern = re.compile(r'=(=+)([^=]+)=\1')
        return [(len(m[1]), m[2]) for m in pattern.finditer(text)]

    # 24. ファイル参照の抽出
    def extract_files(self, text):
        pattern = re.compile(r'\[\[ファイル:(.*?)\|')
        return pattern.findall(text)

    # 25.26,27 テンプレートの抽出
    def extract_templates(self, text, is_remove_emphasis=True, is_remove_inner_link=True):
        pattern = re.compile(r'\{\{基礎情報(.*?)\n\}\}', re.DOTALL)
        basic_info = pattern.search(text).group()
        pattern = re.compile(r'\|(.*?) = (.*?)\n')
        dict = {}
        for m in pattern.finditer(basic_info):
            if is_remove_emphasis:
                dict[m[1]] = re.sub(r"''+", "", m[2])
            else:
                dict[m[1]] = m[2]
            if is_remove_inner_link:
                pass

        return dict
    
    # 29 国旗画像のURLを取得
    def extract_flag_url(self, file_name):
        params = {
            'action': 'query',
            'titles': 'File:' + file_name,
            'format': 'json',
            'prop': 'imageinfo',
            'iiprop': 'url'
        }
        url = 'https://www.mediawiki.org/w/api.php'
        response = requests.get(url, params=params).json()
        print(response['query']['pages']['-1']['imageinfo'][0]['url'])

    def main(self):
        self.extract_flag_url('Flag of the United Kingdom.svg')


if __name__ == '__main__':
    RE().main()
