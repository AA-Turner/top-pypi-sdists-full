r'''
# `google_workstations_workstation_config`

Refer to the Terraform Registry for docs: [`google_workstations_workstation_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config).
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


class GoogleWorkstationsWorkstationConfigA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config google_workstations_workstation_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        workstation_cluster_id: builtins.str,
        workstation_config_id: builtins.str,
        allowed_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigAllowedPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_tcp_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_audit_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigEphemeralDirectories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigHost", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_usable_workstations: typing.Optional[jsii.Number] = None,
        persistent_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigPersistentDirectories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        readiness_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigReadinessChecks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        running_timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config google_workstations_workstation_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location where the workstation cluster config should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#location GoogleWorkstationsWorkstationConfigA#location}
        :param workstation_cluster_id: The ID of the parent workstation cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#workstation_cluster_id GoogleWorkstationsWorkstationConfigA#workstation_cluster_id}
        :param workstation_config_id: The ID to be assigned to the workstation cluster config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#workstation_config_id GoogleWorkstationsWorkstationConfigA#workstation_config_id}
        :param allowed_ports: allowed_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#allowed_ports GoogleWorkstationsWorkstationConfigA#allowed_ports}
        :param annotations: Client-specified annotations. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#annotations GoogleWorkstationsWorkstationConfigA#annotations}
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#container GoogleWorkstationsWorkstationConfigA#container}
        :param disable_tcp_connections: Disables support for plain TCP connections in the workstation. By default the service supports TCP connections via a websocket relay. Setting this option to true disables that relay, which prevents the usage of services that require plain tcp connections, such as ssh. When enabled, all communication must occur over https or wss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_tcp_connections GoogleWorkstationsWorkstationConfigA#disable_tcp_connections}
        :param display_name: Human-readable name for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#display_name GoogleWorkstationsWorkstationConfigA#display_name}
        :param enable_audit_agent: Whether to enable Linux 'auditd' logging on the workstation. When enabled, a service account must also be specified that has 'logging.buckets.write' permission on the project. Operating system audit logging is distinct from Cloud Audit Logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_audit_agent GoogleWorkstationsWorkstationConfigA#enable_audit_agent}
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#encryption_key GoogleWorkstationsWorkstationConfigA#encryption_key}
        :param ephemeral_directories: ephemeral_directories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#ephemeral_directories GoogleWorkstationsWorkstationConfigA#ephemeral_directories}
        :param host: host block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#host GoogleWorkstationsWorkstationConfigA#host}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#id GoogleWorkstationsWorkstationConfigA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_timeout: How long to wait before automatically stopping an instance that hasn't recently received any user traffic. A value of 0 indicates that this instance should never time out from idleness. Defaults to 20 minutes. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#idle_timeout GoogleWorkstationsWorkstationConfigA#idle_timeout}
        :param labels: Client-specified labels that are applied to the resource and that are also propagated to the underlying Compute Engine resources. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#labels GoogleWorkstationsWorkstationConfigA#labels}
        :param max_usable_workstations: Maximum number of workstations under this configuration a user can have workstations.workstation.use permission on. Only enforced on CreateWorkstation API calls on the user issuing the API request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#max_usable_workstations GoogleWorkstationsWorkstationConfigA#max_usable_workstations}
        :param persistent_directories: persistent_directories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#persistent_directories GoogleWorkstationsWorkstationConfigA#persistent_directories}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#project GoogleWorkstationsWorkstationConfigA#project}.
        :param readiness_checks: readiness_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#readiness_checks GoogleWorkstationsWorkstationConfigA#readiness_checks}
        :param replica_zones: Specifies the zones used to replicate the VM and disk resources within the region. If set, exactly two zones within the workstation cluster's region must be specified—for example, '['us-central1-a', 'us-central1-f']'. If this field is empty, two default zones within the region are used. Immutable after the workstation configuration is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#replica_zones GoogleWorkstationsWorkstationConfigA#replica_zones}
        :param running_timeout: How long to wait before automatically stopping a workstation after it was started. A value of 0 indicates that workstations using this configuration should never time out from running duration. Must be greater than 0 and less than 24 hours if 'encryption_key' is set. Defaults to 12 hours. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#running_timeout GoogleWorkstationsWorkstationConfigA#running_timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#timeouts GoogleWorkstationsWorkstationConfigA#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86be159f02a43f8771a41b1e58b45735974b729cf01b74440afe38ed4033705a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleWorkstationsWorkstationConfigAConfig(
            location=location,
            workstation_cluster_id=workstation_cluster_id,
            workstation_config_id=workstation_config_id,
            allowed_ports=allowed_ports,
            annotations=annotations,
            container=container,
            disable_tcp_connections=disable_tcp_connections,
            display_name=display_name,
            enable_audit_agent=enable_audit_agent,
            encryption_key=encryption_key,
            ephemeral_directories=ephemeral_directories,
            host=host,
            id=id,
            idle_timeout=idle_timeout,
            labels=labels,
            max_usable_workstations=max_usable_workstations,
            persistent_directories=persistent_directories,
            project=project,
            readiness_checks=readiness_checks,
            replica_zones=replica_zones,
            running_timeout=running_timeout,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a GoogleWorkstationsWorkstationConfigA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleWorkstationsWorkstationConfigA to import.
        :param import_from_id: The id of the existing GoogleWorkstationsWorkstationConfigA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleWorkstationsWorkstationConfigA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c7b4feb6ee42c31ee60deb96576c491987376d397d90cb6e9e2f383f460254)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAllowedPorts")
    def put_allowed_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigAllowedPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42ec412ce8b32c630e2aa4245bcf724c0c6876de62674f1b98883e445603569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedPorts", [value]))

    @jsii.member(jsii_name="putContainer")
    def put_container(
        self,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        run_as_user: typing.Optional[jsii.Number] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param args: Arguments passed to the entrypoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#args GoogleWorkstationsWorkstationConfigA#args}
        :param command: If set, overrides the default ENTRYPOINT specified by the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#command GoogleWorkstationsWorkstationConfigA#command}
        :param env: Environment variables passed to the container. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#env GoogleWorkstationsWorkstationConfigA#env}
        :param image: Docker image defining the container. This image must be accessible by the config's service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#image GoogleWorkstationsWorkstationConfigA#image}
        :param run_as_user: If set, overrides the USER specified in the image with the given uid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#run_as_user GoogleWorkstationsWorkstationConfigA#run_as_user}
        :param working_dir: If set, overrides the default DIR specified by the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#working_dir GoogleWorkstationsWorkstationConfigA#working_dir}
        '''
        value = GoogleWorkstationsWorkstationConfigContainer(
            args=args,
            command=command,
            env=env,
            image=image,
            run_as_user=run_as_user,
            working_dir=working_dir,
        )

        return typing.cast(None, jsii.invoke(self, "putContainer", [value]))

    @jsii.member(jsii_name="putEncryptionKey")
    def put_encryption_key(
        self,
        *,
        kms_key: builtins.str,
        kms_key_service_account: builtins.str,
    ) -> None:
        '''
        :param kms_key: The name of the Google Cloud KMS encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#kms_key GoogleWorkstationsWorkstationConfigA#kms_key}
        :param kms_key_service_account: The service account to use with the specified KMS key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#kms_key_service_account GoogleWorkstationsWorkstationConfigA#kms_key_service_account}
        '''
        value = GoogleWorkstationsWorkstationConfigEncryptionKey(
            kms_key=kms_key, kms_key_service_account=kms_key_service_account
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKey", [value]))

    @jsii.member(jsii_name="putEphemeralDirectories")
    def put_ephemeral_directories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigEphemeralDirectories", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c51f868822937a19c20a8f7b67fbadfef4a88b82f90d4e1af4a14a9fea3e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEphemeralDirectories", [value]))

    @jsii.member(jsii_name="putHost")
    def put_host(
        self,
        *,
        gce_instance: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstance", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gce_instance: gce_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_instance GoogleWorkstationsWorkstationConfigA#gce_instance}
        '''
        value = GoogleWorkstationsWorkstationConfigHost(gce_instance=gce_instance)

        return typing.cast(None, jsii.invoke(self, "putHost", [value]))

    @jsii.member(jsii_name="putPersistentDirectories")
    def put_persistent_directories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigPersistentDirectories", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca744c7a5ec15408510598afc6c36eb45b04f90b3fbb98f609d91e42b08028b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPersistentDirectories", [value]))

    @jsii.member(jsii_name="putReadinessChecks")
    def put_readiness_checks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigReadinessChecks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961be13a75460ae1f6920fdbfdf07c9e0364a67b4fe8d92bcffaed75a94f8962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReadinessChecks", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#create GoogleWorkstationsWorkstationConfigA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#delete GoogleWorkstationsWorkstationConfigA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#update GoogleWorkstationsWorkstationConfigA#update}.
        '''
        value = GoogleWorkstationsWorkstationConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowedPorts")
    def reset_allowed_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedPorts", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetContainer")
    def reset_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainer", []))

    @jsii.member(jsii_name="resetDisableTcpConnections")
    def reset_disable_tcp_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTcpConnections", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnableAuditAgent")
    def reset_enable_audit_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAuditAgent", []))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetEphemeralDirectories")
    def reset_ephemeral_directories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralDirectories", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdleTimeout")
    def reset_idle_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleTimeout", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxUsableWorkstations")
    def reset_max_usable_workstations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUsableWorkstations", []))

    @jsii.member(jsii_name="resetPersistentDirectories")
    def reset_persistent_directories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistentDirectories", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReadinessChecks")
    def reset_readiness_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadinessChecks", []))

    @jsii.member(jsii_name="resetReplicaZones")
    def reset_replica_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaZones", []))

    @jsii.member(jsii_name="resetRunningTimeout")
    def reset_running_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunningTimeout", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="allowedPorts")
    def allowed_ports(self) -> "GoogleWorkstationsWorkstationConfigAllowedPortsList":
        return typing.cast("GoogleWorkstationsWorkstationConfigAllowedPortsList", jsii.get(self, "allowedPorts"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "GoogleWorkstationsWorkstationConfigConditionsList":
        return typing.cast("GoogleWorkstationsWorkstationConfigConditionsList", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(
        self,
    ) -> "GoogleWorkstationsWorkstationConfigContainerOutputReference":
        return typing.cast("GoogleWorkstationsWorkstationConfigContainerOutputReference", jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="degraded")
    def degraded(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "degraded"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(
        self,
    ) -> "GoogleWorkstationsWorkstationConfigEncryptionKeyOutputReference":
        return typing.cast("GoogleWorkstationsWorkstationConfigEncryptionKeyOutputReference", jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralDirectories")
    def ephemeral_directories(
        self,
    ) -> "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesList":
        return typing.cast("GoogleWorkstationsWorkstationConfigEphemeralDirectoriesList", jsii.get(self, "ephemeralDirectories"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> "GoogleWorkstationsWorkstationConfigHostOutputReference":
        return typing.cast("GoogleWorkstationsWorkstationConfigHostOutputReference", jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="persistentDirectories")
    def persistent_directories(
        self,
    ) -> "GoogleWorkstationsWorkstationConfigPersistentDirectoriesList":
        return typing.cast("GoogleWorkstationsWorkstationConfigPersistentDirectoriesList", jsii.get(self, "persistentDirectories"))

    @builtins.property
    @jsii.member(jsii_name="readinessChecks")
    def readiness_checks(
        self,
    ) -> "GoogleWorkstationsWorkstationConfigReadinessChecksList":
        return typing.cast("GoogleWorkstationsWorkstationConfigReadinessChecksList", jsii.get(self, "readinessChecks"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleWorkstationsWorkstationConfigTimeoutsOutputReference":
        return typing.cast("GoogleWorkstationsWorkstationConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="allowedPortsInput")
    def allowed_ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigAllowedPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigAllowedPorts"]]], jsii.get(self, "allowedPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigContainer"]:
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigContainer"], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="disableTcpConnectionsInput")
    def disable_tcp_connections_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTcpConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAuditAgentInput")
    def enable_audit_agent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAuditAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigEncryptionKey"]:
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigEncryptionKey"], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralDirectoriesInput")
    def ephemeral_directories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigEphemeralDirectories"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigEphemeralDirectories"]]], jsii.get(self, "ephemeralDirectoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional["GoogleWorkstationsWorkstationConfigHost"]:
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigHost"], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="idleTimeoutInput")
    def idle_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUsableWorkstationsInput")
    def max_usable_workstations_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUsableWorkstationsInput"))

    @builtins.property
    @jsii.member(jsii_name="persistentDirectoriesInput")
    def persistent_directories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigPersistentDirectories"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigPersistentDirectories"]]], jsii.get(self, "persistentDirectoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="readinessChecksInput")
    def readiness_checks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigReadinessChecks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigReadinessChecks"]]], jsii.get(self, "readinessChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaZonesInput")
    def replica_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replicaZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="runningTimeoutInput")
    def running_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runningTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleWorkstationsWorkstationConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleWorkstationsWorkstationConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workstationClusterIdInput")
    def workstation_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workstationClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="workstationConfigIdInput")
    def workstation_config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workstationConfigIdInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90ae33cf3fc3ac26d12a3bcf5917af07f0c90e8892a4901eabf65a92a632582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableTcpConnections")
    def disable_tcp_connections(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableTcpConnections"))

    @disable_tcp_connections.setter
    def disable_tcp_connections(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e8d4dc987149ea7f57039ebda1759ae4f4c6bad5b1d5ebe62f565ea53540a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTcpConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6218f2d0a0fa9f5d55eb0104d94e8188f4fb2b63b90393ff55ad766a41b78c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAuditAgent")
    def enable_audit_agent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAuditAgent"))

    @enable_audit_agent.setter
    def enable_audit_agent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5fe3142152fb975bdf691f150e361ed26da1fb9bad5b46b31330612128bd325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAuditAgent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec359a06c1e429b5d5b0a23e70d5d07362ec0c804e52bf09fd8fc7eff6d7b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleTimeout")
    def idle_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleTimeout"))

    @idle_timeout.setter
    def idle_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573fd21238ff53838ae0172702d3e390ab482a7a16710b30e202717c27ad60e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f49e638354e5485dfb260005dd2c2de4ded52328e49fca534519715769adae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8845bd89ee920a162688cb628f023c2545cabb2b0387de222418ea4230ca0153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUsableWorkstations")
    def max_usable_workstations(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUsableWorkstations"))

    @max_usable_workstations.setter
    def max_usable_workstations(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88c71645addc0b71ee092306b5d7b6b672e5ab5c5d917f6a07c6bdbe7e97afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUsableWorkstations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fda6991202e62aeeebb0fe980bc15e11ff93e956000afa203416769269f1b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaZones")
    def replica_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replicaZones"))

    @replica_zones.setter
    def replica_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb15fcf6bda438fc8eb014364daf358604b23f1d8275d434f4bd79f655df299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runningTimeout")
    def running_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runningTimeout"))

    @running_timeout.setter
    def running_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793759f9e7fd654cd5b0299c933039f701b2ab7f6a84f5724d452ce72cc77bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runningTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workstationClusterId")
    def workstation_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workstationClusterId"))

    @workstation_cluster_id.setter
    def workstation_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b6de4b5c300787dc7be27d4cfcc856402fa71ff6b23db985455bf3c8fbf7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workstationClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workstationConfigId")
    def workstation_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workstationConfigId"))

    @workstation_config_id.setter
    def workstation_config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8497c2dfef96f9a391dce0b4c36cb55f897fe1c9d1c26116b86e57d5815b932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workstationConfigId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "workstation_cluster_id": "workstationClusterId",
        "workstation_config_id": "workstationConfigId",
        "allowed_ports": "allowedPorts",
        "annotations": "annotations",
        "container": "container",
        "disable_tcp_connections": "disableTcpConnections",
        "display_name": "displayName",
        "enable_audit_agent": "enableAuditAgent",
        "encryption_key": "encryptionKey",
        "ephemeral_directories": "ephemeralDirectories",
        "host": "host",
        "id": "id",
        "idle_timeout": "idleTimeout",
        "labels": "labels",
        "max_usable_workstations": "maxUsableWorkstations",
        "persistent_directories": "persistentDirectories",
        "project": "project",
        "readiness_checks": "readinessChecks",
        "replica_zones": "replicaZones",
        "running_timeout": "runningTimeout",
        "timeouts": "timeouts",
    },
)
class GoogleWorkstationsWorkstationConfigAConfig(
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
        location: builtins.str,
        workstation_cluster_id: builtins.str,
        workstation_config_id: builtins.str,
        allowed_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigAllowedPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        container: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_tcp_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_audit_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigEphemeralDirectories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        host: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigHost", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_usable_workstations: typing.Optional[jsii.Number] = None,
        persistent_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigPersistentDirectories", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        readiness_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigReadinessChecks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        replica_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        running_timeout: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location where the workstation cluster config should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#location GoogleWorkstationsWorkstationConfigA#location}
        :param workstation_cluster_id: The ID of the parent workstation cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#workstation_cluster_id GoogleWorkstationsWorkstationConfigA#workstation_cluster_id}
        :param workstation_config_id: The ID to be assigned to the workstation cluster config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#workstation_config_id GoogleWorkstationsWorkstationConfigA#workstation_config_id}
        :param allowed_ports: allowed_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#allowed_ports GoogleWorkstationsWorkstationConfigA#allowed_ports}
        :param annotations: Client-specified annotations. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#annotations GoogleWorkstationsWorkstationConfigA#annotations}
        :param container: container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#container GoogleWorkstationsWorkstationConfigA#container}
        :param disable_tcp_connections: Disables support for plain TCP connections in the workstation. By default the service supports TCP connections via a websocket relay. Setting this option to true disables that relay, which prevents the usage of services that require plain tcp connections, such as ssh. When enabled, all communication must occur over https or wss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_tcp_connections GoogleWorkstationsWorkstationConfigA#disable_tcp_connections}
        :param display_name: Human-readable name for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#display_name GoogleWorkstationsWorkstationConfigA#display_name}
        :param enable_audit_agent: Whether to enable Linux 'auditd' logging on the workstation. When enabled, a service account must also be specified that has 'logging.buckets.write' permission on the project. Operating system audit logging is distinct from Cloud Audit Logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_audit_agent GoogleWorkstationsWorkstationConfigA#enable_audit_agent}
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#encryption_key GoogleWorkstationsWorkstationConfigA#encryption_key}
        :param ephemeral_directories: ephemeral_directories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#ephemeral_directories GoogleWorkstationsWorkstationConfigA#ephemeral_directories}
        :param host: host block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#host GoogleWorkstationsWorkstationConfigA#host}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#id GoogleWorkstationsWorkstationConfigA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param idle_timeout: How long to wait before automatically stopping an instance that hasn't recently received any user traffic. A value of 0 indicates that this instance should never time out from idleness. Defaults to 20 minutes. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#idle_timeout GoogleWorkstationsWorkstationConfigA#idle_timeout}
        :param labels: Client-specified labels that are applied to the resource and that are also propagated to the underlying Compute Engine resources. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#labels GoogleWorkstationsWorkstationConfigA#labels}
        :param max_usable_workstations: Maximum number of workstations under this configuration a user can have workstations.workstation.use permission on. Only enforced on CreateWorkstation API calls on the user issuing the API request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#max_usable_workstations GoogleWorkstationsWorkstationConfigA#max_usable_workstations}
        :param persistent_directories: persistent_directories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#persistent_directories GoogleWorkstationsWorkstationConfigA#persistent_directories}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#project GoogleWorkstationsWorkstationConfigA#project}.
        :param readiness_checks: readiness_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#readiness_checks GoogleWorkstationsWorkstationConfigA#readiness_checks}
        :param replica_zones: Specifies the zones used to replicate the VM and disk resources within the region. If set, exactly two zones within the workstation cluster's region must be specified—for example, '['us-central1-a', 'us-central1-f']'. If this field is empty, two default zones within the region are used. Immutable after the workstation configuration is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#replica_zones GoogleWorkstationsWorkstationConfigA#replica_zones}
        :param running_timeout: How long to wait before automatically stopping a workstation after it was started. A value of 0 indicates that workstations using this configuration should never time out from running duration. Must be greater than 0 and less than 24 hours if 'encryption_key' is set. Defaults to 12 hours. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#running_timeout GoogleWorkstationsWorkstationConfigA#running_timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#timeouts GoogleWorkstationsWorkstationConfigA#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(container, dict):
            container = GoogleWorkstationsWorkstationConfigContainer(**container)
        if isinstance(encryption_key, dict):
            encryption_key = GoogleWorkstationsWorkstationConfigEncryptionKey(**encryption_key)
        if isinstance(host, dict):
            host = GoogleWorkstationsWorkstationConfigHost(**host)
        if isinstance(timeouts, dict):
            timeouts = GoogleWorkstationsWorkstationConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499972dbd65c78d8c138dd5310a4ae9f0353acbbc92733a77fdfb56309446771)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument workstation_cluster_id", value=workstation_cluster_id, expected_type=type_hints["workstation_cluster_id"])
            check_type(argname="argument workstation_config_id", value=workstation_config_id, expected_type=type_hints["workstation_config_id"])
            check_type(argname="argument allowed_ports", value=allowed_ports, expected_type=type_hints["allowed_ports"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument disable_tcp_connections", value=disable_tcp_connections, expected_type=type_hints["disable_tcp_connections"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enable_audit_agent", value=enable_audit_agent, expected_type=type_hints["enable_audit_agent"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument ephemeral_directories", value=ephemeral_directories, expected_type=type_hints["ephemeral_directories"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_usable_workstations", value=max_usable_workstations, expected_type=type_hints["max_usable_workstations"])
            check_type(argname="argument persistent_directories", value=persistent_directories, expected_type=type_hints["persistent_directories"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument readiness_checks", value=readiness_checks, expected_type=type_hints["readiness_checks"])
            check_type(argname="argument replica_zones", value=replica_zones, expected_type=type_hints["replica_zones"])
            check_type(argname="argument running_timeout", value=running_timeout, expected_type=type_hints["running_timeout"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "workstation_cluster_id": workstation_cluster_id,
            "workstation_config_id": workstation_config_id,
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
        if allowed_ports is not None:
            self._values["allowed_ports"] = allowed_ports
        if annotations is not None:
            self._values["annotations"] = annotations
        if container is not None:
            self._values["container"] = container
        if disable_tcp_connections is not None:
            self._values["disable_tcp_connections"] = disable_tcp_connections
        if display_name is not None:
            self._values["display_name"] = display_name
        if enable_audit_agent is not None:
            self._values["enable_audit_agent"] = enable_audit_agent
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if ephemeral_directories is not None:
            self._values["ephemeral_directories"] = ephemeral_directories
        if host is not None:
            self._values["host"] = host
        if id is not None:
            self._values["id"] = id
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if labels is not None:
            self._values["labels"] = labels
        if max_usable_workstations is not None:
            self._values["max_usable_workstations"] = max_usable_workstations
        if persistent_directories is not None:
            self._values["persistent_directories"] = persistent_directories
        if project is not None:
            self._values["project"] = project
        if readiness_checks is not None:
            self._values["readiness_checks"] = readiness_checks
        if replica_zones is not None:
            self._values["replica_zones"] = replica_zones
        if running_timeout is not None:
            self._values["running_timeout"] = running_timeout
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def location(self) -> builtins.str:
        '''The location where the workstation cluster config should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#location GoogleWorkstationsWorkstationConfigA#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workstation_cluster_id(self) -> builtins.str:
        '''The ID of the parent workstation cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#workstation_cluster_id GoogleWorkstationsWorkstationConfigA#workstation_cluster_id}
        '''
        result = self._values.get("workstation_cluster_id")
        assert result is not None, "Required property 'workstation_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workstation_config_id(self) -> builtins.str:
        '''The ID to be assigned to the workstation cluster config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#workstation_config_id GoogleWorkstationsWorkstationConfigA#workstation_config_id}
        '''
        result = self._values.get("workstation_config_id")
        assert result is not None, "Required property 'workstation_config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigAllowedPorts"]]]:
        '''allowed_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#allowed_ports GoogleWorkstationsWorkstationConfigA#allowed_ports}
        '''
        result = self._values.get("allowed_ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigAllowedPorts"]]], result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Client-specified annotations. This is distinct from labels.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#annotations GoogleWorkstationsWorkstationConfigA#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def container(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigContainer"]:
        '''container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#container GoogleWorkstationsWorkstationConfigA#container}
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigContainer"], result)

    @builtins.property
    def disable_tcp_connections(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables support for plain TCP connections in the workstation.

        By default the service supports TCP connections via a websocket relay. Setting this option to true disables that relay, which prevents the usage of services that require plain tcp connections, such as ssh. When enabled, all communication must occur over https or wss.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_tcp_connections GoogleWorkstationsWorkstationConfigA#disable_tcp_connections}
        '''
        result = self._values.get("disable_tcp_connections")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Human-readable name for this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#display_name GoogleWorkstationsWorkstationConfigA#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_audit_agent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable Linux 'auditd' logging on the workstation.

        When enabled, a service account must also be specified that has 'logging.buckets.write' permission on the project. Operating system audit logging is distinct from Cloud Audit Logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_audit_agent GoogleWorkstationsWorkstationConfigA#enable_audit_agent}
        '''
        result = self._values.get("enable_audit_agent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigEncryptionKey"]:
        '''encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#encryption_key GoogleWorkstationsWorkstationConfigA#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigEncryptionKey"], result)

    @builtins.property
    def ephemeral_directories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigEphemeralDirectories"]]]:
        '''ephemeral_directories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#ephemeral_directories GoogleWorkstationsWorkstationConfigA#ephemeral_directories}
        '''
        result = self._values.get("ephemeral_directories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigEphemeralDirectories"]]], result)

    @builtins.property
    def host(self) -> typing.Optional["GoogleWorkstationsWorkstationConfigHost"]:
        '''host block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#host GoogleWorkstationsWorkstationConfigA#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigHost"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#id GoogleWorkstationsWorkstationConfigA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[builtins.str]:
        '''How long to wait before automatically stopping an instance that hasn't recently received any user traffic.

        A value of 0 indicates that this instance should never time out from idleness. Defaults to 20 minutes.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#idle_timeout GoogleWorkstationsWorkstationConfigA#idle_timeout}
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Client-specified labels that are applied to the resource and that are also propagated to the underlying Compute Engine resources.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#labels GoogleWorkstationsWorkstationConfigA#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_usable_workstations(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of workstations under this configuration a user can have workstations.workstation.use permission on. Only enforced on CreateWorkstation API calls on the user issuing the API request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#max_usable_workstations GoogleWorkstationsWorkstationConfigA#max_usable_workstations}
        '''
        result = self._values.get("max_usable_workstations")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def persistent_directories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigPersistentDirectories"]]]:
        '''persistent_directories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#persistent_directories GoogleWorkstationsWorkstationConfigA#persistent_directories}
        '''
        result = self._values.get("persistent_directories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigPersistentDirectories"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#project GoogleWorkstationsWorkstationConfigA#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readiness_checks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigReadinessChecks"]]]:
        '''readiness_checks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#readiness_checks GoogleWorkstationsWorkstationConfigA#readiness_checks}
        '''
        result = self._values.get("readiness_checks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigReadinessChecks"]]], result)

    @builtins.property
    def replica_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the zones used to replicate the VM and disk resources within the region.

        If set, exactly two zones within the workstation cluster's region must be specified—for example, '['us-central1-a', 'us-central1-f']'.
        If this field is empty, two default zones within the region are used. Immutable after the workstation configuration is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#replica_zones GoogleWorkstationsWorkstationConfigA#replica_zones}
        '''
        result = self._values.get("replica_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def running_timeout(self) -> typing.Optional[builtins.str]:
        '''How long to wait before automatically stopping a workstation after it was started.

        A value of 0 indicates that workstations using this configuration should never time out from running duration. Must be greater than 0 and less than 24 hours if 'encryption_key' is set. Defaults to 12 hours.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#running_timeout GoogleWorkstationsWorkstationConfigA#running_timeout}
        '''
        result = self._values.get("running_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#timeouts GoogleWorkstationsWorkstationConfigA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigAllowedPorts",
    jsii_struct_bases=[],
    name_mapping={"first": "first", "last": "last"},
)
class GoogleWorkstationsWorkstationConfigAllowedPorts:
    def __init__(
        self,
        *,
        first: typing.Optional[jsii.Number] = None,
        last: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param first: Starting port number for the current range of ports. Valid ports are 22, 80, and ports within the range 1024-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#first GoogleWorkstationsWorkstationConfigA#first}
        :param last: Ending port number for the current range of ports. Valid ports are 22, 80, and ports within the range 1024-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#last GoogleWorkstationsWorkstationConfigA#last}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f58b81d3b4ed82f3f931e38b854c76095db33dde0fa612386f49624bf2d7f4)
            check_type(argname="argument first", value=first, expected_type=type_hints["first"])
            check_type(argname="argument last", value=last, expected_type=type_hints["last"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if first is not None:
            self._values["first"] = first
        if last is not None:
            self._values["last"] = last

    @builtins.property
    def first(self) -> typing.Optional[jsii.Number]:
        '''Starting port number for the current range of ports.

        Valid ports are 22, 80, and ports within the range 1024-65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#first GoogleWorkstationsWorkstationConfigA#first}
        '''
        result = self._values.get("first")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def last(self) -> typing.Optional[jsii.Number]:
        '''Ending port number for the current range of ports.

        Valid ports are 22, 80, and ports within the range 1024-65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#last GoogleWorkstationsWorkstationConfigA#last}
        '''
        result = self._values.get("last")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigAllowedPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigAllowedPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigAllowedPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f326eecafb3dbd8e0afa34b3a2492e716556a0289bd71d57c6da0e5f98aee1a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigAllowedPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d1f7e92ce0b61ab8f98f76fe87fadbfd9f43bc9b9f94de2b0760d23de1bfe4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigAllowedPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cac8478e3988f3cf02a12fbc263baa28bb81ca71d2774e5ed676dabc1799fef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__159d78ce74f927698752bdae0035cf54ded551658de0b46d3c0155dcb23a21de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b0c61ab9d0cb1d3d9d2a4f6af0886a4ef29dd40faa426bb668524f69965b191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigAllowedPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigAllowedPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigAllowedPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab8ab6f8058d59eef6e7b9dd142e15977600a93ef4146db3e2692d0c1d6b98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigAllowedPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigAllowedPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc77bef800a9ad79e36511b0b4dbc645f5c2d013bcbb735e3fe0d6353649b3ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFirst")
    def reset_first(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirst", []))

    @jsii.member(jsii_name="resetLast")
    def reset_last(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLast", []))

    @builtins.property
    @jsii.member(jsii_name="firstInput")
    def first_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstInput"))

    @builtins.property
    @jsii.member(jsii_name="lastInput")
    def last_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lastInput"))

    @builtins.property
    @jsii.member(jsii_name="first")
    def first(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "first"))

    @first.setter
    def first(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b187ea5abeee5bad2bc4ee91e8470172a83f08e27bdc497bf80af4b0e520f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "first", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="last")
    def last(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "last"))

    @last.setter
    def last(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9032b8337d0eb3aec05fce76b820fce2781f2d37fd3a9fb567551e558aa5e2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "last", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigAllowedPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigAllowedPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigAllowedPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb015108af9525a332d368df1e2802bf2143eb1d6dccf96c2cc0246edbe5cc3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleWorkstationsWorkstationConfigConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__926f6b1027ebe7212eaf588c07b841e3e9c7617a0078272f8e31b877918e891c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc32063dc52d49ea3ba89d16e4d05882015aa41f8ac7c94d42e2de41ba7571f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728c853705f52422940e97bbedde4becc6a35f3e9e7b262bdb531537d413b9db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d46767c923c753d1d38b714ede4591a724cfd731b8aedac64f89cdcc99ea13e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97a64d392b96421e6c3a6579d727a9fbbf9a5b06deacde9626c0c642779af6e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4bfd088d67a9c3bcf1534acd939332ebb48bc8b9940c097aac6c636dc0f37b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigConditions]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f34a6c56609560b95ae867fbcc6c1b5fc06d2c7280201c447758b43c58a216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigContainer",
    jsii_struct_bases=[],
    name_mapping={
        "args": "args",
        "command": "command",
        "env": "env",
        "image": "image",
        "run_as_user": "runAsUser",
        "working_dir": "workingDir",
    },
)
class GoogleWorkstationsWorkstationConfigContainer:
    def __init__(
        self,
        *,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        run_as_user: typing.Optional[jsii.Number] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param args: Arguments passed to the entrypoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#args GoogleWorkstationsWorkstationConfigA#args}
        :param command: If set, overrides the default ENTRYPOINT specified by the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#command GoogleWorkstationsWorkstationConfigA#command}
        :param env: Environment variables passed to the container. The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#env GoogleWorkstationsWorkstationConfigA#env}
        :param image: Docker image defining the container. This image must be accessible by the config's service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#image GoogleWorkstationsWorkstationConfigA#image}
        :param run_as_user: If set, overrides the USER specified in the image with the given uid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#run_as_user GoogleWorkstationsWorkstationConfigA#run_as_user}
        :param working_dir: If set, overrides the default DIR specified by the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#working_dir GoogleWorkstationsWorkstationConfigA#working_dir}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee3c2b8b5274b5347acb61996a061437891d4182fcece602107a439113dd209)
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument run_as_user", value=run_as_user, expected_type=type_hints["run_as_user"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if env is not None:
            self._values["env"] = env
        if image is not None:
            self._values["image"] = image
        if run_as_user is not None:
            self._values["run_as_user"] = run_as_user
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments passed to the entrypoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#args GoogleWorkstationsWorkstationConfigA#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If set, overrides the default ENTRYPOINT specified by the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#command GoogleWorkstationsWorkstationConfigA#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables passed to the container.

        The elements are of the form "KEY=VALUE" for the environment variable "KEY" being given the value "VALUE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#env GoogleWorkstationsWorkstationConfigA#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Docker image defining the container. This image must be accessible by the config's service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#image GoogleWorkstationsWorkstationConfigA#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_as_user(self) -> typing.Optional[jsii.Number]:
        '''If set, overrides the USER specified in the image with the given uid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#run_as_user GoogleWorkstationsWorkstationConfigA#run_as_user}
        '''
        result = self._values.get("run_as_user")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''If set, overrides the default DIR specified by the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#working_dir GoogleWorkstationsWorkstationConfigA#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigContainerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa7be205d9b22c30643b6a509851ceaadd1b3bf081be398b88b00f7276df65a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetRunAsUser")
    def reset_run_as_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunAsUser", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="runAsUserInput")
    def run_as_user_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runAsUserInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7a114fce1a035739268e45f8785c76f44920f289bc6c839527973b782b980f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436a7f6ca41947260de5006a049e87d9ce5a4a4e0471a834ed49e5b506e1e3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a5a1c1635b54adb3c0fd68ffc2c52ce32076f1ec02ded213c69e7791cc5860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0584a721510e9ea85d6233389140714e69604aea913a1f8ac61977668e27e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runAsUser")
    def run_as_user(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "runAsUser"))

    @run_as_user.setter
    def run_as_user(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409adb56cc758b9cdc6e686d1448e044d35eebddb393144c680695571acac1db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runAsUser", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f268b6080efda9a6ba062c4bba6bc07792524ea3f4e68a009b82647a4cd14b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigContainer]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a687a265049caefe5b90b2cc207c5b4ba6f806e6224c07118be9e9702857d8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key": "kmsKey",
        "kms_key_service_account": "kmsKeyServiceAccount",
    },
)
class GoogleWorkstationsWorkstationConfigEncryptionKey:
    def __init__(
        self,
        *,
        kms_key: builtins.str,
        kms_key_service_account: builtins.str,
    ) -> None:
        '''
        :param kms_key: The name of the Google Cloud KMS encryption key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#kms_key GoogleWorkstationsWorkstationConfigA#kms_key}
        :param kms_key_service_account: The service account to use with the specified KMS key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#kms_key_service_account GoogleWorkstationsWorkstationConfigA#kms_key_service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2374a9d7609f16534dc028e3d48c8185bfded8860ace4c9babde631a15bfc31)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key": kms_key,
            "kms_key_service_account": kms_key_service_account,
        }

    @builtins.property
    def kms_key(self) -> builtins.str:
        '''The name of the Google Cloud KMS encryption key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#kms_key GoogleWorkstationsWorkstationConfigA#kms_key}
        '''
        result = self._values.get("kms_key")
        assert result is not None, "Required property 'kms_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_service_account(self) -> builtins.str:
        '''The service account to use with the specified KMS key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#kms_key_service_account GoogleWorkstationsWorkstationConfigA#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        assert result is not None, "Required property 'kms_key_service_account' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ff735894586a2f1f7c915ff41c8e36df03309f17991b2f7b14dc3807f588d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10466771bd7e9cb3f4ef36b066198e0903ce852957ff534637bcc32ab53844b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f66aa319faee9ebe86a7092822a6f8c9667fa66b60f51550c756d7239fc548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigEncryptionKey]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cd8b9602876268a2975f55b16cd62c1d7a8bee4ae1e09f6122f9bf797e9bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEphemeralDirectories",
    jsii_struct_bases=[],
    name_mapping={"gce_pd": "gcePd", "mount_path": "mountPath"},
)
class GoogleWorkstationsWorkstationConfigEphemeralDirectories:
    def __init__(
        self,
        *,
        gce_pd: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd", typing.Dict[builtins.str, typing.Any]]] = None,
        mount_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gce_pd: gce_pd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_pd GoogleWorkstationsWorkstationConfigA#gce_pd}
        :param mount_path: Location of this directory in the running workstation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#mount_path GoogleWorkstationsWorkstationConfigA#mount_path}
        '''
        if isinstance(gce_pd, dict):
            gce_pd = GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd(**gce_pd)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382cab08bc0ae440c700a39a8f6cdec5113728641faf1b8799c002a3119ed990)
            check_type(argname="argument gce_pd", value=gce_pd, expected_type=type_hints["gce_pd"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gce_pd is not None:
            self._values["gce_pd"] = gce_pd
        if mount_path is not None:
            self._values["mount_path"] = mount_path

    @builtins.property
    def gce_pd(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd"]:
        '''gce_pd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_pd GoogleWorkstationsWorkstationConfigA#gce_pd}
        '''
        result = self._values.get("gce_pd")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd"], result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''Location of this directory in the running workstation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#mount_path GoogleWorkstationsWorkstationConfigA#mount_path}
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigEphemeralDirectories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd",
    jsii_struct_bases=[],
    name_mapping={
        "disk_type": "diskType",
        "read_only": "readOnly",
        "source_image": "sourceImage",
        "source_snapshot": "sourceSnapshot",
    },
)
class GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd:
    def __init__(
        self,
        *,
        disk_type: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_image: typing.Optional[builtins.str] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: Type of the disk to use. Defaults to '"pd-standard"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disk_type GoogleWorkstationsWorkstationConfigA#disk_type}
        :param read_only: Whether the disk is read only. If true, the disk may be shared by multiple VMs and 'sourceSnapshot' must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#read_only GoogleWorkstationsWorkstationConfigA#read_only}
        :param source_image: Name of the disk image to use as the source for the disk. Must be empty 'sourceSnapshot' is set. Updating 'sourceImage' will update content in the ephemeral directory after the workstation is restarted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_image GoogleWorkstationsWorkstationConfigA#source_image}
        :param source_snapshot: Name of the snapshot to use as the source for the disk. Must be empty if 'sourceImage' is set. Must be empty if 'read_only' is false. Updating 'source_snapshot' will update content in the ephemeral directory after the workstation is restarted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_snapshot GoogleWorkstationsWorkstationConfigA#source_snapshot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2437d13d3345be5585464b4703ded4ba0269930fadc14ddc4cf8cacd02f313)
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument source_image", value=source_image, expected_type=type_hints["source_image"])
            check_type(argname="argument source_snapshot", value=source_snapshot, expected_type=type_hints["source_snapshot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if read_only is not None:
            self._values["read_only"] = read_only
        if source_image is not None:
            self._values["source_image"] = source_image
        if source_snapshot is not None:
            self._values["source_snapshot"] = source_snapshot

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''Type of the disk to use. Defaults to '"pd-standard"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disk_type GoogleWorkstationsWorkstationConfigA#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the disk is read only.

        If true, the disk may be shared by multiple VMs and 'sourceSnapshot' must be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#read_only GoogleWorkstationsWorkstationConfigA#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_image(self) -> typing.Optional[builtins.str]:
        '''Name of the disk image to use as the source for the disk.

        Must be empty 'sourceSnapshot' is set.
        Updating 'sourceImage' will update content in the ephemeral directory after the workstation is restarted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_image GoogleWorkstationsWorkstationConfigA#source_image}
        '''
        result = self._values.get("source_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''Name of the snapshot to use as the source for the disk.

        Must be empty if 'sourceImage' is set.
        Must be empty if 'read_only' is false.
        Updating 'source_snapshot' will update content in the ephemeral directory after the workstation is restarted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_snapshot GoogleWorkstationsWorkstationConfigA#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b4656fb02b7baed0efe16e37965edf70e5c236abc434d51e891563c593470aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSourceImage")
    def reset_source_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImage", []))

    @jsii.member(jsii_name="resetSourceSnapshot")
    def reset_source_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshot", []))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageInput")
    def source_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceImageInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotInput")
    def source_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013935e4b495ade832fa9ed67311391b621cabaf3ee4cce6c0056d1a9814e551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e811179feea4a539539f60244ee7fd82e6213ce12e600a6284e2473aba0e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceImage")
    def source_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImage"))

    @source_image.setter
    def source_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cf0f08d562ede071e2c9f6ea64fb920709c27d62306cb1561de8d0f270225f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1475cb30206c7f46a415b26bb9a360bfe68ad91cf8db98be33900250a82990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe1003e293f6ab84058f2272efaf4ecbcb82c96d00451cdfc706d0430a5001f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigEphemeralDirectoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEphemeralDirectoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__360ad4506c83b60c43aaedb6dbc0ae63b900e246cff6eeb26b7ee9e24c02df98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ca72b3236d91c99faf4680436cfa77dc5a00582e902e51b850e3e6da2adb3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigEphemeralDirectoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be10e5a5a2593864283a1a50fad496edeacdac47620fbb72176a5482f6aeb0ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b8e9588c5053ca2668fe19490f258a9a1202dea21516c35ff398cd2c221842)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f820ca073abccbe548ce1b0f21e3ea13da363c786cf757a56dab28bae138df65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigEphemeralDirectories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigEphemeralDirectories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigEphemeralDirectories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e4da5413ef5f3345c195b0495b33560a133f218a0071728e8d5480f096eccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigEphemeralDirectoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigEphemeralDirectoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0628afbcc323da1ff6d6ed0fd872b432203e0287571c742b1db5ee2d2563951d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGcePd")
    def put_gce_pd(
        self,
        *,
        disk_type: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_image: typing.Optional[builtins.str] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: Type of the disk to use. Defaults to '"pd-standard"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disk_type GoogleWorkstationsWorkstationConfigA#disk_type}
        :param read_only: Whether the disk is read only. If true, the disk may be shared by multiple VMs and 'sourceSnapshot' must be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#read_only GoogleWorkstationsWorkstationConfigA#read_only}
        :param source_image: Name of the disk image to use as the source for the disk. Must be empty 'sourceSnapshot' is set. Updating 'sourceImage' will update content in the ephemeral directory after the workstation is restarted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_image GoogleWorkstationsWorkstationConfigA#source_image}
        :param source_snapshot: Name of the snapshot to use as the source for the disk. Must be empty if 'sourceImage' is set. Must be empty if 'read_only' is false. Updating 'source_snapshot' will update content in the ephemeral directory after the workstation is restarted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_snapshot GoogleWorkstationsWorkstationConfigA#source_snapshot}
        '''
        value = GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd(
            disk_type=disk_type,
            read_only=read_only,
            source_image=source_image,
            source_snapshot=source_snapshot,
        )

        return typing.cast(None, jsii.invoke(self, "putGcePd", [value]))

    @jsii.member(jsii_name="resetGcePd")
    def reset_gce_pd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcePd", []))

    @jsii.member(jsii_name="resetMountPath")
    def reset_mount_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountPath", []))

    @builtins.property
    @jsii.member(jsii_name="gcePd")
    def gce_pd(
        self,
    ) -> GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePdOutputReference:
        return typing.cast(GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePdOutputReference, jsii.get(self, "gcePd"))

    @builtins.property
    @jsii.member(jsii_name="gcePdInput")
    def gce_pd_input(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd], jsii.get(self, "gcePdInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c5a6a27393bf954c81514833e9876ae7bd8d99a4c710b3dedc1cf228fe462f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigEphemeralDirectories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigEphemeralDirectories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigEphemeralDirectories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6a100c0fea855b20eca12f0d7ae9bf98974d19bcda44468b78762317beeb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHost",
    jsii_struct_bases=[],
    name_mapping={"gce_instance": "gceInstance"},
)
class GoogleWorkstationsWorkstationConfigHost:
    def __init__(
        self,
        *,
        gce_instance: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstance", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param gce_instance: gce_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_instance GoogleWorkstationsWorkstationConfigA#gce_instance}
        '''
        if isinstance(gce_instance, dict):
            gce_instance = GoogleWorkstationsWorkstationConfigHostGceInstance(**gce_instance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9759a9085cb20c5b3e7008d4df98bb21c50f25e15b6ca5cf235d3c3e25b55d6)
            check_type(argname="argument gce_instance", value=gce_instance, expected_type=type_hints["gce_instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gce_instance is not None:
            self._values["gce_instance"] = gce_instance

    @builtins.property
    def gce_instance(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstance"]:
        '''gce_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_instance GoogleWorkstationsWorkstationConfigA#gce_instance}
        '''
        result = self._values.get("gce_instance")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstance"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHost(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstance",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "boost_configs": "boostConfigs",
        "boot_disk_size_gb": "bootDiskSizeGb",
        "confidential_instance_config": "confidentialInstanceConfig",
        "disable_public_ip_addresses": "disablePublicIpAddresses",
        "disable_ssh": "disableSsh",
        "enable_nested_virtualization": "enableNestedVirtualization",
        "machine_type": "machineType",
        "pool_size": "poolSize",
        "service_account": "serviceAccount",
        "service_account_scopes": "serviceAccountScopes",
        "shielded_instance_config": "shieldedInstanceConfig",
        "tags": "tags",
        "vm_tags": "vmTags",
    },
)
class GoogleWorkstationsWorkstationConfigHostGceInstance:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boost_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        confidential_instance_config: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_public_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_ssh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        pool_size: typing.Optional[jsii.Number] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#accelerators GoogleWorkstationsWorkstationConfigA#accelerators}
        :param boost_configs: boost_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boost_configs GoogleWorkstationsWorkstationConfigA#boost_configs}
        :param boot_disk_size_gb: Size of the boot disk in GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boot_disk_size_gb GoogleWorkstationsWorkstationConfigA#boot_disk_size_gb}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#confidential_instance_config GoogleWorkstationsWorkstationConfigA#confidential_instance_config}
        :param disable_public_ip_addresses: Whether instances have no public IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_public_ip_addresses GoogleWorkstationsWorkstationConfigA#disable_public_ip_addresses}
        :param disable_ssh: Whether to disable SSH access to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_ssh GoogleWorkstationsWorkstationConfigA#disable_ssh}
        :param enable_nested_virtualization: Whether to enable nested virtualization on the Compute Engine VMs backing the Workstations. See https://cloud.google.com/workstations/docs/reference/rest/v1beta/projects.locations.workstationClusters.workstationConfigs#GceInstance.FIELDS.enable_nested_virtualization Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_nested_virtualization GoogleWorkstationsWorkstationConfigA#enable_nested_virtualization}
        :param machine_type: The name of a Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#machine_type GoogleWorkstationsWorkstationConfigA#machine_type}
        :param pool_size: Number of instances to pool for faster workstation startup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#pool_size GoogleWorkstationsWorkstationConfigA#pool_size}
        :param service_account: Email address of the service account that will be used on VM instances used to support this config. This service account must have permission to pull the specified container image. If not set, VMs will run without a service account, in which case the image must be publicly accessible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#service_account GoogleWorkstationsWorkstationConfigA#service_account}
        :param service_account_scopes: Scopes to grant to the service_account. Various scopes are automatically added based on feature usage. When specified, users of workstations under this configuration must have 'iam.serviceAccounts.actAs' on the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#service_account_scopes GoogleWorkstationsWorkstationConfigA#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#shielded_instance_config GoogleWorkstationsWorkstationConfigA#shielded_instance_config}
        :param tags: Network tags to add to the Compute Engine machines backing the Workstations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#tags GoogleWorkstationsWorkstationConfigA#tags}
        :param vm_tags: Resource manager tags to be bound to the VM instances backing the Workstations. Tag keys and values have the same definition as https://cloud.google.com/resource-manager/docs/tags/tags-overview Keys must be in the format 'tagKeys/{tag_key_id}', and values are in the format 'tagValues/456'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#vm_tags GoogleWorkstationsWorkstationConfigA#vm_tags}
        '''
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig(**shielded_instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39e1f925701dddc052ba6789c97303f918868f6c90b10ab132797a2ebba2fcc)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument boost_configs", value=boost_configs, expected_type=type_hints["boost_configs"])
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument confidential_instance_config", value=confidential_instance_config, expected_type=type_hints["confidential_instance_config"])
            check_type(argname="argument disable_public_ip_addresses", value=disable_public_ip_addresses, expected_type=type_hints["disable_public_ip_addresses"])
            check_type(argname="argument disable_ssh", value=disable_ssh, expected_type=type_hints["disable_ssh"])
            check_type(argname="argument enable_nested_virtualization", value=enable_nested_virtualization, expected_type=type_hints["enable_nested_virtualization"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument pool_size", value=pool_size, expected_type=type_hints["pool_size"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument service_account_scopes", value=service_account_scopes, expected_type=type_hints["service_account_scopes"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vm_tags", value=vm_tags, expected_type=type_hints["vm_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if boost_configs is not None:
            self._values["boost_configs"] = boost_configs
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if confidential_instance_config is not None:
            self._values["confidential_instance_config"] = confidential_instance_config
        if disable_public_ip_addresses is not None:
            self._values["disable_public_ip_addresses"] = disable_public_ip_addresses
        if disable_ssh is not None:
            self._values["disable_ssh"] = disable_ssh
        if enable_nested_virtualization is not None:
            self._values["enable_nested_virtualization"] = enable_nested_virtualization
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if pool_size is not None:
            self._values["pool_size"] = pool_size
        if service_account is not None:
            self._values["service_account"] = service_account
        if service_account_scopes is not None:
            self._values["service_account_scopes"] = service_account_scopes
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if tags is not None:
            self._values["tags"] = tags
        if vm_tags is not None:
            self._values["vm_tags"] = vm_tags

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#accelerators GoogleWorkstationsWorkstationConfigA#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators"]]], result)

    @builtins.property
    def boost_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs"]]]:
        '''boost_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boost_configs GoogleWorkstationsWorkstationConfigA#boost_configs}
        '''
        result = self._values.get("boost_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs"]]], result)

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the boot disk in GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boot_disk_size_gb GoogleWorkstationsWorkstationConfigA#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig"]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#confidential_instance_config GoogleWorkstationsWorkstationConfigA#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig"], result)

    @builtins.property
    def disable_public_ip_addresses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether instances have no public IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_public_ip_addresses GoogleWorkstationsWorkstationConfigA#disable_public_ip_addresses}
        '''
        result = self._values.get("disable_public_ip_addresses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_ssh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable SSH access to the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_ssh GoogleWorkstationsWorkstationConfigA#disable_ssh}
        '''
        result = self._values.get("disable_ssh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_nested_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable nested virtualization on the Compute Engine VMs backing the Workstations.

        See https://cloud.google.com/workstations/docs/reference/rest/v1beta/projects.locations.workstationClusters.workstationConfigs#GceInstance.FIELDS.enable_nested_virtualization

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_nested_virtualization GoogleWorkstationsWorkstationConfigA#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Compute Engine machine type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#machine_type GoogleWorkstationsWorkstationConfigA#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool_size(self) -> typing.Optional[jsii.Number]:
        '''Number of instances to pool for faster workstation startup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#pool_size GoogleWorkstationsWorkstationConfigA#pool_size}
        '''
        result = self._values.get("pool_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Email address of the service account that will be used on VM instances used to support this config.

        This service account must have permission to pull the specified container image. If not set, VMs will run without a service account, in which case the image must be publicly accessible.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#service_account GoogleWorkstationsWorkstationConfigA#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Scopes to grant to the service_account.

        Various scopes are automatically added based on feature usage. When specified, users of workstations under this configuration must have 'iam.serviceAccounts.actAs' on the service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#service_account_scopes GoogleWorkstationsWorkstationConfigA#service_account_scopes}
        '''
        result = self._values.get("service_account_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#shielded_instance_config GoogleWorkstationsWorkstationConfigA#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Network tags to add to the Compute Engine machines backing the Workstations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#tags GoogleWorkstationsWorkstationConfigA#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vm_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource manager tags to be bound to the VM instances backing the Workstations.

        Tag keys and values have the same definition as
        https://cloud.google.com/resource-manager/docs/tags/tags-overview
        Keys must be in the format 'tagKeys/{tag_key_id}', and
        values are in the format 'tagValues/456'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#vm_tags GoogleWorkstationsWorkstationConfigA#vm_tags}
        '''
        result = self._values.get("vm_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHostGceInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "type": "type"},
)
class GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators:
    def __init__(self, *, count: jsii.Number, type: builtins.str) -> None:
        '''
        :param count: Number of accelerator cards exposed to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#count GoogleWorkstationsWorkstationConfigA#count}
        :param type: Type of accelerator resource to attach to the instance, for example, "nvidia-tesla-p100". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#type GoogleWorkstationsWorkstationConfigA#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefc2e6a2375cea379bd914e81cf88ca53fd87c3e6cae3a4fbf60eb3261ab4ee)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Number of accelerator cards exposed to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#count GoogleWorkstationsWorkstationConfigA#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of accelerator resource to attach to the instance, for example, "nvidia-tesla-p100".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#type GoogleWorkstationsWorkstationConfigA#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d58a07754cacc47e46c0213559188fdc815e3d53aa74eb04a606e0ef2e0024)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8090ce369ba802e5b65ed01e25d72c9cd29b88c0228fa799da6bdc1adf99405d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbe8558db163dd96acf7d6eb08684f9fe5c796ad08b1878d190af1e598fc06d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__293ad06462c9de9ff76aa1c6d26c9fecd1fa0771c88569dcdc918e9c8bc6f6ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e349d84dcc4ea0283de7d8316c3e8390132f5bf0e29eceb2f85b7c8bf59291fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c49c8e85aa1d3eca356141e1f5f9a14ab5fb1f0cf53b4cc920e710b12240bf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65631060222940dd4ec7b476f198ef0968a4a404db170eaf1767f079f07665ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478b634ffce09b9b63627396f9e330df63d6326d8113c6e980f6e109c286e8dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e92ab58999ec8597905e8a91afe1ee9508b531011e2739839dde8f864d180a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584e1acd0fd51cca2d7b2bcdaa3dc2091e61270cc6f6ee5aeff00b80eb8d393a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "accelerators": "accelerators",
        "boot_disk_size_gb": "bootDiskSizeGb",
        "enable_nested_virtualization": "enableNestedVirtualization",
        "machine_type": "machineType",
        "pool_size": "poolSize",
    },
)
class GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs:
    def __init__(
        self,
        *,
        id: builtins.str,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        pool_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param id: The id to be used for the boost config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#id GoogleWorkstationsWorkstationConfigA#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#accelerators GoogleWorkstationsWorkstationConfigA#accelerators}
        :param boot_disk_size_gb: Size of the boot disk in GB. The minimum boot disk size is '30' GB. Defaults to '50' GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boot_disk_size_gb GoogleWorkstationsWorkstationConfigA#boot_disk_size_gb}
        :param enable_nested_virtualization: Whether to enable nested virtualization on the Compute Engine VMs backing boosted Workstations. See https://cloud.google.com/workstations/docs/reference/rest/v1beta/projects.locations.workstationClusters.workstationConfigs#GceInstance.FIELDS.enable_nested_virtualization Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_nested_virtualization GoogleWorkstationsWorkstationConfigA#enable_nested_virtualization}
        :param machine_type: The type of machine that boosted VM instances will use—for example, e2-standard-4. For more information about machine types that Cloud Workstations supports, see the list of available machine types https://cloud.google.com/workstations/docs/available-machine-types. Defaults to e2-standard-4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#machine_type GoogleWorkstationsWorkstationConfigA#machine_type}
        :param pool_size: Number of instances to pool for faster workstation boosting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#pool_size GoogleWorkstationsWorkstationConfigA#pool_size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6c47588a147d60ba181efc64c706e1888b0dfc7a2a4dc07979ce93ee1109ed)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument enable_nested_virtualization", value=enable_nested_virtualization, expected_type=type_hints["enable_nested_virtualization"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument pool_size", value=pool_size, expected_type=type_hints["pool_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if enable_nested_virtualization is not None:
            self._values["enable_nested_virtualization"] = enable_nested_virtualization
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if pool_size is not None:
            self._values["pool_size"] = pool_size

    @builtins.property
    def id(self) -> builtins.str:
        '''The id to be used for the boost config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#id GoogleWorkstationsWorkstationConfigA#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#accelerators GoogleWorkstationsWorkstationConfigA#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators"]]], result)

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the boot disk in GB. The minimum boot disk size is '30' GB. Defaults to '50' GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boot_disk_size_gb GoogleWorkstationsWorkstationConfigA#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_nested_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable nested virtualization on the Compute Engine VMs backing boosted Workstations.

        See https://cloud.google.com/workstations/docs/reference/rest/v1beta/projects.locations.workstationClusters.workstationConfigs#GceInstance.FIELDS.enable_nested_virtualization

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_nested_virtualization GoogleWorkstationsWorkstationConfigA#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The type of machine that boosted VM instances will use—for example, e2-standard-4.

        For more information about machine types that Cloud Workstations supports, see the list of available machine types https://cloud.google.com/workstations/docs/available-machine-types. Defaults to e2-standard-4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#machine_type GoogleWorkstationsWorkstationConfigA#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool_size(self) -> typing.Optional[jsii.Number]:
        '''Number of instances to pool for faster workstation boosting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#pool_size GoogleWorkstationsWorkstationConfigA#pool_size}
        '''
        result = self._values.get("pool_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "type": "type"},
)
class GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators:
    def __init__(self, *, count: jsii.Number, type: builtins.str) -> None:
        '''
        :param count: Number of accelerator cards exposed to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#count GoogleWorkstationsWorkstationConfigA#count}
        :param type: Type of accelerator resource to attach to the instance, for example, "nvidia-tesla-p100". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#type GoogleWorkstationsWorkstationConfigA#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499f12009b47e1a910b225680bc23004127332aa4ca345cd003ae8ef525cf3cf)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Number of accelerator cards exposed to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#count GoogleWorkstationsWorkstationConfigA#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of accelerator resource to attach to the instance, for example, "nvidia-tesla-p100".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#type GoogleWorkstationsWorkstationConfigA#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d5d403ad8f5540a96cc012a71f9ff3deeb4ea02830a3c9dc1736bfe8f062f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba20d05530270f0284061a520e6d0928233fc80acd4e7812a0b66b498ce4a238)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96945aab14e771ffd9db6074b74a1c0d838c873d1b79654d8eba53eb6e46f350)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e84931f6f99b9081546e07835447175e44c9af2a9f1426b9abbc545905afbb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a05e537febb025143c9e3cbf64c1f5a60b3d1ab38ab54e2881513a26abfda18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265a6a888743ec13cacf92a1f3c08a2b338a9c1ffcaacaf1f688894c0bcf00ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa6257399fba018374e682c7964230a507f082f883deb1bcb285483d16d8ad8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fefb7af4f377d76603dcc73e7067718d91108d0c2578d5985dd8c130d509df2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba3da83d3f18cf97020c954c05fbc7afa444536908e258c87e0094e73339d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0e8b8cea2ba58f57be4eab921d5ac467c89ccedf0b1ffeb265bfa424f54029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bccbcdfb4b14998d6dab0990059f29f166442561f48b73f7d0f0640a2cab87c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f5f42b202c2a46fa5cb03e84c89e31a7c30e49de8272d89423e5fed9a4cab9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185dc12ae84b64355c3fa35f6a7b167e9cc793f5ee6e5ea62ef605d446a3ef1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb4a6bb8cec94c44dee153b8106f8b1c628e7c87a03dde832ffa20422f101c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f7027ef8d670ea3bc86b2f4bd7235a3dba52f6a7ab9fb85f5474925c3f3017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5473f5fbfda1dcb8a0bc7f173fbdafcec6d1fb2c5b09072cd6eb5ef454293fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40bcffc28c597a390a825c7a976bfbde34e657d4bc812a0f4099de4877937f99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91083237c543372abb5b33a863f843b31887777d42d7b238e3c2274481b9ec12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetEnableNestedVirtualization")
    def reset_enable_nested_virtualization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNestedVirtualization", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetPoolSize")
    def reset_pool_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoolSize", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsList:
        return typing.cast(GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualizationInput")
    def enable_nested_virtualization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNestedVirtualizationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="poolSizeInput")
    def pool_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "poolSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10d05f2103c9fc5cf326d727f75365761493244922fd832ecb194baadea3cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualization")
    def enable_nested_virtualization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNestedVirtualization"))

    @enable_nested_virtualization.setter
    def enable_nested_virtualization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001c1afa2512923d1326bd6f60749c6defdb21a61494371400bed02d64a8ad6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNestedVirtualization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a5769ade1f42df8b50c2892272b9b558a488c47b69694addbed17961552afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d48f2354ffbf8994cd9a423292f79ba1af621a698b3fcf62c646460ad284b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolSize")
    def pool_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "poolSize"))

    @pool_size.setter
    def pool_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e65b48be753c86f337da0a77f31226428086909dfcf7f202dfe4a87723f7e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed16c4c9b223dc874ba29f92b6d17c3d1fe4e1cc79c558b9e351e0b93532880b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_confidential_compute": "enableConfidentialCompute"},
)
class GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_confidential_compute: Whether the instance has confidential compute enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_confidential_compute GoogleWorkstationsWorkstationConfigA#enable_confidential_compute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffbf2f9889f95415a9ac02883d43030cd45dd6175ef5cc4baa90becc60fedb9f)
            check_type(argname="argument enable_confidential_compute", value=enable_confidential_compute, expected_type=type_hints["enable_confidential_compute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_confidential_compute is not None:
            self._values["enable_confidential_compute"] = enable_confidential_compute

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance has confidential compute enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_confidential_compute GoogleWorkstationsWorkstationConfigA#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb0319faa3002c3aec6ccb592f91d1756737fababdf9f7baae2ea712680ba541)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableConfidentialCompute")
    def reset_enable_confidential_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConfidentialCompute", []))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialComputeInput")
    def enable_confidential_compute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConfidentialComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialCompute")
    def enable_confidential_compute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConfidentialCompute"))

    @enable_confidential_compute.setter
    def enable_confidential_compute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f26c4045e0d592ceda819d746823fa476168c9688493a5790af5b4b0bbbeb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3e76bc60612b029f9f0e4d918ae14c3370b67f5bec65e212dd8f60a2db9e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigHostGceInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__714b06735ce8f6ee237eb380d055511f78f18d4423d73f71608124b8d54c54a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5cdf963d6f107587519c93097d28036b4aa1c865622ff84b8408c36da9a97c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putBoostConfigs")
    def put_boost_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4128a6d2035fb1b9557c31283b6134b7f136b6341b29274d30036f66d940c6ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBoostConfigs", [value]))

    @jsii.member(jsii_name="putConfidentialInstanceConfig")
    def put_confidential_instance_config(
        self,
        *,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_confidential_compute: Whether the instance has confidential compute enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_confidential_compute GoogleWorkstationsWorkstationConfigA#enable_confidential_compute}
        '''
        value = GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig(
            enable_confidential_compute=enable_confidential_compute
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Whether the instance has integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_integrity_monitoring GoogleWorkstationsWorkstationConfigA#enable_integrity_monitoring}
        :param enable_secure_boot: Whether the instance has Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_secure_boot GoogleWorkstationsWorkstationConfigA#enable_secure_boot}
        :param enable_vtpm: Whether the instance has the vTPM enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_vtpm GoogleWorkstationsWorkstationConfigA#enable_vtpm}
        '''
        value = GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetBoostConfigs")
    def reset_boost_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBoostConfigs", []))

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetConfidentialInstanceConfig")
    def reset_confidential_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceConfig", []))

    @jsii.member(jsii_name="resetDisablePublicIpAddresses")
    def reset_disable_public_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePublicIpAddresses", []))

    @jsii.member(jsii_name="resetDisableSsh")
    def reset_disable_ssh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableSsh", []))

    @jsii.member(jsii_name="resetEnableNestedVirtualization")
    def reset_enable_nested_virtualization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNestedVirtualization", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetPoolSize")
    def reset_pool_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoolSize", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServiceAccountScopes")
    def reset_service_account_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountScopes", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVmTags")
    def reset_vm_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmTags", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(
        self,
    ) -> GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsList:
        return typing.cast(GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="boostConfigs")
    def boost_configs(
        self,
    ) -> GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsList:
        return typing.cast(GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsList, jsii.get(self, "boostConfigs"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfigOutputReference:
        return typing.cast(GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfigOutputReference, jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfigOutputReference":
        return typing.cast("GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="boostConfigsInput")
    def boost_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]], jsii.get(self, "boostConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfigInput")
    def confidential_instance_config_input(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePublicIpAddressesInput")
    def disable_public_ip_addresses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePublicIpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="disableSshInput")
    def disable_ssh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableSshInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualizationInput")
    def enable_nested_virtualization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNestedVirtualizationInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="poolSizeInput")
    def pool_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "poolSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopesInput")
    def service_account_scopes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAccountScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vmTagsInput")
    def vm_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "vmTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97af91076cba83f612a010f9962917ae8099ff6bb087308f2bd4d08027cfdb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disablePublicIpAddresses")
    def disable_public_ip_addresses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePublicIpAddresses"))

    @disable_public_ip_addresses.setter
    def disable_public_ip_addresses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88fde7136ef5a899104774389d4dad77f9ac4bf110283b00f7aba860dfec5a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePublicIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableSsh")
    def disable_ssh(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableSsh"))

    @disable_ssh.setter
    def disable_ssh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633230e7dc5fc2be81cf6ab2b5fb1f87f1b63891dc21fd13947b027256399b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableSsh", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualization")
    def enable_nested_virtualization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNestedVirtualization"))

    @enable_nested_virtualization.setter
    def enable_nested_virtualization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7e3e729379ff16041ac9f8cc83067b568b9e9222e494a22af0547af0eb83c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNestedVirtualization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23b9a77c60fdffd0eef8648ba54683ae83870ff81e9a2dd317d2e775649b0ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolSize")
    def pool_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "poolSize"))

    @pool_size.setter
    def pool_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91862460504d6ad1d7868bd4fb19f814b4dffa77d04a8997da1033981316548f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c146d1412f59607e222b04f9e0d6f43cb142d422b2c404613b81f0586bb9c5b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopes")
    def service_account_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAccountScopes"))

    @service_account_scopes.setter
    def service_account_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e164e0e0be52dc73accd2849cf3ae761968d4a28943e55e735386aecc76f3af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0951ed20079cdd72c8ed1ae3d4f89afb931e36edd30445cf80347a72c38e57d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmTags")
    def vm_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "vmTags"))

    @vm_tags.setter
    def vm_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e13043a5128dc4acd3afe8ab4d9a216318842696765a3431b88509453726006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstance]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab83c4a070b1bc059348067da93b9503041561b19d028941eba106f05f37da56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Whether the instance has integrity monitoring enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_integrity_monitoring GoogleWorkstationsWorkstationConfigA#enable_integrity_monitoring}
        :param enable_secure_boot: Whether the instance has Secure Boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_secure_boot GoogleWorkstationsWorkstationConfigA#enable_secure_boot}
        :param enable_vtpm: Whether the instance has the vTPM enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_vtpm GoogleWorkstationsWorkstationConfigA#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18497437b3b24bc5d0e90bed02da4196c039382259514e17b3f87b611200af95)
            check_type(argname="argument enable_integrity_monitoring", value=enable_integrity_monitoring, expected_type=type_hints["enable_integrity_monitoring"])
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
            check_type(argname="argument enable_vtpm", value=enable_vtpm, expected_type=type_hints["enable_vtpm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_integrity_monitoring is not None:
            self._values["enable_integrity_monitoring"] = enable_integrity_monitoring
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot
        if enable_vtpm is not None:
            self._values["enable_vtpm"] = enable_vtpm

    @builtins.property
    def enable_integrity_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance has integrity monitoring enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_integrity_monitoring GoogleWorkstationsWorkstationConfigA#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance has Secure Boot enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_secure_boot GoogleWorkstationsWorkstationConfigA#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance has the vTPM enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_vtpm GoogleWorkstationsWorkstationConfigA#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f43a36f057b82d2462f47e1a1bd2a17a490502c82049e5dea3de7b70ca7eed64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIntegrityMonitoring")
    def reset_enable_integrity_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIntegrityMonitoring", []))

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @jsii.member(jsii_name="resetEnableVtpm")
    def reset_enable_vtpm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableVtpm", []))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoringInput")
    def enable_integrity_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIntegrityMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enableVtpmInput")
    def enable_vtpm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableVtpmInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoring")
    def enable_integrity_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIntegrityMonitoring"))

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c387a68ab13642979512e670fd729c2c7b21f944888a2cd97db8fea187cc40de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIntegrityMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSecureBoot")
    def enable_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecureBoot"))

    @enable_secure_boot.setter
    def enable_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e92935848b27fd3e76f597e8bb597214e5a30adfad96343b3a0e41c26ba0485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableVtpm")
    def enable_vtpm(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableVtpm"))

    @enable_vtpm.setter
    def enable_vtpm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc779c7262054efcab9282701c22c8b4bb9130517ecb3504825bc6972f7e8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9d764fb77e0f753f86941e1ca107f9f5afd3e6ee2d9165853a72caf9960bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigHostOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigHostOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cb146c9db7255ff4a4db0641ef4df51af01beca7e066370c3e0259ff23eee4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGceInstance")
    def put_gce_instance(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        boost_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        confidential_instance_config: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        disable_public_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_ssh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        pool_size: typing.Optional[jsii.Number] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vm_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#accelerators GoogleWorkstationsWorkstationConfigA#accelerators}
        :param boost_configs: boost_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boost_configs GoogleWorkstationsWorkstationConfigA#boost_configs}
        :param boot_disk_size_gb: Size of the boot disk in GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#boot_disk_size_gb GoogleWorkstationsWorkstationConfigA#boot_disk_size_gb}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#confidential_instance_config GoogleWorkstationsWorkstationConfigA#confidential_instance_config}
        :param disable_public_ip_addresses: Whether instances have no public IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_public_ip_addresses GoogleWorkstationsWorkstationConfigA#disable_public_ip_addresses}
        :param disable_ssh: Whether to disable SSH access to the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disable_ssh GoogleWorkstationsWorkstationConfigA#disable_ssh}
        :param enable_nested_virtualization: Whether to enable nested virtualization on the Compute Engine VMs backing the Workstations. See https://cloud.google.com/workstations/docs/reference/rest/v1beta/projects.locations.workstationClusters.workstationConfigs#GceInstance.FIELDS.enable_nested_virtualization Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#enable_nested_virtualization GoogleWorkstationsWorkstationConfigA#enable_nested_virtualization}
        :param machine_type: The name of a Compute Engine machine type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#machine_type GoogleWorkstationsWorkstationConfigA#machine_type}
        :param pool_size: Number of instances to pool for faster workstation startup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#pool_size GoogleWorkstationsWorkstationConfigA#pool_size}
        :param service_account: Email address of the service account that will be used on VM instances used to support this config. This service account must have permission to pull the specified container image. If not set, VMs will run without a service account, in which case the image must be publicly accessible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#service_account GoogleWorkstationsWorkstationConfigA#service_account}
        :param service_account_scopes: Scopes to grant to the service_account. Various scopes are automatically added based on feature usage. When specified, users of workstations under this configuration must have 'iam.serviceAccounts.actAs' on the service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#service_account_scopes GoogleWorkstationsWorkstationConfigA#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#shielded_instance_config GoogleWorkstationsWorkstationConfigA#shielded_instance_config}
        :param tags: Network tags to add to the Compute Engine machines backing the Workstations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#tags GoogleWorkstationsWorkstationConfigA#tags}
        :param vm_tags: Resource manager tags to be bound to the VM instances backing the Workstations. Tag keys and values have the same definition as https://cloud.google.com/resource-manager/docs/tags/tags-overview Keys must be in the format 'tagKeys/{tag_key_id}', and values are in the format 'tagValues/456'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#vm_tags GoogleWorkstationsWorkstationConfigA#vm_tags}
        '''
        value = GoogleWorkstationsWorkstationConfigHostGceInstance(
            accelerators=accelerators,
            boost_configs=boost_configs,
            boot_disk_size_gb=boot_disk_size_gb,
            confidential_instance_config=confidential_instance_config,
            disable_public_ip_addresses=disable_public_ip_addresses,
            disable_ssh=disable_ssh,
            enable_nested_virtualization=enable_nested_virtualization,
            machine_type=machine_type,
            pool_size=pool_size,
            service_account=service_account,
            service_account_scopes=service_account_scopes,
            shielded_instance_config=shielded_instance_config,
            tags=tags,
            vm_tags=vm_tags,
        )

        return typing.cast(None, jsii.invoke(self, "putGceInstance", [value]))

    @jsii.member(jsii_name="resetGceInstance")
    def reset_gce_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceInstance", []))

    @builtins.property
    @jsii.member(jsii_name="gceInstance")
    def gce_instance(
        self,
    ) -> GoogleWorkstationsWorkstationConfigHostGceInstanceOutputReference:
        return typing.cast(GoogleWorkstationsWorkstationConfigHostGceInstanceOutputReference, jsii.get(self, "gceInstance"))

    @builtins.property
    @jsii.member(jsii_name="gceInstanceInput")
    def gce_instance_input(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstance]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstance], jsii.get(self, "gceInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigHost]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigHost], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigHost],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52e08646d26a6e767913de7cbce1b2b3305aecb3eb19ace74d0d22eee8ee82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigPersistentDirectories",
    jsii_struct_bases=[],
    name_mapping={"gce_pd": "gcePd", "mount_path": "mountPath"},
)
class GoogleWorkstationsWorkstationConfigPersistentDirectories:
    def __init__(
        self,
        *,
        gce_pd: typing.Optional[typing.Union["GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd", typing.Dict[builtins.str, typing.Any]]] = None,
        mount_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gce_pd: gce_pd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_pd GoogleWorkstationsWorkstationConfigA#gce_pd}
        :param mount_path: Location of this directory in the running workstation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#mount_path GoogleWorkstationsWorkstationConfigA#mount_path}
        '''
        if isinstance(gce_pd, dict):
            gce_pd = GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd(**gce_pd)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8ac223087ae19b8dd08d813b99cecdf5c4e104add8b70188b49b2db6b46a8b)
            check_type(argname="argument gce_pd", value=gce_pd, expected_type=type_hints["gce_pd"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gce_pd is not None:
            self._values["gce_pd"] = gce_pd
        if mount_path is not None:
            self._values["mount_path"] = mount_path

    @builtins.property
    def gce_pd(
        self,
    ) -> typing.Optional["GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd"]:
        '''gce_pd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#gce_pd GoogleWorkstationsWorkstationConfigA#gce_pd}
        '''
        result = self._values.get("gce_pd")
        return typing.cast(typing.Optional["GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd"], result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''Location of this directory in the running workstation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#mount_path GoogleWorkstationsWorkstationConfigA#mount_path}
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigPersistentDirectories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd",
    jsii_struct_bases=[],
    name_mapping={
        "disk_type": "diskType",
        "fs_type": "fsType",
        "reclaim_policy": "reclaimPolicy",
        "size_gb": "sizeGb",
        "source_snapshot": "sourceSnapshot",
    },
)
class GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd:
    def __init__(
        self,
        *,
        disk_type: typing.Optional[builtins.str] = None,
        fs_type: typing.Optional[builtins.str] = None,
        reclaim_policy: typing.Optional[builtins.str] = None,
        size_gb: typing.Optional[jsii.Number] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: The type of the persistent disk for the home directory. Defaults to 'pd-standard'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disk_type GoogleWorkstationsWorkstationConfigA#disk_type}
        :param fs_type: Type of file system that the disk should be formatted with. The workstation image must support this file system type. Must be empty if 'sourceSnapshot' is set. Defaults to 'ext4'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#fs_type GoogleWorkstationsWorkstationConfigA#fs_type}
        :param reclaim_policy: Whether the persistent disk should be deleted when the workstation is deleted. Valid values are 'DELETE' and 'RETAIN'. Defaults to 'DELETE'. Possible values: ["DELETE", "RETAIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#reclaim_policy GoogleWorkstationsWorkstationConfigA#reclaim_policy}
        :param size_gb: The GB capacity of a persistent home directory for each workstation created with this configuration. Must be empty if 'sourceSnapshot' is set. Valid values are '10', '50', '100', '200', '500', or '1000'. Defaults to '200'. If less than '200' GB, the 'diskType' must be 'pd-balanced' or 'pd-ssd'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#size_gb GoogleWorkstationsWorkstationConfigA#size_gb}
        :param source_snapshot: Name of the snapshot to use as the source for the disk. This can be the snapshot's 'self_link', 'id', or a string in the format of 'projects/{project}/global/snapshots/{snapshot}'. If set, 'sizeGb' and 'fsType' must be empty. Can only be updated if it has an existing value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_snapshot GoogleWorkstationsWorkstationConfigA#source_snapshot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db6ac96596e62353b438a9b8bdbe100fc92d67a682ad644f09ce3875b8804b4)
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument fs_type", value=fs_type, expected_type=type_hints["fs_type"])
            check_type(argname="argument reclaim_policy", value=reclaim_policy, expected_type=type_hints["reclaim_policy"])
            check_type(argname="argument size_gb", value=size_gb, expected_type=type_hints["size_gb"])
            check_type(argname="argument source_snapshot", value=source_snapshot, expected_type=type_hints["source_snapshot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if fs_type is not None:
            self._values["fs_type"] = fs_type
        if reclaim_policy is not None:
            self._values["reclaim_policy"] = reclaim_policy
        if size_gb is not None:
            self._values["size_gb"] = size_gb
        if source_snapshot is not None:
            self._values["source_snapshot"] = source_snapshot

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of the persistent disk for the home directory. Defaults to 'pd-standard'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disk_type GoogleWorkstationsWorkstationConfigA#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fs_type(self) -> typing.Optional[builtins.str]:
        '''Type of file system that the disk should be formatted with.

        The workstation image must support this file system type. Must be empty if 'sourceSnapshot' is set. Defaults to 'ext4'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#fs_type GoogleWorkstationsWorkstationConfigA#fs_type}
        '''
        result = self._values.get("fs_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reclaim_policy(self) -> typing.Optional[builtins.str]:
        '''Whether the persistent disk should be deleted when the workstation is deleted.

        Valid values are 'DELETE' and 'RETAIN'. Defaults to 'DELETE'. Possible values: ["DELETE", "RETAIN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#reclaim_policy GoogleWorkstationsWorkstationConfigA#reclaim_policy}
        '''
        result = self._values.get("reclaim_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gb(self) -> typing.Optional[jsii.Number]:
        '''The GB capacity of a persistent home directory for each workstation created with this configuration.

        Must be empty if 'sourceSnapshot' is set.
        Valid values are '10', '50', '100', '200', '500', or '1000'. Defaults to '200'. If less than '200' GB, the 'diskType' must be 'pd-balanced' or 'pd-ssd'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#size_gb GoogleWorkstationsWorkstationConfigA#size_gb}
        '''
        result = self._values.get("size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''Name of the snapshot to use as the source for the disk.

        This can be the snapshot's 'self_link', 'id', or a string in the format of 'projects/{project}/global/snapshots/{snapshot}'. If set, 'sizeGb' and 'fsType' must be empty. Can only be updated if it has an existing value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_snapshot GoogleWorkstationsWorkstationConfigA#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d461f35096b3f78261e84090099d8e4148ad8284c211a39d526d526b3aa8e360)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetFsType")
    def reset_fs_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFsType", []))

    @jsii.member(jsii_name="resetReclaimPolicy")
    def reset_reclaim_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReclaimPolicy", []))

    @jsii.member(jsii_name="resetSizeGb")
    def reset_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGb", []))

    @jsii.member(jsii_name="resetSourceSnapshot")
    def reset_source_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshot", []))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="fsTypeInput")
    def fs_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fsTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="reclaimPolicyInput")
    def reclaim_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reclaimPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGbInput")
    def size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotInput")
    def source_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b011365e38da1847f2452d36e7e0b8ee102448fe47636403d9d6a8c7d31d9810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fsType")
    def fs_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fsType"))

    @fs_type.setter
    def fs_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09178b64a65e650ac1d11e1f6f6ecc7de64cc33403e529fc5866b971fa873097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reclaimPolicy")
    def reclaim_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reclaimPolicy"))

    @reclaim_policy.setter
    def reclaim_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350db772633f8f09ef83575082cac041513d1793a079710fe02b292244054b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reclaimPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @size_gb.setter
    def size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18bc28a2999133e4bd7118b7b00e54ef06d2196c97fe7b2ad88da932c4f4055d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83728c0ec15ac763f512a8c4dd8470c831830b636e9e23496ab04a5ee9da5478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a77c3d8d82abc6bd256a13b312859f3ba9b73c52ffda352c1b6f7069e20dd9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigPersistentDirectoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigPersistentDirectoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__315466b8828112e71fedf5826ef516385ee5b83de0356f251b7bf1d449a7eaec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigPersistentDirectoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a126a69c3d431e786f640efda4990258cd00a6fd4a73f369f8dfbf641157e557)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigPersistentDirectoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ab7f27ca793f97360f14089606b3182f82e73945b422a4cd72b9e694ff22fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a04553c424da2899266290c19867e2b8799b75bd4d889c3556cd90dd3b7d7887)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b52323ba0770e28852b960a1a329cde45ab24cf1904581964fde3945ed123e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigPersistentDirectories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigPersistentDirectories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigPersistentDirectories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a264704ddcf16bc20c59ef4cbe57e2830c0f9d9d50637625d91c9a413d9209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigPersistentDirectoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigPersistentDirectoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a341f3ae41728ffab0ed46348f122801ab8a40acbb539ddea38e9552c19e5999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGcePd")
    def put_gce_pd(
        self,
        *,
        disk_type: typing.Optional[builtins.str] = None,
        fs_type: typing.Optional[builtins.str] = None,
        reclaim_policy: typing.Optional[builtins.str] = None,
        size_gb: typing.Optional[jsii.Number] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_type: The type of the persistent disk for the home directory. Defaults to 'pd-standard'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#disk_type GoogleWorkstationsWorkstationConfigA#disk_type}
        :param fs_type: Type of file system that the disk should be formatted with. The workstation image must support this file system type. Must be empty if 'sourceSnapshot' is set. Defaults to 'ext4'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#fs_type GoogleWorkstationsWorkstationConfigA#fs_type}
        :param reclaim_policy: Whether the persistent disk should be deleted when the workstation is deleted. Valid values are 'DELETE' and 'RETAIN'. Defaults to 'DELETE'. Possible values: ["DELETE", "RETAIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#reclaim_policy GoogleWorkstationsWorkstationConfigA#reclaim_policy}
        :param size_gb: The GB capacity of a persistent home directory for each workstation created with this configuration. Must be empty if 'sourceSnapshot' is set. Valid values are '10', '50', '100', '200', '500', or '1000'. Defaults to '200'. If less than '200' GB, the 'diskType' must be 'pd-balanced' or 'pd-ssd'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#size_gb GoogleWorkstationsWorkstationConfigA#size_gb}
        :param source_snapshot: Name of the snapshot to use as the source for the disk. This can be the snapshot's 'self_link', 'id', or a string in the format of 'projects/{project}/global/snapshots/{snapshot}'. If set, 'sizeGb' and 'fsType' must be empty. Can only be updated if it has an existing value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#source_snapshot GoogleWorkstationsWorkstationConfigA#source_snapshot}
        '''
        value = GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd(
            disk_type=disk_type,
            fs_type=fs_type,
            reclaim_policy=reclaim_policy,
            size_gb=size_gb,
            source_snapshot=source_snapshot,
        )

        return typing.cast(None, jsii.invoke(self, "putGcePd", [value]))

    @jsii.member(jsii_name="resetGcePd")
    def reset_gce_pd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcePd", []))

    @jsii.member(jsii_name="resetMountPath")
    def reset_mount_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountPath", []))

    @builtins.property
    @jsii.member(jsii_name="gcePd")
    def gce_pd(
        self,
    ) -> GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePdOutputReference:
        return typing.cast(GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePdOutputReference, jsii.get(self, "gcePd"))

    @builtins.property
    @jsii.member(jsii_name="gcePdInput")
    def gce_pd_input(
        self,
    ) -> typing.Optional[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd]:
        return typing.cast(typing.Optional[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd], jsii.get(self, "gcePdInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a167c9a201f5e3a75ea0014304553fc86f52f9f5b34598456463a9a5ba0e98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigPersistentDirectories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigPersistentDirectories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigPersistentDirectories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6665eee77f1545754ee1c83f92d743ff40a633ac4345e841363ded45ee25bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigReadinessChecks",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "port": "port"},
)
class GoogleWorkstationsWorkstationConfigReadinessChecks:
    def __init__(self, *, path: builtins.str, port: jsii.Number) -> None:
        '''
        :param path: Path to which the request should be sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#path GoogleWorkstationsWorkstationConfigA#path}
        :param port: Port to which the request should be sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#port GoogleWorkstationsWorkstationConfigA#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f3b90284d7a889d6c651c2d4d3712e302d2122d41d59054123ccd0557762af)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "port": port,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Path to which the request should be sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#path GoogleWorkstationsWorkstationConfigA#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port to which the request should be sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#port GoogleWorkstationsWorkstationConfigA#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigReadinessChecks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigReadinessChecksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigReadinessChecksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__931b7126a5f89921a90e935e13d73635992f92fedc5394ed9d6e99a666fff0db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleWorkstationsWorkstationConfigReadinessChecksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5cc40964504ebd1642fabc6face00798a174d0d341dc4b177bfe74e29ce500)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleWorkstationsWorkstationConfigReadinessChecksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c70b00b721ceaf8de7e28e024d628ebe2b9c5f34460d96b14d58b6644617a9b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a84344398e5d897d22dc4f175f5e042d62b3103ea15dfe198d73fa617d075880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1196f14632b03559d38612e163c8f4b88d2d2f1292ebc49fe0f7061fc762c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigReadinessChecks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigReadinessChecks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigReadinessChecks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258eaee9099277f237dbc783915a95946bab41d08e645a9b8c296ffa6df20f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleWorkstationsWorkstationConfigReadinessChecksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigReadinessChecksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f91073c6a6b15af709e680925209e82617b23e8e5653e81399fa1ba55f4f0a65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021a6e4faa03af4eb5fd92900d3fdcc83882c1282365b39a5b1efc984eea32de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7300357e5ebc6e39a63d4268a905af193ec557e9d7986cb5af186b28c64582e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigReadinessChecks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigReadinessChecks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigReadinessChecks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ba531c9cf0ab8bcb96280cd176e160f88c253b3f51721c03a9fd5ecfc0c6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleWorkstationsWorkstationConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#create GoogleWorkstationsWorkstationConfigA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#delete GoogleWorkstationsWorkstationConfigA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#update GoogleWorkstationsWorkstationConfigA#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df37ef625bcf2ef9446f13bf8268d520ae3a1d9b3f59c54377747724675dc606)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#create GoogleWorkstationsWorkstationConfigA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#delete GoogleWorkstationsWorkstationConfigA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_workstations_workstation_config#update GoogleWorkstationsWorkstationConfigA#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleWorkstationsWorkstationConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleWorkstationsWorkstationConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleWorkstationsWorkstationConfig.GoogleWorkstationsWorkstationConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd7b90bd74ca6e57086450336ae0a0d41a0000117081ebe41dcca99de32477f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ad84011633c5bead3c35bab30b6d4fd4163ec5fa0d71941e948683a52a6c61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1677c7e6d6340cf95546321f43adaf99d66d00edd9a225438d9968b3ad4baea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1eaaeb2d616f50df3152f380ed4c2714816b80b1681f9cba6ff7ad81d06053b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1b1b2caaa76c6ea5b0de2113b1b48f662e722229ea25a76f3db8f1205e7890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleWorkstationsWorkstationConfigA",
    "GoogleWorkstationsWorkstationConfigAConfig",
    "GoogleWorkstationsWorkstationConfigAllowedPorts",
    "GoogleWorkstationsWorkstationConfigAllowedPortsList",
    "GoogleWorkstationsWorkstationConfigAllowedPortsOutputReference",
    "GoogleWorkstationsWorkstationConfigConditions",
    "GoogleWorkstationsWorkstationConfigConditionsList",
    "GoogleWorkstationsWorkstationConfigConditionsOutputReference",
    "GoogleWorkstationsWorkstationConfigContainer",
    "GoogleWorkstationsWorkstationConfigContainerOutputReference",
    "GoogleWorkstationsWorkstationConfigEncryptionKey",
    "GoogleWorkstationsWorkstationConfigEncryptionKeyOutputReference",
    "GoogleWorkstationsWorkstationConfigEphemeralDirectories",
    "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd",
    "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePdOutputReference",
    "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesList",
    "GoogleWorkstationsWorkstationConfigEphemeralDirectoriesOutputReference",
    "GoogleWorkstationsWorkstationConfigHost",
    "GoogleWorkstationsWorkstationConfigHostGceInstance",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsList",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceAcceleratorsOutputReference",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsList",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAcceleratorsOutputReference",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsList",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsOutputReference",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfigOutputReference",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceOutputReference",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig",
    "GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfigOutputReference",
    "GoogleWorkstationsWorkstationConfigHostOutputReference",
    "GoogleWorkstationsWorkstationConfigPersistentDirectories",
    "GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd",
    "GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePdOutputReference",
    "GoogleWorkstationsWorkstationConfigPersistentDirectoriesList",
    "GoogleWorkstationsWorkstationConfigPersistentDirectoriesOutputReference",
    "GoogleWorkstationsWorkstationConfigReadinessChecks",
    "GoogleWorkstationsWorkstationConfigReadinessChecksList",
    "GoogleWorkstationsWorkstationConfigReadinessChecksOutputReference",
    "GoogleWorkstationsWorkstationConfigTimeouts",
    "GoogleWorkstationsWorkstationConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__86be159f02a43f8771a41b1e58b45735974b729cf01b74440afe38ed4033705a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    workstation_cluster_id: builtins.str,
    workstation_config_id: builtins.str,
    allowed_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigAllowedPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_tcp_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_audit_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigEphemeralDirectories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHost, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_usable_workstations: typing.Optional[jsii.Number] = None,
    persistent_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigPersistentDirectories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    readiness_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigReadinessChecks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    running_timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d7c7b4feb6ee42c31ee60deb96576c491987376d397d90cb6e9e2f383f460254(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42ec412ce8b32c630e2aa4245bcf724c0c6876de62674f1b98883e445603569(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigAllowedPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c51f868822937a19c20a8f7b67fbadfef4a88b82f90d4e1af4a14a9fea3e8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigEphemeralDirectories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca744c7a5ec15408510598afc6c36eb45b04f90b3fbb98f609d91e42b08028b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigPersistentDirectories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961be13a75460ae1f6920fdbfdf07c9e0364a67b4fe8d92bcffaed75a94f8962(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigReadinessChecks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90ae33cf3fc3ac26d12a3bcf5917af07f0c90e8892a4901eabf65a92a632582(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e8d4dc987149ea7f57039ebda1759ae4f4c6bad5b1d5ebe62f565ea53540a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6218f2d0a0fa9f5d55eb0104d94e8188f4fb2b63b90393ff55ad766a41b78c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fe3142152fb975bdf691f150e361ed26da1fb9bad5b46b31330612128bd325(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec359a06c1e429b5d5b0a23e70d5d07362ec0c804e52bf09fd8fc7eff6d7b9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573fd21238ff53838ae0172702d3e390ab482a7a16710b30e202717c27ad60e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f49e638354e5485dfb260005dd2c2de4ded52328e49fca534519715769adae(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8845bd89ee920a162688cb628f023c2545cabb2b0387de222418ea4230ca0153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88c71645addc0b71ee092306b5d7b6b672e5ab5c5d917f6a07c6bdbe7e97afa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fda6991202e62aeeebb0fe980bc15e11ff93e956000afa203416769269f1b22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb15fcf6bda438fc8eb014364daf358604b23f1d8275d434f4bd79f655df299(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793759f9e7fd654cd5b0299c933039f701b2ab7f6a84f5724d452ce72cc77bfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b6de4b5c300787dc7be27d4cfcc856402fa71ff6b23db985455bf3c8fbf7c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8497c2dfef96f9a391dce0b4c36cb55f897fe1c9d1c26116b86e57d5815b932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499972dbd65c78d8c138dd5310a4ae9f0353acbbc92733a77fdfb56309446771(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    workstation_cluster_id: builtins.str,
    workstation_config_id: builtins.str,
    allowed_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigAllowedPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    container: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_tcp_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_audit_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigEphemeralDirectories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    host: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHost, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_usable_workstations: typing.Optional[jsii.Number] = None,
    persistent_directories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigPersistentDirectories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    readiness_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigReadinessChecks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    replica_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    running_timeout: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f58b81d3b4ed82f3f931e38b854c76095db33dde0fa612386f49624bf2d7f4(
    *,
    first: typing.Optional[jsii.Number] = None,
    last: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f326eecafb3dbd8e0afa34b3a2492e716556a0289bd71d57c6da0e5f98aee1a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d1f7e92ce0b61ab8f98f76fe87fadbfd9f43bc9b9f94de2b0760d23de1bfe4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cac8478e3988f3cf02a12fbc263baa28bb81ca71d2774e5ed676dabc1799fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159d78ce74f927698752bdae0035cf54ded551658de0b46d3c0155dcb23a21de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0c61ab9d0cb1d3d9d2a4f6af0886a4ef29dd40faa426bb668524f69965b191(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab8ab6f8058d59eef6e7b9dd142e15977600a93ef4146db3e2692d0c1d6b98b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigAllowedPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc77bef800a9ad79e36511b0b4dbc645f5c2d013bcbb735e3fe0d6353649b3ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b187ea5abeee5bad2bc4ee91e8470172a83f08e27bdc497bf80af4b0e520f59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9032b8337d0eb3aec05fce76b820fce2781f2d37fd3a9fb567551e558aa5e2ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb015108af9525a332d368df1e2802bf2143eb1d6dccf96c2cc0246edbe5cc3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigAllowedPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926f6b1027ebe7212eaf588c07b841e3e9c7617a0078272f8e31b877918e891c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc32063dc52d49ea3ba89d16e4d05882015aa41f8ac7c94d42e2de41ba7571f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728c853705f52422940e97bbedde4becc6a35f3e9e7b262bdb531537d413b9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46767c923c753d1d38b714ede4591a724cfd731b8aedac64f89cdcc99ea13e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a64d392b96421e6c3a6579d727a9fbbf9a5b06deacde9626c0c642779af6e1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bfd088d67a9c3bcf1534acd939332ebb48bc8b9940c097aac6c636dc0f37b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f34a6c56609560b95ae867fbcc6c1b5fc06d2c7280201c447758b43c58a216(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee3c2b8b5274b5347acb61996a061437891d4182fcece602107a439113dd209(
    *,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    run_as_user: typing.Optional[jsii.Number] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa7be205d9b22c30643b6a509851ceaadd1b3bf081be398b88b00f7276df65a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7a114fce1a035739268e45f8785c76f44920f289bc6c839527973b782b980f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436a7f6ca41947260de5006a049e87d9ce5a4a4e0471a834ed49e5b506e1e3fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a5a1c1635b54adb3c0fd68ffc2c52ce32076f1ec02ded213c69e7791cc5860(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0584a721510e9ea85d6233389140714e69604aea913a1f8ac61977668e27e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409adb56cc758b9cdc6e686d1448e044d35eebddb393144c680695571acac1db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f268b6080efda9a6ba062c4bba6bc07792524ea3f4e68a009b82647a4cd14b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a687a265049caefe5b90b2cc207c5b4ba6f806e6224c07118be9e9702857d8f4(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2374a9d7609f16534dc028e3d48c8185bfded8860ace4c9babde631a15bfc31(
    *,
    kms_key: builtins.str,
    kms_key_service_account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ff735894586a2f1f7c915ff41c8e36df03309f17991b2f7b14dc3807f588d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10466771bd7e9cb3f4ef36b066198e0903ce852957ff534637bcc32ab53844b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f66aa319faee9ebe86a7092822a6f8c9667fa66b60f51550c756d7239fc548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cd8b9602876268a2975f55b16cd62c1d7a8bee4ae1e09f6122f9bf797e9bd0(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382cab08bc0ae440c700a39a8f6cdec5113728641faf1b8799c002a3119ed990(
    *,
    gce_pd: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd, typing.Dict[builtins.str, typing.Any]]] = None,
    mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2437d13d3345be5585464b4703ded4ba0269930fadc14ddc4cf8cacd02f313(
    *,
    disk_type: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_image: typing.Optional[builtins.str] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4656fb02b7baed0efe16e37965edf70e5c236abc434d51e891563c593470aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013935e4b495ade832fa9ed67311391b621cabaf3ee4cce6c0056d1a9814e551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e811179feea4a539539f60244ee7fd82e6213ce12e600a6284e2473aba0e5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cf0f08d562ede071e2c9f6ea64fb920709c27d62306cb1561de8d0f270225f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1475cb30206c7f46a415b26bb9a360bfe68ad91cf8db98be33900250a82990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe1003e293f6ab84058f2272efaf4ecbcb82c96d00451cdfc706d0430a5001f(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigEphemeralDirectoriesGcePd],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360ad4506c83b60c43aaedb6dbc0ae63b900e246cff6eeb26b7ee9e24c02df98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ca72b3236d91c99faf4680436cfa77dc5a00582e902e51b850e3e6da2adb3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be10e5a5a2593864283a1a50fad496edeacdac47620fbb72176a5482f6aeb0ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b8e9588c5053ca2668fe19490f258a9a1202dea21516c35ff398cd2c221842(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f820ca073abccbe548ce1b0f21e3ea13da363c786cf757a56dab28bae138df65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e4da5413ef5f3345c195b0495b33560a133f218a0071728e8d5480f096eccb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigEphemeralDirectories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0628afbcc323da1ff6d6ed0fd872b432203e0287571c742b1db5ee2d2563951d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c5a6a27393bf954c81514833e9876ae7bd8d99a4c710b3dedc1cf228fe462f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6a100c0fea855b20eca12f0d7ae9bf98974d19bcda44468b78762317beeb1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigEphemeralDirectories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9759a9085cb20c5b3e7008d4df98bb21c50f25e15b6ca5cf235d3c3e25b55d6(
    *,
    gce_instance: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstance, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39e1f925701dddc052ba6789c97303f918868f6c90b10ab132797a2ebba2fcc(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boost_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    confidential_instance_config: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_public_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_ssh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    pool_size: typing.Optional[jsii.Number] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    shielded_instance_config: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vm_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefc2e6a2375cea379bd914e81cf88ca53fd87c3e6cae3a4fbf60eb3261ab4ee(
    *,
    count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d58a07754cacc47e46c0213559188fdc815e3d53aa74eb04a606e0ef2e0024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8090ce369ba802e5b65ed01e25d72c9cd29b88c0228fa799da6bdc1adf99405d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbe8558db163dd96acf7d6eb08684f9fe5c796ad08b1878d190af1e598fc06d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293ad06462c9de9ff76aa1c6d26c9fecd1fa0771c88569dcdc918e9c8bc6f6ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e349d84dcc4ea0283de7d8316c3e8390132f5bf0e29eceb2f85b7c8bf59291fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c49c8e85aa1d3eca356141e1f5f9a14ab5fb1f0cf53b4cc920e710b12240bf6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65631060222940dd4ec7b476f198ef0968a4a404db170eaf1767f079f07665ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478b634ffce09b9b63627396f9e330df63d6326d8113c6e980f6e109c286e8dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e92ab58999ec8597905e8a91afe1ee9508b531011e2739839dde8f864d180a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584e1acd0fd51cca2d7b2bcdaa3dc2091e61270cc6f6ee5aeff00b80eb8d393a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6c47588a147d60ba181efc64c706e1888b0dfc7a2a4dc07979ce93ee1109ed(
    *,
    id: builtins.str,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    pool_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499f12009b47e1a910b225680bc23004127332aa4ca345cd003ae8ef525cf3cf(
    *,
    count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5d403ad8f5540a96cc012a71f9ff3deeb4ea02830a3c9dc1736bfe8f062f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba20d05530270f0284061a520e6d0928233fc80acd4e7812a0b66b498ce4a238(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96945aab14e771ffd9db6074b74a1c0d838c873d1b79654d8eba53eb6e46f350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e84931f6f99b9081546e07835447175e44c9af2a9f1426b9abbc545905afbb7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a05e537febb025143c9e3cbf64c1f5a60b3d1ab38ab54e2881513a26abfda18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265a6a888743ec13cacf92a1f3c08a2b338a9c1ffcaacaf1f688894c0bcf00ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6257399fba018374e682c7964230a507f082f883deb1bcb285483d16d8ad8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefb7af4f377d76603dcc73e7067718d91108d0c2578d5985dd8c130d509df2c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba3da83d3f18cf97020c954c05fbc7afa444536908e258c87e0094e73339d89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0e8b8cea2ba58f57be4eab921d5ac467c89ccedf0b1ffeb265bfa424f54029(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bccbcdfb4b14998d6dab0990059f29f166442561f48b73f7d0f0640a2cab87c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f5f42b202c2a46fa5cb03e84c89e31a7c30e49de8272d89423e5fed9a4cab9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185dc12ae84b64355c3fa35f6a7b167e9cc793f5ee6e5ea62ef605d446a3ef1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb4a6bb8cec94c44dee153b8106f8b1c628e7c87a03dde832ffa20422f101c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f7027ef8d670ea3bc86b2f4bd7235a3dba52f6a7ab9fb85f5474925c3f3017(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5473f5fbfda1dcb8a0bc7f173fbdafcec6d1fb2c5b09072cd6eb5ef454293fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bcffc28c597a390a825c7a976bfbde34e657d4bc812a0f4099de4877937f99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91083237c543372abb5b33a863f843b31887777d42d7b238e3c2274481b9ec12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigsAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10d05f2103c9fc5cf326d727f75365761493244922fd832ecb194baadea3cfe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001c1afa2512923d1326bd6f60749c6defdb21a61494371400bed02d64a8ad6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a5769ade1f42df8b50c2892272b9b558a488c47b69694addbed17961552afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d48f2354ffbf8994cd9a423292f79ba1af621a698b3fcf62c646460ad284b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e65b48be753c86f337da0a77f31226428086909dfcf7f202dfe4a87723f7e72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed16c4c9b223dc874ba29f92b6d17c3d1fe4e1cc79c558b9e351e0b93532880b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbf2f9889f95415a9ac02883d43030cd45dd6175ef5cc4baa90becc60fedb9f(
    *,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0319faa3002c3aec6ccb592f91d1756737fababdf9f7baae2ea712680ba541(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f26c4045e0d592ceda819d746823fa476168c9688493a5790af5b4b0bbbeb2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3e76bc60612b029f9f0e4d918ae14c3370b67f5bec65e212dd8f60a2db9e14(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714b06735ce8f6ee237eb380d055511f78f18d4423d73f71608124b8d54c54a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5cdf963d6f107587519c93097d28036b4aa1c865622ff84b8408c36da9a97c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4128a6d2035fb1b9557c31283b6134b7f136b6341b29274d30036f66d940c6ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleWorkstationsWorkstationConfigHostGceInstanceBoostConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97af91076cba83f612a010f9962917ae8099ff6bb087308f2bd4d08027cfdb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fde7136ef5a899104774389d4dad77f9ac4bf110283b00f7aba860dfec5a41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633230e7dc5fc2be81cf6ab2b5fb1f87f1b63891dc21fd13947b027256399b29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7e3e729379ff16041ac9f8cc83067b568b9e9222e494a22af0547af0eb83c3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23b9a77c60fdffd0eef8648ba54683ae83870ff81e9a2dd317d2e775649b0ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91862460504d6ad1d7868bd4fb19f814b4dffa77d04a8997da1033981316548f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c146d1412f59607e222b04f9e0d6f43cb142d422b2c404613b81f0586bb9c5b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e164e0e0be52dc73accd2849cf3ae761968d4a28943e55e735386aecc76f3af1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0951ed20079cdd72c8ed1ae3d4f89afb931e36edd30445cf80347a72c38e57d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e13043a5128dc4acd3afe8ab4d9a216318842696765a3431b88509453726006(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab83c4a070b1bc059348067da93b9503041561b19d028941eba106f05f37da56(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18497437b3b24bc5d0e90bed02da4196c039382259514e17b3f87b611200af95(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43a36f057b82d2462f47e1a1bd2a17a490502c82049e5dea3de7b70ca7eed64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c387a68ab13642979512e670fd729c2c7b21f944888a2cd97db8fea187cc40de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e92935848b27fd3e76f597e8bb597214e5a30adfad96343b3a0e41c26ba0485(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc779c7262054efcab9282701c22c8b4bb9130517ecb3504825bc6972f7e8fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9d764fb77e0f753f86941e1ca107f9f5afd3e6ee2d9165853a72caf9960bff(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigHostGceInstanceShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb146c9db7255ff4a4db0641ef4df51af01beca7e066370c3e0259ff23eee4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52e08646d26a6e767913de7cbce1b2b3305aecb3eb19ace74d0d22eee8ee82c(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigHost],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8ac223087ae19b8dd08d813b99cecdf5c4e104add8b70188b49b2db6b46a8b(
    *,
    gce_pd: typing.Optional[typing.Union[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd, typing.Dict[builtins.str, typing.Any]]] = None,
    mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db6ac96596e62353b438a9b8bdbe100fc92d67a682ad644f09ce3875b8804b4(
    *,
    disk_type: typing.Optional[builtins.str] = None,
    fs_type: typing.Optional[builtins.str] = None,
    reclaim_policy: typing.Optional[builtins.str] = None,
    size_gb: typing.Optional[jsii.Number] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d461f35096b3f78261e84090099d8e4148ad8284c211a39d526d526b3aa8e360(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b011365e38da1847f2452d36e7e0b8ee102448fe47636403d9d6a8c7d31d9810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09178b64a65e650ac1d11e1f6f6ecc7de64cc33403e529fc5866b971fa873097(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350db772633f8f09ef83575082cac041513d1793a079710fe02b292244054b66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bc28a2999133e4bd7118b7b00e54ef06d2196c97fe7b2ad88da932c4f4055d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83728c0ec15ac763f512a8c4dd8470c831830b636e9e23496ab04a5ee9da5478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a77c3d8d82abc6bd256a13b312859f3ba9b73c52ffda352c1b6f7069e20dd9e(
    value: typing.Optional[GoogleWorkstationsWorkstationConfigPersistentDirectoriesGcePd],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315466b8828112e71fedf5826ef516385ee5b83de0356f251b7bf1d449a7eaec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a126a69c3d431e786f640efda4990258cd00a6fd4a73f369f8dfbf641157e557(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ab7f27ca793f97360f14089606b3182f82e73945b422a4cd72b9e694ff22fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04553c424da2899266290c19867e2b8799b75bd4d889c3556cd90dd3b7d7887(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b52323ba0770e28852b960a1a329cde45ab24cf1904581964fde3945ed123e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a264704ddcf16bc20c59ef4cbe57e2830c0f9d9d50637625d91c9a413d9209(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigPersistentDirectories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a341f3ae41728ffab0ed46348f122801ab8a40acbb539ddea38e9552c19e5999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a167c9a201f5e3a75ea0014304553fc86f52f9f5b34598456463a9a5ba0e98f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6665eee77f1545754ee1c83f92d743ff40a633ac4345e841363ded45ee25bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigPersistentDirectories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f3b90284d7a889d6c651c2d4d3712e302d2122d41d59054123ccd0557762af(
    *,
    path: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931b7126a5f89921a90e935e13d73635992f92fedc5394ed9d6e99a666fff0db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5cc40964504ebd1642fabc6face00798a174d0d341dc4b177bfe74e29ce500(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70b00b721ceaf8de7e28e024d628ebe2b9c5f34460d96b14d58b6644617a9b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84344398e5d897d22dc4f175f5e042d62b3103ea15dfe198d73fa617d075880(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1196f14632b03559d38612e163c8f4b88d2d2f1292ebc49fe0f7061fc762c45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258eaee9099277f237dbc783915a95946bab41d08e645a9b8c296ffa6df20f4d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleWorkstationsWorkstationConfigReadinessChecks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91073c6a6b15af709e680925209e82617b23e8e5653e81399fa1ba55f4f0a65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021a6e4faa03af4eb5fd92900d3fdcc83882c1282365b39a5b1efc984eea32de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7300357e5ebc6e39a63d4268a905af193ec557e9d7986cb5af186b28c64582e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ba531c9cf0ab8bcb96280cd176e160f88c253b3f51721c03a9fd5ecfc0c6aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigReadinessChecks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df37ef625bcf2ef9446f13bf8268d520ae3a1d9b3f59c54377747724675dc606(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7b90bd74ca6e57086450336ae0a0d41a0000117081ebe41dcca99de32477f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad84011633c5bead3c35bab30b6d4fd4163ec5fa0d71941e948683a52a6c61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1677c7e6d6340cf95546321f43adaf99d66d00edd9a225438d9968b3ad4baea7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1eaaeb2d616f50df3152f380ed4c2714816b80b1681f9cba6ff7ad81d06053b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1b1b2caaa76c6ea5b0de2113b1b48f662e722229ea25a76f3db8f1205e7890(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleWorkstationsWorkstationConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
