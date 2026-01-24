r'''
# `aws_emrserverless_application`

Refer to the Terraform Registry for docs: [`aws_emrserverless_application`](https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application).
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


class EmrserverlessApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application aws_emrserverless_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        release_label: builtins.str,
        type: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union["EmrserverlessApplicationAutoStartConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union["EmrserverlessApplicationAutoStopConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image_configuration: typing.Optional[typing.Union["EmrserverlessApplicationImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationInitialCapacity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        interactive_configuration: typing.Optional[typing.Union["EmrserverlessApplicationInteractiveConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_capacity: typing.Optional[typing.Union["EmrserverlessApplicationMaximumCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_configuration: typing.Optional[typing.Union["EmrserverlessApplicationNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationRuntimeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduler_configuration: typing.Optional[typing.Union["EmrserverlessApplicationSchedulerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application aws_emrserverless_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#release_label EmrserverlessApplication#release_label}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#type EmrserverlessApplication#type}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#architecture EmrserverlessApplication#architecture}.
        :param auto_start_configuration: auto_start_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#auto_start_configuration EmrserverlessApplication#auto_start_configuration}
        :param auto_stop_configuration: auto_stop_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#auto_stop_configuration EmrserverlessApplication#auto_stop_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#id EmrserverlessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_configuration: image_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#image_configuration EmrserverlessApplication#image_configuration}
        :param initial_capacity: initial_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity EmrserverlessApplication#initial_capacity}
        :param interactive_configuration: interactive_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#interactive_configuration EmrserverlessApplication#interactive_configuration}
        :param maximum_capacity: maximum_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#maximum_capacity EmrserverlessApplication#maximum_capacity}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#monitoring_configuration EmrserverlessApplication#monitoring_configuration}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#network_configuration EmrserverlessApplication#network_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#region EmrserverlessApplication#region}
        :param runtime_configuration: runtime_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#runtime_configuration EmrserverlessApplication#runtime_configuration}
        :param scheduler_configuration: scheduler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#scheduler_configuration EmrserverlessApplication#scheduler_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#tags EmrserverlessApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#tags_all EmrserverlessApplication#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df9bccdfbfdf93f5315409f44cd957e5f280b30610084c850a05783a46d5416)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EmrserverlessApplicationConfig(
            name=name,
            release_label=release_label,
            type=type,
            architecture=architecture,
            auto_start_configuration=auto_start_configuration,
            auto_stop_configuration=auto_stop_configuration,
            id=id,
            image_configuration=image_configuration,
            initial_capacity=initial_capacity,
            interactive_configuration=interactive_configuration,
            maximum_capacity=maximum_capacity,
            monitoring_configuration=monitoring_configuration,
            network_configuration=network_configuration,
            region=region,
            runtime_configuration=runtime_configuration,
            scheduler_configuration=scheduler_configuration,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a EmrserverlessApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EmrserverlessApplication to import.
        :param import_from_id: The id of the existing EmrserverlessApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EmrserverlessApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9352b6f8885088571c3a23eed26dfcbe559acb5caa0fea530dcc47bf71fb849)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutoStartConfiguration")
    def put_auto_start_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        '''
        value = EmrserverlessApplicationAutoStartConfiguration(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAutoStartConfiguration", [value]))

    @jsii.member(jsii_name="putAutoStopConfiguration")
    def put_auto_stop_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param idle_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#idle_timeout_minutes EmrserverlessApplication#idle_timeout_minutes}.
        '''
        value = EmrserverlessApplicationAutoStopConfiguration(
            enabled=enabled, idle_timeout_minutes=idle_timeout_minutes
        )

        return typing.cast(None, jsii.invoke(self, "putAutoStopConfiguration", [value]))

    @jsii.member(jsii_name="putImageConfiguration")
    def put_image_configuration(self, *, image_uri: builtins.str) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#image_uri EmrserverlessApplication#image_uri}.
        '''
        value = EmrserverlessApplicationImageConfiguration(image_uri=image_uri)

        return typing.cast(None, jsii.invoke(self, "putImageConfiguration", [value]))

    @jsii.member(jsii_name="putInitialCapacity")
    def put_initial_capacity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationInitialCapacity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7e05b2339cb096cca79fcf6d2fe21bf431036b2d4260dcc6212df2ee181922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitialCapacity", [value]))

    @jsii.member(jsii_name="putInteractiveConfiguration")
    def put_interactive_configuration(
        self,
        *,
        livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        studio_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param livy_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#livy_endpoint_enabled EmrserverlessApplication#livy_endpoint_enabled}.
        :param studio_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#studio_enabled EmrserverlessApplication#studio_enabled}.
        '''
        value = EmrserverlessApplicationInteractiveConfiguration(
            livy_endpoint_enabled=livy_endpoint_enabled, studio_enabled=studio_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putInteractiveConfiguration", [value]))

    @jsii.member(jsii_name="putMaximumCapacity")
    def put_maximum_capacity(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        value = EmrserverlessApplicationMaximumCapacity(
            cpu=cpu, memory=memory, disk=disk
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumCapacity", [value]))

    @jsii.member(jsii_name="putMonitoringConfiguration")
    def put_monitoring_configuration(
        self,
        *,
        cloudwatch_logging_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_persistence_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        prometheus_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logging_configuration: cloudwatch_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cloudwatch_logging_configuration EmrserverlessApplication#cloudwatch_logging_configuration}
        :param managed_persistence_monitoring_configuration: managed_persistence_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#managed_persistence_monitoring_configuration EmrserverlessApplication#managed_persistence_monitoring_configuration}
        :param prometheus_monitoring_configuration: prometheus_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#prometheus_monitoring_configuration EmrserverlessApplication#prometheus_monitoring_configuration}
        :param s3_monitoring_configuration: s3_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#s3_monitoring_configuration EmrserverlessApplication#s3_monitoring_configuration}
        '''
        value = EmrserverlessApplicationMonitoringConfiguration(
            cloudwatch_logging_configuration=cloudwatch_logging_configuration,
            managed_persistence_monitoring_configuration=managed_persistence_monitoring_configuration,
            prometheus_monitoring_configuration=prometheus_monitoring_configuration,
            s3_monitoring_configuration=s3_monitoring_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putNetworkConfiguration")
    def put_network_configuration(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#security_group_ids EmrserverlessApplication#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#subnet_ids EmrserverlessApplication#subnet_ids}.
        '''
        value = EmrserverlessApplicationNetworkConfiguration(
            security_group_ids=security_group_ids, subnet_ids=subnet_ids
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfiguration", [value]))

    @jsii.member(jsii_name="putRuntimeConfiguration")
    def put_runtime_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationRuntimeConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0c01fff4c4cc069d850f064091b80484d466cc44d03f25c919434d792664a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRuntimeConfiguration", [value]))

    @jsii.member(jsii_name="putSchedulerConfiguration")
    def put_scheduler_configuration(
        self,
        *,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        queue_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_runs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#max_concurrent_runs EmrserverlessApplication#max_concurrent_runs}.
        :param queue_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#queue_timeout_minutes EmrserverlessApplication#queue_timeout_minutes}.
        '''
        value = EmrserverlessApplicationSchedulerConfiguration(
            max_concurrent_runs=max_concurrent_runs,
            queue_timeout_minutes=queue_timeout_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedulerConfiguration", [value]))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetAutoStartConfiguration")
    def reset_auto_start_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStartConfiguration", []))

    @jsii.member(jsii_name="resetAutoStopConfiguration")
    def reset_auto_stop_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStopConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageConfiguration")
    def reset_image_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageConfiguration", []))

    @jsii.member(jsii_name="resetInitialCapacity")
    def reset_initial_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialCapacity", []))

    @jsii.member(jsii_name="resetInteractiveConfiguration")
    def reset_interactive_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInteractiveConfiguration", []))

    @jsii.member(jsii_name="resetMaximumCapacity")
    def reset_maximum_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumCapacity", []))

    @jsii.member(jsii_name="resetMonitoringConfiguration")
    def reset_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetNetworkConfiguration")
    def reset_network_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRuntimeConfiguration")
    def reset_runtime_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeConfiguration", []))

    @jsii.member(jsii_name="resetSchedulerConfiguration")
    def reset_scheduler_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="autoStartConfiguration")
    def auto_start_configuration(
        self,
    ) -> "EmrserverlessApplicationAutoStartConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationAutoStartConfigurationOutputReference", jsii.get(self, "autoStartConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="autoStopConfiguration")
    def auto_stop_configuration(
        self,
    ) -> "EmrserverlessApplicationAutoStopConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationAutoStopConfigurationOutputReference", jsii.get(self, "autoStopConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="imageConfiguration")
    def image_configuration(
        self,
    ) -> "EmrserverlessApplicationImageConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationImageConfigurationOutputReference", jsii.get(self, "imageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacity")
    def initial_capacity(self) -> "EmrserverlessApplicationInitialCapacityList":
        return typing.cast("EmrserverlessApplicationInitialCapacityList", jsii.get(self, "initialCapacity"))

    @builtins.property
    @jsii.member(jsii_name="interactiveConfiguration")
    def interactive_configuration(
        self,
    ) -> "EmrserverlessApplicationInteractiveConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationInteractiveConfigurationOutputReference", jsii.get(self, "interactiveConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="maximumCapacity")
    def maximum_capacity(
        self,
    ) -> "EmrserverlessApplicationMaximumCapacityOutputReference":
        return typing.cast("EmrserverlessApplicationMaximumCapacityOutputReference", jsii.get(self, "maximumCapacity"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfiguration")
    def monitoring_configuration(
        self,
    ) -> "EmrserverlessApplicationMonitoringConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationOutputReference", jsii.get(self, "monitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> "EmrserverlessApplicationNetworkConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationNetworkConfigurationOutputReference", jsii.get(self, "networkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfiguration")
    def runtime_configuration(
        self,
    ) -> "EmrserverlessApplicationRuntimeConfigurationList":
        return typing.cast("EmrserverlessApplicationRuntimeConfigurationList", jsii.get(self, "runtimeConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="schedulerConfiguration")
    def scheduler_configuration(
        self,
    ) -> "EmrserverlessApplicationSchedulerConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationSchedulerConfigurationOutputReference", jsii.get(self, "schedulerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStartConfigurationInput")
    def auto_start_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationAutoStartConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationAutoStartConfiguration"], jsii.get(self, "autoStartConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStopConfigurationInput")
    def auto_stop_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationAutoStopConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationAutoStopConfiguration"], jsii.get(self, "autoStopConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageConfigurationInput")
    def image_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationImageConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationImageConfiguration"], jsii.get(self, "imageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityInput")
    def initial_capacity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]], jsii.get(self, "initialCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="interactiveConfigurationInput")
    def interactive_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInteractiveConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationInteractiveConfiguration"], jsii.get(self, "interactiveConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumCapacityInput")
    def maximum_capacity_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMaximumCapacity"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMaximumCapacity"], jsii.get(self, "maximumCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfigurationInput")
    def monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfiguration"], jsii.get(self, "monitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationInput")
    def network_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationNetworkConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationNetworkConfiguration"], jsii.get(self, "networkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="releaseLabelInput")
    def release_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "releaseLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigurationInput")
    def runtime_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]], jsii.get(self, "runtimeConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerConfigurationInput")
    def scheduler_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationSchedulerConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationSchedulerConfiguration"], jsii.get(self, "schedulerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f49030a456f2b5539b6276180ab2808f7fe23f4185dabedcc7b0e679d040b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11324e1d03f2dc067ede8c964ffabf8843b143584a09ebb1d145208a89d81b71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c92979a2e53e806bf61b4ebdb1a8631d78d79a7a39b0498e656d49687e626ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bca54c289016f6f63c8e07e406ba7cb453391c54c863508d48df0376b40e21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="releaseLabel")
    def release_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "releaseLabel"))

    @release_label.setter
    def release_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bc1ab4302375629243c2a9fa5d6259cfb9d11ea937a354932e626512b7b45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d611a5b628ebbbc389d4dea4f2266b2a5abd4bdc12466467102beae62c4c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c1d180d226837117a313d0e9265770fef37912cb6743ed00fe743e017288a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a34c4fab2e07a3d5800801503744b181fbadb66748f43a6f731fcf634561a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStartConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class EmrserverlessApplicationAutoStartConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711adc9a70854729f54a13f0e3159d31c4f91ca65924f40f57dd36d442fdc8d0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationAutoStartConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationAutoStartConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStartConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef37e49bfa3d4216f2d547e9aa6a3d07b1cddfb1fe020464f695af6bb745c81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__455bf80d3251b9c3160119b571f6269ce1920c00bcb4345aa49c4a0d9f6e6de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStartConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStartConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationAutoStartConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf7768923180cb1f3c9dfe0a7fa67e78a87f0ecba6ce5654221bd210131f4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStopConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "idle_timeout_minutes": "idleTimeoutMinutes"},
)
class EmrserverlessApplicationAutoStopConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        idle_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param idle_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#idle_timeout_minutes EmrserverlessApplication#idle_timeout_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f606597533d046e346c92c83226fe23ca8c1554f90d3dd534e13d3fb2d7ca78)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument idle_timeout_minutes", value=idle_timeout_minutes, expected_type=type_hints["idle_timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if idle_timeout_minutes is not None:
            self._values["idle_timeout_minutes"] = idle_timeout_minutes

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def idle_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#idle_timeout_minutes EmrserverlessApplication#idle_timeout_minutes}.'''
        result = self._values.get("idle_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationAutoStopConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationAutoStopConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationAutoStopConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74d26e7db4ea3e74daa1926f0fb541b56b6de3e99ea63d26d4c2e9ad4df1188a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIdleTimeoutMinutes")
    def reset_idle_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeoutMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutMinutesInput")
    def idle_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleTimeoutMinutesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b680a022d907eb91f665725dcfe88afe429733dd000ddbf481b317fca29e2f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutMinutes")
    def idle_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleTimeoutMinutes"))

    @idle_timeout_minutes.setter
    def idle_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27e3a3c9b20251c6e4bd3c66b16b65aaf995a444d4455f79d4657f16b08fd3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStopConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStopConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationAutoStopConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8244577ce2ca28471eadbcd403671faf8181aa61e7b05dd4daabdd16da4ddf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "release_label": "releaseLabel",
        "type": "type",
        "architecture": "architecture",
        "auto_start_configuration": "autoStartConfiguration",
        "auto_stop_configuration": "autoStopConfiguration",
        "id": "id",
        "image_configuration": "imageConfiguration",
        "initial_capacity": "initialCapacity",
        "interactive_configuration": "interactiveConfiguration",
        "maximum_capacity": "maximumCapacity",
        "monitoring_configuration": "monitoringConfiguration",
        "network_configuration": "networkConfiguration",
        "region": "region",
        "runtime_configuration": "runtimeConfiguration",
        "scheduler_configuration": "schedulerConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class EmrserverlessApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        release_label: builtins.str,
        type: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStartConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStopConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        image_configuration: typing.Optional[typing.Union["EmrserverlessApplicationImageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationInitialCapacity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        interactive_configuration: typing.Optional[typing.Union["EmrserverlessApplicationInteractiveConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_capacity: typing.Optional[typing.Union["EmrserverlessApplicationMaximumCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        network_configuration: typing.Optional[typing.Union["EmrserverlessApplicationNetworkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationRuntimeConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduler_configuration: typing.Optional[typing.Union["EmrserverlessApplicationSchedulerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.
        :param release_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#release_label EmrserverlessApplication#release_label}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#type EmrserverlessApplication#type}.
        :param architecture: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#architecture EmrserverlessApplication#architecture}.
        :param auto_start_configuration: auto_start_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#auto_start_configuration EmrserverlessApplication#auto_start_configuration}
        :param auto_stop_configuration: auto_stop_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#auto_stop_configuration EmrserverlessApplication#auto_stop_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#id EmrserverlessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_configuration: image_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#image_configuration EmrserverlessApplication#image_configuration}
        :param initial_capacity: initial_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity EmrserverlessApplication#initial_capacity}
        :param interactive_configuration: interactive_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#interactive_configuration EmrserverlessApplication#interactive_configuration}
        :param maximum_capacity: maximum_capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#maximum_capacity EmrserverlessApplication#maximum_capacity}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#monitoring_configuration EmrserverlessApplication#monitoring_configuration}
        :param network_configuration: network_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#network_configuration EmrserverlessApplication#network_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#region EmrserverlessApplication#region}
        :param runtime_configuration: runtime_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#runtime_configuration EmrserverlessApplication#runtime_configuration}
        :param scheduler_configuration: scheduler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#scheduler_configuration EmrserverlessApplication#scheduler_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#tags EmrserverlessApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#tags_all EmrserverlessApplication#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auto_start_configuration, dict):
            auto_start_configuration = EmrserverlessApplicationAutoStartConfiguration(**auto_start_configuration)
        if isinstance(auto_stop_configuration, dict):
            auto_stop_configuration = EmrserverlessApplicationAutoStopConfiguration(**auto_stop_configuration)
        if isinstance(image_configuration, dict):
            image_configuration = EmrserverlessApplicationImageConfiguration(**image_configuration)
        if isinstance(interactive_configuration, dict):
            interactive_configuration = EmrserverlessApplicationInteractiveConfiguration(**interactive_configuration)
        if isinstance(maximum_capacity, dict):
            maximum_capacity = EmrserverlessApplicationMaximumCapacity(**maximum_capacity)
        if isinstance(monitoring_configuration, dict):
            monitoring_configuration = EmrserverlessApplicationMonitoringConfiguration(**monitoring_configuration)
        if isinstance(network_configuration, dict):
            network_configuration = EmrserverlessApplicationNetworkConfiguration(**network_configuration)
        if isinstance(scheduler_configuration, dict):
            scheduler_configuration = EmrserverlessApplicationSchedulerConfiguration(**scheduler_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9110adb97c1b412ea08fd61c6fffd9e9ed1a69090c3dbcf77adbee5f5658f9e7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_start_configuration", value=auto_start_configuration, expected_type=type_hints["auto_start_configuration"])
            check_type(argname="argument auto_stop_configuration", value=auto_stop_configuration, expected_type=type_hints["auto_stop_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            check_type(argname="argument initial_capacity", value=initial_capacity, expected_type=type_hints["initial_capacity"])
            check_type(argname="argument interactive_configuration", value=interactive_configuration, expected_type=type_hints["interactive_configuration"])
            check_type(argname="argument maximum_capacity", value=maximum_capacity, expected_type=type_hints["maximum_capacity"])
            check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument runtime_configuration", value=runtime_configuration, expected_type=type_hints["runtime_configuration"])
            check_type(argname="argument scheduler_configuration", value=scheduler_configuration, expected_type=type_hints["scheduler_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "release_label": release_label,
            "type": type,
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
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_start_configuration is not None:
            self._values["auto_start_configuration"] = auto_start_configuration
        if auto_stop_configuration is not None:
            self._values["auto_stop_configuration"] = auto_stop_configuration
        if id is not None:
            self._values["id"] = id
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration
        if initial_capacity is not None:
            self._values["initial_capacity"] = initial_capacity
        if interactive_configuration is not None:
            self._values["interactive_configuration"] = interactive_configuration
        if maximum_capacity is not None:
            self._values["maximum_capacity"] = maximum_capacity
        if monitoring_configuration is not None:
            self._values["monitoring_configuration"] = monitoring_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if region is not None:
            self._values["region"] = region
        if runtime_configuration is not None:
            self._values["runtime_configuration"] = runtime_configuration
        if scheduler_configuration is not None:
            self._values["scheduler_configuration"] = scheduler_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_label(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#release_label EmrserverlessApplication#release_label}.'''
        result = self._values.get("release_label")
        assert result is not None, "Required property 'release_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#type EmrserverlessApplication#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#architecture EmrserverlessApplication#architecture}.'''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_start_configuration(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStartConfiguration]:
        '''auto_start_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#auto_start_configuration EmrserverlessApplication#auto_start_configuration}
        '''
        result = self._values.get("auto_start_configuration")
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStartConfiguration], result)

    @builtins.property
    def auto_stop_configuration(
        self,
    ) -> typing.Optional[EmrserverlessApplicationAutoStopConfiguration]:
        '''auto_stop_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#auto_stop_configuration EmrserverlessApplication#auto_stop_configuration}
        '''
        result = self._values.get("auto_stop_configuration")
        return typing.cast(typing.Optional[EmrserverlessApplicationAutoStopConfiguration], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#id EmrserverlessApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationImageConfiguration"]:
        '''image_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#image_configuration EmrserverlessApplication#image_configuration}
        '''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationImageConfiguration"], result)

    @builtins.property
    def initial_capacity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]]:
        '''initial_capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity EmrserverlessApplication#initial_capacity}
        '''
        result = self._values.get("initial_capacity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationInitialCapacity"]]], result)

    @builtins.property
    def interactive_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInteractiveConfiguration"]:
        '''interactive_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#interactive_configuration EmrserverlessApplication#interactive_configuration}
        '''
        result = self._values.get("interactive_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationInteractiveConfiguration"], result)

    @builtins.property
    def maximum_capacity(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMaximumCapacity"]:
        '''maximum_capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#maximum_capacity EmrserverlessApplication#maximum_capacity}
        '''
        result = self._values.get("maximum_capacity")
        return typing.cast(typing.Optional["EmrserverlessApplicationMaximumCapacity"], result)

    @builtins.property
    def monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfiguration"]:
        '''monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#monitoring_configuration EmrserverlessApplication#monitoring_configuration}
        '''
        result = self._values.get("monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfiguration"], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationNetworkConfiguration"]:
        '''network_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#network_configuration EmrserverlessApplication#network_configuration}
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationNetworkConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#region EmrserverlessApplication#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]]:
        '''runtime_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#runtime_configuration EmrserverlessApplication#runtime_configuration}
        '''
        result = self._values.get("runtime_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationRuntimeConfiguration"]]], result)

    @builtins.property
    def scheduler_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationSchedulerConfiguration"]:
        '''scheduler_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#scheduler_configuration EmrserverlessApplication#scheduler_configuration}
        '''
        result = self._values.get("scheduler_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationSchedulerConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#tags EmrserverlessApplication#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#tags_all EmrserverlessApplication#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationImageConfiguration",
    jsii_struct_bases=[],
    name_mapping={"image_uri": "imageUri"},
)
class EmrserverlessApplicationImageConfiguration:
    def __init__(self, *, image_uri: builtins.str) -> None:
        '''
        :param image_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#image_uri EmrserverlessApplication#image_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88364ebbb88e6f3cc5aa80d2d1ea3013facb713e1d2d6ff18c77a47cd73db455)
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_uri": image_uri,
        }

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#image_uri EmrserverlessApplication#image_uri}.'''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationImageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationImageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationImageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d614bac5a243d74686f8f994a9cd976f8e16f8e9244d9beab4d38cbe83c20e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0033bea57ff592b3ea8f2d2105cbcbdc54b2287ee63244124d545206044ae31e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationImageConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationImageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationImageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906aed13023e42d70c26dca045452acbd4f448a310a2314592d2f068736189e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacity",
    jsii_struct_bases=[],
    name_mapping={
        "initial_capacity_type": "initialCapacityType",
        "initial_capacity_config": "initialCapacityConfig",
    },
)
class EmrserverlessApplicationInitialCapacity:
    def __init__(
        self,
        *,
        initial_capacity_type: builtins.str,
        initial_capacity_config: typing.Optional[typing.Union["EmrserverlessApplicationInitialCapacityInitialCapacityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param initial_capacity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity_type EmrserverlessApplication#initial_capacity_type}.
        :param initial_capacity_config: initial_capacity_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity_config EmrserverlessApplication#initial_capacity_config}
        '''
        if isinstance(initial_capacity_config, dict):
            initial_capacity_config = EmrserverlessApplicationInitialCapacityInitialCapacityConfig(**initial_capacity_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8fa572c37ec26d6aa4c398a7c687c856693006d42fa026f764b03f35a4cf0e)
            check_type(argname="argument initial_capacity_type", value=initial_capacity_type, expected_type=type_hints["initial_capacity_type"])
            check_type(argname="argument initial_capacity_config", value=initial_capacity_config, expected_type=type_hints["initial_capacity_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "initial_capacity_type": initial_capacity_type,
        }
        if initial_capacity_config is not None:
            self._values["initial_capacity_config"] = initial_capacity_config

    @builtins.property
    def initial_capacity_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity_type EmrserverlessApplication#initial_capacity_type}.'''
        result = self._values.get("initial_capacity_type")
        assert result is not None, "Required property 'initial_capacity_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_capacity_config(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfig"]:
        '''initial_capacity_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#initial_capacity_config EmrserverlessApplication#initial_capacity_config}
        '''
        result = self._values.get("initial_capacity_config")
        return typing.cast(typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInitialCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "worker_count": "workerCount",
        "worker_configuration": "workerConfiguration",
    },
)
class EmrserverlessApplicationInitialCapacityInitialCapacityConfig:
    def __init__(
        self,
        *,
        worker_count: jsii.Number,
        worker_configuration: typing.Optional[typing.Union["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#worker_count EmrserverlessApplication#worker_count}.
        :param worker_configuration: worker_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#worker_configuration EmrserverlessApplication#worker_configuration}
        '''
        if isinstance(worker_configuration, dict):
            worker_configuration = EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration(**worker_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3137ea7acf2b38e736f43d991d62a5d680982c4770134eb3f296da599e7748cd)
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "worker_count": worker_count,
        }
        if worker_configuration is not None:
            self._values["worker_configuration"] = worker_configuration

    @builtins.property
    def worker_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#worker_count EmrserverlessApplication#worker_count}.'''
        result = self._values.get("worker_count")
        assert result is not None, "Required property 'worker_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def worker_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"]:
        '''worker_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#worker_configuration EmrserverlessApplication#worker_configuration}
        '''
        result = self._values.get("worker_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInitialCapacityInitialCapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23832c10a2ba6a0a085009e9bb513e8679491068dbaf3f95d9ff9ccd09d8c773)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWorkerConfiguration")
    def put_worker_configuration(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        value = EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration(
            cpu=cpu, memory=memory, disk=disk
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfiguration", [value]))

    @jsii.member(jsii_name="resetWorkerConfiguration")
    def reset_worker_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="workerConfiguration")
    def worker_configuration(
        self,
    ) -> "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference", jsii.get(self, "workerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigurationInput")
    def worker_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration"], jsii.get(self, "workerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCountInput")
    def worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @worker_count.setter
    def worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7362d9841e0dc977d0a705422aae81a4df82c0f1ce83e7f97c67ca5af5b2dd56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6458e504443767ec382d5631c23a5d787be994cadf3c8b098b3400e630d953ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory", "disk": "disk"},
)
class EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration:
    def __init__(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037dbf4eee9f5d069ca18fda50e3200e441002fca4bbfef958ec0c1d5554b51f)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "memory": memory,
        }
        if disk is not None:
            self._values["disk"] = disk

    @builtins.property
    def cpu(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.'''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.'''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.'''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8cf4b89a131f61095c8dfd8f8c8bf1d8e0e67b18b0f0cbc9663a4d70e186bd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863ec41233987f791b662cb7177a3811e5f12e01d8e8c1a7dd7a43e199b48880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc485f1fdf86d6100a3faa12910e6f8fc3edaa7d72c81a3b2998bf4a4c744dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06913e3c43ad7d6114463f2c7376f00514ded1db980fc9e61c93773fd4b47f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d732da70ad29607ead222879f410e911126b5b6fcf585d715b2cb67dceec5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationInitialCapacityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc7407e074afea99fba7bfad693b5d8339303dd1e1ef6a20d3a1c4b3b7017eaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrserverlessApplicationInitialCapacityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c0a2fa85432655e0fdb947739a7fa8c1c1fbc587b930b7e786348e19592ba4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrserverlessApplicationInitialCapacityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522f152fa762fc57fe3ee5d9c73d071e065df784828c2715bcb1686171d42b26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3173d8881fff75790857d4e2aa869618392148842abd5200116a3d57efec52ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abff6195556794c9b9532e440ea4952925318e6701a54fcfae763f6f57371ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4d982571785c047dd66cf1eb2af442df039c1d23c17523a771b3aa81c77c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationInitialCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInitialCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__940e15624a49afa4241fd5cb9efa5627f6f8cadacd09250d964da6b40a5d3cd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInitialCapacityConfig")
    def put_initial_capacity_config(
        self,
        *,
        worker_count: jsii.Number,
        worker_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param worker_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#worker_count EmrserverlessApplication#worker_count}.
        :param worker_configuration: worker_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#worker_configuration EmrserverlessApplication#worker_configuration}
        '''
        value = EmrserverlessApplicationInitialCapacityInitialCapacityConfig(
            worker_count=worker_count, worker_configuration=worker_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putInitialCapacityConfig", [value]))

    @jsii.member(jsii_name="resetInitialCapacityConfig")
    def reset_initial_capacity_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialCapacityConfig", []))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityConfig")
    def initial_capacity_config(
        self,
    ) -> EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference:
        return typing.cast(EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference, jsii.get(self, "initialCapacityConfig"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityConfigInput")
    def initial_capacity_config_input(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig], jsii.get(self, "initialCapacityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityTypeInput")
    def initial_capacity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initialCapacityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="initialCapacityType")
    def initial_capacity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialCapacityType"))

    @initial_capacity_type.setter
    def initial_capacity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78b406f2f0d9c2ae747c28435bc901ce8054f1c1775719a37c7425c6d6e7a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialCapacityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68439f6ecd07de6cf2e8a512f5c4484f1dd9a69a27f274563f08bd110c10eab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInteractiveConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "livy_endpoint_enabled": "livyEndpointEnabled",
        "studio_enabled": "studioEnabled",
    },
)
class EmrserverlessApplicationInteractiveConfiguration:
    def __init__(
        self,
        *,
        livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        studio_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param livy_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#livy_endpoint_enabled EmrserverlessApplication#livy_endpoint_enabled}.
        :param studio_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#studio_enabled EmrserverlessApplication#studio_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd73c16ad7904d28a4937186eb6fcc11155df7201a7d26f1e20d26ba60a7170b)
            check_type(argname="argument livy_endpoint_enabled", value=livy_endpoint_enabled, expected_type=type_hints["livy_endpoint_enabled"])
            check_type(argname="argument studio_enabled", value=studio_enabled, expected_type=type_hints["studio_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if livy_endpoint_enabled is not None:
            self._values["livy_endpoint_enabled"] = livy_endpoint_enabled
        if studio_enabled is not None:
            self._values["studio_enabled"] = studio_enabled

    @builtins.property
    def livy_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#livy_endpoint_enabled EmrserverlessApplication#livy_endpoint_enabled}.'''
        result = self._values.get("livy_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def studio_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#studio_enabled EmrserverlessApplication#studio_enabled}.'''
        result = self._values.get("studio_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationInteractiveConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationInteractiveConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationInteractiveConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3597c3c78db1fd69c0f10e49002d874ee7101aa4d08d84c496f194ccd566ae5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLivyEndpointEnabled")
    def reset_livy_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivyEndpointEnabled", []))

    @jsii.member(jsii_name="resetStudioEnabled")
    def reset_studio_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStudioEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="livyEndpointEnabledInput")
    def livy_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "livyEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="studioEnabledInput")
    def studio_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "studioEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="livyEndpointEnabled")
    def livy_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "livyEndpointEnabled"))

    @livy_endpoint_enabled.setter
    def livy_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdabe0c212b1c0ad9f14e909a3f7cf4c6eb913a79863ce0ebeefc38d2f4f5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "livyEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="studioEnabled")
    def studio_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "studioEnabled"))

    @studio_enabled.setter
    def studio_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ff08a1a96584d4521a330f984754fbd6608005e02cfd4455a6ba29b8b0c075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationInteractiveConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationInteractiveConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationInteractiveConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc5e58b9017ec9e639fc3bdf57f2d00b6e4be17a9ab14175e95e0d4670ad6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMaximumCapacity",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory", "disk": "disk"},
)
class EmrserverlessApplicationMaximumCapacity:
    def __init__(
        self,
        *,
        cpu: builtins.str,
        memory: builtins.str,
        disk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.
        :param disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6948195f4c180b3da9fb30e8d5636972681835a4ac1cbcd45cec5268f6480835)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "memory": memory,
        }
        if disk is not None:
            self._values["disk"] = disk

    @builtins.property
    def cpu(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cpu EmrserverlessApplication#cpu}.'''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#memory EmrserverlessApplication#memory}.'''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#disk EmrserverlessApplication#disk}.'''
        result = self._values.get("disk")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMaximumCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMaximumCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMaximumCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7dc1aca63e924ae2b162eed43019d2f83533ed84d1ad93dde57e478be3c4699)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisk")
    def reset_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisk", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c39de7ae6d9d67f49282bb4a66bd82cfdc67eaa890455ad57698a53b8ebd2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4642473466af9dc06cfa11718436f1a5988f23772e57295e5e4f7aa9261c4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dcf0aa10a2ddba4b43e3d394b088d604bccc43bc8257ced6768aeda66edde26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMaximumCapacity]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMaximumCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMaximumCapacity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147493e08490f5fcd3baad03af2193265e787c3f0c56a89b9e2db45065ef1763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_logging_configuration": "cloudwatchLoggingConfiguration",
        "managed_persistence_monitoring_configuration": "managedPersistenceMonitoringConfiguration",
        "prometheus_monitoring_configuration": "prometheusMonitoringConfiguration",
        "s3_monitoring_configuration": "s3MonitoringConfiguration",
    },
)
class EmrserverlessApplicationMonitoringConfiguration:
    def __init__(
        self,
        *,
        cloudwatch_logging_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_persistence_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        prometheus_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_monitoring_configuration: typing.Optional[typing.Union["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_logging_configuration: cloudwatch_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cloudwatch_logging_configuration EmrserverlessApplication#cloudwatch_logging_configuration}
        :param managed_persistence_monitoring_configuration: managed_persistence_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#managed_persistence_monitoring_configuration EmrserverlessApplication#managed_persistence_monitoring_configuration}
        :param prometheus_monitoring_configuration: prometheus_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#prometheus_monitoring_configuration EmrserverlessApplication#prometheus_monitoring_configuration}
        :param s3_monitoring_configuration: s3_monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#s3_monitoring_configuration EmrserverlessApplication#s3_monitoring_configuration}
        '''
        if isinstance(cloudwatch_logging_configuration, dict):
            cloudwatch_logging_configuration = EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration(**cloudwatch_logging_configuration)
        if isinstance(managed_persistence_monitoring_configuration, dict):
            managed_persistence_monitoring_configuration = EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration(**managed_persistence_monitoring_configuration)
        if isinstance(prometheus_monitoring_configuration, dict):
            prometheus_monitoring_configuration = EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration(**prometheus_monitoring_configuration)
        if isinstance(s3_monitoring_configuration, dict):
            s3_monitoring_configuration = EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration(**s3_monitoring_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac20d19564cfefcdbed73014c3e7fec55a9d7153593d2e0f4ded49b747f9d3b2)
            check_type(argname="argument cloudwatch_logging_configuration", value=cloudwatch_logging_configuration, expected_type=type_hints["cloudwatch_logging_configuration"])
            check_type(argname="argument managed_persistence_monitoring_configuration", value=managed_persistence_monitoring_configuration, expected_type=type_hints["managed_persistence_monitoring_configuration"])
            check_type(argname="argument prometheus_monitoring_configuration", value=prometheus_monitoring_configuration, expected_type=type_hints["prometheus_monitoring_configuration"])
            check_type(argname="argument s3_monitoring_configuration", value=s3_monitoring_configuration, expected_type=type_hints["s3_monitoring_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_logging_configuration is not None:
            self._values["cloudwatch_logging_configuration"] = cloudwatch_logging_configuration
        if managed_persistence_monitoring_configuration is not None:
            self._values["managed_persistence_monitoring_configuration"] = managed_persistence_monitoring_configuration
        if prometheus_monitoring_configuration is not None:
            self._values["prometheus_monitoring_configuration"] = prometheus_monitoring_configuration
        if s3_monitoring_configuration is not None:
            self._values["s3_monitoring_configuration"] = s3_monitoring_configuration

    @builtins.property
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration"]:
        '''cloudwatch_logging_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#cloudwatch_logging_configuration EmrserverlessApplication#cloudwatch_logging_configuration}
        '''
        result = self._values.get("cloudwatch_logging_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration"], result)

    @builtins.property
    def managed_persistence_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration"]:
        '''managed_persistence_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#managed_persistence_monitoring_configuration EmrserverlessApplication#managed_persistence_monitoring_configuration}
        '''
        result = self._values.get("managed_persistence_monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration"], result)

    @builtins.property
    def prometheus_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"]:
        '''prometheus_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#prometheus_monitoring_configuration EmrserverlessApplication#prometheus_monitoring_configuration}
        '''
        result = self._values.get("prometheus_monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"], result)

    @builtins.property
    def s3_monitoring_configuration(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"]:
        '''s3_monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#s3_monitoring_configuration EmrserverlessApplication#s3_monitoring_configuration}
        '''
        result = self._values.get("s3_monitoring_configuration")
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "encryption_key_arn": "encryptionKeyArn",
        "log_group_name": "logGroupName",
        "log_stream_name_prefix": "logStreamNamePrefix",
        "log_types": "logTypes",
    },
)
class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
        log_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_group_name EmrserverlessApplication#log_group_name}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_stream_name_prefix EmrserverlessApplication#log_stream_name_prefix}.
        :param log_types: log_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_types EmrserverlessApplication#log_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6d956b9ffb501ee3f60c7338071cfc9edb04a35c846a9623b2003b9c88b217)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name_prefix", value=log_stream_name_prefix, expected_type=type_hints["log_stream_name_prefix"])
            check_type(argname="argument log_types", value=log_types, expected_type=type_hints["log_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name_prefix is not None:
            self._values["log_stream_name_prefix"] = log_stream_name_prefix
        if log_types is not None:
            self._values["log_types"] = log_types

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.'''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_group_name EmrserverlessApplication#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_stream_name_prefix EmrserverlessApplication#log_stream_name_prefix}.'''
        result = self._values.get("log_stream_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_types(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes"]]]:
        '''log_types block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_types EmrserverlessApplication#log_types}
        '''
        result = self._values.get("log_types")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#values EmrserverlessApplication#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350a05b68c6fc6f68fecb493554767e4222e08f433faadc24acf3936c0a77380)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#name EmrserverlessApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#values EmrserverlessApplication#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efc8a505d9f60480d915cbe0364d2e69cc6db7c24c1e76b5b2815723759112a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6e557e9d64e698249457c02d0fb9dcacb2695be240eb3ded666a34e73eef58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a7f1b7393f8d4709cdd3f4b10f5afa7534a630918b2ce59810b83309191c1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1d76b0e1137c11e5e5fb2f43182ddd757ee2f18944e6385068d8f3d0f547519)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afad107ecf2b05248b6a7f13d8a8e3806e7031f473dc156e85ea3d076d842845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01b14d775a761c544214b8f345ad5f35a3ef4f0684cd243861b31e3f373b2fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__903ee8e631a771ac0efd15854bd0e16e95de0e702836b517d3eb89ebd7744b46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8884cea40e743d4490b853a5f8a5cc592f544a5b4411745aa6df768d2b605776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98efa9df40aeb644fcea2fe09385e216a67c9d038fd1e56161793d860214ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7b9ba8d693e38eab52e5dba29be3f1067d0ac90a137edb64a50fa51d86debf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3fff1ba86c75dbed2507e3ee4905fda36ebcda0b5cbd88d780a78f16bac776)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogTypes")
    def put_log_types(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd41f2cf0f3a7e335e75f3d88f35688371eee70370717aa51c04a4ca07fbb250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogTypes", [value]))

    @jsii.member(jsii_name="resetEncryptionKeyArn")
    def reset_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyArn", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamNamePrefix")
    def reset_log_stream_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamNamePrefix", []))

    @jsii.member(jsii_name="resetLogTypes")
    def reset_log_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogTypes", []))

    @builtins.property
    @jsii.member(jsii_name="logTypes")
    def log_types(
        self,
    ) -> EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList:
        return typing.cast(EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList, jsii.get(self, "logTypes"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArnInput")
    def encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefixInput")
    def log_stream_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="logTypesInput")
    def log_types_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]], jsii.get(self, "logTypesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1436a54ef15b54fbe13bf1128442f35685e89f22b3f8c70f789739c3c0d18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993c85b87361183cf4d3769a9fb4332c6cacd07bbb411b36948ab94a725e49ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7513604aa9edee8f6ea9675e9b4b75c5a83ae89dece8a07cdbeb97cac7d222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefix")
    def log_stream_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamNamePrefix"))

    @log_stream_name_prefix.setter
    def log_stream_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf30ede7307a362432d32a3ba4a4fe5c55585dd7a4189d446393fb13f886da46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e44ec0d76b6d6914c51b245c4d540933ab5ebe4708e782b3bf292ee488af49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "encryption_key_arn": "encryptionKeyArn"},
)
class EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edc04da65ec0af060f9f43686f81e1757a6feca3a4318adbc9810e3f9fc27e9)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.'''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c8675d36905907acd198f8f28c63d2f3e6fee8df6bcc22a6c424a7eaf8564ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEncryptionKeyArn")
    def reset_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyArn", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArnInput")
    def encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArnInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__757dc968d5ff2fb91514884f5ec3daa3faf29240efbe2fee885f79eb93a25042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae83510d1779d0c39ffd10b3b048d276832a17969caf90d32a086f7821a71d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946b2da92b693107616c9ae327b529c17973b241bc12a15b33fae22e75b8c55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__795c2ba40507055fc998f29830ea3b0bfa7224d308147af3d0d472ef77a7c824)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingConfiguration")
    def put_cloudwatch_logging_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
        log_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_group_name EmrserverlessApplication#log_group_name}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_stream_name_prefix EmrserverlessApplication#log_stream_name_prefix}.
        :param log_types: log_types block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_types EmrserverlessApplication#log_types}
        '''
        value = EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration(
            enabled=enabled,
            encryption_key_arn=encryption_key_arn,
            log_group_name=log_group_name,
            log_stream_name_prefix=log_stream_name_prefix,
            log_types=log_types,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingConfiguration", [value]))

    @jsii.member(jsii_name="putManagedPersistenceMonitoringConfiguration")
    def put_managed_persistence_monitoring_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#enabled EmrserverlessApplication#enabled}.
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        '''
        value = EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration(
            enabled=enabled, encryption_key_arn=encryption_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putManagedPersistenceMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putPrometheusMonitoringConfiguration")
    def put_prometheus_monitoring_configuration(
        self,
        *,
        remote_write_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_write_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#remote_write_url EmrserverlessApplication#remote_write_url}.
        '''
        value = EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration(
            remote_write_url=remote_write_url
        )

        return typing.cast(None, jsii.invoke(self, "putPrometheusMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putS3MonitoringConfiguration")
    def put_s3_monitoring_configuration(
        self,
        *,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_uri EmrserverlessApplication#log_uri}.
        '''
        value = EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration(
            encryption_key_arn=encryption_key_arn, log_uri=log_uri
        )

        return typing.cast(None, jsii.invoke(self, "putS3MonitoringConfiguration", [value]))

    @jsii.member(jsii_name="resetCloudwatchLoggingConfiguration")
    def reset_cloudwatch_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingConfiguration", []))

    @jsii.member(jsii_name="resetManagedPersistenceMonitoringConfiguration")
    def reset_managed_persistence_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPersistenceMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetPrometheusMonitoringConfiguration")
    def reset_prometheus_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrometheusMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetS3MonitoringConfiguration")
    def reset_s3_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3MonitoringConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingConfiguration")
    def cloudwatch_logging_configuration(
        self,
    ) -> EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference:
        return typing.cast(EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference, jsii.get(self, "cloudwatchLoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="managedPersistenceMonitoringConfiguration")
    def managed_persistence_monitoring_configuration(
        self,
    ) -> EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference:
        return typing.cast(EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference, jsii.get(self, "managedPersistenceMonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="prometheusMonitoringConfiguration")
    def prometheus_monitoring_configuration(
        self,
    ) -> "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference", jsii.get(self, "prometheusMonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3MonitoringConfiguration")
    def s3_monitoring_configuration(
        self,
    ) -> "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference":
        return typing.cast("EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference", jsii.get(self, "s3MonitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingConfigurationInput")
    def cloudwatch_logging_configuration_input(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration], jsii.get(self, "cloudwatchLoggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPersistenceMonitoringConfigurationInput")
    def managed_persistence_monitoring_configuration_input(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration], jsii.get(self, "managedPersistenceMonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="prometheusMonitoringConfigurationInput")
    def prometheus_monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration"], jsii.get(self, "prometheusMonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3MonitoringConfigurationInput")
    def s3_monitoring_configuration_input(
        self,
    ) -> typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"]:
        return typing.cast(typing.Optional["EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration"], jsii.get(self, "s3MonitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a96d8070d8a8ae33406cbe1657501f4f8a6c8097f9ec2fa4c959534644fdc1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"remote_write_url": "remoteWriteUrl"},
)
class EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration:
    def __init__(
        self,
        *,
        remote_write_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_write_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#remote_write_url EmrserverlessApplication#remote_write_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83de21ae2bba39cecf16c839068435b8dfc63df7334af3e74baf383dd80571fa)
            check_type(argname="argument remote_write_url", value=remote_write_url, expected_type=type_hints["remote_write_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if remote_write_url is not None:
            self._values["remote_write_url"] = remote_write_url

    @builtins.property
    def remote_write_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#remote_write_url EmrserverlessApplication#remote_write_url}.'''
        result = self._values.get("remote_write_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15814b7247085f2744fa52e5f8558ddec25c26e896c73a0eaf71bef586ca951e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRemoteWriteUrl")
    def reset_remote_write_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteWriteUrl", []))

    @builtins.property
    @jsii.member(jsii_name="remoteWriteUrlInput")
    def remote_write_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteWriteUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteWriteUrl")
    def remote_write_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteWriteUrl"))

    @remote_write_url.setter
    def remote_write_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f6bfee1009296f6cb05ea9c1cefa90a2f6f7ff84d74610c536453c71344385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteWriteUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e6fbabbfeda2eee6fe998a05bc9dc427dcf2faf899eedb0d130932e06a7045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={"encryption_key_arn": "encryptionKeyArn", "log_uri": "logUri"},
)
class EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration:
    def __init__(
        self,
        *,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        log_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.
        :param log_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_uri EmrserverlessApplication#log_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69190f04dc1d63f470174f8b4857fa25fda68b2fe9984c3dc1a05c209103038)
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if log_uri is not None:
            self._values["log_uri"] = log_uri

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#encryption_key_arn EmrserverlessApplication#encryption_key_arn}.'''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#log_uri EmrserverlessApplication#log_uri}.'''
        result = self._values.get("log_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e99898e7069cd2ac1cf9e2834a47f913f644de5cc83276c95b58522718c90b87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncryptionKeyArn")
    def reset_encryption_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyArn", []))

    @jsii.member(jsii_name="resetLogUri")
    def reset_log_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogUri", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArnInput")
    def encryption_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logUriInput")
    def log_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logUriInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9124e4492bdb26a0de1d83d7291a7b32271284613f1e6ef944acefe469b59f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logUri")
    def log_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logUri"))

    @log_uri.setter
    def log_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88fb3a3520cf3f69afd5b2863f27d438bb74b61fce397585681bf7de3bf702ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0a012ff5167326d7c3a81ae326e9ef6d021cd992b8fc448b80a9a110684e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationNetworkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnet_ids": "subnetIds"},
)
class EmrserverlessApplicationNetworkConfiguration:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#security_group_ids EmrserverlessApplication#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#subnet_ids EmrserverlessApplication#subnet_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7697d4f2fb9595f573ee31647a54396c798f646da2bbd9d726833fb5660d2517)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#security_group_ids EmrserverlessApplication#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#subnet_ids EmrserverlessApplication#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationNetworkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationNetworkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationNetworkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f145325a75af414fb48c7a069af17a10b94aef162f5becaa1214212ff271b07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48b011f8ba243e2824896a71614b7dc7b1bb3fa1d86d6735902652568e0be646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6314672af24d072643e6c58fe318b895a09e23ab5951635f5664a65b9e25afcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationNetworkConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationNetworkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationNetworkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a83d94cce86172028a06d3cf39cf6c0e3e82fb17e0112ab1a2f070102b8a16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationRuntimeConfiguration",
    jsii_struct_bases=[],
    name_mapping={"classification": "classification", "properties": "properties"},
)
class EmrserverlessApplicationRuntimeConfiguration:
    def __init__(
        self,
        *,
        classification: builtins.str,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#classification EmrserverlessApplication#classification}.
        :param properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#properties EmrserverlessApplication#properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89799ee648220e38ad0a9c6b8f3a308107ec7bd653fbc3dd083c9a28ee679693)
            check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "classification": classification,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def classification(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#classification EmrserverlessApplication#classification}.'''
        result = self._values.get("classification")
        assert result is not None, "Required property 'classification' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#properties EmrserverlessApplication#properties}.'''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationRuntimeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationRuntimeConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationRuntimeConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__480daa5775d153fff1ea54f5dca11d36dd7417d43e474513187496f938b06da6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EmrserverlessApplicationRuntimeConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3ea0e130f4b58dd24cf063a4192f48a2721e30768d4b06a2a8fb6bd49b6379)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmrserverlessApplicationRuntimeConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d5a826a2d594e53a1dec4bef2f0e0d8bea02d2d84a6238781b23fcacb09451)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f52beec7d8fda6cc075bb8c306e690762034e6744f3080aa24cfb538463131b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dd89bdb0530dcdc76d16e5f3772c3a7e461be6284e07f2b74841e26d3de1d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96155275f57f3d3e49f9e568668bac3a02f6c4f8f910800ef6672b439b68a7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EmrserverlessApplicationRuntimeConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationRuntimeConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e75dd8e71e2f7dd240d7e5f9c3c5736c1f4fb8c97d95f152178bca3ff07938c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="classificationInput")
    def classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "classificationInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="classification")
    def classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classification"))

    @classification.setter
    def classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198e12b3ccf1617c517425c5db637cd8f324e9bb7031dc54ebdec80f8feeee22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0622c752587a3f418c9e521f5b861790d6cac0a83678ef5895a537c1c258cd65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d567e705c5575361b2c927add841b14e8bce4f6e169dfef26ab8e2f61134c044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationSchedulerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "max_concurrent_runs": "maxConcurrentRuns",
        "queue_timeout_minutes": "queueTimeoutMinutes",
    },
)
class EmrserverlessApplicationSchedulerConfiguration:
    def __init__(
        self,
        *,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        queue_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_concurrent_runs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#max_concurrent_runs EmrserverlessApplication#max_concurrent_runs}.
        :param queue_timeout_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#queue_timeout_minutes EmrserverlessApplication#queue_timeout_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfb9d6476afd5d3a449cb39fd375c524028a9c851c716d6856c059a73e7d0dd)
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument queue_timeout_minutes", value=queue_timeout_minutes, expected_type=type_hints["queue_timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if queue_timeout_minutes is not None:
            self._values["queue_timeout_minutes"] = queue_timeout_minutes

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#max_concurrent_runs EmrserverlessApplication#max_concurrent_runs}.'''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.25.0/docs/resources/emrserverless_application#queue_timeout_minutes EmrserverlessApplication#queue_timeout_minutes}.'''
        result = self._values.get("queue_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrserverlessApplicationSchedulerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrserverlessApplicationSchedulerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.emrserverlessApplication.EmrserverlessApplicationSchedulerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05806c7113c66a986ceead7995f8d59104bf0639298416db566a125eb67e3194)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxConcurrentRuns")
    def reset_max_concurrent_runs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentRuns", []))

    @jsii.member(jsii_name="resetQueueTimeoutMinutes")
    def reset_queue_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueTimeoutMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRunsInput")
    def max_concurrent_runs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentRunsInput"))

    @builtins.property
    @jsii.member(jsii_name="queueTimeoutMinutesInput")
    def queue_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queueTimeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRuns")
    def max_concurrent_runs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentRuns"))

    @max_concurrent_runs.setter
    def max_concurrent_runs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7002cd3be6894597514c2b8732a275ed9422bf60ed1ec517c4648cb7070f3ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentRuns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueTimeoutMinutes")
    def queue_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueTimeoutMinutes"))

    @queue_timeout_minutes.setter
    def queue_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9792c8fb895815e4b46485149ecdd47627fa71ea90a2ecd44f0ca2bd5eac7c04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EmrserverlessApplicationSchedulerConfiguration]:
        return typing.cast(typing.Optional[EmrserverlessApplicationSchedulerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EmrserverlessApplicationSchedulerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef85ac35a2b327de852a1e2e46fd13a7e76143a61d0d1c40dd39f88b7f63168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EmrserverlessApplication",
    "EmrserverlessApplicationAutoStartConfiguration",
    "EmrserverlessApplicationAutoStartConfigurationOutputReference",
    "EmrserverlessApplicationAutoStopConfiguration",
    "EmrserverlessApplicationAutoStopConfigurationOutputReference",
    "EmrserverlessApplicationConfig",
    "EmrserverlessApplicationImageConfiguration",
    "EmrserverlessApplicationImageConfigurationOutputReference",
    "EmrserverlessApplicationInitialCapacity",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfig",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfigOutputReference",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration",
    "EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfigurationOutputReference",
    "EmrserverlessApplicationInitialCapacityList",
    "EmrserverlessApplicationInitialCapacityOutputReference",
    "EmrserverlessApplicationInteractiveConfiguration",
    "EmrserverlessApplicationInteractiveConfigurationOutputReference",
    "EmrserverlessApplicationMaximumCapacity",
    "EmrserverlessApplicationMaximumCapacityOutputReference",
    "EmrserverlessApplicationMonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesList",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypesOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfigurationOutputReference",
    "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration",
    "EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfigurationOutputReference",
    "EmrserverlessApplicationNetworkConfiguration",
    "EmrserverlessApplicationNetworkConfigurationOutputReference",
    "EmrserverlessApplicationRuntimeConfiguration",
    "EmrserverlessApplicationRuntimeConfigurationList",
    "EmrserverlessApplicationRuntimeConfigurationOutputReference",
    "EmrserverlessApplicationSchedulerConfiguration",
    "EmrserverlessApplicationSchedulerConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__6df9bccdfbfdf93f5315409f44cd957e5f280b30610084c850a05783a46d5416(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    release_label: builtins.str,
    type: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStartConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStopConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    image_configuration: typing.Optional[typing.Union[EmrserverlessApplicationImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationInitialCapacity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interactive_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInteractiveConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_capacity: typing.Optional[typing.Union[EmrserverlessApplicationMaximumCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_configuration: typing.Optional[typing.Union[EmrserverlessApplicationNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationRuntimeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduler_configuration: typing.Optional[typing.Union[EmrserverlessApplicationSchedulerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__d9352b6f8885088571c3a23eed26dfcbe559acb5caa0fea530dcc47bf71fb849(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7e05b2339cb096cca79fcf6d2fe21bf431036b2d4260dcc6212df2ee181922(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationInitialCapacity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0c01fff4c4cc069d850f064091b80484d466cc44d03f25c919434d792664a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationRuntimeConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f49030a456f2b5539b6276180ab2808f7fe23f4185dabedcc7b0e679d040b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11324e1d03f2dc067ede8c964ffabf8843b143584a09ebb1d145208a89d81b71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c92979a2e53e806bf61b4ebdb1a8631d78d79a7a39b0498e656d49687e626ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bca54c289016f6f63c8e07e406ba7cb453391c54c863508d48df0376b40e21f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bc1ab4302375629243c2a9fa5d6259cfb9d11ea937a354932e626512b7b45a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d611a5b628ebbbc389d4dea4f2266b2a5abd4bdc12466467102beae62c4c14(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c1d180d226837117a313d0e9265770fef37912cb6743ed00fe743e017288a2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a34c4fab2e07a3d5800801503744b181fbadb66748f43a6f731fcf634561a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711adc9a70854729f54a13f0e3159d31c4f91ca65924f40f57dd36d442fdc8d0(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef37e49bfa3d4216f2d547e9aa6a3d07b1cddfb1fe020464f695af6bb745c81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455bf80d3251b9c3160119b571f6269ce1920c00bcb4345aa49c4a0d9f6e6de5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf7768923180cb1f3c9dfe0a7fa67e78a87f0ecba6ce5654221bd210131f4dc(
    value: typing.Optional[EmrserverlessApplicationAutoStartConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f606597533d046e346c92c83226fe23ca8c1554f90d3dd534e13d3fb2d7ca78(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    idle_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d26e7db4ea3e74daa1926f0fb541b56b6de3e99ea63d26d4c2e9ad4df1188a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b680a022d907eb91f665725dcfe88afe429733dd000ddbf481b317fca29e2f8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27e3a3c9b20251c6e4bd3c66b16b65aaf995a444d4455f79d4657f16b08fd3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8244577ce2ca28471eadbcd403671faf8181aa61e7b05dd4daabdd16da4ddf5(
    value: typing.Optional[EmrserverlessApplicationAutoStopConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9110adb97c1b412ea08fd61c6fffd9e9ed1a69090c3dbcf77adbee5f5658f9e7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    release_label: builtins.str,
    type: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStartConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[EmrserverlessApplicationAutoStopConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    image_configuration: typing.Optional[typing.Union[EmrserverlessApplicationImageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_capacity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationInitialCapacity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interactive_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInteractiveConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_capacity: typing.Optional[typing.Union[EmrserverlessApplicationMaximumCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    network_configuration: typing.Optional[typing.Union[EmrserverlessApplicationNetworkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    runtime_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationRuntimeConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduler_configuration: typing.Optional[typing.Union[EmrserverlessApplicationSchedulerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88364ebbb88e6f3cc5aa80d2d1ea3013facb713e1d2d6ff18c77a47cd73db455(
    *,
    image_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d614bac5a243d74686f8f994a9cd976f8e16f8e9244d9beab4d38cbe83c20e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0033bea57ff592b3ea8f2d2105cbcbdc54b2287ee63244124d545206044ae31e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906aed13023e42d70c26dca045452acbd4f448a310a2314592d2f068736189e0(
    value: typing.Optional[EmrserverlessApplicationImageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8fa572c37ec26d6aa4c398a7c687c856693006d42fa026f764b03f35a4cf0e(
    *,
    initial_capacity_type: builtins.str,
    initial_capacity_config: typing.Optional[typing.Union[EmrserverlessApplicationInitialCapacityInitialCapacityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3137ea7acf2b38e736f43d991d62a5d680982c4770134eb3f296da599e7748cd(
    *,
    worker_count: jsii.Number,
    worker_configuration: typing.Optional[typing.Union[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23832c10a2ba6a0a085009e9bb513e8679491068dbaf3f95d9ff9ccd09d8c773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7362d9841e0dc977d0a705422aae81a4df82c0f1ce83e7f97c67ca5af5b2dd56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6458e504443767ec382d5631c23a5d787be994cadf3c8b098b3400e630d953ba(
    value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037dbf4eee9f5d069ca18fda50e3200e441002fca4bbfef958ec0c1d5554b51f(
    *,
    cpu: builtins.str,
    memory: builtins.str,
    disk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cf4b89a131f61095c8dfd8f8c8bf1d8e0e67b18b0f0cbc9663a4d70e186bd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863ec41233987f791b662cb7177a3811e5f12e01d8e8c1a7dd7a43e199b48880(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc485f1fdf86d6100a3faa12910e6f8fc3edaa7d72c81a3b2998bf4a4c744dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06913e3c43ad7d6114463f2c7376f00514ded1db980fc9e61c93773fd4b47f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d732da70ad29607ead222879f410e911126b5b6fcf585d715b2cb67dceec5f(
    value: typing.Optional[EmrserverlessApplicationInitialCapacityInitialCapacityConfigWorkerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7407e074afea99fba7bfad693b5d8339303dd1e1ef6a20d3a1c4b3b7017eaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c0a2fa85432655e0fdb947739a7fa8c1c1fbc587b930b7e786348e19592ba4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522f152fa762fc57fe3ee5d9c73d071e065df784828c2715bcb1686171d42b26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3173d8881fff75790857d4e2aa869618392148842abd5200116a3d57efec52ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abff6195556794c9b9532e440ea4952925318e6701a54fcfae763f6f57371ee2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4d982571785c047dd66cf1eb2af442df039c1d23c17523a771b3aa81c77c6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationInitialCapacity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940e15624a49afa4241fd5cb9efa5627f6f8cadacd09250d964da6b40a5d3cd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78b406f2f0d9c2ae747c28435bc901ce8054f1c1775719a37c7425c6d6e7a9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68439f6ecd07de6cf2e8a512f5c4484f1dd9a69a27f274563f08bd110c10eab0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationInitialCapacity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd73c16ad7904d28a4937186eb6fcc11155df7201a7d26f1e20d26ba60a7170b(
    *,
    livy_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    studio_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3597c3c78db1fd69c0f10e49002d874ee7101aa4d08d84c496f194ccd566ae5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdabe0c212b1c0ad9f14e909a3f7cf4c6eb913a79863ce0ebeefc38d2f4f5e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ff08a1a96584d4521a330f984754fbd6608005e02cfd4455a6ba29b8b0c075(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc5e58b9017ec9e639fc3bdf57f2d00b6e4be17a9ab14175e95e0d4670ad6df(
    value: typing.Optional[EmrserverlessApplicationInteractiveConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6948195f4c180b3da9fb30e8d5636972681835a4ac1cbcd45cec5268f6480835(
    *,
    cpu: builtins.str,
    memory: builtins.str,
    disk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7dc1aca63e924ae2b162eed43019d2f83533ed84d1ad93dde57e478be3c4699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c39de7ae6d9d67f49282bb4a66bd82cfdc67eaa890455ad57698a53b8ebd2bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4642473466af9dc06cfa11718436f1a5988f23772e57295e5e4f7aa9261c4e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcf0aa10a2ddba4b43e3d394b088d604bccc43bc8257ced6768aeda66edde26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147493e08490f5fcd3baad03af2193265e787c3f0c56a89b9e2db45065ef1763(
    value: typing.Optional[EmrserverlessApplicationMaximumCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac20d19564cfefcdbed73014c3e7fec55a9d7153593d2e0f4ded49b747f9d3b2(
    *,
    cloudwatch_logging_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_persistence_monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    prometheus_monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_monitoring_configuration: typing.Optional[typing.Union[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6d956b9ffb501ee3f60c7338071cfc9edb04a35c846a9623b2003b9c88b217(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    encryption_key_arn: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name_prefix: typing.Optional[builtins.str] = None,
    log_types: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350a05b68c6fc6f68fecb493554767e4222e08f433faadc24acf3936c0a77380(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc8a505d9f60480d915cbe0364d2e69cc6db7c24c1e76b5b2815723759112a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6e557e9d64e698249457c02d0fb9dcacb2695be240eb3ded666a34e73eef58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a7f1b7393f8d4709cdd3f4b10f5afa7534a630918b2ce59810b83309191c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d76b0e1137c11e5e5fb2f43182ddd757ee2f18944e6385068d8f3d0f547519(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afad107ecf2b05248b6a7f13d8a8e3806e7031f473dc156e85ea3d076d842845(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01b14d775a761c544214b8f345ad5f35a3ef4f0684cd243861b31e3f373b2fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903ee8e631a771ac0efd15854bd0e16e95de0e702836b517d3eb89ebd7744b46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8884cea40e743d4490b853a5f8a5cc592f544a5b4411745aa6df768d2b605776(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98efa9df40aeb644fcea2fe09385e216a67c9d038fd1e56161793d860214ddf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7b9ba8d693e38eab52e5dba29be3f1067d0ac90a137edb64a50fa51d86debf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3fff1ba86c75dbed2507e3ee4905fda36ebcda0b5cbd88d780a78f16bac776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd41f2cf0f3a7e335e75f3d88f35688371eee70370717aa51c04a4ca07fbb250(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfigurationLogTypes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1436a54ef15b54fbe13bf1128442f35685e89f22b3f8c70f789739c3c0d18a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993c85b87361183cf4d3769a9fb4332c6cacd07bbb411b36948ab94a725e49ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7513604aa9edee8f6ea9675e9b4b75c5a83ae89dece8a07cdbeb97cac7d222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf30ede7307a362432d32a3ba4a4fe5c55585dd7a4189d446393fb13f886da46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e44ec0d76b6d6914c51b245c4d540933ab5ebe4708e782b3bf292ee488af49(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationCloudwatchLoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edc04da65ec0af060f9f43686f81e1757a6feca3a4318adbc9810e3f9fc27e9(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8675d36905907acd198f8f28c63d2f3e6fee8df6bcc22a6c424a7eaf8564ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757dc968d5ff2fb91514884f5ec3daa3faf29240efbe2fee885f79eb93a25042(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae83510d1779d0c39ffd10b3b048d276832a17969caf90d32a086f7821a71d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946b2da92b693107616c9ae327b529c17973b241bc12a15b33fae22e75b8c55a(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationManagedPersistenceMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795c2ba40507055fc998f29830ea3b0bfa7224d308147af3d0d472ef77a7c824(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a96d8070d8a8ae33406cbe1657501f4f8a6c8097f9ec2fa4c959534644fdc1b(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83de21ae2bba39cecf16c839068435b8dfc63df7334af3e74baf383dd80571fa(
    *,
    remote_write_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15814b7247085f2744fa52e5f8558ddec25c26e896c73a0eaf71bef586ca951e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f6bfee1009296f6cb05ea9c1cefa90a2f6f7ff84d74610c536453c71344385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e6fbabbfeda2eee6fe998a05bc9dc427dcf2faf899eedb0d130932e06a7045(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationPrometheusMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69190f04dc1d63f470174f8b4857fa25fda68b2fe9984c3dc1a05c209103038(
    *,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    log_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99898e7069cd2ac1cf9e2834a47f913f644de5cc83276c95b58522718c90b87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9124e4492bdb26a0de1d83d7291a7b32271284613f1e6ef944acefe469b59f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fb3a3520cf3f69afd5b2863f27d438bb74b61fce397585681bf7de3bf702ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0a012ff5167326d7c3a81ae326e9ef6d021cd992b8fc448b80a9a110684e88(
    value: typing.Optional[EmrserverlessApplicationMonitoringConfigurationS3MonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7697d4f2fb9595f573ee31647a54396c798f646da2bbd9d726833fb5660d2517(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f145325a75af414fb48c7a069af17a10b94aef162f5becaa1214212ff271b07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b011f8ba243e2824896a71614b7dc7b1bb3fa1d86d6735902652568e0be646(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6314672af24d072643e6c58fe318b895a09e23ab5951635f5664a65b9e25afcf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a83d94cce86172028a06d3cf39cf6c0e3e82fb17e0112ab1a2f070102b8a16f(
    value: typing.Optional[EmrserverlessApplicationNetworkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89799ee648220e38ad0a9c6b8f3a308107ec7bd653fbc3dd083c9a28ee679693(
    *,
    classification: builtins.str,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480daa5775d153fff1ea54f5dca11d36dd7417d43e474513187496f938b06da6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3ea0e130f4b58dd24cf063a4192f48a2721e30768d4b06a2a8fb6bd49b6379(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d5a826a2d594e53a1dec4bef2f0e0d8bea02d2d84a6238781b23fcacb09451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f52beec7d8fda6cc075bb8c306e690762034e6744f3080aa24cfb538463131b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd89bdb0530dcdc76d16e5f3772c3a7e461be6284e07f2b74841e26d3de1d90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96155275f57f3d3e49f9e568668bac3a02f6c4f8f910800ef6672b439b68a7bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmrserverlessApplicationRuntimeConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75dd8e71e2f7dd240d7e5f9c3c5736c1f4fb8c97d95f152178bca3ff07938c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198e12b3ccf1617c517425c5db637cd8f324e9bb7031dc54ebdec80f8feeee22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0622c752587a3f418c9e521f5b861790d6cac0a83678ef5895a537c1c258cd65(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d567e705c5575361b2c927add841b14e8bce4f6e169dfef26ab8e2f61134c044(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EmrserverlessApplicationRuntimeConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfb9d6476afd5d3a449cb39fd375c524028a9c851c716d6856c059a73e7d0dd(
    *,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    queue_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05806c7113c66a986ceead7995f8d59104bf0639298416db566a125eb67e3194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7002cd3be6894597514c2b8732a275ed9422bf60ed1ec517c4648cb7070f3ea4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9792c8fb895815e4b46485149ecdd47627fa71ea90a2ecd44f0ca2bd5eac7c04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef85ac35a2b327de852a1e2e46fd13a7e76143a61d0d1c40dd39f88b7f63168(
    value: typing.Optional[EmrserverlessApplicationSchedulerConfiguration],
) -> None:
    """Type checking stubs"""
    pass
