r'''
# `azurerm_data_factory_integration_runtime_azure_ssis`

Refer to the Terraform Registry for docs: [`azurerm_data_factory_integration_runtime_azure_ssis`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis).
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


class DataFactoryIntegrationRuntimeAzureSsis(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsis",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis azurerm_data_factory_integration_runtime_azure_ssis}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_factory_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        node_size: builtins.str,
        catalog_info: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisCatalogInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_compute_scale: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale", typing.Dict[builtins.str, typing.Any]]] = None,
        credential_name: typing.Optional[builtins.str] = None,
        custom_setup_script: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        express_custom_setup: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup", typing.Dict[builtins.str, typing.Any]]] = None,
        express_vnet_integration: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        package_store: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisPackageStore", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pipeline_external_compute_scale: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vnet_integration: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisVnetIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis azurerm_data_factory_integration_runtime_azure_ssis} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#data_factory_id DataFactoryIntegrationRuntimeAzureSsis#data_factory_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#location DataFactoryIntegrationRuntimeAzureSsis#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.
        :param node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#node_size DataFactoryIntegrationRuntimeAzureSsis#node_size}.
        :param catalog_info: catalog_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#catalog_info DataFactoryIntegrationRuntimeAzureSsis#catalog_info}
        :param copy_compute_scale: copy_compute_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#copy_compute_scale DataFactoryIntegrationRuntimeAzureSsis#copy_compute_scale}
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#credential_name DataFactoryIntegrationRuntimeAzureSsis#credential_name}.
        :param custom_setup_script: custom_setup_script block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#custom_setup_script DataFactoryIntegrationRuntimeAzureSsis#custom_setup_script}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#description DataFactoryIntegrationRuntimeAzureSsis#description}.
        :param edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#edition DataFactoryIntegrationRuntimeAzureSsis#edition}.
        :param express_custom_setup: express_custom_setup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#express_custom_setup DataFactoryIntegrationRuntimeAzureSsis#express_custom_setup}
        :param express_vnet_integration: express_vnet_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#express_vnet_integration DataFactoryIntegrationRuntimeAzureSsis#express_vnet_integration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#id DataFactoryIntegrationRuntimeAzureSsis#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#license_type DataFactoryIntegrationRuntimeAzureSsis#license_type}.
        :param max_parallel_executions_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#max_parallel_executions_per_node DataFactoryIntegrationRuntimeAzureSsis#max_parallel_executions_per_node}.
        :param number_of_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_nodes}.
        :param package_store: package_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#package_store DataFactoryIntegrationRuntimeAzureSsis#package_store}
        :param pipeline_external_compute_scale: pipeline_external_compute_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#pipeline_external_compute_scale DataFactoryIntegrationRuntimeAzureSsis#pipeline_external_compute_scale}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#proxy DataFactoryIntegrationRuntimeAzureSsis#proxy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#timeouts DataFactoryIntegrationRuntimeAzureSsis#timeouts}
        :param vnet_integration: vnet_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#vnet_integration DataFactoryIntegrationRuntimeAzureSsis#vnet_integration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfe2a3c8135d17d030e4678be10030795f75c48eb8e67953d9bbcf8297de57f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryIntegrationRuntimeAzureSsisConfig(
            data_factory_id=data_factory_id,
            location=location,
            name=name,
            node_size=node_size,
            catalog_info=catalog_info,
            copy_compute_scale=copy_compute_scale,
            credential_name=credential_name,
            custom_setup_script=custom_setup_script,
            description=description,
            edition=edition,
            express_custom_setup=express_custom_setup,
            express_vnet_integration=express_vnet_integration,
            id=id,
            license_type=license_type,
            max_parallel_executions_per_node=max_parallel_executions_per_node,
            number_of_nodes=number_of_nodes,
            package_store=package_store,
            pipeline_external_compute_scale=pipeline_external_compute_scale,
            proxy=proxy,
            timeouts=timeouts,
            vnet_integration=vnet_integration,
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
        '''Generates CDKTF code for importing a DataFactoryIntegrationRuntimeAzureSsis resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataFactoryIntegrationRuntimeAzureSsis to import.
        :param import_from_id: The id of the existing DataFactoryIntegrationRuntimeAzureSsis that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataFactoryIntegrationRuntimeAzureSsis to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039f901c16bb161afdf0240fcb7758782d7ea068fd5b4b396e3b309642a417c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatalogInfo")
    def put_catalog_info(
        self,
        *,
        server_endpoint: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        dual_standby_pair_name: typing.Optional[builtins.str] = None,
        elastic_pool_name: typing.Optional[builtins.str] = None,
        pricing_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#server_endpoint DataFactoryIntegrationRuntimeAzureSsis#server_endpoint}.
        :param administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#administrator_login DataFactoryIntegrationRuntimeAzureSsis#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#administrator_password DataFactoryIntegrationRuntimeAzureSsis#administrator_password}.
        :param dual_standby_pair_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#dual_standby_pair_name DataFactoryIntegrationRuntimeAzureSsis#dual_standby_pair_name}.
        :param elastic_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#elastic_pool_name DataFactoryIntegrationRuntimeAzureSsis#elastic_pool_name}.
        :param pricing_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#pricing_tier DataFactoryIntegrationRuntimeAzureSsis#pricing_tier}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisCatalogInfo(
            server_endpoint=server_endpoint,
            administrator_login=administrator_login,
            administrator_password=administrator_password,
            dual_standby_pair_name=dual_standby_pair_name,
            elastic_pool_name=elastic_pool_name,
            pricing_tier=pricing_tier,
        )

        return typing.cast(None, jsii.invoke(self, "putCatalogInfo", [value]))

    @jsii.member(jsii_name="putCopyComputeScale")
    def put_copy_compute_scale(
        self,
        *,
        data_integration_unit: typing.Optional[jsii.Number] = None,
        time_to_live: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param data_integration_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#data_integration_unit DataFactoryIntegrationRuntimeAzureSsis#data_integration_unit}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#time_to_live DataFactoryIntegrationRuntimeAzureSsis#time_to_live}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale(
            data_integration_unit=data_integration_unit, time_to_live=time_to_live
        )

        return typing.cast(None, jsii.invoke(self, "putCopyComputeScale", [value]))

    @jsii.member(jsii_name="putCustomSetupScript")
    def put_custom_setup_script(
        self,
        *,
        blob_container_uri: builtins.str,
        sas_token: builtins.str,
    ) -> None:
        '''
        :param blob_container_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#blob_container_uri DataFactoryIntegrationRuntimeAzureSsis#blob_container_uri}.
        :param sas_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#sas_token DataFactoryIntegrationRuntimeAzureSsis#sas_token}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript(
            blob_container_uri=blob_container_uri, sas_token=sas_token
        )

        return typing.cast(None, jsii.invoke(self, "putCustomSetupScript", [value]))

    @jsii.member(jsii_name="putExpressCustomSetup")
    def put_express_custom_setup(
        self,
        *,
        command_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        component: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        powershell_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param command_key: command_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#command_key DataFactoryIntegrationRuntimeAzureSsis#command_key}
        :param component: component block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#component DataFactoryIntegrationRuntimeAzureSsis#component}
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#environment DataFactoryIntegrationRuntimeAzureSsis#environment}.
        :param powershell_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#powershell_version DataFactoryIntegrationRuntimeAzureSsis#powershell_version}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup(
            command_key=command_key,
            component=component,
            environment=environment,
            powershell_version=powershell_version,
        )

        return typing.cast(None, jsii.invoke(self, "putExpressCustomSetup", [value]))

    @jsii.member(jsii_name="putExpressVnetIntegration")
    def put_express_vnet_integration(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_id DataFactoryIntegrationRuntimeAzureSsis#subnet_id}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration(
            subnet_id=subnet_id
        )

        return typing.cast(None, jsii.invoke(self, "putExpressVnetIntegration", [value]))

    @jsii.member(jsii_name="putPackageStore")
    def put_package_store(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisPackageStore", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6beb0a3569317ab29a21dd0d06687ee235fef513eff31b27e94c487a3915c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPackageStore", [value]))

    @jsii.member(jsii_name="putPipelineExternalComputeScale")
    def put_pipeline_external_compute_scale(
        self,
        *,
        number_of_external_nodes: typing.Optional[jsii.Number] = None,
        number_of_pipeline_nodes: typing.Optional[jsii.Number] = None,
        time_to_live: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param number_of_external_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_external_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_external_nodes}.
        :param number_of_pipeline_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_pipeline_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_pipeline_nodes}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#time_to_live DataFactoryIntegrationRuntimeAzureSsis#time_to_live}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale(
            number_of_external_nodes=number_of_external_nodes,
            number_of_pipeline_nodes=number_of_pipeline_nodes,
            time_to_live=time_to_live,
        )

        return typing.cast(None, jsii.invoke(self, "putPipelineExternalComputeScale", [value]))

    @jsii.member(jsii_name="putProxy")
    def put_proxy(
        self,
        *,
        self_hosted_integration_runtime_name: builtins.str,
        staging_storage_linked_service_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param self_hosted_integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#self_hosted_integration_runtime_name DataFactoryIntegrationRuntimeAzureSsis#self_hosted_integration_runtime_name}.
        :param staging_storage_linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#staging_storage_linked_service_name DataFactoryIntegrationRuntimeAzureSsis#staging_storage_linked_service_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#path DataFactoryIntegrationRuntimeAzureSsis#path}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisProxy(
            self_hosted_integration_runtime_name=self_hosted_integration_runtime_name,
            staging_storage_linked_service_name=staging_storage_linked_service_name,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#create DataFactoryIntegrationRuntimeAzureSsis#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#delete DataFactoryIntegrationRuntimeAzureSsis#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#read DataFactoryIntegrationRuntimeAzureSsis#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#update DataFactoryIntegrationRuntimeAzureSsis#update}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVnetIntegration")
    def put_vnet_integration(
        self,
        *,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        subnet_name: typing.Optional[builtins.str] = None,
        vnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#public_ips DataFactoryIntegrationRuntimeAzureSsis#public_ips}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_id DataFactoryIntegrationRuntimeAzureSsis#subnet_id}.
        :param subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_name DataFactoryIntegrationRuntimeAzureSsis#subnet_name}.
        :param vnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#vnet_id DataFactoryIntegrationRuntimeAzureSsis#vnet_id}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisVnetIntegration(
            public_ips=public_ips,
            subnet_id=subnet_id,
            subnet_name=subnet_name,
            vnet_id=vnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putVnetIntegration", [value]))

    @jsii.member(jsii_name="resetCatalogInfo")
    def reset_catalog_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogInfo", []))

    @jsii.member(jsii_name="resetCopyComputeScale")
    def reset_copy_compute_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyComputeScale", []))

    @jsii.member(jsii_name="resetCredentialName")
    def reset_credential_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialName", []))

    @jsii.member(jsii_name="resetCustomSetupScript")
    def reset_custom_setup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSetupScript", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetExpressCustomSetup")
    def reset_express_custom_setup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressCustomSetup", []))

    @jsii.member(jsii_name="resetExpressVnetIntegration")
    def reset_express_vnet_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpressVnetIntegration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

    @jsii.member(jsii_name="resetMaxParallelExecutionsPerNode")
    def reset_max_parallel_executions_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxParallelExecutionsPerNode", []))

    @jsii.member(jsii_name="resetNumberOfNodes")
    def reset_number_of_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfNodes", []))

    @jsii.member(jsii_name="resetPackageStore")
    def reset_package_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageStore", []))

    @jsii.member(jsii_name="resetPipelineExternalComputeScale")
    def reset_pipeline_external_compute_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineExternalComputeScale", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVnetIntegration")
    def reset_vnet_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetIntegration", []))

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
    @jsii.member(jsii_name="catalogInfo")
    def catalog_info(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisCatalogInfoOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisCatalogInfoOutputReference", jsii.get(self, "catalogInfo"))

    @builtins.property
    @jsii.member(jsii_name="copyComputeScale")
    def copy_compute_scale(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisCopyComputeScaleOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisCopyComputeScaleOutputReference", jsii.get(self, "copyComputeScale"))

    @builtins.property
    @jsii.member(jsii_name="customSetupScript")
    def custom_setup_script(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisCustomSetupScriptOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisCustomSetupScriptOutputReference", jsii.get(self, "customSetupScript"))

    @builtins.property
    @jsii.member(jsii_name="expressCustomSetup")
    def express_custom_setup(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupOutputReference", jsii.get(self, "expressCustomSetup"))

    @builtins.property
    @jsii.member(jsii_name="expressVnetIntegration")
    def express_vnet_integration(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegrationOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegrationOutputReference", jsii.get(self, "expressVnetIntegration"))

    @builtins.property
    @jsii.member(jsii_name="packageStore")
    def package_store(self) -> "DataFactoryIntegrationRuntimeAzureSsisPackageStoreList":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisPackageStoreList", jsii.get(self, "packageStore"))

    @builtins.property
    @jsii.member(jsii_name="pipelineExternalComputeScale")
    def pipeline_external_compute_scale(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScaleOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScaleOutputReference", jsii.get(self, "pipelineExternalComputeScale"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "DataFactoryIntegrationRuntimeAzureSsisProxyOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisTimeoutsOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vnetIntegration")
    def vnet_integration(
        self,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisVnetIntegrationOutputReference":
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisVnetIntegrationOutputReference", jsii.get(self, "vnetIntegration"))

    @builtins.property
    @jsii.member(jsii_name="catalogInfoInput")
    def catalog_info_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCatalogInfo"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCatalogInfo"], jsii.get(self, "catalogInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="copyComputeScaleInput")
    def copy_compute_scale_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale"], jsii.get(self, "copyComputeScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialNameInput")
    def credential_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customSetupScriptInput")
    def custom_setup_script_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript"], jsii.get(self, "customSetupScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="expressCustomSetupInput")
    def express_custom_setup_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup"], jsii.get(self, "expressCustomSetupInput"))

    @builtins.property
    @jsii.member(jsii_name="expressVnetIntegrationInput")
    def express_vnet_integration_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration"], jsii.get(self, "expressVnetIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxParallelExecutionsPerNodeInput")
    def max_parallel_executions_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxParallelExecutionsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSizeInput")
    def node_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfNodesInput")
    def number_of_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="packageStoreInput")
    def package_store_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisPackageStore"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisPackageStore"]]], jsii.get(self, "packageStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineExternalComputeScaleInput")
    def pipeline_external_compute_scale_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale"], jsii.get(self, "pipelineExternalComputeScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisProxy"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryIntegrationRuntimeAzureSsisTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryIntegrationRuntimeAzureSsisTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetIntegrationInput")
    def vnet_integration_input(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisVnetIntegration"]:
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisVnetIntegration"], jsii.get(self, "vnetIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialName")
    def credential_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentialName"))

    @credential_name.setter
    def credential_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873aae074e38afa85f1235702c2e79d2a64a05fa7ed30725bd360329317fef3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentialName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7327cfe2858da0b0b0e0609efe5bca42aa94b47218f13eae4bdcdf880e090b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e822a80e799145c16caafbfb4c93e1144c51ed3e7a7cdfd06ebddb4c36c91a7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e754ec4936c5f35847e747f22176721acc7598cec1ad18ac66cd820b08b5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63199168f5155ffb0fa2800699156ef5c5a9fed0c7205e1e6ed54a5c6c45abef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b606fab38d412011aa6913559d2c8595d508353a17fecd48c7edd53206203988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02bd010576164a86f8368ee12aa5e1e37733d0ad56a97bc8061bd25eb250a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxParallelExecutionsPerNode")
    def max_parallel_executions_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxParallelExecutionsPerNode"))

    @max_parallel_executions_per_node.setter
    def max_parallel_executions_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53162c7448a1c9bd5f0742050f51594825094c91ce53fd05e0f3b379c8bde3d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxParallelExecutionsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d150e6ab9f1df5a29cfd94790a35a5344db5df78c1d493de6a765f5b8d79c140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeSize")
    def node_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeSize"))

    @node_size.setter
    def node_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0db99bc9389fff086378ee9f76df50ccef1c5477176b265270878f347dd7e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numberOfNodes")
    def number_of_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfNodes"))

    @number_of_nodes.setter
    def number_of_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c6b940ab25c5d02a85f3bb3a48e44f7f52586101c3c911df6cab1db37dfc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfNodes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisCatalogInfo",
    jsii_struct_bases=[],
    name_mapping={
        "server_endpoint": "serverEndpoint",
        "administrator_login": "administratorLogin",
        "administrator_password": "administratorPassword",
        "dual_standby_pair_name": "dualStandbyPairName",
        "elastic_pool_name": "elasticPoolName",
        "pricing_tier": "pricingTier",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisCatalogInfo:
    def __init__(
        self,
        *,
        server_endpoint: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        dual_standby_pair_name: typing.Optional[builtins.str] = None,
        elastic_pool_name: typing.Optional[builtins.str] = None,
        pricing_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#server_endpoint DataFactoryIntegrationRuntimeAzureSsis#server_endpoint}.
        :param administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#administrator_login DataFactoryIntegrationRuntimeAzureSsis#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#administrator_password DataFactoryIntegrationRuntimeAzureSsis#administrator_password}.
        :param dual_standby_pair_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#dual_standby_pair_name DataFactoryIntegrationRuntimeAzureSsis#dual_standby_pair_name}.
        :param elastic_pool_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#elastic_pool_name DataFactoryIntegrationRuntimeAzureSsis#elastic_pool_name}.
        :param pricing_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#pricing_tier DataFactoryIntegrationRuntimeAzureSsis#pricing_tier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415af22b6beda4a326662882de3279ae1df1a6196d0080b1e9dd15b0ded1567a)
            check_type(argname="argument server_endpoint", value=server_endpoint, expected_type=type_hints["server_endpoint"])
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_password", value=administrator_password, expected_type=type_hints["administrator_password"])
            check_type(argname="argument dual_standby_pair_name", value=dual_standby_pair_name, expected_type=type_hints["dual_standby_pair_name"])
            check_type(argname="argument elastic_pool_name", value=elastic_pool_name, expected_type=type_hints["elastic_pool_name"])
            check_type(argname="argument pricing_tier", value=pricing_tier, expected_type=type_hints["pricing_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_endpoint": server_endpoint,
        }
        if administrator_login is not None:
            self._values["administrator_login"] = administrator_login
        if administrator_password is not None:
            self._values["administrator_password"] = administrator_password
        if dual_standby_pair_name is not None:
            self._values["dual_standby_pair_name"] = dual_standby_pair_name
        if elastic_pool_name is not None:
            self._values["elastic_pool_name"] = elastic_pool_name
        if pricing_tier is not None:
            self._values["pricing_tier"] = pricing_tier

    @builtins.property
    def server_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#server_endpoint DataFactoryIntegrationRuntimeAzureSsis#server_endpoint}.'''
        result = self._values.get("server_endpoint")
        assert result is not None, "Required property 'server_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#administrator_login DataFactoryIntegrationRuntimeAzureSsis#administrator_login}.'''
        result = self._values.get("administrator_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#administrator_password DataFactoryIntegrationRuntimeAzureSsis#administrator_password}.'''
        result = self._values.get("administrator_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dual_standby_pair_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#dual_standby_pair_name DataFactoryIntegrationRuntimeAzureSsis#dual_standby_pair_name}.'''
        result = self._values.get("dual_standby_pair_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#elastic_pool_name DataFactoryIntegrationRuntimeAzureSsis#elastic_pool_name}.'''
        result = self._values.get("elastic_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#pricing_tier DataFactoryIntegrationRuntimeAzureSsis#pricing_tier}.'''
        result = self._values.get("pricing_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisCatalogInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisCatalogInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisCatalogInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ed30f7929cb2ea01e7048e64fff11a7c4a99999395a56b9dda24f33bbfb8806)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdministratorLogin")
    def reset_administrator_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLogin", []))

    @jsii.member(jsii_name="resetAdministratorPassword")
    def reset_administrator_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorPassword", []))

    @jsii.member(jsii_name="resetDualStandbyPairName")
    def reset_dual_standby_pair_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDualStandbyPairName", []))

    @jsii.member(jsii_name="resetElasticPoolName")
    def reset_elastic_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticPoolName", []))

    @jsii.member(jsii_name="resetPricingTier")
    def reset_pricing_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPricingTier", []))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordInput")
    def administrator_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="dualStandbyPairNameInput")
    def dual_standby_pair_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dualStandbyPairNameInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticPoolNameInput")
    def elastic_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pricingTierInput")
    def pricing_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingTierInput"))

    @builtins.property
    @jsii.member(jsii_name="serverEndpointInput")
    def server_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0e52c886b9b92aba05db880548d1025482112f490b00507bc719b64f5133ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administratorPassword")
    def administrator_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorPassword"))

    @administrator_password.setter
    def administrator_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c714ae514555d0eb3f9f440776b1e07b61e8626e412d8eb3d7dccbf30c17262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dualStandbyPairName")
    def dual_standby_pair_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dualStandbyPairName"))

    @dual_standby_pair_name.setter
    def dual_standby_pair_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9744c9497264f6dcdd3ad8d8e00d5eae31c7291a6a80965f94c0c91cdcc8675e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dualStandbyPairName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticPoolName")
    def elastic_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticPoolName"))

    @elastic_pool_name.setter
    def elastic_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adcc99f7d96af28880fd1d3e35bf567c754cbccc671190d59a1875029b9b33c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticPoolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pricingTier")
    def pricing_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pricingTier"))

    @pricing_tier.setter
    def pricing_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba280c23a17bf03401df22b200a79bf97c00ec4192dbf9706cf913491de5e3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverEndpoint")
    def server_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverEndpoint"))

    @server_endpoint.setter
    def server_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2dae68fc5a17b267530ebf093c61bd7df176843ace7286739c6d89a22684bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fea809f98b0432b59302da4296f4db0e7069f6738a43af3cfebd028e1ab47a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_factory_id": "dataFactoryId",
        "location": "location",
        "name": "name",
        "node_size": "nodeSize",
        "catalog_info": "catalogInfo",
        "copy_compute_scale": "copyComputeScale",
        "credential_name": "credentialName",
        "custom_setup_script": "customSetupScript",
        "description": "description",
        "edition": "edition",
        "express_custom_setup": "expressCustomSetup",
        "express_vnet_integration": "expressVnetIntegration",
        "id": "id",
        "license_type": "licenseType",
        "max_parallel_executions_per_node": "maxParallelExecutionsPerNode",
        "number_of_nodes": "numberOfNodes",
        "package_store": "packageStore",
        "pipeline_external_compute_scale": "pipelineExternalComputeScale",
        "proxy": "proxy",
        "timeouts": "timeouts",
        "vnet_integration": "vnetIntegration",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        data_factory_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        node_size: builtins.str,
        catalog_info: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        copy_compute_scale: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale", typing.Dict[builtins.str, typing.Any]]] = None,
        credential_name: typing.Optional[builtins.str] = None,
        custom_setup_script: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        express_custom_setup: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup", typing.Dict[builtins.str, typing.Any]]] = None,
        express_vnet_integration: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        license_type: typing.Optional[builtins.str] = None,
        max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        package_store: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisPackageStore", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pipeline_external_compute_scale: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vnet_integration: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisVnetIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#data_factory_id DataFactoryIntegrationRuntimeAzureSsis#data_factory_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#location DataFactoryIntegrationRuntimeAzureSsis#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.
        :param node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#node_size DataFactoryIntegrationRuntimeAzureSsis#node_size}.
        :param catalog_info: catalog_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#catalog_info DataFactoryIntegrationRuntimeAzureSsis#catalog_info}
        :param copy_compute_scale: copy_compute_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#copy_compute_scale DataFactoryIntegrationRuntimeAzureSsis#copy_compute_scale}
        :param credential_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#credential_name DataFactoryIntegrationRuntimeAzureSsis#credential_name}.
        :param custom_setup_script: custom_setup_script block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#custom_setup_script DataFactoryIntegrationRuntimeAzureSsis#custom_setup_script}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#description DataFactoryIntegrationRuntimeAzureSsis#description}.
        :param edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#edition DataFactoryIntegrationRuntimeAzureSsis#edition}.
        :param express_custom_setup: express_custom_setup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#express_custom_setup DataFactoryIntegrationRuntimeAzureSsis#express_custom_setup}
        :param express_vnet_integration: express_vnet_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#express_vnet_integration DataFactoryIntegrationRuntimeAzureSsis#express_vnet_integration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#id DataFactoryIntegrationRuntimeAzureSsis#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#license_type DataFactoryIntegrationRuntimeAzureSsis#license_type}.
        :param max_parallel_executions_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#max_parallel_executions_per_node DataFactoryIntegrationRuntimeAzureSsis#max_parallel_executions_per_node}.
        :param number_of_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_nodes}.
        :param package_store: package_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#package_store DataFactoryIntegrationRuntimeAzureSsis#package_store}
        :param pipeline_external_compute_scale: pipeline_external_compute_scale block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#pipeline_external_compute_scale DataFactoryIntegrationRuntimeAzureSsis#pipeline_external_compute_scale}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#proxy DataFactoryIntegrationRuntimeAzureSsis#proxy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#timeouts DataFactoryIntegrationRuntimeAzureSsis#timeouts}
        :param vnet_integration: vnet_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#vnet_integration DataFactoryIntegrationRuntimeAzureSsis#vnet_integration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(catalog_info, dict):
            catalog_info = DataFactoryIntegrationRuntimeAzureSsisCatalogInfo(**catalog_info)
        if isinstance(copy_compute_scale, dict):
            copy_compute_scale = DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale(**copy_compute_scale)
        if isinstance(custom_setup_script, dict):
            custom_setup_script = DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript(**custom_setup_script)
        if isinstance(express_custom_setup, dict):
            express_custom_setup = DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup(**express_custom_setup)
        if isinstance(express_vnet_integration, dict):
            express_vnet_integration = DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration(**express_vnet_integration)
        if isinstance(pipeline_external_compute_scale, dict):
            pipeline_external_compute_scale = DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale(**pipeline_external_compute_scale)
        if isinstance(proxy, dict):
            proxy = DataFactoryIntegrationRuntimeAzureSsisProxy(**proxy)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryIntegrationRuntimeAzureSsisTimeouts(**timeouts)
        if isinstance(vnet_integration, dict):
            vnet_integration = DataFactoryIntegrationRuntimeAzureSsisVnetIntegration(**vnet_integration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03a6d353e67e9325a1d8e6c4a81f84911a50ee8b2293b7ae487947c38e68acb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_size", value=node_size, expected_type=type_hints["node_size"])
            check_type(argname="argument catalog_info", value=catalog_info, expected_type=type_hints["catalog_info"])
            check_type(argname="argument copy_compute_scale", value=copy_compute_scale, expected_type=type_hints["copy_compute_scale"])
            check_type(argname="argument credential_name", value=credential_name, expected_type=type_hints["credential_name"])
            check_type(argname="argument custom_setup_script", value=custom_setup_script, expected_type=type_hints["custom_setup_script"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument express_custom_setup", value=express_custom_setup, expected_type=type_hints["express_custom_setup"])
            check_type(argname="argument express_vnet_integration", value=express_vnet_integration, expected_type=type_hints["express_vnet_integration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument max_parallel_executions_per_node", value=max_parallel_executions_per_node, expected_type=type_hints["max_parallel_executions_per_node"])
            check_type(argname="argument number_of_nodes", value=number_of_nodes, expected_type=type_hints["number_of_nodes"])
            check_type(argname="argument package_store", value=package_store, expected_type=type_hints["package_store"])
            check_type(argname="argument pipeline_external_compute_scale", value=pipeline_external_compute_scale, expected_type=type_hints["pipeline_external_compute_scale"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vnet_integration", value=vnet_integration, expected_type=type_hints["vnet_integration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_factory_id": data_factory_id,
            "location": location,
            "name": name,
            "node_size": node_size,
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
        if catalog_info is not None:
            self._values["catalog_info"] = catalog_info
        if copy_compute_scale is not None:
            self._values["copy_compute_scale"] = copy_compute_scale
        if credential_name is not None:
            self._values["credential_name"] = credential_name
        if custom_setup_script is not None:
            self._values["custom_setup_script"] = custom_setup_script
        if description is not None:
            self._values["description"] = description
        if edition is not None:
            self._values["edition"] = edition
        if express_custom_setup is not None:
            self._values["express_custom_setup"] = express_custom_setup
        if express_vnet_integration is not None:
            self._values["express_vnet_integration"] = express_vnet_integration
        if id is not None:
            self._values["id"] = id
        if license_type is not None:
            self._values["license_type"] = license_type
        if max_parallel_executions_per_node is not None:
            self._values["max_parallel_executions_per_node"] = max_parallel_executions_per_node
        if number_of_nodes is not None:
            self._values["number_of_nodes"] = number_of_nodes
        if package_store is not None:
            self._values["package_store"] = package_store
        if pipeline_external_compute_scale is not None:
            self._values["pipeline_external_compute_scale"] = pipeline_external_compute_scale
        if proxy is not None:
            self._values["proxy"] = proxy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vnet_integration is not None:
            self._values["vnet_integration"] = vnet_integration

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
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#data_factory_id DataFactoryIntegrationRuntimeAzureSsis#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#location DataFactoryIntegrationRuntimeAzureSsis#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#node_size DataFactoryIntegrationRuntimeAzureSsis#node_size}.'''
        result = self._values.get("node_size")
        assert result is not None, "Required property 'node_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog_info(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo]:
        '''catalog_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#catalog_info DataFactoryIntegrationRuntimeAzureSsis#catalog_info}
        '''
        result = self._values.get("catalog_info")
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo], result)

    @builtins.property
    def copy_compute_scale(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale"]:
        '''copy_compute_scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#copy_compute_scale DataFactoryIntegrationRuntimeAzureSsis#copy_compute_scale}
        '''
        result = self._values.get("copy_compute_scale")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale"], result)

    @builtins.property
    def credential_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#credential_name DataFactoryIntegrationRuntimeAzureSsis#credential_name}.'''
        result = self._values.get("credential_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_setup_script(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript"]:
        '''custom_setup_script block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#custom_setup_script DataFactoryIntegrationRuntimeAzureSsis#custom_setup_script}
        '''
        result = self._values.get("custom_setup_script")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#description DataFactoryIntegrationRuntimeAzureSsis#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#edition DataFactoryIntegrationRuntimeAzureSsis#edition}.'''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def express_custom_setup(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup"]:
        '''express_custom_setup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#express_custom_setup DataFactoryIntegrationRuntimeAzureSsis#express_custom_setup}
        '''
        result = self._values.get("express_custom_setup")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup"], result)

    @builtins.property
    def express_vnet_integration(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration"]:
        '''express_vnet_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#express_vnet_integration DataFactoryIntegrationRuntimeAzureSsis#express_vnet_integration}
        '''
        result = self._values.get("express_vnet_integration")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#id DataFactoryIntegrationRuntimeAzureSsis#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#license_type DataFactoryIntegrationRuntimeAzureSsis#license_type}.'''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_parallel_executions_per_node(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#max_parallel_executions_per_node DataFactoryIntegrationRuntimeAzureSsis#max_parallel_executions_per_node}.'''
        result = self._values.get("max_parallel_executions_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_nodes}.'''
        result = self._values.get("number_of_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def package_store(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisPackageStore"]]]:
        '''package_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#package_store DataFactoryIntegrationRuntimeAzureSsis#package_store}
        '''
        result = self._values.get("package_store")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisPackageStore"]]], result)

    @builtins.property
    def pipeline_external_compute_scale(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale"]:
        '''pipeline_external_compute_scale block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#pipeline_external_compute_scale DataFactoryIntegrationRuntimeAzureSsis#pipeline_external_compute_scale}
        '''
        result = self._values.get("pipeline_external_compute_scale")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale"], result)

    @builtins.property
    def proxy(self) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#proxy DataFactoryIntegrationRuntimeAzureSsis#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisProxy"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#timeouts DataFactoryIntegrationRuntimeAzureSsis#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisTimeouts"], result)

    @builtins.property
    def vnet_integration(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisVnetIntegration"]:
        '''vnet_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#vnet_integration DataFactoryIntegrationRuntimeAzureSsis#vnet_integration}
        '''
        result = self._values.get("vnet_integration")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisVnetIntegration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale",
    jsii_struct_bases=[],
    name_mapping={
        "data_integration_unit": "dataIntegrationUnit",
        "time_to_live": "timeToLive",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale:
    def __init__(
        self,
        *,
        data_integration_unit: typing.Optional[jsii.Number] = None,
        time_to_live: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param data_integration_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#data_integration_unit DataFactoryIntegrationRuntimeAzureSsis#data_integration_unit}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#time_to_live DataFactoryIntegrationRuntimeAzureSsis#time_to_live}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9783dd29a6ae21ac27409b05eb202127ba0831208ce1051606c84c06ae06e177)
            check_type(argname="argument data_integration_unit", value=data_integration_unit, expected_type=type_hints["data_integration_unit"])
            check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_integration_unit is not None:
            self._values["data_integration_unit"] = data_integration_unit
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live

    @builtins.property
    def data_integration_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#data_integration_unit DataFactoryIntegrationRuntimeAzureSsis#data_integration_unit}.'''
        result = self._values.get("data_integration_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_to_live(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#time_to_live DataFactoryIntegrationRuntimeAzureSsis#time_to_live}.'''
        result = self._values.get("time_to_live")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisCopyComputeScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisCopyComputeScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a9b6c282ece13b2507bd26df8a1aa21b7c369dc4306bf594072772b536cb6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataIntegrationUnit")
    def reset_data_integration_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataIntegrationUnit", []))

    @jsii.member(jsii_name="resetTimeToLive")
    def reset_time_to_live(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeToLive", []))

    @builtins.property
    @jsii.member(jsii_name="dataIntegrationUnitInput")
    def data_integration_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataIntegrationUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="timeToLiveInput")
    def time_to_live_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="dataIntegrationUnit")
    def data_integration_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataIntegrationUnit"))

    @data_integration_unit.setter
    def data_integration_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acac2c465a3ccafacd32ff4cabf83efb395e0a367ee3520faea018b0b571da03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataIntegrationUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeToLive")
    def time_to_live(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeToLive"))

    @time_to_live.setter
    def time_to_live(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6334b525e7740cc6bfbf5edc251eeb540ed5a799e95cfdd84613baeef2e583bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105aec8d5871ee4f550e22eb38ae5a32aa47fb0eb3ff501bc3db6fff976ae25f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript",
    jsii_struct_bases=[],
    name_mapping={"blob_container_uri": "blobContainerUri", "sas_token": "sasToken"},
)
class DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript:
    def __init__(
        self,
        *,
        blob_container_uri: builtins.str,
        sas_token: builtins.str,
    ) -> None:
        '''
        :param blob_container_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#blob_container_uri DataFactoryIntegrationRuntimeAzureSsis#blob_container_uri}.
        :param sas_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#sas_token DataFactoryIntegrationRuntimeAzureSsis#sas_token}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8155cdd3121fba27f5cf3c06f802198812e72af2c1e25e78a72a17782daf27)
            check_type(argname="argument blob_container_uri", value=blob_container_uri, expected_type=type_hints["blob_container_uri"])
            check_type(argname="argument sas_token", value=sas_token, expected_type=type_hints["sas_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blob_container_uri": blob_container_uri,
            "sas_token": sas_token,
        }

    @builtins.property
    def blob_container_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#blob_container_uri DataFactoryIntegrationRuntimeAzureSsis#blob_container_uri}.'''
        result = self._values.get("blob_container_uri")
        assert result is not None, "Required property 'blob_container_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sas_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#sas_token DataFactoryIntegrationRuntimeAzureSsis#sas_token}.'''
        result = self._values.get("sas_token")
        assert result is not None, "Required property 'sas_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisCustomSetupScriptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisCustomSetupScriptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa38c9da196cb83a0b5add35e517d0fba4990233844d3ce2ad0899d679c94145)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="blobContainerUriInput")
    def blob_container_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blobContainerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="sasTokenInput")
    def sas_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sasTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="blobContainerUri")
    def blob_container_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blobContainerUri"))

    @blob_container_uri.setter
    def blob_container_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54861b90ec246019300f9057a21da5502604cbc89c0ce2be37783a0547d3017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobContainerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sasToken")
    def sas_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sasToken"))

    @sas_token.setter
    def sas_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d9e440b855fac79f5d17d8624cd3c4f307c9ed58b743dd8be78dd0f18b95e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sasToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f827a08ddf428aee8430b82faf552daa4aae4893b260cbb6e0bdc68c2680af75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup",
    jsii_struct_bases=[],
    name_mapping={
        "command_key": "commandKey",
        "component": "component",
        "environment": "environment",
        "powershell_version": "powershellVersion",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup:
    def __init__(
        self,
        *,
        command_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        component: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent", typing.Dict[builtins.str, typing.Any]]]]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        powershell_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param command_key: command_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#command_key DataFactoryIntegrationRuntimeAzureSsis#command_key}
        :param component: component block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#component DataFactoryIntegrationRuntimeAzureSsis#component}
        :param environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#environment DataFactoryIntegrationRuntimeAzureSsis#environment}.
        :param powershell_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#powershell_version DataFactoryIntegrationRuntimeAzureSsis#powershell_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe486633d72da84961b28616efa02ba4a446cae59dde95f47a996ab3a73774c)
            check_type(argname="argument command_key", value=command_key, expected_type=type_hints["command_key"])
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument powershell_version", value=powershell_version, expected_type=type_hints["powershell_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command_key is not None:
            self._values["command_key"] = command_key
        if component is not None:
            self._values["component"] = component
        if environment is not None:
            self._values["environment"] = environment
        if powershell_version is not None:
            self._values["powershell_version"] = powershell_version

    @builtins.property
    def command_key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey"]]]:
        '''command_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#command_key DataFactoryIntegrationRuntimeAzureSsis#command_key}
        '''
        result = self._values.get("command_key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey"]]], result)

    @builtins.property
    def component(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent"]]]:
        '''component block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#component DataFactoryIntegrationRuntimeAzureSsis#component}
        '''
        result = self._values.get("component")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent"]]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#environment DataFactoryIntegrationRuntimeAzureSsis#environment}.'''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def powershell_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#powershell_version DataFactoryIntegrationRuntimeAzureSsis#powershell_version}.'''
        result = self._values.get("powershell_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey",
    jsii_struct_bases=[],
    name_mapping={
        "target_name": "targetName",
        "user_name": "userName",
        "key_vault_password": "keyVaultPassword",
        "password": "password",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey:
    def __init__(
        self,
        *,
        target_name: builtins.str,
        user_name: builtins.str,
        key_vault_password: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#target_name DataFactoryIntegrationRuntimeAzureSsis#target_name}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#user_name DataFactoryIntegrationRuntimeAzureSsis#user_name}.
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#key_vault_password DataFactoryIntegrationRuntimeAzureSsis#key_vault_password}
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#password DataFactoryIntegrationRuntimeAzureSsis#password}.
        '''
        if isinstance(key_vault_password, dict):
            key_vault_password = DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword(**key_vault_password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315e9bac1c9ffd9b26cde49f70ba205270f2d0d2340308a1779f23ab3128018f)
            check_type(argname="argument target_name", value=target_name, expected_type=type_hints["target_name"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument key_vault_password", value=key_vault_password, expected_type=type_hints["key_vault_password"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_name": target_name,
            "user_name": user_name,
        }
        if key_vault_password is not None:
            self._values["key_vault_password"] = key_vault_password
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def target_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#target_name DataFactoryIntegrationRuntimeAzureSsis#target_name}.'''
        result = self._values.get("target_name")
        assert result is not None, "Required property 'target_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#user_name DataFactoryIntegrationRuntimeAzureSsis#user_name}.'''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_vault_password(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword"]:
        '''key_vault_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#key_vault_password DataFactoryIntegrationRuntimeAzureSsis#key_vault_password}
        '''
        result = self._values.get("key_vault_password")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword"], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#password DataFactoryIntegrationRuntimeAzureSsis#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
        "parameters": "parameters",
        "secret_version": "secretVersion",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_name DataFactoryIntegrationRuntimeAzureSsis#secret_name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#parameters DataFactoryIntegrationRuntimeAzureSsis#parameters}.
        :param secret_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_version DataFactoryIntegrationRuntimeAzureSsis#secret_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc43cf4277dba81a7ba712aa3933bba8e2bb4975c3e22aaf4db007f76a91e7f)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters
        if secret_version is not None:
            self._values["secret_version"] = secret_version

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_name DataFactoryIntegrationRuntimeAzureSsis#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#parameters DataFactoryIntegrationRuntimeAzureSsis#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def secret_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_version DataFactoryIntegrationRuntimeAzureSsis#secret_version}.'''
        result = self._values.get("secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0e1fa956d279286b443bb85e4c6ba3cab86c4eb7a298dca947136802ecd757a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetSecretVersion")
    def reset_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersion", []))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce8fd2d0cb1d924d648c5c8f0e6f713175a093c62a44e2bf0229af456013736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64bb50ca17071593e92b23ea0a4888933a00bb09777e1928494ea1cd1224c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4278fe702ec0c12982b4788dddce100bacb58295b3667f0be98f4ef279d39d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ae1c75a5eac51549e2948152b72d63fda31368b5fed3a429a6e835f86abde4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c63ebda029f73f13aa983d80387fc819ef1fccb21bf52d59ee44819c3acb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c4ef578085dace573e321252eec4cd4fdf00d0595813db4a85c45c7ed60b5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9335af1c6e8b74daec56c9b7061b961382063d4a67a5be2b5818cedf51e86220)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f83851f4e66bd8353a8124a5893852e1089cdf90d94965df5a547e1dec08bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e5f557b7768c4a461ef4c042e6bb754ed1dab39b974d73b37bb1ec9469eb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce9a172e8999439116a064735dd8d3c9fff1d4190e1c25df822890a89a41d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1899b095fedb09f61208c1a634516b91996b107045f607761a7643ecc6f73d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4acc8b275f23f32921e1579e3d1f5424f9c9cb29b397d1b407467243211b278e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKeyVaultPassword")
    def put_key_vault_password(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_name DataFactoryIntegrationRuntimeAzureSsis#secret_name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#parameters DataFactoryIntegrationRuntimeAzureSsis#parameters}.
        :param secret_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_version DataFactoryIntegrationRuntimeAzureSsis#secret_version}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword(
            linked_service_name=linked_service_name,
            secret_name=secret_name,
            parameters=parameters,
            secret_version=secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultPassword", [value]))

    @jsii.member(jsii_name="resetKeyVaultPassword")
    def reset_key_vault_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPassword", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPassword")
    def key_vault_password(
        self,
    ) -> DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPasswordOutputReference:
        return typing.cast(DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPasswordOutputReference, jsii.get(self, "keyVaultPassword"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPasswordInput")
    def key_vault_password_input(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword], jsii.get(self, "keyVaultPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="targetNameInput")
    def target_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e956496cce106df5418cbbaee9ec06449fef5855a60939987c6d4ce56f1bc422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetName")
    def target_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetName"))

    @target_name.setter
    def target_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d65f262549649320897ad701406993266934c2e1139a37dd5672d1a70d3a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094056248ebb8302ee6e3cf790e9f72b063d3e0b8cd302d7c4d94ef09135030d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86db7c48ec2d4609b80ccaadf6a83087bba4893882a4431d4c4ce3f4716a519d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "key_vault_license": "keyVaultLicense",
        "license": "license",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent:
    def __init__(
        self,
        *,
        name: builtins.str,
        key_vault_license: typing.Optional[typing.Union["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense", typing.Dict[builtins.str, typing.Any]]] = None,
        license: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.
        :param key_vault_license: key_vault_license block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#key_vault_license DataFactoryIntegrationRuntimeAzureSsis#key_vault_license}
        :param license: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#license DataFactoryIntegrationRuntimeAzureSsis#license}.
        '''
        if isinstance(key_vault_license, dict):
            key_vault_license = DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense(**key_vault_license)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef02fa91f45d3e92eafd37e5f1d7e0944e7bb202afa233efd7dc083d5c7ee0be)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument key_vault_license", value=key_vault_license, expected_type=type_hints["key_vault_license"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if key_vault_license is not None:
            self._values["key_vault_license"] = key_vault_license
        if license is not None:
            self._values["license"] = license

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_vault_license(
        self,
    ) -> typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense"]:
        '''key_vault_license block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#key_vault_license DataFactoryIntegrationRuntimeAzureSsis#key_vault_license}
        '''
        result = self._values.get("key_vault_license")
        return typing.cast(typing.Optional["DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense"], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#license DataFactoryIntegrationRuntimeAzureSsis#license}.'''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
        "parameters": "parameters",
        "secret_version": "secretVersion",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_name DataFactoryIntegrationRuntimeAzureSsis#secret_name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#parameters DataFactoryIntegrationRuntimeAzureSsis#parameters}.
        :param secret_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_version DataFactoryIntegrationRuntimeAzureSsis#secret_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82825e978c43f80dc95d1cdce0fa76ba5354fe51c4d2e424df849b65154f922f)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters
        if secret_version is not None:
            self._values["secret_version"] = secret_version

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_name DataFactoryIntegrationRuntimeAzureSsis#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#parameters DataFactoryIntegrationRuntimeAzureSsis#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def secret_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_version DataFactoryIntegrationRuntimeAzureSsis#secret_version}.'''
        result = self._values.get("secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicenseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicenseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca48acfe600d36866c611e0e52b354511f9da51cfc555631979cb7efc11c0656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetSecretVersion")
    def reset_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersion", []))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bc3d180c191e599294f57e0c0c2b28e154de01193f6ca5b76bea2a1743cc04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79eeb4679c32e02cdca57584db40ed4027f80a86661eadc334dc03bfd10b6dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e66c6b2f5e9be16b5ae0dfdc929fa0c7cbc4c77411e0a3e8c88bdff54429644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551a6511c42e7eba729fdae3693ddf1790d5a2314ebb0472d97c754e5c210608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec13fe2cf9e1fc7d4ee0689bc226c691a21ccc0207e559a31322d104136915e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7797527d547f23846370556ced3804b3c5bdcf7769cab187876e481068c651)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0d3bd68f0b0a9835d79aaff5c01092a2ea2884e5b55feaa3ecb114ab8f5fe5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570c5a0b1f98662ee887ae92e2de6c0cfebbda89d2482f9d2e8582fd8540db7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5373dfffe03001b82fdffceeb3e18a355a11b29b83ab267109b0084409af7e7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34750c83d01bc4086b7823fe3aed97d14b40f779d26ed366d76d91a0be44e3f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8508171ddfe8171efbfbe1648c566b98f1f2b3188dda7c1d16f6b283be02db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d86b8548393ca75d92db77d47f10e71e183dd8bf9ced061d7101eaaea1f443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKeyVaultLicense")
    def put_key_vault_license(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        secret_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_name DataFactoryIntegrationRuntimeAzureSsis#secret_name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#parameters DataFactoryIntegrationRuntimeAzureSsis#parameters}.
        :param secret_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#secret_version DataFactoryIntegrationRuntimeAzureSsis#secret_version}.
        '''
        value = DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense(
            linked_service_name=linked_service_name,
            secret_name=secret_name,
            parameters=parameters,
            secret_version=secret_version,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultLicense", [value]))

    @jsii.member(jsii_name="resetKeyVaultLicense")
    def reset_key_vault_license(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultLicense", []))

    @jsii.member(jsii_name="resetLicense")
    def reset_license(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicense", []))

    @builtins.property
    @jsii.member(jsii_name="keyVaultLicense")
    def key_vault_license(
        self,
    ) -> DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicenseOutputReference:
        return typing.cast(DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicenseOutputReference, jsii.get(self, "keyVaultLicense"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultLicenseInput")
    def key_vault_license_input(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense], jsii.get(self, "keyVaultLicenseInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseInput")
    def license_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="license")
    def license(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "license"))

    @license.setter
    def license(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2613772031ba675a6664cddf341c8ddb212f16d660df7fa44717303e406376b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "license", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c9bad17cf65c6416247cd575bd55bf48a013ceb27b75c65151b0441e18cc41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6781e08d2a73a16aad880a8d6ea047d0b32c14fc7e46b6f01db619c73a852ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67e16f76aa0209c7bea6ffa9f7ff3084147317c09385daa6a4f92e5b0a5b00fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCommandKey")
    def put_command_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62801aeca7b1f875040f9bf7f7ce0a43484c01c16b8c33911e24ebff69e34638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCommandKey", [value]))

    @jsii.member(jsii_name="putComponent")
    def put_component(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd54eacb2ed9782fe179e94acdb9c6f27d0be29aebb520547a39ed2527fc44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComponent", [value]))

    @jsii.member(jsii_name="resetCommandKey")
    def reset_command_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommandKey", []))

    @jsii.member(jsii_name="resetComponent")
    def reset_component(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComponent", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetPowershellVersion")
    def reset_powershell_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowershellVersion", []))

    @builtins.property
    @jsii.member(jsii_name="commandKey")
    def command_key(
        self,
    ) -> DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyList:
        return typing.cast(DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyList, jsii.get(self, "commandKey"))

    @builtins.property
    @jsii.member(jsii_name="component")
    def component(
        self,
    ) -> DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentList:
        return typing.cast(DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentList, jsii.get(self, "component"))

    @builtins.property
    @jsii.member(jsii_name="commandKeyInput")
    def command_key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]], jsii.get(self, "commandKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="componentInput")
    def component_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]], jsii.get(self, "componentInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="powershellVersionInput")
    def powershell_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "powershellVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9d7828c1e3b00016937a1fe9ea206d295f08dfa26b99e8bf3a29a61f44aff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="powershellVersion")
    def powershell_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "powershellVersion"))

    @powershell_version.setter
    def powershell_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b97374de255b4d61c31419f8e6bd9b945f22b79ec0d97f637c50eff969f2923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powershellVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3eee0d7e522312fc5aad39a4c917c53d2045af2bad5700548a0b16e9e12694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId"},
)
class DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration:
    def __init__(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_id DataFactoryIntegrationRuntimeAzureSsis#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a28a24122af4f5c3ddedfb4034b48c6332800e057391c9924dac4640aeeca2e)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_id DataFactoryIntegrationRuntimeAzureSsis#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb179b7b9557c29e5a655ee413dd2e8adcd9d68d083a03e04aef6e67f745396a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34cefe9a8ae4ab0e813793c2d59bf095b33fc07380593594e90bdda4b8212158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5463bdf2774f2e8fd3b7c4308ed790c8da4cfb4bc519690976f4d229327ecf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisPackageStore",
    jsii_struct_bases=[],
    name_mapping={"linked_service_name": "linkedServiceName", "name": "name"},
)
class DataFactoryIntegrationRuntimeAzureSsisPackageStore:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b238e209a1665b34ef629117517473905b36624e0acf0cacd53623f2914bef3)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "name": name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#linked_service_name DataFactoryIntegrationRuntimeAzureSsis#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#name DataFactoryIntegrationRuntimeAzureSsis#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisPackageStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisPackageStoreList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisPackageStoreList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcecefd712d0e4dd488b90896e2a79e78433bd80439951f7ac80ebd7b60360e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryIntegrationRuntimeAzureSsisPackageStoreOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae7043953382ada95272cc59d3fd4d193fcc015a17fbb2e210069d65c9dc6e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryIntegrationRuntimeAzureSsisPackageStoreOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8d86b58b6538a0d2b6677e4eee35dda63bc36f9ba19e821105ba52f9e471e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1f919b1e6ec860fb7b4be2a8fc8b9af7bcc68182aea269e35f81874180fdd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69774a0eac5af52451d9dc43aa22d0f536361bd316814178687699712692a28d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisPackageStore]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisPackageStore]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisPackageStore]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c573f5d4ddc850048d36ef3c59c5e6466300165cbb231f2e868b2f6758ac20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryIntegrationRuntimeAzureSsisPackageStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisPackageStoreOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4697ea5a417eaef9df91a6757dd44eaf42941c1ebb7f2608e56f81115ece4e59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="linkedServiceNameInput")
    def linked_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceName")
    def linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linkedServiceName"))

    @linked_service_name.setter
    def linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75d9e9e38e9fe9396f04d2960193b0e5d65b78b113df68a4c801fdb339fa3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c6d98e7f0e0b74a67f93b9f9fb8614084ac7aa372b20b18e4f7cffbfa22799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisPackageStore]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisPackageStore]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisPackageStore]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1704941f76bda1b266263ef4a3df4e819f65956942af05670c46f518ef8b1f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale",
    jsii_struct_bases=[],
    name_mapping={
        "number_of_external_nodes": "numberOfExternalNodes",
        "number_of_pipeline_nodes": "numberOfPipelineNodes",
        "time_to_live": "timeToLive",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale:
    def __init__(
        self,
        *,
        number_of_external_nodes: typing.Optional[jsii.Number] = None,
        number_of_pipeline_nodes: typing.Optional[jsii.Number] = None,
        time_to_live: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param number_of_external_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_external_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_external_nodes}.
        :param number_of_pipeline_nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_pipeline_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_pipeline_nodes}.
        :param time_to_live: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#time_to_live DataFactoryIntegrationRuntimeAzureSsis#time_to_live}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cebabb28eceac0e9061ee296cd7ab524e438e3830f2315aba914943b1dc58c)
            check_type(argname="argument number_of_external_nodes", value=number_of_external_nodes, expected_type=type_hints["number_of_external_nodes"])
            check_type(argname="argument number_of_pipeline_nodes", value=number_of_pipeline_nodes, expected_type=type_hints["number_of_pipeline_nodes"])
            check_type(argname="argument time_to_live", value=time_to_live, expected_type=type_hints["time_to_live"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if number_of_external_nodes is not None:
            self._values["number_of_external_nodes"] = number_of_external_nodes
        if number_of_pipeline_nodes is not None:
            self._values["number_of_pipeline_nodes"] = number_of_pipeline_nodes
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live

    @builtins.property
    def number_of_external_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_external_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_external_nodes}.'''
        result = self._values.get("number_of_external_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_pipeline_nodes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#number_of_pipeline_nodes DataFactoryIntegrationRuntimeAzureSsis#number_of_pipeline_nodes}.'''
        result = self._values.get("number_of_pipeline_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_to_live(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#time_to_live DataFactoryIntegrationRuntimeAzureSsis#time_to_live}.'''
        result = self._values.get("time_to_live")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScaleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bee245b0b133a4a1c3e9a55abe24489d2f79ec25860d1bf273d062380e7b8f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNumberOfExternalNodes")
    def reset_number_of_external_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfExternalNodes", []))

    @jsii.member(jsii_name="resetNumberOfPipelineNodes")
    def reset_number_of_pipeline_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfPipelineNodes", []))

    @jsii.member(jsii_name="resetTimeToLive")
    def reset_time_to_live(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeToLive", []))

    @builtins.property
    @jsii.member(jsii_name="numberOfExternalNodesInput")
    def number_of_external_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfExternalNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfPipelineNodesInput")
    def number_of_pipeline_nodes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfPipelineNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeToLiveInput")
    def time_to_live_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeToLiveInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfExternalNodes")
    def number_of_external_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfExternalNodes"))

    @number_of_external_nodes.setter
    def number_of_external_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1b4fcddf607725c28ba85ace67c07d589ee1aaf00a374d1fafeac6afc88909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfExternalNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numberOfPipelineNodes")
    def number_of_pipeline_nodes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfPipelineNodes"))

    @number_of_pipeline_nodes.setter
    def number_of_pipeline_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8640b2c07bb6265331ddd2a7854d493526452d43081872bb8d4413390d8b15de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfPipelineNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeToLive")
    def time_to_live(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeToLive"))

    @time_to_live.setter
    def time_to_live(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb05b0567daf323d5ba689412a69544c1c54e31456b49455e45f9bf706964630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeToLive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e139794fae5d4d06a76cf27fcdaf68f668553a8f610068d650f1ae39243c2a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisProxy",
    jsii_struct_bases=[],
    name_mapping={
        "self_hosted_integration_runtime_name": "selfHostedIntegrationRuntimeName",
        "staging_storage_linked_service_name": "stagingStorageLinkedServiceName",
        "path": "path",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisProxy:
    def __init__(
        self,
        *,
        self_hosted_integration_runtime_name: builtins.str,
        staging_storage_linked_service_name: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param self_hosted_integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#self_hosted_integration_runtime_name DataFactoryIntegrationRuntimeAzureSsis#self_hosted_integration_runtime_name}.
        :param staging_storage_linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#staging_storage_linked_service_name DataFactoryIntegrationRuntimeAzureSsis#staging_storage_linked_service_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#path DataFactoryIntegrationRuntimeAzureSsis#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc544baed0565be20ca2dc1c2c75663846d96d2f89dfdd1c5b46d1b5bb045b7)
            check_type(argname="argument self_hosted_integration_runtime_name", value=self_hosted_integration_runtime_name, expected_type=type_hints["self_hosted_integration_runtime_name"])
            check_type(argname="argument staging_storage_linked_service_name", value=staging_storage_linked_service_name, expected_type=type_hints["staging_storage_linked_service_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "self_hosted_integration_runtime_name": self_hosted_integration_runtime_name,
            "staging_storage_linked_service_name": staging_storage_linked_service_name,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def self_hosted_integration_runtime_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#self_hosted_integration_runtime_name DataFactoryIntegrationRuntimeAzureSsis#self_hosted_integration_runtime_name}.'''
        result = self._values.get("self_hosted_integration_runtime_name")
        assert result is not None, "Required property 'self_hosted_integration_runtime_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def staging_storage_linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#staging_storage_linked_service_name DataFactoryIntegrationRuntimeAzureSsis#staging_storage_linked_service_name}.'''
        result = self._values.get("staging_storage_linked_service_name")
        assert result is not None, "Required property 'staging_storage_linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#path DataFactoryIntegrationRuntimeAzureSsis#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5034f8177be9897dda64da7212b7f0ea1900b19319e0affeecc8a0408d07d651)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="selfHostedIntegrationRuntimeNameInput")
    def self_hosted_integration_runtime_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selfHostedIntegrationRuntimeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingStorageLinkedServiceNameInput")
    def staging_storage_linked_service_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingStorageLinkedServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f45665922c2cedf6fdb1da79994384909c4da0c638dcc36b15c8ace6c9143e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selfHostedIntegrationRuntimeName")
    def self_hosted_integration_runtime_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfHostedIntegrationRuntimeName"))

    @self_hosted_integration_runtime_name.setter
    def self_hosted_integration_runtime_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb65d7557326a0cc6261e174828738a9217c32b859dfffbce2b5150aaa9f47ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selfHostedIntegrationRuntimeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingStorageLinkedServiceName")
    def staging_storage_linked_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingStorageLinkedServiceName"))

    @staging_storage_linked_service_name.setter
    def staging_storage_linked_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73554530580ca6f20eaa9442cc7ef81f670c5484b5c67d180dfbc08f2f4f7b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingStorageLinkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisProxy]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a441839a74b54536aac5c5f4fb0b918171fa9e801e0878c7f8bf997e542a496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#create DataFactoryIntegrationRuntimeAzureSsis#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#delete DataFactoryIntegrationRuntimeAzureSsis#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#read DataFactoryIntegrationRuntimeAzureSsis#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#update DataFactoryIntegrationRuntimeAzureSsis#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a4ba2663659c58e2d455d73e8b4233e5cccbcce6bf9c86952915c9683f93c0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#create DataFactoryIntegrationRuntimeAzureSsis#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#delete DataFactoryIntegrationRuntimeAzureSsis#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#read DataFactoryIntegrationRuntimeAzureSsis#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#update DataFactoryIntegrationRuntimeAzureSsis#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2092a6b875a09b082fc2149bb8d84efee25c3fea9bad4c8053bb1d5278f494b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60310a0b3adb7f87eea128c9869a9d435ef125c2cf9fed67d6b4d5628bf76d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfa93d0362cd39bfcade3857c242a3eaff0a7dbb174fbebadac82348225a2da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e782d36c30c6475db3bdec99ecfc3c84c285004a716563e80778198002acc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa39e3924b64df117b73b61cac664faea1508902ccaa3d4197fdcd8e426561cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382cd5dca9485f2055dbc8818ade58392b1311c24199db888a09f1e2fa56da81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisVnetIntegration",
    jsii_struct_bases=[],
    name_mapping={
        "public_ips": "publicIps",
        "subnet_id": "subnetId",
        "subnet_name": "subnetName",
        "vnet_id": "vnetId",
    },
)
class DataFactoryIntegrationRuntimeAzureSsisVnetIntegration:
    def __init__(
        self,
        *,
        public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        subnet_name: typing.Optional[builtins.str] = None,
        vnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_ips: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#public_ips DataFactoryIntegrationRuntimeAzureSsis#public_ips}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_id DataFactoryIntegrationRuntimeAzureSsis#subnet_id}.
        :param subnet_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_name DataFactoryIntegrationRuntimeAzureSsis#subnet_name}.
        :param vnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#vnet_id DataFactoryIntegrationRuntimeAzureSsis#vnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3befb569afff2e12ea44b675f515af5b105d196c6fb3647f196b9318af093f92)
            check_type(argname="argument public_ips", value=public_ips, expected_type=type_hints["public_ips"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument subnet_name", value=subnet_name, expected_type=type_hints["subnet_name"])
            check_type(argname="argument vnet_id", value=vnet_id, expected_type=type_hints["vnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_ips is not None:
            self._values["public_ips"] = public_ips
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if subnet_name is not None:
            self._values["subnet_name"] = subnet_name
        if vnet_id is not None:
            self._values["vnet_id"] = vnet_id

    @builtins.property
    def public_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#public_ips DataFactoryIntegrationRuntimeAzureSsis#public_ips}.'''
        result = self._values.get("public_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_id DataFactoryIntegrationRuntimeAzureSsis#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#subnet_name DataFactoryIntegrationRuntimeAzureSsis#subnet_name}.'''
        result = self._values.get("subnet_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_integration_runtime_azure_ssis#vnet_id DataFactoryIntegrationRuntimeAzureSsis#vnet_id}.'''
        result = self._values.get("vnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryIntegrationRuntimeAzureSsisVnetIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryIntegrationRuntimeAzureSsisVnetIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryIntegrationRuntimeAzureSsis.DataFactoryIntegrationRuntimeAzureSsisVnetIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfd3eaf524752ea3e00b3426d8a9bcc4d90185446b80534f737df868e4b50937)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicIps")
    def reset_public_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIps", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetSubnetName")
    def reset_subnet_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetName", []))

    @jsii.member(jsii_name="resetVnetId")
    def reset_vnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetId", []))

    @builtins.property
    @jsii.member(jsii_name="publicIpsInput")
    def public_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetNameInput")
    def subnet_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetIdInput")
    def vnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIps")
    def public_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIps"))

    @public_ips.setter
    def public_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b088ef4caea1d634b13fda1d822936ee1bbb62fc74b0518fa71a04f31138545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2254d83265105ecce7e0d03d9bcf68711b63940622417cfd9a73e1411174a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetName")
    def subnet_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetName"))

    @subnet_name.setter
    def subnet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0564fa21e810909397856c645846f9b7298728b87d47a691663c007d01c98044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vnetId")
    def vnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetId"))

    @vnet_id.setter
    def vnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b2523f8d3c67a99f7800051a293bb6fb8e9fdd3bd0d6fbcbb9bbc84207c4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryIntegrationRuntimeAzureSsisVnetIntegration]:
        return typing.cast(typing.Optional[DataFactoryIntegrationRuntimeAzureSsisVnetIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisVnetIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7f16172e15b81b3338f6a4c118689a729ff0fe9ebe60b402eba2b94682641e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataFactoryIntegrationRuntimeAzureSsis",
    "DataFactoryIntegrationRuntimeAzureSsisCatalogInfo",
    "DataFactoryIntegrationRuntimeAzureSsisCatalogInfoOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisConfig",
    "DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale",
    "DataFactoryIntegrationRuntimeAzureSsisCopyComputeScaleOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript",
    "DataFactoryIntegrationRuntimeAzureSsisCustomSetupScriptOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPasswordOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyList",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicenseOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentList",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration",
    "DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegrationOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisPackageStore",
    "DataFactoryIntegrationRuntimeAzureSsisPackageStoreList",
    "DataFactoryIntegrationRuntimeAzureSsisPackageStoreOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale",
    "DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScaleOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisProxy",
    "DataFactoryIntegrationRuntimeAzureSsisProxyOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisTimeouts",
    "DataFactoryIntegrationRuntimeAzureSsisTimeoutsOutputReference",
    "DataFactoryIntegrationRuntimeAzureSsisVnetIntegration",
    "DataFactoryIntegrationRuntimeAzureSsisVnetIntegrationOutputReference",
]

publication.publish()

def _typecheckingstub__dbfe2a3c8135d17d030e4678be10030795f75c48eb8e67953d9bbcf8297de57f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_factory_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    node_size: builtins.str,
    catalog_info: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_compute_scale: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale, typing.Dict[builtins.str, typing.Any]]] = None,
    credential_name: typing.Optional[builtins.str] = None,
    custom_setup_script: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    express_custom_setup: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup, typing.Dict[builtins.str, typing.Any]]] = None,
    express_vnet_integration: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
    package_store: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisPackageStore, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pipeline_external_compute_scale: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vnet_integration: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisVnetIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__039f901c16bb161afdf0240fcb7758782d7ea068fd5b4b396e3b309642a417c0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6beb0a3569317ab29a21dd0d06687ee235fef513eff31b27e94c487a3915c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisPackageStore, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873aae074e38afa85f1235702c2e79d2a64a05fa7ed30725bd360329317fef3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7327cfe2858da0b0b0e0609efe5bca42aa94b47218f13eae4bdcdf880e090b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e822a80e799145c16caafbfb4c93e1144c51ed3e7a7cdfd06ebddb4c36c91a7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e754ec4936c5f35847e747f22176721acc7598cec1ad18ac66cd820b08b5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63199168f5155ffb0fa2800699156ef5c5a9fed0c7205e1e6ed54a5c6c45abef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b606fab38d412011aa6913559d2c8595d508353a17fecd48c7edd53206203988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02bd010576164a86f8368ee12aa5e1e37733d0ad56a97bc8061bd25eb250a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53162c7448a1c9bd5f0742050f51594825094c91ce53fd05e0f3b379c8bde3d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d150e6ab9f1df5a29cfd94790a35a5344db5df78c1d493de6a765f5b8d79c140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0db99bc9389fff086378ee9f76df50ccef1c5477176b265270878f347dd7e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c6b940ab25c5d02a85f3bb3a48e44f7f52586101c3c911df6cab1db37dfc56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415af22b6beda4a326662882de3279ae1df1a6196d0080b1e9dd15b0ded1567a(
    *,
    server_endpoint: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_password: typing.Optional[builtins.str] = None,
    dual_standby_pair_name: typing.Optional[builtins.str] = None,
    elastic_pool_name: typing.Optional[builtins.str] = None,
    pricing_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed30f7929cb2ea01e7048e64fff11a7c4a99999395a56b9dda24f33bbfb8806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0e52c886b9b92aba05db880548d1025482112f490b00507bc719b64f5133ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c714ae514555d0eb3f9f440776b1e07b61e8626e412d8eb3d7dccbf30c17262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9744c9497264f6dcdd3ad8d8e00d5eae31c7291a6a80965f94c0c91cdcc8675e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adcc99f7d96af28880fd1d3e35bf567c754cbccc671190d59a1875029b9b33c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba280c23a17bf03401df22b200a79bf97c00ec4192dbf9706cf913491de5e3cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2dae68fc5a17b267530ebf093c61bd7df176843ace7286739c6d89a22684bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fea809f98b0432b59302da4296f4db0e7069f6738a43af3cfebd028e1ab47a5(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03a6d353e67e9325a1d8e6c4a81f84911a50ee8b2293b7ae487947c38e68acb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_factory_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    node_size: builtins.str,
    catalog_info: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCatalogInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_compute_scale: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale, typing.Dict[builtins.str, typing.Any]]] = None,
    credential_name: typing.Optional[builtins.str] = None,
    custom_setup_script: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    express_custom_setup: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup, typing.Dict[builtins.str, typing.Any]]] = None,
    express_vnet_integration: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    license_type: typing.Optional[builtins.str] = None,
    max_parallel_executions_per_node: typing.Optional[jsii.Number] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
    package_store: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisPackageStore, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pipeline_external_compute_scale: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vnet_integration: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisVnetIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9783dd29a6ae21ac27409b05eb202127ba0831208ce1051606c84c06ae06e177(
    *,
    data_integration_unit: typing.Optional[jsii.Number] = None,
    time_to_live: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a9b6c282ece13b2507bd26df8a1aa21b7c369dc4306bf594072772b536cb6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acac2c465a3ccafacd32ff4cabf83efb395e0a367ee3520faea018b0b571da03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6334b525e7740cc6bfbf5edc251eeb540ed5a799e95cfdd84613baeef2e583bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105aec8d5871ee4f550e22eb38ae5a32aa47fb0eb3ff501bc3db6fff976ae25f(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCopyComputeScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8155cdd3121fba27f5cf3c06f802198812e72af2c1e25e78a72a17782daf27(
    *,
    blob_container_uri: builtins.str,
    sas_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa38c9da196cb83a0b5add35e517d0fba4990233844d3ce2ad0899d679c94145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54861b90ec246019300f9057a21da5502604cbc89c0ce2be37783a0547d3017(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d9e440b855fac79f5d17d8624cd3c4f307c9ed58b743dd8be78dd0f18b95e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f827a08ddf428aee8430b82faf552daa4aae4893b260cbb6e0bdc68c2680af75(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisCustomSetupScript],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe486633d72da84961b28616efa02ba4a446cae59dde95f47a996ab3a73774c(
    *,
    command_key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    component: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    powershell_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315e9bac1c9ffd9b26cde49f70ba205270f2d0d2340308a1779f23ab3128018f(
    *,
    target_name: builtins.str,
    user_name: builtins.str,
    key_vault_password: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc43cf4277dba81a7ba712aa3933bba8e2bb4975c3e22aaf4db007f76a91e7f(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e1fa956d279286b443bb85e4c6ba3cab86c4eb7a298dca947136802ecd757a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce8fd2d0cb1d924d648c5c8f0e6f713175a093c62a44e2bf0229af456013736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64bb50ca17071593e92b23ea0a4888933a00bb09777e1928494ea1cd1224c99(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4278fe702ec0c12982b4788dddce100bacb58295b3667f0be98f4ef279d39d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ae1c75a5eac51549e2948152b72d63fda31368b5fed3a429a6e835f86abde4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c63ebda029f73f13aa983d80387fc819ef1fccb21bf52d59ee44819c3acb3f(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKeyKeyVaultPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c4ef578085dace573e321252eec4cd4fdf00d0595813db4a85c45c7ed60b5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9335af1c6e8b74daec56c9b7061b961382063d4a67a5be2b5818cedf51e86220(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f83851f4e66bd8353a8124a5893852e1089cdf90d94965df5a547e1dec08bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e5f557b7768c4a461ef4c042e6bb754ed1dab39b974d73b37bb1ec9469eb52(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce9a172e8999439116a064735dd8d3c9fff1d4190e1c25df822890a89a41d76(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1899b095fedb09f61208c1a634516b91996b107045f607761a7643ecc6f73d3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acc8b275f23f32921e1579e3d1f5424f9c9cb29b397d1b407467243211b278e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e956496cce106df5418cbbaee9ec06449fef5855a60939987c6d4ce56f1bc422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d65f262549649320897ad701406993266934c2e1139a37dd5672d1a70d3a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094056248ebb8302ee6e3cf790e9f72b063d3e0b8cd302d7c4d94ef09135030d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86db7c48ec2d4609b80ccaadf6a83087bba4893882a4431d4c4ce3f4716a519d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef02fa91f45d3e92eafd37e5f1d7e0944e7bb202afa233efd7dc083d5c7ee0be(
    *,
    name: builtins.str,
    key_vault_license: typing.Optional[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense, typing.Dict[builtins.str, typing.Any]]] = None,
    license: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82825e978c43f80dc95d1cdce0fa76ba5354fe51c4d2e424df849b65154f922f(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca48acfe600d36866c611e0e52b354511f9da51cfc555631979cb7efc11c0656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bc3d180c191e599294f57e0c0c2b28e154de01193f6ca5b76bea2a1743cc04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79eeb4679c32e02cdca57584db40ed4027f80a86661eadc334dc03bfd10b6dbc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e66c6b2f5e9be16b5ae0dfdc929fa0c7cbc4c77411e0a3e8c88bdff54429644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551a6511c42e7eba729fdae3693ddf1790d5a2314ebb0472d97c754e5c210608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec13fe2cf9e1fc7d4ee0689bc226c691a21ccc0207e559a31322d104136915e(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponentKeyVaultLicense],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7797527d547f23846370556ced3804b3c5bdcf7769cab187876e481068c651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0d3bd68f0b0a9835d79aaff5c01092a2ea2884e5b55feaa3ecb114ab8f5fe5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570c5a0b1f98662ee887ae92e2de6c0cfebbda89d2482f9d2e8582fd8540db7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5373dfffe03001b82fdffceeb3e18a355a11b29b83ab267109b0084409af7e7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34750c83d01bc4086b7823fe3aed97d14b40f779d26ed366d76d91a0be44e3f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8508171ddfe8171efbfbe1648c566b98f1f2b3188dda7c1d16f6b283be02db9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d86b8548393ca75d92db77d47f10e71e183dd8bf9ced061d7101eaaea1f443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2613772031ba675a6664cddf341c8ddb212f16d660df7fa44717303e406376b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c9bad17cf65c6416247cd575bd55bf48a013ceb27b75c65151b0441e18cc41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6781e08d2a73a16aad880a8d6ea047d0b32c14fc7e46b6f01db619c73a852ab7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e16f76aa0209c7bea6ffa9f7ff3084147317c09385daa6a4f92e5b0a5b00fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62801aeca7b1f875040f9bf7f7ce0a43484c01c16b8c33911e24ebff69e34638(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupCommandKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd54eacb2ed9782fe179e94acdb9c6f27d0be29aebb520547a39ed2527fc44a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetupComponent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9d7828c1e3b00016937a1fe9ea206d295f08dfa26b99e8bf3a29a61f44aff4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b97374de255b4d61c31419f8e6bd9b945f22b79ec0d97f637c50eff969f2923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3eee0d7e522312fc5aad39a4c917c53d2045af2bad5700548a0b16e9e12694(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressCustomSetup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a28a24122af4f5c3ddedfb4034b48c6332800e057391c9924dac4640aeeca2e(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb179b7b9557c29e5a655ee413dd2e8adcd9d68d083a03e04aef6e67f745396a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34cefe9a8ae4ab0e813793c2d59bf095b33fc07380593594e90bdda4b8212158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5463bdf2774f2e8fd3b7c4308ed790c8da4cfb4bc519690976f4d229327ecf6(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisExpressVnetIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b238e209a1665b34ef629117517473905b36624e0acf0cacd53623f2914bef3(
    *,
    linked_service_name: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcecefd712d0e4dd488b90896e2a79e78433bd80439951f7ac80ebd7b60360e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae7043953382ada95272cc59d3fd4d193fcc015a17fbb2e210069d65c9dc6e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8d86b58b6538a0d2b6677e4eee35dda63bc36f9ba19e821105ba52f9e471e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1f919b1e6ec860fb7b4be2a8fc8b9af7bcc68182aea269e35f81874180fdd4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69774a0eac5af52451d9dc43aa22d0f536361bd316814178687699712692a28d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c573f5d4ddc850048d36ef3c59c5e6466300165cbb231f2e868b2f6758ac20f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryIntegrationRuntimeAzureSsisPackageStore]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4697ea5a417eaef9df91a6757dd44eaf42941c1ebb7f2608e56f81115ece4e59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75d9e9e38e9fe9396f04d2960193b0e5d65b78b113df68a4c801fdb339fa3aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c6d98e7f0e0b74a67f93b9f9fb8614084ac7aa372b20b18e4f7cffbfa22799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1704941f76bda1b266263ef4a3df4e819f65956942af05670c46f518ef8b1f8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisPackageStore]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cebabb28eceac0e9061ee296cd7ab524e438e3830f2315aba914943b1dc58c(
    *,
    number_of_external_nodes: typing.Optional[jsii.Number] = None,
    number_of_pipeline_nodes: typing.Optional[jsii.Number] = None,
    time_to_live: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bee245b0b133a4a1c3e9a55abe24489d2f79ec25860d1bf273d062380e7b8f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1b4fcddf607725c28ba85ace67c07d589ee1aaf00a374d1fafeac6afc88909(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8640b2c07bb6265331ddd2a7854d493526452d43081872bb8d4413390d8b15de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb05b0567daf323d5ba689412a69544c1c54e31456b49455e45f9bf706964630(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e139794fae5d4d06a76cf27fcdaf68f668553a8f610068d650f1ae39243c2a5(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisPipelineExternalComputeScale],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc544baed0565be20ca2dc1c2c75663846d96d2f89dfdd1c5b46d1b5bb045b7(
    *,
    self_hosted_integration_runtime_name: builtins.str,
    staging_storage_linked_service_name: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5034f8177be9897dda64da7212b7f0ea1900b19319e0affeecc8a0408d07d651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f45665922c2cedf6fdb1da79994384909c4da0c638dcc36b15c8ace6c9143e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb65d7557326a0cc6261e174828738a9217c32b859dfffbce2b5150aaa9f47ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73554530580ca6f20eaa9442cc7ef81f670c5484b5c67d180dfbc08f2f4f7b38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a441839a74b54536aac5c5f4fb0b918171fa9e801e0878c7f8bf997e542a496(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a4ba2663659c58e2d455d73e8b4233e5cccbcce6bf9c86952915c9683f93c0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2092a6b875a09b082fc2149bb8d84efee25c3fea9bad4c8053bb1d5278f494b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60310a0b3adb7f87eea128c9869a9d435ef125c2cf9fed67d6b4d5628bf76d1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfa93d0362cd39bfcade3857c242a3eaff0a7dbb174fbebadac82348225a2da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e782d36c30c6475db3bdec99ecfc3c84c285004a716563e80778198002acc47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa39e3924b64df117b73b61cac664faea1508902ccaa3d4197fdcd8e426561cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382cd5dca9485f2055dbc8818ade58392b1311c24199db888a09f1e2fa56da81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryIntegrationRuntimeAzureSsisTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3befb569afff2e12ea44b675f515af5b105d196c6fb3647f196b9318af093f92(
    *,
    public_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    subnet_name: typing.Optional[builtins.str] = None,
    vnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd3eaf524752ea3e00b3426d8a9bcc4d90185446b80534f737df868e4b50937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b088ef4caea1d634b13fda1d822936ee1bbb62fc74b0518fa71a04f31138545(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2254d83265105ecce7e0d03d9bcf68711b63940622417cfd9a73e1411174a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0564fa21e810909397856c645846f9b7298728b87d47a691663c007d01c98044(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b2523f8d3c67a99f7800051a293bb6fb8e9fdd3bd0d6fbcbb9bbc84207c4e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7f16172e15b81b3338f6a4c118689a729ff0fe9ebe60b402eba2b94682641e(
    value: typing.Optional[DataFactoryIntegrationRuntimeAzureSsisVnetIntegration],
) -> None:
    """Type checking stubs"""
    pass
