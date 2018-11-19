# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import pymysql

from datas import cut_word


def get_data_from_sql():
    """
    获取数据
    [(['word1','word2'],label),(['word1','word2','word3'],label)]
    """
    mysql_cn = pymysql.connect(host='10.250.40.99', port=3306, user='root', password='88888888', database='zjy_test')
    sql = "SELECT content,sort FROM language_filterdata where sort!=0 and sort!=3"
    cursor = mysql_cn.cursor()
    cursor.execute(sql)
    alldata = cursor.fetchall()
    cursor.close()
    mysql_cn.close()
    return handle_datas(alldata)


def get_data_self():
    mysql_cn = pymysql.connect(host='192.168.42.112', port=3306, user='unimonitor', password='unimonitor', database='g37')
    sql = "SELECT subject,comment_count FROM weibo where source like 'taptap%' and comment_count!=0 and length(subject)<200 limit 50"
    cursor = mysql_cn.cursor()
    cursor.execute(sql)
    alldata = cursor.fetchall()
    cursor.close()
    mysql_cn.close()
    return handle_datas(alldata)


def handle_datas(datas):
    """处理好数据并分词"""
    r = '{机器型号:[\s\S]*?}|回复：[\s\S]*'
    data_list = []
    for data in datas:
        if int(data[1]) > 3:
            label = 1
        else:
            label = 0
        data_list.append((cut_word.CutWord(re.sub(r, '', data[0]), 'zh').cut(), label))
    return data_list


if __name__ == '__main__':
    datas = get_data_from_sql()
    for data in datas:
        print(data[0], data[1])
