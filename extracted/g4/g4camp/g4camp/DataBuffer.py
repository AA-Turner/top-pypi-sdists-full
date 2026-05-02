from g4camp.IO.gParticles import gParticles
from g4camp.IO.gPhotons import gPhotons
from g4camp.IO.gTracks import gTracks

class DataBuffer():

    def __init__(self):

        self._particles = gParticles('g4_particles')
        self._photons   = gPhotons('g4_photons')
        self._tracks    = gTracks('g4_tracks')

    @property
    def particles(self):
        return self._particles

    @particles.setter
    def particles(self, new_particle: list):
        self._particles.set_data(*new_particle)

    @property
    def photons(self):
        return self._photons

    @photons.setter
    def photons(self, new_photon: list):
        self._photons.set_data(*new_photon)

    @property
    def tracks(self):
        return self._tracks

    @tracks.setter
    def tracks(self, new_track: list):
        self._tracks.set_data(*new_track)

    def clear(self) -> None:
        self.__init__()