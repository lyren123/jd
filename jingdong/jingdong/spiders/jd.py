# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
import re
from ..items import JingdongItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=737,794,798']

    def parse(self, response):
        # 对首页进行分组
        li_list = response.xpath("//ul[@class='gl-warp clearfix']/li")
        # 下一页url地址
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        # 详情页和下一页的url地址与response域名不一样,无法用urljoin进行拼接
        next_url = "https://list.jd.com"+next_url
        for li in li_list:
            item = JingdongItem()
            item["href"] = li.xpath("./div/div[3]/a/@href").extract_first()
            detail_url = "https:"+str(item["href"])
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"item": item})

        # print(next_url)

        # 当前页请求完毕后进行翻页 请求下一页

        yield scrapy.Request(next_url, callback=self.parse)

    # 处理详情页
    def parse_detail(self, response):
        item = response.meta["item"]
        item["brand"] = response.xpath("//ul[@id='parameter-brand']/li//text()").extract()
        item["desc"] = response.xpath("//ul[@id='parameter-brand']/following-sibling::ul//text()").extract()
        num = re.findall(r"/(\d+).", response.url)[0]
        # 分析网页请求，寻找出价格的js
        price_url = "https://c.3.cn/recommend?callback=handleComboCallback&methods=accessories&p=103003&sku=" + num + "&cat=737%2C794%2C798&lid=1&uuid=1524592686&pin=&ck=pin%2CipLocation%2Catw%2Caview&lim=5&cuuid=1524592686&csid=122270672.8.1524592686%7C12.1557971903"

        yield scrapy.Request(url=price_url, callback=self.parse_price, meta={"item": item},
                             dont_filter=True)  # 关闭url地址过滤,否则不会请求js对应的url

    # 根据ajx请求的url地址拿价格

    def parse_price(self, response):
        item = response.meta["item"]
        data = response.body.decode("gbk")
        item["price"] = re.findall(r"wMaprice\":(\d+)", data)
        # print(item)
        yield item
