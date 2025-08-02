import threading
from abc import ABCMeta
from logging import Logger
from typing import Optional

from jsonpickle import json
from retrying import retry

from sidecar.aws_error_helper import AwsErrorHelper
from sidecar.aws_session import AwsSession
from sidecar.azure_clp.azure_clients import AzureClientsManager
from sidecar.const import Const
from sidecar.model.objects import AzureSidecarConfiguration, ISidecarConfiguration, AwsSidecarConfiguration
from sidecar.services.exceptions import NotReadyYetError
from sidecar.utils import Utils


class SandboxMetadataFetcher(metaclass=ABCMeta):
    def get_value(self) -> str:
        raise NotImplementedError()


class SandboxPublicAddressFetcher(SandboxMetadataFetcher):
    ATTEMPT_TIMEOUT_MINUTES = 30
    ATTEMPT_INTERVAL_SECONDS = 10
    NOT_AVAILABLE = 'NotAvailable'

    def __init__(self, logger: Logger, config: ISidecarConfiguration):
        self._sandbox_id = config.sandbox_id
        self._config = config
        self._logger = logger
        self._value = None
        self._thread = None
        self._lock = threading.RLock()

    def get_value(self) -> str:
        if not self._config.ingress_enabled:
            return self.NOT_AVAILABLE

        with self._lock:
            if not self._value and not self._thread:
                result = self._one_time_safe_fetch()
                if result:
                    self._value = result
                else:
                    self._thread = threading.Thread(target=self._fetching_loop, daemon=True)
                    self._thread.start()
            if self._value:
                return self._value
            raise NotReadyYetError()

    def _fetching_loop(self):
        self._logger.info(f'Staring trying to get sandbox public address')
        result = Utils.retry_on_exception(
            func=lambda: self._get_sandbox_public_ip(),
            interval_in_sec=self.ATTEMPT_INTERVAL_SECONDS,
            timeout_in_sec=self.ATTEMPT_TIMEOUT_MINUTES * 60,
            logger=self._logger,
            logger_msg='getting sandbox public address',
            log_every_n_attempts=6 * 2)  # 12 attempts = ~2min
        with self._lock:
            self._value = result
        self._logger.info(f'Sandbox public address is "{result}"')

    def _one_time_safe_fetch(self) -> Optional[str]:
        try:
            if not self._config.ingress_enabled:
                return self.NOT_AVAILABLE
            return self._get_sandbox_public_ip()
        except:
            return None

    def _get_sandbox_public_ip(self) -> str:
        raise NotImplementedError()


class AwsSandboxPublicAddressFetcher(SandboxPublicAddressFetcher):
    def __init__(self, logger: Logger, config: AwsSidecarConfiguration, aws_session: AwsSession):
        super().__init__(logger=logger, config=config)
        self._session = aws_session

    # Exponential Backoff starts from 1 sec to 2 min, until 2 min, in case of throttling
    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=1000 * 60 * 2,
           stop_max_delay=1000 * 60 * 2,
           retry_on_exception=AwsErrorHelper.is_throttling_error)
    def _get_sandbox_public_ip(self) -> str:
        self._logger.info(f'**** _get_sandbox_public_ip: get stack {self._session.infra_stack_name}')

        stack = self._session.get_cf_resource().Stack(self._session.infra_stack_name)

        self._logger.info(f'**** Infra stack outputs: {json.dumps(stack.outputs)}')

        # for production
        if stack.outputs:
            alb_dns = next((o['OutputValue'] for o in stack.outputs if o['OutputKey'] == 'AlbDns'), None)
        else:
            alb_dns = None

        # for sandboxes
        if not alb_dns:
            # Get ALB arn
            response = self._session.get_cf_client().describe_stack_resource(StackName=self._session.infra_stack_name,
                                                                             LogicalResourceId=Const.MAIN_ALB)
            alb_arn = response['StackResourceDetail']['PhysicalResourceId']
            self._logger.info(f'**** _get_sandbox_public_ip: alb_arn {alb_arn}')

            # Get ALB dns
            response = self._session.get_elb_v2_client().describe_load_balancers(LoadBalancerArns=[alb_arn])
            alb_dns = response['LoadBalancers'][0]['DNSName']

        return alb_dns


class AzureSandboxPublicAddressFetcher(SandboxPublicAddressFetcher):
    def __init__(self, logger: Logger, config: AzureSidecarConfiguration, clients_manager: AzureClientsManager):
        super().__init__(logger=logger, config=config)
        self.clients_manager = clients_manager

    def _get_sandbox_public_ip(self) -> str:
        # Get AG resource group name
        rg_name = self._config.production_id or self._config.sandbox_id

        # Get AG
        if self._config.internet_facing:
            ip = self.clients_manager.network_client.public_ip_addresses.get(resource_group_name=rg_name,
                                                                             public_ip_address_name=Const.AG_PUBLIC_IP)
        else:
            ag = self.clients_manager.network_client.application_gateways.get(resource_group_name=rg_name,
                                                                              application_gateway_name=Const.AG_NAME)
            ip = ag.frontend_ip_configurations.private_ip_address

        if not ip.ip_address:
            raise Exception('ApplicationGateway\'s PublicIpAddress resource does not contain the ip yet')

        return ip.ip_address


class K8sSandboxPublicAddressFetcher(SandboxMetadataFetcher):
    def get_value(self) -> str:
        return ''
