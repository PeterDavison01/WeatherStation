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
TimbleDIR = "\\192.168.16.20\WeatherStation\Timble.csv"
BackupDIR = "\home\pi\WeatherData\Backup.csv"
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
    except:
      print("Cannot connect ")
      time.sleep(5)
      continue
#--------------------------------


init()
