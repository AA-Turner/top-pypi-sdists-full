import atexit
import json
import logging
import os
import ssl
import subprocess
import sys
import threading
import typing
from pathlib import Path

from grpclib.client import Channel
from grpclib.config import Configuration
from stigg import Stigg as StiggClientFactory, AsyncStiggClient

from stigg_sidecar_sdk.generated.stigg.sidecar import v1 as sidecar

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

SIDECAR_NPM_PACKAGE_NAME = os.environ.get('SIDECAR_NPM_PACKAGE_NAME', f'@stigg/sidecar@latest')

CA_CERT_PATH = Path(os.path.dirname(__file__), 'certs', 'root-ca.pem')

LOCAL_SIDECAR_HOST = "localhost"
DEFAULT_SIDECAR_PORT = "80"

SIDECAR_READY_LOG_MSG = 'Sidecar is ready'


def _get_local_sidecar_platform():
    if sys.platform.startswith('linux'):
        local_sidecar_platform = 'sidecar-linux'
    elif sys.platform.startswith('darwin'):
        local_sidecar_platform = 'sidecar-macos'
    else:
        raise RuntimeError(f'Unsupported local sidecar platform: {sys.platform}')
    return local_sidecar_platform


class Stigg(sidecar.SidecarServiceStub):
    _sidecar_process: typing.Optional[subprocess.Popen] = None
    _sidecar_supervisor: typing.Optional[threading.Thread] = None
    _api: AsyncStiggClient

    def __init__(self,
                 api_config: sidecar.ApiConfig,
                 *,
                 local_sidecar_config: sidecar.LocalSidecarConfig = None,
                 remote_sidecar_host: str = None,
                 remote_sidecar_port: int = None,
                 remote_sidecar_use_legacy_tls: bool = False
                 ):
        if not remote_sidecar_host:
            logger.warning(f"remote_sidecar_host was not provided, a sidecar process will be spawned. "
                           f"Please note that its not intended for production use!")
        self._sidecar_port = remote_sidecar_port or DEFAULT_SIDECAR_PORT
        ssl_config = ssl.get_default_verify_paths()._replace(cafile=str(CA_CERT_PATH)) \
            if remote_sidecar_use_legacy_tls else None
        channel = Channel(
            host=remote_sidecar_host or LOCAL_SIDECAR_HOST,
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

        if not remote_sidecar_host:
            self._spawn_sidecar(api_config, local_sidecar_config)

    @property
    def api(self):
        return self._api

    def close(self):
        self.channel.close()
        self._terminate_sidecar()

    def _spawn_sidecar(self, api_config: sidecar.ApiConfig, sc_config: sidecar.LocalSidecarConfig = None):
        atexit.register(self._terminate_sidecar)

        env = os.environ.copy()
        env['PORT'] = self._sidecar_port or ''
        env['SERVER_API_KEY'] = api_config.api_key or ''
        env['API_URL'] = api_config.api_url or ''
        env['EDGE_ENABLED'] = str(api_config.edge_enabled or '')
        env['EDGE_API_URL'] = api_config.edge_api_url or ''

        if sc_config:
            env['WS_ENABLED'] = str(sc_config.ws_enabled or '')
            env['WS_URL'] = sc_config.ws_url or ''

            redis_config = sc_config.redis
            if redis_config:
                env['REDIS_ENVIRONMENT_PREFIX'] = redis_config.environment_prefix or ''
                env['REDIS_HOST'] = redis_config.host or ''
                env['REDIS_PORT'] = str(redis_config.port or '')
                env['REDIS_DB'] = str(redis_config.db or '')
                env['REDIS_USERNAME'] = redis_config.username or ''
                env['REDIS_PASSWORD'] = redis_config.password or ''
                env['REDIS_KEYS_TTL_IN_SECS'] = str(redis_config.ttl or '')

            env['CACHE_MAX_SIZE_BYTES'] = str(sc_config.cache_max_size_bytes or '')
            env['ENTITLEMENTS_FALLBACK'] = json.dumps(
                sc_config.entitlements_fallback) if sc_config.entitlements_fallback and len(
                sc_config.entitlements_fallback.keys()) > 0 else ''

        local_sidecar_platform = _get_local_sidecar_platform()

        self._sidecar_process = subprocess.Popen(
            ['npx', '-p', SIDECAR_NPM_PACKAGE_NAME, '-y', local_sidecar_platform],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd='/',
            env=env
        )

        self._wait_for_sidecar_is_ready()

    def _wait_for_sidecar_is_ready(self):
        while True:
            output = next(self._read_sidecar_output())
            if SIDECAR_READY_LOG_MSG in output:
                break

        self._sidecar_supervisor = threading.Thread(target=self._read_sidecar_output, daemon=True)
        self._sidecar_supervisor.start()

    def _read_sidecar_output(self):
        while True:
            output = self._sidecar_process.stdout.readline()
            if output:
                logger.info(f'[Local Sidecar] {output}')
                yield output
            elif self._sidecar_process.poll() is not None:
                raise RuntimeError("Sidecar process terminated")

    def _terminate_sidecar(self):
        try:
            if self._sidecar_process:
                self._sidecar_process.terminate()
        except Exception:
            logger.exception('Failed to terminate sidecar process')
