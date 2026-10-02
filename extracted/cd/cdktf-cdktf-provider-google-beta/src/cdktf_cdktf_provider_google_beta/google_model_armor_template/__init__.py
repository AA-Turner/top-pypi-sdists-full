r'''
# `google_model_armor_template`

Refer to the Terraform Registry for docs: [`google_model_armor_template`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template).
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


class GoogleModelArmorTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template google_model_armor_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter_config: typing.Union["GoogleModelArmorTemplateFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        template_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_metadata: typing.Optional[typing.Union["GoogleModelArmorTemplateTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleModelArmorTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template google_model_armor_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_config GoogleModelArmorTemplate#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#location GoogleModelArmorTemplate#location}
        :param template_id: Id of the requesting object If auto-generating Id server-side, remove this field and template_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#template_id GoogleModelArmorTemplate#template_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#id GoogleModelArmorTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#labels GoogleModelArmorTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#project GoogleModelArmorTemplate#project}.
        :param template_metadata: template_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#template_metadata GoogleModelArmorTemplate#template_metadata}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#timeouts GoogleModelArmorTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec51ea42dffd4149db28f140be7ec1dddc6cdd450576339a6abc6415d655a573)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleModelArmorTemplateConfig(
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
        '''Generates CDKTF code for importing a GoogleModelArmorTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleModelArmorTemplate to import.
        :param import_from_id: The id of the existing GoogleModelArmorTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleModelArmorTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de75158d67ada3ba29a73e2ce83e7289c52de82cc2d9692b967ab3d16c0606a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilterConfig")
    def put_filter_config(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#malicious_uri_filter_settings GoogleModelArmorTemplate#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#pi_and_jailbreak_filter_settings GoogleModelArmorTemplate#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#rai_settings GoogleModelArmorTemplate#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#sdp_settings GoogleModelArmorTemplate#sdp_settings}
        '''
        value = GoogleModelArmorTemplateFilterConfig(
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
        multi_language_detection: typing.Optional[typing.Union["GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_llm_response_safety_error_code: Indicates the custom error code set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_llm_response_safety_error_code GoogleModelArmorTemplate#custom_llm_response_safety_error_code}
        :param custom_llm_response_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_llm_response_safety_error_message GoogleModelArmorTemplate#custom_llm_response_safety_error_message}
        :param custom_prompt_safety_error_code: Indicates the custom error code set by the user to be returned to the end user by the service extension if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_prompt_safety_error_code GoogleModelArmorTemplate#custom_prompt_safety_error_code}
        :param custom_prompt_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_prompt_safety_error_message GoogleModelArmorTemplate#custom_prompt_safety_error_message}
        :param enforcement_type: Possible values: INSPECT_ONLY INSPECT_AND_BLOCK. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#enforcement_type GoogleModelArmorTemplate#enforcement_type}
        :param ignore_partial_invocation_failures: If true, partial detector failures should be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#ignore_partial_invocation_failures GoogleModelArmorTemplate#ignore_partial_invocation_failures}
        :param log_sanitize_operations: If true, log sanitize operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#log_sanitize_operations GoogleModelArmorTemplate#log_sanitize_operations}
        :param log_template_operations: If true, log template crud operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#log_template_operations GoogleModelArmorTemplate#log_template_operations}
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#multi_language_detection GoogleModelArmorTemplate#multi_language_detection}
        '''
        value = GoogleModelArmorTemplateTemplateMetadata(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#create GoogleModelArmorTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#delete GoogleModelArmorTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#update GoogleModelArmorTemplate#update}.
        '''
        value = GoogleModelArmorTemplateTimeouts(
            create=create, delete=delete, update=update
        )

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
    def filter_config(self) -> "GoogleModelArmorTemplateFilterConfigOutputReference":
        return typing.cast("GoogleModelArmorTemplateFilterConfigOutputReference", jsii.get(self, "filterConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="templateMetadata")
    def template_metadata(
        self,
    ) -> "GoogleModelArmorTemplateTemplateMetadataOutputReference":
        return typing.cast("GoogleModelArmorTemplateTemplateMetadataOutputReference", jsii.get(self, "templateMetadata"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleModelArmorTemplateTimeoutsOutputReference":
        return typing.cast("GoogleModelArmorTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="filterConfigInput")
    def filter_config_input(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfig"]:
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfig"], jsii.get(self, "filterConfigInput"))

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
    ) -> typing.Optional["GoogleModelArmorTemplateTemplateMetadata"]:
        return typing.cast(typing.Optional["GoogleModelArmorTemplateTemplateMetadata"], jsii.get(self, "templateMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleModelArmorTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleModelArmorTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a265dad69752736665fda46304bdffe3b7c8fa981917938064bae1ca3760033e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de94b95b02509b67b21826d0a32ec20fb3e4c9f655f272f07643dbe64f6e027b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae6660924925dca8b170f7c645e8378dfa3b9d6eebee5317ca4230735bd8233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e7ee4a0eb2b577bcc227af5298ac14ced3de6aa015ad41057b49e3a78bfdb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateId"))

    @template_id.setter
    def template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab44ab7d8d2a32b00b31746d5a9f02b920450b58b812c942e0ac31f36203f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateConfig",
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
class GoogleModelArmorTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter_config: typing.Union["GoogleModelArmorTemplateFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        template_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        template_metadata: typing.Optional[typing.Union["GoogleModelArmorTemplateTemplateMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleModelArmorTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_config GoogleModelArmorTemplate#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#location GoogleModelArmorTemplate#location}
        :param template_id: Id of the requesting object If auto-generating Id server-side, remove this field and template_id from the method_signature of Create RPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#template_id GoogleModelArmorTemplate#template_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#id GoogleModelArmorTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#labels GoogleModelArmorTemplate#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#project GoogleModelArmorTemplate#project}.
        :param template_metadata: template_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#template_metadata GoogleModelArmorTemplate#template_metadata}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#timeouts GoogleModelArmorTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter_config, dict):
            filter_config = GoogleModelArmorTemplateFilterConfig(**filter_config)
        if isinstance(template_metadata, dict):
            template_metadata = GoogleModelArmorTemplateTemplateMetadata(**template_metadata)
        if isinstance(timeouts, dict):
            timeouts = GoogleModelArmorTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a189481b6d78b001bb3330c9684b74f10178b9d639baf8f043452d41fd655c3)
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
    def filter_config(self) -> "GoogleModelArmorTemplateFilterConfig":
        '''filter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_config GoogleModelArmorTemplate#filter_config}
        '''
        result = self._values.get("filter_config")
        assert result is not None, "Required property 'filter_config' is missing"
        return typing.cast("GoogleModelArmorTemplateFilterConfig", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#location GoogleModelArmorTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_id(self) -> builtins.str:
        '''Id of the requesting object If auto-generating Id server-side, remove this field and template_id from the method_signature of Create RPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#template_id GoogleModelArmorTemplate#template_id}
        '''
        result = self._values.get("template_id")
        assert result is not None, "Required property 'template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#id GoogleModelArmorTemplate#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#labels GoogleModelArmorTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#project GoogleModelArmorTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_metadata(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateTemplateMetadata"]:
        '''template_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#template_metadata GoogleModelArmorTemplate#template_metadata}
        '''
        result = self._values.get("template_metadata")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateTemplateMetadata"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleModelArmorTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#timeouts GoogleModelArmorTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "malicious_uri_filter_settings": "maliciousUriFilterSettings",
        "pi_and_jailbreak_filter_settings": "piAndJailbreakFilterSettings",
        "rai_settings": "raiSettings",
        "sdp_settings": "sdpSettings",
    },
)
class GoogleModelArmorTemplateFilterConfig:
    def __init__(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#malicious_uri_filter_settings GoogleModelArmorTemplate#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#pi_and_jailbreak_filter_settings GoogleModelArmorTemplate#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#rai_settings GoogleModelArmorTemplate#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#sdp_settings GoogleModelArmorTemplate#sdp_settings}
        '''
        if isinstance(malicious_uri_filter_settings, dict):
            malicious_uri_filter_settings = GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings(**malicious_uri_filter_settings)
        if isinstance(pi_and_jailbreak_filter_settings, dict):
            pi_and_jailbreak_filter_settings = GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings(**pi_and_jailbreak_filter_settings)
        if isinstance(rai_settings, dict):
            rai_settings = GoogleModelArmorTemplateFilterConfigRaiSettings(**rai_settings)
        if isinstance(sdp_settings, dict):
            sdp_settings = GoogleModelArmorTemplateFilterConfigSdpSettings(**sdp_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8546d9ca5d11f89670250db5b6f0542c3da0adfdfa219dd6352804d5672bb2c)
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
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings"]:
        '''malicious_uri_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#malicious_uri_filter_settings GoogleModelArmorTemplate#malicious_uri_filter_settings}
        '''
        result = self._values.get("malicious_uri_filter_settings")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings"], result)

    @builtins.property
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"]:
        '''pi_and_jailbreak_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#pi_and_jailbreak_filter_settings GoogleModelArmorTemplate#pi_and_jailbreak_filter_settings}
        '''
        result = self._values.get("pi_and_jailbreak_filter_settings")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"], result)

    @builtins.property
    def rai_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigRaiSettings"]:
        '''rai_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#rai_settings GoogleModelArmorTemplate#rai_settings}
        '''
        result = self._values.get("rai_settings")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigRaiSettings"], result)

    @builtins.property
    def sdp_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettings"]:
        '''sdp_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#sdp_settings GoogleModelArmorTemplate#sdp_settings}
        '''
        result = self._values.get("sdp_settings")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a35495d46e47b491d79486a8a32a96816c717fbfa1586a376f0eb7372fb9445)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbba41120a7064d172e0947c3e2953466f2b470f0720ea1bb4d067fe81bb478b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c84d651471539397e331a19ad4a38568c1def6fb4f5e42cbd80eae2e6e3fb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b4d6ff80dd1e9cd146140019f1faff633f330308ed076d2843bdbdffccbbf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorTemplateFilterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85ba790f0c6788d53d557c96dd35f4616fa53595f931fc5552bfa1b5d79abc7e)
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
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        value = GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings(
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
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#confidence_level GoogleModelArmorTemplate#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        value = GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings(
            confidence_level=confidence_level, filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putPiAndJailbreakFilterSettings", [value]))

    @jsii.member(jsii_name="putRaiSettings")
    def put_rai_settings(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#rai_filters GoogleModelArmorTemplate#rai_filters}
        '''
        value = GoogleModelArmorTemplateFilterConfigRaiSettings(
            rai_filters=rai_filters
        )

        return typing.cast(None, jsii.invoke(self, "putRaiSettings", [value]))

    @jsii.member(jsii_name="putSdpSettings")
    def put_sdp_settings(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#advanced_config GoogleModelArmorTemplate#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#basic_config GoogleModelArmorTemplate#basic_config}
        '''
        value = GoogleModelArmorTemplateFilterConfigSdpSettings(
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
    ) -> GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference:
        return typing.cast(GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference, jsii.get(self, "maliciousUriFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettings")
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> "GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference":
        return typing.cast("GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference", jsii.get(self, "piAndJailbreakFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="raiSettings")
    def rai_settings(
        self,
    ) -> "GoogleModelArmorTemplateFilterConfigRaiSettingsOutputReference":
        return typing.cast("GoogleModelArmorTemplateFilterConfigRaiSettingsOutputReference", jsii.get(self, "raiSettings"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettings")
    def sdp_settings(
        self,
    ) -> "GoogleModelArmorTemplateFilterConfigSdpSettingsOutputReference":
        return typing.cast("GoogleModelArmorTemplateFilterConfigSdpSettingsOutputReference", jsii.get(self, "sdpSettings"))

    @builtins.property
    @jsii.member(jsii_name="maliciousUriFilterSettingsInput")
    def malicious_uri_filter_settings_input(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings], jsii.get(self, "maliciousUriFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettingsInput")
    def pi_and_jailbreak_filter_settings_input(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"]:
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings"], jsii.get(self, "piAndJailbreakFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="raiSettingsInput")
    def rai_settings_input(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigRaiSettings"]:
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigRaiSettings"], jsii.get(self, "raiSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettingsInput")
    def sdp_settings_input(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettings"]:
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettings"], jsii.get(self, "sdpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleModelArmorTemplateFilterConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9196367d32fcd43053b3322d1b6dc8c24d8bfb6f356db2f3415653cbd112eddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_level": "confidenceLevel",
        "filter_enforcement": "filterEnforcement",
    },
)
class GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings:
    def __init__(
        self,
        *,
        confidence_level: typing.Optional[builtins.str] = None,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#confidence_level GoogleModelArmorTemplate#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7844d71e141496598b148e581bc192d3cc3693022e1fba22d979106d941a24de)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#confidence_level GoogleModelArmorTemplate#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d41f318bd1514083cf0e2d0190f8876f46b1b08e360834a4d5363620dcf5025)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d226b53db982413fcade25e188b3fe63f1386d2a53c44abbf6c4e6c2b7cfcbae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65c48bbb4aec98f0b44914ab0b8aab5c1ea682344e90afa70760b3f92505a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632cd7f12789aa3c862f52b54fc599c87966c42ac20d7eacb34995bbbf1746fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigRaiSettings",
    jsii_struct_bases=[],
    name_mapping={"rai_filters": "raiFilters"},
)
class GoogleModelArmorTemplateFilterConfigRaiSettings:
    def __init__(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#rai_filters GoogleModelArmorTemplate#rai_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6590076d54e3af88177396110532fd90f76a645a1d72bb5ef8a6a282fdd93ca)
            check_type(argname="argument rai_filters", value=rai_filters, expected_type=type_hints["rai_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rai_filters": rai_filters,
        }

    @builtins.property
    def rai_filters(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]]:
        '''rai_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#rai_filters GoogleModelArmorTemplate#rai_filters}
        '''
        result = self._values.get("rai_filters")
        assert result is not None, "Required property 'rai_filters' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigRaiSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateFilterConfigRaiSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigRaiSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ddd8369a651a223f48b7979fe9ee161ac6b4ae72653482ef9d4ce4c906e3f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRaiFilters")
    def put_rai_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd8485c77682cbb02d5a9882b20f6afc6296b95524fcaf01d543439319efd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRaiFilters", [value]))

    @builtins.property
    @jsii.member(jsii_name="raiFilters")
    def rai_filters(
        self,
    ) -> "GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList":
        return typing.cast("GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList", jsii.get(self, "raiFilters"))

    @builtins.property
    @jsii.member(jsii_name="raiFiltersInput")
    def rai_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters"]]], jsii.get(self, "raiFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigRaiSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigRaiSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfigRaiSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc98410f3457acafc99ac295d4d36a8eda08c45bc329a11d6d45bdd09e43469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters",
    jsii_struct_bases=[],
    name_mapping={"filter_type": "filterType", "confidence_level": "confidenceLevel"},
)
class GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters:
    def __init__(
        self,
        *,
        filter_type: builtins.str,
        confidence_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_type: Possible values: SEXUALLY_EXPLICIT HATE_SPEECH HARASSMENT DANGEROUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_type GoogleModelArmorTemplate#filter_type}
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#confidence_level GoogleModelArmorTemplate#confidence_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb5935f435d6152ff511e89309cbf63fee933443dd145e104a72ed1f3f56b9c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_type GoogleModelArmorTemplate#filter_type}
        '''
        result = self._values.get("filter_type")
        assert result is not None, "Required property 'filter_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confidence_level(self) -> typing.Optional[builtins.str]:
        '''Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#confidence_level GoogleModelArmorTemplate#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a90a75e7510ef5be23bd3f1b081e60511c1118b9f1508c70086aa814e9f70c6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96c219f2d44d691a9ee03a90ff17d22e366fdf93b5a2595c99b90fd3eab517a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76373083c3140d58e1f1bf8905bc9cab72df11cdae99b18f472faae6d5dce465)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7828e94680c9d75a87f3c0a667456666a40f503d2006a08dd428ad889f52199d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bab73b1c546bfddadab6a560b740bc50b1ca97fe3a5f606f805150ba3c55856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b0b6fe6fbe19caa264bec9265781bde7dd35ed78ea4f4c01083c9393fff4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d2f515da245cbe5cceb29e4d97a9c52ceb9ca455fa6669e2ac61d1110c8183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ec471b02d5b22f9010d4206603356893c3acdc4b0cbc2f848703c173d0f718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @filter_type.setter
    def filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5900212e31f8abb7183369440c2a0d49befd1fe172c9b99361a91ca1170a7de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b8e23f606132a80fbff34725209755d6151d6bab420d377c92e8a16c0ddea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigSdpSettings",
    jsii_struct_bases=[],
    name_mapping={"advanced_config": "advancedConfig", "basic_config": "basicConfig"},
)
class GoogleModelArmorTemplateFilterConfigSdpSettings:
    def __init__(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#advanced_config GoogleModelArmorTemplate#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#basic_config GoogleModelArmorTemplate#basic_config}
        '''
        if isinstance(advanced_config, dict):
            advanced_config = GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig(**advanced_config)
        if isinstance(basic_config, dict):
            basic_config = GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig(**basic_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebde85d9d677547e8155166922ed4cce94782f0ee8b3b47a969e446b270c25c1)
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
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig"]:
        '''advanced_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#advanced_config GoogleModelArmorTemplate#advanced_config}
        '''
        result = self._values.get("advanced_config")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig"], result)

    @builtins.property
    def basic_config(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig"]:
        '''basic_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#basic_config GoogleModelArmorTemplate#basic_config}
        '''
        result = self._values.get("basic_config")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigSdpSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify_template": "deidentifyTemplate",
        "inspect_template": "inspectTemplate",
    },
)
class GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig:
    def __init__(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        inspect_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#deidentify_template GoogleModelArmorTemplate#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#inspect_template GoogleModelArmorTemplate#inspect_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c09f42f7e3d25db9ca03ff9c32b0a243a8ba87ae96362da5aea790f930b808)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#deidentify_template GoogleModelArmorTemplate#deidentify_template}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#inspect_template GoogleModelArmorTemplate#inspect_template}
        '''
        result = self._values.get("inspect_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb82ce4695a0b57ef42c5db59e1efb42e6290ab2675d439c12791451911968e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__024af4640a1c06f635a78cf7e6942c359bd5118bde1dc967f31b2076c900bf0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplate")
    def inspect_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplate"))

    @inspect_template.setter
    def inspect_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6506fad5c8e0ce3474e056677e247efb81acf01136e7e3bf8e1824928d50b448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be12721574931b4d2343ac74dffc25792f338e80e1e7cf95b5141c2e8eb63fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3bec5d2b0b09496c2a66f70b6b3428d8bf507ca582677f552e9e33454e5f98)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6e9d37abfccf1fbb6a9089cee9b576746b7f0aba261c74c1459c0a3fb0dcadb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58ef019ca8b504cc493210a319ea5816b67283706bf29d04839956e1f91305ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cae263e7a0fc0c5cd3e298b72a854db9313e21d2839294f4bdf41929b65c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorTemplateFilterConfigSdpSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateFilterConfigSdpSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c060a1ed0e273d13bbdd6997621431e91dca17cbd5bc09dc703b857303726221)
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
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#deidentify_template GoogleModelArmorTemplate#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#inspect_template GoogleModelArmorTemplate#inspect_template}
        '''
        value = GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig(
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
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#filter_enforcement GoogleModelArmorTemplate#filter_enforcement}
        '''
        value = GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig(
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
    ) -> GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference:
        return typing.cast(GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference, jsii.get(self, "advancedConfig"))

    @builtins.property
    @jsii.member(jsii_name="basicConfig")
    def basic_config(
        self,
    ) -> GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference:
        return typing.cast(GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference, jsii.get(self, "basicConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedConfigInput")
    def advanced_config_input(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "advancedConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="basicConfigInput")
    def basic_config_input(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig], jsii.get(self, "basicConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfe562f15355c8d7058397ccbc66078981a306aa7804c13f93034a66958fa5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateTemplateMetadata",
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
class GoogleModelArmorTemplateTemplateMetadata:
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
        multi_language_detection: typing.Optional[typing.Union["GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_llm_response_safety_error_code: Indicates the custom error code set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_llm_response_safety_error_code GoogleModelArmorTemplate#custom_llm_response_safety_error_code}
        :param custom_llm_response_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the LLM response trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_llm_response_safety_error_message GoogleModelArmorTemplate#custom_llm_response_safety_error_message}
        :param custom_prompt_safety_error_code: Indicates the custom error code set by the user to be returned to the end user by the service extension if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_prompt_safety_error_code GoogleModelArmorTemplate#custom_prompt_safety_error_code}
        :param custom_prompt_safety_error_message: Indicates the custom error message set by the user to be returned to the end user if the prompt trips Model Armor filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_prompt_safety_error_message GoogleModelArmorTemplate#custom_prompt_safety_error_message}
        :param enforcement_type: Possible values: INSPECT_ONLY INSPECT_AND_BLOCK. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#enforcement_type GoogleModelArmorTemplate#enforcement_type}
        :param ignore_partial_invocation_failures: If true, partial detector failures should be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#ignore_partial_invocation_failures GoogleModelArmorTemplate#ignore_partial_invocation_failures}
        :param log_sanitize_operations: If true, log sanitize operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#log_sanitize_operations GoogleModelArmorTemplate#log_sanitize_operations}
        :param log_template_operations: If true, log template crud operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#log_template_operations GoogleModelArmorTemplate#log_template_operations}
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#multi_language_detection GoogleModelArmorTemplate#multi_language_detection}
        '''
        if isinstance(multi_language_detection, dict):
            multi_language_detection = GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection(**multi_language_detection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826db4594cda72b8bab25e2e20fc73c4c9a525ad02a3d69845916d062fa365d0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_llm_response_safety_error_code GoogleModelArmorTemplate#custom_llm_response_safety_error_code}
        '''
        result = self._values.get("custom_llm_response_safety_error_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_llm_response_safety_error_message(self) -> typing.Optional[builtins.str]:
        '''Indicates the custom error message set by the user to be returned to the end user if the LLM response trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_llm_response_safety_error_message GoogleModelArmorTemplate#custom_llm_response_safety_error_message}
        '''
        result = self._values.get("custom_llm_response_safety_error_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_prompt_safety_error_code(self) -> typing.Optional[jsii.Number]:
        '''Indicates the custom error code set by the user to be returned to the end user by the service extension if the prompt trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_prompt_safety_error_code GoogleModelArmorTemplate#custom_prompt_safety_error_code}
        '''
        result = self._values.get("custom_prompt_safety_error_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_prompt_safety_error_message(self) -> typing.Optional[builtins.str]:
        '''Indicates the custom error message set by the user to be returned to the end user if the prompt trips Model Armor filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#custom_prompt_safety_error_message GoogleModelArmorTemplate#custom_prompt_safety_error_message}
        '''
        result = self._values.get("custom_prompt_safety_error_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforcement_type(self) -> typing.Optional[builtins.str]:
        '''Possible values: INSPECT_ONLY INSPECT_AND_BLOCK.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#enforcement_type GoogleModelArmorTemplate#enforcement_type}
        '''
        result = self._values.get("enforcement_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_partial_invocation_failures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, partial detector failures should be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#ignore_partial_invocation_failures GoogleModelArmorTemplate#ignore_partial_invocation_failures}
        '''
        result = self._values.get("ignore_partial_invocation_failures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_sanitize_operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, log sanitize operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#log_sanitize_operations GoogleModelArmorTemplate#log_sanitize_operations}
        '''
        result = self._values.get("log_sanitize_operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_template_operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, log template crud operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#log_template_operations GoogleModelArmorTemplate#log_template_operations}
        '''
        result = self._values.get("log_template_operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def multi_language_detection(
        self,
    ) -> typing.Optional["GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection"]:
        '''multi_language_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#multi_language_detection GoogleModelArmorTemplate#multi_language_detection}
        '''
        result = self._values.get("multi_language_detection")
        return typing.cast(typing.Optional["GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateTemplateMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection",
    jsii_struct_bases=[],
    name_mapping={"enable_multi_language_detection": "enableMultiLanguageDetection"},
)
class GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection:
    def __init__(
        self,
        *,
        enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#enable_multi_language_detection GoogleModelArmorTemplate#enable_multi_language_detection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ff4102d5246bb85fd002264ac288790eb89c6d6d3007daede7ef4828fa0994)
            check_type(argname="argument enable_multi_language_detection", value=enable_multi_language_detection, expected_type=type_hints["enable_multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_multi_language_detection": enable_multi_language_detection,
        }

    @builtins.property
    def enable_multi_language_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, multi language detection will be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#enable_multi_language_detection GoogleModelArmorTemplate#enable_multi_language_detection}
        '''
        result = self._values.get("enable_multi_language_detection")
        assert result is not None, "Required property 'enable_multi_language_detection' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67c5136d7f0a29bcd13c3538a43440930cdde2f93ecc30377c9fc12dd3e9696e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17c98d350be60e8be91415eef576c626201108da4b905cd0c0be8a1ce8e76e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMultiLanguageDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f68c7cabc7194295c5e58f47a616c6d2ff9a4775e8d97fb005ce008e72c7689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorTemplateTemplateMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateTemplateMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e26b755d381b3dad383d674234879b41fd67dccf1885d0b8acf78286d9df74de)
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
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#enable_multi_language_detection GoogleModelArmorTemplate#enable_multi_language_detection}
        '''
        value = GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection(
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
    ) -> GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference:
        return typing.cast(GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference, jsii.get(self, "multiLanguageDetection"))

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
    ) -> typing.Optional[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection], jsii.get(self, "multiLanguageDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="customLlmResponseSafetyErrorCode")
    def custom_llm_response_safety_error_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customLlmResponseSafetyErrorCode"))

    @custom_llm_response_safety_error_code.setter
    def custom_llm_response_safety_error_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb401e93023a9369897e15e7970ef0d0560dbd76521129091a701b96df3241a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLlmResponseSafetyErrorCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customLlmResponseSafetyErrorMessage")
    def custom_llm_response_safety_error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLlmResponseSafetyErrorMessage"))

    @custom_llm_response_safety_error_message.setter
    def custom_llm_response_safety_error_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347b2e54a4a0866d9a9970ea2a943e0fd3cd6765a5b2b34c0a2473032df3dd2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLlmResponseSafetyErrorMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPromptSafetyErrorCode")
    def custom_prompt_safety_error_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customPromptSafetyErrorCode"))

    @custom_prompt_safety_error_code.setter
    def custom_prompt_safety_error_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f7f933dfcfdeb2a1cfa8e001bed0a462a6f8650a07966ea2fa96b6854b7540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPromptSafetyErrorCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPromptSafetyErrorMessage")
    def custom_prompt_safety_error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customPromptSafetyErrorMessage"))

    @custom_prompt_safety_error_message.setter
    def custom_prompt_safety_error_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784943f67e562293f54cd0f013ee694b04b69a848f80fe18b77a1be85d67b872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPromptSafetyErrorMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforcementType")
    def enforcement_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementType"))

    @enforcement_type.setter
    def enforcement_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38daf0552b37f90c93db0fffedd947cdf4fb5c397865638a06c1ab060fd3d837)
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
            type_hints = typing.get_type_hints(_typecheckingstub__056661847f03282647f92e4238394de2baf92e5c07478604642164141525ab1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00802eee31c36708ef851ca3dbff097ca9695429b99dccd13d265a8a57813d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d684ddef3c219d2fa4fe2556662a6d9cab4dac03c7e9959a42d9bdda70e3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTemplateOperations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorTemplateTemplateMetadata]:
        return typing.cast(typing.Optional[GoogleModelArmorTemplateTemplateMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorTemplateTemplateMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9083d144b64194d0a8f6bacb31b893c907030d01b89e257412d51cfdfada93b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleModelArmorTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#create GoogleModelArmorTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#delete GoogleModelArmorTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#update GoogleModelArmorTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a411da3640ccea20dcc51aeff9d2d4930f3de66f95f14cd903a28fd420525876)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#create GoogleModelArmorTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#delete GoogleModelArmorTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_template#update GoogleModelArmorTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorTemplate.GoogleModelArmorTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d24159987ce742d2ab61749b6d15a76f378c52323c352128847b306817c194e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba22b259b3eb6f8904e4e427729c44a255f7555fcb8af206c4a27ffa72399aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f150c46b4a612121f08729a1d19552e964c74203a401d5e90ea41f8b6e16b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803c8dbe1270216ea09ca09d31503c1dbb942c2b12ca85d1e74b097902a1faed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db06588704608c83243eb7330f884f06b0a4490940394ade6f843219a94619a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleModelArmorTemplate",
    "GoogleModelArmorTemplateConfig",
    "GoogleModelArmorTemplateFilterConfig",
    "GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings",
    "GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettingsOutputReference",
    "GoogleModelArmorTemplateFilterConfigOutputReference",
    "GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings",
    "GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettingsOutputReference",
    "GoogleModelArmorTemplateFilterConfigRaiSettings",
    "GoogleModelArmorTemplateFilterConfigRaiSettingsOutputReference",
    "GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters",
    "GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersList",
    "GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFiltersOutputReference",
    "GoogleModelArmorTemplateFilterConfigSdpSettings",
    "GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig",
    "GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfigOutputReference",
    "GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig",
    "GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfigOutputReference",
    "GoogleModelArmorTemplateFilterConfigSdpSettingsOutputReference",
    "GoogleModelArmorTemplateTemplateMetadata",
    "GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection",
    "GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetectionOutputReference",
    "GoogleModelArmorTemplateTemplateMetadataOutputReference",
    "GoogleModelArmorTemplateTimeouts",
    "GoogleModelArmorTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ec51ea42dffd4149db28f140be7ec1dddc6cdd450576339a6abc6415d655a573(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter_config: typing.Union[GoogleModelArmorTemplateFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    template_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_metadata: typing.Optional[typing.Union[GoogleModelArmorTemplateTemplateMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleModelArmorTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__de75158d67ada3ba29a73e2ce83e7289c52de82cc2d9692b967ab3d16c0606a0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a265dad69752736665fda46304bdffe3b7c8fa981917938064bae1ca3760033e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de94b95b02509b67b21826d0a32ec20fb3e4c9f655f272f07643dbe64f6e027b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae6660924925dca8b170f7c645e8378dfa3b9d6eebee5317ca4230735bd8233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e7ee4a0eb2b577bcc227af5298ac14ced3de6aa015ad41057b49e3a78bfdb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab44ab7d8d2a32b00b31746d5a9f02b920450b58b812c942e0ac31f36203f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a189481b6d78b001bb3330c9684b74f10178b9d639baf8f043452d41fd655c3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter_config: typing.Union[GoogleModelArmorTemplateFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    template_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    template_metadata: typing.Optional[typing.Union[GoogleModelArmorTemplateTemplateMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleModelArmorTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8546d9ca5d11f89670250db5b6f0542c3da0adfdfa219dd6352804d5672bb2c(
    *,
    malicious_uri_filter_settings: typing.Optional[typing.Union[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    pi_and_jailbreak_filter_settings: typing.Optional[typing.Union[GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    rai_settings: typing.Optional[typing.Union[GoogleModelArmorTemplateFilterConfigRaiSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    sdp_settings: typing.Optional[typing.Union[GoogleModelArmorTemplateFilterConfigSdpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a35495d46e47b491d79486a8a32a96816c717fbfa1586a376f0eb7372fb9445(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbba41120a7064d172e0947c3e2953466f2b470f0720ea1bb4d067fe81bb478b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c84d651471539397e331a19ad4a38568c1def6fb4f5e42cbd80eae2e6e3fb31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b4d6ff80dd1e9cd146140019f1faff633f330308ed076d2843bdbdffccbbf7(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfigMaliciousUriFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ba790f0c6788d53d557c96dd35f4616fa53595f931fc5552bfa1b5d79abc7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9196367d32fcd43053b3322d1b6dc8c24d8bfb6f356db2f3415653cbd112eddb(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7844d71e141496598b148e581bc192d3cc3693022e1fba22d979106d941a24de(
    *,
    confidence_level: typing.Optional[builtins.str] = None,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d41f318bd1514083cf0e2d0190f8876f46b1b08e360834a4d5363620dcf5025(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d226b53db982413fcade25e188b3fe63f1386d2a53c44abbf6c4e6c2b7cfcbae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65c48bbb4aec98f0b44914ab0b8aab5c1ea682344e90afa70760b3f92505a02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632cd7f12789aa3c862f52b54fc599c87966c42ac20d7eacb34995bbbf1746fc(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfigPiAndJailbreakFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6590076d54e3af88177396110532fd90f76a645a1d72bb5ef8a6a282fdd93ca(
    *,
    rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ddd8369a651a223f48b7979fe9ee161ac6b4ae72653482ef9d4ce4c906e3f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd8485c77682cbb02d5a9882b20f6afc6296b95524fcaf01d543439319efd0d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc98410f3457acafc99ac295d4d36a8eda08c45bc329a11d6d45bdd09e43469(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfigRaiSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb5935f435d6152ff511e89309cbf63fee933443dd145e104a72ed1f3f56b9c(
    *,
    filter_type: builtins.str,
    confidence_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90a75e7510ef5be23bd3f1b081e60511c1118b9f1508c70086aa814e9f70c6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96c219f2d44d691a9ee03a90ff17d22e366fdf93b5a2595c99b90fd3eab517a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76373083c3140d58e1f1bf8905bc9cab72df11cdae99b18f472faae6d5dce465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7828e94680c9d75a87f3c0a667456666a40f503d2006a08dd428ad889f52199d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bab73b1c546bfddadab6a560b740bc50b1ca97fe3a5f606f805150ba3c55856(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b0b6fe6fbe19caa264bec9265781bde7dd35ed78ea4f4c01083c9393fff4a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d2f515da245cbe5cceb29e4d97a9c52ceb9ca455fa6669e2ac61d1110c8183(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ec471b02d5b22f9010d4206603356893c3acdc4b0cbc2f848703c173d0f718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5900212e31f8abb7183369440c2a0d49befd1fe172c9b99361a91ca1170a7de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b8e23f606132a80fbff34725209755d6151d6bab420d377c92e8a16c0ddea7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateFilterConfigRaiSettingsRaiFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebde85d9d677547e8155166922ed4cce94782f0ee8b3b47a969e446b270c25c1(
    *,
    advanced_config: typing.Optional[typing.Union[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_config: typing.Optional[typing.Union[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c09f42f7e3d25db9ca03ff9c32b0a243a8ba87ae96362da5aea790f930b808(
    *,
    deidentify_template: typing.Optional[builtins.str] = None,
    inspect_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb82ce4695a0b57ef42c5db59e1efb42e6290ab2675d439c12791451911968e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024af4640a1c06f635a78cf7e6942c359bd5118bde1dc967f31b2076c900bf0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6506fad5c8e0ce3474e056677e247efb81acf01136e7e3bf8e1824928d50b448(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be12721574931b4d2343ac74dffc25792f338e80e1e7cf95b5141c2e8eb63fb(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsAdvancedConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3bec5d2b0b09496c2a66f70b6b3428d8bf507ca582677f552e9e33454e5f98(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e9d37abfccf1fbb6a9089cee9b576746b7f0aba261c74c1459c0a3fb0dcadb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ef019ca8b504cc493210a319ea5816b67283706bf29d04839956e1f91305ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cae263e7a0fc0c5cd3e298b72a854db9313e21d2839294f4bdf41929b65c01(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettingsBasicConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c060a1ed0e273d13bbdd6997621431e91dca17cbd5bc09dc703b857303726221(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfe562f15355c8d7058397ccbc66078981a306aa7804c13f93034a66958fa5b(
    value: typing.Optional[GoogleModelArmorTemplateFilterConfigSdpSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826db4594cda72b8bab25e2e20fc73c4c9a525ad02a3d69845916d062fa365d0(
    *,
    custom_llm_response_safety_error_code: typing.Optional[jsii.Number] = None,
    custom_llm_response_safety_error_message: typing.Optional[builtins.str] = None,
    custom_prompt_safety_error_code: typing.Optional[jsii.Number] = None,
    custom_prompt_safety_error_message: typing.Optional[builtins.str] = None,
    enforcement_type: typing.Optional[builtins.str] = None,
    ignore_partial_invocation_failures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_sanitize_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_template_operations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multi_language_detection: typing.Optional[typing.Union[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ff4102d5246bb85fd002264ac288790eb89c6d6d3007daede7ef4828fa0994(
    *,
    enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c5136d7f0a29bcd13c3538a43440930cdde2f93ecc30377c9fc12dd3e9696e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c98d350be60e8be91415eef576c626201108da4b905cd0c0be8a1ce8e76e57(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f68c7cabc7194295c5e58f47a616c6d2ff9a4775e8d97fb005ce008e72c7689(
    value: typing.Optional[GoogleModelArmorTemplateTemplateMetadataMultiLanguageDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26b755d381b3dad383d674234879b41fd67dccf1885d0b8acf78286d9df74de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb401e93023a9369897e15e7970ef0d0560dbd76521129091a701b96df3241a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347b2e54a4a0866d9a9970ea2a943e0fd3cd6765a5b2b34c0a2473032df3dd2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f7f933dfcfdeb2a1cfa8e001bed0a462a6f8650a07966ea2fa96b6854b7540(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784943f67e562293f54cd0f013ee694b04b69a848f80fe18b77a1be85d67b872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38daf0552b37f90c93db0fffedd947cdf4fb5c397865638a06c1ab060fd3d837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056661847f03282647f92e4238394de2baf92e5c07478604642164141525ab1d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00802eee31c36708ef851ca3dbff097ca9695429b99dccd13d265a8a57813d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d684ddef3c219d2fa4fe2556662a6d9cab4dac03c7e9959a42d9bdda70e3d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9083d144b64194d0a8f6bacb31b893c907030d01b89e257412d51cfdfada93b1(
    value: typing.Optional[GoogleModelArmorTemplateTemplateMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a411da3640ccea20dcc51aeff9d2d4930f3de66f95f14cd903a28fd420525876(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d24159987ce742d2ab61749b6d15a76f378c52323c352128847b306817c194e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba22b259b3eb6f8904e4e427729c44a255f7555fcb8af206c4a27ffa72399aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f150c46b4a612121f08729a1d19552e964c74203a401d5e90ea41f8b6e16b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803c8dbe1270216ea09ca09d31503c1dbb942c2b12ca85d1e74b097902a1faed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db06588704608c83243eb7330f884f06b0a4490940394ade6f843219a94619a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
