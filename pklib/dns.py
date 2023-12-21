#!/usr/bin/env python3
import socket
from threading import Thread

class DNSSpoofer(Thread):
    daemon = True

    def __init__(self, bind, dest, port):
        super(DNSSpoofer, self).__init__()
        self.sock_src = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_dst = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind = bind
        self.dest = dest
        self.port = port
        self.stop_flag = False  # Flag to signal the thread to stop

        # get local ip-address of your own machine
        self.own_ip = socket.gethostbyname_ex(socket.gethostname())[2][0]

        # ip address in bytes
        self.me = bytes([int(x) for x in self.own_ip.split('.')])

    def run(self):
        self.sock_src.bind((self.bind, self.port))

        print(f'Please set your DNS to {self.own_ip} on your game console.')

        while not self.stop_flag:
            data, addr = self.sock_src.recvfrom(512)

            self.sock_dst.sendto(data, (self.dest, self.port))

            data, _ = self.sock_dst.recvfrom(512)

            # For GTS functionality, the game communicates with http://gamestats2.gs.nintendowifi.net/ over regular HTTP.
            # Redirect all the request that contain "gamestats2" to the address of our machine
            if bytes("gamestats2", encoding='ascii') in data:
                data = data[:-4] + self.me

            self.sock_src.sendto(data, addr)

    def stop(self):
        self.stop_flag = True  # Set the stop flag to True