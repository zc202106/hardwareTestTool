import tkinter as tk
from gui.serial.serialGui import SerialGui as SG
from gui.video.videoGui import VideoGui as VG
from gui.common.common import *
from gui.udp.udpGui import UdpGui as UG

test_buttons = []

if __name__ == "__main__" :
    #创建主窗口
    root = tk.Tk()
    root.title("硬件测试工具")
    root.minsize(550, 100)    

    # 测试项的框架
    test_frame = tk.Frame(root)
    test_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

    # 子测试项按钮采用栅格布局
    serial_test = SG(root)
    btn_serial = tk.Button(test_frame, text="串口测试", command=serial_test.open_serial_test)
    btn_serial.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    test_buttons.append(btn_serial)
    video_test = VG(root)
    btn_video = tk.Button(test_frame, text="视频测试", command=video_test.open_video_test)
    btn_video.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    test_buttons.append(btn_video)
    # 配置测试项框架的行列权重
    test_frame.grid_rowconfigure(0, weight=1)
    test_frame.grid_columnconfigure([0, 1], weight=1)
    
    # UDP连接框架
    udp_connection_frame = UG(root, test_buttons)
    udp_connection_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

    # 主界面居中
    center_window(root)

    # 运行主循环
    root.mainloop()