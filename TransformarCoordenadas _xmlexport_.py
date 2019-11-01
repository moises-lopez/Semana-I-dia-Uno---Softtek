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


def Check (x,y,wmax,hmax,h,w):
    if ((x+wmax)<=w) and ((y+hmax)<=h):
        return x,y,wmax,hmax
    elif ((x+wmax)>w):
        wmax=(x+wmax-w)
        return x,y,wmax,hmax
    elif ((y+hmax)>h):
        hmax=(y+hmax-h)
        return x,y,wmax,hmax
    elif (x+wmax>w) or (y+hmax>h):
        wmax=(x+wmax-w)
        hmax=(y+hmax-h)
        return x,y,wmax,hmax
    
def transformCordinates(x,y,angle,wmax,hmax):
    if angle !=math.pi/2:
        yn=float(y-wmax*math.sin(angle))
        xn=float(x-hmax*math.sin(angle))
        wmaxn=float(2*hmax*math.sin((angle)))
        hmaxn=float(2*wmax*math.sin((angle)))
    else:
        yn=float(y-hmax/2)
        xn=float(x-wmax/2)
        hmaxn=float(hmax)
        wmaxn=float(wmax)   
    return [xn,yn,wmaxn,hmaxn]

    
def pdToXml(name, coordinates, size, img_folder):
    #print(name, coordinates, size, img_folder)
    #print(size["width"])
    #print(size["height"])
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
        #print(type(field))
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
    #print(xml)
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
        val = arr[i]# nombre de la imagen
        mtch = rg.match(val)
        if mtch:
            try:
                di = dict() #diccionario
                val = "{}.jpg".format(val)
                di["name"] = val
                #  matplotlib
                img = mpimg.imread(os.path.join("dataset", val))
                fig,ax = plt.subplots(1)
                ax.imshow(img)               
                (h, w, _) = img.shape
                jumps = int(arr[i+1])
                temp = []
                auxrec = []
                for j in range(0, jumps):
                    coords = arr[i + j +2]
                    #print(coords)
                    temp.append(coords)
                    coords = coords.split()      #Cambié de orden las dos primeras con las dos últimas
                    rec = transformCordinates(float(coords[3]),float(coords[4]),float(coords[2]),float(coords[0]),float(coords[1]))
                    auxrec.append(rec)
                    rect = patches.Rectangle(
                        (rec[0],rec[1]),rec[2],rec[3],
                        linewidth=1,
                        edgecolor='r',
                        facecolor='none')
                    ax.add_patch(rect)
                #plt.show()
                 
                #print(auxrec)
                di["annotations"] = temp
                size = dict()
                size["width"] = w
                size["height"] = h
                di["size"] = size
                #auxArr2 = [[100, 100, 100, 100]]
                #print("test")
                xmltext = pdToXml(val, auxrec, size, "images")
                f = open (arr[i]+".xml","w")
                f.write(xmltext)
                f.close()
                i+=1
            except:
                #path1 = 'C:/Users/Moisés/semanai 2/dirty_dataset/dataset'
                #path3 = arr[i] + ".jpg"
                #path2 = os.path.join(path1, path3)
                #os.remove(arr[i] + ".jpg")
                #path = "./"+arr[i]+".jpg"
                #os.remove(path)
                #print("removing...")
                #print("{} not found...".format(val))
                i+=1
              
        else:
            i+=1




def returnEllipseListFiles(path):
    return [str(f) for f in Path(path).glob('**/*-ellipseList.txt')]

folder = glob.glob("dataset/*.jpg")
folder = pd.Series(folder)
files = returnEllipseListFiles("labels")
[generateArray(f) for f in files]