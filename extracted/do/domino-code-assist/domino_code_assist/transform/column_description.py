import ipyvuetify as v
import ipywidgets
import numpy as np
import pandas as pd
import plotly.express as px
import solara
import traitlets
import vaex
from pandas.api.types import is_numeric_dtype


@solara.memoize(key=lambda df, column: id(df[column]) if column in df.columns else None)
def get_column_description(df, column):
    if column not in df.columns:
        return None, None

    column = column
    df_vx = vaex.from_pandas(df[[column]])
    unique_future = df_vx[column].unique(limit=1000, dropna=True, delay=True)
    description = df_vx.describe().to_dict()[column]
    value_counts = None

    if unique_future.value:
        value_counts = df_vx[column].value_counts()

    for k in ["count", "mean", "std", "min", "max", "NA"]:
        if isinstance(description.get(k), np.ndarray):
            description[k] = description[k].tolist()
    description["data_type"] = repr(description["data_type"])

    description["unique"] = unique_future.value
    try:
        description["unique"].sort()
    except Exception:
        pass

    dtype = str(df[column].dtype)
    if description["data_type"] == dtype:
        description.pop("data_type")

    nbins = 20
    histogram_fig = None
    if value_counts is not None and (len(value_counts) <= nbins or not is_numeric_dtype(df[column])):
        histogram_fig = px.bar(x=value_counts.index, y=value_counts.values)
    else:
        if is_numeric_dtype(df[column]):
            binby = df_vx.count(binby=df_vx[column], limits=[description["min"], description["max"] + 0.000000000001], shape=nbins)
            bins = df_vx.bin_edges(None, limits=[description["min"], description["max"]], shape=nbins)[:-1]
            histogram_fig = px.bar(pd.DataFrame(data={"x": bins.tolist(), "y": binby.tolist()}), x="x", y="y")
    if histogram_fig:
        histogram_fig.update_layout(
            bargap=0,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title=None,
            yaxis={
                "showgrid": False,
                "zeroline": False,
                "visible": False,
            },
        )

    description = {
        "description": description,
        "dtype": dtype,
    }

    return description, histogram_fig


class ColumnDescriptionWidget(v.VuetifyTemplate):
    template_file = (__file__, "column_description.vue")

    column = traitlets.Unicode(allow_none=True).tag(sync=True)
    info = traitlets.Dict(allow_none=True).tag(sync=True)
    histogram = traitlets.Any(allow_none=True).tag(sync=True, **ipywidgets.widget_serialization)
    loading = traitlets.Bool(False).tag(sync=True)
    error = traitlets.Unicode(allow_none=True).tag(sync=True)


@solara.component
def ColumnDescription(df, column):
    last_column = solara.use_previous(column, column is not None)
    # the column we use for the description, is the current column, or when None, the last column
    # this makes sure we finish a calculation when the user hovers aways from the column info menu
    used_column = column or last_column
    stats_result: solara.Result = get_column_description.use_thread(df, used_column)
    loading = stats_result.state == solara.ResultState.RUNNING
    info, histogram_fig = stats_result.value if stats_result.value is not None else (None, None)

    def make_histogram():
        if histogram_fig:
            # force creation of a new figure widget when the plotly figure changes
            # if solara gets a FigurePlotly component that is better at updating
            # data we can avoid that
            return solara.FigurePlotly(histogram_fig).key(str(id(histogram_fig)))
        return None

    # When the histogram_fig becomes None or we change the histogram_fig we create a new
    # element, otherwise we reuse the previous one
    histogram = solara.use_memo(make_histogram, [bool(histogram_fig) and id(histogram_fig)])
    return ColumnDescriptionWidget.element(
        column=used_column,
        info=info,
        histogram=histogram,
        loading=loading,
        error=repr(stats_result.error) if stats_result.state == solara.ResultState.ERROR else None,
    )
