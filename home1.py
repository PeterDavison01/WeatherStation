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
now = strftime("%d-%m-%y")
dir = "/home/pi/WeatherData/"
path = dir + now
#--------------------------------


#SenseHat Sensors
#--------------------------------
def sensors():
  sense = SenseHat()
  temp = str(round(sense.get_temperature()))
  humidity = str(round(sense.get_humidity()))
  pressure = str(round(sense.get_pressure()))
  global temp
  global humidity
  global pressure
#--------------------------------
  
  
#Transmission
#--------------------------------
#--------------------------------
  
  
#Main
#--------------------------------
def main():
  sensors()
  global count
  fields = [temp,pressure,humidity]
  while True:
    if count == 2:
      with open(path, 'ab') as data:
        writer = csv.write(data)
        writer.writerow(fields)
        data.close()
        count = 0
        break
    else:
      time.sleep(1)
      count = count + 1
      print(count)
#--------------------------------

main()
