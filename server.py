# -*- coding: utf-8 -*-
import http.server
import socketserver
import os

PORT = 8001
DIRECTORY = r"C:\Users\12728\.qclaw\workspace\news-website"

os.chdir(DIRECTORY)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}")
    print(f"News website: http://119.237.242.55:{PORT}")
    httpd.serve_forever()
