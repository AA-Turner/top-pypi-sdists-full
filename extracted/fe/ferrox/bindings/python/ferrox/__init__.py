"""ferrox - High-performance atomistic simulation toolkit in Rust.

High-performance base layer for computational materials science. Batch operations
like structure matching/grouping achieve 10-100x speedups over pymatgen via
parallel Rayon processing. Features include I/O (CIF/POSCAR/extXYZ/LAMMPS),
structure matching, symmetry analysis, molecular dynamics, surface science,
defect engineering, trajectory analysis, and more.

## OOP API (recommended)

Core types are available as top-level classes with Pythonic interfaces:

- `ferrox.Element` - Periodic table element with properties
- `ferrox.Species` - Chemical species with optional oxidation state
- `ferrox.Composition` - Formula parsing, reduction, and analysis
- `ferrox.Lattice` - Crystallographic lattice with matrix operations
- `ferrox.Structure` - Crystal structure with symmetry, manipulation, and analysis
- `ferrox.StructureMatcher` - Structure comparison and deduplication

```python
from ferrox import Structure, Composition, Lattice, Element

# Create from prototype
nacl = Structure.from_prototype("rocksalt", ["Na", "Cl"], a=5.64)
print(nacl)  # Full Formula (Na4 Cl4) ...

# Composition analysis
comp = Composition("Fe2O3")
comp.reduced_formula  # 'Fe2O3'
comp.weight  # 159.69

# Lattice operations
lat = Lattice.cubic(5.0)
lat.volume  # 125.0
```

## Submodule Organization

Functions are also organized into submodules by domain (functional API):

- `ferrox.io` - Structure parsing and writing (CIF, POSCAR, XYZ, etc.)
- `ferrox.structure` - Structure manipulation (supercell, sort, interpolate, etc.)
- `ferrox.lattice` - Lattice operations (metric tensor, reduction, etc.)
- `ferrox.neighbors` - Neighbor lists and distance calculations
- `ferrox.coordination` - Coordination numbers and local environments
- `ferrox.composition` - Composition parsing and analysis
- `ferrox.symmetry` - Space groups, Wyckoff positions, symmetry operations
- `ferrox.defects` - Point defect generation and analysis
- `ferrox.surfaces` - Surface/slab operations, Miller indices, adsorption
- `ferrox.cell` - Cell operations (minimum image, reduction)
- `ferrox.elastic` - Elastic tensor calculations
- `ferrox.rdf` - Radial distribution functions
- `ferrox.xrd` - X-ray diffraction
- `ferrox.oxidation` - Oxidation state analysis
- `ferrox.convex_hull` - Convex hull and energy-above-hull calculations
- `ferrox.order_params` - Steinhardt order parameters
- `ferrox.trajectory` - Trajectory analysis (MSD, diffusion)
- `ferrox.md` - Molecular dynamics integrators
- `ferrox.potentials` - Classical interatomic potentials (LJ, Morse, etc.)
- `ferrox.optimizers` - Geometry optimizers (FIRE, CellFIRE)
- `ferrox.properties` - Physical property calculations (volume, density, mass)
- `ferrox.species` - Chemical species with oxidation states
- `ferrox.vasp` - VASP file support (CHGCAR parsing, Fourier extraction)
- `ferrox.mp` - Materials Project REST client (no mp_api dependency)
"""

# Top-level classes and submodules
from ferrox._ferrox import (
    Element,
    __version__,
    cell,
    composition,
    convex_hull,
    coordination,
    defects,
    elastic,
    io,
    lattice,
    md,
    neighbors,
    optimizers,
    order_params,
    oxidation,
    potentials,
    properties,
    rdf,
    species,
    structure,
    surfaces,
    symmetry,
    trajectory,
    vasp,
    xrd,
)
from ferrox._ferrox import mp as _mp_native

# Materials Project error classes (pure Python)
from ferrox.mp import MPClientError, MPDecodeError, MPHTTPError

# Rust-backed Materials Project clients
MPRester = _mp_native.MPRester
MPOpenData = _mp_native.MPOpenData

# OOP classes re-exported at top level for convenience
Composition = composition.Composition
Lattice = lattice.Lattice
Species = species.Species
Structure = structure.Structure
StructureMatcher = structure.StructureMatcher
