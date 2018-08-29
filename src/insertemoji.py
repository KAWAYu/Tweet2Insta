import MeCab
import json
import sys

inputstr = sys.stdin.readline()

f = open('dict.txt')
dic = json.loads(f.read())
f.close()

m = MeCab.Tagger(" -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

# for line in inputstr.split("。"):
    # s = re.sub('.*“(.*)”.*\n', r"\1", line) # コメント部分抽出

inputstr = inputstr.rstrip()
for line in inputstr.split("。"):
    mecab = m.parse(line)
    stack = []
    # print(mecab)
    for l in mecab.split("\n"):
        facestr = l.split("\t")[0]
        if(facestr == "EOS"):
            d = {}
            for k in stack:
                d.update(dic[k])
            if(len(d) > 0):
                maxemoji = max(d.items(), key=lambda x: x[1])
                print(line + maxemoji[0], end="")
            stack = []
        elif("名詞" in l):
            stack.append(facestr)
print("")
# print(json.dumps(data, ensure_ascii=False))
