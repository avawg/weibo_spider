import os
import requests
import tqdm
import time

class Downloader:
    def __init__(self, config):
        self.config = config
        self.prefix = os.getcwd() + os.sep + 'weibo_data' + os.sep

    def download(self, user, weibo):
        # 根据user信息创建上级目录
        img_dir = self.prefix + user.screen_name + os.sep + 'img'
        video_dir = self.prefix + user.screen_name + os.sep + 'video'
        ori_img_dir = img_dir + os.sep + "原创微博图片"
        retweet_img_dir = img_dir + os.sep + "转发微博图片"
        ori_video_dir = video_dir + os.sep + "原创微博视频"
        retweet_video_dir = video_dir + os.sep + "转发微博视频"
        for directory in [ori_img_dir, retweet_img_dir, ori_video_dir, retweet_video_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # 下载微博包含的视频和图片
        print("正在下载%s的微博数据（图片和视频）" % user.screen_name)
        if self.config['pic_download']:
            for pics, dir in [(weibo.pics, ori_img_dir), (weibo.reposts_pics, retweet_img_dir)]:
                for i, pic_url in enumerate(pics):
                    file_name = weibo.created_at + '_' + weibo.id + '_' + str(i) + '.jpg'
                    print("正在下载图片", file_name)
                    self.__download_one_file(pic_url, dir + os.sep + file_name)
                    time.sleep(1)
        if self.config['video_download']:
            for stream_url, dir in [(weibo.stream_url, ori_video_dir), (weibo.reposts_stream_url, retweet_video_dir)]:
                if stream_url != "":
                    file_name = weibo.created_at + '_' + weibo.id + '.mp4'
                    print("正在下载视频", file_name)
                    self.__download_one_file(weibo.stream_url, dir + os.sep + file_name)
                    time.sleep(3)


    @staticmethod
    def __download_one_file(url, path):
        try:
            response = requests.get(url, stream=True)
            file_size = response.headers['Content-length']
            pbar = tqdm.tqdm(total=int(file_size), unit='B', unit_scale=True, desc="downloading progress")
            with(open(path, 'wb')) as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(1024)
            pbar.close()
            print()
        except:
            pass
