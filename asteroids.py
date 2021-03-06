import config
import pygame
from stars import Stars
from ship import Ship
from game import Game
from rock import Rock
from bullet import Bullet
from nuke import Nuke
import config
import inputbox

class Asteroids(Game):
	def __init__(self):
		Game.__init__(self, config.TITLE, config.SCREEN_X, config.SCREEN_Y)
		self.title = config.TITLE
		self.screen_x = config.SCREEN_X
		self.screen_y = config.SCREEN_Y
		self.level = 1
		self.asteroid_count = 0
		self.ship = Ship()
		self.rocks = []
		self.stars = []
		self.bullet = Bullet()
		self.bullet2 = Bullet()
		self.bullet3 = Bullet()
		self.nuke = Nuke()
		self.score = 0
		pygame.init()
		self.name = ''
		pygame.mixer.init(44100, -16, 2, 512)
		self.star_trek = pygame.mixer.Sound("Star Trek Theme Song.wav")
		self.star_trek.play(-1)
		self.ship_explosion_sfx = pygame.mixer.Sound("explosion.ogg")
		self.astroid_explosion_sfx = pygame.mixer.Sound("explosion.ogg")
		for i in range(config.ASTEROID_COUNT):
			self.rocks.append(Rock())
			self.asteroid_count += 1
		for i in range(config.STAR_COUNT):
			self.stars.append(Stars())
		for i in self.rocks:
			if i.active == False:
				self.asteroid_count -= 1
		self.high_count = 10
		self.high_score = []
		try:
			f = open("score.txt", 'r')
			for score in f:
				score.rstrip("\n")
				self.high_score.append(score)
			f.close()
			print self.high_score
		except:
			self.highscore = 0
		self.rock_dead = []

	def reset(self, position, rotation, pull):
		Game.__init__(self, config.TITLE, config.SCREEN_X, config.SCREEN_Y)
		self.ship = Ship()
		self.ship.position = position
		self.ship.rotation = rotation
		self.ship.pull = pull
		self.rocks = []
		self.stars = []
		self.asteroid_count = 0
		self.bullet = Bullet()
		self.bullet2 = Bullet()
		self.bullet3 = Bullet()
		self.nuke = Nuke()
		pygame.init()
		pygame.mixer.init(44100, -16, 2, 512)
		self.star_trek = pygame.mixer.Sound("Star Trek Theme Song.wav")
		self.star_trek.play(-1)
		self.ship_explosion_sfx = pygame.mixer.Sound("explosion.ogg")
		self.astroid_explosion_sfx = pygame.mixer.Sound("explosion.ogg")
		for i in range(config.ASTEROID_COUNT + (self.level + 1)):
			self.rocks.append(Rock())
			self.asteroid_count += 1
		for i in range(config.STAR_COUNT):
			self.stars.append(Stars())
		for i in self.rocks:
			if i.active == False:
				self.asteroid_count -= 1
		self.high_count = 10
		self.high_score = []
		try:
			f = open("score.txt", 'r')
			for score in f:
				score.rstrip()
				self.high_score.append(score)
			f.close()
		except:
			self.highscore = 0
		self.rock_dead = []



	def game_logic(self, keys, newkeys, surface):
		self.ship.game_logic(keys, newkeys,self.bullet, self.nuke)
		self.bullet.game_logic(keys, newkeys)
		self.nuke.game_logic(keys, newkeys)
		for rock in self.rocks:
			if rock.active == True:
				rock.game_logic(keys, newkeys)

				if self.bullet.collision(rock) and self.bullet.active:
					self.astroid_explosion_sfx.play()
					self.rock_dead.append(rock)
					rock.active = False
					self.asteroid_count -= 1
					self.score = self.score + 100

				if self.nuke.collision(rock) and self.nuke.active:
					self.astroid_explosion_sfx.play()
					self.rock_dead.append(rock)
					rock.active = False
					self.score = self.score + 100
					self.asteroid_count -= 1

				if self.ship.collision(rock) and self.ship.active == True:
					self.ship_explosion_sfx.play()
					self.rock_dead.append(rock)
					self.score = self.score -100

					if self.ship.shield_health >0:
						self.ship.shield_health -= 25
					rock.active = False
					self.asteroid_count -= 1
					self.ship.count -= 1

					if self.ship.count == 0:
						self.ship.active = False

		for star in self.stars:
			star.game_logic()

		if self.game_over() == config.GAME_WIN:
			pygame.mixer.quit()
			self.level += 1

			if self.level >= 5:
				self.nuke_count = 2
			self.reset(self.ship.position, self.ship.rotation, self.ship.pull)

		if (self.game_over() != config.GAME_PLAYING):
			self.name = inputbox.ask(surface, "Three Letter Initial")
			self.name = self.name[0:3]
			name_score = self.name, self.score
			self.high_score.append(str(name_score))
			print self.high_score
			self.high_score.sort(key=lambda s: eval(s)[1], reverse=True)

			if len(self.high_score) > self.high_count:
				self.high_score.pop()

	def entry_box(self):
		self.name = inputbox.ask(surface, "Your name")

	def save(self):
		f = open("score.txt", 'w')
		for score in self.high_score:
			score = score.rstrip()
			f.write(str(score)+"\n")
		f.close()

	def game_over(self):
		if not self.ship.active:
			return config.GAME_LOSE
		rocks_dead = True
		for rock in self.rocks:
			if rock.active:
				rocks_dead = False
		if rocks_dead:
			return config.GAME_WIN
		else:
			return config.GAME_PLAYING

	def paint(self, surface):
		surface.fill(config.BACKGROUND_COLOR)
		for star in self.stars:
			star.paint(surface)

		self.ship.paint(surface)
		self.ship.draw_shield(surface)
		self.bullet.paint(surface)
		self.nuke.paint(surface)

		for rock in self.rocks:
			rock.paint(surface)

		F = pygame.font.Font(None, 36)
		text = F.render("Score:" + str(self.score), True, (255, 255, 255))
		F1 = pygame.font.Font(None, 36)
		text1 = F1.render("Shield Health:" + str(self.ship.shield_health), True, (255, 255, 255))
		F2 = pygame.font.Font(None, 36)
		text2 = F2.render("Nukes:" + str(self.nuke.nuke_count), True, (255, 255, 255))
		F3 = pygame.font.Font(None, 36)
		text3 = F3.render("Level:" + str(self.level), True, (255, 255, 255))
		F4 = pygame.font.Font(None, 36)
		text4 = F4.render("Asteroids Left:" + str(self.asteroid_count), True, (255, 255, 255))
		F5 = pygame.font.Font(None, 36)

		surface.blit(text3, (0, 0))
		surface.blit(text, (0, 25))
		surface.blit(text1, (0, 50))
		surface.blit(text2, (0, 75))
		surface.blit(text4, (0, 100))

		if self.game_over() != config.GAME_PLAYING:
			xPos = 250
			yPos = 50
			high = F5.render('High Scores', True, (255, 255, 255))
			surface.blit(high, (xPos, 10))
			for line in self.high_score:
				name1, score1 = eval(str(line))
				text5 = F5.render(name1, True, (255, 255, 255))
				text6 = F5.render(str(score1), True, (255, 255, 255))
				surface.blit(text5, (xPos, yPos))
				surface.blit(text6, (xPos+100, yPos))
				yPos += 50



def main():
	restart = True
	while restart == True:
		restart = False
		try:
			a = Asteroids()
			a.main_loop()
		except UserWarning:
			restart = True

main()
