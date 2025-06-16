import textwrap
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

import plotly

from domino_code_assist import util
from domino_code_assist.util import in_dev_mode, supported_object_store_types


@dataclass(frozen=True)
class Action:
    df_var_out: str = "df"


def pandas_fn_and_params(filename):
    fn_name = filename.lower().split(".")[-1]
    params = ""

    if fn_name.startswith("sas"):
        fn_name = "sas"
        params = ', encoding="utf-8"'
    elif fn_name == "xlsx" or fn_name == "xls":
        fn_name = "excel"
    elif fn_name == "tsv":
        fn_name = "csv"
        params = ', sep="\\t"'

    return fn_name, params


@dataclass(frozen=True)
class ActionOpen(Action):
    filename: Optional[str] = None
    reactive: bool = False

    def render_code(self, df_var_in):
        assert self.filename is not None

        fn_name, params = pandas_fn_and_params(self.filename)
        pd_part = f'pd.read_{fn_name}("{self.filename}"{params})'
        if not self.reactive:
            return f"import pandas as pd\n\n{self.df_var_out} = {pd_part}"

        return textwrap.dedent(
            f"""\
            import pandas as pd
            from domino_code_assist import app

            def load_{self.df_var_out}():
                return {pd_part}

            {self.df_var_out}_reactive = app.ReactiveDf("{self.df_var_out}", load_{self.df_var_out}, "drop dataframe {self.df_var_out} here")
            {self.df_var_out} = {self.df_var_out}_reactive.get()
            """
        )


@dataclass(frozen=True)
class ActionDemo(Action):
    df_name: str = "palmerpenguins"
    reactive: bool = False

    def render_code(self, df_var_in):
        if self.df_name in dir(plotly.data):
            import_part = "import plotly"
            pd_part = f"plotly.data.{self.df_name}()"
        else:
            import_part = "import domino_code_assist as dca"
            pd_part = f"dca.data.{self.df_name}()"

        if not self.reactive:
            return f"{import_part}\n\n{self.df_var_out} = {pd_part}"

        return textwrap.dedent(
            f"""\
            {import_part}
            from domino_code_assist import app

            def load_{self.df_var_out}():
                return {pd_part}

            {self.df_var_out}_reactive = app.ReactiveDf("{self.df_var_out}", load_{self.df_var_out}, "drop dataframe {self.df_var_out} here")
            {self.df_var_out} = {self.df_var_out}_reactive.get()
            """
        )


@dataclass(frozen=True)
class ActionUseNbLocals(Action):
    var_name: Optional[str] = None

    def render_code(self, df_var_in):
        assert self.var_name is not None
        return None


@dataclass(frozen=True)
class ActionDownloadDataSource(Action):
    name: Optional[str] = None
    type_: Optional[str] = None
    use_query: bool = False
    query: Optional[str] = None
    database: Optional[str] = None
    schema: Optional[str] = None
    table: Optional[str] = None
    sample: bool = False
    project: Optional[str] = None
    region: Optional[str] = None

    def render_code(self, df_var_in):
        package = "domino_code_assist.domino_lab_mock" if in_dev_mode() else "domino.data_sources"

        if self.type_ in supported_object_store_types():
            assert self.database
            s3_key = self.database
            fn_name, params = pandas_fn_and_params(s3_key)
            return textwrap.dedent(
                f"""\
                import io
                import pandas as pd
                from {package} import DataSourceClient

                ds = DataSourceClient().get_datasource("{self.name}")

                data = io.BytesIO(ds.get("{s3_key}"))
                {self.df_var_out} = pd.read_{fn_name}(data{params})
                """
            )

        # using limit instead of sample for now, since it's much faster for very large tables. " sample row (10000 rows)"
        query = self.query if self.use_query else f"select * from {self.database}.{self.schema}.{self.table}" + (" limit 2000" if self.sample else "")
        if self.type_ == "BigQueryConfig" and not self.use_query:
            query = f"select * from `{self.project + '.' if self.project else ''}{self.schema}.{self.table}`" + (" limit 2000" if self.sample else "")

        if self.database and self.schema and self.use_query:
            if self.type_ == "SnowflakeConfig":
                return textwrap.dedent(
                    f'''\
                    from {package} import DataSourceClient, SnowflakeConfig

                    ds = DataSourceClient().get_datasource("{self.name}")
                    ds.update(SnowflakeConfig(database="{self.database}", schema="{self.schema}"))

                    res = ds.query("""{query} """)
                    {self.df_var_out} = res.to_pandas()
                    '''
                )

        return textwrap.dedent(
            f'''\
            from {package} import DataSourceClient

            ds = DataSourceClient().get_datasource("{self.name}")
            res = ds.query("""{query} """)
            {self.df_var_out} = res.to_pandas()
            '''
        )


