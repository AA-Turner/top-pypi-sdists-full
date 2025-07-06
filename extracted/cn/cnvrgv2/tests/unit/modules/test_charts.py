import pytest

from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.utils.chart_utils import BarChart, CHART_TYPES, Heatmap, LineChart, ScatterPlot


class TestCharts:
    def test_create_line_chart(self):
        new_chart = LineChart(key="test_chart")

        assert new_chart.chart_type == CHART_TYPES.LINE

    def test_create_bar_chart(self):
        new_chart = BarChart(key="test_bar")

        assert new_chart.chart_type == CHART_TYPES.BAR

    def test_create_scatter_chart(self):
        new_chart = ScatterPlot(key="test_scatter")

        assert new_chart.chart_type == CHART_TYPES.SCATTER

    def test_create_heatmap_chart(self):
        new_chart = Heatmap(key="test_heatmap")

        assert new_chart.chart_type == CHART_TYPES.HEATMAP

    def test_add_regular_series(self):
        new_chart = LineChart(key="test_chart")
        series_name = "test"
        series_values = [1, 2, 3]

        new_chart.add_series(series_values, series_name)
        assert new_chart.series_list[0].get("data")[0] == 1

    def test_add_faulty_regular_series(self):
        new_chart = LineChart(key="test_faulty_series")
        series_name = "test"
        series_values = 'a'

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            new_chart.add_series(series_name, series_values)

        assert "Series" in str(exception_info.value)

    def test_add_non_numeric_series(self):
        new_chart = LineChart(key="test_faulty_series")
        series_name = "test"
        series_values = [1, 'a', 3]

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            new_chart.add_series(series_name, series_values)

        assert "Series" in str(exception_info.value)

    def test_add_heatmap_series(self):
        new_chart = Heatmap(key="test_chart")
        series_name = "test"
        series_values = [(1, 2, 3), (1, 2, 3)]

        new_chart.add_series(series_values, series_name)
        assert new_chart.series_list[0].get("data")[0] == (0, 0, 1)

    def test_add_faulty_heatmap_value_length(self):
        new_chart = Heatmap(key="test_heatmap_faulty")
        series_name = "test"
        series_values = [(1, 2), (1, 2, 3), (1, 2)]

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            new_chart.add_series(series_values, series_name)

        assert "Heatmap" in str(exception_info.value)

    def test_add_faulty_heatmap_value_type(self):
        new_chart = Heatmap(key="test_heatmap_faulty")
        series_name = "test"
        series_values = [(1, 2, 3), (1, 2, 'a'), (1, 2, 3)]

        with pytest.raises(CnvrgArgumentsError) as exception_info:
            new_chart.add_series(series_values, series_name)

        assert "Heatmap" in str(exception_info.value)

    def test_series_add_same_name_multiple_times(self):
        new_chart = LineChart(key="test")
        new_chart.add_series([1, 2, 3], name="test")

        try:
            new_chart.add_series([4, 5, 6], name="test")
        except AttributeError:
            raise pytest.fail("DID RAISE {0}".format(AttributeError))

    def test_add_faulty_heatmap_step(self):
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            Heatmap(key="test_heatmap_faulty", step=1)

        assert "group" in str(exception_info.value)

    def test_add_group_and_step_non_heatmap(self):
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            LineChart(key="non_hm_group", group="test", step=1)

        assert "Heatmaps" in str(exception_info.value)
