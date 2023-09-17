from http.server import BaseHTTPRequestHandler, HTTPServer
import http.cookies
import os
import time
import base64
from urllib.parse import urlparse, parse_qs

# Get port number from the PORT environment varaible or 3000 if not specified
port = int(os.getenv('PORT', 3000))
hostName = '0.0.0.0'

gusp_msg='gusp here'
xss_msg='xss here'


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/xss':
            query = urlparse(self.path).query
            xss_msg=query
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(gusp_msg, 'utf-8'))
            self.wfile.write(bytes(xss_msg, 'utf-8'))
    def do_POST(self):
        if self.path == '/GUSP':
            req_datas = self.rfile.read(int(self.headers['content-length']))
            post_data = urlparse.parse_qs(field_data)

            if self.headers.get("Content-Type") == 'application/gusp':
                gusp_msg=post_data
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(gusp_msg, 'utf-8'))
            self.wfile.write(bytes(xss_msg, 'utf-8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))

    webServer.serve_forever()
