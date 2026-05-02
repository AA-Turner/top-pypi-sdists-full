from geant4_pybind import *

class UserPhysicsList(G4VUserPhysicsList):
    
    def __init__(self) -> None:
        super().__init__()
    
    def ConstructParticle(self) -> None:
        self.electron = G4Electron.Definition()
        G4Positron.Definition()
        G4Gamma.Definition()
        G4MuonMinus.Definition()
        G4MuonPlus.Definition()
        G4PionMinus.Definition()
        G4PionPlus.Definition()
    
    def ConstructProcess(self) -> None:
        proc = G4ProcessTable
        G4ComptonScattering.GetProcessName()
        proc.SetProcessActivation(G4ProcessType.fElectromagnetic, self.electron, True)