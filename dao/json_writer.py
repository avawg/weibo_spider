import os
import json

from dao.writer import Writer

"""
将用户信息和发布的微博写入json文件中，根据user信息创建上级目录
格式: .\\weibo_data\\user.screen_name\\user.id.json
例:   .\\weibo_data\\Dear-迪丽热巴\\1669879400.json
"""
#
class JsonWriter(Writer):
    
    def __init__(self):
        self.prefix = os.getcwd() + os.sep + "weibo_data" + os.sep
    
    def write_user(self, user):
        print("正在写入%s的信息:" % user.screen_name)
        dir = self.prefix + user.screen_name
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_name = dir + os.sep + str(user.id) + ".json"
        
        data = {}
        # 若之前写入过该用户数据，读取之前数据后再更新
        # 自己维护结构 耗时
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.loads(f.read())
        # 更新
        data["user"] = user.__dict__
        with open(file_name, "w") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    def write_weibo(self, user, weibo):
        print("正在写入%s的微博:" % user.screen_name)
        file_name = self.prefix + user.screen_name + os.sep + str(user.id) + ".json"
        with open(file_name, 'r') as f:
            data = json.loads(f.read())
        if "weibos" not in data:
            data["weibos"] = []
        # 之前写入的微博id列表
        set = {weibo["id"] for weibo in data["weibos"]}
        if weibo.id not in set:  # 之前写过则跳过
            data["weibos"].append(weibo.__dict__)
        with open(file_name, 'w') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
