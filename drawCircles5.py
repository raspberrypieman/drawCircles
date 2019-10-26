# drawCircles5.py

'''
  Inspired by, @MiniGirlGeek's beautifully hand-drawn creations
  Python version
	- Twitter @RaspPieman October 2019
'''

import pygame
import cairo
import sys
import math
import random

def getColor(x, y):
	r, g, b, a = getRBGAColor(x, y)
	# returns jsut the red part of the colour tuple
	return r

def getRBGAColor(x, y):
	buf = surface.get_data()
	# get colour component of pixel at x, y
	i = ((y * width) + x) * 4
	# returns a tuple of the red, green, blue and alpha parts
	return buf[i], buf[i+1], buf[i+2], buf[i+3]

def drawRectangle(x, y, w, h):
	ctx.rectangle(x, y, w, h)
	ctx.fill()

def drawCircles(n, r):
	m = r + 2 # prevent circles from exceeding boundary of window
	for i in range(n):
		# generate random coordinates
		x = random.randint(m, width-m) 
		y = random.randint(m, height-m) 
    
		# Only draw a circle if there is sapce for it and do not overlay fixed shaoes
		if isRoomFor(x, y, r):
			r = drawCircle(x,y,r)			

def drawCircle(x,y,r):
	global circles
	global circlesStage
	global stage
	global radius
	radius = r
	# draw a black filled circle
	setColor(BLACK)
	ctx.arc(x, y, r, 0, 2*math.pi)
	ctx.stroke_preserve()
	# fill the middle with white leaving a black circumference
	setColor(WHITE)
	ctx.fill()
	# only do a maximum of stageMax circles then reduce radius
	circles += 1
	stage += 1
	if stage >= stageMax:
		radiusStage = radius
		stage = 0		
		radius -= 1
		# do not let radius get below threshold of 2 pixels
		if radius < 2:
			radius = 2 
		else:
			print('circles', stageMax, 'radius', radiusStage)
			circlesStage += stageMax 
	return radius

def isRoomFor(x,y,z):	
	# this will return false if it detects a pixel with its 'red' component not = offWhite 
	w = 1
	r = z + w  # try to stop overlapping circles
	if not getColor(x, y) == offWhite: return False # centre pixel not offWhite
	for i in range(1, r+1):
		if not getColor(x, y-i) == offWhite: return False # North of centre
		if not getColor(x-i, y) == offWhite: return False # East of centre
		if not getColor(x, y+i) == offWhite: return False # South of centre
		if not getColor(x-i, y) == offWhite: return False # West of centre
		if not getColor(x+i, y-i) == offWhite: return False # North-East of centre
		if not getColor(x+i, y+i) == offWhite: return False # South-East of centre
		if not getColor(x-i, y+i) == offWhite: return False # South-West of centre
		if not getColor(x-i, y-i) == offWhite: return False # North-West of centre
	# All clear, so return True
	return True

def setColor(c):
	rc, gc, bc = c
	r = rc / 255
	g = gc / 255
	b = bc / 255
	ctx.set_source_rgba(b, g, r, 1.0)

# Colours
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
OFFWHITE = (254, 255, 255)
# Refers to just the red portion of the colour tuple
offWhite = 254

# Global variables
width, height = 800, 600
circles = 0
stage = 0
circlesStage = 0
radius = 13
stageMax = 50
tries = 80000

# Create window
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Create a background of offWhite (#FEFFFF)
setColor(OFFWHITE)
drawRectangle(0, 0, width, height)

# Create some fixed shapes which should not be overlapped by circles
# Draw a couple rectangles 
setColor(WHITE)
drawRectangle(120, 120, 250, 250)
drawRectangle(500, 400, 50, 60)

# Draw a triangle
ctx.move_to(500, 150)
ctx.line_to(700, 100)
ctx.line_to(700, 250)
ctx.fill()

# Attempt to draw many circles decreasing in radius
drawCircles(tries, radius)
print('circles', circles-circlesStage, 'radius', radius)	
print('circles', circles, 'done')
#print('circles', circles) # Show how many circles actually created

# Transfer image to pygame
buf = surface.get_data()
# Construct background from image buffer, created above
background = pygame.image.frombuffer(buf, (width, height), "RGBA")

screen = pygame.display.set_mode((width, height))
# Display creatyed background
screen.blit(background, (0, 0))

# Keep displaying until user closes the window
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()

	pygame.display.update()
	pygame.time.delay(100)
