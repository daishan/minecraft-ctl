#!/usr/bin/env python

import os
import socket
import sys

def main():
	if len(sys.argv) < 2:
		print "missing arguments"
		sys.exit(1)

	if os.path.exists(sys.argv[1]) and not os.path.isdir(sys.argv[1]) and not os.path.isfile(sys.argv[1]):
		socketpath = sys.argv[1]
		cmd = ' '.join(sys.argv[2:])
	else:
		socketpath = '/tmp/minecraft-ctl'
		cmd = ' '.join(sys.argv[1:])

	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	s.connect(socketpath)
	s.send(cmd + "\n")
	data = s.recv(1024)
	s.close()
	if data:
		print data


main()
