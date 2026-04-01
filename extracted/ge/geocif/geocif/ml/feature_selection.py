import logging
import os
os.environ["MPLBACKEND"] = "Agg"

import numpy as np
from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor
from collections import Counter
from pathlib import Path
import pandas as pd

from .gomp import gomp_select

logger = logging.getLogger(__name__)


def are_all_features_non_eo(features):
    """
    Check if all the features are non-EO features

    Args:
        features: iterable of feature names

    Returns:
        bool: True if every feature is in the non-EO list
    """
    non_eo_features = [
        'Median Yield (tn per ha)',
        'Analogous Year',
        'Analogous Year Yield',
        'lon',
        'lat',
        't -1 Yield (tn per ha)',
        't -2 Yield (tn per ha)',
        't -3 Yield (tn per ha)',
        't -4 Yield (tn per ha)',
        't -5 Yield (tn per ha)',
    ]
    return all(f in non_eo_features for f in features)


def select_features(
    X, y,
    method="multi",
    min_features_to_select=3,
    threshold_nan=0.2,
    threshold_unique=0.6,
    dir_output=".",
    region=None
):
    """
    Feature-selection wrapper supporting many methods plus a new 'multi' option.

    Parameters
    ----------
    X : pd.DataFrame
    y : array-like
    method : str
        One of {"none", "SHAP", "stabl", "feature_engine", "mrmr", "RFECV", "lasso",
        "BorutaPy", "Leshy", "PowerShap", "BorutaShap", "Genetic", "RFE", "multi",
        "gOMP"}.
        Use "none" to skip feature selection (handled in caller).
    min_features_to_select : int
    threshold_nan : float
        Drop columns with > threshold_nan proportion of NaNs
    threshold_unique : float
        (Reserved for future use)

    Returns
    -------
    selector : fitted selector object or None (for multi)
    X_filtered : pd.DataFrame of selected features
    selected_features : list[str]
    """
    # copy original for multi-mode recursion
    X_clean = X.copy()

    # 1) drop columns with too many NaNs
    nan_prop = X_clean.isna().mean()
    X_clean = X_clean.loc[:, nan_prop <= threshold_nan]

    # 2) fill NaNs with median
    num_cols = X_clean.select_dtypes(include=["number"]).columns  # catches int64, float64, etc.
    X_clean[num_cols] = X_clean[num_cols].fillna(X_clean[num_cols].median())

    # --- multi-method ensemble -------------------------------
    if method == "multi":
        import matplotlib.pyplot as plt
        import seaborn as sns

        logger.info("[multi] Starting multi-method feature selection for region=%s (%d features, %d samples)",
                     region, X_clean.shape[1], X_clean.shape[0])

        counter = Counter()
        selections = {}

        models = ["BorutaPy", "mrmr", "gOMP"]
        # run three selectors and count feature picks
        for sub_m in models:
            logger.info("[multi] Running %s ...", sub_m)
            try:
                _, _, feats = select_features(
                    X_clean, y,
                    method=sub_m,
                    min_features_to_select=min_features_to_select,
                    threshold_nan=threshold_nan,
                    threshold_unique=threshold_unique
                )
            except Exception as e:
                logger.warning("[multi] %s failed: %s", sub_m, e)
                feats = []

            selections[sub_m] = set(feats)
            counter.update(feats)
            logger.info("[multi] %s selected %d features", sub_m, len(feats))

        # union of all features
        combined = sorted(counter.keys())
        logger.info("[multi] Union of all methods: %d features", len(combined))
        X_out = X_clean.loc[:, combined]

        # plot and save histogram
        import pandas as pd
        freq = pd.Series(counter).sort_values(ascending=False)
        fig = freq.plot(kind="bar", width=0.9).get_figure()
        plt.title("Feature selection frequency across methods")
        plt.xlabel("Feature")
        plt.ylabel(f"Times selected (out of {len(models)})")
        plt.tight_layout()

        dir_output = dir_output / Path("feature_selection")
        os.makedirs(dir_output, exist_ok=True)
        fig.savefig(dir_output / f"feature_selection_frequency_{region}.png", dpi=300)
        plt.close(fig)

        # build DataFrame: rows=features, cols=methods, 1 if selected
        sel_df = pd.DataFrame(
            {m: [1 if f in selections[m] else 0 for f in combined] for m in models},
            index=combined
        )

        fig2, ax2 = plt.subplots(figsize=(10, max(6, len(combined) * 0.3)))
        sns.heatmap(sel_df, annot=True, cbar=False, linewidths=0.5, ax=ax2)
        ax2.set_xlabel("Method")
        ax2.set_ylabel("Feature")
        ax2.set_title("Which features each method selected")
        plt.tight_layout()
        fig2.savefig(dir_output / f"feature_selection_methods_{region}.png", dpi=300)
        plt.close(fig2)

        return None, X_out, combined

    # define forest for methods that need it
    forest = RandomForestRegressor(
        n_estimators=500,
        n_jobs=1,
        max_depth=5,
        random_state=1,
    )

    # patch numpy deprecation
    np.int = np.int32
    np.float = np.float64
    np.bool = np.bool_

    if method == "SHAP":
        import pandas as pd
        from catboost import CatBoostRegressor
        from fasttreeshap import TreeExplainer as FastTreeExplainer
        from sklearn.model_selection import cross_val_score

        model = CatBoostRegressor(n_estimators=500, verbose=0, use_best_model=False)
        model.fit(X_clean, y)
        explainer = FastTreeExplainer(model)
        shap_values = explainer.shap_values(X_clean)
        shap_importances = np.mean(np.abs(shap_values), axis=0)
        shap_df = pd.DataFrame({
            "feature": X_clean.columns,
            "importance": shap_importances
        }).sort_values("importance", ascending=False)

        def eval_n(N):
            top = shap_df["feature"].head(N)
            sel = CatBoostRegressor(n_estimators=500, random_state=42, verbose=0)
            scores = cross_val_score(sel, X_clean[top], y,
                                     cv=5, scoring="neg_mean_squared_error",
                                     n_jobs=-1)
            return np.mean(scores)

        nrange = [5,10,15,20,25,30]
        scores = [eval_n(N) for N in tqdm(nrange)]
        best = nrange[np.argmax(scores)]
        selected = shap_df["feature"].head(best).tolist()

    elif method == "stabl":
        from stabl.stabl import Stabl
        from sklearn.linear_model import Lasso

        st = Stabl(
            base_estimator=Lasso(alpha=0.001),
            n_bootstraps=10,
            artificial_type="knockoff",
            artificial_proportion=0.5,
            replace=False,
            fdr_threshold_range=np.arange(0.1,1,0.01),
            sample_fraction=0.5,
            random_state=42,
            lambda_grid="auto",
            verbose=1
        )
        st.fit(X_clean, y)
        selected = st.get_feature_names_out()

    elif method == "feature_engine":
        from feature_engine.selection import SmartCorrelatedSelection
        sel = SmartCorrelatedSelection(
            method="pearson",
            threshold=0.7,
            selection_method="model_performance",
            estimator=forest,
            scoring="neg_mean_squared_error",
        )
        X_fe = sel.fit_transform(X_clean, y)
        selected = X_fe.columns.tolist()

    elif method == "mrmr":
        from mrmr import mrmr_regression
        selected = mrmr_regression(X=X_clean, y=y, K=10)

    elif method == "RFECV":
        from sklearn.feature_selection import RFECV
        from sklearn.model_selection import KFold

        class RFECVProg(RFECV):
            def _fit(self, X, y):
                with tqdm(total=X.shape[1]) as p:
                    orig = self.scorer_
                    def wrap(*a, **k):
                        p.update(1)
                        return orig(*a, **k)
                    self.scorer_ = wrap
                    super()._fit(X, y)

        cv = KFold(n_splits=5)
        sel = RFECVProg(
            estimator=forest,
            step=1,
            cv=cv,
            scoring="neg_mean_squared_error",
            n_jobs=-1,
            verbose=0
        )
        sel.fit(X_clean, y)
        mask = sel.get_support()
        selected = X_clean.columns[mask].tolist()

    elif method == "lasso":
        from sklearn.linear_model import LassoLarsCV
        from sklearn.feature_selection import SelectFromModel

        lr = LassoLarsCV(cv=5)
        lr.fit(X_clean, y)
        sfm = SelectFromModel(lr, prefit=True)
        selected = X_clean.columns[sfm.get_support()].tolist()

    elif method == "gOMP":
        # Generalised Orthogonal Matching Pursuit (Tsagris et al. 2020)
        # Uses BIC stopping by default; selects parsimonious feature sets
        sel, X_out, selected = gomp_select(
            X_clean, y,
            outcome="continuous",
            stopping="bic",
            association="auto",
            max_features=min(30, X_clean.shape[1]),
            bic_delta=2.0,
            verbose=True,
        )
        if len(selected) == 0:
            # fallback: relax to LRT with generous alpha
            sel, X_out, selected = gomp_select(
                X_clean, y,
                outcome="continuous",
                stopping="lrt",
                alpha=0.05,
                max_features=min(30, X_clean.shape[1]),
                verbose=True,
            )

    elif method == "BorutaPy":
        from boruta import BorutaPy
        import itertools as it

        if "Region" in X_clean.columns:
            region_selected = {}
            for region in X_clean["Region"].unique():
                idx = X_clean["Region"] == region
                X_region = X_clean.loc[idx].drop(columns=["Region"])
                y_region = y.loc[idx] if hasattr(y, "loc") else y[idx]

                sel = BorutaPy(
                    estimator=forest,
                    n_estimators="auto",
                    random_state=42,
                    verbose=0
                )

                sel.fit(X_region.values, y_region)
                region_selected[region] = (
                    X_region.columns[sel.support_ | sel.support_weak_].tolist()
                )

            # keep features chosen in ≥ 1 regions
            counts   = Counter(it.chain.from_iterable(region_selected.values()))
            selected = [feat for feat, n in counts.items() if n >= 1]
        else:
            sel = BorutaPy(
                estimator=forest,
                n_estimators="auto",
                random_state=42,
                verbose=0
            )
            sel.fit(X_clean.values, y)
            selected = X_clean.columns[sel.support_ | sel.support_weak_].tolist()

    elif method == "Leshy":
        import arfs.feature_selection.allrelevant as arfsgroot
        from catboost import CatBoostRegressor

        model = CatBoostRegressor(n_estimators=350, verbose=0, use_best_model=False)
        sel = arfsgroot.Leshy(
            model,
            n_estimators="auto",
            verbose=1,
            max_iter=10,
            random_state=42,
            importance="fastshap",
        )
        sel.fit(X_clean, y)
        selected = sel.get_feature_names_out()
    elif method == "PowerShap":
        from powershap import PowerShap
        from catboost import CatBoostRegressor
        sel = PowerShap(
            model=CatBoostRegressor(n_estimators=500, verbose=0),
            power_alpha=0.05,
        )
        sel.fit(X_clean, y)
        selected = sel.transform(X_clean).columns.tolist()

    elif method == "BorutaShap":
        from BorutaShap import BorutaShap
        from catboost import CatBoostRegressor
        params = {
            "depth": 6,
            "learning_rate": 0.05,
            "iterations": 500,
            "subsample": 1.0,
            "random_strength": 0.5,
            "reg_lambda": 0.001,
            "loss_function": "RMSE",
            "early_stopping_rounds": 25,
            "random_seed": 42,
            "verbose": False,
        }
        model = CatBoostRegressor(**params)
        sel = BorutaShap(model=model, importance_measure="shap", classification=False)
        sel.fit(X=X_clean, y=y, n_trials=100, sample=False,
                train_or_test="test", normalize=True, verbose=False)
        selected = sel.Subset().columns.tolist()

    elif method == "Genetic":
        from sklearn_genetic import GAFeatureSelectionCV
        sel = GAFeatureSelectionCV(
            estimator=forest,
            cv=5,
            scoring="neg_mean_squared_error",
            population_size=100,
            generations=40,
            max_features=max(len(X_clean.columns)//3, min_features_to_select),
            crossover_probability=0.9,
            mutation_probability=0.1,
            keep_top_k=2,
            elitism=True,
            n_jobs=-1,
            verbose=1,
        )
        sel.fit(X_clean, y)
        selected = X_clean.columns[sel.support_].tolist()

    elif method == "RFE":
        from sklearn.feature_selection import RFE
        sel = RFE(forest, n_features_to_select=min_features_to_select, step=1, verbose=1)
        sel = sel.fit(X_clean, y)
        selected = X_clean.columns[sel.support_].tolist()
    elif method == "SelectKBest":
        selected = X_clean.columns.tolist()
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # post-filtering: non-EO fallback to SelectKBest
    non_eo = are_all_features_non_eo(selected)
    if non_eo or method == "SelectKBest":
        from sklearn.feature_selection import SelectKBest, f_regression
        k = 15
        skb = SelectKBest(score_func=f_regression, k=k)
        skb.fit(X_clean, y)
        selected = X_clean.columns[skb.get_support()].tolist()

    # return selector (if exists), filtered DataFrame, and feature list
    try:
        return sel, X_clean.loc[:, selected], selected
    except NameError:
        # for methods that didn't create `sel`
        return None, X_clean.loc[:, selected], selected