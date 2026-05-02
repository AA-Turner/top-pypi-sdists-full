import pytest
import pandas as pd

from flowtask.components.TransposeRows import TransposeRows


def test_transpose_rows():
    """Test the TransposeRows component."""

    # Create a sample dataframe.
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [6, 7, 8, 9, 10],
        'C': [11, 12, 13, 14, 15],
        'D': [16, 17, 18, 19, 20],
        'E': [21, 22, 23, 24, 25]
    })

    # Create a new dataframe with the transposed rows.
    transpose_rows = TransposeRows(pivot=['A', 'B'], value="E", columns={"C": "New_C", "D": "New_D"})
    transpose_rows.input = df
    transpose_rows.run()

    # Check that the new dataframe is correct.
    expected_df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [6, 7, 8, 9, 10],
        'C': [11, 12, 13, 14, 15],
        'D': [16, 17, 18, 19, 20],
        'E': [21, 22, 23, 24, 25]
    })
    expected_df = expected_df.set_index(['A', 'B'])

    assert transpose_rows.result == expected_df
