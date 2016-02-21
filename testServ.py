import network

nt = network.Network()

nt.host()

while True:
    print(nt.queue.get())
    print(nt.queue.get())
