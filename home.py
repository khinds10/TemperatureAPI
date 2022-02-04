#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, urllib2, json
import numpy as np
import cv2 as cv
from PIL import Image
import numpy as np
import settings
dirPath = os.path.dirname(os.path.realpath(__file__))

# create a list of all the home environment devices
houseEnvironmentDevices = []
font = cv.FONT_HERSHEY_SIMPLEX

# get current forecast from current location
weatherInfo = json.loads(urllib2.urlopen(settings.weatherAPIURL).read())
currentConditions = weatherInfo['current']
apparentTemperature = int(currentConditions['feels_like'])
currentHumidity = currentConditions['humidity']

def addDevice(deviceName):
    """add a home environment device, append it to the master list to show temps"""
    deviceConditions = []
    deviceData = urllib2.urlopen(settings.deviceLoggerAPI + "/api/read?device=" + deviceName).read()
    deviceData = json.loads(deviceData)
    deviceConditions.append(deviceData[0]['value1'])
    deviceConditions.append(deviceData[0]['value2'])    
    houseEnvironmentDevices.append(deviceConditions)

def rgbOfPixel(img_path, x, y):
    """for given image path, get the color at the x,y coords"""
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

def hexToRgb(hex):
    """for hex get the RGB tuple for Python OpenCV"""
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

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

# add home devices
addDevice('temp-check-basement')
addDevice('weather-clock-small-white')
addDevice('temp-check-living')
addDevice('weather-clock-white')
addDevice('weather-clock-yellow')
addDevice('weather-clock-red')
addDevice('temp-check-attic')

# image width: 540px  height: 598px
img = cv.imread(dirPath + '/house-orig.jpg')

# basement
tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[0][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[0][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[0][0] + "*", (220, 525), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[0][1] + "%", (285, 525), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

# main floor
tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[1][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[1][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[1][0] + "*", (105, 395), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[1][1] + "%", (170, 395), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[2][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[2][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[2][0] + "*", (320, 395), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[2][1] + "%", (385, 395), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

# 2nd floor
tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[3][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[3][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[3][0] + "*", (50, 270), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[3][1] + "%", (115, 270), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[4][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[4][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[4][0] + "*", (215, 270), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[4][1] + "%", (280, 270), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[5][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[5][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[5][0] + "*", (375, 270), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[5][1] + "%", (440, 270), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

tempColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[6][0]), '/temp.png'))
humidityColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[6][1]), '/humidity.png'))
cv.putText(img,houseEnvironmentDevices[6][0] + "*", (205, 150), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + houseEnvironmentDevices[6][1] + "%", (270, 150), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

pt1 = (270, 40)
pt2 = (90, 192)
pt3 = (450, 192)
triangle_cnt = np.array( [pt1, pt2, pt3] )
cv.drawContours(img, [triangle_cnt], 0, (0,0,0), 0)

# show outside temperature
tempColor = hexToRgb(getHexForColor(apparentTemperature, '/temp.png'))
humidityColor = hexToRgb(getHexForColor(currentHumidity, '/humidity.png'))
cv.putText(img,str(apparentTemperature) + "*", (395, 50), font, 1, (tempColor[2],tempColor[1],tempColor[0]), 2)
cv.putText(img,"" + str(currentHumidity) + "%", (460, 50), font, 0.65, (humidityColor[2],humidityColor[1],humidityColor[0]), 2)

# write the image and move it to the clock tablet webroot
cv.imwrite(dirPath + "/house.jpg", img)
os.rename(dirPath + "/house.jpg", settings.clockTabletImageRoot + "house.jpg")
