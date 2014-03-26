import config
import math
import pygame
from shapes import Shapes
from point import Point

class Circle(Shapes):
	def __init__(self, position, radius, color, rotation):
		self.radius = radius
		Shapes.__init__(self, position, rotation, color)
	
	def getPoints(self):
		shape = []
		for i in range(config.COLLISION_POINTS):
			radius = self.radius
			radian = math.radians(i * 360 / config.ASTEROID_POLYGON_SIZE)
			x = math.cos(radian) * radius + self.position.x
			y = math.sin(radian) * radius + self.position.y
			shape.append(Point(x, y))
		return shape	
		
	def contains(self, point):
		dx = self.position.x - point.x
		dy = self.position.y - point.y
		return dx*dx + dy*dy <= self.radius*self.radius
	
	def paint(self, surface):
		if self.active == False:
			return
		pygame.draw.circle(surface, self.color, self.position.pair(), int(self.radius))
