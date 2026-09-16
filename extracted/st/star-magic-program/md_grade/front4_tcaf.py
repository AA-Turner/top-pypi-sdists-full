"""front4_tcaf.py - FRONT 4 instrument (B286, PAPER_2281): the wavevector-
dependent shear viscosity eta(k) of liquid water from the transverse-current
autocorrelation (TCAF), graded against the framework's roll-off
    eta(k)/eta_0 = exp(-0.344 (k/k_c)^2),   a = 0.344/k_c^2 at small k,
for BOTH candidate k_c (Q-247): c_0 = 1480 m/s -> k_c = 5.307 nm^-1;
c_inf = 3200 m/s -> k_c = 2.454 nm^-1.

Why this and not "the transverse current integrated over omega": that
integral is C_T(k,0) = N k_B T / m for every k (equipartition) - flat by
identity. eta(k) is the fluid's transverse-momentum TRANSFER at k, the
observable the claim is about (PAPER_2281 sec 1).

Requirements: openmm >= 8 (pip install openmm), numpy. No token, no bench.
    python front4_tcaf.py --box 5.0 --prod-ps 400 --out front4_eta_k.csv
Runtime: ~1-3 h per 100 ps on 8 CPU cores for a 5 nm box (~4,200 waters);
a GPU (CUDA/OpenCL platform) is 20-50x faster. Start with --box 4 --prod-ps
100 to check the pipeline, then scale.

Method (gmx tcaf convention, Hess JCP 116, 209 (2002)):
  j_T(k,t) = sum_i m_i v_i,perp exp(i k.r_i) for k = (2 pi/L) n, n integer
  vectors; C_T(k,t) = <j_T(k,t) j_T*(k,0)> / <|j_T(k,0)|^2>; fit
  f(t) = exp(-v)(cosh(W v) + sinh(W v)/W), v = -t/(2 tau),
  W = sqrt(1 - 4 tau eta k^2 / rho) -> (tau, eta) per |k|;
  eta_0 from eta(k) = eta_0 (1 - a k^2) over the smallest k.
Output CSV columns: k_per_nm, eta_k (mPa s), eta_0 (mPa s, repeated),
n_kvec, tau_ps. The program's front4_grade_eta_k() grades it.
"""
import argparse, math, sys, time
import numpy as np

