#!/usr/bin/python
# HREELS library Version 1.0    (October 2018 @ WFW)
#
import numpy as np
import re
import os
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.signal import find_peaks_cwt
from datetime import datetime
from datetime import timedelta
from matplotlib.transforms import offset_copy
# from pylab import figure
from matplotlib.pyplot import figure

if os.name == 'nt':
    diskd = 'D:\\'
elif os.name == 'posix':
    diskd = '/mnt/d/'
else:
    print('Define diskd!   System not known ...')

def myPath(path):
    '''Convert any Windows or Linux path to a Linux path. Adds a slash at the end, if missing.'''
    if path == None:
        return path
    try:
        newPath = re.sub(r'\\', '/', path)
        if not newPath[-1] == '/':
            newPath += '/'
        return newPath
    except:
        return path

def offset(ax, x, y):
    return offset_copy(ax.transData, x=x, y=y, units='dots')

def createDataDictionary(fileList, datapath):
    '''A python data dictionary is build from a given list of HREELS data files. All data files are read in and 
    are available with their properties, e.g. d[file].fname, d[file].maxIntensity, d[file].resolution, 
    d[file].xdata, or d[file].ydata.
    '''
    d = {}
    for file in fileList:
        d[file] = HREELS(file, datapath=datapath)
        # print('File:',d[file].fname,' -- ', d[file].maxIntensity, d[file].resolution)
    return d

def HREELS_elog_Dictionary(file, path):
    '''This function reads a HREELS data file (at the given datapath) and creates a dictionary for import into the eLog electronic
    labbook. In addition, the maximal count rate and the elastic peak width are also reported.
    '''
    spec = HREELS(file,datapath=path)
    spec.infoText()
    dic = {'Category':'HREELS', 'Type':'HREELS', 'Substrate':'as before', 'Summary':str(spec.energy)+':%5.0f'% spec.xmin0 +'-%-5.0f'% spec.xmax0, 
        'Temperature':'', 'Pressure_HREELS':'', 'Pressure_Prep':'', 'Pressure_FEL':'', 'Pressure_PreVac':'', 
        'Material':'', 'Energy':str(spec.energy), 'Location':'', 'Duration':str(spec.totalTime), 'File':str(file), 'Thickness':'', 
        'Scan_Range':'%5.0f'% spec.xmin0 +','+'%5.0f'% spec.xmax0, 'Position_x':'', 'Position_y':'', 'Position_z':'', 'Position_phi':'', 
        'Time_Channel':str(spec.timePerChannel), 
        'Filament':'%4.2f'%spec.filament, 'N_channels':spec.channelText, 'Resolution':'%5.1f'%spec.resolution, 'MDate':spec.startTimeEpoch, 
        'MaxCounts':'%7.0f'%spec.maxIntensity, 'Author':'Python Script'}
    return dic


