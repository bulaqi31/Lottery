# main.py
from ui import LotteryUI
from lottery_logic import Lottery

def main():
    # 创建抽奖逻辑对象
    lottery = Lottery()
    
    # 创建并启动Tkinter界面
    app = LotteryUI(lottery)
    app.run()

if __name__ == '__main__':
    main()

