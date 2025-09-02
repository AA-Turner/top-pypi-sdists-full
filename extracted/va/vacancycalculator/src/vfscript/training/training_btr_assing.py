import json, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.metrics import classification_report
import joblib

class ImprovedVacancyClassifier:
    def __init__(self, json_path, random_state=42):
        self.json_path = json_path
        self.random_state = random_state
        self.features = ['surface_area', 'filled_volume', 'cluster_size']
        self.label_map = {0:"1-3",1:"4-6",2:"7-9",3:"10+"}

        # Pipeline base
        self.pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', RandomForestClassifier(class_weight='balanced', random_state=self.random_state))
        ])

        # Distribución de búsqueda
        self.param_dist = {
            'clf__n_estimators': [50,100,200],
            'clf__max_depth': [None,10,20],
            'clf__min_samples_split': [2,5,10]
        }

    def load_and_prepare(self):
        data = json.load(open(self.json_path))
        df = pd.DataFrame(data)
        df['y'] = df['vacancys'].apply(self._clasificar)
        X = df[self.features]
        y = df['y']
        return X, y

    def _clasificar(self, vac):
        if 1<=vac<=3: return 0
        if 4<=vac<=6: return 1
        if 7<=vac<=9: return 2
        return 3

    def train(self):
        X, y = self.load_and_prepare()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=self.random_state
        )

        search = RandomizedSearchCV(
            self.pipe, self.param_dist,
            n_iter=20, cv=5, scoring='f1_macro',
            n_jobs=-1, random_state=self.random_state
        )
        search.fit(X_train, y_train)
        self.model = search.best_estimator_

        # Evaluar en test
        y_pred = self.model.predict(X_test)
        # print("==> Mejoros parámetros:")
        # print(search.best_params_)
        # print("\n==> Reporte en test:")
        # print(classification_report(y_test, y_pred, target_names=self.label_map.values()))

        # Guardar
        joblib.dump(self.model, "best_vacancy_model.pkl")

    def predict(self, X_new):
        numeric = self.model.predict(X_new)
        return [self.label_map[i] for i in numeric]
    def classify_csv(self, csv_path, output_path=None):
        """
        Lee un CSV con las columnas de features, predice el grupo y (opcionalmente)
        vuelca un nuevo CSV con la columna 'grupo_predicho'.
        """
        df = pd.read_csv(csv_path)
        missing = set(self.features) - set(df.columns)
        if missing:
            raise ValueError(f"Faltan columnas en el CSV: {missing}")

        X_new = df[self.features]
        pred_numeric = self.model.predict(X_new)
        df['grupo_predicho'] = [self.label_map[i] for i in pred_numeric]

        if output_path:
            df.to_csv(output_path, index=False)
            print(f"Archivo guardado en {output_path}")

        return df
