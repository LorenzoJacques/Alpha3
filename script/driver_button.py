#!/usr/local/bin/python
# coding: latin-1

import RPi.GPIO as GPIO
import time
import settings
#----Local Variables----#
gpio=settings.GPIO_poignee

#----GPIO Setup----#
GPIO.setup(gpio,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#----To link a function to the rise of a GPIO
def define_callback_poignee(method) : #method will be called if the GPIO rise
	GPIO.add_event_detect(gpio, GPIO.RISING, callback=method)
