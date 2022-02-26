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

6、 MSRA (新闻语料)  <https://pan.baidu.com/s/1twci0QVBeWXUg06dK47tiA?_at_=1645796271787>

7、CTB8 <https://link.zhihu.com/?target=https%3A//pan.baidu.com/s/1DCjDOxB0HD2NmP9w1jm8MA>

8、weibo <https://link.zhihu.com/?target=https%3A//pan.baidu.com/s/1QHoK2ahpZnNmX6X7Y9iCgQ>

<https://github.com/InsaneLife/ChineseNLPCorpus/tree/master/NER> 也有汇总

## Benchmark

|Model|AS|CITYU|MSRA|PKU|
|----|----|----|----|----|
|[Ke et al. (2021)](https://aclanthology.org/2021.naacl-main.436/)| 97.0	|98.2|98.5|96.9|
|[Qiu, Pei, Yan, Huang (2020)](https://aclanthology.org/2020.findings-emnlp.260/)| 	96.4	|96.9	|98.1	|96.4|
|[Tian, Song, Xia, Zhang, Wang (2020)](https://aclanthology.org/2020.acl-main.734/)| 	96.6|	97.9|	98.4|	96.5|
|[Meng et al. (2019)](https://arxiv.org/abs/1901.10125)| 	96.7*|	97.9*|	98.3|	96.7|
|[Huang et al. (2019)](https://arxiv.org/abs/1903.04190)| 	96.6|	97.6|	97.9|	96.6|
|[Ma et al. (2018)](https://aclanthology.org/D18-1529/)| 	96.2|	97.2|	97.4|	96.1|
|[Yang et al. (2017)](https://aclanthology.org/P17-1078/)| 	95.7|	96.9|	97.5|	96.3|
|[Zhou et al. (2017)](https://www.aclweb.org/anthology/D17-1079) |	|	|	97.8|	96.0|

* Unlike others, [Meng et al. (2019)](https://arxiv.org/abs/1901.10125)  do not report converting traditional Chinese to simplified Chinese.

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

[Pre-training with Meta Learning for Chinese Word Segmentation](https://aclanthology.org/2021.naacl-main.436) (Ke et al., NAACL 2021)

[A Concise Model for Multi-Criteria Chinese Word Segmentation with Transformer Encoder](https://aclanthology.org/2020.findings-emnlp.260) (Qiu et al., Findings 2020) Code: <https://paperswithcode.com/paper/?acl=2020.findings-emnlp.260>

[Improving Chinese Word Segmentation with Wordhood Memory Networks](https://aclanthology.org/2020.acl-main.734) (Tian et al., ACL 2020) Code: <https://paperswithcode.com/paper/improving-chinese-word-segmentation-with>



Yuxian Meng, Wei Wu, Fei Wang, Xiaoya Li, Ping Nie, Fan Yin, Muyu Li, Qinghong Han, Xiaofei Sun, Jiwei Li: “Glyce: Glyph-vectors for Chinese Character Representations”, 2019; <a href='http://arxiv.org/abs/1901.10125'>arXiv:1901.10125</a>.

Weipeng Huang, Xingyi Cheng, Kunlong Chen, Taifeng Wang, Wei Chu: “Toward Fast and Accurate Neural Chinese Word Segmentation with Multi-Criteria Learning”, 2019; <a href='http://arxiv.org/abs/1903.04190'>arXiv:1903.04190</a>.

[State-of-the-art Chinese Word Segmentation with Bi-LSTMs](https://aclanthology.org/D18-1529) (Ma et al., EMNLP 2018)

[Neural Word Segmentation with Rich Pretraining](https://aclanthology.org/P17-1078) (Yang et al., ACL 2017) Code: <https://paperswithcode.com/paper/?acl=P17-1078>


[Word-Context Character Embeddings for Chinese Word Segmentation](https://aclanthology.org/D17-1079) (Zhou et al., EMNLP 2017)





# Chinese POS Tagging