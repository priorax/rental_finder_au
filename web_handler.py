import http.server
import socketserver
import urllib.parse
from pprint import pprint
import json

with open('settings.json') as data_file:
    settings = json.load(data_file)

HOST_NAME = settings["server"]["hostname"] # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = settings["server"]["port"] # Maybe set this to 9000.


class Server(http.server.SimpleHTTPRequestHandler):

    print(PORT_NUMBER)

    def do_GET(self):
        from selenium_handler import handler
        self.protocol_version='HTTP/1.1'
        qs = dict(urllib.parse.parse_qsl(self.path))
        pprint(qs)
        Address = ""
        for key, value in qs.items():
            if "addr" in str.lower(key).replace("/?",""):
                    Address = value
        if Address == "":
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("Please use a GET request with the variable addr to find an address", "UTF-8"))
        else:
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/xml')
            self.end_headers()
            handler = handler(Address)
            self.wfile.write(bytes(handler.xml(settings["transport"]), "UTF-8"))
            #self.wfile.write(bytes(Address, "UTF-8"))

    def serve_forever(port):
        socketserver.TCPServer(('', port), Server).serve_forever()

if __name__ == "__main__":
    Server.serve_forever(PORT_NUMBER)
