from threading import Thread
import time

class Activate(Thread) :
	def __init__(self,selector,center) :
		Thread.__init__(self)
		self.selector=selector
		self.center=center
	def run(self) :
		for i in range(240) :
			self.selector.speed+=1
			self.center.speed+=1
			time.sleep(0.1)
		self.selector.speed=1
		self.center.speed=1