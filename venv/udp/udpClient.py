import socket

class UDPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        """ 发送数据到服务器 """
        self.socket.sendto(data.encode(), (self.server_ip, self.server_port))

    def receive_data(self):
        """ 接收服务器返回的数据 """
        data, _ = self.socket.recvfrom(1024)
        return data.decode()

    def close(self):
        """ 关闭 UDP 连接 """
        self.socket.close()
        
    def test_connection(self):
        try:
            self.send_data("test") #发送一个测试数据包
            data, _ = self.socket.recvfrom(1024) #尝试接收回复
            return data.decode() == "success"
        except socket.error:
            return False