def quote(value):
    if '"' in value:
        if "'" not in value:
            return f"'{value}'"
        if '"""' not in value and not value.endswith('"'):
            return f'"""{value}"""'
        if "'''" not in value and not value.endswith("'"):
            return f"'''{value}'''"
        else:
            return repr(value)
    else:
        return f'"{value}"'


@dataclass(frozen=True)
class ActionFilter(Action):
    col: Optional[str] = None
    dtype: Optional[str] = None
    op: Optional[str] = None
    value: Optional[str] = None
    is_string: bool = False

    def render_code(self, df_var_in):
        if not self.is_string and self.value is not None and self.value.lower() == "nan":
            fn = "notna" if self.op == "!=" else "isna"
            return f'{self.df_var_out} = {df_var_in}.loc[{df_var_in}["{self.col}"].{fn}()]'

        value = self.value
        if self.is_string:
            value = quote(value)

        return f'{self.df_var_out} = {df_var_in}.loc[{df_var_in}["{self.col}"] {self.op} {value}]'

    def is_valid(self):
        return self.col is not None and self.op is not None and self.value is not None and self.df_var_out


@dataclass(frozen=True)
class ActionSelectColumns(Action):
    columns: Optional[List[str]] = None

    def render_code(self, df_var_in):
        assert self.columns
        col_str = ", ".join([f'"{c}"' for c in self.columns])
        return f"{self.df_var_out} = {df_var_in}[[{col_str}]]"

    def is_valid(self):
        return bool(self.columns and self.df_var_out)


@dataclass(frozen=True)
class ActionDropColumns(Action):
    columns: Optional[List[str]] = None

    def render_code(self, df_var_in):
        assert self.columns
        col_str = ", ".join([f'"{c}"' for c in self.columns])
        return f"{self.df_var_out} = {df_var_in}.drop(columns=[{col_str}])"

    def is_valid(self):
        return bool(self.columns and self.df_var_out)


@dataclass(frozen=True)
class ActionGroupBy(Action):
    columns: Optional[List[str]] = None
    aggregations: Optional[List[Tuple[str, str]]] = None
    df_var_out: str = "dfg"

    def render_code(self, df_var_in):
        if not self.columns or not self.aggregations:
            raise Exception("Action not complete")
        col_str = ", ".join([f'"{c}"' for c in self.columns])
        agg_str = ", ".join([f'{util.python_safe_name(name)}_{agg}=("{name}", "{agg}")' for name, agg in self.aggregations])
        code = f"{df_var_in}.groupby([{col_str}]).agg({agg_str}).reset_index()"
        return f"{self.df_var_out} = {code}"

    def is_valid(self):
        return bool(self.columns and self.df_var_out)


@dataclass(frozen=True)
class ActionMerge(Action):
    on_index: bool = False
    suffix: str = "_right"
    auto: bool = True
    var_name_other: Optional[str] = None
    mapping: Dict[Optional[str], Optional[str]] = field(default_factory=lambda: {None: None})
    how: Optional[str] = None

    def render_code(self, df_var_in):
        merge_arg = f", how='{self.how}'" if self.how else ""
        if self.on_index:
            return f"{self.df_var_out} = {df_var_in}.join({self.var_name_other}, rsuffix='{self.suffix}')"
        if self.auto:
            return f"{self.df_var_out} = {df_var_in}.merge({self.var_name_other}{merge_arg})"
        else:
            mapping = self.complete_mapping
            args = f"on={list(mapping.keys())}"
            has_renames = bool({k: v for k, v in mapping.items() if k != v})
            if has_renames:
                args = f"left_on={list(mapping.keys())}, right_on={list(mapping.values())}"
            return f"{self.df_var_out} = {df_var_in}.merge({self.var_name_other}, {args}, suffixes=(None, '{self.suffix}'){merge_arg})"

    def is_valid(self):
        return bool(self.var_name_other and self.df_var_out and (self.on_index or self.auto or self.complete_mapping))

    @property
    def complete_mapping(self):
        return {k: v for k, v in self.mapping.items() if k is not None and v is not None}


def render_code_chunks(actions):
    last_out = None
    chunks = []
    for action in actions:
        code_line = action.render_code(last_out)
        if code_line:
            chunks.append(code_line)
        last_out = action.df_var_out

    chunks.append(action.df_var_out)
    return chunks


def render_code(chunks):
    return "\n".join(chunks)


def to_json(obj):
    if isinstance(obj, Action):
        return {"type_action": {"name": obj.__class__.__name__, "data": asdict(obj)}}


def as_action(dct):
    if "type_action" in dct:
        dct = dct["type_action"]
        return globals()[dct["name"]](**dct["data"])
    return dct


def from_json(dct):
    if "type_action" in dct:
        dct = dct["type_action"]
        return globals()[dct["name"]](**dct["data"])
