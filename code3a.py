from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

# Get port number from the PORT environment varaible or 3000 if not specified
port = int(os.getenv('PORT', 3000))
hostName = '0.0.0.0'

username='CNS-user'
password='CNS-password'

class MyServer(BaseHTTPRequestHandler):
    def basic_auth(self, username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return token
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes("failed", 'utf-8'))
        elif self.headers.get("Authorization") == "Basic " + self.basic_auth(username, password):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("ok", 'utf-8'))
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes("failed", 'utf-8'))
    def do_POST(self):
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes("failed", 'utf-8'))
        elif self.headers.get("Authorization") == "Basic " + self.basic_auth(username, password):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("ok", 'utf-8'))
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes("failed", 'utf-8'))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))

    webServer.serve_forever()
