import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from geocif import utils
from geocif.progress import pbar as _pbar

logger = logging.getLogger(__name__)

# Models that need a model-agnostic SHAP explainer (no TreeExplainer support).
_MODEL_AGNOSTIC_XAI = {"tabpfn", "tabicl", "bnn"}

# TabPFN-family models get the shapiq path (faster + supports k-SII
# interactions + PDP via the new xai_shapiq module). Falls back to
# the SHAP PermutationExplainer if shapiq isn't installed.
_TABPFN_FAMILY = {
    "tabpfn", "tabpfn_ft",
    "curated_tabpfn", "top10_tabpfn", "auto_tabpfn",
}


def _last_n_years_index(df_train, n=5, year_col="Harvest Year"):
    """Return a pandas Index of df_train rows from the most-recent N years
    with data, plus the year range used.

    Used to restrict the SHAP/shapiq background distribution to a
    recent slice so the computed E[f(X)] reflects a current-baseline
    expectation rather than the long-historical mean. Falls back to
    all rows when ``year_col`` is missing or the slice would be empty.

    Returns:
        (idx, (year_min, year_max)) — idx is a pandas Index of row
        labels to keep; year_min / year_max are ints (or None when the
        column wasn't usable).
    """
    if year_col not in df_train.columns or df_train.empty:
        return df_train.index, (None, None)
    try:
        years = pd.to_numeric(df_train[year_col], errors="coerce").dropna()
    except Exception:  # noqa: BLE001
        return df_train.index, (None, None)
    if years.empty:
        return df_train.index, (None, None)
    y_max = int(years.max())
    cutoff = y_max - (n - 1)
    keep_idx = df_train.index[
        pd.to_numeric(df_train[year_col], errors="coerce").fillna(-1).astype(int) >= cutoff
    ]
    if len(keep_idx) < 2:
        # Recent-year slice too small — fall back to everything.
        return df_train.index, (None, None)
    return keep_idx, (cutoff, y_max)


def _is_tabpfn_family(model_name: str) -> bool:
    """True for any tabpfn variant including curated_/top<N>_/auto_."""
    import re as _re
    if model_name in _TABPFN_FAMILY:
        return True
    # Match wrapper-prefix patterns programmatically too
    if model_name.startswith("curated_") and model_name.endswith("tabpfn"):
        return True
    if model_name.startswith("auto_") and model_name.endswith("tabpfn"):
        return True
    if _re.match(r"^top\d+_tabpfn(_ft)?$", model_name):
        return True
    return False


def _model_feature_names(model, fallback_df):
    """Resolve a model's training feature names compatibly.

    CatBoost exposes ``feature_names_``; sklearn-style models (TabPFN, TabICL)
    expose ``feature_names_in_``. Fall back to the dataframe columns if neither
    attribute is set.
    """
    for attr in ("feature_names_", "feature_names_in_"):
        names = getattr(model, attr, None)
        if names is not None:
            return list(names)
    return list(fallback_df.columns)


