import time

from lxml import etree
import requests, random, csv
import pandas as pd


class request:

    # 初始化
    def __init__(self, tity):
        self.url = f"https://lishi.tianqi.com{tity}202310.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

    # 响应
    def res(self):
        req = requests.get(url=self.url, headers=self.headers)
        return req.content.decode()

    # 数据
    def data(self):
        res = self.res()
        html = etree.HTML(res)
        # 当前13天的数据
        str = html.xpath("//ul[@class='thrui']/li/div/text()")
        return str


class city:
    def __init__(self):
        self.ap = []
        self.url = "https://www.tianqi.com/chinacity.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

    def res(self):
        res = requests.get(url=self.url, headers=self.headers).content.decode()
        xp = etree.HTML(res).xpath('//div[@class="citybox"]/span[16]/a/@href')
        self.ap = etree.HTML(res).xpath('//div[@class="citybox"]/span[16]/a/text()')
        return xp if xp else None


if __name__ == '__main__':
    # 获取城市
    city_data = city()
    for a, r in enumerate(city_data.res()):
        city = city_data.ap[a]
        time.sleep(random.randint(1, 5))
        print(f"现在是城市: {city}")
        rs = request(r).data()
        print(rs)

        # 写入数据
        with open("../数据清洗练习/data.csv", "a", encoding='UTF-8', newline="") as file:
            # 创建写入器并关联到打开的文件
            writer = csv.writer(file)
            writer.writerow([city] + rs)
            print('写入成功')
