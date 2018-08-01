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
nowdate = strftime("%d-%m-%y")
dir = "/mnt/Nas/"
path = (dir + nowdate+".csv")
hour = strftime("%H")
min = strftime("%M")
sec = strftime("%S")
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

  
#Main
#--------------------------------
def main():
  sensors()
  global count
  ctime = (hour+":"+min+":"+sec)
  emptycell = ""
  fields = [ctime,emptycell,temp,pressure,humidity]
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
      print(count)
#--------------------------------

while True:
  main()
