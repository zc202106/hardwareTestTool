from tkinter import Toplevel
import tkinter as tk
from decorator.gui import manage_window_visibility as mwv
from gui.common.common import *

class VideoGui:
    def __init__(self, root: tk.Tk):
        self.root = root
    def on_close(self, win):
        win.destroy()
        self.root.deiconify()  # 重新显示主窗口
    @mwv
    def open_video_test(self, event=None) -> Toplevel:
        #创建视频测试窗口
        video_win = Toplevel()
        video_win.title("视频测试")
        # 创建一个框架来容纳接收框和滚动条
        receive_frame = tk.Frame(video_win)
        receive_frame.pack(side="top", fill="both", expand=True)
        
        # 接收框标题
        receive_title = tk.Label(receive_frame, text="视频驱动测试接收:", anchor="w")
        receive_title.pack(side="top", fill="x", pady=(5, 0))
        
        # 接收框
        receive_text = tk.Text(receive_frame, height=10)
        receive_text.pack(side="left", fill="both", expand=True)

        # 滚动条
        scroll = tk.Scrollbar(receive_frame, command=receive_text.yview)
        scroll.pack(side="right", fill="y")
        receive_text.config(yscrollcommand=scroll.set)

        # 按钮框架
        button_frame = tk.Frame(video_win)
        button_frame.pack(side="top", fill="x")

        # 开始测试按钮
        start_test_button = tk.Button(button_frame, text="开始测试", command=self.start_test)
        start_test_button.pack(side="left", padx=10, pady=10)

        # 返回主界面按钮
        return_button = tk.Button(button_frame, text="返回主界面", command=lambda: self.on_close(video_win))
        return_button.pack(side="right", padx=10, pady=10)
        video_win.minsize(500, 500)
        #页面居中
        center_window(video_win)
        return video_win
    def start_test(self):
        # 在这里添加开始测试的逻辑
        pass