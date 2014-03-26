from circle import Circle
from point import Point
import config

class Bullet(Circle):
	def __init__(self):
		Circle.__init__(self, Point(0, 0), config.BULLET_RADIUS, config.BULLET_COLOR, 0.0)
		self.active = False
		
	def fire(self, position, rotation):
		if self.active:
			return
		self.position = position
		self.rotation = rotation
		self.active = True
		self.pull = Point(0,0)
		self.accelerate(config.BULLET_SPEED)
		

	
	def game_logic(self, keys, newkeys):
		posx, posy = self.position.pair()
		posx = (posx+self.pull.x)
		posy = (posy+self.pull.y)
		if posx < config.SCREEN_X and posx >= 0 and posy < config.SCREEN_Y and posy >= 0:
			self.move()
		else:
			self.active = False