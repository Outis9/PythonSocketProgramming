import socket

HEADER = 64
PORT = 5050
FORMAT='utf-8'
DISCONNECT_MESSAGE='!DISCONNECT'
SERVER='192.168.157.1'
ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # if client.recv(2048).decode(FORMAT) == ''
    print(client.recv(2048).decode(FORMAT))

def login(uer, pwd):
  """
  将用户名和密码发送给server验证
  :param username:用户名
  :param paaword:密码
  :return:True,用户验证成功;False,用户验证失败
  """
  #传username
  username=uer.encode(FORMAT)       
  uer_length=len(username)
  send_length=str(uer_length).encode(FORMAT)
  send_length += b' '*(HEADER - len(send_length))       #转换成64长度的
  client.send(send_length)
  client.send(username)

  #传password
  password=pwd.encode(FORMAT)
  pwd_length=len(password)
  send_length=str(pwd_length).encode(FORMAT)
  send_length += b' '*(HEADER - len(send_length))
  client.send(send_length)
  client.send(password)

  #接收信息判断登入是否成功
  if client.recv(1).decode(FORMAT)=="1":
      print("登入成功")
      return True
  else:
      print("登入失败")
      return False

def main():
    uer = input("请输入用户名:")
    pwd = input("请输入密码:")
    flag=login(uer, pwd)
    if flag:
        tmp = True
        while tmp:
            text = input('请输入内容(quit-退出,recv-接受服务器信息): ')
            if text == 'quit':
                send(DISCONNECT_MESSAGE)
                tmp = False
            elif text == 'recv':
                print(client.recv(2048).decode(FORMAT))
            else:
                send(text)

if __name__=="__main__":
    main()