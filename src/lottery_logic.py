# lottery_logic.py
import random
from const import *

class Lottery:
    def __init__(self):
        self.participants = []
        self.remaining_participants = []

    def load_participants(self, file_path):
        # 读取参与者名单并解析
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.participants = [line.strip().split(".")[1] for line in lines if "." in line]
            # 名字出现格式为“数字.名字”，最后只输出名字
        self.remaining_participants = self.participants.copy()

    def draw(self, mode):
        if mode == WITH:
            # 放回模式
            if not self.participants:
                return None
            return random.choice(self.participants)
        elif mode == WITHOUT:
            # 不放回模式
            if not self.remaining_participants:
                return None
            winner = random.choice(self.remaining_participants)
            self.remaining_participants.remove(winner)
            return winner
        else:
            raise ValueError("未知的抽奖模式")
        
    def get_random_name(self):
        # 随机返回名单中的一个名字
        # 这个函数在滚动名单时用到
        if self.remaining_participants:
            return random.choice(self.remaining_participants)
        return None
