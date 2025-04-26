from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import StrictUndefined

from tecton_core import data_types
from tecton_core.aggregation_utils import get_aggregation_function_name
from tecton_snowflake.snowflake_type_utils import tecton_type_to_snowflake_type


def snowflake_function(value):
    fn = get_aggregation_function_name(value)
    if fn == "mean":
        return "avg"
    return fn


def load_template(name):
    env = Environment(
        loader=PackageLoader("tecton_snowflake"),
        autoescape=False,
        undefined=StrictUndefined,
    )
    env.globals["data_types"] = data_types
    env.filters["snowflake_function"] = snowflake_function
    env.globals["tecton_type_to_snowflake_type"] = tecton_type_to_snowflake_type
    return env.get_template(name)
