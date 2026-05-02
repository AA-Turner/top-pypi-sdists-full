import numpy as np

from geant4_pybind import *

class SteppingAction(G4UserSteppingAction):

  def __init__(self, app):
    
    super().__init__()
    
    self.app = app
    self.data_buffer = app.data_buffer
    
    n = self.app.refractive_index
    self.cerenkov_threshold_e = G4ParticleDefinition.GetPDGMass(G4Electron.Electron())/GeV/np.sqrt(1.-1./n**2)
  
  def UserSteppingAction(self, step: G4Step):
    
    pre_step_point = step.GetPreStepPoint()
    Etot1 = pre_step_point.GetTotalEnergy()/GeV
    
    # Save every track point
    if Etot1 >= self.cerenkov_threshold_e and Etot1 >= self.app.E_lower_edge:
      # keep step end point
      track    = step.GetTrack()   
      particle = track.GetDefinition()
      
      uid           = track.GetTrackID()
      parent_uid    = track.GetParentID()
      pdgid         = particle.GetPDGEncoding()
      pos_m         = track.GetPosition()/m
      t_ns          = track.GetGlobalTime()/ns
      Etot_GeV      = track.GetTotalEnergy()/GeV
      step_length_m = track.GetStepLength()/m
      if self.app.save_process_name:
        post_step_point = step.GetPostStepPoint()
        process_name = post_step_point.GetProcessDefinedStep().GetProcessName()
        self.data_buffer.tracks = [uid, parent_uid, pdgid, pos_m, t_ns,
                                   Etot_GeV, step_length_m, process_name]
      else:
        self.data_buffer.tracks = [uid, parent_uid, pdgid, pos_m,
                                   t_ns, Etot_GeV, step_length_m]