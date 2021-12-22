#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.connect(('localhost', 8080))
senddat = input('Enter the message: ')
senddat = senddat.encode('utf-8')
sock.send(senddat)

data = sock.recv(1024)
data = data.decode('utf-8')
sock.close()

print (data)
