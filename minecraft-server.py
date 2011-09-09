#!/usr/bin/env python

import os
import sys
import socket
import select
import subprocess

if len(sys.argv) >= 2:
	if not os.path.isdir(sys.argv[1]):
		print sys.argv[1], 'is not a directory'
		sys.exit(1)
	os.chdir(sys.argv[1])

sys.path.insert(0, '')
import ctloptions as options


listensock = None
poll = select.poll()
clients = {}
proc = None


def listen():
	global listensock
	listensock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	try:
		os.remove(options.socket)
	except OSError:
		pass
	listensock.bind(options.socket)
	listensock.listen(1)
	poll.register(listensock.fileno(), select.POLLIN | select.POLLERR | select.POLLHUP)

def accept():
	conn, addr = listensock.accept()
	clients[conn.fileno()] = conn
	poll.register(conn.fileno(), select.POLLIN | select.POLLERR | select.POLLHUP)

def readctl(fd):
	conn = clients[fd]
	data = conn.recv(1024)
	if not data:
		return
	proc.stdin.write(data)
	#conn.send("OK")
	conn.close()
	poll.unregister(fd)
	del clients[fd]
	return

def start_minecraft():
	global proc
	os.chdir(options.dir)
	logfile = open(options.logfile, 'a+')
	cmd = [options.java]
	cmd.extend(options.jvmargs)
	cmd.extend(["-jar", options.serverjar])
	cmd.extend(options.serverargs)
	proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=logfile, stderr=subprocess.STDOUT)

def mainloop():
	while True:
		events = poll.poll(5000) # 5 sec
		for event in events:
			if event[1] == select.POLLIN:
				if event[0] == listensock.fileno():
					accept()
				else:
					readctl(event[0])
			elif event[1] == select.POLLHUP:
				if event[0] == listensock.fileno():
					raise Exception("wait, wat?")
				else:
					print "closing connection", repr(event)
					clients[event[0]].close()
					poll.unregister(event[0])
			elif event[1] == select.POLLERR or event[1] == select.POLLNVAL:
				if event[0] == listensock.fileno():
					raise Exception("wait, wat?")
				else:
					print "connection error..."
					clients[event[0]].close()
					poll.unregister(event[0])
			else:
				print "unhandled poll event", repr(event)
				raise Exception()
			
		# check if server is still running
		ret = proc.poll()
		if ret != None:
			print "server process died, exiting"
			sys.exit(1)

try:
	start_minecraft()
	listen()
	mainloop()
finally:
	if proc and proc.poll() == None:
		print "shutting down minecraft server..."
		proc.terminate()
