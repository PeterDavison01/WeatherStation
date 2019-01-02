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
#--------------------------------


#Variables
#--------------------------------
count = 0
done = False
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
  print("Sensor data extracted.")
#--------------------------------

#Transmission
#--------------------------------
def Transmission():
  try:
      with open(TimbleDIR, 'rb') as HomeTimble:
        reader = csv.reader(HomeTimble)
        lines = list(reader)
      with open(NasDIR, 'wb') as NASTimble:
        writer = csv.writer(NASTimble)
        writer.writerows(lines)  
      HomeTimble.close()
      NASTimble.close()
   # print("Data Transmitted.")
  except:
      print("Cannot connect.")
#--------------------------------

#Main
#--------------------------------
def main():
  sensors()
  fields = [strftime("%y-%m-%d %H:%M:%S"),temp,pressure,humidity]
  while True:
    if (strftime("%M:%S") == "15:30") and (done == False):
      with open(TimbleDIR, 'a') as data:
        writer = csv.writer(data)
        writer.writerow(fields)
        data.close()
        print("Data saved.")
        done = True
      break
    else:
      done = False
      break
#--------------------------------

#Init
#--------------------------------
def init():
  while True:
    try:
      print("77")
      main()
      Transmission()
    except:
      print("Cannot connect ")
      time.sleep(5)
      continue
#--------------------------------


init()
