# flake8: noqa
md1 = """\
# Palmer penguins

[The Palmer penguins dataset](https://github.com/allisonhorst/palmerpenguins) is a great dataset for data exploration & visualization. 
"""

md2 = """\
## Load data
Code Assist includes this dataset, so you can start exploring Code Assist directly.
"""

md3 = """\
# Transformations: filter out rows

For our analysis, we like to get rid of some rows that have missing data. Using Code Assist, we can filter out these rows using a UI without having to remember the proper Pandas syntax.

You can edit the transformation by hovering above the next code cell, hover about the blue Code Assist button,  and choosing "Edit".
"""

md4 = """\
## Visualizations: exploring penguin bills

To explore the bills of the penguins in this dataset, we create a scatter plot of `bill_length` vs `bill_depth` using the Code Assist UI.

We split the dataset into the two sexes, and three species. Without Code Assist, we would probably have to consult the plotly documentation. Using Code Assist, the options are readily available to us.

We use the "crossfilter" option, which will apply selections made in this plot to be applied as a filter in all other plots and widgets.

You can edit the visualizations by hovering above the next code cell, hover about the blue Code Assist button, and choosing "Edit."
"""

md5 = """\
# Visualizations: exploring the islands

Do bill lengths depend on the island the penguins live on? To explore this question, we generate a second visualization, where we plot the average `bill_length` per island.

Because we again enabled the "crossfilter" options, we can select one or multiple island by dragging over the histograms. This selection will be applied as a filter in the scatter plot.


You can edit the visualizations by hovering above the next code cell, hover about the blue Code Assist button, and choosing "Edit."
"""

md6 = """\
# Crossfilter widgets: selecting the year

To explore any effect or change over the years, we add a widget that allows us to select one or multiple years. This selection is also applied as a filter to the other two visualizations.

You can edit the widget by hovering above the next code cell, hover about the blue Code Assist button, and choosing "Edit".
"""

md7 = """\
The following two markdown cells will be used in the app we will create.
"""

md8 = """\
## Usage

  * Drag in the scatter plot to select a group of penguins. This selection will be applied as a filter to the histogram.
  * Drag to select histograms to select islands. The island selection will be applied as a filter to the scatter plot.
  * Select years to filter the years in the histogram and scatter plot.
  * Double-click a plot to clear the filter.
"""

md9 = """\
## Questions

  * Is there an island that only hosts 1 species?
  * Is there a species that is present on all three islands?
"""

md10 = """\
# Creating a penguin app

We now combined the visualizations, the widget, and a few markdown cells into an interactive web app. We can lay out out the visual elements on a grid by dragging them around.

With a single click on "Deploy app", we can deploy our app, so we can share it with others.

You can edit the app by hovering above the next code cell, hover about the blue Code Assist button, and choosing "Edit".
"""
