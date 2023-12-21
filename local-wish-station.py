#!/usr/bin/env python3

import os
import platform
import sys

from pklib import dns, gts

def running_as_root():
    if platform.system() in ['Linux', 'Darwin']:
        if os.geteuid() != 0:
            print('This program needs to run as root in order to use port 53 and 80.')
            print('Please rerun the program as root.')
            return False
        
    return True


def main():

    # macOS and Linux usually require root permissions to use port 53 and 80
    if not running_as_root():
        sys.exit()

    # Redirect all incoming DNS queries to Kaeru WFC, but spoof the DNS responses 
    # for the domains that are responsible for the GTS service to point to our own machine.
    spoofer = dns.DNSSpoofer('0.0.0.0', '178.62.43.212', 53)
    spoofer.start()
    print('DNS Spoofer is running!')

    # Starting the GTS server emulator
    server = gts.GTSServer()
    server.start()
    print('Local Wish Station is running!')

    while True:
        print("Type in 'q' to quit\n>")
        cmd = input()
        if cmd.startswith('q'):
            print('Shutting down...')
            spoofer.stop()
            server.stop()
            break

if __name__ == '__main__':
    main()
