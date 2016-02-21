import socket
import sys
import multiprocessing

class Network:

    def client_handler(conn, addr, q):
        while True:
            msg_size = conn.recv(4)
            msg = conn.recv(int(msg_size))
            q.put(msg)

    def host(self, port = 9090, max_client_queue = 10, pool_size = 100):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(max_client_queue)
        
        ppool = multiprocessing.Pool(processes = pool_size)
        self.queue = multiprocessing.Queue()

        while True:
            conn, addr = self.sock.accept()
            print('connected: ' + str(addr))
            ppool.apply_async(Network.client_handler, (conn, addr, self.queue))

    def connect(self, ip, port = 9090):
        self.sock = socket.socket()
        self.sock.connect((ip, port))

    def send(self, data, size):
        self.sock.send(str(size))
        self.sock.send(data)
    
    def __exit__(self):
        self.sock.close()

