#!/bin/env python
# -*- coding: utf8 -*-

import cv2
import datetime
#import imutils
import logging
import magic        # https://github.com/ahupp/python-magic
import os
import random
import sys
import tempfile
import time
import urllib

sys.path.append('/home/rbruce/caffeV2/adbloq')
from FinalScript import Classify, makeTransparent

logging.basicConfig(filename='adbloq-icap.log', level=logging.INFO)

try:
    import socketserver
except ImportError:
    import SocketServer
    socketserver = SocketServer

sys.path.append('.')

from pyicap import *

def is_image(response_headers):
    try:
        if b"image" in response_headers["content-type"][0]:
            logging.info("Found image")
            return True # Could return content-size
        else:
            return False
    except KeyError, e:
        return False


class ThreadingSimpleServer(socketserver.ThreadingMixIn, ICAPServer):
    pass

class ICAPHandler(BaseICAPRequestHandler):

    def example_OPTIONS(self):
        self.set_icap_response(200)
        self.set_icap_header(b'Methods', b'RESPMOD')
        self.set_icap_header(b'Preview', b'0')
        self.send_headers(False)

    def example_RESPMOD(self):
        print("Hi from Squid! :)")

        self.set_icap_response(200)

        self.set_enc_status(b' '.join(self.enc_res_status)) # We may need to change content-size
        for h in self.enc_res_headers:
            for v in self.enc_res_headers[h]:
                self.set_enc_header(h, v)

        if not self.has_body:                   # Exit ctrlflow if response has no body
            self.send_headers(False)
            return

        if not is_image(self.enc_res_headers):  # Exit ctrlflow if not an image response
            self.no_adaptation_required()

        print self.enc_req
        self.send_headers(True)

        content = ''
        while True:
            chunk = self.read_chunk()
            #self.send_chunk()
            if chunk == '':
                break
            content += chunk

        if len(content) <= 50: # 1x1 pixel images around 50 bytes
            self.send_chunk(content)
            return

        # Determine filetype
        guess = magic.from_buffer(content[:256], mime=True)
        if "jpeg" in guess:
            ftype = "jpeg"
        elif "png" in guess:
            ftype = "png"
        else:
            ftype = None

        # This is just for monitoring/testing the server
        filename = urllib.quote_plus(self.enc_req[1])[:255]
        with open(foldername + os.sep + filename, 'wb') as f:
            f.write(content)

        if ftype: # If we can handle the filetype
            tf = tempfile.NamedTemporaryFile(prefix="adbloq",suffix="tmp")
            tf.write(content)
            img = cv2.imread(tf.name) # can we read directly from buffer?
            tf.close()

            result = Classify(img)

            if result:
                self.send_chunk(content)
                return

            #rotated_img = imutils.rotate(img, 180)

            transparent_img = makeTransparent(img)

            if ftype == "jpeg":
                tmp_jpg = tempfile.NamedTemporaryFile(suffix=".jpg")
                cv2.imwrite(tmp_jpg.name, transparent_img)
                self.send_chunk(tmp_jpg.read())
                tmp_jpg.close()
            elif ftype == "png":
                tmp_png = tempfile.NamedTemporaryFile(suffix=".png")
                cv2.imwrite(tmp_png.name, transparent_img)
                self.send_chunk(tmp_png.read())
                tmp_png.close()

        else:
            self.send_chunk(content)

port = 13440

server = ThreadingSimpleServer((b'', port), ICAPHandler)

foldername = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
os.mkdir(foldername)

try:
    while 1:
        server.handle_request()
except KeyboardInterrupt:
    print("Finished")

