import operator


class BiDirectionMatching(object):

    def __init__(self, maxlen, dic):
        self.window_size = maxlen
        self.dic = dic
        # self.dic = ['研究', '研究生', '生命', '命', '的', '起源']
        # path = "icwb2-data/gold/pku_training_words.utf8"
        # f = open(path,"r",encoding='utf-8')
        # self.dic = f.read().splitlines() #按行读入，返回列表
        # f.close()
        # dic = {}
        # for token in self.dic:
        #     if token in dic.keys():
        #         dic[token] += 1
        #     else:
        #         dic[token] = 1
        # print(dic)
        # print(self.dic)


    def mm_tokenize(self, text):
        tokens = []            # 定义一个空列表来保存切分的结果
        index = 0              # 切分
        text_length = len(text)
        windows_size = min(self.window_size, text_length)

        while text_length > index:    # 循环结束判定条件
            for size in range(windows_size + index, index, -1):   # 根据窗口大小循环，直到找到符合的进行下一次循环
                piece = text[index: size]      # 被匹配字段
                if piece in self.dic:    # 如果需要被匹配的字段在词典中的话匹配成功，新的index为新的匹配字段的起始位置
                    index = size - 1
                    break
            index += 1
            tokens.append(piece)          # 将匹配到的字段保存起来

        return tokens

    def rmm_tokenize(self, text):
        tokens = []
        index = len(text)
        windows_size = min(self.window_size, index)

        while index > 0:
            for size in range(index - windows_size, index):
                w_piece = text[size: index]
                if w_piece in self.dic:
                    index = size + 1
                    break
            index -= 1
            tokens.append(w_piece)
        tokens.reverse()

        return tokens

    def bmm_tokenize(self, text):
        mm_tokens = self.mm_tokenize(text)
        # print('正向最大匹配分词结果:', mm_tokens)
        rmm_tokens = self.rmm_tokenize(text)
        # print('逆向最大匹配分词结果:', rmm_tokens)

        if len(mm_tokens) != len(rmm_tokens):
            if len(mm_tokens) > len(rmm_tokens):
                return rmm_tokens
            else:
                return mm_tokens
        elif len(mm_tokens) == len(rmm_tokens):
            if operator.eq(mm_tokens, rmm_tokens):
                return mm_tokens
            else:
                mm_count, rmm_count = 0, 0
                for mm_tk in mm_tokens:
                    if len(mm_tk) == 1:
                        mm_count += 1
                for rmm_tk in rmm_tokens:
                    if len(rmm_tk) == 1:
                        rmm_count += 1
                if mm_count > rmm_count:
                    return rmm_tokens
                else:
                    return mm_tokens


if __name__ == '__main__':
    print("text:")
    text = input()
    tokenizer = BiDirectionMatching()
    # tokenizer.dic += ["新老师生"]
    print("max_len:")
    tokenizer.window_size = int(input())
    print('双向最大匹配得到的结果：', tokenizer.bmm_tokenize(text))