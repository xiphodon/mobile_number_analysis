#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/17 13:49
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : part1.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os
import re
from multiprocessing.dummy import Pool

title_0 = ['id', 'user_id', 'apply_date', 'overdue_days', 'name', 'sex', 'phone', 'idcard', 'province', 'city',
           'address',
           'qq', 'wechat', 'alipay', 'channel', 'degree', 'source', 'contact_name', 'contact_relation', 'contact_tel',
           'second_name', 'second_relation', 'second_tel', 'third_name', 'third_relation', 'third_tel']

title_1 = ['s_id', 's_user_id', 'overdue', 's_name', 's_phone', 's_idcard', 's_address', 's_qq', 's_wechat', 's_alipay',
           's_contact_tel', 's_second_tel', 's_third_tel', 's_qq_first', 'qq_len', 'wechat_is_phone', 'alipay_is_phone',
           'wechat_is_email', 'alipay_is_email', 'has_first_tel', 'has_second_tel', 'has_third_tel',
           'baidu_phone_user_mark_times', 's_baidu_phone_user_mark_desc', 'baidu_phone_title_times',
           'baidu_phone_content_times', 'baidu_phone_page_times', 'baidu_phone_pages_count',
           'baidu_first_tel_user_mark_times', 's_baidu_first_tel_user_mark_desc', 'baidu_first_tel_title_times',
           'baidu_first_tel_content_times', 'baidu_first_tel_page_times', 'baidu_first_tel_pages_count',
           'baidu_second_tel_user_mark_times', 's_baidu_second_tel_user_mark_desc', 'baidu_second_tel_title_times',
           'baidu_second_tel_content_times', 'baidu_second_tel_page_times', 'baidu_second_tel_pages_count',
           'baidu_third_tel_user_mark_times', 's_baidu_third_tel_user_mark_desc', 'baidu_third_tel_title_times',
           'baidu_third_tel_content_times', 'baidu_third_tel_page_times', 'baidu_third_tel_pages_count']

search_engine = {'baidu': '', '360': ''}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Connection': 'keep-alive'
}


def read_origin_data():
    '''
    从文件中读取原始数据
    :return: 数据集
    '''
    data = []
    with open(r"input/label_file.txt", "r", encoding="utf-8") as fp:
        _data = fp.readlines()
        for line in _data:
            line = line.strip().split("\001")
            if len(line) != 26:
                print("read_origin_data", "len(line) != 26")
                continue
            else:
                data.append(line)
    return data


def parse_data(data):
    '''
    格式化数据，筛选需要的列，生成标签列
    :return: 新数据集
    '''
    new_data = []
    for item in data:
        new_item = []

        new_item.append(item[0])  # id
        new_item.append(item[1])  # user_id
        new_item.append("0" if int(item[3]) <= 10 else ("1" if int(item[3]) >= 30 else "2"))  # overdue
        new_item.append(item[4])  # name
        new_item.append(item[6])  # phone
        new_item.append(item[7])  # idcard
        new_item.append(item[10])  # address
        new_item.append(item[11])  # qq
        new_item.append(item[12])  # wechat
        new_item.append(item[13])  # alipay
        new_item.append(item[19])  # contact_tel
        new_item.append(item[22])  # second_tel
        new_item.append(item[25])  # third_tel

        new_item.append(item[11][0] if len(item[11]) > 5 else "")  # qq_first
        new_item.append(str(len(item[11])) if len(item[11]) > 5 else "")  # qq_len
        new_item.append("1" if item[6] == item[12] else "0")  # wechat_is_phone
        new_item.append("1" if item[6] == item[13] else "0")  # alipay_is_phone
        new_item.append("1" if re.match(r"^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$", item[12]) else "0")  # wechat_is_email
        new_item.append("1" if re.match(r"^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$", item[13]) else "0")  # alipay_is_email
        new_item.append("1" if len(item[19]) > 1 else "0")  # has_first_tel
        new_item.append("1" if len(item[22]) > 1 else "0")  # has_second_tel
        new_item.append("1" if len(item[25]) > 1 else "0")  # has_third_tel

        new_data.append(new_item)
    return new_data


def save_new_data(file_name, data, is_insert_title=False):
    '''
    持久化新数据为csv
    :param data: 简单提取过后的new_data
    :return: 新数据集
    '''
    if is_insert_title:
        data.insert(0, title_1)
    with open(file_name, "w", encoding="utf-8") as fp:
        for item in data:
            fp.write("\001".join(item) + "\n")


