r'''
# `google_composer_environment`

Refer to the Terraform Registry for docs: [`google_composer_environment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment).
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


class ComposerEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment google_composer_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        config: typing.Optional[typing.Union["ComposerEnvironmentConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        storage_config: typing.Optional[typing.Union["ComposerEnvironmentStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComposerEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment google_composer_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#name ComposerEnvironment#name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#config ComposerEnvironment#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#id ComposerEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for this environment. The labels map can contain no more than 64 entries. Entries of the labels map are UTF8 strings that comply with the following restrictions: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Label values must be between 0 and 63 characters long and must conform to the regular expression (`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?. No more than 64 labels can be associated with a given environment. Both keys and values must be <= 128 bytes in size:: **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#labels ComposerEnvironment#labels}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#project ComposerEnvironment#project}
        :param region: The location or Compute Engine region for the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#region ComposerEnvironment#region}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_config ComposerEnvironment#storage_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#timeouts ComposerEnvironment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75963584f3ce33b53cf22e9bb568521d0ad9cc7ce9db83bbcf7c23eafc127fa2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = ComposerEnvironmentConfig(
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
        '''Generates CDKTF code for importing a ComposerEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComposerEnvironment to import.
        :param import_from_id: The id of the existing ComposerEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComposerEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272da7324b38bc5df69c1a6eac59d6a10cec1608914c78e8279e5d7d9529c8be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        database_config: typing.Optional[typing.Union["ComposerEnvironmentConfigDatabaseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_retention_config: typing.Optional[typing.Union["ComposerEnvironmentConfigDataRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_private_builds_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["ComposerEnvironmentConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_size: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["ComposerEnvironmentConfigMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        master_authorized_networks_config: typing.Optional[typing.Union["ComposerEnvironmentConfigMasterAuthorizedNetworksConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["ComposerEnvironmentConfigNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_environment_config: typing.Optional[typing.Union["ComposerEnvironmentConfigPrivateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_config: typing.Optional[typing.Union["ComposerEnvironmentConfigRecoveryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        resilience_mode: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["ComposerEnvironmentConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_config: typing.Optional[typing.Union["ComposerEnvironmentConfigWebServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_network_access_control: typing.Optional[typing.Union["ComposerEnvironmentConfigWebServerNetworkAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        workloads_config: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_config: database_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#database_config ComposerEnvironment#database_config}
        :param data_retention_config: data_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#data_retention_config ComposerEnvironment#data_retention_config}
        :param enable_private_builds_only: Optional. If true, builds performed during operations that install Python packages have only private connectivity to Google services. If false, the builds also have access to the internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_builds_only ComposerEnvironment#enable_private_builds_only}
        :param enable_private_environment: Optional. If true, a private Composer environment will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_environment ComposerEnvironment#enable_private_environment}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#encryption_config ComposerEnvironment#encryption_config}
        :param environment_size: The size of the Cloud Composer environment. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#environment_size ComposerEnvironment#environment_size}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#maintenance_window ComposerEnvironment#maintenance_window}
        :param master_authorized_networks_config: master_authorized_networks_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#master_authorized_networks_config ComposerEnvironment#master_authorized_networks_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#node_config ComposerEnvironment#node_config}
        :param node_count: The number of nodes in the Kubernetes Engine cluster that will be used to run this environment. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#node_count ComposerEnvironment#node_count}
        :param private_environment_config: private_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#private_environment_config ComposerEnvironment#private_environment_config}
        :param recovery_config: recovery_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#recovery_config ComposerEnvironment#recovery_config}
        :param resilience_mode: Whether high resilience is enabled or not. This field is supported for Cloud Composer environments in versions composer-2.1.15-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#resilience_mode ComposerEnvironment#resilience_mode}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#software_config ComposerEnvironment#software_config}
        :param web_server_config: web_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_config ComposerEnvironment#web_server_config}
        :param web_server_network_access_control: web_server_network_access_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_network_access_control ComposerEnvironment#web_server_network_access_control}
        :param workloads_config: workloads_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#workloads_config ComposerEnvironment#workloads_config}
        '''
        value = ComposerEnvironmentConfigA(
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
        :param bucket: Optional. Name of an existing Cloud Storage bucket to be used by the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#bucket ComposerEnvironment#bucket}
        '''
        value = ComposerEnvironmentStorageConfig(bucket=bucket)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#create ComposerEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#delete ComposerEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#update ComposerEnvironment#update}.
        '''
        value = ComposerEnvironmentTimeouts(
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
    def config(self) -> "ComposerEnvironmentConfigAOutputReference":
        return typing.cast("ComposerEnvironmentConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="storageConfig")
    def storage_config(self) -> "ComposerEnvironmentStorageConfigOutputReference":
        return typing.cast("ComposerEnvironmentStorageConfigOutputReference", jsii.get(self, "storageConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComposerEnvironmentTimeoutsOutputReference":
        return typing.cast("ComposerEnvironmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["ComposerEnvironmentConfigA"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigA"], jsii.get(self, "configInput"))

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
    ) -> typing.Optional["ComposerEnvironmentStorageConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentStorageConfig"], jsii.get(self, "storageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComposerEnvironmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComposerEnvironmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a73b8fe5ba4fcfde69cbc597c399ffa0c66d5113d94077f074140d77872045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc316127ef85d7e5d2cda7ea6f2c4c89f0cc174b2e24af26b10ede618ccd2088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b421d5b7908f2fb47cece79c6e16341bfc9d07300ee29a43610d69e448095dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f501ab6cb2ec743efb134adc92e3c40c839447781e12592a0145a8753f69b08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e334b5bb51ca122ffac32ecb08dcf8c7a605f09f3d98ded9821f78d3287e09d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfig",
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
class ComposerEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Optional[typing.Union["ComposerEnvironmentConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        storage_config: typing.Optional[typing.Union["ComposerEnvironmentStorageConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComposerEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#name ComposerEnvironment#name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#config ComposerEnvironment#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#id ComposerEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for this environment. The labels map can contain no more than 64 entries. Entries of the labels map are UTF8 strings that comply with the following restrictions: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Label values must be between 0 and 63 characters long and must conform to the regular expression (`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?)?. No more than 64 labels can be associated with a given environment. Both keys and values must be <= 128 bytes in size:: **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#labels ComposerEnvironment#labels}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#project ComposerEnvironment#project}
        :param region: The location or Compute Engine region for the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#region ComposerEnvironment#region}
        :param storage_config: storage_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_config ComposerEnvironment#storage_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#timeouts ComposerEnvironment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = ComposerEnvironmentConfigA(**config)
        if isinstance(storage_config, dict):
            storage_config = ComposerEnvironmentStorageConfig(**storage_config)
        if isinstance(timeouts, dict):
            timeouts = ComposerEnvironmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2171dc6a6a3a8ebf4e3578f2ad46c20819cd7ab55188b7b0325b1cb764c65f2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#name ComposerEnvironment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["ComposerEnvironmentConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#config ComposerEnvironment#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigA"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#id ComposerEnvironment#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#labels ComposerEnvironment#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#project ComposerEnvironment#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The location or Compute Engine region for the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#region ComposerEnvironment#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_config(self) -> typing.Optional["ComposerEnvironmentStorageConfig"]:
        '''storage_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_config ComposerEnvironment#storage_config}
        '''
        result = self._values.get("storage_config")
        return typing.cast(typing.Optional["ComposerEnvironmentStorageConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComposerEnvironmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#timeouts ComposerEnvironment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComposerEnvironmentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigA",
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
class ComposerEnvironmentConfigA:
    def __init__(
        self,
        *,
        database_config: typing.Optional[typing.Union["ComposerEnvironmentConfigDatabaseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_retention_config: typing.Optional[typing.Union["ComposerEnvironmentConfigDataRetentionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_private_builds_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_private_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["ComposerEnvironmentConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        environment_size: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["ComposerEnvironmentConfigMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        master_authorized_networks_config: typing.Optional[typing.Union["ComposerEnvironmentConfigMasterAuthorizedNetworksConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_config: typing.Optional[typing.Union["ComposerEnvironmentConfigNodeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_environment_config: typing.Optional[typing.Union["ComposerEnvironmentConfigPrivateEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_config: typing.Optional[typing.Union["ComposerEnvironmentConfigRecoveryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        resilience_mode: typing.Optional[builtins.str] = None,
        software_config: typing.Optional[typing.Union["ComposerEnvironmentConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_config: typing.Optional[typing.Union["ComposerEnvironmentConfigWebServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server_network_access_control: typing.Optional[typing.Union["ComposerEnvironmentConfigWebServerNetworkAccessControl", typing.Dict[builtins.str, typing.Any]]] = None,
        workloads_config: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_config: database_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#database_config ComposerEnvironment#database_config}
        :param data_retention_config: data_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#data_retention_config ComposerEnvironment#data_retention_config}
        :param enable_private_builds_only: Optional. If true, builds performed during operations that install Python packages have only private connectivity to Google services. If false, the builds also have access to the internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_builds_only ComposerEnvironment#enable_private_builds_only}
        :param enable_private_environment: Optional. If true, a private Composer environment will be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_environment ComposerEnvironment#enable_private_environment}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#encryption_config ComposerEnvironment#encryption_config}
        :param environment_size: The size of the Cloud Composer environment. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#environment_size ComposerEnvironment#environment_size}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#maintenance_window ComposerEnvironment#maintenance_window}
        :param master_authorized_networks_config: master_authorized_networks_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#master_authorized_networks_config ComposerEnvironment#master_authorized_networks_config}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#node_config ComposerEnvironment#node_config}
        :param node_count: The number of nodes in the Kubernetes Engine cluster that will be used to run this environment. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#node_count ComposerEnvironment#node_count}
        :param private_environment_config: private_environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#private_environment_config ComposerEnvironment#private_environment_config}
        :param recovery_config: recovery_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#recovery_config ComposerEnvironment#recovery_config}
        :param resilience_mode: Whether high resilience is enabled or not. This field is supported for Cloud Composer environments in versions composer-2.1.15-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#resilience_mode ComposerEnvironment#resilience_mode}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#software_config ComposerEnvironment#software_config}
        :param web_server_config: web_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_config ComposerEnvironment#web_server_config}
        :param web_server_network_access_control: web_server_network_access_control block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_network_access_control ComposerEnvironment#web_server_network_access_control}
        :param workloads_config: workloads_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#workloads_config ComposerEnvironment#workloads_config}
        '''
        if isinstance(database_config, dict):
            database_config = ComposerEnvironmentConfigDatabaseConfig(**database_config)
        if isinstance(data_retention_config, dict):
            data_retention_config = ComposerEnvironmentConfigDataRetentionConfig(**data_retention_config)
        if isinstance(encryption_config, dict):
            encryption_config = ComposerEnvironmentConfigEncryptionConfig(**encryption_config)
        if isinstance(maintenance_window, dict):
            maintenance_window = ComposerEnvironmentConfigMaintenanceWindow(**maintenance_window)
        if isinstance(master_authorized_networks_config, dict):
            master_authorized_networks_config = ComposerEnvironmentConfigMasterAuthorizedNetworksConfig(**master_authorized_networks_config)
        if isinstance(node_config, dict):
            node_config = ComposerEnvironmentConfigNodeConfig(**node_config)
        if isinstance(private_environment_config, dict):
            private_environment_config = ComposerEnvironmentConfigPrivateEnvironmentConfig(**private_environment_config)
        if isinstance(recovery_config, dict):
            recovery_config = ComposerEnvironmentConfigRecoveryConfig(**recovery_config)
        if isinstance(software_config, dict):
            software_config = ComposerEnvironmentConfigSoftwareConfig(**software_config)
        if isinstance(web_server_config, dict):
            web_server_config = ComposerEnvironmentConfigWebServerConfig(**web_server_config)
        if isinstance(web_server_network_access_control, dict):
            web_server_network_access_control = ComposerEnvironmentConfigWebServerNetworkAccessControl(**web_server_network_access_control)
        if isinstance(workloads_config, dict):
            workloads_config = ComposerEnvironmentConfigWorkloadsConfig(**workloads_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aee05fb1cc4e2d4b118004bfb75f940668bfc5ff2730fb9cfeac77ccfa0cdad)
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
    ) -> typing.Optional["ComposerEnvironmentConfigDatabaseConfig"]:
        '''database_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#database_config ComposerEnvironment#database_config}
        '''
        result = self._values.get("database_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigDatabaseConfig"], result)

    @builtins.property
    def data_retention_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigDataRetentionConfig"]:
        '''data_retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#data_retention_config ComposerEnvironment#data_retention_config}
        '''
        result = self._values.get("data_retention_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigDataRetentionConfig"], result)

    @builtins.property
    def enable_private_builds_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        If true, builds performed during operations that install Python packages have only private connectivity to Google services. If false, the builds also have access to the internet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_builds_only ComposerEnvironment#enable_private_builds_only}
        '''
        result = self._values.get("enable_private_builds_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_private_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If true, a private Composer environment will be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_environment ComposerEnvironment#enable_private_environment}
        '''
        result = self._values.get("enable_private_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#encryption_config ComposerEnvironment#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigEncryptionConfig"], result)

    @builtins.property
    def environment_size(self) -> typing.Optional[builtins.str]:
        '''The size of the Cloud Composer environment.

        This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#environment_size ComposerEnvironment#environment_size}
        '''
        result = self._values.get("environment_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#maintenance_window ComposerEnvironment#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigMaintenanceWindow"], result)

    @builtins.property
    def master_authorized_networks_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigMasterAuthorizedNetworksConfig"]:
        '''master_authorized_networks_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#master_authorized_networks_config ComposerEnvironment#master_authorized_networks_config}
        '''
        result = self._values.get("master_authorized_networks_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigMasterAuthorizedNetworksConfig"], result)

    @builtins.property
    def node_config(self) -> typing.Optional["ComposerEnvironmentConfigNodeConfig"]:
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#node_config ComposerEnvironment#node_config}
        '''
        result = self._values.get("node_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigNodeConfig"], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes in the Kubernetes Engine cluster that will be used to run this environment.

        This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#node_count ComposerEnvironment#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_environment_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigPrivateEnvironmentConfig"]:
        '''private_environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#private_environment_config ComposerEnvironment#private_environment_config}
        '''
        result = self._values.get("private_environment_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigPrivateEnvironmentConfig"], result)

    @builtins.property
    def recovery_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigRecoveryConfig"]:
        '''recovery_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#recovery_config ComposerEnvironment#recovery_config}
        '''
        result = self._values.get("recovery_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigRecoveryConfig"], result)

    @builtins.property
    def resilience_mode(self) -> typing.Optional[builtins.str]:
        '''Whether high resilience is enabled or not.

        This field is supported for Cloud Composer environments in versions composer-2.1.15-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#resilience_mode ComposerEnvironment#resilience_mode}
        '''
        result = self._values.get("resilience_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#software_config ComposerEnvironment#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigSoftwareConfig"], result)

    @builtins.property
    def web_server_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWebServerConfig"]:
        '''web_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_config ComposerEnvironment#web_server_config}
        '''
        result = self._values.get("web_server_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWebServerConfig"], result)

    @builtins.property
    def web_server_network_access_control(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWebServerNetworkAccessControl"]:
        '''web_server_network_access_control block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_network_access_control ComposerEnvironment#web_server_network_access_control}
        '''
        result = self._values.get("web_server_network_access_control")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWebServerNetworkAccessControl"], result)

    @builtins.property
    def workloads_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfig"]:
        '''workloads_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#workloads_config ComposerEnvironment#workloads_config}
        '''
        result = self._values.get("workloads_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bad0816bd973626671aa0b6e78e5a3e5307b605fed9ac1313da70253b3bac0d5)
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
        :param machine_type: Optional. Cloud SQL machine type used by Airflow database. It has to be one of: db-n1-standard-2, db-n1-standard-4, db-n1-standard-8 or db-n1-standard-16. If not specified, db-n1-standard-2 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        :param zone: Optional. Cloud SQL database preferred zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#zone ComposerEnvironment#zone}
        '''
        value = ComposerEnvironmentConfigDatabaseConfig(
            machine_type=machine_type, zone=zone
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseConfig", [value]))

    @jsii.member(jsii_name="putDataRetentionConfig")
    def put_data_retention_config(
        self,
        *,
        airflow_metadata_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_logs_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param airflow_metadata_retention_config: airflow_metadata_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#airflow_metadata_retention_config ComposerEnvironment#airflow_metadata_retention_config}
        :param task_logs_retention_config: task_logs_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#task_logs_retention_config ComposerEnvironment#task_logs_retention_config}
        '''
        value = ComposerEnvironmentConfigDataRetentionConfig(
            airflow_metadata_retention_config=airflow_metadata_retention_config,
            task_logs_retention_config=task_logs_retention_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDataRetentionConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Optional. Customer-managed Encryption Key available through Google's Key Management Service. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#kms_key_name ComposerEnvironment#kms_key_name}
        '''
        value = ComposerEnvironmentConfigEncryptionConfig(kms_key_name=kms_key_name)

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
        :param end_time: Maintenance window end time. It is used only to calculate the duration of the maintenance window. The value for end-time must be in the future, relative to 'start_time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#end_time ComposerEnvironment#end_time}
        :param recurrence: Maintenance window recurrence. Format is a subset of RFC-5545 (https://tools.ietf.org/html/rfc5545) 'RRULE'. The only allowed values for 'FREQ' field are 'FREQ=DAILY' and 'FREQ=WEEKLY;BYDAY=...'. Example values: 'FREQ=WEEKLY;BYDAY=TU,WE', 'FREQ=DAILY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#recurrence ComposerEnvironment#recurrence}
        :param start_time: Start time of the first recurrence of the maintenance window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#start_time ComposerEnvironment#start_time}
        '''
        value = ComposerEnvironmentConfigMaintenanceWindow(
            end_time=end_time, recurrence=recurrence, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putMasterAuthorizedNetworksConfig")
    def put_master_authorized_networks_config(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cidr_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not master authorized networks is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        :param cidr_blocks: cidr_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cidr_blocks ComposerEnvironment#cidr_blocks}
        '''
        value = ComposerEnvironmentConfigMasterAuthorizedNetworksConfig(
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
        ip_allocation_policy: typing.Optional[typing.Union["ComposerEnvironmentConfigNodeConfigIpAllocationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param composer_internal_ipv4_cidr_block: IPv4 cidr range that will be used by Composer internal components. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#composer_internal_ipv4_cidr_block ComposerEnvironment#composer_internal_ipv4_cidr_block}
        :param composer_network_attachment: PSC (Private Service Connect) Network entry point. Customers can pre-create the Network Attachment and point Cloud Composer environment to use. It is possible to share network attachment among many environments, provided enough IP addresses are available. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#composer_network_attachment ComposerEnvironment#composer_network_attachment}
        :param disk_size_gb: The disk size in GB used for node VMs. Minimum size is 20GB. If unspecified, defaults to 100GB. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#disk_size_gb ComposerEnvironment#disk_size_gb}
        :param enable_ip_masq_agent: Deploys 'ip-masq-agent' daemon set in the GKE cluster and defines nonMasqueradeCIDRs equals to pod IP range so IP masquerading is used for all destination addresses, except between pods traffic. See: https://cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_ip_masq_agent ComposerEnvironment#enable_ip_masq_agent}
        :param ip_allocation_policy: ip_allocation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#ip_allocation_policy ComposerEnvironment#ip_allocation_policy}
        :param machine_type: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        :param network: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. The network must belong to the environment's project. If unspecified, the "default" network ID in the environment's project is used. If a Custom Subnet Network is provided, subnetwork must also be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#network ComposerEnvironment#network}
        :param oauth_scopes: The set of Google API scopes to be made available on all node VMs. Cannot be updated. If empty, defaults to ["https://www.googleapis.com/auth/cloud-platform"]. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#oauth_scopes ComposerEnvironment#oauth_scopes}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. If given, note that the service account must have roles/composer.worker for any GCP resources created under the Cloud Composer Environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#service_account ComposerEnvironment#service_account}
        :param subnetwork: The Compute Engine subnetwork to be used for machine communications, specified as a self-link, relative resource name (e.g. "projects/{project}/regions/{region}/subnetworks/{subnetwork}"), or by name. If subnetwork is provided, network must also be provided and the subnetwork must belong to the enclosing environment's project and region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#subnetwork ComposerEnvironment#subnetwork}
        :param tags: The list of instance tags applied to all node VMs. Tags are used to identify valid sources or targets for network firewalls. Each tag within the list must comply with RFC1035. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#tags ComposerEnvironment#tags}
        :param zone: The Compute Engine zone in which to deploy the VMs running the Apache Airflow software, specified as the zone name or relative resource name (e.g. "projects/{project}/zones/{zone}"). Must belong to the enclosing environment's project and region. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#zone ComposerEnvironment#zone}
        '''
        value = ComposerEnvironmentConfigNodeConfig(
            composer_internal_ipv4_cidr_block=composer_internal_ipv4_cidr_block,
            composer_network_attachment=composer_network_attachment,
            disk_size_gb=disk_size_gb,
            enable_ip_masq_agent=enable_ip_masq_agent,
            ip_allocation_policy=ip_allocation_policy,
            machine_type=machine_type,
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
        :param cloud_composer_connection_subnetwork: When specified, the environment will use Private Service Connect instead of VPC peerings to connect to Cloud SQL in the Tenant Project, and the PSC endpoint in the Customer Project will use an IP address from this subnetwork. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_composer_connection_subnetwork ComposerEnvironment#cloud_composer_connection_subnetwork}
        :param cloud_composer_network_ipv4_cidr_block: The CIDR block from which IP range for Cloud Composer Network in tenant project will be reserved. Needs to be disjoint from private_cluster_config.master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_composer_network_ipv4_cidr_block ComposerEnvironment#cloud_composer_network_ipv4_cidr_block}
        :param cloud_sql_ipv4_cidr_block: The CIDR block from which IP range in tenant project will be reserved for Cloud SQL. Needs to be disjoint from web_server_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_sql_ipv4_cidr_block ComposerEnvironment#cloud_sql_ipv4_cidr_block}
        :param connection_type: Mode of internal communication within the Composer environment. Must be one of "VPC_PEERING" or "PRIVATE_SERVICE_CONNECT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#connection_type ComposerEnvironment#connection_type}
        :param enable_private_endpoint: If true, access to the public endpoint of the GKE cluster is denied. If this field is set to true, ip_allocation_policy.use_ip_aliases must be set to true for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_endpoint ComposerEnvironment#enable_private_endpoint}
        :param enable_privately_used_public_ips: When enabled, IPs from public (non-RFC1918) ranges can be used for ip_allocation_policy.cluster_ipv4_cidr_block and ip_allocation_policy.service_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_privately_used_public_ips ComposerEnvironment#enable_privately_used_public_ips}
        :param master_ipv4_cidr_block: The IP range in CIDR notation to use for the hosted master network. This range is used for assigning internal IP addresses to the cluster master or set of masters and to the internal load balancer virtual IP. This range must not overlap with any other ranges in use within the cluster's network. If left blank, the default value of '172.16.0.0/28' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#master_ipv4_cidr_block ComposerEnvironment#master_ipv4_cidr_block}
        :param web_server_ipv4_cidr_block: The CIDR block from which IP range for web server will be reserved. Needs to be disjoint from master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_ipv4_cidr_block ComposerEnvironment#web_server_ipv4_cidr_block}
        '''
        value = ComposerEnvironmentConfigPrivateEnvironmentConfig(
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
        scheduled_snapshots_config: typing.Optional[typing.Union["ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled_snapshots_config: scheduled_snapshots_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduled_snapshots_config ComposerEnvironment#scheduled_snapshots_config}
        '''
        value = ComposerEnvironmentConfigRecoveryConfig(
            scheduled_snapshots_config=scheduled_snapshots_config
        )

        return typing.cast(None, jsii.invoke(self, "putRecoveryConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        airflow_config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_data_lineage_integration: typing.Optional[typing.Union["ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_version: typing.Optional[builtins.str] = None,
        pypi_packages: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_version: typing.Optional[builtins.str] = None,
        scheduler_count: typing.Optional[jsii.Number] = None,
        web_server_plugins_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param airflow_config_overrides: Apache Airflow configuration properties to override. Property keys contain the section and property names, separated by a hyphen, for example "core-dags_are_paused_at_creation". Section names must not contain hyphens ("-"), opening square brackets ("["), or closing square brackets ("]"). The property name must not be empty and cannot contain "=" or ";". Section and property names cannot contain characters: "." Apache Airflow configuration property names must be written in snake_case. Property values can contain any character, and can be written in any lower/upper case format. Certain Apache Airflow configuration property values are blacklisted, and cannot be overridden. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#airflow_config_overrides ComposerEnvironment#airflow_config_overrides}
        :param cloud_data_lineage_integration: cloud_data_lineage_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_data_lineage_integration ComposerEnvironment#cloud_data_lineage_integration}
        :param env_variables: Additional environment variables to provide to the Apache Airflow scheduler, worker, and webserver processes. Environment variable names must match the regular expression [a-zA-Z_][a-zA-Z0-9_]*. They cannot specify Apache Airflow software configuration overrides (they cannot match the regular expression AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+), and they cannot match any of the following reserved names: AIRFLOW_HOME C_FORCE_ROOT CONTAINER_NAME DAGS_FOLDER GCP_PROJECT GCS_BUCKET GKE_CLUSTER_NAME SQL_DATABASE SQL_INSTANCE SQL_PASSWORD SQL_PROJECT SQL_REGION SQL_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#env_variables ComposerEnvironment#env_variables}
        :param image_version: The version of the software running in the environment. This encapsulates both the version of Cloud Composer functionality and the version of Apache Airflow. It must match the regular expression composer-([0-9]+(.[0-9]+.[0-9]+(-preview.[0-9]+)?)?|latest)-airflow-([0-9]+(.[0-9]+(.[0-9]+)?)?). The Cloud Composer portion of the image version is a full semantic version, or an alias in the form of major version number or 'latest'. The Apache Airflow portion of the image version is a full semantic version that points to one of the supported Apache Airflow versions, or an alias in the form of only major or major.minor versions specified. See documentation for more details and version list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#image_version ComposerEnvironment#image_version}
        :param pypi_packages: Custom Python Package Index (PyPI) packages to be installed in the environment. Keys refer to the lowercase package name (e.g. "numpy"). Values are the lowercase extras and version specifier (e.g. "==1.12.0", "[devel,gcp_api]", "[devel]>=1.8.2, <1.9.2"). To specify a package without pinning it to a version specifier, use the empty string as the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#pypi_packages ComposerEnvironment#pypi_packages}
        :param python_version: The major version of Python used to run the Apache Airflow scheduler, worker, and webserver processes. Can be set to '2' or '3'. If not specified, the default is '2'. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use Python major version 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#python_version ComposerEnvironment#python_version}
        :param scheduler_count: The number of schedulers for Airflow. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-2.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduler_count ComposerEnvironment#scheduler_count}
        :param web_server_plugins_mode: Should be either 'ENABLED' or 'DISABLED'. Defaults to 'ENABLED'. Used in Composer 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_plugins_mode ComposerEnvironment#web_server_plugins_mode}
        '''
        value = ComposerEnvironmentConfigSoftwareConfig(
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
        :param machine_type: Optional. Machine type on which Airflow web server is running. It has to be one of: composer-n1-webserver-2, composer-n1-webserver-4 or composer-n1-webserver-8. If not specified, composer-n1-webserver-2 will be used. Value custom is returned only in response, if Airflow web server parameters were manually changed to a non-standard values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        '''
        value = ComposerEnvironmentConfigWebServerConfig(machine_type=machine_type)

        return typing.cast(None, jsii.invoke(self, "putWebServerConfig", [value]))

    @jsii.member(jsii_name="putWebServerNetworkAccessControl")
    def put_web_server_network_access_control(
        self,
        *,
        allowed_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_ip_range: allowed_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#allowed_ip_range ComposerEnvironment#allowed_ip_range}
        '''
        value = ComposerEnvironmentConfigWebServerNetworkAccessControl(
            allowed_ip_range=allowed_ip_range
        )

        return typing.cast(None, jsii.invoke(self, "putWebServerNetworkAccessControl", [value]))

    @jsii.member(jsii_name="putWorkloadsConfig")
    def put_workloads_config(
        self,
        *,
        dag_processor: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigDagProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigScheduler", typing.Dict[builtins.str, typing.Any]]] = None,
        triggerer: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigTriggerer", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigWebServer", typing.Dict[builtins.str, typing.Any]]] = None,
        worker: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigWorker", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dag_processor: dag_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#dag_processor ComposerEnvironment#dag_processor}
        :param scheduler: scheduler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduler ComposerEnvironment#scheduler}
        :param triggerer: triggerer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#triggerer ComposerEnvironment#triggerer}
        :param web_server: web_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server ComposerEnvironment#web_server}
        :param worker: worker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#worker ComposerEnvironment#worker}
        '''
        value = ComposerEnvironmentConfigWorkloadsConfig(
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
    ) -> "ComposerEnvironmentConfigDatabaseConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigDatabaseConfigOutputReference", jsii.get(self, "databaseConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionConfig")
    def data_retention_config(
        self,
    ) -> "ComposerEnvironmentConfigDataRetentionConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigDataRetentionConfigOutputReference", jsii.get(self, "dataRetentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> "ComposerEnvironmentConfigEncryptionConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="gkeCluster")
    def gke_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeCluster"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "ComposerEnvironmentConfigMaintenanceWindowOutputReference":
        return typing.cast("ComposerEnvironmentConfigMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="masterAuthorizedNetworksConfig")
    def master_authorized_networks_config(
        self,
    ) -> "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference", jsii.get(self, "masterAuthorizedNetworksConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "ComposerEnvironmentConfigNodeConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateEnvironmentConfig")
    def private_environment_config(
        self,
    ) -> "ComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference", jsii.get(self, "privateEnvironmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="recoveryConfig")
    def recovery_config(
        self,
    ) -> "ComposerEnvironmentConfigRecoveryConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigRecoveryConfigOutputReference", jsii.get(self, "recoveryConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(
        self,
    ) -> "ComposerEnvironmentConfigSoftwareConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="webServerConfig")
    def web_server_config(
        self,
    ) -> "ComposerEnvironmentConfigWebServerConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigWebServerConfigOutputReference", jsii.get(self, "webServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="webServerNetworkAccessControl")
    def web_server_network_access_control(
        self,
    ) -> "ComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference":
        return typing.cast("ComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference", jsii.get(self, "webServerNetworkAccessControl"))

    @builtins.property
    @jsii.member(jsii_name="workloadsConfig")
    def workloads_config(
        self,
    ) -> "ComposerEnvironmentConfigWorkloadsConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigWorkloadsConfigOutputReference", jsii.get(self, "workloadsConfig"))

    @builtins.property
    @jsii.member(jsii_name="databaseConfigInput")
    def database_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigDatabaseConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigDatabaseConfig"], jsii.get(self, "databaseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionConfigInput")
    def data_retention_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigDataRetentionConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigDataRetentionConfig"], jsii.get(self, "dataRetentionConfigInput"))

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
    ) -> typing.Optional["ComposerEnvironmentConfigEncryptionConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentSizeInput")
    def environment_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigMaintenanceWindow"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="masterAuthorizedNetworksConfigInput")
    def master_authorized_networks_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigMasterAuthorizedNetworksConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigMasterAuthorizedNetworksConfig"], jsii.get(self, "masterAuthorizedNetworksConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigNodeConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="privateEnvironmentConfigInput")
    def private_environment_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigPrivateEnvironmentConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigPrivateEnvironmentConfig"], jsii.get(self, "privateEnvironmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryConfigInput")
    def recovery_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigRecoveryConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigRecoveryConfig"], jsii.get(self, "recoveryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="resilienceModeInput")
    def resilience_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resilienceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigSoftwareConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerConfigInput")
    def web_server_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWebServerConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWebServerConfig"], jsii.get(self, "webServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerNetworkAccessControlInput")
    def web_server_network_access_control_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWebServerNetworkAccessControl"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWebServerNetworkAccessControl"], jsii.get(self, "webServerNetworkAccessControlInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadsConfigInput")
    def workloads_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfig"], jsii.get(self, "workloadsConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__238250978f31ac3743c45c813e7dedef142c6eb4332a60301bbb72723b31be86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b7f7e480c4b2c42502554498cf46a4de5962e186c3d226980e0f7738824265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentSize")
    def environment_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentSize"))

    @environment_size.setter
    def environment_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61c86eeac63ebe7ba77836cf11e128956724dbe40f3f21f9996661d5c508028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbee362135c8294bd1fc2fabf9c95e2e8eb4a6a849af236afb11ecd22ed00409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resilienceMode")
    def resilience_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resilienceMode"))

    @resilience_mode.setter
    def resilience_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5312ff9f8f8723f2e7db384bed1f375fb8008715115f3c105eabf2f169533f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resilienceMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComposerEnvironmentConfigA]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837af12ab24526421593ec547b855c9055a14846e8ea97a51fdbe91062910256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_metadata_retention_config": "airflowMetadataRetentionConfig",
        "task_logs_retention_config": "taskLogsRetentionConfig",
    },
)
class ComposerEnvironmentConfigDataRetentionConfig:
    def __init__(
        self,
        *,
        airflow_metadata_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        task_logs_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param airflow_metadata_retention_config: airflow_metadata_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#airflow_metadata_retention_config ComposerEnvironment#airflow_metadata_retention_config}
        :param task_logs_retention_config: task_logs_retention_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#task_logs_retention_config ComposerEnvironment#task_logs_retention_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825432b7c61a0dc01c2bdcea5ea6997e438e19f11e4d929ae06a3bc711a29666)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig"]]]:
        '''airflow_metadata_retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#airflow_metadata_retention_config ComposerEnvironment#airflow_metadata_retention_config}
        '''
        result = self._values.get("airflow_metadata_retention_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig"]]], result)

    @builtins.property
    def task_logs_retention_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]]:
        '''task_logs_retention_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#task_logs_retention_config ComposerEnvironment#task_logs_retention_config}
        '''
        result = self._values.get("task_logs_retention_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigDataRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "retention_days": "retentionDays",
        "retention_mode": "retentionMode",
    },
)
class ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig:
    def __init__(
        self,
        *,
        retention_days: typing.Optional[jsii.Number] = None,
        retention_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retention_days: How many days data should be retained for. This field is supported for Cloud Composer environments in composer 3 and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#retention_days ComposerEnvironment#retention_days}
        :param retention_mode: Whether database retention is enabled or not. This field is supported for Cloud Composer environments in composer 3 and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#retention_mode ComposerEnvironment#retention_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41db014169569aac3c95f6368c2dcdc17bc182210d968094a4655babbedd31c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#retention_days ComposerEnvironment#retention_days}
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_mode(self) -> typing.Optional[builtins.str]:
        '''Whether database retention is enabled or not.

        This field is supported for Cloud Composer environments in composer 3 and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#retention_mode ComposerEnvironment#retention_mode}
        '''
        result = self._values.get("retention_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67d139bda6978efc157020ce32f0ca894c280613175cb890bf0a74430cba5072)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafa997a383b5cedee5e7db2a4670018b74e484066ab4a8ddf6d38bd6bc3a46f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01886439fc9490c134315b0bad37b04580628fb5d729c71e499bc559f79ee9e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b310f9866ac6980bdab347cd9111ce4a24938a4be38083a1d8e3004ad1251a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2b08a28287b29af4d6a74be34311938ff410ce202512c445abe3451c04e4fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8363698592b999781c2755ac6218fec447a13a3e60c2cc8826e7627d5abe6368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4005c941f97ce65eea2ee60b1765cf45124499cd84859cb24fb10e8a949ccf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f42b556485baf882c147bded1eedf8dc9a1258b0a5c245640bdbde4c8b30ddc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionMode")
    def retention_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionMode"))

    @retention_mode.setter
    def retention_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c15e4ce06ebbfcc309831c3e032ef23f8c056c259665eaaefab63e9d7dc25e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45302557dc380b9564f7b66ae6e8d036266aa8c03ca51b7bedc7f0ce1a4b5bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigDataRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18670ce1c82269a8c5d618df981e52eced8954bb66ff37e69d8f116faa08fa67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAirflowMetadataRetentionConfig")
    def put_airflow_metadata_retention_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46e59461ad7caa5110295d2cd957948ceeee8a0d895df1b15f06b0178c37b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAirflowMetadataRetentionConfig", [value]))

    @jsii.member(jsii_name="putTaskLogsRetentionConfig")
    def put_task_logs_retention_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5696f65409d46aefc6e3cebd20bb4d95efd6712743fb884d5fcde4374d5fe5c)
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
    ) -> ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList:
        return typing.cast(ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList, jsii.get(self, "airflowMetadataRetentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="taskLogsRetentionConfig")
    def task_logs_retention_config(
        self,
    ) -> "ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList":
        return typing.cast("ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList", jsii.get(self, "taskLogsRetentionConfig"))

    @builtins.property
    @jsii.member(jsii_name="airflowMetadataRetentionConfigInput")
    def airflow_metadata_retention_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]], jsii.get(self, "airflowMetadataRetentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="taskLogsRetentionConfigInput")
    def task_logs_retention_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig"]]], jsii.get(self, "taskLogsRetentionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigDataRetentionConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigDataRetentionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigDataRetentionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcd585ffed5d2aea59632dc9ea7a580609840944918832780df5d45dff78995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig",
    jsii_struct_bases=[],
    name_mapping={"storage_mode": "storageMode"},
)
class ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig:
    def __init__(self, *, storage_mode: typing.Optional[builtins.str] = None) -> None:
        '''
        :param storage_mode: Whether logs in cloud logging only is enabled or not. This field is supported for Cloud Composer environments in versions composer-2.0.32-airflow-2.1.4 and newer but not in composer-3* Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_mode ComposerEnvironment#storage_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0b24b89254dae3f1a2d91507938bfd58ae35bb309447a71fbd0d1e2cf9311e)
            check_type(argname="argument storage_mode", value=storage_mode, expected_type=type_hints["storage_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if storage_mode is not None:
            self._values["storage_mode"] = storage_mode

    @builtins.property
    def storage_mode(self) -> typing.Optional[builtins.str]:
        '''Whether logs in cloud logging only is enabled or not.

        This field is supported for Cloud Composer environments in versions composer-2.0.32-airflow-2.1.4 and newer but not in composer-3*

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_mode ComposerEnvironment#storage_mode}
        '''
        result = self._values.get("storage_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__741b3894e162589acfb35fcb4af262e4ea22b27ad190c04e4c511da5cecce6a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1bf2d1120de248e8668d74085470ec56a8a77b1e39ec6ed443ca2dde981690)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71928b81000f0ce39fce5cdf35d50fcb8f8413396e09106c8d6ddd4ac7b53805)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecd9ad99eb712b70a9922fbf34d83c3b0c4fc588362fefdab0e4a5fc09249fbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a2b82301e9b9b5264b34bd92e7c75d2af52525b5211e8a73f4d09a87306bbd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0278dc997fa628649ee284b55cc6828eca5037800f87a24d9039c99fbe854bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bde2495a572414017163b966f0fb83ab624d914830ce8441ab9505426f4964f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd2f0f9c93bb15785df4d987a05ebb5c0b32f5f7456735ac0dbafac96ea06f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904eec58f53aca76ef894d11de765178fe8d82947862e6bcbe1ab42bcc4eff6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDatabaseConfig",
    jsii_struct_bases=[],
    name_mapping={"machine_type": "machineType", "zone": "zone"},
)
class ComposerEnvironmentConfigDatabaseConfig:
    def __init__(
        self,
        *,
        machine_type: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_type: Optional. Cloud SQL machine type used by Airflow database. It has to be one of: db-n1-standard-2, db-n1-standard-4, db-n1-standard-8 or db-n1-standard-16. If not specified, db-n1-standard-2 will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        :param zone: Optional. Cloud SQL database preferred zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#zone ComposerEnvironment#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818af818997685510761d6a2f50839d356dfc85ba488b1542c25bf336667e891)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional. Cloud SQL database preferred zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#zone ComposerEnvironment#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigDatabaseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigDatabaseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__043d127e421770726372cd34919c2d55535771569a51d84b22188e22db6da19c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__375b817c25679baa6754b6ea30e9837fcdd6458ad99e5f626839736c9b4308f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a244ac7579906089283653a7021b5fc51e1141d173142facee4ddf95edc210e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigDatabaseConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigDatabaseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigDatabaseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d067cf0dfee4ec019e5e6fd910551286208049b50de6d7389f8128eab79b78ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class ComposerEnvironmentConfigEncryptionConfig:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Optional. Customer-managed Encryption Key available through Google's Key Management Service. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#kms_key_name ComposerEnvironment#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb5e57299eba67a0cf3239bd439586f61105fd1843ddfdc96e0f245701717b2b)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Optional. Customer-managed Encryption Key available through Google's Key Management Service. Cannot be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#kms_key_name ComposerEnvironment#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea9cac4c0e9dc5724e52e1ffd69f0cdfd8c59c592d3ec10117f6d4ed0b2be9ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2bd0aae8bda100784addfc3a9865c83ff7795a2520af828f462fcfb81f2d1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigEncryptionConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9985d17bcf34c23b81fb9074e0e51f9d138ea87d6655f245c90f8cc690959d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "end_time": "endTime",
        "recurrence": "recurrence",
        "start_time": "startTime",
    },
)
class ComposerEnvironmentConfigMaintenanceWindow:
    def __init__(
        self,
        *,
        end_time: builtins.str,
        recurrence: builtins.str,
        start_time: builtins.str,
    ) -> None:
        '''
        :param end_time: Maintenance window end time. It is used only to calculate the duration of the maintenance window. The value for end-time must be in the future, relative to 'start_time'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#end_time ComposerEnvironment#end_time}
        :param recurrence: Maintenance window recurrence. Format is a subset of RFC-5545 (https://tools.ietf.org/html/rfc5545) 'RRULE'. The only allowed values for 'FREQ' field are 'FREQ=DAILY' and 'FREQ=WEEKLY;BYDAY=...'. Example values: 'FREQ=WEEKLY;BYDAY=TU,WE', 'FREQ=DAILY'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#recurrence ComposerEnvironment#recurrence}
        :param start_time: Start time of the first recurrence of the maintenance window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#start_time ComposerEnvironment#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac65fb28b7e8c5b4c6fb528ba832c08b8c61e8975f3b60154f40986dd5ce90fd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#end_time ComposerEnvironment#end_time}
        '''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence(self) -> builtins.str:
        '''Maintenance window recurrence.

        Format is a subset of RFC-5545 (https://tools.ietf.org/html/rfc5545) 'RRULE'. The only allowed values for 'FREQ' field are 'FREQ=DAILY' and 'FREQ=WEEKLY;BYDAY=...'. Example values: 'FREQ=WEEKLY;BYDAY=TU,WE', 'FREQ=DAILY'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#recurrence ComposerEnvironment#recurrence}
        '''
        result = self._values.get("recurrence")
        assert result is not None, "Required property 'recurrence' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Start time of the first recurrence of the maintenance window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#start_time ComposerEnvironment#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0965ba1beb560c6a8b2fce35adf15cebceb56be4584fb369eedf82c7f8e73631)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a262d56e356164e625eccf30822f6305470305a1d14aa328dbca95d6f756ca9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrence"))

    @recurrence.setter
    def recurrence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0701a20a563e160d2f7caf0a2695d9b4253ed6930d7579e9fdea81b2a15012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70724a0e79f926016fa548ce980d16a05059db5c3283b7e4a2c1483e2244d03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigMaintenanceWindow]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21cb9376209b79b8ccd2734e21e57692852e96fbb6c32bc3f18184cc5fd7c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMasterAuthorizedNetworksConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "cidr_blocks": "cidrBlocks"},
)
class ComposerEnvironmentConfigMasterAuthorizedNetworksConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cidr_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Whether or not master authorized networks is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        :param cidr_blocks: cidr_blocks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cidr_blocks ComposerEnvironment#cidr_blocks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fddc2032e443b3b948d4737960119242f2065bda140f1805dac132f7d4012e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cidr_blocks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks"]]]:
        '''cidr_blocks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cidr_blocks ComposerEnvironment#cidr_blocks}
        '''
        result = self._values.get("cidr_blocks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigMasterAuthorizedNetworksConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks",
    jsii_struct_bases=[],
    name_mapping={"cidr_block": "cidrBlock", "display_name": "displayName"},
)
class ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks:
    def __init__(
        self,
        *,
        cidr_block: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cidr_block: cidr_block must be specified in CIDR notation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cidr_block ComposerEnvironment#cidr_block}
        :param display_name: display_name is a field for users to identify CIDR blocks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#display_name ComposerEnvironment#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24946083b6d182ecf4380de47e7120cbe09a67f3668abaf4bfd2ea9aa50d7a02)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cidr_block ComposerEnvironment#cidr_block}
        '''
        result = self._values.get("cidr_block")
        assert result is not None, "Required property 'cidr_block' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''display_name is a field for users to identify CIDR blocks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#display_name ComposerEnvironment#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fd9950e9d202e663ca3ee52e7dd84bdb89ba5896a416919052406bd9a433c98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01a71d43aeb13e7121c0f0229c23f973b66b87e0583af44130410bf1c99eac7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41470b14a3ff9185cb37b485879856730ed0a1e649b4b898f06710a387b11cf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__772e0a14d37955e6aef8a9bcee9f2954f66c33cb4533abd7bf55a47e174eea6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77890d6eec39b355ebfadec3984366dcec4162c38b4d405b7fa09696f34725ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7390094f4cea328b386a742b023c6877fa91616f4b767ca6a61a5316e7091a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__735df287e01ee431922ae6be97b15b77eebb9971887f851f184d11cb750c55e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e945ae84b79df00027850713ba117bb421745e0e86b94621f44ab7bc60abc11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485be438e8eac405748de85994d806cf8b2077f2fb1ad68efe0036da610cafe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c187e343af2f6672fcb1a676ec62218fb6348edd9bceacb2ef1001a1d57fd28e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdbb4ffa7e317729350c605b90465d1612e193ef9343713ac715848f925003e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCidrBlocks")
    def put_cidr_blocks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf8ba1205b72a7aa0d878f48443880ca6ea5312938a9aeaa3308a5e424796d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCidrBlocks", [value]))

    @jsii.member(jsii_name="resetCidrBlocks")
    def reset_cidr_blocks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrBlocks", []))

    @builtins.property
    @jsii.member(jsii_name="cidrBlocks")
    def cidr_blocks(
        self,
    ) -> ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList:
        return typing.cast(ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList, jsii.get(self, "cidrBlocks"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlocksInput")
    def cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]], jsii.get(self, "cidrBlocksInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__af180a45ec062ce5b65406ebb9ae02fa6167af9eede0d0165cbd3320eb0d6a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigMasterAuthorizedNetworksConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigMasterAuthorizedNetworksConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigMasterAuthorizedNetworksConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccc798ea665d4f839f11280a4c16b58ecb5f7067ad8be83aa1e2827f612eda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigNodeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "composer_internal_ipv4_cidr_block": "composerInternalIpv4CidrBlock",
        "composer_network_attachment": "composerNetworkAttachment",
        "disk_size_gb": "diskSizeGb",
        "enable_ip_masq_agent": "enableIpMasqAgent",
        "ip_allocation_policy": "ipAllocationPolicy",
        "machine_type": "machineType",
        "network": "network",
        "oauth_scopes": "oauthScopes",
        "service_account": "serviceAccount",
        "subnetwork": "subnetwork",
        "tags": "tags",
        "zone": "zone",
    },
)
class ComposerEnvironmentConfigNodeConfig:
    def __init__(
        self,
        *,
        composer_internal_ipv4_cidr_block: typing.Optional[builtins.str] = None,
        composer_network_attachment: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        enable_ip_masq_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_allocation_policy: typing.Optional[typing.Union["ComposerEnvironmentConfigNodeConfigIpAllocationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_account: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param composer_internal_ipv4_cidr_block: IPv4 cidr range that will be used by Composer internal components. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#composer_internal_ipv4_cidr_block ComposerEnvironment#composer_internal_ipv4_cidr_block}
        :param composer_network_attachment: PSC (Private Service Connect) Network entry point. Customers can pre-create the Network Attachment and point Cloud Composer environment to use. It is possible to share network attachment among many environments, provided enough IP addresses are available. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#composer_network_attachment ComposerEnvironment#composer_network_attachment}
        :param disk_size_gb: The disk size in GB used for node VMs. Minimum size is 20GB. If unspecified, defaults to 100GB. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#disk_size_gb ComposerEnvironment#disk_size_gb}
        :param enable_ip_masq_agent: Deploys 'ip-masq-agent' daemon set in the GKE cluster and defines nonMasqueradeCIDRs equals to pod IP range so IP masquerading is used for all destination addresses, except between pods traffic. See: https://cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_ip_masq_agent ComposerEnvironment#enable_ip_masq_agent}
        :param ip_allocation_policy: ip_allocation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#ip_allocation_policy ComposerEnvironment#ip_allocation_policy}
        :param machine_type: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        :param network: The Compute Engine machine type used for cluster instances, specified as a name or relative resource name. For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. The network must belong to the environment's project. If unspecified, the "default" network ID in the environment's project is used. If a Custom Subnet Network is provided, subnetwork must also be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#network ComposerEnvironment#network}
        :param oauth_scopes: The set of Google API scopes to be made available on all node VMs. Cannot be updated. If empty, defaults to ["https://www.googleapis.com/auth/cloud-platform"]. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#oauth_scopes ComposerEnvironment#oauth_scopes}
        :param service_account: The Google Cloud Platform Service Account to be used by the node VMs. If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. If given, note that the service account must have roles/composer.worker for any GCP resources created under the Cloud Composer Environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#service_account ComposerEnvironment#service_account}
        :param subnetwork: The Compute Engine subnetwork to be used for machine communications, specified as a self-link, relative resource name (e.g. "projects/{project}/regions/{region}/subnetworks/{subnetwork}"), or by name. If subnetwork is provided, network must also be provided and the subnetwork must belong to the enclosing environment's project and region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#subnetwork ComposerEnvironment#subnetwork}
        :param tags: The list of instance tags applied to all node VMs. Tags are used to identify valid sources or targets for network firewalls. Each tag within the list must comply with RFC1035. Cannot be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#tags ComposerEnvironment#tags}
        :param zone: The Compute Engine zone in which to deploy the VMs running the Apache Airflow software, specified as the zone name or relative resource name (e.g. "projects/{project}/zones/{zone}"). Must belong to the enclosing environment's project and region. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#zone ComposerEnvironment#zone}
        '''
        if isinstance(ip_allocation_policy, dict):
            ip_allocation_policy = ComposerEnvironmentConfigNodeConfigIpAllocationPolicy(**ip_allocation_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee3a648d418e87474e7e3e5d07985b54ef4ff1138afec41d6d55403a9639263)
            check_type(argname="argument composer_internal_ipv4_cidr_block", value=composer_internal_ipv4_cidr_block, expected_type=type_hints["composer_internal_ipv4_cidr_block"])
            check_type(argname="argument composer_network_attachment", value=composer_network_attachment, expected_type=type_hints["composer_network_attachment"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument enable_ip_masq_agent", value=enable_ip_masq_agent, expected_type=type_hints["enable_ip_masq_agent"])
            check_type(argname="argument ip_allocation_policy", value=ip_allocation_policy, expected_type=type_hints["ip_allocation_policy"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#composer_internal_ipv4_cidr_block ComposerEnvironment#composer_internal_ipv4_cidr_block}
        '''
        result = self._values.get("composer_internal_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def composer_network_attachment(self) -> typing.Optional[builtins.str]:
        '''PSC (Private Service Connect) Network entry point.

        Customers can pre-create the Network Attachment and point Cloud Composer environment to use. It is possible to share network attachment among many environments, provided enough IP addresses are available.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#composer_network_attachment ComposerEnvironment#composer_network_attachment}
        '''
        result = self._values.get("composer_network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The disk size in GB used for node VMs.

        Minimum size is 20GB. If unspecified, defaults to 100GB. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#disk_size_gb ComposerEnvironment#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ip_masq_agent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deploys 'ip-masq-agent' daemon set in the GKE cluster and defines nonMasqueradeCIDRs equals to pod IP range so IP masquerading is used for all destination addresses, except between pods traffic.

        See: https://cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_ip_masq_agent ComposerEnvironment#enable_ip_masq_agent}
        '''
        result = self._values.get("enable_ip_masq_agent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_allocation_policy(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigNodeConfigIpAllocationPolicy"]:
        '''ip_allocation_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#ip_allocation_policy ComposerEnvironment#ip_allocation_policy}
        '''
        result = self._values.get("ip_allocation_policy")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigNodeConfigIpAllocationPolicy"], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine machine type used for cluster instances, specified as a name or relative resource name.

        For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine machine type used for cluster instances, specified as a name or relative resource name.

        For example: "projects/{project}/zones/{zone}/machineTypes/{machineType}". Must belong to the enclosing environment's project and region/zone. The network must belong to the environment's project. If unspecified, the "default" network ID in the environment's project is used. If a Custom Subnet Network is provided, subnetwork must also be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#network ComposerEnvironment#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of Google API scopes to be made available on all node VMs.

        Cannot be updated. If empty, defaults to ["https://www.googleapis.com/auth/cloud-platform"]. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#oauth_scopes ComposerEnvironment#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform Service Account to be used by the node VMs.

        If a service account is not specified, the "default" Compute Engine service account is used. Cannot be updated. If given, note that the service account must have roles/composer.worker for any GCP resources created under the Cloud Composer Environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#service_account ComposerEnvironment#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine subnetwork to be used for machine communications, specified as a self-link, relative resource name (e.g. "projects/{project}/regions/{region}/subnetworks/{subnetwork}"), or by name. If subnetwork is provided, network must also be provided and the subnetwork must belong to the enclosing environment's project and region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#subnetwork ComposerEnvironment#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of instance tags applied to all node VMs.

        Tags are used to identify valid sources or targets for network firewalls. Each tag within the list must comply with RFC1035. Cannot be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#tags ComposerEnvironment#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone in which to deploy the VMs running the Apache Airflow software, specified as the zone name or relative resource name (e.g. "projects/{project}/zones/{zone}"). Must belong to the enclosing environment's project and region. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#zone ComposerEnvironment#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigNodeConfigIpAllocationPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_ipv4_cidr_block": "clusterIpv4CidrBlock",
        "cluster_secondary_range_name": "clusterSecondaryRangeName",
        "services_ipv4_cidr_block": "servicesIpv4CidrBlock",
        "services_secondary_range_name": "servicesSecondaryRangeName",
        "use_ip_aliases": "useIpAliases",
    },
)
class ComposerEnvironmentConfigNodeConfigIpAllocationPolicy:
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
        :param cluster_ipv4_cidr_block: The IP address range used to allocate IP addresses to pods in the cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cluster_ipv4_cidr_block ComposerEnvironment#cluster_ipv4_cidr_block}
        :param cluster_secondary_range_name: The name of the cluster's secondary range used to allocate IP addresses to pods. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cluster_secondary_range_name ComposerEnvironment#cluster_secondary_range_name}
        :param services_ipv4_cidr_block: The IP address range used to allocate IP addresses in this cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#services_ipv4_cidr_block ComposerEnvironment#services_ipv4_cidr_block}
        :param services_secondary_range_name: The name of the services' secondary range used to allocate IP addresses to the cluster. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#services_secondary_range_name ComposerEnvironment#services_secondary_range_name}
        :param use_ip_aliases: Whether or not to enable Alias IPs in the GKE cluster. If true, a VPC-native cluster is created. Defaults to true if the ip_allocation_policy block is present in config. This field is only supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use VPC-native GKE clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#use_ip_aliases ComposerEnvironment#use_ip_aliases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf90c7993267d2883df452ab884e2a4405ce17573a935346e4a953f77d5587c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cluster_ipv4_cidr_block ComposerEnvironment#cluster_ipv4_cidr_block}
        '''
        result = self._values.get("cluster_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_secondary_range_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster's secondary range used to allocate IP addresses to pods.

        Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cluster_secondary_range_name ComposerEnvironment#cluster_secondary_range_name}
        '''
        result = self._values.get("cluster_secondary_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP address range used to allocate IP addresses in this cluster.

        For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#services_ipv4_cidr_block ComposerEnvironment#services_ipv4_cidr_block}
        '''
        result = self._values.get("services_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services_secondary_range_name(self) -> typing.Optional[builtins.str]:
        '''The name of the services' secondary range used to allocate IP addresses to the cluster.

        Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#services_secondary_range_name ComposerEnvironment#services_secondary_range_name}
        '''
        result = self._values.get("services_secondary_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ip_aliases(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to enable Alias IPs in the GKE cluster.

        If true, a VPC-native cluster is created. Defaults to true if the ip_allocation_policy block is present in config. This field is only supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use VPC-native GKE clusters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#use_ip_aliases ComposerEnvironment#use_ip_aliases}
        '''
        result = self._values.get("use_ip_aliases")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigNodeConfigIpAllocationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c59bc2b5ad96c6080c05b2b5c1f5e14c41fed87016385bb91ed7b7ac9e99a91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__774f48dec144c04e8cacc6ca4b05810f5628f0da269ed4eab5ceacc241d16c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterSecondaryRangeName")
    def cluster_secondary_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterSecondaryRangeName"))

    @cluster_secondary_range_name.setter
    def cluster_secondary_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ea5c5d0c5b209efd12ae0665929c6aca18083b6aeb7a7025158050b1585b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterSecondaryRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesIpv4CidrBlock")
    def services_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicesIpv4CidrBlock"))

    @services_ipv4_cidr_block.setter
    def services_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38232f4155b9895787834935aaf731148de827567e0c9e605d75817f32a791b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicesSecondaryRangeName")
    def services_secondary_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicesSecondaryRangeName"))

    @services_secondary_range_name.setter
    def services_secondary_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052e55e09bbf4c3738fa014b95db7fbf023b0fc7910bb982a195089b79cef9a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edbef236edfccd284135af86ab10efdc90d0a415f739b86aa469ad0caf7ea52b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIpAliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8e62c2a53ccf772840f9ce1713076483db3aa39262ef9b5a4209b63908f0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea87e8ba81e4e4ae951b0afe43f34313656bba10e4dab0e4ba5ca6f8b46e8435)
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
        :param cluster_ipv4_cidr_block: The IP address range used to allocate IP addresses to pods in the cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cluster_ipv4_cidr_block ComposerEnvironment#cluster_ipv4_cidr_block}
        :param cluster_secondary_range_name: The name of the cluster's secondary range used to allocate IP addresses to pods. Specify either cluster_secondary_range_name or cluster_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cluster_secondary_range_name ComposerEnvironment#cluster_secondary_range_name}
        :param services_ipv4_cidr_block: The IP address range used to allocate IP addresses in this cluster. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Set to blank to have GKE choose a range with the default size. Set to /netmask (e.g. /14) to have GKE choose a range with a specific netmask. Set to a CIDR notation (e.g. 10.96.0.0/14) from the RFC-1918 private networks (e.g. 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) to pick a specific range to use. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#services_ipv4_cidr_block ComposerEnvironment#services_ipv4_cidr_block}
        :param services_secondary_range_name: The name of the services' secondary range used to allocate IP addresses to the cluster. Specify either services_secondary_range_name or services_ipv4_cidr_block but not both. For Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*, this field is applicable only when use_ip_aliases is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#services_secondary_range_name ComposerEnvironment#services_secondary_range_name}
        :param use_ip_aliases: Whether or not to enable Alias IPs in the GKE cluster. If true, a VPC-native cluster is created. Defaults to true if the ip_allocation_policy block is present in config. This field is only supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use VPC-native GKE clusters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#use_ip_aliases ComposerEnvironment#use_ip_aliases}
        '''
        value = ComposerEnvironmentConfigNodeConfigIpAllocationPolicy(
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
    ) -> ComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference:
        return typing.cast(ComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference, jsii.get(self, "ipAllocationPolicy"))

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
    ) -> typing.Optional[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy], jsii.get(self, "ipAllocationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb482c657715a00ef2fe6e8f3c722c9da80ffbcab1b109f5efda9828dce3b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "composerInternalIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="composerNetworkAttachment")
    def composer_network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "composerNetworkAttachment"))

    @composer_network_attachment.setter
    def composer_network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dd26d527672ea32f57adc3d8ca8cc6061755cc4bf22c274606761197ebd92c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "composerNetworkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618956bd4493d2ce1e93f68228fb9b49df6805f583fe74c935acd1301f1d9d57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__355c2d6eb0277f4e6c14b96aa3d807bcc396eb5086e9e5bed6782ffb55752292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpMasqAgent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f37f5466736e7fd1ed86c6eefa66e9921348258bb42bf932735d901559eeb5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5236cea288cff62859a8e89283bb47064bfe6f642d384086b7a0c041bc968655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d93c5d0937a0025365b9c6bdc6f07851d753fbcb109658ba77a03d80d6ad16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e99e044e29159cf9c52a10e7e18c0367f92f498ab679bbf96b791730eb55c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492a3adecc7a87091838968c91b0647fc12a86a50ba0884a83acd3972f4c6bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01398324b2a42853c13d8d83bc0af162cfb02b600cbef5bac5a45414efa3fc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a325afd1e84e3d076e2874c4c096d7145d471ded39e2a6f9eeb74a13a27bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComposerEnvironmentConfigNodeConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba80e25041bf5eaf02acee84f5228487f08c6f26cd5a6c25a6908e283721ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigPrivateEnvironmentConfig",
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
class ComposerEnvironmentConfigPrivateEnvironmentConfig:
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
        :param cloud_composer_connection_subnetwork: When specified, the environment will use Private Service Connect instead of VPC peerings to connect to Cloud SQL in the Tenant Project, and the PSC endpoint in the Customer Project will use an IP address from this subnetwork. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_composer_connection_subnetwork ComposerEnvironment#cloud_composer_connection_subnetwork}
        :param cloud_composer_network_ipv4_cidr_block: The CIDR block from which IP range for Cloud Composer Network in tenant project will be reserved. Needs to be disjoint from private_cluster_config.master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_composer_network_ipv4_cidr_block ComposerEnvironment#cloud_composer_network_ipv4_cidr_block}
        :param cloud_sql_ipv4_cidr_block: The CIDR block from which IP range in tenant project will be reserved for Cloud SQL. Needs to be disjoint from web_server_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_sql_ipv4_cidr_block ComposerEnvironment#cloud_sql_ipv4_cidr_block}
        :param connection_type: Mode of internal communication within the Composer environment. Must be one of "VPC_PEERING" or "PRIVATE_SERVICE_CONNECT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#connection_type ComposerEnvironment#connection_type}
        :param enable_private_endpoint: If true, access to the public endpoint of the GKE cluster is denied. If this field is set to true, ip_allocation_policy.use_ip_aliases must be set to true for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_endpoint ComposerEnvironment#enable_private_endpoint}
        :param enable_privately_used_public_ips: When enabled, IPs from public (non-RFC1918) ranges can be used for ip_allocation_policy.cluster_ipv4_cidr_block and ip_allocation_policy.service_ipv4_cidr_block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_privately_used_public_ips ComposerEnvironment#enable_privately_used_public_ips}
        :param master_ipv4_cidr_block: The IP range in CIDR notation to use for the hosted master network. This range is used for assigning internal IP addresses to the cluster master or set of masters and to the internal load balancer virtual IP. This range must not overlap with any other ranges in use within the cluster's network. If left blank, the default value of '172.16.0.0/28' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#master_ipv4_cidr_block ComposerEnvironment#master_ipv4_cidr_block}
        :param web_server_ipv4_cidr_block: The CIDR block from which IP range for web server will be reserved. Needs to be disjoint from master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_ipv4_cidr_block ComposerEnvironment#web_server_ipv4_cidr_block}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136264cc2d36d96867b641484db61ef144349da161ac0550238daa9f9fb23aa3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_composer_connection_subnetwork ComposerEnvironment#cloud_composer_connection_subnetwork}
        '''
        result = self._values.get("cloud_composer_connection_subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_composer_network_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The CIDR block from which IP range for Cloud Composer Network in tenant project will be reserved.

        Needs to be disjoint from private_cluster_config.master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-2.*.*-airflow-*.*.* and newer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_composer_network_ipv4_cidr_block ComposerEnvironment#cloud_composer_network_ipv4_cidr_block}
        '''
        result = self._values.get("cloud_composer_network_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_sql_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The CIDR block from which IP range in tenant project will be reserved for Cloud SQL.

        Needs to be disjoint from web_server_ipv4_cidr_block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_sql_ipv4_cidr_block ComposerEnvironment#cloud_sql_ipv4_cidr_block}
        '''
        result = self._values.get("cloud_sql_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''Mode of internal communication within the Composer environment. Must be one of "VPC_PEERING" or "PRIVATE_SERVICE_CONNECT".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#connection_type ComposerEnvironment#connection_type}
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_private_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, access to the public endpoint of the GKE cluster is denied.

        If this field is set to true, ip_allocation_policy.use_ip_aliases must be set to true for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_private_endpoint ComposerEnvironment#enable_private_endpoint}
        '''
        result = self._values.get("enable_private_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_privately_used_public_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, IPs from public (non-RFC1918) ranges can be used for ip_allocation_policy.cluster_ipv4_cidr_block and ip_allocation_policy.service_ipv4_cidr_block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enable_privately_used_public_ips ComposerEnvironment#enable_privately_used_public_ips}
        '''
        result = self._values.get("enable_privately_used_public_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def master_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The IP range in CIDR notation to use for the hosted master network.

        This range is used for assigning internal IP addresses to the cluster master or set of masters and to the internal load balancer virtual IP. This range must not overlap with any other ranges in use within the cluster's network. If left blank, the default value of '172.16.0.0/28' is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#master_ipv4_cidr_block ComposerEnvironment#master_ipv4_cidr_block}
        '''
        result = self._values.get("master_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_server_ipv4_cidr_block(self) -> typing.Optional[builtins.str]:
        '''The CIDR block from which IP range for web server will be reserved.

        Needs to be disjoint from master_ipv4_cidr_block and cloud_sql_ipv4_cidr_block. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_ipv4_cidr_block ComposerEnvironment#web_server_ipv4_cidr_block}
        '''
        result = self._values.get("web_server_ipv4_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigPrivateEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70bf21af434ff5809e0cd896dc7df83eabf1388c0fe65ccc5581353b48d3b95f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cffe25758a872aad3ff91cee9140767b4a734671b6c07b0812db574748056bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudComposerConnectionSubnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudComposerNetworkIpv4CidrBlock")
    def cloud_composer_network_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudComposerNetworkIpv4CidrBlock"))

    @cloud_composer_network_ipv4_cidr_block.setter
    def cloud_composer_network_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd69a9a4b05b4fdc2e6aecca0de20ffe52d5185a136232ff3cff2f4117eee5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudComposerNetworkIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudSqlIpv4CidrBlock")
    def cloud_sql_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlIpv4CidrBlock"))

    @cloud_sql_ipv4_cidr_block.setter
    def cloud_sql_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c15ba22d93db5644a8028e361fd9f2276081a61d103bd10d19690bbe07aa835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionType"))

    @connection_type.setter
    def connection_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288978ff95191bd2596d2328a6209d5ed2533930f06610b0654307f659c8b03a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6afb8a343ab9acc9fa710bb10e6d3bd5fd1a1e6c8176d429306c3bc8b748360d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2a47759a591cbb5f0030c734fdb2aa1b3f7e6383945786a0c71a02fcaa97912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivatelyUsedPublicIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterIpv4CidrBlock")
    def master_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterIpv4CidrBlock"))

    @master_ipv4_cidr_block.setter
    def master_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5eb6a0b67c47cbe26c83db238572511d6d7ec6076ff45630fba065b569bcfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webServerIpv4CidrBlock")
    def web_server_ipv4_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webServerIpv4CidrBlock"))

    @web_server_ipv4_cidr_block.setter
    def web_server_ipv4_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b6f881c5b65e30ac171795a0ebbe9ddf5a68b3d8296ba1dcd33d399d68dfd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webServerIpv4CidrBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigPrivateEnvironmentConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigPrivateEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigPrivateEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e56e77f10cd20f946682b4912007d6c79c0881465a3b7bb93e10947fd973f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigRecoveryConfig",
    jsii_struct_bases=[],
    name_mapping={"scheduled_snapshots_config": "scheduledSnapshotsConfig"},
)
class ComposerEnvironmentConfigRecoveryConfig:
    def __init__(
        self,
        *,
        scheduled_snapshots_config: typing.Optional[typing.Union["ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled_snapshots_config: scheduled_snapshots_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduled_snapshots_config ComposerEnvironment#scheduled_snapshots_config}
        '''
        if isinstance(scheduled_snapshots_config, dict):
            scheduled_snapshots_config = ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(**scheduled_snapshots_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488158e036c81570d00e4f2ad53829c1e5bc627a8e7dbd8bdda0bec4e3514fa0)
            check_type(argname="argument scheduled_snapshots_config", value=scheduled_snapshots_config, expected_type=type_hints["scheduled_snapshots_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scheduled_snapshots_config is not None:
            self._values["scheduled_snapshots_config"] = scheduled_snapshots_config

    @builtins.property
    def scheduled_snapshots_config(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"]:
        '''scheduled_snapshots_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduled_snapshots_config ComposerEnvironment#scheduled_snapshots_config}
        '''
        result = self._values.get("scheduled_snapshots_config")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigRecoveryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigRecoveryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigRecoveryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40bc1fbcbdc14197e7261887650ab3b05483e8ac944292224e42590b2d660c3e)
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
        :param enabled: When enabled, Cloud Composer periodically saves snapshots of your environment to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        :param snapshot_creation_schedule: Snapshot schedule, in the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#snapshot_creation_schedule ComposerEnvironment#snapshot_creation_schedule}
        :param snapshot_location: the URI of a bucket folder where to save the snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#snapshot_location ComposerEnvironment#snapshot_location}
        :param time_zone: A time zone for the schedule. This value is a time offset and does not take into account daylight saving time changes. Valid values are from UTC-12 to UTC+12. Examples: UTC, UTC-01, UTC+03. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#time_zone ComposerEnvironment#time_zone}
        '''
        value = ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(
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
    ) -> "ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference":
        return typing.cast("ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference", jsii.get(self, "scheduledSnapshotsConfig"))

    @builtins.property
    @jsii.member(jsii_name="scheduledSnapshotsConfigInput")
    def scheduled_snapshots_config_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig"], jsii.get(self, "scheduledSnapshotsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigRecoveryConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigRecoveryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigRecoveryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9bd1531fea9f53610f7e2fa282d7043ceccd09bbd3cc814a212f5a7ae5d8fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "snapshot_creation_schedule": "snapshotCreationSchedule",
        "snapshot_location": "snapshotLocation",
        "time_zone": "timeZone",
    },
)
class ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        snapshot_creation_schedule: typing.Optional[builtins.str] = None,
        snapshot_location: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: When enabled, Cloud Composer periodically saves snapshots of your environment to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        :param snapshot_creation_schedule: Snapshot schedule, in the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#snapshot_creation_schedule ComposerEnvironment#snapshot_creation_schedule}
        :param snapshot_location: the URI of a bucket folder where to save the snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#snapshot_location ComposerEnvironment#snapshot_location}
        :param time_zone: A time zone for the schedule. This value is a time offset and does not take into account daylight saving time changes. Valid values are from UTC-12 to UTC+12. Examples: UTC, UTC-01, UTC+03. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#time_zone ComposerEnvironment#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ca79626eaf66a96792cbc6c3406154a0b9cb8c214695e27501cf2d230ccb98)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def snapshot_creation_schedule(self) -> typing.Optional[builtins.str]:
        '''Snapshot schedule, in the unix-cron format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#snapshot_creation_schedule ComposerEnvironment#snapshot_creation_schedule}
        '''
        result = self._values.get("snapshot_creation_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_location(self) -> typing.Optional[builtins.str]:
        '''the URI of a bucket folder where to save the snapshot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#snapshot_location ComposerEnvironment#snapshot_location}
        '''
        result = self._values.get("snapshot_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''A time zone for the schedule.

        This value is a time offset and does not take into account daylight saving time changes. Valid values are from UTC-12 to UTC+12. Examples: UTC, UTC-01, UTC+03.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#time_zone ComposerEnvironment#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a1ec61992be19f731831a9cebd47e4d881dbc3615d9986934f61fed2cc8605)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3130a3e331f82589bfd482ef25b138b4fdc398f99751a49bd1a48ec17f91000e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotCreationSchedule")
    def snapshot_creation_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotCreationSchedule"))

    @snapshot_creation_schedule.setter
    def snapshot_creation_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ffdb61ea36028a53c9f221c4f585600a6652d39346b699ad04cafc31bb4deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotCreationSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotLocation")
    def snapshot_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotLocation"))

    @snapshot_location.setter
    def snapshot_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad71a4b2d603d319389eba6db62f3cd4a55f67aa72579d8bd10431490a6d9de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811f049cd6a211353eeb39a6f5a65971f0696dee3f12012e14d512a34d836280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8caa9be6e5bd34d5b96aa1b93f4f28530ed4ef9300f7d9ba48f3efdc9b1d6880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigSoftwareConfig",
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
class ComposerEnvironmentConfigSoftwareConfig:
    def __init__(
        self,
        *,
        airflow_config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cloud_data_lineage_integration: typing.Optional[typing.Union["ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image_version: typing.Optional[builtins.str] = None,
        pypi_packages: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_version: typing.Optional[builtins.str] = None,
        scheduler_count: typing.Optional[jsii.Number] = None,
        web_server_plugins_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param airflow_config_overrides: Apache Airflow configuration properties to override. Property keys contain the section and property names, separated by a hyphen, for example "core-dags_are_paused_at_creation". Section names must not contain hyphens ("-"), opening square brackets ("["), or closing square brackets ("]"). The property name must not be empty and cannot contain "=" or ";". Section and property names cannot contain characters: "." Apache Airflow configuration property names must be written in snake_case. Property values can contain any character, and can be written in any lower/upper case format. Certain Apache Airflow configuration property values are blacklisted, and cannot be overridden. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#airflow_config_overrides ComposerEnvironment#airflow_config_overrides}
        :param cloud_data_lineage_integration: cloud_data_lineage_integration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_data_lineage_integration ComposerEnvironment#cloud_data_lineage_integration}
        :param env_variables: Additional environment variables to provide to the Apache Airflow scheduler, worker, and webserver processes. Environment variable names must match the regular expression [a-zA-Z_][a-zA-Z0-9_]*. They cannot specify Apache Airflow software configuration overrides (they cannot match the regular expression AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+), and they cannot match any of the following reserved names: AIRFLOW_HOME C_FORCE_ROOT CONTAINER_NAME DAGS_FOLDER GCP_PROJECT GCS_BUCKET GKE_CLUSTER_NAME SQL_DATABASE SQL_INSTANCE SQL_PASSWORD SQL_PROJECT SQL_REGION SQL_USER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#env_variables ComposerEnvironment#env_variables}
        :param image_version: The version of the software running in the environment. This encapsulates both the version of Cloud Composer functionality and the version of Apache Airflow. It must match the regular expression composer-([0-9]+(.[0-9]+.[0-9]+(-preview.[0-9]+)?)?|latest)-airflow-([0-9]+(.[0-9]+(.[0-9]+)?)?). The Cloud Composer portion of the image version is a full semantic version, or an alias in the form of major version number or 'latest'. The Apache Airflow portion of the image version is a full semantic version that points to one of the supported Apache Airflow versions, or an alias in the form of only major or major.minor versions specified. See documentation for more details and version list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#image_version ComposerEnvironment#image_version}
        :param pypi_packages: Custom Python Package Index (PyPI) packages to be installed in the environment. Keys refer to the lowercase package name (e.g. "numpy"). Values are the lowercase extras and version specifier (e.g. "==1.12.0", "[devel,gcp_api]", "[devel]>=1.8.2, <1.9.2"). To specify a package without pinning it to a version specifier, use the empty string as the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#pypi_packages ComposerEnvironment#pypi_packages}
        :param python_version: The major version of Python used to run the Apache Airflow scheduler, worker, and webserver processes. Can be set to '2' or '3'. If not specified, the default is '2'. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use Python major version 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#python_version ComposerEnvironment#python_version}
        :param scheduler_count: The number of schedulers for Airflow. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-2.*.*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduler_count ComposerEnvironment#scheduler_count}
        :param web_server_plugins_mode: Should be either 'ENABLED' or 'DISABLED'. Defaults to 'ENABLED'. Used in Composer 3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_plugins_mode ComposerEnvironment#web_server_plugins_mode}
        '''
        if isinstance(cloud_data_lineage_integration, dict):
            cloud_data_lineage_integration = ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration(**cloud_data_lineage_integration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2f296d44ab927909be3266f0ae36edf1c8b5f336a066dd4a9af327a7767815)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#airflow_config_overrides ComposerEnvironment#airflow_config_overrides}
        '''
        result = self._values.get("airflow_config_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cloud_data_lineage_integration(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration"]:
        '''cloud_data_lineage_integration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cloud_data_lineage_integration ComposerEnvironment#cloud_data_lineage_integration}
        '''
        result = self._values.get("cloud_data_lineage_integration")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration"], result)

    @builtins.property
    def env_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional environment variables to provide to the Apache Airflow scheduler, worker, and webserver processes.

        Environment variable names must match the regular expression [a-zA-Z_][a-zA-Z0-9_]*. They cannot specify Apache Airflow software configuration overrides (they cannot match the regular expression AIRFLOW__[A-Z0-9_]+__[A-Z0-9_]+), and they cannot match any of the following reserved names: AIRFLOW_HOME C_FORCE_ROOT CONTAINER_NAME DAGS_FOLDER GCP_PROJECT GCS_BUCKET GKE_CLUSTER_NAME SQL_DATABASE SQL_INSTANCE SQL_PASSWORD SQL_PROJECT SQL_REGION SQL_USER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#env_variables ComposerEnvironment#env_variables}
        '''
        result = self._values.get("env_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''The version of the software running in the environment.

        This encapsulates both the version of Cloud Composer functionality and the version of Apache Airflow. It must match the regular expression composer-([0-9]+(.[0-9]+.[0-9]+(-preview.[0-9]+)?)?|latest)-airflow-([0-9]+(.[0-9]+(.[0-9]+)?)?). The Cloud Composer portion of the image version is a full semantic version, or an alias in the form of major version number or 'latest'. The Apache Airflow portion of the image version is a full semantic version that points to one of the supported Apache Airflow versions, or an alias in the form of only major or major.minor versions specified. See documentation for more details and version list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#image_version ComposerEnvironment#image_version}
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pypi_packages(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom Python Package Index (PyPI) packages to be installed in the environment.

        Keys refer to the lowercase package name (e.g. "numpy"). Values are the lowercase extras and version specifier (e.g. "==1.12.0", "[devel,gcp_api]", "[devel]>=1.8.2, <1.9.2"). To specify a package without pinning it to a version specifier, use the empty string as the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#pypi_packages ComposerEnvironment#pypi_packages}
        '''
        result = self._values.get("pypi_packages")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_version(self) -> typing.Optional[builtins.str]:
        '''The major version of Python used to run the Apache Airflow scheduler, worker, and webserver processes.

        Can be set to '2' or '3'. If not specified, the default is '2'. Cannot be updated. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-*.*.*. Environments in newer versions always use Python major version 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#python_version ComposerEnvironment#python_version}
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduler_count(self) -> typing.Optional[jsii.Number]:
        '''The number of schedulers for Airflow. This field is supported for Cloud Composer environments in versions composer-1.*.*-airflow-2.*.*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduler_count ComposerEnvironment#scheduler_count}
        '''
        result = self._values.get("scheduler_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def web_server_plugins_mode(self) -> typing.Optional[builtins.str]:
        '''Should be either 'ENABLED' or 'DISABLED'. Defaults to 'ENABLED'. Used in Composer 3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server_plugins_mode ComposerEnvironment#web_server_plugins_mode}
        '''
        result = self._values.get("web_server_plugins_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether or not Cloud Data Lineage integration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a697b7dd0a807390feefce5227a14bfc8e9f26f1f91aef3788b51de2948a50)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not Cloud Data Lineage integration is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d8bc76fa888fd46ae66b93a99a8eecc7842e5fe198aa22c7ccbe2edb78ed0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d08aa80ecc60b699b0ef0c468ddca7870230dbd60b89664e04b0d48aefbe34c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2a909c2f5c3adfa468c3b6741d4c3e9edb1692e21f160c0d127f9746a80334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1dc29ff37741f221331b17445398e7c717ae35d5b5ac8d352ce2b6e04a7cc33)
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
        :param enabled: Whether or not Cloud Data Lineage integration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#enabled ComposerEnvironment#enabled}
        '''
        value = ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration(
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
    ) -> ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference:
        return typing.cast(ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference, jsii.get(self, "cloudDataLineageIntegration"))

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
    ) -> typing.Optional[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration], jsii.get(self, "cloudDataLineageIntegrationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d305d6bf25fa5fca1e252807b4cde3142c76966c88b14d2a6e533da38646a831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "airflowConfigOverrides", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envVariables")
    def env_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "envVariables"))

    @env_variables.setter
    def env_variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f942bcaa513d7a103d9e4fe158f2070dc081b638c4ce64d865e04c5275da6038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2351853f7bf583ffe42bd356957187cade3eddaeb8d554614ab39a3d45bbe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pypiPackages")
    def pypi_packages(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "pypiPackages"))

    @pypi_packages.setter
    def pypi_packages(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb3c4b4bf5508c9ef2f91839e8942cd09b4d6c565d7eb0de544865075bc7044)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pypiPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonVersion")
    def python_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonVersion"))

    @python_version.setter
    def python_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea47c0643f3759adfb811a069a39764828ea29cd988dfdb6782a2e425345a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulerCount")
    def scheduler_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "schedulerCount"))

    @scheduler_count.setter
    def scheduler_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b21105e30fca1005d43ab556ab2ccda0248a8f7455610fb09cb85e45a7b72a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webServerPluginsMode")
    def web_server_plugins_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webServerPluginsMode"))

    @web_server_plugins_mode.setter
    def web_server_plugins_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c8cb8abcaa94d3ba2d8a436ca86272a3fc38ac20af289806efbba066d9e503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webServerPluginsMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigSoftwareConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7d881477a195de15a19ccb84136d77b78da6f86ad12b58525271ffa8ae5a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerConfig",
    jsii_struct_bases=[],
    name_mapping={"machine_type": "machineType"},
)
class ComposerEnvironmentConfigWebServerConfig:
    def __init__(self, *, machine_type: builtins.str) -> None:
        '''
        :param machine_type: Optional. Machine type on which Airflow web server is running. It has to be one of: composer-n1-webserver-2, composer-n1-webserver-4 or composer-n1-webserver-8. If not specified, composer-n1-webserver-2 will be used. Value custom is returned only in response, if Airflow web server parameters were manually changed to a non-standard values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8835e195c99e9f19691bc6e6b8733b21a30001edd81c0b5967661ee14e97d9)
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_type": machine_type,
        }

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''Optional.

        Machine type on which Airflow web server is running. It has to be one of: composer-n1-webserver-2, composer-n1-webserver-4 or composer-n1-webserver-8. If not specified, composer-n1-webserver-2 will be used. Value custom is returned only in response, if Airflow web server parameters were manually changed to a non-standard values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#machine_type ComposerEnvironment#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWebServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWebServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7c91c1431332e24a4c05bfd84f30fc58ae184258f9561611ff82488d47fba7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32195ed09f92a8dd981a50e1300bb682e2165a9863fd2c41740c11b31831f54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWebServerConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWebServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWebServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723ed8a3010582f9ec279fbf7696f993e3a97dc74efe31bf85877441b72801a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerNetworkAccessControl",
    jsii_struct_bases=[],
    name_mapping={"allowed_ip_range": "allowedIpRange"},
)
class ComposerEnvironmentConfigWebServerNetworkAccessControl:
    def __init__(
        self,
        *,
        allowed_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowed_ip_range: allowed_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#allowed_ip_range ComposerEnvironment#allowed_ip_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f013e88ade589bc5d89c985111937aea08f62b80e00474589916ecdf67253c)
            check_type(argname="argument allowed_ip_range", value=allowed_ip_range, expected_type=type_hints["allowed_ip_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_ip_range is not None:
            self._values["allowed_ip_range"] = allowed_ip_range

    @builtins.property
    def allowed_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange"]]]:
        '''allowed_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#allowed_ip_range ComposerEnvironment#allowed_ip_range}
        '''
        result = self._values.get("allowed_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWebServerNetworkAccessControl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "description": "description"},
)
class ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange:
    def __init__(
        self,
        *,
        value: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: IP address or range, defined using CIDR notation, of requests that this rule applies to. Examples: 192.168.1.1 or 192.168.0.0/16 or 2001:db8::/32 or 2001:0db8:0000:0042:0000:8a2e:0370:7334. IP range prefixes should be properly truncated. For example, 1.2.3.4/24 should be truncated to 1.2.3.0/24. Similarly, for IPv6, 2001:db8::1/32 should be truncated to 2001:db8::/32. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#value ComposerEnvironment#value}
        :param description: A description of this ip range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#description ComposerEnvironment#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f9de9a23b6a3c76ca58ce62d28a6182b3882b2c2de61a37e3ef27db3545002)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#value ComposerEnvironment#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this ip range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#description ComposerEnvironment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e99a5f746a457494d079ec945901a23b1072e1e7e42dd1b0d16e1caec676a2c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546aed7a0a99888bcbd65538f8a0bcd2ba0bbdcdd489323a0a6feb3755b3af29)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec24033d8952e39bc33b6609a70fd9fe271c64d271bdecf9245c13373aee45a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a4f6c8cf6f841d1b1db6a641ed77e51561b6c36efa64e4c2cce8991060be5b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2f44d5f54f16f16b285a40c2b383f4e3f74526a6a530a446b721fb1f1fc7bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b469ca2aa74f475a68195dcab749093e995c2c88b32bdac44746499d88a1065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__030676b683330bcb895871cca0c9e64fae324d697bdf508a527d4da4beeb551e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4593b72eb8708cfdbe38a4c6ed9be5bcf550ab0f63b2db3e075ca75e3083ca70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d0652ebdfc373dba70d1c08e8486120f1cbb155d8c6b42b3d743fb0f69c885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839dab0e3e45e473e28e9a9473f9c158c0ffaf4b2b1fb70b062788a1e7e12ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63dd2c12e53b746cae575f5a8a8653b88301155939eacb0886c3d2fb29d33f7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedIpRange")
    def put_allowed_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b004c1f53584adb135674eef17dc57172cf570ef3b73ac13a324c89bf15217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedIpRange", [value]))

    @jsii.member(jsii_name="resetAllowedIpRange")
    def reset_allowed_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIpRange", []))

    @builtins.property
    @jsii.member(jsii_name="allowedIpRange")
    def allowed_ip_range(
        self,
    ) -> ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList:
        return typing.cast(ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList, jsii.get(self, "allowedIpRange"))

    @builtins.property
    @jsii.member(jsii_name="allowedIpRangeInput")
    def allowed_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]], jsii.get(self, "allowedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWebServerNetworkAccessControl]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWebServerNetworkAccessControl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWebServerNetworkAccessControl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f471ee82e261e02156fb9589f278321384e09f154c9536c9d4199ff9226a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dag_processor": "dagProcessor",
        "scheduler": "scheduler",
        "triggerer": "triggerer",
        "web_server": "webServer",
        "worker": "worker",
    },
)
class ComposerEnvironmentConfigWorkloadsConfig:
    def __init__(
        self,
        *,
        dag_processor: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigDagProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigScheduler", typing.Dict[builtins.str, typing.Any]]] = None,
        triggerer: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigTriggerer", typing.Dict[builtins.str, typing.Any]]] = None,
        web_server: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigWebServer", typing.Dict[builtins.str, typing.Any]]] = None,
        worker: typing.Optional[typing.Union["ComposerEnvironmentConfigWorkloadsConfigWorker", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dag_processor: dag_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#dag_processor ComposerEnvironment#dag_processor}
        :param scheduler: scheduler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduler ComposerEnvironment#scheduler}
        :param triggerer: triggerer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#triggerer ComposerEnvironment#triggerer}
        :param web_server: web_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server ComposerEnvironment#web_server}
        :param worker: worker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#worker ComposerEnvironment#worker}
        '''
        if isinstance(dag_processor, dict):
            dag_processor = ComposerEnvironmentConfigWorkloadsConfigDagProcessor(**dag_processor)
        if isinstance(scheduler, dict):
            scheduler = ComposerEnvironmentConfigWorkloadsConfigScheduler(**scheduler)
        if isinstance(triggerer, dict):
            triggerer = ComposerEnvironmentConfigWorkloadsConfigTriggerer(**triggerer)
        if isinstance(web_server, dict):
            web_server = ComposerEnvironmentConfigWorkloadsConfigWebServer(**web_server)
        if isinstance(worker, dict):
            worker = ComposerEnvironmentConfigWorkloadsConfigWorker(**worker)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a351f02b3a12b948fa76c9f7fb9a49cc538a0e6f3ac28f820e56e2f066d77592)
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
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigDagProcessor"]:
        '''dag_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#dag_processor ComposerEnvironment#dag_processor}
        '''
        result = self._values.get("dag_processor")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigDagProcessor"], result)

    @builtins.property
    def scheduler(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigScheduler"]:
        '''scheduler block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#scheduler ComposerEnvironment#scheduler}
        '''
        result = self._values.get("scheduler")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigScheduler"], result)

    @builtins.property
    def triggerer(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigTriggerer"]:
        '''triggerer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#triggerer ComposerEnvironment#triggerer}
        '''
        result = self._values.get("triggerer")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigTriggerer"], result)

    @builtins.property
    def web_server(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWebServer"]:
        '''web_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#web_server ComposerEnvironment#web_server}
        '''
        result = self._values.get("web_server")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWebServer"], result)

    @builtins.property
    def worker(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWorker"]:
        '''worker block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#worker ComposerEnvironment#worker}
        '''
        result = self._values.get("worker")
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWorker"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWorkloadsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigDagProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "cpu": "cpu",
        "memory_gb": "memoryGb",
        "storage_gb": "storageGb",
    },
)
class ComposerEnvironmentConfigWorkloadsConfigDagProcessor:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of DAG processors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        :param cpu: CPU request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5a95382a9cbcf013b8cffbf2cb231d232a6503e2443fabc4040811759d0a83)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''CPU request and limit for DAG processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for DAG processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for DAG processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWorkloadsConfigDagProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5158f828472664f48d6b3b7e91ca7499b8114302b238140b95eabf62aede64d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c7edcdd1146c7a38944baeda27036ceb9e6348b4a5ae0e2eb9d6bd4842fb90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7538befdfd463c6c15bb2b12df903722cd95951f3840da721982d3a12c861fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f73d905b5b88041e55a353b5ea9713eeb9378fed154be27cea6e5c0eda82242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a259f35c0cb64630726494c7c34fde03508ccccda1b0b15f5e2733b5d8ee305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfigDagProcessor]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfigDagProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigDagProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e0c202762695279cfbca65a8a9f0ed9ebd4355fded58f226ba617b95298181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComposerEnvironmentConfigWorkloadsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc185b6c9ac0ff40b38d9978a4587c8a71149e948004fe2001738174c0c92b7a)
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
        :param count: Number of DAG processors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        :param cpu: CPU request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for DAG processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        value = ComposerEnvironmentConfigWorkloadsConfigDagProcessor(
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
        :param count: The number of schedulers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        value = ComposerEnvironmentConfigWorkloadsConfigScheduler(
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
        :param count: The number of triggerers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        value = ComposerEnvironmentConfigWorkloadsConfigTriggerer(
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
        :param cpu: CPU request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        value = ComposerEnvironmentConfigWorkloadsConfigWebServer(
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
        :param cpu: CPU request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param max_count: Maximum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#max_count ComposerEnvironment#max_count}
        :param memory_gb: Memory (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param min_count: Minimum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#min_count ComposerEnvironment#min_count}
        :param storage_gb: Storage (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        value = ComposerEnvironmentConfigWorkloadsConfigWorker(
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
    ) -> ComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference:
        return typing.cast(ComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference, jsii.get(self, "dagProcessor"))

    @builtins.property
    @jsii.member(jsii_name="scheduler")
    def scheduler(
        self,
    ) -> "ComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference":
        return typing.cast("ComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference", jsii.get(self, "scheduler"))

    @builtins.property
    @jsii.member(jsii_name="triggerer")
    def triggerer(
        self,
    ) -> "ComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference":
        return typing.cast("ComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference", jsii.get(self, "triggerer"))

    @builtins.property
    @jsii.member(jsii_name="webServer")
    def web_server(
        self,
    ) -> "ComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference":
        return typing.cast("ComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference", jsii.get(self, "webServer"))

    @builtins.property
    @jsii.member(jsii_name="worker")
    def worker(self) -> "ComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference":
        return typing.cast("ComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference", jsii.get(self, "worker"))

    @builtins.property
    @jsii.member(jsii_name="dagProcessorInput")
    def dag_processor_input(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfigDagProcessor]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfigDagProcessor], jsii.get(self, "dagProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulerInput")
    def scheduler_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigScheduler"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigScheduler"], jsii.get(self, "schedulerInput"))

    @builtins.property
    @jsii.member(jsii_name="triggererInput")
    def triggerer_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigTriggerer"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigTriggerer"], jsii.get(self, "triggererInput"))

    @builtins.property
    @jsii.member(jsii_name="webServerInput")
    def web_server_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWebServer"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWebServer"], jsii.get(self, "webServerInput"))

    @builtins.property
    @jsii.member(jsii_name="workerInput")
    def worker_input(
        self,
    ) -> typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWorker"]:
        return typing.cast(typing.Optional["ComposerEnvironmentConfigWorkloadsConfigWorker"], jsii.get(self, "workerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055dd78371420af32305de4a52515766f74b040baef04443be735c0f7cb5d46a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigScheduler",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "cpu": "cpu",
        "memory_gb": "memoryGb",
        "storage_gb": "storageGb",
    },
)
class ComposerEnvironmentConfigWorkloadsConfigScheduler:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The number of schedulers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for a single Airflow scheduler replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50958b7dbf00727388ff1eb31028ad826190310e5fe1ed5c0c180325695cb7db)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''CPU request and limit for a single Airflow scheduler replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for a single Airflow scheduler replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for a single Airflow scheduler replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWorkloadsConfigScheduler(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff79c2d01fe316b58b9c514d5cc1af0b1402065e74ec0366a2078608671eab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3e92d25bf6c63c1fb7ef55ebdeafd4629ed98f78aab0ffecb48920460b2fe22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd356c8ae2264d769e41c9def12f6f64ecff02292d4523b3c573e5d5e80ede3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7705cc4620be2216990f261d3d82c70c040d4fbfc7e6b3cc28afd8ac2dec6c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5240ce8d9421c9a23ea8866743d88fa96565a721725b3732a6df3bceb9d2c28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfigScheduler]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfigScheduler], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigScheduler],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaa657ae99b9a97dc27c4f3eb2751b4c03d6a80552a55d0207c585ac0e3aa02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigTriggerer",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "cpu": "cpu", "memory_gb": "memoryGb"},
)
class ComposerEnvironmentConfigWorkloadsConfigTriggerer:
    def __init__(
        self,
        *,
        count: jsii.Number,
        cpu: jsii.Number,
        memory_gb: jsii.Number,
    ) -> None:
        '''
        :param count: The number of triggerers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        :param cpu: CPU request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for a single Airflow triggerer replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd056c2c1efbd493e86fb6aee30f83b0f99998875d8c0989ff5fa5040b01329c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#count ComposerEnvironment#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''CPU request and limit for a single Airflow triggerer replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_gb(self) -> jsii.Number:
        '''Memory (GB) request and limit for a single Airflow triggerer replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        assert result is not None, "Required property 'memory_gb' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWorkloadsConfigTriggerer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7b95e10c9b06b8ff564d1bb294ee24620e2d032ebab99532e0d2d80bec312af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb9b2d3d8425edc6c89b3d8701ceb557893737f84be35ed2bf69ac2d3ccff2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec951639322925549e081ae7335fb9e7050a07b788d9c1fd0b6277e8b03c1cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a880926f4f2bb3c63153ed4d3134474bd43aac491fddc357f62ea2ad61a1b53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfigTriggerer]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfigTriggerer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigTriggerer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637c054e23d2646e2ceaacef0c02d61a4d327e57b46b0b58e7c95974995577a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigWebServer",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory_gb": "memoryGb", "storage_gb": "storageGb"},
)
class ComposerEnvironmentConfigWorkloadsConfigWebServer:
    def __init__(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_gb: typing.Optional[jsii.Number] = None,
        storage_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu: CPU request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param memory_gb: Memory (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param storage_gb: Storage (GB) request and limit for Airflow web server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f4610126e59409ab996f4a3880eabe12eee23737806246c826e297eae9c02a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for Airflow web server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for Airflow web server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWorkloadsConfigWebServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b45fceb85e9eba0cd1525b1cc1e3ef85525107ac133d174973a90176e6d23ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18ee6a98fbdf748d631576ef5d090015e197c547c434ab0d3f910ad02612da0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96cb2b9d9a7a7e454c0223aacea1c3f7b779fcdcc63446efc9b066c9f4b550ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad91abf01b90ad7779211ad147e6a501be8e5a5c42c339b91dcb53ae311e152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWebServer]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWebServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWebServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad514a41c07e1109f861bae3073c6b1ece673c672e6ad0179820733191aaf07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigWorker",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "max_count": "maxCount",
        "memory_gb": "memoryGb",
        "min_count": "minCount",
        "storage_gb": "storageGb",
    },
)
class ComposerEnvironmentConfigWorkloadsConfigWorker:
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
        :param cpu: CPU request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        :param max_count: Maximum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#max_count ComposerEnvironment#max_count}
        :param memory_gb: Memory (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        :param min_count: Minimum number of workers for autoscaling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#min_count ComposerEnvironment#min_count}
        :param storage_gb: Storage (GB) request and limit for a single Airflow worker replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa8acca393551d8c2285d4ff1cfa6688d521415ab0db246f483512a5e77ae6d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#cpu ComposerEnvironment#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of workers for autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#max_count ComposerEnvironment#max_count}
        '''
        result = self._values.get("max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory (GB) request and limit for a single Airflow worker replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#memory_gb ComposerEnvironment#memory_gb}
        '''
        result = self._values.get("memory_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of workers for autoscaling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#min_count ComposerEnvironment#min_count}
        '''
        result = self._values.get("min_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage (GB) request and limit for a single Airflow worker replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#storage_gb ComposerEnvironment#storage_gb}
        '''
        result = self._values.get("storage_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentConfigWorkloadsConfigWorker(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66ca374224178437214b695dc59d5360a28e6fda7c7905d74d03bd0d359fa67f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b9be05bd88dfffbaf8b185bd3f21e2a9e2218b5bcb989c58e8d77f790e5794c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxCount")
    def max_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCount"))

    @max_count.setter
    def max_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214b55d2bd6c505435628a0593a5af583840fdd3b316a62a3bf990d60b6410e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryGb")
    def memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryGb"))

    @memory_gb.setter
    def memory_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dfc730436a9bac79a693c4556edc3f8dd3475ba10df070a4382ff81fea3a856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCount")
    def min_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCount"))

    @min_count.setter
    def min_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f2cfca86dce22999a9d746cf091dec5b06cd4fb774968c48f1af6ee22cab29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageGb")
    def storage_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageGb"))

    @storage_gb.setter
    def storage_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a2071e558eea9cc4ed4d1f63784dd68da7bc5dd65c5e39dd81e8329cb61bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWorker]:
        return typing.cast(typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWorker], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWorker],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025ade44810a0b984ff22443bdcaf4b3d43e950c1a95826d7dde5e16f90373aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentStorageConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket"},
)
class ComposerEnvironmentStorageConfig:
    def __init__(self, *, bucket: builtins.str) -> None:
        '''
        :param bucket: Optional. Name of an existing Cloud Storage bucket to be used by the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#bucket ComposerEnvironment#bucket}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ce6511b6d7177be1bd159312a50a14c918e1bd19b898e60d5b375cfa68abdd)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Optional. Name of an existing Cloud Storage bucket to be used by the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#bucket ComposerEnvironment#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentStorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentStorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5db1e6f4161c800253fe4156cc7f327c3c15fffd93ef98658da66088593ab397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed4bbd755d1c9b1a71ec93847699087ea3f655ab26979a6fc080d57c64e4d722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComposerEnvironmentStorageConfig]:
        return typing.cast(typing.Optional[ComposerEnvironmentStorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComposerEnvironmentStorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4e7862f5b9df479226c2e30158b49d85b8e181841b1483d9026cd62af52bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComposerEnvironmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#create ComposerEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#delete ComposerEnvironment#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#update ComposerEnvironment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199b67111d9d72870dc221df92b369dcf41db33e4ba5742512f8792fb9e2cfb7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#create ComposerEnvironment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#delete ComposerEnvironment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/composer_environment#update ComposerEnvironment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComposerEnvironmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComposerEnvironmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.composerEnvironment.ComposerEnvironmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3183728fc80faa0122cae43911ab15c34a76df71b0a006efae8a20089402ad39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1ea05b89c03402401b6ec09ae04d890104a701102f6af23fa3d81621bab00b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025ded286ef9a0acd929a788b61739f684ff324e4fca6f0a5aa3026eb30d196a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba62159b8a52227ae840bd73935006260f9fcffdfd33bc7e09fa72b7c7051df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8d9d8bb054e5b1559cb5a6fd75362a7698c5d109277f79af986b8b28a04075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComposerEnvironment",
    "ComposerEnvironmentConfig",
    "ComposerEnvironmentConfigA",
    "ComposerEnvironmentConfigAOutputReference",
    "ComposerEnvironmentConfigDataRetentionConfig",
    "ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig",
    "ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigList",
    "ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfigOutputReference",
    "ComposerEnvironmentConfigDataRetentionConfigOutputReference",
    "ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig",
    "ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigList",
    "ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfigOutputReference",
    "ComposerEnvironmentConfigDatabaseConfig",
    "ComposerEnvironmentConfigDatabaseConfigOutputReference",
    "ComposerEnvironmentConfigEncryptionConfig",
    "ComposerEnvironmentConfigEncryptionConfigOutputReference",
    "ComposerEnvironmentConfigMaintenanceWindow",
    "ComposerEnvironmentConfigMaintenanceWindowOutputReference",
    "ComposerEnvironmentConfigMasterAuthorizedNetworksConfig",
    "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks",
    "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksList",
    "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocksOutputReference",
    "ComposerEnvironmentConfigMasterAuthorizedNetworksConfigOutputReference",
    "ComposerEnvironmentConfigNodeConfig",
    "ComposerEnvironmentConfigNodeConfigIpAllocationPolicy",
    "ComposerEnvironmentConfigNodeConfigIpAllocationPolicyOutputReference",
    "ComposerEnvironmentConfigNodeConfigOutputReference",
    "ComposerEnvironmentConfigPrivateEnvironmentConfig",
    "ComposerEnvironmentConfigPrivateEnvironmentConfigOutputReference",
    "ComposerEnvironmentConfigRecoveryConfig",
    "ComposerEnvironmentConfigRecoveryConfigOutputReference",
    "ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig",
    "ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfigOutputReference",
    "ComposerEnvironmentConfigSoftwareConfig",
    "ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration",
    "ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegrationOutputReference",
    "ComposerEnvironmentConfigSoftwareConfigOutputReference",
    "ComposerEnvironmentConfigWebServerConfig",
    "ComposerEnvironmentConfigWebServerConfigOutputReference",
    "ComposerEnvironmentConfigWebServerNetworkAccessControl",
    "ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange",
    "ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeList",
    "ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRangeOutputReference",
    "ComposerEnvironmentConfigWebServerNetworkAccessControlOutputReference",
    "ComposerEnvironmentConfigWorkloadsConfig",
    "ComposerEnvironmentConfigWorkloadsConfigDagProcessor",
    "ComposerEnvironmentConfigWorkloadsConfigDagProcessorOutputReference",
    "ComposerEnvironmentConfigWorkloadsConfigOutputReference",
    "ComposerEnvironmentConfigWorkloadsConfigScheduler",
    "ComposerEnvironmentConfigWorkloadsConfigSchedulerOutputReference",
    "ComposerEnvironmentConfigWorkloadsConfigTriggerer",
    "ComposerEnvironmentConfigWorkloadsConfigTriggererOutputReference",
    "ComposerEnvironmentConfigWorkloadsConfigWebServer",
    "ComposerEnvironmentConfigWorkloadsConfigWebServerOutputReference",
    "ComposerEnvironmentConfigWorkloadsConfigWorker",
    "ComposerEnvironmentConfigWorkloadsConfigWorkerOutputReference",
    "ComposerEnvironmentStorageConfig",
    "ComposerEnvironmentStorageConfigOutputReference",
    "ComposerEnvironmentTimeouts",
    "ComposerEnvironmentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__75963584f3ce33b53cf22e9bb568521d0ad9cc7ce9db83bbcf7c23eafc127fa2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    config: typing.Optional[typing.Union[ComposerEnvironmentConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    storage_config: typing.Optional[typing.Union[ComposerEnvironmentStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComposerEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__272da7324b38bc5df69c1a6eac59d6a10cec1608914c78e8279e5d7d9529c8be(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a73b8fe5ba4fcfde69cbc597c399ffa0c66d5113d94077f074140d77872045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc316127ef85d7e5d2cda7ea6f2c4c89f0cc174b2e24af26b10ede618ccd2088(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b421d5b7908f2fb47cece79c6e16341bfc9d07300ee29a43610d69e448095dbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f501ab6cb2ec743efb134adc92e3c40c839447781e12592a0145a8753f69b08b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e334b5bb51ca122ffac32ecb08dcf8c7a605f09f3d98ded9821f78d3287e09d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2171dc6a6a3a8ebf4e3578f2ad46c20819cd7ab55188b7b0325b1cb764c65f2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    config: typing.Optional[typing.Union[ComposerEnvironmentConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    storage_config: typing.Optional[typing.Union[ComposerEnvironmentStorageConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComposerEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aee05fb1cc4e2d4b118004bfb75f940668bfc5ff2730fb9cfeac77ccfa0cdad(
    *,
    database_config: typing.Optional[typing.Union[ComposerEnvironmentConfigDatabaseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_retention_config: typing.Optional[typing.Union[ComposerEnvironmentConfigDataRetentionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_private_builds_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_private_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[ComposerEnvironmentConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_size: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[ComposerEnvironmentConfigMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    master_authorized_networks_config: typing.Optional[typing.Union[ComposerEnvironmentConfigMasterAuthorizedNetworksConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_config: typing.Optional[typing.Union[ComposerEnvironmentConfigNodeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    node_count: typing.Optional[jsii.Number] = None,
    private_environment_config: typing.Optional[typing.Union[ComposerEnvironmentConfigPrivateEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_config: typing.Optional[typing.Union[ComposerEnvironmentConfigRecoveryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    resilience_mode: typing.Optional[builtins.str] = None,
    software_config: typing.Optional[typing.Union[ComposerEnvironmentConfigSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    web_server_config: typing.Optional[typing.Union[ComposerEnvironmentConfigWebServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    web_server_network_access_control: typing.Optional[typing.Union[ComposerEnvironmentConfigWebServerNetworkAccessControl, typing.Dict[builtins.str, typing.Any]]] = None,
    workloads_config: typing.Optional[typing.Union[ComposerEnvironmentConfigWorkloadsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad0816bd973626671aa0b6e78e5a3e5307b605fed9ac1313da70253b3bac0d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238250978f31ac3743c45c813e7dedef142c6eb4332a60301bbb72723b31be86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b7f7e480c4b2c42502554498cf46a4de5962e186c3d226980e0f7738824265(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61c86eeac63ebe7ba77836cf11e128956724dbe40f3f21f9996661d5c508028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbee362135c8294bd1fc2fabf9c95e2e8eb4a6a849af236afb11ecd22ed00409(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5312ff9f8f8723f2e7db384bed1f375fb8008715115f3c105eabf2f169533f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837af12ab24526421593ec547b855c9055a14846e8ea97a51fdbe91062910256(
    value: typing.Optional[ComposerEnvironmentConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825432b7c61a0dc01c2bdcea5ea6997e438e19f11e4d929ae06a3bc711a29666(
    *,
    airflow_metadata_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    task_logs_retention_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41db014169569aac3c95f6368c2dcdc17bc182210d968094a4655babbedd31c(
    *,
    retention_days: typing.Optional[jsii.Number] = None,
    retention_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d139bda6978efc157020ce32f0ca894c280613175cb890bf0a74430cba5072(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafa997a383b5cedee5e7db2a4670018b74e484066ab4a8ddf6d38bd6bc3a46f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01886439fc9490c134315b0bad37b04580628fb5d729c71e499bc559f79ee9e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b310f9866ac6980bdab347cd9111ce4a24938a4be38083a1d8e3004ad1251a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b08a28287b29af4d6a74be34311938ff410ce202512c445abe3451c04e4fa7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8363698592b999781c2755ac6218fec447a13a3e60c2cc8826e7627d5abe6368(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4005c941f97ce65eea2ee60b1765cf45124499cd84859cb24fb10e8a949ccf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42b556485baf882c147bded1eedf8dc9a1258b0a5c245640bdbde4c8b30ddc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c15e4ce06ebbfcc309831c3e032ef23f8c056c259665eaaefab63e9d7dc25e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45302557dc380b9564f7b66ae6e8d036266aa8c03ca51b7bedc7f0ce1a4b5bc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18670ce1c82269a8c5d618df981e52eced8954bb66ff37e69d8f116faa08fa67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46e59461ad7caa5110295d2cd957948ceeee8a0d895df1b15f06b0178c37b81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigDataRetentionConfigAirflowMetadataRetentionConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5696f65409d46aefc6e3cebd20bb4d95efd6712743fb884d5fcde4374d5fe5c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcd585ffed5d2aea59632dc9ea7a580609840944918832780df5d45dff78995(
    value: typing.Optional[ComposerEnvironmentConfigDataRetentionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0b24b89254dae3f1a2d91507938bfd58ae35bb309447a71fbd0d1e2cf9311e(
    *,
    storage_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741b3894e162589acfb35fcb4af262e4ea22b27ad190c04e4c511da5cecce6a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1bf2d1120de248e8668d74085470ec56a8a77b1e39ec6ed443ca2dde981690(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71928b81000f0ce39fce5cdf35d50fcb8f8413396e09106c8d6ddd4ac7b53805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd9ad99eb712b70a9922fbf34d83c3b0c4fc588362fefdab0e4a5fc09249fbe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2b82301e9b9b5264b34bd92e7c75d2af52525b5211e8a73f4d09a87306bbd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0278dc997fa628649ee284b55cc6828eca5037800f87a24d9039c99fbe854bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde2495a572414017163b966f0fb83ab624d914830ce8441ab9505426f4964f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd2f0f9c93bb15785df4d987a05ebb5c0b32f5f7456735ac0dbafac96ea06f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904eec58f53aca76ef894d11de765178fe8d82947862e6bcbe1ab42bcc4eff6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigDataRetentionConfigTaskLogsRetentionConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818af818997685510761d6a2f50839d356dfc85ba488b1542c25bf336667e891(
    *,
    machine_type: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043d127e421770726372cd34919c2d55535771569a51d84b22188e22db6da19c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375b817c25679baa6754b6ea30e9837fcdd6458ad99e5f626839736c9b4308f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a244ac7579906089283653a7021b5fc51e1141d173142facee4ddf95edc210e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d067cf0dfee4ec019e5e6fd910551286208049b50de6d7389f8128eab79b78ae(
    value: typing.Optional[ComposerEnvironmentConfigDatabaseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5e57299eba67a0cf3239bd439586f61105fd1843ddfdc96e0f245701717b2b(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9cac4c0e9dc5724e52e1ffd69f0cdfd8c59c592d3ec10117f6d4ed0b2be9ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bd0aae8bda100784addfc3a9865c83ff7795a2520af828f462fcfb81f2d1dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985d17bcf34c23b81fb9074e0e51f9d138ea87d6655f245c90f8cc690959d16(
    value: typing.Optional[ComposerEnvironmentConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac65fb28b7e8c5b4c6fb528ba832c08b8c61e8975f3b60154f40986dd5ce90fd(
    *,
    end_time: builtins.str,
    recurrence: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0965ba1beb560c6a8b2fce35adf15cebceb56be4584fb369eedf82c7f8e73631(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a262d56e356164e625eccf30822f6305470305a1d14aa328dbca95d6f756ca9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0701a20a563e160d2f7caf0a2695d9b4253ed6930d7579e9fdea81b2a15012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70724a0e79f926016fa548ce980d16a05059db5c3283b7e4a2c1483e2244d03e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21cb9376209b79b8ccd2734e21e57692852e96fbb6c32bc3f18184cc5fd7c4d(
    value: typing.Optional[ComposerEnvironmentConfigMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fddc2032e443b3b948d4737960119242f2065bda140f1805dac132f7d4012e(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cidr_blocks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24946083b6d182ecf4380de47e7120cbe09a67f3668abaf4bfd2ea9aa50d7a02(
    *,
    cidr_block: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd9950e9d202e663ca3ee52e7dd84bdb89ba5896a416919052406bd9a433c98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01a71d43aeb13e7121c0f0229c23f973b66b87e0583af44130410bf1c99eac7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41470b14a3ff9185cb37b485879856730ed0a1e649b4b898f06710a387b11cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772e0a14d37955e6aef8a9bcee9f2954f66c33cb4533abd7bf55a47e174eea6b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77890d6eec39b355ebfadec3984366dcec4162c38b4d405b7fa09696f34725ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7390094f4cea328b386a742b023c6877fa91616f4b767ca6a61a5316e7091a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735df287e01ee431922ae6be97b15b77eebb9971887f851f184d11cb750c55e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e945ae84b79df00027850713ba117bb421745e0e86b94621f44ab7bc60abc11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485be438e8eac405748de85994d806cf8b2077f2fb1ad68efe0036da610cafe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c187e343af2f6672fcb1a676ec62218fb6348edd9bceacb2ef1001a1d57fd28e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbb4ffa7e317729350c605b90465d1612e193ef9343713ac715848f925003e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf8ba1205b72a7aa0d878f48443880ca6ea5312938a9aeaa3308a5e424796d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigMasterAuthorizedNetworksConfigCidrBlocks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af180a45ec062ce5b65406ebb9ae02fa6167af9eede0d0165cbd3320eb0d6a1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccc798ea665d4f839f11280a4c16b58ecb5f7067ad8be83aa1e2827f612eda2(
    value: typing.Optional[ComposerEnvironmentConfigMasterAuthorizedNetworksConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee3a648d418e87474e7e3e5d07985b54ef4ff1138afec41d6d55403a9639263(
    *,
    composer_internal_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    composer_network_attachment: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    enable_ip_masq_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_allocation_policy: typing.Optional[typing.Union[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_account: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf90c7993267d2883df452ab884e2a4405ce17573a935346e4a953f77d5587c(
    *,
    cluster_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    cluster_secondary_range_name: typing.Optional[builtins.str] = None,
    services_ipv4_cidr_block: typing.Optional[builtins.str] = None,
    services_secondary_range_name: typing.Optional[builtins.str] = None,
    use_ip_aliases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c59bc2b5ad96c6080c05b2b5c1f5e14c41fed87016385bb91ed7b7ac9e99a91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774f48dec144c04e8cacc6ca4b05810f5628f0da269ed4eab5ceacc241d16c98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ea5c5d0c5b209efd12ae0665929c6aca18083b6aeb7a7025158050b1585b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38232f4155b9895787834935aaf731148de827567e0c9e605d75817f32a791b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052e55e09bbf4c3738fa014b95db7fbf023b0fc7910bb982a195089b79cef9a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbef236edfccd284135af86ab10efdc90d0a415f739b86aa469ad0caf7ea52b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8e62c2a53ccf772840f9ce1713076483db3aa39262ef9b5a4209b63908f0d7(
    value: typing.Optional[ComposerEnvironmentConfigNodeConfigIpAllocationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea87e8ba81e4e4ae951b0afe43f34313656bba10e4dab0e4ba5ca6f8b46e8435(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb482c657715a00ef2fe6e8f3c722c9da80ffbcab1b109f5efda9828dce3b28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dd26d527672ea32f57adc3d8ca8cc6061755cc4bf22c274606761197ebd92c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618956bd4493d2ce1e93f68228fb9b49df6805f583fe74c935acd1301f1d9d57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355c2d6eb0277f4e6c14b96aa3d807bcc396eb5086e9e5bed6782ffb55752292(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f37f5466736e7fd1ed86c6eefa66e9921348258bb42bf932735d901559eeb5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5236cea288cff62859a8e89283bb47064bfe6f642d384086b7a0c041bc968655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d93c5d0937a0025365b9c6bdc6f07851d753fbcb109658ba77a03d80d6ad16(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e99e044e29159cf9c52a10e7e18c0367f92f498ab679bbf96b791730eb55c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492a3adecc7a87091838968c91b0647fc12a86a50ba0884a83acd3972f4c6bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01398324b2a42853c13d8d83bc0af162cfb02b600cbef5bac5a45414efa3fc87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a325afd1e84e3d076e2874c4c096d7145d471ded39e2a6f9eeb74a13a27bc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba80e25041bf5eaf02acee84f5228487f08c6f26cd5a6c25a6908e283721ba9(
    value: typing.Optional[ComposerEnvironmentConfigNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136264cc2d36d96867b641484db61ef144349da161ac0550238daa9f9fb23aa3(
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

def _typecheckingstub__70bf21af434ff5809e0cd896dc7df83eabf1388c0fe65ccc5581353b48d3b95f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffe25758a872aad3ff91cee9140767b4a734671b6c07b0812db574748056bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd69a9a4b05b4fdc2e6aecca0de20ffe52d5185a136232ff3cff2f4117eee5e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c15ba22d93db5644a8028e361fd9f2276081a61d103bd10d19690bbe07aa835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288978ff95191bd2596d2328a6209d5ed2533930f06610b0654307f659c8b03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afb8a343ab9acc9fa710bb10e6d3bd5fd1a1e6c8176d429306c3bc8b748360d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a47759a591cbb5f0030c734fdb2aa1b3f7e6383945786a0c71a02fcaa97912(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5eb6a0b67c47cbe26c83db238572511d6d7ec6076ff45630fba065b569bcfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b6f881c5b65e30ac171795a0ebbe9ddf5a68b3d8296ba1dcd33d399d68dfd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e56e77f10cd20f946682b4912007d6c79c0881465a3b7bb93e10947fd973f7(
    value: typing.Optional[ComposerEnvironmentConfigPrivateEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488158e036c81570d00e4f2ad53829c1e5bc627a8e7dbd8bdda0bec4e3514fa0(
    *,
    scheduled_snapshots_config: typing.Optional[typing.Union[ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bc1fbcbdc14197e7261887650ab3b05483e8ac944292224e42590b2d660c3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9bd1531fea9f53610f7e2fa282d7043ceccd09bbd3cc814a212f5a7ae5d8fb(
    value: typing.Optional[ComposerEnvironmentConfigRecoveryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ca79626eaf66a96792cbc6c3406154a0b9cb8c214695e27501cf2d230ccb98(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    snapshot_creation_schedule: typing.Optional[builtins.str] = None,
    snapshot_location: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a1ec61992be19f731831a9cebd47e4d881dbc3615d9986934f61fed2cc8605(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3130a3e331f82589bfd482ef25b138b4fdc398f99751a49bd1a48ec17f91000e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ffdb61ea36028a53c9f221c4f585600a6652d39346b699ad04cafc31bb4deb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad71a4b2d603d319389eba6db62f3cd4a55f67aa72579d8bd10431490a6d9de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811f049cd6a211353eeb39a6f5a65971f0696dee3f12012e14d512a34d836280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8caa9be6e5bd34d5b96aa1b93f4f28530ed4ef9300f7d9ba48f3efdc9b1d6880(
    value: typing.Optional[ComposerEnvironmentConfigRecoveryConfigScheduledSnapshotsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2f296d44ab927909be3266f0ae36edf1c8b5f336a066dd4a9af327a7767815(
    *,
    airflow_config_overrides: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    cloud_data_lineage_integration: typing.Optional[typing.Union[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    env_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image_version: typing.Optional[builtins.str] = None,
    pypi_packages: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_version: typing.Optional[builtins.str] = None,
    scheduler_count: typing.Optional[jsii.Number] = None,
    web_server_plugins_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a697b7dd0a807390feefce5227a14bfc8e9f26f1f91aef3788b51de2948a50(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d8bc76fa888fd46ae66b93a99a8eecc7842e5fe198aa22c7ccbe2edb78ed0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08aa80ecc60b699b0ef0c468ddca7870230dbd60b89664e04b0d48aefbe34c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2a909c2f5c3adfa468c3b6741d4c3e9edb1692e21f160c0d127f9746a80334(
    value: typing.Optional[ComposerEnvironmentConfigSoftwareConfigCloudDataLineageIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dc29ff37741f221331b17445398e7c717ae35d5b5ac8d352ce2b6e04a7cc33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d305d6bf25fa5fca1e252807b4cde3142c76966c88b14d2a6e533da38646a831(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f942bcaa513d7a103d9e4fe158f2070dc081b638c4ce64d865e04c5275da6038(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2351853f7bf583ffe42bd356957187cade3eddaeb8d554614ab39a3d45bbe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb3c4b4bf5508c9ef2f91839e8942cd09b4d6c565d7eb0de544865075bc7044(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea47c0643f3759adfb811a069a39764828ea29cd988dfdb6782a2e425345a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b21105e30fca1005d43ab556ab2ccda0248a8f7455610fb09cb85e45a7b72a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c8cb8abcaa94d3ba2d8a436ca86272a3fc38ac20af289806efbba066d9e503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7d881477a195de15a19ccb84136d77b78da6f86ad12b58525271ffa8ae5a10(
    value: typing.Optional[ComposerEnvironmentConfigSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8835e195c99e9f19691bc6e6b8733b21a30001edd81c0b5967661ee14e97d9(
    *,
    machine_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7c91c1431332e24a4c05bfd84f30fc58ae184258f9561611ff82488d47fba7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32195ed09f92a8dd981a50e1300bb682e2165a9863fd2c41740c11b31831f54f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723ed8a3010582f9ec279fbf7696f993e3a97dc74efe31bf85877441b72801a1(
    value: typing.Optional[ComposerEnvironmentConfigWebServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f013e88ade589bc5d89c985111937aea08f62b80e00474589916ecdf67253c(
    *,
    allowed_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f9de9a23b6a3c76ca58ce62d28a6182b3882b2c2de61a37e3ef27db3545002(
    *,
    value: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99a5f746a457494d079ec945901a23b1072e1e7e42dd1b0d16e1caec676a2c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546aed7a0a99888bcbd65538f8a0bcd2ba0bbdcdd489323a0a6feb3755b3af29(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec24033d8952e39bc33b6609a70fd9fe271c64d271bdecf9245c13373aee45a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4f6c8cf6f841d1b1db6a641ed77e51561b6c36efa64e4c2cce8991060be5b2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f44d5f54f16f16b285a40c2b383f4e3f74526a6a530a446b721fb1f1fc7bae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b469ca2aa74f475a68195dcab749093e995c2c88b32bdac44746499d88a1065(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030676b683330bcb895871cca0c9e64fae324d697bdf508a527d4da4beeb551e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4593b72eb8708cfdbe38a4c6ed9be5bcf550ab0f63b2db3e075ca75e3083ca70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d0652ebdfc373dba70d1c08e8486120f1cbb155d8c6b42b3d743fb0f69c885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839dab0e3e45e473e28e9a9473f9c158c0ffaf4b2b1fb70b062788a1e7e12ea8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dd2c12e53b746cae575f5a8a8653b88301155939eacb0886c3d2fb29d33f7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b004c1f53584adb135674eef17dc57172cf570ef3b73ac13a324c89bf15217(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComposerEnvironmentConfigWebServerNetworkAccessControlAllowedIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f471ee82e261e02156fb9589f278321384e09f154c9536c9d4199ff9226a22(
    value: typing.Optional[ComposerEnvironmentConfigWebServerNetworkAccessControl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a351f02b3a12b948fa76c9f7fb9a49cc538a0e6f3ac28f820e56e2f066d77592(
    *,
    dag_processor: typing.Optional[typing.Union[ComposerEnvironmentConfigWorkloadsConfigDagProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler: typing.Optional[typing.Union[ComposerEnvironmentConfigWorkloadsConfigScheduler, typing.Dict[builtins.str, typing.Any]]] = None,
    triggerer: typing.Optional[typing.Union[ComposerEnvironmentConfigWorkloadsConfigTriggerer, typing.Dict[builtins.str, typing.Any]]] = None,
    web_server: typing.Optional[typing.Union[ComposerEnvironmentConfigWorkloadsConfigWebServer, typing.Dict[builtins.str, typing.Any]]] = None,
    worker: typing.Optional[typing.Union[ComposerEnvironmentConfigWorkloadsConfigWorker, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5a95382a9cbcf013b8cffbf2cb231d232a6503e2443fabc4040811759d0a83(
    *,
    count: typing.Optional[jsii.Number] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5158f828472664f48d6b3b7e91ca7499b8114302b238140b95eabf62aede64d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c7edcdd1146c7a38944baeda27036ceb9e6348b4a5ae0e2eb9d6bd4842fb90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7538befdfd463c6c15bb2b12df903722cd95951f3840da721982d3a12c861fe1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f73d905b5b88041e55a353b5ea9713eeb9378fed154be27cea6e5c0eda82242(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a259f35c0cb64630726494c7c34fde03508ccccda1b0b15f5e2733b5d8ee305(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e0c202762695279cfbca65a8a9f0ed9ebd4355fded58f226ba617b95298181(
    value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigDagProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc185b6c9ac0ff40b38d9978a4587c8a71149e948004fe2001738174c0c92b7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055dd78371420af32305de4a52515766f74b040baef04443be735c0f7cb5d46a(
    value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50958b7dbf00727388ff1eb31028ad826190310e5fe1ed5c0c180325695cb7db(
    *,
    count: typing.Optional[jsii.Number] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff79c2d01fe316b58b9c514d5cc1af0b1402065e74ec0366a2078608671eab0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e92d25bf6c63c1fb7ef55ebdeafd4629ed98f78aab0ffecb48920460b2fe22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd356c8ae2264d769e41c9def12f6f64ecff02292d4523b3c573e5d5e80ede3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7705cc4620be2216990f261d3d82c70c040d4fbfc7e6b3cc28afd8ac2dec6c1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5240ce8d9421c9a23ea8866743d88fa96565a721725b3732a6df3bceb9d2c28a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaa657ae99b9a97dc27c4f3eb2751b4c03d6a80552a55d0207c585ac0e3aa02(
    value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigScheduler],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd056c2c1efbd493e86fb6aee30f83b0f99998875d8c0989ff5fa5040b01329c(
    *,
    count: jsii.Number,
    cpu: jsii.Number,
    memory_gb: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b95e10c9b06b8ff564d1bb294ee24620e2d032ebab99532e0d2d80bec312af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb9b2d3d8425edc6c89b3d8701ceb557893737f84be35ed2bf69ac2d3ccff2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec951639322925549e081ae7335fb9e7050a07b788d9c1fd0b6277e8b03c1cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a880926f4f2bb3c63153ed4d3134474bd43aac491fddc357f62ea2ad61a1b53e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637c054e23d2646e2ceaacef0c02d61a4d327e57b46b0b58e7c95974995577a8(
    value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigTriggerer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f4610126e59409ab996f4a3880eabe12eee23737806246c826e297eae9c02a(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b45fceb85e9eba0cd1525b1cc1e3ef85525107ac133d174973a90176e6d23ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ee6a98fbdf748d631576ef5d090015e197c547c434ab0d3f910ad02612da0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cb2b9d9a7a7e454c0223aacea1c3f7b779fcdcc63446efc9b066c9f4b550ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad91abf01b90ad7779211ad147e6a501be8e5a5c42c339b91dcb53ae311e152(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad514a41c07e1109f861bae3073c6b1ece673c672e6ad0179820733191aaf07a(
    value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWebServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa8acca393551d8c2285d4ff1cfa6688d521415ab0db246f483512a5e77ae6d(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    max_count: typing.Optional[jsii.Number] = None,
    memory_gb: typing.Optional[jsii.Number] = None,
    min_count: typing.Optional[jsii.Number] = None,
    storage_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ca374224178437214b695dc59d5360a28e6fda7c7905d74d03bd0d359fa67f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9be05bd88dfffbaf8b185bd3f21e2a9e2218b5bcb989c58e8d77f790e5794c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214b55d2bd6c505435628a0593a5af583840fdd3b316a62a3bf990d60b6410e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfc730436a9bac79a693c4556edc3f8dd3475ba10df070a4382ff81fea3a856(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f2cfca86dce22999a9d746cf091dec5b06cd4fb774968c48f1af6ee22cab29(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a2071e558eea9cc4ed4d1f63784dd68da7bc5dd65c5e39dd81e8329cb61bf8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025ade44810a0b984ff22443bdcaf4b3d43e950c1a95826d7dde5e16f90373aa(
    value: typing.Optional[ComposerEnvironmentConfigWorkloadsConfigWorker],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ce6511b6d7177be1bd159312a50a14c918e1bd19b898e60d5b375cfa68abdd(
    *,
    bucket: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db1e6f4161c800253fe4156cc7f327c3c15fffd93ef98658da66088593ab397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4bbd755d1c9b1a71ec93847699087ea3f655ab26979a6fc080d57c64e4d722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4e7862f5b9df479226c2e30158b49d85b8e181841b1483d9026cd62af52bff(
    value: typing.Optional[ComposerEnvironmentStorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199b67111d9d72870dc221df92b369dcf41db33e4ba5742512f8792fb9e2cfb7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3183728fc80faa0122cae43911ab15c34a76df71b0a006efae8a20089402ad39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ea05b89c03402401b6ec09ae04d890104a701102f6af23fa3d81621bab00b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025ded286ef9a0acd929a788b61739f684ff324e4fca6f0a5aa3026eb30d196a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba62159b8a52227ae840bd73935006260f9fcffdfd33bc7e09fa72b7c7051df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8d9d8bb054e5b1559cb5a6fd75362a7698c5d109277f79af986b8b28a04075(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComposerEnvironmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
