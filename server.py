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
    contentLength ='Content-Length: '
    thePage = ''
    location = ''	

    def finalHeader(self):
        #makes the header from given info
	self.sendHeader += self.mimetype 
	print 'finalHeader to open stuff: ' + self.location
	f = open (self.location, 'r') #os.curdir + os.sep + 
	self.thePage = f.read()
	#can't do below until sure it's a file, not a directory! If /, show appropriate index and content back	
	self.getContentLength()
	self.sendHeader += 'Content-Length: ' + self.contentLength + '\r\n'
	#f.close()
	

    def getContentLength(self):
	#gets the length of the content for the header
	self.contentLength = str( len( self.thePage.encode('utf-8') ) )
        print self.contentLength

    def getMimetype(self, part):
	ender = part.split('.')[-1]
	print 'ender is:' + ender
	if(ender == 'html'):
		return 'text/html;\r\n'
	if(ender == 'css'):
		print 'returning css answer'
		return 'text/css;\r\n'

    def headerNotFound(self):
	#builds a 404 not found
	self.sendHeader += 'HTTP/1.1 404 Not Found\r\n'
	self.sendHeader += self.mimetype + 'text/html;\r\n'
	self.thePage = "<html><head></head><body><h1>404 NOT FOUND</h1></body></html>"
	self.getContentLength()
	self.sendHeader += 'Content-Length: ' + self.contentLength + '\r\n'

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	
	a = self.data.split()
	print(a[0])

	if(a[0] == 'GET'):
            #code goes here to do anything at all

		#figure out what they want to see
		print a[1]
		

                if(os.path.isdir(os.curdir + '/www'+  a[1]) ):
                	print os.curdir + a[1]
                	print'Thats a valid directory above me! 200 Here!'
			a[1] += 'index.html'
			self.sendHeader += 'HTTP/1.1 200 OK\r\n'
			mimetypeOfficial = self.getMimetype(a[1])        	
			self.mimetype   += mimetypeOfficial
                    	self.pageExists = True
			self.location = os.curdir + '/www'+  a[1]

		elif(os.path.isfile(os.curdir + '/www' + a[1]) ):
			print os.curdir + a[1]
			print 'Thats a valid file above me! 200 OK!'
			self.sendHeader += 'HTTP/1.1 200 OK\r\n'
			mimetypeOfficial = self.getMimetype(a[1])        	
			self.mimetype   += mimetypeOfficial
                    	self.pageExists = True
			self.location = os.curdir + '/www'+  a[1]
		
		#if(a[1] == '/index.html'): #remove afterwards
                    	#load the site
                #    	self.sendHeader += 'HTTP/1.1 200 OK\r\n'
		#	mimetypeOfficial = self.getMimetype(a[1])        	
		#	self.mimetype   += mimetypeOfficial
                #    	self.pageExists = True
		#	self.location = os.curdir + '/www'+  a[1]
                
                #elif('css' in a[1]):
                    #need to make sure which one you're serving but good for now
                #   	print 'In css code'
		#	self.sendHeader += 'HTTP/1.1 200 OK\r\n'
                #   	mimetypeOfficial = self.getMimetype(a[1])    
		#	self.mimetype   += mimetypeOfficial    	
                   	#f = open(os.curdir + os.sep + 'www/base.css')
                   	#self.thePage = f.read()
                #   	self.pageExists = True
                #	self.location = os.curdir + '/www'+  a[1]


		if(self.pageExists):
		#load that page (try for index.html for now)
                    self.finalHeader() 
                   
		else:
                    #page does not exist, throw 404
                	self.headerNotFound()
	     		

	else:
		#provide error message that POST/PUT/DELETE not supported
		self.sendHeader = '405 Method Not Allowed\r\n'

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
