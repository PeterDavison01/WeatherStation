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
  temp = str(round(sense.get_temperature()))
  pressure = str(round(sense.get_pressure()))
  humidity = str(round(sense.get_humidity()))
  #print("Sensor data extracted.")
#--------------------------------

#Calculating the changes
#--------------------------------
def Calcs():
  global temp
  global humidity
  global pressure
  with open(NasDIR,'rb') as NAS:
    Naslines = NAS.readlines()
    NAS.close()
  lastline = np.genfromtxt(Naslines[-1:],delimiter=',')
  d_temp = int(temp) - int(lastline[1])
  d_pressure = int(pressure) - int(lastline[2])
  d_humidity = int(humidity) - int(lastline[3])
  with open(NasDIR,'wb') as f:
    f[-1:7] = temp
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
      Calcs()
      Transmission()
    except:
      print("Cannot connect ")
      continue
#--------------------------------

sensors()
Calcs()
#init()
