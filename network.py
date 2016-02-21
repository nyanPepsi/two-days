import socket
import sys
import os
import multiprocessing
from multiprocessing import Pool
import threading

def client_handler(conn, q):
    #print conn
    #return ["test"]
    while True:
        #yield "test"
        msg_size = conn.recv(4)
        q.put(msg_size)
        return "test"
        #yield msg_size
        #print msg_size
        #msg = conn.recv(int(msg_size))
        #q.put(msg)
        #q.task_done()

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

            pool = []
            t = threading.Thread(target=client_handler, args=(conn, self.queue))
            t.start()
            pool.append(t)
            for el in pool:
              el.join()
            print self.queue.get()
            #print(ppool.apply_async(os.getpid, ()).get(timeout = 1))
            #res = ppool.apply_async(client_handler, args = (conn, addr)).get()
            #print conn
            #result.append(ppool.apply_async(client_handler, args = ([conn, ])).get())
            #print(result)

    def connect(self, ip, port = 9090):
        self.sock = socket.socket()
        self.sock.connect((ip, port))

    def send(self, data, size):
        self.sock.send(str(size))
        self.sock.send(data)
    
    def __exit__(self):
        self.sock.close()