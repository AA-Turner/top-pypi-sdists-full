r'''
# `google_composer_environment`

Refer to the Terraform Registry for docs: [`google_composer_environment`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment).
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


class GoogleComposerEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment google_composer_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        storage_config: typing.Optional[typing.Union["GoogleComposerEnvironmentStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComposerEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment google_composer_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#name GoogleComposerEnvironment#name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#config GoogleComposerEnvironment#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#id GoogleComposerEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for this environment. The labels map can contain no more than 64 entries. Entries of the labels map are UTF8 strings that comply with the following restrictions: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Label values must be between 0 and 63 characters long and must conform to the regular expression (`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?. No more than 64 labels can be associated with a given environment. Both keys and values must be <= 128 bytes in size:: **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#labels GoogleComposerEnvironment#labels}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#project GoogleComposerEnvironment#project}
        :param region: The location or Compute Engine region for the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#region GoogleComposerEnvironment#region}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_config GoogleComposerEnvironment#storage_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#timeouts GoogleComposerEnvironment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f071866de60b7b738d4cca5bee2c1adb6e8fd448a2f2c18853c3d100487f0f6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = GoogleComposerEnvironmentConfig(
            name=name,
            config=config,
            id=id,
            labels=labels,
            project=project,
            region=region,
            storage_config=storage_config,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a GoogleComposerEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComposerEnvironment to import.
        :param import_from_id: The id of the existing GoogleComposerEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComposerEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de71c4f3e7b75844cb085af056360751e6925871803be802d18f6e50726c43a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        database_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigDatabaseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_retention_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_private_builds_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_size: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        master_authorized_networks_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_environment_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigPrivateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigRecoveryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        resilience_mode: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWebServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_network_access_control: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWebServerNetworkAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        workloads_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_config: database_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#database_config GoogleComposerEnvironment#database_config}
        :param data_retention_config: data_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#data_retention_config GoogleComposerEnvironment#data_retention_config}
        :param enable_private_builds_only: Optional. If true, builds performed during operations that install Python packages have only private connectivity to Google services. If false, the builds also have access to the internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_builds_only GoogleComposerEnvironment#enable_private_builds_only}
        :param enable_private_environment: Optional. If true, a private Composer environment will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_environment GoogleComposerEnvironment#enable_private_environment}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#encryption_config GoogleComposerEnvironment#encryption_config}
        :param environment_size: The size of the Cloud Composer environment. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#environment_size GoogleComposerEnvironment#environment_size}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#maintenance_window GoogleComposerEnvironment#maintenance_window}
        :param master_authorized_networks_config: master_authorized_networks_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#master_authorized_networks_config GoogleComposerEnvironment#master_authorized_networks_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#node_config GoogleComposerEnvironment#node_config}
        :param node_count: The number of nodes in the Kubernetes Engine cluster that will be used to run this environment. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#node_count GoogleComposerEnvironment#node_count}
        :param private_environment_config: private_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#private_environment_config GoogleComposerEnvironment#private_environment_config}
        :param recovery_config: recovery_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#recovery_config GoogleComposerEnvironment#recovery_config}
        :param resilience_mode: Whether high resilience is enabled or not. This field is supported for Cloud Composer environments in versions composer-2.1.15-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#resilience_mode GoogleComposerEnvironment#resilience_mode}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#software_config GoogleComposerEnvironment#software_config}
        :param web_server_config: web_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_config GoogleComposerEnvironment#web_server_config}
        :param web_server_network_access_control: web_server_network_access_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_network_access_control GoogleComposerEnvironment#web_server_network_access_control}
        :param workloads_config: workloads_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#workloads_config GoogleComposerEnvironment#workloads_config}
        '''
        value = GoogleComposerEnvironmentConfigA(
            database_config=database_config,
            data_retention_config=data_retention_config,
            enable_private_builds_only=enable_private_builds_only,
            enable_private_environment=enable_private_environment,
            encryption_config=encryption_config,
            environment_size=environment_size,
            maintenance_window=maintenance_window,
            master_authorized_networks_config=master_authorized_networks_config,
            node_config=node_config,
            node_count=node_count,
            private_environment_config=private_environment_config,
            recovery_config=recovery_config,
            resilience_mode=resilience_mode,
            software_config=software_config,
            web_server_config=web_server_config,
            web_server_network_access_control=web_server_network_access_control,
            workloads_config=workloads_config,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putStorageConfig")
    def put_storage_config(self, *, bucket: builtins.str) -> None:
        '''
        :param bucket: Optional. Name of an existing Cloud Storage bucket to be used by the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#bucket GoogleComposerEnvironment#bucket}
        '''
        value = GoogleComposerEnvironmentStorageConfig(bucket=bucket)

        return typing.cast(None, jsii.invoke(self, "putStorageConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#create GoogleComposerEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#delete GoogleComposerEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#update GoogleComposerEnvironment#update}.
        '''
        value = GoogleComposerEnvironmentTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStorageConfig")
    def reset_storage_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConfig", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "GoogleComposerEnvironmentConfigAOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="storageConfig")
    def storage_config(self) -> "GoogleComposerEnvironmentStorageConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentStorageConfigOutputReference", jsii.get(self, "storageConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComposerEnvironmentTimeoutsOutputReference":
        return typing.cast("GoogleComposerEnvironmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["GoogleComposerEnvironmentConfigA"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigInput")
    def storage_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentStorageConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentStorageConfig"], jsii.get(self, "storageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComposerEnvironmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComposerEnvironmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6aae58565e4b1b330f31bb3dd7054b5286a8ae83ddc629bcff629d08238692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc257e32c7de8a96bfafdfc0b4797670eee4d3dfa3b4c0ea0d909c530d0596d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e16b4918495b2a323e3ecab2a9bfdc2e3c77488ad4e223ec8f0b25f1127a0b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c55eb12208b9f605deffff03690083dcf6e340d44038ea1c30af4a85f7cf6ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9103473a995879a9f2bc2e7cb0f861e0a2e0b55da58d74d162122df26c5ab30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfig",
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
        "config": "config",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "region": "region",
        "storage_config": "storageConfig",
        "timeouts": "timeouts",
    },
)
class GoogleComposerEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        storage_config: typing.Optional[typing.Union["GoogleComposerEnvironmentStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComposerEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#name GoogleComposerEnvironment#name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#config GoogleComposerEnvironment#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#id GoogleComposerEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for this environment. The labels map can contain no more than 64 entries. Entries of the labels map are UTF8 strings that comply with the following restrictions: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Label values must be between 0 and 63 characters long and must conform to the regular expression (`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?. No more than 64 labels can be associated with a given environment. Both keys and values must be <= 128 bytes in size:: **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#labels GoogleComposerEnvironment#labels}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#project GoogleComposerEnvironment#project}
        :param region: The location or Compute Engine region for the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#region GoogleComposerEnvironment#region}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_config GoogleComposerEnvironment#storage_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#timeouts GoogleComposerEnvironment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = GoogleComposerEnvironmentConfigA(**config)
        if isinstance(storage_config, dict):
            storage_config = GoogleComposerEnvironmentStorageConfig(**storage_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleComposerEnvironmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164ece5e6ddd4ccde928c31b0a8b38d8e3442a019ecc0797281cee7020e042ef)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument storage_config", value=storage_config, expected_type=type_hints["storage_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if config is not None:
            self._values["config"] = config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if storage_config is not None:
            self._values["storage_config"] = storage_config
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
    def name(self) -> builtins.str:
        '''Name of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#name GoogleComposerEnvironment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["GoogleComposerEnvironmentConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#config GoogleComposerEnvironment#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#id GoogleComposerEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for this environment.

        The labels map can contain no more than 64 entries. Entries of the labels map are UTF8 strings that comply with the following restrictions: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Label values must be between 0 and 63 characters long and must conform to the regular expression (`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?. No more than 64 labels can be associated with a given environment. Both keys and values must be <= 128 bytes in size::

           			**Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
           			Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#labels GoogleComposerEnvironment#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#project GoogleComposerEnvironment#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The location or Compute Engine region for the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#region GoogleComposerEnvironment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentStorageConfig"]:
        '''storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_config GoogleComposerEnvironment#storage_config}
        '''
        result = self._values.get("storage_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentStorageConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComposerEnvironmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#timeouts GoogleComposerEnvironment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "database_config": "databaseConfig",
        "data_retention_config": "dataRetentionConfig",
        "enable_private_builds_only": "enablePrivateBuildsOnly",
        "enable_private_environment": "enablePrivateEnvironment",
        "encryption_config": "encryptionConfig",
        "environment_size": "environmentSize",
        "maintenance_window": "maintenanceWindow",
        "master_authorized_networks_config": "masterAuthorizedNetworksConfig",
        "node_config": "nodeConfig",
        "node_count": "nodeCount",
        "private_environment_config": "privateEnvironmentConfig",
        "recovery_config": "recoveryConfig",
        "resilience_mode": "resilienceMode",
        "software_config": "softwareConfig",
        "web_server_config": "webServerConfig",
        "web_server_network_access_control": "webServerNetworkAccessControl",
        "workloads_config": "workloadsConfig",
    },
)
class GoogleComposerEnvironmentConfigA:
    def __init__(
        self,
        *,
        database_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigDatabaseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_retention_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_private_builds_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_size: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        master_authorized_networks_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_environment_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigPrivateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigRecoveryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        resilience_mode: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWebServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_network_access_control: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWebServerNetworkAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        workloads_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_config: database_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#database_config GoogleComposerEnvironment#database_config}
        :param data_retention_config: data_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#data_retention_config GoogleComposerEnvironment#data_retention_config}
        :param enable_private_builds_only: Optional. If true, builds performed during operations that install Python packages have only private connectivity to Google services. If false, the builds also have access to the internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_builds_only GoogleComposerEnvironment#enable_private_builds_only}
        :param enable_private_environment: Optional. If true, a private Composer environment will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_environment GoogleComposerEnvironment#enable_private_environment}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#encryption_config GoogleComposerEnvironment#encryption_config}
        :param environment_size: The size of the Cloud Composer environment. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#environment_size GoogleComposerEnvironment#environment_size}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#maintenance_window GoogleComposerEnvironment#maintenance_window}
        :param master_authorized_networks_config: master_authorized_networks_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#master_authorized_networks_config GoogleComposerEnvironment#master_authorized_networks_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#node_config GoogleComposerEnvironment#node_config}
        :param node_count: The number of nodes in the Kubernetes Engine cluster that will be used to run this environment. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#node_count GoogleComposerEnvironment#node_count}
        :param private_environment_config: private_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#private_environment_config GoogleComposerEnvironment#private_environment_config}
        :param recovery_config: recovery_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#recovery_config GoogleComposerEnvironment#recovery_config}
        :param resilience_mode: Whether high resilience is enabled or not. This field is supported for Cloud Composer environments in versions composer-2.1.15-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#resilience_mode GoogleComposerEnvironment#resilience_mode}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#software_config GoogleComposerEnvironment#software_config}
        :param web_server_config: web_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_config GoogleComposerEnvironment#web_server_config}
        :param web_server_network_access_control: web_server_network_access_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_network_access_control GoogleComposerEnvironment#web_server_network_access_control}
        :param workloads_config: workloads_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#workloads_config GoogleComposerEnvironment#workloads_config}
        '''
        if isinstance(database_config, dict):
            database_config = GoogleComposerEnvironmentConfigDatabaseConfig(**database_config)
        if isinstance(data_retention_config, dict):
            data_retention_config = GoogleComposerEnvironmentConfigDataRetentionConfig(**data_retention_config)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleComposerEnvironmentConfigEncryptionConfig(**encryption_config)
        if isinstance(maintenance_window, dict):
            maintenance_window = GoogleComposerEnvironmentConfigMaintenanceWindow(**maintenance_window)
        if isinstance(master_authorized_networks_config, dict):
            master_authorized_networks_config = GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig(**master_authorized_networks_config)
        if isinstance(node_config, dict):
            node_config = GoogleComposerEnvironmentConfigNodeConfig(**node_config)
        if isinstance(private_environment_config, dict):
            private_environment_config = GoogleComposerEnvironmentConfigPrivateEnvironmentConfig(**private_environment_config)
        if isinstance(recovery_config, dict):
            recovery_config = GoogleComposerEnvironmentConfigRecoveryConfig(**recovery_config)
        if isinstance(software_config, dict):
            software_config = GoogleComposerEnvironmentConfigSoftwareConfig(**software_config)
        if isinstance(web_server_config, dict):
            web_server_config = GoogleComposerEnvironmentConfigWebServerConfig(**web_server_config)
        if isinstance(web_server_network_access_control, dict):
            web_server_network_access_control = GoogleComposerEnvironmentConfigWebServerNetworkAccessControl(**web_server_network_access_control)
        if isinstance(workloads_config, dict):
            workloads_config = GoogleComposerEnvironmentConfigWorkloadsConfig(**workloads_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97701be78db1faa6abbb2a6bd2bc968eef5a49d9406ff651b402dadae2aac74d)
            check_type(argname="argument database_config", value=database_config, expected_type=type_hints["database_config"])
            check_type(argname="argument data_retention_config", value=data_retention_config, expected_type=type_hints["data_retention_config"])
            check_type(argname="argument enable_private_builds_only", value=enable_private_builds_only, expected_type=type_hints["enable_private_builds_only"])
            check_type(argname="argument enable_private_environment", value=enable_private_environment, expected_type=type_hints["enable_private_environment"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument environment_size", value=environment_size, expected_type=type_hints["environment_size"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument master_authorized_networks_config", value=master_authorized_networks_config, expected_type=type_hints["master_authorized_networks_config"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument private_environment_config", value=private_environment_config, expected_type=type_hints["private_environment_config"])
            check_type(argname="argument recovery_config", value=recovery_config, expected_type=type_hints["recovery_config"])
            check_type(argname="argument resilience_mode", value=resilience_mode, expected_type=type_hints["resilience_mode"])
            check_type(argname="argument software_config", value=software_config, expected_type=type_hints["software_config"])
            check_type(argname="argument web_server_config", value=web_server_config, expected_type=type_hints["web_server_config"])
            check_type(argname="argument web_server_network_access_control", value=web_server_network_access_control, expected_type=type_hints["web_server_network_access_control"])
            check_type(argname="argument workloads_config", value=workloads_config, expected_type=type_hints["workloads_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_config is not None:
            self._values["database_config"] = database_config
        if data_retention_config is not None:
            self._values["data_retention_config"] = data_retention_config
        if enable_private_builds_only is not None:
            self._values["enable_private_builds_only"] = enable_private_builds_only
        if enable_private_environment is not None:
            self._values["enable_private_environment"] = enable_private_environment
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if environment_size is not None:
            self._values["environment_size"] = environment_size
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if master_authorized_networks_config is not None:
            self._values["master_authorized_networks_config"] = master_authorized_networks_config
        if node_config is not None:
            self._values["node_config"] = node_config
        if node_count is not None:
            self._values["node_count"] = node_count
        if private_environment_config is not None:
            self._values["private_environment_config"] = private_environment_config
        if recovery_config is not None:
            self._values["recovery_config"] = recovery_config
        if resilience_mode is not None:
            self._values["resilience_mode"] = resilience_mode
        if software_config is not None:
            self._values["software_config"] = software_config
        if web_server_config is not None:
            self._values["web_server_config"] = web_server_config
        if web_server_network_access_control is not None:
            self._values["web_server_network_access_control"] = web_server_network_access_control
        if workloads_config is not None:
            self._values["workloads_config"] = workloads_config

    @builtins.property
    def database_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigDatabaseConfig"]:
        '''database_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#database_config GoogleComposerEnvironment#database_config}
        '''
        result = self._values.get("database_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigDatabaseConfig"], result)

    @builtins.property
    def data_retention_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigDataRetentionConfig"]:
        '''data_retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#data_retention_config GoogleComposerEnvironment#data_retention_config}
        '''
        result = self._values.get("data_retention_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigDataRetentionConfig"], result)

    @builtins.property
    def enable_private_builds_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, builds performed during operations that install Python packages have only private connectivity to Google services. If false, the builds also have access to the internet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_builds_only GoogleComposerEnvironment#enable_private_builds_only}
        '''
        result = self._values.get("enable_private_builds_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_private_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, a private Composer environment will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_environment GoogleComposerEnvironment#enable_private_environment}
        '''
        result = self._values.get("enable_private_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#encryption_config GoogleComposerEnvironment#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigEncryptionConfig"], result)

    @builtins.property
    def environment_size(self) -> typing.Optional[builtins.str]:
        '''The size of the Cloud Composer environment.

        This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#environment_size GoogleComposerEnvironment#environment_size}
        '''
        result = self._values.get("environment_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#maintenance_window GoogleComposerEnvironment#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigMaintenanceWindow"], result)

    @builtins.property
    def master_authorized_networks_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig"]:
        '''master_authorized_networks_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#master_authorized_networks_config GoogleComposerEnvironment#master_authorized_networks_config}
        '''
        result = self._values.get("master_authorized_networks_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig"], result)

    @builtins.property
    def node_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#node_config GoogleComposerEnvironment#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigNodeConfig"], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes in the Kubernetes Engine cluster that will be used to run this environment.

        This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#node_count GoogleComposerEnvironment#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_environment_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigPrivateEnvironmentConfig"]:
        '''private_environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#private_environment_config GoogleComposerEnvironment#private_environment_config}
        '''
        result = self._values.get("private_environment_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigPrivateEnvironmentConfig"], result)

    @builtins.property
    def recovery_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfig"]:
        '''recovery_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#recovery_config GoogleComposerEnvironment#recovery_config}
        '''
        result = self._values.get("recovery_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfig"], result)

    @builtins.property
    def resilience_mode(self) -> typing.Optional[builtins.str]:
        '''Whether high resilience is enabled or not.

        This field is supported for Cloud Composer environments in versions composer-2.1.15-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#resilience_mode GoogleComposerEnvironment#resilience_mode}
        '''
        result = self._values.get("resilience_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#software_config GoogleComposerEnvironment#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigSoftwareConfig"], result)

    @builtins.property
    def web_server_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWebServerConfig"]:
        '''web_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_config GoogleComposerEnvironment#web_server_config}
        '''
        result = self._values.get("web_server_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWebServerConfig"], result)

    @builtins.property
    def web_server_network_access_control(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWebServerNetworkAccessControl"]:
        '''web_server_network_access_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_network_access_control GoogleComposerEnvironment#web_server_network_access_control}
        '''
        result = self._values.get("web_server_network_access_control")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWebServerNetworkAccessControl"], result)

    @builtins.property
    def workloads_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfig"]:
        '''workloads_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#workloads_config GoogleComposerEnvironment#workloads_config}
        '''
        result = self._values.get("workloads_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c22931bb54fd251e7524756a6e39678404adce5d7e456c7dc5cd7ecec46f1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatabaseConfig")
    def put_database_config(
        self,
        *,
        machine_type: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_type: Optional. Cloud SQL machine type used by Airflow database. It has to be one of: db-n1-standard-2, db-n1-standard-4, db-n1-standard-8 or db-n1-standard-16. If not specified, db-n1-standard-2 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        :param zone: Optional. Cloud SQL database preferred zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#zone GoogleComposerEnvironment#zone}
        '''
        value = GoogleComposerEnvironmentConfigDatabaseConfig(
            machine_type=machine_type, zone=zone
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseConfig", [value]))

    @jsii.member(jsii_name="putDataRetentionConfig")
    def put_data_retention_config(
        self,
        *,
        airflow_metadata_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_logs_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param airflow_metadata_retention_config: airflow_metadata_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#airflow_metadata_retention_config GoogleComposerEnvironment#airflow_metadata_retention_config}
        :param task_logs_retention_config: task_logs_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#task_logs_retention_config GoogleComposerEnvironment#task_logs_retention_config}
        '''
        value = GoogleComposerEnvironmentConfigDataRetentionConfig(
            airflow_metadata_retention_config=airflow_metadata_retention_config,
            task_logs_retention_config=task_logs_retention_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDataRetentionConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Optional. Customer-managed Encryption Key available through Google's Key Management Service. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#kms_key_name GoogleComposerEnvironment#kms_key_name}
        '''
        value = GoogleComposerEnvironmentConfigEncryptionConfig(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        end_time: builtins.str,
        recurrence: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param end_time: Maintenance window end time. It is used only to calculate the duration of the maintenance window. The value for end-time must be in the future, relative to 'start_time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#end_time GoogleComposerEnvironment#end_time}
        :param recurrence: Maintenance window recurrence. Format is a subset of RFC-5545 (https://tools.ietf.org/html/rfc5545) 'RRULE'. The only allowed values for 'FREQ' field are 'FREQ=DAILY' and 'FREQ=WEEKLY;BYDAY=...'. Example values: 'FREQ=WEEKLY;BYDAY=TU,WE', 'FREQ=DAILY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#recurrence GoogleComposerEnvironment#recurrence}
        :param start_time: Start time of the first recurrence of the maintenance window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#start_time GoogleComposerEnvironment#start_time}
        '''
        value = GoogleComposerEnvironmentConfigMaintenanceWindow(
            end_time=end_time, recurrence=recurrence, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putMasterAuthorizedNetworksConfig")
    def put_master_authorized_networks_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cidr_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not master authorized networks is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        :param cidr_blocks: cidr_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cidr_blocks GoogleComposerEnvironment#cidr_blocks}
        '''
        value = GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig(
            enabled=enabled, cidr_blocks=cidr_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putMasterAuthorizedNetworksConfig", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        composer_internal_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        composer_network_attachment: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        enable_ip_masq_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_allocation_policy: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param composer_internal_ipv4_cidr_block: IPv4 cidr range that will be used by Composer internal components. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#composer_internal_ipv4_cidr_block GoogleComposerEnvironment#composer_internal_ipv4_cidr_block}
        :param composer_network_attachment: PSC (Private Service Connect) Network entry point. Customers can pre-create the Network Attachment and point Cloud Composer environment to use. It is possible to share network attachment among many environments, provided enough IP addresses are available. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#composer_network_attachment GoogleComposerEnvironment#composer_network_attachment}
        :param disk_size_gb: The disk size in GB used for node VMs. Minimum size is 20GB. If unspecified, defaults to 100GB. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#disk_size_gb GoogleComposerEnvironment#disk_size_gb}
        :param enable_ip_masq_agent: Deploys 'ip-masq-agent' daemon set in the GKE cluster and defines nonMasqueradeCIDRs equals to pod IP range so IP masquerading is used for all destination addresses, except between pods traffic. See: https://cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_ip_masq_agent GoogleComposerEnvironment#enable_ip_masq_agent}
        :param ip_allocation_policy: ip_allocation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#ip_allocation_policy GoogleComposerEnvironment#ip_allocation_policy}
        :param machine_type: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        :param max_pods_per_node: The maximum pods per node in the GKE cluster allocated during environment creation. Lowering this value reduces IP address consumption by the Cloud Composer Kubernetes cluster. This value can only be set during environment creation, and only if the environment is VPC-Native. The range of possible values is 8-110, and the default is 32. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#max_pods_per_node GoogleComposerEnvironment#max_pods_per_node}
        :param network: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. The network must belong to the environment's project. If unspecified, the "default" network ID in the environment's project is used. If a Custom Subnet Network is provided, subnetwork must also be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#network GoogleComposerEnvironment#network}
        :param oauth_scopes: The set of Google API scopes to be made available on all node VMs. Cannot be updated. If empty, defaults to ["https://www.googleapis.com/auth/cloud-platform"]. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#oauth_scopes GoogleComposerEnvironment#oauth_scopes}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. If given, note that the service account must have roles/composer.worker for any GCP resources created under the Cloud Composer Environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#service_account GoogleComposerEnvironment#service_account}
        :param subnetwork: The Compute Engine subnetwork to be used for machine communications, specified as a self-link, relative resource name (e.g. "projects/{project}/regions/{region}/subnetworks/{subnetwork}"), or by name. If subnetwork is provided, network must also be provided and the subnetwork must belong to the enclosing environment's project and region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#subnetwork GoogleComposerEnvironment#subnetwork}
        :param tags: The list of instance tags applied to all node VMs. Tags are used to identify valid sources or targets for network firewalls. Each tag within the list must comply with RFC1035. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#tags GoogleComposerEnvironment#tags}
        :param zone: The Compute Engine zone in which to deploy the VMs running the Apache Airflow software, specified as the zone name or relative resource name (e.g. "projects/{project}/zones/{zone}"). Must belong to the enclosing environment's project and region. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#zone GoogleComposerEnvironment#zone}
        '''
        value = GoogleComposerEnvironmentConfigNodeConfig(
            composer_internal_ipv4_cidr_block=composer_internal_ipv4_cidr_block,
            composer_network_attachment=composer_network_attachment,
            disk_size_gb=disk_size_gb,
            enable_ip_masq_agent=enable_ip_masq_agent,
            ip_allocation_policy=ip_allocation_policy,
            machine_type=machine_type,
            max_pods_per_node=max_pods_per_node,
            network=network,
            oauth_scopes=oauth_scopes,
            service_account=service_account,
            subnetwork=subnetwork,
            tags=tags,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putPrivateEnvironmentConfig")
    def put_private_environment_config(
        self,
        *,
        cloud_composer_connection_subnetwork: typing.Optional[builtins.str] = None,
        cloud_composer_network_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        cloud_sql_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[builtins.str] = None,
        enable_private_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_privately_used_public_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        master_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        web_server_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_composer_connection_subnetwork: When specified, the environment will use Private Service Connect instead of VPC peerings to connect to Cloud SQL in the Tenant Project, and the PSC endpoint in the Customer Project will use an IP address from this subnetwork. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_composer_connection_subnetwork GoogleComposerEnvironment#cloud_composer_connection_subnetwork}
        :param cloud_composer_network_ipv4_cidr_block: The CIDR block from which IP range for Cloud Composer Network in tenant project will be reserved. Needs to be disjoint from private_cluster_config.master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_composer_network_ipv4_cidr_block GoogleComposerEnvironment#cloud_composer_network_ipv4_cidr_block}
        :param cloud_sql_ipv4_cidr_block: The CIDR block from which IP range in tenant project will be reserved for Cloud SQL. Needs to be disjoint from web_server_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_sql_ipv4_cidr_block GoogleComposerEnvironment#cloud_sql_ipv4_cidr_block}
        :param connection_type: Mode of internal communication within the Composer environment. Must be one of "VPC_PEERING" or "PRIVATE_SERVICE_CONNECT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#connection_type GoogleComposerEnvironment#connection_type}
        :param enable_private_endpoint: If true, access to the public endpoint of the GKE cluster is denied. If this field is set to true, ip_allocation_policy.use_ip_aliases must be set to true for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_endpoint GoogleComposerEnvironment#enable_private_endpoint}
        :param enable_privately_used_public_ips: When enabled, IPs from public (non-RFC1918) ranges can be used for ip_allocation_policy.cluster_ipv4_cidr_block and ip_allocation_policy.service_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_privately_used_public_ips GoogleComposerEnvironment#enable_privately_used_public_ips}
        :param master_ipv4_cidr_block: The IP range in CIDR notation to use for the hosted master network. This range is used for assigning internal IP addresses to the cluster master or set of masters and to the internal load balancer virtual IP. This range must not overlap with any other ranges in use within the cluster's network. If left blank, the default value of '172.16.0.0/28' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#master_ipv4_cidr_block GoogleComposerEnvironment#master_ipv4_cidr_block}
        :param web_server_ipv4_cidr_block: The CIDR block from which IP range for web server will be reserved. Needs to be disjoint from master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_ipv4_cidr_block GoogleComposerEnvironment#web_server_ipv4_cidr_block}
        '''
        value = GoogleComposerEnvironmentConfigPrivateEnvironmentConfig(
            cloud_composer_connection_subnetwork=cloud_composer_connection_subnetwork,
            cloud_composer_network_ipv4_cidr_block=cloud_composer_network_ipv4_cidr_block,
            cloud_sql_ipv4_cidr_block=cloud_sql_ipv4_cidr_block,
            connection_type=connection_type,
            enable_private_endpoint=enable_private_endpoint,
            enable_privately_used_public_ips=enable_privately_used_public_ips,
            master_ipv4_cidr_block=master_ipv4_cidr_block,
            web_server_ipv4_cidr_block=web_server_ipv4_cidr_block,
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateEnvironmentConfig", [value]))

    @jsii.member(jsii_name="putRecoveryConfig")
    def put_recovery_config(
        self,
        *,
        scheduled_snapshots_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled_snapshots_config: scheduled_snapshots_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduled_snapshots_config GoogleComposerEnvironment#scheduled_snapshots_config}
        '''
        value = GoogleComposerEnvironmentConfigRecoveryConfig(
            scheduled_snapshots_config=scheduled_snapshots_config
        )

        return typing.cast(None, jsii.invoke(self, "putRecoveryConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        airflow_config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_data_lineage_integration: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_version: typing.Optional[builtins.str] = None,
        pypi_packages: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_version: typing.Optional[builtins.str] = None,
        scheduler_count: typing.Optional[jsii.Number] = None,
        web_server_plugins_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param airflow_config_overrides: Apache Airflow configuration properties to override. Property keys contain the section and property names, separated by a hyphen, for example "core-dags_are_paused_at_creation". Section names must not contain hyphens ("-"), opening square brackets ("["), or closing square brackets ("]"). The property name must not be empty and cannot contain "=" or ";". Section and property names cannot contain characters: "." Apache Airflow configuration property names must be written in snake_case. Property values can contain any character, and can be written in any lower/upper case format. Certain Apache Airflow configuration property values are blacklisted, and cannot be overridden. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#airflow_config_overrides GoogleComposerEnvironment#airflow_config_overrides}
        :param cloud_data_lineage_integration: cloud_data_lineage_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_data_lineage_integration GoogleComposerEnvironment#cloud_data_lineage_integration}
        :param env_variables: Additional environment variables to provide to the Apache Airflow scheduler, worker, and webserver processes. Environment variable names must match the regular expression [a-zA-Z_][a-zA-Z0-9_]*. They cannot specify Apache Airflow software configuration overrides (they cannot match the regular expression AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+), and they cannot match any of the following reserved names: AIRFLOW_HOME C_FORCE_ROOT CONTAINER_NAME DAGS_FOLDER GCP_PROJECT GCS_BUCKET GKE_CLUSTER_NAME SQL_DATABASE SQL_INSTANCE SQL_PASSWORD SQL_PROJECT SQL_REGION SQL_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#env_variables GoogleComposerEnvironment#env_variables}
        :param image_version: The version of the software running in the environment. This encapsulates both the version of Cloud Composer functionality and the version of Apache Airflow. It must match the regular expression composer-([0-9]+(.[0-9]+.[0-9]+(-preview.[0-9]+)?)?|latest)-airflow-([0-9]+(.[0-9]+(.[0-9]+)?)?). The Cloud Composer portion of the image version is a full semantic version, or an alias in the form of major version number or 'latest'. The Apache Airflow portion of the image version is a full semantic version that points to one of the supported Apache Airflow versions, or an alias in the form of only major or major.minor versions specified. See documentation for more details and version list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#image_version GoogleComposerEnvironment#image_version}
        :param pypi_packages: Custom Python Package Index (PyPI) packages to be installed in the environment. Keys refer to the lowercase package name (e.g. "numpy"). Values are the lowercase extras and version specifier (e.g. "==1.12.0", "[devel,gcp_api]", "[devel]>=1.8.2, <1.9.2"). To specify a package without pinning it to a version specifier, use the empty string as the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#pypi_packages GoogleComposerEnvironment#pypi_packages}
        :param python_version: The major version of Python used to run the Apache Airflow scheduler, worker, and webserver processes. Can be set to '2' or '3'. If not specified, the default is '2'. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use Python major version 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#python_version GoogleComposerEnvironment#python_version}
        :param scheduler_count: The number of schedulers for Airflow. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-2.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduler_count GoogleComposerEnvironment#scheduler_count}
        :param web_server_plugins_mode: Should be either 'ENABLED' or 'DISABLED'. Defaults to 'ENABLED'. Used in Composer 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_plugins_mode GoogleComposerEnvironment#web_server_plugins_mode}
        '''
        value = GoogleComposerEnvironmentConfigSoftwareConfig(
            airflow_config_overrides=airflow_config_overrides,
            cloud_data_lineage_integration=cloud_data_lineage_integration,
            env_variables=env_variables,
            image_version=image_version,
            pypi_packages=pypi_packages,
            python_version=python_version,
            scheduler_count=scheduler_count,
            web_server_plugins_mode=web_server_plugins_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putSoftwareConfig", [value]))

    @jsii.member(jsii_name="putWebServerConfig")
    def put_web_server_config(self, *, machine_type: builtins.str) -> None:
        '''
        :param machine_type: Optional. Machine type on which Airflow web server is running. It has to be one of: composer-n1-webserver-2, composer-n1-webserver-4 or composer-n1-webserver-8. If not specified, composer-n1-webserver-2 will be used. Value custom is returned only in response, if Airflow web server parameters were manually changed to a non-standard values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        '''
        value = GoogleComposerEnvironmentConfigWebServerConfig(
            machine_type=machine_type
        )

        return typing.cast(None, jsii.invoke(self, "putWebServerConfig", [value]))

    @jsii.member(jsii_name="putWebServerNetworkAccessControl")
    def put_web_server_network_access_control(
        self,
        *,
        allowed_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_ip_range: allowed_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#allowed_ip_range GoogleComposerEnvironment#allowed_ip_range}
        '''
        value = GoogleComposerEnvironmentConfigWebServerNetworkAccessControl(
            allowed_ip_range=allowed_ip_range
        )

        return typing.cast(None, jsii.invoke(self, "putWebServerNetworkAccessControl", [value]))

    @jsii.member(jsii_name="putWorkloadsConfig")
    def put_workloads_config(
        self,
        *,
        dag_processor: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigScheduler", typing.Dict[builtins.str, typing.Any]]] = None,
        triggerer: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigWebServer", typing.Dict[builtins.str, typing.Any]]] = None,
        worker: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigWorker", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dag_processor: dag_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#dag_processor GoogleComposerEnvironment#dag_processor}
        :param scheduler: scheduler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduler GoogleComposerEnvironment#scheduler}
        :param triggerer: triggerer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#triggerer GoogleComposerEnvironment#triggerer}
        :param web_server: web_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server GoogleComposerEnvironment#web_server}
        :param worker: worker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#worker GoogleComposerEnvironment#worker}
        '''
        value = GoogleComposerEnvironmentConfigWorkloadsConfig(
            dag_processor=dag_processor,
            scheduler=scheduler,
            triggerer=triggerer,
            web_server=web_server,
            worker=worker,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkloadsConfig", [value]))

    @jsii.member(jsii_name="resetDatabaseConfig")
    def reset_database_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseConfig", []))

    @jsii.member(jsii_name="resetDataRetentionConfig")
    def reset_data_retention_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataRetentionConfig", []))

    @jsii.member(jsii_name="resetEnablePrivateBuildsOnly")
    def reset_enable_private_builds_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePrivateBuildsOnly", []))

    @jsii.member(jsii_name="resetEnablePrivateEnvironment")
    def reset_enable_private_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePrivateEnvironment", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetEnvironmentSize")
    def reset_environment_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentSize", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetMasterAuthorizedNetworksConfig")
    def reset_master_authorized_networks_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterAuthorizedNetworksConfig", []))

    @jsii.member(jsii_name="resetNodeConfig")
    def reset_node_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeConfig", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetPrivateEnvironmentConfig")
    def reset_private_environment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateEnvironmentConfig", []))

    @jsii.member(jsii_name="resetRecoveryConfig")
    def reset_recovery_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryConfig", []))

    @jsii.member(jsii_name="resetResilienceMode")
    def reset_resilience_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResilienceMode", []))

    @jsii.member(jsii_name="resetSoftwareConfig")
    def reset_software_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareConfig", []))

    @jsii.member(jsii_name="resetWebServerConfig")
    def reset_web_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebServerConfig", []))

    @jsii.member(jsii_name="resetWebServerNetworkAccessControl")
    def reset_web_server_network_access_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebServerNetworkAccessControl", []))

    @jsii.member(jsii_name="resetWorkloadsConfig")
    def reset_workloads_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="airflowUri")
    def airflow_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "airflowUri"))

    @builtins.property
    @jsii.member(jsii_name="dagGcsPrefix")
    def dag_gcs_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dagGcsPrefix"))

    @builtins.property
    @jsii.member(jsii_name="databaseConfig")
    def database_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigDatabaseConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigDatabaseConfigOutputReference", jsii.get(self, "databaseConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionConfig")
    def data_retention_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigDataRetentionConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigDataRetentionConfigOutputReference", jsii.get(self, "dataRetentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigEncryptionConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="gkeCluster")
    def gke_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeCluster"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "GoogleComposerEnvironmentConfigMaintenanceWindowOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="masterAuthorizedNetworksConfig")
    def master_authorized_networks_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference", jsii.get(self, "masterAuthorizedNetworksConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GoogleComposerEnvironmentConfigNodeConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateEnvironmentConfig")
    def private_environment_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference", jsii.get(self, "privateEnvironmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="recoveryConfig")
    def recovery_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigRecoveryConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigRecoveryConfigOutputReference", jsii.get(self, "recoveryConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigSoftwareConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="webServerConfig")
    def web_server_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigWebServerConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWebServerConfigOutputReference", jsii.get(self, "webServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="webServerNetworkAccessControl")
    def web_server_network_access_control(
        self,
    ) -> "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference", jsii.get(self, "webServerNetworkAccessControl"))

    @builtins.property
    @jsii.member(jsii_name="workloadsConfig")
    def workloads_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigWorkloadsConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWorkloadsConfigOutputReference", jsii.get(self, "workloadsConfig"))

    @builtins.property
    @jsii.member(jsii_name="databaseConfigInput")
    def database_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigDatabaseConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigDatabaseConfig"], jsii.get(self, "databaseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionConfigInput")
    def data_retention_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigDataRetentionConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigDataRetentionConfig"], jsii.get(self, "dataRetentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateBuildsOnlyInput")
    def enable_private_builds_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivateBuildsOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateEnvironmentInput")
    def enable_private_environment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivateEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigEncryptionConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentSizeInput")
    def environment_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigMaintenanceWindow"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="masterAuthorizedNetworksConfigInput")
    def master_authorized_networks_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig"], jsii.get(self, "masterAuthorizedNetworksConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigNodeConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="privateEnvironmentConfigInput")
    def private_environment_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigPrivateEnvironmentConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigPrivateEnvironmentConfig"], jsii.get(self, "privateEnvironmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryConfigInput")
    def recovery_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfig"], jsii.get(self, "recoveryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="resilienceModeInput")
    def resilience_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resilienceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigSoftwareConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerConfigInput")
    def web_server_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWebServerConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWebServerConfig"], jsii.get(self, "webServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerNetworkAccessControlInput")
    def web_server_network_access_control_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWebServerNetworkAccessControl"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWebServerNetworkAccessControl"], jsii.get(self, "webServerNetworkAccessControlInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadsConfigInput")
    def workloads_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfig"], jsii.get(self, "workloadsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateBuildsOnly")
    def enable_private_builds_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivateBuildsOnly"))

    @enable_private_builds_only.setter
    def enable_private_builds_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264472f671f8096f16d59ec35f7bd3fe6b03236a20b67a0ec2727326a26f5d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateBuildsOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePrivateEnvironment")
    def enable_private_environment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivateEnvironment"))

    @enable_private_environment.setter
    def enable_private_environment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a25d0e4172bb7436643c8e107b6ff453507260af466d2dfdfcadef17fe239f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentSize")
    def environment_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentSize"))

    @environment_size.setter
    def environment_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb22d7ab17306de93b3f1223f72014b9c54515354495910c4f9fa6d924945fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baec230458d3650cec4d4a0180a721766b4479427731f9ba82a47c87ccdb165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resilienceMode")
    def resilience_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resilienceMode"))

    @resilience_mode.setter
    def resilience_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fd4174cee128ec88ccfcc00f1bf5e54f61914705d867c26366276d3da151db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resilienceMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComposerEnvironmentConfigA]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4931c17e1743f8d67ba9ba6ef245677b92a52493145f7c3154b3ab55fc16bf42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_metadata_retention_config": "airflowMetadataRetentionConfig",
        "task_logs_retention_config": "taskLogsRetentionConfig",
    },
)
class GoogleComposerEnvironmentConfigDataRetentionConfig:
    def __init__(
        self,
        *,
        airflow_metadata_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_logs_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param airflow_metadata_retention_config: airflow_metadata_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#airflow_metadata_retention_config GoogleComposerEnvironment#airflow_metadata_retention_config}
        :param task_logs_retention_config: task_logs_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#task_logs_retention_config GoogleComposerEnvironment#task_logs_retention_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06be248df1197e20dab725057281d48b8dc1487b3e19c6576c3f43b822d7d95)
            check_type(argname="argument airflow_metadata_retention_config", value=airflow_metadata_retention_config, expected_type=type_hints["airflow_metadata_retention_config"])
            check_type(argname="argument task_logs_retention_config", value=task_logs_retention_config, expected_type=type_hints["task_logs_retention_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if airflow_metadata_retention_config is not None:
            self._values["airflow_metadata_retention_config"] = airflow_metadata_retention_config
        if task_logs_retention_config is not None:
            self._values["task_logs_retention_config"] = task_logs_retention_config

    @builtins.property
    def airflow_metadata_retention_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig"]]]:
        '''airflow_metadata_retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#airflow_metadata_retention_config GoogleComposerEnvironment#airflow_metadata_retention_config}
        '''
        result = self._values.get("airflow_metadata_retention_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig"]]], result)

    @builtins.property
    def task_logs_retention_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]]:
        '''task_logs_retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#task_logs_retention_config GoogleComposerEnvironment#task_logs_retention_config}
        '''
        result = self._values.get("task_logs_retention_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigDataRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "retention_days": "retentionDays",
        "retention_mode": "retentionMode",
    },
)
class GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig:
    def __init__(
        self,
        *,
        retention_days: typing.Optional[jsii.Number] = None,
        retention_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retention_days: How many days data should be retained for. This field is supported for Cloud Composer environments in composer 3 and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#retention_days GoogleComposerEnvironment#retention_days}
        :param retention_mode: Whether database retention is enabled or not. This field is supported for Cloud Composer environments in composer 3 and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#retention_mode GoogleComposerEnvironment#retention_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7bdaa902838281dc4887a6d388685a1696aa20f4efa856a94baa1a72d979d05)
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            check_type(argname="argument retention_mode", value=retention_mode, expected_type=type_hints["retention_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_days is not None:
            self._values["retention_days"] = retention_days
        if retention_mode is not None:
            self._values["retention_mode"] = retention_mode

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''How many days data should be retained for.

        This field is supported for Cloud Composer environments in composer 3 and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#retention_days GoogleComposerEnvironment#retention_days}
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_mode(self) -> typing.Optional[builtins.str]:
        '''Whether database retention is enabled or not.

        This field is supported for Cloud Composer environments in composer 3 and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#retention_mode GoogleComposerEnvironment#retention_mode}
        '''
        result = self._values.get("retention_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__505e89b4d3dec77375f5a8049c75044c25310bf49fd0e25f8448d77f50f5c587)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a65911ea6735e2621c7c77c9d9fdfa8f7e14fb80b33ef3da68c353cbf983cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b468dbcf2f8f04a8c17cc732070c17f5382ef4c58b776e90ff218b9640e640)
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
            type_hints = typing.get_type_hints(_typecheckingstub__180dc0572acd525526a5a729b72404e86bd0e335d55a96560eafb6b644416b60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9139047f2e1665bb0c6111fbdc685817025cab2945db7dae8c2e6c526e1cd24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a504806e6915a9cb5496a5cc95eb1727bc37f587406aa2d453ab22e8bdbe7818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39c45466d09c7fc078781a2855f5f2706a83729b884dac6410c7031302a37094)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRetentionDays")
    def reset_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDays", []))

    @jsii.member(jsii_name="resetRetentionMode")
    def reset_retention_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionMode", []))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionModeInput")
    def retention_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a15183045eca43759fb33958e676c441f675009780f6af7e2bffa4b697ae769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionMode")
    def retention_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionMode"))

    @retention_mode.setter
    def retention_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e082c78d0978d7755afa33cd465dc3a03fe0c70b54022685183f57d8fe9f1f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b891091b21baa13cccbb29274d9669ccada240b5234e890a963c7af5daae37a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigDataRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6535316b7b80a0b7e67c5605025493423979dcdb8aad3fd55e4b0986dc41b6a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAirflowMetadataRetentionConfig")
    def put_airflow_metadata_retention_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93db275c19425e35f5cf288be50ede4d8b1e988dd839bef13bd448bd3f7c37c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAirflowMetadataRetentionConfig", [value]))

    @jsii.member(jsii_name="putTaskLogsRetentionConfig")
    def put_task_logs_retention_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa04c304d2ff0cc2ca8efae27d4b20fa901797afc21158b1035f577410664898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaskLogsRetentionConfig", [value]))

    @jsii.member(jsii_name="resetAirflowMetadataRetentionConfig")
    def reset_airflow_metadata_retention_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAirflowMetadataRetentionConfig", []))

    @jsii.member(jsii_name="resetTaskLogsRetentionConfig")
    def reset_task_logs_retention_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskLogsRetentionConfig", []))

    @builtins.property
    @jsii.member(jsii_name="airflowMetadataRetentionConfig")
    def airflow_metadata_retention_config(
        self,
    ) -> GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList:
        return typing.cast(GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList, jsii.get(self, "airflowMetadataRetentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="taskLogsRetentionConfig")
    def task_logs_retention_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList":
        return typing.cast("GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList", jsii.get(self, "taskLogsRetentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="airflowMetadataRetentionConfigInput")
    def airflow_metadata_retention_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]], jsii.get(self, "airflowMetadataRetentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="taskLogsRetentionConfigInput")
    def task_logs_retention_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]], jsii.get(self, "taskLogsRetentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigDataRetentionConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigDataRetentionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigDataRetentionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6866733cd38d12c832e3083a79317d57f5fd4502140509ca22759be35753106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={"storage_mode": "storageMode"},
)
class GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig:
    def __init__(self, *, storage_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param storage_mode: Whether logs in cloud logging only is enabled or not. This field is supported for Cloud Composer environments in versions composer-2.0.32-airflow-2.1.4 and newer but not in composer-3* Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_mode GoogleComposerEnvironment#storage_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581fd1632c3bae82d60ddc42e77fd27073e7a14c39b9fa6d1166a5e3c4212169)
            check_type(argname="argument storage_mode", value=storage_mode, expected_type=type_hints["storage_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if storage_mode is not None:
            self._values["storage_mode"] = storage_mode

    @builtins.property
    def storage_mode(self) -> typing.Optional[builtins.str]:
        '''Whether logs in cloud logging only is enabled or not.

        This field is supported for Cloud Composer environments in versions composer-2.0.32-airflow-2.1.4 and newer but not in composer-3*

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_mode GoogleComposerEnvironment#storage_mode}
        '''
        result = self._values.get("storage_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed97819fe6d7fbded4966f2e848ebfc6a4501f6978a889a196c328e74260482)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088ebe926ccf7ad9319ebd6bd96054dd9b213aa7f0f65c81d58e08b1406fd757)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08459314ba5a857ad5f8163c7f5676d47f3ff349a8da3a644a10f09b63bb7c94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ffb93f11753120cfd0d49f58f96dd63bbce5d5a894e9ca87ca4081c838ad418)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a616e75c50472254fad2253adac578f5ee277b5da1cf9009266ba42d8f1adaa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1624b36a501a9c4acd1039dcd3e39a60a62abae808e3ca1b2917457a9f94fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1e1c12da9eb2483518d9b22e54abdd9418b8268b08a9055abcedcffed97edb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStorageMode")
    def reset_storage_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageMode", []))

    @builtins.property
    @jsii.member(jsii_name="storageModeInput")
    def storage_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageModeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageMode")
    def storage_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageMode"))

    @storage_mode.setter
    def storage_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b9840428ed3caa3972415d116d0aba4c4e0d53a847175b2bd34101787569b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4a2e63043c3234f0666871a41a88d80981ed3cfb55df0695acc57425057aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDatabaseConfig",
    jsii_struct_bases=[],
    name_mapping={"machine_type": "machineType", "zone": "zone"},
)
class GoogleComposerEnvironmentConfigDatabaseConfig:
    def __init__(
        self,
        *,
        machine_type: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_type: Optional. Cloud SQL machine type used by Airflow database. It has to be one of: db-n1-standard-2, db-n1-standard-4, db-n1-standard-8 or db-n1-standard-16. If not specified, db-n1-standard-2 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        :param zone: Optional. Cloud SQL database preferred zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#zone GoogleComposerEnvironment#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a24f0a52739eac8c9933d6a4bf493b6380ccfd4ddf21fa253bec29bfcbc1a7)
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Cloud SQL machine type used by Airflow database. It has to be one of: db-n1-standard-2, db-n1-standard-4, db-n1-standard-8 or db-n1-standard-16. If not specified, db-n1-standard-2 will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional. Cloud SQL database preferred zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#zone GoogleComposerEnvironment#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigDatabaseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigDatabaseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__976d41908666c65341cef47c473adbd02a937218ebb9ed01bebf1c054e862a2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9095a272f15d778f88d0dcdd8eabe3faf144d396e8cab545ed6aacf1225e1725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749cdbf4b4215801b3a25e096612789d92d621fb7660d16650bc284df5cb7500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigDatabaseConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigDatabaseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigDatabaseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3607d7a3453a0d0c5dd401c0f2186e34ab22483087ed3a56c9016cda437ff733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleComposerEnvironmentConfigEncryptionConfig:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Optional. Customer-managed Encryption Key available through Google's Key Management Service. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#kms_key_name GoogleComposerEnvironment#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b2e6d0a5ba904eda299fc25fa0db73949f76dec3d4e2c90509d4c719f4eba3)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Optional. Customer-managed Encryption Key available through Google's Key Management Service. Cannot be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#kms_key_name GoogleComposerEnvironment#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__629c4ab4ba33be5e5bbd08d9f5c39ac78eb207a74fe2953ecf4dfa426a8e7f79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b8bb092442c8a7f2ad05ffcee72163cf01f0c95346ed8ed54cf1959ca6054c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff84dbebf4b17fa51f179de0ee582074ef8e92ba8ed037e583bec3060a01418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "end_time": "endTime",
        "recurrence": "recurrence",
        "start_time": "startTime",
    },
)
class GoogleComposerEnvironmentConfigMaintenanceWindow:
    def __init__(
        self,
        *,
        end_time: builtins.str,
        recurrence: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param end_time: Maintenance window end time. It is used only to calculate the duration of the maintenance window. The value for end-time must be in the future, relative to 'start_time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#end_time GoogleComposerEnvironment#end_time}
        :param recurrence: Maintenance window recurrence. Format is a subset of RFC-5545 (https://tools.ietf.org/html/rfc5545) 'RRULE'. The only allowed values for 'FREQ' field are 'FREQ=DAILY' and 'FREQ=WEEKLY;BYDAY=...'. Example values: 'FREQ=WEEKLY;BYDAY=TU,WE', 'FREQ=DAILY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#recurrence GoogleComposerEnvironment#recurrence}
        :param start_time: Start time of the first recurrence of the maintenance window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#start_time GoogleComposerEnvironment#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f806ff1d257b96da650cbf0acd016bb15f7b6cfc81d2dcd80bc31972ac8e7219)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_time": end_time,
            "recurrence": recurrence,
            "start_time": start_time,
        }

    @builtins.property
    def end_time(self) -> builtins.str:
        '''Maintenance window end time.

        It is used only to calculate the duration of the maintenance window. The value for end-time must be in the future, relative to 'start_time'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#end_time GoogleComposerEnvironment#end_time}
        '''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence(self) -> builtins.str:
        '''Maintenance window recurrence.

        Format is a subset of RFC-5545 (https://tools.ietf.org/html/rfc5545) 'RRULE'. The only allowed values for 'FREQ' field are 'FREQ=DAILY' and 'FREQ=WEEKLY;BYDAY=...'. Example values: 'FREQ=WEEKLY;BYDAY=TU,WE', 'FREQ=DAILY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#recurrence GoogleComposerEnvironment#recurrence}
        '''
        result = self._values.get("recurrence")
        assert result is not None, "Required property 'recurrence' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Start time of the first recurrence of the maintenance window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#start_time GoogleComposerEnvironment#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72bebd5b3ed1376bb2da575ff3418422700ab8584810f5888a9c5109959242ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24435bd48fcdff76f2f38c90824ec192fd01f02cc8f9d1689f50544a1dba0305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrence"))

    @recurrence.setter
    def recurrence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7512906ba417d4541ebabf9fb396d08c9c9bdbc563b4bc3e8bd5f1f80b9e0e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b483d41fd6a4a1ff6ed1a96927458cdd8437ea48b61bfcab699ebf442b5056d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9110d25b893d1f663e84882021a16c8e7dcc51a28d684dc692bb82c0758fda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "cidr_blocks": "cidrBlocks"},
)
class GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cidr_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not master authorized networks is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        :param cidr_blocks: cidr_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cidr_blocks GoogleComposerEnvironment#cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38be4ce0698dbaddd8c822ac94a37496faeb8827b805c659835cc8de885f013)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument cidr_blocks", value=cidr_blocks, expected_type=type_hints["cidr_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if cidr_blocks is not None:
            self._values["cidr_blocks"] = cidr_blocks

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not master authorized networks is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cidr_blocks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks"]]]:
        '''cidr_blocks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cidr_blocks GoogleComposerEnvironment#cidr_blocks}
        '''
        result = self._values.get("cidr_blocks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks",
    jsii_struct_bases=[],
    name_mapping={"cidr_block": "cidrBlock", "display_name": "displayName"},
)
class GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks:
    def __init__(
        self,
        *,
        cidr_block: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cidr_block: cidr_block must be specified in CIDR notation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cidr_block GoogleComposerEnvironment#cidr_block}
        :param display_name: display_name is a field for users to identify CIDR blocks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#display_name GoogleComposerEnvironment#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421d13eda24fec0bbb4bbf12c36f8e1e79841ea5dca510dbecc09c021728f484)
            check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr_block": cidr_block,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def cidr_block(self) -> builtins.str:
        '''cidr_block must be specified in CIDR notation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cidr_block GoogleComposerEnvironment#cidr_block}
        '''
        result = self._values.get("cidr_block")
        assert result is not None, "Required property 'cidr_block' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''display_name is a field for users to identify CIDR blocks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#display_name GoogleComposerEnvironment#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e093dc69775f3bf6f454978085cd08c9633f9b3651836f80de490f7b0d389fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b235c6eff8207b02644ba8a1438e86671e1d7c27aff45b3d14f5556b44819f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1409be879dcee521c3a37f1f6639121e3d9ec892b35f88bb45c74b9aeebeefa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7890e019a44cf698a5ef1da8e8d3686ecb4dae68ca8504eec40dd394cdae7c6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe7602f837c6027b86a069a3e7695cbaeca736f53634e361180d49a64586ebba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02af2fe390e371900719259acc74052995e7e4a4a58f9832dc8e96dc5ec5829b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c1504a63cca1cc25fe6495b8fd660ec6444d74c79232430cfbaeed67bfe2e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="cidrBlockInput")
    def cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidrBlock"))

    @cidr_block.setter
    def cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f308bd088ddf1f67808651b78bf49ca569c11e5327261e039cc4f9690da6dc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1765441e4bd182e66bf0c9d1e3ceaf051262550f65a7fa0a85adb766bf5ab50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008804e5ee92012ef1b605c2bf91aa9e8e7cb208bebc2e5eb7ec62b6fb5b97f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4751839d4fdbeae238a880e0dcfbc520ee8efe938d085c73cebef616c621481)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCidrBlocks")
    def put_cidr_blocks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8efceb17e8a5eb0bc528b7dab0ea1ccedb3300b126f6e2d99e812e51118510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCidrBlocks", [value]))

    @jsii.member(jsii_name="resetCidrBlocks")
    def reset_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrBlocks", []))

    @builtins.property
    @jsii.member(jsii_name="cidrBlocks")
    def cidr_blocks(
        self,
    ) -> GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList:
        return typing.cast(GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList, jsii.get(self, "cidrBlocks"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlocksInput")
    def cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]], jsii.get(self, "cidrBlocksInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7849efe19b4b87363d6de374d265b63c407f6a8e59af17b7fb7dba7b62a38a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d42977ba151518d97a50229468afc8d7292333fa8020c2c6251a1ece6cfc7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "composer_internal_ipv4_cidr_block": "composerInternalIpv4CidrBlock",
        "composer_network_attachment": "composerNetworkAttachment",
        "disk_size_gb": "diskSizeGb",
        "enable_ip_masq_agent": "enableIpMasqAgent",
        "ip_allocation_policy": "ipAllocationPolicy",
        "machine_type": "machineType",
        "max_pods_per_node": "maxPodsPerNode",
        "network": "network",
        "oauth_scopes": "oauthScopes",
        "service_account": "serviceAccount",
        "subnetwork": "subnetwork",
        "tags": "tags",
        "zone": "zone",
    },
)
class GoogleComposerEnvironmentConfigNodeConfig:
    def __init__(
        self,
        *,
        composer_internal_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        composer_network_attachment: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        enable_ip_masq_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_allocation_policy: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        network: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param composer_internal_ipv4_cidr_block: IPv4 cidr range that will be used by Composer internal components. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#composer_internal_ipv4_cidr_block GoogleComposerEnvironment#composer_internal_ipv4_cidr_block}
        :param composer_network_attachment: PSC (Private Service Connect) Network entry point. Customers can pre-create the Network Attachment and point Cloud Composer environment to use. It is possible to share network attachment among many environments, provided enough IP addresses are available. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#composer_network_attachment GoogleComposerEnvironment#composer_network_attachment}
        :param disk_size_gb: The disk size in GB used for node VMs. Minimum size is 20GB. If unspecified, defaults to 100GB. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#disk_size_gb GoogleComposerEnvironment#disk_size_gb}
        :param enable_ip_masq_agent: Deploys 'ip-masq-agent' daemon set in the GKE cluster and defines nonMasqueradeCIDRs equals to pod IP range so IP masquerading is used for all destination addresses, except between pods traffic. See: https://cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_ip_masq_agent GoogleComposerEnvironment#enable_ip_masq_agent}
        :param ip_allocation_policy: ip_allocation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#ip_allocation_policy GoogleComposerEnvironment#ip_allocation_policy}
        :param machine_type: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        :param max_pods_per_node: The maximum pods per node in the GKE cluster allocated during environment creation. Lowering this value reduces IP address consumption by the Cloud Composer Kubernetes cluster. This value can only be set during environment creation, and only if the environment is VPC-Native. The range of possible values is 8-110, and the default is 32. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#max_pods_per_node GoogleComposerEnvironment#max_pods_per_node}
        :param network: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. The network must belong to the environment's project. If unspecified, the "default" network ID in the environment's project is used. If a Custom Subnet Network is provided, subnetwork must also be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#network GoogleComposerEnvironment#network}
        :param oauth_scopes: The set of Google API scopes to be made available on all node VMs. Cannot be updated. If empty, defaults to ["https://www.googleapis.com/auth/cloud-platform"]. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#oauth_scopes GoogleComposerEnvironment#oauth_scopes}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. If given, note that the service account must have roles/composer.worker for any GCP resources created under the Cloud Composer Environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#service_account GoogleComposerEnvironment#service_account}
        :param subnetwork: The Compute Engine subnetwork to be used for machine communications, specified as a self-link, relative resource name (e.g. "projects/{project}/regions/{region}/subnetworks/{subnetwork}"), or by name. If subnetwork is provided, network must also be provided and the subnetwork must belong to the enclosing environment's project and region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#subnetwork GoogleComposerEnvironment#subnetwork}
        :param tags: The list of instance tags applied to all node VMs. Tags are used to identify valid sources or targets for network firewalls. Each tag within the list must comply with RFC1035. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#tags GoogleComposerEnvironment#tags}
        :param zone: The Compute Engine zone in which to deploy the VMs running the Apache Airflow software, specified as the zone name or relative resource name (e.g. "projects/{project}/zones/{zone}"). Must belong to the enclosing environment's project and region. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#zone GoogleComposerEnvironment#zone}
        '''
        if isinstance(ip_allocation_policy, dict):
            ip_allocation_policy = GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy(**ip_allocation_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e478c439c73439e119f9c8a544739a138ab659e35fd2e6224ef3e5a03fbdf5b)
            check_type(argname="argument composer_internal_ipv4_cidr_block", value=composer_internal_ipv4_cidr_block, expected_type=type_hints["composer_internal_ipv4_cidr_block"])
            check_type(argname="argument composer_network_attachment", value=composer_network_attachment, expected_type=type_hints["composer_network_attachment"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument enable_ip_masq_agent", value=enable_ip_masq_agent, expected_type=type_hints["enable_ip_masq_agent"])
            check_type(argname="argument ip_allocation_policy", value=ip_allocation_policy, expected_type=type_hints["ip_allocation_policy"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if composer_internal_ipv4_cidr_block is not None:
            self._values["composer_internal_ipv4_cidr_block"] = composer_internal_ipv4_cidr_block
        if composer_network_attachment is not None:
            self._values["composer_network_attachment"] = composer_network_attachment
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if enable_ip_masq_agent is not None:
            self._values["enable_ip_masq_agent"] = enable_ip_masq_agent
        if ip_allocation_policy is not None:
            self._values["ip_allocation_policy"] = ip_allocation_policy
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node
        if network is not None:
            self._values["network"] = network
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes
        if service_account is not None:
            self._values["service_account"] = service_account
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tags is not None:
            self._values["tags"] = tags
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def composer_internal_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv4 cidr range that will be used by Composer internal components.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#composer_internal_ipv4_cidr_block GoogleComposerEnvironment#composer_internal_ipv4_cidr_block}
        '''
        result = self._values.get("composer_internal_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def composer_network_attachment(self) -> typing.Optional[builtins.str]:
        '''PSC (Private Service Connect) Network entry point.

        Customers can pre-create the Network Attachment and point Cloud Composer environment to use. It is possible to share network attachment among many environments, provided enough IP addresses are available.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#composer_network_attachment GoogleComposerEnvironment#composer_network_attachment}
        '''
        result = self._values.get("composer_network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The disk size in GB used for node VMs.

        Minimum size is 20GB. If unspecified, defaults to 100GB. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#disk_size_gb GoogleComposerEnvironment#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ip_masq_agent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deploys 'ip-masq-agent' daemon set in the GKE cluster and defines nonMasqueradeCIDRs equals to pod IP range so IP masquerading is used for all destination addresses, except between pods traffic.

        See: https://cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_ip_masq_agent GoogleComposerEnvironment#enable_ip_masq_agent}
        '''
        result = self._values.get("enable_ip_masq_agent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_allocation_policy(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy"]:
        '''ip_allocation_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#ip_allocation_policy GoogleComposerEnvironment#ip_allocation_policy}
        '''
        result = self._values.get("ip_allocation_policy")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy"], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine machine type used for cluster instances, specified as a name or relative resource name.

        For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''The maximum pods per node in the GKE cluster allocated during environment creation.

        Lowering this value reduces IP address consumption by the Cloud Composer Kubernetes cluster. This value can only be set during environment creation, and only if the environment is VPC-Native. The range of possible values is 8-110, and the default is 32. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#max_pods_per_node GoogleComposerEnvironment#max_pods_per_node}
        '''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine machine type used for cluster instances, specified as a name or relative resource name.

        For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. The network must belong to the environment's project. If unspecified, the "default" network ID in the environment's project is used. If a Custom Subnet Network is provided, subnetwork must also be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#network GoogleComposerEnvironment#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of Google API scopes to be made available on all node VMs.

        Cannot be updated. If empty, defaults to ["https://www.googleapis.com/auth/cloud-platform"]. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#oauth_scopes GoogleComposerEnvironment#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform Service Account to be used by the node VMs.

        If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. If given, note that the service account must have roles/composer.worker for any GCP resources created under the Cloud Composer Environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#service_account GoogleComposerEnvironment#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine subnetwork to be used for machine communications, specified as a self-link, relative resource name (e.g. "projects/{project}/regions/{region}/subnetworks/{subnetwork}"), or by name. If subnetwork is provided, network must also be provided and the subnetwork must belong to the enclosing environment's project and region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#subnetwork GoogleComposerEnvironment#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of instance tags applied to all node VMs.

        Tags are used to identify valid sources or targets for network firewalls. Each tag within the list must comply with RFC1035. Cannot be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#tags GoogleComposerEnvironment#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone in which to deploy the VMs running the Apache Airflow software, specified as the zone name or relative resource name (e.g. "projects/{project}/zones/{zone}"). Must belong to the enclosing environment's project and region. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#zone GoogleComposerEnvironment#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_ipv4_cidr_block": "clusterIpv4CidrBlock",
        "cluster_secondary_range_name": "clusterSecondaryRangeName",
        "services_ipv4_cidr_block": "servicesIpv4CidrBlock",
        "services_secondary_range_name": "servicesSecondaryRangeName",
        "use_ip_aliases": "useIpAliases",
    },
)
class GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy:
    def __init__(
        self,
        *,
        cluster_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        cluster_secondary_range_name: typing.Optional[builtins.str] = None,
        services_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        services_secondary_range_name: typing.Optional[builtins.str] = None,
        use_ip_aliases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_ipv4_cidr_block: The IP address range used to allocate IP addresses to pods in the cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cluster_ipv4_cidr_block GoogleComposerEnvironment#cluster_ipv4_cidr_block}
        :param cluster_secondary_range_name: The name of the cluster's secondary range used to allocate IP addresses to pods. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cluster_secondary_range_name GoogleComposerEnvironment#cluster_secondary_range_name}
        :param services_ipv4_cidr_block: The IP address range used to allocate IP addresses in this cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#services_ipv4_cidr_block GoogleComposerEnvironment#services_ipv4_cidr_block}
        :param services_secondary_range_name: The name of the services' secondary range used to allocate IP addresses to the cluster. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#services_secondary_range_name GoogleComposerEnvironment#services_secondary_range_name}
        :param use_ip_aliases: Whether or not to enable Alias IPs in the GKE cluster. If true, a VPC-native cluster is created. Defaults to true if the ip_allocation_policy block is present in config. This field is only supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use VPC-native GKE clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#use_ip_aliases GoogleComposerEnvironment#use_ip_aliases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17117a91daae18ba0ce49caaf849f28852d57dba96c569d25c69fd7fa9e32e4f)
            check_type(argname="argument cluster_ipv4_cidr_block", value=cluster_ipv4_cidr_block, expected_type=type_hints["cluster_ipv4_cidr_block"])
            check_type(argname="argument cluster_secondary_range_name", value=cluster_secondary_range_name, expected_type=type_hints["cluster_secondary_range_name"])
            check_type(argname="argument services_ipv4_cidr_block", value=services_ipv4_cidr_block, expected_type=type_hints["services_ipv4_cidr_block"])
            check_type(argname="argument services_secondary_range_name", value=services_secondary_range_name, expected_type=type_hints["services_secondary_range_name"])
            check_type(argname="argument use_ip_aliases", value=use_ip_aliases, expected_type=type_hints["use_ip_aliases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_ipv4_cidr_block is not None:
            self._values["cluster_ipv4_cidr_block"] = cluster_ipv4_cidr_block
        if cluster_secondary_range_name is not None:
            self._values["cluster_secondary_range_name"] = cluster_secondary_range_name
        if services_ipv4_cidr_block is not None:
            self._values["services_ipv4_cidr_block"] = services_ipv4_cidr_block
        if services_secondary_range_name is not None:
            self._values["services_secondary_range_name"] = services_secondary_range_name
        if use_ip_aliases is not None:
            self._values["use_ip_aliases"] = use_ip_aliases

    @builtins.property
    def cluster_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP address range used to allocate IP addresses to pods in the cluster.

        For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cluster_ipv4_cidr_block GoogleComposerEnvironment#cluster_ipv4_cidr_block}
        '''
        result = self._values.get("cluster_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_secondary_range_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster's secondary range used to allocate IP addresses to pods.

        Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cluster_secondary_range_name GoogleComposerEnvironment#cluster_secondary_range_name}
        '''
        result = self._values.get("cluster_secondary_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP address range used to allocate IP addresses in this cluster.

        For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#services_ipv4_cidr_block GoogleComposerEnvironment#services_ipv4_cidr_block}
        '''
        result = self._values.get("services_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services_secondary_range_name(self) -> typing.Optional[builtins.str]:
        '''The name of the services' secondary range used to allocate IP addresses to the cluster.

        Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#services_secondary_range_name GoogleComposerEnvironment#services_secondary_range_name}
        '''
        result = self._values.get("services_secondary_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ip_aliases(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to enable Alias IPs in the GKE cluster.

        If true, a VPC-native cluster is created. Defaults to true if the ip_allocation_policy block is present in config. This field is only supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use VPC-native GKE clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#use_ip_aliases GoogleComposerEnvironment#use_ip_aliases}
        '''
        result = self._values.get("use_ip_aliases")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b14e1982454e27bc2da5308cfbf5e809ee953e4dc722613ba3e0a7517de64fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterIpv4CidrBlock")
    def reset_cluster_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetClusterSecondaryRangeName")
    def reset_cluster_secondary_range_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterSecondaryRangeName", []))

    @jsii.member(jsii_name="resetServicesIpv4CidrBlock")
    def reset_services_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicesIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetServicesSecondaryRangeName")
    def reset_services_secondary_range_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicesSecondaryRangeName", []))

    @jsii.member(jsii_name="resetUseIpAliases")
    def reset_use_ip_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseIpAliases", []))

    @builtins.property
    @jsii.member(jsii_name="clusterIpv4CidrBlockInput")
    def cluster_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterSecondaryRangeNameInput")
    def cluster_secondary_range_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterSecondaryRangeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesIpv4CidrBlockInput")
    def services_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicesIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesSecondaryRangeNameInput")
    def services_secondary_range_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicesSecondaryRangeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="useIpAliasesInput")
    def use_ip_aliases_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useIpAliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIpv4CidrBlock")
    def cluster_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIpv4CidrBlock"))

    @cluster_ipv4_cidr_block.setter
    def cluster_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f7bc0d919aadf559f58aa8efd81a3a58fb8431846ef8a7032e3702ff2e8a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterSecondaryRangeName")
    def cluster_secondary_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterSecondaryRangeName"))

    @cluster_secondary_range_name.setter
    def cluster_secondary_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2f6c9e5586be1e464b3f7d1fc740ba4805e46e89c955df84a19592f5dffaeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterSecondaryRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesIpv4CidrBlock")
    def services_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicesIpv4CidrBlock"))

    @services_ipv4_cidr_block.setter
    def services_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efeec3d71e090c5061d51c8c73dc5f589e3dc5b0f0a2543a2f119558343a8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesSecondaryRangeName")
    def services_secondary_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicesSecondaryRangeName"))

    @services_secondary_range_name.setter
    def services_secondary_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcebdaae17e25824d65973c864d3d147fc1bc0199421b82a197dff7e4b7987d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesSecondaryRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useIpAliases")
    def use_ip_aliases(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useIpAliases"))

    @use_ip_aliases.setter
    def use_ip_aliases(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4bb27e1981af905a9e4bf9b70eb7a61ab65226fce9658125d60fe45937c3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIpAliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7dd1adb320136ae6b8bc6ba33c05dc821943ce3cbb94e59c2e582e7ce221afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4ca3c284df956c89d37ef491e6e6edad9553e6a185fe6694e0274e22626295a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpAllocationPolicy")
    def put_ip_allocation_policy(
        self,
        *,
        cluster_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        cluster_secondary_range_name: typing.Optional[builtins.str] = None,
        services_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        services_secondary_range_name: typing.Optional[builtins.str] = None,
        use_ip_aliases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_ipv4_cidr_block: The IP address range used to allocate IP addresses to pods in the cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cluster_ipv4_cidr_block GoogleComposerEnvironment#cluster_ipv4_cidr_block}
        :param cluster_secondary_range_name: The name of the cluster's secondary range used to allocate IP addresses to pods. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cluster_secondary_range_name GoogleComposerEnvironment#cluster_secondary_range_name}
        :param services_ipv4_cidr_block: The IP address range used to allocate IP addresses in this cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#services_ipv4_cidr_block GoogleComposerEnvironment#services_ipv4_cidr_block}
        :param services_secondary_range_name: The name of the services' secondary range used to allocate IP addresses to the cluster. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#services_secondary_range_name GoogleComposerEnvironment#services_secondary_range_name}
        :param use_ip_aliases: Whether or not to enable Alias IPs in the GKE cluster. If true, a VPC-native cluster is created. Defaults to true if the ip_allocation_policy block is present in config. This field is only supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use VPC-native GKE clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#use_ip_aliases GoogleComposerEnvironment#use_ip_aliases}
        '''
        value = GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy(
            cluster_ipv4_cidr_block=cluster_ipv4_cidr_block,
            cluster_secondary_range_name=cluster_secondary_range_name,
            services_ipv4_cidr_block=services_ipv4_cidr_block,
            services_secondary_range_name=services_secondary_range_name,
            use_ip_aliases=use_ip_aliases,
        )

        return typing.cast(None, jsii.invoke(self, "putIpAllocationPolicy", [value]))

    @jsii.member(jsii_name="resetComposerInternalIpv4CidrBlock")
    def reset_composer_internal_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComposerInternalIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetComposerNetworkAttachment")
    def reset_composer_network_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComposerNetworkAttachment", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetEnableIpMasqAgent")
    def reset_enable_ip_masq_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpMasqAgent", []))

    @jsii.member(jsii_name="resetIpAllocationPolicy")
    def reset_ip_allocation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAllocationPolicy", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMaxPodsPerNode")
    def reset_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPodsPerNode", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="ipAllocationPolicy")
    def ip_allocation_policy(
        self,
    ) -> GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference:
        return typing.cast(GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference, jsii.get(self, "ipAllocationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="composerInternalIpv4CidrBlockInput")
    def composer_internal_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "composerInternalIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="composerNetworkAttachmentInput")
    def composer_network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "composerNetworkAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpMasqAgentInput")
    def enable_ip_masq_agent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpMasqAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAllocationPolicyInput")
    def ip_allocation_policy_input(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy], jsii.get(self, "ipAllocationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="composerInternalIpv4CidrBlock")
    def composer_internal_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "composerInternalIpv4CidrBlock"))

    @composer_internal_ipv4_cidr_block.setter
    def composer_internal_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27853e5234e9f8ce836d8cf40380f0a001e65f2b71622e8e115f51b214663440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "composerInternalIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="composerNetworkAttachment")
    def composer_network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "composerNetworkAttachment"))

    @composer_network_attachment.setter
    def composer_network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca3aac71544b6c3ea03225eabaedbf6d5b84e6e7f8a50f2cc48c8858525fa64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "composerNetworkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefb4b02f89eda51330ab426e5a5be7e0a30af5fd566127e2cc0f23ad91ac81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableIpMasqAgent")
    def enable_ip_masq_agent(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpMasqAgent"))

    @enable_ip_masq_agent.setter
    def enable_ip_masq_agent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af781d6f24c4a43c85581dc848ddea6de4d537913971cb93460d369c9cf6177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpMasqAgent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3a43244a3163185852babe502be93f9c9ae024f92f1aacce0f2487e2d04871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e3395b879b62dd95517fcdc1812ea1f8b9b52890ea7e6e47086907231b60d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a57215c50b64950ec21bb7ff9ff49e045c3ee41281fd0ec74202eb167be324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7d87bceb92009eeadfbf20a0b347d07fb91edbe5d2e366e1ee2c328a67ac9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b48a20f53ce6d6f0c47171c78e88472ce5507c9bac7578133806909704afdb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92129a97323d377c0311821f9412adc6a24a45d84b35f1dbf49189a0c392c7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73667b39ee39edbfd7464911a4a27eccde7c9791cf824d55b9db454af2f44cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70649edcc81e0de3023572c5f69786fe81af539a2578e8535b839555b56aa2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigNodeConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383237ae2cd75d01b8a2c1517c73f1680014c9f5c5bc17e40c49d438f07af909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigPrivateEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_composer_connection_subnetwork": "cloudComposerConnectionSubnetwork",
        "cloud_composer_network_ipv4_cidr_block": "cloudComposerNetworkIpv4CidrBlock",
        "cloud_sql_ipv4_cidr_block": "cloudSqlIpv4CidrBlock",
        "connection_type": "connectionType",
        "enable_private_endpoint": "enablePrivateEndpoint",
        "enable_privately_used_public_ips": "enablePrivatelyUsedPublicIps",
        "master_ipv4_cidr_block": "masterIpv4CidrBlock",
        "web_server_ipv4_cidr_block": "webServerIpv4CidrBlock",
    },
)
class GoogleComposerEnvironmentConfigPrivateEnvironmentConfig:
    def __init__(
        self,
        *,
        cloud_composer_connection_subnetwork: typing.Optional[builtins.str] = None,
        cloud_composer_network_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        cloud_sql_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        connection_type: typing.Optional[builtins.str] = None,
        enable_private_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_privately_used_public_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        master_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        web_server_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_composer_connection_subnetwork: When specified, the environment will use Private Service Connect instead of VPC peerings to connect to Cloud SQL in the Tenant Project, and the PSC endpoint in the Customer Project will use an IP address from this subnetwork. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_composer_connection_subnetwork GoogleComposerEnvironment#cloud_composer_connection_subnetwork}
        :param cloud_composer_network_ipv4_cidr_block: The CIDR block from which IP range for Cloud Composer Network in tenant project will be reserved. Needs to be disjoint from private_cluster_config.master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_composer_network_ipv4_cidr_block GoogleComposerEnvironment#cloud_composer_network_ipv4_cidr_block}
        :param cloud_sql_ipv4_cidr_block: The CIDR block from which IP range in tenant project will be reserved for Cloud SQL. Needs to be disjoint from web_server_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_sql_ipv4_cidr_block GoogleComposerEnvironment#cloud_sql_ipv4_cidr_block}
        :param connection_type: Mode of internal communication within the Composer environment. Must be one of "VPC_PEERING" or "PRIVATE_SERVICE_CONNECT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#connection_type GoogleComposerEnvironment#connection_type}
        :param enable_private_endpoint: If true, access to the public endpoint of the GKE cluster is denied. If this field is set to true, ip_allocation_policy.use_ip_aliases must be set to true for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_endpoint GoogleComposerEnvironment#enable_private_endpoint}
        :param enable_privately_used_public_ips: When enabled, IPs from public (non-RFC1918) ranges can be used for ip_allocation_policy.cluster_ipv4_cidr_block and ip_allocation_policy.service_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_privately_used_public_ips GoogleComposerEnvironment#enable_privately_used_public_ips}
        :param master_ipv4_cidr_block: The IP range in CIDR notation to use for the hosted master network. This range is used for assigning internal IP addresses to the cluster master or set of masters and to the internal load balancer virtual IP. This range must not overlap with any other ranges in use within the cluster's network. If left blank, the default value of '172.16.0.0/28' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#master_ipv4_cidr_block GoogleComposerEnvironment#master_ipv4_cidr_block}
        :param web_server_ipv4_cidr_block: The CIDR block from which IP range for web server will be reserved. Needs to be disjoint from master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_ipv4_cidr_block GoogleComposerEnvironment#web_server_ipv4_cidr_block}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9768930bac1aed96af54ba0c08b00225a91eb2f3ad72ed310166ffdfeaf6575)
            check_type(argname="argument cloud_composer_connection_subnetwork", value=cloud_composer_connection_subnetwork, expected_type=type_hints["cloud_composer_connection_subnetwork"])
            check_type(argname="argument cloud_composer_network_ipv4_cidr_block", value=cloud_composer_network_ipv4_cidr_block, expected_type=type_hints["cloud_composer_network_ipv4_cidr_block"])
            check_type(argname="argument cloud_sql_ipv4_cidr_block", value=cloud_sql_ipv4_cidr_block, expected_type=type_hints["cloud_sql_ipv4_cidr_block"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument enable_private_endpoint", value=enable_private_endpoint, expected_type=type_hints["enable_private_endpoint"])
            check_type(argname="argument enable_privately_used_public_ips", value=enable_privately_used_public_ips, expected_type=type_hints["enable_privately_used_public_ips"])
            check_type(argname="argument master_ipv4_cidr_block", value=master_ipv4_cidr_block, expected_type=type_hints["master_ipv4_cidr_block"])
            check_type(argname="argument web_server_ipv4_cidr_block", value=web_server_ipv4_cidr_block, expected_type=type_hints["web_server_ipv4_cidr_block"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_composer_connection_subnetwork is not None:
            self._values["cloud_composer_connection_subnetwork"] = cloud_composer_connection_subnetwork
        if cloud_composer_network_ipv4_cidr_block is not None:
            self._values["cloud_composer_network_ipv4_cidr_block"] = cloud_composer_network_ipv4_cidr_block
        if cloud_sql_ipv4_cidr_block is not None:
            self._values["cloud_sql_ipv4_cidr_block"] = cloud_sql_ipv4_cidr_block
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if enable_private_endpoint is not None:
            self._values["enable_private_endpoint"] = enable_private_endpoint
        if enable_privately_used_public_ips is not None:
            self._values["enable_privately_used_public_ips"] = enable_privately_used_public_ips
        if master_ipv4_cidr_block is not None:
            self._values["master_ipv4_cidr_block"] = master_ipv4_cidr_block
        if web_server_ipv4_cidr_block is not None:
            self._values["web_server_ipv4_cidr_block"] = web_server_ipv4_cidr_block

    @builtins.property
    def cloud_composer_connection_subnetwork(self) -> typing.Optional[builtins.str]:
        '''When specified, the environment will use Private Service Connect instead of VPC peerings to connect to Cloud SQL in the Tenant Project, and the PSC endpoint in the Customer Project will use an IP address from this subnetwork.

        This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_composer_connection_subnetwork GoogleComposerEnvironment#cloud_composer_connection_subnetwork}
        '''
        result = self._values.get("cloud_composer_connection_subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_composer_network_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The CIDR block from which IP range for Cloud Composer Network in tenant project will be reserved.

        Needs to be disjoint from private_cluster_config.master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_composer_network_ipv4_cidr_block GoogleComposerEnvironment#cloud_composer_network_ipv4_cidr_block}
        '''
        result = self._values.get("cloud_composer_network_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_sql_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The CIDR block from which IP range in tenant project will be reserved for Cloud SQL.

        Needs to be disjoint from web_server_ipv4_cidr_block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_sql_ipv4_cidr_block GoogleComposerEnvironment#cloud_sql_ipv4_cidr_block}
        '''
        result = self._values.get("cloud_sql_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''Mode of internal communication within the Composer environment. Must be one of "VPC_PEERING" or "PRIVATE_SERVICE_CONNECT".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#connection_type GoogleComposerEnvironment#connection_type}
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_private_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, access to the public endpoint of the GKE cluster is denied.

        If this field is set to true, ip_allocation_policy.use_ip_aliases must be set to true for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_private_endpoint GoogleComposerEnvironment#enable_private_endpoint}
        '''
        result = self._values.get("enable_private_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_privately_used_public_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, IPs from public (non-RFC1918) ranges can be used for ip_allocation_policy.cluster_ipv4_cidr_block and ip_allocation_policy.service_ipv4_cidr_block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enable_privately_used_public_ips GoogleComposerEnvironment#enable_privately_used_public_ips}
        '''
        result = self._values.get("enable_privately_used_public_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def master_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP range in CIDR notation to use for the hosted master network.

        This range is used for assigning internal IP addresses to the cluster master or set of masters and to the internal load balancer virtual IP. This range must not overlap with any other ranges in use within the cluster's network. If left blank, the default value of '172.16.0.0/28' is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#master_ipv4_cidr_block GoogleComposerEnvironment#master_ipv4_cidr_block}
        '''
        result = self._values.get("master_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_server_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The CIDR block from which IP range for web server will be reserved.

        Needs to be disjoint from master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_ipv4_cidr_block GoogleComposerEnvironment#web_server_ipv4_cidr_block}
        '''
        result = self._values.get("web_server_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigPrivateEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9d0029b59f9b2d7e5a3aa284c3c1cf6497f97eb03d7f7e52b65fb1d21937df7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudComposerConnectionSubnetwork")
    def reset_cloud_composer_connection_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudComposerConnectionSubnetwork", []))

    @jsii.member(jsii_name="resetCloudComposerNetworkIpv4CidrBlock")
    def reset_cloud_composer_network_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudComposerNetworkIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetCloudSqlIpv4CidrBlock")
    def reset_cloud_sql_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetConnectionType")
    def reset_connection_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionType", []))

    @jsii.member(jsii_name="resetEnablePrivateEndpoint")
    def reset_enable_private_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePrivateEndpoint", []))

    @jsii.member(jsii_name="resetEnablePrivatelyUsedPublicIps")
    def reset_enable_privately_used_public_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePrivatelyUsedPublicIps", []))

    @jsii.member(jsii_name="resetMasterIpv4CidrBlock")
    def reset_master_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterIpv4CidrBlock", []))

    @jsii.member(jsii_name="resetWebServerIpv4CidrBlock")
    def reset_web_server_ipv4_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebServerIpv4CidrBlock", []))

    @builtins.property
    @jsii.member(jsii_name="cloudComposerConnectionSubnetworkInput")
    def cloud_composer_connection_subnetwork_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudComposerConnectionSubnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudComposerNetworkIpv4CidrBlockInput")
    def cloud_composer_network_ipv4_cidr_block_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudComposerNetworkIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlIpv4CidrBlockInput")
    def cloud_sql_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSqlIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionTypeInput")
    def connection_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateEndpointInput")
    def enable_private_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivateEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivatelyUsedPublicIpsInput")
    def enable_privately_used_public_ips_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivatelyUsedPublicIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="masterIpv4CidrBlockInput")
    def master_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerIpv4CidrBlockInput")
    def web_server_ipv4_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webServerIpv4CidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudComposerConnectionSubnetwork")
    def cloud_composer_connection_subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudComposerConnectionSubnetwork"))

    @cloud_composer_connection_subnetwork.setter
    def cloud_composer_connection_subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad42dc9e959abfe3a7ff006be9c4348f893555781d2e39a59e33fe9ae375e89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudComposerConnectionSubnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudComposerNetworkIpv4CidrBlock")
    def cloud_composer_network_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudComposerNetworkIpv4CidrBlock"))

    @cloud_composer_network_ipv4_cidr_block.setter
    def cloud_composer_network_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264826a6a43afda101087df0de956c94f5379c535711e4590945ded20d5fbb58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudComposerNetworkIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudSqlIpv4CidrBlock")
    def cloud_sql_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlIpv4CidrBlock"))

    @cloud_sql_ipv4_cidr_block.setter
    def cloud_sql_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38bbc66efb44e4751132e7345c7a1bf0eed6d9ee1e55d8ce5f9fae7768c8f6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionType"))

    @connection_type.setter
    def connection_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c6b17c8abbb6c7de9c56c01c8915c957f504daa55003db602ee7f44423284a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePrivateEndpoint")
    def enable_private_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivateEndpoint"))

    @enable_private_endpoint.setter
    def enable_private_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dd443872893672521ce3698c1668388188f33bd52c43a7fbf0e0aa525dec86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePrivatelyUsedPublicIps")
    def enable_privately_used_public_ips(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivatelyUsedPublicIps"))

    @enable_privately_used_public_ips.setter
    def enable_privately_used_public_ips(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f63c0965102bab5a7bdf0975b15aeea6ee80e91024c980a9256b4ca3672e181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivatelyUsedPublicIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterIpv4CidrBlock")
    def master_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterIpv4CidrBlock"))

    @master_ipv4_cidr_block.setter
    def master_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdcfaab689a5211b329d8a75c2fa642859f7ffc401a66cd457311b049ac78c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webServerIpv4CidrBlock")
    def web_server_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webServerIpv4CidrBlock"))

    @web_server_ipv4_cidr_block.setter
    def web_server_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da203bf206b86a0b5584d0ed0fc0456418abfb82f1c104783d8aa22ebd23167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webServerIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigPrivateEnvironmentConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigPrivateEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigPrivateEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579db399d2ec1f8b6f1a910f4dca13c7b2e473489c49434455070747ac212e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigRecoveryConfig",
    jsii_struct_bases=[],
    name_mapping={"scheduled_snapshots_config": "scheduledSnapshotsConfig"},
)
class GoogleComposerEnvironmentConfigRecoveryConfig:
    def __init__(
        self,
        *,
        scheduled_snapshots_config: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled_snapshots_config: scheduled_snapshots_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduled_snapshots_config GoogleComposerEnvironment#scheduled_snapshots_config}
        '''
        if isinstance(scheduled_snapshots_config, dict):
            scheduled_snapshots_config = GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(**scheduled_snapshots_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0e57783e3ea41e2b6a0e8dc3bac11f124a14dde02c2c3f6711ed43ef5e1de0)
            check_type(argname="argument scheduled_snapshots_config", value=scheduled_snapshots_config, expected_type=type_hints["scheduled_snapshots_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scheduled_snapshots_config is not None:
            self._values["scheduled_snapshots_config"] = scheduled_snapshots_config

    @builtins.property
    def scheduled_snapshots_config(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"]:
        '''scheduled_snapshots_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduled_snapshots_config GoogleComposerEnvironment#scheduled_snapshots_config}
        '''
        result = self._values.get("scheduled_snapshots_config")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigRecoveryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigRecoveryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigRecoveryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d2a31bdc36491afbc1ea49ac5598e8ff64a04dd64f633b6584de2cbd3edff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScheduledSnapshotsConfig")
    def put_scheduled_snapshots_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        snapshot_creation_schedule: typing.Optional[builtins.str] = None,
        snapshot_location: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: When enabled, Cloud Composer periodically saves snapshots of your environment to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        :param snapshot_creation_schedule: Snapshot schedule, in the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#snapshot_creation_schedule GoogleComposerEnvironment#snapshot_creation_schedule}
        :param snapshot_location: the URI of a bucket folder where to save the snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#snapshot_location GoogleComposerEnvironment#snapshot_location}
        :param time_zone: A time zone for the schedule. This value is a time offset and does not take into account daylight saving time changes. Valid values are from UTC-12 to UTC+12. Examples: UTC, UTC-01, UTC+03. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#time_zone GoogleComposerEnvironment#time_zone}
        '''
        value = GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(
            enabled=enabled,
            snapshot_creation_schedule=snapshot_creation_schedule,
            snapshot_location=snapshot_location,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduledSnapshotsConfig", [value]))

    @jsii.member(jsii_name="resetScheduledSnapshotsConfig")
    def reset_scheduled_snapshots_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledSnapshotsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="scheduledSnapshotsConfig")
    def scheduled_snapshots_config(
        self,
    ) -> "GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference", jsii.get(self, "scheduledSnapshotsConfig"))

    @builtins.property
    @jsii.member(jsii_name="scheduledSnapshotsConfigInput")
    def scheduled_snapshots_config_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"], jsii.get(self, "scheduledSnapshotsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2a3a4ca26c5ffcbb6555e528e900776998752b8b2ffd073d7efae32f39711e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "snapshot_creation_schedule": "snapshotCreationSchedule",
        "snapshot_location": "snapshotLocation",
        "time_zone": "timeZone",
    },
)
class GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        snapshot_creation_schedule: typing.Optional[builtins.str] = None,
        snapshot_location: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: When enabled, Cloud Composer periodically saves snapshots of your environment to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        :param snapshot_creation_schedule: Snapshot schedule, in the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#snapshot_creation_schedule GoogleComposerEnvironment#snapshot_creation_schedule}
        :param snapshot_location: the URI of a bucket folder where to save the snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#snapshot_location GoogleComposerEnvironment#snapshot_location}
        :param time_zone: A time zone for the schedule. This value is a time offset and does not take into account daylight saving time changes. Valid values are from UTC-12 to UTC+12. Examples: UTC, UTC-01, UTC+03. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#time_zone GoogleComposerEnvironment#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97aa5d483c432d41282ff929ab18374df4a0ec23cf60544c8dde5e4db3a15493)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument snapshot_creation_schedule", value=snapshot_creation_schedule, expected_type=type_hints["snapshot_creation_schedule"])
            check_type(argname="argument snapshot_location", value=snapshot_location, expected_type=type_hints["snapshot_location"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if snapshot_creation_schedule is not None:
            self._values["snapshot_creation_schedule"] = snapshot_creation_schedule
        if snapshot_location is not None:
            self._values["snapshot_location"] = snapshot_location
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''When enabled, Cloud Composer periodically saves snapshots of your environment to a Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def snapshot_creation_schedule(self) -> typing.Optional[builtins.str]:
        '''Snapshot schedule, in the unix-cron format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#snapshot_creation_schedule GoogleComposerEnvironment#snapshot_creation_schedule}
        '''
        result = self._values.get("snapshot_creation_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_location(self) -> typing.Optional[builtins.str]:
        '''the URI of a bucket folder where to save the snapshot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#snapshot_location GoogleComposerEnvironment#snapshot_location}
        '''
        result = self._values.get("snapshot_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''A time zone for the schedule.

        This value is a time offset and does not take into account daylight saving time changes. Valid values are from UTC-12 to UTC+12. Examples: UTC, UTC-01, UTC+03.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#time_zone GoogleComposerEnvironment#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5b3c0984c1b47b462465f280d5a6bf61693be3e1cab7164adf0c082068838eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSnapshotCreationSchedule")
    def reset_snapshot_creation_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotCreationSchedule", []))

    @jsii.member(jsii_name="resetSnapshotLocation")
    def reset_snapshot_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotLocation", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotCreationScheduleInput")
    def snapshot_creation_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotCreationScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotLocationInput")
    def snapshot_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f417749b64cf08e985d4808b09babdca7bdad69bfca3318a2a1d65573a83f9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotCreationSchedule")
    def snapshot_creation_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotCreationSchedule"))

    @snapshot_creation_schedule.setter
    def snapshot_creation_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59beabb540ece0a3ef0e7c0c3180dfb588b7ab359216355cab6b96e59958186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotCreationSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotLocation")
    def snapshot_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotLocation"))

    @snapshot_location.setter
    def snapshot_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328f1cddca1215de9007d03879171b61ceb7a24b59b4295b03a79c4b3fede07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4ac64297b6081c070bcb8c1c9af41964d53bf433376d0d4a8ce0cfdcaeaa49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66e75f5158c1c904d9036d2dcf442eb79960840c35141c3c2b31d5c5756031c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_config_overrides": "airflowConfigOverrides",
        "cloud_data_lineage_integration": "cloudDataLineageIntegration",
        "env_variables": "envVariables",
        "image_version": "imageVersion",
        "pypi_packages": "pypiPackages",
        "python_version": "pythonVersion",
        "scheduler_count": "schedulerCount",
        "web_server_plugins_mode": "webServerPluginsMode",
    },
)
class GoogleComposerEnvironmentConfigSoftwareConfig:
    def __init__(
        self,
        *,
        airflow_config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_data_lineage_integration: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_version: typing.Optional[builtins.str] = None,
        pypi_packages: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_version: typing.Optional[builtins.str] = None,
        scheduler_count: typing.Optional[jsii.Number] = None,
        web_server_plugins_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param airflow_config_overrides: Apache Airflow configuration properties to override. Property keys contain the section and property names, separated by a hyphen, for example "core-dags_are_paused_at_creation". Section names must not contain hyphens ("-"), opening square brackets ("["), or closing square brackets ("]"). The property name must not be empty and cannot contain "=" or ";". Section and property names cannot contain characters: "." Apache Airflow configuration property names must be written in snake_case. Property values can contain any character, and can be written in any lower/upper case format. Certain Apache Airflow configuration property values are blacklisted, and cannot be overridden. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#airflow_config_overrides GoogleComposerEnvironment#airflow_config_overrides}
        :param cloud_data_lineage_integration: cloud_data_lineage_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_data_lineage_integration GoogleComposerEnvironment#cloud_data_lineage_integration}
        :param env_variables: Additional environment variables to provide to the Apache Airflow scheduler, worker, and webserver processes. Environment variable names must match the regular expression [a-zA-Z_][a-zA-Z0-9_]*. They cannot specify Apache Airflow software configuration overrides (they cannot match the regular expression AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+), and they cannot match any of the following reserved names: AIRFLOW_HOME C_FORCE_ROOT CONTAINER_NAME DAGS_FOLDER GCP_PROJECT GCS_BUCKET GKE_CLUSTER_NAME SQL_DATABASE SQL_INSTANCE SQL_PASSWORD SQL_PROJECT SQL_REGION SQL_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#env_variables GoogleComposerEnvironment#env_variables}
        :param image_version: The version of the software running in the environment. This encapsulates both the version of Cloud Composer functionality and the version of Apache Airflow. It must match the regular expression composer-([0-9]+(.[0-9]+.[0-9]+(-preview.[0-9]+)?)?|latest)-airflow-([0-9]+(.[0-9]+(.[0-9]+)?)?). The Cloud Composer portion of the image version is a full semantic version, or an alias in the form of major version number or 'latest'. The Apache Airflow portion of the image version is a full semantic version that points to one of the supported Apache Airflow versions, or an alias in the form of only major or major.minor versions specified. See documentation for more details and version list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#image_version GoogleComposerEnvironment#image_version}
        :param pypi_packages: Custom Python Package Index (PyPI) packages to be installed in the environment. Keys refer to the lowercase package name (e.g. "numpy"). Values are the lowercase extras and version specifier (e.g. "==1.12.0", "[devel,gcp_api]", "[devel]>=1.8.2, <1.9.2"). To specify a package without pinning it to a version specifier, use the empty string as the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#pypi_packages GoogleComposerEnvironment#pypi_packages}
        :param python_version: The major version of Python used to run the Apache Airflow scheduler, worker, and webserver processes. Can be set to '2' or '3'. If not specified, the default is '2'. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use Python major version 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#python_version GoogleComposerEnvironment#python_version}
        :param scheduler_count: The number of schedulers for Airflow. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-2.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduler_count GoogleComposerEnvironment#scheduler_count}
        :param web_server_plugins_mode: Should be either 'ENABLED' or 'DISABLED'. Defaults to 'ENABLED'. Used in Composer 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_plugins_mode GoogleComposerEnvironment#web_server_plugins_mode}
        '''
        if isinstance(cloud_data_lineage_integration, dict):
            cloud_data_lineage_integration = GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration(**cloud_data_lineage_integration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bda64ee99d5d72be623fa48913427a8f6a3e0c11aae5033405c6064e9e35162)
            check_type(argname="argument airflow_config_overrides", value=airflow_config_overrides, expected_type=type_hints["airflow_config_overrides"])
            check_type(argname="argument cloud_data_lineage_integration", value=cloud_data_lineage_integration, expected_type=type_hints["cloud_data_lineage_integration"])
            check_type(argname="argument env_variables", value=env_variables, expected_type=type_hints["env_variables"])
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument pypi_packages", value=pypi_packages, expected_type=type_hints["pypi_packages"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument scheduler_count", value=scheduler_count, expected_type=type_hints["scheduler_count"])
            check_type(argname="argument web_server_plugins_mode", value=web_server_plugins_mode, expected_type=type_hints["web_server_plugins_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if airflow_config_overrides is not None:
            self._values["airflow_config_overrides"] = airflow_config_overrides
        if cloud_data_lineage_integration is not None:
            self._values["cloud_data_lineage_integration"] = cloud_data_lineage_integration
        if env_variables is not None:
            self._values["env_variables"] = env_variables
        if image_version is not None:
            self._values["image_version"] = image_version
        if pypi_packages is not None:
            self._values["pypi_packages"] = pypi_packages
        if python_version is not None:
            self._values["python_version"] = python_version
        if scheduler_count is not None:
            self._values["scheduler_count"] = scheduler_count
        if web_server_plugins_mode is not None:
            self._values["web_server_plugins_mode"] = web_server_plugins_mode

    @builtins.property
    def airflow_config_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Apache Airflow configuration properties to override.

        Property keys contain the section and property names, separated by a hyphen, for example "core-dags_are_paused_at_creation". Section names must not contain hyphens ("-"), opening square brackets ("["), or closing square brackets ("]"). The property name must not be empty and cannot contain "=" or ";". Section and property names cannot contain characters: "." Apache Airflow configuration property names must be written in snake_case. Property values can contain any character, and can be written in any lower/upper case format. Certain Apache Airflow configuration property values are blacklisted, and cannot be overridden.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#airflow_config_overrides GoogleComposerEnvironment#airflow_config_overrides}
        '''
        result = self._values.get("airflow_config_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cloud_data_lineage_integration(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration"]:
        '''cloud_data_lineage_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cloud_data_lineage_integration GoogleComposerEnvironment#cloud_data_lineage_integration}
        '''
        result = self._values.get("cloud_data_lineage_integration")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration"], result)

    @builtins.property
    def env_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional environment variables to provide to the Apache Airflow scheduler, worker, and webserver processes.

        Environment variable names must match the regular expression [a-zA-Z_][a-zA-Z0-9_]*. They cannot specify Apache Airflow software configuration overrides (they cannot match the regular expression AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+), and they cannot match any of the following reserved names: AIRFLOW_HOME C_FORCE_ROOT CONTAINER_NAME DAGS_FOLDER GCP_PROJECT GCS_BUCKET GKE_CLUSTER_NAME SQL_DATABASE SQL_INSTANCE SQL_PASSWORD SQL_PROJECT SQL_REGION SQL_USER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#env_variables GoogleComposerEnvironment#env_variables}
        '''
        result = self._values.get("env_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''The version of the software running in the environment.

        This encapsulates both the version of Cloud Composer functionality and the version of Apache Airflow. It must match the regular expression composer-([0-9]+(.[0-9]+.[0-9]+(-preview.[0-9]+)?)?|latest)-airflow-([0-9]+(.[0-9]+(.[0-9]+)?)?). The Cloud Composer portion of the image version is a full semantic version, or an alias in the form of major version number or 'latest'. The Apache Airflow portion of the image version is a full semantic version that points to one of the supported Apache Airflow versions, or an alias in the form of only major or major.minor versions specified. See documentation for more details and version list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#image_version GoogleComposerEnvironment#image_version}
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pypi_packages(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom Python Package Index (PyPI) packages to be installed in the environment.

        Keys refer to the lowercase package name (e.g. "numpy"). Values are the lowercase extras and version specifier (e.g. "==1.12.0", "[devel,gcp_api]", "[devel]>=1.8.2, <1.9.2"). To specify a package without pinning it to a version specifier, use the empty string as the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#pypi_packages GoogleComposerEnvironment#pypi_packages}
        '''
        result = self._values.get("pypi_packages")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_version(self) -> typing.Optional[builtins.str]:
        '''The major version of Python used to run the Apache Airflow scheduler, worker, and webserver processes.

        Can be set to '2' or '3'. If not specified, the default is '2'. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use Python major version 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#python_version GoogleComposerEnvironment#python_version}
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduler_count(self) -> typing.Optional[jsii.Number]:
        '''The number of schedulers for Airflow. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-2.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduler_count GoogleComposerEnvironment#scheduler_count}
        '''
        result = self._values.get("scheduler_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def web_server_plugins_mode(self) -> typing.Optional[builtins.str]:
        '''Should be either 'ENABLED' or 'DISABLED'. Defaults to 'ENABLED'. Used in Composer 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server_plugins_mode GoogleComposerEnvironment#web_server_plugins_mode}
        '''
        result = self._values.get("web_server_plugins_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not Cloud Data Lineage integration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb6b5b8a335445644063b09eb40e1e50b71b29d1d4c8e9fdd3944cb0cede626)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not Cloud Data Lineage integration is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d14ec609433ad7146cfc4c522e52028b3d3c7104b44c60c05785acafb6d6ba1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__905bf1659cba86316584733c64e472f151a89010e09f3f6d04d8f0f92d4ea160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bbfee5a76c2f296b81ce25671977952f2d53e4b7af29ccef606100f23556e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b554a8a028b463e2325aa88e8404917cc4a69995e42a824e81a904b2c1557184)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudDataLineageIntegration")
    def put_cloud_data_lineage_integration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not Cloud Data Lineage integration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#enabled GoogleComposerEnvironment#enabled}
        '''
        value = GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putCloudDataLineageIntegration", [value]))

    @jsii.member(jsii_name="resetAirflowConfigOverrides")
    def reset_airflow_config_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAirflowConfigOverrides", []))

    @jsii.member(jsii_name="resetCloudDataLineageIntegration")
    def reset_cloud_data_lineage_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudDataLineageIntegration", []))

    @jsii.member(jsii_name="resetEnvVariables")
    def reset_env_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvVariables", []))

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetPypiPackages")
    def reset_pypi_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPypiPackages", []))

    @jsii.member(jsii_name="resetPythonVersion")
    def reset_python_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonVersion", []))

    @jsii.member(jsii_name="resetSchedulerCount")
    def reset_scheduler_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulerCount", []))

    @jsii.member(jsii_name="resetWebServerPluginsMode")
    def reset_web_server_plugins_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebServerPluginsMode", []))

    @builtins.property
    @jsii.member(jsii_name="cloudDataLineageIntegration")
    def cloud_data_lineage_integration(
        self,
    ) -> GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference:
        return typing.cast(GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference, jsii.get(self, "cloudDataLineageIntegration"))

    @builtins.property
    @jsii.member(jsii_name="airflowConfigOverridesInput")
    def airflow_config_overrides_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "airflowConfigOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudDataLineageIntegrationInput")
    def cloud_data_lineage_integration_input(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration], jsii.get(self, "cloudDataLineageIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="envVariablesInput")
    def env_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="pypiPackagesInput")
    def pypi_packages_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "pypiPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonVersionInput")
    def python_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerCountInput")
    def scheduler_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerPluginsModeInput")
    def web_server_plugins_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webServerPluginsModeInput"))

    @builtins.property
    @jsii.member(jsii_name="airflowConfigOverrides")
    def airflow_config_overrides(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "airflowConfigOverrides"))

    @airflow_config_overrides.setter
    def airflow_config_overrides(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8aeaa95d656c0583d40d85faaf269ab17054ffb1ecce5bde80806cf704ec2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "airflowConfigOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envVariables")
    def env_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVariables"))

    @env_variables.setter
    def env_variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d04436791b9592c966b256bc4b038840277388dfd376a9e12e3c34fa2c2938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639e60dc4d3043740c7e9fa9d236fb316c523d371cd6b3eb787bf3dda7e2cb8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pypiPackages")
    def pypi_packages(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "pypiPackages"))

    @pypi_packages.setter
    def pypi_packages(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ee1bc00a90fc34bf22b844de2ab929fef45f65ef6bf5ff68c28316ea9d6671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pypiPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonVersion")
    def python_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonVersion"))

    @python_version.setter
    def python_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ed08c07972f59a9ed97a44738d93a6f53f9440087802a1eecfa1adf93d4a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulerCount")
    def scheduler_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "schedulerCount"))

    @scheduler_count.setter
    def scheduler_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49dad3233e94559cd3ebe57f615901fd205b58e622764f23feb15cb3a27e0361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webServerPluginsMode")
    def web_server_plugins_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webServerPluginsMode"))

    @web_server_plugins_mode.setter
    def web_server_plugins_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51072f0e45fe28a6a59a3a6e322b0c1cc61c9e1248f29df417749ecdb15b7b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webServerPluginsMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba579262f69349404edaaac91b0d9667c42e2f0dda590929f5eeb3bc1a0bf4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerConfig",
    jsii_struct_bases=[],
    name_mapping={"machine_type": "machineType"},
)
class GoogleComposerEnvironmentConfigWebServerConfig:
    def __init__(self, *, machine_type: builtins.str) -> None:
        '''
        :param machine_type: Optional. Machine type on which Airflow web server is running. It has to be one of: composer-n1-webserver-2, composer-n1-webserver-4 or composer-n1-webserver-8. If not specified, composer-n1-webserver-2 will be used. Value custom is returned only in response, if Airflow web server parameters were manually changed to a non-standard values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05541bb52233791b51bdddf3c67f60436afeb2b1fc14c6d123da1f409ab46b59)
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_type": machine_type,
        }

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''Optional.

        Machine type on which Airflow web server is running. It has to be one of: composer-n1-webserver-2, composer-n1-webserver-4 or composer-n1-webserver-8. If not specified, composer-n1-webserver-2 will be used. Value custom is returned only in response, if Airflow web server parameters were manually changed to a non-standard values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#machine_type GoogleComposerEnvironment#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWebServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWebServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31bf4a216589016a97267bdc03185270a9715db2c7fd7ee7d397fea49b864ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e4434446ff7ada56559ca6438c195892e3c5443f071194dbc74387218bb065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWebServerConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWebServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWebServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386c4e4843f65d533e8da197af385bbde1c859e6eb9bb618d968ac940a06b206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerNetworkAccessControl",
    jsii_struct_bases=[],
    name_mapping={"allowed_ip_range": "allowedIpRange"},
)
class GoogleComposerEnvironmentConfigWebServerNetworkAccessControl:
    def __init__(
        self,
        *,
        allowed_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_ip_range: allowed_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#allowed_ip_range GoogleComposerEnvironment#allowed_ip_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1630e5f6ae74a9e4c62acd8331dac3c7a7df47baebe7a248f663043195e3196b)
            check_type(argname="argument allowed_ip_range", value=allowed_ip_range, expected_type=type_hints["allowed_ip_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_ip_range is not None:
            self._values["allowed_ip_range"] = allowed_ip_range

    @builtins.property
    def allowed_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange"]]]:
        '''allowed_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#allowed_ip_range GoogleComposerEnvironment#allowed_ip_range}
        '''
        result = self._values.get("allowed_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWebServerNetworkAccessControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "description": "description"},
)
class GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange:
    def __init__(
        self,
        *,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: IP address or range, defined using CIDR notation, of requests that this rule applies to. Examples: 192.168.1.1 or 192.168.0.0/16 or 2001:db8::/32 or 2001:0db8:0000:0042:0000:8a2e:0370:7334. IP range prefixes should be properly truncated. For example, 1.2.3.4/24 should be truncated to 1.2.3.0/24. Similarly, for IPv6, 2001:db8::1/32 should be truncated to 2001:db8::/32. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#value GoogleComposerEnvironment#value}
        :param description: A description of this ip range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#description GoogleComposerEnvironment#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcb90db58d54caba979a864681a3d78f6d2a2d09fc2ce8f56460196f5ea7256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def value(self) -> builtins.str:
        '''IP address or range, defined using CIDR notation, of requests that this rule applies to.

        Examples: 192.168.1.1 or 192.168.0.0/16 or 2001:db8::/32 or 2001:0db8:0000:0042:0000:8a2e:0370:7334. IP range prefixes should be properly truncated. For example, 1.2.3.4/24 should be truncated to 1.2.3.0/24. Similarly, for IPv6, 2001:db8::1/32 should be truncated to 2001:db8::/32.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#value GoogleComposerEnvironment#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this ip range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#description GoogleComposerEnvironment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dab59b32b95c33cfef3d85043beee05a854fbf2b8a8f8f097f63d9473843146f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb1b7cbca311d14bd855f9a586832cfb14d09695931e40bb883601ae5e8307d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1673291bce56d4d5fb655ffb22a5107e43839310cb03026f08a88232b9a8055)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4bc688ffaa58df3097fd138cdec205ab6506dfe4e530bec35877825266caf9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7028d625e2f6e2d3c06381c9303d4f671bdeeb9f9f22eaac75005003b549255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b063811d8130f7be467998994988316e90692c6b16166ca8c55bd645f529963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cac05697c32f33852258a2aaf7b1910a3595fa8d40f526ae8ae1c778512ede57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18174ab3e31cb83b3466d6980c215c163d2f43929021a99679ee778cb9fe9e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8b3e57394bd95fa3b22d02ba9f9005daf0bbdada4900cca2d813c10ee368b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2662ded4bb311cf40ca54cfc27eb8e7a2a40685839a42bcefe670d47103845b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0cdc285935a7b6d74b1f8681c0d1fd98cc8705a8d5a6d04208fc174bfed627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedIpRange")
    def put_allowed_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192508e51d54c7b216556a80b702dc0b725bb320c7a3166805f200b6b943574f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedIpRange", [value]))

    @jsii.member(jsii_name="resetAllowedIpRange")
    def reset_allowed_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIpRange", []))

    @builtins.property
    @jsii.member(jsii_name="allowedIpRange")
    def allowed_ip_range(
        self,
    ) -> GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList:
        return typing.cast(GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList, jsii.get(self, "allowedIpRange"))

    @builtins.property
    @jsii.member(jsii_name="allowedIpRangeInput")
    def allowed_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]], jsii.get(self, "allowedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWebServerNetworkAccessControl]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWebServerNetworkAccessControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWebServerNetworkAccessControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd51a5364a6aa5052a0b9a90558a1b6e43f4552f136d13ca43021afeeb31994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dag_processor": "dagProcessor",
        "scheduler": "scheduler",
        "triggerer": "triggerer",
        "web_server": "webServer",
        "worker": "worker",
    },
)
class GoogleComposerEnvironmentConfigWorkloadsConfig:
    def __init__(
        self,
        *,
        dag_processor: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigScheduler", typing.Dict[builtins.str, typing.Any]]] = None,
        triggerer: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigWebServer", typing.Dict[builtins.str, typing.Any]]] = None,
        worker: typing.Optional[typing.Union["GoogleComposerEnvironmentConfigWorkloadsConfigWorker", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dag_processor: dag_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#dag_processor GoogleComposerEnvironment#dag_processor}
        :param scheduler: scheduler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduler GoogleComposerEnvironment#scheduler}
        :param triggerer: triggerer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#triggerer GoogleComposerEnvironment#triggerer}
        :param web_server: web_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server GoogleComposerEnvironment#web_server}
        :param worker: worker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#worker GoogleComposerEnvironment#worker}
        '''
        if isinstance(dag_processor, dict):
            dag_processor = GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor(**dag_processor)
        if isinstance(scheduler, dict):
            scheduler = GoogleComposerEnvironmentConfigWorkloadsConfigScheduler(**scheduler)
        if isinstance(triggerer, dict):
            triggerer = GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer(**triggerer)
        if isinstance(web_server, dict):
            web_server = GoogleComposerEnvironmentConfigWorkloadsConfigWebServer(**web_server)
        if isinstance(worker, dict):
            worker = GoogleComposerEnvironmentConfigWorkloadsConfigWorker(**worker)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a170f72e4813e5916f0dcf16148cef086c29eae98cd086500ac47d64e676d2)
            check_type(argname="argument dag_processor", value=dag_processor, expected_type=type_hints["dag_processor"])
            check_type(argname="argument scheduler", value=scheduler, expected_type=type_hints["scheduler"])
            check_type(argname="argument triggerer", value=triggerer, expected_type=type_hints["triggerer"])
            check_type(argname="argument web_server", value=web_server, expected_type=type_hints["web_server"])
            check_type(argname="argument worker", value=worker, expected_type=type_hints["worker"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dag_processor is not None:
            self._values["dag_processor"] = dag_processor
        if scheduler is not None:
            self._values["scheduler"] = scheduler
        if triggerer is not None:
            self._values["triggerer"] = triggerer
        if web_server is not None:
            self._values["web_server"] = web_server
        if worker is not None:
            self._values["worker"] = worker

    @builtins.property
    def dag_processor(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor"]:
        '''dag_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#dag_processor GoogleComposerEnvironment#dag_processor}
        '''
        result = self._values.get("dag_processor")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor"], result)

    @builtins.property
    def scheduler(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigScheduler"]:
        '''scheduler block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#scheduler GoogleComposerEnvironment#scheduler}
        '''
        result = self._values.get("scheduler")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigScheduler"], result)

    @builtins.property
    def triggerer(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer"]:
        '''triggerer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#triggerer GoogleComposerEnvironment#triggerer}
        '''
        result = self._values.get("triggerer")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer"], result)

    @builtins.property
    def web_server(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWebServer"]:
        '''web_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#web_server GoogleComposerEnvironment#web_server}
        '''
        result = self._values.get("web_server")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWebServer"], result)

    @builtins.property
    def worker(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWorker"]:
        '''worker block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#worker GoogleComposerEnvironment#worker}
        '''
        result = self._values.get("worker")
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWorker"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWorkloadsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "cpu": "cpu",
        "memory_gb": "memoryGb",
        "storage_gb": "storageGb",
    },
)
class GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of DAG processors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        :param cpu: CPU request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128e8cc5c4258b2da5ae1c83e9e6d561830243048a744291733b13082448ac07)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_gb", value=memory_gb, expected_type=type_hints["memory_gb"])
            check_type(argname="argument storage_gb", value=storage_gb, expected_type=type_hints["storage_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_gb is not None:
            self._values["memory_gb"] = memory_gb
        if storage_gb is not None:
            self._values["storage_gb"] = storage_gb

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of DAG processors.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''CPU request and limit for DAG processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for DAG processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for DAG processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e9271dac78fef9c9fe8f5f648c2f91011894f4cce8298df5beeaf013ea30d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemoryGb")
    def reset_memory_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGb", []))

    @jsii.member(jsii_name="resetStorageGb")
    def reset_storage_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageGb", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGbInput")
    def memory_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGbInput"))

    @builtins.property
    @jsii.member(jsii_name="storageGbInput")
    def storage_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageGbInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a853d1caf67e2c4e3d1e59fc842ffbdb3e8058cc2473b8f8a4c39a3ac090ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11693cdcbaf3a7eaa1c4cd5c02d53933972423fc5f11ca634e51e3f92da58eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c7383aadf9ceeeded954f8f6f8b17e443559ac854c79dd1f82cb90eea28b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac82875ad881a576fd9eaf36bef31918fb704f9516d771db412458f4a1e11c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa73d4ee01dffff95992623ae18ae28205d34412afcaf4146d6dca9cfb9107d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComposerEnvironmentConfigWorkloadsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69819d33757b8121a96ecf7c1720d35a2a5457b6269899b189c0c3cfdf0e1ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDagProcessor")
    def put_dag_processor(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of DAG processors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        :param cpu: CPU request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        value = GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor(
            count=count, cpu=cpu, memory_gb=memory_gb, storage_gb=storage_gb
        )

        return typing.cast(None, jsii.invoke(self, "putDagProcessor", [value]))

    @jsii.member(jsii_name="putScheduler")
    def put_scheduler(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The number of schedulers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        value = GoogleComposerEnvironmentConfigWorkloadsConfigScheduler(
            count=count, cpu=cpu, memory_gb=memory_gb, storage_gb=storage_gb
        )

        return typing.cast(None, jsii.invoke(self, "putScheduler", [value]))

    @jsii.member(jsii_name="putTriggerer")
    def put_triggerer(
        self,
        *,
        count: jsii.Number,
        cpu: jsii.Number,
        memory_gb: jsii.Number,
    ) -> None:
        '''
        :param count: The number of triggerers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        value = GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer(
            count=count, cpu=cpu, memory_gb=memory_gb
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerer", [value]))

    @jsii.member(jsii_name="putWebServer")
    def put_web_server(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu: CPU request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        value = GoogleComposerEnvironmentConfigWorkloadsConfigWebServer(
            cpu=cpu, memory_gb=memory_gb, storage_gb=storage_gb
        )

        return typing.cast(None, jsii.invoke(self, "putWebServer", [value]))

    @jsii.member(jsii_name="putWorker")
    def put_worker(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        max_count: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        min_count: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu: CPU request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param max_count: Maximum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#max_count GoogleComposerEnvironment#max_count}
        :param memory_gb: Memory (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param min_count: Minimum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#min_count GoogleComposerEnvironment#min_count}
        :param storage_gb: Storage (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        value = GoogleComposerEnvironmentConfigWorkloadsConfigWorker(
            cpu=cpu,
            max_count=max_count,
            memory_gb=memory_gb,
            min_count=min_count,
            storage_gb=storage_gb,
        )

        return typing.cast(None, jsii.invoke(self, "putWorker", [value]))

    @jsii.member(jsii_name="resetDagProcessor")
    def reset_dag_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDagProcessor", []))

    @jsii.member(jsii_name="resetScheduler")
    def reset_scheduler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduler", []))

    @jsii.member(jsii_name="resetTriggerer")
    def reset_triggerer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerer", []))

    @jsii.member(jsii_name="resetWebServer")
    def reset_web_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebServer", []))

    @jsii.member(jsii_name="resetWorker")
    def reset_worker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorker", []))

    @builtins.property
    @jsii.member(jsii_name="dagProcessor")
    def dag_processor(
        self,
    ) -> GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference:
        return typing.cast(GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference, jsii.get(self, "dagProcessor"))

    @builtins.property
    @jsii.member(jsii_name="scheduler")
    def scheduler(
        self,
    ) -> "GoogleComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference", jsii.get(self, "scheduler"))

    @builtins.property
    @jsii.member(jsii_name="triggerer")
    def triggerer(
        self,
    ) -> "GoogleComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference", jsii.get(self, "triggerer"))

    @builtins.property
    @jsii.member(jsii_name="webServer")
    def web_server(
        self,
    ) -> "GoogleComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference", jsii.get(self, "webServer"))

    @builtins.property
    @jsii.member(jsii_name="worker")
    def worker(
        self,
    ) -> "GoogleComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference":
        return typing.cast("GoogleComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference", jsii.get(self, "worker"))

    @builtins.property
    @jsii.member(jsii_name="dagProcessorInput")
    def dag_processor_input(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor], jsii.get(self, "dagProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerInput")
    def scheduler_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigScheduler"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigScheduler"], jsii.get(self, "schedulerInput"))

    @builtins.property
    @jsii.member(jsii_name="triggererInput")
    def triggerer_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer"], jsii.get(self, "triggererInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerInput")
    def web_server_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWebServer"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWebServer"], jsii.get(self, "webServerInput"))

    @builtins.property
    @jsii.member(jsii_name="workerInput")
    def worker_input(
        self,
    ) -> typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWorker"]:
        return typing.cast(typing.Optional["GoogleComposerEnvironmentConfigWorkloadsConfigWorker"], jsii.get(self, "workerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93af13de80781544ac2772e48d5fedd80a2488818a6d823933f6b0c532bafebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigScheduler",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "cpu": "cpu",
        "memory_gb": "memoryGb",
        "storage_gb": "storageGb",
    },
)
class GoogleComposerEnvironmentConfigWorkloadsConfigScheduler:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The number of schedulers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0016f2648ede41e80f9266a03bf2ba2470e4f76e451de28363e380c395d0ff9e)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_gb", value=memory_gb, expected_type=type_hints["memory_gb"])
            check_type(argname="argument storage_gb", value=storage_gb, expected_type=type_hints["storage_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_gb is not None:
            self._values["memory_gb"] = memory_gb
        if storage_gb is not None:
            self._values["storage_gb"] = storage_gb

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The number of schedulers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''CPU request and limit for a single Airflow scheduler replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for a single Airflow scheduler replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for a single Airflow scheduler replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWorkloadsConfigScheduler(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b12e7dac010e04122a80ecb9073ff2ae09d9b24b3cd0d960ec830af5284761b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemoryGb")
    def reset_memory_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGb", []))

    @jsii.member(jsii_name="resetStorageGb")
    def reset_storage_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageGb", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGbInput")
    def memory_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGbInput"))

    @builtins.property
    @jsii.member(jsii_name="storageGbInput")
    def storage_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageGbInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf462a078c2a6b6883e7791d68a5a11223be5a0cf491cd6acd7a8b04adf8d75e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb3bf7bae714bdabfc350e1cd196e1f1b276d3a9aea2e12b70dbd23fae6d5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f803c56eb64d12b52a9c1c010d37ad4217f04fcca7ded59ad3cbdc90053ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811ad395020e209deebf98e6d51865bb84efe11e8e6b8e4b2d603aa8da431620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigScheduler]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigScheduler], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigScheduler],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fe3b4450190bef90a555ed917b642a0336ac477738ac217905f10170a0bf6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "cpu": "cpu", "memory_gb": "memoryGb"},
)
class GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer:
    def __init__(
        self,
        *,
        count: jsii.Number,
        cpu: jsii.Number,
        memory_gb: jsii.Number,
    ) -> None:
        '''
        :param count: The number of triggerers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758735e99a5bca24b25cbed718d730faf7e113a4a941002435575611c09df12e)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_gb", value=memory_gb, expected_type=type_hints["memory_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "cpu": cpu,
            "memory_gb": memory_gb,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of triggerers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#count GoogleComposerEnvironment#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''CPU request and limit for a single Airflow triggerer replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_gb(self) -> jsii.Number:
        '''Memory (GB) request and limit for a single Airflow triggerer replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        assert result is not None, "Required property 'memory_gb' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98b9e4dfd32e27ef33c0b58aaa7cd4d5fe17b9a4218729011c47d02844a6d900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGbInput")
    def memory_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGbInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb748d76a9378fc4473e863ec31140883c4316a5f0c8d7392be2a210e9a12e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3ec0d8413e5de565f08b633800a4e8d28d94d98af48c4e2ead1a2d21a0f42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e3f3e44f2fbab9495af88d845a8a48e6fc635d3c143e13ffa8cdca27aef2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71df2a141fdce7bdee0397bb0de852332df65431ac7be54a0d0742fec3da38ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigWebServer",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory_gb": "memoryGb", "storage_gb": "storageGb"},
)
class GoogleComposerEnvironmentConfigWorkloadsConfigWebServer:
    def __init__(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu: CPU request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251aba12f74026793d593dcb81bed5cff3266cc3c7b5d99bd69012e9020f7518)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_gb", value=memory_gb, expected_type=type_hints["memory_gb"])
            check_type(argname="argument storage_gb", value=storage_gb, expected_type=type_hints["storage_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_gb is not None:
            self._values["memory_gb"] = memory_gb
        if storage_gb is not None:
            self._values["storage_gb"] = storage_gb

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''CPU request and limit for Airflow web server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for Airflow web server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for Airflow web server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWorkloadsConfigWebServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11fe1df74d6c2c8c230da8ab98afb2e1f6307b22b1e5837c97e483e8a6dbcc88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMemoryGb")
    def reset_memory_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGb", []))

    @jsii.member(jsii_name="resetStorageGb")
    def reset_storage_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageGb", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGbInput")
    def memory_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGbInput"))

    @builtins.property
    @jsii.member(jsii_name="storageGbInput")
    def storage_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageGbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31859bbfdca7fbd8e6aa0d7514a1881654fba254d0b5fb91a785a16d94687e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1190f539e7596f6c750b33d7d4ddae8aa4c5ce523dc5f620ccc5bbc234a29afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a8f930a63a8d80ef720e06cb640f65463b2a583ecfc3eef16dfc40bc0054d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWebServer]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWebServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWebServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee906935bf7967cc7286e580b3fc89e8b2bb3cddcb645e34d8ca16cdfda1cde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigWorker",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "max_count": "maxCount",
        "memory_gb": "memoryGb",
        "min_count": "minCount",
        "storage_gb": "storageGb",
    },
)
class GoogleComposerEnvironmentConfigWorkloadsConfigWorker:
    def __init__(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        max_count: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        min_count: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu: CPU request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        :param max_count: Maximum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#max_count GoogleComposerEnvironment#max_count}
        :param memory_gb: Memory (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        :param min_count: Minimum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#min_count GoogleComposerEnvironment#min_count}
        :param storage_gb: Storage (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6694e126fcf28dab9e3958525ed2ccf8ce4962a453cd43300030ad0480c3fb)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
            check_type(argname="argument memory_gb", value=memory_gb, expected_type=type_hints["memory_gb"])
            check_type(argname="argument min_count", value=min_count, expected_type=type_hints["min_count"])
            check_type(argname="argument storage_gb", value=storage_gb, expected_type=type_hints["storage_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if max_count is not None:
            self._values["max_count"] = max_count
        if memory_gb is not None:
            self._values["memory_gb"] = memory_gb
        if min_count is not None:
            self._values["min_count"] = min_count
        if storage_gb is not None:
            self._values["storage_gb"] = storage_gb

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''CPU request and limit for a single Airflow worker replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#cpu GoogleComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of workers for autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#max_count GoogleComposerEnvironment#max_count}
        '''
        result = self._values.get("max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for a single Airflow worker replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#memory_gb GoogleComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of workers for autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#min_count GoogleComposerEnvironment#min_count}
        '''
        result = self._values.get("min_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for a single Airflow worker replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#storage_gb GoogleComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentConfigWorkloadsConfigWorker(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84d132489dc2a78454a302a9706feb6f84424d79bcc2aeeb1348442a59296cf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetMaxCount")
    def reset_max_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCount", []))

    @jsii.member(jsii_name="resetMemoryGb")
    def reset_memory_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryGb", []))

    @jsii.member(jsii_name="resetMinCount")
    def reset_min_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCount", []))

    @jsii.member(jsii_name="resetStorageGb")
    def reset_storage_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageGb", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCountInput")
    def max_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCountInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryGbInput")
    def memory_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryGbInput"))

    @builtins.property
    @jsii.member(jsii_name="minCountInput")
    def min_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageGbInput")
    def storage_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageGbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f127180045ea9e02bf0a23e841481837a395bdb3d16f2c75fd516196c74b0eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxCount")
    def max_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCount"))

    @max_count.setter
    def max_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53981ea07ea4cfe30241d87bace1e1e0e5f0f31c349f044e5f1f742f2c9e0a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dad9a018da13bccdb7d027ba4ecca371e1135f0504dc680eb5b65255e8d480b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCount")
    def min_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCount"))

    @min_count.setter
    def min_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4473ac46590a271abf664346e7e10d8143d01fe2252ab7dea7d4731c6c2255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be85016bcb95f64053802b436e326842945608cc9a1e88f57fb0a1a4a19720da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWorker]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWorker], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWorker],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e640180bb91477bbf027a9ec6e18befe0a8888280efac704f2964a253b64a5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentStorageConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket"},
)
class GoogleComposerEnvironmentStorageConfig:
    def __init__(self, *, bucket: builtins.str) -> None:
        '''
        :param bucket: Optional. Name of an existing Cloud Storage bucket to be used by the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#bucket GoogleComposerEnvironment#bucket}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2dc7cb7dc945845a5de338376192566e3e957f4e24310cc597ebf7a8e6c987)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Optional. Name of an existing Cloud Storage bucket to be used by the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#bucket GoogleComposerEnvironment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aaae8abf6d5435ac5c226ba8f6c56a2d1b99f29ecbf86d162e5ad73930d72c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e4373016398be75f09564e37ce393a41bd06f3800ea0dc1816f288a035087b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComposerEnvironmentStorageConfig]:
        return typing.cast(typing.Optional[GoogleComposerEnvironmentStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComposerEnvironmentStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98749e0a601a4de859eb65887b3d73e7e99fb17d41c556945baa688033a6f98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComposerEnvironmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#create GoogleComposerEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#delete GoogleComposerEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#update GoogleComposerEnvironment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c6db8079ab8a93d06bb2d82aa469cdc5bfe40e0dd3dbdb7e9a1f266b5a72c8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#create GoogleComposerEnvironment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#delete GoogleComposerEnvironment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_composer_environment#update GoogleComposerEnvironment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComposerEnvironmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComposerEnvironmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComposerEnvironment.GoogleComposerEnvironmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b69e915f1d12b7ed5dfef0e68c1029efc21ac0052ff2021aa39cf4bbde9bf36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8d7c9656edc0112b6643bb13d35926a6cc354d38a33214f1dd504f11a9237fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2c88a318d12204e13fba10a61e7e06827cd3a91c75074556d773349bd20c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d6a6384afcb76e9022e1627325402eba87f89c4ae03bead40e6db801ae6d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0020e3220781f252f82f833d340d037101cd67d10562e534b03f784a7aa022e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComposerEnvironment",
    "GoogleComposerEnvironmentConfig",
    "GoogleComposerEnvironmentConfigA",
    "GoogleComposerEnvironmentConfigAOutputReference",
    "GoogleComposerEnvironmentConfigDataRetentionConfig",
    "GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig",
    "GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList",
    "GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference",
    "GoogleComposerEnvironmentConfigDataRetentionConfigOutputReference",
    "GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig",
    "GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList",
    "GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference",
    "GoogleComposerEnvironmentConfigDatabaseConfig",
    "GoogleComposerEnvironmentConfigDatabaseConfigOutputReference",
    "GoogleComposerEnvironmentConfigEncryptionConfig",
    "GoogleComposerEnvironmentConfigEncryptionConfigOutputReference",
    "GoogleComposerEnvironmentConfigMaintenanceWindow",
    "GoogleComposerEnvironmentConfigMaintenanceWindowOutputReference",
    "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig",
    "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks",
    "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList",
    "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference",
    "GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference",
    "GoogleComposerEnvironmentConfigNodeConfig",
    "GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy",
    "GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference",
    "GoogleComposerEnvironmentConfigNodeConfigOutputReference",
    "GoogleComposerEnvironmentConfigPrivateEnvironmentConfig",
    "GoogleComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference",
    "GoogleComposerEnvironmentConfigRecoveryConfig",
    "GoogleComposerEnvironmentConfigRecoveryConfigOutputReference",
    "GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig",
    "GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference",
    "GoogleComposerEnvironmentConfigSoftwareConfig",
    "GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration",
    "GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference",
    "GoogleComposerEnvironmentConfigSoftwareConfigOutputReference",
    "GoogleComposerEnvironmentConfigWebServerConfig",
    "GoogleComposerEnvironmentConfigWebServerConfigOutputReference",
    "GoogleComposerEnvironmentConfigWebServerNetworkAccessControl",
    "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange",
    "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList",
    "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference",
    "GoogleComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference",
    "GoogleComposerEnvironmentConfigWorkloadsConfig",
    "GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor",
    "GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference",
    "GoogleComposerEnvironmentConfigWorkloadsConfigOutputReference",
    "GoogleComposerEnvironmentConfigWorkloadsConfigScheduler",
    "GoogleComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference",
    "GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer",
    "GoogleComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference",
    "GoogleComposerEnvironmentConfigWorkloadsConfigWebServer",
    "GoogleComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference",
    "GoogleComposerEnvironmentConfigWorkloadsConfigWorker",
    "GoogleComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference",
    "GoogleComposerEnvironmentStorageConfig",
    "GoogleComposerEnvironmentStorageConfigOutputReference",
    "GoogleComposerEnvironmentTimeouts",
    "GoogleComposerEnvironmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f071866de60b7b738d4cca5bee2c1adb6e8fd448a2f2c18853c3d100487f0f6c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    storage_config: typing.Optional[typing.Union[GoogleComposerEnvironmentStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComposerEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8de71c4f3e7b75844cb085af056360751e6925871803be802d18f6e50726c43a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6aae58565e4b1b330f31bb3dd7054b5286a8ae83ddc629bcff629d08238692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc257e32c7de8a96bfafdfc0b4797670eee4d3dfa3b4c0ea0d909c530d0596d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e16b4918495b2a323e3ecab2a9bfdc2e3c77488ad4e223ec8f0b25f1127a0b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c55eb12208b9f605deffff03690083dcf6e340d44038ea1c30af4a85f7cf6ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9103473a995879a9f2bc2e7cb0f861e0a2e0b55da58d74d162122df26c5ab30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164ece5e6ddd4ccde928c31b0a8b38d8e3442a019ecc0797281cee7020e042ef(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    storage_config: typing.Optional[typing.Union[GoogleComposerEnvironmentStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComposerEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97701be78db1faa6abbb2a6bd2bc968eef5a49d9406ff651b402dadae2aac74d(
    *,
    database_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigDatabaseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_retention_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigDataRetentionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_private_builds_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_private_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_size: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    master_authorized_networks_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_count: typing.Optional[jsii.Number] = None,
    private_environment_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigPrivateEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigRecoveryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    resilience_mode: typing.Optional[builtins.str] = None,
    software_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    web_server_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWebServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    web_server_network_access_control: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWebServerNetworkAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    workloads_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWorkloadsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c22931bb54fd251e7524756a6e39678404adce5d7e456c7dc5cd7ecec46f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264472f671f8096f16d59ec35f7bd3fe6b03236a20b67a0ec2727326a26f5d13(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a25d0e4172bb7436643c8e107b6ff453507260af466d2dfdfcadef17fe239f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb22d7ab17306de93b3f1223f72014b9c54515354495910c4f9fa6d924945fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baec230458d3650cec4d4a0180a721766b4479427731f9ba82a47c87ccdb165(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fd4174cee128ec88ccfcc00f1bf5e54f61914705d867c26366276d3da151db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4931c17e1743f8d67ba9ba6ef245677b92a52493145f7c3154b3ab55fc16bf42(
    value: typing.Optional[GoogleComposerEnvironmentConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06be248df1197e20dab725057281d48b8dc1487b3e19c6576c3f43b822d7d95(
    *,
    airflow_metadata_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    task_logs_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7bdaa902838281dc4887a6d388685a1696aa20f4efa856a94baa1a72d979d05(
    *,
    retention_days: typing.Optional[jsii.Number] = None,
    retention_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505e89b4d3dec77375f5a8049c75044c25310bf49fd0e25f8448d77f50f5c587(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a65911ea6735e2621c7c77c9d9fdfa8f7e14fb80b33ef3da68c353cbf983cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b468dbcf2f8f04a8c17cc732070c17f5382ef4c58b776e90ff218b9640e640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180dc0572acd525526a5a729b72404e86bd0e335d55a96560eafb6b644416b60(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9139047f2e1665bb0c6111fbdc685817025cab2945db7dae8c2e6c526e1cd24c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a504806e6915a9cb5496a5cc95eb1727bc37f587406aa2d453ab22e8bdbe7818(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c45466d09c7fc078781a2855f5f2706a83729b884dac6410c7031302a37094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a15183045eca43759fb33958e676c441f675009780f6af7e2bffa4b697ae769(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e082c78d0978d7755afa33cd465dc3a03fe0c70b54022685183f57d8fe9f1f4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b891091b21baa13cccbb29274d9669ccada240b5234e890a963c7af5daae37a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6535316b7b80a0b7e67c5605025493423979dcdb8aad3fd55e4b0986dc41b6a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93db275c19425e35f5cf288be50ede4d8b1e988dd839bef13bd448bd3f7c37c3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa04c304d2ff0cc2ca8efae27d4b20fa901797afc21158b1035f577410664898(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6866733cd38d12c832e3083a79317d57f5fd4502140509ca22759be35753106(
    value: typing.Optional[GoogleComposerEnvironmentConfigDataRetentionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581fd1632c3bae82d60ddc42e77fd27073e7a14c39b9fa6d1166a5e3c4212169(
    *,
    storage_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed97819fe6d7fbded4966f2e848ebfc6a4501f6978a889a196c328e74260482(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088ebe926ccf7ad9319ebd6bd96054dd9b213aa7f0f65c81d58e08b1406fd757(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08459314ba5a857ad5f8163c7f5676d47f3ff349a8da3a644a10f09b63bb7c94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffb93f11753120cfd0d49f58f96dd63bbce5d5a894e9ca87ca4081c838ad418(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a616e75c50472254fad2253adac578f5ee277b5da1cf9009266ba42d8f1adaa1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1624b36a501a9c4acd1039dcd3e39a60a62abae808e3ca1b2917457a9f94fcd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e1c12da9eb2483518d9b22e54abdd9418b8268b08a9055abcedcffed97edb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b9840428ed3caa3972415d116d0aba4c4e0d53a847175b2bd34101787569b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4a2e63043c3234f0666871a41a88d80981ed3cfb55df0695acc57425057aac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a24f0a52739eac8c9933d6a4bf493b6380ccfd4ddf21fa253bec29bfcbc1a7(
    *,
    machine_type: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976d41908666c65341cef47c473adbd02a937218ebb9ed01bebf1c054e862a2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9095a272f15d778f88d0dcdd8eabe3faf144d396e8cab545ed6aacf1225e1725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749cdbf4b4215801b3a25e096612789d92d621fb7660d16650bc284df5cb7500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3607d7a3453a0d0c5dd401c0f2186e34ab22483087ed3a56c9016cda437ff733(
    value: typing.Optional[GoogleComposerEnvironmentConfigDatabaseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b2e6d0a5ba904eda299fc25fa0db73949f76dec3d4e2c90509d4c719f4eba3(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629c4ab4ba33be5e5bbd08d9f5c39ac78eb207a74fe2953ecf4dfa426a8e7f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b8bb092442c8a7f2ad05ffcee72163cf01f0c95346ed8ed54cf1959ca6054c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff84dbebf4b17fa51f179de0ee582074ef8e92ba8ed037e583bec3060a01418(
    value: typing.Optional[GoogleComposerEnvironmentConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f806ff1d257b96da650cbf0acd016bb15f7b6cfc81d2dcd80bc31972ac8e7219(
    *,
    end_time: builtins.str,
    recurrence: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bebd5b3ed1376bb2da575ff3418422700ab8584810f5888a9c5109959242ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24435bd48fcdff76f2f38c90824ec192fd01f02cc8f9d1689f50544a1dba0305(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7512906ba417d4541ebabf9fb396d08c9c9bdbc563b4bc3e8bd5f1f80b9e0e6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b483d41fd6a4a1ff6ed1a96927458cdd8437ea48b61bfcab699ebf442b5056d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9110d25b893d1f663e84882021a16c8e7dcc51a28d684dc692bb82c0758fda2(
    value: typing.Optional[GoogleComposerEnvironmentConfigMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38be4ce0698dbaddd8c822ac94a37496faeb8827b805c659835cc8de885f013(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cidr_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421d13eda24fec0bbb4bbf12c36f8e1e79841ea5dca510dbecc09c021728f484(
    *,
    cidr_block: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e093dc69775f3bf6f454978085cd08c9633f9b3651836f80de490f7b0d389fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b235c6eff8207b02644ba8a1438e86671e1d7c27aff45b3d14f5556b44819f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1409be879dcee521c3a37f1f6639121e3d9ec892b35f88bb45c74b9aeebeefa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7890e019a44cf698a5ef1da8e8d3686ecb4dae68ca8504eec40dd394cdae7c6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7602f837c6027b86a069a3e7695cbaeca736f53634e361180d49a64586ebba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02af2fe390e371900719259acc74052995e7e4a4a58f9832dc8e96dc5ec5829b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1504a63cca1cc25fe6495b8fd660ec6444d74c79232430cfbaeed67bfe2e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f308bd088ddf1f67808651b78bf49ca569c11e5327261e039cc4f9690da6dc87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1765441e4bd182e66bf0c9d1e3ceaf051262550f65a7fa0a85adb766bf5ab50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008804e5ee92012ef1b605c2bf91aa9e8e7cb208bebc2e5eb7ec62b6fb5b97f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4751839d4fdbeae238a880e0dcfbc520ee8efe938d085c73cebef616c621481(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8efceb17e8a5eb0bc528b7dab0ea1ccedb3300b126f6e2d99e812e51118510(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849efe19b4b87363d6de374d265b63c407f6a8e59af17b7fb7dba7b62a38a24(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d42977ba151518d97a50229468afc8d7292333fa8020c2c6251a1ece6cfc7ee(
    value: typing.Optional[GoogleComposerEnvironmentConfigMasterAuthorizedNetworksConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e478c439c73439e119f9c8a544739a138ab659e35fd2e6224ef3e5a03fbdf5b(
    *,
    composer_internal_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    composer_network_attachment: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    enable_ip_masq_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_allocation_policy: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    network: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_account: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17117a91daae18ba0ce49caaf849f28852d57dba96c569d25c69fd7fa9e32e4f(
    *,
    cluster_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    cluster_secondary_range_name: typing.Optional[builtins.str] = None,
    services_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    services_secondary_range_name: typing.Optional[builtins.str] = None,
    use_ip_aliases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b14e1982454e27bc2da5308cfbf5e809ee953e4dc722613ba3e0a7517de64fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f7bc0d919aadf559f58aa8efd81a3a58fb8431846ef8a7032e3702ff2e8a2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2f6c9e5586be1e464b3f7d1fc740ba4805e46e89c955df84a19592f5dffaeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efeec3d71e090c5061d51c8c73dc5f589e3dc5b0f0a2543a2f119558343a8fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcebdaae17e25824d65973c864d3d147fc1bc0199421b82a197dff7e4b7987d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4bb27e1981af905a9e4bf9b70eb7a61ab65226fce9658125d60fe45937c3fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7dd1adb320136ae6b8bc6ba33c05dc821943ce3cbb94e59c2e582e7ce221afe(
    value: typing.Optional[GoogleComposerEnvironmentConfigNodeConfigIpAllocationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ca3c284df956c89d37ef491e6e6edad9553e6a185fe6694e0274e22626295a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27853e5234e9f8ce836d8cf40380f0a001e65f2b71622e8e115f51b214663440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca3aac71544b6c3ea03225eabaedbf6d5b84e6e7f8a50f2cc48c8858525fa64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefb4b02f89eda51330ab426e5a5be7e0a30af5fd566127e2cc0f23ad91ac81e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af781d6f24c4a43c85581dc848ddea6de4d537913971cb93460d369c9cf6177(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3a43244a3163185852babe502be93f9c9ae024f92f1aacce0f2487e2d04871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e3395b879b62dd95517fcdc1812ea1f8b9b52890ea7e6e47086907231b60d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a57215c50b64950ec21bb7ff9ff49e045c3ee41281fd0ec74202eb167be324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7d87bceb92009eeadfbf20a0b347d07fb91edbe5d2e366e1ee2c328a67ac9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b48a20f53ce6d6f0c47171c78e88472ce5507c9bac7578133806909704afdb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92129a97323d377c0311821f9412adc6a24a45d84b35f1dbf49189a0c392c7b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73667b39ee39edbfd7464911a4a27eccde7c9791cf824d55b9db454af2f44cc8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70649edcc81e0de3023572c5f69786fe81af539a2578e8535b839555b56aa2f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383237ae2cd75d01b8a2c1517c73f1680014c9f5c5bc17e40c49d438f07af909(
    value: typing.Optional[GoogleComposerEnvironmentConfigNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9768930bac1aed96af54ba0c08b00225a91eb2f3ad72ed310166ffdfeaf6575(
    *,
    cloud_composer_connection_subnetwork: typing.Optional[builtins.str] = None,
    cloud_composer_network_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    cloud_sql_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    connection_type: typing.Optional[builtins.str] = None,
    enable_private_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_privately_used_public_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    master_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    web_server_ipv4_cidr_block: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d0029b59f9b2d7e5a3aa284c3c1cf6497f97eb03d7f7e52b65fb1d21937df7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad42dc9e959abfe3a7ff006be9c4348f893555781d2e39a59e33fe9ae375e89b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264826a6a43afda101087df0de956c94f5379c535711e4590945ded20d5fbb58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38bbc66efb44e4751132e7345c7a1bf0eed6d9ee1e55d8ce5f9fae7768c8f6b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c6b17c8abbb6c7de9c56c01c8915c957f504daa55003db602ee7f44423284a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dd443872893672521ce3698c1668388188f33bd52c43a7fbf0e0aa525dec86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f63c0965102bab5a7bdf0975b15aeea6ee80e91024c980a9256b4ca3672e181(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdcfaab689a5211b329d8a75c2fa642859f7ffc401a66cd457311b049ac78c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da203bf206b86a0b5584d0ed0fc0456418abfb82f1c104783d8aa22ebd23167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579db399d2ec1f8b6f1a910f4dca13c7b2e473489c49434455070747ac212e20(
    value: typing.Optional[GoogleComposerEnvironmentConfigPrivateEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0e57783e3ea41e2b6a0e8dc3bac11f124a14dde02c2c3f6711ed43ef5e1de0(
    *,
    scheduled_snapshots_config: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d2a31bdc36491afbc1ea49ac5598e8ff64a04dd64f633b6584de2cbd3edff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2a3a4ca26c5ffcbb6555e528e900776998752b8b2ffd073d7efae32f39711e(
    value: typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97aa5d483c432d41282ff929ab18374df4a0ec23cf60544c8dde5e4db3a15493(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    snapshot_creation_schedule: typing.Optional[builtins.str] = None,
    snapshot_location: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b3c0984c1b47b462465f280d5a6bf61693be3e1cab7164adf0c082068838eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f417749b64cf08e985d4808b09babdca7bdad69bfca3318a2a1d65573a83f9a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59beabb540ece0a3ef0e7c0c3180dfb588b7ab359216355cab6b96e59958186(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328f1cddca1215de9007d03879171b61ceb7a24b59b4295b03a79c4b3fede07b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4ac64297b6081c070bcb8c1c9af41964d53bf433376d0d4a8ce0cfdcaeaa49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66e75f5158c1c904d9036d2dcf442eb79960840c35141c3c2b31d5c5756031c(
    value: typing.Optional[GoogleComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bda64ee99d5d72be623fa48913427a8f6a3e0c11aae5033405c6064e9e35162(
    *,
    airflow_config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    cloud_data_lineage_integration: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image_version: typing.Optional[builtins.str] = None,
    pypi_packages: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_version: typing.Optional[builtins.str] = None,
    scheduler_count: typing.Optional[jsii.Number] = None,
    web_server_plugins_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb6b5b8a335445644063b09eb40e1e50b71b29d1d4c8e9fdd3944cb0cede626(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d14ec609433ad7146cfc4c522e52028b3d3c7104b44c60c05785acafb6d6ba1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905bf1659cba86316584733c64e472f151a89010e09f3f6d04d8f0f92d4ea160(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bbfee5a76c2f296b81ce25671977952f2d53e4b7af29ccef606100f23556e5(
    value: typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b554a8a028b463e2325aa88e8404917cc4a69995e42a824e81a904b2c1557184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8aeaa95d656c0583d40d85faaf269ab17054ffb1ecce5bde80806cf704ec2b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d04436791b9592c966b256bc4b038840277388dfd376a9e12e3c34fa2c2938(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639e60dc4d3043740c7e9fa9d236fb316c523d371cd6b3eb787bf3dda7e2cb8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ee1bc00a90fc34bf22b844de2ab929fef45f65ef6bf5ff68c28316ea9d6671(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ed08c07972f59a9ed97a44738d93a6f53f9440087802a1eecfa1adf93d4a9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49dad3233e94559cd3ebe57f615901fd205b58e622764f23feb15cb3a27e0361(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51072f0e45fe28a6a59a3a6e322b0c1cc61c9e1248f29df417749ecdb15b7b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba579262f69349404edaaac91b0d9667c42e2f0dda590929f5eeb3bc1a0bf4bc(
    value: typing.Optional[GoogleComposerEnvironmentConfigSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05541bb52233791b51bdddf3c67f60436afeb2b1fc14c6d123da1f409ab46b59(
    *,
    machine_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31bf4a216589016a97267bdc03185270a9715db2c7fd7ee7d397fea49b864ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e4434446ff7ada56559ca6438c195892e3c5443f071194dbc74387218bb065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386c4e4843f65d533e8da197af385bbde1c859e6eb9bb618d968ac940a06b206(
    value: typing.Optional[GoogleComposerEnvironmentConfigWebServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1630e5f6ae74a9e4c62acd8331dac3c7a7df47baebe7a248f663043195e3196b(
    *,
    allowed_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcb90db58d54caba979a864681a3d78f6d2a2d09fc2ce8f56460196f5ea7256(
    *,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab59b32b95c33cfef3d85043beee05a854fbf2b8a8f8f097f63d9473843146f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb1b7cbca311d14bd855f9a586832cfb14d09695931e40bb883601ae5e8307d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1673291bce56d4d5fb655ffb22a5107e43839310cb03026f08a88232b9a8055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bc688ffaa58df3097fd138cdec205ab6506dfe4e530bec35877825266caf9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7028d625e2f6e2d3c06381c9303d4f671bdeeb9f9f22eaac75005003b549255(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b063811d8130f7be467998994988316e90692c6b16166ca8c55bd645f529963(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac05697c32f33852258a2aaf7b1910a3595fa8d40f526ae8ae1c778512ede57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18174ab3e31cb83b3466d6980c215c163d2f43929021a99679ee778cb9fe9e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8b3e57394bd95fa3b22d02ba9f9005daf0bbdada4900cca2d813c10ee368b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2662ded4bb311cf40ca54cfc27eb8e7a2a40685839a42bcefe670d47103845b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0cdc285935a7b6d74b1f8681c0d1fd98cc8705a8d5a6d04208fc174bfed627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192508e51d54c7b216556a80b702dc0b725bb320c7a3166805f200b6b943574f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd51a5364a6aa5052a0b9a90558a1b6e43f4552f136d13ca43021afeeb31994(
    value: typing.Optional[GoogleComposerEnvironmentConfigWebServerNetworkAccessControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a170f72e4813e5916f0dcf16148cef086c29eae98cd086500ac47d64e676d2(
    *,
    dag_processor: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWorkloadsConfigScheduler, typing.Dict[builtins.str, typing.Any]]] = None,
    triggerer: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_server: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWorkloadsConfigWebServer, typing.Dict[builtins.str, typing.Any]]] = None,
    worker: typing.Optional[typing.Union[GoogleComposerEnvironmentConfigWorkloadsConfigWorker, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128e8cc5c4258b2da5ae1c83e9e6d561830243048a744291733b13082448ac07(
    *,
    count: typing.Optional[jsii.Number] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e9271dac78fef9c9fe8f5f648c2f91011894f4cce8298df5beeaf013ea30d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a853d1caf67e2c4e3d1e59fc842ffbdb3e8058cc2473b8f8a4c39a3ac090ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11693cdcbaf3a7eaa1c4cd5c02d53933972423fc5f11ca634e51e3f92da58eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c7383aadf9ceeeded954f8f6f8b17e443559ac854c79dd1f82cb90eea28b33(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac82875ad881a576fd9eaf36bef31918fb704f9516d771db412458f4a1e11c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa73d4ee01dffff95992623ae18ae28205d34412afcaf4146d6dca9cfb9107d8(
    value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigDagProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69819d33757b8121a96ecf7c1720d35a2a5457b6269899b189c0c3cfdf0e1ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93af13de80781544ac2772e48d5fedd80a2488818a6d823933f6b0c532bafebb(
    value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0016f2648ede41e80f9266a03bf2ba2470e4f76e451de28363e380c395d0ff9e(
    *,
    count: typing.Optional[jsii.Number] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b12e7dac010e04122a80ecb9073ff2ae09d9b24b3cd0d960ec830af5284761b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf462a078c2a6b6883e7791d68a5a11223be5a0cf491cd6acd7a8b04adf8d75e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb3bf7bae714bdabfc350e1cd196e1f1b276d3a9aea2e12b70dbd23fae6d5f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f803c56eb64d12b52a9c1c010d37ad4217f04fcca7ded59ad3cbdc90053ecf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811ad395020e209deebf98e6d51865bb84efe11e8e6b8e4b2d603aa8da431620(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fe3b4450190bef90a555ed917b642a0336ac477738ac217905f10170a0bf6f(
    value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigScheduler],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758735e99a5bca24b25cbed718d730faf7e113a4a941002435575611c09df12e(
    *,
    count: jsii.Number,
    cpu: jsii.Number,
    memory_gb: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b9e4dfd32e27ef33c0b58aaa7cd4d5fe17b9a4218729011c47d02844a6d900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb748d76a9378fc4473e863ec31140883c4316a5f0c8d7392be2a210e9a12e71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3ec0d8413e5de565f08b633800a4e8d28d94d98af48c4e2ead1a2d21a0f42a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e3f3e44f2fbab9495af88d845a8a48e6fc635d3c143e13ffa8cdca27aef2c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71df2a141fdce7bdee0397bb0de852332df65431ac7be54a0d0742fec3da38ed(
    value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigTriggerer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251aba12f74026793d593dcb81bed5cff3266cc3c7b5d99bd69012e9020f7518(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fe1df74d6c2c8c230da8ab98afb2e1f6307b22b1e5837c97e483e8a6dbcc88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31859bbfdca7fbd8e6aa0d7514a1881654fba254d0b5fb91a785a16d94687e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1190f539e7596f6c750b33d7d4ddae8aa4c5ce523dc5f620ccc5bbc234a29afa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a8f930a63a8d80ef720e06cb640f65463b2a583ecfc3eef16dfc40bc0054d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee906935bf7967cc7286e580b3fc89e8b2bb3cddcb645e34d8ca16cdfda1cde2(
    value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWebServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6694e126fcf28dab9e3958525ed2ccf8ce4962a453cd43300030ad0480c3fb(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    max_count: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    min_count: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d132489dc2a78454a302a9706feb6f84424d79bcc2aeeb1348442a59296cf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f127180045ea9e02bf0a23e841481837a395bdb3d16f2c75fd516196c74b0eed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53981ea07ea4cfe30241d87bace1e1e0e5f0f31c349f044e5f1f742f2c9e0a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dad9a018da13bccdb7d027ba4ecca371e1135f0504dc680eb5b65255e8d480b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4473ac46590a271abf664346e7e10d8143d01fe2252ab7dea7d4731c6c2255(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be85016bcb95f64053802b436e326842945608cc9a1e88f57fb0a1a4a19720da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e640180bb91477bbf027a9ec6e18befe0a8888280efac704f2964a253b64a5cf(
    value: typing.Optional[GoogleComposerEnvironmentConfigWorkloadsConfigWorker],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2dc7cb7dc945845a5de338376192566e3e957f4e24310cc597ebf7a8e6c987(
    *,
    bucket: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaae8abf6d5435ac5c226ba8f6c56a2d1b99f29ecbf86d162e5ad73930d72c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e4373016398be75f09564e37ce393a41bd06f3800ea0dc1816f288a035087b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98749e0a601a4de859eb65887b3d73e7e99fb17d41c556945baa688033a6f98b(
    value: typing.Optional[GoogleComposerEnvironmentStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c6db8079ab8a93d06bb2d82aa469cdc5bfe40e0dd3dbdb7e9a1f266b5a72c8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b69e915f1d12b7ed5dfef0e68c1029efc21ac0052ff2021aa39cf4bbde9bf36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d7c9656edc0112b6643bb13d35926a6cc354d38a33214f1dd504f11a9237fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2c88a318d12204e13fba10a61e7e06827cd3a91c75074556d773349bd20c39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d6a6384afcb76e9022e1627325402eba87f89c4ae03bead40e6db801ae6d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0020e3220781f252f82f833d340d037101cd67d10562e534b03f784a7aa022e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComposerEnvironmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
