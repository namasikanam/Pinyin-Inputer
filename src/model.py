import pickle
import math
from IPython import embed
import sys

alpha = 0.93

with open('./data/uniCharProb.pkl', 'rb') as f:
    uniCharProb = pickle.load(f)
with open('./data/biCharProb.pkl', 'rb') as f:
    biCharProb = pickle.load(f)
with open('./data/hanzi.pkl', 'rb') as f:
    hanzi = pickle.load(f)
with open('./data/pinyin2hanzi.pkl', 'rb') as f:
    pinyin2hanzi = pickle.load(f)

if len(sys.argv) > 1:
    inputFile = sys.argv[1]
else:
    inputFile = './data/input.txt'
if len(sys.argv) > 2:
    outputFile = sys.argv[2]
else:
    outputFile = './data/output.txt'

with open(inputFile, 'r') as fin:
    with open(outputFile, 'w') as fout:
        for line in fin.readlines():
            if len(line) < 2:
                continue
            pinyins = line.replace('\n', '').split(' ')

            f = [{} for i in range(len(pinyins))]
            path = [{} for i in range(len(pinyins))]

            for c in pinyin2hanzi[pinyins[0]]:
                if (('#', '#'), (pinyins[0], c)) in biCharProb:
                    f[0][c] = math.log(
                        biCharProb[(('#', '#'), (pinyins[0], c))])
                else:
                    if ((pinyins[0], c),) in uniCharProb:
                        f[0][c] = math.log(uniCharProb[((pinyins[0], c), )])
                    else:
                        f[0][c] = -1e10  # -inf

            for i in range(1, len(pinyins)):
                for cur in pinyin2hanzi[pinyins[i]]:
                    f[i][cur] = -1e10
                    if ((pinyins[i], cur), ) in uniCharProb:
                        for last in pinyin2hanzi[pinyins[i - 1]]:
                            if ((pinyins[i-1], last), (pinyins[i], cur)) in biCharProb:
                                prob = alpha * \
                                    biCharProb[((pinyins[i-1], last), (pinyins[i], cur))] + \
                                    (1 - alpha) * \
                                    uniCharProb[((pinyins[i], cur), )]
                            else:
                                if ((pinyins[i], cur), ) in uniCharProb:
                                    prob = (1 - alpha) * \
                                        uniCharProb[((pinyins[i], cur), )]
                            prob = math.log(prob)
                            if f[i - 1][last] + prob > f[i][cur]:
                                f[i][cur] = f[i - 1][last] + prob
                                path[i][cur] = last

            c = max(f[-1], key=f[-1].get)
            ans = [c]
            for i in range(len(pinyins) - 1, 0, -1):
                try:
                    c = path[i][c]
                except:
                    embed()
                ans.append(c)

            for c in reversed(ans):
                fout.write(c)
            fout.write('\n')
