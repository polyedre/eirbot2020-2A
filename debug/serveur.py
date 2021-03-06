#!/usr/bin/env python

import socket
import sys
import threading
import time

import connection

class ServerConnection(connection.Connection):

    def __init__(self, port):
        super().__init__()
        try:
            self.sock.bind(('localhost', port))
        except socket.error as msg:
            print('Bind failed. {} : {}'.format(msg.errno, msg.args))
            sys.exit()

    def start(self):
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        # print("Inbound connection from {}".format(addr))
        threading.Thread(target=self.start_listening_thread).start()

    def start_listening_thread(self):
        if self.conn:
            self.running = True

            while self.running:
                data = self.conn.recv(1024).decode()
                if data:
                    self.on_recv(data)
        else:
            print("No connection established")

    def send_log(self, tag, message):
        self.send("{} : {} : {}".format(time.time(), tag, message))

    def send(self, data):
        """Send data to the last conn"""
        print(data)
        self.conn.send(data.encode())

    def on_recv(self, data):
        tag, message = data.split(" ", 1)
        if tag == 'SIMULATE':
            try:
                tag, message = message.split(" ", 1)
                self.send_log(tag, message)
            except:
                self.send_log("ERROR", "SIMULATE : BAD formatting")
        else:
            self.send_log(tag, message)

if __name__ == '__main__':
    s = ServerConnection(1222)
    s.start()
