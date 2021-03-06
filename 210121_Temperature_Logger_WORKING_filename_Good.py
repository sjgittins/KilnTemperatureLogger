# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from RPi import GPIO
#import RPi.GPIO as GPIO
import board
import busio
import digitalio
import adafruit_max31855
GPIO.setmode(GPIO.BCM)
from subprocess import Popen, PIPE
from time import sleep, strftime, time
import datetime
import requests
import os
import pandas as pd
import numpy
from numpy import polyfit

#from RPLCD.gpio import CharLCD
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



#From LCD module, 4 BIT data, top 4 BITs selected, Their corresponding GPIO.BCM numbering - 
#refers to the GPIO# not the PIN number like GPIO.BOARD would be
# DB7=18
# DB6=23
# DB5=24
# DB4=25
#setup the LCD including pin and # of bits (4) 
# lcd = CharLCD(pin_rs=22, pin_e=17, pins_data=[DB4, DB5, DB6, DB7], 
# numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8, charmap='A00', auto_linebreaks=True)

#setup MAX31855 for configuration
#DO pin goes to SPI MISO aka pin Physical/Board pin 21 GPIO/BCM pin 9 Wiring Pi pin 13
#CS Alt0 GPCLK2	S Physical/Board pin 31 GPIO/BCM pin 6 Wiring Pi pin 22
#CLK alt SPIO SCLK Physical/Board pin 23 GPIO/BCM pin 11 Wiring Pi pin 14
#VCC not to exceed 4 volts, use 3.3V power
#Create the SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
max31855 = adafruit_max31855.MAX31855(spi, cs)

#setting up matplotlib doing an interactive
#plot, and creates the 2 lists that we be stuffing data into
plt.ion()
x = []
y = []

filename = 'KilnTemperature-' +str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.csv')
os.chdir('/home/pi/Data/Kiln_Temperature_Data')

with open(filename, "a") as log:
    while True:
        tempC = max31855.temperature
        tempF = tempC * 1.8 + 32
        # lcd.cursor_pos = (0,0)
        # lcd.write_string("Temp: %d C" % tempC)
        #sleep(1)
        y.append(tempF)
        x.append(time())
        plt.clf()
        plt.scatter(x,y)
        plt.xlabel('time')
        plt.ylabel('Temp F')
        plt.plot(x,y)
        plt.pause(10)
        plt.draw()

        #log the data
        #log.write is the command, and the first portion with the "{0},{1}" means
        #its a string containing two placeholders separated by a comma, and 
        #ending in a new line ( \n ) 
        #the .format(1,2) is where the 2 strings are defined ({0},{1})
        #the strftime stands for string ftime? just remember this
        #it means the current date and time as a string
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(tempF)))
#         lcd.cursor_pos = (0,0)
#         lcd.write_string("Temp: %d F" % tempF)
        print("Temperature: {} F ".format(tempF))
