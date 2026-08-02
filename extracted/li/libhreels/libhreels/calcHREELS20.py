#!/usr/bin/env python3
import numpy as np
import json
import sys, re, os
from libhreels.HREELS import myPath
from copy import deepcopy

import scipy.integrate as integrate

libDir = os.path.dirname(os.path.realpath(__file__)) 

try:
    from libhreels import myEels20 as LambinEELS   # wrapper for myEels20.f90
    from libhreels import myBoson as LambinBoson  # wrapper for myBoson.f90
except:
    print('myEels20 and MyBoson are not available here (Check your version)')			
    print('''Make sure the Fortran routines 'myEels20' and 'myBoson' 
    have been complied with the proper f2py for the right python version!!''')
    print('\n\n\n')

# Experimental setup as dictionary:
setup = {
    "e0": 4.0,
    "theta": 60.,
    "phia": 0.33,
    "phib": 2.0,
    "temperature": 298.,
    "debug": False
}
# Instrumental function describing elastic peak shape:
instrument = {
    "width": 18.,
    "intensity": 100000.,
    "asym": 0.01,
    "gauss": 0.88
}

	
def importMaterials(string='', path=libDir):
    ''' Returns a dictionary with all phonon parameters for the material provided 
    as string argument. If the string is empty or not matching, a list of all available 
    materials is printed.
    '''
    file = os.path.join(myPath(path),'materials20.json')
    with open(file) as json_file:
        materials = json.load(json_file)
        try:
            mat = materials[string]

            #Following if-case for preventing old material data to be used in  wrong terminology
            if mat["wLO"][0]==1 and mat["gLO"][0]==1 and mat["wTO"][0]<0 and mat["gTO"][0]<0:
                print('It seems you are trying to load a Material from an older version. Parameter will be altered to fit the current Version.')
                wTO = 0
                gTO = -mat["gTO"][0]                
                wLO = -mat["wTO"][0]
                gLO = -mat["gTO"][0]        
                mat["wTO"][0] = wTO
                mat["gTO"][0] = gTO
                mat["wLO"][0] = wLO
                mat["gLO"][0] = gLO
        except:
            print('No data for material >>{}<< found in {} materials.json!!'.format(string, path))
            print('Available materials:\n{}\n'.format(materials.keys()))
            mat = 'None'
    return mat

def addDrude(wLOPlasma, gLOPlasma, material, gTOPlasma='None'):
    ''' Adds a generalized Drude response to the materials properties (which are provided 
    as last argument) and returns a new materials dictionary with all phonon parameters. Note 
    that at least the eps_infinity has to given before.
    '''
    if gTOPlasma == 'none':
        gTOPlasma = gLOPlasma
    newMaterial = deepcopy(material)
    try:
        if len(newMaterial['wTO']) > 0:
            newMaterial['wTO'] += [0.]
            newMaterial['gTO'] += [gTOPlasma]
            newMaterial['wLO'] += [wLOPlasma]
            newMaterial['gLO'] += [gLOPlasma]
            if newMaterial.get('Q'):
                newMaterial['Q'] += [0]
            return newMaterial
    except:
        print('Cannot add Drude to material',material)
    return material

