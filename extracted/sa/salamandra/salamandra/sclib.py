# Copyright 2021 EnICS Labs, Bar-Ilan University.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0


#This library contains common pre-built standard-cells.
#It is mainly aimed for net-list creation purposes, and as such the cells are built mostly without the inner logic.
#
#The cells are heavily based on (and default to) tcbn65lp standard-cell library by TSMC
#for cell and pin names and structure.
#####################################################################################################################
##USAGE EXAMPLE: Creating a simple, default AND gate##
#####################################################################################################################
'''
from sclib import *

myAnd = And()
'''
#####################################################################################################################
##THATS IT! you can also customize the values and names if you want (see example files).
#####################################################################################################################
#
#Feel free to add more gates\cells\anything if you like,
#but please try and use the template given below when adding a new cell:
#
#####################################################################################################################
##TEMPLATE FOR GATES:
#####################################################################################################################
'''
#Cell description (Optional: name in library)
class T(Component):
    __defaultName = 'Tx'
    
    def __init__(self, name=__defaultName):
        Component.__init__(self,name)
'''
#####################################################################################################################

from salamandra import *
#####################################################################################################################
##Generic Gates
#####################################################################################################################

#Generic gate with 1 input and 1 output
class G1in1out(Component):
    __defaultName = 'G1IN1OUT'
    
    def __init__(self, name=__defaultName, in1='in1', out='out'):
        Component.__init__(self,name)
        self.add_pin(Output(out))
        self.add_pin(Input(in1))


#Generic gate with 2 inputs and 1 output
class G2in1out(G1in1out):
    __defaultName = 'G2IN1OUT'
    
    def __init__(self, name=__defaultName, in1='in1', in2='in2', out='out'):
        G1in1out.__init__(self,name,in1,out)
        self.add_pin(Input(in2))

#Generic gate with variable number of inputs and 1 output
class Gxin1out(Component):
    __defaultName = 'GXIN1OUT'
    
    def __init__(self, name=__defaultName, inNum=1, out='out', inArr=None, nameFormat='in'):
        Component.__init__(self,name)
        self.add_pin(Output(out))
        self.addInputs(inNum,inArr,nameFormat)
        
    
    def addInputs(self, inNum,inArr=None,nameFormat='in'):
        if (inArr is None):
            inArr = [nameFormat+'1']
            
        arrSize = len(inArr)
        for i in range(1,inNum+1):
            nextIn=''            
            if (i<=arrSize):
                nextIn=inArr[i-1]
            else:
                nextIn=nameFormat+str(i)
            self.add_pin(Input(nextIn))


#Generic gate with variable number of inputs and outputs
class Gxinxout(Gxin1out):
    __defaultName = 'GXINXOUT'
    
    def __init__(self, name=__defaultName, inNum=1, inArr=None, inNameFormat='in', outNum=1, outArr=None, outNameFormat='out'):
        Component.__init__(self,name)
        self.addInputs(inNum,inArr,inNameFormat)
        self.addOutputs(outNum,outArr,outNameFormat)
        
    
    def addOutputs(self,outNum,outArr=None,nameFormat='out'):
        if (outArr is None):
            outArr = [nameFormat+'1']
            
        arrSize = len(outArr)
        for i in range(1,outNum+1):
            nextOut=''            
            if (i<=arrSize):
                nextOut=outArr[i-1]
            else:
                nextOut=nameFormat+str(i)
            self.add_pin(Output(nextOut))
            
#####################################################################################################################
##Transistors (not standard cells) 
#####################################################################################################################
            
#Nmos
class Nmos(Component):
    __defaultName = 'Nmos'
    
    def __init__(self, name=__defaultName, source='source', drain='drain',gateIn='gate',bulk='bulk'):
        Component.__init__(self,name)
        self.add_pin(Inout(source))
        self.add_pin(Inout(drain))
        self.add_pin(Input(gateIn))
        self.add_pin(Input(bulk))
   
#Pmos
class Pmos(Nmos):
    __defaultName = 'Pmos'
    
    def __init__(self, name=__defaultName, source='source', drain='drain',gateIn='gate',bulk='bulk'):
        Nmos.__init__(self, name,source,drain,gateIn,bulk)

#####################################################################################################################
## Misc.
#####################################################################################################################
        
