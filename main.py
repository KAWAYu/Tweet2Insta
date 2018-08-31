#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from io import open
from cabocha.analyzer import CaboChaAnalyzer
import MeCab
import json
import random

from emoji_lib import insertemoji

app = Flask(__name__)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=8080, type=int)
    return parser.parse_args()


# /にアクセスが来たときはindex.htmlに飛ばす
@app.route('/')
def index():
    title = "Tweet2InstagramConverter"
    return render_template('index.html', title=title)


# /postにアクセスが来た時、文字列が入っていればchunkで分けて#をつける
# そうじゃなければindex.htmlにリダイレクト（結局同じ）
@app.route('/post', methods=['GET', 'POST'])
def post():
    e_list = make_entities("data/hash_tag.counted.re")
    hashes = hashtag_count_map("data/insta_post_jap500_ent354.tags.dat", minimum_count=2)
    trans_dict = ja2en("data/top_hash.tsv")
    title = "Tweet2InstagramConverter"
    if request.method == 'POST':
        emojistring = insertemoji.insert_emoji(request.form['tweet-content'], 'data/emoji.txt')
        return render_template('instagram.html',
                hashtag=emojistring + tweet2insta(request.form['tweet-content'], e_list, hashes, trans_dict),
                title=title, message='hashtag does not exist')
    else:
        return redirect(url_for('index'))


def make_entities(filepath):
    entities_list = []
    with open(filepath, encoding='utf-8') as fin:
        for line in fin:
            entities_list.append(line.strip())
    return entities_list


def hashtag_count_map(filepath, minimum_count=5):
    hashtag_count = {}
    with open(filepath, encoding='utf-8') as fin:
        for line in fin:
            word, count = line.strip().split('\t')
            hashtag_count[word] = int(count)
    hashtags = [k for k, _ in filter(lambda x: x[1] >= minimum_count, hashtag_count.items())]
    return hashtags


def ja2en(filepath):
    ja2en_dict = {}
    with open(filepath, encoding='utf-8') as fin:
        for line in fin:
            word_en, word_ja = line.strip().split('\t')
            if word_ja in ja2en_dict:
                ja2en_dict[word_ja].append(word_en)
            else:
                ja2en_dict[word_ja] = [word_en]
    return ja2en_dict


def tweet2insta(content, entities, hashtags, translate):
    # TODO: 文節区切りでハッシュタグをつける
    # フィルタリング：固有名詞は残す、有名人のハッシュタグが含まれていれば残す
    # とりあえずつけとけばいいハッシュタグ「写真好きとつながりたい」みたいなのをつける
    toriaezu_hash = ['#写真好きとつながりたい', '#love', '#instagood', '#happy', '#new',
                    '#photo', '#instalike', '#photooftheday', '#like4like', '#l4l']
    hashtag = []
    tree = CaboChaAnalyzer().parse(content)
    # chunkからタグ候補作成
    for chunk in tree:
        _chunk = ''
        for token in chunk.tokens:
            if token.pos not in ['助詞', '助動詞']:
                _chunk += token.genkei if token.genkei != '*' else token.surface
            else:
                break
        hashtag.append(_chunk)
    # 固有名詞っぽいもの以外抜き取り
    _hashtags1 = []
    for _hashtag in hashtag:
        if _hashtag in entities:
            _hashtags1.append(_hashtag)
    _hashtags2 = []
    for _hashtag in hashtag:
        if _hashtag in hashtags:
            _hashtags2.append(_hashtag)
    eng_tag = []
    for _h in hashtag:
        if _h in translate:
            eng_tag += translate[_h]

    hashtag = set(_hashtags1) | set(_hashtags2) | set(eng_tag)

    _toriaezu = random.sample(toriaezu_hash, k=4)

    hashtag = ['#%s' % s for s in hashtag] + _toriaezu
    return ' '.join(hashtag)


if __name__ == '__main__':
    args = parse()
    app.debug = True
    app.run(host='0.0.0.0', port=args.port)
