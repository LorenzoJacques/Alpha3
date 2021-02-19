import time

#Initialisation de Pygame et de la fenetre principale
import pygame
from pygame.locals import *

pygame.init()
screen_dimension=(500,500)
screen_mid=(screen_dimension[0]/2,screen_dimension[1]/2)
Screen=pygame.display.set_mode(screen_dimension) #Rajouter pygame.FULLSCREEN en argument pour le mode plein écran

son_win=pygame.mixer.Sound("ressources//sound//win.wav")
son_loose=pygame.mixer.Sound("ressources//sound//bad.wav")
son_end=pygame.mixer.Sound("ressources//sound//end.wav")
son_loop=pygame.mixer.Sound("ressources//sound//loop.wav")
on=True

while on :
	for event in pygame.event.get():
                #Quitter
		if event.type == QUIT:
			on=False
		if event.type == KEYDOWN and event.key == K_SPACE :
			son_win.play()
			time.sleep(3)
			son_win.stop()
			son_loose.play()
		if event.type == KEYDOWN and event.key == K_TAB :
			son_win.play()
			time.sleep(5)
			son_end.play()
		if event.type == KEYDOWN and event.key == K_a :
			print(son_loop.get_length())
			son_loop.play(loops= -1)

