regression_forecasting_metric_options = [
    ["rmse", "Root mean squared error."],
    ["mae", "mean absolute error."],
]

classification_forecasting_metric_options = [
    ["log_loss", "Default metric for multiclass classification."],
    ["accuracy", "1 - accuracy as the corresponding metric to minimize."],
    ["roc_auc", "Minimize 1 - roc_auc_score. Default metric for binary classification."],
    ["roc_auc_weighted", """Minimize 1 - roc_auc_score with average="weighted"."""],
    ["f1", "Minimize 1 - f1_score."],
    ["micro_f1", """Minimize 1 - f1_score with average="micro"."""],
    ["macro_f1", """Minimize 1 - f1_score with average="macro"."""],
]

# See: https://microsoft.github.io/FLAML/docs/Use-Cases/Task-Oriented-AutoML#estimator-and-search-space
hyperparameters = [
    {
        "id": "lgbm",
        "name": "LGBMEstimator",
        "tasks": ["classification", "regression", "rank", "ts_forecast", "ts_forecast_classification"],
        "hyper-parameters": {
            "n_estimators": {"type": "int"},
            "num_leaves": {"type": "int"},
            "min_child_samples": {"type": "int"},
            "learning_rate": {"type": "float"},
            "log_max_bin": {"type": "int"},
            "colsample_bytree": {"type": "float"},
            "reg_alpha": {"type": "float"},
            "reg_lambda": {"type": "float"},
        },
        "hyper-meta": {"log_max_bin": {"comment": "(logarithm of (max_bin + 1) with base 2)"}},
    },
    {
        "id": "xgboost",
        "name": "XGBoostSkLearnEstimator",
        "tasks": ["classification", "regression", "rank", "ts_forecast", "ts_forecast_classification"],
        "hyper-parameters": {
            "n_estimators": {"type": "int"},
            "max_leaves": {"type": "int"},
            "min_child_weight": {"type": "float"},
            "learning_rate": {"type": "float"},
            "subsample": {"type": "float"},
            "colsample_bylevel": {"type": "float"},
            "colsample_bytree": {"type": "float"},
            "reg_alpha": {"type": "float"},
            "reg_lambda": {"type": "float"},
        },
    },
    {
        "id": "xgb_limitdepth",
        "name": "XGBoostLimitDepthEstimator",
        "tasks": ["classification", "regression", "rank", "ts_forecast", "ts_forecast_classification"],
        "hyper-parameters": {
            "n_estimators": {"type": "int"},
            "max_depth": {"type": "int"},
            "min_child_weight": {"type": "float"},
            "learning_rate": {"type": "float"},
            "subsample": {"type": "float"},
            "colsample_bylevel": {"type": "float"},
            "colsample_bytree": {"type": "float"},
            "reg_alpha": {"type": "float"},
            "reg_lambda": {"type": "float"},
        },
    },
    {
        "id": "rf",
        "name": "RandomForestEstimator",
        "tasks": ["classification", "regression", "ts_forecast", "ts_forecast_classification"],
        "hyper-parameters": {
            "n_estimators": {"type": "int"},
            "max_features": {"type": ["sqrt", "log2", "None"]},
            "max_leaves": {"type": "int"},
            "criterion": {"type": ["gini" "entropy" "log_loss"]},
        },
        "hyper-meta": {"criterion": {"tasks": ["classification"]}},
        "extra": "Starting from v1.1.0, it uses a fixed random_state by default.",
    },
    {
        "id": "extra_tree",
        "name": "ExtraTreesEstimator",
        "tasks": ["classification", "regression", "ts_forecast", "ts_forecast_classification"],
        "hyper-parameters": {
            "n_estimators": {"type": "int"},
            "max_features": {"type": ["sqrt", "log2", "None"]},
            "max_leaves": {"type": "int"},
            "criterion": {"type": ["gini" "entropy" "log_loss"]},
        },
        "hyper-meta": {"criterion": {"tasks": ["classification"]}},
        "extra": "Starting from v1.1.0, it uses a fixed random_state by default.",
    },
    {
        "id": "lrl1",
        "readable_name": "logistic regression L1",
        "name": "LRL1Classifier (sklearn.LogisticRegression with L1 regularization)",
        "tasks": ["classification"],
        "hyper-parameters": {
            "C": {"type": "float"},
        },
    },
    {
        "id": "lrl2",
        "readable_name": "logistic regression L2",
        "name": "LRL2Classifier (sklearn.LogisticRegression with L2 regularization)",
        "tasks": ["classification"],
        "hyper-parameters": {
            "C": {"type": "float"},
        },
    },
    {
        "id": "catboost",
        "name": "CatBoostEstimator",
        "tasks": ["classification", "regression"],
        "hyper-parameters": {
            "early_stopping_rounds": {"type": "int"},
            "learning_rate": {"type": "float"},
            "n_estimators": {"type": "int"},
        },
    },
    {
        "id": "kneighbor",
        "name": "KNeighborsEstimator",
        "tasks": ["classification", "regression"],
        "hyper-parameters": {
            "n_neighbors": {"type": "int"},
        },
    },
    {
        "id": "prophet",
        "name": "Prophet",
        "tasks": ["ts_forecast"],
        "hyper-parameters": {
            "changepoint_prior_scale": {"type": "float"},
            "seasonality_prior_scale": {"type": "float"},
            "holidays_prior_scale": {"type": "float"},
            "seasonality_mode": {"type": ["additive", "multiplicative"]},
        },
    },
    {
        "id": "arima",
        "name": "ARIMA",
        "tasks": ["ts_forecast"],
        "hyper-parameters": {
            "p": {"type": "int"},
            "d": {"type": "int"},
            "q": {"type": "int"},
        },
    },
    {
        "id": "sarimax",
        "name": "SARIMAX",
        "tasks": ["ts_forecast"],
        "hyper-parameters": {
            "p": {"type": "int"},
            "d": {"type": "int"},
            "q": {"type": "int"},
            "P": {"type": "int"},
            "D": {"type": "int"},
            "Q": {"type": "int"},
            "s": {"type": "int"},
        },
    },
    {
        "id": "transformer",
        "name": "Huggingface transformer models",
        "tasks": ["seq-classification", "seq-regression", "multichoice-classification", "token-classification", "summarization"],
        "hyper-parameters": {
            "learning_rate": {"type": "float"},
            "num_train_epochs": {"type": "int"},
            "per_device_train_batch_size": {"type": "int"},
            "warmup_ratio": {"type": "float"},
            "weight_decay": {"type": "float"},
            "adam_epsilon": {"type": "float"},
            "seed": {"type": "int"},
        },
    },
    {
        "id": "temporal_fusion_transformer",
        "name": "TemporalFusionTransformerEstimator",
        "tasks": ["ts_forecast_panel"],
        "hyper-parameters": {
            "gradient_clip_val": {"type": "float"},
            "hidden_size": {"type": "int"},
            "hidden_continuous_size": {"type": "int"},
            "attention_head_size": {"type": "int"},
            "dropout": {"type": "float"},
            "learning_rate": {"type": "float"},
        },
        "extra": "There is a known issue with pytorch-forecast logging.",
    },
]


def get_estimator_ids_for_task(task):
    return [item["id"] for item in hyperparameters if task in item["tasks"]]


def get_hyper_parameters_for_task(estimator, task):
    def valid(param):
        for_tasks = estimator.get("hyper-meta", {}).get(param, {}).get("tasks")
        return for_tasks is None or task in for_tasks

    return [param for param in estimator["hyper-parameters"].keys() if valid(param)]
