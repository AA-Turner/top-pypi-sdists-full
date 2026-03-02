import os

import matplotlib.pyplot as plt
import shap
from tqdm import tqdm


def explain(df_train, df_test, **kwargs):
    cluster_strategy = kwargs.get("cluster_strategy", "auto_detect")
    model = kwargs.get("model")
    model_name = kwargs.get("model_name")
    forecast_season = kwargs.get("forecast_season")
    crop = kwargs.get("crop")
    country = kwargs.get("country")
    analysis_dir = kwargs.get("analysis_dir")

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
    shap_values = explainer(df_test[model.feature_names_])
    for idx, row in tqdm(df_test.iterrows(), desc="SHAP waterfall", leave=False):
        region_name = row["Region"]

        try:
            shap.plots.waterfall(shap_values[idx], show=False)
        except Exception as e:
            print(f"Exception {e}")
            continue

        plt.title(f"Region: {region_name}\n{forecast_season}")
        plt.tight_layout()

        fname = f"waterfall_{region_name}_{crop}_{forecast_season}.png"
        plt.savefig(out_dir / fname, dpi=250)
        plt.close()

    # """ Store SHAP scores in dataframe """
    # df["SHAP"] = None
    # df["SHAP Features"] = None
    # for idx, row in df_test.iterrows():
    #     df.at[idx, "SHAP"] = [shap_values[idx].values]
    #     df.at[idx, "SHAP Features"] = shap_values.feature_names
    #
    # return df
