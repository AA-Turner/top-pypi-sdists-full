"""Tab 1: Yield Predictions.

Interactive time series of predicted vs observed yield with
cascading filters (country / crop / region / stage / model)
and summary metrics (R², RMSE, MAPE).
"""

import numpy as np
import panel as pn

pn.extension("tabulator")


def create_tab(data):
    """Build the Yield Predictions tab."""
    import hvplot.pandas  # noqa: F401 — activates .hvplot accessor

    tables = data.list_prediction_tables()  # [(country, crop, table), ...]
    country_options = sorted({c for c, _, _ in tables})

    country_w = pn.widgets.Select(name="Country", options=country_options, width=220)
    crop_w = pn.widgets.Select(name="Crop", options=[], width=220)
    model_w = pn.widgets.Select(name="Model", options=[], width=220)
    stage_w = pn.widgets.Select(name="Stage", options=[], width=220)
    region_w = pn.widgets.Select(name="Region", options=[], width=220)

    plot_pane = pn.pane.HoloViews(None, sizing_mode="stretch_both")
    metrics_row = pn.Row()

    # ── cascading filters ────────────────────────────────────────────

    _cache = {}  # table_name -> DataFrame

    def _get_df(table):
        if table not in _cache:
            _cache[table] = data.query_predictions(table)
        return _cache[table]

    def _update_crops(event):
        country = event.new
        crops = sorted({cr for c, cr, _ in tables if c == country})
        crop_w.options = crops
        crop_w.value = crops[0] if crops else None

    def _update_filters(event):
        country = country_w.value
        crop = crop_w.value
        table = next((t for c, cr, t in tables if c == country and cr == crop), None)
        if table is None:
            return
        df = _get_df(table)
        if "Model" in df.columns:
            models = sorted(df["Model"].dropna().unique())
            model_w.options = models
            model_w.value = models[0] if models else None
        if "Stage Name" in df.columns:
            stages = sorted(df["Stage Name"].dropna().unique())
            stage_w.options = stages
            stage_w.value = stages[0] if stages else None
        if "Region" in df.columns:
            regions = sorted(df["Region"].dropna().unique())
            region_w.options = ["All"] + regions
            region_w.value = "All"

    country_w.param.watch(_update_crops, "value")
    crop_w.param.watch(_update_filters, "value")

    # ── plot + metrics ───────────────────────────────────────────────

    def _update_plot(*_):
        country = country_w.value
        crop = crop_w.value
        model = model_w.value
        stage = stage_w.value
        region = region_w.value

        table = next((t for c, cr, t in tables if c == country and cr == crop), None)
        if table is None:
            plot_pane.object = None
            return

        df = _get_df(table)
        mask = df["Model"] == model
        if "Stage Name" in df.columns and stage:
            mask &= df["Stage Name"] == stage
        if region and region != "All" and "Region" in df.columns:
            mask &= df["Region"] == region

        dff = df[mask].copy()
        if dff.empty:
            plot_pane.object = None
            return

        pred_col = "Predicted Yield (tn per ha)"
        obs_col = "Observed Yield (tn per ha)"

        # Aggregate by harvest year (mean across regions if "All")
        group = dff.groupby("Harvest Year")[[pred_col, obs_col]].mean().reset_index()
        group = group.sort_values("Harvest Year")

        plot = group.hvplot.line(
            x="Harvest Year",
            y=[pred_col, obs_col],
            legend="top_left",
            height=400,
            responsive=True,
            title=f"{country.replace('_', ' ').title()} — {crop.replace('_', ' ').title()}",
            ylabel="Yield (tn/ha)",
        )
        plot_pane.object = plot

        # Compute metrics
        valid = group.dropna(subset=[pred_col, obs_col])
        metrics_row.clear()
        if len(valid) >= 3:
            from scipy.stats import pearsonr
            from sklearn.metrics import mean_squared_error, mean_absolute_error

            obs = valid[obs_col].values
            pred = valid[pred_col].values
            r2 = pearsonr(obs, pred)[0] ** 2
            rmse = np.sqrt(mean_squared_error(obs, pred))
            mape_val = np.mean(np.abs((obs - pred) / obs)) * 100

            metrics_row.extend([
                pn.indicators.Number(
                    name="R²", value=round(r2, 3), format="{value:.3f}",
                    font_size="24pt", title_size="10pt",
                ),
                pn.indicators.Number(
                    name="RMSE", value=round(rmse, 3), format="{value:.3f}",
                    font_size="24pt", title_size="10pt",
                ),
                pn.indicators.Number(
                    name="MAPE (%)", value=round(mape_val, 1), format="{value:.1f}",
                    font_size="24pt", title_size="10pt",
                ),
            ])

    for w in [model_w, stage_w, region_w]:
        w.param.watch(_update_plot, "value")
    crop_w.param.watch(lambda e: _update_plot(), "value")

    # initialise
    if country_options:
        country_w.value = country_options[0]
    _update_plot()

    sidebar = pn.Column(
        "### Filters",
        country_w, crop_w, model_w, stage_w, region_w,
        width=250,
    )
    main = pn.Column(plot_pane, metrics_row, sizing_mode="stretch_both")

    return pn.Row(sidebar, main, sizing_mode="stretch_both")
