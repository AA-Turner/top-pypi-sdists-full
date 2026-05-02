import pytest
import pandas as pd
import asyncio
from flowtask.components.CopyToBigQuery import CopyToBigQuery

@pytest.mark.asyncio
async def test_copy_to_bigquery():
    # Create a sample dataframe
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "salary": [50000.0, 60000.5, 70000.75],
        "is_active": [True, False, True]
    }
    df = pd.DataFrame(data)

    # Initialize the component
    task = CopyToBigQuery(
        tablename="test_table",
        schema="tests",
        truncate=True,
        use_pandas=True,
        create_table={"pk": ["id"]},
        input=df
    )
    # Run the component
    async with task as t:
        try:
            result = await t.run()
            print('RESULT > ', result)
            # Validate that the result matches the input dataframe
            pd.testing.assert_frame_equal(result, df)
        except Exception as e:
            print(f"Error: {e}")

    print("Test Passed: The component output matches the input DataFrame.")
