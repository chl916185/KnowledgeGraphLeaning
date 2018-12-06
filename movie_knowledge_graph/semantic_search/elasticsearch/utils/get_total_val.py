#!/usr/bin/env python
# coding=utf-8
"""
# 获取属性值和属性间的映射

通过对数据库进行查表得到各个实体的属性和属性值，而后将其存储为./data/total_val.txt 文件在搜索时使用。

获取所有实体
我们直接通过Mysql的的操作得到所有实体的倒出并存储为一个文件，名为./data/all_entity.tx
"""

import pymysql    
from pymysql import connections
from collections import defaultdict
 
class connec_mysql(object):
    def __init__(self):    
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='nlp',
            db='baidu_baike',
            charset='utf8mb4',
            use_unicode=True
            )    
        self.cursor = self.conn.cursor()

    def get_json(self):
        for cate in ["actor", "movie"]:
            cate = cate.strip()
            self.cursor.execute("SELECT MAX({}_id) FROM {}".format(cate, cate))
            result = self.cursor.fetchall()
            max_id = result[0][0] if result[0][0] != None else 0
            print("max_id: ", max_id)
            f = open(__package__ + "/../data/{}.txt".format(cate), "w+")
            for id in range(1, max_id+1):
                self.cursor.execute("SELECT * FROM {} WHERE {}_id = {}".format(cate, cate, id))
                item_lists = self.cursor.fetchall()
#                self.cursor.execute("SELECT COLUMN FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(cate))
                actor_column_attr = ["actor_id", "actor_bio", "actor_chName", "actor_foreName", "actor_nationality", "actor_constellation", "actor_birthPlace", "actor_birthDay", "actor_repWorks", "actor_achiem", "actor_brokerage"]
                movie_column_attr = [ "movie_id", "movie_bio", "movie_chName", "movie_foreName", "movie_prodTime", "movie_prodCompany", "movie_director", "movie_screenwriter", "movie_genre", "movie_star", "movie_length", "movie_rekeaseTime", "movie_language", "movie_achiem"]
                column_attr = actor_column_attr if cate == "actor" else movie_column_attr

                if item_lists == None and column_attr == None:
                    continue
                try:
                    assert len(item_lists[0]) == 14 or len(item_lists[0]) == 11
                    for i in range(1, len(item_lists[0])):
                        if item_lists[0][i] == 'None':
                            continue
                        f.write(item_lists[0][i] + " " + column_attr[i] + "\n")

                except Exception as e:
                    print(e)


if __name__ == "__main__":
    connect_sql = connec_mysql()
    connect_sql.get_json()
