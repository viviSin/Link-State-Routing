import logging, threading, functools
import sched, time
import time
import socket, sys, time,random

def main():
	global neig
	# global sender
	global nodePort
	nodeId = str(sys.argv[1])
	nodePort = int(sys.argv[2])
	filename = str(sys.argv[3])
	_count = -1
	numNeig = 0
	neig =[]
	try:
		f = open(filename, "r")
		numNeig = f.read(1)
		for line in f:
			if (_count == -1):
				_count = 1
				continue
			st = line.split(" ")
			name = str(st[0])
			cost = float(st[1])
			port =int(st[2])
			temp_ =[nodeId,name,cost,port]
			neig.append([nodeId,name,cost,port])
		f.close()
	except:
		sys.exit("fail to read file")

	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# threads = []
	t = threading.Thread(target=boardCast)
	t2 = threading.Thread(target=receive)
	# threads.append(t)
	t.setDaemon(True)
	t2.setDaemon(True)
	t.start()
	t2.start()
	while True:
		time.sleep(1)

def boardCast():
	global neig
	# global sender
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	while True:
		for i in range(len(neig)):
			receiver_host = "localhost"
			receiver_port = neig[i][3]
			addr = (receiver_host, receiver_port)
			sender.sendto(str(neig),(receiver_host,receiver_port))
			# print(receiver_port)

		print ("boardcast to neig")
		time.sleep(1)



def receive():
	"""thread worker function"""
	global neig
	# global sender
	global nodePort
	receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiver.bind(("localhost", nodePort))
	while True:
		print('receive') 
		response, addr = receiver.recvfrom(1024)
		p2 = eval(response)
		print (p2)
		# time.sleep(1)

main()
