from typing import Any, Dict, List

from tinybird.prompts import mock_prompt
from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import push_data
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.fixture import persist_fixture_sql
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.llm_utils import extract_xml


def append_mock_data(
    tb_client: TinyB,
    datasource_name: str,
    url: str,
):
    push_data(
        tb_client,
        datasource_name,
        url,
        mode="append",
        concurrency=1,
        silent=True,
    )


def create_mock_data(
    datasource_name: str,
    datasource_content: str,
    rows: int,
    prompt: str,
    config: CLIConfig,
    ctx_config: Dict[str, Any],
    user_token: str,
    tb_client: TinyB,
    format_: str,
    folder: str,
) -> List[Dict[str, Any]]:
    user_client = config.get_client(token=ctx_config.get("token"), host=ctx_config.get("host"))
    llm = LLM(user_token=user_token, host=user_client.host)
    prompt = f"<datasource_schema>{datasource_content}</datasource_schema>\n<user_input>{prompt}</user_input>"
    sql = ""
    attempts = 0
    data = []
    error = ""
    sql_path = None
    while True:
        try:
            response = llm.ask(system_prompt=mock_prompt(rows, error), prompt=prompt, feature="tb_mock")
            sql = extract_xml(response, "sql")
            sql_path = persist_fixture_sql(datasource_name, sql, folder)
            sql_format = "JSON" if format_ == "ndjson" else "CSV"
            result = tb_client.query(f"SELECT * FROM ({sql}) LIMIT {rows} FORMAT {sql_format}")
            if sql_format == "JSON":
                data = result.get("data", [])[:rows]
                error_response = result.get("error", None)
                if error_response:
                    raise Exception(error_response)
            else:
                data = result
            break
        except Exception as e:
            error = str(e)
            attempts += 1
            if attempts > 5:
                raise Exception(
                    f"Failed to generate a valid solution. Check {str(sql_path or '.sql path')} and try again."
                )
            else:
                continue
    return data
