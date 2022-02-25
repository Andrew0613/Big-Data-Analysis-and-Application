# Chinese Word Segmentation
## What is word segmentation?
Word segmentation (or tokenization) is the process of dividing up a sequence of characters into a sequence of words.

## Metrics
准确率(Precision)和召回率(Recall)

Precision = 正确切分出的词的数目 / 切分出的词的总数

Recall = 正确切分出的词的数目 / 应切分出的词的总数

 

综合性能指标F-measure

F $\beta$ = $ \frac{(\beta + 1)*Precision*Recall}{\beta*Precision + Recall}$

β为权重因子，如果将准确率和召回率同等看待，取β = 1，就得到最常用的F1-measure

F1 = $\frac{2*Precisiton*Recall}{Precision+Recall}$

 

未登录词召回率(R_OOV)和词典中词的召回率(R_IV)

R_OOV = 正确切分出的未登录词的数目 / 标准答案中未知词的总数

R_IV = 正确切分出的已知词的数目 / 标准答案中已知词的总数

## Datasets
1、SIGHAN Bakeoff 2005 MSRA,560KB  http://sighan.cs.uchicago.edu/bakeoff2005/

2、SIGHAN Bakeoff 2005 PKU, 510KB  http://sighan.cs.uchicago.edu/bakeoff2005/

3、SIGHAN Bakeoff 2005 CityU, 510KB  http://sighan.cs.uchicago.edu/bakeoff2005/

4、SIGHAN Bakeoff 2005 AS, 510KB  http://sighan.cs.uchicago.edu/bakeoff2005/

5、人民日报 2014, 65MB  https://pan.baidu.com/s/1hq3KKX

6、 MSRA (新闻语料)  https://pan.baidu.com/s/1twci0QVBeWXUg06dK47tiA?_at_=1645796271787


## References
https://chinesenlp.xyz/#/docs/word_segmentation

https://www.zhihu.com/question/19578687

中科院计算所NLPIR http://ictclas.nlpir.org/nlpir/ 

ansj分词器 https://github.com/NLPchina/ansj_seg

哈工大的LTP https://github.com/HIT-SCIR/ltp

清华大学THULAC https://github.com/thunlp/THULAC

斯坦福分词器 https://nlp.stanford.edu/software/segmenter.shtml

Hanlp分词器 https://github.com/hankcs/HanLP

结巴分词 https://github.com/yanyiwu/cppjieba

KCWS分词器(字嵌入+Bi-LSTM+CRF) https://github.com/koth/kcws

ZPar https://github.com/frcchang/zpar/releases

IKAnalyzer https://github.com/wks/ik-analy





# Chinese POS Tagging