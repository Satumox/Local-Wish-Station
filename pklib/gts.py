#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import hashlib
from base64 import urlsafe_b64decode, urlsafe_b64encode
from pklib import decrypt, util
from threading import Thread

import logging

GEN5_GTS_SALT = bytes('HZEdGCzcGGLvguqUEKQN', encoding='ascii')
GEN5_GTS_TOKEN = bytes.fromhex('00') * 32

class GTSHandler(BaseHTTPRequestHandler):

    pkmn = None

    #def log_message(self, format, *args):
    #    pass

    def do_GET(self):
        # print(self.client_address)
        # print(self.path)
        # print(self.request)
        # print(self.headers)

        path = urlparse(self.path).path
        params = parse_qs(urlparse(self.path).query)

        if len(params) == 1:
            self.send_response(200)
            self.send_header('Content-length', len(GEN5_GTS_TOKEN))
            self.end_headers()
            self.wfile.write(GEN5_GTS_TOKEN)
            return
        
        elif len(params) == 3:
            response = None

            try:
                pid = params['pid'][0]
                hash = params['hash'][0]
                data = params['data'][0]

            except IndexError:
                self.close_connection()
                return

            if path == '/syachi2ds/web/worldexchange/info.asp':
                response = bytes.fromhex('01 00')
            
            if path == '/syachi2ds/web/common/setProfile.asp':
                response = bytes.fromhex('00') * 8
            

            if path == '/syachi2ds/web/worldexchange/result.asp':

                if GTSHandler.pkmn is None:
                    response = bytes.fromhex('05 00')
                else:
                    response = GTSHandler.pkmn
                    pkmn_enc = decrypt.gen5_decrypt(GTSHandler.pkmn)
                    response += util.add_gts_data(pkmn_enc)[220:]
                    print('Sending the clone...')

            if path == '/syachi2ds/web/worldexchange/delete.asp':
                response = bytes.fromhex( '01 00')

            if path == '/syachi2ds/web/worldexchange/post.asp':
                response = bytes.fromhex('0C 00')

                data = urlsafe_b64decode(bytearray(data, encoding='ascii'))
                GTSHandler.pkmn = data[0x0C:0xE8]

                print('Stored the data for cloning!\nReenter the GTS to collect your clone.')

            hash = hashlib.sha1()
            hash.update(GEN5_GTS_SALT + urlsafe_b64encode(response) + GEN5_GTS_SALT)
            response += bytes(hash.hexdigest(), encoding='ascii')
        
            self.send_response(200)
            self.send_header('Content-length', len(response))
            self.end_headers()
            self.wfile.write(response)

class GTSServer(Thread):
    daemon = True

    def __init__(self):
        super().__init__()
        self.null_logger = logging.getLogger('null')
        self.null_logger.addHandler(logging.NullHandler())
        self.server = HTTPServer(('', 80), GTSHandler)

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()