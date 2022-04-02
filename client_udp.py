# -*- coding: utf-8 -*-
import socket
import time

#client 发送端
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = 8000
FORMAT='utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
server_address = (SERVER, PORT)  # 接收方 服务器的ip地址和端口号
DISCONNECT_MESSAGE='0'
while True:
      start = time.time()  #获取当前时间
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start)))  #以指定格式显示当前时间
      msg=input(f"本客户端{SERVER},请输入要发送的内容：")  
      if msg==DISCONNECT_MESSAGE:
            break
      client_socket.sendto(msg.encode(), server_address) #将msg内容发送给指定接收方
      now = time.time() #获取当前时间
      run_time = now-start #计算时间差，即运行时间
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now)))
      print("run_time: %d seconds\n" %run_time)
