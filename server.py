#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import os, shutil
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8080
URL = "http://192.168.1.20" + ":" + str(PORT) + "/"

class Handler(BaseHTTPRequestHandler):

    def isDir(self, path):
        return os.path.isdir(path)

    def isFile(self, path):
        return os.path.isfile(path)

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

        return path

    def parseDirPath(self, path):
        if not path.endswith("/"):
            path = path + "/"

        return path

    def do_GET(self):
        try:
            path = self.parsePath(self.path)

            if path == None:
                self.send_error(403, "forbidden page")
                return

            if self.isDir(path):
                path = self.parseDirPath(path)

                index = self.getIndex(path)

                # Send code 200 response
                self.send_response(200)

                # Send header first
                self.send_header('Content-type','text/plain; charset=utf-8')
                self.end_headers()

                # Send index to client
                for elem in index:
                    self.wfile.write(URL + path + elem + '\n')

                return

            if self.isFile(path):
                # Send code 200 response
                self.send_response(200)

                # Send header first
                self.send_header('Content-type','application/octet-stream')
                self.end_headers()

                # Send file to client
                file = open(path, 'rb')
                shutil.copyfileobj(file, self.wfile)
                file.close()

                return

            self.send_error(404, "file not found")
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
