import socket
import threading

HEADER = 64
PORT = 5050
FORMAT='utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE='!DISCONNECT'
ADDR = (SERVER,PORT)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

messageList = []
addr_pool = []
conn_pool = []
host = []

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.\n")
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MESSAGE:
                connected=False
            else:
                messageList.append((addr,msg)) 
            print(f"[{addr}] {msg} ")
            conn.sendall(msg.upper().encode(FORMAT))
    conn.close()

def boardcast(msg):
  for i in range(0,len(conn_pool)):
    conn_pool[i].sendall(msg.encode(FORMAT))

def forwarding(index,msg):
    conn_pool[index].sendall(msg.encode(FORMAT))

def select(username, password):
  """
  用于用户名和密码的验证
  :param username:用户名
  :param paaword:密码
  :return:True,用户验证成功;False,用户验证失败
  """
  try:
    f = open("users.txt", "r", encoding="utf-8")
    for line in f:
      line = line.strip() # 清除换行符
      # 无参数时移除两侧空格，换行符
      # 有参数时移除两侧指定的字符
      line_list = line.split("$")
      if line_list[0] == username and line_list[1] == password:     #用户名与密码能对上
        return True
    return False
  except IOError:
    return False

def testlogin(conn):
    username_length=conn.recv(HEADER).decode(FORMAT)    #接收username信息
    username_length=int(username_length)
    username=conn.recv(username_length).decode(FORMAT)
    password_length=conn.recv(HEADER).decode(FORMAT)    #接收password信息
    password_length=int(password_length)
    password=conn.recv(password_length).decode(FORMAT)
    if select(username,password):   #身份验证正确
        conn.send("1".encode(FORMAT))   #向client传回信息
        return True
    else:
        conn.send("0".encode(FORMAT))
        return False

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn,addr=server.accept()
        addr_pool.append(addr)
        conn_pool.append(conn)
        set=testlogin(conn)     #验证身份
        if set:
          thread = threading.Thread(target=handle_client,args=(conn,addr))
          thread.start()
          print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-2}\n")

if __name__ == "__main__":
  print("[STARTING] sever is starting ...")
  thread2 = threading.Thread(target=start)
  thread2.start()
  while True:
    cmd = input('''
    1:查看在线人数
    2:查看所有信息
    3:广播在线客户端信息
    4:广播任意输入的信息
    5:转发信息
    6:转发消息
    7:退出
    ''')
    if cmd == '1':
      print('当前在线人数:', len(addr_pool),addr_pool)
      
    elif cmd == '2':
      print('信息列表:',messageList)
    
    elif cmd == '3':
      for h,p in addr_pool:
        text = h+':'+str(p)
        host.append(text)
      content = ' , '.join(host)
      boardcast('在线：'+content)

    elif cmd == '4':
      content = input("需要广播的信息:")
      boardcast(content)

    elif cmd == '5':
      addr,msg = messageList[0]
      forwarding(1,msg)
    elif cmd == '6':
      addr,msg = messageList[1]
      forwarding(0,msg)
    elif cmd == '7':
      exit()
