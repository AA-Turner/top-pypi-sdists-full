from geant4_pybind import *
from g4camp.PrimaryGeneratorAction import PrimaryGeneratorAction
from g4camp.RunAction import RunAction
from g4camp.EventAction import EventAction
from g4camp.StackingAction import StackingAction
from g4camp.SteppingAction import SteppingAction
from g4camp.DataBuffer import DataBuffer

class ActionInitialization(G4VUserActionInitialization):

    def __init__(self, app, primary_generator, gun_args={}):
        super().__init__()
        self.app = app
        self.primary_generator = primary_generator
        self.gun_args = gun_args
    
    def configure(self):
        self.app.E_init = self.primGenAct.particleGun.GetParticleEnergy()
        self.app.E_skip_min = self.app.skip_min
        self.app.E_skip_max = self.app.skip_max
        if self.app.skip_mode == 'fraction':
            self.app.E_skip_min *= self.app.E_init
            self.app.E_skip_max *= self.app.E_init

    def BuildForMaster(self):  # invoked in multithread mode only
        self.SetUserAction(RunAction(True))

    def Build(self):           # invoked in in boths modes: multihread - multiple time, serial - once
        self.primGenAct = PrimaryGeneratorAction(self.primary_generator, gun_args=self.gun_args)
        self.SetUserAction(self.primGenAct)
        self.SetUserAction(RunAction(False))
        self.SetUserAction(EventAction(self.app))
        self.SetUserAction(StackingAction(self.app))
        self.SetUserAction(SteppingAction(self.app))
