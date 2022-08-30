import re


with open("2022.txt", 'r', encoding='utf-8') as f2020:
    with open("2022_.txt", 'w', encoding='utf-8') as f:
        all = f2020.readlines()
        for line in all:
            f.write(line[:-1])
