from geant4_pybind import *
import numpy as np

class StackingAction(G4UserStackingAction):

    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.data_buffer = app.data_buffer
        
        n = self.app.refractive_index
        self.cerenkov_threshold_e = G4ParticleDefinition.GetPDGMass(G4Electron.Electron())/GeV/np.sqrt(1.-1./n**2)

    def ClassifyNewTrack(self, track: G4Track):
        
        if track.GetDefinition().GetParticleType() == 'nucleus':
            return G4ClassificationOfNewTrack.fKill
        
        particle = track.GetDefinition()
        uid      = track.GetTrackID()
        Etot_GeV = track.GetTotalEnergy()/GeV
        
        if track.GetDefinition() == G4OpticalPhoton.OpticalPhoton():
            if self.app.ph_counter % self.app.ph_suppression_factor == 0:
                parent_uid = track.GetParentID()
                pos_m      = track.GetPosition()/m
                t_ns       = track.GetGlobalTime()/ns
                dir        = track.GetMomentumDirection()
                wl_nm      = 1.23984193*1.e-6/Etot_GeV # in nm
                #if parent_uid != 1: print(f"{time:.4f} photon    parent uid: {parent_uid}")
                self.data_buffer.photons = [parent_uid, pos_m, t_ns, dir, wl_nm]
            self.app.ph_counter += 1
            return G4ClassificationOfNewTrack.fKill
        elif Etot_GeV > self.app.E_skip_min and Etot_GeV <= self.app.E_skip_max and uid != 1 \
        and track.GetDefinition() in (G4Electron.Electron(), G4Positron.Positron()):
            parent_uid = track.GetParentID()
            pdgid = particle.GetPDGEncoding()
            pos_m = track.GetPosition()/m
            t_ns = track.GetGlobalTime()/ns
            dir = track.GetMomentumDirection()
            Etot_GeV = Etot_GeV
            step_length_m = track.GetStepLength()/m
            if self.app.save_process_name:
                process_name = track.GetCreatorProcess().GetProcessName()
                self.data_buffer.particles = [uid, parent_uid, pdgid, pos_m, t_ns,
                                              dir, Etot_GeV, process_name]
            else:
                self.data_buffer.particles = [uid, parent_uid, pdgid, pos_m, t_ns,
                                              dir, Etot_GeV]
            self.data_buffer.particles.counter += 1
            return G4ClassificationOfNewTrack.fKill
        elif Etot_GeV >= self.cerenkov_threshold_e and Etot_GeV >= self.app.E_lower_edge:
            parent_uid    = track.GetParentID()
            pdgid         = particle.GetPDGEncoding()
            pos_m         = track.GetPosition()/m
            t_ns          = track.GetGlobalTime()/ns
            Etot_GeV      = track.GetTotalEnergy()/GeV
            step_length_m = track.GetStepLength()/m
            if self.app.save_process_name:
                creator_process = track.GetCreatorProcess()
                if creator_process:
                    process_name = track.GetCreatorProcess().GetProcessName()
                else:
                    process_name = 'Init'
                self.data_buffer.tracks = [uid, parent_uid, pdgid, pos_m, t_ns,
                                           Etot_GeV, step_length_m, process_name]
            else:
                self.data_buffer.tracks = [uid, parent_uid, pdgid, pos_m, t_ns,
                                           Etot_GeV, step_length_m]
            return G4ClassificationOfNewTrack.fUrgent
        else:
            return G4ClassificationOfNewTrack.fKill