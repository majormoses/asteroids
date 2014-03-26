import pygame
from polygon import Polygon
from point import Point
import config
import math
import random

class Ship(Polygon):
	def __init__(self):
		shape = [Point(24, 0), Point(-12, -12), Point(0, 0), Point(-12, 12)]
		position = Point(config.SCREEN_X/2, config.SCREEN_Y/2)
		self.rotation = config.SHIP_INITIAL_DIRECTION
		color = config.SHIP_COLOR
		Polygon.__init__(self, shape, position, self.rotation, color)
		self.accelerate = (0, 0)
		self.stop = Point(0, 0)
		pygame.mixer.init()
		self.fire_sfx = pygame.mixer.Sound("laser.wav")
		self.count = 5
		self.shield_health = 100
		self.nuke_count = 1

	def draw_shield(self, surface):
			if self.count == 5:
				self.color = pygame.Color('green')
				pygame.draw.polygon(surface, self.color, self.pairs)
			if self.count == 4:
				self.color = pygame.Color('yellow')
				pygame.draw.polygon(surface, self.color, self.pairs)
			if self.count == 3:
				self.color = pygame.Color('orange')
				pygame.draw.polygon(surface, self.color, self.pairs)
			if self.count == 2:
				self.color = pygame.Color('red')
				pygame.draw.polygon(surface, self.color, self.pairs)
			if self.count == 1:
				self.color = pygame.Color('grey')
				pygame.draw.polygon(surface, self.color, self.pairs)

	def teleport(self):
		if self.active == False:
			return
		self.position = Point(random.randint(0, config.SCREEN_X),random.randint(0, config.SCREEN_Y))

	def self_destruct(self):
		self.active = False

	def game_logic(self, keys, newkeys, bullet,nuke):
		self.move()
		#keymapping
		if pygame.K_LEFT in keys:
			self.rotate(-config.SHIP_ROTATION_RATE)
		if pygame.K_RIGHT in keys:
			self.rotate(config.SHIP_ROTATION_RATE)
		if pygame.K_UP in keys:
			angleinradians = math.radians(self.rotation)
			self.pull = Point(self.pull.x + config.SHIP_ACCELERATION_RATE * math.cos(angleinradians), self.pull.y + config.SHIP_ACCELERATION_RATE * math.sin(angleinradians))
		if pygame.K_DOWN in keys:
			angleinradians = math.radians(self.rotation - 180)
			self.pull = Point(self.pull.x + config.SHIP_ACCELERATION_RATE * math.cos(angleinradians), self.pull.y + config.SHIP_ACCELERATION_RATE * math.sin(angleinradians))
		if pygame.K_RSHIFT in keys:
			angleinradians = math.radians(self.rotation + 90)
			self.pull = Point(self.pull.x - config.SHIP_ACCELERATION_RATE * math.cos(angleinradians), self.pull.y - config.SHIP_ACCELERATION_RATE * math.sin(angleinradians))
		if pygame.K_END in keys:
			angleinradians = math.radians(self.rotation - 90)
			self.pull = Point(self.pull.x - config.SHIP_ACCELERATION_RATE * math.cos(angleinradians), self.pull.y - config.SHIP_ACCELERATION_RATE * math.sin(angleinradians))
		if pygame.K_RALT in keys:
			 self.pull = self.stop
		if pygame.K_LALT in keys:
			self.pull = Point(self.pull.x / 1.2, self.pull.y / 1.2)
		if pygame.K_SPACE in newkeys:
			if not self.active:
				return
			bullet.fire(self.position, self.rotation)
			self.fire_sfx.play()
		if pygame.K_r in keys:
			raise UserWarning()
		if pygame.K_n in keys and nuke.nuke_count > 0:
			nuke.fire(self.position, self.rotation)
		if pygame.K_t in newkeys:
			self.teleport()
		if pygame.K_DELETE in keys and pygame.K_RALT in keys:
			self.self_destruct()
