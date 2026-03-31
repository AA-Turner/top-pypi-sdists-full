"""Tab 4: Historical Accuracy + Maps.

Scatter plot of observed vs predicted yield (all regions, color by year),
MAPE distribution histogram, and yield outlook map (pre-generated PNG).
"""

import numpy as np
import panel as pn


def create_tab(data, outlook_root=None):
    """Build the Historical Accuracy tab."""
    import hvplot.pandas  # noqa: F401

    df_metrics = data.query_country_metrics()
    tables = data.list_prediction_tables()
    country_options = sorted({c for c, _, _ in tables})

    if not country_options:
        return pn.pane.Markdown("*No prediction data available.*")

    country_w = pn.widgets.Select(name="Country", options=country_options, width=220)
    crop_w = pn.widgets.Select(name="Crop", options=[], width=220)
    model_w = pn.widgets.Select(name="Model", options=[], width=220)
    stage_w = pn.widgets.Select(name="Stage", options=[], width=220)

    scatter_pane = pn.pane.HoloViews(None, sizing_mode="stretch_both")
    hist_pane = pn.pane.HoloViews(None, sizing_mode="stretch_both")
    map_pane = pn.Column()

    _cache = {}

    def _get_df(table):
        if table not in _cache:
            _cache[table] = data.query_predictions(table)
        return _cache[table]

    # ── cascading filters ────────────────────────────────────────────

    def _update_crops(event):
        crops = sorted({cr for c, cr, _ in tables if c == event.new})
        crop_w.options = crops
        crop_w.value = crops[0] if crops else None

    def _update_models(event):
        table = next(
            (t for c, cr, t in tables if c == country_w.value and cr == crop_w.value),
            None,
        )
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

    country_w.param.watch(_update_crops, "value")
    crop_w.param.watch(_update_models, "value")

    # ── plots ────────────────────────────────────────────────────────

    def _update_plots(*_):
        country = country_w.value
        crop = crop_w.value
        model = model_w.value
        stage = stage_w.value

        table = next(
            (t for c, cr, t in tables if c == country and cr == crop), None,
        )
        if table is None:
            scatter_pane.object = None
            hist_pane.object = None
            return

        df = _get_df(table)
        pred_col = "Predicted Yield (tn per ha)"
        obs_col = "Observed Yield (tn per ha)"

        mask = df["Model"] == model
        if "Stage Name" in df.columns and stage:
            mask &= df["Stage Name"] == stage
        dff = df[mask].dropna(subset=[pred_col, obs_col]).copy()

        # ── scatter: observed vs predicted ──
        if not dff.empty and len(dff) >= 3:
            from scipy.stats import pearsonr
            from sklearn.metrics import mean_squared_error

            obs = dff[obs_col].values
            pred = dff[pred_col].values
            r2 = pearsonr(obs, pred)[0] ** 2
            rmse = np.sqrt(mean_squared_error(obs, pred))

            vmin = min(obs.min(), pred.min()) * 0.9
            vmax = max(obs.max(), pred.max()) * 1.1

            import holoviews as hv
            scatter = dff.hvplot.scatter(
                x=obs_col, y=pred_col,
                c="Harvest Year", cmap="viridis",
                height=400, responsive=True,
                title=f"Observed vs Predicted (R²={r2:.3f}, RMSE={rmse:.3f})",
                xlim=(vmin, vmax), ylim=(vmin, vmax),
            )
            line_11 = hv.Curve(
                [(vmin, vmin), (vmax, vmax)],
            ).opts(color="red", line_dash="dashed", line_width=1)
            scatter_pane.object = scatter * line_11
        else:
            scatter_pane.object = None

        # ── MAPE histogram ──
        df_reg = data.query_regional_metrics()
        if not df_reg.empty:
            sub = df_reg[
                (df_reg["Country"] == country)
                & (df_reg["Crop"] == crop)
                & (df_reg["Model"] == model)
            ]
            mape_col = "Mean Absolute Percentage Error"
            if mape_col in sub.columns and not sub.empty:
                hist_pane.object = sub.hvplot.hist(
                    y=mape_col, bins=20,
                    height=300, responsive=True,
                    title="MAPE Distribution Across Regions",
                    xlabel="MAPE (%)", ylabel="Count",
                    color="#2ca02c",
                )
            else:
                hist_pane.object = None
        else:
            hist_pane.object = None

        # ── outlook map PNG ──
        map_pane.clear()
        outlook_pngs = data.discover_outlook_pngs()
        country_clean = country.replace("_", " ").lower()
        crop_clean = crop.replace("_", " ").lower()
        matched = [
            p for p in outlook_pngs
            if country_clean in p.stem.lower() or crop_clean in p.stem.lower()
        ]
        if matched:
            map_pane.append(pn.pane.Markdown("### Yield Outlook Map"))
            map_pane.append(
                pn.pane.PNG(str(matched[0]), sizing_mode="scale_width", max_width=1000)
            )

    for w in [model_w, stage_w]:
        w.param.watch(_update_plots, "value")
    crop_w.param.watch(lambda e: _update_plots(), "value")

    # initialise
    if country_options:
        country_w.value = country_options[0]
    _update_plots()

    sidebar = pn.Column(
        "### Filters",
        country_w, crop_w, model_w, stage_w,
        width=250,
    )
    main = pn.Column(
        scatter_pane,
        hist_pane,
        map_pane,
        sizing_mode="stretch_both",
    )

    return pn.Row(sidebar, main, sizing_mode="stretch_both")
