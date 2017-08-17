#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 10:32
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : part3.py
# @Software: PyCharm


from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os
import re
from multiprocessing.dummy import Pool
import base64
import time
import random

try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract



ip_available_list = []

proxy_list = ['222.93.19.112:8118', '182.90.83.72:8123', '182.88.44.236:8123', '27.43.143.202:80', '110.73.3.134:8123', '115.46.151.100:8123', '218.15.25.153:808', '183.33.243.96:808', '221.7.175.127:8123', '114.115.200.211:80', '114.115.200.211:80', '110.72.31.244:8123', '112.193.68.175:808', '183.63.126.227:63000', '27.43.166.94:80', '218.241.131.249:80', '113.123.19.190:808', '182.90.78.94:80', '120.27.5.62:9090', '112.114.98.62:8118', '59.61.72.202:8080', '115.151.7.82:808', '58.255.183.148:80', '115.215.69.224:808', '120.83.97.209:808', '183.153.25.58:808', '113.121.254.102:808', '113.106.94.213:80', '120.76.114.50:80', '113.123.127.115:808', '222.95.19.1:808', '123.57.184.70:8081', '183.63.223.2:63000', '111.76.225.101:808', '183.153.32.174:808', '218.64.92.15:808', '222.195.76.103:80', '222.85.50.226:808', '222.242.171.5:63000', '115.213.203.46:808', '113.123.18.205:808', '114.230.31.54:808', '61.178.238.122:63000', '115.202.177.53:808', '222.95.22.248:808', '114.239.150.231:808', '118.178.227.171:80', '58.253.70.149:8080', '110.73.35.180:8123', '122.112.253.67:80']


'''
user_agents 随机头信息
'''
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}


def IPspider(numpage):

    url = 'http://www.xicidaili.com/nn/'

    with open(r"data/ip_port2.txt","a",encoding="utf8") as fp:

        for num in range(1, numpage + 1):
            ipurl = url + str(num)

            try:
                web_data = requests.get(ipurl, headers=headers, timeout=5, proxies=get_random_proxy_ip())
                soup = BeautifulSoup(web_data.text,"lxml")
                ip_list = soup.select("tr > td:nth-of-type(2)")
                port_list = soup.select("tr > td:nth-of-type(3)")

                print("numpage = %d , len(ip_list) = %d , len(port_list) = %d" % (num,len(ip_list),len(port_list)))

                for _ip,_port in zip(ip_list,port_list):
                    fp.write(_ip.text.strip() + ":" + _port.text.strip() + "\n")
            except:
                continue



def get_random_proxy_ip():
    proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    proxy = {'http': proxy_ip}
    # proxies = {'http': 'http://122.72.33.138:80'}
    return proxy


def get_proxy_ip(proxy_ip):
    proxy = {'http': proxy_ip}
    return proxy



