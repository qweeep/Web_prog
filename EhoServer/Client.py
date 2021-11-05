import socket
host_name = (input('Введите имя хоста -> '))
addr = (input('Введите адрес -> '))
if (len(host_name) == 0):
	host_name = 'localhost'
if (len(addr) == 0):
	addr = "8080"
sock = socket.socket()
sock.connect((host_name, int(addr)))
while True:
	mess = input('Введите сообщение -> ')
	mess = mess.encode('utf-8')
	sock.send(mess)

	data = sock.recv(1024)
	data = data.decode('utf-8')
	print (data)
	if data == "exit":
		break
sock.close()
