#!/usr/bin/python
# LEED library Version 0.1    (July 2019 @ WFW)
#
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy import optimize, interpolate
from datetime import datetime
from datetime import timedelta
from matplotlib.transforms import offset_copy
# from pylab import figure
from matplotlib.pyplot import figure
import cv2
import os

def offset(ax, x, y):
    return offset_copy(ax.transData, x=x, y=y, units='dots')

def LEED_elog_Dictionary(file, path):
    spec = LEED(file,datapath=path)
    dic = {'Category':'LEED', 'Type':'LEED', 'Substrate':'as before', 
        'Summary':spec.energy+' eV', 
        'Temperature':'', 'File':str(file), 
        'Scan_Range':'', 'Energy':spec.energy,
        'N_channels':'', 'MDate':spec.startTimeEpoch, 
        'Author':'Python Script'}
    return dic

class LEED:
    """This class handles LEED data and their plotting."""
    path = "./"
    def __init__(self, _filename, datapath=path):
        self.datapath = datapath
        self.readDataFile(_filename)

    def readDataFile(self, _filename):
        # if _filename.find(".") == -1:
        #     _filename +=".aes"
        self.filename = _filename
        self.fname = self.filename[0:self.filename.find(".")]
        import glob
        f = glob.glob(self.datapath+"**/"+self.filename, recursive=True)
        if len(f) == 0:
            print('Error: No files found!')
            print('Not found:',self.filename)
            return
        f = glob.glob(self.datapath+"**/"+self.filename, recursive=True)[0]
        self.datapath = os.path.dirname(f)
        self.startTime = datetime.fromtimestamp(os.path.getmtime(f))        # Only the file saving time
        self.startTimeEpoch = os.path.getmtime(f)
        match = re.search(r"\_(\d*)eV",self.fname)
        self.energy = match.group(1)
        self.picture = cv2.imread(f)

    def __str__(self):
        return self.datapath+self.filename

    def info(self):
        print("filename: \t\t",self.filename)
        print("datapath: \t\t",self.datapath)
        print("startTime: \t\t",self.startTime)
        print("energy: \t\t",self.energy)
        print('--------')

    def plot(self):
        new_pic = self.picture
        # Pmin = min(new_pic.all())
        # Pmax = max(new_pic.any())
        # new_pic = (new_pic-Pmin)/(Pmax-Pmin)*255
        cv2.imshow('LEED'+self.fname,new_pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    path = 'D:\Data\Python\LEED'
    d1 = LEED("190122_L_01_42eV.tif",datapath=path)
    
    d1.info()
    d1.plot()
    
    import code
    code.interact(local=locals())
