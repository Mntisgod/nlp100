# jawiki-country.json.gzを解凍

import re
import gzip
import json


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
    
    # 25. テンプレートの抽出
    def extract_templates(self, text):
        pattern = re.compile(r'\{\{基礎情報(.*?\<references\>)', re.DOTALL)
        basic_info = pattern.search(text)
        print(basic_info.group(1))
        if not basic_info:
            return {}
        pattern = re.compile(r'\|(.+?)\s*=\s*(.+?)(?=\n\||\n\}\})', re.DOTALL)
        return dict(pattern.findall(basic_info.group(1)))

    def main(self):
        text = self.extract_UK()
        dict = self.extract_templates(text)
        print(dict)


if __name__ == '__main__':
    RE().main()
