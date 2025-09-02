import json
import os
import joblib
import pandas as pd
from typing import List, Optional, Dict, Any
import numpy as np
from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, classification_report


class VacancyModelTrainer:
    """
    Pipeline:
      1) load_data(): carga JSON y crea df, con 'grupo' usando _clasificar_grupo (solo para entrenar).
      2) train_group_classifier(): entrena clasificador XGB para predecir grupo a partir de features.
      3) train_all_regressors(): entrena un regresor por grupo.
      4) predict_from_csv(): si el CSV NO trae 'grupo_predicho', lo clasifica con el clasificador y
         luego usa el regresor del grupo correspondiente para predecir 'vacancys'.
    """

    GROUPS = ['1-3', '4-6', '7-9', '10+']

    def __init__(
        self,
        json_path: Optional[str] = None,
        target: str = 'vacancys',
        features: Optional[List[str]] = None,
        models_dir: str = "."
    ):
        self.json_path = json_path
        self.target = target
        self.features = features or ['surface_area', 'filled_volume', 'cluster_size']
        self.models_dir = models_dir

        self.data: Optional[List[Dict[str, Any]]] = None
        self.df: Optional[pd.DataFrame] = None

        # Modelos
        self.group_clf: Optional[XGBClassifier] = None
        self.label_encoder: Optional[LabelEncoder] = None
        self.group_regressors: Dict[str, XGBRegressor] = {}

    # ---------------------------
    # Utils de paths
    # ---------------------------
    def _model_path_clf(self) -> str:
        return os.path.join(self.models_dir, "outputs/xgb_group_classifier.pkl")

    def _model_path_le(self) -> str:
        return os.path.join(self.models_dir, "outputs/xgb_group_labelencoder.pkl")

    def _model_path_reg(self, grupo: str) -> str:
        return os.path.join(self.models_dir, f"outputs/xgb_model_{grupo}.pkl")

    # ---------------------------
    # Carga de datos
    # ---------------------------
    def load_data(self):
        if not self.json_path:
            raise ValueError("Debes pasar json_path para cargar datos.")
        with open(self.json_path, 'r') as f:
            self.data = json.load(f)
        self.df = pd.DataFrame(self.data)

        # Validaciones básicas
        missing = [c for c in self.features + [self.target] if c not in self.df.columns]
        if missing:
            raise ValueError(f"Faltan columnas en el JSON: {missing}")

        # Grupo SOLO para entrenamiento (se usa el target real para etiquetar)
        self.df['grupo'] = self.df[self.target].apply(self._clasificar_grupo)
        #print(f"✅ Datos cargados: {len(self.df)} filas. Grupos: {self.df['grupo'].value_counts().to_dict()}")

    @staticmethod
    def _clasificar_grupo(vac: float) -> str:
        vac = int(vac)
        if 1 <= vac <= 3:
            return "1-3"
        elif 4 <= vac <= 6:
            return "4-6"
        elif 7 <= vac <= 9:
            return "7-9"
        else:
            return "10+"

    # ---------------------------
    # Entrenamiento
    # ---------------------------
    def train_group_classifier(self, test_size: float = 0.2, random_state: int = 42):
        """
        Clasificador para predecir 'grupo' desde features.
        """
        if self.df is None:
            raise RuntimeError("Primero ejecuta load_data().")

        X = self.df[self.features]
        y = self.df['grupo']

        self.label_encoder = LabelEncoder()
        y_enc = self.label_encoder.fit_transform(y)

        X_tr, X_te, y_tr, y_te = train_test_split(X, y_enc, test_size=test_size, random_state=random_state, stratify=y_enc)

        self.group_clf = XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective='multi:softprob',
            num_class=len(self.GROUPS),
            eval_metric='mlogloss',
            n_jobs=-1
        )
        self.group_clf.fit(X_tr, y_tr)

        # Evaluación rápida
        y_pred_enc = self.group_clf.predict(X_te)
        #print("✅ Clasificador de grupo entrenado:")
        ##print(classification_report(self.label_encoder.inverse_transform(y_te),
         #                          self.label_encoder.inverse_transform(y_pred_enc),
         #                          labels=self.GROUPS))

        # Guardar modelos del clasificador
        joblib.dump(self.group_clf, self._model_path_clf())
        joblib.dump(self.label_encoder, self._model_path_le())
        #print(f"💾 Clasificador guardado en: {self._model_path_clf()}")
        #print(f"💾 LabelEncoder guardado en: {self._model_path_le()}")

    def train_all_regressors(self, test_size: float = 0.2, random_state: int = 42, min_rows_per_group: int = 3):
        """
        Entrena un XGBRegressor por grupo.
        """
        if self.df is None:
            raise RuntimeError("Primero ejecuta load_data().")

        for grupo in self.GROUPS:
            df_g = self.df[self.df['grupo'] == grupo]
            if df_g.shape[0] < min_rows_per_group:
                print(f"⚠️ Grupo {grupo}: {df_g.shape[0]} filas (<{min_rows_per_group}). Se omite este regresor.")
                continue

            X = df_g[self.features]
            y = df_g[self.target]

            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size, random_state=random_state)

            reg = XGBRegressor(
                n_estimators=400,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.9,
                objective='reg:squarederror',
                n_jobs=-1
            )
            reg.fit(X_tr, y_tr)

            y_pred = reg.predict(X_te)
            mse = mean_squared_error(y_te, y_pred)
            #print(f"✅ Regresor grupo {grupo} entrenado. MSE: {mse:.4f}")

            self.group_regressors[grupo] = reg
            joblib.dump(reg, self._model_path_reg(grupo))
            #print(f"💾 Guardado: {self._model_path_reg(grupo)}")

        #print("✔️ Entrenamiento de regresores por grupo finalizado.")

    # ---------------------------
    # Carga de modelos ya guardados
    # ---------------------------
    def load_models_from_disk(self):
        clf_path = self._model_path_clf()
        le_path = self._model_path_le()
        if os.path.exists(clf_path) and os.path.exists(le_path):
            self.group_clf = joblib.load(clf_path)
            self.label_encoder = joblib.load(le_path)
            #print(f"📦 Clasificador cargado: {clf_path}")
        else:
            print("ℹ️ No se encontró clasificador/label encoder guardado.")

        self.group_regressors = {}
        for g in self.GROUPS:
            p = self._model_path_reg(g)
            if os.path.exists(p):
                self.group_regressors[g] = joblib.load(p)
                #print(f"📦 Regresor {g} cargado: {p}")

    # ---------------------------
    # Predicción helpers
    # ---------------------------
    def _infer_group(self, X_df: pd.DataFrame) -> pd.Series:
        if self.group_clf is None or self.label_encoder is None:
            raise RuntimeError("No hay clasificador cargado. Ejecuta train_group_classifier() o load_models_from_disk().")
        y_pred_enc = self.group_clf.predict(X_df[self.features])
        y_pred = self.label_encoder.inverse_transform(y_pred_enc)
        return pd.Series(y_pred, index=X_df.index, name="grupo_predicho")

    def _predict_with_group_regressor(self, grupo: str, X_row: pd.Series) -> float:
        # Asegurar el orden de features
        X = X_row[self.features].values.reshape(1, -1)
        path = self._model_path_reg(grupo)
        if grupo in self.group_regressors:
            reg = self.group_regressors[grupo]
        elif os.path.exists(path):
            reg = joblib.load(path)
            self.group_regressors[grupo] = reg
        else:
            raise FileNotFoundError(f"❌ No hay regresor entrenado para el grupo '{grupo}'. ({path})")
        return float(reg.predict(X)[0])

    # ---------------------------
    # API de predicción
    # ---------------------------
    def predict_single(self, sample_dict: Dict[str, Any], grupo_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Predice grupo (si no se indica) y luego vacancys con el regresor del grupo.
        """
        row = pd.Series(sample_dict)
        if not all(f in row.index for f in self.features):
            raise ValueError(f"Faltan features en sample_dict. Se requieren: {self.features}")

        if grupo_override is None:
            # inferimos grupo con el clasificador
            df_tmp = pd.DataFrame([row])
            grupo = self._infer_group(df_tmp).iloc[0]
        else:
            grupo = grupo_override

        pred = self._predict_with_group_regressor(grupo, row)
        return {"grupo_predicho": grupo, "predicted_vacancy": pred}

    def predict_from_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Si el CSV trae 'grupo_predicho', lo usa.
        Si no, infiere el grupo con el clasificador.
        Luego usa el regresor del grupo correspondiente para predecir.
        """
        df = pd.read_csv(csv_path)

        # Validar features
        missing = [c for c in self.features if c not in df.columns]
        if missing:
            raise ValueError(f"❌ El CSV debe contener las columnas: {self.features}. Faltan: {missing}")

        # Asegurar clasificador y regresores
        if self.group_clf is None or self.label_encoder is None:
            # intentar cargar
            self.load_models_from_disk()
        if self.group_clf is None or self.label_encoder is None:
            raise RuntimeError("No hay clasificador disponible. Entrena o carga modelos primero.")

        # Obtener/Inferir grupo
        if 'grupo_predicho' in df.columns:
            grupos = df['grupo_predicho'].astype(str)
            #print("ℹ️ Usando 'grupo_predicho' provisto en el CSV.")
        else:
            grupos = self._infer_group(df)
            df['grupo_predicho'] = grupos
            #print("🔎 Grupo inferido con el clasificador.")

        # Predicciones enrutadas por grupo
        preds: List[float] = []
        for idx, row in df.iterrows():
            g = str(row['grupo_predicho'])
            pred = np.ceil(self._predict_with_group_regressor(g, row))  # 🔼 siempre hacia arriba
            preds.append(pred)

        df['predicted_vacancy'] = preds
        #print("🔮 Predicciones completadas (primeras 5 filas):")
        #print(df[['grupo_predicho', 'predicted_vacancy']].head())
        return df


# if __name__ == "__main__":
#     trainer = VacancyModelTrainer(json_path="outputs/json/training_graph.json")
#     trainer.load_data()
#     trainer.train_group_classifier()
#     trainer.train_all_regressors()
#
#     # Predicción por CSV
#     out_df = trainer.predict_from_csv("mi_batch.csv")
#     out_df.to_csv("mi_batch_predicho.csv", index=False)
#     print("✅ Guardado mi_batch_predicho.csv")
