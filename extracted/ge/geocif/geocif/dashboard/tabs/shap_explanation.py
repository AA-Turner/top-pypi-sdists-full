"""Tab 3: Model Explanation (SHAP).

Feature importance bar chart (top 20 by mean |SHAP|) and
SHAP value distribution strip plot, filtered by
country / crop / model / forecast season.
"""

import panel as pn


def create_tab(data):
    """Build the SHAP Model Explanation tab."""
    import hvplot.pandas  # noqa: F401

    df_imp = data.query_feature_importance()
    has_imp = not df_imp.empty

    # Determine available filter values from feature_importance or shap_values
    if has_imp:
        countries = sorted(df_imp["Country"].dropna().unique())
    else:
        df_shap = data.query_shap_values()
        countries = sorted(df_shap["Country"].dropna().unique()) if not df_shap.empty else []

    if not countries:
        return pn.pane.Markdown("*No SHAP data available.*")

    country_w = pn.widgets.Select(name="Country", options=countries, width=220)
    crop_w = pn.widgets.Select(name="Crop", options=[], width=220)
    model_w = pn.widgets.Select(name="Model", options=[], width=220)
    season_w = pn.widgets.Select(name="Forecast Season", options=[], width=220)

    imp_pane = pn.pane.HoloViews(None, sizing_mode="stretch_both")
    dist_pane = pn.pane.HoloViews(None, sizing_mode="stretch_both")

    # ── cascading filters ────────────────────────────────────────────

    def _update_crops(event):
        src = df_imp if has_imp else data.query_shap_values()
        crops = sorted(src[src["Country"] == event.new]["Crop"].dropna().unique())
        crop_w.options = crops
        crop_w.value = crops[0] if crops else None

    def _update_models(event):
        src = df_imp if has_imp else data.query_shap_values()
        sub = src[(src["Country"] == country_w.value) & (src["Crop"] == crop_w.value)]
        models = sorted(sub["Model"].dropna().unique())
        model_w.options = models
        model_w.value = models[0] if models else None

    def _update_seasons(event):
        src = df_imp if has_imp else data.query_shap_values()
        sub = src[
            (src["Country"] == country_w.value)
            & (src["Crop"] == crop_w.value)
            & (src["Model"] == model_w.value)
        ]
        seasons = sorted(sub["Forecast Season"].dropna().unique())
        season_w.options = seasons
        season_w.value = seasons[0] if seasons else None

    country_w.param.watch(_update_crops, "value")
    crop_w.param.watch(_update_models, "value")
    model_w.param.watch(_update_seasons, "value")

    # ── plots ────────────────────────────────────────────────────────

    def _update_plots(*_):
        country = country_w.value
        crop = crop_w.value
        model = model_w.value
        season = season_w.value

        # Feature importance bar chart
        if has_imp:
            sub = df_imp[
                (df_imp["Country"] == country)
                & (df_imp["Crop"] == crop)
                & (df_imp["Model"] == model)
                & (df_imp["Forecast Season"] == season)
            ].nlargest(20, "Mean_Abs_SHAP")

            if not sub.empty:
                imp_pane.object = sub.hvplot.barh(
                    y="Feature", x="Mean_Abs_SHAP",
                    title="Feature Importance (Mean |SHAP|)",
                    height=500, responsive=True,
                    color="#1f77b4",
                    invert=True,
                )
            else:
                imp_pane.object = None

        # SHAP value distribution strip plot
        df_shap = data.query_shap_values()
        if not df_shap.empty:
            sub_shap = df_shap[
                (df_shap["Country"] == country)
                & (df_shap["Crop"] == crop)
                & (df_shap["Model"] == model)
                & (df_shap["Forecast Season"] == season)
            ]
            shap_cols = [c for c in sub_shap.columns if c.startswith("SHAP_")]
            if shap_cols and not sub_shap.empty:
                melted = sub_shap[shap_cols].melt(
                    var_name="Feature", value_name="SHAP Value",
                )
                melted["Feature"] = melted["Feature"].str.replace("SHAP_", "", regex=False)

                # Keep top 20 features by mean absolute
                top = (
                    melted.groupby("Feature")["SHAP Value"]
                    .apply(lambda x: x.abs().mean())
                    .nlargest(20)
                    .index.tolist()
                )
                melted = melted[melted["Feature"].isin(top)]

                dist_pane.object = melted.hvplot.scatter(
                    x="SHAP Value", y="Feature",
                    height=500, responsive=True,
                    alpha=0.3, size=10,
                    title="SHAP Value Distribution",
                )
            else:
                dist_pane.object = None
        else:
            dist_pane.object = None

    season_w.param.watch(_update_plots, "value")

    # initialise
    if countries:
        country_w.value = countries[0]
    _update_plots()

    sidebar = pn.Column(
        "### Filters",
        country_w, crop_w, model_w, season_w,
        width=250,
    )
    main = pn.Column(
        pn.Row(imp_pane, dist_pane, sizing_mode="stretch_both"),
        sizing_mode="stretch_both",
    )

    return pn.Row(sidebar, main, sizing_mode="stretch_both")
