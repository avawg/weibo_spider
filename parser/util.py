import requests
from datetime import datetime

def request_json(url, **args):
    """
    ajax从服务器请求json数据
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    response = requests.get(url, headers=headers, **args).json()
    # 返回状态码和数据
    return response['ok'], response['data']


def format_time(text):
    """
        格式化时间
        "Sat May 29 10:07:53 +0800 2021"
        ---> "2021-05-29 10:07:53"
        ---> "20210529"
    """
    GMT_FORMAT = "%a %b %d %H:%M:%S +0800 %Y"
    time = datetime.strptime(text, GMT_FORMAT)
    time = ''.join(str(time).split(' ')[0].split('-'))
    return time