def explain(df_train, df_test, **kwargs):
    cluster_strategy = kwargs.get("cluster_strategy", "auto_detect")
    model = kwargs.get("model")
    model_name = kwargs.get("model_name")
    forecast_season = kwargs.get("forecast_season")
    crop = kwargs.get("crop")
    country = kwargs.get("country")
    analysis_dir = kwargs.get("analysis_dir")
    db_path = kwargs.get("db_path")

    # Change Harvest Year and Region_ID to type int
    df_test["Harvest Year"] = df_test["Harvest Year"].astype(int)
    df_test["Region_ID"] = df_test["Region_ID"].astype(int)

    df_test.reset_index(inplace=True, drop=True)
    if cluster_strategy == "individual" or len(df_test) == 1:
        model = model
    elif cluster_strategy in ["auto_detect", "single"]:
        # Assume you are using MERF
        # TODO make it user configurable
        # model = model.trained_fe_model
        model = model

    ############################
    # Model specific feature importance
    ############################
    features = _model_feature_names(model, df_train)
    X_train_feat = df_train[features]
    X_test_feat = df_test[features]

    # TabPFN-family: try the shapiq path first (faster + interactions + PDP).
    # If shapiq isn't installed, the explainer returns None and we fall back
    # to the SHAP PermutationExplainer below.
    # Restrict the SHAP / shapiq background to the last 5 years of training
    # data so E[f(X)] reflects a current-baseline expectation rather than
    # the long-historical mean. Falls back to the full training set if the
    # 5-year slice is too small (or "Harvest Year" column is missing).
    bg_idx, bg_year_range = _last_n_years_index(df_train, n=5)
    df_train_bg = df_train.loc[bg_idx]
    X_train_bg = df_train_bg[features]
    if bg_year_range != (None, None):
        logger.info(
            f"  XAI background restricted to last 5 years: "
            f"{bg_year_range[0]}..{bg_year_range[1]} "
            f"({len(X_train_bg)} of {len(X_train_feat)} rows)"
        )

    shapiq_used = False
    if _is_tabpfn_family(model_name):
        from geocif.ml import xai_shapiq

        n_bg = min(50, len(X_train_bg))
        bg_sample = X_train_bg.sample(n=n_bg, random_state=0) if len(X_train_bg) > n_bg else X_train_bg
        target_col_kw = kwargs.get("target_col", "Yield (tn per ha)")
        y_bg = df_train.loc[bg_sample.index, target_col_kw] \
            if target_col_kw in df_train.columns else np.zeros(len(bg_sample))

        # Q4 first: SHAP-compatible values — drops into the existing
        # beeswarm/waterfall/DB-store paths unchanged.
        shap_compat_test = xai_shapiq.explain_shap_compat(
            model, bg_sample, y_bg, X_test_feat, features,
        )
        if shap_compat_test is not None:
            shap_compat_train = xai_shapiq.explain_shap_compat(
                model, bg_sample, y_bg, X_train_feat, features,
            )
            shap_values = shap_compat_train
            shap_values_test = shap_compat_test
            shapiq_used = True

            # Q2: pairwise interactions (k-SII order=2) on the test set
            region_name_for_files = (
                df_test["Region"].iloc[0]
                if "Region" in df_test.columns and len(df_test) else "region"
            )
            shapiq_out = analysis_dir / country / crop / model_name / str(forecast_season)
            xai_shapiq.explain_interactions(
                model, bg_sample, y_bg, X_test_feat, features,
                out_dir=shapiq_out,
                region_name=region_name_for_files,
                forecast_season=forecast_season,
            )

            # Q3: partial dependence for top-N features (global view, once
            # per (country, crop, model, forecast_season) — no per-region
            # variation because PDP averages across regions anyway).
            try:
                mean_abs = np.abs(shap_values.values).mean(axis=0)
            except Exception:  # noqa: BLE001
                mean_abs = None
            xai_shapiq.explain_pdp(
                model, X_train_feat, features,
                out_dir=shapiq_out,
                country=country, crop=crop,
                feature_importance=mean_abs,
                top_n_features=5,
            )

    if not shapiq_used:
        # Strip curated_/top<N>_/auto_/last<N>m_ so variants of the
        # model-agnostic models (e.g. curated_bnn, curated_tabpfn) don't
        # fall through to TreeExplainer, which rejects non-tree models.
        from .trainers import strip_variant_prefix

        if strip_variant_prefix(model_name) in _MODEL_AGNOSTIC_XAI:
            # PermutationExplainer perturbs the feature matrix by subtraction,
            # which crashes on object/string columns (e.g. the categorical
            # "Region" — cat_features = ["Harvest Year", "Region_ID", "Region"]).
            # Drop non-numeric columns ONLY for this branch; TreeExplainer
            # (catboost etc.) needs the full matrix because catboost's
            # internal cat_features index references columns by position
            # in the original feature list (dropping columns shifts indices
            # and raises "Invalid cat_features[i] = N: index must be < N").
            X_train_num = X_train_feat.select_dtypes(include=[np.number])
            X_test_num = X_test_feat.select_dtypes(include=[np.number])
            dropped = [c for c in X_train_feat.columns if c not in X_train_num.columns]
            if dropped:
                logger.warning(
                    f"  SHAP PermutationExplainer ({model_name}): dropped "
                    f"{len(dropped)} non-numeric features {sorted(dropped)} — "
                    f"can't perturb string/object columns."
                )

            # Background must be small because TabPFN/TabICL inference is
            # expensive on CPU. SHAP requires max_evals >= 2 * n_features + 1.
            # Draw the background from the last-5-years slice computed above
            # so E[f(X)] is a current-baseline expectation.
            X_train_num_bg = X_train_bg.select_dtypes(include=[np.number])
            n_bg = min(50, len(X_train_num_bg))
            background = shap.sample(X_train_num_bg, n_bg, random_state=0)
            explainer = shap.PermutationExplainer(model.predict, background)
            n_features_num = X_train_num.shape[1]
            max_evals = max(500, 2 * n_features_num + 1)
            shap_values = explainer(X_train_num, max_evals=max_evals)
            shap_values_test = explainer(X_test_num, max_evals=max_evals)
        else:
            # TreeExplainer (CatBoost / XGBoost / etc) handles categoricals
            # natively via cat_features indices stored in the trained model.
            # Must pass the FULL X_train_feat so column positions match
            # cat_features[i] indices.
            explainer = shap.TreeExplainer(model)
            shap_values = explainer(X_train_feat)
            shap_values_test = explainer(X_test_feat)

    ############################
    # SHAP beeswarm plot
    ############################
    region_name = df_test.Region_ID.unique()[0]

    fig, ax = plt.subplots()
    plt.ioff()  # Hack to avoid weird tkinter error
    ax = shap.plots.beeswarm(shap_values, show=False)
    # ax = shap.plots.bar(shap_values.abs.mean(0), show=False)
    plt.title(f"Region: {region_name}\n{forecast_season}")
    plt.tight_layout()

    fname = f"beeswarm_{region_name}_{forecast_season}.png"
    out_dir = analysis_dir / country / crop / model_name / str(forecast_season)
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(out_dir / fname, dpi=250)
    plt.close()

    ############################
    # SHAP waterfall plot
    ############################
    for idx, row in _pbar(df_test.iterrows(), desc="SHAP waterfall", leave=False):
        region_name = row["Region"]

        try:
            shap.plots.waterfall(shap_values_test[idx], show=False)
        except Exception as e:
            print(f"Exception {e}")
            continue

        plt.title(f"Region: {region_name}\n{forecast_season}")
        plt.tight_layout()

        fname = f"waterfall_{region_name}_{crop}_{forecast_season}.png"
        plt.savefig(out_dir / fname, dpi=250)
        plt.close()

    ############################
    # Persist SHAP values to DB
    ############################
    if db_path is not None:
        _store_shap_to_db(
            db_path, shap_values_test, df_test, features,
            country, crop, model_name, forecast_season,
        )


