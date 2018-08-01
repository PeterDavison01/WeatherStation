#Libraries
#--------------------------------
import time
from time import strftime
import os
from sense_hat import SenseHat
import csv
#--------------------------------


#Variables
#--------------------------------
count = 0
dir = "/mnt/Nas/"
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
  path = (dir + strftime("%d-%m-%y")+".csv")
  print(path)
  global count
  emptycell = ""
  fields = [strftime("%H:%M:%S"),emptycell,temp,pressure,humidity]
  while True:
    if count == 5:
      with open(path, 'a') as data:
        writer = csv.writer(data)
        writer.writerow(fields)
        data.close()
        count = 0
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
      print("Data uploaded.")
    except:
      print("Error. Retrying in 5 seconds")
      time.sleep(5)
      count = 0
      continue
#--------------------------------

init()
