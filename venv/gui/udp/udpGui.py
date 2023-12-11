import tkinter as tk
from udp.udpClient import UDPClient as UC

class UdpGui(tk.Frame):
    def __init__(self, parent, test_buttons):
        super().__init__(parent)
        self.udp_client = None #udp客户端实例
        self.test_buttons = test_buttons
        #初始化时禁用测试项按钮
        # self.enable_test_buttons(False)
        # IP输入框
        tk.Label(self, text="IP:").pack(side="left", padx=(0, 5))
        self.ip_entry = tk.Entry(self, width=15)
        self.ip_entry.pack(side="left", padx=5)

        # 端口输入框
        tk.Label(self, text="Port:").pack(side="left", padx=(10, 5))
        self.port_entry = tk.Entry(self, width=5)
        self.port_entry.pack(side="left", padx=5)

        # 连接按钮
        connect_button = tk.Button(self, text="连接", command=self.connect)
        connect_button.pack(side="left", padx=10)

        # 断开连接按钮
        disconnect_button = tk.Button(self, text="断开连接", command=self.disconnect)
        disconnect_button.pack(side="left", padx=10)

        # 连接状态显示框
        self.status_label = tk.Label(self, text="连接状态: 未连接")
        self.status_label.pack(side="left", padx=10)

    def connect(self):
        '''打开UDP连接'''
        # 这里添加连接逻辑
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        try:
            port = int(port)
        except ValueError:
            self.status_label.config(text="连接状态：端口号无效")
            return
        self.udp_client = UC(ip, port)
        
        if self.udp_client.test_connection():
            self.status_label.config(text="连接状态: 已连接")
            self.enable_test_buttons(True)
        else:
            self.status_label.config(text="连接状态: 连接失败")
            self.enable_test_buttons(False)
            self.udp_client = None
            
    def disconnect(self):
        '''断开UDP连接'''
        if self.udp_client:
            self.udp_client.close()
            self.udp_client = None
            self.status_label.config(text="连接状态: 未连接")
            
    def enable_test_buttons(self, enable):
        state = "normal" if enable else "disabled"
        for button in self.test_buttons:
            button.config(state=state) 
            
