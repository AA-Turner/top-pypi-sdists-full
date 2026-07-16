import multiprocessing as mp

import numpy as np
import pandas as pd
import optuna
from catboost import CatBoostRegressor
from geocif.progress import pbar as _pbar


class BassRegressor:
    """scikit-learn-style wrapper around pyBASS (BASS = Bayesian Adaptive
    Spline Surfaces = Bayesian MARS: adaptive hinge-spline bases + automatic
    interaction selection, MCMC-fit).

    One-hot-encodes categorical/object columns, fills NaN with the train
    median, and returns the posterior-MEAN prediction. pyBASS is a git-only
    optional dependency (``pip install git+https://github.com/lanl/pyBASS.git``)
    imported lazily so geocif installs without it. Tuned poppy defaults
    (maxInt=1 additive, npart=15) beat cubist on MIN_ESI4WK LOOCV (0.489 vs
    0.443); interactions overfit the small sample.
    """

    def __init__(self, max_int=1, npart=15, max_basis=1000,
                 nmcmc=14000, nburn=9000, thin=10):
        self.max_int = max_int
        self.npart = npart
        self.max_basis = max_basis
        self.nmcmc = nmcmc
        self.nburn = nburn
        self.thin = thin

    def get_params(self, deep=True):
        return dict(max_int=self.max_int, npart=self.npart, max_basis=self.max_basis,
                    nmcmc=self.nmcmc, nburn=self.nburn, thin=self.thin)

    def set_params(self, **p):
        for k, v in p.items():
            setattr(self, k, v)
        return self

    def _numeric(self, X):
        X = pd.DataFrame(X).copy()
        obj = list(X.select_dtypes(include=["object", "category"]).columns)
        if obj:
            X = pd.get_dummies(X, columns=obj, dummy_na=False)
        return X.apply(pd.to_numeric, errors="coerce")

    def fit(self, X, y):
        try:
            import pyBASS as pb
        except ImportError as exc:
            raise ImportError(
                "model = 'bass' requires pyBASS (Bayesian MARS), a git-only "
                "optional dependency:\n"
                "    pip install git+https://github.com/lanl/pyBASS.git"
            ) from exc
        Xn = self._numeric(X)
        self._median = Xn.median(numeric_only=True)
        Xn = Xn.fillna(self._median).fillna(0.0)
        self.columns_ = list(Xn.columns)
        self.model_ = pb.bass(
            Xn.values.astype(float), np.asarray(y, dtype=float),
            maxInt=self.max_int, npart=self.npart, maxBasis=self.max_basis,
            nmcmc=self.nmcmc, nburn=self.nburn, thin=self.thin, verbose=False,
        )
        return self

    def predict(self, X):
        Xn = self._numeric(X).reindex(columns=self.columns_, fill_value=0.0)
        Xn = Xn.fillna(self._median).fillna(0.0)
        preds = np.asarray(self.model_.predict(Xn.values.astype(float)))
        return preds.mean(axis=0)


