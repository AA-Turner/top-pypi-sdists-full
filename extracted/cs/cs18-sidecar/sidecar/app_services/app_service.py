import json
import socket
import threading
from abc import ABCMeta, abstractmethod
from logging import Logger
from time import sleep
from typing import Optional, List, Dict, Tuple

from retrying import retry

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.aws_session import AwsSession
from sidecar.aws_status_maintainer import AWSStatusMaintainer
from sidecar.aws_tag_helper import AwsTagHelper
from sidecar.azure_clp.azure_status_maintainer import AzureStatusMaintainer
from sidecar.azure_clp.azure_clients import AzureClientsManager
from sidecar.const import Const, get_app_selector
from sidecar.kub_api_service import IKubApiService
from sidecar.kub_status_maintainer import KubStatusMaintainer
from sidecar.model.objects import EnvironmentType, AzureSidecarConfiguration, AwsSidecarConfiguration
from sidecar.sandbox_error import SandboxError
from sidecar.utils import Utils, CallsLogger


class StaleAppException(Exception):
    pass


class AppService:
    __metaclass__ = ABCMeta

    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def update_network_status(self, app_name: str, status: str):
        raise NotImplementedError

    @abstractmethod
    def update_artifacts_status(self, app_name: str, status: str):
        raise NotImplementedError

    @abstractmethod
    def get_private_dns_name_by_app_name(self, app_name: str, infra_id: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_sandbox_gateway_address(self, app_name: str, infra_id: str, address_read_timeout: int,
                                    internet_facing: bool) -> str:
        raise NotImplementedError

    @abstractmethod
    def can_access_from_public_address(self, identifier: AppInstanceIdentifier) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_error(self, app_name: str, error: SandboxError):
        raise NotImplementedError


class AzureAppService(AppService):
    def __init__(self, logger: Logger,
                 config: AzureSidecarConfiguration,
                 clients_manager: AzureClientsManager,
                 status_maintainer: AzureStatusMaintainer):
        super().__init__(logger)
        self._config = config
        self._sandbox_id = config.sandbox_id
        self._production_id = config.production_id
        self._network_client = clients_manager.network_client
        self._status_maintainer = status_maintainer
        self._env_type = config.env_type

    def update_network_status(self, app_name: str, status: str):
        self._status_maintainer.update_logical_app_healthcheck_status(app_name=app_name, status=status)

    def update_artifacts_status(self, app_name: str, status: str):
        self._status_maintainer.update_logical_app_artifacts_status(app_name=app_name, status=status)

    def add_error(self, app_name: str, error: SandboxError):
        self._status_maintainer.add_logical_app_error(app_name=app_name, error=error)

    def get_private_dns_name_by_app_name(self, app_name: str, infra_id: str) -> Optional[str]:
        # need this check in order to exclude apps that don't expose any ports at all.
        # checking only the internal ports property because every external port is internal as well
        # and will appear in the list
        internal_ports = self._status_maintainer.get_internal_ports_for_app(app_name=app_name)
        if internal_ports:
            return "{}.{}.sandbox.com".format(app_name, self._sandbox_id)
        else:
            return None

    def get_sandbox_gateway_address(self, app_name: str, infra_id: str, address_read_timeout: int,
                                    internet_facing: bool) -> str:
        if internet_facing:
            return Utils.retry_on_exception(func=lambda: self._get_public_ip_from_app_gateway(),
                                            timeout_in_sec=address_read_timeout, logger=self._logger,
                                            logger_msg="trying to get public dns for app '{}'.".format(app_name))

        return Utils.retry_on_exception(func=lambda: self._get_private_ip_from_app_gateway(),
                                        timeout_in_sec=address_read_timeout, logger=self._logger,
                                        logger_msg="trying to get private ip of application gateway.")

    def _get_private_ip_from_app_gateway(self):
        rg_name = self._get_app_gateway_resource_group_name()
        ag = self._network_client.application_gateways.get(resource_group_name=rg_name,
                                                           application_gateway_name=Const.AG_NAME)
        ag_frontend_ip_configurations = ag.frontend_ip_configurations
        if not ag_frontend_ip_configurations:
            raise Exception(f"App gateway '{ag.name}' has no frontend ip configurations")

        private_ip = ag_frontend_ip_configurations[0].private_ip_address
        if not private_ip:
            raise Exception(f"Ip configuration '{ag.frontend_ip_configurations[0].name}' has no private ip address")

        return private_ip

    def _get_public_ip_from_app_gateway(self) -> str:
        ag_resource_group = self._get_app_gateway_resource_group_name()
        # NOTE: we're getting the ip address via the gateway and not by querying for public_ip_address resource directly
        # because we want to wait for the gateway to be created and attached to the ip address before running public HC
        ag_list = list(self._network_client.application_gateways.list(ag_resource_group))
        if not ag_list:
            raise Exception(f"No application gateways were found in resource group '{ag_resource_group}'")
        if len(ag_list) > 1:
            raise Exception(f"There is more than one application gateway in resource group '{ag_resource_group}'")

        ag = ag_list[0]
        ag_frontend_ip_configurations = ag.frontend_ip_configurations
        if not ag_frontend_ip_configurations:
            raise Exception(f"App gateway '{ag.name}' has no frontend ip configurations")
        if len(ag_frontend_ip_configurations) > 1:
            raise Exception(f"There is more than one ip configuration in app gateway '{ag.name}'")

        ag_frontend_ip_configuration = ag_frontend_ip_configurations[0]
        ag_public_ip_address = ag_frontend_ip_configuration.public_ip_address
        if not ag_public_ip_address:
            raise Exception(f"Ip configuration '{ag_frontend_ip_configuration.name}' has no public ip address")

        public_ip_address_name = ag_public_ip_address.id.rpartition("/")[2]
        public_ip_address = self._network_client.public_ip_addresses.get(ag_resource_group, public_ip_address_name)
        if not public_ip_address:
            raise Exception(f"Public ip address '{public_ip_address_name}' was not found in "
                            f"resource group '{ag_resource_group}'")
        return public_ip_address.ip_address

    def _get_app_gateway_resource_group_name(self):
        return self._production_id or self._sandbox_id

    def can_access_from_public_address(self, identifier: AppInstanceIdentifier) -> bool:
        if not self._config.ingress_enabled:
            return False

        # TODO: should return False for ProductionGreen sandbox but only as long as it's green
        #  - hence cannot use env_type from config but instead should take the tag value that is updated on "promote"
        if self._env_type == EnvironmentType.ProductionGreen:
            return False
        for route in self._status_maintainer.get_ingress_routes():
            if route.app_name == identifier.name and \
                    route.app_port == route.listener_port and \
                    not route.path and not route.host and \
                    route.color.lower() == 'blue':
                return True

        return False


class K8sAppService(AppService):
    DNS_RESOLVING_TIMEOUT = 60 * 3  # 3min

    def __init__(self, api: IKubApiService, sandbox_id: str, logger: Logger,
                 k8s_status_maintainer: KubStatusMaintainer):
        super().__init__(logger)
        self._k8s_status_maintainer = k8s_status_maintainer
        self.sandbox_id = sandbox_id
        self._api = api
        self._lock = threading.RLock()

    @CallsLogger.wrap
    def get_private_dns_name_by_app_name(self, app_name: str, infra_id: str) -> Optional[str]:
        service = self._get_service_of_app(app_name=app_name,
                                           service_type='ClusterIP')
        if not service:
            raise StaleAppException(f"Cannot get '{app_name}' since the service exposing it does not exists.")

        return "{}.{}".format(service['metadata']['name'], self.sandbox_id)

    @CallsLogger.wrap
    def get_sandbox_gateway_address(self, app_name: str, infra_id: str, address_read_timeout: int,
                                    internet_facing: bool) -> str:
        dns_name = Utils.retry_on_exception(func=lambda: self._get_ingress_address_by_app_name(app_name=app_name),
                                            timeout_in_sec=address_read_timeout,
                                            logger=self._logger,
                                            logger_msg=f"getting public dns for app '{app_name}'")
        Utils.retry_on_exception(func=lambda: socket.gethostbyname(dns_name),
                                 timeout_in_sec=self.DNS_RESOLVING_TIMEOUT,
                                 logger=self._logger,
                                 logger_msg=f"resolving public dns to ip for app '{app_name}'")
        return dns_name

    def _get_ingress_address_by_app_name(self, app_name: str) -> Optional[str]:
        service = self._get_service_of_app(app_name=app_name,
                                           service_type='LoadBalancer')
        if not service:
            return None

        if "status" not in service:
            raise StaleAppException(f"Cannot get public dns of '{app_name}' "
                                    f"since the service exposing does not have 'status' yet. "
                                    f"service details: {json.dumps(service)}")

        if "loadBalancer" not in service["status"]:
            raise StaleAppException(f"Cannot get public dns of '{app_name}' "
                                    f"since the service exposing does not have 'status.loadBalancer' yet. "
                                    f"service details: {json.dumps(service)}")

        load_balancer = service["status"]['loadBalancer']
        if "ingress" not in load_balancer:
            raise StaleAppException(f"Cannot get public dns of '{app_name}' "
                                    f"since the service exposing "
                                    f"does not have 'status.loadBalancer.ingress' yet. "
                                    f"service details: {json.dumps(service)}")

        ingress = next(iter(load_balancer['ingress']), None)
        if ingress and "ip" not in ingress and "hostname" not in ingress:
            raise StaleAppException(f"Cannot get public dns of '{app_name}' "
                                    f"since the service exposing "
                                    f"does not have 'status.loadBalancer.ingress.ip' or 'status.loadBalancer.ingress.hostname' yet. "
                                    f"service details: {json.dumps(service)}")

        return ingress['ip'] if "ip" in ingress else ingress['hostname']

    @CallsLogger.wrap
    def update_network_status(self, app_name: str, status: str):
        self._k8s_status_maintainer.update_logical_app_healthcheck_status(
            app_name=app_name,
            status=status)

    @CallsLogger.wrap
    def update_artifacts_status(self, app_name: str, status: str):
        self._k8s_status_maintainer.update_logical_app_artifacts_status(
            app_name=app_name,
            status=status)

    @CallsLogger.wrap
    def add_error(self, app_name: str, error: SandboxError):
        self._k8s_status_maintainer.add_logical_app_error(
            app_name=app_name,
            error=error)

    def _get_service_of_app(self, app_name: str, service_type: str) -> Optional[dict]:
        services = self._api.get_all_services()
        for service in services:
            if service['spec']['selector'] == {get_app_selector(app_name): app_name} and service["spec"][
                "type"] == service_type:
                return service
        return None

    def can_access_from_public_address(self, identifier: AppInstanceIdentifier) -> bool:
        return True


class AWSAppService(AppService):
    PUBLIC_PORT_ACCESS = "public port access"
    PUBLIC_HEALTH_CHECK = "public health check"

    def __init__(self,
                 session: AwsSession,
                 aws_status_maintainer: AWSStatusMaintainer,
                 config: AwsSidecarConfiguration,
                 logger: Logger):

        super().__init__(logger)
        self._aws_status_maintainer = aws_status_maintainer
        self._config = config
        self.default_region = config.onboarding_region
        self._sandbox_id = config.sandbox_id
        self._production_id = config.production_id
        self._table_name = config.data_table_name
        self._env_type = config.env_type
        self._session = session
        self._lock = threading.RLock()

    @CallsLogger.wrap
    def update_network_status(self, app_name: str, status: str):
        self._aws_status_maintainer.update_logical_app_healthcheck_status(app_name=app_name, status=status)

    @CallsLogger.wrap
    def update_artifacts_status(self, app_name: str, status: str):
        self._aws_status_maintainer.update_logical_app_artifacts_status(app_name=app_name, status=status)

    @CallsLogger.wrap
    def add_error(self, app_name: str, error: SandboxError):
        self._aws_status_maintainer.add_logical_app_error(app_name, error)

    def _get_instance_external_ports(self, identifier: AppInstanceIdentifier) -> List[int]:
        ec2_resource = self._session.get_ec2_resource()
        instance = ec2_resource.Instance(identifier.infra_id)
        logical_id = AwsTagHelper.wait_for_tag(instance, Const.INSTANCELOGICALID, self._logger)
        _, item = Utils.retry_on_exception(
            func=lambda: self._get_table(sandbox_id=self._sandbox_id),
            logger=self._logger,
            logger_msg=f'getting dynamo-db table for retrieving instance "{logical_id} external ports')

        instance_data = item['spec']['expected_apps'].get(logical_id)
        if instance_data:
            return [int(port) for app_ports in instance_data['colony-external-ports'].values() for port in app_ports]
        else:
            self._logger.warning('instance id {} was not found under "expected_apps"'.format(logical_id))
            return []

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=1000 * 60 * 2,
           stop_max_delay=1000 * 60 * 5, retry_on_result=lambda x: not x)
    def _get_alb_security_group(self) -> Dict:
        ec2_client = self._session.get_ec2_client()
        if self._production_id:
            response = ec2_client.describe_security_groups(
                Filters=[{'Name': f'tag:{Const.PRODUCTION_ID_TAG}', 'Values': [self._production_id]},
                         {'Name': 'tag:Name', 'Values': [Const.MAIN_ALB_SG]}])
        else:
            response = ec2_client.describe_security_groups(
                Filters=[{'Name': f'tag:{Const.SANDBOX_ID_TAG}', 'Values': [self._sandbox_id]},
                         {'Name': 'tag:Name', 'Values': [Const.MAIN_ALB_SG]}])

        return next(iter(response['SecurityGroups']), None)

    def _get_permissions_for_ports(self, sg: Dict, external_ports: List[int]) -> List[Dict]:
        permissions = [p for p in sg['IpPermissions'] if p['FromPort'] in external_ports]
        permissions = [port
                       for port in permissions
                       if len(port["IpRanges"]) > 0 and len([ip
                                                             for ip in port["IpRanges"]
                                                             if "Description" in ip and ip[
                                                                 "Description"] == self.PUBLIC_PORT_ACCESS]) > 0]
        return permissions

    @CallsLogger.wrap
    def get_private_dns_name_by_app_name(self, app_name: str, infra_id: str) -> Optional[str]:
        instance = self._session.get_ec2_resource().Instance(infra_id)
        internal_ports = AwsTagHelper.wait_for_tags(instance, self._logger).get(Const.INTERNAL_PORTS)
        if internal_ports:
            return "{}.{}.sandbox.com".format(app_name, self._sandbox_id)
        else:
            return None

    @CallsLogger.wrap
    def get_sandbox_gateway_address(self, app_name: str, infra_id: str, address_read_timeout: int,
                                    internet_facing: bool) -> str:
        return Utils.retry_on_exception(func=lambda: self._get_sandbox_alb_dns(instance_id=infra_id),
                                        timeout_in_sec=address_read_timeout,
                                        logger=self._logger,
                                        logger_msg="trying to get sandbox gateway dns for app '{}'.".format(app_name))

    @CallsLogger.wrap
    def can_access_from_public_address(self, identifier: AppInstanceIdentifier) -> bool:
        if not self._config.ingress_enabled:
            return False

        # _, item = Utils.retry_on_exception(
        #     func=lambda: self._get_table(sandbox_id=self._sandbox_id),
        #     logger=self._logger,
        #     logger_msg="Cannot get sandbox {} data for instance {} ports".format(self._sandbox_id, logical_id))
        # TODO: should return False for ProductionGreen sandbox but only while it's green
        #  - hence cannot use env_type from config but instead should take the tag value that is updated on "promote"
        if self._env_type == EnvironmentType.ProductionGreen:
            return False
        for route in self._aws_status_maintainer.get_ingress_routes():
            if route.app_name == identifier.name and \
                    route.app_port == route.listener_port and \
                    not route.path and not route.host and \
                    route.color.lower() == 'blue' and self._session:
                return True

        return False

    def _get_table(self, sandbox_id: str) -> Tuple[any, dict]:
        dynamo_resource = self._session.get_dynamo_resource(default_region=self.default_region)
        table = dynamo_resource.Table(self._table_name)
        item = table.get_item(Key={Const.SANDBOX_ID_TAG: sandbox_id})
        if "Item" not in item:
            raise Exception("dynamodb table is not ready yet")
        return table, item["Item"]

    def _get_sandbox_alb_dns(self, instance_id: str):
        instance = self._session.get_ec2_resource().Instance(instance_id)
        dns = AwsTagHelper.wait_for_tags(instance, self._logger).get(Const.EXTERNAL_ELB_DNS_NAME)
        return dns
