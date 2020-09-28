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
	def __init__(self, proc_time):
		self.proc_rate = proc_time
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
		self.time_remaining=new_task.get_pages()*60/self.page_rate
class request:
	from random import randrange
	def __init__(self, time):
		self.timestamp = time
		self.pages = randrange(1, 21)
	def get_stamp(self):
		return self.timestamp
	def get_pages(self):
		return self.pages
	def wait_time(self, current_time):
		return current_time - self.timestamp	
