from parser.util import request_json, format_time
from entity.weibo import Weibo
from pyquery import PyQuery

class WeiboParser:
    def __init__(self, config):
        self.since_date = config['since_date']
        self.end_date = config['end_date']
    
    def parse_weibos(self, user):
        continuing = True
        print("正在爬取%s的微博:" % user.screen_name)
        base_url = "https://m.weibo.cn/api/container/getIndex"
        params = {
            'uid': user.id,
            'luicode': '10000011',
            'type': 'uid',
            'value': user.id,
            'containerid': '107603' + str(user.id),
            'page': 1
        }
        while continuing:
            status_code, data = request_json(base_url, params=params)
            if status_code == 0:  # status_code == 0, 说明爬取到最后一页微博
                break
            yield self.__parse_one_page(data['cards'], [continuing])  # 爬取一页后立即保存，避免内存中有过多的用户信息
            params['page'] += 1
    
    def __parse_one_page(self, cards, continuing):
        # 解析cards列表
        weibos = []
        for card in cards:
            if card['card_type'] != 9:  # 9 代表微博
                continue
            mblog = card['mblog']
            cur_date = format_time(mblog['created_at'])
            if cur_date > self.end_date:
                continue
            if cur_date < self.since_date:
                continuing[0] = False
                break
            
            weibo = Weibo()
            attrs_list = ['id', 'source', 'reposts_count', 'comments_count', 'attitudes_count']
            try:
                for attr, value in mblog.items():  # 将mblog dict提取，转换为Weibo类
                    if attr in attrs_list:
                        setattr(weibo, attr, value)
                    elif attr == 'created_at':
                        setattr(weibo, 'created_at', format_time(value))
                        # 格式化时间
                    elif attr == 'text':
                        setattr(weibo, 'text', PyQuery(value).text())
                        # 用PyQuery去除text的标签，只保留文本
                    elif attr == 'user':
                        setattr(weibo, 'uid', value['id'])
                    elif attr == 'pics':
                        for pic in value:
                            weibo.pics.append(pic['large']['url'])
                    elif attr == 'page_info':  # 存在视频属性
                        if value['type'] == 'video':
                            setattr(weibo, 'stream_url', value['urls']['mp4_720p_mp4'])
                    elif attr == 'retweeted_status':  # 转发微博
                        setattr(weibo, 'original', False)
                        if 'pics' in value:  # 存在图片
                            for pic in value['pics']:
                                weibo.reposts_pics.append(pic['large']['url'])
                        if 'page_info' in value:  # 存在视频
                            if value['page_info']['type'] == 'video':
                                setattr(weibo, 'reposts_stream_url', value['page_info']['urls']['mp4_720p_mp4'])
            except:
                continue
            weibos.append(weibo)
        return weibos
