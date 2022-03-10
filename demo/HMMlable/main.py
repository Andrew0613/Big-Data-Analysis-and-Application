from lable import *


l = Lable()
l.train()
text = "研究生研究生命的起源"
ans = l.do_lable(text)
print(ans)
# ans_jieba = do_label_jieba(text)
# print(ans_jieba)