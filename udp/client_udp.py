# -*- coding: utf-8 -*-
import socket
import time

#用户名口令登录
username = input("请输入用户名：")
password = input("请输入密码：")

#client 发送端
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = 8000
FORMAT='utf-8'
CLIENT = socket.gethostbyname(socket.gethostname())
server_address = ('192.168.62.2', PORT)  # 接收方 服务器的ip地址和端口号
check = '1 ' + username + '$' + password
client_socket.sendto(check.encode(), server_address)
receive_data = client_socket.recv(1024)
if receive_data.decode('utf-8') != "ok":
      print(receive_data.decode('utf-8'))
      print("登录失败！")
else:
      print("登录成功！")
      while True:
            print("\n")
            start = time.time()  #获取当前时间
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start)))  #以指定格式显示当前时间
            print("1.查看在线用户")
            print("2.向服务器发送信息")
            print("3.向在线用户发送信息")
            print("4.接收信息")
            print("5.退出")
            choice=input(f"本用户{username},请选择")
            if choice == '1':
                  msg = '3 ' + username
                  client_socket.sendto(msg.encode(), server_address) #将msg内容发送给指定接收方
                  print(client_socket.recv(1024).decode('utf-8'))
            elif choice == '2':
                  msg = input("输入要发送的内容：")
                  msg = '2 ' + msg
                  client_socket.sendto(msg.encode(), server_address) #将msg内容发送给指定接收方
                  print(client_socket.recv(1024).decode('utf-8'))
            elif choice == '3':
                  userto = input("输入用户名：")
                  while True:
                        msg = input("输入要发送的内容：")
                        if msg == 'esc':
                              break
                        msg = '4 ' + userto + '$' + msg
                        client_socket.sendto(msg.encode(), server_address) #将msg内容发送给指定接收方
                        receive = client_socket.recv(1024).decode('utf-8')
                        print(receive)
                        if receive == '用户不在！' or '用户不存在！':
                              break
            elif choice == '4':
                  client_socket.settimeout(1)  #设置一个时间提示，如果1秒钟没接到数据退出
                  print("正在接收信息")
                  while True:
                        try:
                              receive = client_socket.recv(1024)
                              print(receive.decode('utf-8'))
                        except socket.timeout:
                              print("停止接收信息")
                              break
            elif choice == '5':
                  msg = '5 esc'
                  client_socket.sendto(msg.encode(), server_address)
                  if client_socket.recv(1024).decode('utf-8') == 'ok':
                        print(f"用户{username}下线")
                        break
client_socket.close()
