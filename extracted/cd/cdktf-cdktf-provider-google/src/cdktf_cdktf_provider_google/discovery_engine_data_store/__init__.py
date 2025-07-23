r'''
# `google_discovery_engine_data_store`

Refer to the Terraform Registry for docs: [`google_discovery_engine_data_store`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store).
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


class DiscoveryEngineDataStore(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStore",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store google_discovery_engine_data_store}.'''

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
        advanced_site_search_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreAdvancedSiteSearchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        document_processing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineDataStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store google_discovery_engine_data_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param content_config: The content config of the data store. Possible values: ["NO_CONTENT", "CONTENT_REQUIRED", "PUBLIC_WEBSITE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#content_config DiscoveryEngineDataStore#content_config}
        :param data_store_id: The unique id of the data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#data_store_id DiscoveryEngineDataStore#data_store_id}
        :param display_name: The display name of the data store. This field must be a UTF-8 encoded string with a length limit of 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#display_name DiscoveryEngineDataStore#display_name}
        :param industry_vertical: The industry vertical that the data store registers. Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#industry_vertical DiscoveryEngineDataStore#industry_vertical}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#location DiscoveryEngineDataStore#location}
        :param advanced_site_search_config: advanced_site_search_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#advanced_site_search_config DiscoveryEngineDataStore#advanced_site_search_config}
        :param create_advanced_site_search: If true, an advanced data store for site search will be created. If the data store is not configured as site search (GENERIC vertical and PUBLIC_WEBSITE contentConfig), this flag will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#create_advanced_site_search DiscoveryEngineDataStore#create_advanced_site_search}
        :param document_processing_config: document_processing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#document_processing_config DiscoveryEngineDataStore#document_processing_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#id DiscoveryEngineDataStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: KMS key resource name which will be used to encrypt resources: '/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{keyId}' The KMS key to be used to protect this DataStore at creation time. Must be set for requests that need to comply with CMEK Org Policy protections. If this field is set and processed successfully, the DataStore will be protected by the KMS key, as indicated in the cmek_config field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#kms_key_name DiscoveryEngineDataStore#kms_key_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#project DiscoveryEngineDataStore#project}.
        :param skip_default_schema_creation: A boolean flag indicating whether to skip the default schema creation for the data store. Only enable this flag if you are certain that the default schema is incompatible with your use case. If set to true, you must manually create a schema for the data store before any documents can be ingested. This flag cannot be specified if 'data_store.starting_schema' is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#skip_default_schema_creation DiscoveryEngineDataStore#skip_default_schema_creation}
        :param solution_types: The solutions that the data store enrolls. Possible values: ["SOLUTION_TYPE_RECOMMENDATION", "SOLUTION_TYPE_SEARCH", "SOLUTION_TYPE_CHAT", "SOLUTION_TYPE_GENERATIVE_CHAT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#solution_types DiscoveryEngineDataStore#solution_types}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#timeouts DiscoveryEngineDataStore#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13421286928bae1c35a2a721a1d1a6773a90c0f27f27d3891f23e0fd335ffe3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DiscoveryEngineDataStoreConfig(
            content_config=content_config,
            data_store_id=data_store_id,
            display_name=display_name,
            industry_vertical=industry_vertical,
            location=location,
            advanced_site_search_config=advanced_site_search_config,
            create_advanced_site_search=create_advanced_site_search,
            document_processing_config=document_processing_config,
            id=id,
            kms_key_name=kms_key_name,
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
        '''Generates CDKTF code for importing a DiscoveryEngineDataStore resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DiscoveryEngineDataStore to import.
        :param import_from_id: The id of the existing DiscoveryEngineDataStore that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DiscoveryEngineDataStore to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b855c3204654a00e59346c4938d126260a2409e261ede110809498b9c5e6e6fd)
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
        :param disable_automatic_refresh: If set true, automatic refresh is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#disable_automatic_refresh DiscoveryEngineDataStore#disable_automatic_refresh}
        :param disable_initial_index: If set true, initial indexing is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#disable_initial_index DiscoveryEngineDataStore#disable_initial_index}
        '''
        value = DiscoveryEngineDataStoreAdvancedSiteSearchConfig(
            disable_automatic_refresh=disable_automatic_refresh,
            disable_initial_index=disable_initial_index,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSiteSearchConfig", [value]))

    @jsii.member(jsii_name="putDocumentProcessingConfig")
    def put_document_processing_config(
        self,
        *,
        chunking_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parsing_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chunking_config: chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#chunking_config DiscoveryEngineDataStore#chunking_config}
        :param default_parsing_config: default_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#default_parsing_config DiscoveryEngineDataStore#default_parsing_config}
        :param parsing_config_overrides: parsing_config_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#parsing_config_overrides DiscoveryEngineDataStore#parsing_config_overrides}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#create DiscoveryEngineDataStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#delete DiscoveryEngineDataStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#update DiscoveryEngineDataStore#update}.
        '''
        value = DiscoveryEngineDataStoreTimeouts(
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

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

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
    ) -> "DiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference":
        return typing.cast("DiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference", jsii.get(self, "advancedSiteSearchConfig"))

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
    ) -> "DiscoveryEngineDataStoreDocumentProcessingConfigOutputReference":
        return typing.cast("DiscoveryEngineDataStoreDocumentProcessingConfigOutputReference", jsii.get(self, "documentProcessingConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DiscoveryEngineDataStoreTimeoutsOutputReference":
        return typing.cast("DiscoveryEngineDataStoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedSiteSearchConfigInput")
    def advanced_site_search_config_input(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreAdvancedSiteSearchConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreAdvancedSiteSearchConfig"], jsii.get(self, "advancedSiteSearchConfigInput"))

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
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfig"]:
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfig"], jsii.get(self, "documentProcessingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="industryVerticalInput")
    def industry_vertical_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "industryVerticalInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineDataStoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DiscoveryEngineDataStoreTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="contentConfig")
    def content_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentConfig"))

    @content_config.setter
    def content_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbcbddffdf24ed2e552ed09ccfc343f7624da9d509d8a4c0c038efad928de4e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__247c8bd8aaa616e9d6e79357654d76e2b71a02416a3cca3701f6653d5e33357d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createAdvancedSiteSearch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreId")
    def data_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreId"))

    @data_store_id.setter
    def data_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cb1b9e81b1ffe3ef9ffb278e34977e8e7abfd3573334459e2e1d8cdef53e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b7063accea4d22f1c8eb8dd9219175387f0d6665e58ce423f32312dc04f4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b48eb89699bdd1619e5a55a5932d8fe78a6d8be56319da4944b1993e2acaae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="industryVertical")
    def industry_vertical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "industryVertical"))

    @industry_vertical.setter
    def industry_vertical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f913e84edfcb0ba8d97c2f81a112dcd79a02575c6866f1a71ee07f8d9541bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "industryVertical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7381adfb2b5a873f029acac0a3be1b8c1131da8dca9f64e280ada9e2f1bee719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4c471798a99f0e8a7cccb7c595bd1864ab6e3f840608f537b23a8b21860800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fb37d8f632f4acb3921215ff03f00fd9c3665c7524f61313762148d52dc604)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00243890fe84e7dc86cc197f029c840cf54f6c317f1a609adaa4f514c1bcbbfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipDefaultSchemaCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="solutionTypes")
    def solution_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "solutionTypes"))

    @solution_types.setter
    def solution_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff12e82f0818f9eb7cb7ce8ce4618824cfdf5abe0b10bf7cafa8100705f967f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "solutionTypes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreAdvancedSiteSearchConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disable_automatic_refresh": "disableAutomaticRefresh",
        "disable_initial_index": "disableInitialIndex",
    },
)
class DiscoveryEngineDataStoreAdvancedSiteSearchConfig:
    def __init__(
        self,
        *,
        disable_automatic_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_initial_index: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_automatic_refresh: If set true, automatic refresh is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#disable_automatic_refresh DiscoveryEngineDataStore#disable_automatic_refresh}
        :param disable_initial_index: If set true, initial indexing is disabled for the DataStore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#disable_initial_index DiscoveryEngineDataStore#disable_initial_index}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efcf86c881aea6944abb7e0253e3d2238a14594bdce624afc9fe192e4013636)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#disable_automatic_refresh DiscoveryEngineDataStore#disable_automatic_refresh}
        '''
        result = self._values.get("disable_automatic_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_initial_index(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set true, initial indexing is disabled for the DataStore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#disable_initial_index DiscoveryEngineDataStore#disable_initial_index}
        '''
        result = self._values.get("disable_initial_index")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreAdvancedSiteSearchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7d0c1f8c3441e52455877cae6c2ba089dcf963bc6de6eb027cb1dff24961b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__192174437606603b43c30632dcae4ec957059b112c346e962f777a9ffef8a212)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40918ff8da3d8c885de4cd82b430c9a40354ff0f17b32aa882e6b0a39c76337c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableInitialIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreAdvancedSiteSearchConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreAdvancedSiteSearchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreAdvancedSiteSearchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7149c0de83eef7c41af8e2ef707acbc208b09d687e1de75c5ddd86c7761779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreConfig",
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
        "kms_key_name": "kmsKeyName",
        "project": "project",
        "skip_default_schema_creation": "skipDefaultSchemaCreation",
        "solution_types": "solutionTypes",
        "timeouts": "timeouts",
    },
)
class DiscoveryEngineDataStoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        advanced_site_search_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreAdvancedSiteSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        document_processing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DiscoveryEngineDataStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param content_config: The content config of the data store. Possible values: ["NO_CONTENT", "CONTENT_REQUIRED", "PUBLIC_WEBSITE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#content_config DiscoveryEngineDataStore#content_config}
        :param data_store_id: The unique id of the data store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#data_store_id DiscoveryEngineDataStore#data_store_id}
        :param display_name: The display name of the data store. This field must be a UTF-8 encoded string with a length limit of 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#display_name DiscoveryEngineDataStore#display_name}
        :param industry_vertical: The industry vertical that the data store registers. Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#industry_vertical DiscoveryEngineDataStore#industry_vertical}
        :param location: The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#location DiscoveryEngineDataStore#location}
        :param advanced_site_search_config: advanced_site_search_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#advanced_site_search_config DiscoveryEngineDataStore#advanced_site_search_config}
        :param create_advanced_site_search: If true, an advanced data store for site search will be created. If the data store is not configured as site search (GENERIC vertical and PUBLIC_WEBSITE contentConfig), this flag will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#create_advanced_site_search DiscoveryEngineDataStore#create_advanced_site_search}
        :param document_processing_config: document_processing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#document_processing_config DiscoveryEngineDataStore#document_processing_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#id DiscoveryEngineDataStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: KMS key resource name which will be used to encrypt resources: '/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{keyId}' The KMS key to be used to protect this DataStore at creation time. Must be set for requests that need to comply with CMEK Org Policy protections. If this field is set and processed successfully, the DataStore will be protected by the KMS key, as indicated in the cmek_config field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#kms_key_name DiscoveryEngineDataStore#kms_key_name}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#project DiscoveryEngineDataStore#project}.
        :param skip_default_schema_creation: A boolean flag indicating whether to skip the default schema creation for the data store. Only enable this flag if you are certain that the default schema is incompatible with your use case. If set to true, you must manually create a schema for the data store before any documents can be ingested. This flag cannot be specified if 'data_store.starting_schema' is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#skip_default_schema_creation DiscoveryEngineDataStore#skip_default_schema_creation}
        :param solution_types: The solutions that the data store enrolls. Possible values: ["SOLUTION_TYPE_RECOMMENDATION", "SOLUTION_TYPE_SEARCH", "SOLUTION_TYPE_CHAT", "SOLUTION_TYPE_GENERATIVE_CHAT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#solution_types DiscoveryEngineDataStore#solution_types}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#timeouts DiscoveryEngineDataStore#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_site_search_config, dict):
            advanced_site_search_config = DiscoveryEngineDataStoreAdvancedSiteSearchConfig(**advanced_site_search_config)
        if isinstance(document_processing_config, dict):
            document_processing_config = DiscoveryEngineDataStoreDocumentProcessingConfig(**document_processing_config)
        if isinstance(timeouts, dict):
            timeouts = DiscoveryEngineDataStoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a651110d418daa26708a494797d010a16a6de1d3034a6b9850935d33026811)
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
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
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
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#content_config DiscoveryEngineDataStore#content_config}
        '''
        result = self._values.get("content_config")
        assert result is not None, "Required property 'content_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_id(self) -> builtins.str:
        '''The unique id of the data store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#data_store_id DiscoveryEngineDataStore#data_store_id}
        '''
        result = self._values.get("data_store_id")
        assert result is not None, "Required property 'data_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the data store.

        This field must be a UTF-8 encoded
        string with a length limit of 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#display_name DiscoveryEngineDataStore#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def industry_vertical(self) -> builtins.str:
        '''The industry vertical that the data store registers. Possible values: ["GENERIC", "MEDIA", "HEALTHCARE_FHIR"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#industry_vertical DiscoveryEngineDataStore#industry_vertical}
        '''
        result = self._values.get("industry_vertical")
        assert result is not None, "Required property 'industry_vertical' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The geographic location where the data store should reside. The value can only be one of "global", "us" and "eu".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#location DiscoveryEngineDataStore#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_site_search_config(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreAdvancedSiteSearchConfig]:
        '''advanced_site_search_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#advanced_site_search_config DiscoveryEngineDataStore#advanced_site_search_config}
        '''
        result = self._values.get("advanced_site_search_config")
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreAdvancedSiteSearchConfig], result)

    @builtins.property
    def create_advanced_site_search(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, an advanced data store for site search will be created.

        If the
        data store is not configured as site search (GENERIC vertical and
        PUBLIC_WEBSITE contentConfig), this flag will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#create_advanced_site_search DiscoveryEngineDataStore#create_advanced_site_search}
        '''
        result = self._values.get("create_advanced_site_search")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def document_processing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfig"]:
        '''document_processing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#document_processing_config DiscoveryEngineDataStore#document_processing_config}
        '''
        result = self._values.get("document_processing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#id DiscoveryEngineDataStore#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''KMS key resource name which will be used to encrypt resources: '/{project}/locations/{location}/keyRings/{keyRing}/cryptoKeys/{keyId}' The KMS key to be used to protect this DataStore at creation time.

        Must be
        set for requests that need to comply with CMEK Org Policy protections.
        If this field is set and processed successfully, the DataStore will be
        protected by the KMS key, as indicated in the cmek_config field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#kms_key_name DiscoveryEngineDataStore#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#project DiscoveryEngineDataStore#project}.'''
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#skip_default_schema_creation DiscoveryEngineDataStore#skip_default_schema_creation}
        '''
        result = self._values.get("skip_default_schema_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def solution_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The solutions that the data store enrolls. Possible values: ["SOLUTION_TYPE_RECOMMENDATION", "SOLUTION_TYPE_SEARCH", "SOLUTION_TYPE_CHAT", "SOLUTION_TYPE_GENERATIVE_CHAT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#solution_types DiscoveryEngineDataStore#solution_types}
        '''
        result = self._values.get("solution_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DiscoveryEngineDataStoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#timeouts DiscoveryEngineDataStore#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "chunking_config": "chunkingConfig",
        "default_parsing_config": "defaultParsingConfig",
        "parsing_config_overrides": "parsingConfigOverrides",
    },
)
class DiscoveryEngineDataStoreDocumentProcessingConfig:
    def __init__(
        self,
        *,
        chunking_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parsing_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chunking_config: chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#chunking_config DiscoveryEngineDataStore#chunking_config}
        :param default_parsing_config: default_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#default_parsing_config DiscoveryEngineDataStore#default_parsing_config}
        :param parsing_config_overrides: parsing_config_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#parsing_config_overrides DiscoveryEngineDataStore#parsing_config_overrides}
        '''
        if isinstance(chunking_config, dict):
            chunking_config = DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig(**chunking_config)
        if isinstance(default_parsing_config, dict):
            default_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig(**default_parsing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f277a0214b43425ae373beedcb60f4453aabbacd8480e839badcb9a330263be)
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
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig"]:
        '''chunking_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#chunking_config DiscoveryEngineDataStore#chunking_config}
        '''
        result = self._values.get("chunking_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig"], result)

    @builtins.property
    def default_parsing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig"]:
        '''default_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#default_parsing_config DiscoveryEngineDataStore#default_parsing_config}
        '''
        result = self._values.get("default_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig"], result)

    @builtins.property
    def parsing_config_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]]:
        '''parsing_config_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#parsing_config_overrides DiscoveryEngineDataStore#parsing_config_overrides}
        '''
        result = self._values.get("parsing_config_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig",
    jsii_struct_bases=[],
    name_mapping={"layout_based_chunking_config": "layoutBasedChunkingConfig"},
)
class DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig:
    def __init__(
        self,
        *,
        layout_based_chunking_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param layout_based_chunking_config: layout_based_chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_based_chunking_config DiscoveryEngineDataStore#layout_based_chunking_config}
        '''
        if isinstance(layout_based_chunking_config, dict):
            layout_based_chunking_config = DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig(**layout_based_chunking_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5db726e607cdb52d0e67e6c6c4a07817f642363e5bb053f36174c3a8d44d356)
            check_type(argname="argument layout_based_chunking_config", value=layout_based_chunking_config, expected_type=type_hints["layout_based_chunking_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if layout_based_chunking_config is not None:
            self._values["layout_based_chunking_config"] = layout_based_chunking_config

    @builtins.property
    def layout_based_chunking_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig"]:
        '''layout_based_chunking_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_based_chunking_config DiscoveryEngineDataStore#layout_based_chunking_config}
        '''
        result = self._values.get("layout_based_chunking_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "chunk_size": "chunkSize",
        "include_ancestor_headings": "includeAncestorHeadings",
    },
)
class DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig:
    def __init__(
        self,
        *,
        chunk_size: typing.Optional[jsii.Number] = None,
        include_ancestor_headings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param chunk_size: The token size limit for each chunk. Supported values: 100-500 (inclusive). Default value: 500. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#chunk_size DiscoveryEngineDataStore#chunk_size}
        :param include_ancestor_headings: Whether to include appending different levels of headings to chunks from the middle of the document to prevent context loss. Default value: False. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#include_ancestor_headings DiscoveryEngineDataStore#include_ancestor_headings}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63da38a71ec3d4a4ac1cc05d2f9c95974dad5edd5a81993716e045f1ac5415f3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#chunk_size DiscoveryEngineDataStore#chunk_size}
        '''
        result = self._values.get("chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def include_ancestor_headings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to include appending different levels of headings to chunks from the middle of the document to prevent context loss.

        Default value: False.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#include_ancestor_headings DiscoveryEngineDataStore#include_ancestor_headings}
        '''
        result = self._values.get("include_ancestor_headings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b0ccc3d2b6e082e13d2a52ad793dca7daf93c71c9e9a02300c4118055619bf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0e10fb10e8950cf6042f4983aff3bcc5278c79b5b429c274b388a38ad141ae1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f4a4f07e01bd3d21eb7bdb2a4418d88ebee779cd0ed515d95dae15d33e96f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAncestorHeadings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea3fe9180913e8ebc59a10be45f95992cf2fa435796285506f3a2178389930f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae28bd2b218466fcfdc663162c11723d7d946699da73e7ce19d64e3820054ddc)
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
        :param chunk_size: The token size limit for each chunk. Supported values: 100-500 (inclusive). Default value: 500. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#chunk_size DiscoveryEngineDataStore#chunk_size}
        :param include_ancestor_headings: Whether to include appending different levels of headings to chunks from the middle of the document to prevent context loss. Default value: False. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#include_ancestor_headings DiscoveryEngineDataStore#include_ancestor_headings}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig(
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
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference, jsii.get(self, "layoutBasedChunkingConfig"))

    @builtins.property
    @jsii.member(jsii_name="layoutBasedChunkingConfigInput")
    def layout_based_chunking_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig], jsii.get(self, "layoutBasedChunkingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5501d4e9dcdac68a6c0f13577ccfbb53feda7807ca22aa95f2840f22090b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "digital_parsing_config": "digitalParsingConfig",
        "layout_parsing_config": "layoutParsingConfig",
        "ocr_parsing_config": "ocrParsingConfig",
    },
)
class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig:
    def __init__(
        self,
        *,
        digital_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        layout_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ocr_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param digital_parsing_config: digital_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#digital_parsing_config DiscoveryEngineDataStore#digital_parsing_config}
        :param layout_parsing_config: layout_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_parsing_config DiscoveryEngineDataStore#layout_parsing_config}
        :param ocr_parsing_config: ocr_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#ocr_parsing_config DiscoveryEngineDataStore#ocr_parsing_config}
        '''
        if isinstance(digital_parsing_config, dict):
            digital_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig(**digital_parsing_config)
        if isinstance(layout_parsing_config, dict):
            layout_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig(**layout_parsing_config)
        if isinstance(ocr_parsing_config, dict):
            ocr_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig(**ocr_parsing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fcf53cec42f0ee32c649bb56fd34fe04d99ebe91e98179a2a6e9f94c8f2f2d)
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
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig"]:
        '''digital_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#digital_parsing_config DiscoveryEngineDataStore#digital_parsing_config}
        '''
        result = self._values.get("digital_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig"], result)

    @builtins.property
    def layout_parsing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig"]:
        '''layout_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_parsing_config DiscoveryEngineDataStore#layout_parsing_config}
        '''
        result = self._values.get("layout_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig"], result)

    @builtins.property
    def ocr_parsing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig"]:
        '''ocr_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#ocr_parsing_config DiscoveryEngineDataStore#ocr_parsing_config}
        '''
        result = self._values.get("ocr_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e487f476b6efd504e66ef8a9a7c85d9edd682ca2b83d2f5a0e3b14aaeb3fd51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5141b3e3a17cadde1562f5e291cf65101825bc6fb5dda57732899b2e3b714c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_image_annotation": "enableImageAnnotation",
        "enable_table_annotation": "enableTableAnnotation",
        "exclude_html_classes": "excludeHtmlClasses",
        "exclude_html_elements": "excludeHtmlElements",
        "exclude_html_ids": "excludeHtmlIds",
        "structured_content_types": "structuredContentTypes",
    },
)
class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig:
    def __init__(
        self,
        *,
        enable_image_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_table_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_html_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        structured_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_image_annotation: If true, the LLM based annotation is added to the image during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_image_annotation DiscoveryEngineDataStore#enable_image_annotation}
        :param enable_table_annotation: If true, the LLM based annotation is added to the table during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_table_annotation DiscoveryEngineDataStore#enable_table_annotation}
        :param exclude_html_classes: List of HTML classes to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_classes DiscoveryEngineDataStore#exclude_html_classes}
        :param exclude_html_elements: List of HTML elements to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_elements DiscoveryEngineDataStore#exclude_html_elements}
        :param exclude_html_ids: List of HTML ids to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_ids DiscoveryEngineDataStore#exclude_html_ids}
        :param structured_content_types: Contains the required structure types to extract from the document. Supported values: 'shareholder-structure'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#structured_content_types DiscoveryEngineDataStore#structured_content_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b691b7f188852c9bfb2768b1d92c29788148688031ec87b0cb72063deadd0d0)
            check_type(argname="argument enable_image_annotation", value=enable_image_annotation, expected_type=type_hints["enable_image_annotation"])
            check_type(argname="argument enable_table_annotation", value=enable_table_annotation, expected_type=type_hints["enable_table_annotation"])
            check_type(argname="argument exclude_html_classes", value=exclude_html_classes, expected_type=type_hints["exclude_html_classes"])
            check_type(argname="argument exclude_html_elements", value=exclude_html_elements, expected_type=type_hints["exclude_html_elements"])
            check_type(argname="argument exclude_html_ids", value=exclude_html_ids, expected_type=type_hints["exclude_html_ids"])
            check_type(argname="argument structured_content_types", value=structured_content_types, expected_type=type_hints["structured_content_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_image_annotation is not None:
            self._values["enable_image_annotation"] = enable_image_annotation
        if enable_table_annotation is not None:
            self._values["enable_table_annotation"] = enable_table_annotation
        if exclude_html_classes is not None:
            self._values["exclude_html_classes"] = exclude_html_classes
        if exclude_html_elements is not None:
            self._values["exclude_html_elements"] = exclude_html_elements
        if exclude_html_ids is not None:
            self._values["exclude_html_ids"] = exclude_html_ids
        if structured_content_types is not None:
            self._values["structured_content_types"] = structured_content_types

    @builtins.property
    def enable_image_annotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the LLM based annotation is added to the image during parsing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_image_annotation DiscoveryEngineDataStore#enable_image_annotation}
        '''
        result = self._values.get("enable_image_annotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_table_annotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the LLM based annotation is added to the table during parsing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_table_annotation DiscoveryEngineDataStore#enable_table_annotation}
        '''
        result = self._values.get("enable_table_annotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_html_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTML classes to exclude from the parsed content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_classes DiscoveryEngineDataStore#exclude_html_classes}
        '''
        result = self._values.get("exclude_html_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_html_elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTML elements to exclude from the parsed content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_elements DiscoveryEngineDataStore#exclude_html_elements}
        '''
        result = self._values.get("exclude_html_elements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_html_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTML ids to exclude from the parsed content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_ids DiscoveryEngineDataStore#exclude_html_ids}
        '''
        result = self._values.get("exclude_html_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def structured_content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the required structure types to extract from the document. Supported values: 'shareholder-structure'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#structured_content_types DiscoveryEngineDataStore#structured_content_types}
        '''
        result = self._values.get("structured_content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce59267cb4e82b3ca9c2eed9d92dc5ee205058ddbfd91c2446e0bff4678acf6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableImageAnnotation")
    def reset_enable_image_annotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableImageAnnotation", []))

    @jsii.member(jsii_name="resetEnableTableAnnotation")
    def reset_enable_table_annotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableTableAnnotation", []))

    @jsii.member(jsii_name="resetExcludeHtmlClasses")
    def reset_exclude_html_classes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHtmlClasses", []))

    @jsii.member(jsii_name="resetExcludeHtmlElements")
    def reset_exclude_html_elements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHtmlElements", []))

    @jsii.member(jsii_name="resetExcludeHtmlIds")
    def reset_exclude_html_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHtmlIds", []))

    @jsii.member(jsii_name="resetStructuredContentTypes")
    def reset_structured_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStructuredContentTypes", []))

    @builtins.property
    @jsii.member(jsii_name="enableImageAnnotationInput")
    def enable_image_annotation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableImageAnnotationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableTableAnnotationInput")
    def enable_table_annotation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableTableAnnotationInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlClassesInput")
    def exclude_html_classes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeHtmlClassesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlElementsInput")
    def exclude_html_elements_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeHtmlElementsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlIdsInput")
    def exclude_html_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeHtmlIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="structuredContentTypesInput")
    def structured_content_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "structuredContentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableImageAnnotation")
    def enable_image_annotation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableImageAnnotation"))

    @enable_image_annotation.setter
    def enable_image_annotation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130e88f6a5044c84c032842eabc01ae47c95b2d2d0b23208f4b9a35d9af37427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableImageAnnotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableTableAnnotation")
    def enable_table_annotation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableTableAnnotation"))

    @enable_table_annotation.setter
    def enable_table_annotation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0c9dc0cbaebec892f44605a8ae50fb5c2700d32d29ec0f9f17ef0f01e1a6d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableTableAnnotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlClasses")
    def exclude_html_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeHtmlClasses"))

    @exclude_html_classes.setter
    def exclude_html_classes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280efb07f1798a2dacb0c2d823652fd7f67a09bbc7eb7a9b8d2e5e7f637b65e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHtmlClasses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlElements")
    def exclude_html_elements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeHtmlElements"))

    @exclude_html_elements.setter
    def exclude_html_elements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0e200ec5d4ed055321500bf543d6221279b17cf597e2c1327ef5e581e00451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHtmlElements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlIds")
    def exclude_html_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeHtmlIds"))

    @exclude_html_ids.setter
    def exclude_html_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4d34c22782060509128f113039b396d3e4f2645e5008704a8740b6e17ffc6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHtmlIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="structuredContentTypes")
    def structured_content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "structuredContentTypes"))

    @structured_content_types.setter
    def structured_content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cf4b94ecc03c0a9b06319c2e0ccb053901bacce410084e7684646e998a7e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "structuredContentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39be4c8a0f0a22986e745c0ba4767bf4d8cfcc5675fe5d33cb44ce860e25058a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig",
    jsii_struct_bases=[],
    name_mapping={"use_native_text": "useNativeText"},
)
class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig:
    def __init__(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#use_native_text DiscoveryEngineDataStore#use_native_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a367527f7529392bc2cb52691e206500ffe650cca3db5c95b8a1b7d261b02e)
            check_type(argname="argument use_native_text", value=use_native_text, expected_type=type_hints["use_native_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if use_native_text is not None:
            self._values["use_native_text"] = use_native_text

    @builtins.property
    def use_native_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, will use native text instead of OCR text on pages containing native text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#use_native_text DiscoveryEngineDataStore#use_native_text}
        '''
        result = self._values.get("use_native_text")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__035153900d8c238ffe7f0949107dfd4cc3f5a8ff3d3c0672d31ea6bac4c69e2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dab4f5c5197a2d22aa917bba7303d53c4416f698af1f32707a45f94ba09879d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNativeText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a7d8fcf4fc1524c7684c28f8d94ff6e38d33a8280dbe16e7185fa014bd1f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e5510b5a432d9a24c0be426802557aed4e1440f098d8135fbc1a3c72a80ada6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDigitalParsingConfig")
    def put_digital_parsing_config(self) -> None:
        value = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig()

        return typing.cast(None, jsii.invoke(self, "putDigitalParsingConfig", [value]))

    @jsii.member(jsii_name="putLayoutParsingConfig")
    def put_layout_parsing_config(
        self,
        *,
        enable_image_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_table_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_html_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        structured_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_image_annotation: If true, the LLM based annotation is added to the image during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_image_annotation DiscoveryEngineDataStore#enable_image_annotation}
        :param enable_table_annotation: If true, the LLM based annotation is added to the table during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_table_annotation DiscoveryEngineDataStore#enable_table_annotation}
        :param exclude_html_classes: List of HTML classes to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_classes DiscoveryEngineDataStore#exclude_html_classes}
        :param exclude_html_elements: List of HTML elements to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_elements DiscoveryEngineDataStore#exclude_html_elements}
        :param exclude_html_ids: List of HTML ids to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_ids DiscoveryEngineDataStore#exclude_html_ids}
        :param structured_content_types: Contains the required structure types to extract from the document. Supported values: 'shareholder-structure'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#structured_content_types DiscoveryEngineDataStore#structured_content_types}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig(
            enable_image_annotation=enable_image_annotation,
            enable_table_annotation=enable_table_annotation,
            exclude_html_classes=exclude_html_classes,
            exclude_html_elements=exclude_html_elements,
            exclude_html_ids=exclude_html_ids,
            structured_content_types=structured_content_types,
        )

        return typing.cast(None, jsii.invoke(self, "putLayoutParsingConfig", [value]))

    @jsii.member(jsii_name="putOcrParsingConfig")
    def put_ocr_parsing_config(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#use_native_text DiscoveryEngineDataStore#use_native_text}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig(
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
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference, jsii.get(self, "digitalParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfig")
    def layout_parsing_config(
        self,
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference, jsii.get(self, "layoutParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfig")
    def ocr_parsing_config(
        self,
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference, jsii.get(self, "ocrParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="digitalParsingConfigInput")
    def digital_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig], jsii.get(self, "digitalParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfigInput")
    def layout_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig], jsii.get(self, "layoutParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfigInput")
    def ocr_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig], jsii.get(self, "ocrParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1147e8a3d4ad0be56a36e54dd3782494afbca85cf1262bce6598921d1ec377fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineDataStoreDocumentProcessingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dabef1cf820be49269aa53a072350c82e52b22a33cf84906403877d753af15b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putChunkingConfig")
    def put_chunking_config(
        self,
        *,
        layout_based_chunking_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param layout_based_chunking_config: layout_based_chunking_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_based_chunking_config DiscoveryEngineDataStore#layout_based_chunking_config}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig(
            layout_based_chunking_config=layout_based_chunking_config
        )

        return typing.cast(None, jsii.invoke(self, "putChunkingConfig", [value]))

    @jsii.member(jsii_name="putDefaultParsingConfig")
    def put_default_parsing_config(
        self,
        *,
        digital_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        layout_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        ocr_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param digital_parsing_config: digital_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#digital_parsing_config DiscoveryEngineDataStore#digital_parsing_config}
        :param layout_parsing_config: layout_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_parsing_config DiscoveryEngineDataStore#layout_parsing_config}
        :param ocr_parsing_config: ocr_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#ocr_parsing_config DiscoveryEngineDataStore#ocr_parsing_config}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig(
            digital_parsing_config=digital_parsing_config,
            layout_parsing_config=layout_parsing_config,
            ocr_parsing_config=ocr_parsing_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultParsingConfig", [value]))

    @jsii.member(jsii_name="putParsingConfigOverrides")
    def put_parsing_config_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e952fff3c6ddaf1a60c9b7d1b4b69060fd6825c95c37d9064d8086c46b6ecb56)
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
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference, jsii.get(self, "chunkingConfig"))

    @builtins.property
    @jsii.member(jsii_name="defaultParsingConfig")
    def default_parsing_config(
        self,
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference, jsii.get(self, "defaultParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="parsingConfigOverrides")
    def parsing_config_overrides(
        self,
    ) -> "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList":
        return typing.cast("DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList", jsii.get(self, "parsingConfigOverrides"))

    @builtins.property
    @jsii.member(jsii_name="chunkingConfigInput")
    def chunking_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig], jsii.get(self, "chunkingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultParsingConfigInput")
    def default_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig], jsii.get(self, "defaultParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingConfigOverridesInput")
    def parsing_config_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides"]]], jsii.get(self, "parsingConfigOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc31c5c1d00e04107daac13310616fd3aeab23046c125e3ab85fb51807cb3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "file_type": "fileType",
        "digital_parsing_config": "digitalParsingConfig",
        "layout_parsing_config": "layoutParsingConfig",
        "ocr_parsing_config": "ocrParsingConfig",
    },
)
class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides:
    def __init__(
        self,
        *,
        file_type: builtins.str,
        digital_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        layout_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ocr_parsing_config: typing.Optional[typing.Union["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#file_type DiscoveryEngineDataStore#file_type}.
        :param digital_parsing_config: digital_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#digital_parsing_config DiscoveryEngineDataStore#digital_parsing_config}
        :param layout_parsing_config: layout_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_parsing_config DiscoveryEngineDataStore#layout_parsing_config}
        :param ocr_parsing_config: ocr_parsing_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#ocr_parsing_config DiscoveryEngineDataStore#ocr_parsing_config}
        '''
        if isinstance(digital_parsing_config, dict):
            digital_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig(**digital_parsing_config)
        if isinstance(layout_parsing_config, dict):
            layout_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig(**layout_parsing_config)
        if isinstance(ocr_parsing_config, dict):
            ocr_parsing_config = DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig(**ocr_parsing_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d59175601863178596cc97885314bb9fbbbcdf95428af79c77bbf1eacd093fc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#file_type DiscoveryEngineDataStore#file_type}.'''
        result = self._values.get("file_type")
        assert result is not None, "Required property 'file_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def digital_parsing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig"]:
        '''digital_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#digital_parsing_config DiscoveryEngineDataStore#digital_parsing_config}
        '''
        result = self._values.get("digital_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig"], result)

    @builtins.property
    def layout_parsing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig"]:
        '''layout_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#layout_parsing_config DiscoveryEngineDataStore#layout_parsing_config}
        '''
        result = self._values.get("layout_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig"], result)

    @builtins.property
    def ocr_parsing_config(
        self,
    ) -> typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig"]:
        '''ocr_parsing_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#ocr_parsing_config DiscoveryEngineDataStore#ocr_parsing_config}
        '''
        result = self._values.get("ocr_parsing_config")
        return typing.cast(typing.Optional["DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b0a27d31f6bf371e819f31619d13cead978bd016fe972895a518d31ca3b60f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5c882f8547862a3cb61194689538e05922246a7f9d27eff18fb226236bf2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_image_annotation": "enableImageAnnotation",
        "enable_table_annotation": "enableTableAnnotation",
        "exclude_html_classes": "excludeHtmlClasses",
        "exclude_html_elements": "excludeHtmlElements",
        "exclude_html_ids": "excludeHtmlIds",
        "structured_content_types": "structuredContentTypes",
    },
)
class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig:
    def __init__(
        self,
        *,
        enable_image_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_table_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_html_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        structured_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_image_annotation: If true, the LLM based annotation is added to the image during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_image_annotation DiscoveryEngineDataStore#enable_image_annotation}
        :param enable_table_annotation: If true, the LLM based annotation is added to the table during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_table_annotation DiscoveryEngineDataStore#enable_table_annotation}
        :param exclude_html_classes: List of HTML classes to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_classes DiscoveryEngineDataStore#exclude_html_classes}
        :param exclude_html_elements: List of HTML elements to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_elements DiscoveryEngineDataStore#exclude_html_elements}
        :param exclude_html_ids: List of HTML ids to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_ids DiscoveryEngineDataStore#exclude_html_ids}
        :param structured_content_types: Contains the required structure types to extract from the document. Supported values: 'shareholder-structure'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#structured_content_types DiscoveryEngineDataStore#structured_content_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03d54e524c96c2839fdd8af2c5b187eff60f6f0ec1bbdddb0268a8124806582)
            check_type(argname="argument enable_image_annotation", value=enable_image_annotation, expected_type=type_hints["enable_image_annotation"])
            check_type(argname="argument enable_table_annotation", value=enable_table_annotation, expected_type=type_hints["enable_table_annotation"])
            check_type(argname="argument exclude_html_classes", value=exclude_html_classes, expected_type=type_hints["exclude_html_classes"])
            check_type(argname="argument exclude_html_elements", value=exclude_html_elements, expected_type=type_hints["exclude_html_elements"])
            check_type(argname="argument exclude_html_ids", value=exclude_html_ids, expected_type=type_hints["exclude_html_ids"])
            check_type(argname="argument structured_content_types", value=structured_content_types, expected_type=type_hints["structured_content_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_image_annotation is not None:
            self._values["enable_image_annotation"] = enable_image_annotation
        if enable_table_annotation is not None:
            self._values["enable_table_annotation"] = enable_table_annotation
        if exclude_html_classes is not None:
            self._values["exclude_html_classes"] = exclude_html_classes
        if exclude_html_elements is not None:
            self._values["exclude_html_elements"] = exclude_html_elements
        if exclude_html_ids is not None:
            self._values["exclude_html_ids"] = exclude_html_ids
        if structured_content_types is not None:
            self._values["structured_content_types"] = structured_content_types

    @builtins.property
    def enable_image_annotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the LLM based annotation is added to the image during parsing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_image_annotation DiscoveryEngineDataStore#enable_image_annotation}
        '''
        result = self._values.get("enable_image_annotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_table_annotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the LLM based annotation is added to the table during parsing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_table_annotation DiscoveryEngineDataStore#enable_table_annotation}
        '''
        result = self._values.get("enable_table_annotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_html_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTML classes to exclude from the parsed content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_classes DiscoveryEngineDataStore#exclude_html_classes}
        '''
        result = self._values.get("exclude_html_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_html_elements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTML elements to exclude from the parsed content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_elements DiscoveryEngineDataStore#exclude_html_elements}
        '''
        result = self._values.get("exclude_html_elements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_html_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTML ids to exclude from the parsed content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_ids DiscoveryEngineDataStore#exclude_html_ids}
        '''
        result = self._values.get("exclude_html_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def structured_content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the required structure types to extract from the document. Supported values: 'shareholder-structure'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#structured_content_types DiscoveryEngineDataStore#structured_content_types}
        '''
        result = self._values.get("structured_content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f082e46f6d3fa3e37934c9f97e57cfd9f75f02f123d474e15660593eeb070dc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableImageAnnotation")
    def reset_enable_image_annotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableImageAnnotation", []))

    @jsii.member(jsii_name="resetEnableTableAnnotation")
    def reset_enable_table_annotation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableTableAnnotation", []))

    @jsii.member(jsii_name="resetExcludeHtmlClasses")
    def reset_exclude_html_classes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHtmlClasses", []))

    @jsii.member(jsii_name="resetExcludeHtmlElements")
    def reset_exclude_html_elements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHtmlElements", []))

    @jsii.member(jsii_name="resetExcludeHtmlIds")
    def reset_exclude_html_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeHtmlIds", []))

    @jsii.member(jsii_name="resetStructuredContentTypes")
    def reset_structured_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStructuredContentTypes", []))

    @builtins.property
    @jsii.member(jsii_name="enableImageAnnotationInput")
    def enable_image_annotation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableImageAnnotationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableTableAnnotationInput")
    def enable_table_annotation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableTableAnnotationInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlClassesInput")
    def exclude_html_classes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeHtmlClassesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlElementsInput")
    def exclude_html_elements_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeHtmlElementsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlIdsInput")
    def exclude_html_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeHtmlIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="structuredContentTypesInput")
    def structured_content_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "structuredContentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="enableImageAnnotation")
    def enable_image_annotation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableImageAnnotation"))

    @enable_image_annotation.setter
    def enable_image_annotation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a516653e6976f546d6dc651af756f612a4f2f4c37e45e580a61feb9cbcc37892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableImageAnnotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableTableAnnotation")
    def enable_table_annotation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableTableAnnotation"))

    @enable_table_annotation.setter
    def enable_table_annotation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3b4911b5463c276e5a56c125ad237eab64b50aab8e2a679fae590654d4f385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableTableAnnotation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlClasses")
    def exclude_html_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeHtmlClasses"))

    @exclude_html_classes.setter
    def exclude_html_classes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1a923ad724215006cf475137472347c4b8aabc8f6139dafbfa16db595f5254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHtmlClasses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlElements")
    def exclude_html_elements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeHtmlElements"))

    @exclude_html_elements.setter
    def exclude_html_elements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be65212cc7cb09ce554c0f123d28c2b49b33c70f499d10f15f5182757052a9fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHtmlElements", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeHtmlIds")
    def exclude_html_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeHtmlIds"))

    @exclude_html_ids.setter
    def exclude_html_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2395fa1770bc9e0664733bf04fc7bb4b09391cb3cccedbc2823273c8eb4dd1a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeHtmlIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="structuredContentTypes")
    def structured_content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "structuredContentTypes"))

    @structured_content_types.setter
    def structured_content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47491b89fd4c6720ab5b74412bdf2492132e9407afb3748918c8222978bccc6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "structuredContentTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4770069fea5a591d48e9a6d7cad8c1d277224ea8282b585a0dc3e585163fadd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2409d7ebec09c44b7a8f4e077569556681fd0fc2ad6d4eb603b18cbdfa40af7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5749b165e40628765e38c50bb5e96ad71ad55b3dac6a3209fbdc9155128a03ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e89bd77e1bc6ac5402b9a3e95a644d9f0275b1763b5f0995e9caee456a49859)
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
            type_hints = typing.get_type_hints(_typecheckingstub__108d4751a92517dc87938bb84bf886f65491fbec05685a1982d23980900dca87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__981cea246128e13dd4ac40fff7fe58797beb16c56ee0771fba505f997357133e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa18f7eb2a44e4c62b5705fa813a8e9e186be43acc86e939504870d303301a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig",
    jsii_struct_bases=[],
    name_mapping={"use_native_text": "useNativeText"},
)
class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig:
    def __init__(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#use_native_text DiscoveryEngineDataStore#use_native_text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa03f9ea41cf916f1e25ba84c41c48ca67a2b37df70586091f0c6a388490414)
            check_type(argname="argument use_native_text", value=use_native_text, expected_type=type_hints["use_native_text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if use_native_text is not None:
            self._values["use_native_text"] = use_native_text

    @builtins.property
    def use_native_text(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, will use native text instead of OCR text on pages containing native text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#use_native_text DiscoveryEngineDataStore#use_native_text}
        '''
        result = self._values.get("use_native_text")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9fec331b7e0b9a36a791f5031009c2d3c17bb18ee3900fef3be3a420b6f32c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__570d8e9557f7dffb0e47596f47c593e1cba83f76144f3c3a161c8977fc3ca130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useNativeText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d5794044458bcdabda9728fabf893db90750d53b2d7e1cb64ce29fb8bfcc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e849fbaf24a0c2cd1469fe6679d975addbba4be0355a6103bd64b4adff44c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDigitalParsingConfig")
    def put_digital_parsing_config(self) -> None:
        value = DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig()

        return typing.cast(None, jsii.invoke(self, "putDigitalParsingConfig", [value]))

    @jsii.member(jsii_name="putLayoutParsingConfig")
    def put_layout_parsing_config(
        self,
        *,
        enable_image_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_table_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_html_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_html_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        structured_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_image_annotation: If true, the LLM based annotation is added to the image during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_image_annotation DiscoveryEngineDataStore#enable_image_annotation}
        :param enable_table_annotation: If true, the LLM based annotation is added to the table during parsing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#enable_table_annotation DiscoveryEngineDataStore#enable_table_annotation}
        :param exclude_html_classes: List of HTML classes to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_classes DiscoveryEngineDataStore#exclude_html_classes}
        :param exclude_html_elements: List of HTML elements to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_elements DiscoveryEngineDataStore#exclude_html_elements}
        :param exclude_html_ids: List of HTML ids to exclude from the parsed content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#exclude_html_ids DiscoveryEngineDataStore#exclude_html_ids}
        :param structured_content_types: Contains the required structure types to extract from the document. Supported values: 'shareholder-structure'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#structured_content_types DiscoveryEngineDataStore#structured_content_types}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig(
            enable_image_annotation=enable_image_annotation,
            enable_table_annotation=enable_table_annotation,
            exclude_html_classes=exclude_html_classes,
            exclude_html_elements=exclude_html_elements,
            exclude_html_ids=exclude_html_ids,
            structured_content_types=structured_content_types,
        )

        return typing.cast(None, jsii.invoke(self, "putLayoutParsingConfig", [value]))

    @jsii.member(jsii_name="putOcrParsingConfig")
    def put_ocr_parsing_config(
        self,
        *,
        use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param use_native_text: If true, will use native text instead of OCR text on pages containing native text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#use_native_text DiscoveryEngineDataStore#use_native_text}
        '''
        value = DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig(
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
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference, jsii.get(self, "digitalParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfig")
    def layout_parsing_config(
        self,
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference, jsii.get(self, "layoutParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfig")
    def ocr_parsing_config(
        self,
    ) -> DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference:
        return typing.cast(DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference, jsii.get(self, "ocrParsingConfig"))

    @builtins.property
    @jsii.member(jsii_name="digitalParsingConfigInput")
    def digital_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig], jsii.get(self, "digitalParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="layoutParsingConfigInput")
    def layout_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig], jsii.get(self, "layoutParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ocrParsingConfigInput")
    def ocr_parsing_config_input(
        self,
    ) -> typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig]:
        return typing.cast(typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig], jsii.get(self, "ocrParsingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5a01d9d4a4e9319efa682ed31cea5edcd962c34f856f0ef36ea317ab7e6171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a10a6ff9d5e2f5cd5c4b0242569b37004367ddebe7a2f5bdd95ddb9702aad73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DiscoveryEngineDataStoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#create DiscoveryEngineDataStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#delete DiscoveryEngineDataStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#update DiscoveryEngineDataStore#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1798cc891b91ad5558fa033bab326d7b0d3be7d1bb06304a9d16dbe5a0f9632)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#create DiscoveryEngineDataStore#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#delete DiscoveryEngineDataStore#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/discovery_engine_data_store#update DiscoveryEngineDataStore#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscoveryEngineDataStoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DiscoveryEngineDataStoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.discoveryEngineDataStore.DiscoveryEngineDataStoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b24c9f4f486eaa2ee62bec8cf849358f2c30239181594d3135a9f759ed0fbc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6092d91998165aa537121814038d2d5376e6f05fcf8e870afdd97ee6e36d6f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee4e61d8c8940cb051c7ccd6efe9bb4136d78e9a153a41025b909b2096d28a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab0cc82847770959bb32cbd1a7bb412cf1980cc60d606b25c1d878606962a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2feb947a6a24971496123fd24ab38f02911d6fd591cb429c14b0a8e0c62835c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DiscoveryEngineDataStore",
    "DiscoveryEngineDataStoreAdvancedSiteSearchConfig",
    "DiscoveryEngineDataStoreAdvancedSiteSearchConfigOutputReference",
    "DiscoveryEngineDataStoreConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesList",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfigOutputReference",
    "DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOutputReference",
    "DiscoveryEngineDataStoreTimeouts",
    "DiscoveryEngineDataStoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d13421286928bae1c35a2a721a1d1a6773a90c0f27f27d3891f23e0fd335ffe3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    content_config: builtins.str,
    data_store_id: builtins.str,
    display_name: builtins.str,
    industry_vertical: builtins.str,
    location: builtins.str,
    advanced_site_search_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreAdvancedSiteSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    document_processing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineDataStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b855c3204654a00e59346c4938d126260a2409e261ede110809498b9c5e6e6fd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbcbddffdf24ed2e552ed09ccfc343f7624da9d509d8a4c0c038efad928de4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247c8bd8aaa616e9d6e79357654d76e2b71a02416a3cca3701f6653d5e33357d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cb1b9e81b1ffe3ef9ffb278e34977e8e7abfd3573334459e2e1d8cdef53e83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b7063accea4d22f1c8eb8dd9219175387f0d6665e58ce423f32312dc04f4a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b48eb89699bdd1619e5a55a5932d8fe78a6d8be56319da4944b1993e2acaae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f913e84edfcb0ba8d97c2f81a112dcd79a02575c6866f1a71ee07f8d9541bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7381adfb2b5a873f029acac0a3be1b8c1131da8dca9f64e280ada9e2f1bee719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4c471798a99f0e8a7cccb7c595bd1864ab6e3f840608f537b23a8b21860800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fb37d8f632f4acb3921215ff03f00fd9c3665c7524f61313762148d52dc604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00243890fe84e7dc86cc197f029c840cf54f6c317f1a609adaa4f514c1bcbbfd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff12e82f0818f9eb7cb7ce8ce4618824cfdf5abe0b10bf7cafa8100705f967f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efcf86c881aea6944abb7e0253e3d2238a14594bdce624afc9fe192e4013636(
    *,
    disable_automatic_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_initial_index: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7d0c1f8c3441e52455877cae6c2ba089dcf963bc6de6eb027cb1dff24961b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192174437606603b43c30632dcae4ec957059b112c346e962f777a9ffef8a212(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40918ff8da3d8c885de4cd82b430c9a40354ff0f17b32aa882e6b0a39c76337c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7149c0de83eef7c41af8e2ef707acbc208b09d687e1de75c5ddd86c7761779(
    value: typing.Optional[DiscoveryEngineDataStoreAdvancedSiteSearchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a651110d418daa26708a494797d010a16a6de1d3034a6b9850935d33026811(
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
    advanced_site_search_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreAdvancedSiteSearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    create_advanced_site_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    document_processing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    skip_default_schema_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    solution_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DiscoveryEngineDataStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f277a0214b43425ae373beedcb60f4453aabbacd8480e839badcb9a330263be(
    *,
    chunking_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parsing_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5db726e607cdb52d0e67e6c6c4a07817f642363e5bb053f36174c3a8d44d356(
    *,
    layout_based_chunking_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63da38a71ec3d4a4ac1cc05d2f9c95974dad5edd5a81993716e045f1ac5415f3(
    *,
    chunk_size: typing.Optional[jsii.Number] = None,
    include_ancestor_headings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0ccc3d2b6e082e13d2a52ad793dca7daf93c71c9e9a02300c4118055619bf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e10fb10e8950cf6042f4983aff3bcc5278c79b5b429c274b388a38ad141ae1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f4a4f07e01bd3d21eb7bdb2a4418d88ebee779cd0ed515d95dae15d33e96f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea3fe9180913e8ebc59a10be45f95992cf2fa435796285506f3a2178389930f(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfigLayoutBasedChunkingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae28bd2b218466fcfdc663162c11723d7d946699da73e7ce19d64e3820054ddc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5501d4e9dcdac68a6c0f13577ccfbb53feda7807ca22aa95f2840f22090b57(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigChunkingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fcf53cec42f0ee32c649bb56fd34fe04d99ebe91e98179a2a6e9f94c8f2f2d(
    *,
    digital_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    layout_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ocr_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e487f476b6efd504e66ef8a9a7c85d9edd682ca2b83d2f5a0e3b14aaeb3fd51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5141b3e3a17cadde1562f5e291cf65101825bc6fb5dda57732899b2e3b714c3(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigDigitalParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b691b7f188852c9bfb2768b1d92c29788148688031ec87b0cb72063deadd0d0(
    *,
    enable_image_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_table_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_html_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_html_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_html_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    structured_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce59267cb4e82b3ca9c2eed9d92dc5ee205058ddbfd91c2446e0bff4678acf6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130e88f6a5044c84c032842eabc01ae47c95b2d2d0b23208f4b9a35d9af37427(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0c9dc0cbaebec892f44605a8ae50fb5c2700d32d29ec0f9f17ef0f01e1a6d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280efb07f1798a2dacb0c2d823652fd7f67a09bbc7eb7a9b8d2e5e7f637b65e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0e200ec5d4ed055321500bf543d6221279b17cf597e2c1327ef5e581e00451(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4d34c22782060509128f113039b396d3e4f2645e5008704a8740b6e17ffc6f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cf4b94ecc03c0a9b06319c2e0ccb053901bacce410084e7684646e998a7e44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39be4c8a0f0a22986e745c0ba4767bf4d8cfcc5675fe5d33cb44ce860e25058a(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigLayoutParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a367527f7529392bc2cb52691e206500ffe650cca3db5c95b8a1b7d261b02e(
    *,
    use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035153900d8c238ffe7f0949107dfd4cc3f5a8ff3d3c0672d31ea6bac4c69e2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dab4f5c5197a2d22aa917bba7303d53c4416f698af1f32707a45f94ba09879d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a7d8fcf4fc1524c7684c28f8d94ff6e38d33a8280dbe16e7185fa014bd1f90(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfigOcrParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5510b5a432d9a24c0be426802557aed4e1440f098d8135fbc1a3c72a80ada6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1147e8a3d4ad0be56a36e54dd3782494afbca85cf1262bce6598921d1ec377fc(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigDefaultParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dabef1cf820be49269aa53a072350c82e52b22a33cf84906403877d753af15b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e952fff3c6ddaf1a60c9b7d1b4b69060fd6825c95c37d9064d8086c46b6ecb56(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc31c5c1d00e04107daac13310616fd3aeab23046c125e3ab85fb51807cb3bb(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d59175601863178596cc97885314bb9fbbbcdf95428af79c77bbf1eacd093fc(
    *,
    file_type: builtins.str,
    digital_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    layout_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ocr_parsing_config: typing.Optional[typing.Union[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0a27d31f6bf371e819f31619d13cead978bd016fe972895a518d31ca3b60f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5c882f8547862a3cb61194689538e05922246a7f9d27eff18fb226236bf2ed(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesDigitalParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03d54e524c96c2839fdd8af2c5b187eff60f6f0ec1bbdddb0268a8124806582(
    *,
    enable_image_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_table_annotation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_html_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_html_elements: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_html_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    structured_content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f082e46f6d3fa3e37934c9f97e57cfd9f75f02f123d474e15660593eeb070dc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a516653e6976f546d6dc651af756f612a4f2f4c37e45e580a61feb9cbcc37892(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3b4911b5463c276e5a56c125ad237eab64b50aab8e2a679fae590654d4f385(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1a923ad724215006cf475137472347c4b8aabc8f6139dafbfa16db595f5254(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be65212cc7cb09ce554c0f123d28c2b49b33c70f499d10f15f5182757052a9fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2395fa1770bc9e0664733bf04fc7bb4b09391cb3cccedbc2823273c8eb4dd1a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47491b89fd4c6720ab5b74412bdf2492132e9407afb3748918c8222978bccc6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4770069fea5a591d48e9a6d7cad8c1d277224ea8282b585a0dc3e585163fadd8(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesLayoutParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2409d7ebec09c44b7a8f4e077569556681fd0fc2ad6d4eb603b18cbdfa40af7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5749b165e40628765e38c50bb5e96ad71ad55b3dac6a3209fbdc9155128a03ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e89bd77e1bc6ac5402b9a3e95a644d9f0275b1763b5f0995e9caee456a49859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108d4751a92517dc87938bb84bf886f65491fbec05685a1982d23980900dca87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981cea246128e13dd4ac40fff7fe58797beb16c56ee0771fba505f997357133e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa18f7eb2a44e4c62b5705fa813a8e9e186be43acc86e939504870d303301a43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa03f9ea41cf916f1e25ba84c41c48ca67a2b37df70586091f0c6a388490414(
    *,
    use_native_text: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fec331b7e0b9a36a791f5031009c2d3c17bb18ee3900fef3be3a420b6f32c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570d8e9557f7dffb0e47596f47c593e1cba83f76144f3c3a161c8977fc3ca130(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d5794044458bcdabda9728fabf893db90750d53b2d7e1cb64ce29fb8bfcc36(
    value: typing.Optional[DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverridesOcrParsingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e849fbaf24a0c2cd1469fe6679d975addbba4be0355a6103bd64b4adff44c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5a01d9d4a4e9319efa682ed31cea5edcd962c34f856f0ef36ea317ab7e6171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a10a6ff9d5e2f5cd5c4b0242569b37004367ddebe7a2f5bdd95ddb9702aad73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreDocumentProcessingConfigParsingConfigOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1798cc891b91ad5558fa033bab326d7b0d3be7d1bb06304a9d16dbe5a0f9632(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b24c9f4f486eaa2ee62bec8cf849358f2c30239181594d3135a9f759ed0fbc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6092d91998165aa537121814038d2d5376e6f05fcf8e870afdd97ee6e36d6f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee4e61d8c8940cb051c7ccd6efe9bb4136d78e9a153a41025b909b2096d28a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab0cc82847770959bb32cbd1a7bb412cf1980cc60d606b25c1d878606962a4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2feb947a6a24971496123fd24ab38f02911d6fd591cb429c14b0a8e0c62835c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DiscoveryEngineDataStoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
