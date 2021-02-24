#!/usr/local/bin/python
# coding: latin-1

#INITIALISATION
#Initialisation de Pygame et de la fenetre principale
import pygame
from pygame.locals import *
import settings

pygame.init()
screen_mid=settings.screen_mid
Screen=pygame.display.set_mode(settings.screen_dimension) #Rajouter pygame.FULLSCREEN en argument pour le mode plein écran
#Screen étant un objet essentiel apellé tout le long du programme, il prend une majuscule
#Les dépendances on besoin que pygame soit lancé pour s'éxecuter

#Lancement des dépendances. Elles sont utilisées ici ou dans d'autres parties du programme
import time
import math
import random

#Lancement des différentes parties du programme
from easy import * #Liste de méthodes personnalsiées utilisées pour me simplifier la vie
from data import * #Structure de donnée utilisée dans le jeu
from cache import * #Gestion des animations et du cache
import driver_potentiometer as potard
import driver_encoder as encoder
import driver_button as button
import sound #Gestion du son

#CLASSE ANIMATION

#La classe Animation est utilisé pour l'affichage de toutes les animations mises dans le cache. Elle est conçue pour fonctionner avec la routine de méthodes définies plus bas.
#Avec cette classe, il n'est pas possible de faire une animation de déplacement. En revanche, on peut modifier sa vitesse et la faire boucler.
#En gros, on initialise une instace en spécifiant une position et une string arbitraire qui correspond à une des animations stockée dans le dictionnaire cache.

class Animation() : #Classe générale contenant le principe de fonctionnement de l'animation
	def __init__(self,img,pos,speed=1,anim_loop=False,begin_loop_at=0,end_loop_before=0) :
		self.max_frame=len(Cache[img])-end_loop_before #Nombre de frames contenu dans l'animation. En fonction du fps choisit, l'animation dureras plus ou moins longtemps
		self.img=img
		self.pos=pos #Position initiale de l'animation
		self.current_frame=0 #Compteur permettant de connaitre l'état général de l'animation
		self.speed=speed # Vitesse de l'animation. Définie l'incrémentation des étapes, minimum 1
		self.loop=anim_loop # Si l'animation boucle ou pas
		self.begin_loop_at=begin_loop_at #Permet de loop à en retournant à un une frame spécifiée plutot qu'à la frame 0
	def step(self) : #Méthode apellée à chaque actualisation de la fenetre
		CenterBlit(Screen,Cache[self.img][self.current_frame],self.pos) #récupére l'image correspondant à current_frame dans le cache et la colle sur Screen
		self.current_frame+=1*self.speed #La vitesse modifie la fois la vitesse d'animation
	def isOver(self) : #Verifie si l'animation est arrivée à son terme, utilisé dans le step_animation() pour supprimer les animations finies
		if self.current_frame>=self.max_frame :
			if self.loop : #Si l'animation doti boucler, la remet à zéro
				self.current_frame=0+self.begin_loop_at
				return False
			else :
				return True
		else :
			return False

#CLASSE LOGFILE

class LogFile() :
	def __init__(self) :
		self.file_name="Alpha_LogFile_"+str(time.strftime("%A %d %B %Y %H.%M.%S")+".txt")
		self.file=open(self.file_name,"w")
		self.date_start=time.strftime("%A %d %B %Y")
		self.time_start=time.strftime("%H.%M.%S")
		self.number_input=0
		self.text=[0]*3
		self.text[0]="Ce fichier est un log du jeu Astrolabium. Une partie a ete commencee le "+str(self.date_start)+" a "+str(self.time_start)+"\n"
		self.text[1]="Numero de l'input(0):Heure de l'input(1)               :Etat Hardware potentiomètre(2):Etat de la partie(3)"+"\n"
		self.text[2]="self.number_input   :time.strftime(\"%A %d %B %Y %H.%M.%S\"):chiffre de 1 à 29             :tableau contenant l'etat de chacun des points (False ou True)"+"\n"
		self.file.write(self.text[0])
		self.file.write(self.text[1])
		self.file.write(self.text[2])
		self.file.close()
		self.timer=0
	def tic(self) :
		if self.timer>=fps :
			self.shoot()
			self.timer=0
		else :
			self.timer+=1
	def shoot(self) :
		self.line=[""]*4
		self.line[0]=str(self.number_input)
		self.line[1]=str(time.strftime("%A %d %B %Y %H.%M.%S"))
		#self.line[2]=str(driver.get_msg())
		self.line[3]=str(Points)
		self.write(self.line)
	def write(self,line) :
		self.to_write=""
		for string in line :
			self.to_write=self.to_write+string+":"
		self.to_write=self.to_write+"\n"
		self.file=open(self.file_name,"a")
		self.file.write(self.to_write)
		self.file.close()
		self.number_input=self.number_input+1