################################################################################
################################################################################
class lambin:
    def __init__(self, film, setup=setup, instrument=instrument):
        self.e0 = setup['e0']
        self.theta = setup['theta']
        self.phia = setup['phia']
        self.phib = setup['phib']
        self.temperature = setup['temperature']
        self.debug = setup['debug']
        self.width = instrument['width']
        self.gauss = instrument['gauss']
        self.intensity = instrument['intensity']
        self.asym = instrument['asym']
        self.layers = len(film)          # number of layers
        self.neps = self.layers
        # name_size = self.layers
        self.name = []; self.thick=[]; self.listNOsci=[]; self.epsinf =[]; Q = []
        allTO=[]; allgTO=[];  allgLO=[]; nDrude=0; Qdummy = []
        name2 = []
        for layer in film:
            try:
                a = layer[0]['name']
            except:
                a = 'None'
            self.name.append('{:<10}'.format(a[:10]))        # film name and material
            name2.append(a)
            try:
                a = layer[1]
            except:
                a = 10000.
            self.thick.append(a)
            self.epsinf.append(layer[0]['eps'])
            nTO = 2 * len(layer[0]['wTO'])
            allTO.extend(layer[0]['wTO'])
            allgTO.extend(layer[0]['gTO'])
            allTO.extend(layer[0]['wLO'])
            allgTO.extend(layer[0]['gLO'])
            qList = layer[0].get('Q')
            if qList:
                Q.extend(layer[0]['Q'])
                Q.extend(len(layer[0]['Q'])*[0.])
            else:
                Q.extend(2* len(layer[0]['wTO'])*[0.])
            self.listNOsci.append(nTO)

        if len(allTO)!=sum(self.listNOsci) or len(allgTO)!=sum(self.listNOsci):
            print('Error in materials: ', layer[0])
        if len(Q)!=sum(self.listNOsci) :
            print('Error in materials (Check Q): ', layer[0])
        self.wOsc = np.array(allTO)
        self.gOsc = np.array(allgTO)
        self.osc = np.array([self.wOsc, np.array(Q), self.gOsc])
        # print('[self.wOsc, np.array(Q), self.gOsc]: \n',self.osc)
        return

    def calcSurfaceLoss(self,x):
        ''' Calculate the surface loss spectrum for the array of x, which needs to be an equidistant array. 
        All parameters are defined in the class __init__() call.'''
        wmin = min(x)
        wmax = max(x)-0.001
        dw = (wmax-wmin)/(len(x)-1)     # assumes that x is an equidistant array
        wn_array_size = len(x)     # size of array for x and epsilon (wn_array, loss_array)
        nper = 1.
        contrl = '{:<10}'.format('None'[:10])   # Can be 'image' to include image charge
        mode = '{:<10}'.format('kurosawa'[:10])           
        wn_array,loss_array = LambinEELS.mod_doeels.doeels(self.e0,self.theta,self.phia,self.phib,
            wmin,wmax,dw,self.layers,self.neps,nper,self.name,
            self.thick,self.epsinf,self.listNOsci,self.osc,contrl,mode,wn_array_size)
        i=0
        for item in wn_array:
            if item > 0: break
            i += 1
        return wn_array[i-1:], loss_array[i-1:]

    def calcHREELS(self,x, normalized=True, areanormalized=False):
        emin = min(x)
        emax = max(x)-0.001
        norm = 1
        xLoss,loss_array = self.calcSurfaceLoss(x)
        wmin = min(xLoss)
        wmax = max(xLoss)
        xOut,spectrum,n = LambinBoson.doboson3(self.temperature,self.width,self.gauss,self.asym,
            emin,emax,wmin,wmax,loss_array,self.debug,len(loss_array))
        if normalized:
            norm = max(spectrum[:n])
            if areanormalized: #edit by HHE
                try:                    
                    areanormalize_xstart = np.argmin(abs(x+100.)) #seems to be oddly complicated, but is way more stable than x.index(-100.) or where()
                except:
                    areanormalize_xstart = 0
                try:
                    areanormalize_xend = np.argmin(abs(x-1000.))
                except:
                    areanormalize_xend = len(x)
                cropped_spectra=spectrum[areanormalize_xstart:areanormalize_xend]
                cropped_x=x[areanormalize_xstart:areanormalize_xend]

                norm=integrate.simps(cropped_spectra, dx=x[areanormalize_xstart+1]-x[areanormalize_xstart])

        # else:
        #     print("not normalized")
        return xOut[:len(x)], spectrum[:len(x)]/norm

    def calcEps(self, x):
        epsArray = []
        nOsci = len(self.wOsc)
        for wn in x:
            yn = LambinEELS.mod_doeels.seteps(self.listNOsci,nOsci,self.osc,self.epsinf,wn,self.layers)
            epsArray.append(yn)
        return np.transpose(np.array(epsArray))

