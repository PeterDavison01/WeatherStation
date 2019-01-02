import csv
from time import strftime

now = strftime("%d-%m-%y")
dir = "/home/pi/WeatherData/"
path = dir + "Timble.csv"

with open(path, 'r') as csv:
  for row in csv:
    print(row)
