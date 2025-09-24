r'''
# `newrelic_cloud_azure_integrations`

Refer to the Terraform Registry for docs: [`newrelic_cloud_azure_integrations`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class CloudAzureIntegrations(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrations",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations newrelic_cloud_azure_integrations}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        api_management: typing.Optional[typing.Union["CloudAzureIntegrationsApiManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        app_gateway: typing.Optional[typing.Union["CloudAzureIntegrationsAppGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        app_service: typing.Optional[typing.Union["CloudAzureIntegrationsAppService", typing.Dict[builtins.str, typing.Any]]] = None,
        containers: typing.Optional[typing.Union["CloudAzureIntegrationsContainers", typing.Dict[builtins.str, typing.Any]]] = None,
        cosmos_db: typing.Optional[typing.Union["CloudAzureIntegrationsCosmosDb", typing.Dict[builtins.str, typing.Any]]] = None,
        cost_management: typing.Optional[typing.Union["CloudAzureIntegrationsCostManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        data_factory: typing.Optional[typing.Union["CloudAzureIntegrationsDataFactory", typing.Dict[builtins.str, typing.Any]]] = None,
        event_hub: typing.Optional[typing.Union["CloudAzureIntegrationsEventHub", typing.Dict[builtins.str, typing.Any]]] = None,
        express_route: typing.Optional[typing.Union["CloudAzureIntegrationsExpressRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        firewalls: typing.Optional[typing.Union["CloudAzureIntegrationsFirewalls", typing.Dict[builtins.str, typing.Any]]] = None,
        front_door: typing.Optional[typing.Union["CloudAzureIntegrationsFrontDoor", typing.Dict[builtins.str, typing.Any]]] = None,
        functions: typing.Optional[typing.Union["CloudAzureIntegrationsFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key_vault: typing.Optional[typing.Union["CloudAzureIntegrationsKeyVault", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer: typing.Optional[typing.Union["CloudAzureIntegrationsLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        logic_apps: typing.Optional[typing.Union["CloudAzureIntegrationsLogicApps", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_learning: typing.Optional[typing.Union["CloudAzureIntegrationsMachineLearning", typing.Dict[builtins.str, typing.Any]]] = None,
        maria_db: typing.Optional[typing.Union["CloudAzureIntegrationsMariaDb", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["CloudAzureIntegrationsMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql: typing.Optional[typing.Union["CloudAzureIntegrationsMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql_flexible: typing.Optional[typing.Union["CloudAzureIntegrationsMysqlFlexible", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["CloudAzureIntegrationsPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_flexible: typing.Optional[typing.Union["CloudAzureIntegrationsPostgresqlFlexible", typing.Dict[builtins.str, typing.Any]]] = None,
        power_bi_dedicated: typing.Optional[typing.Union["CloudAzureIntegrationsPowerBiDedicated", typing.Dict[builtins.str, typing.Any]]] = None,
        redis_cache: typing.Optional[typing.Union["CloudAzureIntegrationsRedisCache", typing.Dict[builtins.str, typing.Any]]] = None,
        service_bus: typing.Optional[typing.Union["CloudAzureIntegrationsServiceBus", typing.Dict[builtins.str, typing.Any]]] = None,
        sql: typing.Optional[typing.Union["CloudAzureIntegrationsSql", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_managed: typing.Optional[typing.Union["CloudAzureIntegrationsSqlManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["CloudAzureIntegrationsStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["CloudAzureIntegrationsVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_networks: typing.Optional[typing.Union["CloudAzureIntegrationsVirtualNetworks", typing.Dict[builtins.str, typing.Any]]] = None,
        vms: typing.Optional[typing.Union["CloudAzureIntegrationsVms", typing.Dict[builtins.str, typing.Any]]] = None,
        vpn_gateway: typing.Optional[typing.Union["CloudAzureIntegrationsVpnGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations newrelic_cloud_azure_integrations} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param linked_account_id: The ID of the linked Azure account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#linked_account_id CloudAzureIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#account_id CloudAzureIntegrations#account_id}
        :param api_management: api_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#api_management CloudAzureIntegrations#api_management}
        :param app_gateway: app_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#app_gateway CloudAzureIntegrations#app_gateway}
        :param app_service: app_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#app_service CloudAzureIntegrations#app_service}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#containers CloudAzureIntegrations#containers}
        :param cosmos_db: cosmos_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#cosmos_db CloudAzureIntegrations#cosmos_db}
        :param cost_management: cost_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#cost_management CloudAzureIntegrations#cost_management}
        :param data_factory: data_factory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#data_factory CloudAzureIntegrations#data_factory}
        :param event_hub: event_hub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#event_hub CloudAzureIntegrations#event_hub}
        :param express_route: express_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#express_route CloudAzureIntegrations#express_route}
        :param firewalls: firewalls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#firewalls CloudAzureIntegrations#firewalls}
        :param front_door: front_door block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#front_door CloudAzureIntegrations#front_door}
        :param functions: functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#functions CloudAzureIntegrations#functions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#id CloudAzureIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_vault: key_vault block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#key_vault CloudAzureIntegrations#key_vault}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#load_balancer CloudAzureIntegrations#load_balancer}
        :param logic_apps: logic_apps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#logic_apps CloudAzureIntegrations#logic_apps}
        :param machine_learning: machine_learning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#machine_learning CloudAzureIntegrations#machine_learning}
        :param maria_db: maria_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#maria_db CloudAzureIntegrations#maria_db}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#monitor CloudAzureIntegrations#monitor}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#mysql CloudAzureIntegrations#mysql}
        :param mysql_flexible: mysql_flexible block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#mysql_flexible CloudAzureIntegrations#mysql_flexible}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#postgresql CloudAzureIntegrations#postgresql}
        :param postgresql_flexible: postgresql_flexible block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#postgresql_flexible CloudAzureIntegrations#postgresql_flexible}
        :param power_bi_dedicated: power_bi_dedicated block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#power_bi_dedicated CloudAzureIntegrations#power_bi_dedicated}
        :param redis_cache: redis_cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#redis_cache CloudAzureIntegrations#redis_cache}
        :param service_bus: service_bus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#service_bus CloudAzureIntegrations#service_bus}
        :param sql: sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#sql CloudAzureIntegrations#sql}
        :param sql_managed: sql_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#sql_managed CloudAzureIntegrations#sql_managed}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#storage CloudAzureIntegrations#storage}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#virtual_machine CloudAzureIntegrations#virtual_machine}
        :param virtual_networks: virtual_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#virtual_networks CloudAzureIntegrations#virtual_networks}
        :param vms: vms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#vms CloudAzureIntegrations#vms}
        :param vpn_gateway: vpn_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#vpn_gateway CloudAzureIntegrations#vpn_gateway}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d141dd03a0dfe6b24f19b959a1c00338ad703fb54e474e9622232db4980b760c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudAzureIntegrationsConfig(
            linked_account_id=linked_account_id,
            account_id=account_id,
            api_management=api_management,
            app_gateway=app_gateway,
            app_service=app_service,
            containers=containers,
            cosmos_db=cosmos_db,
            cost_management=cost_management,
            data_factory=data_factory,
            event_hub=event_hub,
            express_route=express_route,
            firewalls=firewalls,
            front_door=front_door,
            functions=functions,
            id=id,
            key_vault=key_vault,
            load_balancer=load_balancer,
            logic_apps=logic_apps,
            machine_learning=machine_learning,
            maria_db=maria_db,
            monitor=monitor,
            mysql=mysql,
            mysql_flexible=mysql_flexible,
            postgresql=postgresql,
            postgresql_flexible=postgresql_flexible,
            power_bi_dedicated=power_bi_dedicated,
            redis_cache=redis_cache,
            service_bus=service_bus,
            sql=sql,
            sql_managed=sql_managed,
            storage=storage,
            virtual_machine=virtual_machine,
            virtual_networks=virtual_networks,
            vms=vms,
            vpn_gateway=vpn_gateway,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a CloudAzureIntegrations resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudAzureIntegrations to import.
        :param import_from_id: The id of the existing CloudAzureIntegrations that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudAzureIntegrations to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7363e4ba7335e906677b75e6df37ae4c2c0d53a616b0176898076a81d3f764)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApiManagement")
    def put_api_management(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsApiManagement(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putApiManagement", [value]))

    @jsii.member(jsii_name="putAppGateway")
    def put_app_gateway(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsAppGateway(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putAppGateway", [value]))

    @jsii.member(jsii_name="putAppService")
    def put_app_service(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsAppService(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putAppService", [value]))

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsContainers(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putCosmosDb")
    def put_cosmos_db(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsCosmosDb(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putCosmosDb", [value]))

    @jsii.member(jsii_name="putCostManagement")
    def put_cost_management(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param tag_keys: Specify if additional cost data per tag should be collected. This field is case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#tag_keys CloudAzureIntegrations#tag_keys}
        '''
        value = CloudAzureIntegrationsCostManagement(
            metrics_polling_interval=metrics_polling_interval, tag_keys=tag_keys
        )

        return typing.cast(None, jsii.invoke(self, "putCostManagement", [value]))

    @jsii.member(jsii_name="putDataFactory")
    def put_data_factory(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsDataFactory(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putDataFactory", [value]))

    @jsii.member(jsii_name="putEventHub")
    def put_event_hub(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsEventHub(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putEventHub", [value]))

    @jsii.member(jsii_name="putExpressRoute")
    def put_express_route(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsExpressRoute(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putExpressRoute", [value]))

    @jsii.member(jsii_name="putFirewalls")
    def put_firewalls(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsFirewalls(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putFirewalls", [value]))

    @jsii.member(jsii_name="putFrontDoor")
    def put_front_door(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsFrontDoor(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putFrontDoor", [value]))

    @jsii.member(jsii_name="putFunctions")
    def put_functions(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsFunctions(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putFunctions", [value]))

    @jsii.member(jsii_name="putKeyVault")
    def put_key_vault(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsKeyVault(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVault", [value]))

    @jsii.member(jsii_name="putLoadBalancer")
    def put_load_balancer(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsLoadBalancer(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancer", [value]))

    @jsii.member(jsii_name="putLogicApps")
    def put_logic_apps(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsLogicApps(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putLogicApps", [value]))

    @jsii.member(jsii_name="putMachineLearning")
    def put_machine_learning(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsMachineLearning(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putMachineLearning", [value]))

    @jsii.member(jsii_name="putMariaDb")
    def put_maria_db(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsMariaDb(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putMariaDb", [value]))

    @jsii.member(jsii_name="putMonitor")
    def put_monitor(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: A flag that specifies if the integration is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#enabled CloudAzureIntegrations#enabled}
        :param exclude_tags: Specify resource tags in 'key:value' form to be excluded from monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#exclude_tags CloudAzureIntegrations#exclude_tags}
        :param include_tags: Specify resource tags in 'key:value' form to be monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#include_tags CloudAzureIntegrations#include_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        :param resource_types: Specify each Azure resource type that needs to be monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_types CloudAzureIntegrations#resource_types}
        '''
        value = CloudAzureIntegrationsMonitor(
            enabled=enabled,
            exclude_tags=exclude_tags,
            include_tags=include_tags,
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
            resource_types=resource_types,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitor", [value]))

    @jsii.member(jsii_name="putMysql")
    def put_mysql(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsMysql(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putMysql", [value]))

    @jsii.member(jsii_name="putMysqlFlexible")
    def put_mysql_flexible(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsMysqlFlexible(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putMysqlFlexible", [value]))

    @jsii.member(jsii_name="putPostgresql")
    def put_postgresql(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsPostgresql(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresql", [value]))

    @jsii.member(jsii_name="putPostgresqlFlexible")
    def put_postgresql_flexible(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsPostgresqlFlexible(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresqlFlexible", [value]))

    @jsii.member(jsii_name="putPowerBiDedicated")
    def put_power_bi_dedicated(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsPowerBiDedicated(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putPowerBiDedicated", [value]))

    @jsii.member(jsii_name="putRedisCache")
    def put_redis_cache(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsRedisCache(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putRedisCache", [value]))

    @jsii.member(jsii_name="putServiceBus")
    def put_service_bus(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsServiceBus(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putServiceBus", [value]))

    @jsii.member(jsii_name="putSql")
    def put_sql(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsSql(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putSql", [value]))

    @jsii.member(jsii_name="putSqlManaged")
    def put_sql_managed(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsSqlManaged(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putSqlManaged", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsStorage(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putStorage", [value]))

    @jsii.member(jsii_name="putVirtualMachine")
    def put_virtual_machine(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsVirtualMachine(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachine", [value]))

    @jsii.member(jsii_name="putVirtualNetworks")
    def put_virtual_networks(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsVirtualNetworks(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualNetworks", [value]))

    @jsii.member(jsii_name="putVms")
    def put_vms(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsVms(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putVms", [value]))

    @jsii.member(jsii_name="putVpnGateway")
    def put_vpn_gateway(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        value = CloudAzureIntegrationsVpnGateway(
            metrics_polling_interval=metrics_polling_interval,
            resource_groups=resource_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putVpnGateway", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetApiManagement")
    def reset_api_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiManagement", []))

    @jsii.member(jsii_name="resetAppGateway")
    def reset_app_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppGateway", []))

    @jsii.member(jsii_name="resetAppService")
    def reset_app_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppService", []))

    @jsii.member(jsii_name="resetContainers")
    def reset_containers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainers", []))

    @jsii.member(jsii_name="resetCosmosDb")
    def reset_cosmos_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCosmosDb", []))

    @jsii.member(jsii_name="resetCostManagement")
    def reset_cost_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostManagement", []))

    @jsii.member(jsii_name="resetDataFactory")
    def reset_data_factory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFactory", []))

    @jsii.member(jsii_name="resetEventHub")
    def reset_event_hub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHub", []))

    @jsii.member(jsii_name="resetExpressRoute")
    def reset_express_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressRoute", []))

    @jsii.member(jsii_name="resetFirewalls")
    def reset_firewalls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewalls", []))

    @jsii.member(jsii_name="resetFrontDoor")
    def reset_front_door(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontDoor", []))

    @jsii.member(jsii_name="resetFunctions")
    def reset_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyVault")
    def reset_key_vault(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVault", []))

    @jsii.member(jsii_name="resetLoadBalancer")
    def reset_load_balancer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancer", []))

    @jsii.member(jsii_name="resetLogicApps")
    def reset_logic_apps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicApps", []))

    @jsii.member(jsii_name="resetMachineLearning")
    def reset_machine_learning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineLearning", []))

    @jsii.member(jsii_name="resetMariaDb")
    def reset_maria_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMariaDb", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetMysql")
    def reset_mysql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysql", []))

    @jsii.member(jsii_name="resetMysqlFlexible")
    def reset_mysql_flexible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlFlexible", []))

    @jsii.member(jsii_name="resetPostgresql")
    def reset_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresql", []))

    @jsii.member(jsii_name="resetPostgresqlFlexible")
    def reset_postgresql_flexible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlFlexible", []))

    @jsii.member(jsii_name="resetPowerBiDedicated")
    def reset_power_bi_dedicated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowerBiDedicated", []))

    @jsii.member(jsii_name="resetRedisCache")
    def reset_redis_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisCache", []))

    @jsii.member(jsii_name="resetServiceBus")
    def reset_service_bus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceBus", []))

    @jsii.member(jsii_name="resetSql")
    def reset_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSql", []))

    @jsii.member(jsii_name="resetSqlManaged")
    def reset_sql_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlManaged", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetVirtualMachine")
    def reset_virtual_machine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachine", []))

    @jsii.member(jsii_name="resetVirtualNetworks")
    def reset_virtual_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworks", []))

    @jsii.member(jsii_name="resetVms")
    def reset_vms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVms", []))

    @jsii.member(jsii_name="resetVpnGateway")
    def reset_vpn_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpnGateway", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="apiManagement")
    def api_management(self) -> "CloudAzureIntegrationsApiManagementOutputReference":
        return typing.cast("CloudAzureIntegrationsApiManagementOutputReference", jsii.get(self, "apiManagement"))

    @builtins.property
    @jsii.member(jsii_name="appGateway")
    def app_gateway(self) -> "CloudAzureIntegrationsAppGatewayOutputReference":
        return typing.cast("CloudAzureIntegrationsAppGatewayOutputReference", jsii.get(self, "appGateway"))

    @builtins.property
    @jsii.member(jsii_name="appService")
    def app_service(self) -> "CloudAzureIntegrationsAppServiceOutputReference":
        return typing.cast("CloudAzureIntegrationsAppServiceOutputReference", jsii.get(self, "appService"))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> "CloudAzureIntegrationsContainersOutputReference":
        return typing.cast("CloudAzureIntegrationsContainersOutputReference", jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="cosmosDb")
    def cosmos_db(self) -> "CloudAzureIntegrationsCosmosDbOutputReference":
        return typing.cast("CloudAzureIntegrationsCosmosDbOutputReference", jsii.get(self, "cosmosDb"))

    @builtins.property
    @jsii.member(jsii_name="costManagement")
    def cost_management(self) -> "CloudAzureIntegrationsCostManagementOutputReference":
        return typing.cast("CloudAzureIntegrationsCostManagementOutputReference", jsii.get(self, "costManagement"))

    @builtins.property
    @jsii.member(jsii_name="dataFactory")
    def data_factory(self) -> "CloudAzureIntegrationsDataFactoryOutputReference":
        return typing.cast("CloudAzureIntegrationsDataFactoryOutputReference", jsii.get(self, "dataFactory"))

    @builtins.property
    @jsii.member(jsii_name="eventHub")
    def event_hub(self) -> "CloudAzureIntegrationsEventHubOutputReference":
        return typing.cast("CloudAzureIntegrationsEventHubOutputReference", jsii.get(self, "eventHub"))

    @builtins.property
    @jsii.member(jsii_name="expressRoute")
    def express_route(self) -> "CloudAzureIntegrationsExpressRouteOutputReference":
        return typing.cast("CloudAzureIntegrationsExpressRouteOutputReference", jsii.get(self, "expressRoute"))

    @builtins.property
    @jsii.member(jsii_name="firewalls")
    def firewalls(self) -> "CloudAzureIntegrationsFirewallsOutputReference":
        return typing.cast("CloudAzureIntegrationsFirewallsOutputReference", jsii.get(self, "firewalls"))

    @builtins.property
    @jsii.member(jsii_name="frontDoor")
    def front_door(self) -> "CloudAzureIntegrationsFrontDoorOutputReference":
        return typing.cast("CloudAzureIntegrationsFrontDoorOutputReference", jsii.get(self, "frontDoor"))

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(self) -> "CloudAzureIntegrationsFunctionsOutputReference":
        return typing.cast("CloudAzureIntegrationsFunctionsOutputReference", jsii.get(self, "functions"))

    @builtins.property
    @jsii.member(jsii_name="keyVault")
    def key_vault(self) -> "CloudAzureIntegrationsKeyVaultOutputReference":
        return typing.cast("CloudAzureIntegrationsKeyVaultOutputReference", jsii.get(self, "keyVault"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "CloudAzureIntegrationsLoadBalancerOutputReference":
        return typing.cast("CloudAzureIntegrationsLoadBalancerOutputReference", jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="logicApps")
    def logic_apps(self) -> "CloudAzureIntegrationsLogicAppsOutputReference":
        return typing.cast("CloudAzureIntegrationsLogicAppsOutputReference", jsii.get(self, "logicApps"))

    @builtins.property
    @jsii.member(jsii_name="machineLearning")
    def machine_learning(
        self,
    ) -> "CloudAzureIntegrationsMachineLearningOutputReference":
        return typing.cast("CloudAzureIntegrationsMachineLearningOutputReference", jsii.get(self, "machineLearning"))

    @builtins.property
    @jsii.member(jsii_name="mariaDb")
    def maria_db(self) -> "CloudAzureIntegrationsMariaDbOutputReference":
        return typing.cast("CloudAzureIntegrationsMariaDbOutputReference", jsii.get(self, "mariaDb"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> "CloudAzureIntegrationsMonitorOutputReference":
        return typing.cast("CloudAzureIntegrationsMonitorOutputReference", jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="mysql")
    def mysql(self) -> "CloudAzureIntegrationsMysqlOutputReference":
        return typing.cast("CloudAzureIntegrationsMysqlOutputReference", jsii.get(self, "mysql"))

    @builtins.property
    @jsii.member(jsii_name="mysqlFlexible")
    def mysql_flexible(self) -> "CloudAzureIntegrationsMysqlFlexibleOutputReference":
        return typing.cast("CloudAzureIntegrationsMysqlFlexibleOutputReference", jsii.get(self, "mysqlFlexible"))

    @builtins.property
    @jsii.member(jsii_name="postgresql")
    def postgresql(self) -> "CloudAzureIntegrationsPostgresqlOutputReference":
        return typing.cast("CloudAzureIntegrationsPostgresqlOutputReference", jsii.get(self, "postgresql"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlFlexible")
    def postgresql_flexible(
        self,
    ) -> "CloudAzureIntegrationsPostgresqlFlexibleOutputReference":
        return typing.cast("CloudAzureIntegrationsPostgresqlFlexibleOutputReference", jsii.get(self, "postgresqlFlexible"))

    @builtins.property
    @jsii.member(jsii_name="powerBiDedicated")
    def power_bi_dedicated(
        self,
    ) -> "CloudAzureIntegrationsPowerBiDedicatedOutputReference":
        return typing.cast("CloudAzureIntegrationsPowerBiDedicatedOutputReference", jsii.get(self, "powerBiDedicated"))

    @builtins.property
    @jsii.member(jsii_name="redisCache")
    def redis_cache(self) -> "CloudAzureIntegrationsRedisCacheOutputReference":
        return typing.cast("CloudAzureIntegrationsRedisCacheOutputReference", jsii.get(self, "redisCache"))

    @builtins.property
    @jsii.member(jsii_name="serviceBus")
    def service_bus(self) -> "CloudAzureIntegrationsServiceBusOutputReference":
        return typing.cast("CloudAzureIntegrationsServiceBusOutputReference", jsii.get(self, "serviceBus"))

    @builtins.property
    @jsii.member(jsii_name="sql")
    def sql(self) -> "CloudAzureIntegrationsSqlOutputReference":
        return typing.cast("CloudAzureIntegrationsSqlOutputReference", jsii.get(self, "sql"))

    @builtins.property
    @jsii.member(jsii_name="sqlManaged")
    def sql_managed(self) -> "CloudAzureIntegrationsSqlManagedOutputReference":
        return typing.cast("CloudAzureIntegrationsSqlManagedOutputReference", jsii.get(self, "sqlManaged"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "CloudAzureIntegrationsStorageOutputReference":
        return typing.cast("CloudAzureIntegrationsStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachine")
    def virtual_machine(self) -> "CloudAzureIntegrationsVirtualMachineOutputReference":
        return typing.cast("CloudAzureIntegrationsVirtualMachineOutputReference", jsii.get(self, "virtualMachine"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworks")
    def virtual_networks(
        self,
    ) -> "CloudAzureIntegrationsVirtualNetworksOutputReference":
        return typing.cast("CloudAzureIntegrationsVirtualNetworksOutputReference", jsii.get(self, "virtualNetworks"))

    @builtins.property
    @jsii.member(jsii_name="vms")
    def vms(self) -> "CloudAzureIntegrationsVmsOutputReference":
        return typing.cast("CloudAzureIntegrationsVmsOutputReference", jsii.get(self, "vms"))

    @builtins.property
    @jsii.member(jsii_name="vpnGateway")
    def vpn_gateway(self) -> "CloudAzureIntegrationsVpnGatewayOutputReference":
        return typing.cast("CloudAzureIntegrationsVpnGatewayOutputReference", jsii.get(self, "vpnGateway"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementInput")
    def api_management_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsApiManagement"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsApiManagement"], jsii.get(self, "apiManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="appGatewayInput")
    def app_gateway_input(self) -> typing.Optional["CloudAzureIntegrationsAppGateway"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsAppGateway"], jsii.get(self, "appGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="appServiceInput")
    def app_service_input(self) -> typing.Optional["CloudAzureIntegrationsAppService"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsAppService"], jsii.get(self, "appServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(self) -> typing.Optional["CloudAzureIntegrationsContainers"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsContainers"], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosDbInput")
    def cosmos_db_input(self) -> typing.Optional["CloudAzureIntegrationsCosmosDb"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsCosmosDb"], jsii.get(self, "cosmosDbInput"))

    @builtins.property
    @jsii.member(jsii_name="costManagementInput")
    def cost_management_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsCostManagement"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsCostManagement"], jsii.get(self, "costManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryInput")
    def data_factory_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsDataFactory"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsDataFactory"], jsii.get(self, "dataFactoryInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubInput")
    def event_hub_input(self) -> typing.Optional["CloudAzureIntegrationsEventHub"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsEventHub"], jsii.get(self, "eventHubInput"))

    @builtins.property
    @jsii.member(jsii_name="expressRouteInput")
    def express_route_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsExpressRoute"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsExpressRoute"], jsii.get(self, "expressRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallsInput")
    def firewalls_input(self) -> typing.Optional["CloudAzureIntegrationsFirewalls"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsFirewalls"], jsii.get(self, "firewallsInput"))

    @builtins.property
    @jsii.member(jsii_name="frontDoorInput")
    def front_door_input(self) -> typing.Optional["CloudAzureIntegrationsFrontDoor"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsFrontDoor"], jsii.get(self, "frontDoorInput"))

    @builtins.property
    @jsii.member(jsii_name="functionsInput")
    def functions_input(self) -> typing.Optional["CloudAzureIntegrationsFunctions"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsFunctions"], jsii.get(self, "functionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultInput")
    def key_vault_input(self) -> typing.Optional["CloudAzureIntegrationsKeyVault"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsKeyVault"], jsii.get(self, "keyVaultInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedAccountIdInput")
    def linked_account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "linkedAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInput")
    def load_balancer_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsLoadBalancer"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsLoadBalancer"], jsii.get(self, "loadBalancerInput"))

    @builtins.property
    @jsii.member(jsii_name="logicAppsInput")
    def logic_apps_input(self) -> typing.Optional["CloudAzureIntegrationsLogicApps"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsLogicApps"], jsii.get(self, "logicAppsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningInput")
    def machine_learning_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsMachineLearning"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsMachineLearning"], jsii.get(self, "machineLearningInput"))

    @builtins.property
    @jsii.member(jsii_name="mariaDbInput")
    def maria_db_input(self) -> typing.Optional["CloudAzureIntegrationsMariaDb"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsMariaDb"], jsii.get(self, "mariaDbInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional["CloudAzureIntegrationsMonitor"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsMonitor"], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlFlexibleInput")
    def mysql_flexible_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsMysqlFlexible"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsMysqlFlexible"], jsii.get(self, "mysqlFlexibleInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlInput")
    def mysql_input(self) -> typing.Optional["CloudAzureIntegrationsMysql"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsMysql"], jsii.get(self, "mysqlInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlFlexibleInput")
    def postgresql_flexible_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsPostgresqlFlexible"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsPostgresqlFlexible"], jsii.get(self, "postgresqlFlexibleInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlInput")
    def postgresql_input(self) -> typing.Optional["CloudAzureIntegrationsPostgresql"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsPostgresql"], jsii.get(self, "postgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="powerBiDedicatedInput")
    def power_bi_dedicated_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsPowerBiDedicated"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsPowerBiDedicated"], jsii.get(self, "powerBiDedicatedInput"))

    @builtins.property
    @jsii.member(jsii_name="redisCacheInput")
    def redis_cache_input(self) -> typing.Optional["CloudAzureIntegrationsRedisCache"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsRedisCache"], jsii.get(self, "redisCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceBusInput")
    def service_bus_input(self) -> typing.Optional["CloudAzureIntegrationsServiceBus"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsServiceBus"], jsii.get(self, "serviceBusInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlInput")
    def sql_input(self) -> typing.Optional["CloudAzureIntegrationsSql"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsSql"], jsii.get(self, "sqlInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlManagedInput")
    def sql_managed_input(self) -> typing.Optional["CloudAzureIntegrationsSqlManaged"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsSqlManaged"], jsii.get(self, "sqlManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["CloudAzureIntegrationsStorage"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineInput")
    def virtual_machine_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsVirtualMachine"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsVirtualMachine"], jsii.get(self, "virtualMachineInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworksInput")
    def virtual_networks_input(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsVirtualNetworks"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsVirtualNetworks"], jsii.get(self, "virtualNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="vmsInput")
    def vms_input(self) -> typing.Optional["CloudAzureIntegrationsVms"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsVms"], jsii.get(self, "vmsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnGatewayInput")
    def vpn_gateway_input(self) -> typing.Optional["CloudAzureIntegrationsVpnGateway"]:
        return typing.cast(typing.Optional["CloudAzureIntegrationsVpnGateway"], jsii.get(self, "vpnGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a01589fa7f1711ba7b77ce2e45c34b154f9996989650016575ba5e6e8891aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92d8154df06c1054340548e1a826b72e671227dbf466a4c01d94dfda651deea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedAccountId")
    def linked_account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "linkedAccountId"))

    @linked_account_id.setter
    def linked_account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3677b76635f299e5c327982d4034ac772fd9f98393dc3b75da3549c77455f5ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsApiManagement",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsApiManagement:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99666a8e297dc41bb6603a2f5b5fe5400a30771fc2235188022acb6da849160f)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsApiManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsApiManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsApiManagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c218a51492d01d521d024c7853d89ded927bfdd2ed432e882e776fd471ddc5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf001879bb202f47515ab10368e68a547ac6c7f205cdefa1686d12d38d1fa44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa9518f394d0f8eb47549e8339c0dc1c005d11076078de666aac2d72d685a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsApiManagement]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsApiManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsApiManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f5436078455d6808b08219e2120fc63dd0c647c7fd31b44c24669152c8039e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsAppGateway",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsAppGateway:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58752629d821f42bd699e3c4febf7814452e151e424c772413fc250db6c9e370)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsAppGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsAppGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsAppGatewayOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59159e36e5d3f0e946fff901575e440c5e899cf1f57dc2f8e7709aacbaf3927c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6130f41ac9dac30accaed89850f07e2838fc9491930c63d577a432feb74ddcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5ba992ddc59fef1dcb10af5747c83d76cf31cc448fceee4813157276f139f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsAppGateway]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsAppGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsAppGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e64389b7e81db6f6f120b1b7d21477c2dafc4463de4737282ccd79c0ba5ec6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsAppService",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsAppService:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322510f410884ff89e9453cc12c053370754a94bc464aafe26da8cc05bd879f9)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsAppService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsAppServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsAppServiceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffde5f2b021cbd50d130a76a4a5a142874fa54cd3b00243ec97bb7207afefe84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e3a6e8ecc1206ddf66120695294ae44eec9b107db061da67f7618c5ee08d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70ebef4787f84178eb88a3aa2c6a0ce11372d3646dbb51e22a06ed1dfe8e047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsAppService]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsAppService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsAppService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4084ee20c4b376be429b8b9046d4f221f0b2d6cfb472d18f0774988011d9a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "linked_account_id": "linkedAccountId",
        "account_id": "accountId",
        "api_management": "apiManagement",
        "app_gateway": "appGateway",
        "app_service": "appService",
        "containers": "containers",
        "cosmos_db": "cosmosDb",
        "cost_management": "costManagement",
        "data_factory": "dataFactory",
        "event_hub": "eventHub",
        "express_route": "expressRoute",
        "firewalls": "firewalls",
        "front_door": "frontDoor",
        "functions": "functions",
        "id": "id",
        "key_vault": "keyVault",
        "load_balancer": "loadBalancer",
        "logic_apps": "logicApps",
        "machine_learning": "machineLearning",
        "maria_db": "mariaDb",
        "monitor": "monitor",
        "mysql": "mysql",
        "mysql_flexible": "mysqlFlexible",
        "postgresql": "postgresql",
        "postgresql_flexible": "postgresqlFlexible",
        "power_bi_dedicated": "powerBiDedicated",
        "redis_cache": "redisCache",
        "service_bus": "serviceBus",
        "sql": "sql",
        "sql_managed": "sqlManaged",
        "storage": "storage",
        "virtual_machine": "virtualMachine",
        "virtual_networks": "virtualNetworks",
        "vms": "vms",
        "vpn_gateway": "vpnGateway",
    },
)
class CloudAzureIntegrationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        api_management: typing.Optional[typing.Union[CloudAzureIntegrationsApiManagement, typing.Dict[builtins.str, typing.Any]]] = None,
        app_gateway: typing.Optional[typing.Union[CloudAzureIntegrationsAppGateway, typing.Dict[builtins.str, typing.Any]]] = None,
        app_service: typing.Optional[typing.Union[CloudAzureIntegrationsAppService, typing.Dict[builtins.str, typing.Any]]] = None,
        containers: typing.Optional[typing.Union["CloudAzureIntegrationsContainers", typing.Dict[builtins.str, typing.Any]]] = None,
        cosmos_db: typing.Optional[typing.Union["CloudAzureIntegrationsCosmosDb", typing.Dict[builtins.str, typing.Any]]] = None,
        cost_management: typing.Optional[typing.Union["CloudAzureIntegrationsCostManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        data_factory: typing.Optional[typing.Union["CloudAzureIntegrationsDataFactory", typing.Dict[builtins.str, typing.Any]]] = None,
        event_hub: typing.Optional[typing.Union["CloudAzureIntegrationsEventHub", typing.Dict[builtins.str, typing.Any]]] = None,
        express_route: typing.Optional[typing.Union["CloudAzureIntegrationsExpressRoute", typing.Dict[builtins.str, typing.Any]]] = None,
        firewalls: typing.Optional[typing.Union["CloudAzureIntegrationsFirewalls", typing.Dict[builtins.str, typing.Any]]] = None,
        front_door: typing.Optional[typing.Union["CloudAzureIntegrationsFrontDoor", typing.Dict[builtins.str, typing.Any]]] = None,
        functions: typing.Optional[typing.Union["CloudAzureIntegrationsFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key_vault: typing.Optional[typing.Union["CloudAzureIntegrationsKeyVault", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer: typing.Optional[typing.Union["CloudAzureIntegrationsLoadBalancer", typing.Dict[builtins.str, typing.Any]]] = None,
        logic_apps: typing.Optional[typing.Union["CloudAzureIntegrationsLogicApps", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_learning: typing.Optional[typing.Union["CloudAzureIntegrationsMachineLearning", typing.Dict[builtins.str, typing.Any]]] = None,
        maria_db: typing.Optional[typing.Union["CloudAzureIntegrationsMariaDb", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["CloudAzureIntegrationsMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql: typing.Optional[typing.Union["CloudAzureIntegrationsMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql_flexible: typing.Optional[typing.Union["CloudAzureIntegrationsMysqlFlexible", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["CloudAzureIntegrationsPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_flexible: typing.Optional[typing.Union["CloudAzureIntegrationsPostgresqlFlexible", typing.Dict[builtins.str, typing.Any]]] = None,
        power_bi_dedicated: typing.Optional[typing.Union["CloudAzureIntegrationsPowerBiDedicated", typing.Dict[builtins.str, typing.Any]]] = None,
        redis_cache: typing.Optional[typing.Union["CloudAzureIntegrationsRedisCache", typing.Dict[builtins.str, typing.Any]]] = None,
        service_bus: typing.Optional[typing.Union["CloudAzureIntegrationsServiceBus", typing.Dict[builtins.str, typing.Any]]] = None,
        sql: typing.Optional[typing.Union["CloudAzureIntegrationsSql", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_managed: typing.Optional[typing.Union["CloudAzureIntegrationsSqlManaged", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["CloudAzureIntegrationsStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machine: typing.Optional[typing.Union["CloudAzureIntegrationsVirtualMachine", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_networks: typing.Optional[typing.Union["CloudAzureIntegrationsVirtualNetworks", typing.Dict[builtins.str, typing.Any]]] = None,
        vms: typing.Optional[typing.Union["CloudAzureIntegrationsVms", typing.Dict[builtins.str, typing.Any]]] = None,
        vpn_gateway: typing.Optional[typing.Union["CloudAzureIntegrationsVpnGateway", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param linked_account_id: The ID of the linked Azure account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#linked_account_id CloudAzureIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#account_id CloudAzureIntegrations#account_id}
        :param api_management: api_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#api_management CloudAzureIntegrations#api_management}
        :param app_gateway: app_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#app_gateway CloudAzureIntegrations#app_gateway}
        :param app_service: app_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#app_service CloudAzureIntegrations#app_service}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#containers CloudAzureIntegrations#containers}
        :param cosmos_db: cosmos_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#cosmos_db CloudAzureIntegrations#cosmos_db}
        :param cost_management: cost_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#cost_management CloudAzureIntegrations#cost_management}
        :param data_factory: data_factory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#data_factory CloudAzureIntegrations#data_factory}
        :param event_hub: event_hub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#event_hub CloudAzureIntegrations#event_hub}
        :param express_route: express_route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#express_route CloudAzureIntegrations#express_route}
        :param firewalls: firewalls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#firewalls CloudAzureIntegrations#firewalls}
        :param front_door: front_door block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#front_door CloudAzureIntegrations#front_door}
        :param functions: functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#functions CloudAzureIntegrations#functions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#id CloudAzureIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_vault: key_vault block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#key_vault CloudAzureIntegrations#key_vault}
        :param load_balancer: load_balancer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#load_balancer CloudAzureIntegrations#load_balancer}
        :param logic_apps: logic_apps block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#logic_apps CloudAzureIntegrations#logic_apps}
        :param machine_learning: machine_learning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#machine_learning CloudAzureIntegrations#machine_learning}
        :param maria_db: maria_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#maria_db CloudAzureIntegrations#maria_db}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#monitor CloudAzureIntegrations#monitor}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#mysql CloudAzureIntegrations#mysql}
        :param mysql_flexible: mysql_flexible block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#mysql_flexible CloudAzureIntegrations#mysql_flexible}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#postgresql CloudAzureIntegrations#postgresql}
        :param postgresql_flexible: postgresql_flexible block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#postgresql_flexible CloudAzureIntegrations#postgresql_flexible}
        :param power_bi_dedicated: power_bi_dedicated block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#power_bi_dedicated CloudAzureIntegrations#power_bi_dedicated}
        :param redis_cache: redis_cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#redis_cache CloudAzureIntegrations#redis_cache}
        :param service_bus: service_bus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#service_bus CloudAzureIntegrations#service_bus}
        :param sql: sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#sql CloudAzureIntegrations#sql}
        :param sql_managed: sql_managed block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#sql_managed CloudAzureIntegrations#sql_managed}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#storage CloudAzureIntegrations#storage}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#virtual_machine CloudAzureIntegrations#virtual_machine}
        :param virtual_networks: virtual_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#virtual_networks CloudAzureIntegrations#virtual_networks}
        :param vms: vms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#vms CloudAzureIntegrations#vms}
        :param vpn_gateway: vpn_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#vpn_gateway CloudAzureIntegrations#vpn_gateway}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(api_management, dict):
            api_management = CloudAzureIntegrationsApiManagement(**api_management)
        if isinstance(app_gateway, dict):
            app_gateway = CloudAzureIntegrationsAppGateway(**app_gateway)
        if isinstance(app_service, dict):
            app_service = CloudAzureIntegrationsAppService(**app_service)
        if isinstance(containers, dict):
            containers = CloudAzureIntegrationsContainers(**containers)
        if isinstance(cosmos_db, dict):
            cosmos_db = CloudAzureIntegrationsCosmosDb(**cosmos_db)
        if isinstance(cost_management, dict):
            cost_management = CloudAzureIntegrationsCostManagement(**cost_management)
        if isinstance(data_factory, dict):
            data_factory = CloudAzureIntegrationsDataFactory(**data_factory)
        if isinstance(event_hub, dict):
            event_hub = CloudAzureIntegrationsEventHub(**event_hub)
        if isinstance(express_route, dict):
            express_route = CloudAzureIntegrationsExpressRoute(**express_route)
        if isinstance(firewalls, dict):
            firewalls = CloudAzureIntegrationsFirewalls(**firewalls)
        if isinstance(front_door, dict):
            front_door = CloudAzureIntegrationsFrontDoor(**front_door)
        if isinstance(functions, dict):
            functions = CloudAzureIntegrationsFunctions(**functions)
        if isinstance(key_vault, dict):
            key_vault = CloudAzureIntegrationsKeyVault(**key_vault)
        if isinstance(load_balancer, dict):
            load_balancer = CloudAzureIntegrationsLoadBalancer(**load_balancer)
        if isinstance(logic_apps, dict):
            logic_apps = CloudAzureIntegrationsLogicApps(**logic_apps)
        if isinstance(machine_learning, dict):
            machine_learning = CloudAzureIntegrationsMachineLearning(**machine_learning)
        if isinstance(maria_db, dict):
            maria_db = CloudAzureIntegrationsMariaDb(**maria_db)
        if isinstance(monitor, dict):
            monitor = CloudAzureIntegrationsMonitor(**monitor)
        if isinstance(mysql, dict):
            mysql = CloudAzureIntegrationsMysql(**mysql)
        if isinstance(mysql_flexible, dict):
            mysql_flexible = CloudAzureIntegrationsMysqlFlexible(**mysql_flexible)
        if isinstance(postgresql, dict):
            postgresql = CloudAzureIntegrationsPostgresql(**postgresql)
        if isinstance(postgresql_flexible, dict):
            postgresql_flexible = CloudAzureIntegrationsPostgresqlFlexible(**postgresql_flexible)
        if isinstance(power_bi_dedicated, dict):
            power_bi_dedicated = CloudAzureIntegrationsPowerBiDedicated(**power_bi_dedicated)
        if isinstance(redis_cache, dict):
            redis_cache = CloudAzureIntegrationsRedisCache(**redis_cache)
        if isinstance(service_bus, dict):
            service_bus = CloudAzureIntegrationsServiceBus(**service_bus)
        if isinstance(sql, dict):
            sql = CloudAzureIntegrationsSql(**sql)
        if isinstance(sql_managed, dict):
            sql_managed = CloudAzureIntegrationsSqlManaged(**sql_managed)
        if isinstance(storage, dict):
            storage = CloudAzureIntegrationsStorage(**storage)
        if isinstance(virtual_machine, dict):
            virtual_machine = CloudAzureIntegrationsVirtualMachine(**virtual_machine)
        if isinstance(virtual_networks, dict):
            virtual_networks = CloudAzureIntegrationsVirtualNetworks(**virtual_networks)
        if isinstance(vms, dict):
            vms = CloudAzureIntegrationsVms(**vms)
        if isinstance(vpn_gateway, dict):
            vpn_gateway = CloudAzureIntegrationsVpnGateway(**vpn_gateway)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b38caeaf90cdfca3b21c94277eb3f00ace750df95799e3cd0e0395662cab3e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument linked_account_id", value=linked_account_id, expected_type=type_hints["linked_account_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument api_management", value=api_management, expected_type=type_hints["api_management"])
            check_type(argname="argument app_gateway", value=app_gateway, expected_type=type_hints["app_gateway"])
            check_type(argname="argument app_service", value=app_service, expected_type=type_hints["app_service"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument cosmos_db", value=cosmos_db, expected_type=type_hints["cosmos_db"])
            check_type(argname="argument cost_management", value=cost_management, expected_type=type_hints["cost_management"])
            check_type(argname="argument data_factory", value=data_factory, expected_type=type_hints["data_factory"])
            check_type(argname="argument event_hub", value=event_hub, expected_type=type_hints["event_hub"])
            check_type(argname="argument express_route", value=express_route, expected_type=type_hints["express_route"])
            check_type(argname="argument firewalls", value=firewalls, expected_type=type_hints["firewalls"])
            check_type(argname="argument front_door", value=front_door, expected_type=type_hints["front_door"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_vault", value=key_vault, expected_type=type_hints["key_vault"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument logic_apps", value=logic_apps, expected_type=type_hints["logic_apps"])
            check_type(argname="argument machine_learning", value=machine_learning, expected_type=type_hints["machine_learning"])
            check_type(argname="argument maria_db", value=maria_db, expected_type=type_hints["maria_db"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument mysql", value=mysql, expected_type=type_hints["mysql"])
            check_type(argname="argument mysql_flexible", value=mysql_flexible, expected_type=type_hints["mysql_flexible"])
            check_type(argname="argument postgresql", value=postgresql, expected_type=type_hints["postgresql"])
            check_type(argname="argument postgresql_flexible", value=postgresql_flexible, expected_type=type_hints["postgresql_flexible"])
            check_type(argname="argument power_bi_dedicated", value=power_bi_dedicated, expected_type=type_hints["power_bi_dedicated"])
            check_type(argname="argument redis_cache", value=redis_cache, expected_type=type_hints["redis_cache"])
            check_type(argname="argument service_bus", value=service_bus, expected_type=type_hints["service_bus"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument sql_managed", value=sql_managed, expected_type=type_hints["sql_managed"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
            check_type(argname="argument virtual_networks", value=virtual_networks, expected_type=type_hints["virtual_networks"])
            check_type(argname="argument vms", value=vms, expected_type=type_hints["vms"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_account_id": linked_account_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if account_id is not None:
            self._values["account_id"] = account_id
        if api_management is not None:
            self._values["api_management"] = api_management
        if app_gateway is not None:
            self._values["app_gateway"] = app_gateway
        if app_service is not None:
            self._values["app_service"] = app_service
        if containers is not None:
            self._values["containers"] = containers
        if cosmos_db is not None:
            self._values["cosmos_db"] = cosmos_db
        if cost_management is not None:
            self._values["cost_management"] = cost_management
        if data_factory is not None:
            self._values["data_factory"] = data_factory
        if event_hub is not None:
            self._values["event_hub"] = event_hub
        if express_route is not None:
            self._values["express_route"] = express_route
        if firewalls is not None:
            self._values["firewalls"] = firewalls
        if front_door is not None:
            self._values["front_door"] = front_door
        if functions is not None:
            self._values["functions"] = functions
        if id is not None:
            self._values["id"] = id
        if key_vault is not None:
            self._values["key_vault"] = key_vault
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if logic_apps is not None:
            self._values["logic_apps"] = logic_apps
        if machine_learning is not None:
            self._values["machine_learning"] = machine_learning
        if maria_db is not None:
            self._values["maria_db"] = maria_db
        if monitor is not None:
            self._values["monitor"] = monitor
        if mysql is not None:
            self._values["mysql"] = mysql
        if mysql_flexible is not None:
            self._values["mysql_flexible"] = mysql_flexible
        if postgresql is not None:
            self._values["postgresql"] = postgresql
        if postgresql_flexible is not None:
            self._values["postgresql_flexible"] = postgresql_flexible
        if power_bi_dedicated is not None:
            self._values["power_bi_dedicated"] = power_bi_dedicated
        if redis_cache is not None:
            self._values["redis_cache"] = redis_cache
        if service_bus is not None:
            self._values["service_bus"] = service_bus
        if sql is not None:
            self._values["sql"] = sql
        if sql_managed is not None:
            self._values["sql_managed"] = sql_managed
        if storage is not None:
            self._values["storage"] = storage
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine
        if virtual_networks is not None:
            self._values["virtual_networks"] = virtual_networks
        if vms is not None:
            self._values["vms"] = vms
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def linked_account_id(self) -> jsii.Number:
        '''The ID of the linked Azure account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#linked_account_id CloudAzureIntegrations#linked_account_id}
        '''
        result = self._values.get("linked_account_id")
        assert result is not None, "Required property 'linked_account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#account_id CloudAzureIntegrations#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def api_management(self) -> typing.Optional[CloudAzureIntegrationsApiManagement]:
        '''api_management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#api_management CloudAzureIntegrations#api_management}
        '''
        result = self._values.get("api_management")
        return typing.cast(typing.Optional[CloudAzureIntegrationsApiManagement], result)

    @builtins.property
    def app_gateway(self) -> typing.Optional[CloudAzureIntegrationsAppGateway]:
        '''app_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#app_gateway CloudAzureIntegrations#app_gateway}
        '''
        result = self._values.get("app_gateway")
        return typing.cast(typing.Optional[CloudAzureIntegrationsAppGateway], result)

    @builtins.property
    def app_service(self) -> typing.Optional[CloudAzureIntegrationsAppService]:
        '''app_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#app_service CloudAzureIntegrations#app_service}
        '''
        result = self._values.get("app_service")
        return typing.cast(typing.Optional[CloudAzureIntegrationsAppService], result)

    @builtins.property
    def containers(self) -> typing.Optional["CloudAzureIntegrationsContainers"]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#containers CloudAzureIntegrations#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional["CloudAzureIntegrationsContainers"], result)

    @builtins.property
    def cosmos_db(self) -> typing.Optional["CloudAzureIntegrationsCosmosDb"]:
        '''cosmos_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#cosmos_db CloudAzureIntegrations#cosmos_db}
        '''
        result = self._values.get("cosmos_db")
        return typing.cast(typing.Optional["CloudAzureIntegrationsCosmosDb"], result)

    @builtins.property
    def cost_management(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsCostManagement"]:
        '''cost_management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#cost_management CloudAzureIntegrations#cost_management}
        '''
        result = self._values.get("cost_management")
        return typing.cast(typing.Optional["CloudAzureIntegrationsCostManagement"], result)

    @builtins.property
    def data_factory(self) -> typing.Optional["CloudAzureIntegrationsDataFactory"]:
        '''data_factory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#data_factory CloudAzureIntegrations#data_factory}
        '''
        result = self._values.get("data_factory")
        return typing.cast(typing.Optional["CloudAzureIntegrationsDataFactory"], result)

    @builtins.property
    def event_hub(self) -> typing.Optional["CloudAzureIntegrationsEventHub"]:
        '''event_hub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#event_hub CloudAzureIntegrations#event_hub}
        '''
        result = self._values.get("event_hub")
        return typing.cast(typing.Optional["CloudAzureIntegrationsEventHub"], result)

    @builtins.property
    def express_route(self) -> typing.Optional["CloudAzureIntegrationsExpressRoute"]:
        '''express_route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#express_route CloudAzureIntegrations#express_route}
        '''
        result = self._values.get("express_route")
        return typing.cast(typing.Optional["CloudAzureIntegrationsExpressRoute"], result)

    @builtins.property
    def firewalls(self) -> typing.Optional["CloudAzureIntegrationsFirewalls"]:
        '''firewalls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#firewalls CloudAzureIntegrations#firewalls}
        '''
        result = self._values.get("firewalls")
        return typing.cast(typing.Optional["CloudAzureIntegrationsFirewalls"], result)

    @builtins.property
    def front_door(self) -> typing.Optional["CloudAzureIntegrationsFrontDoor"]:
        '''front_door block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#front_door CloudAzureIntegrations#front_door}
        '''
        result = self._values.get("front_door")
        return typing.cast(typing.Optional["CloudAzureIntegrationsFrontDoor"], result)

    @builtins.property
    def functions(self) -> typing.Optional["CloudAzureIntegrationsFunctions"]:
        '''functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#functions CloudAzureIntegrations#functions}
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional["CloudAzureIntegrationsFunctions"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#id CloudAzureIntegrations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault(self) -> typing.Optional["CloudAzureIntegrationsKeyVault"]:
        '''key_vault block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#key_vault CloudAzureIntegrations#key_vault}
        '''
        result = self._values.get("key_vault")
        return typing.cast(typing.Optional["CloudAzureIntegrationsKeyVault"], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional["CloudAzureIntegrationsLoadBalancer"]:
        '''load_balancer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#load_balancer CloudAzureIntegrations#load_balancer}
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional["CloudAzureIntegrationsLoadBalancer"], result)

    @builtins.property
    def logic_apps(self) -> typing.Optional["CloudAzureIntegrationsLogicApps"]:
        '''logic_apps block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#logic_apps CloudAzureIntegrations#logic_apps}
        '''
        result = self._values.get("logic_apps")
        return typing.cast(typing.Optional["CloudAzureIntegrationsLogicApps"], result)

    @builtins.property
    def machine_learning(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsMachineLearning"]:
        '''machine_learning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#machine_learning CloudAzureIntegrations#machine_learning}
        '''
        result = self._values.get("machine_learning")
        return typing.cast(typing.Optional["CloudAzureIntegrationsMachineLearning"], result)

    @builtins.property
    def maria_db(self) -> typing.Optional["CloudAzureIntegrationsMariaDb"]:
        '''maria_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#maria_db CloudAzureIntegrations#maria_db}
        '''
        result = self._values.get("maria_db")
        return typing.cast(typing.Optional["CloudAzureIntegrationsMariaDb"], result)

    @builtins.property
    def monitor(self) -> typing.Optional["CloudAzureIntegrationsMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#monitor CloudAzureIntegrations#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["CloudAzureIntegrationsMonitor"], result)

    @builtins.property
    def mysql(self) -> typing.Optional["CloudAzureIntegrationsMysql"]:
        '''mysql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#mysql CloudAzureIntegrations#mysql}
        '''
        result = self._values.get("mysql")
        return typing.cast(typing.Optional["CloudAzureIntegrationsMysql"], result)

    @builtins.property
    def mysql_flexible(self) -> typing.Optional["CloudAzureIntegrationsMysqlFlexible"]:
        '''mysql_flexible block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#mysql_flexible CloudAzureIntegrations#mysql_flexible}
        '''
        result = self._values.get("mysql_flexible")
        return typing.cast(typing.Optional["CloudAzureIntegrationsMysqlFlexible"], result)

    @builtins.property
    def postgresql(self) -> typing.Optional["CloudAzureIntegrationsPostgresql"]:
        '''postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#postgresql CloudAzureIntegrations#postgresql}
        '''
        result = self._values.get("postgresql")
        return typing.cast(typing.Optional["CloudAzureIntegrationsPostgresql"], result)

    @builtins.property
    def postgresql_flexible(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsPostgresqlFlexible"]:
        '''postgresql_flexible block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#postgresql_flexible CloudAzureIntegrations#postgresql_flexible}
        '''
        result = self._values.get("postgresql_flexible")
        return typing.cast(typing.Optional["CloudAzureIntegrationsPostgresqlFlexible"], result)

    @builtins.property
    def power_bi_dedicated(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsPowerBiDedicated"]:
        '''power_bi_dedicated block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#power_bi_dedicated CloudAzureIntegrations#power_bi_dedicated}
        '''
        result = self._values.get("power_bi_dedicated")
        return typing.cast(typing.Optional["CloudAzureIntegrationsPowerBiDedicated"], result)

    @builtins.property
    def redis_cache(self) -> typing.Optional["CloudAzureIntegrationsRedisCache"]:
        '''redis_cache block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#redis_cache CloudAzureIntegrations#redis_cache}
        '''
        result = self._values.get("redis_cache")
        return typing.cast(typing.Optional["CloudAzureIntegrationsRedisCache"], result)

    @builtins.property
    def service_bus(self) -> typing.Optional["CloudAzureIntegrationsServiceBus"]:
        '''service_bus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#service_bus CloudAzureIntegrations#service_bus}
        '''
        result = self._values.get("service_bus")
        return typing.cast(typing.Optional["CloudAzureIntegrationsServiceBus"], result)

    @builtins.property
    def sql(self) -> typing.Optional["CloudAzureIntegrationsSql"]:
        '''sql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#sql CloudAzureIntegrations#sql}
        '''
        result = self._values.get("sql")
        return typing.cast(typing.Optional["CloudAzureIntegrationsSql"], result)

    @builtins.property
    def sql_managed(self) -> typing.Optional["CloudAzureIntegrationsSqlManaged"]:
        '''sql_managed block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#sql_managed CloudAzureIntegrations#sql_managed}
        '''
        result = self._values.get("sql_managed")
        return typing.cast(typing.Optional["CloudAzureIntegrationsSqlManaged"], result)

    @builtins.property
    def storage(self) -> typing.Optional["CloudAzureIntegrationsStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#storage CloudAzureIntegrations#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["CloudAzureIntegrationsStorage"], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsVirtualMachine"]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#virtual_machine CloudAzureIntegrations#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional["CloudAzureIntegrationsVirtualMachine"], result)

    @builtins.property
    def virtual_networks(
        self,
    ) -> typing.Optional["CloudAzureIntegrationsVirtualNetworks"]:
        '''virtual_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#virtual_networks CloudAzureIntegrations#virtual_networks}
        '''
        result = self._values.get("virtual_networks")
        return typing.cast(typing.Optional["CloudAzureIntegrationsVirtualNetworks"], result)

    @builtins.property
    def vms(self) -> typing.Optional["CloudAzureIntegrationsVms"]:
        '''vms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#vms CloudAzureIntegrations#vms}
        '''
        result = self._values.get("vms")
        return typing.cast(typing.Optional["CloudAzureIntegrationsVms"], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional["CloudAzureIntegrationsVpnGateway"]:
        '''vpn_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#vpn_gateway CloudAzureIntegrations#vpn_gateway}
        '''
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional["CloudAzureIntegrationsVpnGateway"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsContainers",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsContainers:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beea570aac5416ef4b0588ba1094fa843ddafa29d871e7ae2d8760d41d76e770)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsContainersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b018258b66965e46ddbe40c683334756dbd315194dee79d38e5359ab78898717)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04cd4b5c4cfc7038996defe5e24084c4fe2ec25804fbf632be89b14446de0d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec00a7f3963225e573d5706a078b45ee3537e7b784cb8783ff4f2e30142726e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsContainers]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsContainers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsContainers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3a92334d17f3346772803797d60a715efd9c4217697f7021940f0e88c4c51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsCosmosDb",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsCosmosDb:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017b6c6e9145dcd6313121c29f6f073b91d5cc44a2dcb92668b2a77466016b41)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsCosmosDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsCosmosDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsCosmosDbOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabd4a3f0557579dd9af0f242682e184bef3678f887e1a077cab532591786ade)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b62ec72558c598195ed5ddddd269983c7e0750fc40465e704638196bd972e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aafd5f8ee5613b19386a1d4e2ec8211fcee8efb0f9bc84109405efe188545dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsCosmosDb]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsCosmosDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsCosmosDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28eaee0a8125e0e9f0c0cf93571a4324af1b0ed6bd3067ada5a2e99fabcec4a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsCostManagement",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_keys": "tagKeys",
    },
)
class CloudAzureIntegrationsCostManagement:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param tag_keys: Specify if additional cost data per tag should be collected. This field is case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#tag_keys CloudAzureIntegrations#tag_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94973ebbd074b10355ecb4e5daead82ea85d379466493b44371a5e23b7bd87c9)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_keys", value=tag_keys, expected_type=type_hints["tag_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_keys is not None:
            self._values["tag_keys"] = tag_keys

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify if additional cost data per tag should be collected. This field is case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#tag_keys CloudAzureIntegrations#tag_keys}
        '''
        result = self._values.get("tag_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsCostManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsCostManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsCostManagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053808b312ee19fab790ff90b2f7f8c8bf098f7384c77a1431ad39664525f414)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKeys")
    def reset_tag_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKeys", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeysInput")
    def tag_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f9946776c1184cc66e2051d95a2f5cee50b92c2440c02e99c2e73244f7cd46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKeys")
    def tag_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagKeys"))

    @tag_keys.setter
    def tag_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c21edc45e864a08eaabf23d086501477e45329a54f073a8a87005abbc1cbd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsCostManagement]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsCostManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsCostManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8e52de5aed5b4df0d2dff4e8a68d351a9ca7ac7d7730dc09c62e841037a3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsDataFactory",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsDataFactory:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d69242da02a0948f8b2fabedeaac1e11a466b6181741f51339116d3d7271a6c)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsDataFactory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsDataFactoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsDataFactoryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca42ccfafcd02829c4b34a80e88c6c2dec0e03f84a72688ef32005da541167b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2485a4079ee01552dbe776e453078f23ed59a551680ab9b74c858e588d878e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564d3e114c7df63a688cc9ca66455efbdeed9f8b96c049a552a444f00c97ba31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsDataFactory]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsDataFactory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsDataFactory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6d59f627662fc848bbbc0519b8f0998e70039e6e630930e8806d4e6c2a3cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsEventHub",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsEventHub:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8920cb9e9dbab5bf850d23ef0f7d517f9c9ef0b84de326efffa398e2cf95c399)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsEventHub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsEventHubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsEventHubOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66d57e85d1b1c6c590448d4f874592918a4c6a7c3185dac57ceadc4d1503c8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095f150e873cb98e8dd0526d397bee466e26980093c6461f21486eb300452cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d35412e2dd6f7821d90c9ecba02a74555e5db3fa8cae3ac298885be24a47d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsEventHub]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsEventHub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsEventHub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193f0746e997b84c84759e758b91a287ed48ba6692168bd28c341ddcc6d2b381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsExpressRoute",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsExpressRoute:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d219373af51e4448040c8d3e22e35524427f8a8f4c87eb0c7eb6a7f8fc2186ab)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsExpressRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsExpressRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsExpressRouteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabaae8e8ed5c70b3862ffbb9d1a8d66b568c7bd6bab136ea5116c40edb5a119)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157616a3dbcdb25041203f01dc138c13b48310f4547c5fe104cd4925bdaa67c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026fe46f89da4979af8a4b5c318d5d0ce311df2860ad6a7f720edbaadbe6cd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsExpressRoute]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsExpressRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsExpressRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e58fd999fa45d0cfe9d29bc1b666d4864f3eefd12ee72a6d1d48e9b7fe6e255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsFirewalls",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsFirewalls:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e569b05e1e4b4e4639632bf69122e4f9e04fe148faef4f016f8b8dcc7266df)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsFirewalls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsFirewallsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsFirewallsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81aa83b2fce243d41303a26e7dc7b8fdef371da4dba6eb8a382654329302fa18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a7d50adb6a0bb062c60e982e36bb0f79a7daecba8ab7da39f220741b658f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a264863db378258c887da5de85e81b9c4bbcf56f1755cc2ec9650815b04d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsFirewalls]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsFirewalls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsFirewalls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0335630154f00c03bd986baa2880c91c53c21dd1d88c329a5e22a75d40faa6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsFrontDoor",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsFrontDoor:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10268924df74aa499e93912ceec70b0d72f95b80f05daa273f01d8c62a3dd24)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsFrontDoor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsFrontDoorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsFrontDoorOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac036f737c236c5cbc1835f968ba3f8a79c8585776be484b7887b5cdce5d832d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f935fea2866cbed83bb173c24923888545e3af33f30a525217abd346e740c81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32303773c210786f1f92ee01ee33ffd504920c19f8408811cfb56a8f2794e565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsFrontDoor]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsFrontDoor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsFrontDoor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae122d547ab6f77ec05bf8e3eac4ed47411463c2d3c01689dae7639fac0b5a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsFunctions:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf317ce796c198e2498d1ba072491cad3907ccdfd55ce44d26722aab5d5c2c2)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsFunctionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd6efc0a9f38831075cdaba74a9e8c1277d9dcf988cb2fe5b4e671ae095867b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7ede262c3f7a5f368996541236d40989e3443ead8a91b60db512dbae0cb5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cb6915b6144174c6ef435fdfa51d3795c37ab021805ca23d01cf34a532fb5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsFunctions]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsFunctions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsFunctions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed95979b2e3ebd5286795c7ef027db76d2880d8ea7dd8b29f40c553c24fb270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsKeyVault",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsKeyVault:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb08c3021ecbb836b1f0c55010013733664ac8a3c4921bb69eac078834a2f691)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsKeyVault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsKeyVaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsKeyVaultOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab83d2c8506b04d9ab81abdfa9ec23ebc4d793c0376b61a709dc477a29f1da85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8a356daa8b788df700051feb29ebf7af7826dc4153ee309d34f31839b007e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42ca401a9d2b6559397d75b02bb60e37f237a7730a577649b3b33c719f50781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsKeyVault]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsKeyVault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsKeyVault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27fb2ca292c190ef94662b59a27d7456c0939c0302af4d0e954031a9091ebf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsLoadBalancer",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsLoadBalancer:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03af203168a83126c7353b5fbb49784c2c678dc40bf95ebd7008899e9fa9af6b)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsLoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsLoadBalancerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsLoadBalancerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f95e38d0e67d9f70573dafedcf5dac57e1d2b6672e07bc3f150cf85d74c736)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7545b1e7f85be9e2200c83e488a3861859cae6e8ee7be169d49571d0e85ea429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88de7521b05a6deb662799c74fd9697c31ba63153ceac56ebf23c006ad6037a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsLoadBalancer]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsLoadBalancer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsLoadBalancer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fb56a2b925099fe3f9d3e1c40cd547ea32df73180728b5ecafb5747bb764df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsLogicApps",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsLogicApps:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bf425ee69410cecdc7dd61386a8cd21145c911ee4ed965ea1f914e4d02a682)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsLogicApps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsLogicAppsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsLogicAppsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4a79669719664559268f220384cffd21649a757c8798374710c7ea6d713d57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34a398cc24d3bf4cdda0771eb08ffcf8b3863f02c15ac289831a0d22fea259f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7580b89ee474b8f1571eed992f5537b4dc4f8a50fe734f0e04912f836930fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsLogicApps]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsLogicApps], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsLogicApps],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c043ccad04f353425dd04ea7fb77d5be25894b515d082fb7a2e1d46dc428a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMachineLearning",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsMachineLearning:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053136e2f18b07dcbf7a41de79e92d7dd95d6cb309e40dad6f7fc46562da195c)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsMachineLearning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsMachineLearningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMachineLearningOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5e6f6da23dc251ec895d299b03dbd738c00e829fe805a06ad6c231873148ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa1cbb3e6f900bbba14328274785bad6d1cafd007d9f2106183326e0e374b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa492ad19436cb03805682018add39b13a946813aed44dfba34fab2c2437f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsMachineLearning]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsMachineLearning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsMachineLearning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237badac773ea30d64ce2e0744f99838dc9bc64850824340b1cbcd8172ae6049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMariaDb",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsMariaDb:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e263082b32e1960e57849acc57c6512bd3f644e4c410978ea7889e2a27d04f)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsMariaDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsMariaDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMariaDbOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8fd3de2f406df0dda57e45af4baab3a672297f85cadd2d4de94fc44c77e202)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ece926968833822a2da198df5ae766096f9f4b34bef0800abccf12a984e2a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faefb892a54fcc8e594d81ae5b5933a819c42c67e213f7f6468d499b63075b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsMariaDb]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsMariaDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsMariaDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c44ff898ff8160a6da33c38e0bf27d896795a22c66fc4bfaac6a85ae88c6c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMonitor",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "exclude_tags": "excludeTags",
        "include_tags": "includeTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
        "resource_types": "resourceTypes",
    },
)
class CloudAzureIntegrationsMonitor:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: A flag that specifies if the integration is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#enabled CloudAzureIntegrations#enabled}
        :param exclude_tags: Specify resource tags in 'key:value' form to be excluded from monitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#exclude_tags CloudAzureIntegrations#exclude_tags}
        :param include_tags: Specify resource tags in 'key:value' form to be monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#include_tags CloudAzureIntegrations#include_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        :param resource_types: Specify each Azure resource type that needs to be monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_types CloudAzureIntegrations#resource_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ff5b0adbe7eb73f86d1664e0c5fcb705e72d6b7953e6731eb72dbdd9b35396)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exclude_tags", value=exclude_tags, expected_type=type_hints["exclude_tags"])
            check_type(argname="argument include_tags", value=include_tags, expected_type=type_hints["include_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if exclude_tags is not None:
            self._values["exclude_tags"] = exclude_tags
        if include_tags is not None:
            self._values["include_tags"] = include_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag that specifies if the integration is active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#enabled CloudAzureIntegrations#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify resource tags in 'key:value' form to be excluded from monitoring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#exclude_tags CloudAzureIntegrations#exclude_tags}
        '''
        result = self._values.get("exclude_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify resource tags in 'key:value' form to be monitored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#include_tags CloudAzureIntegrations#include_tags}
        '''
        result = self._values.get("include_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Azure resource type that needs to be monitored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_types CloudAzureIntegrations#resource_types}
        '''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMonitorOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac4624a67379590060c0f9fd3bbb7a7bab5ecb34d9e5fd37696a2af9fa9e813)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExcludeTags")
    def reset_exclude_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeTags", []))

    @jsii.member(jsii_name="resetIncludeTags")
    def reset_include_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeTagsInput")
    def exclude_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeTagsInput")
    def include_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e884230b4ce417a7539a8b71170b8a7a98c7a3084cf8b66d730c336e11a2d79b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeTags")
    def exclude_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeTags"))

    @exclude_tags.setter
    def exclude_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d22d5a4cdaf6504e3fe281f1f584e8b770b98b582b2a0f5de6d12e89b2a77dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeTags")
    def include_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeTags"))

    @include_tags.setter
    def include_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735044179ba0a6dd797d0165a126590f5eee0f10ae1cce8e64d18f803bfb4307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f0e9a4c005ace0d67fe825086831e0ee8f13046273be8e5f6e894e22bd1dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51a7b9e540bc8ad0274cd9715a4d6480db72d876ac2929046eb8d276147a1f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e07d6766ae0c3ee7cc6bfaa3e4ea193baf0bcbc95c5015757843a5603b9dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsMonitor]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9976f048ffc5ae4ee16ad3e5af2bcf894489cf171ebc636e78f933f20e2ee967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMysql",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsMysql:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99d3dfe6e539fda32eaa9d7f9e2e3c3d68251021122fca742fde8c87ee92549)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsMysql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMysqlFlexible",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsMysqlFlexible:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41dba33ee44e2df1bd672294c185c74fff558ffc1aef921fb6f0b000e699d81)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsMysqlFlexible(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsMysqlFlexibleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMysqlFlexibleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654e8f2f5906a97ff7cc7dc930109db5e87493d3f6d77347993252c19dd14cd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbb7af86ffe9c4e59144fe2aafd26a8e7a58c322cbec7b3c783ab57fe18cd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332f9323e160fa8722986bbb6b78c75dfcf4014817e8b68a4655d5a997c50582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsMysqlFlexible]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsMysqlFlexible], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsMysqlFlexible],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfea0a2c42e9276455d33aba5f26c62730dea918f47a22dffb968ca1bd3f09d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudAzureIntegrationsMysqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsMysqlOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9efff158440a256016ccedf35d22938aae398da5d50c6c73bc9b566c139f24c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a04bc66ee407c1c3d349209f8b45ffd361f0a2182a7aeab82397d07c1d5c755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ec4128844211db6ee8b23412cc892faa2ab6d89fda3676d8116aa46e80818b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsMysql]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsMysql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsMysql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a55202516983aff4ff3a3ef2c62fa4999664d619e026171eaea691d3cb5fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsPostgresql",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsPostgresql:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57cea74c523a00c6b8913d093e5a7ef64a52aa8217c1530345109e4751a589a)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsPostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsPostgresqlFlexible",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsPostgresqlFlexible:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34972eaf6da565601b3b9b3b859317cf9bdc294b5aec795198654d4e0d5269d4)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsPostgresqlFlexible(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsPostgresqlFlexibleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsPostgresqlFlexibleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a324d28b6a346524996641c14c43e959ace16c576960318be80ddb733e75638)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97a02588417312971466aaadab0795c17c24ebfa1f2620390c48e73e2554772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d0d90ee9d475e4c75165d01304cf2c26ef87b704fc256978eab827f741a3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAzureIntegrationsPostgresqlFlexible]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsPostgresqlFlexible], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsPostgresqlFlexible],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8e4cf82d1e959ad4a92f59c1175a54ad33a8514c773bb3402d313c60678375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudAzureIntegrationsPostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsPostgresqlOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137d19afa4041a8cda30396010bdf8d6338fc37786f2430f37b400408ec1da5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d103d24c07102e1d5dfe260b0f1e8754a2038481bc4c6211fb31bae194690c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d8ac98d2b35748b0df5c9bfd696d7d1b3eb6108297a134c37eff9891c69ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsPostgresql]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsPostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsPostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934348723024a91b602f98687f4b5e23fe22e75c82970ea7ebe2653c5282469b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsPowerBiDedicated",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsPowerBiDedicated:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866d90296f33d109ca7f8e7317077213be942271e617474a71e932d992e2347e)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsPowerBiDedicated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsPowerBiDedicatedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsPowerBiDedicatedOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93364f4b33c7fda60c1fc3fa27188c581f8cf0bb3920507f6e543436353993cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea80aea07a96fa7412027a07133284b8ab8c431cab4064a700fe677c5dfaf2db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121a3de1ae78bdfb9a1f7caacd2084cd2db795ab36007b90124560c5ad5f223a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsPowerBiDedicated]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsPowerBiDedicated], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsPowerBiDedicated],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d88699d8e7b283e6c279e542e5244c085b62c69e568a201c82b38625a1cf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsRedisCache",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsRedisCache:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bc28abd6beafd41916c5aa801a03896b60d4c1ded5228b184fe8b55a145230)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsRedisCache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsRedisCacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsRedisCacheOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5180756f024d00fbd2de938bd30f4edd20ba5b0498cc263e7333fa27520ea3b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148445c848b22d2adab5f7f09a4053cbafb85bc3802bbb4d3eb77d1995185cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de39cc92fb8bff1c803675b4237981ce617ebc43739c5cc366679e2a737b6f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsRedisCache]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsRedisCache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsRedisCache],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0a5c82f66051fe0d766f620308bdaea5b0ac18a0bf29bcc5253a1767d9d234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsServiceBus",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsServiceBus:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35eac16d1716f14a1e80c5d7272ca5054e2acec8e7f31c3270dc35530e64f2d)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsServiceBus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsServiceBusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsServiceBusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c0d49b9b689d66d5ec9fad6c25a6aa9b007e3463f9389906c790428abb8c71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b972507c24a6f5b021031d76a810380ca4684309a889404f47e1fe962139ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc566f24f5cb0f2e9f03a936c93c879db2268dfaee34baf6bb88bde792a18ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsServiceBus]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsServiceBus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsServiceBus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb35dbb2bd1ded808590bd6be9a265ced72427d10d58f5523225b7436516c660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsSql",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsSql:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171fd9142bc1c5db6e9b32a88936934d5a33127e5e93b09b54d602c27f9c423f)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsSqlManaged",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsSqlManaged:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05402b7d3e0f00054fa4d33f659f6984929d8c6c9836446513d7d275ecce8b6f)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsSqlManaged(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsSqlManagedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsSqlManagedOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5594cc8cac497f100efaf7ab8423b95fb1e132b44b967e0fd855812e97e89dbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdad4f37645b86338cc5ed970ea641dbf8a9d7f07d02b89c37cf7d062bd5e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfc6f2c4b92b1f91ae5ab1fadbe2aba65bbd0de0b49ab6749db4f627086f013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsSqlManaged]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsSqlManaged], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsSqlManaged],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fb414d272307c4d2bf6b952a8206e7a61cee905ee5be98409872a14bf3343f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudAzureIntegrationsSqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsSqlOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bc6c3ffc0a7e5d4298f1a013aa6c0d8411fc87e909048fdfd38cc08bf8b8f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189c08088fda0fe5994f219285897f2c68876a25725253d5ebb546fae34224d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf8d62898449a2f59ea6065af86beedfbc7d8726ff6691445f902bb3d5ca3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsSql]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsSql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAzureIntegrationsSql]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ccba02fba2b75d1e95e1e5942779e17008217429ef5684e6eec2da2dbe108fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsStorage",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsStorage:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45839cf9409c6f6353b9db559836b04635b4782e8f0682880f5905f29afd4073)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsStorageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595333f1ce57f870d856cefb81a55982ab8d191f93b160c365a3e6b6ec245f24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41919bc4e9dbafa5014f8f209874d019aaa51e72ccd0e2a0b8043fa67681803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd911261d884446f842eaff36f02ab9ff17d88574c06124b4759af2dba50f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsStorage]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8d7b5672312dad3ab8cae9897f1e8678c7bf1696e636232a88b7ef529d0027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsVirtualMachine:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4cb54482b07fe3d354e5fbbbe5351751da9f4fed368a2b787b385d1999e154)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsVirtualMachineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVirtualMachineOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6715a05701b3881e9cdf4495fe5874f21fa110aa6beae13f542e3bd1d6e1966c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4989684026de032a673402aa9cc5b35c34d61724919318a050ad189a816eabe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b75ca36384c09b09d0c6de0dcca350da5836c31a0b60028d29c4099fa6e8f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsVirtualMachine]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsVirtualMachine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsVirtualMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb659f89587db15c425579cb077ec02ef40285d57374a3352daebf416ceb95ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVirtualNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsVirtualNetworks:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f4e5851f866620ad8e0ac15c36722771f224421a1f217c378f7aede9094f89)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsVirtualNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsVirtualNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVirtualNetworksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90ca60e0ba54bbd23df20341679a78f7c45df43aa9407186056b614b0175332)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0293a779a3b584b8be30a0b267ea2ea11bc8d708a3d5cb90ff0f7d67f70b66f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c0c52cd6bdd115fcb08359a27345a3938a5f991d4992a2ae1c10f189cea8e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsVirtualNetworks]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsVirtualNetworks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsVirtualNetworks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc0c0d9ac41b226a07755624178fd5c2ff08633b50a29a9918acd05e6ef8a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVms",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsVms:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b747a4efb4dcf27c935b1d2b25e2e8bdbf34f3a94de3c7644314010a75844a)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsVms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsVmsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVmsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8457edbdffd71b84915581713c2d1ec3e12cb9e2fe37555ba7d8a1c49b39cf0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528a02b6733a6a69b8d0226d896b11b568715efd58b510701650a5cd053b831f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54021a5638cad6a5b4e227d4afade777cd1f5828fee81a0bd58b54fef6c66db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsVms]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsVms], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAzureIntegrationsVms]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a0bcd6034427b79b540cc863702f0761edc86e98e43d53dee4c6276186e344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVpnGateway",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "resource_groups": "resourceGroups",
    },
)
class CloudAzureIntegrationsVpnGateway:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        :param resource_groups: Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dcd8ea1180ea35b1d1d4f69ddcd068275b9a32cee5b0ea6bc07c76138cd1e48)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if resource_groups is not None:
            self._values["resource_groups"] = resource_groups

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#metrics_polling_interval CloudAzureIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each Resource group associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_azure_integrations#resource_groups CloudAzureIntegrations#resource_groups}
        '''
        result = self._values.get("resource_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAzureIntegrationsVpnGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAzureIntegrationsVpnGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAzureIntegrations.CloudAzureIntegrationsVpnGatewayOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78a35704b601447c76abf244f2544659d91cb11103b68d0da44e32dc47d8bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetResourceGroups")
    def reset_resource_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroups", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58a19fe87477821c0f1fe4e041d8f46a305a4c4eefe23772faf7a6c1ec04246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceGroups"))

    @resource_groups.setter
    def resource_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc880d2a7bfcc7cb87337d1b613ff3b7ae29d6dc1511199e8c16e2d93f1b7b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAzureIntegrationsVpnGateway]:
        return typing.cast(typing.Optional[CloudAzureIntegrationsVpnGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAzureIntegrationsVpnGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a83749eb9c04a4389f1e65044876c24894b11bf8a403fc0d43faaaa048b7879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudAzureIntegrations",
    "CloudAzureIntegrationsApiManagement",
    "CloudAzureIntegrationsApiManagementOutputReference",
    "CloudAzureIntegrationsAppGateway",
    "CloudAzureIntegrationsAppGatewayOutputReference",
    "CloudAzureIntegrationsAppService",
    "CloudAzureIntegrationsAppServiceOutputReference",
    "CloudAzureIntegrationsConfig",
    "CloudAzureIntegrationsContainers",
    "CloudAzureIntegrationsContainersOutputReference",
    "CloudAzureIntegrationsCosmosDb",
    "CloudAzureIntegrationsCosmosDbOutputReference",
    "CloudAzureIntegrationsCostManagement",
    "CloudAzureIntegrationsCostManagementOutputReference",
    "CloudAzureIntegrationsDataFactory",
    "CloudAzureIntegrationsDataFactoryOutputReference",
    "CloudAzureIntegrationsEventHub",
    "CloudAzureIntegrationsEventHubOutputReference",
    "CloudAzureIntegrationsExpressRoute",
    "CloudAzureIntegrationsExpressRouteOutputReference",
    "CloudAzureIntegrationsFirewalls",
    "CloudAzureIntegrationsFirewallsOutputReference",
    "CloudAzureIntegrationsFrontDoor",
    "CloudAzureIntegrationsFrontDoorOutputReference",
    "CloudAzureIntegrationsFunctions",
    "CloudAzureIntegrationsFunctionsOutputReference",
    "CloudAzureIntegrationsKeyVault",
    "CloudAzureIntegrationsKeyVaultOutputReference",
    "CloudAzureIntegrationsLoadBalancer",
    "CloudAzureIntegrationsLoadBalancerOutputReference",
    "CloudAzureIntegrationsLogicApps",
    "CloudAzureIntegrationsLogicAppsOutputReference",
    "CloudAzureIntegrationsMachineLearning",
    "CloudAzureIntegrationsMachineLearningOutputReference",
    "CloudAzureIntegrationsMariaDb",
    "CloudAzureIntegrationsMariaDbOutputReference",
    "CloudAzureIntegrationsMonitor",
    "CloudAzureIntegrationsMonitorOutputReference",
    "CloudAzureIntegrationsMysql",
    "CloudAzureIntegrationsMysqlFlexible",
    "CloudAzureIntegrationsMysqlFlexibleOutputReference",
    "CloudAzureIntegrationsMysqlOutputReference",
    "CloudAzureIntegrationsPostgresql",
    "CloudAzureIntegrationsPostgresqlFlexible",
    "CloudAzureIntegrationsPostgresqlFlexibleOutputReference",
    "CloudAzureIntegrationsPostgresqlOutputReference",
    "CloudAzureIntegrationsPowerBiDedicated",
    "CloudAzureIntegrationsPowerBiDedicatedOutputReference",
    "CloudAzureIntegrationsRedisCache",
    "CloudAzureIntegrationsRedisCacheOutputReference",
    "CloudAzureIntegrationsServiceBus",
    "CloudAzureIntegrationsServiceBusOutputReference",
    "CloudAzureIntegrationsSql",
    "CloudAzureIntegrationsSqlManaged",
    "CloudAzureIntegrationsSqlManagedOutputReference",
    "CloudAzureIntegrationsSqlOutputReference",
    "CloudAzureIntegrationsStorage",
    "CloudAzureIntegrationsStorageOutputReference",
    "CloudAzureIntegrationsVirtualMachine",
    "CloudAzureIntegrationsVirtualMachineOutputReference",
    "CloudAzureIntegrationsVirtualNetworks",
    "CloudAzureIntegrationsVirtualNetworksOutputReference",
    "CloudAzureIntegrationsVms",
    "CloudAzureIntegrationsVmsOutputReference",
    "CloudAzureIntegrationsVpnGateway",
    "CloudAzureIntegrationsVpnGatewayOutputReference",
]

publication.publish()

def _typecheckingstub__d141dd03a0dfe6b24f19b959a1c00338ad703fb54e474e9622232db4980b760c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    api_management: typing.Optional[typing.Union[CloudAzureIntegrationsApiManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    app_gateway: typing.Optional[typing.Union[CloudAzureIntegrationsAppGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    app_service: typing.Optional[typing.Union[CloudAzureIntegrationsAppService, typing.Dict[builtins.str, typing.Any]]] = None,
    containers: typing.Optional[typing.Union[CloudAzureIntegrationsContainers, typing.Dict[builtins.str, typing.Any]]] = None,
    cosmos_db: typing.Optional[typing.Union[CloudAzureIntegrationsCosmosDb, typing.Dict[builtins.str, typing.Any]]] = None,
    cost_management: typing.Optional[typing.Union[CloudAzureIntegrationsCostManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    data_factory: typing.Optional[typing.Union[CloudAzureIntegrationsDataFactory, typing.Dict[builtins.str, typing.Any]]] = None,
    event_hub: typing.Optional[typing.Union[CloudAzureIntegrationsEventHub, typing.Dict[builtins.str, typing.Any]]] = None,
    express_route: typing.Optional[typing.Union[CloudAzureIntegrationsExpressRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    firewalls: typing.Optional[typing.Union[CloudAzureIntegrationsFirewalls, typing.Dict[builtins.str, typing.Any]]] = None,
    front_door: typing.Optional[typing.Union[CloudAzureIntegrationsFrontDoor, typing.Dict[builtins.str, typing.Any]]] = None,
    functions: typing.Optional[typing.Union[CloudAzureIntegrationsFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key_vault: typing.Optional[typing.Union[CloudAzureIntegrationsKeyVault, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer: typing.Optional[typing.Union[CloudAzureIntegrationsLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    logic_apps: typing.Optional[typing.Union[CloudAzureIntegrationsLogicApps, typing.Dict[builtins.str, typing.Any]]] = None,
    machine_learning: typing.Optional[typing.Union[CloudAzureIntegrationsMachineLearning, typing.Dict[builtins.str, typing.Any]]] = None,
    maria_db: typing.Optional[typing.Union[CloudAzureIntegrationsMariaDb, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[CloudAzureIntegrationsMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql: typing.Optional[typing.Union[CloudAzureIntegrationsMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql_flexible: typing.Optional[typing.Union[CloudAzureIntegrationsMysqlFlexible, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[CloudAzureIntegrationsPostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_flexible: typing.Optional[typing.Union[CloudAzureIntegrationsPostgresqlFlexible, typing.Dict[builtins.str, typing.Any]]] = None,
    power_bi_dedicated: typing.Optional[typing.Union[CloudAzureIntegrationsPowerBiDedicated, typing.Dict[builtins.str, typing.Any]]] = None,
    redis_cache: typing.Optional[typing.Union[CloudAzureIntegrationsRedisCache, typing.Dict[builtins.str, typing.Any]]] = None,
    service_bus: typing.Optional[typing.Union[CloudAzureIntegrationsServiceBus, typing.Dict[builtins.str, typing.Any]]] = None,
    sql: typing.Optional[typing.Union[CloudAzureIntegrationsSql, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_managed: typing.Optional[typing.Union[CloudAzureIntegrationsSqlManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[CloudAzureIntegrationsStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[CloudAzureIntegrationsVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_networks: typing.Optional[typing.Union[CloudAzureIntegrationsVirtualNetworks, typing.Dict[builtins.str, typing.Any]]] = None,
    vms: typing.Optional[typing.Union[CloudAzureIntegrationsVms, typing.Dict[builtins.str, typing.Any]]] = None,
    vpn_gateway: typing.Optional[typing.Union[CloudAzureIntegrationsVpnGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7363e4ba7335e906677b75e6df37ae4c2c0d53a616b0176898076a81d3f764(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a01589fa7f1711ba7b77ce2e45c34b154f9996989650016575ba5e6e8891aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92d8154df06c1054340548e1a826b72e671227dbf466a4c01d94dfda651deea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3677b76635f299e5c327982d4034ac772fd9f98393dc3b75da3549c77455f5ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99666a8e297dc41bb6603a2f5b5fe5400a30771fc2235188022acb6da849160f(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c218a51492d01d521d024c7853d89ded927bfdd2ed432e882e776fd471ddc5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf001879bb202f47515ab10368e68a547ac6c7f205cdefa1686d12d38d1fa44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa9518f394d0f8eb47549e8339c0dc1c005d11076078de666aac2d72d685a8e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f5436078455d6808b08219e2120fc63dd0c647c7fd31b44c24669152c8039e(
    value: typing.Optional[CloudAzureIntegrationsApiManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58752629d821f42bd699e3c4febf7814452e151e424c772413fc250db6c9e370(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59159e36e5d3f0e946fff901575e440c5e899cf1f57dc2f8e7709aacbaf3927c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6130f41ac9dac30accaed89850f07e2838fc9491930c63d577a432feb74ddcb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5ba992ddc59fef1dcb10af5747c83d76cf31cc448fceee4813157276f139f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e64389b7e81db6f6f120b1b7d21477c2dafc4463de4737282ccd79c0ba5ec6f(
    value: typing.Optional[CloudAzureIntegrationsAppGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322510f410884ff89e9453cc12c053370754a94bc464aafe26da8cc05bd879f9(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffde5f2b021cbd50d130a76a4a5a142874fa54cd3b00243ec97bb7207afefe84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e3a6e8ecc1206ddf66120695294ae44eec9b107db061da67f7618c5ee08d40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70ebef4787f84178eb88a3aa2c6a0ce11372d3646dbb51e22a06ed1dfe8e047(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4084ee20c4b376be429b8b9046d4f221f0b2d6cfb472d18f0774988011d9a00(
    value: typing.Optional[CloudAzureIntegrationsAppService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b38caeaf90cdfca3b21c94277eb3f00ace750df95799e3cd0e0395662cab3e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    api_management: typing.Optional[typing.Union[CloudAzureIntegrationsApiManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    app_gateway: typing.Optional[typing.Union[CloudAzureIntegrationsAppGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    app_service: typing.Optional[typing.Union[CloudAzureIntegrationsAppService, typing.Dict[builtins.str, typing.Any]]] = None,
    containers: typing.Optional[typing.Union[CloudAzureIntegrationsContainers, typing.Dict[builtins.str, typing.Any]]] = None,
    cosmos_db: typing.Optional[typing.Union[CloudAzureIntegrationsCosmosDb, typing.Dict[builtins.str, typing.Any]]] = None,
    cost_management: typing.Optional[typing.Union[CloudAzureIntegrationsCostManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    data_factory: typing.Optional[typing.Union[CloudAzureIntegrationsDataFactory, typing.Dict[builtins.str, typing.Any]]] = None,
    event_hub: typing.Optional[typing.Union[CloudAzureIntegrationsEventHub, typing.Dict[builtins.str, typing.Any]]] = None,
    express_route: typing.Optional[typing.Union[CloudAzureIntegrationsExpressRoute, typing.Dict[builtins.str, typing.Any]]] = None,
    firewalls: typing.Optional[typing.Union[CloudAzureIntegrationsFirewalls, typing.Dict[builtins.str, typing.Any]]] = None,
    front_door: typing.Optional[typing.Union[CloudAzureIntegrationsFrontDoor, typing.Dict[builtins.str, typing.Any]]] = None,
    functions: typing.Optional[typing.Union[CloudAzureIntegrationsFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key_vault: typing.Optional[typing.Union[CloudAzureIntegrationsKeyVault, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer: typing.Optional[typing.Union[CloudAzureIntegrationsLoadBalancer, typing.Dict[builtins.str, typing.Any]]] = None,
    logic_apps: typing.Optional[typing.Union[CloudAzureIntegrationsLogicApps, typing.Dict[builtins.str, typing.Any]]] = None,
    machine_learning: typing.Optional[typing.Union[CloudAzureIntegrationsMachineLearning, typing.Dict[builtins.str, typing.Any]]] = None,
    maria_db: typing.Optional[typing.Union[CloudAzureIntegrationsMariaDb, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[CloudAzureIntegrationsMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql: typing.Optional[typing.Union[CloudAzureIntegrationsMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql_flexible: typing.Optional[typing.Union[CloudAzureIntegrationsMysqlFlexible, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[CloudAzureIntegrationsPostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_flexible: typing.Optional[typing.Union[CloudAzureIntegrationsPostgresqlFlexible, typing.Dict[builtins.str, typing.Any]]] = None,
    power_bi_dedicated: typing.Optional[typing.Union[CloudAzureIntegrationsPowerBiDedicated, typing.Dict[builtins.str, typing.Any]]] = None,
    redis_cache: typing.Optional[typing.Union[CloudAzureIntegrationsRedisCache, typing.Dict[builtins.str, typing.Any]]] = None,
    service_bus: typing.Optional[typing.Union[CloudAzureIntegrationsServiceBus, typing.Dict[builtins.str, typing.Any]]] = None,
    sql: typing.Optional[typing.Union[CloudAzureIntegrationsSql, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_managed: typing.Optional[typing.Union[CloudAzureIntegrationsSqlManaged, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[CloudAzureIntegrationsStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machine: typing.Optional[typing.Union[CloudAzureIntegrationsVirtualMachine, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_networks: typing.Optional[typing.Union[CloudAzureIntegrationsVirtualNetworks, typing.Dict[builtins.str, typing.Any]]] = None,
    vms: typing.Optional[typing.Union[CloudAzureIntegrationsVms, typing.Dict[builtins.str, typing.Any]]] = None,
    vpn_gateway: typing.Optional[typing.Union[CloudAzureIntegrationsVpnGateway, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beea570aac5416ef4b0588ba1094fa843ddafa29d871e7ae2d8760d41d76e770(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b018258b66965e46ddbe40c683334756dbd315194dee79d38e5359ab78898717(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04cd4b5c4cfc7038996defe5e24084c4fe2ec25804fbf632be89b14446de0d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec00a7f3963225e573d5706a078b45ee3537e7b784cb8783ff4f2e30142726e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3a92334d17f3346772803797d60a715efd9c4217697f7021940f0e88c4c51d(
    value: typing.Optional[CloudAzureIntegrationsContainers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017b6c6e9145dcd6313121c29f6f073b91d5cc44a2dcb92668b2a77466016b41(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabd4a3f0557579dd9af0f242682e184bef3678f887e1a077cab532591786ade(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b62ec72558c598195ed5ddddd269983c7e0750fc40465e704638196bd972e20(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafd5f8ee5613b19386a1d4e2ec8211fcee8efb0f9bc84109405efe188545dcd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28eaee0a8125e0e9f0c0cf93571a4324af1b0ed6bd3067ada5a2e99fabcec4a8(
    value: typing.Optional[CloudAzureIntegrationsCosmosDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94973ebbd074b10355ecb4e5daead82ea85d379466493b44371a5e23b7bd87c9(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053808b312ee19fab790ff90b2f7f8c8bf098f7384c77a1431ad39664525f414(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f9946776c1184cc66e2051d95a2f5cee50b92c2440c02e99c2e73244f7cd46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c21edc45e864a08eaabf23d086501477e45329a54f073a8a87005abbc1cbd8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8e52de5aed5b4df0d2dff4e8a68d351a9ca7ac7d7730dc09c62e841037a3b6(
    value: typing.Optional[CloudAzureIntegrationsCostManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d69242da02a0948f8b2fabedeaac1e11a466b6181741f51339116d3d7271a6c(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca42ccfafcd02829c4b34a80e88c6c2dec0e03f84a72688ef32005da541167b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2485a4079ee01552dbe776e453078f23ed59a551680ab9b74c858e588d878e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564d3e114c7df63a688cc9ca66455efbdeed9f8b96c049a552a444f00c97ba31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6d59f627662fc848bbbc0519b8f0998e70039e6e630930e8806d4e6c2a3cd0(
    value: typing.Optional[CloudAzureIntegrationsDataFactory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8920cb9e9dbab5bf850d23ef0f7d517f9c9ef0b84de326efffa398e2cf95c399(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66d57e85d1b1c6c590448d4f874592918a4c6a7c3185dac57ceadc4d1503c8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095f150e873cb98e8dd0526d397bee466e26980093c6461f21486eb300452cb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d35412e2dd6f7821d90c9ecba02a74555e5db3fa8cae3ac298885be24a47d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193f0746e997b84c84759e758b91a287ed48ba6692168bd28c341ddcc6d2b381(
    value: typing.Optional[CloudAzureIntegrationsEventHub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d219373af51e4448040c8d3e22e35524427f8a8f4c87eb0c7eb6a7f8fc2186ab(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabaae8e8ed5c70b3862ffbb9d1a8d66b568c7bd6bab136ea5116c40edb5a119(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157616a3dbcdb25041203f01dc138c13b48310f4547c5fe104cd4925bdaa67c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026fe46f89da4979af8a4b5c318d5d0ce311df2860ad6a7f720edbaadbe6cd1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e58fd999fa45d0cfe9d29bc1b666d4864f3eefd12ee72a6d1d48e9b7fe6e255(
    value: typing.Optional[CloudAzureIntegrationsExpressRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e569b05e1e4b4e4639632bf69122e4f9e04fe148faef4f016f8b8dcc7266df(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81aa83b2fce243d41303a26e7dc7b8fdef371da4dba6eb8a382654329302fa18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a7d50adb6a0bb062c60e982e36bb0f79a7daecba8ab7da39f220741b658f4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a264863db378258c887da5de85e81b9c4bbcf56f1755cc2ec9650815b04d31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0335630154f00c03bd986baa2880c91c53c21dd1d88c329a5e22a75d40faa6c2(
    value: typing.Optional[CloudAzureIntegrationsFirewalls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10268924df74aa499e93912ceec70b0d72f95b80f05daa273f01d8c62a3dd24(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac036f737c236c5cbc1835f968ba3f8a79c8585776be484b7887b5cdce5d832d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f935fea2866cbed83bb173c24923888545e3af33f30a525217abd346e740c81e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32303773c210786f1f92ee01ee33ffd504920c19f8408811cfb56a8f2794e565(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae122d547ab6f77ec05bf8e3eac4ed47411463c2d3c01689dae7639fac0b5a2a(
    value: typing.Optional[CloudAzureIntegrationsFrontDoor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf317ce796c198e2498d1ba072491cad3907ccdfd55ce44d26722aab5d5c2c2(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd6efc0a9f38831075cdaba74a9e8c1277d9dcf988cb2fe5b4e671ae095867b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7ede262c3f7a5f368996541236d40989e3443ead8a91b60db512dbae0cb5d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cb6915b6144174c6ef435fdfa51d3795c37ab021805ca23d01cf34a532fb5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed95979b2e3ebd5286795c7ef027db76d2880d8ea7dd8b29f40c553c24fb270(
    value: typing.Optional[CloudAzureIntegrationsFunctions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb08c3021ecbb836b1f0c55010013733664ac8a3c4921bb69eac078834a2f691(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab83d2c8506b04d9ab81abdfa9ec23ebc4d793c0376b61a709dc477a29f1da85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8a356daa8b788df700051feb29ebf7af7826dc4153ee309d34f31839b007e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42ca401a9d2b6559397d75b02bb60e37f237a7730a577649b3b33c719f50781(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27fb2ca292c190ef94662b59a27d7456c0939c0302af4d0e954031a9091ebf3(
    value: typing.Optional[CloudAzureIntegrationsKeyVault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03af203168a83126c7353b5fbb49784c2c678dc40bf95ebd7008899e9fa9af6b(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f95e38d0e67d9f70573dafedcf5dac57e1d2b6672e07bc3f150cf85d74c736(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7545b1e7f85be9e2200c83e488a3861859cae6e8ee7be169d49571d0e85ea429(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88de7521b05a6deb662799c74fd9697c31ba63153ceac56ebf23c006ad6037a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fb56a2b925099fe3f9d3e1c40cd547ea32df73180728b5ecafb5747bb764df(
    value: typing.Optional[CloudAzureIntegrationsLoadBalancer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bf425ee69410cecdc7dd61386a8cd21145c911ee4ed965ea1f914e4d02a682(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4a79669719664559268f220384cffd21649a757c8798374710c7ea6d713d57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34a398cc24d3bf4cdda0771eb08ffcf8b3863f02c15ac289831a0d22fea259f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7580b89ee474b8f1571eed992f5537b4dc4f8a50fe734f0e04912f836930fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c043ccad04f353425dd04ea7fb77d5be25894b515d082fb7a2e1d46dc428a5(
    value: typing.Optional[CloudAzureIntegrationsLogicApps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053136e2f18b07dcbf7a41de79e92d7dd95d6cb309e40dad6f7fc46562da195c(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5e6f6da23dc251ec895d299b03dbd738c00e829fe805a06ad6c231873148ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa1cbb3e6f900bbba14328274785bad6d1cafd007d9f2106183326e0e374b69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa492ad19436cb03805682018add39b13a946813aed44dfba34fab2c2437f43(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237badac773ea30d64ce2e0744f99838dc9bc64850824340b1cbcd8172ae6049(
    value: typing.Optional[CloudAzureIntegrationsMachineLearning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e263082b32e1960e57849acc57c6512bd3f644e4c410978ea7889e2a27d04f(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8fd3de2f406df0dda57e45af4baab3a672297f85cadd2d4de94fc44c77e202(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ece926968833822a2da198df5ae766096f9f4b34bef0800abccf12a984e2a58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faefb892a54fcc8e594d81ae5b5933a819c42c67e213f7f6468d499b63075b50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c44ff898ff8160a6da33c38e0bf27d896795a22c66fc4bfaac6a85ae88c6c5a(
    value: typing.Optional[CloudAzureIntegrationsMariaDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ff5b0adbe7eb73f86d1664e0c5fcb705e72d6b7953e6731eb72dbdd9b35396(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac4624a67379590060c0f9fd3bbb7a7bab5ecb34d9e5fd37696a2af9fa9e813(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e884230b4ce417a7539a8b71170b8a7a98c7a3084cf8b66d730c336e11a2d79b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d22d5a4cdaf6504e3fe281f1f584e8b770b98b582b2a0f5de6d12e89b2a77dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735044179ba0a6dd797d0165a126590f5eee0f10ae1cce8e64d18f803bfb4307(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f0e9a4c005ace0d67fe825086831e0ee8f13046273be8e5f6e894e22bd1dbf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51a7b9e540bc8ad0274cd9715a4d6480db72d876ac2929046eb8d276147a1f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e07d6766ae0c3ee7cc6bfaa3e4ea193baf0bcbc95c5015757843a5603b9dc2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9976f048ffc5ae4ee16ad3e5af2bcf894489cf171ebc636e78f933f20e2ee967(
    value: typing.Optional[CloudAzureIntegrationsMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99d3dfe6e539fda32eaa9d7f9e2e3c3d68251021122fca742fde8c87ee92549(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41dba33ee44e2df1bd672294c185c74fff558ffc1aef921fb6f0b000e699d81(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654e8f2f5906a97ff7cc7dc930109db5e87493d3f6d77347993252c19dd14cd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbb7af86ffe9c4e59144fe2aafd26a8e7a58c322cbec7b3c783ab57fe18cd0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332f9323e160fa8722986bbb6b78c75dfcf4014817e8b68a4655d5a997c50582(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfea0a2c42e9276455d33aba5f26c62730dea918f47a22dffb968ca1bd3f09d1(
    value: typing.Optional[CloudAzureIntegrationsMysqlFlexible],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9efff158440a256016ccedf35d22938aae398da5d50c6c73bc9b566c139f24c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a04bc66ee407c1c3d349209f8b45ffd361f0a2182a7aeab82397d07c1d5c755(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ec4128844211db6ee8b23412cc892faa2ab6d89fda3676d8116aa46e80818b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a55202516983aff4ff3a3ef2c62fa4999664d619e026171eaea691d3cb5fbe(
    value: typing.Optional[CloudAzureIntegrationsMysql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57cea74c523a00c6b8913d093e5a7ef64a52aa8217c1530345109e4751a589a(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34972eaf6da565601b3b9b3b859317cf9bdc294b5aec795198654d4e0d5269d4(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a324d28b6a346524996641c14c43e959ace16c576960318be80ddb733e75638(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97a02588417312971466aaadab0795c17c24ebfa1f2620390c48e73e2554772(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d0d90ee9d475e4c75165d01304cf2c26ef87b704fc256978eab827f741a3de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8e4cf82d1e959ad4a92f59c1175a54ad33a8514c773bb3402d313c60678375(
    value: typing.Optional[CloudAzureIntegrationsPostgresqlFlexible],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137d19afa4041a8cda30396010bdf8d6338fc37786f2430f37b400408ec1da5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d103d24c07102e1d5dfe260b0f1e8754a2038481bc4c6211fb31bae194690c64(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d8ac98d2b35748b0df5c9bfd696d7d1b3eb6108297a134c37eff9891c69ba7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934348723024a91b602f98687f4b5e23fe22e75c82970ea7ebe2653c5282469b(
    value: typing.Optional[CloudAzureIntegrationsPostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866d90296f33d109ca7f8e7317077213be942271e617474a71e932d992e2347e(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93364f4b33c7fda60c1fc3fa27188c581f8cf0bb3920507f6e543436353993cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea80aea07a96fa7412027a07133284b8ab8c431cab4064a700fe677c5dfaf2db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121a3de1ae78bdfb9a1f7caacd2084cd2db795ab36007b90124560c5ad5f223a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d88699d8e7b283e6c279e542e5244c085b62c69e568a201c82b38625a1cf40(
    value: typing.Optional[CloudAzureIntegrationsPowerBiDedicated],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bc28abd6beafd41916c5aa801a03896b60d4c1ded5228b184fe8b55a145230(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5180756f024d00fbd2de938bd30f4edd20ba5b0498cc263e7333fa27520ea3b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148445c848b22d2adab5f7f09a4053cbafb85bc3802bbb4d3eb77d1995185cb7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de39cc92fb8bff1c803675b4237981ce617ebc43739c5cc366679e2a737b6f4d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0a5c82f66051fe0d766f620308bdaea5b0ac18a0bf29bcc5253a1767d9d234(
    value: typing.Optional[CloudAzureIntegrationsRedisCache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35eac16d1716f14a1e80c5d7272ca5054e2acec8e7f31c3270dc35530e64f2d(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c0d49b9b689d66d5ec9fad6c25a6aa9b007e3463f9389906c790428abb8c71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b972507c24a6f5b021031d76a810380ca4684309a889404f47e1fe962139ea6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc566f24f5cb0f2e9f03a936c93c879db2268dfaee34baf6bb88bde792a18ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb35dbb2bd1ded808590bd6be9a265ced72427d10d58f5523225b7436516c660(
    value: typing.Optional[CloudAzureIntegrationsServiceBus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171fd9142bc1c5db6e9b32a88936934d5a33127e5e93b09b54d602c27f9c423f(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05402b7d3e0f00054fa4d33f659f6984929d8c6c9836446513d7d275ecce8b6f(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5594cc8cac497f100efaf7ab8423b95fb1e132b44b967e0fd855812e97e89dbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdad4f37645b86338cc5ed970ea641dbf8a9d7f07d02b89c37cf7d062bd5e54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfc6f2c4b92b1f91ae5ab1fadbe2aba65bbd0de0b49ab6749db4f627086f013(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fb414d272307c4d2bf6b952a8206e7a61cee905ee5be98409872a14bf3343f(
    value: typing.Optional[CloudAzureIntegrationsSqlManaged],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bc6c3ffc0a7e5d4298f1a013aa6c0d8411fc87e909048fdfd38cc08bf8b8f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189c08088fda0fe5994f219285897f2c68876a25725253d5ebb546fae34224d0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf8d62898449a2f59ea6065af86beedfbc7d8726ff6691445f902bb3d5ca3df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccba02fba2b75d1e95e1e5942779e17008217429ef5684e6eec2da2dbe108fe(
    value: typing.Optional[CloudAzureIntegrationsSql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45839cf9409c6f6353b9db559836b04635b4782e8f0682880f5905f29afd4073(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595333f1ce57f870d856cefb81a55982ab8d191f93b160c365a3e6b6ec245f24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41919bc4e9dbafa5014f8f209874d019aaa51e72ccd0e2a0b8043fa67681803(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd911261d884446f842eaff36f02ab9ff17d88574c06124b4759af2dba50f29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d7b5672312dad3ab8cae9897f1e8678c7bf1696e636232a88b7ef529d0027(
    value: typing.Optional[CloudAzureIntegrationsStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4cb54482b07fe3d354e5fbbbe5351751da9f4fed368a2b787b385d1999e154(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6715a05701b3881e9cdf4495fe5874f21fa110aa6beae13f542e3bd1d6e1966c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4989684026de032a673402aa9cc5b35c34d61724919318a050ad189a816eabe3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b75ca36384c09b09d0c6de0dcca350da5836c31a0b60028d29c4099fa6e8f38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb659f89587db15c425579cb077ec02ef40285d57374a3352daebf416ceb95ea(
    value: typing.Optional[CloudAzureIntegrationsVirtualMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f4e5851f866620ad8e0ac15c36722771f224421a1f217c378f7aede9094f89(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90ca60e0ba54bbd23df20341679a78f7c45df43aa9407186056b614b0175332(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0293a779a3b584b8be30a0b267ea2ea11bc8d708a3d5cb90ff0f7d67f70b66f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c0c52cd6bdd115fcb08359a27345a3938a5f991d4992a2ae1c10f189cea8e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc0c0d9ac41b226a07755624178fd5c2ff08633b50a29a9918acd05e6ef8a6e(
    value: typing.Optional[CloudAzureIntegrationsVirtualNetworks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b747a4efb4dcf27c935b1d2b25e2e8bdbf34f3a94de3c7644314010a75844a(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8457edbdffd71b84915581713c2d1ec3e12cb9e2fe37555ba7d8a1c49b39cf0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528a02b6733a6a69b8d0226d896b11b568715efd58b510701650a5cd053b831f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54021a5638cad6a5b4e227d4afade777cd1f5828fee81a0bd58b54fef6c66db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a0bcd6034427b79b540cc863702f0761edc86e98e43d53dee4c6276186e344(
    value: typing.Optional[CloudAzureIntegrationsVms],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcd8ea1180ea35b1d1d4f69ddcd068275b9a32cee5b0ea6bc07c76138cd1e48(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    resource_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78a35704b601447c76abf244f2544659d91cb11103b68d0da44e32dc47d8bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58a19fe87477821c0f1fe4e041d8f46a305a4c4eefe23772faf7a6c1ec04246(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc880d2a7bfcc7cb87337d1b613ff3b7ae29d6dc1511199e8c16e2d93f1b7b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a83749eb9c04a4389f1e65044876c24894b11bf8a403fc0d43faaaa048b7879(
    value: typing.Optional[CloudAzureIntegrationsVpnGateway],
) -> None:
    """Type checking stubs"""
    pass
