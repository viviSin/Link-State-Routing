import logging, threading, functools
import sched, time
import time
import socket, sys, time,random,fileinput, heapq
from sets import Set
from thread import allocate_lock
lock = allocate_lock()
def main():
	global neig
	global bcList
	global graph
	global nodeId
	global nodePort
	global dieList
	dieList=[]
	nodeId = str(sys.argv[1])
	nodePort = int(sys.argv[2])
	filename = str(sys.argv[3])
	_count = -1
	numNeig = 0
	neig =[]
	aa_=[]
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
			life = True
			if (nodeId < name):
				temp_ =[nodeId,name,cost,port]
			else:
				temp_ =[name,nodeId,cost,port]
			aa_.append(temp_)
			neig.append([name,cost,port,life])
		f.close(
)	except:
		sys.exit("fail to read file")

	bcList = aa_[:]
	graph = aa_[:]
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	lock = allocate_lock()
	
	t = threading.Thread(target=broadCast)
	t2 = threading.Thread(target=receive)
	t3 = threading.Thread(target=heartbeat)
	t4 = threading.Thread(target=algo)
	t.setDaemon(True)
	t2.setDaemon(True)
	t3.setDaemon(True)
	t4.setDaemon(True)
	t2.start()
	t3.start()
	t4.start()
	t.start()
	while True:
		time.sleep(1)
def algo():
	global neig
	# global bcList
	global graph
	global nodeId

	while True:
		dest = Set([])
		aGraph = dict()
		# print "len"
		# print len(graph)
		for i in range(len(graph)):
			# print "graphs"
			# print graph
			a = graph[i][0]
			b = graph[i][1]
			dest.add(graph[i][0])
			dest.add(graph[i][1])
			cost = float(graph[i][2])

			aGraph.setdefault(a, dict())
			aGraph.setdefault(b, dict())
			aGraph[a][b] = cost
			aGraph[b][a] = cost
		if nodeId in dest:
			dest.remove(nodeId)
		# print "_____life________"
		# print dest
		for destination in dest:
			(path, minCost) = Dijkstra(aGraph, nodeId, destination)
			pathArray = " ".join(path)
			print "least-cost path to node " +str(destination)+" : "+ str(pathArray) +" and the cost is " + str(minCost)
		time.sleep(30)


def Dijkstra (aGraph, nodeId, destination):
	visited = dict()  
	cost = dict() 
	parent = dict()   
	queue = []        
	path = []         

	for node in aGraph.keys():
		visited[node] = False
		cost[node] = float("inf")
	cost[nodeId] = 0
	heapq.heappush(queue, (0, nodeId))

	while queue:
		curr = heapq.heappop(queue)[1]
		visited[curr] = True
		for ne in aGraph[curr].keys():
			if (not visited[ne]):
				totCost = cost[curr] + aGraph[curr][ne]
				heapq.heappush(queue, (totCost, ne))
				if (totCost < cost[ne]):
					cost[ne] = totCost
					parent[ne] = curr
	goBack = destination
	while (not goBack == nodeId):
		path.insert(0, goBack)
		goBack = parent[goBack]

	path.insert(0, nodeId)

	return (path, cost[destination])




def heartbeat():
	global neig
	global bcList
	global graph
	global nodeId
	beater = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while True:
		for i in range(len(neig)):
			receiver_host = "localhost"
			receiver_port = neig[i][2]
			
			addr = (receiver_host, receiver_port)
			beater.sendto(str(['aLive',nodeId]),(receiver_host,receiver_port))
		# print ("heart Beating")
		time.sleep(0.3)



def broadCast():
	global neig
	global bcList
	global graph
	global dieList
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	neigHist =[[] for i in range(len(neig))]
	sendList=[]
	time.sleep(1)
	while True:
		deadList=[]
		lock.acquire(
)		#print ("my neig_____")
		#print (neig)
		if (dieList):
			# print ("who die:____")
			# print dieList
			for h in range(len(dieList)):
				if (dieList[h][1]=='new'):
					sendList=['Dead',dieList[h][0]]
					for k in range(len(neig)):
						if (neig[k][3] == True):
							# print ("pass MSG to neig : " +neig[k][0])
							receiver_host = "localhost"
							receiver_port = neig[k][2]
							addr = (receiver_host, receiver_port)
							sender.sendto(str([sendList,nodeId]),(receiver_host,receiver_port))
					dieList[h][1]= 'old'
			# dieList=[]
		lock.release()
		for i in range(len(neig)):
			sendList=[]
			if (neig[i][3] == False):
				deadList.append(neig[i])
				lis_ = []
				for ab in range(len(graph)):
					if (neig[i][0] == graph[ab][0] or neig[i][0] == graph[ab][1]):
						lis_.append(graph[ab])
				for kn in range(len(lis_)):
					graph.remove(lis_[kn])
				sendList=['Dead',neig[i][0]]
				for k in range(len(neig)):
					receiver_host = "localhost"
					receiver_port = neig[k][2]
					addr = (receiver_host, receiver_port)
					sender.sendto(str([sendList,nodeId]),(receiver_host,receiver_port))
				continue
			else:
				neig[i][3] = False
				# sendList=bcList[:]- neigHist[i][:]
				for j in range(len(bcList)):
					equal = False
					for k in range(len(neigHist[i])):
						if ((not neig[i][3]) and (bcList[j][0] == neigHist[i][k][0]) and (bcList[j][1] == neigHist[i][k][1])):
							equal = True
					if(not equal):
						sendList.append(bcList[j])
				neigHist[i].extend(sendList)
				receiver_host = "localhost"
				receiver_port = neig[i][2]
				addr = (receiver_host, receiver_port)
				sender.sendto(str([sendList,nodeId]),(receiver_host,receiver_port))
				sendList=[]
		if (deadList):
			neig.remove(deadList[0])
			deadList=[]
		time.sleep(5)



def receive():
	global neig
	global bcList
	global graph
	global nodePort
	global dieList
	receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiver.bind(("localhost", nodePort))
	while True:
		response, addr = receiver.recvfrom(1024)
		p2 = eval(response)
		# print ("recv: ")
		# print (p2)
		if (p2 and (p2[0]=='aLive')):
			for i in range(len(neig)):
				if (neig[i][0]==p2[1]):
					neig[i][3]=True
		elif (p2 and p2[0] and p2 [0][0] and (p2[0][0]=='Dead')):
			# print ("receive desd msg: " +p2[0][1])
			lock.acquire()
			repeat=False
			for i in range(len(dieList)):
				if(dieList[i][0] == p2[0][1]):
					repeat=True
			if(not repeat):
				dieList.append([p2[0][1],'new'])
			
			lock.release()
			lis_ = []
			for ab in range(len(graph)):
				if (p2[0][1] == graph[ab][0] or p2[0][1] == graph[ab][1]):
					lis_.append(graph[ab])
			for kn in range(len(lis_)):
				graph.remove(lis_[kn])
		else:	
			sendeer = p2[1]
			msg= p2[0]
			for i in range(len(msg)):
				equalG = False
				equalB = False
				if not msg:
					break
				for j in range(len(graph)):
					if ((msg[i][0] == graph[j][0]) and (msg[i][1] == graph[j][1])):
						equalG = True
				for j in range(len(bcList)):
					if ((msg[i][0] == bcList[j][0]) and (msg[i][1] == bcList[j][1])):
						equalB = True
				if(not equalG):
					graph.append(msg[i])
				if(not equalB):
					bcList.append(msg[i])


main()
