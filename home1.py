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
NasDIR = '/mnt/Nas/Timble Data.csv'

# --------------------------------
# Main
def main():
  # Read the SenseHat Sensors
  sense = SenseHat()
  temp = (round(sense.get_temperature()))
  pressure = (round(sense.get_pressure()))
  humidity = (round(sense.get_humidity()))
  Naslines = str
  NAS = ""
  NASTimble = ()

  # Calculate the changes from the last read
  try:
    with open(NasDIR, 'rb') as NAS:
      Naslines = NAS.readlines()
  except IOError:
    print("Could not read file:", NasDIR)
  finally:
    NAS.close()  

  lastline = np.genfromtxt(Naslines[-1:], delimiter=',')
  d_temp = (temp) - (lastline[1])
  d_pressure = (pressure) - (lastline[2])
  d_humidity = (humidity) - (lastline[3])

  # write the data to the NAS
  fields = [strftime("%d-%m-%Y %H:%M:%S"), temp, pressure, humidity, d_temp, d_pressure, d_humidity]
  try:
    with open(NasDIR, 'a') as NASTimble:
      writer = csv.writer(NASTimble)
      writer.writerow(fields)
  except:
    print("Could not write to file:", NasDIR)
  finally:
    NASTimble.close()
# --------------------------------

main()
