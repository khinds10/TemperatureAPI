#!/usr/bin/python
import os, sys, re, json
from flask import Flask, request
from flask_cors import CORS
from PIL import Image
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
dirPath = os.path.dirname(os.path.realpath(__file__))

def rgbOfPixel(img_path, x, y):
    """for given image path, get the color at the x,y coords"""
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

def getHexForColor(temperature, gradientImageFile):
    """get HEX code for given color"""    
    try:    
        temperature = temperature * 10
        if temperature > 999:
            temperature = 999
        if temperature < 0:
            temperature = 0
        color = rgbOfPixel(dirPath + gradientImageFile, temperature, 5)
        return '#%02x%02x%02x' % color
    except:
        return '#ffffff'

@app.route("/")
def getTemperatureColor():
    """get temperature to generate the HEX color"""    
    temperature = int(request.args.get('temperature'))
    return getHexForColor(int(temperature), '/temp.png') 

@app.route("/neopixel")
def getTemperatureColorNeoPixel():
    """get temperature to generate the HEX color for neopixel color scheme"""
    temperature = int(request.args.get('temperature'))
    return getHexForColor(int(temperature), '/neopixel.png')

@app.route("/humidity")
def getHumidityColor():
    """get humidity to generate the HEX color"""    
    humidity = int(request.args.get('humidity'))
    return getHexForColor(int(humidity), '/humidity.png')

@app.route("/precipitation")
def getPrecipitationColor():
    """get humidity to generate the HEX color"""    
    humidity = float(request.args.get('precipitation'))
    return getHexForColor(int(humidity), '/precipitation.png')

@app.route("/multiple-humidity")
def getMultipleHumidityColors():
    """get humidity to generate the HEX color from a comma separated list"""
    humidities = request.args.get('humidities')
    humidities = re.split(',', humidities)

    # for all the given temperatures return as a JSON array
    humidityResults = []
    for humidity in humidities:
        humidityResults.append(getHexForColor(int(humidity), '/humidity.png'))
    return json.dumps(humidityResults)

@app.route("/multiple")
def getMultipleTemperatureColors():
    """get temperature to generate the HEX color from a comma separated list"""
    temperatures = request.args.get('temperatures')
    temperatures = re.split(',', temperatures)

    # for all the given temperatures return as a JSON array
    temperatureResults = []
    for temperature in temperatures:
        temperatureResults.append(getHexForColor(int(temperature), '/temp.png'))
    return json.dumps(temperatureResults)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response

# run the flask python API
if __name__ == "__main__":
    app.run()
