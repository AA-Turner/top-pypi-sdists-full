import json
import os
import csv
import numpy as np

from vfscript.training.utils import resolve_input_params_path
from vfscript.training.training_fingerstyle import DumpProcessor, StatisticsCalculator  # o usa tu import local

class ClusterFeatureExporter:
    def __init__(self, json_path: str, output_csv: str = "outputs/csv/finger_key_files.csv"):
        self.json_path = json_path
        self.output_csv = output_csv
        self.dump_paths = self._load_cluster_paths()

    def _load_cluster_paths(self):
        if not os.path.isfile(self.json_path):
            raise FileNotFoundError(f"No se encontró el archivo JSON: {self.json_path}")

        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'clusters_final' not in data:
            raise KeyError("El JSON debe contener la clave 'clusters_final' con una lista de rutas .dump")

        return data['clusters_final']

    def export(self):
        header = [
            "file_name", "N",  "mean", "std",
            "skewness", "kurtosis", "Q1", "median", "Q3", "IQR"
        ] + [f"hist_bin_{i}" for i in range(1, 11)]

        os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)

        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for dump_path in self.dump_paths:
                if not os.path.isfile(dump_path):
                    print(f"⚠️ No se encontró {dump_path}, se salta.")
                    continue

                processor = DumpProcessor(dump_path)
                try:
                    processor.read_and_translate()
                    processor.compute_norms()
                except Exception as e:
                    print(f"❌ Error procesando {dump_path}: {e}")
                    continue

                norms = processor.norms
                stats = StatisticsCalculator.compute_statistics(norms)

                file_name = os.path.basename(dump_path)
                row = [
                    file_name,
                    stats['N'],
                    stats['mean'],
                    stats['std'],
                    stats['skewness'],
                    stats['kurtosis'],
                    stats['Q1'],
                    stats['median'],
                    stats['Q3'],
                    stats['IQR']
                ]
                row += [stats[f"hist_bin_{i}"] for i in range(1, 11)]

                writer.writerow(row)

        print(f"✅ CSV generado: {self.output_csv}")

