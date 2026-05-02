import asyncio
from collections.abc import Callable
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas


class tUnnest(tPandas):
    """
    tUnnest

        Overview

            The tUnnest class is a component for splitting a column in a DataFrame into multiple rows, based on a specified
            separator. This component supports options to drop the original column after splitting and to define a new column
            for the split values.

        :widths: auto

            | source_column  |   Yes    | The name of the column to split into multiple rows.                    |
            | destination    |   No     | The name of the column to store the split values. Defaults to source.  |
            | drop_source    |   No     | Boolean indicating if the original column should be dropped after split.|
            | separator      |   No     | The separator used to split the values. Defaults to ", ".              |

        Returns

            This component returns a DataFrame where the specified `source_column` is split into multiple rows based on the
            `separator`. If `drop_source` is set to True, the original column is removed after the split. Errors related to
            column splitting are logged and raised as exceptions.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tUnnest:
          source_column: warehouse_store_ids
          destination: store_id
          drop_source: true
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.source_column: str = kwargs.pop('source_column', None)
        self.destination: str = kwargs.get('destination', None)
        self.drop_source: bool = kwargs.get('drop_source', False)
        self.separator: str = kwargs.get('separator', ', ')
        if not self.source_column:
            raise ConfigError(
                "Missing Source_column for making unnest."
            )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def _run(self):
        try:
            # Split the column into multiple rows
            df = self.data.assign(
                **{
                    self.destination: self.data[self.source_column].str.split(self.separator)
                }
            ).explode(self.destination)
            if self.drop_source is True:
                # Drop the original column
                df = df.drop(columns=[self.source_column])
            return df
        except Exception as err:
            raise ComponentError(
                f"Unknown error {err!s}"
            ) from err
