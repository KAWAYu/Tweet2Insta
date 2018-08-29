import MeCab
import re
import emoji
import json

# from cabocha.analyzer import CaboChaAnalyzer

with open("insta_post_jap500_ent354.tsv") as f:
    emojis = ""
    data = {}
    m = MeCab.Tagger(" -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

    for line in f:
        s = re.sub('.*“(.*)”.*\n', r"\1", line) # コメント部分抽出

        mecab = m.parse(s)
        stack = []
        for l in mecab.split("\n"):
            emojistr = l.split("\t")[0]
            if(emojistr in emoji.UNICODE_EMOJI):
                for k in stack:
                    if k in data:
                        if emojistr in data[k]:
                            data[k][emojistr] += 1
                        else:
                            data[k] = {emojistr: 1}
                    else:
                        data[k] = {emojistr: 1}
                stack = []
            elif("名詞" in l):
                stack.append(emojistr)
    print(json.dumps(data, ensure_ascii=False))

    #     rst = ''.join(c for c in s if c in emoji.UNICODE_EMOJI)
    #     emojis += rst

    # emojilist = list(set(emojis))
    # print("".join(emojilist))