#----Activating et Crashing gèrent l'animation du feedback

class Activating() :
	def __init__(self) :
		self.activating=False
		self.current_frame=0
	def step(self) :
		Layers['selector'][0].speed+=1
		Layers['selector'][1].speed+=1
		self.current_frame+=1
		if self.current_frame>=150 :
			Layers['selector'][0].speed=1
			Layers['selector'][1].speed=1
			self.activating=False
			self.current_frame=0
			sound.activation.play()
			Points[self.msg]["on"]=True #Active le point demandé par msg
			Layers['point'].append(Animation("charge_point",Points[self.msg]['pos'],anim_loop=True,begin_loop_at=30,end_loop_before=30))
	def define_msg(self,msg) :
		self.msg=msg

class Crashing() :
	def __init__(self) :
		self.activating=False
		self.current_frame=0
	def step(self) :
		Layers['selector'][0].speed+=1
		Layers['selector'][1].speed+=1
		self.current_frame+=1
		if self.current_frame>=90 :
			sound.charge.stop()
			sound.bug.play()
			Layers['selector'][0].speed=1
			Layers['selector'][1].speed=1
			self.activating=False
			self.current_frame=0

#----Creation des points----#
#L'état de chacun des 27 points à ouvrir est rangé dans la list Points
#C'est cette liste qui défini l'état de la partie
Points=[0]*30
for i in range(0,30) :
	if i!=0 and i!=10 and i!= 20 : #0, 10 et 20 ne coorepondent pas à des points qui existent.
		Points[i]={'on':False,'num':str(i),'pos':(Data[i]["pos"][0]+screen_mid[0],Data[i]["pos"][1]+screen_mid[1]),'img':pygame.transform.rotate(Data[i]["img"],Data[i]["tilt"])} #Récupère les données correspondante dans data
	else :
		Points[i]=False
#La liste Layers acceuille les différentes couches sur lesquelles on place les animation. Elles sont appliquées dans cet ordre
Layers={'background':[],'selector':[],'point':[],'temp':[]}




Layers['selector'].append(Animation("decharge_center",screen_mid,speed=1,anim_loop=True,begin_loop_at=90,end_loop_before=90)) #Lance une animation de selecteur
Layers['selector'].append(Animation("rotate_selector_0",screen_mid,speed=1,anim_loop=True)) #Lance une animation de selecteur


fps=settings.fps
on=True #Variable permettant d'arreter la boucle while principale

Clock = pygame.time.Clock() #Creation de Clock, qui sert à définir et mesurer les fps
log=LogFile() #Création du LogFile()
sound.loop.play(loops = -1) #Lancement du loop de son
activator=Activating() #Creation des classes gérant l'animation de feedback
crasher=Crashing()



#METHODE DE RAFRAICHISEMENT DE L'ECRAN

#La méthode step() sert à rafraichir l'écran. Elle centralise en fait différentes étapes pour plus de lisibilité
def step() : #Méthode apellée à chaque actualisation de l'écran
	step_clean() #Nettoie l'écran
	step_animation() #Actualise les animations en cours
	step_check_state() #Place les Points activés
	step_check_point()
	show_fps() #Montre les fps
	if activator.activating==True :
		activator.step()
	if crasher.activating==True :
		crasher.step()
	pygame.display.update() #Affiche le nouvel écran

