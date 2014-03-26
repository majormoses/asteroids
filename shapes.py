import config
import math
from point import Point

class Shapes:
	def __init__(self, position, rotation, color):
		self.position = position
		self.rotation = rotation
		self.color = color
		self.active = True
		self.pull = Point(0, 0)
		

	def paint(self, surface):
		raise NotImplementedError()
		
	def game_logic(self, keys, newkeys):
		raise NotImplementedError()

	def accelerate(self, acceleration):
		angleinradians = math.radians(self.rotation)
		x = self.pull.x + acceleration * math.cos(angleinradians)
		y = self.pull.y + acceleration * math.sin(angleinradians)
		self.pull = Point(x, y)
			
	def move(self):
		if self.active == False:
			return
		posx, posy = self.position.pair()
		posx = (posx+self.pull.x) % config.SCREEN_X
		posy = (posy+self.pull.y) % config.SCREEN_Y
		self.position = Point(posx, posy)
	
	
	def rotate(self, rotation):
		if self.active == False:
			return
		self.rotation = self.rotation + rotation
		if self.rotation >= 360:
			self.rotation -= 360
		if self.rotation < 0:
			self.rotation += 360
	
	def collision(polygon1, polygon2):
		for point in polygon1.getPoints():
			if polygon2.contains(point):
				return True
		for point in polygon2.getPoints():
			if polygon1.contains(point):
				return True
		return False 