import pygame
import random
from easy import *
from data import *

#On trouve ici le cache des animations sous la forme d'un dictionnaire apellé Cache.
#Il y a aussi les méthodes permettant de charger différents tyeps d'animation
#En fin de code, on retrouve le chargement des animations qui serotn nécessaires à l'execution du programme
#C'est ce script qui charge toutes les animations, c'est donc lui qui ralenti l'ordinateur au démarage.
calibrageW=4
calibrageH=7
Cache={}
screen_dimension=(1024,768)
screen_mid=(screen_dimension[0]/2+calibrageW,screen_dimension[1]/2+calibrageH)

#METHODES DE CHARGEMENT D'ANIMATION
def load_rotate(img,name) : #Pré-charge une animation de rotation de l'image "img". Elle peut être apellé grace au string "rotate_name"
	name="rotate_"+name #Défini le nom à donner à l'instance d'Animation()
	print("Loading animation "+str(name))
	Cache[name]=[]
	for i in range(0,720) : #La rotation se fait par demi-degré. Il est possible d'augmenter ou de réduire la decomposition du mouvement en modifiant le nombre de frames. La vitesse de l'animation peut être changée à l'aide de Animation.speed
		Cache[name].append(pygame.transform.rotate(img,i/2))

def load_glow(img,name) : #Pré-charge une animation d'apparition et de disparition de l'image "img". Elle peut être apellé grace au string "glow_name"
	name="glow_"+name #Défini le nom à donner à l'instance d'Animation()
	print("Loading animation "+str(name))
	Cache[name]=[]
	for i in range(0,255) :
		temp=img.copy()
		temp.fill((255,255,255,255-i),None,pygame.BLEND_RGBA_MULT) #Cette ligne de code définit l'alpha de img. Je ne sais pas comment elle marche.
		Cache[name].append(temp)
	for i in range(0,255) :
		temp=img.copy()
		temp.fill((255,255,255,i),None,pygame.BLEND_RGBA_MULT) #Cette ligne de code définit l'alpha de img. Je ne sais pas comment elle marche.
		Cache[name].append(temp)

def load_charge(dimension,name,ball_alpha=False,img=False,concentration=3,duration=480,speed_of_ball=15) : #Pré-charge une animation de "chargement" ou des petites lumières se rassemblent en un centre où se trouve l'image "img"
	name="charge_"+name #Défini le nom à donner à l'instance d'Animation()
	print("Loading animation "+str(name))
	if ball_alpha==False :
		img_ball=pygame.image.load("..//ressources//mini0.png").convert_alpha() #Image de balle utilisée par l'animation
	else :
		img_ball=pygame.image.load("..//ressources//ball.png").convert_alpha()
	layers=[]
	surface=pygame.Surface(dimension) #Chaque balle seras crée puis intégrée à une surface. Ce sont des "photographies" de ces surface qui viendront remplir la list de frames dans Cache
	Cache[name]=[]
	for i in range(0,duration) : #A chaque itération, on crée trois nouvelles instances de charge_ball(), puis on anime les contenants de layers. On peut ensuite intégrer l'image au centre du chergement, copier l'etat de surface et l'enregistrer dans Cache
		if i<(duration-speed_of_ball) :
			for j in range(0,concentration) : #Création de trois nouvelles instances de charge_ball
				layers.append(charge_ball(surface,(random.randrange(0,dimension[0]),random.randrange(0,dimension[1])),(dimension[0]/2,dimension[1]/2),img_ball,speed_of_ball))
		surface.fill((0,0,0)) #Nettoyage de la surface
		for ball in layers :
			ball.step()
			if ball.isOver() : #Si l'animation est finie, elle est supprimée de sa couche
				layers.remove(ball)
		if img==False :
			CenterBlit(surface,img_ball,(dimension[0]/2,dimension[1]/2)) #Une fois toutes les balls déplacées, on place img par dessus, au centre
		else :
			CenterBlit(surface,img,(dimension[0]/2,dimension[1]/2)) #Une fois toutes les balls déplacées, on place img par dessus, au centre
		temp=surface.copy()
		temp.set_colorkey((0,0,0)) #Défini tous les pixels noirs comme transparents
		Cache[name].append(temp) #Intégration de la "photographie" de la surface comme une frame d'animation normale