def get_parse_data_0(is_pandas=True):
    '''
    获得初级解析的数据
    :return: dataframe
    '''
    file_name = r"input/data.csv"
    if not os.path.exists(file_name):
        data = read_origin_data()
        data = parse_data(data)
        save_new_data(file_name, data, is_insert_title=True)

    if is_pandas:
        return pd.read_csv(file_name, sep="\001", encoding="utf-8", error_bad_lines=False)
    else:
        data = []
        with open(file_name, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                item = line.strip().split('\001')
                # if len(item) != len(title_1):
                #     print("get_parse_data", "open_file", len(item), item)
                #     continue
                data.append(item)
        return data


def request_baidu(item):
    '''
    请求搜索引擎
    :param item: 数据
    :return:查询结果
    '''
    try:
        phone_index_list = [4, 10, 11, 12]  # phone,first_tel,second_tel,third_tel
        baidu_feature_count_per_tel = 6

        # for i in range(len(phone_index_list) * baidu_feature_count_per_tel):
        #     item.append("")

        while True:
            if len(item) < len(title_1):
                item.append("")
            else:
                break

        for item_index in phone_index_list:
            search_phone = item[item_index]
            phone_index_list_index = phone_index_list.index(item_index)

            if len(search_phone) < 5:
                item[22 + phone_index_list_index * baidu_feature_count_per_tel] = ""  # baidu_phone_user_mark_times
                item[23 + phone_index_list_index * baidu_feature_count_per_tel] = ""  # s_baidu_phone_user_mark_desc
                item[24 + phone_index_list_index * baidu_feature_count_per_tel] = ""  # baidu_phone_title_times
                item[25 + phone_index_list_index * baidu_feature_count_per_tel] = ""  # baidu_phone_content_times
                item[26 + phone_index_list_index * baidu_feature_count_per_tel] = ""  # baidu_phone_page_times
                item[27 + phone_index_list_index * baidu_feature_count_per_tel] = ""  # baidu_phone_pages_count

                continue

            url = "https://www.baidu.com/s?wd=" + str(search_phone)
            web_data = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(web_data.text, "lxml")

            user_mark = soup.select("div.op_fraudphone_word")
            if len(user_mark) > 0:
                user_mark_text = user_mark[0].text.strip()
                print(user_mark_text)

                p1 = re.compile(r'\d+')
                user_mark_times_list = p1.findall(user_mark_text)
                if len(user_mark_times_list) > 0:
                    user_mark_times = user_mark_times_list[0]
                    item[22 + phone_index_list_index * baidu_feature_count_per_tel] = str(user_mark_times)
                else:
                    item[22 + phone_index_list_index * baidu_feature_count_per_tel] = ""

                p2 = re.compile('"(.*)"')
                user_mark_desc_list = p2.findall(user_mark_text)
                if len(user_mark_desc_list) > 0:
                    user_mark_desc = user_mark_desc_list[0]
                    item[23 + phone_index_list_index * baidu_feature_count_per_tel] = user_mark_desc
                else:
                    item[23 + phone_index_list_index * baidu_feature_count_per_tel] = ""
            else:
                item[22 + phone_index_list_index * baidu_feature_count_per_tel] = ""
                item[23 + phone_index_list_index * baidu_feature_count_per_tel] = ""

            result_title = soup.select("h3.t > a")
            result_title_str = "".join([item.text.strip() for item in result_title])
            search_phone_title_times = result_title_str.count(search_phone)
            print(u"标题匹配次数", search_phone_title_times)
            item[24 + phone_index_list_index * baidu_feature_count_per_tel] = str(search_phone_title_times)
            # for item in result_title:
            #     print(item.text.strip())

            result_content = soup.select("div.c-abstract")
            result_content_str = "".join([item.text.strip() for item in result_content])
            search_phone_content_times = result_content_str.count(search_phone)
            print(u"内容头匹配次数", search_phone_content_times)
            item[25 + phone_index_list_index * baidu_feature_count_per_tel] = str(search_phone_content_times)
            # for item in result_content:
            #     print(item.text.strip())

            search_phone_all_times = search_phone_title_times + search_phone_content_times
            print(u"页面匹配次数", search_phone_all_times)
            item[26 + phone_index_list_index * baidu_feature_count_per_tel] = str(search_phone_all_times)

            page_number_list = soup.select("span.pc")
            if len(page_number_list) > 0:
                page_number = page_number_list[-1].text.strip()
                print(u"页面数量", page_number)
                item[27 + phone_index_list_index * baidu_feature_count_per_tel] = str(page_number)
            else:
                item[27 + phone_index_list_index * baidu_feature_count_per_tel] = "1"
                print(u"页面数量", "1")
        print(item)
        print("============当前进度：%d / %d   %.4f%%" % (
            data_2.index(item), len_data_2, 100 * data_2.index(item) / len_data_2))
    except Exception as e:
        print("request_baidu", e)


if __name__ == "__main__":
    data = get_parse_data_0(is_pandas=False)

    print(len(data))

    data_2 = []
    for item in data[1:]:
        if item[2] != "2":
            data_2.append(item)

    print(title_1)
    # print(data[1])



    len_data_2 = len(data_2)

    # item_index=0
    # for item in data_2:
    #     item_index += 1
    #     try:
    #         request_baidu(item)
    #     except Exception as e:
    #         print("request_baidu",e)
    #     print(item)
    #     print("============当前进度：%d / %d   %.4f%%" % (item_index,len_data_2,100 * item_index / len_data_2))

    pool = Pool(processes=20)
    pool.map(request_baidu, data_2)
    pool.close()
    pool.join()

    save_new_data(r"input/data2.csv", data_2)
