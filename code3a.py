from http.server import BaseHTTPRequestHandler, HTTPServer
import http.cookies
import os
import time
import base64
from urllib.parse import urlparse, parse_qs
import jwt

# Get port number from the PORT environment varaible or 3000 if not specified
port = int(os.getenv('PORT', 3000))
hostName = '0.0.0.0'

username='CNS-user'
password='CNS-password'

class MyServer(BaseHTTPRequestHandler):
    def basic_auth(self, username, password):
        token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return token
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        if self.path=='/basic':
            if self.headers.get("Authorization") == None:
                self.do_AUTHHEAD()
                self.wfile.write(bytes("failed", 'utf-8'))
            elif self.headers.get("Authorization") == "Basic " + self.basic_auth(username, password):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("ok", 'utf-8'))
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
        elif self.path == '/cookie':
            cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
            if 'username' not in cookies or 'password' not in cookies:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
            elif 'CNS-user' != cookies['username'].value or 'CNS-password' != cookies['password'].value:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("ok", 'utf-8'))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("root page", 'utf-8'))
    def do_POST(self):
        if self.path == '/basic':
            if self.headers.get("Authorization") == None:
                self.do_AUTHHEAD()
                self.wfile.write(bytes("failed", 'utf-8'))
            elif self.headers.get("Authorization") == "Basic " + self.basic_auth(username, password):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("ok", 'utf-8'))
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
        elif self.path == '/cookie':
            req_datas = b'https://cnshw3.adaptable.app/cookie?' + self.rfile.read(int(self.headers['content-length']))
            post_data=parse_qs(urlparse(req_datas).query)
            if b'username' not in post_data or b'password' not in post_data:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
            elif [b'CNS-user'] != post_data[b'username'] or [b'CNS-password'] != post_data[b'password']:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
            else:
                print(req_datas.decode())
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                cookie = http.cookies.SimpleCookie()
                cookie['username'] = "CNS-user"
                cookie['password'] = "CNS-password"

                for morsel in cookie.values():
                    self.send_header("Set-Cookie", morsel.OutputString())

                self.end_headers()
                self.wfile.write(bytes("ok", 'utf-8'))
        elif self.path == '/jwt':
            req_datas = b'https://cnshw3.adaptable.app/jwt?' + self.rfile.read(int(self.headers['content-length']))
            post_data=parse_qs(urlparse(req_datas).query)
            if b'username' not in post_data or b'password' not in post_data:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
            elif [b'CNS-user'] != post_data[b'username'] or [b'CNS-password'] != post_data[b'password']:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("failed", 'utf-8'))
            else:
                print(req_datas.decode())
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                body_jwt = jwt.encode({"username": "CNS-user", "password": "CNS-password"}, "secret", algorithm="HS256")
                self.wfile.write(bytes(body_jwt, 'utf-8'))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("root page", 'utf-8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))

    webServer.serve_forever()