def loocv(
    model,
    df,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv=1.0,
    cat_features=[],
    trial_id=0,
    seed=0,
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
    selected_values = np.random.default_rng(seed).choice(unique_values, size=num_to_select, replace=False)
    pbar = _pbar(selected_values, leave=False)
    for idx, var in enumerate(pbar):
        pbar.set_description(f"Trial {trial_id}, LOOCV {var}")

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
                    "depth": trial.suggest_int("depth", 2, 5),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
                    "iterations": trial.suggest_int(
                        "iterations", low=1000, high=5000, step=500
                    ),
                    "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                    "bootstrap_type": "Bernoulli",
                    "random_strength": trial.suggest_float("random_strength", 0.3, 1.0),
                    "reg_lambda": trial.suggest_float("reg_lambda", 1.0, 30.0, log=True),
                    "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 3, 10),
                    "loss_function": "RMSE",
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
                    seed,
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
            _optuna_objective, n_trials=n_trials, n_jobs=1
        )
        if study.best_trial is None:
            raise ValueError("Optimization failed to complete any trials.")
        hyperparams = study.best_trial.params

    except Exception as e:
        print(f"Optimization failed: {e}")
        hyperparams = {
            "depth": 4,
            "learning_rate": 0.01,
            "iterations": 10,
            "subsample": 1.0,
            "bootstrap_type": "Bernoulli",
            "random_strength": 0.5,
            "reg_lambda": 5.0,
            "min_data_in_leaf": 5,
            "loss_function": "RMSE",
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
    cubist_params: dict = None,
    bass_params: dict = None,
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
    # `curated_<algo>`, `top<N>_<algo>` and `auto_<algo>` are all
    # config-driven CID-selection wrappers that dispatch to the same
    # underlying algo. The section name carries the selection knobs
    # (use_cids, top_n, auto_min_count, etc.) — Geocif applies those
    # before training. Here we strip the wrapper prefix so every
    # existing `elif model_name == "tabpfn"` / "catboost" / ... branch
    # below works unchanged. Examples:
    #   curated_tabpfn → tabpfn
    #   top10_tabpfn   → tabpfn
    #   auto_tabpfn    → tabpfn
    # The original section name still lives on the caller side and is
    # what shows up in DB rows / plot filenames, keeping variants
    # distinguishable.
    import re as _re
    if model_name.startswith("curated_"):
        model_name = model_name.split("_", 1)[1]
    elif model_name.startswith("auto_"):
        model_name = model_name.split("_", 1)[1]
    else:
        _m = _re.match(r"^top\d+_(.+)$", model_name)
        if _m:
            model_name = _m.group(1)

    if optimize:
        hyperparams, model = optimized_model(
            model_name, df_train, use_loocv, loocv_var,
            feature_names, target_col, fraction_loocv,
            cat_features, seed
        )
    else:
        hyperparams = {}

        if model_name in ["catboost", "merf", "catboost_quantile"]:
            from catboost import CatBoostRegressor, CatBoostClassifier

            # catboost_quantile trains catboost against the 0.25-quantile
            # loss instead of RMSE. Same hyperparams; useful for insurance-
            # trigger scenarios where distinguishing the LOW tail matters
            # more than mean accuracy (RMSE loss mean-reverts and rarely
            # predicts below-threshold yields on small data).
            if model_name == "catboost_quantile":
                loss_function = "Quantile:alpha=0.25"
            else:
                loss_function = "RMSE" if model_type == "REGRESSION" else "MultiClass"
            # Small-n / high-feature-count tuning (Kenya-maize regime,
            # ~300 rows × ~500 features per fold):
            #   subsample=0.7   → activate Bernoulli bagging (was 1.0 → inert)
            #   border_count=64 → coarser feature quantization (default 254
            #                     over-fits noise at small n)
            #   reg_lambda=12   → stronger L2 (was 5.0)
            hyperparams = {
                "iterations": 2500,
                "learning_rate": 0.01,
                "depth": 4,
                "subsample": 0.7,
                "bootstrap_type": "Bernoulli",
                "random_strength": 0.5,
                "reg_lambda": 12.0,
                "border_count": 64,
                "min_data_in_leaf": 5,
                "loss_function": loss_function,
                "early_stopping_rounds": 50,
                "random_seed": seed,
                "verbose": False,
            }

            if model_name in ("catboost", "catboost_quantile"):
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
            from tabpfn import TabPFNRegressor

            # Identify the column indices for cat_features in X_train
            if cat_features is None:
                cat_feature_indices = []
            else:
                cat_feature_indices = [X_train.columns.get_loc(col) for col in cat_features if
                    col in X_train.columns]

            # Tuning notes — see IDEAS.md at project root:
            #   * n_estimators=8: tabpfn default. A/B tested 8/16/32 on
            #     Kenya maize (0.4.787 → 0.4.790 → 0.4.791); all three
            #     produced RMSE within 0.4% of each other (0.4723 / 0.4741
            #     / 0.4760) and R² within 0.004. The ensemble is saturated
            #     at ~40 training points per region-year — bumping does
            #     nothing but burn compute (1x/1.5x/3x runtime). Kept at
            #     tabpfn's own default to avoid the illusion of tuning.
            #   * ignore_pretraining_limits=True: REQUIRED at our sample
            #     size. tabpfn 8.x enforces a CPU-only guardrail that
            #     aborts with RuntimeError "Running on CPU with more than
            #     1000 samples is not allowed by default" when the training
            #     set exceeds 1000 rows. Kenya has ~1700 rows per season,
            #     so removing the flag breaks every fit. (Learned the hard
            #     way in 0.4.789 — every prediction failed silently.)
            #   * random_state=int(seed): guarantees deterministic ensemble
            #     permutations across estimators, safe against float-seed
            #     configs.
            #   * inference_config left at None: custom PREPROCESS_TRANSFORMS
            #     / FEATURE_SHIFT_METHOD tuning (Tier 2b) is a future
            #     experiment — see IDEAS.md.
            model = TabPFNRegressor(
                device="auto",
                categorical_features_indices=cat_feature_indices,
                random_state=int(seed),
                n_estimators=8,
                ignore_pretraining_limits=True,
            )
        elif model_name == "tabpfn_phe":
            # Post-Hoc Ensembling wrapper from tabpfn_extensions — runs
            # TabPFN with multiple preprocessing configurations and
            # ensembles their predictions. In published benchmarks it's
            # typically the strongest zero-shot tabular regressor
            # available, at 3-10x the runtime of base TabPFN.
            #
            # Named "tabpfn_phe" rather than "auto_tabpfn" to avoid the
            # wrapper-prefix regex at the top of this function, which
            # strips "auto_" and would route "auto_tabpfn" back to the
            # plain "tabpfn" branch.
            #
            # max_time bounds the per-fit optimization budget; 600s = 10min
            # is a reasonable operational ceiling. Cat feature indices
            # aren't currently accepted by AutoTabPFNRegressor's ctor
            # (the underlying PHE machinery detects them itself), so we
            # don't pass them. See IDEAS.md for benchmarking notes.
            from tabpfn_extensions.post_hoc_ensembles.sklearn_interface import (
                AutoTabPFNRegressor,
            )
            # ignore_pretraining_limits=True passes through to the
            # constituent TabPFN estimators, suppressing the same
            # >1000-samples-CPU guardrail that would otherwise abort
            # every fit on our ~1700-row Kenya training sets.
            model = AutoTabPFNRegressor(
                max_time=600,
                random_state=int(seed),
                ignore_pretraining_limits=True,
            )
        elif model_name == "tabfm":
            # Google Research's TabFM (tabular foundation model) — zero-shot
            # inference like TabPFN, so no fit-time hyperparameters and no
            # Optuna. PyTorch CPU backend is the correct choice on this
            # cluster (JAX-on-CPU JIT-recompiles every call → ~130s/row vs
            # PyTorch's ~10s/row; a V100 16GB doesn't fit the ~11GB weights
            # + working memory, so GPU is deferred).
            #
            # Load is heavy (~26s cold; ~0s if HF cache is warm — cluster
            # HF_HOME lives on /gpfs so the ~13GB weights persist between
            # runs). Loading per-call mirrors the tabpfn branch above; if
            # this becomes a bottleneck on production runs, cache the
            # pretrained handle at module level.
            import tabfm as _tabfm

            class _TabFMWithObjectDtype:
                """sklearn-shaped wrapper that casts pandas category
                columns back to object before fit/predict.

                Why: TabFM's tokenizer misreads CategoricalDtype as
                numeric codes — verified 10x worse RMSE on a synthetic
                fixture (1.410 vs 0.149) with the same underlying data.
                geocif casts cat_features to category at geocif.py:1270
                because catboost/tabpfn/etc. need it; we can't unwind
                that upstream cast without breaking the other models.
                So this adapter locally undoes it for TabFM only."""
                def __init__(self, pretrained):
                    self._reg = _tabfm.TabFMRegressor(model=pretrained)

                @staticmethod
                def _cast(X):
                    X = X.copy()
                    for c in X.columns:
                        if hasattr(X[c], "cat"):
                            X[c] = X[c].astype(object)
                    return X

                def fit(self, X, y):
                    return self._reg.fit(self._cast(X), y)

                def predict(self, X):
                    return self._reg.predict(self._cast(X))

            _pretrained = _tabfm.tabfm_v1_0_0_pytorch.load(model_type="regression")
            model = _TabFMWithObjectDtype(_pretrained)
        elif model_name == "tabpfn_ft":
            from tabpfn.finetuning import FinetunedTabPFNRegressor

            if cat_features is None:
                cat_feature_indices = []
            else:
                cat_feature_indices = [X_train.columns.get_loc(col) for col in cat_features if
                    col in X_train.columns]

            # Fine-tuned variant of TabPFN. Needs X_val/y_val (handled by
            # TabPFNFTFitter in geocif.py). Defaults from PriorLabs tutorial;
            # CPU works but expect ~5-10x slower per task than zero-shot 'tabpfn'.
            model = FinetunedTabPFNRegressor(
                device="auto",
                epochs=30,
                learning_rate=1e-5,
                n_estimators_finetune=2,
                n_estimators_validation=2,
                n_estimators_final_inference=8,
                early_stopping=True,
                early_stopping_patience=8,
                use_fixed_preprocessing_seed=False,
                random_state=seed,
                extra_regressor_kwargs={
                    "categorical_features_indices": cat_feature_indices,
                    "ignore_pretraining_limits": True,
                },
            )
        elif model_name == "tabicl":
            from tabicl import TabICLRegressor

            model = TabICLRegressor(
                n_estimators=16,
                norm_methods=["none", "power", "quantile", "robust"],
                outlier_threshold=5.0,
                random_state=seed,
            )
        elif model_name == "tabicl_ft":
            from tabicl import FinetunedTabICLRegressor

            # Fine-tuned variant of TabICL. Needs X_val/y_val for early
            # stopping — wired in the TabICLFTFitter class in geocif.py.
            # GPU-friendly; falls back to CPU when no CUDA device is
            # available — expect ~5-10x slower per task on CPU. Defaults
            # come from the tabicl tutorial.
            model = FinetunedTabICLRegressor(
                epochs=60,
                learning_rate=1e-5,
                n_estimators_finetune=2,
                n_estimators_validation=2,
                n_estimators_inference=4,
                early_stopping=True,
                patience=10,
                random_state=seed,
                verbose=False,
            )
        elif model_name == "desreg":
            try:
                from desReg.des.DESRegression import DESRegression
            except ImportError as exc:
                raise ImportError(
                    "model = 'desreg' requires desReg, which is an OPTIONAL "
                    "geocif extra (held out because it's an obscure package "
                    "with historical install quirks). Install with:\n"
                    "    pip install geocif[desreg]\n"
                    "Or pick a different model in [DEFAULT] models = [...]."
                ) from exc
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
            # Placeholder — real term construction and the single gridsearch
            # fit happen in GAMFitter.fit() where the final fit-time feature
            # matrix and column order are known.  Constructing with terms here
            # would lock them to a stale X_train layout, and calling .fit()
            # here would be redundant with GAMFitter.
            from pygam import LinearGAM, LogisticGAM
            gam_cls = LogisticGAM if model_type == "CLASSIFICATION" else LinearGAM
            model = gam_cls()
        elif model_name == "geospaNN":
            try:
                import torch
                import geospaNN
            except ImportError as exc:
                raise ImportError(
                    "model = 'geospaNN' requires torch + geospaNN, an "
                    "OPTIONAL geocif extra (held out because geospaNN "
                    "depends on torch-scatter, which has a broken build "
                    "system that can't find torch under PEP-517 build "
                    "isolation). Install in this order:\n"
                    "    pip install torch\n"
                    "    pip install geocif[geospann] --no-build-isolation\n"
                    "Or pick a different model in [DEFAULT] models = [...]."
                ) from exc

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

            # n_committees=10: default 5 (R Cubist legacy) under-boosts on
            # yield data where errors correlate across regions.
            # extrapolation=0.10: default 0.05 clips predictions too tightly
            # for climate-driven yield anomalies that exceed the training range.
            # unbiased=True: yield is right-skewed; default minimizes MAE and
            # underestimates the high tail.
            # These defaults suit data-rich crops; small-n crops override them
            # via [ML] cubist_* config (e.g. poppy: n_committees=1,
            # extrapolation=0.0) — see cubist_params in geocif.py.
            cub = dict(n_committees=10, auto=True, extrapolation=0.10, unbiased=True)
            cub.update(cubist_params or {})
            # `neighbors` (composite instance-based correction) requires
            # auto=False; flip it defensively so a config that sets neighbors
            # without auto=False doesn't raise mid-run.
            if cub.get("neighbors") is not None and cub.get("auto", True):
                cub["auto"] = False
            model = Cubist(random_state=seed, **cub)
        elif model_name == "bass":
            # BASS = Bayesian MARS (pyBASS). Tuned poppy defaults (maxInt=1
            # additive, npart=15) beat cubist on MIN_ESI4WK; interactions
            # overfit small samples. Overridable per-project via [ML] bass_*.
            bass = dict(max_int=1, npart=15, max_basis=1000,
                        nmcmc=14000, nburn=9000, thin=10)
            bass.update(bass_params or {})
            model = BassRegressor(**bass)
        elif model_name == "gpr":
            from sklearn.gaussian_process import GaussianProcessRegressor
            from sklearn.gaussian_process.kernels import (
                RBF, WhiteKernel, ConstantKernel as C,
            )

            kernel = (
                C(1.0, (1e-3, 1e3))
                * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e2))
                + WhiteKernel(noise_level=1.0, noise_level_bounds=(1e-5, 1e1))
            )
            model = GaussianProcessRegressor(
                kernel=kernel,
                n_restarts_optimizer=5,
                normalize_y=True,
                random_state=seed,
            )
        elif model_name == "xgboost":
            raise NotImplementedError("XGBoost model not implemented yet")
        else:
            raise ValueError(f"Unknown model name: {model_name}")

    return hyperparams, model


