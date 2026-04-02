from typing import Any, Callable

from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame
from pyspark.sql.functions import lit

from seshat.general.exceptions import InvalidArgumentsError
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
    safe_import_testcase,
)
from seshat.transformer.deriver.base import SFrameDeriver


class StaticValueColumnAdder(SFrameDeriver):
    """
    A deriver that adds a new column with a static value to a DataFrame.

    This class allows adding a column with either a fixed value or a value generated
    by a function. It supports both pandas DataFrame and PySpark DataFrame.

    Parameters
    ----------
    col_name : str
        The name of the column to be added to the DataFrame.
    value : Any, optional
        The static value to be added to the column. Either this or value_function must be provided.
    value_function : Callable[[], Any], optional
        A function that returns the value to be added to the column. Either this or value must be provided.
    group_keys : dict, optional
        Dictionary mapping group names to their respective keys.

    Raises
    ------
    InvalidArgumentsError
        If neither value nor value_function is provided.

    Examples
    --------
    >>> # Add a column with a static value
    >>> adder = StaticValueColumnAdder(col_name="status", value="active")
    >>> result = adder.derive(dataframe)

    >>> # Add a column with a value from a function
    >>> adder = StaticValueColumnAdder(col_name="timestamp", value_function=lambda: datetime.now())
    >>> result = adder.derive(dataframe)
    """

    def __init__(
        self,
        col_name: str,
        value: Any = None,
        value_function: Callable[[], Any] = None,
        group_keys=None,
    ):
        super().__init__(group_keys)

        self.col_name = col_name
        if not value and not value_function:
            raise InvalidArgumentsError(
                "Either 'value' or 'value_func' must be provided."
            )

        self.value = value
        self.value_func = value_function

    def derive_df(self, default: DataFrame, *args, **kwargs):
        default[self.col_name] = self._get_value()
        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        return {"default": default.withColumn(self.col_name, lit(self._get_value()))}

    def _get_value(self):
        return self.value if self.value else self.value_func()


class StaticValueColumnAdderStory(BaseTransformerStory):
    transformer = StaticValueColumnAdder
    use_cases = [
        (
            "Adding current time to sframe by using value_function that return "
            "current time"
        )
    ]
    logic_overview = "Get the value and add it as new column"
    steps = [
        "If value_func provided run the function to find the value",
        "Add value to the sframe with column name `col_name`",
    ]
    tags = ["deriver", "single-sf-operation"]

    def get_scenarios(self):
        testcase = safe_import_testcase("test", "StaticValueColumnAdderDFTestCase")
        if testcase is None:
            return []
        return TransformerScenario.from_testcase(testcase, transformer=self.transformer)
