#Begin by establishing the relevant classes below:
class queue:
	def __init__(self):
		self.items = []
	def is_empty(self):
		return self.items == []
	def enqueue(self, item):
		self.items.insert(0,item)
	def dequeue(self):
		return self.items.pop()
	def size(self):
		return len(self.items)
class server:
	def __init__(self):
		self.current_task = None
		self.time_remaining = 0
	def tick(self):
		if self.current_task != None:
			self.time_remaining = self.time_remaining - 1
		if self.time_remaining <= 0:
			self.current_task = None
	def busy(self):
		if self.current_task != None:
			return True
		else:
			return False
	def start_next(self,new_task):
		self.current_task = new_task
		self.time_remaining=new_task.get_req()
class request:
	def __init__(self, time, process_req):
		self.timestamp=time
		self.process_req=process_req
	def get_stamp(self):
		return self.timestamp
	def get_req(self):
		return self.process_req
	def wait_time(self, current_time):
		return current_time - self.timestamp
def simulateOneServer(input_file):
	#Function to simulate one single server. Includes remaining queue in output.
	from csv import reader
	server_one=server()
	s_queue=queue()
	queue_time=[]
	with open(input_file) as csv_file:
		csv_requests=reader(csv_file)
		for line in csv_requests:
			job=request(int(line[0]),int(line[2]))
			s_queue.enqueue(job)
			if (not server_one.busy()) and (not s_queue.is_empty()):
				next_task=s_queue.dequeue()
				queue_time.append(next_task.wait_time(int(line[0])))
				server_one.start_next(next_task)
			server_one.tick()
	csv_file.close()
	average_wait = sum(queue_time)/len(queue_time)
	print("Average Wait %6.2f secs %3d tasks remaining."%(average_wait, s_queue.size()))
def simulateManyServers(number_servers,input_file):
	#Function to simulate many servers... not sure I did this correctly.
	from csv import reader
	queue_time=[]
	server_farm=[]
	for n in range(0,int(number_servers)):
		server_farm.append([])
		server_farm[n].append(server())
		server_farm[n].append(queue())
	#Less readable as nested lists, but it does seem to work
	with open(input_file) as csv_file:
		csv_requests=reader(csv_file)
		counter=-1
		for line in csv_requests:
			counter+=1 
			job=request(int(line[0]),int(line[2]))
			server_farm[counter%len(server_farm)][1].enqueue(job)
			if (not server_farm[counter%len(server_farm)][0].busy()) and (not server_farm[counter%len(server_farm)][1].is_empty()):
				next_task=server_farm[counter%len(server_farm)][1].dequeue()
				queue_time.append(next_task.wait_time(int(line[0])))
				server_farm[counter%len(server_farm)][0].start_next(next_task)
			server_farm[counter%len(server_farm)][0].tick()
	csv_file.close()
	average_wait = sum(queue_time)/len(queue_time)
	print("Average Wait %6.2f secs."%(average_wait))
	#Realized very late that I am unsure if I am supposed to include queue information in this function too.
	#Did I implement round robin functionality correctly? The server_farm[counter%len(server_farm)] might have worked.
def main():
	#Main function that takes relevant arguments
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('--file', type=str)
	parser.add_argument('--servers', type=int)
	args=parser.parse_args()
	if not args.servers or (args.servers==1):
		simulateOneServer(args.file)
	else:
		simulateManyServers(args.servers,args.file)
if __name__=="__main__":
	main()	
#To answer the question in Part III, the higher the number of servers, the lower the average latency		
