from geant4_pybind import *

class PrimaryGeneratorAction(G4VUserPrimaryGeneratorAction):
    
    def __init__(self, primary_generator, gun_args={}):
        super().__init__()
        if primary_generator == 'gps':
            self.particleGun = G4GeneralParticleSource()
        elif primary_generator == 'gun':
            nofParticles = 1
            self.particleGun = G4ParticleGun(nofParticles)
            gun_args = self.FillMissingGunParameters(gun_args)
            particle_table = G4ParticleTable.GetParticleTable()
            particleDefinition = particle_table.FindParticle(gun_args['particle'])
            self.particleGun.SetParticleDefinition(particleDefinition)
            self.particleGun.SetParticleMomentumDirection(G4ThreeVector(*gun_args['direction']))
            self.particleGun.SetParticlePosition(G4ThreeVector(*gun_args['position_m'])*m)
            self.particleGun.SetParticleEnergy(gun_args['energy_GeV']*GeV)
        else:
            sys.exit("Wrong primary generator type ({primary_generator}), it can be either 'gps' or 'gun'")
        
    def FillMissingGunParameters(self, gun_args):
        if 'particle' not in gun_args.keys():
            gun_args['particle'] = 'mu-'
        if 'energy_GeV' not in gun_args.keys():
            gun_args['energy_GeV'] = 100*GeV
        if 'position_m' not in gun_args.keys():
            gun_args['position_m'] = [0, 0, 0]
        if 'direction' not in gun_args.keys():
            gun_args['direction'] = [0, 0, 1]
        return gun_args
        
    def GeneratePrimaries(self, anEvent):
        # This function is called at the begining of event
        self.particleGun.GeneratePrimaryVertex(anEvent)

