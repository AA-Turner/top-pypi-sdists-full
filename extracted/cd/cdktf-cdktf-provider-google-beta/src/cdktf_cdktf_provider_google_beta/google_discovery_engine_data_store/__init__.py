r'''
# `google_discovery_engine_data_store`

Refer to the Terraform Registry for docs: [`google_discovery_engine_data_store`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store).
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


class GoogleDiscoveryEngineDataStore(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStore",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store google_discovery_engine_data_store}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        content_config: builtins.str,
        data_store_id: builtins.str,
        display_name: builtins.str,
        industry_vertical: builtins.str,
        location: builtins.str,
        advanced_site_search_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        document_processing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store google_discovery_engine_data_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param content_config: The content config of the data store. Possible values: ["NO_CONTENT", "CONTENT_REQUIRED", "PUBLIC_WEBSITE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#content_config GoogleDiscoveryEngineDataStore#content_config}
        :param data_store_id: The unique id of the data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#data_store_id GoogleDiscoveryEngineDataStore#data_store_id}
        :param display_name: The display name of the data store. This field must be a UTF-8 encoded string with a length limit of 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#display_name GoogleDiscoveryEngineDataStore#display_name}
        :param industry_vertical: The industry vertical that the data store registers. Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#industry_vertical GoogleDiscoveryEngineDataStore#industry_vertical}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#location GoogleDiscoveryEngineDataStore#location}
        :param advanced_site_search_config: advanced_site_search_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#advanced_site_search_config GoogleDiscoveryEngineDataStore#advanced_site_search_config}
        :param create_advanced_site_search: If true, an advanced data store for site search will be created. If the data store is not configured as site search (GENERIC vertical and PUBLIC_WEBSITE contentConfig), this flag will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#create_advanced_site_search GoogleDiscoveryEngineDataStore#create_advanced_site_search}
        :param document_processing_config: document_processing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#document_processing_config GoogleDiscoveryEngineDataStore#document_processing_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#id GoogleDiscoveryEngineDataStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#project GoogleDiscoveryEngineDataStore#project}.
        :param skip_default_schema_creation: A boolean flag indicating whether to skip the default schema creation for the data store. Only enable this flag if you are certain that the default schema is incompatible with your use case. If set to true, you must manually create a schema for the data store before any documents can be ingested. This flag cannot be specified if 'data_store.starting_schema' is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#skip_default_schema_creation GoogleDiscoveryEngineDataStore#skip_default_schema_creation}
        :param solution_types: The solutions that the data store enrolls. Possible values: ["SOLUTION_TYPE_RECOMMENDATION", "SOLUTION_TYPE_SEARCH", "SOLUTION_TYPE_CHAT", "SOLUTION_TYPE_GENERATIVE_CHAT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#solution_types GoogleDiscoveryEngineDataStore#solution_types}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#timeouts GoogleDiscoveryEngineDataStore#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c54ea33b1860acfe322f5e2957f6e518230e12a998c320fc4a8a5c59bc97a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDiscoveryEngineDataStoreConfig(
            content_config=content_config,
            data_store_id=data_store_id,
            display_name=display_name,
            industry_vertical=industry_vertical,
            location=location,
            advanced_site_search_config=advanced_site_search_config,
            create_advanced_site_search=create_advanced_site_search,
            document_processing_config=document_processing_config,
            id=id,
            project=project,
            skip_default_schema_creation=skip_default_schema_creation,
            solution_types=solution_types,
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
        '''Generates CDKTF code for importing a GoogleDiscoveryEngineDataStore resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDiscoveryEngineDataStore to import.
        :param import_from_id: The id of the existing GoogleDiscoveryEngineDataStore that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDiscoveryEngineDataStore to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6934bd9498afd3fe4ee5f1941403f77ec28a73d88a1895313742f8999f1e23bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSiteSearchConfig")
    def put_advanced_site_search_config(
        self,
        *,
        disable_automatic_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_initial_index: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_automatic_refresh: If set true, automatic refresh is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#disable_automatic_refresh GoogleDiscoveryEngineDataStore#disable_automatic_refresh}
        :param disable_initial_index: If set true, initial indexing is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#disable_initial_index GoogleDiscoveryEngineDataStore#disable_initial_index}
        '''
        value = GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig(
            disable_automatic_refresh=disable_automatic_refresh,
            disable_initial_index=disable_initial_index,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSiteSearchConfig", [value]))

    @jsii.member(jsii_name="putDocumentProcessingConfig")
    def put_document_processing_config(
        self,
        *,
        chunking_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parsing_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chunking_config: chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#chunking_config GoogleDiscoveryEngineDataStore#chunking_config}
        :param default_parsing_config: default_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#default_parsing_config GoogleDiscoveryEngineDataStore#default_parsing_config}
        :param parsing_config_overrides: parsing_config_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#parsing_config_overrides GoogleDiscoveryEngineDataStore#parsing_config_overrides}
        '''
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfig(
            chunking_config=chunking_config,
            default_parsing_config=default_parsing_config,
            parsing_config_overrides=parsing_config_overrides,
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentProcessingConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#create GoogleDiscoveryEngineDataStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#delete GoogleDiscoveryEngineDataStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#update GoogleDiscoveryEngineDataStore#update}.
        '''
        value = GoogleDiscoveryEngineDataStoreTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedSiteSearchConfig")
    def reset_advanced_site_search_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSiteSearchConfig", []))

    @jsii.member(jsii_name="resetCreateAdvancedSiteSearch")
    def reset_create_advanced_site_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateAdvancedSiteSearch", []))

    @jsii.member(jsii_name="resetDocumentProcessingConfig")
    def reset_document_processing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentProcessingConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSkipDefaultSchemaCreation")
    def reset_skip_default_schema_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipDefaultSchemaCreation", []))

    @jsii.member(jsii_name="resetSolutionTypes")
    def reset_solution_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSolutionTypes", []))

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
    @jsii.member(jsii_name="advancedSiteSearchConfig")
    def advanced_site_search_config(
        self,
    ) -> "GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference", jsii.get(self, "advancedSiteSearchConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="defaultSchemaId")
    def default_schema_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSchemaId"))

    @builtins.property
    @jsii.member(jsii_name="documentProcessingConfig")
    def document_processing_config(
        self,
    ) -> "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigOutputReference":
        return typing.cast("GoogleDiscoveryEngineDataStoreDocumentProcessingConfigOutputReference", jsii.get(self, "documentProcessingConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDiscoveryEngineDataStoreTimeoutsOutputReference":
        return typing.cast("GoogleDiscoveryEngineDataStoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedSiteSearchConfigInput")
    def advanced_site_search_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig"], jsii.get(self, "advancedSiteSearchConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="contentConfigInput")
    def content_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="createAdvancedSiteSearchInput")
    def create_advanced_site_search_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createAdvancedSiteSearchInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreIdInput")
    def data_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreIdInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentProcessingConfigInput")
    def document_processing_config_input(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfig"]:
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfig"], jsii.get(self, "documentProcessingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="industryVerticalInput")
    def industry_vertical_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "industryVerticalInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="skipDefaultSchemaCreationInput")
    def skip_default_schema_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipDefaultSchemaCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="solutionTypesInput")
    def solution_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "solutionTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineDataStoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDiscoveryEngineDataStoreTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="contentConfig")
    def content_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentConfig"))

    @content_config.setter
    def content_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24adaef055167257aa3eda46ef7e5457cc4eb8162e628005bcb57546d8d5e511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createAdvancedSiteSearch")
    def create_advanced_site_search(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createAdvancedSiteSearch"))

    @create_advanced_site_search.setter
    def create_advanced_site_search(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14bafd94fea5a0d13c16ed192ce544d069c6bc2611d76471e1b83c2a15d285d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAdvancedSiteSearch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreId")
    def data_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreId"))

    @data_store_id.setter
    def data_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc63cb4a46d7e78aef9637f9f584070ca0f9878857e917c5dd527d72f16a8f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017289dc62336a50f44f2f70c9187d2d08697126106e03cad53a677330536b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c261ecfdef3001b1a315868f0835e52e4cbf1bebe688d8cd2a344e1b72973a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6887a83427a5d0f9a29217a3522851598fd677b4e024268f97d98d5767ba5a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30d8cbbdcd60d2c9cfce9e1ef4919c6bb7acaabd43cb1e156082ba239501fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3b2d483487c6b75a3e5679c7b3f613f0d0191d6bd87f1e83415e240b62bdaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipDefaultSchemaCreation")
    def skip_default_schema_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipDefaultSchemaCreation"))

    @skip_default_schema_creation.setter
    def skip_default_schema_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693d174113597bd4dba55dc52335f33ed3a428fc1b4805424d48a8f79e75e48b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipDefaultSchemaCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="solutionTypes")
    def solution_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "solutionTypes"))

    @solution_types.setter
    def solution_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76871c98c2a43a8aec0e1a263716fd31311549b928a46150b9edf46d71f06f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "solutionTypes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_automatic_refresh": "disableAutomaticRefresh",
        "disable_initial_index": "disableInitialIndex",
    },
)
class GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig:
    def __init__(
        self,
        *,
        disable_automatic_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_initial_index: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_automatic_refresh: If set true, automatic refresh is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#disable_automatic_refresh GoogleDiscoveryEngineDataStore#disable_automatic_refresh}
        :param disable_initial_index: If set true, initial indexing is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#disable_initial_index GoogleDiscoveryEngineDataStore#disable_initial_index}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f96a788b4aa18ac61fc9b8c1f3b901d12396999afe749d24b8a1503f8c51fb)
            check_type(argname="argument disable_automatic_refresh", value=disable_automatic_refresh, expected_type=type_hints["disable_automatic_refresh"])
            check_type(argname="argument disable_initial_index", value=disable_initial_index, expected_type=type_hints["disable_initial_index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_automatic_refresh is not None:
            self._values["disable_automatic_refresh"] = disable_automatic_refresh
        if disable_initial_index is not None:
            self._values["disable_initial_index"] = disable_initial_index

    @builtins.property
    def disable_automatic_refresh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set true, automatic refresh is disabled for the DataStore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#disable_automatic_refresh GoogleDiscoveryEngineDataStore#disable_automatic_refresh}
        '''
        result = self._values.get("disable_automatic_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_initial_index(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set true, initial indexing is disabled for the DataStore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#disable_initial_index GoogleDiscoveryEngineDataStore#disable_initial_index}
        '''
        result = self._values.get("disable_initial_index")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75910f8ace077e3791c4063ef025f4fe82e8d1f6646a14a4ce49d60fb687e27e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableAutomaticRefresh")
    def reset_disable_automatic_refresh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutomaticRefresh", []))

    @jsii.member(jsii_name="resetDisableInitialIndex")
    def reset_disable_initial_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableInitialIndex", []))

    @builtins.property
    @jsii.member(jsii_name="disableAutomaticRefreshInput")
    def disable_automatic_refresh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAutomaticRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="disableInitialIndexInput")
    def disable_initial_index_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableInitialIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutomaticRefresh")
    def disable_automatic_refresh(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAutomaticRefresh"))

    @disable_automatic_refresh.setter
    def disable_automatic_refresh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4f0f8a9ddadf231246da33c121d291b7619a8ec3771393ea87bf95f09b9bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutomaticRefresh", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableInitialIndex")
    def disable_initial_index(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableInitialIndex"))

    @disable_initial_index.setter
    def disable_initial_index(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bec098ba6680e29ac80e5d340f686040ef0504b14a847dc9f6e70aeb17e22b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableInitialIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f19e329d05e8a27ff196e7545a07204edf4ea4fa72daf1b0395c1d23957d97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "content_config": "contentConfig",
        "data_store_id": "dataStoreId",
        "display_name": "displayName",
        "industry_vertical": "industryVertical",
        "location": "location",
        "advanced_site_search_config": "advancedSiteSearchConfig",
        "create_advanced_site_search": "createAdvancedSiteSearch",
        "document_processing_config": "documentProcessingConfig",
        "id": "id",
        "project": "project",
        "skip_default_schema_creation": "skipDefaultSchemaCreation",
        "solution_types": "solutionTypes",
        "timeouts": "timeouts",
    },
)
class GoogleDiscoveryEngineDataStoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        content_config: builtins.str,
        data_store_id: builtins.str,
        display_name: builtins.str,
        industry_vertical: builtins.str,
        location: builtins.str,
        advanced_site_search_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        document_processing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param content_config: The content config of the data store. Possible values: ["NO_CONTENT", "CONTENT_REQUIRED", "PUBLIC_WEBSITE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#content_config GoogleDiscoveryEngineDataStore#content_config}
        :param data_store_id: The unique id of the data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#data_store_id GoogleDiscoveryEngineDataStore#data_store_id}
        :param display_name: The display name of the data store. This field must be a UTF-8 encoded string with a length limit of 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#display_name GoogleDiscoveryEngineDataStore#display_name}
        :param industry_vertical: The industry vertical that the data store registers. Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#industry_vertical GoogleDiscoveryEngineDataStore#industry_vertical}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#location GoogleDiscoveryEngineDataStore#location}
        :param advanced_site_search_config: advanced_site_search_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#advanced_site_search_config GoogleDiscoveryEngineDataStore#advanced_site_search_config}
        :param create_advanced_site_search: If true, an advanced data store for site search will be created. If the data store is not configured as site search (GENERIC vertical and PUBLIC_WEBSITE contentConfig), this flag will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#create_advanced_site_search GoogleDiscoveryEngineDataStore#create_advanced_site_search}
        :param document_processing_config: document_processing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#document_processing_config GoogleDiscoveryEngineDataStore#document_processing_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#id GoogleDiscoveryEngineDataStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#project GoogleDiscoveryEngineDataStore#project}.
        :param skip_default_schema_creation: A boolean flag indicating whether to skip the default schema creation for the data store. Only enable this flag if you are certain that the default schema is incompatible with your use case. If set to true, you must manually create a schema for the data store before any documents can be ingested. This flag cannot be specified if 'data_store.starting_schema' is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#skip_default_schema_creation GoogleDiscoveryEngineDataStore#skip_default_schema_creation}
        :param solution_types: The solutions that the data store enrolls. Possible values: ["SOLUTION_TYPE_RECOMMENDATION", "SOLUTION_TYPE_SEARCH", "SOLUTION_TYPE_CHAT", "SOLUTION_TYPE_GENERATIVE_CHAT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#solution_types GoogleDiscoveryEngineDataStore#solution_types}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#timeouts GoogleDiscoveryEngineDataStore#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_site_search_config, dict):
            advanced_site_search_config = GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig(**advanced_site_search_config)
        if isinstance(document_processing_config, dict):
            document_processing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfig(**document_processing_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDiscoveryEngineDataStoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f135a0683947028653da4263012223560cf02002a6aa054e06cc6f4cc6f6cf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument content_config", value=content_config, expected_type=type_hints["content_config"])
            check_type(argname="argument data_store_id", value=data_store_id, expected_type=type_hints["data_store_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument industry_vertical", value=industry_vertical, expected_type=type_hints["industry_vertical"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument advanced_site_search_config", value=advanced_site_search_config, expected_type=type_hints["advanced_site_search_config"])
            check_type(argname="argument create_advanced_site_search", value=create_advanced_site_search, expected_type=type_hints["create_advanced_site_search"])
            check_type(argname="argument document_processing_config", value=document_processing_config, expected_type=type_hints["document_processing_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument skip_default_schema_creation", value=skip_default_schema_creation, expected_type=type_hints["skip_default_schema_creation"])
            check_type(argname="argument solution_types", value=solution_types, expected_type=type_hints["solution_types"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_config": content_config,
            "data_store_id": data_store_id,
            "display_name": display_name,
            "industry_vertical": industry_vertical,
            "location": location,
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
        if advanced_site_search_config is not None:
            self._values["advanced_site_search_config"] = advanced_site_search_config
        if create_advanced_site_search is not None:
            self._values["create_advanced_site_search"] = create_advanced_site_search
        if document_processing_config is not None:
            self._values["document_processing_config"] = document_processing_config
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if skip_default_schema_creation is not None:
            self._values["skip_default_schema_creation"] = skip_default_schema_creation
        if solution_types is not None:
            self._values["solution_types"] = solution_types
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
    def content_config(self) -> builtins.str:
        '''The content config of the data store. Possible values: ["NO_CONTENT", "CONTENT_REQUIRED", "PUBLIC_WEBSITE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#content_config GoogleDiscoveryEngineDataStore#content_config}
        '''
        result = self._values.get("content_config")
        assert result is not None, "Required property 'content_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_id(self) -> builtins.str:
        '''The unique id of the data store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#data_store_id GoogleDiscoveryEngineDataStore#data_store_id}
        '''
        result = self._values.get("data_store_id")
        assert result is not None, "Required property 'data_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the data store.

        This field must be a UTF-8 encoded
        string with a length limit of 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#display_name GoogleDiscoveryEngineDataStore#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def industry_vertical(self) -> builtins.str:
        '''The industry vertical that the data store registers. Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#industry_vertical GoogleDiscoveryEngineDataStore#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        assert result is not None, "Required property 'industry_vertical' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#location GoogleDiscoveryEngineDataStore#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_site_search_config(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig]:
        '''advanced_site_search_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#advanced_site_search_config GoogleDiscoveryEngineDataStore#advanced_site_search_config}
        '''
        result = self._values.get("advanced_site_search_config")
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig], result)

    @builtins.property
    def create_advanced_site_search(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, an advanced data store for site search will be created.

        If the
        data store is not configured as site search (GENERIC vertical and
        PUBLIC_WEBSITE contentConfig), this flag will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#create_advanced_site_search GoogleDiscoveryEngineDataStore#create_advanced_site_search}
        '''
        result = self._values.get("create_advanced_site_search")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def document_processing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfig"]:
        '''document_processing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#document_processing_config GoogleDiscoveryEngineDataStore#document_processing_config}
        '''
        result = self._values.get("document_processing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#id GoogleDiscoveryEngineDataStore#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#project GoogleDiscoveryEngineDataStore#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_default_schema_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean flag indicating whether to skip the default schema creation for the data store.

        Only enable this flag if you are certain that the default
        schema is incompatible with your use case.
        If set to true, you must manually create a schema for the data store
        before any documents can be ingested.
        This flag cannot be specified if 'data_store.starting_schema' is
        specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#skip_default_schema_creation GoogleDiscoveryEngineDataStore#skip_default_schema_creation}
        '''
        result = self._values.get("skip_default_schema_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def solution_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The solutions that the data store enrolls. Possible values: ["SOLUTION_TYPE_RECOMMENDATION", "SOLUTION_TYPE_SEARCH", "SOLUTION_TYPE_CHAT", "SOLUTION_TYPE_GENERATIVE_CHAT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#solution_types GoogleDiscoveryEngineDataStore#solution_types}
        '''
        result = self._values.get("solution_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDiscoveryEngineDataStoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#timeouts GoogleDiscoveryEngineDataStore#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "chunking_config": "chunkingConfig",
        "default_parsing_config": "defaultParsingConfig",
        "parsing_config_overrides": "parsingConfigOverrides",
    },
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfig:
    def __init__(
        self,
        *,
        chunking_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parsing_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chunking_config: chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#chunking_config GoogleDiscoveryEngineDataStore#chunking_config}
        :param default_parsing_config: default_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#default_parsing_config GoogleDiscoveryEngineDataStore#default_parsing_config}
        :param parsing_config_overrides: parsing_config_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#parsing_config_overrides GoogleDiscoveryEngineDataStore#parsing_config_overrides}
        '''
        if isinstance(chunking_config, dict):
            chunking_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig(**chunking_config)
        if isinstance(default_parsing_config, dict):
            default_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig(**default_parsing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f06b8ba8abb8efe45bf0bd11dc023df7ffee6920e636488f4b7fdc783c2378)
            check_type(argname="argument chunking_config", value=chunking_config, expected_type=type_hints["chunking_config"])
            check_type(argname="argument default_parsing_config", value=default_parsing_config, expected_type=type_hints["default_parsing_config"])
            check_type(argname="argument parsing_config_overrides", value=parsing_config_overrides, expected_type=type_hints["parsing_config_overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chunking_config is not None:
            self._values["chunking_config"] = chunking_config
        if default_parsing_config is not None:
            self._values["default_parsing_config"] = default_parsing_config
        if parsing_config_overrides is not None:
            self._values["parsing_config_overrides"] = parsing_config_overrides

    @builtins.property
    def chunking_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig"]:
        '''chunking_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#chunking_config GoogleDiscoveryEngineDataStore#chunking_config}
        '''
        result = self._values.get("chunking_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig"], result)

    @builtins.property
    def default_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig"]:
        '''default_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#default_parsing_config GoogleDiscoveryEngineDataStore#default_parsing_config}
        '''
        result = self._values.get("default_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig"], result)

    @builtins.property
    def parsing_config_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]]:
        '''parsing_config_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#parsing_config_overrides GoogleDiscoveryEngineDataStore#parsing_config_overrides}
        '''
        result = self._values.get("parsing_config_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig",
    jsii_struct_bases=[],
    name_mapping={"layout_based_chunking_config": "layoutBasedChunkingConfig"},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig:
    def __init__(
        self,
        *,
        layout_based_chunking_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param layout_based_chunking_config: layout_based_chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_based_chunking_config GoogleDiscoveryEngineDataStore#layout_based_chunking_config}
        '''
        if isinstance(layout_based_chunking_config, dict):
            layout_based_chunking_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig(**layout_based_chunking_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbb5759a3897b0df6a402feba90babcaf37887e53f91de7230a4bebdb6c5716)
            check_type(argname="argument layout_based_chunking_config", value=layout_based_chunking_config, expected_type=type_hints["layout_based_chunking_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if layout_based_chunking_config is not None:
            self._values["layout_based_chunking_config"] = layout_based_chunking_config

    @builtins.property
    def layout_based_chunking_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig"]:
        '''layout_based_chunking_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_based_chunking_config GoogleDiscoveryEngineDataStore#layout_based_chunking_config}
        '''
        result = self._values.get("layout_based_chunking_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "chunk_size": "chunkSize",
        "include_ancestor_headings": "includeAncestorHeadings",
    },
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig:
    def __init__(
        self,
        *,
        chunk_size: typing.Optional[jsii.Number] = None,
        include_ancestor_headings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param chunk_size: The token size limit for each chunk. Supported values: 100-500 (inclusive). Default value: 500. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#chunk_size GoogleDiscoveryEngineDataStore#chunk_size}
        :param include_ancestor_headings: Whether to include appending different levels of headings to chunks from the middle of the document to prevent context loss. Default value: False. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#include_ancestor_headings GoogleDiscoveryEngineDataStore#include_ancestor_headings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a92895b5f6951bf431a4246677bd6733a2458982a4c7e32d5677cc21a4e670)
            check_type(argname="argument chunk_size", value=chunk_size, expected_type=type_hints["chunk_size"])
            check_type(argname="argument include_ancestor_headings", value=include_ancestor_headings, expected_type=type_hints["include_ancestor_headings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chunk_size is not None:
            self._values["chunk_size"] = chunk_size
        if include_ancestor_headings is not None:
            self._values["include_ancestor_headings"] = include_ancestor_headings

    @builtins.property
    def chunk_size(self) -> typing.Optional[jsii.Number]:
        '''The token size limit for each chunk. Supported values: 100-500 (inclusive). Default value: 500.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#chunk_size GoogleDiscoveryEngineDataStore#chunk_size}
        '''
        result = self._values.get("chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def include_ancestor_headings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to include appending different levels of headings to chunks from the middle of the document to prevent context loss.

        Default value: False.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#include_ancestor_headings GoogleDiscoveryEngineDataStore#include_ancestor_headings}
        '''
        result = self._values.get("include_ancestor_headings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45dc4cd6ebabaf8ecdff2f3dc4146f2a433e5792aeda6ffcbeedfd76ce793fa2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChunkSize")
    def reset_chunk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChunkSize", []))

    @jsii.member(jsii_name="resetIncludeAncestorHeadings")
    def reset_include_ancestor_headings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAncestorHeadings", []))

    @builtins.property
    @jsii.member(jsii_name="chunkSizeInput")
    def chunk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "chunkSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAncestorHeadingsInput")
    def include_ancestor_headings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAncestorHeadingsInput"))

    @builtins.property
    @jsii.member(jsii_name="chunkSize")
    def chunk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "chunkSize"))

    @chunk_size.setter
    def chunk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1737ec9ef4a52b8cf62f73bd91c2e36063b939cf41e2be3c796bea3e666fa6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chunkSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeAncestorHeadings")
    def include_ancestor_headings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAncestorHeadings"))

    @include_ancestor_headings.setter
    def include_ancestor_headings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7a8e85ae8b6919dd5198b30065bb45a2ce942004e62a21dcc52042d6de711d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAncestorHeadings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727878963f11c66544b2eb7a49e54e421624810a92f078078fa1be42f91a153e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eae2948b1f9183c57c3e4c46419ac166d96c4641f23139a12521771c670b7b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLayoutBasedChunkingConfig")
    def put_layout_based_chunking_config(
        self,
        *,
        chunk_size: typing.Optional[jsii.Number] = None,
        include_ancestor_headings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param chunk_size: The token size limit for each chunk. Supported values: 100-500 (inclusive). Default value: 500. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#chunk_size GoogleDiscoveryEngineDataStore#chunk_size}
        :param include_ancestor_headings: Whether to include appending different levels of headings to chunks from the middle of the document to prevent context loss. Default value: False. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#include_ancestor_headings GoogleDiscoveryEngineDataStore#include_ancestor_headings}
        '''
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig(
            chunk_size=chunk_size, include_ancestor_headings=include_ancestor_headings
        )

        return typing.cast(None, jsii.invoke(self, "putLayoutBasedChunkingConfig", [value]))

    @jsii.member(jsii_name="resetLayoutBasedChunkingConfig")
    def reset_layout_based_chunking_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayoutBasedChunkingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="layoutBasedChunkingConfig")
    def layout_based_chunking_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference, jsii.get(self, "layoutBasedChunkingConfig"))

    @builtins.property
    @jsii.member(jsii_name="layoutBasedChunkingConfigInput")
    def layout_based_chunking_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig], jsii.get(self, "layoutBasedChunkingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89326247f63688536641306b26d0ec9bd92e5264438e2d25b850e4f2699904a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "digital_parsing_config": "digitalParsingConfig",
        "layout_parsing_config": "layoutParsingConfig",
        "ocr_parsing_config": "ocrParsingConfig",
    },
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig:
    def __init__(
        self,
        *,
        digital_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        layout_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ocr_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param digital_parsing_config: digital_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#digital_parsing_config GoogleDiscoveryEngineDataStore#digital_parsing_config}
        :param layout_parsing_config: layout_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_parsing_config GoogleDiscoveryEngineDataStore#layout_parsing_config}
        :param ocr_parsing_config: ocr_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#ocr_parsing_config GoogleDiscoveryEngineDataStore#ocr_parsing_config}
        '''
        if isinstance(digital_parsing_config, dict):
            digital_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig(**digital_parsing_config)
        if isinstance(layout_parsing_config, dict):
            layout_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig(**layout_parsing_config)
        if isinstance(ocr_parsing_config, dict):
            ocr_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig(**ocr_parsing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097ffe5dbc60b6047fa1ad4f4955b1851577954304bf9be15d46ab1643680bab)
            check_type(argname="argument digital_parsing_config", value=digital_parsing_config, expected_type=type_hints["digital_parsing_config"])
            check_type(argname="argument layout_parsing_config", value=layout_parsing_config, expected_type=type_hints["layout_parsing_config"])
            check_type(argname="argument ocr_parsing_config", value=ocr_parsing_config, expected_type=type_hints["ocr_parsing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if digital_parsing_config is not None:
            self._values["digital_parsing_config"] = digital_parsing_config
        if layout_parsing_config is not None:
            self._values["layout_parsing_config"] = layout_parsing_config
        if ocr_parsing_config is not None:
            self._values["ocr_parsing_config"] = ocr_parsing_config

    @builtins.property
    def digital_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig"]:
        '''digital_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#digital_parsing_config GoogleDiscoveryEngineDataStore#digital_parsing_config}
        '''
        result = self._values.get("digital_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig"], result)

    @builtins.property
    def layout_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig"]:
        '''layout_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_parsing_config GoogleDiscoveryEngineDataStore#layout_parsing_config}
        '''
        result = self._values.get("layout_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig"], result)

    @builtins.property
    def ocr_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig"]:
        '''ocr_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#ocr_parsing_config GoogleDiscoveryEngineDataStore#ocr_parsing_config}
        '''
        result = self._values.get("ocr_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f04edfd19d63d13670e6482c40bb1fa55cdadbe03ffa4888543024f87c6f2e74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27de7be61e0c789569bdd043c685321acc758066d17cda85d4412de444fa7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__788f1610f02a969bbd8424e807f76c70fbcdfb82103b61d601063f7e65fbce5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bef8d54e367744bcd67a99edfae319573d184fb73f6525d0b99a8001adde98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig",
    jsii_struct_bases=[],
    name_mapping={"use_native_text": "useNativeText"},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig:
    def __init__(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#use_native_text GoogleDiscoveryEngineDataStore#use_native_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c8ceb3574459b34098839e0f777176405c3e69c7cf4326f29bcc59876549fe)
            check_type(argname="argument use_native_text", value=use_native_text, expected_type=type_hints["use_native_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if use_native_text is not None:
            self._values["use_native_text"] = use_native_text

    @builtins.property
    def use_native_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, will use native text instead of OCR text on pages containing native text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#use_native_text GoogleDiscoveryEngineDataStore#use_native_text}
        '''
        result = self._values.get("use_native_text")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3b5d75f9b10277a8858d86feac8f4e250c7f2f1e2bcd842d74a8140df9547d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUseNativeText")
    def reset_use_native_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseNativeText", []))

    @builtins.property
    @jsii.member(jsii_name="useNativeTextInput")
    def use_native_text_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useNativeTextInput"))

    @builtins.property
    @jsii.member(jsii_name="useNativeText")
    def use_native_text(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useNativeText"))

    @use_native_text.setter
    def use_native_text(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d7ac7a20b9efc5389e0eee6812fe8aace74450df9115645d4b7d03265dda97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNativeText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e0940137878a5986e1a68553c9d7f7d7a3b5ac506a52e40f9380808d733304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a189beecf952cedf30b140ce6d6c6557564804af40af42e35ed642829224e0cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDigitalParsingConfig")
    def put_digital_parsing_config(self) -> None:
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig()

        return typing.cast(None, jsii.invoke(self, "putDigitalParsingConfig", [value]))

    @jsii.member(jsii_name="putLayoutParsingConfig")
    def put_layout_parsing_config(self) -> None:
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig()

        return typing.cast(None, jsii.invoke(self, "putLayoutParsingConfig", [value]))

    @jsii.member(jsii_name="putOcrParsingConfig")
    def put_ocr_parsing_config(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#use_native_text GoogleDiscoveryEngineDataStore#use_native_text}
        '''
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig(
            use_native_text=use_native_text
        )

        return typing.cast(None, jsii.invoke(self, "putOcrParsingConfig", [value]))

    @jsii.member(jsii_name="resetDigitalParsingConfig")
    def reset_digital_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigitalParsingConfig", []))

    @jsii.member(jsii_name="resetLayoutParsingConfig")
    def reset_layout_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayoutParsingConfig", []))

    @jsii.member(jsii_name="resetOcrParsingConfig")
    def reset_ocr_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcrParsingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="digitalParsingConfig")
    def digital_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference, jsii.get(self, "digitalParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfig")
    def layout_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference, jsii.get(self, "layoutParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfig")
    def ocr_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference, jsii.get(self, "ocrParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="digitalParsingConfigInput")
    def digital_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig], jsii.get(self, "digitalParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfigInput")
    def layout_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig], jsii.get(self, "layoutParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfigInput")
    def ocr_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig], jsii.get(self, "ocrParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588950a89dd28bceec43e3e90103a571d4236de9ebf9944e9aab8e315309f61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec76dffa92a10fec5f73e0c1199833df1e7e6359aa57805fb6ad11672caba213)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putChunkingConfig")
    def put_chunking_config(
        self,
        *,
        layout_based_chunking_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param layout_based_chunking_config: layout_based_chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_based_chunking_config GoogleDiscoveryEngineDataStore#layout_based_chunking_config}
        '''
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig(
            layout_based_chunking_config=layout_based_chunking_config
        )

        return typing.cast(None, jsii.invoke(self, "putChunkingConfig", [value]))

    @jsii.member(jsii_name="putDefaultParsingConfig")
    def put_default_parsing_config(
        self,
        *,
        digital_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        layout_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        ocr_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param digital_parsing_config: digital_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#digital_parsing_config GoogleDiscoveryEngineDataStore#digital_parsing_config}
        :param layout_parsing_config: layout_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_parsing_config GoogleDiscoveryEngineDataStore#layout_parsing_config}
        :param ocr_parsing_config: ocr_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#ocr_parsing_config GoogleDiscoveryEngineDataStore#ocr_parsing_config}
        '''
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig(
            digital_parsing_config=digital_parsing_config,
            layout_parsing_config=layout_parsing_config,
            ocr_parsing_config=ocr_parsing_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultParsingConfig", [value]))

    @jsii.member(jsii_name="putParsingConfigOverrides")
    def put_parsing_config_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622751bed01a88f268caecbabe4a4fa1b0ee3d7b8d8e497e1dc8db82e6ddeb83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParsingConfigOverrides", [value]))

    @jsii.member(jsii_name="resetChunkingConfig")
    def reset_chunking_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChunkingConfig", []))

    @jsii.member(jsii_name="resetDefaultParsingConfig")
    def reset_default_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultParsingConfig", []))

    @jsii.member(jsii_name="resetParsingConfigOverrides")
    def reset_parsing_config_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParsingConfigOverrides", []))

    @builtins.property
    @jsii.member(jsii_name="chunkingConfig")
    def chunking_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference, jsii.get(self, "chunkingConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultParsingConfig")
    def default_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference, jsii.get(self, "defaultParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="parsingConfigOverrides")
    def parsing_config_overrides(
        self,
    ) -> "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList":
        return typing.cast("GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList", jsii.get(self, "parsingConfigOverrides"))

    @builtins.property
    @jsii.member(jsii_name="chunkingConfigInput")
    def chunking_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig], jsii.get(self, "chunkingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultParsingConfigInput")
    def default_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig], jsii.get(self, "defaultParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingConfigOverridesInput")
    def parsing_config_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]], jsii.get(self, "parsingConfigOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ff3c65923ac97c47f4fecff726337e24b59d12b603133cbead184a5f1a5a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "file_type": "fileType",
        "digital_parsing_config": "digitalParsingConfig",
        "layout_parsing_config": "layoutParsingConfig",
        "ocr_parsing_config": "ocrParsingConfig",
    },
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides:
    def __init__(
        self,
        *,
        file_type: builtins.str,
        digital_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        layout_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ocr_parsing_config: typing.Optional[typing.Union["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#file_type GoogleDiscoveryEngineDataStore#file_type}.
        :param digital_parsing_config: digital_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#digital_parsing_config GoogleDiscoveryEngineDataStore#digital_parsing_config}
        :param layout_parsing_config: layout_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_parsing_config GoogleDiscoveryEngineDataStore#layout_parsing_config}
        :param ocr_parsing_config: ocr_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#ocr_parsing_config GoogleDiscoveryEngineDataStore#ocr_parsing_config}
        '''
        if isinstance(digital_parsing_config, dict):
            digital_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig(**digital_parsing_config)
        if isinstance(layout_parsing_config, dict):
            layout_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig(**layout_parsing_config)
        if isinstance(ocr_parsing_config, dict):
            ocr_parsing_config = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig(**ocr_parsing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0dc59ccfba71edc7ab550d7398eb1a7f9c9dcf806d9f91ded049c5a838fcc7)
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
            check_type(argname="argument digital_parsing_config", value=digital_parsing_config, expected_type=type_hints["digital_parsing_config"])
            check_type(argname="argument layout_parsing_config", value=layout_parsing_config, expected_type=type_hints["layout_parsing_config"])
            check_type(argname="argument ocr_parsing_config", value=ocr_parsing_config, expected_type=type_hints["ocr_parsing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_type": file_type,
        }
        if digital_parsing_config is not None:
            self._values["digital_parsing_config"] = digital_parsing_config
        if layout_parsing_config is not None:
            self._values["layout_parsing_config"] = layout_parsing_config
        if ocr_parsing_config is not None:
            self._values["ocr_parsing_config"] = ocr_parsing_config

    @builtins.property
    def file_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#file_type GoogleDiscoveryEngineDataStore#file_type}.'''
        result = self._values.get("file_type")
        assert result is not None, "Required property 'file_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def digital_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig"]:
        '''digital_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#digital_parsing_config GoogleDiscoveryEngineDataStore#digital_parsing_config}
        '''
        result = self._values.get("digital_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig"], result)

    @builtins.property
    def layout_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig"]:
        '''layout_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#layout_parsing_config GoogleDiscoveryEngineDataStore#layout_parsing_config}
        '''
        result = self._values.get("layout_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig"], result)

    @builtins.property
    def ocr_parsing_config(
        self,
    ) -> typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig"]:
        '''ocr_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#ocr_parsing_config GoogleDiscoveryEngineDataStore#ocr_parsing_config}
        '''
        result = self._values.get("ocr_parsing_config")
        return typing.cast(typing.Optional["GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f56122af845ea63d524a098568657580f0aa7be58c44c8aa58693bc3da29775)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca365b6128a8db84cf8cccee271fe3c2f616199e53aaffe8106c89d83259f256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d069e37732c47db9914bb2fd1df0e5f100a4744d0941d762102d3b92accbdaaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37dbde4a7b2a1ca01f7226eb9d067ea057d2132a7922df4512e1a3d588f5c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6770caeea2872967bbf7db490ca8a8e7519c12cedec352f592d8ab1c231a345)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ae32d8f5c58a5716a4c75f5dd2b9993873b4a9741ba6ce3dbba59145cfbb7f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dba7d5bf29d4525c9264ecdc146e413715be2b7566b754247441ed3d76ec0e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dc1e972937c95ac69de9eb5954c746bd50b64c47ef4cfbaef36fa0bbc4dbb32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__448cf26a01218465cdf77919f531b5e4a6611fbe371776e820e3283870e88217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc617177c5d8d662e42092a880fb1052d92930515752963f8332a76cec17bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig",
    jsii_struct_bases=[],
    name_mapping={"use_native_text": "useNativeText"},
)
class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig:
    def __init__(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#use_native_text GoogleDiscoveryEngineDataStore#use_native_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda7902b09ba1164509528e434c6e7b781a5970e8711e93e445b9fed5db51b99)
            check_type(argname="argument use_native_text", value=use_native_text, expected_type=type_hints["use_native_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if use_native_text is not None:
            self._values["use_native_text"] = use_native_text

    @builtins.property
    def use_native_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, will use native text instead of OCR text on pages containing native text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#use_native_text GoogleDiscoveryEngineDataStore#use_native_text}
        '''
        result = self._values.get("use_native_text")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29894ea5c86be9f48319b8c8b1e98c4af812cfd330637230b739bbc4411cc08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUseNativeText")
    def reset_use_native_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseNativeText", []))

    @builtins.property
    @jsii.member(jsii_name="useNativeTextInput")
    def use_native_text_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useNativeTextInput"))

    @builtins.property
    @jsii.member(jsii_name="useNativeText")
    def use_native_text(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useNativeText"))

    @use_native_text.setter
    def use_native_text(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a7a6905fac880b3e623ee8c35e614a458b9179786496a002a0798a1f45b930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNativeText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48de9026dc5e3c622f0cdcd22b099ccf51199044e70d5c5215b41f1c09ec314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e839afc8dde94cfdef7d5d9a0ce5d2d0386513a00901e21193fe7027b709a67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDigitalParsingConfig")
    def put_digital_parsing_config(self) -> None:
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig()

        return typing.cast(None, jsii.invoke(self, "putDigitalParsingConfig", [value]))

    @jsii.member(jsii_name="putLayoutParsingConfig")
    def put_layout_parsing_config(self) -> None:
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig()

        return typing.cast(None, jsii.invoke(self, "putLayoutParsingConfig", [value]))

    @jsii.member(jsii_name="putOcrParsingConfig")
    def put_ocr_parsing_config(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#use_native_text GoogleDiscoveryEngineDataStore#use_native_text}
        '''
        value = GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig(
            use_native_text=use_native_text
        )

        return typing.cast(None, jsii.invoke(self, "putOcrParsingConfig", [value]))

    @jsii.member(jsii_name="resetDigitalParsingConfig")
    def reset_digital_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigitalParsingConfig", []))

    @jsii.member(jsii_name="resetLayoutParsingConfig")
    def reset_layout_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLayoutParsingConfig", []))

    @jsii.member(jsii_name="resetOcrParsingConfig")
    def reset_ocr_parsing_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcrParsingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="digitalParsingConfig")
    def digital_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference, jsii.get(self, "digitalParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfig")
    def layout_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference, jsii.get(self, "layoutParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfig")
    def ocr_parsing_config(
        self,
    ) -> GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference:
        return typing.cast(GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference, jsii.get(self, "ocrParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="digitalParsingConfigInput")
    def digital_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig], jsii.get(self, "digitalParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfigInput")
    def layout_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig], jsii.get(self, "layoutParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfigInput")
    def ocr_parsing_config_input(
        self,
    ) -> typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig]:
        return typing.cast(typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig], jsii.get(self, "ocrParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911b61c1a6e0aada48795bfdddd17940056b4ac485d3738a9e7513212dc6f16a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc17199f45e96fced078339aa11ca5edfafe0e4d0f73c531b640fc3283eaa43a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDiscoveryEngineDataStoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#create GoogleDiscoveryEngineDataStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#delete GoogleDiscoveryEngineDataStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#update GoogleDiscoveryEngineDataStore#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ab3c91925604242e961e52a3dbc281acbc0519b6a0814634ca241583e1c42d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#create GoogleDiscoveryEngineDataStore#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#delete GoogleDiscoveryEngineDataStore#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_discovery_engine_data_store#update GoogleDiscoveryEngineDataStore#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDiscoveryEngineDataStoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDiscoveryEngineDataStoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDiscoveryEngineDataStore.GoogleDiscoveryEngineDataStoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8b6caf0c6f17ed3864a4bf1b19ff2ce01462409958b93b028c0f41438e6cbca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e1f97209e025520796d6fa30ad99aec05bd33c2be2e75d538051ef23a075547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e69d7bb8531b43530f3657344dd4e33a5ed5cdf8abcd17a3297e9ab8830115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429f720e6c63e3d065f0dce1bedb47f72ee422467a8604b9b698123c356374c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fe6fd3f61a65145b0224c33b1df16c74fc88537448b4a198297b92b5df9d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDiscoveryEngineDataStore",
    "GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig",
    "GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference",
    "GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference",
    "GoogleDiscoveryEngineDataStoreTimeouts",
    "GoogleDiscoveryEngineDataStoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__91c54ea33b1860acfe322f5e2957f6e518230e12a998c320fc4a8a5c59bc97a5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    content_config: builtins.str,
    data_store_id: builtins.str,
    display_name: builtins.str,
    industry_vertical: builtins.str,
    location: builtins.str,
    advanced_site_search_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    document_processing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6934bd9498afd3fe4ee5f1941403f77ec28a73d88a1895313742f8999f1e23bb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24adaef055167257aa3eda46ef7e5457cc4eb8162e628005bcb57546d8d5e511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14bafd94fea5a0d13c16ed192ce544d069c6bc2611d76471e1b83c2a15d285d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc63cb4a46d7e78aef9637f9f584070ca0f9878857e917c5dd527d72f16a8f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017289dc62336a50f44f2f70c9187d2d08697126106e03cad53a677330536b18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c261ecfdef3001b1a315868f0835e52e4cbf1bebe688d8cd2a344e1b72973a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6887a83427a5d0f9a29217a3522851598fd677b4e024268f97d98d5767ba5a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30d8cbbdcd60d2c9cfce9e1ef4919c6bb7acaabd43cb1e156082ba239501fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3b2d483487c6b75a3e5679c7b3f613f0d0191d6bd87f1e83415e240b62bdaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693d174113597bd4dba55dc52335f33ed3a428fc1b4805424d48a8f79e75e48b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76871c98c2a43a8aec0e1a263716fd31311549b928a46150b9edf46d71f06f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f96a788b4aa18ac61fc9b8c1f3b901d12396999afe749d24b8a1503f8c51fb(
    *,
    disable_automatic_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_initial_index: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75910f8ace077e3791c4063ef025f4fe82e8d1f6646a14a4ce49d60fb687e27e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4f0f8a9ddadf231246da33c121d291b7619a8ec3771393ea87bf95f09b9bfd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bec098ba6680e29ac80e5d340f686040ef0504b14a847dc9f6e70aeb17e22b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f19e329d05e8a27ff196e7545a07204edf4ea4fa72daf1b0395c1d23957d97f(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f135a0683947028653da4263012223560cf02002a6aa054e06cc6f4cc6f6cf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_config: builtins.str,
    data_store_id: builtins.str,
    display_name: builtins.str,
    industry_vertical: builtins.str,
    location: builtins.str,
    advanced_site_search_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreAdvancedSiteSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    document_processing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f06b8ba8abb8efe45bf0bd11dc023df7ffee6920e636488f4b7fdc783c2378(
    *,
    chunking_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parsing_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbb5759a3897b0df6a402feba90babcaf37887e53f91de7230a4bebdb6c5716(
    *,
    layout_based_chunking_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a92895b5f6951bf431a4246677bd6733a2458982a4c7e32d5677cc21a4e670(
    *,
    chunk_size: typing.Optional[jsii.Number] = None,
    include_ancestor_headings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dc4cd6ebabaf8ecdff2f3dc4146f2a433e5792aeda6ffcbeedfd76ce793fa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1737ec9ef4a52b8cf62f73bd91c2e36063b939cf41e2be3c796bea3e666fa6c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7a8e85ae8b6919dd5198b30065bb45a2ce942004e62a21dcc52042d6de711d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727878963f11c66544b2eb7a49e54e421624810a92f078078fa1be42f91a153e(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eae2948b1f9183c57c3e4c46419ac166d96c4641f23139a12521771c670b7b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89326247f63688536641306b26d0ec9bd92e5264438e2d25b850e4f2699904a8(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097ffe5dbc60b6047fa1ad4f4955b1851577954304bf9be15d46ab1643680bab(
    *,
    digital_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    layout_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ocr_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04edfd19d63d13670e6482c40bb1fa55cdadbe03ffa4888543024f87c6f2e74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27de7be61e0c789569bdd043c685321acc758066d17cda85d4412de444fa7bc(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788f1610f02a969bbd8424e807f76c70fbcdfb82103b61d601063f7e65fbce5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bef8d54e367744bcd67a99edfae319573d184fb73f6525d0b99a8001adde98(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c8ceb3574459b34098839e0f777176405c3e69c7cf4326f29bcc59876549fe(
    *,
    use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b5d75f9b10277a8858d86feac8f4e250c7f2f1e2bcd842d74a8140df9547d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d7ac7a20b9efc5389e0eee6812fe8aace74450df9115645d4b7d03265dda97(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e0940137878a5986e1a68553c9d7f7d7a3b5ac506a52e40f9380808d733304(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a189beecf952cedf30b140ce6d6c6557564804af40af42e35ed642829224e0cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588950a89dd28bceec43e3e90103a571d4236de9ebf9944e9aab8e315309f61d(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec76dffa92a10fec5f73e0c1199833df1e7e6359aa57805fb6ad11672caba213(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622751bed01a88f268caecbabe4a4fa1b0ee3d7b8d8e497e1dc8db82e6ddeb83(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ff3c65923ac97c47f4fecff726337e24b59d12b603133cbead184a5f1a5a6c(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0dc59ccfba71edc7ab550d7398eb1a7f9c9dcf806d9f91ded049c5a838fcc7(
    *,
    file_type: builtins.str,
    digital_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    layout_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ocr_parsing_config: typing.Optional[typing.Union[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f56122af845ea63d524a098568657580f0aa7be58c44c8aa58693bc3da29775(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca365b6128a8db84cf8cccee271fe3c2f616199e53aaffe8106c89d83259f256(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d069e37732c47db9914bb2fd1df0e5f100a4744d0941d762102d3b92accbdaaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37dbde4a7b2a1ca01f7226eb9d067ea057d2132a7922df4512e1a3d588f5c12(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6770caeea2872967bbf7db490ca8a8e7519c12cedec352f592d8ab1c231a345(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ae32d8f5c58a5716a4c75f5dd2b9993873b4a9741ba6ce3dbba59145cfbb7f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dba7d5bf29d4525c9264ecdc146e413715be2b7566b754247441ed3d76ec0e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc1e972937c95ac69de9eb5954c746bd50b64c47ef4cfbaef36fa0bbc4dbb32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448cf26a01218465cdf77919f531b5e4a6611fbe371776e820e3283870e88217(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc617177c5d8d662e42092a880fb1052d92930515752963f8332a76cec17bfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda7902b09ba1164509528e434c6e7b781a5970e8711e93e445b9fed5db51b99(
    *,
    use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29894ea5c86be9f48319b8c8b1e98c4af812cfd330637230b739bbc4411cc08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a7a6905fac880b3e623ee8c35e614a458b9179786496a002a0798a1f45b930(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48de9026dc5e3c622f0cdcd22b099ccf51199044e70d5c5215b41f1c09ec314(
    value: typing.Optional[GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e839afc8dde94cfdef7d5d9a0ce5d2d0386513a00901e21193fe7027b709a67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911b61c1a6e0aada48795bfdddd17940056b4ac485d3738a9e7513212dc6f16a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc17199f45e96fced078339aa11ca5edfafe0e4d0f73c531b640fc3283eaa43a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ab3c91925604242e961e52a3dbc281acbc0519b6a0814634ca241583e1c42d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b6caf0c6f17ed3864a4bf1b19ff2ce01462409958b93b028c0f41438e6cbca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1f97209e025520796d6fa30ad99aec05bd33c2be2e75d538051ef23a075547(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e69d7bb8531b43530f3657344dd4e33a5ed5cdf8abcd17a3297e9ab8830115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429f720e6c63e3d065f0dce1bedb47f72ee422467a8604b9b698123c356374c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fe6fd3f61a65145b0224c33b1df16c74fc88537448b4a198297b92b5df9d42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDiscoveryEngineDataStoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
