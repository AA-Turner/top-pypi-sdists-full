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
# mitra/mitra_ft: a 12-layer Transformer behind a plain .predict, so the
# permutation path is the only option -- and every permutation is a fresh
# in-context forward pass, so keep do_xai off for them unless the fold count
# is small.
_MODEL_AGNOSTIC_XAI = {"tabpfn", "tabicl", "bnn", "mitra", "mitra_ft"}

# Models fitted on mixed-type frames (string Region next to numeric CIDs) whose
# predict needs every fitted column back: cubist (its Cubist wrapper rejects a
# narrower frame) and kumo (in-context, reindexes queries to the support set).
# The plain permutation branch above drops string columns, so these get their
# own branch: string/category columns are integer-coded for shap to permute and
# decoded to their fitted dtype before geocif's own test-time preprocessing.
_MIXED_TYPE_XAI = {"cubist", "kumo"}
# Each kumo predict is a full in-context forward pass, and permutation SHAP
# sends max_evals x background rows per explained row to the model in ONE call
# (shap's delta masking does not batch): 500 x 50 = 25,000 query rows at the
# defaults, ~10 min per row for kumo-large on one CPU thread. For these models
# explain only the held-out (test) rows -- the ones stored in shap_values --
# on a smaller background and budget, and draw the beeswarm from them
# (train_rows = 0). Additivity stays exact; only the permutation sample shrinks.
_SLOW_XAI = {"kumo": {"train_rows": 0, "background": 10, "max_evals": 200}}

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


def _mixed_type_codec(X_train_feat, X_test_feat):
    """Integer-code the non-numeric columns so shap can permute them.

    Returns (X_train_coded, X_test_coded, decode). ``decode`` turns a coded
    matrix (numpy or DataFrame, as shap passes it) back into a frame with the
    fitted columns and dtypes: codes map to their original levels (category
    columns keep their categories, so numeric-valued categoricals such as
    Region_ID round-trip exactly) and integer columns are cast back. Permutation
    SHAP only swaps in values seen in real rows, so every code is a real level.
    """
    both = pd.concat([X_train_feat, X_test_feat])
    columns = list(X_train_feat.columns)
    dtypes = X_train_feat.dtypes
    levels = {}
    for c in columns:
        # Judge by the fitted (training) dtype too: explain() casts the test
        # rows' Region_ID to int, so the concatenation alone can look numeric.
        if any(
            isinstance(s.dtype, pd.CategoricalDtype) or not pd.api.types.is_numeric_dtype(s)
            for s in (both[c], X_train_feat[c])
        ):
            lv = pd.unique(both[c].dropna().astype(object))
            levels[c] = np.array(list(lv) + [np.nan], dtype=object)  # code -1 -> NaN

    def encode(X):
        out = X.copy()
        for c, lv in levels.items():
            out[c] = pd.Categorical(X[c].astype(object), categories=lv[:-1]).codes.astype(float)
        return out.astype(float)

    def decode(A):
        df = pd.DataFrame(np.asarray(A, dtype=float), columns=columns)
        for c in columns:
            if c in levels:
                vals = levels[c][np.rint(df[c].to_numpy()).astype(int)]
                if isinstance(dtypes[c], pd.CategoricalDtype):
                    df[c] = pd.Categorical(vals, dtype=dtypes[c])
                else:
                    try:
                        df[c] = pd.Series(vals).astype(dtypes[c])
                    except (TypeError, ValueError):
                        df[c] = pd.Series(vals, dtype=object)
            elif pd.api.types.is_integer_dtype(dtypes[c]):
                df[c] = np.rint(df[c]).astype(dtypes[c])
            elif pd.api.types.is_bool_dtype(dtypes[c]):
                df[c] = df[c].astype(bool)
        return df

    return encode(X_train_feat), encode(X_test_feat), decode


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
    from .trainers import strip_variant_prefix

    base_name = strip_variant_prefix(model_name)
    features = _model_feature_names(model, df_train)
    if base_name in _MIXED_TYPE_XAI and not any(
        getattr(model, a, None) is not None for a in ("feature_names_", "feature_names_in_")
    ):
        # kumo records no feature names; df_train is the whole region frame
        # (target and metadata included), so use the fitted column list.
        features = list(kwargs.get("feature_names") or features)
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
    # What E[f(X)] (the waterfall's base value) averages over, stored with the
    # SHAP rows so a reader of the DB (viz/shap_explained.py) can say it.
    bg_years = (f"{bg_year_range[0]}-{bg_year_range[1]}"
                if bg_year_range != (None, None) else "all")
    bg_rows = None

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
            bg_rows = len(bg_sample)

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
        if base_name in _MIXED_TYPE_XAI:
            # predict_fn (from geocif) applies the same test-time
            # preprocessing as predict() -- cubist's fit-column alignment and
            # NaN fills, kumo's train-median fills -- before model.predict.
            predict_fn = kwargs.get("predict_fn") or model.predict
            X_tr_c, X_te_c, decode = _mixed_type_codec(X_train_feat, X_test_feat)
            slow = _SLOW_XAI.get(base_name, {})
            bg_pos = np.flatnonzero(X_train_feat.index.isin(X_train_bg.index))
            bg_c = X_tr_c.iloc[bg_pos] if len(bg_pos) else X_tr_c
            background = shap.sample(bg_c, min(slow.get("background", 50), len(bg_c)), random_state=0)
            bg_rows = len(background)
            if not len(bg_pos):
                bg_years = "all"
            explainer = shap.PermutationExplainer(
                lambda A: np.asarray(predict_fn(decode(A)), dtype=float), background
            )
            max_evals = max(slow.get("max_evals", 500), 2 * X_tr_c.shape[1] + 1)
            shap_values_test = explainer(X_te_c, max_evals=max_evals)
            cap = slow.get("train_rows")
            pos = np.arange(len(X_tr_c))
            if cap is not None and len(pos) > cap:
                pos = np.sort(np.random.RandomState(0).choice(len(pos), cap, replace=False))
            # Plots label feature values from display_data: show the region
            # name, not its integer code.
            try:
                shap_values_test.display_data = X_test_feat.to_numpy()
            except Exception:  # noqa: BLE001
                pass
            if len(pos):
                shap_values = explainer(X_tr_c.iloc[pos], max_evals=max_evals)
                try:
                    shap_values.display_data = X_train_feat.iloc[pos].to_numpy()
                except Exception:  # noqa: BLE001
                    pass
            else:  # beeswarm from the held-out rows
                shap_values = shap_values_test
        elif base_name in _MODEL_AGNOSTIC_XAI:
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
            bg_rows = len(background)
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
            # Path-dependent TreeExplainer: E[f(X)] is over the model's own
            # training rows, not the last-5-years slice.
            bg_rows, bg_years = len(X_train_feat), "all"

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
        # No tight_layout here: shap decides whether each bar's number fits
        # inside the bar while drawing, so shrinking the axes afterwards cut
        # the numbers of narrow bars off. A tight bounding box at save time
        # trims the margins without resizing anything.
        fname = f"waterfall_{region_name}_{crop}_{forecast_season}.png"
        plt.savefig(out_dir / fname, dpi=250, bbox_inches="tight")
        plt.close()

    ############################
    # Persist SHAP values to DB
    ############################
    if db_path is not None:
        _store_shap_to_db(
            db_path, shap_values_test, df_test, features,
            country, crop, model_name, forecast_season,
            background=(bg_rows, bg_years),
        )


