import math
import re
import jieba
from nlpir.native import ICTCLAS
from ltp import LTP
import thulac   
from BiDirectionMatching import BiDirectionMatching
from HMM.segment.hmm import *
from tqdm import tqdm, trange
import time

class Corpus:
    def __init__(self) -> None:
        self.token_dict = {}
        self.train_path = "data/train1.utf8"
        self.pku_test_path = "data/icwb2-data/testing/pku_test.utf8"
        self.msr_test_path = "data/icwb2-data/testing/msr_test.utf8"
        self.maxlen = 0
        self.pre()
    
    def cut_sentences(self, content):
        sentences = re.split(r'(\.|\!|\?|。|！|？|\.{6})', content)
        return sentences
    
    def pre(self):
        with open(self.train_path, 'r', encoding='UTF-8') as f:
            total_tmp = f.read().split()
        with open(self.pku_test_path, 'r', encoding='UTF-8') as f:
            # [\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]
            # self.pku_test = re.split(r'(\r| |——|\n|……|：|,|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）)',f.read())
            self.pku_test = re.split(r'(\r|\t|\n|[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b])',f.read())
        with open(self.msr_test_path, 'r', encoding='UTF-8') as f:
            self.msr_test = re.split(r'(\r|\t|\n|[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b])',f.read())

        length = len(total_tmp)
        for token in total_tmp:
            if len(token) > self.maxlen:
                self.maxlen = len(token)
            if token in self.token_dict.keys():
                self.token_dict[token] += 1/length
            else:
                self.token_dict[token] = 1e-4

        for token in self.token_dict.keys():
            self.token_dict[token] = round(-math.log(self.token_dict[token]), 2)


