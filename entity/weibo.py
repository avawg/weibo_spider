class Weibo:
    def __init__(self):
        self.id = ""
        self.uid = ""
        
        self.text = ""
        
        self.created_at = ""
        self.source = ""
        
        self.reposts_count = 0  # 转发数
        self.comments_count = 0  # 评论数
        self.attitudes_count = 0  # 点赞数
        
        self.original = True
        self.pics = []
        self.stream_url = ""  # 视频地址
        
        self.reposts_pics = []
        self.reposts_stream_url = ""
    
    def __str__(self):
        """
        微博
        """
        result = ""
        result += u"内容: %s\n" % self.text
        result += u"发布时间: %s\n" % self.created_at
        result += u"发布工具: %s\n" % self.source
        result += u"点赞数: %s\n" % self.attitudes_count
        result += u"转发数: %s\n" % self.reposts_count
        result += u"评论数: %s\n" % self.comments_count
        result += u"pics: %s\n" % self.pics
        result += u"stream_url: %s\n" % self.stream_url
        result += u"reposts_pics: %s\n" % self.reposts_pics
        result += u"reposts_stream_url: %s\n" % self.reposts_stream_url
        return result