def estimate_ci(model_type, model_name, model, alpha=0.05, ci_method="crepes"):
    """
    Wrap a fitted model for conformal prediction.

    Args:
        model_type: 'REGRESSION' or 'CLASSIFICATION'
        model_name: Model name (e.g. 'catboost', 'xgboost')
        model: The fitted model
        alpha: Significance level for confidence intervals
        ci_method: 'crepes' (default) or 'mapie'

    Returns:
        Wrapped model for confidence interval estimation
    """
    # Mirror auto_train's wrapper-prefix strip so estimate_ci treats
    # curated_/top<N>_/auto_ variants like their underlying algo.
    import re as _re
    if model_name.startswith("curated_"):
        model_name = model_name.split("_", 1)[1]
    elif model_name.startswith("auto_"):
        model_name = model_name.split("_", 1)[1]
    else:
        _m = _re.match(r"^top\d+_(.+)$", model_name)
        if _m:
            model_name = _m.group(1)

    if model_name in ["ngboost", "tabpfn", "tabpfn_ft", "tabicl", "tabicl_ft"]:
        return model
    elif model_type == "CLASSIFICATION" and model_name == "catboost":
        return model
    elif model_type == "REGRESSION":
        if ci_method == "crepes":
            from crepes import WrapRegressor
            model = WrapRegressor(model)
        else:
            from mapie.regression import SplitConformalRegressor
            model = SplitConformalRegressor(estimator=model, confidence_level=1 - alpha, prefit=True)
    elif model_type == "CLASSIFICATION":
        from mapie.classification import SplitConformalClassifier
        model = SplitConformalClassifier(estimator=model, confidence_level=1 - alpha, prefit=True)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    return model

