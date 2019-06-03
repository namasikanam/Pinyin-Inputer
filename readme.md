## 使用说明

在此文件夹目录下，执行

```bash
python ./src/model.py <input file> <output file>
```

如果没有`<input file>`和`<output file>`，默认执行：
```bash
python ./src/model.py ./data/input.txt ./data/output.txt
```

## 目录说明

- `data`
  - `hanzi.pkl`: 一二级汉字集
  - `pinyin2hanzi.pkl`: 每个拼音对应的汉字表
  - `uniCharProb.pkl`: 单字出现概率$P(w_i)$
  - `biCharProb.pkl`: 相邻汉字出现的条件概率$P(w_i | w_j)$
- `src`
  - `model.py`: 模型代码