def get_parse_data(file_name,is_pandas=True):
    '''
    获得初级解析的数据
    :return: dataframe
    '''
    if not os.path.exists(file_name):
        return None

    if is_pandas:
        return pd.read_csv(file_name, sep="\001", encoding="utf-8", error_bad_lines=False)
    else:
        data = []
        with open(file_name, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                item = line.strip().split('\001')
                data.append(item)
        return data

def add_new_feature_title(title):
    '''
    添加新的特征列
    :param title: 原特征列
    :return: 新特征列
    '''

    len_title = len(title)

    if len_title==46:
        title.append("360_phone_user_mark_times") # index 46
        title.append("s_360_phone_user_mark_desc") # 47
        title.append("360_phone_title_times") # 48
        title.append("360_phone_content_times") # 49
        title.append("360_phone_page_times") # 50
        title.append("360_phone_pages_count") # 51
        title.append("360_phone_find_count") # 52


        title.append("360_first_tel_user_mark_times")  # 53
        title.append("s_360_first_tel_user_mark_desc")  # 54
        title.append("360_first_tel_title_times")  # 55
        title.append("360_first_tel_content_times")  # 56
        title.append("360_first_tel_page_times")  # 57
        title.append("360_first_tel_pages_count")  # 58
        title.append("360_first_tel_find_count") # 59


        title.append("360_second_tel_user_mark_times")  # 60
        title.append("s_360_second_tel_user_mark_desc")  # 61
        title.append("360_second_tel_title_times")  # 62
        title.append("360_second_tel_content_times")  # 63
        title.append("360_second_tel_page_times")  # 64
        title.append("360_second_tel_pages_count")  # 65
        title.append("360_second_tel_find_count") # 66


        title.append("360_third_tel_user_mark_times")  # 67
        title.append("s_360_third_tel_user_mark_desc")  # 68
        title.append("360_third_tel_title_times")  # 69
        title.append("360_third_tel_content_times")  # 70
        title.append("360_third_tel_page_times")  # 71
        title.append("360_third_tel_pages_count")  # 72
        title.append("360_third_tel_find_count") # 73


        return title

    elif len_title == 74:
        return title

    else:
        print("title len error!!!")
        return None



def request_360(item):
    '''
    请求360搜索引擎
    :param item:
    :return:
    '''
    try:
        phone_index_list = [4, 10, 11, 12]  # phone,first_tel,second_tel,third_tel
        _360_feature_count_per_tel = 7

        while True:
            if len(item) < 74:
                item.append("")
            else:
                break

        for item_index in phone_index_list:
            search_phone = item[item_index]
            phone_index_list_index = phone_index_list.index(item_index)

            if len(search_phone) < 5:
                item[46 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[47 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[48 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[49 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[50 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[51 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[52 + phone_index_list_index * _360_feature_count_per_tel] = ""

                continue

            url = "https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q=" + str(search_phone)
            # url = "https://www.so.com/s?q=" + str(search_phone)
            web_data = requests.get(url, headers=headers, timeout=15, proxies=get_random_proxy_ip())
            soup = BeautifulSoup(web_data.text, "lxml")

            user_mark = soup.select("p.mh-hy-tips.mh-hy > strong > img")
            if len(user_mark) > 0:
                item[46 + phone_index_list_index * _360_feature_count_per_tel] = "1"
                item[47 + phone_index_list_index * _360_feature_count_per_tel] = "1"
            else:
                item[46 + phone_index_list_index * _360_feature_count_per_tel] = ""
                item[47 + phone_index_list_index * _360_feature_count_per_tel] = ""


            result_title = soup.select("li.res-list > h3.res-title > a")
            result_title_str = "".join([item.text.strip() for item in result_title])
            search_phone_title_times = result_title_str.count(search_phone)
            print(u"标题匹配次数", search_phone_title_times)
            item[48 + phone_index_list_index * _360_feature_count_per_tel] = str(search_phone_title_times)

            result_content = soup.select("li.res-list > p.res-desc")
            result_content_str = "".join([item.text.strip() for item in result_content])
            search_phone_content_times = result_content_str.count(search_phone)
            print(u"内容头匹配次数", search_phone_content_times)
            item[49 + phone_index_list_index * _360_feature_count_per_tel] = str(search_phone_content_times)

            search_phone_all_times = search_phone_title_times + search_phone_content_times
            print(u"页面匹配次数", search_phone_all_times)
            item[50 + phone_index_list_index * _360_feature_count_per_tel] = str(search_phone_all_times)

            page_number_list = soup.select("div#page > strong + a")
            if len(page_number_list) > 0:
                page_number = page_number_list[-1].text.strip()
                print(u"页面数量", page_number)
                item[51 + phone_index_list_index * _360_feature_count_per_tel] = str(page_number)
            else:
                item[51 + phone_index_list_index * _360_feature_count_per_tel] = "1"
                print(u"页面数量", "1")

            search_phone_all_pages_times = soup.select("div#page > span.nums")
            if len(search_phone_all_pages_times) > 0:
                find_all_times = search_phone_all_pages_times[0].text.strip()

                p1 = re.compile(r'\d+')
                find_all_times_int_list = p1.findall(find_all_times)
                if len(find_all_times_int_list) > 0:
                    print(u"找到相关结果数量", find_all_times_int_list[0])
                    item[52 + phone_index_list_index * _360_feature_count_per_tel] = str(find_all_times_int_list[0])
                else:
                    item[52 + phone_index_list_index * _360_feature_count_per_tel] = "0"
            else:
                item[52 + phone_index_list_index * _360_feature_count_per_tel] = "0"

    except Exception as e:
        print("request_360", e)
    else:
        print(item)



def save_new_data(file_name, data, title=None):
    '''
    持久化新数据为csv
    :param data: 简单提取过后的new_data
    :return: 新数据集
    '''
    if title:
        data.insert(0, title)
    with open(file_name, "w", encoding="utf-8") as fp:
        for item in data:
            fp.write("\001".join(item) + "\n")



def check_ip_port(ip_port):
    '''
    检查该代理是否可用
    :param ip_port:
    :return:
    '''
    try:
        r = requests.get("http://www.baidu.com", headers=headers, timeout=2, proxies=get_proxy_ip(ip_port))
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        # print(e)
        return False

def read_proxies():
    '''
    读取爬取的代理
    :return:
    '''
    ip_port_list = []
    with open(r"data/ip_port.txt","r") as fp:
        for item in fp.readlines():
            ip_port_list.append(item.rstrip("\n"))
    return ip_port_list


def pool_check_ip(item):
    if check_ip_port(item):
        ip_available_list.append(item)
        print(item)


if __name__ == "__main__":
    # try:
    #     IPspider(500)
    # except Exception as e:
    #     print(e)


    # ip_port_list = read_proxies()
    #
    # pool = Pool(processes=20)
    # pool.map(pool_check_ip, ip_port_list)
    # pool.close()
    # pool.join()
    #
    # print(ip_available_list)
    #
    # with open(r"data/ip_available.txt","w") as fp:
    #     fp.write(",".join(ip_available_list))
    #
    # print("finish")




    # j = 0
    # for i in range(1000):
    #     r = requests.get("https://www.sogou.com/web?ie=utf8&query=" + str(13790341394))
    #     print(r.text)
    #     j += 1
    #     print(j , "=========================================================")




    # data = get_parse_data(r"input/data2_title.csv",is_pandas=False)

    # if not data:
    #     print("$$$$$$$$$$$$$$$$$$__data is None")
    #
    # data_title = data[0]
    #
    # new_data_title = add_new_feature_title(data_title)
    #
    # if not new_data_title:
    #     print("$$$$$$$$$$$$$$$$$$__new_data_title is None")
    # else:
    #     print(new_data_title)
    #     print(len(new_data_title))
    #
    # data_1 = data[1:]
    #
    # pool = Pool(processes=5)
    # pool.map(request_360, data_1)
    # pool.close()
    # pool.join()

    # save_new_data(r"input/data_baidu_360.csv", data_1, title=new_data_title)

    data = pd.read_csv(r"input/data_baidu_phone_qq.csv", sep=",", encoding="utf-8", error_bad_lines=False)
    del data["user_id"]
    data.to_csv(r"input/data_baidu_phone_qq4.csv", index=False)