class HREELS:
    """This class handles HREELS data and their plotting. """ 
    path = "\\\\backup-ep3\\BackUp02\\0_experiments\\EELS-PC4\HREELS\\gph_dat\\"
    pathSav = "\\\\backup-ep3\\BackUp02\\0_experiments\\EELS-PC4\HREELS\\BATCH\\sav\\"
    # path = "./"
    def __init__(self, _filename, datapath=path, dataSav=" ", scan=-1):
    # def __init__(self, _filename, datapath=path, dataSav=pathSav, scan=-1):
        global eV2cm
        eV2cm = 8065.6
        self.maxIntensity = 1.
        if scan < 0:
            self.datapath = myPath(datapath)
        else:
            if dataSav == " ":
                self.datapath = myPath(datapath+"..\\BATCH\\sav\\")
            else:
                self.datapath = myPath(dataSav)
            print('Directory {} is used to access individual scans.'.format(dataSav))
            _filename += '.{:03.0f}'.format(scan)
            print('File {} is used.'.format(_filename))

        if self.readDataFile(_filename):
            try:
                self.getElasticPeak()
                self.correctOffset()
                print('File: %s: Counts: %6.0f, Res: %4.1f' % (self.fname, self.maxIntensity, self.resolution))
            except:
                print("Error fitting elastic peak.")
                self.maxIntensity = 1.
                self.resolution = 0
                self.xOffset = -999
            self.valid = True
        else:
            print('No valid datafile:', _filename)
            self.valid = False

    def readDataFile(self, _filename):
        '''Read DELTA 0.5 HREELS data file and extracts xy data in counts/s and cm-1.
        '''
        if _filename.find(".") == -1:
            _filename +=".GPH"
        self.filename = _filename
        self.fname = self.filename[0:self.filename.find(".")]
        xdata = []
        ydata = []
        self.segments = []
        file =os.path.join(self.datapath,self.filename)
        with open(file, 'r', encoding='iso-8859-15') as f:
            f.readline()
            code=f.readline().split()[2]
            if code != "DELTA":
                print ("Data file has wrong format!",code)
                return False
            for line in f:
                if re.search(r"^S \d+ ([-+]?[0-9]*\.?[0-9]+)",line):
                    xdata.append(line.split()[2])
                if re.search(r"^M \d+ (\d+\.\d+)",line):
                    ydata.append(line.split()[2])
                match = re.search('(.*)\t#\tStartzeit',line)
                if match:
                    self.startTime = datetime.strptime(match.group(1), "%m-%d-%Y %H:%M:%S")
                    self.startTimeEpoch = self.startTime.timestamp()
                match = re.search('(.*)\t#\tEndzeit',line)
                if match:
                    self.stopTime = datetime.strptime(match.group(1), "%m-%d-%Y %H:%M:%S")
                match = re.search('(.*)\t#\tMeas time',line)
                if match:
                    self.timePerChannel = float(match.group(1))
                match = re.search('(.*)\t#\tNumber of Segments',line)
                if match:
                    self.numberSegments = int(match.group(1))
                match = re.search('(.*)\t#\tSegmentsize',line)
                if match:
                    a = match.group(1).split()
                    self.segments.append((int(a[0]),float(a[2])*eV2cm,float(a[3])*eV2cm,float(a[5])))
                match = re.search('(.*)\t#\tAmpere',line)
                if match:
                    self.filament = float(match.group(1))
                match = re.search('^E0 + ([-+]?[0-9]*\.?[0-9]+)',line)
                if match:
                    self.energy = float(match.group(1))
                match = re.search('(.*)\t#\tSave extension',line)   # Number of identicals scans (filename.000, .001, .002 are the related data)
                if match:
                    self.scans = float(match.group(1))


        self.xdata = eV2cm * np.array(xdata, dtype=float)
        self.ydata = np.array(ydata, dtype=float)/self.timePerChannel
        self.data = list(zip(self.xdata,self.ydata))
        if len(xdata) < 5:
            print('There are no spectral data in file', self.filename)
            self.xmin = 0.
            self.xmax = 0.
            return False
        else:
            self.xmin = self.xdata[0]
            self.xmax = self.xdata[-1]
        self.xmin0 = self.xmin
        self.xmax0 = self.xmax
        self.totalTime = self.stopTime-self.startTime
        self.marker = []
        return True

    def __str__(self):
        return self.datapath+self.filename

    def info(self):
        print("filename: \t\t",self.filename)
        print("datapath: \t\t",self.datapath)
        print("startTime: \t\t",self.startTime)
        print("totalTime: \t\t",self.totalTime)
        print("xmin: \t\t\t","%6.1f"%self.xmin,"cm-1")
        print("xmax: \t\t\t","%6.1f"%self.xmax,"cm-1")
        print("timePerChannel:\t\t","%4.2f"%self.timePerChannel,"s")
        if len(self.segments) > 1:
            print("segments: \t\t")
            for each in self.segments:
                print("\t\t%5d channels: %6.1f to %6.1f cm-1 in %4.2f s per channel"%each)
        else:
            print("channels: \t\t","%5d"%self.segments[0][0])
        if len(self.marker)>0:
            print("marker: \t\t")
            for each in self.marker:
                print("\t\t%6.1f\t %8.1f"%each)
        print("maxIntensity: \t\t","%8.1f"%self.maxIntensity,"counts/s")
        print("resolution: \t\t","%5.1f"%self.resolution,"cm-1")
        print("xOffset: \t\t","%6.3f"%self.xOffset,"cm-1")
        print('--------')

    def infoText(self):
        channelText =" "
        longText = "filename: \t\t"+self.filename+'\n'
        longText +="datapath: \t\t"+self.datapath+'\n'
        longText +="startTime: \t\t"+str(self.startTime)+'\n'
        longText +="totalTime: \t\t"+str(self.totalTime)+'\n'
        longText +="xmin: \t\t\t"+"%6.1f"%self.xmin+" cm-1"+'\n'
        longText +="xmax: \t\t\t"+"%6.1f"%self.xmax+" cm-1"+'\n'
        longText +="timePerChannel:\t\t"+"%4.2f"%self.timePerChannel+" s"+'\n'
        if len(self.segments) > 1:
            longText +="segments: \t\t"+'\n'
            for each in self.segments:
                longText +="\t\t%5d channels: %6.1f to %6.1f cm-1 in %4.2f s per channel"%each+'\n'
                channelText += "%5d channels: %6.1f to %6.1f cm-1 in %4.2f s per channel"%each+'<br>'
        else:
            longText +="channels: \t\t"+"%5d"%self.segments[0][0]+'\n'
            channelText += "%5d"%self.segments[0][0]
        self.channelText = channelText
        if len(self.marker)>0:
            longText +="marker: \t\t"+'\n'
            for each in self.marker:
                longText +="\t\t%6.1f\t %8.1f"%each+'\n'
        longText +="maxIntensity: \t\t"+"%8.1f"%self.maxIntensity+" counts/s"+'\n'
        longText +="resolution: \t\t"+"%5.1f"%self.resolution+" cm-1"+'\n'
        longText +="xOffset: \t\t\t"+"%6.3f"%self.xOffset+" cm-1"+'\n'
        longText +='--------'
        return longText

    def findIndex(self, lossenergy):
        for i in range(len(self.xdata)):
            if self.xdata[i] > lossenergy: 
                return i
        print('HREELS.findIndex: lossenergy', lossenergy, 'not found in xdata')
        return len(self.xdata)-1

    def plot(self, xmin=None, xmax=None, factor=1, label='x', normalized=False, color="b-",marker=True):
        ''' plot(self, xmin=None, xmax=None, factor=1, label='x', normalized=False, color="b-",marker=True)'''
        self.pFactor = factor
        if xmin:
            nstart = self.findIndex(xmin)
        else:
            nstart = 0
        if xmax:
            nend = self.findIndex(xmax)
        else:
            nend = len(self.xdata)
        if normalized:
            factor /= self.maxIntensity
        if label == "x":
            label = self.filename
        
        plt.plot(self.xdata[nstart:nend], factor*self.ydata[nstart:nend], color, label=label)
        self.factor = factor
        plt.xlabel('Energy Loss (cm$^{-1}$)')
        if normalized:
            plt.ylabel('Normalized Intensity')
        else:
            plt.ylabel('Intensity (s$^{-1}$)')
        plt.legend()
        if marker:
            for (x,y) in self.marker:
                self.setMarker(x,y*factor)
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

    def drawAndWait(self):
        plt.draw()
        plt.pause(0.001)
        value = input("Press [enter] to continue.")
        return value

    def func(self, x, a, width, x0):
            return a * np.exp(-((x-x0)/width*1.6651092)**2)

    def gaussQB(self, x, amp, width, x0, const=0., lin=0., q=0.):
        ''' Function for a Gaussian peak with quadratic background.'''
        return amp * np.exp(-((x-x0)/width*1.6651092)**2) + const + lin *(x-x0) + q*(x-x0)**2

    def getElasticPeak(self):
        if self.xmin < -20.:
            initialWidth = 20.
            xmin_Index =self.findIndex(-initialWidth)
            xmax_Index =self.findIndex(initialWidth)
            # (ftx,fity) is the data range to fit the elastic peak initially
            fitx = self.xdata[xmin_Index:xmax_Index]
            fity = self.ydata[xmin_Index:xmax_Index]
            #print(xmax_Index-xmin_Index)
            if (xmax_Index-xmin_Index < 10):
                return np.array([ 0., 0., 0.])
            popt, dummy = optimize.curve_fit(self.func, fitx, fity, p0=[28000., 8.,0.], bounds=([0., 2., -8.], [900000., 30., 8.]))
            #print('Fit: I=%5.1f kc/s, FWHM=%4.1f cm^-1, Offset=%5.3f cm^-1' % tuple(popt))
            # We now take a smaller x range that is centered around the peak position and fit again:
            xmin_Index2 =self.findIndex(-popt[1]*0.55)
            xmax_Index2 =self.findIndex(popt[1]*0.55)
            fitx = self.xdata[xmin_Index2:xmax_Index2]
            fity = self.ydata[xmin_Index2:xmax_Index2]
            popt, dummy = optimize.curve_fit(self.func, fitx, fity, p0=[28000., 8.,0.], bounds=([0., 2., -8.], [900000., 30., 8.]))
            # print('Fit: I=%5.1f kc/s, FWHM=%4.1f cm^-1, Offset=%5.3f cm^-1' % tuple(popt))
            self.maxIntensity = popt[0]
            self.resolution = popt[1]
            self.xOffset = popt[2]
            return popt
        else:
            print('Dataset without elastic peak.')
            self.maxIntensity = 1.
            self.resolution = 0.
            self.xOffset = 0.


    def getPeak(self, x0, y0):
        initialWidth = 60.
        xmin_Index =self.findIndex(x0-initialWidth)
        xmax_Index =self.findIndex(x0+initialWidth)
        # (ftx,fity) is the data range to fit the elastic peak initially
        fitx = self.xdata[xmin_Index:xmax_Index]
        fity = self.ydata[xmin_Index:xmax_Index]*self.factor
        popt, dummy = optimize.curve_fit(self.func, fitx, fity, p0=[y0, 20.,x0], bounds=([y0/4., 2., x0-50.], [y0*3., 90., x0+50.]))
        # print('Fit: I=%5.1f kc/s, FWHM=%4.1f cm^-1, peak=%5.3f cm^-1' % tuple(popt))
        self.fit = popt
        return popt

    def getPeakQB(self, x0, y0):
        ''' Fits a Gaussian peak centered around x0 with quadratic background.'''
        initialWidth = 80.
        xmin_Index =self.findIndex(x0-initialWidth)
        xmax_Index =self.findIndex(x0+initialWidth)
        fitx = self.xdata[xmin_Index:xmax_Index]
        fity = self.ydata[xmin_Index:xmax_Index]*self.factor
        startValues = [y0,      30.,    x0,     2.,     0., 0.]   # amp, width, x0, const, lin, q
        lowerBounds = [y0/4.,   10.,    x0-60,  0.,    -10000., 0.]  
        upperBounds = [y0*3.,   80.,   x0+60,  1000000.,   10000., 0.001]  
        popt, dummy = optimize.curve_fit(self.gaussQB, fitx, fity, p0=startValues, bounds=(lowerBounds, upperBounds))
        x0 = popt[2]
        xmin_Index =self.findIndex(x0-initialWidth)
        xmax_Index =self.findIndex(x0+initialWidth)
        fitx = self.xdata[xmin_Index:xmax_Index]
        fity = self.ydata[xmin_Index:xmax_Index]*self.factor
        startValues = popt
        popt, dummy = optimize.curve_fit(self.gaussQB, fitx, fity, p0=startValues, bounds=(lowerBounds, upperBounds))
        print('Fit: I=%5.1f kc/s, FWHM=%4.1f cm^-1, peak=%5.3f cm^-1, const=%5.3f, lin=%5.3f, q=%6.5f' % tuple(popt))
        self.fit = popt
        x = np.linspace(self.fit[2]-initialWidth,self.fit[2]+initialWidth)
        self.fitCurve = self.gaussQB(x, self.fit[0],self.fit[1],self.fit[2],self.fit[3],self.fit[4],self.fit[5])
        return popt

    def getPeakFromMarker(self, index):
        # popt = self.getPeak(self.marker[index][0],self.marker[index][1])
        popt = self.getPeak(self.marker[index][0],self.marker[index][1])
        self.marker[index] =(popt[2],popt[0]/self.factor)
        # print('Fit peak:',popt[2],popt[0]/self.factor)

    def showPeak(self):
        initialWidth = 80.
        x0 = self.fit[2]
        x = np.linspace(x0-initialWidth,x0+initialWidth)
        if len(self.fit)==3:
            fit = self.func(x, self.fit[0],self.fit[1],self.fit[2])
        elif len(self.fit)==6:
            fit = self.gaussQB(x, self.fit[0],self.fit[1],self.fit[2],self.fit[3],self.fit[4],self.fit[5])
        else:
            print('Wrong number of fit arguments!')
            return
        plt.plot(x,fit)
        return

    def selectData(self,x1, x2=None):
        """Returns the HREELS data as (x,y) list between the
        wavenumbers x1 and x2. If x2 is omitted the full range is used."""
        if not x2:
            x2 = self.xmax
        a = self.findIndex(x1)
        b = self.findIndex(x2)+1
        return self.data[a:b]

    def plotInfoAmp(self,factor=400,xmin=300,marker=True):
        self.info()
        self.figure()
        self.plot(label=self.fname+"\n"+str(self.startTime),marker=False)
        self.plot(xmin=xmin, factor=factor, color='r-', label='x%i' % factor, marker=marker)
        #self.drawAndWait()

    def labelFactor(self, xlabel):
        nxlabel = self.findIndex(xlabel)
        plt.text(self.xdata[nxlabel],self.ydata[nxlabel]*self.factor*1.1,'x%3i' % self.pFactor,  
        verticalalignment='bottom', horizontalalignment='left')

    def pickPeak(self):
        def onclick(event):
            if event.button ==1:
                self.getPeakQB(event.xdata,event.ydata)
                self.marker.append((self.fit[2],self.fit[0]/self.factor))
                self.setMarker(self.fit[2],self.fit[0])
                self.showPeak()
                self.fig.canvas.draw()
            else:
                self.marker.pop()
                print("Marker #{} deleted!".format(len(self.marker)+1))
                self.fig.canvas.draw()
        self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.ax.set_title('pick Marker with left button ... (right button:Erase last)')

    def setMarker(self, x, y, ymin=0, size=None):
        ''' Set vertical marker with text label. Note that self.figure() needs to be 
        called before use.'''
        trans = offset(self.ax, 0, 30)
        # plt.plot([x,x],[ymin,y], lw=1, c='black', ls='dashed')
        self.ax.plot([x,x],[ymin,y], lw=1, c='black', ls='dashed')
        x = round(x)
        # plt.text(x,y,'%4i' % x, rotation=90, 
        self.ax.text(x,y,'%4i' % x, rotation=90, 
        verticalalignment='bottom', horizontalalignment='center', transform=trans)
        return

    def correctOffset(self):
        self.xdata -= self.xOffset
        self.data = list(zip(self.xdata,self.ydata))
        self.xmin = self.xdata[0]
        self.xmax = self.xdata[-1]
        # self.xOffset = 0.

    def peakFind(self,xStart=60, marker=False):
        ''' Finds all peaks and returns a list of their x values. If marker='True', 
        markers will be added to an existing plot.'''
        x2 = self.xdata[self.findIndex(xStart):]
        y2 = self.ydata[self.findIndex(xStart):]
        peakind = find_peaks_cwt(y2, np.arange(11,28))
        for i in peakind[1:]:
            print('Detected peak at %5.1f' % x2[i])
        if (marker):
            for i in peakind[1:]:
                self.setMarker(x2[i],y2[i])
        return self.xdata[self.findIndex(xStart):][peakind]

    def plotWaterFall(self, fileList, offset, xmin=0, xmax=0, colorSeq=False, reverse=False, factor=1., legend=False, normalized=False, myColor=None):
        if xmin:
            nstart = self.findIndex(xmin)
        else:
            nstart = 0
        if xmax:
            nend = self.findIndex(xmax)
        else:
            nend = len(self.xdata)
        label = None
        i = 0.
        iMax = float(len(fileList))
        if normalized:
            normFactor = factor/self.maxIntensity
        if reverse:
            fileList = reversed(fileList)
        for item in fileList:
            self.__init__(item, datapath=self.datapath)
            if normalized:
                normFactor = factor/self.maxIntensity
            else:
                normFactor = factor
            if myColor:
                plotColor = myColor
            else:
                plotColor=plt.cm.RdYlBu(i/iMax)
            plt.plot(self.xdata[nstart:nend], normFactor*self.ydata[nstart:nend]+i*offset, color=plotColor, label=self.fname)
            i += 1.
        if legend:
            plt.legend()
        return
        

def myMain():
    fig = None
    datapath = diskd+ "/Data/Python/HREELS/expHREELS/data"
    data1 = HREELS("I2L02",datapath)
    if data1.valid:
        data1.info()
        data1.figure()
        data1.plot(label=data1.fname+"\n"+str(data1.startTime))
        data1.plot(xmin=300, factor= 10, color='r-', label='')
        if data1.drawAndWait() == 'm':
            data1.plot(xmin=1400, factor= 600, color='g.', label='')

    a = data1.infoText()
    print('InfoText:\n',a)
    print('Filament: {:4.2f} A'.format(data1.filament))
    print('Energy: {:2.0f} eV'.format(data1.energy))



if __name__ == '__main__':
	myMain()