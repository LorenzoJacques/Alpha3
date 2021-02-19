import RPi.GPIO as GPIO
from time import *

#CONFIGURATION DES PORTS GPIO
#Déclaration des variables hardware
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
MCP=[12,16,18,22] #GPIO connectés aux pins supérieurs 4, 5, 6 et 7 du MCP3008. Les pins 1 et 2 sont branchés sur 3.3 volts, et les pins 3 et 8 sur la masse 
buttons=[32,3,5,40] #Autres GPIO. Le premier correspond à la source d'éléctricité. Le deuxième au A, et le troisième au B de l'Encoder Rotatif. Le quatrième détecte la poussée de la poignée

#Déclaration des constantes
fps_driver=10 #Taux de rafraichissement de la classe Driver
angle_tic=0.30 #Taille de l'angle d'un tic de la roue
gpio={
"rotor_A":buttons[1],
"rotor_B":buttons[2],
"poignee":buttons[3],
"MCP":[12,16,18,22] #Autres GPIO. Le premier correspond à la source d'éléctricité. Le deuxième au A, et le troisième au B de l'Encoder Rotatif. Le quatrième détecte la poussée de la poignée
}
prev_inputA = 0
prev_inputB = 0
angle=0

#Configuration des GPIO
GPIO.setup(buttons[0], GPIO.OUT) #GPIO source pour la roue et la poignée
GPIO.output(buttons[0],True)
GPIO.setup(buttons[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #GPIO de l'interrupteur A de la roue
GPIO.setup(buttons[2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #GPIO de l'interrupteur B de la roue
GPIO.setup(buttons[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #GPIO de l'interrupteur de la poignée
GPIO.setup(MCP[0],GPIO.OUT) #GPIO du pin 4 du MCP3008
GPIO.setup(MCP[1],GPIO.IN) #GPIO du pin 5 du MCP3008
GPIO.setup(MCP[2],GPIO.OUT) #GPIO du pin 6 du MCP3008
GPIO.setup(MCP[3],GPIO.OUT) #GPIO du pin 7 du MCP3008

#METHODE D'ECOUTE

def get_element() : #Traduit l'angle de la roue en l'élément correspondant
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

def get_type() : #Récupère la valeur du potentiomètre et retourne 0, 10 ou 20 selon sa position
	GPIO.output(gpio["MCP"][3], True)
	GPIO.output(gpio["MCP"][0], False)  # start clock low
	GPIO.output(gpio["MCP"][3], False)	 # bring CS low
	commandout = 0
	commandout |= 0x18  # start bit + single-ended bit
	commandout <<= 3	# we only need to send 5 bits here
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(gpio["MCP"][2], True)
		else:
			GPIO.output(gpio["MCP"][2], False)
		commandout <<= 1
		GPIO.output(gpio["MCP"][0], True)
		GPIO.output(gpio["MCP"][0], False)
	adcout = 0
	# read in one empty bit, one null bit and 10 ADC bits
	for i in range(12):
		GPIO.output(gpio["MCP"][0], True)
		GPIO.output(gpio["MCP"][0], False)
		adcout <<= 1
		if (GPIO.input(gpio["MCP"][1])):
			adcout |= 0x1
	GPIO.output(gpio["MCP"][3], True)
	adcout /= 2	   # first bit is 'null' so drop it
	if 20<adcout<180 : #Si la valeur du potentiomètre augmentait proportionnellement à la distance parcourue, les ratios serianet 0-333-666-1024. Mais ce n'est pas le cas, et les valeurs utilisés sont celles divisant empiriquement la distance totale en 3
		return 0
	if 180<adcout<400 :
		return 10
	if 400<adcout<1030 :
		return 20
	return 0

def get_msg() : #Retourn le message envoyé à la machine en combinant l'élément et le type séléctionné
	return get_element()+get_type()

#CALLBACK DE LA ROUE

def rising_A():
	global angle
	if GPIO.input(gpio["rotor_B"]) :
		angle+=angle_tic
	else :
		angle-=angle_tic
	angle=angle%360

def rising_B():
	global angle
	if GPIO.input(gpio["rotor_A"]) :
		angle-=angle_tic
	else :
		angle+=angle_tic
	angle=angle%360

def falling_A():
	global angle
	if GPIO.input(gpio["rotor_A"]) :
		angle-=angle_tic
	else :
		angle+=angle_tic
	angle=angle%360

def falling_B():
	global angle
	if GPIO.input(gpio["rotor_B"]) :
		angle+=angle_tic
	else :
		angle-=angle_tic
	angle=angle%360

def callback_A(channel):
	if GPIO.input(channel)  :
		rising_A()
	else :
		falling_A()

def callback_B(channel):
	if GPIO.input(channel) :
		rising_B()
	else :
		falling_B()

GPIO.add_event_detect(gpio['rotor_A'], GPIO.BOTH, callback=callback_A)
GPIO.add_event_detect(gpio['rotor_B'], GPIO.BOTH, callback=callback_B)

#CALLBACK DE LA POIGNEE

def define_callback_poignee(methode) : #Methode permettant de connecter une methode à l'activation de la poignée
	GPIO.add_event_detect(gpio['poignee'], GPIO.RISING, callback=methode)

