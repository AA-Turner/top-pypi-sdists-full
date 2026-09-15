"""kt_stage2_cutouts.py - STAGE 2 of the kill test (B282): full-resolution
cutouts around the most intense sampled events, graded by the 1182-form
statistic with the LOCAL maximum (the sub-volume's own ||omega||_inf).

Run on SciServer (Compute -> container with the Turbulence data volume) or
on a local machine with `pip install givernylocal` (local GetCutout cap 3 GB;
SciServer 16 GB). ONE request at a time (JHTDB policy). Token from the
environment, never from a file that could be committed:

    export JHTDB_TOKEN=...            # your personal token
    python kt_stage2_cutouts.py hotspots.tsv isotropic8192 1 256

hotspots.tsv: one line per event, "x<TAB>y<TAB>z" in radians (the stage-1
top-K coordinates). For each event a cube of `nbox`^3 grid points centred
on it is pulled (velocity, raw grid, no interpolation), the gradient is
taken by 4th-order central differences ON THE GRID (so the statistic is
the true local field, not an interpolant), and the box is graded:

    ratio_local = mean(omega.S.omega) / (max|omega| * mean|omega|^2)   [1182 form, box max]
    peak_local  = (omega.S.omega / |omega|^3) at the box's peak-enstrophy cell
    eff(oct)    = sum(omega.S.omega) / (sum|omega|^2 * sqrt(w2_oct))   per enstrophy octave

Output: kt_stage2_<dataset>_t<t>.csv (one row per box + one per octave) and a
provenance JSON with request sizes and timings. The cap is killed if ANY
box returns ratio_local > 0.85 (vacuum branch) - and the paper must then
say so; the program's harness `grade_cap_against_dns` re-grades the CSV.
"""
import csv, json, os, sys, time
import numpy as np

TOKEN = os.environ.get('JHTDB_TOKEN')
if not TOKEN:
    sys.exit('set JHTDB_TOKEN in the environment (never in a tracked file)')

GRID = {'isotropic8192': 8192, 'isotropic32768': 32768, 'isotropic4096': 4096,
        'isotropic1024coarse': 1024, 'channel': (2048, 512, 1536), 'channel5200': (10240, 1536, 7680)}

def getcutout(dataset, t, x0, y0, z0, n):
    """Raw gridded velocity cube via giverny (SciServer) or givernylocal."""
    try:
        from giverny.turbulence_dataset import turb_dataset
        from giverny.turbulence_toolkit import getCutout
    except ImportError:
        from givernylocal.turbulence_dataset import turb_dataset
        from givernylocal.turbulence_toolkit import getCutout
    ds = turb_dataset(dataset_title=dataset, output_path='./kt_cutouts', auth_token=TOKEN)
    axes = [[x0, x0 + n - 1], [y0, y0 + n - 1], [z0, z0 + n - 1]]
    return getCutout(ds, 'velocity', t, axes, strides=[1, 1, 1])  # xarray (nz, ny, nx, 3)

def grade_box(u, dx):
    """u: (n, n, n, 3) velocity on a uniform grid; 4th-order central differences."""
    def d(f, ax):
        return (-np.roll(f, -2, ax) + 8 * np.roll(f, -1, ax) - 8 * np.roll(f, 1, ax) + np.roll(f, 2, ax)) / (12 * dx)
    # interior only (drop 2-cell halo where roll wraps)
    g = np.empty(u.shape[:3] + (3, 3))
    for i in range(3):
        for j, ax in enumerate((2, 1, 0)):  # d/dx, d/dy, d/dz with array order (z, y, x)
            g[..., i, j] = d(u[..., i], ax)
    g = g[2:-2, 2:-2, 2:-2]
    S = 0.5 * (g + np.swapaxes(g, -1, -2))
    ox = g[..., 2, 1] - g[..., 1, 2]; oy = g[..., 0, 2] - g[..., 2, 0]; oz = g[..., 1, 0] - g[..., 0, 1]
    om = np.stack([ox, oy, oz], -1)
    w2 = (om ** 2).sum(-1)
    st = np.einsum('...i,...ij,...j->...', om, S, om)
    mean_w2, max_w2, mean_st = w2.mean(), w2.max(), st.mean()
    ratio_local = mean_st / (np.sqrt(max_w2) * mean_w2)
    k = np.unravel_index(np.argmax(w2), w2.shape)
    peak_local = st[k] / w2[k] ** 1.5
    octs = {}
    b = np.floor(np.log2(w2 / mean_w2)).astype(int)
    for o in range(int(b.min()), int(b.max()) + 1):
        m = b == o
        if m.sum():
            octs[o] = dict(n=int(m.sum()), eff=float(st[m].sum() / (w2[m].sum() * np.sqrt(w2[m].mean()))))
    return dict(mean_w2=float(mean_w2), max_w2=float(max_w2), mean_st=float(mean_st),
                ratio_local=float(ratio_local), peak_local=float(peak_local),
                pos_frac=float((st > 0).mean()), cells=int(w2.size), octaves=octs)

def main():
    hot, dataset, t, nbox = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
    N = GRID[dataset]; L = 2 * np.pi; dx = L / N
    rows, prov = [], []
    for line in open(hot):
        if not line.strip():
            continue
        x, y, z = map(float, line.split())
        ix, iy, iz = [int(round(v / dx)) - nbox // 2 for v in (x, y, z)]
        t0 = time.time()
        cube = getcutout(dataset, t, ix % N, iy % N, iz % N, nbox)
        u = np.asarray(cube).reshape(nbox, nbox, nbox, 3)
        prov.append(dict(xyz=[x, y, z], origin=[ix % N, iy % N, iz % N], nbox=nbox, bytes=int(u.nbytes), s=round(time.time() - t0, 1)))
        r = grade_box(u, dx); r.update(xyz=f'{x} {y} {z}'); rows.append(r)
        print(f'{x:.5f} {y:.5f} {z:.5f}  ratio_local {r["ratio_local"]:.5f}  peak_local {r["peak_local"]:.4f}  max_w2 {r["max_w2"]:.4g}  cells {r["cells"]}', flush=True)
        time.sleep(2)  # sequential, polite
    out = f'kt_stage2_{dataset}_t{t:g}.csv'
    with open(out, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['xyz', 'cells', 'mean_w2', 'max_w2', 'mean_st', 'ratio_local', 'peak_local', 'pos_frac'])
        for r in rows:
            w.writerow([r['xyz'], r['cells'], r['mean_w2'], r['max_w2'], r['mean_st'], r['ratio_local'], r['peak_local'], r['pos_frac']])
        w.writerow([]); w.writerow(['xyz', 'octave', 'n', 'eff'])
        for r in rows:
            for o, v in sorted(r['octaves'].items()):
                w.writerow([r['xyz'], o, v['n'], v['eff']])
    json.dump(prov, open(out.replace('.csv', '_provenance.json'), 'w'), indent=1)
    worst = max(r['ratio_local'] for r in rows)
    print(f'\n{len(rows)} boxes graded; worst ratio_local {worst:.5f}  ->  {"CAP IS DEAD" if worst > 0.85 else "CAP HOLDS (local max)"}')

if __name__ == '__main__':
    main()
