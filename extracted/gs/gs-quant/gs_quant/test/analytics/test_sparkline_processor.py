"""
Copyright 2026 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import datetime as dt

import numpy as np
import pandas as pd

from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.analytics.datagrid import ColumnFormat
from gs_quant.analytics.datagrid.data_column import RenderType
from gs_quant.analytics.processors import SparklineProcessor
from gs_quant.data import DataCoordinate, DataFrequency, DataMeasure


def _get_processor(max_points: int = 100) -> SparklineProcessor:
    coordinate = DataCoordinate(measure=DataMeasure.CLOSE_PRICE, frequency=DataFrequency.DAILY)
    return SparklineProcessor(coordinate, start=dt.date(2021, 1, 1), max_points=max_points)


def test_sparkline_processor_returns_points():
    processor = _get_processor()
    index = pd.date_range('2021-01-01', periods=4, freq='D')
    series = pd.Series([1.0, np.nan, 3.0, 2.0], index=index)
    processor.children_data['a'] = ProcessorResult(True, series)

    result = processor.process()

    assert result.success is True
    assert result.data == {
        'timestamps': [str(index[0]), str(index[2]), str(index[3])],
        'values': [1.0, 3.0, 2.0],
        'last': 2.0,
    }


def test_sparkline_processor_limits_points_and_keeps_last():
    processor = _get_processor(max_points=5)
    series = pd.Series([float(i) for i in range(50)], index=pd.date_range('2021-01-01', periods=50, freq='D'))
    processor.children_data['a'] = ProcessorResult(True, series)

    result = processor.process()

    assert result.success is True
    assert len(result.data['values']) == 5
    assert result.data['values'][0] == 0.0
    assert result.data['values'][-1] == 49.0
    assert result.data['last'] == 49.0


def test_sparkline_processor_limited_points_are_unique():
    for length in range(3, 200):
        for max_points in range(2, length):
            processor = _get_processor(max_points=max_points)
            series = pd.Series([float(i) for i in range(length)])
            processor.children_data['a'] = ProcessorResult(True, series)

            values = processor.process().data['values']

            assert len(values) == max_points
            assert all(a < b for a, b in zip(values, values[1:]))
            assert values[0] == 0.0
            assert values[-1] == float(length - 1)


def test_sparkline_processor_without_data():
    processor = _get_processor()
    assert processor.process().success is False

    processor.children_data['a'] = ProcessorResult(True, pd.Series(dtype=float))
    assert processor.process().success is False


def test_sparkline_processor_serialization():
    processor = _get_processor(max_points=20)
    processor_dict = processor.as_dict()

    assert processor_dict['processorName'] == 'SparklineProcessor'
    assert processor_dict['parameters']['max_points'] == {'type': 'int', 'value': 20}


def test_sparkline_render_type_serialization():
    column_format = ColumnFormat(renderType=RenderType.SPARKLINE)
    assert column_format.as_dict()['renderType'] == 'sparkline'