def _store_shap_to_db(
    db_path, shap_values, df_test, features,
    country, crop, model_name, forecast_season,
):
    """Store SHAP values and feature importance to the SQLite database."""
    # ── shap_values table: one row per test observation ──
    shap_cols = {f"SHAP_{feat}": shap_values.values[:, i]
                 for i, feat in enumerate(features)}

    df_shap = pd.DataFrame(shap_cols)
    df_shap["Country"] = country
    df_shap["Crop"] = crop
    df_shap["Model"] = model_name
    df_shap["Forecast Season"] = str(forecast_season)
    df_shap["Base Value"] = shap_values.base_values

    if "Region" in df_test.columns:
        df_shap["Region"] = df_test["Region"].values
    if "Harvest Year" in df_test.columns:
        df_shap["Harvest Year"] = df_test["Harvest Year"].values

    df_shap.index.set_names(["Index"], inplace=True)

    try:
        utils.to_db(db_path, "shap_values", df_shap)
        logger.info(f"Stored {len(df_shap)} SHAP value rows for {country} {crop} {model_name}")
    except Exception as e:
        logger.warning(f"Failed to store SHAP values: {e}")

    # ── feature_importance table: one row per feature ──
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)

    df_imp = pd.DataFrame({
        "Feature": features,
        "Mean_Abs_SHAP": np.around(mean_abs_shap, 6),
        "Country": country,
        "Crop": crop,
        "Model": model_name,
        "Forecast Season": str(forecast_season),
    })
    df_imp.index.set_names(["Index"], inplace=True)

    try:
        utils.to_db(db_path, "feature_importance", df_imp)
        logger.info(f"Stored {len(df_imp)} feature importance rows for {country} {crop} {model_name}")
    except Exception as e:
        logger.warning(f"Failed to store feature importance: {e}")
