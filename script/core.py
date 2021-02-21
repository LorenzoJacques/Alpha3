#!/usr/local/bin/python
# coding: latin-1

#----Initialize Pygame----#
import Pygame
from pygame.locals import *

pygame.init()

Screen=pygame.display.set_mode(settings.screen_dimension,pygame.FULLSCREEN)



if __name__=="__main__":
	if len(sys.argv)>1 :
		if sys.argv[1]=="debug" :
			print("Debug Mode")
	else :
