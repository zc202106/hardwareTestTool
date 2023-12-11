from tkinter import Toplevel
import tkinter as tk
from decorator.gui import manage_window_visibility as mwv
from gui.common.common import *
from tkinter import ttk
from serialClient.serialClient import SerialClient as SC
from tkinter import messagebox as mb
from serial.tools import list_ports

class SerialGui:
    __values = ["COM1", "COM2", "COM3"]
    def __init__(self, root: tk.Tk):
        self.root = root
        self.serial_client = None
        self.is_port_open = False #跟踪串口状态的标记
        
    def on_close(self, win):
        win.destroy()
        self.root.deiconify()  # 重新显示主窗口
    @mwv
    def open_serial_test(self, event=None) -> Toplevel:
        #创建串口测试窗口
        serial_win = Toplevel()
        serial_win.title("串口测试")
        #获取可用串口
        self.port_list = self.get_available_ports()
        # 端口号下拉框
        ttk.Label(serial_win, text="端口号:").grid(column=0, row=0, padx=10, pady=10)
        self.port_combobox = ttk.Combobox(serial_win, values=self.port_list)
        self.port_combobox.grid(column=1, row=0, padx=10, pady=10)
        if self.port_list:
            self.port_combobox.current(0)
        # 波特率设置下拉框
        ttk.Label(serial_win, text="波特率:").grid(column=0, row=1, padx=10, pady=10)
        self.baudrate_combobox = ttk.Combobox(serial_win, values=[9600, 19200, 38400, 57600, 115200, 230400])
        self.baudrate_combobox.grid(column=1, row=1, padx=10, pady=10)
        #设置默认选择项
        self.baudrate_combobox.current(4)
        # 校验位下拉框
        ttk.Label(serial_win, text="校验位:").grid(column=0, row=2, padx=10, pady=10)
        self.parity_combobox = ttk.Combobox(serial_win, values=["None", "Even", "Odd"])
        self.parity_combobox.grid(column=1, row=2, padx=10, pady=10)
        self.parity_combobox.current(0)
        # 数据位下拉框
        ttk.Label(serial_win, text="数据位:").grid(column=0, row=3, padx=10, pady=10)
        self.databit_combobox = ttk.Combobox(serial_win, values=["5", "6", "7", "8"])
        self.databit_combobox.grid(column=1, row=3, padx=10, pady=10)
        self.databit_combobox.current(3)
        # 停止位下拉框
        ttk.Label(serial_win, text="停止位:").grid(column=0, row=4, padx=10, pady=10)
        self.stopbit_combobox = ttk.Combobox(serial_win, values=["1", "1.5", "2"])
        self.stopbit_combobox.grid(column=1, row=4, padx=10, pady=10)
        self.stopbit_combobox.current(0)
        # 流控下拉框
        ttk.Label(serial_win, text="流控:").grid(column=0, row=5, padx=10, pady=10)
        self.flowcontrol_combobox = ttk.Combobox(serial_win, values=["None", "XON/XOFF", "RTS/CTS"])
        self.flowcontrol_combobox.grid(column=1, row=5, padx=10, pady=10)
        self.flowcontrol_combobox.current(0)
        # 打开串口按钮
        self.open_port_button = tk.Button(serial_win, text="打开串口", command=self.open_port)
        self.open_port_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10, sticky="ew")
        # 板端测试串口下拉框
        ttk.Label(serial_win, text="板端测试串口:").grid(column=0, row=7, padx=10, pady=10)
        board_port_combobox = ttk.Combobox(serial_win, values=["ttyS" + str(i) for i in range(0, 11)])
        board_port_combobox.grid(column=1, row=7, padx=10, pady=10)
        board_port_combobox.current(0)  # 默认选择第一个
        
        
        # 测试板端串口接收容器
        test_frame = ttk.LabelFrame(serial_win, text="测试板端串口接收")
        test_frame.grid(column=2, row=0, columnspan=2, rowspan=10, padx=10, pady=10, sticky="nsew")

        # 板端串口接收及其滚动条
        ttk.Label(test_frame, text="板端串口接收:").pack(padx=10, pady=(10, 0), anchor="w")
        receive_frame = ttk.Frame(test_frame)
        receive_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.receive_text = tk.Text(receive_frame, height=10, width=30)
        receive_scroll = ttk.Scrollbar(receive_frame, orient="vertical", command=self.receive_text.yview)
        self.receive_text.configure(yscrollcommand=receive_scroll.set)
        self.receive_text.pack(side="left", fill="both", expand=True)
        receive_scroll.pack(side="right", fill="y")

        # PC端串口发送及其滚动条
        ttk.Label(test_frame, text="PC端串口发送:").pack(padx=10, pady=(10, 0), anchor="w")
        send_frame = ttk.Frame(test_frame)
        send_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.send_text = tk.Text(send_frame, height=5, width=30)
        send_scroll = ttk.Scrollbar(send_frame, orient="vertical", command=self.send_text.yview)
        self.send_text.configure(yscrollcommand=send_scroll.set)
        self.send_text.pack(side="left", fill="both", expand=True)
        send_scroll.pack(side="right", fill="y")

        # 定时发送控件
        self.timing_send_var = tk.IntVar()
        timing_send_checkbutton = tk.Checkbutton(test_frame, text="定时发送: ", variable=self.timing_send_var)
        timing_send_checkbutton.pack(side="left", padx=10, pady=10)

        # 时间间隔输入框
        self.timing_interval_entry = tk.Entry(test_frame, width=5)
        self.timing_interval_entry.pack(side="left", padx=10, pady=10)

        # ms/次标签
        ttk.Label(test_frame, text="ms/次").pack(side="left", pady=10)

        # 发送按钮
        self.send_button = tk.Button(test_frame, text="发送")
        self.send_button.pack(side="left", padx=10, pady=10)

        # 字符数统计控件
        self.char_count_frame = ttk.LabelFrame(test_frame, text="字符数", relief="sunken")
        self.char_count_frame.pack(padx=10, pady=10, fill="x")
        self.received_chars_label = ttk.Label(self.char_count_frame, text="R: 0")
        self.received_chars_label.pack(side="left", padx=10)
        self.sent_chars_label = ttk.Label(self.char_count_frame, text="S: 0")
        self.sent_chars_label.pack(side="left", padx=10)
        
        # 测试板端串口发送容器
        send_test_frame = ttk.LabelFrame(serial_win, text="测试板端串口发送")
        send_test_frame.grid(column=4, row=0, columnspan=2, rowspan=10, padx=10, pady=10, sticky="nsew")

        # PC端串口接收及其滚动条
        ttk.Label(send_test_frame, text="PC端串口接收:").pack(padx=10, pady=(10, 0), anchor="w")
        pc_receive_frame = ttk.Frame(send_test_frame)
        pc_receive_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.pc_receive_text = tk.Text(pc_receive_frame, height=10, width=30)
        pc_receive_scroll = ttk.Scrollbar(pc_receive_frame, orient="vertical", command=self.pc_receive_text.yview)
        self.pc_receive_text.configure(yscrollcommand=pc_receive_scroll.set)
        self.pc_receive_text.pack(side="left", fill="both", expand=True)
        pc_receive_scroll.pack(side="right", fill="y")

        # 板端串口发送及其滚动条
        ttk.Label(send_test_frame, text="板端串口发送:").pack(padx=10, pady=(10, 0), anchor="w")
        board_send_frame = ttk.Frame(send_test_frame)
        board_send_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.board_send_text = tk.Text(board_send_frame, height=5, width=30)
        board_send_scroll = ttk.Scrollbar(board_send_frame, orient="vertical", command=self.board_send_text.yview)
        self.board_send_text.configure(yscrollcommand=board_send_scroll.set)
        self.board_send_text.pack(side="left", fill="both", expand=True)
        board_send_scroll.pack(side="right", fill="y")
                
        # 定时发送控件
        self.timing_send_var_ban_to_pc = tk.IntVar()
        timing_send_checkbutton_var_ban_to_pc = tk.Checkbutton(send_test_frame, text="定时发送: ", variable=self.timing_send_var)
        timing_send_checkbutton_var_ban_to_pc.pack(side="left", padx=10, pady=10)

        # 时间间隔输入框
        self.timing_interval_entry_var_ban_to_pc = tk.Entry(send_test_frame, width=5)
        self.timing_interval_entry_var_ban_to_pc.pack(side="left", padx=10, pady=10)

        # ms/次标签
        ttk.Label(send_test_frame, text="ms/次").pack(side="left", pady=10)

        # 发送按钮
        self.send_button_var_ban_to_pc = tk.Button(send_test_frame, text="发送")
        self.send_button_var_ban_to_pc.pack(side="left", padx=10, pady=10)

        # 字符数统计控件
        self.char_count_frame_var_ban_to_pc = ttk.LabelFrame(send_test_frame, text="字符数", relief="sunken")
        self.char_count_frame_var_ban_to_pc.pack(padx=10, pady=10, fill="x")
        self.received_chars_label_var_ban_to_pc = ttk.Label(self.char_count_frame_var_ban_to_pc, text="R: 0")
        self.received_chars_label_var_ban_to_pc.pack(side="left", padx=10)
        self.sent_chars_label_var_ban_to_pc = ttk.Label(self.char_count_frame_var_ban_to_pc, text="S: 0")
        self.sent_chars_label_var_ban_to_pc.pack(side="left", padx=10)
        
        # 返回主界面按钮
        self.return_button = tk.Button(serial_win, text="返回主界面", command=lambda: self.on_close(serial_win))
        self.return_button.grid(column=2, row=10, padx=10, pady=10, sticky="ew")
        
        
        # 这将允许右侧的接收框和发送框在必要时扩展
        for i in range(10):
            serial_win.grid_rowconfigure(i, weight=1)
        for j in range(3):
            serial_win.grid_columnconfigure(j, weight=1)

        serial_win.minsize(1000, 600)
        #页面居中
        center_window(serial_win)
        return serial_win
    
    def open_port(self):
        # 在这里添加打开串口的逻辑
        if self.is_port_open:
            # 如果串口已经打开，关闭串口
            self.close_port()
        else:
            # 如果串口关闭，打开串口
            self.port = self.port_combobox.get()
            self.baudrate = self.baudrate_combobox.get()
            # 校验位、数据位、停止位和流控的获取逻辑
            self.databit = self.databit_combobox.get()
            self.paritybit = self.parity_combobox.get()
            self.stopbit = self.stopbit_combobox.get()
            self.flowcontrol = self.flowcontrol_combobox.get()
            
            self.serial_client = SC(self.port, self.baudrate)
            if self.serial_client.open():
                self.is_port_open = True
                self.open_port_button.config(text="关闭串口")
                # 更新其他串口状态相关的操作
            else:
                # 串口打开失败的处理
                mb.showerror("串口打开失败")
                
    def close_port(self):
        if self.serial_client:
            self.serial_client.close()
            self.is_port_open = False
            self.open_port_button.config(text="打开串口")
            # 更新其他串口状态相关的操作            
                
    def get_available_ports(self):
        '''获取系统可用串口列表'''
        self.ports = list_ports.comports()
        return [port.device for port in self.ports]