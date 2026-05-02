from geant4_pybind import *
#from MuNuclearBuilder import MuNuclearBuilder

def list_available_physics():
    import geant4_pybind as g4
    for v in sorted(dir(g4)):
      if ("Physics" in v) and ("G4V" not in v) and ("Vector" not in v):
        print(v)
    print(" ")

class CustomPhysicsList(G4VModularPhysicsList):

  def __init__(self, mode='all_phys', optics=True):
    super().__init__()

    self.phys_constructors = {}
    
    if mode == 'em_cascade':
      self.phys_constructors["decay"] = G4DecayPhysics()
      self.phys_constructors["em"] = G4EmStandardPhysics_option4()   # G4EmStandardPhysics(),  G4EmStandardPhysics_option1()
    elif mode == 'all_phys':
      self.phys_constructors["decay"] = G4DecayPhysics()
      self.phys_constructors["em"] = G4EmStandardPhysics_option4()
      self.phys_constructors["em_extra"] = G4EmExtraPhysics()  # for muon nuclear interaction
      self.phys_constructors["rad_decay"] = G4RadioactiveDecayPhysics()
      self.phys_constructors["hadron_elastic"] = G4HadronElasticPhysics()
      self.phys_constructors["hadron"] = G4HadronPhysicsFTFP_BERT()
      self.phys_constructors["stopping"] = G4StoppingPhysics()
    elif mode == 'fast':
      self.phys_constructors["decay"] = G4DecayPhysics()
      self.phys_constructors["em"] = G4EmStandardPhysics_option1()
      self.phys_constructors["em_extra"] = G4EmExtraPhysics()  # for muon nuclear interaction
      self.phys_constructors["hadron_elastic"] = G4HadronElasticPhysics()
      self.phys_constructors["hadron"] = G4HadronPhysicsQGSP_FTFP_BERT()
      #self.phys_constructors["ion"] = G4IonQMDPhysics()
      #self.phys_constructors["ion"] = G4IonElasticPhysics()
    
    if optics:
      self.phys_constructors["optical"] = G4OpticalPhysics()

    for key, phys in self.phys_constructors.items():
      self.RegisterPhysics(phys)
      phys.SetVerboseLevel(0)

    #list_available_physics()