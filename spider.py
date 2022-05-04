from dao.mysql_writer import MysqlWriter
from dao.downloader import Downloader
from parser.weibo_parser import WeiboParser
from parser.user_parser import UserParser

class Spider:
    def __init__(self, config):
        self.config = config
        self.user_parser = UserParser()
        self.weibo_parser = WeiboParser(config)
        self.writer = MysqlWriter()
        # self.writer = JsonWriter()
        self.downloader = Downloader(config)
    
    def run(self, uid):
        # 爬取并保存用户info
        user = self.user_parser.parse_user(uid)
        self.writer.write_user(user)
        # 爬取并保存用户微博信息
        for weibos in self.weibo_parser.parse_weibos(user):
            for weibo in weibos:
                self.writer.write_weibo(user, weibo)
                # 下载图片和视频
                self.downloader.download(user, weibo)


if __name__ == "__main__":
    config = {
        'since_date': '20220301',
        'end_date': '20220502',
        'pic_download': True,
        'video_download': True
    }
    spider = Spider(config)
    user_name = input("请输入要爬取的用户名：")
    uid = spider.user_parser.get_uid(user_name)
    print(uid)
    spider.run(uid)
