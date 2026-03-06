"""ferrox - High-performance atomistic simulation toolkit in Rust.

High-performance base layer for computational materials science. Batch operations
like structure matching/grouping achieve 10-100x speedups over pymatgen via
parallel Rayon processing. Features include I/O (CIF/POSCAR/extXYZ/LAMMPS),
structure matching, symmetry analysis, molecular dynamics, surface science,
defect engineering, trajectory analysis, and more.

## Submodule Organization

Functions are organized into submodules by domain:

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
- `ferrox.mp` - Materials Project REST client (no mp_api dependency)

## Usage Example

```python
from ferrox import Element
from ferrox import io, structure, defects

# Parse a structure file
struct = io.parse_structure_file("POSCAR")

# Create a supercell
supercell = structure.make_supercell(struct, [[2, 0, 0], [0, 2, 0], [0, 0, 2]])

# Create a vacancy defect
defect = defects.create_vacancy(supercell, 0)
```
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
    xrd,
)
from ferrox._ferrox import mp as _mp_native

# Materials Project error classes (pure Python)
from ferrox.mp import MPClientError, MPDecodeError, MPHTTPError

# Rust-backed Materials Project clients
MPRester = _mp_native.MPRester
MPOpenData = _mp_native.MPOpenData

# Backward-compatible re-exports
Structure = structure.Structure
StructureMatcher = structure.StructureMatcher
