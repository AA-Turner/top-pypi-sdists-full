from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import push_data


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
