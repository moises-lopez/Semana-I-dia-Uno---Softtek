# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:32:46 2019

@author: cyber
"""

import glob
import math
from pathlib import Path
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
import os


def transformCordinates(x, y, angle, wmax, hmax):    
    if angle !=math.pi/2:
        yn=int(y-hmax*math.sin(((math.pi)/2)-angle)/2)
        xn=int(x-hmax*math.cos(((math.pi)/2)-angle)/2)
        wmaxn=int(hmax*math.cos(((math.pi)/2)-angle))
        hmaxn=int(hmax*math.sin(((math.pi)/2)-angle))
    else:
        yn=int(y-hmax/2)
        xn=int(x-wmax/2)
        hmaxn=int(hmax)
        wmaxn=int(wmax)   
    
    return xn,yn,wmaxn,hmaxn,angle
def Check (xn,yn,wmaxn,hmaxn,hn,wn):
    if (xn+wmaxn<wn) and (yn+hmaxn<hn):
        return xn,yn,wmaxn,hmaxn,hn,wn
    elif (xn+wmaxn>wn):
        wmaxn=(xn+wmaxn-wn)
        return xn,yn,wmaxn,hmaxn,hn,wn
    elif (yn+hmaxn>hn):
        hmaxn=(yn+hmaxn-hn)
        return xn,yn,wmaxn,hmaxn,hn,wn
    else:
        wmaxn=(xn+wmaxn-wn)
        hmaxn=(yn+hmaxn-hn)
        return xn,yn,wmaxn,hmaxn,hn,wn
    
def stringsToArray(stringArray):
    result = []
    stringArrayLength = len(stringArray)
    for i in range(0, stringArrayLength):
        s = ''
        stringLength = stringArray[i]
        
    
    
def pdToXml(name, coordinates, size, img_folder):
    xml = ['<annotation>']
    xml.append("    <folder>{}</folder>".format(img_folder))
    xml.append("    <filename>{}</filename>".format(name))
    xml.append("    <source>")
    xml.append("        <database>Unknown</database>")
    xml.append("    </source>")
    xml.append("    <size>")
    xml.append("        <width>{}</width>".format(size["width"]))
    xml.append("        <height>{}</height>".format(size["height"]))
    xml.append("        <depth>3</depth>".format())
    xml.append("    </size>")
    xml.append("    <segmented>0</segmented>")

    for field in coordinates:
        xmin, ymin = max(0,field[0]), max(0,field[1])
        xmax = min(size["width"], field[0]+field[2])
        ymax = min(size["height"], field[1]+field[3])

        xml.append("    <object>")
        xml.append("        <name>Face</name>")
        xml.append("        <pose>Unspecified</pose>")
        xml.append("        <truncated>0</truncated>")
        xml.append("        <difficult>0</difficult>")
        xml.append("        <bndbox>")
        xml.append("            <xmin>{}</xmin>".format(int(xmin)))
        xml.append("            <ymin>{}</ymin>".format(int(ymin)))
        xml.append("            <xmax>{}</xmax>".format(int(xmax)))
        xml.append("            <ymax>{}</ymax>".format(int(ymax)))
        xml.append("        </bndbox>")
        xml.append("    </object>")
    xml.append('</annotation>')
    return '\n'.join(xml)

def generateArray(file):
    with open(file, "r") as f:
        arr = f.read().splitlines()
    
    arr_len = len(arr)
    i = 0    
    # regex
    rg = re.compile("(\d)*_(\d)*_(\d)*_big")
    output = []
    
    while i != arr_len:
        val = arr[i] # nombre de la imagen
        mtch = rg.match(val)
        if mtch:
            try:
                di = dict() #diccionario
                val = "{}.jpg".format(val)
                di["name"] = val
                #  matplotlib
                img = mpimg.imread(os.path.join("dataset", val))
                
                (h, w, _) = img.shape
                
                fig,ax=plt.sublots(1)
                ax.imshow(img)
                
                jumps = int(arr[i+1])
                temp = []
                for j in range(0, jumps):
                    coords = arr[i + j +2]
                    temp.append(coords)
                    # transformCordinates(string, w, h)
                    rect=patches.Rectangle(
                        (rec[0],rec[1]),rec[2],rec[3],
                        linewidth=1,
                        edgecolor='r',
                        facecolor='none')
                    ax.add_patch(rect)
                plt.show()
                di["annotations"] = temp
                
                output.append(di)
                disize=dict()
                disize["height","width"]=h,w
                di["size"]=disize
                
                
            except:
                print("{} not found...".format(val))
                i+=1
              
        else:
            i+=1
            
   

def returnEllipseListFiles(path):
    return [str(f) for f in Path(path).glob('**/*-ellipseList.txt')]

folder = glob.glob("dataset/*.jpg")
folder = pd.Series(folder)
files = returnEllipseListFiles("labels")
dictionary=[generateArray(f) for f in files]
