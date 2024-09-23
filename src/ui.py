# ui.py
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk  # 用于处理其他格式的图片，如JPEG
from const import *
from lottery_logic import Lottery

class LotteryUI:
    def __init__(self, lottery_logic):
        self.root = tk.Tk()
        self.root.configure(bg = BG)
        self.root.title("BULAQI's Lottery")
        self.root.geometry("800x600")
        
        self.roll_job = None               # 这个变量用来后续取消屏幕滚动
        self.lottery_logic = lottery_logic

        current_dir = os.path.dirname(__file__)  # 获取当前文件所在目录(src)
        assets_dir = os.path.join(current_dir, "../assets")  # 指定assets文件夹路径

        # 其中两个按钮以图片形式呈现
        #raw = Image.open(os.path.join(assets_dir, "with_replacement.png"))
        #refine = raw.resize((100,100))
        #self.with_replace = ImageTk.PhotoImage(refine)

        #raw = Image.open(os.path.join(assets_dir, "without_replacement.png"))
        #refine = raw.resize((100,100))
        #self.without_replace = ImageTk.PhotoImage(refine)

        raw = Image.open(os.path.join(assets_dir, "button.png"))
        refine = raw.resize((120,90))
        self.button = ImageTk.PhotoImage(refine)


        # 导入文件按钮
        self.import_button = tk.Button(self.root, text="Import Names", command=self.import_list,width=20,height=1,font=(FONT_E,20))
        self.import_button.pack(pady=PADY)

        # 放回与不放回模式选择
        self.mode_var = tk.StringVar(value=WITH)
        mode_frame = tk.Frame(self.root,bg=BG)
        mode_frame.pack(pady=0)
        
        #self.with_replacement_rb = tk.Radiobutton(mode_frame, image=self.with_replace, variable=self.mode_var, value="with_replacement",bg=BG)
        #self.with_replacement_rb.pack(side=tk.LEFT, padx=PADX)
        
        # 设置一个类似ON OFF的模式开关
        self.mode_button = tk.Button(self.root,text=self.mode_var.get(),command=self.toggle_mode,width=20,height=1,font=(FONT_E,20))
        self.mode_button.pack(pady=PADY)

        #self.without_replacement_rb = tk.Radiobutton(mode_frame, image=self.without_replace, variable=self.mode_var, value="without_replacement",bg=BG)
        #self.without_replacement_rb.pack(side=tk.LEFT, padx=PADX)

        # 抽奖按钮
        self.draw_button = tk.Button(self.root, image=self.button, command=self.draw_winner,bg=BG)
        self.draw_button.pack(pady=PADY)

        # 显示获奖者的标签
        self.winner_label = tk.Label(self.root, text="", font=(FONT_C, 96), fg="black",bg=BG)
        self.winner_label.pack(pady=PADY*2)

    def import_list(self):
        # 打开文件对话框，让用户选择文件
        file_path = filedialog.askopenfilename(
            title="选择抽奖名单文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.lottery_logic.load_participants(file_path)
                self.winner_label.config(text="Ready")
            except Exception as e:
                messagebox.showerror("导入失败", f"导入抽奖名单时出错:\n{e}")

    def toggle_mode(self):
        # 一个按钮进行模式切换
        if self.mode_var.get() == WITH:
            self.mode_var.set(WITHOUT)
        else:
            self.mode_var.set(WITH)
        self.mode_button.config(text=self.mode_var.get())

    def draw_winner(self):
        # 先来一段滚动名单的效果
        wait = self.roll_names()
        # 两秒后显示真正的抽奖者
        self.root.after(wait,self.display_winner)

    def roll_names(self):
        # 滚动名单 需要调用lottery_logic
        random_name = self.lottery_logic.get_random_name()
        if random_name:
            self.winner_label.config(text=random_name)
            self.roll_job = self.root.after(ROLL_TIME,self.roll_names)
            return 2000 #停两秒
        return 0

    def display_winner(self):
        mode = self.mode_var.get()
        winner = self.lottery_logic.draw(mode)
        if winner:
            self.winner_label.config(text=winner)
        else:
            self.winner_label.config(text="All done!")
        # 停止滚动效果
        if self.roll_job:
            self.root.after_cancel(self.roll_job)
            self.roll_job = None

    def run(self):
        self.root.mainloop()
