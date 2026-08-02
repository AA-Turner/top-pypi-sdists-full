"""
models/denial_prediction.py
---------------------------
Predicts claim denials using a simple decision tree classifier.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def predict_claim_denials(df, target="denied"):
    """
    Builds a decision tree model to predict claim denials.

    Parameters
    ----------
    df : pd.DataFrame
        Claims dataset with categorical and numeric columns.

    Returns
    -------
    float
        Model accuracy on test data.
    """
    features = ["payer_type", "amount", "claim_age_days"]
    X = pd.get_dummies(df[features], drop_first=True)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"💡 Claim denial prediction accuracy: {acc:.2%}")
    return acc
