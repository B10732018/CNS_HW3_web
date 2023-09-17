from http.server import BaseHTTPRequestHandler, HTTPServer
import http.cookies
import os
import time
import base64
from urllib.parse import urlparse, parse_qs

# Get port number from the PORT environment varaible or 3000 if not specified
port = int(os.getenv('PORT', 3000))
hostName = '0.0.0.0'

class MyServer(BaseHTTPRequestHandler):
    xss_msg = 'xss here'
    gusp_msg = 'gusp here'
    location= []
    id=[]
    def sent_ok(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(MyServer.gusp_msg + '<br>', 'utf-8'))
        self.wfile.write(bytes(MyServer.xss_msg, 'utf-8'))
    def do_GET(self):
        if urlparse(self.path).path=='/xss':
            query = urlparse(self.path).query
            print(query)
            MyServer.xss_msg=query
            print(MyServer.xss_msg)
            self.sent_ok()
        elif '/gusp/' in urlparse(self.path).path:
            if urlparse(self.path).path[6:] in MyServer.id:
                self.send_response(302)
                self.send_header("Location", MyServer.location[int(urlparse(self.path).path[6:])])
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.sent_ok()
    def do_POST(self):
        if urlparse(self.path).path=='/gusp':
            post_data = self.rfile.read(int(self.headers['content-length'])).decode()

            if self.headers.get("Content-Type") == 'application/gusp':
                MyServer.gusp_msg = post_data
                url=post_data.split('|')[2]
                url=url.split('[')[0]
                MyServer.gusp_msg += '<br>'+ url+' '+len(MyServer.location)
                if url not in MyServer.location:
                    MyServer.gusp_msg += '<br>new'
                    short_id = str(len(MyServer.location))
                    MyServer.location.append(url)
                    MyServer.id.append(short_id)
                    print(MyServer.location)
                    MyServer.gusp_msg += '<br>'+short_id
                    success='[gusp]SUCCESS|'+str(len(short_id))+'|'+short_id+'[/gusp]'
                    MyServer.gusp_msg += '<br>' + success

                    self.send_response(200)
                    self.send_header("Content-Type", "application/gusp")
                    self.end_headers()
                    self.wfile.write(bytes(success, 'utf-8'))
                else:
                    MyServer.gusp_msg += '<br>old'
                    self.send_response(200)
                    self.send_header("Content-Type", "application/gusp")
                    self.end_headers()
                    self.wfile.write(bytes('[gusp]ERROR|5|error[/gusp]', 'utf-8'))
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
        else:
            self.sent_ok()

if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))
    webServer.serve_forever()
