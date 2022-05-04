class User:
    def __init__(self):
        self.id = ""
        self.screen_name = ""
        
        self.gender = ""
        self.description = ""
        self.verified_reason = ""
        
        self.statuses_count = ""  # 微博数
        self.follow_count = ""
        self.followers_count = ""
        self.fans = []
        self.follows = []
    
    def __str__(self) -> str:
        """
        微博用户信息
        """
        result = ""
        result += u"昵称: %s\n" % self.screen_name
        result += u"id: %s\n" % self.id
        result += u"性别: %s\n" % ("男" if self.gender == "m" else "女")
        result += u"简介: %s\n" % self.description
        result += u"微博认证: %s\n" % self.verified_reason
        result += u"微博数: %s\n" % self.statuses_count
        result += u"关注数: %s\n" % self.follow_count
        result += u"粉丝数: %s\n" % self.followers_count
        return result
