#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import os
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SimpleHTTPServer
import SocketServer

PORT = 8080
URL = "http://192.168.1.20" + ":" + str(PORT)

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == '/':
                self.send_error(403, "You have not permissions to visit: %s" % self.path)
                return None

            if os.path.isdir('.' + self.path):
                if not self.path.endswith('/'):
                    self.send_response(301)
                    self.path = self.path + '/'

                try:
                    print '.' + self.path + 'index.txt'
                    list = os.listdir('.' + self.path)
                    file = open('.' + self.path + 'index.txt', 'w')
                    for x in list:
                        if x == "index.txt":
                            continue
                        file.write(URL + self.path + x + '\n')
                    file.close
                except os.error:
                    self.send_error(404, "No permission to list directory")
                    return None

                #self.path = self.path + 'index.txt'
                self.path = '/prueba/index.txt'
                print self.path
                #return BaseHTTPRequestHandler.do_GET(self)
                return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

            print self.path
            #return BaseHTTPRequestHandler.do_GET(self)
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        except IOError:
            print error
            self.send_error(404,"File Not Found: %s" % self.path)
            return None

def main():
    try:
        server = SocketServer.TCPServer(('', PORT), Handler)
        #server = HTTPServer(('', PORT), Handler)
        print "Serving at port", PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down server"
        server.server_close()

if __name__ == '__main__':
    main()
