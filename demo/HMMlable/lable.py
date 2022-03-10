import jieba
import jieba.posseg as psg
from collections import defaultdict, Counter
import numpy as np
import math

from tables import Unknown
import logging

jieba.setLogLevel(logging.INFO)

class Lable():
    def __init__(self) -> None:
        self.words = []
        self.tags = []
        self.is_head = []

    def train(self):
        with open('renmin.txt', 'r', encoding='utf8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                # 用于组合词
                combine_word = ''
                combine_tag = ''
                combine_flag = False
                for i, word in enumerate(line.split()):
                    if i == 0:
                        # 去掉开头的报纸日期
                        continue
                    if i == 1:
                        self.is_head.append(1)
                    else:
                        self.is_head.append(0)
                    if word.find('[') != -1:
                        combine_word += word.split('[')[1].split('/')[0]
                        combine_flag = True
                        continue
                    elif word.rfind(']') != -1:
                        combine_word += word.split(']')[0].split('/')[0]
                        combine_tag = word.split(']')[1]
                        self.words.append(combine_word)
                        self.tags.append(combine_tag)
                        combine_word = ''
                        combine_flag = False
                        continue
                    if combine_flag:
                        combine_word += word.split('/')[0]
                        continue
                    self.words.append(word.split('/')[0])
                    self.tags.append(word.split('/')[1])
    
        self.ids_to_word = list(set(self.words))
        self.ids_to_tag = list(set(self.tags))
        self.words_len = len(self.ids_to_word)
        self.tags_len = len(self.ids_to_tag)

        self.word_to_ids = dict((w, i) for i, w in enumerate(self.ids_to_word))
        self.tag_to_ids = dict((t, i) for i, t in enumerate(self.ids_to_tag))
        self.word_to_tag = dict((w, t) for w, t in zip(self.words, self.tags))
        self.A = [[0 for j in range(self.words_len)] for i in range(self.tags_len)]
        self.B = [0 for i in range(self.tags_len)]
        self.C = [[0 for j in range(self.tags_len)] for i in range(self.tags_len)]

        # 构建A数组
        pre_word, pre_tag, pre_head = 0, 0, 0
        for word, tag, head in zip(self.words, self.tags, self.is_head):
            if head:
                self.B[self.tag_to_ids[tag]] += 1
            else:
                self.A[self.tag_to_ids[tag]][self.word_to_ids[word]] += 1
                self.C[self.tag_to_ids[pre_tag]][self.tag_to_ids[tag]] += 1
                
            pre_word, pre_tag, pre_head = word, tag, head
            
        self.A = np.array(self.A, dtype=float)
        self.B = np.array(self.B, dtype=float)
        self.C = np.array(self.C, dtype=float)

        for i in range(self.A.shape[0]):
            summ = self.A[i].sum()
            for j in range(self.A.shape[1]):
                self.A[i][j] = (self.A[i][j] + 1) / (summ + self.A.shape[1])
            
        summ = self.B.sum()
        for i in range(self.B.shape[0]):
            self.B[i] = (self.B[i] + 1) / (summ + self.B.shape[0])

        for i in range(self.C.shape[0]):
            summ = self.C[i].sum()
            for j in range(self.C.shape[1]):
                self.C[i][j] = (self.C[i][j] + 1) / (summ + self.C.shape[1])

    def pre(self, content):
        new_content = []
        unknown = {}
        # content = content.split()
        content = jieba.lcut(content)
        for i in range(len(content)):
            token = content[i]
            if token in self.words:
                new_content.append(token)
            else:
                unknown[i] = token
        return new_content, unknown, len(content)

    def do_lable(self, content):
        content, unknown, ori_len = self.pre(content)
        dp = [[0 for j in range(self.tags_len)] for i in range(len(content))]
        path = [0 for i in range(len(content))]

        res = []
        for tag in range(self.tags_len):
            dp[0][tag] = -math.log(self.A[tag][self.word_to_ids[content[0]]]) - math.log(self.B[tag])

        for i in range(1, len(content)):
            minn = float('inf')
            minn_tag = ''
            for z in range(self.tags_len):
                if dp[i-1][z] < minn:
                    minn, minn_tag = dp[i-1][z], z
            path[i-1] = minn_tag
            for j in range(self.tags_len):
                dp[i][j] = -math.log(self.A[j][self.word_to_ids[content[i]]]) - math.log(self.C[minn_tag][j]) + minn
                
        minn = float('inf')
        minn_tag = ''
        for z in range(self.tags_len):
            if dp[-1][z] < minn:
                minn, minn_tag = dp[-1][z], z
        path[-1] = minn_tag

        position = 0
        res = ""
        for i in range(ori_len):
            if i in unknown.keys():
                res += unknown[i] + '/un '
            else:
                res += content[position] + '/' + self.ids_to_tag[path[position]] + ' '
                position += 1
        
        return res

def do_label_jieba(content):
    words = psg.cut(content)
    res = ''
    for w in words:
        res = res + w.word+'/'+w.flag+' '
    return res

if __name__ == '__main__':
    l = Lable()
    l.train()
    text = "让我再打最后一把排位"
    ans = l.do_lable(text)
    print(ans)
    ans_jieba = do_label_jieba(text)
    print(ans_jieba)
    