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
weatherInfo = json.loads(urllib2.urlopen(settings.weatherAPIURL + settings.weatherAPIKey + '/' + str(settings.latitude) + ',' + str(settings.longitude) + '?lang=en').read())
currentConditions = weatherInfo['currently']
apparentTemperature = int(currentConditions['apparentTemperature'])

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

def getHexForColor(temperature):
    """get HEX code for given color"""    
    try:    
        temperature = temperature * 10
        if temperature > 999:
            temperature = 999
        if temperature < 0:
            temperature = 0
        color = rgbOfPixel(dirPath + '/temp.png', temperature, 5)
        return '#%02x%02x%02x' % color
    except:
        return '#ffffff'

# add home devices
addDevice('weather-clock-gray')
addDevice('weather-clock-small-white')
addDevice('weather-clock')
addDevice('weather-clock-white')
addDevice('weather-clock-yellow')
addDevice('weather-clock-red')

# image width: 540px  height: 598px
img = cv.imread(dirPath + '/house-orig.jpg')

# basement
hexColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[0][0])))
img = cv.rectangle(img, (60,450), (480,570), (0,0,0), 0)
cv.putText(img,houseEnvironmentDevices[0][0] + "*", (230, 525), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

# main floor
hexColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[1][0])))
img = cv.rectangle(img, (60,320), (242,440), (0,0,0), 0)
cv.putText(img,houseEnvironmentDevices[1][0] + "*", (125, 395), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

hexColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[2][0])))
img = cv.rectangle(img, (250,320), (480,440), (0,0,0), 0)
cv.putText(img,houseEnvironmentDevices[2][0] + "*", (340, 395), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

# 2nd floor
hexColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[3][0])))
img = cv.rectangle(img, (60,200), (200,310), (0,0,0), 0)
cv.putText(img,houseEnvironmentDevices[3][0] + "*", (110, 270), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

hexColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[4][0])))
img = cv.rectangle(img, (208,200), (338,310), (0,0,0), 0)
cv.putText(img,houseEnvironmentDevices[4][0] + "*", (250, 270), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

hexColor = hexToRgb(getHexForColor(int(houseEnvironmentDevices[5][0])))
img = cv.rectangle(img, (346,200), (478,310), (0,0,0), 0)
cv.putText(img,houseEnvironmentDevices[5][0] + "*", (385, 270), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

# attic (temporary +10 for now)
atticTemp = apparentTemperature + 10
hexColor = hexToRgb(getHexForColor(atticTemp))
pt1 = (270, 40)
pt2 = (90, 192)
pt3 = (450, 192)
triangle_cnt = np.array( [pt1, pt2, pt3] )
cv.drawContours(img, [triangle_cnt], 0, (0,0,0), 0)
cv.putText(img,str(atticTemp) + "*", (240, 150), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

# show outside temperature
hexColor = hexToRgb(getHexForColor(apparentTemperature))
cv.putText(img,str(apparentTemperature) + "*", (395, 50), font, 1, (hexColor[2],hexColor[1],hexColor[0]), 2)

# write the image and move it to the clock tablet webroot
cv.imwrite(dirPath + "/house.jpg",img)
os.rename(dirPath + "/house.jpg", settings.clockTabletImageRoot + "house.jpg")
