import os
import json
from vfscript.training.utils import resolve_input_params_path

from ovito.io import import_file, export_file
from ovito.modifiers import (
    ExpressionSelectionModifier,
    InvertSelectionModifier,
    DeleteSelectedModifier
)
import numpy as np
from scipy.spatial import ConvexHull

class HSM:
    """
    Lee un dump de LAMMPS, centra las coordenadas, calcula hull y genera expresión Ovito.
    Puede aplicar la expresión a un dump de referencia.
    """
    def __init__(self, dump_path: str):
        self.dump_path = resolve_input_params_path(dump_path)
        self.coords_originales = None
        self.center_of_mass = None
        self.coords_trasladadas = None
        self.norms = None
        self.ovito_expr = None

    def read_and_translate(self):
        """
        Carga el dump y centra las coordenadas en el centro de masa.
        """
        if not os.path.isfile(self.dump_path):
            raise FileNotFoundError(f"No se encontró el archivo: {self.dump_path}")

        coords = []
        with open(self.dump_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        start_index = next((i for i, line in enumerate(lines)
                            if line.strip().startswith("ITEM: ATOMS")), None)
        if start_index is None:
            raise ValueError(f"No se encontró 'ITEM: ATOMS' en {self.dump_path}")

        for line in lines[start_index+1:]:
            parts = line.split()
            if not parts or parts[0] == "ITEM:":
                break
            if len(parts) < 5:
                continue
            try:
                x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                coords.append((x, y, z))
            except ValueError:
                continue

        if not coords:
            raise ValueError(f"No halló coordenadas tras 'ITEM: ATOMS' en {self.dump_path}")

        self.coords_originales = np.array(coords)
        self.center_of_mass = self.coords_originales.mean(axis=0)
        self.coords_trasladadas = self.coords_originales - self.center_of_mass
        self.norms = np.linalg.norm(self.coords_trasladadas, axis=1)

    def compute_hull_expression(self, strict: bool = True) -> str:
        """
        Genera expresión Ovito a partir del ConvexHull.
        strict=True usa < y > en lugar de <= y >=.
        """
        if self.coords_originales is None:
            raise RuntimeError("Debe llamar a read_and_translate() primero")

        hull = ConvexHull(self.coords_originales)
        conditions = []
        seen = set()

        for a, b, c, d in hull.equations:
            if abs(c) < 1e-8:
                continue
            key = tuple(np.round([a, b, c, d], 6))
            if key in seen:
                continue
            seen.add(key)

            coef_x = -a / c
            coef_y = -b / c
            const = -d / c
            rhs = f"({coef_x:.6f})*Position.X + ({coef_y:.6f})*Position.Y + ({const:.6f})"

            if strict:
                cond = f"Position.Z <= 2*{rhs}" if c > 0 else f"Position.Z >= 2*{rhs}"
            else:
                cond = f"Position.Z <= 2*{rhs}" if c > 0 else f"Position.Z >= 2*{rhs}"

            conditions.append(cond)

        self.ovito_expr = " && ".join(conditions)
        return self.ovito_expr

    def apply_to_reference(self, ref_dump_path: str, output_path: str):
        """
        Aplica la expresión Ovito a un dump de referencia y exporta el resultado.
        """
        if self.ovito_expr is None:
            raise RuntimeError("Debe llamar a compute_hull_expression() primero")

        ref_path = resolve_input_params_path(ref_dump_path)
        pipeline = import_file(ref_path)
        pipeline.modifiers.append(
            ExpressionSelectionModifier(expression=self.ovito_expr)
        )
        pipeline.modifiers.append(InvertSelectionModifier())
        pipeline.modifiers.append(DeleteSelectedModifier())

        export_file(
            pipeline,
            output_path,
            'lammps/dump',
            columns=[
                'Particle Identifier', 'Particle Type',
                'Position.X', 'Position.Y', 'Position.Z'
            ]
        )
    def filter(self):
        self.coords_originales

# ——————————————
# Bloque principal
# ——————————————
#if __name__ == "__main__":
    # 1) Leer JSON con rutas de dumps
    #key_file = resolve_input_params_path('outputs/json/key_archivos.json')
    #with open(key_file, 'r', encoding='utf-8') as jf:
        #config = json.load(jf)

    #cluster_files = config.get('clusters_final', [])
    #ref_file = config['defect']  # tu red de referencia

    #for cluster_path in cluster_files:
        # Nombre base para salida
        #base = os.path.splitext(os.path.basename(cluster_path))[0]
        #out_dump = f'outputs/dump/{base}_inside.dump'

        # Procesar cada dump
        #proc = HSM(cluster_path)
        #proc.read_and_translate()
        #expr = proc.compute_hull_expression(strict=True)
        #print(f"Expresión para {cluster_path}:\n{expr}\n")
        #proc.apply_to_reference(ref_file, out_dump)
        #print(f"→ Dump filtrado escrito en: {out_dump}\n")