def step_clean() : #Peint un écran noir par dessus l'image actuelle
	Screen.fill((0,0,0))

def step_check_state() : #Actualise le feedback sur l'état hardware
	msg=get_msg()
	msg1=str(msg+100)
	element=int(msg1[2])
	if element==0 :
		element=1
	tipe=int(msg1[1])
	Layers['selector'][1].img="rotate_selector_"+str(tipe*10)
	CenterBlit(Screen,Data[element+10]["img"],screen_mid)

def get_msg() :
	first_digit=potard.get_type()
	angle=encoder.get_angle()
	second_digit=get_element(angle)
	msg=first_digit+second_digit
	return msg

def get_element(angle) : #Traduit l'angle de la roue en l'élément correspondant
	if angle>340 or angle<20 :
		return 1
	if 20<angle<60 :
		return 2
	if 60<angle<100 :
		return 3
	if 100<angle<140 :
		return  4
	if 140<angle<180 :
		return 5
	if 180<angle<220 :
		return 6
	if 220<angle<260 :
		return 7
	if 260<angle<300 :
		return 8
	if 300<angle<340 :
		return 9



def step_check_point() :
	for point in Points :
		if point!=False :
			if point["on"] :
				CenterBlit(Screen,point["img"],point["pos"])

def step_animation() : #Pour chaque animation en cours, la fait avancer d'une frame, et l'affiche
	for layer in Layers :
		for anim in Layers[layer] : #Necessiée d'apeller Layers[layer] pour utiliser remove(anim) à la ligne 96
			anim.step()
			if anim.isOver() : #Si l'animation est finie, elle est supprimée de sa couche
				Layers[layer].remove(anim)

def show_fps() : #Methode affichant les fps réel en haut à gauche de la fenêtre pygame
	str_fps=str(int(Clock.get_fps()))
	font=pygame.font.SysFont("Arial", 18)
	to_blit=font.render(str_fps,1,pygame.Color("coral"))
	Screen.blit(to_blit,(0,0))

#METHODES APELLEES A L'ACTIVATION

#Activation
def Activation(meh) :
	print(meh)
	msg=get_msg()
	if IsMsgOk(msg) :
		Activation_Good(msg)
	else :
		Activation_Bad()

def Activation_Good(msg) :
	sound.charge.play()
	activator.activating=True
	activator.define_msg(msg)

def Activation_Bad() :
	sound.charge.play()
	crasher.activating=True

def IsMsgOk(msg) : #Verifie les conditions d'activation du Point demandé par msg
	if msg==1 and Points[1]["on"]==False :
		return True #Aether n'a pas de conditions d'activation
	else :
		for need in Data[msg]["need"] : #Pour chaque condition d'activation du point demandé, verifie leur activation
			if Points[need]["on"]==True and Points[msg]["on"]==False :
				return True
		return False

button.define_callback_poignee(Activation)

#Lancement de la boucle principale
while on :
	step() #Actualise l'image
	for event in pygame.event.get(): #Si pygame recoit l'évènement QUIT, arrete la boucle principale
		if event.type==QUIT :
			on=0
		if event.type == KEYDOWN and event.key == K_SPACE :
			Layers['temp'].append(Animation("charge_ending",screen_mid,speed=1,anim_loop=True)) #Lance une animation de selecteur
	log.tic() # Compte le nomre d'itération, et active la photographie du log
	Clock.tick(fps) #Attend le temps nécessaire pour avoir le fps demandé

#DEBUG

#def do_the_thing(pos) : #Lance una animation pour chaque Points, comme s'ils étaient tous activés
#	#Layers['selector'].append(Animation("decharge_win",(250,250),speed=2)) #Lance une animation de selecteur
#	for i in range(0,30) :
#		if i!=0 and i!=10 and i!=20 :
#			Layers['point'].append(Animation("charge_"+str(i),Points[i]['pos'],anim_loop=True,begin_loop_at=60,end_loop_before=60))
