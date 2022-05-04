import time

from entity.user import User
from parser.util import request_json
from urllib.parse import quote

class UserParser:
    # 根据输入的微博用户名获取id
    def get_uid(self, uname):
        # 中文url encode
        url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D" + quote(uname) + "%26t%3D0&page_type=searchall"
        status_code, data = request_json(url)
        if status_code != 1:
            print("未找到输入的用户")
            return
        card = data["cards"][1]["card_group"][0]  # 返回第一个用户
        return card["user"]["id"]
    
    def parse_user(self, uid):
        print("正在爬取用户(uid=%s)的资料:" % uid)
        info_url = "https://m.weibo.cn/api/container/getIndex"
        "https://m.weibo.cn/api/container/getIndex?uid=1223178222&luicode=10000011&type=uid&value=1223178222&containerid=1005051223178222"
        params = {
            "uid": uid,
            "luicode": "10000011",
            "type": "uid",
            "value": uid,
            "containerid": "100505" + str(uid)
        }
        status_code, data = request_json(info_url, params=params)
        user = User()
        attrs_list = ["id", "screen_name", "gender", "description", "verified_reason",
                      "statuses_count", "follow_count", "followers_count"]
        for attr, value in data["userInfo"].items():  # 将userInfo dict提取 转化为User类
            if attr in attrs_list:
                setattr(user, attr, value)
        setattr(user, "fans", self.__parse_fans(user))
        setattr(user, "follows", self.__parse_followers(user))
        print("爬取到用户信息:" + str(user))
        return user
    
    @staticmethod
    def __parse_fans(user):
        fans = []
        fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_%s&since_id=%s"
        since_id = 1
        print("正在爬取%s的粉丝列表" % user.screen_name)
        while since_id <= 10:  # 只爬取前25页粉丝
            status_code, data = request_json(fans_url % (user.id, str(since_id)))
            if status_code == 0:
                break
            for card in data['cards'][0]['card_group']:
                fans.append(card['user']['id'])
            since_id += 1
            if since_id % 10 == 0:
                time.sleep(1)
        print("爬取%s的粉丝列表完毕" % user.screen_name)
        return fans
    
    @staticmethod
    def __parse_followers(user):
        followers = []
        followers_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_%s&page=%s"
        page = 1
        print("正在爬取%s关注人列表" % user.screen_name)
        while True:
            ok, data = request_json(followers_url % (user.id, str(page)))
            if ok == 0:
                print("爬取%s关注人列表完毕" % user.screen_name)
                break
            for card in data['cards'][-1]['card_group']:
                followers.append(card['user']['id'])
                # if card['user']['id'] not in followers:
                #     followers.append(card['user']['id'])
            page += 1
            if page % 10 == 0:
                time.sleep(1)
        return followers
