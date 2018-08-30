#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import MeCab
import re
import emoji
import json


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', '-f', help='file path')

    return parser.parse_args()


def make_dictionary(file_path):
    emojis = ''
    data = {}
    m = MeCab.Tagger(" -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

    with open(file_path) as fin:
        for line in fin:
            s = re.sub('.*“(.*)”.*\n', r'\1', line)  # コメント部分の抽出
            morphs = m.parse(s)
            stack = []
            for l in morphs.split('\n'):
                emoji_str = l.split('\t')[0]
                if emoji_str in emoji.UNICODE_EMOJI:
                    for k in stack:
                        if k in data:
                            if emoji_str in data[k]:
                                data[k][emoji_str] += 1
                            else:
                                data[k] = {emoji_str: 1}
                        else:
                            data[k] = {emoji_str: 1}
                    stack = []
                elif '名詞' in l:
                    stack.append(emoji_str)
    print(json.dumps(data, ensure_ascii=False))

    #     rst = ''.join(c for c in s if c in emoji.UNICODE_EMOJI)
    #     emojis += rst

    # emojilist = list(set(emojis))
    # print("".join(emojilist))

if __name__ == '__main__':
    args = parse()
    print('Making emoji dictionary...')
    make_dictionary(args.filepath)
