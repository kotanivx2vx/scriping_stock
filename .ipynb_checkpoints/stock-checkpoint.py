import pandas as pd
import lxml.html
import re
import os
import json

path = "."
files=os.listdir(path)
file = open("address.json","r")
info = json.load(file)
URL = info["URL"]

def stockdata():
    url = URL
    dfs = pd.read_html(url)
    df = dfs[0]

    #add column
    df["銘柄"] = 0
    df["終値"] = 0
    df["前日比金額"] = 0

    #chage column name
    df = df.loc[:, ['順位', '銘柄','名称・コード・市場','終値',  '取引値', '前日比金額','前日比', '出来高']]
    df.columns =['rank', 'name', 'code', 'value', 'time', 'change', '%change', 'volume']

    #datastrf
    df['name'] = [re.search(r'\D+', datum).group() for datum in df['code'].tolist()]
    df['code'] = [re.search(r'\d+', datum).group() for datum in df['code'].tolist()]
    df['value'] = [datum[:-5].replace(",","") for datum in df['time'].tolist()]
    df['time'] = [datum[-5:] for datum in df['time'].tolist()]
    df["change"] = [datum[:-6].replace("+","").replace(",","") for datum in df["%change"].tolist()]
    df["%change"] = [datum[-6:].replace("+","").replace("%","") for datum in df["%change"].tolist()]
    df['volume'] = [datum[:-1].replace(",","").replace("---","0") for datum in df['volume'].tolist()]
    df = df.astype({
        'rank':int,
        'code':int,
        'value':float,
        'change':float,
        '%change':float,
        'volume':int  
    })
    df.to_csv("stockdata.csv",index = False,encoding="shift jis")
    
if __name__ == "__main__":
    stockdata()