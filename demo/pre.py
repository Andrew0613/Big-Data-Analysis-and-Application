import jieba


with open("./2020.txt", 'r', encoding='utf-8') as file:
    tmp = file.readlines()
    with open("data/renmin_data/2020.txt",'w',encoding='utf-8') as f:
        for line in tmp:
            res = " ".join(jieba.lcut(line))
            f.write(res)

with open("./2021.txt", 'r', encoding='utf-8') as file:
    tmp = file.readlines()
    with open("data/renmin_data/2021.txt",'w',encoding='utf-8') as f:
        for line in tmp:
            res = " ".join(jieba.lcut(line))
            f.write(res)
with open("./2022.txt", 'r', encoding='utf-8') as file:
    tmp = file.readlines()
    with open("data/renmin_data/2022.txt",'w',encoding='utf-8') as f:
        for line in tmp:
            res = " ".join(jieba.lcut(line))
            f.write(res)

