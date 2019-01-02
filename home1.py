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
NasDIR = "\mnt\Nas\Timble.csv"
TimbleDIR = "\home\pi\WeatherData\Timble.csv"
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
  #print("Sensor data extracted.")
#--------------------------------

#Transmission
#--------------------------------
def Transmission():
  try:
    with open(TimbleDIR, 'rb') as HomeTimble:
      print("40")
      reader = csv.reader(HomeTimble)
      print("42")
      lines = list(reader)
      print("44")
      lines[2] = row
    with open(NasDIR, 'a') as NASTimble:
      writer = csv.writer(NASTimble)
      print("48")
      writer.writerows(lines)
    HomeTime.close()
    NASTimble.close()
    print("Data Transmitted.")
  except:
    print("Cannot connect.")
#--------------------------------

#Main
#--------------------------------
def main():
  sensors()
  fields = [strftime("%y-%m-%d %H:%M:%S"),temp,pressure,humidity]
  while True:
    if strftime("%M:%S") == "21:00":
      with open(TimbleDIR, 'w') as data:
        writer = csv.writer(data)
        writer.writerow(fields)
        data.close()
        print("Data saved.")
        backup = False
      break
    else:
      break
#--------------------------------

#Init
#--------------------------------
def init():
  while True:
    try:
      main()
      Transmission()
    except:
      print("Cannot connect ")
      time.sleep(5)
      continue
#--------------------------------


init()
