# -*- coding: utf-8 -*-

#server



def calc_part_key(key_publ_s, key_prim, key_publ_m):
    key_part_m = key_publ_s ** key_prim % key_publ_m
    return key_part_m

def calc_full_key(key_part_s, key_prim, key_publ_m):
    key_full = key_part_s ** key_prim % key_publ_m
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
                key_publ_s = int(conn.recv(1024))
                if check(key_publ_s):
                    msg = str(key_publ_m)
                    conn.send(msg.encode())
                else:
                    print("This key isn't correct")
                    flag = False
                    break
        if i == 2:
                key_part_s = int(conn.recv(1024))
                key_part_m = calc_part_key(key_publ_s, key_prim, key_publ_m)
                msg = str(key_part_m)
                conn.send(msg.encode())
        if i == 3:
                key_full_s = int(conn.recv(1024))
                key_full_m = calc_full_key(key_part_s, key_prim, key_publ_m)
                msg = str(key_full_m)
                conn.send(msg.encode())
                print(key_full_s)
                with open ('keys_s.txt','w') as f:
                    f.write(str(key_full_m))
    return key_full_m
    
def mess(conn, key_full_m):
    msg = conn.recv(1024).decode()
    msg_new = decoding(msg,key_full_m)
    print('m from server:\t', msg_new)
    msg1 = input('m from you:\t')
    msg_new1 = coding(msg1,key_full_m)
    conn.send(msg_new1.encode())
    return msg_new

def new_port(conn, key_full_m, port):
    msg = conn.recv(1024).decode()
    msg_new = decoding(msg,key_full_m)
    print('m from server:\t', msg_new)
    msg1 = str(port)
    print('m from you:\t', msg1)
    msg_new1 = coding(msg1,key_full_m)
    conn.send(msg_new1.encode())
   
def check(key_publ_s):
    i = False
    with open ('key_list.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            print(line[0])
            if line[0] == str(key_publ_s):
                i = True
    return i

def scanner(host_str):
    sock = socket.socket()
    for i in range(1024,65536):
        try:
            sock.bind((host_str, i))
            f = i
            sock.close()
            return f
        except socket.error:
            pass

import socket, csv

flag = True
port = scanner('localhost')
print(port)
sock = socket.socket()
sock.bind(('', 9090))
print('connection')
sock.listen(3)
i = 0
conn, addr = sock.accept()
print(addr)
try:
    with open ('keys_s.txt','r') as f:
        for line in f:
            key_full_m = int(line);
except:
    key_publ_m = 151
    key_prim = 157
    i = 0
    msg = ''
    key_full_m = gener(i, key_prim, key_publ_m)
    
if flag:
    new_port(conn, key_full_m, port)
    sock.close()
    sock = socket.socket()
    sock.bind(('localhost',int(port)))
    sock.listen(1)
    conn, addr = sock.accept()
    while True:
        mess(conn, key_full_m)
    
sock.close()