import logging
import os
import ssl
from pathlib import Path

from grpclib.client import Channel
from grpclib.config import Configuration
from stigg import Stigg as StiggClientFactory, AsyncStiggClient

from stigg_sidecar_sdk.generated.stigg.sidecar import v1 as sidecar

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

CA_CERT_PATH = Path(os.path.dirname(__file__), 'certs', 'root-ca.pem')

DEFAULT_SIDECAR_PORT = "80"


class Stigg(sidecar.SidecarServiceStub):
    _api: AsyncStiggClient

    def __init__(self,
                 api_config: sidecar.ApiConfig,
                 *,
                 remote_sidecar_host: str,
                 remote_sidecar_port: int = None,
                 remote_sidecar_use_legacy_tls: bool = False
                 ):
        self._sidecar_port = remote_sidecar_port or DEFAULT_SIDECAR_PORT
        ssl_config = ssl.get_default_verify_paths()._replace(cafile=str(CA_CERT_PATH)) \
            if remote_sidecar_use_legacy_tls else None
        channel = Channel(
            host=remote_sidecar_host,
            port=self._sidecar_port,
            ssl=ssl_config,
            config=Configuration(ssl_target_name_override="localhost")
        )
        super().__init__(channel=channel)

        api_client_args = dict(api_key=api_config.api_key)
        if api_config.api_url:
            api_client_args['api_url'] = api_config.api_url
        if api_config.edge_enabled is not None:
            api_client_args['enable_edge'] = api_config.edge_enabled
        if api_config.edge_api_url:
            api_client_args['edge_api_url'] = api_config.edge_api_url
        self._api = StiggClientFactory.create_async_client(**api_client_args)

    @property
    def api(self):
        return self._api

    def close(self):
        self.channel.close()
