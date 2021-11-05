import socket

def datasender(conn):
    while True:
    	data = conn.recv(1024)
    	datacheck = (data.decode("utf-8"))
    	print (datacheck)
    	if datacheck.upper == 'EXIT':
    		conn.send(data.upper())
    		break
    	else:
    		if not data:
    			break
    		else:
    			conn.send(data.upper())

sock = socket.socket()
sock.bind(('', 8080))
while True:
	sock.listen(1)
	conn, addr = sock.accept()

	print ('connected:', addr)
	datasender(conn)

conn.close()
