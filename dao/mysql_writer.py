import copy

import pymysql
import json

from dao.writer import Writer

# 将用户信息和发布的微博写入mysql数据库中
# 数据库自己维护索引结构
class MysqlWriter(Writer):
    
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='296513', database='weibodata')
        self.conn.autocommit(True)
    
    def write_user(self, user):
        # 写用户信息
        cursor = self.conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS `%s` (
               `id` VARCHAR(20)  PRIMARY KEY,
               `uid` BIGINT(10),
               `text` VARCHAR(500),
               `created_at` VARCHAR(20),
               `source` VARCHAR(20),
               `reposts_count` VARCHAR(20),
               `comments_count` VARCHAR(20),
               `attitudes_count` VARCHAR(20),
               `original` TINYINT(10),
               `pics` JSON,
               `stream_url` VARCHAR(500),
               `reposts_pics` JSON,
               `reposts_stream_url` VARCHAR(500))
            """ % user.screen_name
        cursor.execute(sql)
        print("正在写入%s的信息:" % user.screen_name)
        print(user)
        item = user.__dict__
        item['fans'] = json.dumps(item['fans'])
        item['follows'] = json.dumps(item['follows'])
        keys = ', '.join(['`{}`'.format(key) for key in item.keys()])
        values = ', '.join(['%s'] * len(item))
        update = ', '.join(['{0:}=VALUES({0:})'.format('`{}`'.format(key)) for key in item.keys()])
        sql = 'INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE '.format('user', keys, values) + update
        cursor.execute(sql, tuple(item.values()))
    
    def write_weibo(self, user, weibo):
        cursor = self.conn.cursor()
        print("正在写入%s的微博:" % user.screen_name)
        print(weibo)
        item = copy.deepcopy(weibo).__dict__
        item['pics'] = json.dumps(item['pics'])
        item['reposts_pics'] = json.dumps(item['reposts_pics'])
        keys = ', '.join(['`{}`'.format(key) for key in item.keys()])
        values = ', '.join(['%s'] * len(item))
        update = ', '.join(['{0:}=VALUES({0:})'.format('`{}`'.format(key)) for key in item.keys()])
        sql = 'INSERT INTO `{}` ({}) VALUES ({}) ON DUPLICATE KEY UPDATE '.format(user.screen_name, keys, values) + update
        cursor.execute(sql, tuple(item.values()))
