r'''
# `google_storage_control_organization_intelligence_config`

Refer to the Terraform Registry for docs: [`google_storage_control_organization_intelligence_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config).
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


class GoogleStorageControlOrganizationIntelligenceConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config google_storage_control_organization_intelligence_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        edition_config: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config google_storage_control_organization_intelligence_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Identifier of the GCP Organization. For GCP org, this field should be organization number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#name GoogleStorageControlOrganizationIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, DISABLED, TRIAL and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#edition_config GoogleStorageControlOrganizationIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#filter GoogleStorageControlOrganizationIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#id GoogleStorageControlOrganizationIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#timeouts GoogleStorageControlOrganizationIntelligenceConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfc9d1bb9941bec7fbdcbe2bfba92e1cc795dd3a6dc8db77dad5f88bb0c9820)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleStorageControlOrganizationIntelligenceConfigConfig(
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
        '''Generates CDKTF code for importing a GoogleStorageControlOrganizationIntelligenceConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleStorageControlOrganizationIntelligenceConfig to import.
        :param import_from_id: The id of the existing GoogleStorageControlOrganizationIntelligenceConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleStorageControlOrganizationIntelligenceConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8254932bfeef58c2ca4e99d5a315f960d39d900790cbadb7457628db064525)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#excluded_cloud_storage_buckets GoogleStorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#excluded_cloud_storage_locations GoogleStorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#included_cloud_storage_buckets GoogleStorageControlOrganizationIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#included_cloud_storage_locations GoogleStorageControlOrganizationIntelligenceConfig#included_cloud_storage_locations}
        '''
        value = GoogleStorageControlOrganizationIntelligenceConfigFilter(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#create GoogleStorageControlOrganizationIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#delete GoogleStorageControlOrganizationIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#update GoogleStorageControlOrganizationIntelligenceConfig#update}.
        '''
        value = GoogleStorageControlOrganizationIntelligenceConfigTimeouts(
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
    ) -> "GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList":
        return typing.cast("GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList", jsii.get(self, "effectiveIntelligenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> "GoogleStorageControlOrganizationIntelligenceConfigFilterOutputReference":
        return typing.cast("GoogleStorageControlOrganizationIntelligenceConfigFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleStorageControlOrganizationIntelligenceConfigTimeoutsOutputReference":
        return typing.cast("GoogleStorageControlOrganizationIntelligenceConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialConfig")
    def trial_config(
        self,
    ) -> "GoogleStorageControlOrganizationIntelligenceConfigTrialConfigList":
        return typing.cast("GoogleStorageControlOrganizationIntelligenceConfigTrialConfigList", jsii.get(self, "trialConfig"))

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
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilter"]:
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilter"], jsii.get(self, "filterInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageControlOrganizationIntelligenceConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleStorageControlOrganizationIntelligenceConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="editionConfig")
    def edition_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "editionConfig"))

    @edition_config.setter
    def edition_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb1bcb8ac2da0d11c9f0d36abd7eec4761d375eb3be63edca243f0a3bc53786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "editionConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0389a1dae7aa01659cf6e9bfb890023b79f117e9f7a6d333b4e05555f03c6792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d113a148653451adac10e0e933f4c7118eb26fcb6da2661c23701bec7a4501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigConfig",
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
class GoogleStorageControlOrganizationIntelligenceConfigConfig(
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
        filter: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Identifier of the GCP Organization. For GCP org, this field should be organization number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#name GoogleStorageControlOrganizationIntelligenceConfig#name}
        :param edition_config: Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, DISABLED, TRIAL and STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#edition_config GoogleStorageControlOrganizationIntelligenceConfig#edition_config}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#filter GoogleStorageControlOrganizationIntelligenceConfig#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#id GoogleStorageControlOrganizationIntelligenceConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#timeouts GoogleStorageControlOrganizationIntelligenceConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = GoogleStorageControlOrganizationIntelligenceConfigFilter(**filter)
        if isinstance(timeouts, dict):
            timeouts = GoogleStorageControlOrganizationIntelligenceConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46893a1434f5b2f5a5dfac237d6e4df5cf07063e21d36d3a16052866043f2f90)
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
        '''Identifier of the GCP Organization. For GCP org, this field should be organization number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#name GoogleStorageControlOrganizationIntelligenceConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition_config(self) -> typing.Optional[builtins.str]:
        '''Edition configuration of the Storage Intelligence resource. Valid values are INHERIT, DISABLED, TRIAL and STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#edition_config GoogleStorageControlOrganizationIntelligenceConfig#edition_config}
        '''
        result = self._values.get("edition_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#filter GoogleStorageControlOrganizationIntelligenceConfig#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#id GoogleStorageControlOrganizationIntelligenceConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#timeouts GoogleStorageControlOrganizationIntelligenceConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4587665fe6ed96478d89c093c5e0c44236b985c4cc8ace084d8b1e1da0b574a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58bf1b40baaec4ff893c1846f41567fc88cbadbf6fe4e651d632403df7058cdd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__886de24a307ecf7815f940a25ea2cfd1d1b2d49bc9ef62d8c41ded317922e339)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f23af29239a1c025ec48b6aa88c5ceb7b111846e7d8f5f3535d63489e372148)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70e440ba973944022628e6d6b6728b50ef59a91c369861abad69876e6f94159c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a33e7e3c445cddab6dff12748df7c27f574d9dde99838acbf5bdc2b74b86a80d)
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
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8c63dbc6f5c43230b533802297990c647f69e1fb030aaffd7ec16faa8788f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilter",
    jsii_struct_bases=[],
    name_mapping={
        "excluded_cloud_storage_buckets": "excludedCloudStorageBuckets",
        "excluded_cloud_storage_locations": "excludedCloudStorageLocations",
        "included_cloud_storage_buckets": "includedCloudStorageBuckets",
        "included_cloud_storage_locations": "includedCloudStorageLocations",
    },
)
class GoogleStorageControlOrganizationIntelligenceConfigFilter:
    def __init__(
        self,
        *,
        excluded_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_buckets: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets", typing.Dict[builtins.str, typing.Any]]] = None,
        included_cloud_storage_locations: typing.Optional[typing.Union["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excluded_cloud_storage_buckets: excluded_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#excluded_cloud_storage_buckets GoogleStorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_buckets}
        :param excluded_cloud_storage_locations: excluded_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#excluded_cloud_storage_locations GoogleStorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_locations}
        :param included_cloud_storage_buckets: included_cloud_storage_buckets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#included_cloud_storage_buckets GoogleStorageControlOrganizationIntelligenceConfig#included_cloud_storage_buckets}
        :param included_cloud_storage_locations: included_cloud_storage_locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#included_cloud_storage_locations GoogleStorageControlOrganizationIntelligenceConfig#included_cloud_storage_locations}
        '''
        if isinstance(excluded_cloud_storage_buckets, dict):
            excluded_cloud_storage_buckets = GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets(**excluded_cloud_storage_buckets)
        if isinstance(excluded_cloud_storage_locations, dict):
            excluded_cloud_storage_locations = GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations(**excluded_cloud_storage_locations)
        if isinstance(included_cloud_storage_buckets, dict):
            included_cloud_storage_buckets = GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets(**included_cloud_storage_buckets)
        if isinstance(included_cloud_storage_locations, dict):
            included_cloud_storage_locations = GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations(**included_cloud_storage_locations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7abcaaf867ddf612a99a7437bb1ea484956aafa968b7a6a86158d3d9174a8fd)
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
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets"]:
        '''excluded_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#excluded_cloud_storage_buckets GoogleStorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_buckets}
        '''
        result = self._values.get("excluded_cloud_storage_buckets")
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets"], result)

    @builtins.property
    def excluded_cloud_storage_locations(
        self,
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations"]:
        '''excluded_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#excluded_cloud_storage_locations GoogleStorageControlOrganizationIntelligenceConfig#excluded_cloud_storage_locations}
        '''
        result = self._values.get("excluded_cloud_storage_locations")
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations"], result)

    @builtins.property
    def included_cloud_storage_buckets(
        self,
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets"]:
        '''included_cloud_storage_buckets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#included_cloud_storage_buckets GoogleStorageControlOrganizationIntelligenceConfig#included_cloud_storage_buckets}
        '''
        result = self._values.get("included_cloud_storage_buckets")
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets"], result)

    @builtins.property
    def included_cloud_storage_locations(
        self,
    ) -> typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations"]:
        '''included_cloud_storage_locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#included_cloud_storage_locations GoogleStorageControlOrganizationIntelligenceConfig#included_cloud_storage_locations}
        '''
        result = self._values.get("included_cloud_storage_locations")
        return typing.cast(typing.Optional["GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#bucket_id_regexes GoogleStorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56daeb1a253c3722a2998567870c3276791c8da30420acba55e4c3cc3e4a58d4)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#bucket_id_regexes GoogleStorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db1291448afb88af1888c730d167536e7a1b396ca626a6b1141da2365dd782d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5453f4c936ca2c42b435206487af7e6446e1a3a64aa1a6bf6c294c2a38e1a569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301b7ed6a85762c28365fd7451935d4d8d9de669b677892df5045cc402dc3e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#locations GoogleStorageControlOrganizationIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947f95febb4706928cfb0c4dbebcce42fd00c27467e13bd0530c8a952325b93c)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#locations GoogleStorageControlOrganizationIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22629afb2011165024a12f3fb94e85da5882b86b6cd6279a7fc5b1eba7935073)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20fd5b81e026c480a1d4e4db38170d70fbf71e8506a2eb4bf7619c7cc183c26a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78541a6bf6fafcd6d6470bdde1d018cd79a59972f3d3d49dbfdd54bfad6f8207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets",
    jsii_struct_bases=[],
    name_mapping={"bucket_id_regexes": "bucketIdRegexes"},
)
class GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets:
    def __init__(self, *, bucket_id_regexes: typing.Sequence[builtins.str]) -> None:
        '''
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#bucket_id_regexes GoogleStorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7e67e151875c619e793a0818a7a34e31457c4bf6af381134ec030faf9827b5)
            check_type(argname="argument bucket_id_regexes", value=bucket_id_regexes, expected_type=type_hints["bucket_id_regexes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_id_regexes": bucket_id_regexes,
        }

    @builtins.property
    def bucket_id_regexes(self) -> typing.List[builtins.str]:
        '''List of bucket id regexes to exclude in the storage intelligence plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#bucket_id_regexes GoogleStorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        result = self._values.get("bucket_id_regexes")
        assert result is not None, "Required property 'bucket_id_regexes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ff0906c95649dd12a3d32013591348f9485bf2dfd8002ef090afa68391650e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__add3031e0e3ae62cdc45f65d0da2876152cb9717d80d0162000d1570f7049351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketIdRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92ea11541da7b14102125d5654a04c7074f1b4b8471c5b378380ec3ae9c3704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations",
    jsii_struct_bases=[],
    name_mapping={"locations": "locations"},
)
class GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations:
    def __init__(self, *, locations: typing.Sequence[builtins.str]) -> None:
        '''
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#locations GoogleStorageControlOrganizationIntelligenceConfig#locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7929e8f12e8985028c76f512d78828db62af8017597a00b2d37666d4fb84b5b)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''List of locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#locations GoogleStorageControlOrganizationIntelligenceConfig#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d62fb97db1e925ce261a28fe6c66d48f8a295e9173844ab3f302aca7f62f555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ddb78a22eb68aa233299faa642772b0000b1d6eb66b70fb8f0a33f191a9d9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6dcec4b61e8e580d754418ff4ec5f8c977b5aaa496b32d8a0bfd056c270406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleStorageControlOrganizationIntelligenceConfigFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e909042fc07f1cab2e51724fe2acdb991a383b9573f5d17b4fb153746cd574)
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
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#bucket_id_regexes GoogleStorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        value = GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets(
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
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#locations GoogleStorageControlOrganizationIntelligenceConfig#locations}
        '''
        value = GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations(
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
        :param bucket_id_regexes: List of bucket id regexes to exclude in the storage intelligence plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#bucket_id_regexes GoogleStorageControlOrganizationIntelligenceConfig#bucket_id_regexes}
        '''
        value = GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets(
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
        :param locations: List of locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#locations GoogleStorageControlOrganizationIntelligenceConfig#locations}
        '''
        value = GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations(
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
    ) -> GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference:
        return typing.cast(GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference, jsii.get(self, "excludedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocations")
    def excluded_cloud_storage_locations(
        self,
    ) -> GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference:
        return typing.cast(GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference, jsii.get(self, "excludedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBuckets")
    def included_cloud_storage_buckets(
        self,
    ) -> GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference:
        return typing.cast(GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference, jsii.get(self, "includedCloudStorageBuckets"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocations")
    def included_cloud_storage_locations(
        self,
    ) -> GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference:
        return typing.cast(GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference, jsii.get(self, "includedCloudStorageLocations"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageBucketsInput")
    def excluded_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets], jsii.get(self, "excludedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedCloudStorageLocationsInput")
    def excluded_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations], jsii.get(self, "excludedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageBucketsInput")
    def included_cloud_storage_buckets_input(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets], jsii.get(self, "includedCloudStorageBucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedCloudStorageLocationsInput")
    def included_cloud_storage_locations_input(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations], jsii.get(self, "includedCloudStorageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilter]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8966b570ba9f52220c072247452114c7337d1f5ec53f6c9ffb5edbd882d6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleStorageControlOrganizationIntelligenceConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#create GoogleStorageControlOrganizationIntelligenceConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#delete GoogleStorageControlOrganizationIntelligenceConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#update GoogleStorageControlOrganizationIntelligenceConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bcbeb8b7a75ec1514c2b3defd1d1cabe01dcf2404fb6165dad89789374f4d20)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#create GoogleStorageControlOrganizationIntelligenceConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#delete GoogleStorageControlOrganizationIntelligenceConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_storage_control_organization_intelligence_config#update GoogleStorageControlOrganizationIntelligenceConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b2155d82612e64a64e97656eb5a4ec855d460706958dca4aa53743829f96c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fec10c4b27d18847dd1c2a70782459a5094ffb7019d66da51ab39047d4efc59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6b11cd06b3ef317a7526f3861dbf272411caf1d3246d1c0142a0d2d83f2d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd7b957fb89e0f695a64f42ca3f93de7cd08336433a267e3f69bbd49b95d81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlOrganizationIntelligenceConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlOrganizationIntelligenceConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlOrganizationIntelligenceConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b9700a690ef2601b0d2bbf74af075ad6433b63cde43a825a0eed346ac75f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigTrialConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleStorageControlOrganizationIntelligenceConfigTrialConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleStorageControlOrganizationIntelligenceConfigTrialConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleStorageControlOrganizationIntelligenceConfigTrialConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigTrialConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7a9b6e76c21ff6589c8adb1c72eb44e69e18363c4dcc31ab2283a9acbb3ee44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleStorageControlOrganizationIntelligenceConfigTrialConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355a84eecce385f91b5203996c3c8d850f6b8336ccc33e84af87ab24eaa7ba5f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleStorageControlOrganizationIntelligenceConfigTrialConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7080d30f2e532d1ca07e5de546c83d9a9d8f3fa43d94d922c216f366c37fcda8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc3d68ce71719acfbd102e7d16744820f5f1da06f614b191a485898d8747cf2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__219273b39fabdcfea1513b7148670fad5d4c903470e11d13f5628191e2a79b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleStorageControlOrganizationIntelligenceConfigTrialConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleStorageControlOrganizationIntelligenceConfig.GoogleStorageControlOrganizationIntelligenceConfigTrialConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c87ff692228d071a8bdf26c498697a55c8c55086bb33e01bc83614d5a4b3a78f)
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
    ) -> typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigTrialConfig]:
        return typing.cast(typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigTrialConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigTrialConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcef9885fed2359a24dcac7a8e4ef6f48deb4b7a70bac4cb7c731682b9675860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleStorageControlOrganizationIntelligenceConfig",
    "GoogleStorageControlOrganizationIntelligenceConfigConfig",
    "GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig",
    "GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigList",
    "GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfigOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigFilter",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBucketsOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocationsOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBucketsOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocationsOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigFilterOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigTimeouts",
    "GoogleStorageControlOrganizationIntelligenceConfigTimeoutsOutputReference",
    "GoogleStorageControlOrganizationIntelligenceConfigTrialConfig",
    "GoogleStorageControlOrganizationIntelligenceConfigTrialConfigList",
    "GoogleStorageControlOrganizationIntelligenceConfigTrialConfigOutputReference",
]

publication.publish()

def _typecheckingstub__dcfc9d1bb9941bec7fbdcbe2bfba92e1cc795dd3a6dc8db77dad5f88bb0c9820(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    edition_config: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fd8254932bfeef58c2ca4e99d5a315f960d39d900790cbadb7457628db064525(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb1bcb8ac2da0d11c9f0d36abd7eec4761d375eb3be63edca243f0a3bc53786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0389a1dae7aa01659cf6e9bfb890023b79f117e9f7a6d333b4e05555f03c6792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d113a148653451adac10e0e933f4c7118eb26fcb6da2661c23701bec7a4501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46893a1434f5b2f5a5dfac237d6e4df5cf07063e21d36d3a16052866043f2f90(
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
    filter: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4587665fe6ed96478d89c093c5e0c44236b985c4cc8ace084d8b1e1da0b574a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bf1b40baaec4ff893c1846f41567fc88cbadbf6fe4e651d632403df7058cdd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886de24a307ecf7815f940a25ea2cfd1d1b2d49bc9ef62d8c41ded317922e339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f23af29239a1c025ec48b6aa88c5ceb7b111846e7d8f5f3535d63489e372148(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e440ba973944022628e6d6b6728b50ef59a91c369861abad69876e6f94159c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33e7e3c445cddab6dff12748df7c27f574d9dde99838acbf5bdc2b74b86a80d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8c63dbc6f5c43230b533802297990c647f69e1fb030aaffd7ec16faa8788f5(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigEffectiveIntelligenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7abcaaf867ddf612a99a7437bb1ea484956aafa968b7a6a86158d3d9174a8fd(
    *,
    excluded_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_buckets: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets, typing.Dict[builtins.str, typing.Any]]] = None,
    included_cloud_storage_locations: typing.Optional[typing.Union[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56daeb1a253c3722a2998567870c3276791c8da30420acba55e4c3cc3e4a58d4(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db1291448afb88af1888c730d167536e7a1b396ca626a6b1141da2365dd782d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5453f4c936ca2c42b435206487af7e6446e1a3a64aa1a6bf6c294c2a38e1a569(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301b7ed6a85762c28365fd7451935d4d8d9de669b677892df5045cc402dc3e0a(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947f95febb4706928cfb0c4dbebcce42fd00c27467e13bd0530c8a952325b93c(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22629afb2011165024a12f3fb94e85da5882b86b6cd6279a7fc5b1eba7935073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fd5b81e026c480a1d4e4db38170d70fbf71e8506a2eb4bf7619c7cc183c26a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78541a6bf6fafcd6d6470bdde1d018cd79a59972f3d3d49dbfdd54bfad6f8207(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterExcludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7e67e151875c619e793a0818a7a34e31457c4bf6af381134ec030faf9827b5(
    *,
    bucket_id_regexes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff0906c95649dd12a3d32013591348f9485bf2dfd8002ef090afa68391650e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add3031e0e3ae62cdc45f65d0da2876152cb9717d80d0162000d1570f7049351(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92ea11541da7b14102125d5654a04c7074f1b4b8471c5b378380ec3ae9c3704(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageBuckets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7929e8f12e8985028c76f512d78828db62af8017597a00b2d37666d4fb84b5b(
    *,
    locations: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d62fb97db1e925ce261a28fe6c66d48f8a295e9173844ab3f302aca7f62f555(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddb78a22eb68aa233299faa642772b0000b1d6eb66b70fb8f0a33f191a9d9b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6dcec4b61e8e580d754418ff4ec5f8c977b5aaa496b32d8a0bfd056c270406(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilterIncludedCloudStorageLocations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e909042fc07f1cab2e51724fe2acdb991a383b9573f5d17b4fb153746cd574(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8966b570ba9f52220c072247452114c7337d1f5ec53f6c9ffb5edbd882d6f9(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bcbeb8b7a75ec1514c2b3defd1d1cabe01dcf2404fb6165dad89789374f4d20(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b2155d82612e64a64e97656eb5a4ec855d460706958dca4aa53743829f96c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec10c4b27d18847dd1c2a70782459a5094ffb7019d66da51ab39047d4efc59c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6b11cd06b3ef317a7526f3861dbf272411caf1d3246d1c0142a0d2d83f2d72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd7b957fb89e0f695a64f42ca3f93de7cd08336433a267e3f69bbd49b95d81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b9700a690ef2601b0d2bbf74af075ad6433b63cde43a825a0eed346ac75f33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleStorageControlOrganizationIntelligenceConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a9b6e76c21ff6589c8adb1c72eb44e69e18363c4dcc31ab2283a9acbb3ee44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355a84eecce385f91b5203996c3c8d850f6b8336ccc33e84af87ab24eaa7ba5f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7080d30f2e532d1ca07e5de546c83d9a9d8f3fa43d94d922c216f366c37fcda8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3d68ce71719acfbd102e7d16744820f5f1da06f614b191a485898d8747cf2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219273b39fabdcfea1513b7148670fad5d4c903470e11d13f5628191e2a79b40(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87ff692228d071a8bdf26c498697a55c8c55086bb33e01bc83614d5a4b3a78f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcef9885fed2359a24dcac7a8e4ef6f48deb4b7a70bac4cb7c731682b9675860(
    value: typing.Optional[GoogleStorageControlOrganizationIntelligenceConfigTrialConfig],
) -> None:
    """Type checking stubs"""
    pass