#Inverter (INVDx)
class Inverter(G1in1out):
    __defaultName = 'INVD0'
    
    def __init__(self,name=__defaultName, in1='I', out='ZN'):
        G1in1out.__init__(self,name,in1,out)

#Buffer (BUFFDx)
class Buffer(G1in1out):
    __defaultName = 'BUFFD0'
    
    def __init__(self,name=__defaultName, in1='I', out='Z'):
        G1in1out.__init__(self,name,in1,out)
        
#Delay (DELx)
class Delay(G1in1out):
    __defaultName = 'DEL0'
    
    def __init__(self,name=__defaultName, in1='I', out='Z'):
        G1in1out.__init__(self,name,in1,out)
        
#D-FF (DFDx)
class Dff(G2in1out):
    __defaultName = 'DFD0'
    
    def __init__(self, name=__defaultName, in1='D', in2='CP', out1='Q',out2='QN'):
        G2in1out.__init__(self,name,in1,in2,out1)
        self.add_pin(Output(out2))

#####################################################################################################################
##AND Gates
#####################################################################################################################
        
#AND2 (AN2Dx)
class And(G2in1out):
    __defaultName = 'AN2D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', out='Z'):
        G2in1out.__init__(self,name,in1,in2,out)


#AND3 (AN3Dx)
class And3(And):
    __defaultName = 'AN3D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', out='Z'):
        And.__init__(self,name,in1,in2,out)
        self.add_pin(Input(in3))


#AND4 (AN4Dx)
class And4(And3):
    __defaultName = 'AN4D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', in4='A4', out='Z'):
        And3.__init__(self,name,in1,in2,in3,out)
        self.add_pin(Input(in4))
        

#Flexible AND
class Andx(Gxin1out):
    __defaultName = 'AN2D0'
    
    def __init__(self, name=__defaultName, inNum=2, out='Z', inArr=None, nameFormat='A'):
        Gxin1out.__init__(self,name,inNum,out,inArr,nameFormat)

#####################################################################################################################
##OR Gates
#####################################################################################################################
        
#OR2 (OR2Dx)
class Or(G2in1out):
    __defaultName = 'OR2D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', out='Z'):
        G2in1out.__init__(self,name,in1,in2,out)


#OR3 (OR3Dx)
class Or3(Or):
    __defaultName = 'OR3D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', out='Z'):
        Or.__init__(self,name,in1,in2,out)
        self.add_pin(Input(in3))


#OR4 (OR4Dx)
class Or4(Or3):
    __defaultName = 'OR4D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', in4='A4', out='Z'):
        Or3.__init__(self,name,in1,in2,in3,out)
        self.add_pin(Input(in4))


#Flexible OR
class Orx(Gxin1out):
    __defaultName = 'OR2D0'
    
    def __init__(self, name=__defaultName, inNum=2, out='Z', inArr=None, nameFormat='A'):
        Gxin1out.__init__(self,name,inNum,out,inArr,nameFormat)

#####################################################################################################################
##XOR Gates
#####################################################################################################################
        
#XOR2 (XOR2Dx)
class Xor(G2in1out):
    __defaultName = 'XOR2D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', out='Z'):
        G2in1out.__init__(self,name,in1,in2,out)


#XOR3 (XOR3Dx)
class Xor3(Xor):
    __defaultName = 'XOR3D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', out='Z'):
        Xor.__init__(self,name,in1,in2,out)
        self.add_pin(Input(in3))


#XOR4 (XOR4Dx)
class Xor4(Xor3):
    __defaultName = 'XOR4D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', in4='A4', out='Z'):
        Xor3.__init__(self,name,in1,in2,in3,out)
        self.add_pin(Input(in4))


#Flexible XOR
class Xorx(Gxin1out):
    __defaultName = 'XOR2D0'
    
    def __init__(self, name=__defaultName, inNum=2, out='Z', inArr=None, nameFormat='A'):
        Gxin1out.__init__(self,name,inNum,out,inArr,nameFormat)

#####################################################################################################################
##NAND Gates
#####################################################################################################################

#NAND2 (ND2Dx)
class Nand(And):
    __defaultName = 'ND2D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', out='ZN'):
        And.__init__(self,name,in1,in2,out)
        

#NAND3 (ND3Dx)
class Nand3(Nand):
    __defaultName = 'ND3D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', out='ZN'):
        Nand.__init__(self,name,in1,in2,out)
        self.add_pin(Input(in3))


