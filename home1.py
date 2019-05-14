# Libraries
# --------------------------------
import time
from time import strftime
from sense_hat import SenseHat
import csv
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

  # Calculate the changes from the last read
  NAS = open(NasDIR, 'rb')
  try:
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
  NAS=open(NasDIR, 'a')
  try:
      writer = csv.writer(NAS)
      writer.writerow(fields)
  except:
    print("Could not write to file:", NasDIR)
  finally:
    NAS.close()

  #NASTimble.close()
# --------------------------------

main()
