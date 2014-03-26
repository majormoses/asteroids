from polygon import Polygon
import random
import config
from point import Point
import pygame
import pygame.locals
import math

class Rock(Polygon):
	def __init__(self):
		shape = []
		position = Point(random.uniform(0, config.SCREEN_X), random.uniform(0, config.SCREEN_Y))
		color = config.ASTEROID_COLOR
		self.speed = random.uniform(config.ASTEROID_MIN_SPEED, config.ASTEROID_MAX_SPEED)
		rotation = random.uniform(0.0, 359.99)
		
		
		if random.randint(0, 1):
			self.speed *= -1
			
		for i in range(config.ASTEROID_POLYGON_SIZE):
			radius = random.uniform(config.ASTEROID_MIN_RADIUS, config.ASTEROID_MAX_RADIUS)
			radian = math.radians(i * 360 / config.ASTEROID_POLYGON_SIZE)
			x = math.cos(radian) * radius
			y = math.sin(radian) * radius
			shape.append(Point(x, y))
		
		Polygon.__init__(self, shape, position, rotation, color)
		self.ast_speed = random.uniform(config.ASTEROID_MIN_SPEED, config.ASTEROID_MAX_SPEED)
		self.accelerate(self.ast_speed) 


	def game_logic(self, keys, newkeys):
		self.move()
		self.rotate(self.speed)
