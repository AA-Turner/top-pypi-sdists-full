import sys, logging
logformat='[%(name)12s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)

#trying to load the 
try: 
    from geant4_pybind import *
except Exception as e:
    print(e)
    sys.exit("Package 'geant4_pybind' is not available.")

from g4camp.ActionInitialization import ActionInitialization
from g4camp.DetectorConstruction import DetectorConstruction
from g4camp.CustomPhysicsList import CustomPhysicsList
from g4camp.DataBuffer import DataBuffer

class g4camp:

    def __init__(self, physics="Custom", mode_physlist='all_phys', optics=True, primary_generator="gun", gun_args={},
                 multithread=False, thread_num=4):
        # By some reason multithread mode does not faster than serial mode
        # FIXME: number of threads can not be configured from here (why???)
        #
        self.log = logging.getLogger('g4camp')
        #
        super().__init__()
        self.mode_physlist     = mode_physlist
        self.optics            = optics             # switch on/off optic physics
        self.primary_generator = primary_generator  # can be 'gun' or 'gps'
        self.multithread       = multithread
        self.thread_num        = thread_num
        self.get_process       = False
        #
        self.data_buffer = DataBuffer()
        self.gps_macro = ""
        #
        self.ph_suppression_factor = 10 # must be integer
        self.skip_mode = 'fraction'     # 'fraction' (relative to E_init) or 'GeV' (absolute)
        self.skip_min = 0.              # min energy to skip particle (wrt. E_init or in GeV)
        self.skip_max = 1.e-2           # max energy to skip particle (wrt. E_init or in GeV)
        self.random_seed = 1
        self.det_height_m = 1500        # detector volume: cylinder height
        self.det_radius_m = 1500        # detector volume: cylinder radius
        self.rock_depth_m = 200
        self.refractive_index = 1.34
        # the following varialbes are to be set later
        self.E_skip_min = 0.            # min particle energy to skip
        self.E_skip_max = 0.            # max particle energy to skip
        self.E_init = 0.                # initial kinetic energy in GeV
        self.E_lower_edge = 0.
        #
        self.physListOptions = {"FTFP_BERT": FTFP_BERT,
                                "QGSP_BERT": QGSP_BERT,
                                "QGSP_BIC": QGSP_BIC}
        #
        self.ph_counter = 0
        #
        self.save_process_name = False
        #
        if multithread:
            self.runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.MT, thread_num)
        else:
            self.runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
        self.detConstruction = DetectorConstruction()
        if physics == "Custom": 
            self.physList = CustomPhysicsList(mode=self.mode_physlist, optics=self.optics)
        else:
            self.physList = self.physListOptions[physics]()
            if self.optics :
                self.log.error("Optics is only available with 'Custom' physics list")
                sys.exit()
        self.actInit = ActionInitialization(self, primary_generator=self.primary_generator, 
                                                  gun_args=gun_args)
        #
        self.runManager.SetUserInitialization(self.detConstruction)
        self.runManager.SetUserInitialization(self.physList)
        self.runManager.SetUserInitialization(self.actInit)
        #
        self.setVerbose()
        self.setDefaultCuts()
    
    def configure(self):
        #self.actInit.stackingAction.SetPhotonSuppressionFactor(1./self.ph_fraction)
        if self.multithread: 
            UImanager.ApplyCommand(f"/run/numberOfThreads", [self.thread_num])
        if self.optics:
            self.configureOptics()
        self.actInit.configure()
        self.detConstruction.SetDetectorHeight(self.det_height_m)
        self.detConstruction.SetDetectorRadius(self.det_radius_m)
        self.detConstruction.SetRockDepth(self.rock_depth_m)
        self.runManager.Initialize()
        #self.applyGeant4Command("/run/particle/dumpCutValues")
        if self.primary_generator == 'gps':
            self.applyGeant4Command("/control/execute", [self.gps_macro])
        G4Random.setTheSeed(self.random_seed)

    def setVerbose(self, control_verbose=0, tracking_verbose=0, run_verbose=0, 
                   em_process_verbose=0, had_process_verbose=0):
        self.applyGeant4Command("/control/verbose", [control_verbose])
        self.applyGeant4Command("/tracking/verbose", [tracking_verbose])
        self.applyGeant4Command("/run/verbose", [run_verbose])
        self.applyGeant4Command("/process/em/verbose", [em_process_verbose])
        self.applyGeant4Command("/process/had/verbose", [had_process_verbose])
        self.applyGeant4Command("/process/eLoss/verbose 0")
        self.applyGeant4Command("/particle/verbose 0")
        self.applyGeant4Command("/cuts/verbose 0")

    def setCut(self, particle, cut_value, cut_unit):
        # to be invoked before 'configure()'
        self.applyGeant4Command("/run/setCutForAGivenParticle", [particle, cut_value, cut_unit])

    def setDefaultCuts(self):
        # default cuts ensure all particle capable to produce Cherenkov light are tracked
        # i.e. E_threshold is about 260 keV (kinetic energy)
        self.setCut("gamma", 95., "cm")
        self.setCut("e-", 0.055, "cm")
        self.setCut("e+", 0.055, "cm")
        #self.applyGeant4Command("/cuts/setLowEdge", [760, "keV"]) # This can only lower energy limit

    def applyGeant4Command(self, command, arguments=[]):
        arg_string = ""
        for arg in arguments:
            arg_string += f" {arg}"
        UImanager = G4UImanager.GetUIpointer()
        UImanager.ApplyCommand(command + arg_string)
        #print(command + arg_string)
    
    def SetMaxEnergy(self, ene_val: float, ene_unit: str) -> None:
        self.applyGeant4Command(f'/process/eLoss/maxKinEnergy {ene_val} {ene_unit}')
        self.applyGeant4Command(f'/process/eLoss/bremThreshold {ene_val} {ene_unit}')
        self.applyGeant4Command(f'/process/eLoss/bremMuHadThreshold {ene_val} {ene_unit}')
        self.applyGeant4Command(f'/process/eLoss/LowestElectronEnergy {ene_val} {ene_unit}')
        self.applyGeant4Command(f'/process/eLoss/LowestMuHadEnergy {ene_val} {ene_unit}')
        #self.applyGeant4Command('/process/msc/EnergyLimit {ene_val} {ene_unit}')
        self.applyGeant4Command(f'/process/had/maxEnergy {ene_val} {ene_unit}')
    
    def SetMinEnergyE(self, ene_val: float, ene_unit: str) -> None:
        self.applyGeant4Command(f'/process/em/lowestElectronEnergy {ene_val} {ene_unit}')
    
    def SetMinEnergyMuHad(self, ene_val: float, ene_unit: str) -> None:
        self.applyGeant4Command(f'/process/em/lowestMuHadEnergy {ene_val} {ene_unit}')
    
    def SetStepFunction(self, alpha_R: float, rho_R_val, rho_R_unit: str) -> None:
        self.applyGeant4Command(f'/process/eLoss/StepFunctionLightIons {alpha_R} {rho_R_val} {rho_R_unit}')
        self.applyGeant4Command(f'/process/eLoss/StepFunctionMuHad {alpha_R} {rho_R_val} {rho_R_unit}')
        self.applyGeant4Command(f'/process/eLoss/StepFunctionIons {alpha_R} {rho_R_val} {rho_R_unit}')
        self.applyGeant4Command(f'/process/eLoss/StepFunction {alpha_R} {rho_R_val} {rho_R_unit}')
    
    def SetProductionCut(self, particle: str, range_val: float, range_unit: str) -> None:
        self.applyGeant4Command(f'/run/setCutForAGivenParticle {particle} {range_val} {range_unit}')
    
    def configureOptics(self):
        if not self.optics:
            self.log.warning("Optics is disabled")
            return
        self.applyGeant4Command("/process/optical/processActivation", ['Cerenkov', True])
        self.applyGeant4Command("/process/optical/processActivation", ['OpAbsorption', False])
        self.applyGeant4Command("/process/optical/processActivation", ['OpRayleigh', False])
        self.applyGeant4Command("/process/optical/processActivation", ['OpMieHG', False])
        self.applyGeant4Command("/process/optical/cerenkov/setStackPhotons", [True])

    def setGunParticle(self, particle_pdgid):
        particleTable = G4ParticleTable.GetParticleTable()
        particle_definition = particleTable.FindParticle(particle_pdgid)
        self.applyGeant4Command(f"/gun/particle {particle_definition.GetParticleName()}")

    def setGunEnergy(self, ene_val, ene_unit):
        self.applyGeant4Command(f"/gun/energy {ene_val} {ene_unit}")

    def setGunPosition(self, x_val, y_val, z_val, pos_unit):
        self.applyGeant4Command(f"/gun/position {x_val} {y_val} {z_val} {pos_unit}")

    def setGunTime(self, time_val, time_unit):
        self.applyGeant4Command(f"/gun/time {time_val} {time_unit}")

    def setGunDirection(self, dx, dy, dz):
        self.applyGeant4Command(f"/gun/direction {dx} {dy} {dz}")
        
    def setGunMomentum(self, px, py, pz, p_unit):
        self.applyGeant4Command(f"/gun/direction {px} {py} {pz} {p_unit}")

    def setGPSMacro(self, macro):
        if self.primary_generator != 'gps':
            self.log.warning("'primary_generator' was set to '{self.primary_generator}', switching it to 'gps'")
            self.primary_generator = 'gps'
        self.gps_macro = macro

    def setSkipMinMax(self, skip_mode, skip_min, skip_max):
        self.skip_mode = skip_mode
        self.skip_min = skip_min
        self.skip_max = skip_max
    
    def SetEnergyLowerEdge(self, ene):
        self.E_lower_edge = ene

    def setRandomSeed(self, val):
        self.random_seed = int(val)

    def setPhotonSuppressionFactor(self, val):
        self.ph_suppression_factor = float(val)

    def setDetectorHeight(self, val):
        self.det_height_m = val

    def setDetectorRadius(self, val):
        self.det_radius_m = val
        
    def setRockDepth(self, val):
        self.rock_depth_m = val
    
    def setRefractiveIndex(self, val):
        self.refractive_index = val
    
    def SaveProcessName(self, save_process_name) -> None:
        self.save_process_name = save_process_name

    def run(self, n_events):
        self.log.debug(f"random seed: {G4Random.getTheSeed()}")
        for i in range(n_events):
            self.runManager.BeamOn(1)
            yield self.data_buffer
