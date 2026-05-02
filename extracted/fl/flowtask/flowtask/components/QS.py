"""
    QuerySource.
    QS is a new kind of component supporting the new sources for
    QuerySource and making transformations of data, returning a transformed
    Pandas DataFrame.


        Example:

        ```yaml
        QS:
          query: troc_mileage.tpl
          from_templates_dir: true
          conditions:
            tenant: bose
            firstdate: '{first}'
            lastdate: '{last}'
            forms:
            - 4184
            - 4149
            - 4177
            - 4152
            - 3900
            - 3931
            - 3959
          masks:
            first:
            - date_diff_dow
            - day_of_week: monday
              diff: 8
              mask: '%Y-%m-%d'
            last:
            - date_diff_dow
            - day_of_week: monday
              diff: 2
              mask: '%Y-%m-%d'
        ```

    """
import asyncio
from collections.abc import Callable
import pandas as pd
from asyncdb.exceptions import NoDataFound
from querysource.queries import MultiQS
from querysource.exceptions import DataNotFound as DNF
from querysource.exceptions import (
    ParserError,
    DriverError,
    QueryException,
    SlugNotFound,
)
from querysource.libs.encoders import DefaultEncoder
from querysource.types.validators import is_empty
from ..exceptions import ComponentError, DataNotFound, ConfigError
from .flow import FlowComponent
from ..interfaces.dataframes import PandasDataframe
from ..interfaces import TemplateSupport
from ..utils import SafeDict
from ..utils.transformations import to_camel_case, to_snake_case


class QS(FlowComponent, TemplateSupport, PandasDataframe):
    """
    QS.

    Overview

        Calling Complex QuerySource operations from Flowtask.
        This component supports QuerySource,
        making transformations of data and returning a transformed Pandas DataFrame.

    Component Syntax:
        "QS": {
            "query": "path to file",
            "conditions": {
                "firstdate": "",
                "lastdate": "",
                forms: [1, 2, 3, 4]
            }
        }
        or
        "QS": {
            "slug": "troc_mileage"
        }

    :widths: auto

    | slug                   |   Yes    | The slug identifier for the query.                                           |
    | query                  |   No     | The query template file to use.                                              |
    | conditions             |   No     | Conditions to apply to the query.                                            |
    | map                    |   No     | Dictionary for mapping or transforming the resulting DataFrame.              |
    | infer_types            |   No     | If True, converts DataFrame columns to appropriate dtypes. Default is False. |
    | to_string              |   No     | If True, converts DataFrame columns to string dtype. Default is True.        |
    | use_template           |   No     | If True, use a query template for the query. Default is True.                |

    Returns

    This component returns a pandas DataFrame containing the queried and transformed data.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          QS:
          query: troc_mileage.tpl
          from_templates_dir: true
          conditions:
          tenant: bose
          firstdate: '{first}'
          lastdate: '{last}'
          forms:
          - 4184
          - 4149
          - 4177
          - 4152
          - 3900
          - 3931
          - 3959
          masks:
          first:
          - date_diff_dow
          - day_of_week: monday
          diff: 8
          mask: '%Y-%m-%d'
          last:
          - date_diff_dow
          - day_of_week: monday
          diff: 2
          mask: '%Y-%m-%d'
        ```
    """
    _version = "1.0.0"
    use_template: bool = True

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.slug: str = None
        self._kwargs: dict = {}
        self.to_string: bool = True
        self._queries: dict = {}
        self._files: dict = {}
        self._options: dict = {}
        self.conditions: dict = {}
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._program_tpl = kwargs.get('program', self._program)
        self._encoder = DefaultEncoder()

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        ## define conditions:
        if self.conditions:
            self.set_conditions()
        # Processing Masks
        if hasattr(self, "masks"):
            for key, val in self.conditions.items():
                print('QS KEY :', key, ' Value :', val, ' Masks: ', self._mask)
                if key in self._variables:
                    self.conditions[key] = self._variables[key]
                elif key in self._mask:
                    self.conditions[key] = self.mask_replacement(val)
                elif isinstance(val, str):
                    if val in self._mask:
                        self.conditions[key] = self.mask_replacement(val)
                    else:
                        value = val.format_map(
                            SafeDict(**self._mask)
                        )
                        self.conditions[key] = value
        if 'program' in self.conditions:
            del self.conditions['program']
        if hasattr(self, "query"):
            query = await self.open_templatefile(
                self.query,
                program=self._program_tpl,
                from_templates_dir=self.from_templates_dir,
                **self.conditions
            )
            if not query:
                raise ComponentError(
                    f"Empty Query on Template {self.query}"
                )
            try:
                slug_data = self._encoder.load(query)
                self._logger.notice(
                    f" :: Query :: {slug_data}"
                )
                self._options = slug_data
                self._queries = slug_data.get('queries', {})
                self._files = slug_data.get('files', {})
            except Exception as exc:
                raise ComponentError(
                    f"Unable to decode JSON from Query {query}: {exc}"
                ) from exc

    def from_dict(self, result):
        if not result:
            self._variables["_numRows_"] = 0
            self._variables[f"{self.StepName}_NUMROWS"] = 0
            raise NoDataFound("Data Not Found")
        try:
            df = pd.DataFrame.from_dict(result, orient="columns")
            df.infer_objects()
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes(convert_string=self.to_string)
            if self._debug:
                print(df)
                print("::: Printing Column Information === ")
                columns = list(df.columns)
                for column in columns:
                    t = df[column].dtype
                    print(column, "->", t, "->", df[column].iloc[0])
            self._variables["_numRows_"] = len(df.index)
            self._variables[f"{self.StepName}_NUMROWS"] = len(df.index)
            return df
        except Exception as err:
            self._logger.error(f"{self._driver}: Error Creating Dataframe {err!s}")

    async def run(self):
        try:
            qs = MultiQS(
                slug=self.slug,
                queries=self._queries,
                files=self._files,
                query=self._options
            )
            result, _ = await qs.query()
            if is_empty(result):
                raise DataNotFound(
                    "Data Not Found"
                )
            self._result = result
        except DNF as dnf:
            raise DataNotFound(
                f"Data Not Found in QS: {dnf}",
            )
        except SlugNotFound as snf:
            raise ConfigError(
                f"Slug Not Found: {snf}",
            )
        except ParserError as pe:
            raise ConfigError(
                f"Error parsing Query Slug: {pe}"
            )
        except (QueryException, DriverError) as qe:
            raise ComponentError(
                f"Query Error: {qe}"
            )
        # Mapping:
        if hasattr(self, "map"):
            # transforming dataframe using a Map or auto-map:
            if "auto" in self.map:
                # auto-mapping:
                _case = self.map.get("case", "snake")
                if _case == "snake":
                    self._result = self._result.rename(columns=to_snake_case)
                elif _case == "camel":
                    self._result = self._result.rename(columns=to_camel_case)
                else:
                    self._logger.warning(f"QS Map: Unsupported Map Case {_case}")
            else:
                raise NotImplementedError(
                    "QS Map: Not Implemented Yet."
                )
        numrows = len(self._result.index)
        self.add_metric("NUMROWS", numrows)
        self.add_metric('COLUMNS', self._result.columns.tolist())
        self.add_metric('ROWS', numrows)
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in self._result.dtypes.items():
                print(column, "->", t, "->", self._result[column].iloc[0])
        return self._result

    async def close(self):
        """Closing QS Object."""
