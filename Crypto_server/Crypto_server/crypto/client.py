# -*- coding: utf-8 -*-

#client



def calc_part_key(key_publ_m, key_prim, key_publ_s):
    key_part_m = key_publ_m ** key_prim % key_publ_s
    return key_part_m


def calc_full_key(key_part_s, key_prim, key_publ_s):
    key_full = key_part_s ** key_prim % key_publ_s
    return key_full

def coding (st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j += key
        j = chr(j)
        s[i] = j
    return(''.join(s))


def decoding (st, key):
    s = list(st)
    for i in range(len(s)):
        j = ord(s[i])
        j -= key
        j = chr(j)
        s[i] = j
    return(''.join(s))

def gener(i, key_prim, key_publ_m):
    global flag
    while i<3:
        i += 1
        if i == 1:
                msg = str(key_publ_m)
                sock.send(msg.encode())
                try:
                    key_publ_s = int(sock.recv(1024))
                except ValueError:
                    print("You key is invalid.")
                    flag = False
                    break
        if i == 2:
                key_part_m = calc_part_key(key_publ_m, key_prim, key_publ_s) 
                msg = str(key_part_m)
                sock.send(msg.encode())
                key_part_s = int(sock.recv(1024))
        if i == 3:
                key_full_m = calc_full_key(key_part_s, key_prim, key_publ_s)
                print(key_part_s, key_prim, key_publ_s)
                msg = str(key_full_m)
                sock.send(msg.encode())
                key_full_s = int(sock.recv(1024))
                print(key_full_s)
                with open ('keys_c.txt','w') as f:
                    f.write(str(key_full_s))
    return key_full_s

def mess(sock, key_full_m):
    msg = input('m from you:\t')
    msg_new = coding(msg,key_full_m)
    sock.send(msg_new.encode())
    msg = sock.recv(1024).decode()
    msg_new = decoding(msg,key_full_m)
    print('m from server:\t', msg_new)
    return msg_new
  
import socket
flag = True

sock = socket.socket()

sock.setblocking(1)
sock.connect(('localhost', 9090))
print('connection')
try:
    with open ('keys_c.txt','r') as f:
        for line in f:
            key_full_s = int(line);
except:
    key_prim = 199
    key_publ_m = 197
    i = 0
    msg = ''
    key_full_s = gener(i, key_prim, key_publ_m)

if flag:     
    port = mess(sock, key_full_s)
    sock.close()
    sock = socket.socket()
    sock.connect(('localhost', 1024))
    while True:
            mess(sock, key_full_s)
sock.close()
