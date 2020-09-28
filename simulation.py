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

def main():
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('--file', type=str)
	args=parser.parse_args()
	simulateOneServer(args.file)
if __name__=="__main__":
	main()	
		
