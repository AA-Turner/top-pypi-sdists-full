from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Dict, Optional, List
import os
import glob
from pathlib import Path


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# seaborn es opcional; solo para el violín
try:
    import seaborn as sns
    _HAS_SNS = True
except Exception:
    _HAS_SNS = False


@dataclass
class GroupDef:
    name: str
    min_v: int
    max_v: Optional[int]  # None para 10+ (sin tope)


class GroupCoefficientCalculator:
    """
    coef(grupo) = mean(surface_area del grupo) / (menor número de vacancias del grupo)
    Grupos:
      1-3  -> min_v=1, max_v=3
      4-6  -> min_v=4, max_v=6
      7-9  -> min_v=7, max_v=9
      10+  -> min_v=10, max_v=None
    """

    GROUPS: Dict[str, GroupDef] = {
        "1-3": GroupDef("1-3", 1, 3),
        "4-6": GroupDef("4-6", 4, 6),
        "7-9": GroupDef("7-9", 7, 9),
        "10+": GroupDef("10+", 10, None),
    }

    def __init__(self, json_path: str = "outputs/json/training_graph.json"):
        self.json_path = json_path
        self.df: Optional[pd.DataFrame] = None

    # -------------------- Carga y preparación --------------------
    def load(self) -> pd.DataFrame:
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        for c in ("surface_area", "vacancys"):
            if c not in df.columns:
                raise ValueError(f"Falta la columna requerida '{c}' en el JSON.")

        df = df.dropna(subset=["surface_area", "vacancys"]).copy()
        df = df[df["vacancys"] > 0].copy()

        df["area_por_vacancia"] = df["surface_area"] / df["vacancys"]
        df["grupo"] = df["vacancys"].apply(self._clasificar_grupo)
        self.df = df
        return df

    @staticmethod
    def _clasificar_grupo(v: float) -> str:
        v = int(v)
        if 1 <= v <= 3:
            return "1-3"
        elif 4 <= v <= 6:
            return "4-6"
        elif 7 <= v <= 9:
            return "7-9"
        else:
            return "10+"

    # -------------------- Cálculo del coeficiente --------------------
    def compute_coefficients(self, use_observed_min_instead: bool = False) -> pd.DataFrame:
        """
        Devuelve DataFrame con:
          grupo, n_rows, mean_surface_area, min_divisor, coeficiente,
          mean_area_por_vacancia, std_area_por_vacancia
        """
        if self.df is None:
            self.load()

        rows = []
        for gname, gdef in self.GROUPS.items():
            gdf = self._slice_group(self.df, gdef)
            if gdf.empty:
                rows.append({
                    "grupo": gname,
                    "n_rows": 0,
                    "mean_surface_area": np.nan,
                    "min_divisor": gdef.min_v if not use_observed_min_instead else np.nan,
                    "coeficiente": np.nan,
                    "mean_area_por_vacancia": np.nan,
                    "std_area_por_vacancia": np.nan,
                })
                continue

            mean_sa = float(gdf["surface_area"].mean())
            min_div = int(gdf["vacancys"].min()) if use_observed_min_instead else gdef.min_v
            coef = mean_sa / min_div if min_div > 0 else np.nan

            rows.append({
                "grupo": gname,
                "n_rows": int(len(gdf)),
                "mean_surface_area": mean_sa,
                "min_divisor": int(min_div),
                "coeficiente": float(coef),
                "mean_area_por_vacancia": float(gdf["area_por_vacancia"].mean()),
                "std_area_por_vacancia": float(gdf["area_por_vacancia"].std(ddof=1)) if len(gdf) > 1 else 0.0,
            })

        out = pd.DataFrame(rows)
        order = ["1-3", "4-6", "7-9", "10+"]
        out["grupo"] = pd.Categorical(out["grupo"], categories=order, ordered=True)
        out = out.sort_values("grupo").reset_index(drop=True)
        return out

    def _slice_group(self, df: pd.DataFrame, g: GroupDef) -> pd.DataFrame:
        if g.max_v is None:
            return df[(df["vacancys"] >= g.min_v)]
        return df[(df["vacancys"] >= g.min_v) & (df["vacancys"] <= g.max_v)]

    # -------------------- Nueva funcionalidad: estimar por CSV --------------------
    def estimate_from_defect_csv(
        self,
        defect_csv_path: str = "outputs/csv/finger_data_clasificado.csv",
        group_col: Optional[str] = None,
        surface_area_col: str = "surface_area",
        out_path: Optional[str] = "outputs/csv/defect_data_estimated.csv",
        use_observed_min_instead: bool = False,
        round_mode: str = "ceil",  # "ceil" | "round" | "floor"
    ) -> pd.DataFrame:
        """
        Lee un CSV de defectos, usa el grupo de cada fila y el coeficiente del grupo
        para estimar el número de vacancias: vac_est = ceil(surface_area / coef_grupo)

        - Si el grupo no existe en el mapa de coeficientes, se intenta inferir por nombre.
        - Si un coeficiente está NaN (sin datos en entrenamiento), se usa fallback global:
            coef_fallback = mean(surface_area de TODO el dataset) / min_v_del_grupo
        - Se recorta el estimado al rango del grupo (1–3, 4–6, 7–9; 10+ solo mínimo 10).
        """
        # 1) Coeficientes por grupo
        coef_df = self.compute_coefficients(use_observed_min_instead=use_observed_min_instead)
        coef_map = {row["grupo"]: row["coeficiente"] for _, row in coef_df.iterrows()}

        # Fallback global si falta algún coef
        if self.df is None:
            self.load()
        global_mean_sa = float(self.df["surface_area"].mean())

        # 2) Leer CSV de defectos
        df = pd.read_csv(defect_csv_path)

        # Resolver columna de grupo si no se especifica
        candidate_cols: List[str] = [group_col] if group_col else [
            "grupo_predicho", "grupo", "Group", "label", "group"
        ]
        use_col = None
        for c in candidate_cols:
            if c and c in df.columns:
                use_col = c
                break
        if use_col is None:
            raise ValueError(
                f"No encontré columna de grupo. Probé: {candidate_cols}. "
                f"Pasá group_col='mi_columna' si el nombre es distinto."
            )
        if surface_area_col not in df.columns:
            raise ValueError(f"El CSV no tiene la columna '{surface_area_col}'.")

        # 3) Estimar por fila
        est_vals = []
        used_coefs = []
        clamped_vals = []
        min_bounds = []
        max_bounds = []

        for _, row in df.iterrows():
            g = str(row[use_col]).strip()
            sa = float(row[surface_area_col])

            # coef del grupo (con fallback)
            coef = coef_map.get(g, np.nan)
            if np.isnan(coef):
                # fallback: media global / min_v del grupo
                gdef = self.GROUPS.get(g)
                if gdef is None:
                    # intentar normalizar nombres como "10-plus", etc.
                    g = self._normalize_group_name(g)
                    gdef = self.GROUPS.get(g, GroupDef("10+", 10, None))
                coef = global_mean_sa / max(gdef.min_v, 1)
            used_coefs.append(coef)

            # estimación cruda
            raw_est = sa / coef if coef > 0 else np.nan

            # redondeo
            if round_mode == "ceil":
                vac_est = int(np.ceil(raw_est))
            elif round_mode == "floor":
                vac_est = int(np.floor(raw_est))
            else:
                vac_est = int(np.round(raw_est))

            # recorte al rango del grupo
            gdef = self.GROUPS.get(g, None)
            if gdef is None:
                g = self._normalize_group_name(g)
                gdef = self.GROUPS.get(g, GroupDef("10+", 10, None))

            lo = gdef.min_v
            hi = gdef.max_v if gdef.max_v is not None else None
            min_bounds.append(lo)
            max_bounds.append(hi if hi is not None else -1)

            if hi is None:
                vac_est_clamped = max(vac_est, lo)
            else:
                vac_est_clamped = min(max(vac_est, lo), hi)

            est_vals.append(vac_est)
            clamped_vals.append(vac_est_clamped)

        # 4) Salida
        df_out = df.copy()
        df_out["coef_grupo_usado"] = used_coefs
        df_out["vacancys_est_raw"] = est_vals
        df_out["vacancys_est"] = clamped_vals
        df_out["grupo_min_v"] = min_bounds
        df_out["grupo_max_v"] = max_bounds  # -1 indica "sin tope" (10+)

        if out_path:
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            df_out.to_csv(out_path, index=False)
            # print(f"✅ Guardado: {out_path}")

        return df_out

    @staticmethod
    def _normalize_group_name(g: str) -> str:
        g = g.strip().replace(" ", "")
        g = g.replace("to", "-").replace("+", "+").lower()
        # normalizaciones simples
        if g in {"1-3", "1–3", "1—3"}:
            return "1-3"
        if g in {"4-6", "4–6", "4—6"}:
            return "4-6"
        if g in {"7-9", "7–9", "7—9"}:
            return "7-9"
        if "10" in g:
            return "10+"
        return g

    # -------------------- Plots (opcionales) --------------------
    def plot_violin(self):
        if self.df is None:
            self.load()
        if not _HAS_SNS:
            raise RuntimeError("Seaborn no está disponible.")
        df = self.df

        grouped = df.groupby("vacancys")["area_por_vacancia"]
        stats = grouped.agg(["mean", "std"]).reset_index()
        stats["std"] = stats["std"].fillna(0)

        plt.figure(figsize=(10, 6))
        sns.violinplot(x="vacancys", y="area_por_vacancia", data=df, inner=None, color="lightblue")
        plt.errorbar(
            x=stats["vacancys"], y=stats["mean"], yerr=stats["std"],
            fmt="o", color="darkblue", ecolor="black",
            elinewidth=1.5, capsize=4, label="Media ± std"
        )
        plt.xlabel("Número de vacancias")
        plt.ylabel("Área de superficie por vacancia")
        plt.title("Distribución del área por vacancia (violín + media ± std)")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()
