"""Tab 2: AgMet Graphics browser.

Lets users browse pre-generated agmet PNG plots by
country / crop-season-year / admin level / region.
"""

import panel as pn


def create_tab(data):
    """Build the AgMet Graphics tab."""
    index = data.discover_agmet_pngs()

    countries = sorted(index.keys())
    country_w = pn.widgets.Select(name="Country", options=countries, width=220)
    folder_w = pn.widgets.Select(name="Crop / Season / Year", options=[], width=220)
    level_w = pn.widgets.RadioButtonGroup(
        name="Level", options=["adm1", "district"], value="adm1", width=220,
    )
    region_w = pn.widgets.Select(name="Region", options=[], width=220)

    # ── cascading updates ────────────────────────────────────────────

    def _update_folders(event):
        country = event.new
        folders = sorted(index.get(country, {}).keys())
        folder_w.options = folders
        folder_w.value = folders[0] if folders else None

    def _update_regions(*_):
        country = country_w.value
        folder = folder_w.value
        level = level_w.value
        regions = index.get(country, {}).get(folder, {}).get(level, [])
        region_w.options = regions
        region_w.value = regions[0] if regions else None

    country_w.param.watch(_update_folders, "value")
    folder_w.param.watch(_update_regions, "value")
    level_w.param.watch(_update_regions, "value")

    # initialise
    if countries:
        country_w.value = countries[0]

    # ── image pane ───────────────────────────────────────────────────

    image_pane = pn.pane.PNG(None, sizing_mode="scale_width", max_width=1200)

    def _update_image(*_):
        path = data.get_agmet_png(
            country_w.value, folder_w.value, level_w.value, region_w.value,
        )
        if path and path.exists():
            image_pane.object = str(path)
        else:
            image_pane.object = None

    region_w.param.watch(_update_image, "value")
    # trigger initial render
    _update_image()

    sidebar = pn.Column(
        "### Filters",
        country_w, folder_w, level_w, region_w,
        width=250,
    )
    main = pn.Column(image_pane, sizing_mode="stretch_both")

    return pn.Row(sidebar, main, sizing_mode="stretch_both")