def _store_shap_to_db(
    db_path, shap_values, df_test, features,
    country, crop, model_name, forecast_season,
    background=None,
):
    """Store SHAP values and feature importance to the SQLite database.

    ``background`` is (rows, years) of the sample the base value averages over,
    stored as ``Background Rows`` / ``Background Years`` when known.
    """
    # ── shap_values table: one row per test observation ──
    shap_cols = {f"SHAP_{feat}": shap_values.values[:, i]
                 for i, feat in enumerate(features)}

    df_shap = pd.DataFrame(shap_cols)
    # The feature values next to their SHAP values, for dependence plots
    # (how far the forecast moves per unit of an input).
    for feat in features:
        if feat in df_test.columns:
            df_shap[f"VALUE_{feat}"] = df_test[feat].to_numpy()
    df_shap["Country"] = country
    df_shap["Crop"] = crop
    df_shap["Model"] = model_name
    df_shap["Forecast Season"] = str(forecast_season)
    df_shap["Base Value"] = shap_values.base_values
    if background is not None and background[0] is not None:
        df_shap["Background Rows"] = int(background[0])
        df_shap["Background Years"] = str(background[1])

    if "Region" in df_test.columns:
        df_shap["Region"] = df_test["Region"].values
    if "Harvest Year" in df_test.columns:
        df_shap["Harvest Year"] = df_test["Harvest Year"].values

    # to_db upserts on the index. A positional 0..n-1 index made every fold
    # and model overwrite the previous one's rows, so the table kept only the
    # last write; key each row by what it explains instead.
    keys = [c for c in ("Country", "Crop", "Model", "Forecast Season", "Region", "Harvest Year")
            if c in df_shap.columns]
    if "Region" not in keys:
        df_shap["Row"] = np.arange(len(df_shap))
        keys.append("Row")
    df_shap = df_shap.set_index(keys)

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
    }).set_index(["Country", "Crop", "Model", "Forecast Season", "Feature"])  # one row per fold and feature

    try:
        utils.to_db(db_path, "feature_importance", df_imp)
        logger.info(f"Stored {len(df_imp)} feature importance rows for {country} {crop} {model_name}")
    except Exception as e:
        logger.warning(f"Failed to store feature importance: {e}")
