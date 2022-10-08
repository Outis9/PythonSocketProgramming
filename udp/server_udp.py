# -*- coding: utf-8 -*-

import socket  #导入socket模块
import time #导入time模块
    #server 接收端
    # 设置服务器默认端口号
PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
FORMAT='utf-8'
address = (SERVER, PORT)  
server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口

def userpass(): # 读取初始信息
    f = open("word.txt") # 用户名密码
    r = f.read()
    z=r.split()
    username=[]
    password=[]
    port=[]
    for word in z:
        a,b = word.split('$',1)
        username.append(a)
        password.append(b)
        port.append(0)
    return username,password,port

def start():
    a,b,c=userpass()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        now = time.time()  #获取当前时间
        receive_data, client = server_socket.recvfrom(1024) #接收信息
        choice,data=receive_data.decode('utf-8').split(' ',1)
        if choice == '1': #用户验证
            username,password=data.split('$',1)
            if username in a:
                num = a.index(username)
                if b[num] == password:
                    c[num] = client[1]
                    server_socket.sendto("ok".encode("utf-8"),client)
                    print("用户{}上线".format(username))
                else:
                    server_socket.sendto("密码错误".encode("utf-8"),client)
            else:
                server_socket.sendto("用户名不存在".encode("utf-8"),client)
        elif choice == '2': #服务器接收信息
            if client[1] in c:
                num = c.index(client[1])
                username = a[num]
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))) #以指定格式显示时间
                print("来自用户{}发来的信息：{}".format(username,data))  #打印接收的内容
                server_socket.sendto("收到！".encode("utf-8"),client)
        elif choice == '3': #查询在线用户
            useron = '在线用户：'
            for port in c:
                if port:
                    useron = useron + ' ' + a[c.index(port)]
            server_socket.sendto(str(useron).encode("utf-8"),client)
        elif choice == '4': #服务器传递信息
            username,msg=data.split('$',1)
            if username in a:
                num = a.index(username)
                if c[num] == 0:
                    server_socket.sendto("用户不在！".encode("utf-8"),client)
                else:
                    userfrom = a[c.index(client[1])]
                    server_socket.sendto("信息已发送".encode("utf-8"),client)
                    client = (client[0],c[num])
                    server_socket.sendto(f"来自用户{userfrom}发来的信息：{msg}".encode("utf-8"),client)
            else:
                server_socket.sendto("用户不存在！".encode("utf-8"),client)
        elif choice == '5': #用户下线
            if client[1] in c:
                num = c.index(client[1])
                username = a[num]
                c[num] = 0
                server_socket.sendto("ok".encode("utf-8"),client)
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))) #以指定格式显示时间
                print("用户{}下线".format(username))
    server_socket.close()

print("[STARTING] sever is starting ...")
start()
