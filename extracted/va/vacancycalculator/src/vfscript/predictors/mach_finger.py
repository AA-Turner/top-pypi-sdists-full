import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class FingerprintVacancyAssigner:
    """
    Compara fingerprints desde un archivo query con una base de datos,
    asignando el número de vacancias directamente desde la columna 'vacancys'.
    """
    def __init__(self,
                 base_csv_path: str,
                 query_csv_path: str,
                 weight_N: float = 2.0):
        # Cargo ambos CSV
        self.df_base  = pd.read_csv(base_csv_path)
        self.df_query = pd.read_csv(query_csv_path)
        self.weight_N = weight_N

        # Me aseguro de que exista la columna 'vacancys'
        if 'vacancys' not in self.df_base.columns:
            raise KeyError("El CSV base debe contener la columna 'vacancys'.")

        # Columnas de features: histogramas + estadísticos + N
        self.feature_cols = (
            [c for c in self.df_base.columns if c.startswith("hist_bin_")] +
            ["mean", "std", "skewness", "kurtosis", "Q1", "median", "Q3", "IQR", "N"]
        )
        # Verifico que existan en ambos
        for col in self.feature_cols:
            if col not in self.df_base.columns or col not in self.df_query.columns:
                raise KeyError(f"Falta la columna '{col}' en alguno de los CSVs.")

    def assign(self) -> pd.DataFrame:
        """
        Para cada fila de df_query, busca el índice de la fila más
        similar en df_base y copia su valor 'vacancys'.
        """
        # Preparo las matrices
        Xb = self.df_base[self.feature_cols].copy()
        Xq = self.df_query[self.feature_cols].copy()

        # Aplico peso a N
        Xb["N"] *= self.weight_N
        Xq["N"] *= self.weight_N

        Xq_clean = Xq.fillna(0)
        Xb_clean = Xb.fillna(0)
        sim = cosine_similarity(Xq_clean.values, Xb_clean.values)

        best_idx = sim.argmax(axis=1)

        # Extraigo vacancys directamente
        matched_vac = self.df_base.iloc[best_idx]["vacancys"].values

        # Agrego columna al query
        self.df_query["assigned_vacancies"] = matched_vac
        return self.df_query
