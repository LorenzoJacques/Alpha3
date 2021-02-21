import RPi.GPIO as GPIO

#----Déclaration des contantes----#
fps=
encoder_tic=

#----Déclaration des paths----#


#----Variables d'intégration----#
potentiometer_inferior=333
potentiometer_superior=666

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
