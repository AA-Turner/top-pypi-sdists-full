from ase.io.lammpsrun import read_lammps_dump
from ase.build import bulk
from ase import Atoms
from ase.io import write as ase_write
from ovito.io import import_file, export_file
from scipy.spatial import cKDTree
import numpy as np
import tempfile, os
from typing import List

class WSMet:
    """
    Clase para generar una red perfecta a partir de un dump defectuoso y detectar vacancias.
    """

    def __init__(self,
                 defect_dump_path: str,
                 lattice_type: str = 'bcc',
                 element: str = 'Fe',
                 tolerance: float = 0.5,
                 perfect_dump_path: str = 'inputs/red_perfecta.dump',
                 vacancies_xyz_path: str = 'vacancias_detectadas.xyz'):
        """
        Inicializa el analizador.

        Parámetros:
        - defect_dump_path: ruta al dump LAMMPS defectuoso.
        - lattice_type: 'bcc' o 'fcc'.
        - element: símbolo del elemento, e.g. 'Fe'.
        - tolerance: distancia umbral para detectar vacancias (Å).
        - perfect_dump_path: ruta de salida para el dump perfecto.
        - vacancies_xyz_path: ruta de salida para el xyz de vacancias.
        """
        self.defect_dump_path = defect_dump_path
        self.lattice_type = lattice_type.lower()
        self.element = element
        self.tolerance = tolerance
        self.perfect_dump_path = perfect_dump_path
        self.vacancies_xyz_path = vacancies_xyz_path

        # Cargar estructura defectuosa
        self.at_defect = read_lammps_dump(self.defect_dump_path, index=-1)

    def _compute_lattice_parameter(self, atoms: Atoms) -> float:
        """Calcula el parámetro de red a partir de la densidad atómica."""
        cell = atoms.get_cell()
        vol = cell.volume
        n = len(atoms)
        natoms_cell = 2 if self.lattice_type == 'bcc' else 4
        density = n / vol
        cell_vol = natoms_cell / density
        return cell_vol ** (1/3)

    def _compute_ideal_distance(self, a: float) -> float:
        """Calcula la distancia ideal al primer vecino en la red."""
        if self.lattice_type == 'bcc':
            return np.sqrt(3) / 2 * a
        elif self.lattice_type == 'fcc':
            return a / np.sqrt(2)
        else:
            raise ValueError("Tipo de red no reconocido: usar 'bcc' o 'fcc'.")

    def generate_perfect_atoms(self) -> Atoms:
        """Genera el objeto Atoms de la red perfecta sin vacancias."""
        # calcular parámetro de red
        a = self._compute_lattice_parameter(self.at_defect)
        # construir celda unitaria perfecta
        red_unit = bulk(name=self.element, crystalstructure=self.lattice_type, a=a, cubic=True)
        # repetir para llenar la celda original
        reps = np.ceil(self.at_defect.get_cell().lengths() / a).astype(int)
        red = red_unit * reps.tolist()
        # escalar y alinear
        red.set_cell(self.at_defect.get_cell(), scale_atoms=True)
        red.set_pbc([True, True, True])
        centro_def = np.mean(self.at_defect.get_positions(), axis=0)
        centro_red = np.mean(red.get_positions(), axis=0)
        red.translate(centro_def - centro_red)
        return red

    def export_perfect_dump(self, atoms_perfect: Atoms) -> None:
        """Exporta la estructura perfecta a un archivo LAMMPS dump usando OVITO."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as tmp:
            ase_write(tmp.name, atoms_perfect, format="xyz")
            tmp_path = tmp.name
        pipeline = import_file(tmp_path)
        export_file(pipeline, self.perfect_dump_path, "lammps/dump",
                    columns=["Particle Identifier","Particle Type","Position.X","Position.Y","Position.Z"])
        os.remove(tmp_path)

    def detect_vacancies(self, atoms_perfect: Atoms) -> List[np.ndarray]:
        """Detecta vacancias comparando la red perfecta con la defectuosa."""
        pos_perfect = atoms_perfect.get_positions()
        pos_defect = self.at_defect.get_positions()
        tree = cKDTree(pos_defect)
        vac_positions = []
        for pos in pos_perfect:
            dist, _ = tree.query(pos, k=1)
            if dist > self.tolerance:
                vac_positions.append(pos)
        # exportar XYZ si hay vacancias
        if vac_positions:
            vac_atoms = Atoms(positions=vac_positions,
                              symbols=[atoms_perfect[0].symbol]*len(vac_positions))
            vac_atoms.set_cell(atoms_perfect.get_cell())
            vac_atoms.set_pbc([True, True, True])
            ase_write(self.vacancies_xyz_path, vac_atoms)
        return vac_positions

    def run(self) -> List[np.ndarray]:
        """Ejecuta flujo completo: genera red perfecta, exporta .dump y detecta vacancias."""
        #print(f"🔧 Generando red perfecta para '{self.defect_dump_path}'")
        atoms_perfect = self.generate_perfect_atoms()
        #print(f"💾 Exportando red perfecta a '{self.perfect_dump_path}'")
        self.export_perfect_dump(atoms_perfect)
        print("🔍 Detectando vacancias...")
        vacs = self.detect_vacancies(atoms_perfect)
        print(f"✅ Vacancies encontradas: {len(vacs)}")
        return vacs

# Ejemplo de uso:
# analyzer = VacancyAnalyzer("inputs/void_15.dump", "bcc", "Fe", tolerance=0.5)
# vac_positions = analyzer.run()
