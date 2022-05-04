from abc import ABC, abstractmethod

# 基类
class Writer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def write_user(self, user):
        pass

    @abstractmethod
    def write_weibo(self, user, weibo):
        pass
