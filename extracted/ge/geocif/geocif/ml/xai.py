import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from tqdm import tqdm

from geocif import utils

logger = logging.getLogger(__name__)


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
    explainer = shap.TreeExplainer(model)
    # shap.KernelExplainer(model.predict, df_train[selected_features])
    # Ensure that train and test dataframes have the same columns by using feature_names_

    shap_values = explainer(df_train[model.feature_names_])

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
    shap_values_test = explainer(df_test[model.feature_names_])
    for idx, row in tqdm(df_test.iterrows(), desc="SHAP waterfall", leave=False):
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
            db_path, shap_values_test, df_test, model,
            country, crop, model_name, forecast_season,
        )


def _store_shap_to_db(
    db_path, shap_values, df_test, model,
    country, crop, model_name, forecast_season,
):
    """Store SHAP values and feature importance to the SQLite database."""
    features = model.feature_names_

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
        logger.info("Stored %d SHAP value rows for %s %s %s",
                     len(df_shap), country, crop, model_name)
    except Exception as e:
        logger.warning("Failed to store SHAP values: %s", e)

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
        logger.info("Stored %d feature importance rows for %s %s %s",
                     len(df_imp), country, crop, model_name)
    except Exception as e:
        logger.warning("Failed to store feature importance: %s", e)
