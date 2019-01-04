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
NasDIR = '/mnt/Nas/Timble Data Final.csv'
TimbleDIR = '/home/pi/WeatherData/Timble.csv'
#--------------------------------

 
#SenseHat Sensors
#--------------------------------
def sensors():
  sense = SenseHat()
  global temp
  global humidity
  global pressure
  temp = (round(sense.get_temperature()))
  pressure = (round(sense.get_pressure()))
  humidity = (round(sense.get_humidity()))
  #print("Sensor data extracted.")
#--------------------------------

#Calculating the changes
#--------------------------------
def Calcs():
  global temp, humidity, pressure, d_temp, d_humidity, d_pressure
  with open(NasDIR,'r') as NAS:
    Naslines = NAS.readlines()
    NAS.close()
  lastline = np.genfromtxt(Naslines[-1:],delimiter=',')
  print(lastline)
  d_temp = (temp) - (lastline[1])
  d_pressure = (pressure) - (lastline[2])
  d_humidity = (humidity) - (lastline[3])
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
  Calcs()
  fields = [strftime("%y-%m-%d %H:%M:%S"),temp,pressure,humidity,d_temp,d_pressire,d_humidity]
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
      Calcs()
      Transmission()
    except:
      print("Cannot connect ")
      continue
#--------------------------------


init()
