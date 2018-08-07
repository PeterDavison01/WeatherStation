#Libraries
#--------------------------------
import time
from time import strftime
import os
from sense_hat import SenseHat
import csv
import shutil
from distutils import dir_util
#--------------------------------


#Variables
#--------------------------------
count = 0
NASdir = "/mnt/Nas/"
LocalDir = "/home/pi/WeatherData/"
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
  LocalPath = (LocalDir + strftime("%d-%m-%y")+".csv")
  global count
  emptycell = ""
  fields = [strftime("%H:%M:%S"),emptycell,temp,pressure,humidity]
  while True:
    if count == 2:
      with open(LocalPath, 'a') as data:
        writer = csv.writer(data)
        writer.writerow(fields)
        data.close()
        print("Data saved.")
        count = 0
      Transmission()
      break
    else:
      time.sleep(1)
      count = count + 1
#--------------------------------

#Init
#--------------------------------
def init():
  while True:
    try:
      main()
    except:
      print("Error. Retrying in 5 seconds")
      time.sleep(5)
      count = 0
      continue
#--------------------------------


#Transmission
#--------------------------------
def Transmission():
  try:
    #distutils.dir_util.copy_tree(LocalDir, NASdir)
    shutil.copytree(Local, NASdir)
    print("Transmitted")
  except shutil.Error as e:
    print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
  except OSError as e:
    print('Directory not copied. Error: %s' % e)
 
#--------------------------------


init()
