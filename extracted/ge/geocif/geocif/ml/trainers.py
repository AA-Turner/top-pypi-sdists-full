import multiprocessing as mp

import numpy as np
import pandas as pd
import optuna
from catboost import CatBoostRegressor
from tqdm import tqdm


def loocv(
    model,
    df,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv=1.0,
    cat_features=[],
    trial_id=0,
):
    """
    Perform Leave-One-Out Cross Validation (LOOCV)
    :param model: CatBoostRegressor, CatBoost model
    :param df: pd.DataFrame, training data
    :param loocv_var: str, variable to perform LOOCV on
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :return: float, average RMSE
    """
    from sklearn.metrics import root_mean_squared_error

    rmse_values = []

    X = df[feature_names + cat_features]
    y = df[target_col]

    # Perform LOOCV based on precentage of loocv_var
    # Find unique values
    unique_values = df[loocv_var].unique()
    num_to_select = int(len(unique_values) * fraction_loocv)
    # Randomly select X% of the unique values without replacement
    selected_values = np.random.choice(unique_values, size=num_to_select, replace=False)
    pbar = tqdm(selected_values, leave=False)
    for idx, var in enumerate(pbar):
        pbar.set_description(f"Trial {trial_id}, LOOCV {var}")
        pbar.update()

        train_index = df[df[loocv_var] != var].index
        val_index = df[df[loocv_var] == var].index

        X_train, X_val = X.loc[train_index], X.loc[val_index]
        y_train, y_val = y.loc[train_index], y.loc[val_index]

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_val)

        # Calculate RMSE
        rmse = root_mean_squared_error(y_val, y_pred)
        rmse_values.append(rmse)

    # Compute average MSE
    average_rmse = np.mean(rmse_values)

    return average_rmse


def optuna_objective(model, df, feature_names, target_col, cat_features=[]):
    """

    Args:
        model:
        df:
        feature_names:
        target_col:
        cat_features:

    Returns:

    """
    from sklearn.metrics import root_mean_squared_error
    from sklearn.model_selection import train_test_split

    X = df[feature_names + cat_features]
    y = df[target_col]

    # Divide the data into training and validation sets
    train_X, val_X, train_y, val_y = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    model.fit(
        train_X,
        train_y,
        cat_features=cat_features,
        eval_set=(val_X, val_y),
        early_stopping_rounds=100,
        use_best_model=True,
        verbose=False,
    )

    # Make predictions
    val_preds = model.predict(val_X)

    # Evaluate predictions
    rmse = root_mean_squared_error(val_y, val_preds)

    return rmse


def optimized_model(
    model_name,
    df,
    use_loocv,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv,
    cat_features=[],
    seed=0,
):
    """
    Train CatBoost model using Optuna hyperparameter optimization
    :param model_name: str, 'CatBoost' or 'XGBoost'
    :param df: pd.DataFrame, training data
    :param loocv_var: str, 'Harvest Year'
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :param seed: int, random seed
    """
    # Define objecive function for optuna Hyperparameter tuning
    def _optuna_objective(trial):
        try:
            if model_name == "catboost":
                params = {
                    "depth": trial.suggest_int("depth", 1, 7),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
                    "iterations": trial.suggest_int(
                        "iterations", low=1000, high=5000, step=500
                    ),
                    "subsample": trial.suggest_float("subsample", 1.0, 1.0),
                    "random_strength": trial.suggest_float("random_strength", 0.3, 1.0),
                    "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 1.0),
                    "loss_function": "MAPE",
                    "early_stopping_rounds": 50,
                    "random_seed": seed,
                    "verbose": False,
                }

                # Fit the optuna model
                optuna_model = CatBoostRegressor(**params, cat_features=cat_features)
            else:
                raise NotImplementedError

            if use_loocv:
                trial_id = trial.number
                error_metric = loocv(
                    optuna_model,
                    df,
                    loocv_var,
                    feature_names,
                    target_col,
                    fraction_loocv,
                    cat_features,
                    trial_id,
                )
            else:
                error_metric = optuna_objective(
                    optuna_model, df, feature_names, target_col, cat_features
                )

            return error_metric
        except Exception as e:
            print(f"Trial failed with exception: {e}")
            return np.inf  # Assign a high cost to failed trials

    try:
        # Optimize hyperparameters
        n_trials = min(20, int(mp.cpu_count() * 0.9))
        optuna.logging.set_verbosity(optuna.logging.WARNING)  # Disable verbose
        sampler = optuna.samplers.TPESampler(seed=seed)
        study = optuna.create_study(sampler=sampler, direction="minimize")
        study.optimize(
            _optuna_objective, n_trials=n_trials, n_jobs=int(mp.cpu_count() * 0.4)
        )
        if study.best_trial is None:
            raise ValueError("Optimization failed to complete any trials.")
        hyperparams = study.best_trial.params

    except Exception as e:
        print(f"Optimization failed: {e}")
        hyperparams = {
            "depth": 6,
            "learning_rate": 0.01,
            "iterations": 10,
            "subsample": 1.0,
            "random_strength": 0.5,
            "reg_lambda": 0.001,
            "loss_function": "MAPE",
            "early_stopping_rounds": 50,
            "random_seed": seed,
            "verbose": False,
        }

    # Model Initialization & Training
    if model_name == "catboost":
        model = CatBoostRegressor(**hyperparams, cat_features=cat_features)
    else:
        raise NotImplementedError

    return hyperparams, model


