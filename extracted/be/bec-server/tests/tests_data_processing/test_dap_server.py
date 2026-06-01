from unittest import mock

from bec_lib.service_config import ServiceConfig
from bec_server.data_processing.dap_server import DAPServer
from bec_server.data_processing.dap_service import DAPServiceBase


def test_dap_server():
    config = ServiceConfig()
    server = DAPServer(
        config=config, connector_cls=mock.MagicMock(), provided_services=DAPServiceBase, forced=True
    )
    assert server._service_id == "DAPServiceBase"