#NAND4 (ND4Dx)
class Nand4(Nand3):
    __defaultName = 'ND4D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', in4='A4', out='ZN'):
        And3.__init__(self,name,in1,in2,in3,out)
        self.add_pin(Input(in4))
        

#Flexible NAND
class Nandx(Gxin1out):
    __defaultName = 'ND2D0'
    
    def __init__(self, name=__defaultName, inNum=2, out='ZN', inArr=None, nameFormat='A'):
        Gxin1out.__init__(self,name,inNum,out,inArr,nameFormat)
        
#####################################################################################################################
##NOR Gates
#####################################################################################################################

#NOR2 (NR2Dx)
class Nor(Or):
    __defaultName = 'NR2D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', out='ZN'):
        Or.__init__(self,name,in1,in2,out)
        

#NOR3 (NR3Dx)
class Nor3(Nor):
    __defaultName = 'NR3D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', out='ZN'):
        Nor.__init__(self,name,in1,in2,out)
        self.add_pin(Input(in3))


#NOR4 (NR4Dx)
class Nor4(Nor3):
    __defaultName = 'NR4D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='A3', in4='A4', out='ZN'):
        Nor3.__init__(self,name,in1,in2,in3,out)
        self.add_pin(Input(in4))
        

#Flexible NOR
class Norx(Gxin1out):
    __defaultName = 'NR2D0'
    
    def __init__(self, name=__defaultName, inNum=2, out='ZN', inArr=None, nameFormat='A'):
        Gxin1out.__init__(self,name,inNum,out,inArr,nameFormat)

#####################################################################################################################
##AO's
#####################################################################################################################
        
#AO21 (AO21Dx)
class Ao21(And3):
    __defaultName = 'AO21D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='B', out='Z', andG=None, orG=None):
        And3.__init__(self,name,in1,in2,in3,out)
        
        if (andG is None):
            try:
                andGate = Component.get_component_by_name('AN2D0')
            except:
                andGate = And()
            self.add_component(andGate,'and')
        else:
            self.add_component(And(andG),'and')

        if (orG is None):
            try:
                orGate = Component.get_component_by_name('OR2D0')
            except:
                orGate = Or()
            self.add_component(orGate,'or')
        else:
            self.add_component(Or(orG),'or')
            
        self.connect(in1,'and.A1')
        self.connect(in2,'and.A2')
        self.add_net(Net('andZ'))
        self.connect('andZ','and.Z')
        self.connect('andZ','or.A1')
        self.connect(in3,'or.A2')
        self.connect(out,'or.Z')

#AO211 (AO211Dx)
class Ao211(And4):
    __defaultName = 'AO211D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='B', in4='C', out='Z', andG=None, orG=None):
        And4.__init__(self,name,in1,in2,in3,in4,out)
        
        if (andG is None):
            try:    
                andGate = Component.get_component_by_name('AN2D0')
            except:
                andGate = And()
            self.add_component(andGate,'and')
        else:
            self.add_component(And(andG),'and')

        if (orG is None):
            try:    
                orGate = Component.get_component_by_name('OR3D0')
            except:
                orGate = Or3()
            self.add_component(orGate,'or3')
        else:
            self.add_component(Or3(orG),'or3')
            
        self.connect(in1,'and.A1')
        self.connect(in2,'and.A2')
        self.add_net(Net('andZ'))
        self.connect('andZ','and.Z')
        self.connect('andZ','or3.A1')
        self.connect(in3,'or3.A2')
        self.connect(in4,'or3.A3')
        self.connect(out,'or3.Z')


#AO221 (AO221Dx)
class Ao221(Andx):
    __defaultName = 'AO221D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='B1', in4='B2', in5='C', out='Z', andG=None, orG=None):
        Andx.__init__(self, name, 5, out, inArr=[in1,in2,in3,in4,in5])
        
        if (andG is None):
            try:    
                andGate = Component.get_component_by_name('AN2D0')
            except:
                andGate = And()
        else:
            andGate = And(andG)
            
        self.add_component(andGate,'and1')
        self.add_component(andGate,'and2')

        if (orG is None):
            try:    
                orGate = Component.get_component_by_name('OR3D0')
            except:
                orGate = Or3()
            self.add_component(orGate,'or3')
        else:
            self.add_component(Or3(orG),'or3')
            
        self.connect(in1,'and1.A1')
        self.connect(in2,'and1.A2')
        self.connect(in3,'and2.A1')
        self.connect(in4,'and2.A2')
        self.add_net(Net('and1Z'))
        self.add_net(Net('and2Z'))
        self.connect('and1Z','and1.Z')
        self.connect('and2Z','and2.Z')
        self.connect('and1Z','or3.A1')
        self.connect('and2Z','or3.A2')
        self.connect(in5,'or3.A3')
        self.connect(out,'or3.Z')

