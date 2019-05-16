# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


client = MongoClient()
collections = client["jd"]['cate2']

class JingdongPipeline(object):
    def process_item(self, item, spider):
        # 对抓取数据格式进行处理,保存到mongodb数据库中
        item["brand"] = "".join([i.strip() for i in item["brand"]])
        item["href"] = "http"+item["href"]
        item["price"] = item["price"][0].strip()
        item["desc"] = "".join([i.strip() for i in item["desc"]])
        item = dict(item)
        collections.insert_one(item)
        # 控制台打印爬取数据,方便观察爬取状态
        print(item)
        return item
