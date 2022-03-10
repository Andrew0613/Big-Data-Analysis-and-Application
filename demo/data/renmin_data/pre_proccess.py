import pandas as pd

with open("观点.txt",'r',encoding='utf-8') as f:
    guandian = f.readlines()

with open("要闻.txt",'r',encoding='utf-8') as f:
    yaowen = f.readlines()

data = pd.DataFrame(columns=['Date','Title'])

for line in guandian+yaowen:
    items = line.split("/")
    for item in items[1:]:
        if len(item)!=4:
            items.remove(item)
    title, date = items[0], items[1]+items[2]
    data.loc[len(data.index)] = [date, title]

data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")
data.sort_index(ascending=True, inplace=True)
# print(data.head(100))
data.to_csv("news.csv", encoding='utf-8')