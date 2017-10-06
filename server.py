#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import os, shutil
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8080
URL = "http://192.168.1.20" + ":" + str(PORT) + "/"

class Handler(BaseHTTPRequestHandler):

    def getIndex(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            print "Error indexing directory."
            return None

        return list

    def parsePath(self, path):
        if(path == "/"):
            return None

        while path.startswith("/"):
            path = path.strip("/")

        if not os.path.exists(path):
            return None

        return path

    def setContentType(self, path):
        if os.path.isdir(path):
            return 'text/plain; charset=utf-8'
        else:
            return 'application/octet-stream'

    def do_GET(self):
        try:
            path = self.parsePath(self.path)

            if path == None:
                self.send_error(404, "file not found")
                return

            # Send code 200 response
            self.send_response(200)

            # Send header first
            self.send_header('Content-type', self.setContentType(path))
            self.end_headers()

            # Send body of the message
            if os.path.isdir(path):
                index = self.getIndex(path)

                for elem in index:
                    self.wfile.write(URL + path + '/' + elem + '\n')
            else:
                file = open(path, 'rb')
                shutil.copyfileobj(file, self.wfile)
                file.close()

            return

        except IOError:
            self.send_error(404, "file not found")
            return

def main():
    try:
        server = HTTPServer(('', PORT), Handler)
        print "Serving at port", PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down server"
        server.server_close()

if __name__ == '__main__':
    main()
