from geant4_pybind import *
import numpy as np

class DetectorConstruction(G4VUserDetectorConstruction):

  def __init__(self):
    super().__init__()
    self.rho = 1500*m
    self.zmin = 0*m
    self.zmax = 1500.*m
    self.rock_depth = 200.*m
    self.check_overlaps = True
    #
    #self.mie_g_forward = 0.98
    #self.mie_g_backward = 0.99
    #self.mie_f_to_b_ratio = 1.0
    #self.mie_fraction = 0.99
    #
    self.sensDet = None
    #
    self.DefineMaterials()


  def DefineMaterials(self):
    man = G4NistManager.Instance()
    elH  = man.FindOrBuildElement("H", False)
    elO  = man.FindOrBuildElement("O", False)
    elC  = man.FindOrBuildElement("C", False)
    elCa = man.FindOrBuildElement("Ca", False)
    elMg = man.FindOrBuildElement("Mg", False)
    #
    # Water
    nelements = 2
    self.matWater = G4Material("Water", 1.0*g/cm3, nelements, kStateLiquid)
    self.matWater.AddElement(elH, 2)
    self.matWater.AddElement(elO, 1)
    #
    # Rock for lake bed
    nelements = 4
    self.matStdRock = G4Material("StdRock", 2.65*g/cm3, nelements, kStateSolid);
    self.matStdRock.AddElement(elO,  0.52);
    self.matStdRock.AddElement(elCa, 0.27);
    self.matStdRock.AddElement(elC,  0.12);
    self.matStdRock.AddElement(elMg, 0.09);
    #
    # Optical properties
    #  (just some dummy values)
    ph_ene = 1239.84193/np.array([650, 350])*eV
    ph_rindex = np.full(ph_ene.shape, fill_value=1.34)
    ph_abs =    np.full(ph_ene.shape, fill_value=20*m)
    ph_scat =   np.full(ph_ene.shape, fill_value=60*m)

    MPT_water = G4MaterialPropertiesTable()
    MPT_water.AddProperty("RINDEX", G4doubleVector(ph_ene), G4doubleVector(ph_rindex))
    MPT_water.AddProperty("ABSLENGTH", G4doubleVector(ph_ene), G4doubleVector(ph_abs))
    MPT_water.AddProperty("RAYLEIGH", G4doubleVector(ph_ene), G4doubleVector(ph_scat))
    #MPT_water.AddProperty("MIEHG", G4doubleVector(ph_ene), G4doubleVector(ph_scat))
    #MPT_water.AddConstProperty("MIEHG_FORWARD", self.mie_g_forward);
    #MPT_water.AddConstProperty("MIEHG_BACKWARD", self.mie_g_backward);
    #MPT_water.AddConstProperty("MIEHG_FORWARD_RATIO", self.mie_f_to_b_ratio)
    self.matWater.SetMaterialPropertiesTable(MPT_water)


  def Construct(self):
    print(f"Detector volume: H={self.zmax/m:.0f} m, R={self.rho/m:.0f} m")
    # Get materials
    matManager = G4NistManager.Instance()
    matWater = matManager.FindOrBuildMaterial("Water");
    matStdRock = matManager.FindOrBuildMaterial("StdRock");
    #
    # Mother volume
    worldRho = 1.1 * self.rho
    worldH   = 1.1 * 2. * max(abs(self.zmax),abs(self.zmin),abs(self.rock_depth))
    world_solid = G4Tubs("World", 0., worldRho, worldH/2., 0., 360.*deg)
    world_log   = G4LogicalVolume(world_solid, matWater, "World")
    world_phys  = G4PVPlacement(None, G4ThreeVector(0,0,0), world_log,
                                "World", None, False, self.check_overlaps)
    #
    # Lake bed
    lakeBed_solid = G4Tubs("LakeBed", 0., self.rho, self.rock_depth/2., 0, 360*deg)
    lakeBed_log   = G4LogicalVolume(lakeBed_solid, matStdRock, "LakeBed")
    G4PVPlacement(None, G4ThreeVector(0,0,-self.rock_depth/2.), lakeBed_log,
                  "LakeBed", world_log, False, self.check_overlaps);
    #
    # Segmented sensitive volume
    water_solid = G4Tubs("Water", 0., self.rho, (self.zmax-self.zmin)/2., 0, 360*deg)
    water_log   = G4LogicalVolume(water_solid, matWater, "Water")
    G4PVPlacement(None, G4ThreeVector(0,0,(self.zmax+self.zmin)/2.), water_log,
                  "Water", world_log, False, self.check_overlaps);
    self.det_log = water_log
    #
    return world_phys


  def ConstructSDandField(self):
    pass
    #self.sensDet = SensitiveDetector("SensDet")
    #G4SDManager.GetSDMpointer().AddNewDetector(self.sensDet)
    #self.det_log.SetSensitiveDetector(self.sensDet)


  def GetSensitiveDetector(self):
    return self.sensDet

  def SetDetectorHeight(self, val): # in meters
    self.zmax = val*m

  def SetDetectorRadius(self, val): # in meters
    self.rho = val*m

  def SetRockDepth(self, val):
    self.rock_depth = val*m