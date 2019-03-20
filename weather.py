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
import pygal
from pygal.style import Style
# from io import StringIO

app = Flask(__name__)
NasDIR = '/mnt/Nas/Timble Data.csv'
HarrogateModel='/home/pi/WeatherStation/Harrogate model.sav'
chartHTML = '/Templates/chart.html'


@app.route("/")
def homepage():
        # read the log file from the NAS
        outputhtml=""
        TD = strftime("%d-%m-%y %H:%M:%S")
        NAS=open(NasDIR,'rb')

        try:
                        Naslines = NAS.readlines()
        except IOError:
                        print ("Could not read file:", NasDIR)
        finally:
                        NAS.close()

        # deconstruct last line into useful components
        logdate=np.genfromtxt(Naslines[-24:],delimiter=',',usecols=0,dtype=str)
        logdata=np.genfromtxt(Naslines[-24:],delimiter=',',usecols=(1,2,3,4,5,6),dtype=float)
        curr_logdate=logdate[-1:]
        curr_logdata=logdata[-1:]
        currstats=curr_logdata.reshape(1,6)

        # load the model, and use it to predict the future temp
        try:
                loaded_model = pickle.load(open(HarrogateModel, 'rb'))
                result = loaded_model.predict(currstats)
                result = "{:3.1f}".format(result[0])
        except (AttributeError, EOFError, ImportError, IndexError) as e:
                # secondary errors
                print(traceback.format_exc(e))

        # create the line graphs of temp, pressure and humdity
        pressdata=logdata[:,1]
        press_chart = pygal.Line(x_label_rotation=45,y_title="Pressure (mb)",show_legend=False)
        press_chart.x_labels=logdate
        press_chart.add('Pressure', pressdata)

        humiditydata=logdata[:,2]
        humidity_chart = pygal.Line(x_label_rotation=45,y_title="Humidity",show_legend=False)
        humidity_chart.x_labels=logdate
        humidity_chart.add('Humidity', humiditydata)

        logdate=np.append(logdate,str(TD))
        tempdata=logdata[:,0]
        tempdata2=np.append(tempdata,float(result))
        custom_style = Style(colors=('blue','red'))
        temp_chart = pygal.Line(x_label_rotation=45,y_title="Temp (C)",show_legend=False,style=custom_style)
        temp_chart.x_labels=logdate
        temp_chart.add('Prediction', tempdata2)
        temp_chart.add('Temp', tempdata)

        # construct the HTML output from all the data gathered
        outputhtml = """
        <html>
                <head>
                        <title>%s</title>
                </head>
                <body>
                        <h1>We predict temperature for the next hour will be %s°C</h1>
                        <h3>Current time is: %s</h3>
                        %s%s%s
                </body>
        </html>
        """ % ("Timble Weather",result,TD,temp_chart.render(),press_chart.render(),humidity_chart.render())
        return(outputhtml)


if __name__ == '__main__':
        # app.run()
        app.run(debug=True,port=8082,host='192.168.16.25')


