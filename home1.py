#Libraries
#--------------------------------
import time
from time import strftime
import os
from sense_hat import SenseHat
import csv
import shutil
import distutils
from distutils import dir_util
import numpy as np
#--------------------------------


#Variables
#--------------------------------
global done
count = 0
NasDIR = '/mnt/Nas/Timble.csv'
TimbleDIR = '/home/pi/WeatherData/Timble.csv'
#--------------------------------

 
#SenseHat Sensors
#--------------------------------
def sensors():
  sense = SenseHat()
  global temp
  global humidity
  global pressure
  temp = str(round(sense.get_temperature()))
  humidity = str(round(sense.get_humidity()))
  pressure = str(round(sense.get_pressure()))
 # print("Sensor data extracted.")
#--------------------------------

#Calculating the changes
#--------------------------------
def Calcs():
  with open(NasDIR,'r') as NAS:
    lines = NAS.readlines()
  lastline = np.genfromtxt(lines[-1:],delimiter=',')
  print(lastline)
#--------------------------------

#Transmission
#--------------------------------
def Transmission():
  try:
    if done == True:
      with open(TimbleDIR, 'rb') as HomeTimble:
        reader = csv.reader(HomeTimble)
        lines = list(reader)
      with open(NasDIR, 'a') as NASTimble:
        writer = csv.writer(NASTimble)
        writer.writerows(lines)  
      HomeTimble.close()
      NASTimble.close()
      print("Transmitted")
      done = False
      global done
      time.sleep(59)
  except:
    done = False
    global done
#--------------------------------

#Main
#--------------------------------
def main():
  sensors()
  fields = [strftime("%y-%m-%d %H:%M:%S"),temp,pressure,humidity]
  while True:
    if strftime("%M:%S") == "00:00":
      with open(TimbleDIR, 'a') as data:
        writer = csv.writer(data)
        writer.writerow(fields)
        data.close()
        print("Data saved.")
        done=True
        global done
      break
    else:
      break
#--------------------------------

#Init
#--------------------------------
def init():
  done = False
  while True:
    try:
      #print("80")
      main()
      Transmission()
    except:
      print("Cannot connect ")
      continue
#--------------------------------

Calc()
#init()