class Segment_naive:
    def __init__(self) -> None:
        self.corpus = Corpus()
        self.bmm_tokenizer = BiDirectionMatching(self.corpus.maxlen, self.corpus.token_dict.keys())
        # self.segger = HMMSegger()
        # self.segger.load_data(self.corpus.train_path)
        # self.segger.load_data("data/icwb2-data/training/pku_training.utf8")
        # print("基于训练集训练中……")
        # self.segger.train()
        # print("done!")
        # jieba.load_userdict('data/pre1.dict')
        # self.thu1 = thulac.thulac(seg_only=True)  #默认模式
        self.ltp = LTP()

    def word_break(self, s, dic):
        def sentences(cur):
            result = []
            if cur < len(s):
                for next in range(cur+1, len(s)+1):
                    if s[cur:next] in dic:
                        result = result + [s[cur:next] + (tail and ','+tail) for tail in sentences(next)]
            else:
                return ['']
            return result
        
        list_new = []
        for line in sentences(0):
            line = line.split(",")
            list_new.append(line)
        return list_new

    def word_segment_ngram(self, input_str):
        segments = self.word_break(input_str, self.corpus.token_dict.keys())
        best_segment = []
        best_score = math.inf
        for seg in segments:
            score = 0
            for word in seg:
                if word in self.corpus.token_dict.keys():
                    score += self.corpus.token_dict[word]
                else:
                    score += round(-math.log(1e-10), 1)
            if score < best_score:
                best_score = score
                best_segment = seg
        if len(best_segment)==0:
            return [input_str]
        return best_segment

    def word_segment_bmm(self, input_str):
        return self.bmm_tokenizer.bmm_tokenize(input_str)

    def word_segment_mm(self, input_str):
        return self.bmm_tokenizer.mm_tokenize(input_str)

    def word_segment_rmm(self, input_str):
        return self.bmm_tokenizer.rmm_tokenize(input_str)
    
    def test_ngram(self, test_name):
        filename = 'result/ngram_'+test_name+'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test
        else:
            test = self.corpus.msr_test
        with open(filename,'w', encoding='utf-8') as f:
            with tqdm(total=len(test)) as pbar:
                for sentence in test:
                    # print(len(sentence))
                    if len(sentence) > 35:
                        res = self.word_segment_bmm(sentence)
                    else:
                        res = self.word_segment_ngram(sentence)
                    # res = self.word_segment_ngram(sentence)
                    w = "  ".join(str(i) for i in res) + '  '
                    # print("res",res)
                    # print("w",w)
                    f.write(w)
                    pbar.update(1)
                    # time.sleep(.1)
                    # cnt += 1
                    # print(cnt)

    def test_bmm(self, test_name):
        filename = 'result/bmm_'+test_name+'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test
        else:
            test = self.corpus.msr_test
        with open(filename,'w', encoding='utf-8') as f:
            with tqdm(total=len(test)) as pbar:
                for sentence in test:
                    res = self.word_segment_bmm(sentence)
                    w = "  ".join(str(i) for i in res) + "  "
                    f.write(w)
                    pbar.update(1)

    def test_mm(self, test_name):
        filename = 'result/mm_'+test_name+'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test
        else:
            test = self.corpus.msr_test
        with open(filename,'w', encoding='utf-8') as f:
            with tqdm(total=len(test)) as pbar:
                for sentence in test:
                    res = self.word_segment_mm(sentence)
                    w = "  ".join(str(i) for i in res) + "  "
                    f.write(w)
                    pbar.update(1)

    def test_rmm(self, test_name):
        filename = 'result/rmm_'+test_name+'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test
        else:
            test = self.corpus.msr_test
        with open(filename,'w', encoding='utf-8') as f:
            with tqdm(total=len(test)) as pbar:
                for sentence in test:
                    res = self.word_segment_rmm(sentence)
                    w = "  ".join(str(i) for i in res) + "  "
                    f.write(w)
                    pbar.update(1)

    def test_HMM(self, test_name):
        filename = 'result/HMM_'+ test_name +'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test
        else:
            test = self.corpus.msr_test
        segger = self.segger
        
        with open(filename,'w', encoding='utf-8') as f:
            with tqdm(total=len(test)) as pbar:
                for sentence in test:
                    res = segger.cut(sentence)
                    w = "  ".join(str(i) for i in res) + "  "
                    # print("res",res)
                    # print("w",w)
                    f.write(w)
                    pbar.update(1)

    def test_DAG(self, test_name):
        filename = 'result/DAG_'+ test_name +'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test_path
        else:
            test = self.corpus.msr_test_path

        with open(filename,'w', encoding='utf-8') as f:
            with open(test, 'r', encoding='utf-8') as f1:
                lines = f1.readlines()
                for line in lines:
                    res = jieba.cut(line)
                    w = "  ".join(str(i) for i in res)
                    f.write(w)

    def test_nlpir(self, test_name):
        filename = 'result/NLPIR_'+ test_name +'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test_path
        else:
            test = self.corpus.msr_test_path

        ictclas = ICTCLAS()
        with open(filename,'w', encoding='utf-8') as f:
            with open(test, 'r', encoding='utf-8') as f1:
                lines = f1.readlines()
                for line in lines:
                    res = ictclas.paragraph_process(line, 0).split()
                    w = "  ".join(str(i) for i in res) + "\n"
                    f.write(w)

    def test_thulac(self, test_name):
        filename = 'result/THULAC_'+ test_name +'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test_path
        else:
            test = self.corpus.msr_test_path

        thu1 = self.thu1
        with open(filename,'w', encoding='utf-8') as f:
            with open(test, 'r', encoding='utf-8') as f1:
                lines = f1.readlines()
                for line in lines:
                    res = thu1.cut(line, text=True).split()
                    w = "  ".join(str(i) for i in res) + "\n"
                    f.write(w)

    def test_ltp(self, test_name):
        filename = 'result/LTP_'+ test_name +'_result.txt'
        if test_name == 'pku':
            test = self.corpus.pku_test_path
        else:
            test = self.corpus.msr_test_path

        with open(filename,'w', encoding='utf-8') as f:
            with open(test, 'r', encoding='utf-8') as f1:
                lines = f1.readlines()
                # for line in lines:
                res = self.ltp.seg(lines)
                for line in res[0]:
                    w = "  ".join(str(i) for i in line) + "\n"
                    f.write(w)

    def seg_HMM(self, sentence):
        segger = self.segger
        
        res = segger.cut(sentence)
        w = " ".join(str(i) for i in res)

        return res

# c = Segment_naive()
# print("text:")
# res = c.seg_HMM(input())
# print("HMM分词结果：", res)
# # print(c.word_segment_naive("共同创造美好的新世纪——二○○一年新年贺词"))
c = Segment_naive()
begin = time.time()
# c.test_HMM("pku")
# c.test_mm("msr")
# c.test_rmm("msr")
# c.test_bmm("msr")
# c.test_DAG("pku")
# c.test_ltp("pku")
c.test_thulac("pku")
# c.test_nlpir("pku")
# c.test_ngram("msr")
end = time.time()
print("use:",end-begin)
