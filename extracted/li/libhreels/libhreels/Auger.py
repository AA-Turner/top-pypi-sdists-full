#!/usr/bin/python
# Auger library Version 0.1    (December 2018 @ WFW)
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
import os

def offset(ax, x, y):
    return offset_copy(ax.transData, x=x, y=y, units='dots')

def Auger_elog_Dictionary(file, path):
    spec = Auger(file,datapath=path)
    dic = {'Category':'Auger', 'Type':'Auger', 'Substrate':'as before', 
        'Summary':'%5.0f'% spec.xmin +'-'+'%-5.0f'% spec.xmax, 
        'Temperature':'', 'File':str(file), 
        'Scan_Range':'%5.0f'% spec.xmin +','+'%5.0f'% spec.xmax, 
        'N_channels':'%4d'%spec.totalTime, 'MDate':spec.startTimeEpoch, 
        'Author':'Python Script'}
    return dic

class Auger:
    """This class handles Auger data and their plotting."""
    path = "./"
    def __init__(self, _filename, datapath=path):
        self.datapath = datapath
        self.readDataFile(_filename)
        self.Auger = interpolate.interp1d(self.xdata, self.ydata, kind='linear')
        # self.Auger = interp1d(self.xdata, self.ydata, kind='nearest')

    def readDataFile(self, _filename):
        # if _filename.find(".") == -1:
        #     _filename +=".aes"
        self.filename = _filename
        # self.fname = self.filename[0:self.filename.find(".")]
        self.fname = _filename
        xdata = []
        ydata = []
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
        with open(f, 'r') as f:
            for line in f:
                str_x, str_d, str_y = line.split()
                # print(str_x, str_y)
                try:
                    xdata.append(float(str_x))
                    ydata.append(float(str_y))
                except:
                    xdata.append(float(str_x.replace(",",".")))
                    ydata.append(float(str_y.replace(",",".")))
        self.xdata = np.array(xdata)
        self.ydata = np.array(ydata)
        self.xmin = self.xdata[0]
        self.xmax = self.xdata[-1]
        self.deltay = max(ydata)-min(ydata)
        self.ymax = max(ydata)
        self.totalTime = 1.0 * len(self.xdata)
        self.marker = []
        self.valid = True


    def __str__(self):
        return self.datapath+self.filename

    def info(self):
        print("filename: \t\t",self.filename)
        print("datapath: \t\t",self.datapath)
        print("startTime: \t\t",self.startTime)
        print("xmin: \t\t\t","%6.1f"%self.xmin,"eV")
        print("xmax: \t\t\t","%6.1f"%self.xmax,"eV")
        if len(self.marker)>0:
            print("marker: \t\t")
            for each in self.marker:
                print("\t\t%6.1f\t %8.1f"%each)
        print('--------')

    def infoText(self):
        langtext = "filename: \t\t"+self.filename+'\n'
        langtext +="datapath: \t\t"+self.datapath+'\n'
        langtext +="startTime: \t\t"+str(self.startTime)+'\n'
        langtext +="xmin: \t\t\t"+"%6.1f"%self.xmin+" eV"+'\n'
        langtext +="xmax: \t\t\t"+"%6.1f"%self.xmax+" eV"+'\n'
        if len(self.marker)>0:
            langtext +="marker: \t\t"+'\n'
            for each in self.marker:
                langtext +="\t\t%6.1f\t %8.1f"%each+'\n'
        langtext +='--------'
        return langtext


    def findIndex(self, kinEnergy):
        for i in range(len(self.xdata)):
            if self.xdata[i] > kinEnergy: 
                return i
        print('Auger.findIndex: kinEnergy', kinEnergy, 'not found in xdata')
        return len(self.xdata)-1

    def plot(self, xmin=None, xmax=None, label='x', color="b-",marker=True, offset=0.):
        ''' plot(self, xmin=None, xmax=None,  label='x', normalized=False, color="b-",marker=True,offset=0.)'''
        if xmin:
            nstart = self.findIndex(xmin)
        else:
            nstart = 0
        if xmax:
            nend = self.findIndex(xmax)
        else:
            nend = len(self.xdata)
        if label == "x":
            label = self.filename
        plt.plot(self.xdata[nstart:nend], self.ydata[nstart:nend]+offset, color, label=label)
        plt.xlabel('Kinetic Energy (eV)')
        plt.ylabel('dN/dE (arb. u.)')
        plt.legend()
        if marker:
            for (x,y) in self.marker:
                self.setMarker(x,y)
        return

    def pickMarker(self):
        def onclick(event):
            # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #     ('double' if event.dblclick else 'single', event.button,
            #     event.x, event.y, event.xdata, event.ydata))
            if event.button ==1:
                self.marker.append((event.xdata, event.ydata))
                self.setMarker(event.xdata, event.ydata)
                self.fig.canvas.draw()
            else:
                self.marker = []
                print("All marker deleted!")
                self.fig.canvas.draw()
        self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.ax.set_title('Pick marker with left mouse button ... (right:erase all)')

    def figure(self):
        self.fig=figure()
        self.ax=self.fig.add_subplot(111)

    def show(self):
        plt.show()

    def selectData(self,x1, x2=None):
        """Returns the data as (x,y) list between 
         x1 and x2. If x2 is omitted the full range is used."""
        if not x2:
            x2 = self.xmax
        a = self.findIndex(x1)
        b = self.findIndex(x2)+1
        return self.data[a:b]

    def setMarker(self, x, y, ymin=0, size=None):
        trans = offset(self.ax, 0, 10)
        plt.plot([x,x],[y,self.ymax-0.2*self.deltay], lw=1, c='b', ls='dashed')
        x = round(x*10)/10.
        plt.text(x,self.ymax-0.2*self.deltay,'%5.1f' % x, rotation=90, 
        verticalalignment='bottom', horizontalalignment='center', transform=trans)
        return


if __name__ == '__main__':
    path = 'D:\Data\Python\Auger\data'
    d1 = Auger("181207_A_01",datapath=path)
    d2 = Auger("190207_A_02",datapath=path)
    dy=0.
    d2.info();d2.plot(color='m-');dy-=0.5
    d1.info();d1.plot(offset=dy);dy-=0.5
    d2.show()

    import code
    code.interact(local=locals())
