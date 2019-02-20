# -*- coding: utf-8 -*-
#!/usr/bin/python3
'''
from werkzeug.debug import DebuggedApplication
from myapp import app
app = DebuggedApplication(app, evalex=True)
'''
from flask import Flask, render_template
import numpy as np
import csv
import pandas
import pickle
from sklearn.linear_model import LinearRegression
from time import strftime
import time
import io
# from io import StringIO

app = Flask(__name__)
NasDIR = '/home/pi/mnt/Nas/Timble Data.csv'
HarrogateModel='/home/pi/Documents/WeatherStation/Harrogate model.sav'
# NasDIR = '//mpd-ds/WeatherStation/Timble Data.csv'

@app.route("/")
def homepage():
        # read the log file from the NAS
        outputhtml=""
        TD = strftime("%H:%M:%S on %d-%m-%y")
        # datacsv=io.open(NasDIR,'rb')

        with open(NasDIR,'rb') as NAS:
               Naslines = NAS.readlines()
               NAS.close()
        # deconstruct last line into useful components
        logdate=np.genfromtxt(Naslines[-1:],delimiter=',',usecols=0,dtype=str)
        logdata=np.genfromtxt(Naslines[-1:],delimiter=',',usecols=(1,2,3,4,5,6),dtype=float)
        currstats=logdata.reshape(1,6)

        # load the model, and use it to predict the future temp
        loaded_model = pickle.load(open(HarrogateModel, 'rb'))
        result = loaded_model.predict(currstats)
        result = "{:3.1f}".format(result[0])
        # construct the HTML output from all the data gathered
        outputhtml = outputhtml + "<h2>Current time is: "+TD+"</h2>"
        outputhtml = outputhtml + "The last log readings were from: " + str(logdate) + "</p>"
        outputhtml = outputhtml + "<table border=""1"">"
        outputhtml = outputhtml + "<tr><th>Temperature</p>(°C)</th><th>Pressure</p>(mb)</th><th>Humidity</p>(??)</th><th>Change in</p>Temp (°C)</th><th>Change in</p>Press (mb)</th><th>Change in</p>Humidity (??)</th></tr>"
        outputhtml = outputhtml + "<tr><th>"+str(logdata[0])+"</th><th>"+str(logdata[1])+"</th><th>"+str(logdata[2])+"</th><th>"+str(logdata[3])+"</th><th>"+str(logdata[4])+"</th><th>"+str(logdata[5])+"</th></tr>"
        outputhtml = outputhtml + "</table>"
        outputhtml = outputhtml + "<h1>Using this data in the model - gives a predicted temperature for the next hour of " + result + "°C</h1>"
        return(outputhtml)

if __name__ == '__main__':
   app.run(debug=True,port=80,host='0.0.0.0')
