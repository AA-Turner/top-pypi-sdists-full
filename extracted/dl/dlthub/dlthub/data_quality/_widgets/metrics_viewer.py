import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import dlt
    import altair as alt

    import dlthub.data_quality as dq
    from dlthub.data_quality.metrics._reader import get_existing_metrics_from_dataset

    pipeline_name = "metrics_demo"


@app.cell
def _():
    mo.stop(pipeline_name is None)
    pipeline = dlt.attach(pipeline_name)
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(dataset):
    existing_metrics = get_existing_metrics_from_dataset(dataset)
    return (existing_metrics,)


@app.cell
def _(existing_metrics):
    _tables = list(
        sorted(set(m["table_name"] for m in existing_metrics if m["table_name"] is not None))
    ) + [None]
    table_select = mo.ui.dropdown(
        options=_tables, value=_tables[0] if _tables else None, label="Table"
    )
    return (table_select,)


@app.cell
def _(existing_metrics, table_select):
    _columns = list(
        sorted(
            set(
                m["column_name"]
                for m in existing_metrics
                if (m["table_name"] == table_select.value) and m["column_name"] is not None
            )
        )
    ) + [None]
    column_select = mo.ui.dropdown(
        options=_columns, value=_columns[0] if _columns else None, label="Column"
    )
    return (column_select,)


@app.cell
def _(column_select, existing_metrics, table_select):
    _columns = list(
        sorted(
            set(
                m["metric_name"]
                for m in existing_metrics
                if m["table_name"] == table_select.value
                and m["column_name"] == column_select.value
                and m["metric_name"] is not None
            )
        )
    )
    metric_select = mo.ui.dropdown(
        options=_columns, value=_columns[0] if _columns else None, label="Metric"
    )
    return (metric_select,)


@app.cell
def _(column_select, metric_select, table_select):
    mo.hstack([metric_select, table_select, column_select], justify="start")
    return


@app.cell
def _():
    _options = {"load_id": "_dlt_load_id", "load_time": "loaded_at"}
    x_axis_select = mo.ui.dropdown(options=_options, value="load_id", label="X-axis")
    x_axis_select
    return


@app.cell
def _(column_select, metric_select, table_select):
    metric_name = (
        metric_select.value[0] if isinstance(metric_select.value, list) else metric_select.value
    )
    column_name = column_select.value
    table_name = table_select.value
    return column_name, metric_name, table_name


@app.cell
def _(metric_table, metric_name, column_name, x_axis_select):
    _x_col = x_axis_select.value
    _x_title = "Load id" if _x_col == "_dlt_load_id" else "Load time"
    _y_title = f"{metric_name}({column_name})"

    alt.Chart(metric_table).mark_line(point=True).encode(
        x=alt.X(_x_col, title=_x_title),
        y=alt.Y("metric_value", title=_y_title),
        tooltip=["loaded_at", "_dlt_load_id", "metric_name", "metric_value"],
    ).interactive()
    return


@app.cell
def _(column_name, dataset, metric_name, table_name):
    metric_table = dq.read_metric(dataset, table_name, column_name, metric=metric_name).arrow()
    metric_table
    return


if __name__ == "__main__":
    app.run()