#####################################################################################################################
##AOI's
#####################################################################################################################
        
#AOI21 (AOI21Dx)
class Aoi21(And3):
    __defaultName = 'AOI21D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='B', out='ZN',aoG=None, andG=None, orG=None, invG=None):
        And3.__init__(self,name,in1,in2,in3,out)
        
        if (aoG is None):
            try:
                ao21 = Component.get_component_by_name('AO21D0')
            except:
                ao21 = Ao21(andG=andG, orG=orG)
            self.add_component(ao21,'ao21')
        else:
            self.add_component(Ao21(name=aoG,andG=andG,orG=orG),'ao21')
        
        if (invG is None):
            try:    
                inv = Component.get_component_by_name('INVD0')
            except:
                inv = Inverter()
            self.add_component(inv,'inv')
        else:
            self.add_component(Inverter(invG),'inv')
        
        self.connect(in1,'ao21.A1')
        self.connect(in2,'ao21.A2')
        self.connect(in3,'ao21.B')
        self.add_net(Net('aoZ'))
        self.connect('aoZ','ao21.Z')
        self.connect('aoZ','inv.I')
        self.connect(out,'inv.ZN')


#AOI211 (AOI211Dx)
class Aoi211(Andx):
    __defaultName = 'AOI221D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='B', in4='C', out='ZN',aoG=None, andG=None, orG=None, invG=None):
        And4.__init__(self,name,in1,in2,in3,in4,out)
        
        if (aoG is None):
            try:    
                ao211 = Component.get_component_by_name('AO211D0')
            except:
                ao211 = Ao211(andG=andG, orG=orG)
            self.add_component(ao211,'ao211')
        else:
            self.add_component(Ao211(name=aoG,andG=andG,orG=orG),'ao211')
        
        if (invG is None):
            try:    
                inv = Component.get_component_by_name('INVD0')
            except:
                inv = Inverter()
            self.add_component(inv,'inv')
        else:
            self.add_component(Inverter(invG),'inv')
        
        self.connect(in1,'ao211.A1')
        self.connect(in2,'ao211.A2')
        self.connect(in3,'ao211.B')
        self.connect(in4,'ao211.C')
        self.add_net(Net('aoZ'))
        self.connect('aoZ','ao211.Z')
        self.connect('aoZ','inv.I')
        self.connect(out,'inv.ZN')
        
        
#AOI221 (AOI221Dx)
class Aoi221(Andx):
    __defaultName = 'AOI211D0'
    
    def __init__(self, name=__defaultName, in1='A1', in2='A2', in3='B1', in4='B2', in5='C', out='ZN',aoG=None, andG=None, orG=None, invG=None):
        Andx.__init__(self, name, 5, out, inArr=[in1,in2,in3,in4,in5])
        
        if (aoG is None):
            try:    
                ao221 = Component.get_component_by_name('AO221D0')
            except:
                ao221 = Ao211(andG=andG, orG=orG)
            self.add_component(ao221,'ao221')
        else:
            self.add_component(Ao211(name=aoG,andG=andG,orG=orG),'ao221')
        
        if (invG is None):
            try:    
                inv = Component.get_component_by_name('INVD0')
            except:
                inv = Inverter()
            self.add_component(inv,'inv')
        else:
            self.add_component(Inverter(invG),'inv')
        
        self.connect(in1,'ao221.A1')
        self.connect(in2,'ao221.A2')
        self.connect(in3,'ao221.B1')
        self.connect(in4,'ao221.B2')
        self.connect(in5,'ao221.C')
        self.add_net(Net('aoZ'))
        self.connect('aoZ','ao221.Z')
        self.connect('aoZ','inv.I')
        self.connect(out,'inv.ZN')
