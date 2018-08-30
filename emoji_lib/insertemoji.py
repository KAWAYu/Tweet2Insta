import MeCab
import json
import sys


# for line in inputstr.split("。"):
    # s = re.sub('.*“(.*)”.*\n', r"\1", line) # コメント部分抽出
def insert_emoji(sentences, dict_path, end=' '):
    f = open(dict_path)
    dic = json.loads(f.read())
    f.close()
    m = MeCab.Tagger()

    emojistr = ''
    for line in sentences.split('。'):  # 1行ずつの処理
        tokens = m.parse(line)
        stack = []
        for l in tokens.split('\n'):  # 1形態素ずつの処理
            facestr = l.split('\t')[0]
            if facestr == "EOS":
                d = {}
                for k in stack:
                    d.update(dic[k])
                if d:
                    maxemoji = max(d.items(), key=lambda x: x[1])
                    emojistr += line + maxemoji[0]
                stack = []
            elif '名詞' in l:
                stack.append(facestr)
    return emojistr + end
# print(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    input_str = sys.stdin.readline()
    print(insert_emoji(input_str, '../data/emoji.txt', end=''))
