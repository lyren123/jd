import requests
import json
import re
from pymongo import MongoClient
client = MongoClient()
collections = client["jd"]["cate1"]
# 直接对京东响应分类信息的url请求,返回数据为字符串,提取其中的分类参数
# 对数据进行处理 将分类数字参数保存在mongdb数据库中
# 共计1310个小分类
url = "https://dc.3.cn/category/get"
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}

response = requests.get(url,headers=headers)
# 将返回的json数据转换为字典数据 方便处理
data = json.loads(response.content.decode("gbk"))
for i in data["data"]:
    cate = i["s"][0]["s"]
    for j in cate:
        cate2 = j["s"]
        for k in cate2:
            item ={}
            cate3 = k["n"]
            num1 = re.findall(r"(\d+,\d+,\d+)",cate3)
            num2 = re.findall(r"(\d+-\d+-\d+)",cate3)
            cate_name = re.findall(r"\|(.+)\|\|",cate3)[0]
            if len(num1):
                item["cate_name"] = cate_name
                item["cate_num"] = num1[0]
                collections.insert_one(item)
                print(item)
            if len(num2):
                num2 = ",".join(num2[0].split("-"))
                item["cate_name"] = cate_name
                item["cate_num"] = num2
                print(item)
                collections.insert_one(item)





