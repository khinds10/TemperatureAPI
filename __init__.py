#!/usr/bin/python
import os, sys, re, json
from flask import Flask
from flask import request
from PIL import Image
app = Flask(__name__)
dirPath = os.path.dirname(os.path.realpath(__file__))

def rgb_of_pixel(img_path, x, y):
    """for given image path, get the color at the x,y coords"""
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

def getHexForColor(temperature):
    """get HEX code for given color"""    
    try:    
        temperature = temperature * 10
        if temperature > 999:
            temperature = 999
        if temperature < 0:
            temperature = 0
        color = rgb_of_pixel(dirPath + '/temp.png', temperature, 5)
        return '#%02x%02x%02x' % color
    except:
        return '#ffffff'
        
@app.route("/")
def getColor():
    """get temperature to generate the HEX color"""    
    temperature = int(request.args.get('temperature'))
    return getHexForColor(temperature) 

@app.route("/multiple")
def getMultipleColors():
    """get temperature to generate the HEX color from a comma separated list"""
    temperatures = request.args.get('temperatures')
    temperatures = re.split(',', temperatures)

    # for all the given temperatures return as a JSON array
    temperatureResults = []
    for temperature in temperatures:
        temperatureResults.append(getHexForColor(int(temperature)))
    return json.dumps(temperatureResults)
        
# run the flask python API
if __name__ == "__main__":
    app.run()