####################################################################################
def myMain():
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    from libhreels import dielectrics20 as dielectrics

    x = np.linspace(-100.,1000,400)
    material = {'eps': 1.,
                'wTO': [-200, -750],  
                'gTO': [  12,   8], 
                'wLO': [   1,   1],     # this parameter is irrelvant if wTO is negativ
                'gLO': [   1,   1],     # this parameter is irrelvant if wTO is negativ
                'Q'  : [  10,  15]}
    material2 = {'eps': 1.,
                'wTO': [-200, -750],  
                'gTO': [  12,   8], 
                'wLO': [   1,   1],     # this parameter is irrelvant if wTO is negativ
                'gLO': [   1,   1],     # this parameter is irrelvant if wTO is negativ
                'Q'  : [  0.1,  15]}
    material3 = {'eps': 1.,
                'wTO': [-200, -750,   0],  
                'gTO': [  12,   8,   50], 
                'wLO': [   1,   1, 2000],     # this parameter is irrelvant if wTO is negativ
                'gLO': [   1,   1,   50],     # this parameter is irrelvant if wTO is negativ
                'Q'  : [  10,  15,    0]}

    film1 = lambin(film=[[material,10000.]])
    film2 = lambin(film=[[material2,10000.]])
    film3 = lambin(film=[[material3,10000.]])
    eps3= film3.calcEps(x)[0]
    eps2= film2.calcEps(x)[0]
    eps = film1.calcEps(x)[0]
    plt.plot(x,np.real(eps))
    plt.plot(x,np.real(eps2))
    plt.plot(x,np.real(eps3))

    ############# Comparison with dielectrics ################
    osci1  = dielectrics.simpleOscillator(material3['wTO'][0], 
                                          material3['Q'  ][0],
                                      gTO=material3['gTO'][0])
    osci2  = dielectrics.simpleOscillator(material3['wTO'][1], 
                                          material3['Q'  ][1],
                                      gTO=material3['gTO'][1])
    drude = dielectrics.drude(material3['wLO'][2],material3['gTO'][2],material3['gLO'][2])
    epsInfinity = material3['eps']
    eps_dielectrics = epsInfinity * (osci1(x) + osci2(x)  + (1 + drude(x)))
    plt.plot(x,np.real(eps_dielectrics),linestyle='dotted')



    plt.ylabel(r'$Re(\epsilon)$')
    plt.xlabel('Energy Loss (cm$^{-1}$)')
    plt.xlim(left=5)
    # plt.ylim(-6000,6000)

    plt.text(0.99, 0.01,os.path.basename(__file__), fontsize=10, ha='right', va='bottom', transform=plt.gcf().transFigure)
    output_filename = os.path.splitext(__file__)[0] + '.png'
    plt.savefig(output_filename)

    plt.show()

    plt.plot(x,np.imag(eps))
    plt.plot(x,np.imag(eps2))
    plt.plot(x,np.imag(eps3))
    plt.plot(x,np.imag(eps_dielectrics))
    plt.xlim(left=0)
    plt.ylim(-1500,1500)
    plt.show()

    # plt.plot(x,np.imag(dielectrics.sigma(eps,x)))
    # plt.plot(x,np.imag(dielectrics.sigma(eps2,x)))
    # plt.plot(x,np.imag(dielectrics.sigma(eps3,x)))
    # plt.xlim(left=0)
    # plt.ylim(-1500,1500)
    # plt.show()

    xs, spectrum = film3.calcHREELS(x,normalized=True,areanormalized=False)
    plt.plot(xs[:-1],spectrum[:-1], label='normalized=False')
    plt.show()

    material4 = {'eps': 1.,
                'wTO': [ 200, 750,   0],  
                'gTO': [  12,   8,   50], 
                'wLO': [ 600, 950, 2000],     
                'gLO': [  10,  10,   50],     
                'Q'  : [  10,  15,    0]}

    # material4 = {'eps': 1.,
    #             'wTO': [ 200, 750,   0],  
    #             'gTO': [  12,   8,   50], 
    #             'wLO': [ 300, 950, 2000], 
    #             'gLO': [  10,  10,   50]}


    film4 = lambin(film=[[material4,10000.]])
    xs, spectrum = film4.calcHREELS(x,normalized=True,areanormalized=False)
    plt.plot(xs[:-1],spectrum[:-1], label='normalized=False')
    plt.show()

if __name__ == '__main__':
	myMain()