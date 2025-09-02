import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class BehaviorTreeModel:
    def __init__(self, weight_cluster_size=1.0, max_depth=None, random_state=42):
        self.weight_cluster_size = weight_cluster_size
        self.clf = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
        self.label_map = {0: "1-3", 1: "4-6", 2: "7-9", 3: "10+"}

    def load_data(self, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def clasificar_grupo(self, vac):
        if 1 <= vac <= 3:
            return 0
        elif 4 <= vac <= 6:
            return 1
        elif 7 <= vac <= 9:
            return 2
        else:
            return 3

    def prepare_features(self, df):
        X = df[['surface_area', 'filled_volume', 'cluster_size']].copy()
        X['cluster_size'] *= self.weight_cluster_size
        y = df['vacancys'].apply(self.clasificar_grupo)
        return X, y

    def train(self, json_path, test_size=0.3):
        df = self.load_data(json_path)
        X, y = self.prepare_features(df)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.clf.random_state)
        self.clf.fit(X_train, y_train)
        y_pred = self.clf.predict(X_test)
        print("Reporte de clasificación:")
        print(classification_report(y_test, y_pred, target_names=self.label_map.values()))
        return self

    def predict(self, surface_area, filled_volume, cluster_size):
        df_new = pd.DataFrame({
            'surface_area': surface_area,
            'filled_volume': filled_volume,
            'cluster_size': cluster_size
        })
        df_new['cluster_size'] *= self.weight_cluster_size
        y_pred = self.clf.predict(df_new)
        return [self.label_map[val] for val in y_pred]

    def classify_csv(self, csv_path, output_path=None):
        df = pd.read_csv(csv_path)

        required_cols = {'surface_area', 'filled_volume', 'cluster_size'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"El CSV debe contener las columnas: {required_cols}")

        X_new = df[['surface_area', 'filled_volume', 'cluster_size']].copy()
        X_new['cluster_size'] *= self.weight_cluster_size

        pred_numeric = self.clf.predict(X_new)
        df['grupo_predicho'] = [self.label_map[val] for val in pred_numeric]

        if output_path:
            df.to_csv(output_path, index=False)
            print(f"Archivo guardado en {output_path}")

        return df

    def feature_importances(self):
        return dict(zip(['surface_area', 'filled_volume', 'cluster_size'],
                        self.clf.feature_importances_))