def auto_train(
    cluster_strategy: str,
    model_name: str,
    model_type: str,
    use_loocv: bool,
    loocv_var: str,
    df_train: pd.DataFrame,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    feature_names: list,
    target_col: str,
    optimize: bool = False,
    fraction_loocv: float = 1.0,
    cat_features: list = None,
    monotonic_features: list = None,
    seed: int = 0,
):
    """
    Train a model using specified parameters and optionally perform hyperparameter optimization.

    :param cluster_strategy: Clustering strategy ('individual', 'auto_detect', 'single')
    :param model_name: Name of the model ('catboost', 'xgboost', 'merf', 'oblique', 'ydf', 'linear', 'gam', etc.)
    :param model_type: Type of model ('REGRESSION' or 'CLASSIFICATION')
    :param use_loocv: Whether to use leave-one-out cross-validation
    :param loocv_var: Variable for LOOCV
    :param df_train: Training dataset
    :param X_train: Training features
    :param y_train: Training target
    :param feature_names: List of feature names
    :param target_col: Name of the target column
    :param optimize: Whether to optimize hyperparameters
    :param fraction_loocv: Fraction of unique values for LOOCV
    :param cat_features: List of categorical features (optional)
    :param monotonic_features: List of monotonic features (optional)
    :param seed: Random seed for reproducibility
    :return: Hyperparameters and trained model
    """
    if optimize:
        hyperparams, model = optimized_model(
            model_name, df_train, use_loocv, loocv_var,
            feature_names, target_col, fraction_loocv,
            cat_features, seed
        )
    else:
        hyperparams = {}

        if model_name in ["catboost", "merf"]:
            from catboost import CatBoostRegressor, CatBoostClassifier

            loss_function = "MAPE" if model_type == "REGRESSION" else "MultiClass"
            bootstrap_type = "Bernoulli" if model_type == "CLASSIFICATION" else "MVS"
            hyperparams = {
                "iterations": 2500,
                "learning_rate": 0.01,
                "depth": 6,
                "subsample": 1.0,
                "bootstrap_type": bootstrap_type,
                "random_strength": 0.5,
                "reg_lambda": 0.1,
                "loss_function": loss_function,
                "early_stopping_rounds": 20,
                "random_seed": seed,
                "verbose": False,
            }

            if model_name == "catboost":
                model_cls = CatBoostRegressor if model_type == "REGRESSION" else CatBoostClassifier
                model = model_cls(**hyperparams, cat_features=cat_features)

            elif model_name == "merf":
                from merf import MERF
                hyperparams["iterations"] = 1000
                regr_cls = CatBoostRegressor if model_type == "REGRESSION" else CatBoostClassifier
                regr = regr_cls(**hyperparams, cat_features=cat_features)
                model = MERF(regr, max_iterations=10)

        elif model_name == "oblique":
            from treeple import ExtraObliqueRandomForestRegressor, ExtraObliqueRandomForestClassifier
            n_features = X_train.shape[1]
            oblique_cls = ExtraObliqueRandomForestRegressor if model_type == "REGRESSION" else ExtraObliqueRandomForestClassifier
            model = oblique_cls(
                n_estimators=1500, max_depth=20, max_features=n_features**2,
                feature_combinations=n_features, n_jobs=-1, random_state=42
            )
        elif model_name == "tabpfn":
            # from tabpfn_extensions.post_hoc_ensembles.sklearn_interface import AutoTabPFNRegressor
            from tabpfn import TabPFNRegressor

            # Identify the column indices for cat_features in X_train
            if cat_features is None:
                cat_feature_indices = []
            else:
                cat_feature_indices = [X_train.columns.get_loc(col) for col in cat_features if
                    col in X_train.columns]

            model = TabPFNRegressor(device="auto")

            # model = AutoTabPFNRegressor(max_time=600,
            #                            #categorical_feature_indices=cat_feature_indices,
            #                            ignore_pretraining_limits=True)
        elif model_name == "tabicl":
            from tabicl import TabICLRegressor

            model = TabICLRegressor(
                n_estimators=16,
                norm_methods=["none", "power", "quantile", "robust"],
                outlier_threshold=5.0,
                random_state=seed,
            )
        elif model_name == "desreg":
            from desReg.des.DESRegression import DESRegression
            from tabpfn_extensions.post_hoc_ensembles.sklearn_interface import AutoTabPFNRegressor
            from catboost import CatBoostRegressor

            model_catboost = CatBoostRegressor(**hyperparams, cat_features=cat_features)

            # Identify the column indices for cat_features in X_train
            if cat_features is None:
                cat_feature_indices = []
            else:
                cat_feature_indices = [X_train.columns.get_loc(col) for col in cat_features if
                    col in X_train.columns]
            model_tabpfn = AutoTabPFNRegressor(max_time=600,
                                               # categorical_feature_indices=cat_feature_indices,
                                               ignore_pretraining_limits=True)
            
            import ydf
            templates = ydf.GradientBoostedTreesLearner.hyperparameter_templates()
            task = ydf.Task.REGRESSION if model_type == "REGRESSION" else ydf.Task.CLASSIFICATION
            model_ydf = ydf.GradientBoostedTreesLearner(
                label=target_col, task=task,
                growing_strategy='BEST_FIRST_GLOBAL',
                categorical_algorithm='RANDOM',
                split_axis='SPARSE_OBLIQUE',
                sparse_oblique_normalization='MIN_MAX',
                sparse_oblique_num_projections_exponent=2.0
            )
            hyperparams = templates["benchmark_rank1v1"]

            model = DESRegression(regressors_list=[model_catboost, model_ydf])
        elif model_name == "ngboost":
            if model_type == "REGRESSION":
                from ngboost import NGBRegressor
                from ngboost.distns import Normal
                from ngboost.scores import MLE

                # Initialize and train NGBoost regressor
                model = NGBRegressor(Dist=Normal, Score=MLE, natural_gradient=True)
            elif model_type == "CLASSIFICATION":
                from ngboost import NGBClassifier
                from ngboost.distns import k_categorical
                from ngboost.scores import LogScore

                # Initialize and train NGBoost classifier
                model = NGBClassifier(Dist=k_categorical(3), Score=LogScore, natural_gradient=True)
        elif model_name == "ydf":
            import ydf
            templates = ydf.GradientBoostedTreesLearner.hyperparameter_templates()
            task = ydf.Task.REGRESSION if model_type == "REGRESSION" else ydf.Task.CLASSIFICATION
            model = ydf.GradientBoostedTreesLearner(
                label=target_col, task=task,
                growing_strategy='BEST_FIRST_GLOBAL',
                categorical_algorithm='RANDOM',
                split_axis='SPARSE_OBLIQUE',
                sparse_oblique_normalization='MIN_MAX',
                sparse_oblique_num_projections_exponent=2.0,
                validation_ratio=0.0,
            )
            hyperparams = templates["benchmark_rank1v1"]

        elif model_name == "linear":
            from sklearn.linear_model import LassoCV, LogisticRegressionCV
            linear_cls = LassoCV if model_type == "REGRESSION" else LogisticRegressionCV
            model = linear_cls(cv=5, random_state=42)
        elif model_name == "logistic":
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(multi_class='multinomial', solver='lbfgs')

        elif model_name.startswith("gam"):
            from pygam import GAM, LinearGAM, LogisticGAM, s, f, te
            is_classification = model_type == "CLASSIFICATION"
            gam_cls = LogisticGAM if is_classification else LinearGAM
            gam_formulas = {
                "cumulative_1": s(0) + f(1),
                "cumulative_2": s(0) + s(1) + te(0, 1) + f(2),
                "cumulative_3": s(0) + s(1) + s(2) + te(0, 1) + te(0, 2) + te(1, 2) + f(3),
            }
            formula = gam_formulas.get(model_name, gam_cls(n_splines=25, spline_order=3))
            model = gam_cls(n_splines=25, spline_order=3).gridsearch(X_train, y_train.values, lam=np.logspace(-3, 3, 11)) if model_name.startswith("gam") else formula
        elif model_name == "geospaNN":
            import torch
            import geospaNN

            X_train = X_train.drop(columns=cat_features)
            X, Y = torch.from_numpy(X_train.to_numpy()).float(), torch.from_numpy(y_train.to_numpy().reshape(-1)).float()
            coord = torch.from_numpy(df_train[['lon', 'lat']].to_numpy()).float()
            p, n, nn = X.shape[1], X.shape[0], 5

            data = geospaNN.make_graph(X, Y, coord, nn)
            mlp = torch.nn.Sequential(
                torch.nn.Linear(p, 50), torch.nn.ReLU(),
                torch.nn.Linear(50, 20), torch.nn.ReLU(),
                torch.nn.Linear(20, 10), torch.nn.ReLU(),
                torch.nn.Linear(10, 1)
            )

            data_train, data_val, data_test = geospaNN.split_data(X, Y, coord, neighbor_size=nn, test_proportion=0.1)
            theta0 = geospaNN.theta_update(torch.tensor([1, 1.5, 0.01]), mlp(data_train.x).squeeze() - data_train.y, data_train.pos, neighbor_size=5)
            model = geospaNN.nngls(p=p, neighbor_size=nn, coord_dimensions=2, mlp=mlp, theta=torch.tensor(theta0))
            model = geospaNN.nngls_train(model, lr=0.01, min_delta=0.001)
            training_log = model.train(data_train, data_val, data_test, Update_init=10, Update_step=10)
        elif model_name == "cubist":
            from cubist import Cubist

            model = Cubist(n_committees=5, auto=True, random_state=seed)
        elif model_name == "xgboost":
            raise NotImplementedError("XGBoost model not implemented yet")
        else:
            raise ValueError(f"Unknown model name: {model_name}")

    return hyperparams, model


def estimate_ci(model_type, model_name, model):
    """
    Estimate confidence intervals for the model using MapieRegressor or MapieClassifier.

    Args:
        model_type: str, Type of the model ('REGRESSION' or 'CLASSIFICATION')
        model_name: str, Name of the model ('catboost', 'xgboost', 'merf', 'oblique', 'ydf', 'linear', 'gam', etc.)
        model: The trained model

    Returns:
        model: The model wrapped with Mapie for confidence interval estimation
    """
    if model_name == "ngboost":
        return model
    elif model_type == "CLASSIFICATION" and model_name == "catboost":
        return model
    elif model_type == "REGRESSION":
        from mapie.regression import MapieRegressor
        model = MapieRegressor(model, n_jobs=-1)
    elif model_type == "CLASSIFICATION":
        from mapie.classification import MapieClassifier
        model = MapieClassifier(model, n_jobs=-1, method="naive")
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    return model

