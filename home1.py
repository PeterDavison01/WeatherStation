# Libraries
# --------------------------------
import time
from time import strftime
import os
from sense_hat import SenseHat
import csv
import shutil
import distutils
from distutils import dir_util
import numpy as np

# --------------------------------
# Variables
NasDIR = '/home/pi/mnt/Nas/Timble Data.csv'

# --------------------------------
# Main
def main():
  # Read the SenseHat Sensors
  sense = SenseHat()
  temp = (round(sense.get_temperature()))
  pressure = (round(sense.get_pressure()))
  humidity = (round(sense.get_humidity()))

  # Calculate the changes from the last read
  try:
    with open(NasDIR, 'rb') as NAS:
      Naslines = NAS.readlines()
      NAS.close()
  except IOError:
    print("Could not read file:", NasDIR)

  lastline = np.genfromtxt(Naslines[-1:], delimiter=',')
  d_temp = (temp) - (lastline[1])
  d_pressure = (pressure) - (lastline[2])
  d_humidity = (humidity) - (lastline[3])

  # write the data to the NAS
  fields = [strftime("%y-%m-%d %H:%M:%S"), temp, pressure, humidity, d_temp, d_pressure, d_humidity]
  try:
    with open(NasDIR, 'a') as NASTimble:
      writer = csv.writer(NASTimble)
      writer.writerow(fields)
      NASTimble.close()
  except:
    print("Could not write to file:", NasDIR)
# --------------------------------

main()
