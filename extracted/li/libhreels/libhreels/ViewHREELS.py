#!/usr/bin/env python3
import os
import re
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets, uic
#from PyQt6 import QtCore, QtGui, QtWidgets, uic
import libhreels as hh
hhPath = os.path.dirname(__file__)
from libhreels.HREELS import HREELS, myPath
from datetime import datetime  
import argparse
#import libhreels.expLogbook as lgb
import libhreels.NoExpLogbook as lgb

# fix HighRes Displays
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class HREELS_Window(QtWidgets.QMainWindow):
    """ fill in some initial data """
    def __init__(self,datapath=None, remoteDir=None, startWithFile=None, comment=None):
        super(HREELS_Window, self).__init__()
        f = os.path.join(hhPath,"viewhreels.ui")  # path to the package directory. Needed to find graphical user interface files (*.ui)
        self.ui = self.ui = uic.loadUi(f, self)
        self.xmin = 50.
        self.factor = 10.
        self.offset = 0.1
        self.useOffset = False
        self.normalized = False
        self.Areanormalized = False
        self.comment = comment
        self.showComment = lgb.available
        if datapath and os.path.exists(datapath):
            self.datapath = datapath
        else:
            self.datapath = './'
        self.directory = self.datapath
        if remoteDir and os.path.exists(remoteDir):
            self.remoteDir = remoteDir
        else:
            self.remoteDir = '//141.48.167.189/BackUp02/0_experiments/EELS-PC4/HREELS/gph_dat/'
        self.wideScan = True
        self.marker = []
        # self.markerSet = False

        # initialize the widget "drawWidget" and attach it into the ui
        self.drawing_figure = plt.figure(frameon=False,figsize=(5, 4), dpi=150, tight_layout = True)
        self.drawing_pane = FigureCanvas(self.drawing_figure)
        self.drawing_figure.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.drawing_figure.canvas.setFocus()        
        # self.drawing_figure.canvas.mpl_connect('button_press_event', self.onMouse)
        self.drawing_pane.axes = self.drawing_pane.figure.add_subplot(111)
        self.ui.drawWidget.layout().addWidget(self.drawing_pane)

        #Add a cursor:
        self.cursor = Cursor(self.drawing_pane, self.drawing_pane.axes)
        # self.cursorId = self.drawing_figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)

        # Add toolbar
        self.xToolbar = NavigationToolbar(self.drawing_pane, self)
        self.ui.drawWidget.layout().addWidget(self.xToolbar)
        self.xToolbar.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed))
        
        self.ui.lineEdit_directory.setText(self.datapath)
        self.ui.lineEdit_xmin.setText('%4.1f'%self.xmin)
        self.ui.lineEdit_factor.setText('%4.1f'%(self.factor))
        self.ui.lineEdit_offset.setText('%4.1f'%(self.offset))
        self.ui.checkBoxWideScans.setChecked(True)
        self.ui.checkBoxComment.setChecked(lgb.available)
        # self.ui.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)


        # Action on user events
        self.ui.checkBoxWideScans.toggled.connect(self.onWideScans)
        self.ui.checkBoxNormalized.toggled.connect(self.onNormalized)
        self.ui.checkBoxAreaNormalization.toggled.connect(self.onAreaNormalized)
        
        self.ui.checkBoxOffset.toggled.connect(self.onUseOffset)
        self.ui.checkBoxMarker.toggled.connect(self.onMarkerSet)
        self.ui.checkBoxComment.toggled.connect(self.onCommentSet)
        self.ui.pushButton_details.clicked.connect(self.onPushButton_details)
        self.ui.lineEdit_xmin.editingFinished.connect(self.onXmin)
        self.ui.lineEdit_factor.editingFinished.connect(self.onFactor)
        self.ui.lineEdit_offset.editingFinished.connect(self.onOffset)
        self.ui.lineEdit_directory.editingFinished.connect(self.onNewDirectory)
        self.ui.listWidget.itemSelectionChanged.connect(self.onFileSelection)

        # Action on user menu events: 
        self.action_directory.triggered.connect(self.onActionDir)
        self.action_test.triggered.connect(self.onActionTest)
        self.action_help.triggered.connect(self.onActionHelp)
        self.actionFile_info.triggered.connect(self.onPushButton_details)

        # Create list of all datafiles in the directory
        self.createFileList()
        self.dataDir = QtWidgets.QFileDialog(self)
        if os.name == 'nt':
            self.dataDir.setDirectory("D:\\Data\\Python\\HREELS\\expHREELS\\data")
        else:
            self.dataDir.setDirectory("/mnt/d/Data/Python/HREELS/expHREELS/data")

        if startWithFile:
            self.selectFile(startWithFile)


    def onXmin(self):
        '''Routine called by a new value of "Xmin". It will trigger a data window update.'''
        try:
            val = float(self.ui.lineEdit_xmin.text())
            self.xmin = val
        except ValueError:
            self.ui.lineEdit_xmin.setText('%4.1f'%self.xmin)
        self.onFileSelection()

    def onFactor(self):
        '''Routine called by a new value of "Factor", which defines the amplification factor for the energy loss
        region (larger than Xmin). It will trigger a data window update.'''
        try:
            val = float(self.ui.lineEdit_factor.text())
            self.factor = val
        except ValueError:
            self.ui.lineEdit_factor.setText('%4.1f'%(self.factor))
        self.onFileSelection()

    def onUseOffset(self):
        '''Routine called by toggling "Use Offset": If set, the  energy loss
        region (larger than Xmin) will be vertically offseted if multiple spectra are selected. 
        It will trigger a data window update.'''
        self.useOffset = self.ui.checkBoxOffset.isChecked()
        self.onOffset()

    def onOffset(self):
        try:
            val = float(self.ui.lineEdit_offset.text())
            self.offset = val
        except ValueError:
            self.ui.lineEdit_offset.setText('%4.1f'%(self.offset))
        self.onFileSelection()

    def onNormalized(self):
        '''Routine called by toggling "Normalized": If set, all spectra will be normalized to a maximum
        count rate of unity. It will trigger a data window update.'''
        self.ui.checkBoxAreaNormalization.setChecked(False)
        self.normalized = self.ui.checkBoxNormalized.isChecked()
        self.onFileSelection()

    def onAreaNormalized(self):
        '''Routine called by toggling "Area Normalized": If set, all spectra will be normalized to a sum of counts between -100 to 1000cm^-1 (or less if the dataset is shorter). It will trigger a data window update.'''
        self.ui.checkBoxNormalized.setChecked(False)
        self.Areanormalized = self.ui.checkBoxAreaNormalization.isChecked()
        self.onFileSelection()    

    def onActionDir(self):
        '''Routine calls Directory Selection Interface upon Menu selection. It will 
        create a data list from the chosen directory.'''
        # if os.name == 'nt':
        #     self.dataDir.setDirectory("D:\\Data\\Python\\HREELS\\expHREELS\\data")
        # else:
        #     self.dataDir.setDirectory("/mnt/d/Data/Python/HREELS/expHREELS/data")
        directory = self.openDirectoryDialog()
        if directory:
            self.ui.lineEdit_directory.setText(directory)
            self.directory = directory
            self.ui.listWidget.clear()
            self.datapath = directory
            self.createFileList()

    def onNewDirectory(self):
        '''Routine called if Directory field is modified. It will 
        create a data list from the chosen new directory (but only if it exists).'''
        dirText = self.ui.lineEdit_directory.text()
        tt = myPath(dirText)
        print('New directory: ',tt)
        self.directoryOld = self.directory
        if os.path.exists(tt):
            self.directory = tt
            self.ui.listWidget.clear()
            self.datapath = self.directory
            self.createFileList()
        else:
            self.ui.lineEdit_directory.setText(self.directoryOld)


    def onActionTest(self):
        '''Routine called by Menu item 'Test'. It is for playing 
        with future options.'''
        self.dataDir.setDirectory(self.remoteDir)
        directory = self.openDirectoryDialog()
        if directory:
            self.ui.lineEdit_directory.setText(directory)
            self.directory = directory
            self.ui.listWidget.clear()
            self.datapath = directory
            self.createFileList()

    def onActionHelp(self):
        pass
        msg = QtWidgets.QMessageBox()
        msg.setText('''
        This is the HREELS data browser of the Martin-Luther University Halle-Wittenberg
        (Version 0.9) designed for fast data screening and plotting.
        Copyright @ wolf.widdra@physik.uni-halle.de.
        ''')
        msg.setWindowTitle("HREELS data browser help")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        layout = msg.layout()
        widget = QtWidgets.QWidget()
        widget.setFixedSize(650, 1)
        layout.addWidget(widget, 3, 0, 1, 3)
        msg.buttonClicked.connect(self.onOK)            
        msg.exec_()

    def onPushButton_details(self):
        """Routine for showing a dialog window containing HREELS data details"""
        try:
            self.d.infoText()
        except:
            return
        self.dialog = QtWidgets.QDialog(self)
        f = os.path.join(hhPath,"viewhreels_dialog.ui")
        self.dialog.ui = uic.loadUi(f, self.dialog)
        self.dialog.ui.setWindowTitle('Dataset details')
        self.dialog.ui.textArea.setPlainText(self.d.infoText())
        self.dialog.show()

    def onMarkerSet(self):
        '''Routine called if selection "Set Marker" is toggled. It allows to draw dashed vertical lines
        with the energy loss values. The value 'self.markerSet' is used to decide later if lines have to be drawn.'''
        b = self.ui.checkBoxMarker.isChecked()
        self.markerSet = b
        if not b:
            # Disconnect all mouse events from canvas:
            self.drawing_figure.canvas.mpl_disconnect(self.cursorId)
            self.drawing_figure.canvas.mpl_disconnect(self.canvasId)
        else:
            # Connect all mouse events from canvas to routines:
            self.cursorId = self.drawing_figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
            self.canvasId = self.drawing_figure.canvas.mpl_connect('button_press_event', self.onMouse)
            print('mouse enabled')

    def onCommentSet(self):
        '''Routine called if selection "Show Comment" is toggled. It allows to draw dashed vertical lines
        with the energy loss values. The value 'self.markerSet' is used to decide later if lines have to be drawn.'''
        self.showComment =  self.ui.checkBoxComment.isChecked()
        # print('onCommentSet:', lgb.available, self.showComment, self.ui.listWidget.selectedItems()[0].text())
        if self.showComment:
            if lgb.available:                
                text = lgb.logbook.getShortMessage4File(self.d.fname)
                ids = lgb.logbook.search({'file':self.d.fname})
                if len(ids) > 0:
                    _, attributes, _ = lgb.logbook.read(ids[0])
                    print(self.d.fname, ids[0],': ', attributes['Date'],'\t',text[:-2])
            else:
                text = self.comment if self.comment else ''
                self.comment = None
            self.pCom = self.drawing_pane.axes.text(0.12, 0.98,text, ha='left', va='top', transform=self.drawing_pane.axes.transAxes)
        else:
            try:
                self.pCom.remove()
            except:
                pass

    def onOK(self, button):
        print("Button pressed is:",button.text())

    def onWideScans(self):
        '''Routine called if selection "Only wide scans" is toggled. The switch 'self.wideScan' decides 
        if all spectra or only spectra with a wider energy range (data files larger than 21 kB) 
        are listed on the left side.'''
        b = self.ui.checkBoxWideScans.isChecked()
        self.wideScan = b
        self.ui.listWidget.clear()
        self.createFileList()

    def selectFile(self, file):
        '''Select the file within the QListWidget by the program, e.g. as start parameter. 
        Make sure before that it exists. The file extension is dropped by re.split. '''
        matchingItems = self.ui.listWidget.findItems(re.split('\.',file)[0], QtCore.Qt.MatchExactly)
        self.ui.listWidget.setCurrentItem(matchingItems[0])
        for it in matchingItems:
            it.setSelected(True)
        self.ui.listWidget.setFocus()
        return

    def onFileSelection(self):
        '''Routine called if user makes a file selection or changes the file selection within the left list.
        The selected spectra are plotted according to the given flags (Xmin, Factor, Normalized, Offset). '''
        iMax = len(self.ui.listWidget.selectedItems())
        if iMax == 0:
            return
        # print([it.text() for it in self.ui.listWidget.selectedItems()])
        firstItem = self.ui.listWidget.selectedItems()[0]

        self.d = HREELS(firstItem.text(),self.datapath)
        if self.d.valid:
            plotColor = plt.cm.gnuplot(0)     # Define the color map (coolwarm; plasma; inferno; gnuplot)         
            self.updatePlot(xmin=self.xmin, factor=self.factor, normalized=self.normalized, Areanormalized=self.Areanormalized, color=plotColor)
            try:
                self.dialog.ui.textArea.setPlainText(self.d.infoText())
            except:
                pass
        else:
            self.drawing_pane.axes.cla()
            self.drawing_pane.draw()
            return
        if iMax > 1:
            i = 1.
            myList = self.ui.listWidget.selectedItems()[1:]
            for item in myList:     # Add here sorting according to ...
                plotColor = plt.cm.gnuplot(i/iMax)     # Define the color map (coolwarm; plasma; inferno; gnuplot)
                self.d = HREELS(item.text(),self.datapath)
                self.secondPlot(xmin=self.xmin, factor=self.factor, normalized=self.normalized, Areanormalized=self.Areanormalized,offset=i*self.offset*self.useOffset, color=plotColor)
                # print(i, item.text())
                i += 1
        # Reversing the sequence of labels in the legend:
        handles, labels = self.drawing_pane.axes.get_legend_handles_labels()
        self.drawing_pane.axes.legend(handles[::-1], labels[::-1])
        self.drawing_pane.axes.set_ylim(bottom=0.)
        self.drawing_figure.tight_layout()
        self.cursor = Cursor(self.drawing_pane, self.drawing_pane.axes)
        self.drawing_figure.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
        self.drawing_pane.draw()

    def onMouse(self, event):
        if not self.markerSet:
            return
        if (event.xdata):
            if event.button==1:
                x,y = event.xdata, event.ydata
                print(x,y)
                self.marker.append((x,y))
                self.setMarker(x,y)
            elif event.button==3:
                pass
            self.drawing_pane.draw()

    def setMarker(self, x, y, ymin=0, size=None):
        ''' Set vertical marker with text label. Note that self.figure() needs to be 
        called before use.'''
        # trans = offset(self.ax, 0, 30)
        self.drawing_pane.axes.plot([x,x],[ymin,y], lw=1, c='black', ls='dashed')
        x = round(x)
        # plt.text(x,y,'%4i' % x, rotation=90, verticalalignment='bottom', horizontalalignment='center', transform=trans)
        self.drawing_pane.axes.text(x,y,'%4i' % x, rotation=90, verticalalignment='bottom', horizontalalignment='center')
        return
    

    def updatePlot(self,xmin=70, factor=10, normalized=False, Areanormalized=False, color="red"):
        '''Plotting the first of the selected spectra. '''
        self.drawing_pane.axes.cla()
        self.plotWidget(normalized=normalized, Areanormalized=Areanormalized, showComment=False)
        self.plotWidget(xmin=xmin, factor=factor, color=color, label='x %3i'%factor, normalized=normalized, Areanormalized=Areanormalized, showComment=self.showComment)

    def secondPlot(self,xmin=70, factor=10, normalized=False, Areanormalized=False, offset = 0., color="b-"):
        '''Plotting the second and all further selected spectra. '''
        self.plotWidget(xmin=xmin, factor=factor, color=color, label=self.d.fname, normalized=normalized, Areanormalized=Areanormalized, offset = offset)

    def plotWidget(self, xmin=None, xmax=None, factor=1, label='x', normalized=False, Areanormalized=False, color="black",
                        marker=True, offset = 0., showComment=False):
        ''' plot(self, xmin=None, xmax=None, factor=1, label='x', normalized=False, color="b-",marker=True)'''
        self.d.pFactor = factor
        if xmin:
            nstart = self.d.findIndex(xmin)
        else:
            nstart = 0
        if xmax:
            nend = self.d.findIndex(xmax)
        else:
            nend = len(self.d.xdata)
        if normalized:
            factor /= self.d.maxIntensity
            Areanormalized = False # just in case
        elif Areanormalized:
            try:                    
                areanormalize_xstart = np.argmin(abs(self.d.xdata+100.)) #seems to be oddly complicated, but is way more stable than x.index(-100.)
            except:
                areanormalize_xstart = 0
            try:
                areanormalize_xend = np.argmin(abs(self.d.xdata-1000.))
            except:
                areanormalize_xend = len(self.d.xdata)

            factor /= self.d.ydata[areanormalize_xstart:areanormalize_xend].sum()
            #print("Area normalization in x[", self.d.xdata[areanormalize_xstart],":",self.d.xdata[areanormalize_xend],"] is used.")    
        if label == "x":
            label = self.d.fname        
        self.drawing_pane.axes.plot(self.d.xdata[nstart:nend], factor*self.d.ydata[nstart:nend] + offset, color=color, label=label)
        self.d.factor = factor
        if showComment: self.onCommentSet()
        self.drawing_pane.axes.set_xlabel('Energy Loss (cm$^{-1}$)')
        if normalized:
            self.drawing_pane.axes.set_ylabel('Normalized Intensity')
        elif Areanormalized:
            self.drawing_pane.axes.set_ylabel('Area Normalized Intensity')
        else:    
            self.drawing_pane.axes.set_ylabel('Intensity (s$^{-1}$)')
        
        if marker:
            for (x,y) in self.d.marker:
                self.d.setMarker(x,y*factor)
        return

    def getFileList(self, directory, sizeMin=0.):
        '''Get the list of all *.gph or *.GPH data files with a file size larger 
        than sizeMin. A good value to remove the datfile with just the elastic peak is 
        sizeMin=21000. The list is sorted by the file creation date.'''
        list = os.listdir(directory)
        files = []
        for file in list:
            location = os.path.join(directory, file)
            size = os.path.getsize(location)
            time = os.path.getmtime(location)
            if size>sizeMin:
                files.append((file, time, size))
        # files.sort(key=lambda s: -s[1])  # sort by time
        files.sort(key=lambda s: s[1])  # sort by reversed time
        fileNames = [item[0] for item in files]
        data_ext = ['gph', 'GPH']
        gphFiles = [fn for fn in fileNames
                    if any(fn.endswith(ext) for ext in data_ext)]
        return gphFiles, len(gphFiles)

    def createFileList(self):
        if self.wideScan:
            sizeMin = 21000.
        else:
            sizeMin = 5.
        for item in self.getFileList(self.datapath,sizeMin=sizeMin)[0]:
            fname = re.split('\.',item)[0]
            self.ui.listWidget.addItem(fname)
          
    def openDirectoryDialog(self):
        self.dataDir = QtWidgets.QFileDialog(self)
        options = self.dataDir.Options()
        # options = self.dataDir.ShowDirsOnly
        options |= self.dataDir.DontUseNativeDialog
        dir =self.dataDir.getExistingDirectory(self, 'Select data directory', options=options)
        if dir:
            return dir

