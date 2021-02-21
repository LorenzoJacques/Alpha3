#!/usr/local/bin/python
# coding: latin-1

import RPi.GPIO as GPIO
import time
import settings

#----GPIO Setup----#
gpio=[
settings.GPIO_MCP[0],
settings.GPIO_MCP[1],
settings.GPIO_MCP[2],
settings.GPIO_MCP[3]
]
GPIO.setup(gpio[0],GPIO.OUT) #GPIO du pin 4 du MCP3008
GPIO.setup(gpio[1],GPIO.IN) #GPIO du pin 5 du MCP3008
GPIO.setup(gpio[2],GPIO.OUT) #GPIO du pin 6 du MCP3008
GPIO.setup(gpio[3],GPIO.OUT) #GPIO du pin 7 du MCP3008
#----Get Integrations Variables----#
low=settings.potentiometer_inferior
high=settings.potentiometer_superior

#----Methods----#
def get_type(low=low,high=high):
    value=get_potentiometer_value()
    if value<low :
        return 0
    elif low<value<high :
        return 10
    else :
        return 20

def get_potentiometer_value() :
    GPIO.output(gpio[3], True)
    GPIO.output(gpio[0], False)  # start clock low
    GPIO.output(gpio[3], False)	 # bring CS low
    commandout = 0
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3	# we only need to send 5 bits here
    for i in range(5):
    	if (commandout & 0x80):
    		GPIO.output(gpio[2], True)
    	else:
    		GPIO.output(gpio[2], False)
    	commandout <<= 1
    	GPIO.output(gpio[0], True)
    	GPIO.output(gpio[0], False)
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
    	GPIO.output(gpio[0], True)
    	GPIO.output(gpio[0], False)
    	adcout <<= 1
    	if (GPIO.input(gpio[1])):
    		adcout |= 0x1
    GPIO.output(gpio[3], True)
    adcout /= 2	   # first bit is 'null' so drop it
    return adcout

if __name__=="__main__" :
    on=True
    while on :
        print(get_type())
        time.sleep(1)
