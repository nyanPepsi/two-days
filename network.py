import socket
import sys
import os
import multiprocessing
import threading
import time
import struct

def client_handler(conn, q):
    #print conn
    #return ["test"]
    while True:
        #yield "test"
        msg_size_str = conn.recv(4)
        if not msg_size_str:
            return
        msg_size = struct.unpack('I', msg_size_str)[0]
        msg = conn.recv(msg_size)
        q.put(msg)
        q.task_done()

class Network:
    
    def close(self):
        if not (self.sock is None):
            self.sock.close()

    def host(self, port = 9090, max_client_queue = 10, pool_size = 10):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(max_client_queue)
        
        ppool = multiprocessing.Pool(processes = pool_size)
        self.queue = multiprocessing.queues.JoinableQueue()
        result = []

        while True:
            conn, addr = self.sock.accept()
            print('connected: ' + str(addr))

            t = threading.Thread(target=client_handler, args=(conn, self.queue))
            t.start()

            print self.queue.get()
            print self.queue.get()

    def connect(self, ip, port = 9090):
        self.sock = socket.socket()
        self.sock.connect((ip, port))

    def send(self, data, size):
        msg_size = struct.pack('I', size)
        self.sock.send(msg_size)
        self.sock.send(data)
    
    def __exit__(self):
        self.sock.close()
