# -*- coding: utf-8 -*-
#!/usr/bin/python3
'''
from werkzeug.debug import DebuggedApplication
from myapp import app
app = DebuggedApplication(app, evalex=True)
'''
from flask import Flask, render_template, Markup
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
NasDIR = '/mnt/Nas/Timble Data.csv'
HarrogateModel='/home/pi/WeatherStation/Harrogate model.sav'
# NasDIR = '//mpd-ds/WeatherStation/Timble Data.csv'

@app.route("/")
def homepage():
        # read the log file from the NAS
        outputhtml=""
        TD = strftime("%H:%M:%S on %d-%m-%y")
        NAS=open(NasDIR,'rb')

        try:
                Naslines = NAS.readlines()
        except IOError:
                print ("Could not read file:", NasDIR)
        finally:
                NAS.close()

        # deconstruct last line into useful components
        logdate=np.genfromtxt(Naslines[-1:],delimiter=',',usecols=0,dtype=str)
        logdata=np.genfromtxt(Naslines[-1:],delimiter=',',usecols=(1,2,3,4,5,6),dtype=float)
        currstats=logdata.reshape(1,6)

        # load the model, and use it to predict the future temp
        try:
                loaded_model = pickle.load(open(HarrogateModel, 'rb'))
                result = loaded_model.predict(currstats)
                result = "{:3.1f}".format(result[0])
        except (AttributeError, EOFError, ImportError, IndexError) as e:
                # secondary errors
                print(traceback.format_exc(e))


        # construct the HTML output from all the data gathered
        outputhtml = outputhtml + "<h2>Current time is: "+TD+"</h2>"
        outputhtml = outputhtml + "The last log readings were from: " + str(logdate) + "</p>"
        outputhtml = outputhtml + "<table border=""1"">"
        outputhtml = outputhtml + "<tr><th>Temperature</p>(°C)</th><th>Pressure</p>(mb)</th><th>Humidity</p>(Pa)</th><th>Change in</p>Temp (°C)</th><th>Change in</p>Press (mb)</th><th>Change in</p>Humidity (Pa)</th></tr>"
        outputhtml = outputhtml + "<tr><th>"+str(logdata[0])+"</th><th>"+str(logdata[1])+"</th><th>"+str(logdata[2])+"</th><th>"+str(logdata[3])+"</th><th>"+str(logdata[4])+"</th><th>"+str(logdata[5])+"</th></tr>"
        outputhtml = outputhtml + "</table>"
        outputhtml = outputhtml + "<h1>Using this data in the model - gives a predicted temperature for the next hour of " + result + "°C</h1>"
        outputhtml = outputhtml + " "
#        outputhtml = outputhtml + "<div><img src='{{ graph }}'></img></div>"
        return(outputhtml)

if __name__ == '__main__':
        app.run(debug=True,port=5000,host='0.0.0.0')

