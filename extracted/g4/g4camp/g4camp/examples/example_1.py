from g4camp.g4camp import g4camp
from time import time
import sys

n_events = 10
gun_args = { 'particle':   'e-', 
             'energy_GeV': 100,
             'position_m': [0,0,10],
             'direction':  [0,0,1]  }
optics = True

sim = g4camp(primary_generator='gun', gun_args=gun_args, optics=optics)
sim.setSkipMinMax('fraction', 0.0, 0.01)
sim.setPhotonSuppressionFactor(100)
sim.configure()

time0 = time()
for data in sim.run(n_events):
    particles = data.particles
    tracks = data.tracks
    photons = data.photons
    print(f"{photons.counter:>10}(x{sim.ph_suppression_factor}) photons, {tracks.counter:>6} tracks, {particles.counter:>6} particles;")
print(f"# Run time:  {(time()-time0):.2f} sec, {((time()-time0)/n_events):.2f} sec/event")
