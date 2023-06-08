from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

# Get port number from the PORT environment varaible or 3000 if not specified
port = int(os.getenv('PORT', 3000))
hostName = '0.0.0.0'

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, port), MyServer)
    print("Server started http://%s:%s" % (hostName, port))

    webServer.serve_forever()
