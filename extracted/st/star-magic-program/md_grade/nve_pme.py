import numpy as np, time, sys
from md_pme import WaterPME
ns = int(sys.argv[1]) if len(sys.argv) > 1 else 13
w = WaterPME(ns, T=298.0, rc=0.9, seed=7, alpha=3.5, grid_spacing=0.1, order=4)
t0 = time.time()
w.run(400, dt=0.0005, tau_T=0.05); w.run(1500, dt=0.001, tau_T=0.1); w.run(3000, dt=0.002, tau_T=0.2)
print('equil %.0f s  T %.1f  E/N %.3f' % (time.time() - t0, w.temperature(), w.forces()[1] / w.N))
Es = []
def cb(step, E): Es.append(E + w.kinetic())
for dt in (0.002, 0.001):
    Es.clear(); w.run(int(2.0 / dt), dt=dt, callback=cb, cb_every=max(1, int(0.02 / dt)))
    Es_ = np.array(Es) / w.N; sl = np.polyfit(np.arange(len(Es_)) * 0.02, Es_, 1)[0]
    print('NVE dt=%.3f: 2 ps, dE_total/N = %+.4f kJ/mol (drift %+.4f kJ/mol/ps, std %.4f)  T %.1f' % (dt, Es_[-1] - Es_[0], sl, Es_.std(), w.temperature()))
print('E_pot/N %.3f  parts %s' % (w.forces()[1] / w.N, {k: round(v / w.N, 3) for k, v in w.E_parts.items()}))