class Cursor(object):
    def __init__(self, fig, ax):
        self.figure = fig
        self.ax = ax
        self.ly = ax.axvline(color='r')  # the vert line

    def mouse_move(self, event):
        if not event.inaxes:
            return
        self.ly.set_data([event.xdata, event.xdata], [0, 1])
        self.figure.draw()

def runViewer(datapath= None, remoteDir=None, startWithFile=None, comment=None):
    """ Main function for graphical application start """
    app = QtWidgets.QApplication(sys.argv)
    form = HREELS_Window(datapath=datapath, remoteDir=remoteDir, startWithFile=startWithFile, comment=comment)
    form.show()
    sys.exit(app.exec_())


def myMain():
    parser = argparse.ArgumentParser()
    #################  Command line handling  ######################
    def is_valid_file(string):
        if not os.path.exists(string):
            parser.error("The file %s does not exist!" % string)
            return False
        else:
            return string
    parser.add_argument("file", nargs='?', help="Start viewer with this datafile", type=is_valid_file)
    parser.add_argument("-f", "--file2", help="Start viewer with this datafile")
    parser.add_argument("-c", "--comment", default=None, help="Text comment")
    args = parser.parse_args()

    if args.file:
        fPath,fName = os.path.split(args.file)
        # print(">>> ", fPath, " <<< ", fName)
    elif args.file2:
        fPath,fName = os.path.split(args.file2)
        # print(">>> ", fPath, " <<< ", fName)
    else:
        if os.name == 'nt':
            fPath = "D:\\Data\\Python\\HREELS\\expHREELS\\data"
        else:
            fPath = "/mnt/d/Data/Python/HREELS/expHREELS/data"
        fName = None

    runViewer(datapath=fPath, startWithFile=fName, comment=args.comment)




if __name__ == '__main__':
	myMain()