#!/usr/local/bin/python
# coding: latin-1

import RPi.GPIO as GPIO

#----Variables d'intégration----#
#Calibrage du potentiometre
potentiometer_inferior=333
potentiometer_superior=666
#Calibrage du vitrail
calibrageW=4
calibrageH=7
r0=380 #Tailel des trois cercles permettant de centrer les points dans le vitrail
r1=295
r2=200

#----Déclaration des contantes----#
fps=30
screen_dimension=(1024,768)
screen_mid=(screen_dimension[0]/2+calibrageW,screen_dimension[1]/2+calibrageH) #Variable contenant les coordonnées du milieu approxiamtif du vitrail

#----Déclaration des paths----#




#----Configuration des ports GPIO----#
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#GPIO du MCP3008 servant à la lecture du potentiomètre linéaire
#GPIO connectés aux pins supérieurs 4, 5, 6 et 7 du MCP3008. Les pins 1 et 2 sont branchés sur 3.3 volts, et les pins 3 et 8 sur la masse
GPIO_MCP=[12,16,18,22]
GPIO_source=32 #GPIO fournissant l'éléctricité de l'encoeur et de la poignée
GPIO_encoder=[3,5] #GPIO dédiées à l'encodeur
GPIO_poignee=40 #GPIO dédiées à la poignée

GPIO.setup(GPIO_source), GPIO.OUT) #Allumage de la source éléctrique
