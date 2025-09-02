import os
import csv
import numpy as np
import json

from vfscript.training.utils import resolve_input_params_path
class DumpProcessor:
    """
    Se encarga de leer un archivo .dump de LAMMPS, desplazar las coordenadas
    al centro de masa y devolver las normas de las coordenadas desplazadas.
    """
    def __init__(self, dump_path: str):
        self.dump_path = dump_path
        self.coords_originales = None      
        self.center_of_mass = None         
        self.coords_trasladadas = None    
        self.norms = None                 

    def read_and_translate(self):
        """
        Lee el archivo .dump y traslada las coordenadas de modo que el
        centro de masa quede en el origen. Guarda en los atributos:
          - self.coords_originales
          - self.center_of_mass
          - self.coords_trasladadas
        """
        if not os.path.isfile(self.dump_path):
            raise FileNotFoundError(f"No se encontró el archivo: {self.dump_path}")

        coords = []
        with open(self.dump_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        
        start_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("ITEM: ATOMS"):
                start_index = i + 1
                break

        if start_index is None:
            raise ValueError(f"No se encontró 'ITEM: ATOMS' en {self.dump_path}")

        
        for line in lines[start_index:]:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "ITEM:":
                break  
            if len(parts) < 5:
                continue
            try:
                x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                coords.append((x, y, z))
            except ValueError:
               
                continue

        if not coords:
            raise ValueError(f"No se hallaron coordenadas válidas tras 'ITEM: ATOMS' en {self.dump_path}")

        
        self.coords_originales = np.array(coords)
        com = tuple(self.coords_originales.mean(axis=0))
        self.center_of_mass = com

        
        self.coords_trasladadas = self.coords_originales - np.array(com)

    def compute_norms(self):
        """
        Calcula la norma de cada vector de coordenadas trasladadas.
        Debe llamarse después de read_and_translate().
        Guarda el resultado ordenado en self.norms (numpy array de tamaño N).
        """
        if self.coords_trasladadas is None:
            raise RuntimeError("Debes llamar primero a read_and_translate() antes de compute_norms().")

        
        self.norms = np.linalg.norm(self.coords_trasladadas, axis=1)
        
        self.norms = np.sort(self.norms)


class StatisticsCalculator:
    """
    Calcula un conjunto de estadísticas (min, max, mean, std, skewness, kurtosis,
    percentiles, IQR, histograma normalizado) sobre un array 1D de valores.
    """
    @staticmethod
    def compute_statistics(arr: np.ndarray) -> dict:
        stats = {}
        N = len(arr)
        stats['N'] = N

        if N == 0:
            
            stats.update({ 'mean': np.nan, 'std': np.nan,
                'skewness': np.nan, 'kurtosis': np.nan,
                'Q1': np.nan, 'median': np.nan, 'Q3': np.nan, 'IQR': np.nan
            })
            for i in range(1, 11):
                stats[f'hist_bin_{i}'] = 0.0
            return stats

        min_val = float(np.min(arr))
        max_val = float(np.max(arr))
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr, ddof=0))

        
        skew_val = float(np.mean(((arr - mean_val) / std_val) ** 3)) if std_val > 0 else 0.0
        
        kurt_val = float(np.mean(((arr - mean_val) / std_val) ** 4) - 3) if std_val > 0 else 0.0

        Q1 = float(np.percentile(arr, 25))
        med = float(np.percentile(arr, 50))
        Q3 = float(np.percentile(arr, 75))
        IQR = Q3 - Q1

        
        hist_counts, _ = np.histogram(arr, bins=10, range=(min_val, max_val))
        hist_norm = hist_counts / N 

        stats.update({
            'mean': mean_val,
            'std': std_val,
            'skewness': skew_val,
            'kurtosis': kurt_val,
            'Q1': Q1,
            'median': med,
            'Q3': Q3,
            'IQR': IQR
        })
        for i, h in enumerate(hist_norm, start=1):
            stats[f'hist_bin_{i}'] = float(h)

        return stats


class FeatureExporter:
    """
    Recorre una lista de archivos .dump, utiliza DumpProcessor para
    extraer normas y StatisticsCalculator para obtener estadísticas,
    y finalmente escribe un CSV con todas las características.
    """
    def __init__(self, dump_paths: list[str] = None, output_csv: str = "outputs/csv/finger_data.csv"):
        self.output_csv = output_csv

        # Cargar parámetros desde input_params.json
        json_params_path = resolve_input_params_path("input_params.json")
        with open(json_params_path, "r", encoding="utf-8") as f:
            all_params = json.load(f)

        if "CONFIG" not in all_params or not isinstance(all_params["CONFIG"], list) or len(all_params["CONFIG"]) == 0:
            raise KeyError("input_params.json debe contener la clave 'CONFIG' como lista no vacía.")
        
        config = all_params["CONFIG"][0]
        self.max_training_file_index = config["training_file_index"]

        # Si dump_paths no se pasa, lo generamos automáticamente
        if dump_paths is None:
            self.dump_paths = [
                f"outputs/dump/vacancy_{i}_training.dump"
                for i in range(1, self.max_training_file_index + 1)
            ]
        else:
            self.dump_paths = dump_paths


        

    def export(self):
        # Cabecera con primer campo renombrado a 'vacancys'
        header = [
            "vacancys", "N",  "mean", "std",
            "skewness", "kurtosis", "Q1", "median", "Q3", "IQR"
        ] + [f"hist_bin_{i}" for i in range(1, 11)]

        os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            # it arranca en 1 y cuenta hasta max_training_file_index
            it = 1
            for dump_path in self.dump_paths:
                if not os.path.isfile(dump_path):
                    print(f"⚠️ No se encontró {dump_path}, se salta.")
                    continue

                # Procesar normas y stats
                processor = DumpProcessor(dump_path)
                try:
                    processor.read_and_translate()
                    processor.compute_norms()
                except Exception as e:
                    print(f"❌ Error en {dump_path}: {e}")
                    continue

                stats = StatisticsCalculator.compute_statistics(processor.norms)

                # Preparo la fila: primer elemento = número de vacancias (it)
                row = [
                    it,
                    stats['N'],
                    stats['mean'],
                    stats['std'],
                    stats['skewness'],
                    stats['kurtosis'],
                    stats['Q1'],
                    stats['median'],
                    stats['Q3'],
                    stats['IQR']
                ] + [stats[f"hist_bin_{i}"] for i in range(1, 11)]

                writer.writerow(row)

                # Incremento y reseteo si supero el máximo
                it += 1
                if it > self.max_training_file_index:
                    it = 1


        print(f"Se generó el CSV con características en: {self.output_csv}")


#if __name__ == "__main__":
    #exporter = FeatureExporter()
    #exporter.export()
