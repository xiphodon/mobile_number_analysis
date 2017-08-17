#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/2 15:15
# @Author  : GuoChang
# @Site    : https://github.com/xiphodon
# @File    : selenium_test.py
# @Software: PyCharm

# 引入WebDriver包
from selenium import webdriver
# 引入WebDriver Keys包
from selenium.webdriver.common.keys import Keys
import time
# 创建浏览器对象
browser = webdriver.Firefox()
# browser = webdriver.Chrome()
# 导航到百度主页
browser.get('https://www.baidu.com')
time.sleep(2)
# 检查标题是否为‘百度一下，你就知道’
assert '百度一下，你就知道' in browser.title
# 找到名字为wd的元素，赋值给elem
elem = browser.find_element_by_name('wd') # 找到搜索框
elem.send_keys('selenium' + Keys.RETURN)# 搜索selenium