def build_water_box(box_nm, temperature_K):
    """TIP4P/2005 water box via OpenMM Modeller (parameters from Abascal &
    Vega, JCP 123, 234505 (2005)): O-H 0.9572 A, HOH 104.52 deg, O-M 0.1546 A,
    q_H = +0.5564, q_M = -1.1128, sigma_O = 3.1589 A, eps_O = 0.7749 kJ/mol."""
    import openmm as mm, openmm.app as app, openmm.unit as u
    # Write a minimal TIP4P/2005 force-field XML (OpenMM ships tip4pew/tip4pfb, not 2005)
    xml = """<ForceField>
 <AtomTypes>
  <Type name="tip4p2005-O" class="OW" element="O" mass="15.99943"/>
  <Type name="tip4p2005-H" class="HW" element="H" mass="1.007947"/>
  <Type name="tip4p2005-M" class="MW" mass="0"/>
 </AtomTypes>
 <Residues>
  <Residue name="HOH">
   <Atom name="O" type="tip4p2005-O"/><Atom name="H1" type="tip4p2005-H"/><Atom name="H2" type="tip4p2005-H"/>
   <Atom name="M" type="tip4p2005-M"/>
   <VirtualSite type="average3" siteName="M" atomName1="O" atomName2="H1" atomName3="H2" weight1="0.736124" weight2="0.131938" weight3="0.131938"/>
   <Bond atomName1="O" atomName2="H1"/><Bond atomName1="O" atomName2="H2"/>
  </Residue>
 </Residues>
 <HarmonicBondForce><Bond class1="OW" class2="HW" length="0.09572" k="462750.4"/></HarmonicBondForce>
 <HarmonicAngleForce><Angle class1="HW" class2="OW" class3="HW" angle="1.82421813418" k="836.8"/></HarmonicAngleForce>
 <NonbondedForce coulomb14scale="0.5" lj14scale="0.5">
  <Atom type="tip4p2005-O" charge="0" sigma="0.31589" epsilon="0.7749"/>
  <Atom type="tip4p2005-H" charge="0.5564" sigma="1" epsilon="0"/>
  <Atom type="tip4p2005-M" charge="-1.1128" sigma="1" epsilon="0"/>
 </NonbondedForce>
</ForceField>"""
    open('_tip4p2005.xml', 'w').write(xml)
    ff = app.ForceField('_tip4p2005.xml')
    # start from OpenMM's tip4pew water box and let the force field re-type it
    modeller = app.Modeller(app.Topology(), [])
    modeller.addSolvent(app.ForceField('tip4pew.xml'), model='tip4pew', boxSize=mm.Vec3(box_nm, box_nm, box_nm) * u.nanometer)
    system = ff.createSystem(modeller.topology, nonbondedMethod=app.PME, nonbondedCutoff=0.9 * u.nanometer,
                             constraints=app.AllBonds, rigidWater=True, ewaldErrorTolerance=1e-4)
    return modeller, system

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--box', type=float, default=5.0, help='cubic box edge, nm (>= 4; 8 for the full spec)')
    ap.add_argument('--T', type=float, default=298.0)
    ap.add_argument('--equil-ps', type=float, default=100.0)
    ap.add_argument('--prod-ps', type=float, default=400.0)
    ap.add_argument('--dt-fs', type=float, default=2.0)
    ap.add_argument('--sample-fs', type=float, default=20.0, help='j_T(k,t) sampling interval')
    ap.add_argument('--nmax', type=int, default=16, help='max integer k index per axis (k_max = 2 pi nmax / L)')
    ap.add_argument('--out', default='front4_eta_k.csv')
    ap.add_argument('--platform', default=None)
    a = ap.parse_args()
    import openmm as mm, openmm.app as app, openmm.unit as u
    modeller, system = build_water_box(a.box, a.T)
    L = a.box
    integrator = mm.LangevinMiddleIntegrator(a.T * u.kelvin, 1.0 / u.picosecond, a.dt_fs * u.femtosecond)
    plat = mm.Platform.getPlatformByName(a.platform) if a.platform else None
    sim = app.Simulation(modeller.topology, system, integrator, plat) if plat else app.Simulation(modeller.topology, system, integrator)
    sim.context.setPositions(modeller.positions)
    print('platform', sim.context.getPlatform().getName(), '| atoms', system.getNumParticles(), '| box', L, 'nm', flush=True)
    sim.minimizeEnergy(); sim.context.setVelocitiesToTemperature(a.T * u.kelvin)
    sim.step(int(a.equil_ps * 1000 / a.dt_fs)); print('equilibrated', a.equil_ps, 'ps', flush=True)
    # switch to NVE-like sampling: a weakly coupled thermostat perturbs TCAF little; keep Langevin gamma small
    integrator.setFriction(0.1 / u.picosecond)
    # k-vectors: all integer n with 1 <= |n| <= nmax, grouped by |n|^2; transverse projection via two perpendicular unit vectors
    masses = np.array([system.getParticleMass(i).value_in_unit(u.amu) for i in range(system.getNumParticles())])
    real = masses > 0
    nvecs = {}
    for nx in range(-a.nmax, a.nmax + 1):
        for ny in range(-a.nmax, a.nmax + 1):
            for nz in range(0, a.nmax + 1):
                n2 = nx * nx + ny * ny + nz * nz
                if n2 == 0 or n2 > a.nmax * a.nmax: continue
                if nz == 0 and (ny < 0 or (ny == 0 and nx < 0)): continue   # one of each +/- pair
                nvecs.setdefault(n2, []).append((nx, ny, nz))
    shells = sorted(nvecs)
    kvec = np.array([v for s in shells for v in nvecs[s]], float) * (2 * math.pi / L)   # nm^-1
    shell_of = np.array([s for s in shells for _ in nvecs[s]])
    # perpendicular unit vectors per k
    e1 = np.cross(kvec, np.where(np.abs(kvec[:, [2]]) < 0.9 * np.linalg.norm(kvec, axis=1, keepdims=True), [[0, 0, 1]], [[1, 0, 0]]))
    e1 /= np.linalg.norm(e1, axis=1, keepdims=True); e2 = np.cross(kvec, e1); e2 /= np.linalg.norm(e2, axis=1, keepdims=True)
    steps_per_sample = max(1, int(a.sample_fs / a.dt_fs)); nsamp = int(a.prod_ps * 1000 / a.sample_fs)
    J = np.zeros((nsamp, len(kvec), 2), complex)
    t0 = time.time()
    for s in range(nsamp):
        sim.step(steps_per_sample)
        st = sim.context.getState(getPositions=True, getVelocities=True)
        r = st.getPositions(asNumpy=True).value_in_unit(u.nanometer)[real]
        v = st.getVelocities(asNumpy=True).value_in_unit(u.nanometer / u.picosecond)[real]
        ph = np.exp(1j * (r @ kvec.T))                       # (N, K)
        mv = masses[real][:, None] * v                       # (N, 3)
        J[s, :, 0] = np.einsum('nk,nk->k', ph, mv @ e1.T)
        J[s, :, 1] = np.einsum('nk,nk->k', ph, mv @ e2.T)
        if s % 500 == 0: print('sample', s, '/', nsamp, '%.0f s' % (time.time() - t0), flush=True)
    dt = a.sample_fs / 1000.0   # ps
    nlag = min(nsamp // 4, int(20.0 / dt))                    # 20 ps of lag
    rho = masses[real].sum() / L ** 3                         # amu nm^-3; eta from the fit is then amu nm^-1 ps^-1
    rows = []
    for sidx, s in enumerate(shells):
        sel = shell_of == s; k = math.sqrt(s) * 2 * math.pi / L
        c = np.zeros(nlag)
        for comp in (0, 1):
            x = J[:, sel, comp]
            for lag in range(nlag):
                c[lag] += np.real(np.mean(np.sum(x[lag:] * np.conj(x[:nsamp - lag]), axis=1)))
        c /= c[0]
        t = np.arange(nlag) * dt
        # fit gmx tcaf form by least squares on (tau, eta)
        from scipy.optimize import least_squares
        def f(p):
            tau, eta = p; v_ = -t / (2 * tau); W2 = 1 - 4 * tau * eta * k * k / rho
            if W2 >= 0:
                W = math.sqrt(W2); m = np.exp(v_) * (np.cosh(W * v_) + np.sinh(W * v_) / W)
            else:
                W = math.sqrt(-W2); m = np.exp(v_) * (np.cos(W * v_) + np.sin(W * v_) / W)
            return m - c
        # initial guess: exponential decay rate nu k^2 with nu ~ 0.9 nm^2/ps (water)
        p0 = [0.2, 0.9 * rho]
        res = least_squares(f, p0, bounds=([1e-4, 1e-6], [50, 1e6]))
        tau, eta_amu = res.x
        eta_mPas = eta_amu * 1.66053907e-3                       # 1 amu nm^-1 ps^-1 = 1.66054e-6 Pa s = 1.66054e-3 mPa s
        rows.append((k, eta_mPas, int(sel.sum()), tau))
        print('|k| = %.3f nm^-1  eta = %.4f mPa s  tau = %.3f ps  (%d vectors)' % (k, eta_mPas, tau, sel.sum()), flush=True)
    # eta_0 from the smallest three shells: eta(k) = eta0 (1 - a k^2)
    ks = np.array([r[0] for r in rows[:3]]); es = np.array([r[1] for r in rows[:3]])
    A = np.vstack([np.ones_like(ks), -ks ** 2]).T; (eta0, eta0a), *_ = np.linalg.lstsq(A, es, rcond=None)
    a_nm2 = eta0a / eta0
    with open(a.out, 'w') as fh:
        fh.write('k_per_nm,eta_k,eta_0,n_kvec,tau_ps\n')
        for k, e, n, tau in rows: fh.write('%.5f,%.6f,%.6f,%d,%.5f\n' % (k, e, eta0, n, tau))
    print('\neta_0 = %.4f mPa s   small-k coefficient a = %.5f nm^2' % (eta0, a_nm2))
    print('framework prediction: a = 0.344/k_c^2 = 0.0122 nm^2 (c_0, k_c 5.31)  |  0.0570 nm^2 (c_inf, k_c 2.45)')
    print('wrote', a.out, '- grade with uqff_ns_assembly.front4_grade_eta_k()')

if __name__ == '__main__':
    main()
