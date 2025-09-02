from ase.io.lammpsrun import read_lammps_dump
from scipy.spatial import cKDTree
import numpy as np

class DeformationAnalyzer:
    """
    Clase para calcular la métrica de deformación δ de una estructura atómica LAMMPS dump
    y decidir automáticamente si usar el método geométrico o el modelo de ML.
    """

    def __init__(self, dump_path: str, lattice_type: str, element: str, threshold: float = 0.02):
        """
        Parámetros:
        - dump_path: ruta al archivo LAMMPS dump defectuoso.
        - lattice_type: 'bcc' o 'fcc'.
        - element: símbolo del elemento (ej. 'Fe').
        - threshold: umbral δ para definir deformación alta.
        """
        self.dump_path = dump_path
        self.lattice_type = lattice_type.lower()
        self.element = element
        self.threshold = threshold

        # Cargar átomos
        self.atoms = read_lammps_dump(self.dump_path, index=-1)
        self.cell = self.atoms.get_cell()
        self.volume = self.cell.volume
        self.n_atoms = len(self.atoms)

        # Calcular parámetro de red y distancia ideal NN
        self.a = self._compute_lattice_parameter()
        self.d_ideal = self._compute_d_ideal()

    def _compute_lattice_parameter(self) -> float:
        """
        Calcula el parámetro de red 'a' estimado desde la densidad atómica.
        """
        natoms_per_cell = 2 if self.lattice_type == 'bcc' else 4
        density = self.n_atoms / self.volume
        unit_cell_volume = natoms_per_cell / density
        return unit_cell_volume ** (1/3)

    def _compute_d_ideal(self) -> float:
        """
        Calcula la distancia ideal al primer vecino para la red definida.
        """
        if self.lattice_type == 'bcc':
            return np.sqrt(3) / 2 * self.a
        elif self.lattice_type == 'fcc':
            return self.a / np.sqrt(2)
        else:
            raise ValueError("Tipo de red no reconocido: usar 'bcc' o 'fcc'.")

    def compute_metric(self) -> float:
        """
        Computa δ = σ_nn / d_ideal, donde σ_nn es la desviación estándar de las
        distancias al vecino más cercano.
        """
        positions = self.atoms.get_positions()
        tree = cKDTree(positions)
        dists, _ = tree.query(positions, k=2)
        nn_dists = dists[:, 1]  # descartamos la distancia cero a sí mismo
        sigma = np.std(nn_dists)
        return sigma / self.d_ideal

    def is_highly_deformed(self) -> bool:
        """
        Devuelve True si δ ≥ threshold, lo que indica muestra "muy deformada".
        """
        return self.compute_metric() >= self.threshold

    def select_method(self) -> str:
        """
        Retorna 'geometric' si la muestra está poco deformada (δ < threshold),
        o 'ml' si está muy deformada.
        """
        return 'ml' if self.is_highly_deformed() else 'geometric'

# Ejemplo de uso:
# analyzer = DeformationAnalyzer("inputs/fe6.dump", "bcc", "Fe", threshold=0.02)
# δ = analyzer.compute_metric()
# method = analyzer.select_method()
# print(f"Métrica δ = {δ:.4f}, método seleccionado: {method}")
