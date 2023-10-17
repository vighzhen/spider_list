import time

import requests
from lxml import etree
import pandas as pd

def boos(page,brand_list):
    # 免费代理池的API地址，这里只是示例，请根据实际情况更改
    proxy_pool_url = '114.231.45.14:8888'

    proxy_dict = {
        'http': f'http://{proxy_pool_url}',
        'http': f'http://{proxy_pool_url}'
    }

    print(proxy_dict)

    # 请求头
    headers = {
        'Cookie': 'lastCity=101250100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1678149277,1678869073; wd_guid=da82346d-5b8b-4442-8bab-1217b989c595; historyState=state; __zp_seo_uuid__=ee8ce5a6-8676-4670-b381-1ce1293cdc4a; __l=r=https%3A%2F%2Fwww.bing.com%2F&l=%2Fcitysite%2Fchangsha%2F&s=1; _bl_uid=17lewnhhidgtFwnnjnj32atqbg5t; JSESSIONID=75074DE6D3D7A9E4D367C4817E7CFB38; boss_login_mode=app; wt2=DGP0bkaLEgz51fs4blmN1cyVFWKcdwNUmWDMjv2rm7i2TEeI2oOZKU2AMzEEs5exk4Rv1WI1s4fyC89IZ0A2hPw~~; wbg=0; __c=1696903534; __g=-; __a=90014644.1678149279.1681050226.1696903534.84.4.1.84; __fid=28d0583f6750ad2a3788202b5ab95e8f; __zp_stoken__=8972eYXA%2BXFAwbUpKSUw4OlxvUyYjAXFeIGtBTzENMWNpS040PF58dXBvLiQbEFc2NmNKeQ9AYzAHOGQfQUpRcHwKbXRYJBtGbh4SUHAFUF8CBEEgC3NKVEtTURgxMBgydFp4Bn0%2FSE04eT4%3D; geek_zp_token=V1RN0mFu3-01xjVtRvxhsRKC2z6jrfwiQ~',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    url = f"https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=java%E5%BC%80%E5%8F%91&city=101250100&page={page}&pageSize=30"
    # 请求
    res = requests.get(url=url, headers=headers, proxies=proxy_dict).json()
    # 数据列表
    data_list = res['zpData']['jobList']
    # print(data_list[0]['encryptJobId'])

    brand_list = {}

    for date in data_list:
        # 公司名字
        brandName = date['brandName']
        # 公司规模人数
        brandScaleName = date['brandScaleName']
        # 工作城市
        cityName = date['cityName']
        # 岗位
        jobName = date['jobName']
        # 薪资
        salaryDesc = date['salaryDesc']
        # 招聘信息首页地址由以下三个组成
        # encryptJobId = date['encryptJobId']
        # lid = date['lid']
        # date['securityId']

        # 请求携带参数
        a = f"{date['lid']}&securityId={date['securityId']}"

        # 招聘信息首页地址
        date_url = f"https://www.zhipin.com/job_detail/{date['encryptJobId']}.html?{a}"

        # 招聘详细信息地址
        zpDate = f"https://www.zhipin.com/wapi/zpgeek/job/card.json?{a}"

        list = {'brandName': brandName,
                'brandScaleName': brandScaleName,
                'date_url': date_url, 'zpDate': zpDate}
        brand_list[f"{brandName}"] = list

    #  获取每一条详细信息
    for i in brand_list.values():
        print('开始第二阶段')
        # 详细信息接口地址
        url = i["zpDate"]

        jobCard = requests.get(url=url, headers=headers).json()['zpData']["jobCard"]
        # print(jobCard)
        # 招聘岗位
        i['jobName']=jobCard['jobName']
        # 岗位要求
        i['postDescription'] = jobCard['postDescription']
        # 学历要求
        i['degreeName'] = jobCard['degreeName']
        # 工作城市
        i['cityName'] = jobCard['cityName']
        # 工作地点
        i['address'] = jobCard["address"]
        # 工作薪资
        i['salaryDesc'] = jobCard['salaryDesc']
        # 工作要求
        i['experienceName'] = jobCard['experienceName']
        # 招聘人岗位和姓名
        i['boss_title_name']=jobCard['bossTitle']+jobCard['bossName']
        # 招聘人活跃状态
        i['activeTimeDesc'] = jobCard['activeTimeDesc']

    print(brand_list)
    return brand_list




i =1
brand_list =[]
while i<=4:
    print(f'第{i}次爬取开始')
    brand_list.append(boos(i, brand_list))
    print(f'第{i}次爬取成功休息3秒')
    time.sleep(5)
    i+=1

for b in brand_list:
    # 将数据写到文件内
    df = pd.DataFrame(b).T
    df.to_csv("data.csv",mode='a')
    print("数据写入成功")