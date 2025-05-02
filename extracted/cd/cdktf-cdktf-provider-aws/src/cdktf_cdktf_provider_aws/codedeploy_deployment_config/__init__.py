r'''
# `aws_codedeploy_deployment_config`

Refer to the Terraform Registry for docs: [`aws_codedeploy_deployment_config`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config).
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


class CodedeployDeploymentConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config aws_codedeploy_deployment_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        deployment_config_name: builtins.str,
        compute_platform: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union["CodedeployDeploymentConfigMinimumHealthyHosts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_routing_config: typing.Optional[typing.Union["CodedeployDeploymentConfigTrafficRoutingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        zonal_config: typing.Optional[typing.Union["CodedeployDeploymentConfigZonalConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config aws_codedeploy_deployment_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deployment_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#deployment_config_name CodedeployDeploymentConfig#deployment_config_name}.
        :param compute_platform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#compute_platform CodedeployDeploymentConfig#compute_platform}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#id CodedeployDeploymentConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_healthy_hosts: minimum_healthy_hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#minimum_healthy_hosts CodedeployDeploymentConfig#minimum_healthy_hosts}
        :param traffic_routing_config: traffic_routing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#traffic_routing_config CodedeployDeploymentConfig#traffic_routing_config}
        :param zonal_config: zonal_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#zonal_config CodedeployDeploymentConfig#zonal_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fecb089dffe43959612f288f6a5bc69cdaf53ef75a4ab90b823c83e1353e52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CodedeployDeploymentConfigConfig(
            deployment_config_name=deployment_config_name,
            compute_platform=compute_platform,
            id=id,
            minimum_healthy_hosts=minimum_healthy_hosts,
            traffic_routing_config=traffic_routing_config,
            zonal_config=zonal_config,
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
        '''Generates CDKTF code for importing a CodedeployDeploymentConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CodedeployDeploymentConfig to import.
        :param import_from_id: The id of the existing CodedeployDeploymentConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CodedeployDeploymentConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d75f8bc6620fa5736e4d976208eba64929957cd2b50211e49b33d266aa1fc2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMinimumHealthyHosts")
    def put_minimum_healthy_hosts(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#value CodedeployDeploymentConfig#value}.
        '''
        value_ = CodedeployDeploymentConfigMinimumHealthyHosts(type=type, value=value)

        return typing.cast(None, jsii.invoke(self, "putMinimumHealthyHosts", [value_]))

    @jsii.member(jsii_name="putTrafficRoutingConfig")
    def put_traffic_routing_config(
        self,
        *,
        time_based_canary: typing.Optional[typing.Union["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary", typing.Dict[builtins.str, typing.Any]]] = None,
        time_based_linear: typing.Optional[typing.Union["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param time_based_canary: time_based_canary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#time_based_canary CodedeployDeploymentConfig#time_based_canary}
        :param time_based_linear: time_based_linear block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#time_based_linear CodedeployDeploymentConfig#time_based_linear}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.
        '''
        value = CodedeployDeploymentConfigTrafficRoutingConfig(
            time_based_canary=time_based_canary,
            time_based_linear=time_based_linear,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putTrafficRoutingConfig", [value]))

    @jsii.member(jsii_name="putZonalConfig")
    def put_zonal_config(
        self,
        *,
        first_zone_monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
        minimum_healthy_hosts_per_zone: typing.Optional[typing.Union["CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param first_zone_monitor_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#first_zone_monitor_duration_in_seconds CodedeployDeploymentConfig#first_zone_monitor_duration_in_seconds}.
        :param minimum_healthy_hosts_per_zone: minimum_healthy_hosts_per_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#minimum_healthy_hosts_per_zone CodedeployDeploymentConfig#minimum_healthy_hosts_per_zone}
        :param monitor_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#monitor_duration_in_seconds CodedeployDeploymentConfig#monitor_duration_in_seconds}.
        '''
        value = CodedeployDeploymentConfigZonalConfig(
            first_zone_monitor_duration_in_seconds=first_zone_monitor_duration_in_seconds,
            minimum_healthy_hosts_per_zone=minimum_healthy_hosts_per_zone,
            monitor_duration_in_seconds=monitor_duration_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putZonalConfig", [value]))

    @jsii.member(jsii_name="resetComputePlatform")
    def reset_compute_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputePlatform", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimumHealthyHosts")
    def reset_minimum_healthy_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumHealthyHosts", []))

    @jsii.member(jsii_name="resetTrafficRoutingConfig")
    def reset_traffic_routing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficRoutingConfig", []))

    @jsii.member(jsii_name="resetZonalConfig")
    def reset_zonal_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZonalConfig", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigId")
    def deployment_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigId"))

    @builtins.property
    @jsii.member(jsii_name="minimumHealthyHosts")
    def minimum_healthy_hosts(
        self,
    ) -> "CodedeployDeploymentConfigMinimumHealthyHostsOutputReference":
        return typing.cast("CodedeployDeploymentConfigMinimumHealthyHostsOutputReference", jsii.get(self, "minimumHealthyHosts"))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfig")
    def traffic_routing_config(
        self,
    ) -> "CodedeployDeploymentConfigTrafficRoutingConfigOutputReference":
        return typing.cast("CodedeployDeploymentConfigTrafficRoutingConfigOutputReference", jsii.get(self, "trafficRoutingConfig"))

    @builtins.property
    @jsii.member(jsii_name="zonalConfig")
    def zonal_config(self) -> "CodedeployDeploymentConfigZonalConfigOutputReference":
        return typing.cast("CodedeployDeploymentConfigZonalConfigOutputReference", jsii.get(self, "zonalConfig"))

    @builtins.property
    @jsii.member(jsii_name="computePlatformInput")
    def compute_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigNameInput")
    def deployment_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumHealthyHostsInput")
    def minimum_healthy_hosts_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigMinimumHealthyHosts"]:
        return typing.cast(typing.Optional["CodedeployDeploymentConfigMinimumHealthyHosts"], jsii.get(self, "minimumHealthyHostsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfigInput")
    def traffic_routing_config_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfig"]:
        return typing.cast(typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfig"], jsii.get(self, "trafficRoutingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="zonalConfigInput")
    def zonal_config_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigZonalConfig"]:
        return typing.cast(typing.Optional["CodedeployDeploymentConfigZonalConfig"], jsii.get(self, "zonalConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computePlatform"))

    @compute_platform.setter
    def compute_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ab34b4b67ce9fae91167a1d102c6d5913bbb4ea2c868998af329ad1c401d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computePlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ce897e0e8b1737defa00f45218a0f286bfb1476e11fabf7cb6e0ec4f19e365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentConfigName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd197eb1845cf7cb44b56d73d102ada5b005dcac83778c7e7f6b74acb3f37db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "deployment_config_name": "deploymentConfigName",
        "compute_platform": "computePlatform",
        "id": "id",
        "minimum_healthy_hosts": "minimumHealthyHosts",
        "traffic_routing_config": "trafficRoutingConfig",
        "zonal_config": "zonalConfig",
    },
)
class CodedeployDeploymentConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        deployment_config_name: builtins.str,
        compute_platform: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union["CodedeployDeploymentConfigMinimumHealthyHosts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_routing_config: typing.Optional[typing.Union["CodedeployDeploymentConfigTrafficRoutingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        zonal_config: typing.Optional[typing.Union["CodedeployDeploymentConfigZonalConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deployment_config_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#deployment_config_name CodedeployDeploymentConfig#deployment_config_name}.
        :param compute_platform: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#compute_platform CodedeployDeploymentConfig#compute_platform}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#id CodedeployDeploymentConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_healthy_hosts: minimum_healthy_hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#minimum_healthy_hosts CodedeployDeploymentConfig#minimum_healthy_hosts}
        :param traffic_routing_config: traffic_routing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#traffic_routing_config CodedeployDeploymentConfig#traffic_routing_config}
        :param zonal_config: zonal_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#zonal_config CodedeployDeploymentConfig#zonal_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(minimum_healthy_hosts, dict):
            minimum_healthy_hosts = CodedeployDeploymentConfigMinimumHealthyHosts(**minimum_healthy_hosts)
        if isinstance(traffic_routing_config, dict):
            traffic_routing_config = CodedeployDeploymentConfigTrafficRoutingConfig(**traffic_routing_config)
        if isinstance(zonal_config, dict):
            zonal_config = CodedeployDeploymentConfigZonalConfig(**zonal_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb67ecf3cf6c0ea7515a90d8f9a89afcf33be7c62526ed4811d5ad3bbeb6f454)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimum_healthy_hosts", value=minimum_healthy_hosts, expected_type=type_hints["minimum_healthy_hosts"])
            check_type(argname="argument traffic_routing_config", value=traffic_routing_config, expected_type=type_hints["traffic_routing_config"])
            check_type(argname="argument zonal_config", value=zonal_config, expected_type=type_hints["zonal_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment_config_name": deployment_config_name,
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
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if id is not None:
            self._values["id"] = id
        if minimum_healthy_hosts is not None:
            self._values["minimum_healthy_hosts"] = minimum_healthy_hosts
        if traffic_routing_config is not None:
            self._values["traffic_routing_config"] = traffic_routing_config
        if zonal_config is not None:
            self._values["zonal_config"] = zonal_config

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
    def deployment_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#deployment_config_name CodedeployDeploymentConfig#deployment_config_name}.'''
        result = self._values.get("deployment_config_name")
        assert result is not None, "Required property 'deployment_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#compute_platform CodedeployDeploymentConfig#compute_platform}.'''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#id CodedeployDeploymentConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_healthy_hosts(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigMinimumHealthyHosts"]:
        '''minimum_healthy_hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#minimum_healthy_hosts CodedeployDeploymentConfig#minimum_healthy_hosts}
        '''
        result = self._values.get("minimum_healthy_hosts")
        return typing.cast(typing.Optional["CodedeployDeploymentConfigMinimumHealthyHosts"], result)

    @builtins.property
    def traffic_routing_config(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfig"]:
        '''traffic_routing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#traffic_routing_config CodedeployDeploymentConfig#traffic_routing_config}
        '''
        result = self._values.get("traffic_routing_config")
        return typing.cast(typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfig"], result)

    @builtins.property
    def zonal_config(self) -> typing.Optional["CodedeployDeploymentConfigZonalConfig"]:
        '''zonal_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#zonal_config CodedeployDeploymentConfig#zonal_config}
        '''
        result = self._values.get("zonal_config")
        return typing.cast(typing.Optional["CodedeployDeploymentConfigZonalConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigMinimumHealthyHosts",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class CodedeployDeploymentConfigMinimumHealthyHosts:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#value CodedeployDeploymentConfig#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ff7b7bf8d3d23c171065321f8250ccfd6c0612958b8bbe995d7f8632552285)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#value CodedeployDeploymentConfig#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigMinimumHealthyHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentConfigMinimumHealthyHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigMinimumHealthyHostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b2cb4dc5d2e05da5f74342937009c38ec3d941c2da0c522c897e4fbfd27cca4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59adb5d64bba30d08a4428b442c1efc94a2fd08a03d1a6dde3516adef143c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3e521803b84d2595cdba93d18d47ffc40ecc30234a5203c65fb096fef112c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentConfigMinimumHealthyHosts]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigMinimumHealthyHosts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentConfigMinimumHealthyHosts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b7bd3b987a6019e5e38b47651a6e26c6c032cd1a8725baac8344e17e71f75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigTrafficRoutingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "time_based_canary": "timeBasedCanary",
        "time_based_linear": "timeBasedLinear",
        "type": "type",
    },
)
class CodedeployDeploymentConfigTrafficRoutingConfig:
    def __init__(
        self,
        *,
        time_based_canary: typing.Optional[typing.Union["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary", typing.Dict[builtins.str, typing.Any]]] = None,
        time_based_linear: typing.Optional[typing.Union["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param time_based_canary: time_based_canary block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#time_based_canary CodedeployDeploymentConfig#time_based_canary}
        :param time_based_linear: time_based_linear block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#time_based_linear CodedeployDeploymentConfig#time_based_linear}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.
        '''
        if isinstance(time_based_canary, dict):
            time_based_canary = CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary(**time_based_canary)
        if isinstance(time_based_linear, dict):
            time_based_linear = CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear(**time_based_linear)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a7400a578c53bd4560ae4ee4c949bf476b63f4d08cb71e42e22104092e6419b)
            check_type(argname="argument time_based_canary", value=time_based_canary, expected_type=type_hints["time_based_canary"])
            check_type(argname="argument time_based_linear", value=time_based_linear, expected_type=type_hints["time_based_linear"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if time_based_canary is not None:
            self._values["time_based_canary"] = time_based_canary
        if time_based_linear is not None:
            self._values["time_based_linear"] = time_based_linear
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def time_based_canary(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary"]:
        '''time_based_canary block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#time_based_canary CodedeployDeploymentConfig#time_based_canary}
        '''
        result = self._values.get("time_based_canary")
        return typing.cast(typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary"], result)

    @builtins.property
    def time_based_linear(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear"]:
        '''time_based_linear block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#time_based_linear CodedeployDeploymentConfig#time_based_linear}
        '''
        result = self._values.get("time_based_linear")
        return typing.cast(typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigTrafficRoutingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentConfigTrafficRoutingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigTrafficRoutingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__537f445acf3ae9d3c1009d08161b3c0ed3c226ce27b43b20ec097a6e2f9d9ef4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimeBasedCanary")
    def put_time_based_canary(
        self,
        *,
        interval: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#interval CodedeployDeploymentConfig#interval}.
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#percentage CodedeployDeploymentConfig#percentage}.
        '''
        value = CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary(
            interval=interval, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putTimeBasedCanary", [value]))

    @jsii.member(jsii_name="putTimeBasedLinear")
    def put_time_based_linear(
        self,
        *,
        interval: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#interval CodedeployDeploymentConfig#interval}.
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#percentage CodedeployDeploymentConfig#percentage}.
        '''
        value = CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear(
            interval=interval, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putTimeBasedLinear", [value]))

    @jsii.member(jsii_name="resetTimeBasedCanary")
    def reset_time_based_canary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeBasedCanary", []))

    @jsii.member(jsii_name="resetTimeBasedLinear")
    def reset_time_based_linear(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeBasedLinear", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="timeBasedCanary")
    def time_based_canary(
        self,
    ) -> "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanaryOutputReference":
        return typing.cast("CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanaryOutputReference", jsii.get(self, "timeBasedCanary"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedLinear")
    def time_based_linear(
        self,
    ) -> "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinearOutputReference":
        return typing.cast("CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinearOutputReference", jsii.get(self, "timeBasedLinear"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedCanaryInput")
    def time_based_canary_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary"]:
        return typing.cast(typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary"], jsii.get(self, "timeBasedCanaryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedLinearInput")
    def time_based_linear_input(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear"]:
        return typing.cast(typing.Optional["CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear"], jsii.get(self, "timeBasedLinearInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e767b150cf50b9d96ded5afe4405484697e25a95b73fe2bdc8fc2f42886345f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfig]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e36ecdf739093252a52cdbe1c85023bf024e208b6d875b23f690f18a2e6ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "percentage": "percentage"},
)
class CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary:
    def __init__(
        self,
        *,
        interval: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#interval CodedeployDeploymentConfig#interval}.
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#percentage CodedeployDeploymentConfig#percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a2addd845c969e0b8277d0a218e9796fc61260dd247c10917f6d9506f8a2f8)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#interval CodedeployDeploymentConfig#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#percentage CodedeployDeploymentConfig#percentage}.'''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanaryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanaryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdd6e249f3b4a05419df427d6e06bfba7beb4c6d253cd53a67232cf5a9ed45bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269587d979f851b82ed1caf818c2be618d68b0cea7761a1408e7d5320261b60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c8f7d9e415e9538c9bbbf8c0200fa5ba4687a7850f60f32d1f23d9b1dd7a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbc60db05bfd6a52d22ee7eb19f7391a0d1d48a11e0a3decc8cd542af007813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "percentage": "percentage"},
)
class CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear:
    def __init__(
        self,
        *,
        interval: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#interval CodedeployDeploymentConfig#interval}.
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#percentage CodedeployDeploymentConfig#percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaac61be9ca80e3b28c23172cb2f6034f5efbfa48e320398ca09021b99ce2939)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#interval CodedeployDeploymentConfig#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#percentage CodedeployDeploymentConfig#percentage}.'''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinearOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinearOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cbdeda9061903800783aa7d3480c0eb1fc0f38b1cc3766f9744b5ff80000016)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a6b41e8d144faa055ccb1f4ecf13694571646e2a1cd454625458836f62e73f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496929c2faee4aed49d37d7f1578b009bf296048ff74d2d299738c56cfcc18d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb2fb9d668b4ce39209411c19345de346114caca25033cc3cb487a577778a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigZonalConfig",
    jsii_struct_bases=[],
    name_mapping={
        "first_zone_monitor_duration_in_seconds": "firstZoneMonitorDurationInSeconds",
        "minimum_healthy_hosts_per_zone": "minimumHealthyHostsPerZone",
        "monitor_duration_in_seconds": "monitorDurationInSeconds",
    },
)
class CodedeployDeploymentConfigZonalConfig:
    def __init__(
        self,
        *,
        first_zone_monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
        minimum_healthy_hosts_per_zone: typing.Optional[typing.Union["CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param first_zone_monitor_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#first_zone_monitor_duration_in_seconds CodedeployDeploymentConfig#first_zone_monitor_duration_in_seconds}.
        :param minimum_healthy_hosts_per_zone: minimum_healthy_hosts_per_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#minimum_healthy_hosts_per_zone CodedeployDeploymentConfig#minimum_healthy_hosts_per_zone}
        :param monitor_duration_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#monitor_duration_in_seconds CodedeployDeploymentConfig#monitor_duration_in_seconds}.
        '''
        if isinstance(minimum_healthy_hosts_per_zone, dict):
            minimum_healthy_hosts_per_zone = CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone(**minimum_healthy_hosts_per_zone)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947a2517a21f904f3670b224b83ad1653147c553daa0ebac02f8be97d0029d3b)
            check_type(argname="argument first_zone_monitor_duration_in_seconds", value=first_zone_monitor_duration_in_seconds, expected_type=type_hints["first_zone_monitor_duration_in_seconds"])
            check_type(argname="argument minimum_healthy_hosts_per_zone", value=minimum_healthy_hosts_per_zone, expected_type=type_hints["minimum_healthy_hosts_per_zone"])
            check_type(argname="argument monitor_duration_in_seconds", value=monitor_duration_in_seconds, expected_type=type_hints["monitor_duration_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if first_zone_monitor_duration_in_seconds is not None:
            self._values["first_zone_monitor_duration_in_seconds"] = first_zone_monitor_duration_in_seconds
        if minimum_healthy_hosts_per_zone is not None:
            self._values["minimum_healthy_hosts_per_zone"] = minimum_healthy_hosts_per_zone
        if monitor_duration_in_seconds is not None:
            self._values["monitor_duration_in_seconds"] = monitor_duration_in_seconds

    @builtins.property
    def first_zone_monitor_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#first_zone_monitor_duration_in_seconds CodedeployDeploymentConfig#first_zone_monitor_duration_in_seconds}.'''
        result = self._values.get("first_zone_monitor_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_healthy_hosts_per_zone(
        self,
    ) -> typing.Optional["CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone"]:
        '''minimum_healthy_hosts_per_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#minimum_healthy_hosts_per_zone CodedeployDeploymentConfig#minimum_healthy_hosts_per_zone}
        '''
        result = self._values.get("minimum_healthy_hosts_per_zone")
        return typing.cast(typing.Optional["CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone"], result)

    @builtins.property
    def monitor_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#monitor_duration_in_seconds CodedeployDeploymentConfig#monitor_duration_in_seconds}.'''
        result = self._values.get("monitor_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigZonalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#value CodedeployDeploymentConfig#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c6020c2ca6b98f47e19a52510d3cae586282efa98fda4f39d7b526d10b8573)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#value CodedeployDeploymentConfig#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9baf2d742cfa0e7666a2f2b2bab37d5323014d89d07ea1ac343635e35878f65f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810bf3a19eb38307962aa670428fc498566a56e282303e13b7abe370545ab66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8b42503c987af544a26e3fe803023847b4b99921a6c00585b64ed4d79f1911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a9f7b4f97a1652cdf12e12c451fea6f8816fd564b73eb70d0ed44119472e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodedeployDeploymentConfigZonalConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codedeployDeploymentConfig.CodedeployDeploymentConfigZonalConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deacfb10668a5cb373978d7705d881e46e050c43c6099073c032482bc470aa93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMinimumHealthyHostsPerZone")
    def put_minimum_healthy_hosts_per_zone(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#type CodedeployDeploymentConfig#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/codedeploy_deployment_config#value CodedeployDeploymentConfig#value}.
        '''
        value_ = CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putMinimumHealthyHostsPerZone", [value_]))

    @jsii.member(jsii_name="resetFirstZoneMonitorDurationInSeconds")
    def reset_first_zone_monitor_duration_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstZoneMonitorDurationInSeconds", []))

    @jsii.member(jsii_name="resetMinimumHealthyHostsPerZone")
    def reset_minimum_healthy_hosts_per_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumHealthyHostsPerZone", []))

    @jsii.member(jsii_name="resetMonitorDurationInSeconds")
    def reset_monitor_duration_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorDurationInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="minimumHealthyHostsPerZone")
    def minimum_healthy_hosts_per_zone(
        self,
    ) -> CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZoneOutputReference:
        return typing.cast(CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZoneOutputReference, jsii.get(self, "minimumHealthyHostsPerZone"))

    @builtins.property
    @jsii.member(jsii_name="firstZoneMonitorDurationInSecondsInput")
    def first_zone_monitor_duration_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstZoneMonitorDurationInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumHealthyHostsPerZoneInput")
    def minimum_healthy_hosts_per_zone_input(
        self,
    ) -> typing.Optional[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone], jsii.get(self, "minimumHealthyHostsPerZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorDurationInSecondsInput")
    def monitor_duration_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monitorDurationInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="firstZoneMonitorDurationInSeconds")
    def first_zone_monitor_duration_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstZoneMonitorDurationInSeconds"))

    @first_zone_monitor_duration_in_seconds.setter
    def first_zone_monitor_duration_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734cb460e0b7a1f08e77c69d92fc6bad5ef37d2ce42f48b0124bff825e7752a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstZoneMonitorDurationInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorDurationInSeconds")
    def monitor_duration_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitorDurationInSeconds"))

    @monitor_duration_in_seconds.setter
    def monitor_duration_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba9248245006d8c7a10a5bfe0a31a30c7c20cdde125c5a7f8d71ced04f4f8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorDurationInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodedeployDeploymentConfigZonalConfig]:
        return typing.cast(typing.Optional[CodedeployDeploymentConfigZonalConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodedeployDeploymentConfigZonalConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04daeb70c10bfbb16c9a9d2c90b374ecb8779ef7b310f02e333f5b6e4e0dc3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CodedeployDeploymentConfig",
    "CodedeployDeploymentConfigConfig",
    "CodedeployDeploymentConfigMinimumHealthyHosts",
    "CodedeployDeploymentConfigMinimumHealthyHostsOutputReference",
    "CodedeployDeploymentConfigTrafficRoutingConfig",
    "CodedeployDeploymentConfigTrafficRoutingConfigOutputReference",
    "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary",
    "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanaryOutputReference",
    "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear",
    "CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinearOutputReference",
    "CodedeployDeploymentConfigZonalConfig",
    "CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone",
    "CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZoneOutputReference",
    "CodedeployDeploymentConfigZonalConfigOutputReference",
]

publication.publish()

def _typecheckingstub__97fecb089dffe43959612f288f6a5bc69cdaf53ef75a4ab90b823c83e1353e52(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    deployment_config_name: builtins.str,
    compute_platform: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_healthy_hosts: typing.Optional[typing.Union[CodedeployDeploymentConfigMinimumHealthyHosts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_routing_config: typing.Optional[typing.Union[CodedeployDeploymentConfigTrafficRoutingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    zonal_config: typing.Optional[typing.Union[CodedeployDeploymentConfigZonalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2d75f8bc6620fa5736e4d976208eba64929957cd2b50211e49b33d266aa1fc2b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ab34b4b67ce9fae91167a1d102c6d5913bbb4ea2c868998af329ad1c401d7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ce897e0e8b1737defa00f45218a0f286bfb1476e11fabf7cb6e0ec4f19e365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd197eb1845cf7cb44b56d73d102ada5b005dcac83778c7e7f6b74acb3f37db6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb67ecf3cf6c0ea7515a90d8f9a89afcf33be7c62526ed4811d5ad3bbeb6f454(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deployment_config_name: builtins.str,
    compute_platform: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_healthy_hosts: typing.Optional[typing.Union[CodedeployDeploymentConfigMinimumHealthyHosts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_routing_config: typing.Optional[typing.Union[CodedeployDeploymentConfigTrafficRoutingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    zonal_config: typing.Optional[typing.Union[CodedeployDeploymentConfigZonalConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ff7b7bf8d3d23c171065321f8250ccfd6c0612958b8bbe995d7f8632552285(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2cb4dc5d2e05da5f74342937009c38ec3d941c2da0c522c897e4fbfd27cca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59adb5d64bba30d08a4428b442c1efc94a2fd08a03d1a6dde3516adef143c85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3e521803b84d2595cdba93d18d47ffc40ecc30234a5203c65fb096fef112c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b7bd3b987a6019e5e38b47651a6e26c6c032cd1a8725baac8344e17e71f75c(
    value: typing.Optional[CodedeployDeploymentConfigMinimumHealthyHosts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7400a578c53bd4560ae4ee4c949bf476b63f4d08cb71e42e22104092e6419b(
    *,
    time_based_canary: typing.Optional[typing.Union[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary, typing.Dict[builtins.str, typing.Any]]] = None,
    time_based_linear: typing.Optional[typing.Union[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537f445acf3ae9d3c1009d08161b3c0ed3c226ce27b43b20ec097a6e2f9d9ef4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e767b150cf50b9d96ded5afe4405484697e25a95b73fe2bdc8fc2f42886345f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e36ecdf739093252a52cdbe1c85023bf024e208b6d875b23f690f18a2e6ad9(
    value: typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a2addd845c969e0b8277d0a218e9796fc61260dd247c10917f6d9506f8a2f8(
    *,
    interval: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd6e249f3b4a05419df427d6e06bfba7beb4c6d253cd53a67232cf5a9ed45bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269587d979f851b82ed1caf818c2be618d68b0cea7761a1408e7d5320261b60d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c8f7d9e415e9538c9bbbf8c0200fa5ba4687a7850f60f32d1f23d9b1dd7a41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbc60db05bfd6a52d22ee7eb19f7391a0d1d48a11e0a3decc8cd542af007813(
    value: typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedCanary],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaac61be9ca80e3b28c23172cb2f6034f5efbfa48e320398ca09021b99ce2939(
    *,
    interval: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbdeda9061903800783aa7d3480c0eb1fc0f38b1cc3766f9744b5ff80000016(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a6b41e8d144faa055ccb1f4ecf13694571646e2a1cd454625458836f62e73f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496929c2faee4aed49d37d7f1578b009bf296048ff74d2d299738c56cfcc18d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb2fb9d668b4ce39209411c19345de346114caca25033cc3cb487a577778a81(
    value: typing.Optional[CodedeployDeploymentConfigTrafficRoutingConfigTimeBasedLinear],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947a2517a21f904f3670b224b83ad1653147c553daa0ebac02f8be97d0029d3b(
    *,
    first_zone_monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
    minimum_healthy_hosts_per_zone: typing.Optional[typing.Union[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c6020c2ca6b98f47e19a52510d3cae586282efa98fda4f39d7b526d10b8573(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9baf2d742cfa0e7666a2f2b2bab37d5323014d89d07ea1ac343635e35878f65f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810bf3a19eb38307962aa670428fc498566a56e282303e13b7abe370545ab66a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8b42503c987af544a26e3fe803023847b4b99921a6c00585b64ed4d79f1911(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a9f7b4f97a1652cdf12e12c451fea6f8816fd564b73eb70d0ed44119472e28(
    value: typing.Optional[CodedeployDeploymentConfigZonalConfigMinimumHealthyHostsPerZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deacfb10668a5cb373978d7705d881e46e050c43c6099073c032482bc470aa93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734cb460e0b7a1f08e77c69d92fc6bad5ef37d2ce42f48b0124bff825e7752a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba9248245006d8c7a10a5bfe0a31a30c7c20cdde125c5a7f8d71ced04f4f8f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04daeb70c10bfbb16c9a9d2c90b374ecb8779ef7b310f02e333f5b6e4e0dc3e2(
    value: typing.Optional[CodedeployDeploymentConfigZonalConfig],
) -> None:
    """Type checking stubs"""
    pass
