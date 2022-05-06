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
            print(f"[{addr}] {msg} ")
            conn.send("Msg received".encode(FORMAT))
    conn.close()

def select(username, password):
  """
  用于用户名和密码的验证
  :param username:用户名
  :param paaword:密码
  :return:True,用户验证成功；False，用户验证失败
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
        set=testlogin(conn)     #验证身份
        if set:
          thread = threading.Thread(target=handle_client,args=(conn,addr))
          thread.start()
          print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] sever is starting ...")
start()
