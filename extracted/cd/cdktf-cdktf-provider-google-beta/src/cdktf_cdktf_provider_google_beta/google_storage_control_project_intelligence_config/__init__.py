r'''
# `google_storage_control_project_intelligence_config`

Refer to the Terraform Registry for docs: [`google_storage_control_project_intelligence_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config).
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


class GoogleStorageControlProjectIntelligenceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config google_storage_control_project_intelligence_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config google_storage_control_project_intelligence_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier of the GCP project. For GCP project, this field can be project name or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#name GoogleStorageControlProjectIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#edition_config GoogleStorageControlProjectIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#filter GoogleStorageControlProjectIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#id GoogleStorageControlProjectIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#timeouts GoogleStorageControlProjectIntelligenceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402e8a37021d16866d639594e1b57be65d23f5e080a2b99373dc8427a0a463fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageControlProjectIntelligenceConfigConfig(
            name=name,
            edition_config=edition_config,
            filter=filter,
            id=id,
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
        '''Generates CDKTF code for importing a GoogleStorageControlProjectIntelligenceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageControlProjectIntelligenceConfig to import.
        :param import_from_id: The id of the existing GoogleStorageControlProjectIntelligenceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageControlProjectIntelligenceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435bbec1591f91fea400e35f88847550e9b671825c0d7dca5672726842ea30ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#excluded_cloud_storage_buckets GoogleStorageControlProjectIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#excluded_cloud_storage_locations GoogleStorageControlProjectIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#included_cloud_storage_buckets GoogleStorageControlProjectIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#included_cloud_storage_locations GoogleStorageControlProjectIntelligenceConfig#included_cloud_storage_locations}
        '''
        value = GoogleStorageControlProjectIntelligenceConfigFilter(
            excluded_cloud_storage_buckets=excluded_cloud_storage_buckets,
            excluded_cloud_storage_locations=excluded_cloud_storage_locations,
            included_cloud_storage_buckets=included_cloud_storage_buckets,
            included_cloud_storage_locations=included_cloud_storage_locations,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#create GoogleStorageControlProjectIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#delete GoogleStorageControlProjectIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#update GoogleStorageControlProjectIntelligenceConfig#update}.
        '''
        value = GoogleStorageControlProjectIntelligenceConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEditionConfig")
    def reset_edition_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEditionConfig", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="effectiveIntelligenceConfig")
    def effective_intelligence_config(
        self,
    ) -> "GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList":
        return typing.cast("GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList", jsii.get(self, "effectiveIntelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> "GoogleStorageControlProjectIntelligenceConfigFilterOutputReference":
        return typing.cast("GoogleStorageControlProjectIntelligenceConfigFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleStorageControlProjectIntelligenceConfigTimeoutsOutputReference":
        return typing.cast("GoogleStorageControlProjectIntelligenceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialConfig")
    def trial_config(
        self,
    ) -> "GoogleStorageControlProjectIntelligenceConfigTrialConfigList":
        return typing.cast("GoogleStorageControlProjectIntelligenceConfigTrialConfigList", jsii.get(self, "trialConfig"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="editionConfigInput")
    def edition_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilter"]:
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageControlProjectIntelligenceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageControlProjectIntelligenceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="editionConfig")
    def edition_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editionConfig"))

    @edition_config.setter
    def edition_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d48b889dc4c34c85a9fcc2746069ae1212cc4900c695ec2f483ef016965f791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "editionConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d894b27201cf4cf652ce06309490412f0bf74c48cd45b1fc443777b799ce71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb03bde553bf1e2d5e9b39606acebc9aa2ffcdefa3beb40541cf958c2073d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigConfig",
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
        "edition_config": "editionConfig",
        "filter": "filter",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleStorageControlProjectIntelligenceConfigConfig(
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
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier of the GCP project. For GCP project, this field can be project name or project number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#name GoogleStorageControlProjectIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#edition_config GoogleStorageControlProjectIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#filter GoogleStorageControlProjectIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#id GoogleStorageControlProjectIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#timeouts GoogleStorageControlProjectIntelligenceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = GoogleStorageControlProjectIntelligenceConfigFilter(**filter)
        if isinstance(timeouts, dict):
            timeouts = GoogleStorageControlProjectIntelligenceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9d205e4b53b53b487665e3b7ed9ee3c0775089abecc333d924629ee65a2e86)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument edition_config", value=edition_config, expected_type=type_hints["edition_config"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
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
        if edition_config is not None:
            self._values["edition_config"] = edition_config
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
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
        '''Identifier of the GCP project. For GCP project, this field can be project name or project number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#name GoogleStorageControlProjectIntelligenceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition_config(self) -> typing.Optional[builtins.str]:
        '''Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, TRIAL, DISABLED and STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#edition_config GoogleStorageControlProjectIntelligenceConfig#edition_config}
        '''
        result = self._values.get("edition_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#filter GoogleStorageControlProjectIntelligenceConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#id GoogleStorageControlProjectIntelligenceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#timeouts GoogleStorageControlProjectIntelligenceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__faae1a3dcb2fd62778c44787cae34e5324474c45ce8c11706cacf29fd841fe47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580f6e5f946602a4c37129a9f0e48d5f80f0a1b14daf7903877dc8b9761b8083)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaebb8b6752550fb1e7bd7437d736d5c0c3acb04613eec97bbaa2d8f93d9897)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccb724441ee7030eb8207c2a5b15a20c7f58d346c2b80e4e83a168496fa6155b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8316979f71c6dca6b9b687779d760bbc9edb7316e3d2f1ee8d4f47491bb834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b961f20844a28d616d24f6d90d046dc0e99a45825319f96e404388d9d532c8df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectiveEdition")
    def effective_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveEdition"))

    @builtins.property
    @jsii.member(jsii_name="intelligenceConfig")
    def intelligence_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b46eb20180ccf3cbbc80e5abbd1fa6a52089a18593df59ea5939e9146394b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilter",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_cloud_storage_buckets": "excludedCloudStorageBuckets",
        "excluded_cloud_storage_locations": "excludedCloudStorageLocations",
        "included_cloud_storage_buckets": "includedCloudStorageBuckets",
        "included_cloud_storage_locations": "includedCloudStorageLocations",
    },
)
class GoogleStorageControlProjectIntelligenceConfigFilter:
    def __init__(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#excluded_cloud_storage_buckets GoogleStorageControlProjectIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#excluded_cloud_storage_locations GoogleStorageControlProjectIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#included_cloud_storage_buckets GoogleStorageControlProjectIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#included_cloud_storage_locations GoogleStorageControlProjectIntelligenceConfig#included_cloud_storage_locations}
        '''
        if isinstance(excluded_cloud_storage_buckets, dict):
            excluded_cloud_storage_buckets = GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets(**excluded_cloud_storage_buckets)
        if isinstance(excluded_cloud_storage_locations, dict):
            excluded_cloud_storage_locations = GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations(**excluded_cloud_storage_locations)
        if isinstance(included_cloud_storage_buckets, dict):
            included_cloud_storage_buckets = GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets(**included_cloud_storage_buckets)
        if isinstance(included_cloud_storage_locations, dict):
            included_cloud_storage_locations = GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations(**included_cloud_storage_locations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3000dabadc0c6e69336643363c166e41f3a5d9c4c59358fbb0edf1e87502605)
            check_type(argname="argument excluded_cloud_storage_buckets", value=excluded_cloud_storage_buckets, expected_type=type_hints["excluded_cloud_storage_buckets"])
            check_type(argname="argument excluded_cloud_storage_locations", value=excluded_cloud_storage_locations, expected_type=type_hints["excluded_cloud_storage_locations"])
            check_type(argname="argument included_cloud_storage_buckets", value=included_cloud_storage_buckets, expected_type=type_hints["included_cloud_storage_buckets"])
            check_type(argname="argument included_cloud_storage_locations", value=included_cloud_storage_locations, expected_type=type_hints["included_cloud_storage_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excluded_cloud_storage_buckets is not None:
            self._values["excluded_cloud_storage_buckets"] = excluded_cloud_storage_buckets
        if excluded_cloud_storage_locations is not None:
            self._values["excluded_cloud_storage_locations"] = excluded_cloud_storage_locations
        if included_cloud_storage_buckets is not None:
            self._values["included_cloud_storage_buckets"] = included_cloud_storage_buckets
        if included_cloud_storage_locations is not None:
            self._values["included_cloud_storage_locations"] = included_cloud_storage_locations

    @builtins.property
    def excluded_cloud_storage_buckets(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets"]:
        '''excluded_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#excluded_cloud_storage_buckets GoogleStorageControlProjectIntelligenceConfig#excluded_cloud_storage_buckets}
        '''
        result = self._values.get("excluded_cloud_storage_buckets")
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets"], result)

    @builtins.property
    def excluded_cloud_storage_locations(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations"]:
        '''excluded_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#excluded_cloud_storage_locations GoogleStorageControlProjectIntelligenceConfig#excluded_cloud_storage_locations}
        '''
        result = self._values.get("excluded_cloud_storage_locations")
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations"], result)

    @builtins.property
    def included_cloud_storage_buckets(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets"]:
        '''included_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#included_cloud_storage_buckets GoogleStorageControlProjectIntelligenceConfig#included_cloud_storage_buckets}
        '''
        result = self._values.get("included_cloud_storage_buckets")
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets"], result)

    @builtins.property
    def included_cloud_storage_locations(
        self,
    ) -> typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations"]:
        '''included_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#included_cloud_storage_locations GoogleStorageControlProjectIntelligenceConfig#included_cloud_storage_locations}
        '''
        result = self._values.get("included_cloud_storage_locations")
        return typing.cast(typing.Optional["GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#bucket_id_regexes GoogleStorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abd377c9e9880de1601942bed6213624ebe6bcd1fc9ae9c5d719ac77f4f9bf4)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#bucket_id_regexes GoogleStorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc33901973d38b93d50f3a7a72f83eb03f13d23dc7cf1b49824464a0013012c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexesInput")
    def bucket_id_regexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketIdRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexes")
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bucketIdRegexes"))

    @bucket_id_regexes.setter
    def bucket_id_regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a71388fde0640dba5d61dbc7966ae381bcb57739fb7bfaf0c791f6e00df705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072118a29e8573bd1414f76f5f4d447e3d8ad395ace89c909e6ad54e1a6ea36b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#locations GoogleStorageControlProjectIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccda3355037433f98498e9fcfef85c28e495fd2dd1e834f3686dbcfad0e34b26)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#locations GoogleStorageControlProjectIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2b3cc53dd156fe8cf13bc8ac07ad37f289f8b20b5cbf9e69dd82838dfe56ae2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ab5523461e79ad970e9c20e99b2297a923c418d46541a158a1c6c91a4ab600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f947cf81b8414ffba19794f57e1d3a83f4e889371a20884fe7c484b69a617697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#bucket_id_regexes GoogleStorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a090735310ee8bc3e440ff310190951df9c63e4179c0b24d80bfa91a1c86a53)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#bucket_id_regexes GoogleStorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfc823e5bbb1ef235388bca1004ebf922070cde0571851d97f6ec02f0b18d152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexesInput")
    def bucket_id_regexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketIdRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketIdRegexes")
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bucketIdRegexes"))

    @bucket_id_regexes.setter
    def bucket_id_regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be62b9883b73f4f1d13962d13387867437b71d1fd0b0b995e97f10d892981b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572e53f9256be40209f6baf259a0d16506317d1686fd6f81edfe9d2c3f2b6cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#locations GoogleStorageControlProjectIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366c4ca99fa97d3a991bde1ac2a2bc5deb07f39ec5f577bb4a69254118fd5efa)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#locations GoogleStorageControlProjectIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df900478c919f682a3993175579ee51b1c5b7bbeffe2df3fa1ac2f9b57768ff1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1888eea66e95e6fc342d477518d55aa7f698c851f8e8e1dc88710310b5e8b37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ea0e027f6455e3b6b70dd8a6384aef47a21df8e9d94bcc56ddc60fdfaec8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageControlProjectIntelligenceConfigFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bbf5d9e3c736589affc0a98460874d8324b07601c6a033b1a2e7d9d1c5d0568)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludedCloudStorageBuckets")
    def put_excluded_cloud_storage_buckets(
        self,
        *,
        bucket_id_regexes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#bucket_id_regexes GoogleStorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        value = GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets(
            bucket_id_regexes=bucket_id_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedCloudStorageBuckets", [value]))

    @jsii.member(jsii_name="putExcludedCloudStorageLocations")
    def put_excluded_cloud_storage_locations(
        self,
        *,
        locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#locations GoogleStorageControlProjectIntelligenceConfig#locations}
        '''
        value = GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedCloudStorageLocations", [value]))

    @jsii.member(jsii_name="putIncludedCloudStorageBuckets")
    def put_included_cloud_storage_buckets(
        self,
        *,
        bucket_id_regexes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#bucket_id_regexes GoogleStorageControlProjectIntelligenceConfig#bucket_id_regexes}
        '''
        value = GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets(
            bucket_id_regexes=bucket_id_regexes
        )

        return typing.cast(None, jsii.invoke(self, "putIncludedCloudStorageBuckets", [value]))

    @jsii.member(jsii_name="putIncludedCloudStorageLocations")
    def put_included_cloud_storage_locations(
        self,
        *,
        locations: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#locations GoogleStorageControlProjectIntelligenceConfig#locations}
        '''
        value = GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations(
            locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putIncludedCloudStorageLocations", [value]))

    @jsii.member(jsii_name="resetExcludedCloudStorageBuckets")
    def reset_excluded_cloud_storage_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedCloudStorageBuckets", []))

    @jsii.member(jsii_name="resetExcludedCloudStorageLocations")
    def reset_excluded_cloud_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedCloudStorageLocations", []))

    @jsii.member(jsii_name="resetIncludedCloudStorageBuckets")
    def reset_included_cloud_storage_buckets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedCloudStorageBuckets", []))

    @jsii.member(jsii_name="resetIncludedCloudStorageLocations")
    def reset_included_cloud_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedCloudStorageLocations", []))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBuckets")
    def excluded_cloud_storage_buckets(
        self,
    ) -> GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference:
        return typing.cast(GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference, jsii.get(self, "excludedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocations")
    def excluded_cloud_storage_locations(
        self,
    ) -> GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference:
        return typing.cast(GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference, jsii.get(self, "excludedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBuckets")
    def included_cloud_storage_buckets(
        self,
    ) -> GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference:
        return typing.cast(GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference, jsii.get(self, "includedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocations")
    def included_cloud_storage_locations(
        self,
    ) -> GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference:
        return typing.cast(GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference, jsii.get(self, "includedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBucketsInput")
    def excluded_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "excludedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocationsInput")
    def excluded_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "excludedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBucketsInput")
    def included_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "includedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocationsInput")
    def included_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "includedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilter]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb39c7788ba7a3de89536d61d05a95505c57277af39fc5dc404c7adbff5b2ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleStorageControlProjectIntelligenceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#create GoogleStorageControlProjectIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#delete GoogleStorageControlProjectIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#update GoogleStorageControlProjectIntelligenceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4809144e116a449217d8fe6e416e8ad7684dfbb9cd951f1fc97d5ff685be423e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#create GoogleStorageControlProjectIntelligenceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#delete GoogleStorageControlProjectIntelligenceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_project_intelligence_config#update GoogleStorageControlProjectIntelligenceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2134d41439fa084d54a752b53c234850c0029dc88df8cd1d873631d621539321)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e778761f4094e497167b9fd202e05652a5e34af487b0fbed4fdbea2f66eeb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eef82497a2c52ba67d364ede792735a98143d3681a7ab82d03e0b3f8ffc60b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ac99a61b5827d62af8988b12b3ea59c706f7e8e0e48217eb257bc9701a960a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlProjectIntelligenceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlProjectIntelligenceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlProjectIntelligenceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca648dbe3932b799df3dc57107cac4ad08cd1465928e65c91be52ab96b0befb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigTrialConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleStorageControlProjectIntelligenceConfigTrialConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlProjectIntelligenceConfigTrialConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlProjectIntelligenceConfigTrialConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigTrialConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__515d309cfe155dbdd991c95a2fd30a27d4693f43bfc1622423f72020cc4bfc2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageControlProjectIntelligenceConfigTrialConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62027120ba33b886f8a0467c2e0c5623566b7f01050286a7004c1ef0ffecdf8d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageControlProjectIntelligenceConfigTrialConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e0c487190aca01477f1d393ca047dbfc11a55dc2704b0e9e6d580059d38544)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd89bcf83f1b0362762d921a7d7638600114a7756cfc7dc5f85856f5eae25452)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d65cb0551b6b2ce4c231181b59e485524b59073fa589823be4a5f50af385cfab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleStorageControlProjectIntelligenceConfigTrialConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlProjectIntelligenceConfig.GoogleStorageControlProjectIntelligenceConfigTrialConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38ff7aa2328a07f8ebdfd0118a10dbfc6c90a8933d98457ba75dcee33e5aca28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlProjectIntelligenceConfigTrialConfig]:
        return typing.cast(typing.Optional[GoogleStorageControlProjectIntelligenceConfigTrialConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigTrialConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280df8704ccc49a00b11fe0948cfa5be10e12441d8812752d317c385a6e85beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageControlProjectIntelligenceConfig",
    "GoogleStorageControlProjectIntelligenceConfigConfig",
    "GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig",
    "GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigList",
    "GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigFilter",
    "GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets",
    "GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations",
    "GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets",
    "GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations",
    "GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigFilterOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigTimeouts",
    "GoogleStorageControlProjectIntelligenceConfigTimeoutsOutputReference",
    "GoogleStorageControlProjectIntelligenceConfigTrialConfig",
    "GoogleStorageControlProjectIntelligenceConfigTrialConfigList",
    "GoogleStorageControlProjectIntelligenceConfigTrialConfigOutputReference",
]

publication.publish()

def _typecheckingstub__402e8a37021d16866d639594e1b57be65d23f5e080a2b99373dc8427a0a463fb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__435bbec1591f91fea400e35f88847550e9b671825c0d7dca5672726842ea30ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d48b889dc4c34c85a9fcc2746069ae1212cc4900c695ec2f483ef016965f791(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d894b27201cf4cf652ce06309490412f0bf74c48cd45b1fc443777b799ce71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb03bde553bf1e2d5e9b39606acebc9aa2ffcdefa3beb40541cf958c2073d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9d205e4b53b53b487665e3b7ed9ee3c0775089abecc333d924629ee65a2e86(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faae1a3dcb2fd62778c44787cae34e5324474c45ce8c11706cacf29fd841fe47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580f6e5f946602a4c37129a9f0e48d5f80f0a1b14daf7903877dc8b9761b8083(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaebb8b6752550fb1e7bd7437d736d5c0c3acb04613eec97bbaa2d8f93d9897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb724441ee7030eb8207c2a5b15a20c7f58d346c2b80e4e83a168496fa6155b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8316979f71c6dca6b9b687779d760bbc9edb7316e3d2f1ee8d4f47491bb834(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b961f20844a28d616d24f6d90d046dc0e99a45825319f96e404388d9d532c8df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b46eb20180ccf3cbbc80e5abbd1fa6a52089a18593df59ea5939e9146394b74(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigEffectiveIntelligenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3000dabadc0c6e69336643363c166e41f3a5d9c4c59358fbb0edf1e87502605(
    *,
    excluded_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abd377c9e9880de1601942bed6213624ebe6bcd1fc9ae9c5d719ac77f4f9bf4(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc33901973d38b93d50f3a7a72f83eb03f13d23dc7cf1b49824464a0013012c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a71388fde0640dba5d61dbc7966ae381bcb57739fb7bfaf0c791f6e00df705(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072118a29e8573bd1414f76f5f4d447e3d8ad395ace89c909e6ad54e1a6ea36b(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccda3355037433f98498e9fcfef85c28e495fd2dd1e834f3686dbcfad0e34b26(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b3cc53dd156fe8cf13bc8ac07ad37f289f8b20b5cbf9e69dd82838dfe56ae2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ab5523461e79ad970e9c20e99b2297a923c418d46541a158a1c6c91a4ab600(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f947cf81b8414ffba19794f57e1d3a83f4e889371a20884fe7c484b69a617697(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterExcludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a090735310ee8bc3e440ff310190951df9c63e4179c0b24d80bfa91a1c86a53(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc823e5bbb1ef235388bca1004ebf922070cde0571851d97f6ec02f0b18d152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be62b9883b73f4f1d13962d13387867437b71d1fd0b0b995e97f10d892981b6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572e53f9256be40209f6baf259a0d16506317d1686fd6f81edfe9d2c3f2b6cfd(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366c4ca99fa97d3a991bde1ac2a2bc5deb07f39ec5f577bb4a69254118fd5efa(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df900478c919f682a3993175579ee51b1c5b7bbeffe2df3fa1ac2f9b57768ff1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1888eea66e95e6fc342d477518d55aa7f698c851f8e8e1dc88710310b5e8b37b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ea0e027f6455e3b6b70dd8a6384aef47a21df8e9d94bcc56ddc60fdfaec8f9(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilterIncludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbf5d9e3c736589affc0a98460874d8324b07601c6a033b1a2e7d9d1c5d0568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb39c7788ba7a3de89536d61d05a95505c57277af39fc5dc404c7adbff5b2ff(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4809144e116a449217d8fe6e416e8ad7684dfbb9cd951f1fc97d5ff685be423e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2134d41439fa084d54a752b53c234850c0029dc88df8cd1d873631d621539321(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e778761f4094e497167b9fd202e05652a5e34af487b0fbed4fdbea2f66eeb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eef82497a2c52ba67d364ede792735a98143d3681a7ab82d03e0b3f8ffc60b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ac99a61b5827d62af8988b12b3ea59c706f7e8e0e48217eb257bc9701a960a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca648dbe3932b799df3dc57107cac4ad08cd1465928e65c91be52ab96b0befb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlProjectIntelligenceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515d309cfe155dbdd991c95a2fd30a27d4693f43bfc1622423f72020cc4bfc2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62027120ba33b886f8a0467c2e0c5623566b7f01050286a7004c1ef0ffecdf8d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e0c487190aca01477f1d393ca047dbfc11a55dc2704b0e9e6d580059d38544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd89bcf83f1b0362762d921a7d7638600114a7756cfc7dc5f85856f5eae25452(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65cb0551b6b2ce4c231181b59e485524b59073fa589823be4a5f50af385cfab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ff7aa2328a07f8ebdfd0118a10dbfc6c90a8933d98457ba75dcee33e5aca28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280df8704ccc49a00b11fe0948cfa5be10e12441d8812752d317c385a6e85beb(
    value: typing.Optional[GoogleStorageControlProjectIntelligenceConfigTrialConfig],
) -> None:
    """Type checking stubs"""
    pass
