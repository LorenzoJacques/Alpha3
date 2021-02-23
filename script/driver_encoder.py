#!/usr/local/bin/python
# coding: latin-1

import RPi.GPIO as GPIO
import time
import settings

#This program is event based :
#It will wait for a change in the value of A or B.
#Then, the callback and the rising/falling methods will understand in wich direction the encoder is being rotated.
#Since our encoder is very precise, we use a moving average to clean the input

#----Local Variables----#
angle=0 #Variable saving the relative angle of the encoder from it's start position
angle_tic=0.30 #Since we are using a 1200-per-rotation encoder, one tic is equal to 0.30 degree
nb_event_to_save=9 #Number of past event constituting the moving average
moving_avg=[0]*nb_event_to_save
gpio={
"rotor_A":settings.GPIO_encoder[0],
"rotor_B":settings.GPIO_encoder[1]
}

#Configuration of the callback function
GPIO.add_event_detect(gpio['rotor_A'], GPIO.BOTH, callback=callback_A)
GPIO.add_event_detect(gpio['rotor_B'], GPIO.BOTH, callback=callback_B)


#----Methods----#

def get_angle() :
    global angle
    return angle

def average_handler(input) : #Method handling the moving average
    global angle
    moving_avg.append(input)
    moving_avg.pop(0)
    if sum(moving_avg)>=5 :
        angle += angle_tic
    else :
        angle -= angle_tic
    angle=angle%360

#----Callback Methods----#
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

#----Which call one of those----#

def rising_A():
	global angle
	if GPIO.input(gpio["rotor_B"]) :
		average_handler(1)
	else :
		average_handler(0)

def rising_B():
	global angle
	if GPIO.input(gpio["rotor_A"]) :
		average_handler(0)
	else :
		average_handler(1)

def falling_A():
	global angle
	if GPIO.input(gpio["rotor_A"]) :
		average_handler(0)
	else :
		average_handler(1)

def falling_B():
	global angle
	if GPIO.input(gpio["rotor_B"]) :
		average_handler(1)
	else :
		average_handler(0)

if __name__=="__main__" :
    on=True
    while on :
        print(angle)
        time.sleep(1)
