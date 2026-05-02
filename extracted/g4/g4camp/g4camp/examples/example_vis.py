from geant4_pybind import *
from g4camp.g4camp import g4camp
import sys

n_events = 10
gun_args = { 'particle':   'mu-', 
             'energy_GeV': 100000,
             'position_m': [0,0,10],
             'direction':  [0,0,1]  }

app = g4camp(optics=False, primary_generator='gun', gun_args=gun_args)
ui = G4UIExecutive(len(sys.argv), sys.argv)
visManager = G4VisExecutive("Quiet")
visManager.Initialize()
app.configure() # should be after initialization of visual manager
app.applyGeant4Command("/control/execute",  ["vis.mac"])
ui.SessionStart()
