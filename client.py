#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import socket
import base64
import random
import string
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from threading import Thread
import getpass
import os
 
class CryptoClient(object):
    def __init__(self):
        print("Welcome to CryptoChat, a secure P2P chat client coded by Me")
        print("If you don't know what you're doing, read the README.md!!!")
        self.IP = input("Please enter the IP address you wish to chat with: ")
        self.PORT = int(input("Enter the port for communication: "))
        print()
        print("Now enter the keys for the different encryption methods, make sure they are different.")
        print("Please note they will not be printed for your security.")
        print()
        self.EncryptKeyXOR = getpass.getpass("Enter desired key for XOR encryption: ")
        self.EncryptKeyAES = hashlib.md5(getpass.getpass("Enter a secure passphrase for AES: ").encode()).hexdigest()
        print()
        input("Press enter when both clients are ready.")
        ### Shit for AES padding
        BS = 16
        self.pad = lambda s: s + (BS - len(s) % BS).to_bytes(1, byteorder='big', signed=False) * (BS - len(s) % BS)
        self.unpad = lambda s: s[:-s[-1]]
        ### Start chat server and client
        try:
            Thread(target=self.RecvMSG, args=()).start()
        except socket.error as e:
            print(self.IP + " is not ready! Press enter when " + self.IP + " is ready.")
            input()
            Thread(target=self.RecvMSG, args=()).start()
        self.SendMSG()
 
    # ... (rest of your methods remain the same)
 
    def RecvMSG(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        serversocket.bind(('', self.PORT))
        while True:
            data, addr = serversocket.recvfrom(1073741824)  # buffer size is 1 gbit (for large files/images)
            data = self.DecryptMSG(data.decode())
            if data.startswith("\x02"):
                # ... (rest of the code remains the same)
            elif data.startswith("\x01"):  # all messages start with "\x01" to prevent file spamming
                data = list(data)
                del data[0]
                data = ''.join(data)
                print("[" + addr[0] + "] >  |   " + data)
            elif data.startswith("\x03"):
                print("[CLIENT] " + addr[0] + " has left.")
                sys.exit(0)
 
if __name__ == "__main__":
    if os.name == 'nt':  # Check if running on Windows
        print("Windows detected.")
        CryptoClient()
    elif os.name == 'posix':  # Check if running on Linux
        print("Linux detected.")
        CryptoClient()
    else:
        print("Unsupported operating system.")
