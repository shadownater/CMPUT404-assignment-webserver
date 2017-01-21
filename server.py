#  coding: utf-8 
import SocketServer, urllib2, mimetypes, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    #to send stuff, they need to receive a header
    sendHeader = '' 
    pageExists = False
    directExists = False
    mimetype = 'Content-Type: '

    #def finalHeader(self):
        #makes the header from given info
#	self.sendHeader += self.mimetype 
#	print os.curdir + os.sep + 'index.html'
#	f = open (os.curdir + os.sep + 'www/index.html')
#	self.thePage = f.read()
	#f.close()

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	
	a = self.data.split()
	print(a[0])

	if(a[0] == 'GET'):
            #code goes here to do anything at all

		#figure out what they want to see
		print a[1]
		
                #if(os.path.isdir(os.curdir + a[1]) ):
                #   print os.curdir + a[1]
                #   print'Thats a valid directory above me!'

                #if('deep' in a[1]):
                #    #serve deep index, css, if valid. 302 otherwise
                #    print 'Deep!'


                #    if(a[1] != '/deep'):
                #        #302 error here
                #        print 'Im a 302 error!'
                #    else:
                        #all is well
                #        print 'Arrived in deep ok!'
                #        self.sendHeader += 'HTTP/1.1 200 OK\r\n'
                #        self.mimetype += 'text/html\r\n'
                #        self.pageExists = True

		if(a[1] == '/'):
                    #load the site
                    self.sendHeader += 'HTTP/1.1 200 OK\r\n'
                    self.mimetype += 'text/html\r\n'
                    self.pageExists = True
                
                elif('css' in a[1]):
               #     #need to make sure which one you're serving but good for now
                   self.sendHeader += 'HTTP/1.1 200 OK\r\n'
                   self.mimetype += 'text/css\r\n'
                   f = open(os.curdir + os.sep + 'www/base.css')
                   self.thePage = f.read()
                   #self.pageExists = True
                


		if(self.pageExists):
		#load that page (try for index.html for now)
                    #self.finalHeader() IF THERE'S A PROBLEM IT'S HERE
                    self.sendHeader += self.mimetype
                    print 'Look below:'
                    print self.sendHeader
                    #print os.curdir + os.sep + 'index.html'
                    f = open (os.curdir + os.sep + 'www/index.html')
                    self.thePage = f.read()
		#else:
                    #page does not exist, throw 404
                #    print '404 Not ready lol!'
	     		

	else:
		#provide error message that POST/PUT/DELETE not supported
		self.sendHeader = '405 Method Not Allowed'

        self.request.sendall(self.sendHeader + '\r\n' + self.thePage)
        #self.request.sendall('OK')




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
