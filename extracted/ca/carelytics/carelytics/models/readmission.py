"""
models/readmission.py
---------------------
Predicts hospital readmission risk using Logistic Regression.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def predict_readmission(df, target="readmitted"):
    """
    Builds a simple logistic regression model to predict readmission risk.

    Parameters
    ----------
    df : pd.DataFrame
        Patient data with features and a 'readmitted' column.

    Returns
    -------
    float
        Model accuracy on test data.
    """
    features = ["age", "visits", "diagnoses_count"]
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"🧠 Readmission prediction accuracy: {acc:.2%}")
    return acc