class charge_ball() : #Classe utilisée par loard_charge(). Elle utilise le même principe que la classe Animation(), mais est utilisée sur une autre Surface par load_charge()
	def __init__(self,surface,pos,aim,img,speed) :
		self.surface=surface
		self.img=img
		self.pos=pos
		self.aim=aim
		self.nb_frames=speed #Les balles crées parcouront la distance entre leur position initiale (pos) et leur destination (aim) en ce nombre de frame.
		self.move_step=(self.aim[0]-self.pos[0],self.aim[1]-self.pos[1])
		self.move_step=(self.move_step[0]/self.nb_frames,self.move_step[1]/self.nb_frames)
		self.current_frame=0
	def step(self) :
		self.pos=(self.pos[0]+self.move_step[0],self.pos[1]+self.move_step[1])
		CenterBlit(self.surface,self.img,self.pos)
		self.current_frame+=1
	def isOver(self) : #Verifie si l'animation est arrivée à son terme, utilisé dans le step_animation() pour supprimer les animations finies
		if self.current_frame>=self.nb_frames :
				return True
		else :
			return False

def load_decharge(dimension,name,img=False,concentration=3,speed=15) : #Pré-charge une animation de "déchargement" ou des petites lumières sont expulsées du centre où se trouve l'image "img"
	name="decharge_"+name #Défini le nom à donner à l'instance d'Animation()
	print("Loading animation "+str(name))
	img_ball=pygame.image.load("..//ressources//mini0.png").convert_alpha() #Image de balle utilisée par l'animation
	layers=[]
	surface=pygame.Surface(dimension) #Chaque balle seras crée puis intégrée à une surface. Ce sont des "photographies" de ces surface qui viendront remplir la list de frames dans Cache
	Cache[name]=[]
	for i in range(0,480) : #A chaque itération, on crée trois nouvelles instances de charge_ball(), puis on anime les contenants de layers. On peut ensuite intégrer l'image au centre du chergement, copier l'etat de surface et l'enregistrer dans Cache
		if i<(480-speed) :
			for j in range(0,concentration) : #Création de trois nouvelles instances de charge_ball
				layers.append(charge_ball(surface,(dimension[0]/2,dimension[1]/2),(random.randrange(0,dimension[0]),random.randrange(0,dimension[1])),img_ball,speed))
		surface.fill((0,0,0)) #Nettoyage de la surface
		for ball in layers :
			ball.step()
			if ball.isOver() : #Si l'animation est finie, elle est supprimée de sa couche
				layers.remove(ball)
		if img==False :
			CenterBlit(surface,img_ball,(dimension[0]/2,dimension[1]/2)) #Une fois toutes les balls déplacées, on place img par dessus, au centre
		else :
			CenterBlit(surface,img,(dimension[0]/2,dimension[1]/2)) #Une fois toutes les balls déplacées, on place img par dessus, au centre
		temp=surface.copy()
		temp.set_colorkey((0,0,0)) #Défini tous les pixels noirs comme transparents
		Cache[name].append(temp) #Intégration de la "photographie" de la surface comme une frame d'animation normale

def load_grow(img,name,size,nb_frame) : #Pré-charge une animation d'apparition et de disparition de l'image "img". Elle peut être apellé grace au string "glow_name"
	name="grow_"+name #Défini le nom à donner à l'instance d'Animation()
	print("Loading animation "+str(name))
	Cache[name]=[]
	img_size=img.get_size()
	temp_img=img
	step_to_add=(
	(size[0]-img_size[0])/nb_frame,
	(size[1]-img_size[1])/nb_frame,
	)
	for i in range(0,nb_frame+1) :
		Cache[name].append(pygame.transform.scale(temp_img,(img_size[0]+int(step_to_add[0]*i),img_size[1]+int(step_to_add[1]*i))))
	Cache[name].reverse()

#MISE EN CACHE DES ANIMATIONS NECESSAIRES

#Mise en cache des animations du selecteur
load_rotate(pygame.image.load("..//ressources//anim//selector//Selector_01.png").convert_alpha(),"selector_0") #Charge dans le cache une annimation de rotation du selector de l'element
load_rotate(pygame.image.load("..//ressources//anim//selector//Selector_101.png").convert_alpha(),"selector_10") #Charge dans le cache une annimation de rotation du selector de la planete
load_rotate(pygame.image.load("..//ressources//anim//selector//Selector_201.png").convert_alpha(),"selector_20") #Charge dans le cache une annimation de rotation du selector de la position

#Mise en cache des animation de chacun des 27 Points quand ils sont activés
#for i in range(0,30) : #Charge l'animation de chargement de chacuns des 27 points possibles
#	if i!=0 and i!=10 and i!=20 :
#		load_charge((100,100),str(i),img=pygame.transform.rotate(Data[i]["img"],Data[i]["tilt"]),concentration=5,speed=30)

load_charge((100,100),"point",concentration=5,speed_of_ball=30)
load_decharge((300,300),"center",concentration=5,speed=90)

load_charge((600,600),"ending",ball_alpha=True,concentration=15,duration=150,speed_of_ball=70)
load_grow(pygame.image.load("..//ressources//anim//grow//ball1000.png").convert_alpha(),"ending",(10,10),60)
