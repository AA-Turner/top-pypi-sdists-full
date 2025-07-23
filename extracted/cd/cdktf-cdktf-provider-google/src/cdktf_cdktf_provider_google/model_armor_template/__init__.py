r'''
# `google_model_armor_template`

Refer to the Terraform Registry for docs: [`google_model_armor_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template).
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


class ModelArmorTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template google_model_armor_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter_config: typing.Union["ModelArmorTemplateFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        template_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_metadata: typing.Optional[typing.Union["ModelArmorTemplateTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ModelArmorTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template google_model_armor_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_config ModelArmorTemplate#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#location ModelArmorTemplate#location}
        :param template_id: Id of the requesting object If auto-generating Id server-side, remove this field and template_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#template_id ModelArmorTemplate#template_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#id ModelArmorTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#labels ModelArmorTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#project ModelArmorTemplate#project}.
        :param template_metadata: template_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#template_metadata ModelArmorTemplate#template_metadata}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#timeouts ModelArmorTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f352601458d1d638cad8742300eef10a8df8bb63a33e211ef568ec2e60306b5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ModelArmorTemplateConfig(
            filter_config=filter_config,
            location=location,
            template_id=template_id,
            id=id,
            labels=labels,
            project=project,
            template_metadata=template_metadata,
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
        '''Generates CDKTF code for importing a ModelArmorTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ModelArmorTemplate to import.
        :param import_from_id: The id of the existing ModelArmorTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ModelArmorTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d08f44670ba367cdb23a3c0bc9cd4bea3a64503b29b645102c71b65bde6a3e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilterConfig")
    def put_filter_config(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#malicious_uri_filter_settings ModelArmorTemplate#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#pi_and_jailbreak_filter_settings ModelArmorTemplate#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#rai_settings ModelArmorTemplate#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#sdp_settings ModelArmorTemplate#sdp_settings}
        '''
        value = ModelArmorTemplateFilterConfig(
            malicious_uri_filter_settings=malicious_uri_filter_settings,
            pi_and_jailbreak_filter_settings=pi_and_jailbreak_filter_settings,
            rai_settings=rai_settings,
            sdp_settings=sdp_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putFilterConfig", [value]))

    @jsii.member(jsii_name="putTemplateMetadata")
    def put_template_metadata(
        self,
        *,
        custom_llm_response_safety_error_code: typing.Optional[jsii.Number] = None,
        custom_llm_response_safety_error_message: typing.Optional[builtins.str] = None,
        custom_prompt_safety_error_code: typing.Optional[jsii.Number] = None,
        custom_prompt_safety_error_message: typing.Optional[builtins.str] = None,
        enforcement_type: typing.Optional[builtins.str] = None,
        ignore_partial_invocation_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_sanitize_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_template_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multi_language_detection: typing.Optional[typing.Union["ModelArmorTemplateTemplateMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_llm_response_safety_error_code: Indicates the custom error code set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_llm_response_safety_error_code ModelArmorTemplate#custom_llm_response_safety_error_code}
        :param custom_llm_response_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_llm_response_safety_error_message ModelArmorTemplate#custom_llm_response_safety_error_message}
        :param custom_prompt_safety_error_code: Indicates the custom error code set by the user to be returned to the end user by the service extension if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_prompt_safety_error_code ModelArmorTemplate#custom_prompt_safety_error_code}
        :param custom_prompt_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_prompt_safety_error_message ModelArmorTemplate#custom_prompt_safety_error_message}
        :param enforcement_type: Possible values: INSPECT_ONLY INSPECT_AND_BLOCK. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#enforcement_type ModelArmorTemplate#enforcement_type}
        :param ignore_partial_invocation_failures: If true, partial detector failures should be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#ignore_partial_invocation_failures ModelArmorTemplate#ignore_partial_invocation_failures}
        :param log_sanitize_operations: If true, log sanitize operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#log_sanitize_operations ModelArmorTemplate#log_sanitize_operations}
        :param log_template_operations: If true, log template crud operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#log_template_operations ModelArmorTemplate#log_template_operations}
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#multi_language_detection ModelArmorTemplate#multi_language_detection}
        '''
        value = ModelArmorTemplateTemplateMetadata(
            custom_llm_response_safety_error_code=custom_llm_response_safety_error_code,
            custom_llm_response_safety_error_message=custom_llm_response_safety_error_message,
            custom_prompt_safety_error_code=custom_prompt_safety_error_code,
            custom_prompt_safety_error_message=custom_prompt_safety_error_message,
            enforcement_type=enforcement_type,
            ignore_partial_invocation_failures=ignore_partial_invocation_failures,
            log_sanitize_operations=log_sanitize_operations,
            log_template_operations=log_template_operations,
            multi_language_detection=multi_language_detection,
        )

        return typing.cast(None, jsii.invoke(self, "putTemplateMetadata", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#create ModelArmorTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#delete ModelArmorTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#update ModelArmorTemplate#update}.
        '''
        value = ModelArmorTemplateTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTemplateMetadata")
    def reset_template_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateMetadata", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="filterConfig")
    def filter_config(self) -> "ModelArmorTemplateFilterConfigOutputReference":
        return typing.cast("ModelArmorTemplateFilterConfigOutputReference", jsii.get(self, "filterConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="templateMetadata")
    def template_metadata(self) -> "ModelArmorTemplateTemplateMetadataOutputReference":
        return typing.cast("ModelArmorTemplateTemplateMetadataOutputReference", jsii.get(self, "templateMetadata"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ModelArmorTemplateTimeoutsOutputReference":
        return typing.cast("ModelArmorTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="filterConfigInput")
    def filter_config_input(self) -> typing.Optional["ModelArmorTemplateFilterConfig"]:
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfig"], jsii.get(self, "filterConfigInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="templateIdInput")
    def template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="templateMetadataInput")
    def template_metadata_input(
        self,
    ) -> typing.Optional["ModelArmorTemplateTemplateMetadata"]:
        return typing.cast(typing.Optional["ModelArmorTemplateTemplateMetadata"], jsii.get(self, "templateMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ModelArmorTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ModelArmorTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6971700633ea9a7d3d65ceda8a69287ef41286b1db623f7928a8185cc697e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca79f057b294e6689688776666613a7bb836c5d05eff2a4c48ef17c562cdcb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b80c7a8d64c01301df9866783f5ae0bc206d9a761ec87bd0db0f93fec011e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c10148c818fbedbdb75ad8483d393fa76b31e7f056427351b2f8ef70765fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8adefea9bd3cb8fd46f56f5a9a9a1df7e203f071509506018dcc0945e2afb09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter_config": "filterConfig",
        "location": "location",
        "template_id": "templateId",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "template_metadata": "templateMetadata",
        "timeouts": "timeouts",
    },
)
class ModelArmorTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter_config: typing.Union["ModelArmorTemplateFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        template_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_metadata: typing.Optional[typing.Union["ModelArmorTemplateTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ModelArmorTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_config ModelArmorTemplate#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#location ModelArmorTemplate#location}
        :param template_id: Id of the requesting object If auto-generating Id server-side, remove this field and template_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#template_id ModelArmorTemplate#template_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#id ModelArmorTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#labels ModelArmorTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#project ModelArmorTemplate#project}.
        :param template_metadata: template_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#template_metadata ModelArmorTemplate#template_metadata}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#timeouts ModelArmorTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter_config, dict):
            filter_config = ModelArmorTemplateFilterConfig(**filter_config)
        if isinstance(template_metadata, dict):
            template_metadata = ModelArmorTemplateTemplateMetadata(**template_metadata)
        if isinstance(timeouts, dict):
            timeouts = ModelArmorTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107f104711ef861f82658a242e5fe94388ab79ad1b10b772a178c828661b8ea8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter_config", value=filter_config, expected_type=type_hints["filter_config"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument template_metadata", value=template_metadata, expected_type=type_hints["template_metadata"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_config": filter_config,
            "location": location,
            "template_id": template_id,
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
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if template_metadata is not None:
            self._values["template_metadata"] = template_metadata
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
    def filter_config(self) -> "ModelArmorTemplateFilterConfig":
        '''filter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_config ModelArmorTemplate#filter_config}
        '''
        result = self._values.get("filter_config")
        assert result is not None, "Required property 'filter_config' is missing"
        return typing.cast("ModelArmorTemplateFilterConfig", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#location ModelArmorTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_id(self) -> builtins.str:
        '''Id of the requesting object If auto-generating Id server-side, remove this field and template_id from the method_signature of Create RPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#template_id ModelArmorTemplate#template_id}
        '''
        result = self._values.get("template_id")
        assert result is not None, "Required property 'template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#id ModelArmorTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#labels ModelArmorTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#project ModelArmorTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_metadata(
        self,
    ) -> typing.Optional["ModelArmorTemplateTemplateMetadata"]:
        '''template_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#template_metadata ModelArmorTemplate#template_metadata}
        '''
        result = self._values.get("template_metadata")
        return typing.cast(typing.Optional["ModelArmorTemplateTemplateMetadata"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ModelArmorTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#timeouts ModelArmorTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ModelArmorTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "malicious_uri_filter_settings": "maliciousUriFilterSettings",
        "pi_and_jailbreak_filter_settings": "piAndJailbreakFilterSettings",
        "rai_settings": "raiSettings",
        "sdp_settings": "sdpSettings",
    },
)
class ModelArmorTemplateFilterConfig:
    def __init__(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#malicious_uri_filter_settings ModelArmorTemplate#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#pi_and_jailbreak_filter_settings ModelArmorTemplate#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#rai_settings ModelArmorTemplate#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#sdp_settings ModelArmorTemplate#sdp_settings}
        '''
        if isinstance(malicious_uri_filter_settings, dict):
            malicious_uri_filter_settings = ModelArmorTemplateFilterConfigMaliciousUriFilterSettings(**malicious_uri_filter_settings)
        if isinstance(pi_and_jailbreak_filter_settings, dict):
            pi_and_jailbreak_filter_settings = ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings(**pi_and_jailbreak_filter_settings)
        if isinstance(rai_settings, dict):
            rai_settings = ModelArmorTemplateFilterConfigRaiSettings(**rai_settings)
        if isinstance(sdp_settings, dict):
            sdp_settings = ModelArmorTemplateFilterConfigSdpSettings(**sdp_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89712cf35567f0cc603bf207c7df101198f4afb7d2b281df7c55a10ac467fbc5)
            check_type(argname="argument malicious_uri_filter_settings", value=malicious_uri_filter_settings, expected_type=type_hints["malicious_uri_filter_settings"])
            check_type(argname="argument pi_and_jailbreak_filter_settings", value=pi_and_jailbreak_filter_settings, expected_type=type_hints["pi_and_jailbreak_filter_settings"])
            check_type(argname="argument rai_settings", value=rai_settings, expected_type=type_hints["rai_settings"])
            check_type(argname="argument sdp_settings", value=sdp_settings, expected_type=type_hints["sdp_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if malicious_uri_filter_settings is not None:
            self._values["malicious_uri_filter_settings"] = malicious_uri_filter_settings
        if pi_and_jailbreak_filter_settings is not None:
            self._values["pi_and_jailbreak_filter_settings"] = pi_and_jailbreak_filter_settings
        if rai_settings is not None:
            self._values["rai_settings"] = rai_settings
        if sdp_settings is not None:
            self._values["sdp_settings"] = sdp_settings

    @builtins.property
    def malicious_uri_filter_settings(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigMaliciousUriFilterSettings"]:
        '''malicious_uri_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#malicious_uri_filter_settings ModelArmorTemplate#malicious_uri_filter_settings}
        '''
        result = self._values.get("malicious_uri_filter_settings")
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigMaliciousUriFilterSettings"], result)

    @builtins.property
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"]:
        '''pi_and_jailbreak_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#pi_and_jailbreak_filter_settings ModelArmorTemplate#pi_and_jailbreak_filter_settings}
        '''
        result = self._values.get("pi_and_jailbreak_filter_settings")
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"], result)

    @builtins.property
    def rai_settings(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigRaiSettings"]:
        '''rai_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#rai_settings ModelArmorTemplate#rai_settings}
        '''
        result = self._values.get("rai_settings")
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigRaiSettings"], result)

    @builtins.property
    def sdp_settings(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigSdpSettings"]:
        '''sdp_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#sdp_settings ModelArmorTemplate#sdp_settings}
        '''
        result = self._values.get("sdp_settings")
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigSdpSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigMaliciousUriFilterSettings",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class ModelArmorTemplateFilterConfigMaliciousUriFilterSettings:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe72b77e6f5a1b4908d8492835df79c82651e9a9196a0e94644eb9d428bb6ab)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigMaliciousUriFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22c9b688889e12327c8b6df3c3bf3b0667d6779f9db4ca74b2b944dae5005dde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilterEnforcement")
    def reset_filter_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnforcement", []))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcementInput")
    def filter_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2785559ba72b56d6dd34449ba7384605cc7adc8ff69c8fdbbe3462fc72e021a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0cb1ec6081ea57483720e9ee95d28f4e504cb5870ac2465b3ce9f9219d9a02f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorTemplateFilterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97a4fe4aed26d575080f0b004272abbadc648f539fc5d85e42b0252c0d642ff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaliciousUriFilterSettings")
    def put_malicious_uri_filter_settings(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        value = ModelArmorTemplateFilterConfigMaliciousUriFilterSettings(
            filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putMaliciousUriFilterSettings", [value]))

    @jsii.member(jsii_name="putPiAndJailbreakFilterSettings")
    def put_pi_and_jailbreak_filter_settings(
        self,
        *,
        confidence_level: typing.Optional[builtins.str] = None,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#confidence_level ModelArmorTemplate#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        value = ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings(
            confidence_level=confidence_level, filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putPiAndJailbreakFilterSettings", [value]))

    @jsii.member(jsii_name="putRaiSettings")
    def put_rai_settings(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#rai_filters ModelArmorTemplate#rai_filters}
        '''
        value = ModelArmorTemplateFilterConfigRaiSettings(rai_filters=rai_filters)

        return typing.cast(None, jsii.invoke(self, "putRaiSettings", [value]))

    @jsii.member(jsii_name="putSdpSettings")
    def put_sdp_settings(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#advanced_config ModelArmorTemplate#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#basic_config ModelArmorTemplate#basic_config}
        '''
        value = ModelArmorTemplateFilterConfigSdpSettings(
            advanced_config=advanced_config, basic_config=basic_config
        )

        return typing.cast(None, jsii.invoke(self, "putSdpSettings", [value]))

    @jsii.member(jsii_name="resetMaliciousUriFilterSettings")
    def reset_malicious_uri_filter_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaliciousUriFilterSettings", []))

    @jsii.member(jsii_name="resetPiAndJailbreakFilterSettings")
    def reset_pi_and_jailbreak_filter_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiAndJailbreakFilterSettings", []))

    @jsii.member(jsii_name="resetRaiSettings")
    def reset_rai_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRaiSettings", []))

    @jsii.member(jsii_name="resetSdpSettings")
    def reset_sdp_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSdpSettings", []))

    @builtins.property
    @jsii.member(jsii_name="maliciousUriFilterSettings")
    def malicious_uri_filter_settings(
        self,
    ) -> ModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference:
        return typing.cast(ModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference, jsii.get(self, "maliciousUriFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettings")
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> "ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference":
        return typing.cast("ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference", jsii.get(self, "piAndJailbreakFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="raiSettings")
    def rai_settings(
        self,
    ) -> "ModelArmorTemplateFilterConfigRaiSettingsOutputReference":
        return typing.cast("ModelArmorTemplateFilterConfigRaiSettingsOutputReference", jsii.get(self, "raiSettings"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettings")
    def sdp_settings(
        self,
    ) -> "ModelArmorTemplateFilterConfigSdpSettingsOutputReference":
        return typing.cast("ModelArmorTemplateFilterConfigSdpSettingsOutputReference", jsii.get(self, "sdpSettings"))

    @builtins.property
    @jsii.member(jsii_name="maliciousUriFilterSettingsInput")
    def malicious_uri_filter_settings_input(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings], jsii.get(self, "maliciousUriFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettingsInput")
    def pi_and_jailbreak_filter_settings_input(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"]:
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"], jsii.get(self, "piAndJailbreakFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="raiSettingsInput")
    def rai_settings_input(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigRaiSettings"]:
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigRaiSettings"], jsii.get(self, "raiSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettingsInput")
    def sdp_settings_input(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigSdpSettings"]:
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigSdpSettings"], jsii.get(self, "sdpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ModelArmorTemplateFilterConfig]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e0f7534be48b1bce2a9952cd8f70f32f2933f40d27b9cc72fd00f5dee3be76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_level": "confidenceLevel",
        "filter_enforcement": "filterEnforcement",
    },
)
class ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings:
    def __init__(
        self,
        *,
        confidence_level: typing.Optional[builtins.str] = None,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#confidence_level ModelArmorTemplate#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa76c42fcc222b91acb4b003c27d8b2ae8f0ca68c7627b7c289f9448230d172)
            check_type(argname="argument confidence_level", value=confidence_level, expected_type=type_hints["confidence_level"])
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidence_level is not None:
            self._values["confidence_level"] = confidence_level
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def confidence_level(self) -> typing.Optional[builtins.str]:
        '''Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#confidence_level ModelArmorTemplate#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d22654dd5c220c3047cd3cf5037525104ca2144745f9b32c47ea6376aa6c17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfidenceLevel")
    def reset_confidence_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceLevel", []))

    @jsii.member(jsii_name="resetFilterEnforcement")
    def reset_filter_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnforcement", []))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevelInput")
    def confidence_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidenceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcementInput")
    def filter_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevel")
    def confidence_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidenceLevel"))

    @confidence_level.setter
    def confidence_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9088083a907acfb85cc416ed4e650a22a75675ca175355b52eb96fc13d7024fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb5d909dea6b68bda87d11640fc1a963f18bb390e0aa80acc7e1007d5346396d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a9d3f24c693c0d3e4d9f4cc6a48883e11dd551f9b133a89169637fb2c8fa45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigRaiSettings",
    jsii_struct_bases=[],
    name_mapping={"rai_filters": "raiFilters"},
)
class ModelArmorTemplateFilterConfigRaiSettings:
    def __init__(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#rai_filters ModelArmorTemplate#rai_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58fe96c73ba2c676e04a138134a0d95446fbd57f8cc3028dd8ed5e77ef99769b)
            check_type(argname="argument rai_filters", value=rai_filters, expected_type=type_hints["rai_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rai_filters": rai_filters,
        }

    @builtins.property
    def rai_filters(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]]:
        '''rai_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#rai_filters ModelArmorTemplate#rai_filters}
        '''
        result = self._values.get("rai_filters")
        assert result is not None, "Required property 'rai_filters' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigRaiSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateFilterConfigRaiSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigRaiSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7003ef5bdd0618a452d03b1dbc93fa9998f1bc270b9c8292653b733802498071)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRaiFilters")
    def put_rai_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e034e4cc9aaf92306025086eb060687ec5d19d2f967739fd8faf9a6cf9a18cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRaiFilters", [value]))

    @builtins.property
    @jsii.member(jsii_name="raiFilters")
    def rai_filters(self) -> "ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList":
        return typing.cast("ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList", jsii.get(self, "raiFilters"))

    @builtins.property
    @jsii.member(jsii_name="raiFiltersInput")
    def rai_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]]], jsii.get(self, "raiFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigRaiSettings]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigRaiSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfigRaiSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337eeaa95d2774f6fbecefde91e517b1115668fd72692a4e50d73f5ddadc2dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigRaiSettingsRaiFilters",
    jsii_struct_bases=[],
    name_mapping={"filter_type": "filterType", "confidence_level": "confidenceLevel"},
)
class ModelArmorTemplateFilterConfigRaiSettingsRaiFilters:
    def __init__(
        self,
        *,
        filter_type: builtins.str,
        confidence_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_type: Possible values: SEXUALLY_EXPLICIT HATE_SPEECH HARASSMENT DANGEROUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_type ModelArmorTemplate#filter_type}
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#confidence_level ModelArmorTemplate#confidence_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed780c5ce181ab240b77f0e7540fbf817762b315735efbf4f5975f35c9d34ae)
            check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            check_type(argname="argument confidence_level", value=confidence_level, expected_type=type_hints["confidence_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_type": filter_type,
        }
        if confidence_level is not None:
            self._values["confidence_level"] = confidence_level

    @builtins.property
    def filter_type(self) -> builtins.str:
        '''Possible values: SEXUALLY_EXPLICIT HATE_SPEECH HARASSMENT DANGEROUS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_type ModelArmorTemplate#filter_type}
        '''
        result = self._values.get("filter_type")
        assert result is not None, "Required property 'filter_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confidence_level(self) -> typing.Optional[builtins.str]:
        '''Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#confidence_level ModelArmorTemplate#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigRaiSettingsRaiFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff184ac495751917fdb7ed3403e6f9bd00598cb41aaf80ac7f025a0d6faaf1c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985d87f4bb9af779d9faac6965dd3304aac4f8f5c7cce38ef908179670261111)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d82617e56ac0c99f608c434dc1e2e1e7a947924a86e73992c478f03eeb543f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26d0ab91d61e5b21f8d244a61af3f41523b150a317d63fa1192ff6c29283b482)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7bb5323417432a253ac00b59e56bfa890795eb35560cc3ba73831a4ddb18f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15bd5d4773e92acda46cba4b2569654eefdc3846402c7d7dc614dd4338b65de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b7294a7c02be55ee2e5535a7f1bdc4e91b3435b7c7fc54e5730eb1c7929eb8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfidenceLevel")
    def reset_confidence_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceLevel", []))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevelInput")
    def confidence_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidenceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="filterTypeInput")
    def filter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevel")
    def confidence_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidenceLevel"))

    @confidence_level.setter
    def confidence_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea442618df4fdccbc589ef8027887b061df8379b887b348fc4d6b83c1fdc65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @filter_type.setter
    def filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff99305b2565d6c567e2e78953bf928110a08926da3a992259bd4c16770e215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a13ff131662fa7853cd12181d744701e0b1be7001d83cc6acbe649e98986ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigSdpSettings",
    jsii_struct_bases=[],
    name_mapping={"advanced_config": "advancedConfig", "basic_config": "basicConfig"},
)
class ModelArmorTemplateFilterConfigSdpSettings:
    def __init__(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["ModelArmorTemplateFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#advanced_config ModelArmorTemplate#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#basic_config ModelArmorTemplate#basic_config}
        '''
        if isinstance(advanced_config, dict):
            advanced_config = ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig(**advanced_config)
        if isinstance(basic_config, dict):
            basic_config = ModelArmorTemplateFilterConfigSdpSettingsBasicConfig(**basic_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c026e8f8985e92f4606f8473a2955e344512d9b8a5afee036219cd6009ef74b6)
            check_type(argname="argument advanced_config", value=advanced_config, expected_type=type_hints["advanced_config"])
            check_type(argname="argument basic_config", value=basic_config, expected_type=type_hints["basic_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_config is not None:
            self._values["advanced_config"] = advanced_config
        if basic_config is not None:
            self._values["basic_config"] = basic_config

    @builtins.property
    def advanced_config(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig"]:
        '''advanced_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#advanced_config ModelArmorTemplate#advanced_config}
        '''
        result = self._values.get("advanced_config")
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig"], result)

    @builtins.property
    def basic_config(
        self,
    ) -> typing.Optional["ModelArmorTemplateFilterConfigSdpSettingsBasicConfig"]:
        '''basic_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#basic_config ModelArmorTemplate#basic_config}
        '''
        result = self._values.get("basic_config")
        return typing.cast(typing.Optional["ModelArmorTemplateFilterConfigSdpSettingsBasicConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigSdpSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify_template": "deidentifyTemplate",
        "inspect_template": "inspectTemplate",
    },
)
class ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig:
    def __init__(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        inspect_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#deidentify_template ModelArmorTemplate#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#inspect_template ModelArmorTemplate#inspect_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f9045fd53549763af5ae2ec3805555b827accf3805c3a69e3f8fe68e3400b9)
            check_type(argname="argument deidentify_template", value=deidentify_template, expected_type=type_hints["deidentify_template"])
            check_type(argname="argument inspect_template", value=inspect_template, expected_type=type_hints["inspect_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deidentify_template is not None:
            self._values["deidentify_template"] = deidentify_template
        if inspect_template is not None:
            self._values["inspect_template"] = inspect_template

    @builtins.property
    def deidentify_template(self) -> typing.Optional[builtins.str]:
        '''Optional Sensitive Data Protection Deidentify template resource name.

        If provided then DeidentifyContent action is performed during Sanitization
        using this template and inspect template. The De-identified data will
        be returned in SdpDeidentifyResult.
        Note that all info-types present in the deidentify template must be present
        in inspect template.
        e.g.
        'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#deidentify_template ModelArmorTemplate#deidentify_template}
        '''
        result = self._values.get("deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_template(self) -> typing.Optional[builtins.str]:
        '''Sensitive Data Protection inspect template resource name If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization.

        All Sensitive Data Protection findings identified during
        inspection will be returned as SdpFinding in SdpInsepctionResult.
        e.g:-
        'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#inspect_template ModelArmorTemplate#inspect_template}
        '''
        result = self._values.get("inspect_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e15661dae7c59923d257b91f4f69fa572626003f9ab6d5eb32ae9c33d4687e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeidentifyTemplate")
    def reset_deidentify_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeidentifyTemplate", []))

    @jsii.member(jsii_name="resetInspectTemplate")
    def reset_inspect_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplateInput")
    def deidentify_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deidentifyTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateInput")
    def inspect_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplate")
    def deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deidentifyTemplate"))

    @deidentify_template.setter
    def deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09ecec38a3efa684568503aeaee80cf0d6f1e04256fc100ad988fd4cae94260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplate")
    def inspect_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplate"))

    @inspect_template.setter
    def inspect_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055f3fb82c3a0cf1d297cb7bcb589f7ba26be8f6a8fc10be0d61b1043bea6337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183f74a734df65feb2e2bd5e114968eaa7279f598b4ff88cd0bf1a597373c1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigSdpSettingsBasicConfig",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class ModelArmorTemplateFilterConfigSdpSettingsBasicConfig:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95283432c4211dfdf8e0b2459a0bafec123dc33d6100964d676e472577886b6c)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateFilterConfigSdpSettingsBasicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b53234a266bec037925c3d8b89a0270f4f70ebc91780024146f4aa147053c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilterEnforcement")
    def reset_filter_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnforcement", []))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcementInput")
    def filter_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f65a3780211f0ef7f0a3accfbf3a54fbeb99719173a5226d2b2eaaa81113a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ed81a3ff9de9666aa8adcfbd134158f5c3980a75924e2c3150b4ee05ad9de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorTemplateFilterConfigSdpSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateFilterConfigSdpSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1121ae76e56803986d5644dab10465bcbe6b8a211a8fa1453c576487984593a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedConfig")
    def put_advanced_config(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        inspect_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#deidentify_template ModelArmorTemplate#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#inspect_template ModelArmorTemplate#inspect_template}
        '''
        value = ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig(
            deidentify_template=deidentify_template, inspect_template=inspect_template
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedConfig", [value]))

    @jsii.member(jsii_name="putBasicConfig")
    def put_basic_config(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#filter_enforcement ModelArmorTemplate#filter_enforcement}
        '''
        value = ModelArmorTemplateFilterConfigSdpSettingsBasicConfig(
            filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putBasicConfig", [value]))

    @jsii.member(jsii_name="resetAdvancedConfig")
    def reset_advanced_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedConfig", []))

    @jsii.member(jsii_name="resetBasicConfig")
    def reset_basic_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicConfig", []))

    @builtins.property
    @jsii.member(jsii_name="advancedConfig")
    def advanced_config(
        self,
    ) -> ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference:
        return typing.cast(ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference, jsii.get(self, "advancedConfig"))

    @builtins.property
    @jsii.member(jsii_name="basicConfig")
    def basic_config(
        self,
    ) -> ModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference:
        return typing.cast(ModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference, jsii.get(self, "basicConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedConfigInput")
    def advanced_config_input(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "advancedConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="basicConfigInput")
    def basic_config_input(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig], jsii.get(self, "basicConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateFilterConfigSdpSettings]:
        return typing.cast(typing.Optional[ModelArmorTemplateFilterConfigSdpSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateFilterConfigSdpSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0ce0eb976432a46ea846f5bf7b5296aaf1e88bd37a99b3eb11438ad34fb1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateTemplateMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "custom_llm_response_safety_error_code": "customLlmResponseSafetyErrorCode",
        "custom_llm_response_safety_error_message": "customLlmResponseSafetyErrorMessage",
        "custom_prompt_safety_error_code": "customPromptSafetyErrorCode",
        "custom_prompt_safety_error_message": "customPromptSafetyErrorMessage",
        "enforcement_type": "enforcementType",
        "ignore_partial_invocation_failures": "ignorePartialInvocationFailures",
        "log_sanitize_operations": "logSanitizeOperations",
        "log_template_operations": "logTemplateOperations",
        "multi_language_detection": "multiLanguageDetection",
    },
)
class ModelArmorTemplateTemplateMetadata:
    def __init__(
        self,
        *,
        custom_llm_response_safety_error_code: typing.Optional[jsii.Number] = None,
        custom_llm_response_safety_error_message: typing.Optional[builtins.str] = None,
        custom_prompt_safety_error_code: typing.Optional[jsii.Number] = None,
        custom_prompt_safety_error_message: typing.Optional[builtins.str] = None,
        enforcement_type: typing.Optional[builtins.str] = None,
        ignore_partial_invocation_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_sanitize_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_template_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multi_language_detection: typing.Optional[typing.Union["ModelArmorTemplateTemplateMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_llm_response_safety_error_code: Indicates the custom error code set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_llm_response_safety_error_code ModelArmorTemplate#custom_llm_response_safety_error_code}
        :param custom_llm_response_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_llm_response_safety_error_message ModelArmorTemplate#custom_llm_response_safety_error_message}
        :param custom_prompt_safety_error_code: Indicates the custom error code set by the user to be returned to the end user by the service extension if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_prompt_safety_error_code ModelArmorTemplate#custom_prompt_safety_error_code}
        :param custom_prompt_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_prompt_safety_error_message ModelArmorTemplate#custom_prompt_safety_error_message}
        :param enforcement_type: Possible values: INSPECT_ONLY INSPECT_AND_BLOCK. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#enforcement_type ModelArmorTemplate#enforcement_type}
        :param ignore_partial_invocation_failures: If true, partial detector failures should be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#ignore_partial_invocation_failures ModelArmorTemplate#ignore_partial_invocation_failures}
        :param log_sanitize_operations: If true, log sanitize operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#log_sanitize_operations ModelArmorTemplate#log_sanitize_operations}
        :param log_template_operations: If true, log template crud operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#log_template_operations ModelArmorTemplate#log_template_operations}
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#multi_language_detection ModelArmorTemplate#multi_language_detection}
        '''
        if isinstance(multi_language_detection, dict):
            multi_language_detection = ModelArmorTemplateTemplateMetadataMultiLanguageDetection(**multi_language_detection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e111eef05dd6c06313a7fa027295a29acd244be58065bd4f5a3aa27d953ad2f)
            check_type(argname="argument custom_llm_response_safety_error_code", value=custom_llm_response_safety_error_code, expected_type=type_hints["custom_llm_response_safety_error_code"])
            check_type(argname="argument custom_llm_response_safety_error_message", value=custom_llm_response_safety_error_message, expected_type=type_hints["custom_llm_response_safety_error_message"])
            check_type(argname="argument custom_prompt_safety_error_code", value=custom_prompt_safety_error_code, expected_type=type_hints["custom_prompt_safety_error_code"])
            check_type(argname="argument custom_prompt_safety_error_message", value=custom_prompt_safety_error_message, expected_type=type_hints["custom_prompt_safety_error_message"])
            check_type(argname="argument enforcement_type", value=enforcement_type, expected_type=type_hints["enforcement_type"])
            check_type(argname="argument ignore_partial_invocation_failures", value=ignore_partial_invocation_failures, expected_type=type_hints["ignore_partial_invocation_failures"])
            check_type(argname="argument log_sanitize_operations", value=log_sanitize_operations, expected_type=type_hints["log_sanitize_operations"])
            check_type(argname="argument log_template_operations", value=log_template_operations, expected_type=type_hints["log_template_operations"])
            check_type(argname="argument multi_language_detection", value=multi_language_detection, expected_type=type_hints["multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_llm_response_safety_error_code is not None:
            self._values["custom_llm_response_safety_error_code"] = custom_llm_response_safety_error_code
        if custom_llm_response_safety_error_message is not None:
            self._values["custom_llm_response_safety_error_message"] = custom_llm_response_safety_error_message
        if custom_prompt_safety_error_code is not None:
            self._values["custom_prompt_safety_error_code"] = custom_prompt_safety_error_code
        if custom_prompt_safety_error_message is not None:
            self._values["custom_prompt_safety_error_message"] = custom_prompt_safety_error_message
        if enforcement_type is not None:
            self._values["enforcement_type"] = enforcement_type
        if ignore_partial_invocation_failures is not None:
            self._values["ignore_partial_invocation_failures"] = ignore_partial_invocation_failures
        if log_sanitize_operations is not None:
            self._values["log_sanitize_operations"] = log_sanitize_operations
        if log_template_operations is not None:
            self._values["log_template_operations"] = log_template_operations
        if multi_language_detection is not None:
            self._values["multi_language_detection"] = multi_language_detection

    @builtins.property
    def custom_llm_response_safety_error_code(self) -> typing.Optional[jsii.Number]:
        '''Indicates the custom error code set by the user to be returned to the end user if the LLM response trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_llm_response_safety_error_code ModelArmorTemplate#custom_llm_response_safety_error_code}
        '''
        result = self._values.get("custom_llm_response_safety_error_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_llm_response_safety_error_message(self) -> typing.Optional[builtins.str]:
        '''Indicates the custom error message set by the user to be returned to the end user if the LLM response trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_llm_response_safety_error_message ModelArmorTemplate#custom_llm_response_safety_error_message}
        '''
        result = self._values.get("custom_llm_response_safety_error_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_prompt_safety_error_code(self) -> typing.Optional[jsii.Number]:
        '''Indicates the custom error code set by the user to be returned to the end user by the service extension if the prompt trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_prompt_safety_error_code ModelArmorTemplate#custom_prompt_safety_error_code}
        '''
        result = self._values.get("custom_prompt_safety_error_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_prompt_safety_error_message(self) -> typing.Optional[builtins.str]:
        '''Indicates the custom error message set by the user to be returned to the end user if the prompt trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#custom_prompt_safety_error_message ModelArmorTemplate#custom_prompt_safety_error_message}
        '''
        result = self._values.get("custom_prompt_safety_error_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforcement_type(self) -> typing.Optional[builtins.str]:
        '''Possible values: INSPECT_ONLY INSPECT_AND_BLOCK.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#enforcement_type ModelArmorTemplate#enforcement_type}
        '''
        result = self._values.get("enforcement_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_partial_invocation_failures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, partial detector failures should be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#ignore_partial_invocation_failures ModelArmorTemplate#ignore_partial_invocation_failures}
        '''
        result = self._values.get("ignore_partial_invocation_failures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_sanitize_operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, log sanitize operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#log_sanitize_operations ModelArmorTemplate#log_sanitize_operations}
        '''
        result = self._values.get("log_sanitize_operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_template_operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, log template crud operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#log_template_operations ModelArmorTemplate#log_template_operations}
        '''
        result = self._values.get("log_template_operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def multi_language_detection(
        self,
    ) -> typing.Optional["ModelArmorTemplateTemplateMetadataMultiLanguageDetection"]:
        '''multi_language_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#multi_language_detection ModelArmorTemplate#multi_language_detection}
        '''
        result = self._values.get("multi_language_detection")
        return typing.cast(typing.Optional["ModelArmorTemplateTemplateMetadataMultiLanguageDetection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateTemplateMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateTemplateMetadataMultiLanguageDetection",
    jsii_struct_bases=[],
    name_mapping={"enable_multi_language_detection": "enableMultiLanguageDetection"},
)
class ModelArmorTemplateTemplateMetadataMultiLanguageDetection:
    def __init__(
        self,
        *,
        enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#enable_multi_language_detection ModelArmorTemplate#enable_multi_language_detection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26075dd55aa8767436e7321700ae0f14834c761b5eaa944836666fef584a690)
            check_type(argname="argument enable_multi_language_detection", value=enable_multi_language_detection, expected_type=type_hints["enable_multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_multi_language_detection": enable_multi_language_detection,
        }

    @builtins.property
    def enable_multi_language_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, multi language detection will be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#enable_multi_language_detection ModelArmorTemplate#enable_multi_language_detection}
        '''
        result = self._values.get("enable_multi_language_detection")
        assert result is not None, "Required property 'enable_multi_language_detection' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateTemplateMetadataMultiLanguageDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5284fa4360d5eb05ff0e080c804652de5e79ea3ed52798d1bd4bc1333caa9a70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableMultiLanguageDetectionInput")
    def enable_multi_language_detection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableMultiLanguageDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableMultiLanguageDetection")
    def enable_multi_language_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableMultiLanguageDetection"))

    @enable_multi_language_detection.setter
    def enable_multi_language_detection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e19ae4acebdc30295168fda3ad12cc9b2c945b6caa334ff5e62b838fc69d4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMultiLanguageDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorTemplateTemplateMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[ModelArmorTemplateTemplateMetadataMultiLanguageDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateTemplateMetadataMultiLanguageDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168c9c713f80f46ea23c8136412dfbaca6f31030ee9c65256ebcb5fad7d433fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorTemplateTemplateMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateTemplateMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d17cceab2fe548c8ee9d714becae3dbb37d0513d865d22e2ee293658ce5b2d23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMultiLanguageDetection")
    def put_multi_language_detection(
        self,
        *,
        enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#enable_multi_language_detection ModelArmorTemplate#enable_multi_language_detection}
        '''
        value = ModelArmorTemplateTemplateMetadataMultiLanguageDetection(
            enable_multi_language_detection=enable_multi_language_detection
        )

        return typing.cast(None, jsii.invoke(self, "putMultiLanguageDetection", [value]))

    @jsii.member(jsii_name="resetCustomLlmResponseSafetyErrorCode")
    def reset_custom_llm_response_safety_error_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLlmResponseSafetyErrorCode", []))

    @jsii.member(jsii_name="resetCustomLlmResponseSafetyErrorMessage")
    def reset_custom_llm_response_safety_error_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLlmResponseSafetyErrorMessage", []))

    @jsii.member(jsii_name="resetCustomPromptSafetyErrorCode")
    def reset_custom_prompt_safety_error_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPromptSafetyErrorCode", []))

    @jsii.member(jsii_name="resetCustomPromptSafetyErrorMessage")
    def reset_custom_prompt_safety_error_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPromptSafetyErrorMessage", []))

    @jsii.member(jsii_name="resetEnforcementType")
    def reset_enforcement_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforcementType", []))

    @jsii.member(jsii_name="resetIgnorePartialInvocationFailures")
    def reset_ignore_partial_invocation_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnorePartialInvocationFailures", []))

    @jsii.member(jsii_name="resetLogSanitizeOperations")
    def reset_log_sanitize_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogSanitizeOperations", []))

    @jsii.member(jsii_name="resetLogTemplateOperations")
    def reset_log_template_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogTemplateOperations", []))

    @jsii.member(jsii_name="resetMultiLanguageDetection")
    def reset_multi_language_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiLanguageDetection", []))

    @builtins.property
    @jsii.member(jsii_name="multiLanguageDetection")
    def multi_language_detection(
        self,
    ) -> ModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference:
        return typing.cast(ModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference, jsii.get(self, "multiLanguageDetection"))

    @builtins.property
    @jsii.member(jsii_name="customLlmResponseSafetyErrorCodeInput")
    def custom_llm_response_safety_error_code_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customLlmResponseSafetyErrorCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="customLlmResponseSafetyErrorMessageInput")
    def custom_llm_response_safety_error_message_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLlmResponseSafetyErrorMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="customPromptSafetyErrorCodeInput")
    def custom_prompt_safety_error_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "customPromptSafetyErrorCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="customPromptSafetyErrorMessageInput")
    def custom_prompt_safety_error_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customPromptSafetyErrorMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcementTypeInput")
    def enforcement_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforcementTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ignorePartialInvocationFailuresInput")
    def ignore_partial_invocation_failures_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignorePartialInvocationFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="logSanitizeOperationsInput")
    def log_sanitize_operations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logSanitizeOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="logTemplateOperationsInput")
    def log_template_operations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logTemplateOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="multiLanguageDetectionInput")
    def multi_language_detection_input(
        self,
    ) -> typing.Optional[ModelArmorTemplateTemplateMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[ModelArmorTemplateTemplateMetadataMultiLanguageDetection], jsii.get(self, "multiLanguageDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="customLlmResponseSafetyErrorCode")
    def custom_llm_response_safety_error_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customLlmResponseSafetyErrorCode"))

    @custom_llm_response_safety_error_code.setter
    def custom_llm_response_safety_error_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d35da850ef3b83c7bbbb74ee16293408d0c8227560b2303922c74ff77072b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLlmResponseSafetyErrorCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customLlmResponseSafetyErrorMessage")
    def custom_llm_response_safety_error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLlmResponseSafetyErrorMessage"))

    @custom_llm_response_safety_error_message.setter
    def custom_llm_response_safety_error_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf820a1a2962c1eac57eff2010210077435672c10539569b162e7896d20d765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLlmResponseSafetyErrorMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPromptSafetyErrorCode")
    def custom_prompt_safety_error_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customPromptSafetyErrorCode"))

    @custom_prompt_safety_error_code.setter
    def custom_prompt_safety_error_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5b9114aa442daf6caf12607929b79e4f97906a73585a396740a4c1b2e85730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPromptSafetyErrorCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPromptSafetyErrorMessage")
    def custom_prompt_safety_error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPromptSafetyErrorMessage"))

    @custom_prompt_safety_error_message.setter
    def custom_prompt_safety_error_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e86c0c28f39e9beb7525762e39ef7d1918a263128bd6110481f85f9a48e070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPromptSafetyErrorMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcementType")
    def enforcement_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementType"))

    @enforcement_type.setter
    def enforcement_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb61d1cfba0ea22cdacbf7bb0c90587adf54ad788f4da2578112c1bf64a5c90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcementType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignorePartialInvocationFailures")
    def ignore_partial_invocation_failures(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignorePartialInvocationFailures"))

    @ignore_partial_invocation_failures.setter
    def ignore_partial_invocation_failures(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eeedd14401178f2afde67496d20666e5c673157901f9693ee86c1565c4eee52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignorePartialInvocationFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logSanitizeOperations")
    def log_sanitize_operations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logSanitizeOperations"))

    @log_sanitize_operations.setter
    def log_sanitize_operations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c0f5b0c6c7ae8bc2fb93c4ea04baf6783b9ac68f5b51c48d7d50ac4148fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logSanitizeOperations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTemplateOperations")
    def log_template_operations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logTemplateOperations"))

    @log_template_operations.setter
    def log_template_operations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4c72ba0f765728f2ff787e0176d81182c96c8987ab828b4ab72e7802a7a540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTemplateOperations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ModelArmorTemplateTemplateMetadata]:
        return typing.cast(typing.Optional[ModelArmorTemplateTemplateMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorTemplateTemplateMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962ec031c1183423ff7c91d03a280a5639443b384961936186c066a80ed6112f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ModelArmorTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#create ModelArmorTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#delete ModelArmorTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#update ModelArmorTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae19ba67b027a28e9173fb83bfe5dea06a0b5fb22fdc0e5906e738b7bb92b3d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#create ModelArmorTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#delete ModelArmorTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_template#update ModelArmorTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorTemplate.ModelArmorTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__251a2fa8fc2920e313e95e4c5ecfb4d1f96a5cb0d5da44c164662d89eb3114e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b195a00320989f11b15d802dcb872d1e27eb8ec186d3f6afb5a2da5d244f743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308e90b57ba9efe387d350953ea9288096c3e17a8eb8a2161b406ea141e000b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc2102936be5112ad13cfdba707dc348509496552759593f45dbe08d7410207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f6de870359d0f95b6566b7d6efb1ca388569c7c3d25bfeeb020949c99d5abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ModelArmorTemplate",
    "ModelArmorTemplateConfig",
    "ModelArmorTemplateFilterConfig",
    "ModelArmorTemplateFilterConfigMaliciousUriFilterSettings",
    "ModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference",
    "ModelArmorTemplateFilterConfigOutputReference",
    "ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings",
    "ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference",
    "ModelArmorTemplateFilterConfigRaiSettings",
    "ModelArmorTemplateFilterConfigRaiSettingsOutputReference",
    "ModelArmorTemplateFilterConfigRaiSettingsRaiFilters",
    "ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList",
    "ModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference",
    "ModelArmorTemplateFilterConfigSdpSettings",
    "ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig",
    "ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference",
    "ModelArmorTemplateFilterConfigSdpSettingsBasicConfig",
    "ModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference",
    "ModelArmorTemplateFilterConfigSdpSettingsOutputReference",
    "ModelArmorTemplateTemplateMetadata",
    "ModelArmorTemplateTemplateMetadataMultiLanguageDetection",
    "ModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference",
    "ModelArmorTemplateTemplateMetadataOutputReference",
    "ModelArmorTemplateTimeouts",
    "ModelArmorTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f352601458d1d638cad8742300eef10a8df8bb63a33e211ef568ec2e60306b5b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter_config: typing.Union[ModelArmorTemplateFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    template_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_metadata: typing.Optional[typing.Union[ModelArmorTemplateTemplateMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ModelArmorTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7d08f44670ba367cdb23a3c0bc9cd4bea3a64503b29b645102c71b65bde6a3e1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6971700633ea9a7d3d65ceda8a69287ef41286b1db623f7928a8185cc697e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca79f057b294e6689688776666613a7bb836c5d05eff2a4c48ef17c562cdcb36(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b80c7a8d64c01301df9866783f5ae0bc206d9a761ec87bd0db0f93fec011e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c10148c818fbedbdb75ad8483d393fa76b31e7f056427351b2f8ef70765fe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8adefea9bd3cb8fd46f56f5a9a9a1df7e203f071509506018dcc0945e2afb09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107f104711ef861f82658a242e5fe94388ab79ad1b10b772a178c828661b8ea8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter_config: typing.Union[ModelArmorTemplateFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    template_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_metadata: typing.Optional[typing.Union[ModelArmorTemplateTemplateMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ModelArmorTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89712cf35567f0cc603bf207c7df101198f4afb7d2b281df7c55a10ac467fbc5(
    *,
    malicious_uri_filter_settings: typing.Optional[typing.Union[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    pi_and_jailbreak_filter_settings: typing.Optional[typing.Union[ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    rai_settings: typing.Optional[typing.Union[ModelArmorTemplateFilterConfigRaiSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    sdp_settings: typing.Optional[typing.Union[ModelArmorTemplateFilterConfigSdpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe72b77e6f5a1b4908d8492835df79c82651e9a9196a0e94644eb9d428bb6ab(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c9b688889e12327c8b6df3c3bf3b0667d6779f9db4ca74b2b944dae5005dde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2785559ba72b56d6dd34449ba7384605cc7adc8ff69c8fdbbe3462fc72e021a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cb1ec6081ea57483720e9ee95d28f4e504cb5870ac2465b3ce9f9219d9a02f(
    value: typing.Optional[ModelArmorTemplateFilterConfigMaliciousUriFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a4fe4aed26d575080f0b004272abbadc648f539fc5d85e42b0252c0d642ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e0f7534be48b1bce2a9952cd8f70f32f2933f40d27b9cc72fd00f5dee3be76(
    value: typing.Optional[ModelArmorTemplateFilterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa76c42fcc222b91acb4b003c27d8b2ae8f0ca68c7627b7c289f9448230d172(
    *,
    confidence_level: typing.Optional[builtins.str] = None,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d22654dd5c220c3047cd3cf5037525104ca2144745f9b32c47ea6376aa6c17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9088083a907acfb85cc416ed4e650a22a75675ca175355b52eb96fc13d7024fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5d909dea6b68bda87d11640fc1a963f18bb390e0aa80acc7e1007d5346396d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a9d3f24c693c0d3e4d9f4cc6a48883e11dd551f9b133a89169637fb2c8fa45(
    value: typing.Optional[ModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fe96c73ba2c676e04a138134a0d95446fbd57f8cc3028dd8ed5e77ef99769b(
    *,
    rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ModelArmorTemplateFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7003ef5bdd0618a452d03b1dbc93fa9998f1bc270b9c8292653b733802498071(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e034e4cc9aaf92306025086eb060687ec5d19d2f967739fd8faf9a6cf9a18cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ModelArmorTemplateFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337eeaa95d2774f6fbecefde91e517b1115668fd72692a4e50d73f5ddadc2dd6(
    value: typing.Optional[ModelArmorTemplateFilterConfigRaiSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed780c5ce181ab240b77f0e7540fbf817762b315735efbf4f5975f35c9d34ae(
    *,
    filter_type: builtins.str,
    confidence_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff184ac495751917fdb7ed3403e6f9bd00598cb41aaf80ac7f025a0d6faaf1c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985d87f4bb9af779d9faac6965dd3304aac4f8f5c7cce38ef908179670261111(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d82617e56ac0c99f608c434dc1e2e1e7a947924a86e73992c478f03eeb543f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d0ab91d61e5b21f8d244a61af3f41523b150a317d63fa1192ff6c29283b482(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7bb5323417432a253ac00b59e56bfa890795eb35560cc3ba73831a4ddb18f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bd5d4773e92acda46cba4b2569654eefdc3846402c7d7dc614dd4338b65de0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7294a7c02be55ee2e5535a7f1bdc4e91b3435b7c7fc54e5730eb1c7929eb8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea442618df4fdccbc589ef8027887b061df8379b887b348fc4d6b83c1fdc65f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff99305b2565d6c567e2e78953bf928110a08926da3a992259bd4c16770e215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a13ff131662fa7853cd12181d744701e0b1be7001d83cc6acbe649e98986ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateFilterConfigRaiSettingsRaiFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c026e8f8985e92f4606f8473a2955e344512d9b8a5afee036219cd6009ef74b6(
    *,
    advanced_config: typing.Optional[typing.Union[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_config: typing.Optional[typing.Union[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f9045fd53549763af5ae2ec3805555b827accf3805c3a69e3f8fe68e3400b9(
    *,
    deidentify_template: typing.Optional[builtins.str] = None,
    inspect_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e15661dae7c59923d257b91f4f69fa572626003f9ab6d5eb32ae9c33d4687e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09ecec38a3efa684568503aeaee80cf0d6f1e04256fc100ad988fd4cae94260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055f3fb82c3a0cf1d297cb7bcb589f7ba26be8f6a8fc10be0d61b1043bea6337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183f74a734df65feb2e2bd5e114968eaa7279f598b4ff88cd0bf1a597373c1f4(
    value: typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95283432c4211dfdf8e0b2459a0bafec123dc33d6100964d676e472577886b6c(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b53234a266bec037925c3d8b89a0270f4f70ebc91780024146f4aa147053c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f65a3780211f0ef7f0a3accfbf3a54fbeb99719173a5226d2b2eaaa81113a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ed81a3ff9de9666aa8adcfbd134158f5c3980a75924e2c3150b4ee05ad9de7(
    value: typing.Optional[ModelArmorTemplateFilterConfigSdpSettingsBasicConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1121ae76e56803986d5644dab10465bcbe6b8a211a8fa1453c576487984593a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0ce0eb976432a46ea846f5bf7b5296aaf1e88bd37a99b3eb11438ad34fb1ba(
    value: typing.Optional[ModelArmorTemplateFilterConfigSdpSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e111eef05dd6c06313a7fa027295a29acd244be58065bd4f5a3aa27d953ad2f(
    *,
    custom_llm_response_safety_error_code: typing.Optional[jsii.Number] = None,
    custom_llm_response_safety_error_message: typing.Optional[builtins.str] = None,
    custom_prompt_safety_error_code: typing.Optional[jsii.Number] = None,
    custom_prompt_safety_error_message: typing.Optional[builtins.str] = None,
    enforcement_type: typing.Optional[builtins.str] = None,
    ignore_partial_invocation_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_sanitize_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_template_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multi_language_detection: typing.Optional[typing.Union[ModelArmorTemplateTemplateMetadataMultiLanguageDetection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26075dd55aa8767436e7321700ae0f14834c761b5eaa944836666fef584a690(
    *,
    enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5284fa4360d5eb05ff0e080c804652de5e79ea3ed52798d1bd4bc1333caa9a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e19ae4acebdc30295168fda3ad12cc9b2c945b6caa334ff5e62b838fc69d4e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168c9c713f80f46ea23c8136412dfbaca6f31030ee9c65256ebcb5fad7d433fe(
    value: typing.Optional[ModelArmorTemplateTemplateMetadataMultiLanguageDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17cceab2fe548c8ee9d714becae3dbb37d0513d865d22e2ee293658ce5b2d23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d35da850ef3b83c7bbbb74ee16293408d0c8227560b2303922c74ff77072b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf820a1a2962c1eac57eff2010210077435672c10539569b162e7896d20d765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5b9114aa442daf6caf12607929b79e4f97906a73585a396740a4c1b2e85730(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e86c0c28f39e9beb7525762e39ef7d1918a263128bd6110481f85f9a48e070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb61d1cfba0ea22cdacbf7bb0c90587adf54ad788f4da2578112c1bf64a5c90d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eeedd14401178f2afde67496d20666e5c673157901f9693ee86c1565c4eee52(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c0f5b0c6c7ae8bc2fb93c4ea04baf6783b9ac68f5b51c48d7d50ac4148fb4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4c72ba0f765728f2ff787e0176d81182c96c8987ab828b4ab72e7802a7a540(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962ec031c1183423ff7c91d03a280a5639443b384961936186c066a80ed6112f(
    value: typing.Optional[ModelArmorTemplateTemplateMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae19ba67b027a28e9173fb83bfe5dea06a0b5fb22fdc0e5906e738b7bb92b3d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251a2fa8fc2920e313e95e4c5ecfb4d1f96a5cb0d5da44c164662d89eb3114e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b195a00320989f11b15d802dcb872d1e27eb8ec186d3f6afb5a2da5d244f743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308e90b57ba9efe387d350953ea9288096c3e17a8eb8a2161b406ea141e000b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc2102936be5112ad13cfdba707dc348509496552759593f45dbe08d7410207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f6de870359d0f95b6566b7d6efb1ca388569c7c3d25bfeeb020949c99d5abf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
