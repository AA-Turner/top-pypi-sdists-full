r'''
# `google_clouddeploy_automation`

Refer to the Terraform Registry for docs: [`google_clouddeploy_automation`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation).
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


class GoogleClouddeployAutomation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation google_clouddeploy_automation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        delivery_pipeline: builtins.str,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationRules", typing.Dict[builtins.str, typing.Any]]]],
        selector: typing.Union["GoogleClouddeployAutomationSelector", typing.Dict[builtins.str, typing.Any]],
        service_account: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployAutomationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation google_clouddeploy_automation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param delivery_pipeline: The delivery_pipeline for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#delivery_pipeline GoogleClouddeployAutomation#delivery_pipeline}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#location GoogleClouddeployAutomation#location}
        :param name: Name of the 'Automation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#name GoogleClouddeployAutomation#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#rules GoogleClouddeployAutomation#rules}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#selector GoogleClouddeployAutomation#selector}
        :param service_account: Required. Email address of the user-managed IAM service account that creates Cloud Deploy release and rollout resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#service_account GoogleClouddeployAutomation#service_account}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#annotations GoogleClouddeployAutomation#annotations}
        :param description: Optional. Description of the 'Automation'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#description GoogleClouddeployAutomation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#labels GoogleClouddeployAutomation#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#project GoogleClouddeployAutomation#project}.
        :param suspended: Optional. When Suspended, automation is deactivated from execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#suspended GoogleClouddeployAutomation#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#timeouts GoogleClouddeployAutomation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d56e6e797ed752a1201533b0a9b6d733ad865c5aa2df3661f218f8e98aeb7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleClouddeployAutomationConfig(
            delivery_pipeline=delivery_pipeline,
            location=location,
            name=name,
            rules=rules,
            selector=selector,
            service_account=service_account,
            annotations=annotations,
            description=description,
            id=id,
            labels=labels,
            project=project,
            suspended=suspended,
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
        '''Generates CDKTF code for importing a GoogleClouddeployAutomation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleClouddeployAutomation to import.
        :param import_from_id: The id of the existing GoogleClouddeployAutomation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleClouddeployAutomation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df2000a1b8422b9ba5183b15ca493634b11b27e7be406da05935a3cdceac0b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d86b79c5dc673bb8fb58c88b83ef0f9d014b35973258e621b764580a049a5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        *,
        targets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationSelectorTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#targets GoogleClouddeployAutomation#targets}
        '''
        value = GoogleClouddeployAutomationSelector(targets=targets)

        return typing.cast(None, jsii.invoke(self, "putSelector", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#create GoogleClouddeployAutomation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#delete GoogleClouddeployAutomation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#update GoogleClouddeployAutomation#update}.
        '''
        value = GoogleClouddeployAutomationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSuspended")
    def reset_suspended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspended", []))

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
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "GoogleClouddeployAutomationRulesList":
        return typing.cast("GoogleClouddeployAutomationRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "GoogleClouddeployAutomationSelectorOutputReference":
        return typing.cast("GoogleClouddeployAutomationSelectorOutputReference", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleClouddeployAutomationTimeoutsOutputReference":
        return typing.cast("GoogleClouddeployAutomationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryPipelineInput")
    def delivery_pipeline_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional["GoogleClouddeployAutomationSelector"]:
        return typing.cast(typing.Optional["GoogleClouddeployAutomationSelector"], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendedInput")
    def suspended_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suspendedInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployAutomationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployAutomationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b367d629a689d3173e8d9762799be6b4a091818f3573a5a1a1113ee3076ce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryPipeline")
    def delivery_pipeline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryPipeline"))

    @delivery_pipeline.setter
    def delivery_pipeline(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ad7d3d7f76654484641123901fc6876e6124230d8f32b0aa391bcf954e8a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryPipeline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8802c2a4e9d44d626c1df03e6ac181b19a09a324fb9c0b1c4077c74382f20b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b3739623cad3ce5490badd5ed5965d90f4ee0920075c95c749815503740b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9b7749994ebb7118ede9cc4f8bbd970b64a05fceb942b5e6a62e10e6bed7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ff6445a9332a500e1f8fbe34135b1184a4b4acecc16a7d3698b75eff49c736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dfe2517a78f3a31f70f86411625a0a66a88080b017cb529df9d3bd305baab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78ab66e6a2769359c3d9b56f88d83b1a8be745258e9c3fe98b1857f7f1ae08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07ab6a2718a3dca031d074023c889b36ee56305ecbb620bd528719c7c0ae98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspended")
    def suspended(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suspended"))

    @suspended.setter
    def suspended(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97364d2c0969369f11cf3b2a6d4c2dd0fde82100c8e4502c26d0d1725532194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "delivery_pipeline": "deliveryPipeline",
        "location": "location",
        "name": "name",
        "rules": "rules",
        "selector": "selector",
        "service_account": "serviceAccount",
        "annotations": "annotations",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "suspended": "suspended",
        "timeouts": "timeouts",
    },
)
class GoogleClouddeployAutomationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        delivery_pipeline: builtins.str,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationRules", typing.Dict[builtins.str, typing.Any]]]],
        selector: typing.Union["GoogleClouddeployAutomationSelector", typing.Dict[builtins.str, typing.Any]],
        service_account: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployAutomationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param delivery_pipeline: The delivery_pipeline for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#delivery_pipeline GoogleClouddeployAutomation#delivery_pipeline}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#location GoogleClouddeployAutomation#location}
        :param name: Name of the 'Automation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#name GoogleClouddeployAutomation#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#rules GoogleClouddeployAutomation#rules}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#selector GoogleClouddeployAutomation#selector}
        :param service_account: Required. Email address of the user-managed IAM service account that creates Cloud Deploy release and rollout resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#service_account GoogleClouddeployAutomation#service_account}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#annotations GoogleClouddeployAutomation#annotations}
        :param description: Optional. Description of the 'Automation'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#description GoogleClouddeployAutomation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#labels GoogleClouddeployAutomation#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#project GoogleClouddeployAutomation#project}.
        :param suspended: Optional. When Suspended, automation is deactivated from execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#suspended GoogleClouddeployAutomation#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#timeouts GoogleClouddeployAutomation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(selector, dict):
            selector = GoogleClouddeployAutomationSelector(**selector)
        if isinstance(timeouts, dict):
            timeouts = GoogleClouddeployAutomationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8923f77a4a01e94e4743f23627dec202502d72011f15aa8778403c4d132f6c82)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument delivery_pipeline", value=delivery_pipeline, expected_type=type_hints["delivery_pipeline"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_pipeline": delivery_pipeline,
            "location": location,
            "name": name,
            "rules": rules,
            "selector": selector,
            "service_account": service_account,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if suspended is not None:
            self._values["suspended"] = suspended
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
    def delivery_pipeline(self) -> builtins.str:
        '''The delivery_pipeline for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#delivery_pipeline GoogleClouddeployAutomation#delivery_pipeline}
        '''
        result = self._values.get("delivery_pipeline")
        assert result is not None, "Required property 'delivery_pipeline' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#location GoogleClouddeployAutomation#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the 'Automation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#name GoogleClouddeployAutomation#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#rules GoogleClouddeployAutomation#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRules"]], result)

    @builtins.property
    def selector(self) -> "GoogleClouddeployAutomationSelector":
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#selector GoogleClouddeployAutomation#selector}
        '''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast("GoogleClouddeployAutomationSelector", result)

    @builtins.property
    def service_account(self) -> builtins.str:
        '''Required. Email address of the user-managed IAM service account that creates Cloud Deploy release and rollout resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#service_account GoogleClouddeployAutomation#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#annotations GoogleClouddeployAutomation#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the 'Automation'. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#description GoogleClouddeployAutomation#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#labels GoogleClouddeployAutomation#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#project GoogleClouddeployAutomation#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When Suspended, automation is deactivated from execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#suspended GoogleClouddeployAutomation#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleClouddeployAutomationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#timeouts GoogleClouddeployAutomation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRules",
    jsii_struct_bases=[],
    name_mapping={
        "advance_rollout_rule": "advanceRolloutRule",
        "promote_release_rule": "promoteReleaseRule",
        "repair_rollout_rule": "repairRolloutRule",
        "timed_promote_release_rule": "timedPromoteReleaseRule",
    },
)
class GoogleClouddeployAutomationRules:
    def __init__(
        self,
        *,
        advance_rollout_rule: typing.Optional[typing.Union["GoogleClouddeployAutomationRulesAdvanceRolloutRule", typing.Dict[builtins.str, typing.Any]]] = None,
        promote_release_rule: typing.Optional[typing.Union["GoogleClouddeployAutomationRulesPromoteReleaseRule", typing.Dict[builtins.str, typing.Any]]] = None,
        repair_rollout_rule: typing.Optional[typing.Union["GoogleClouddeployAutomationRulesRepairRolloutRule", typing.Dict[builtins.str, typing.Any]]] = None,
        timed_promote_release_rule: typing.Optional[typing.Union["GoogleClouddeployAutomationRulesTimedPromoteReleaseRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advance_rollout_rule: advance_rollout_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#advance_rollout_rule GoogleClouddeployAutomation#advance_rollout_rule}
        :param promote_release_rule: promote_release_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#promote_release_rule GoogleClouddeployAutomation#promote_release_rule}
        :param repair_rollout_rule: repair_rollout_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#repair_rollout_rule GoogleClouddeployAutomation#repair_rollout_rule}
        :param timed_promote_release_rule: timed_promote_release_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#timed_promote_release_rule GoogleClouddeployAutomation#timed_promote_release_rule}
        '''
        if isinstance(advance_rollout_rule, dict):
            advance_rollout_rule = GoogleClouddeployAutomationRulesAdvanceRolloutRule(**advance_rollout_rule)
        if isinstance(promote_release_rule, dict):
            promote_release_rule = GoogleClouddeployAutomationRulesPromoteReleaseRule(**promote_release_rule)
        if isinstance(repair_rollout_rule, dict):
            repair_rollout_rule = GoogleClouddeployAutomationRulesRepairRolloutRule(**repair_rollout_rule)
        if isinstance(timed_promote_release_rule, dict):
            timed_promote_release_rule = GoogleClouddeployAutomationRulesTimedPromoteReleaseRule(**timed_promote_release_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118d5e9a961af4ede2eddd87b76b9c2cb28de5793102746f66a5ff81b2c9fba4)
            check_type(argname="argument advance_rollout_rule", value=advance_rollout_rule, expected_type=type_hints["advance_rollout_rule"])
            check_type(argname="argument promote_release_rule", value=promote_release_rule, expected_type=type_hints["promote_release_rule"])
            check_type(argname="argument repair_rollout_rule", value=repair_rollout_rule, expected_type=type_hints["repair_rollout_rule"])
            check_type(argname="argument timed_promote_release_rule", value=timed_promote_release_rule, expected_type=type_hints["timed_promote_release_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advance_rollout_rule is not None:
            self._values["advance_rollout_rule"] = advance_rollout_rule
        if promote_release_rule is not None:
            self._values["promote_release_rule"] = promote_release_rule
        if repair_rollout_rule is not None:
            self._values["repair_rollout_rule"] = repair_rollout_rule
        if timed_promote_release_rule is not None:
            self._values["timed_promote_release_rule"] = timed_promote_release_rule

    @builtins.property
    def advance_rollout_rule(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesAdvanceRolloutRule"]:
        '''advance_rollout_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#advance_rollout_rule GoogleClouddeployAutomation#advance_rollout_rule}
        '''
        result = self._values.get("advance_rollout_rule")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesAdvanceRolloutRule"], result)

    @builtins.property
    def promote_release_rule(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesPromoteReleaseRule"]:
        '''promote_release_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#promote_release_rule GoogleClouddeployAutomation#promote_release_rule}
        '''
        result = self._values.get("promote_release_rule")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesPromoteReleaseRule"], result)

    @builtins.property
    def repair_rollout_rule(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRule"]:
        '''repair_rollout_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#repair_rollout_rule GoogleClouddeployAutomation#repair_rollout_rule}
        '''
        result = self._values.get("repair_rollout_rule")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRule"], result)

    @builtins.property
    def timed_promote_release_rule(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesTimedPromoteReleaseRule"]:
        '''timed_promote_release_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#timed_promote_release_rule GoogleClouddeployAutomation#timed_promote_release_rule}
        '''
        result = self._values.get("timed_promote_release_rule")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesTimedPromoteReleaseRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesAdvanceRolloutRule",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "source_phases": "sourcePhases", "wait": "wait"},
)
class GoogleClouddeployAutomationRulesAdvanceRolloutRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        source_phases: typing.Optional[typing.Sequence[builtins.str]] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source_phases: Optional. Proceeds only after phase name matched any one in the list. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#source_phases GoogleClouddeployAutomation#source_phases}
        :param wait: Optional. How long to wait after a rollout is finished. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95afd554d2cf1a265746e79fa5152f1e2e195d9f8815229dc9c37d8e5ffdc47f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source_phases", value=source_phases, expected_type=type_hints["source_phases"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if source_phases is not None:
            self._values["source_phases"] = source_phases
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_phases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Proceeds only after phase name matched any one in the list. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#source_phases GoogleClouddeployAutomation#source_phases}
        '''
        result = self._values.get("source_phases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.str]:
        '''Optional. How long to wait after a rollout is finished.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesAdvanceRolloutRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesAdvanceRolloutRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesAdvanceRolloutRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22ffecbd803eef8f44d6a21cee2e1f54418b672080a51bd22f800e40ce809e99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourcePhases")
    def reset_source_phases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcePhases", []))

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcePhasesInput")
    def source_phases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcePhasesInput"))

    @builtins.property
    @jsii.member(jsii_name="waitInput")
    def wait_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a584ef90b1e8277fc0d14c6de41a250c98a7720cce521b530c73fdb1b9873f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePhases")
    def source_phases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourcePhases"))

    @source_phases.setter
    def source_phases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a19a69c3a6fe00bf2115f396a51c6e7d81d6b2f17dea2b3dbd5b697c5cf88b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePhases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wait"))

    @wait.setter
    def wait(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a425019fbb60e79fff01b98fd41df2e3e774927a5728ed192f332f20c18b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesAdvanceRolloutRule]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesAdvanceRolloutRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationRulesAdvanceRolloutRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9399a7099cd0fcc0b8e027a5bc50d226e4e4ce6df68750afea0575b304e0e22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployAutomationRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__403dafbc4721793ad4fc21f1b46ce07ffb88084abb27c30d9834440cd33b440c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployAutomationRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d52ec4ba64a6149eff796168baf94cc59dc3b1980d6b3a2d6fcdb4bcc9efcc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployAutomationRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19571f1731b72ca4cc0490e7d702674d664cc10aa253560c4b158f016f92e990)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b25766acc93e06ec94e32ad0f131ac08e2d94d1dc200bde044c1a1a3209c5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c998155ff6ff5f2b1cfd215b3547a4aaf9f3b22c5a37fcdbd6d081f7d32a0261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f218430e5f0b0d416fd2db5d93fa52839181a3f40ba2c6d2689e400c450fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployAutomationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__602425dc1aebe7cd3e37d91aeed77ca30bd785b995f92ce51a5c00406e916802)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAdvanceRolloutRule")
    def put_advance_rollout_rule(
        self,
        *,
        id: builtins.str,
        source_phases: typing.Optional[typing.Sequence[builtins.str]] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source_phases: Optional. Proceeds only after phase name matched any one in the list. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#source_phases GoogleClouddeployAutomation#source_phases}
        :param wait: Optional. How long to wait after a rollout is finished. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        value = GoogleClouddeployAutomationRulesAdvanceRolloutRule(
            id=id, source_phases=source_phases, wait=wait
        )

        return typing.cast(None, jsii.invoke(self, "putAdvanceRolloutRule", [value]))

    @jsii.member(jsii_name="putPromoteReleaseRule")
    def put_promote_release_rule(
        self,
        *,
        id: builtins.str,
        destination_phase: typing.Optional[builtins.str] = None,
        destination_target_id: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param destination_phase: Optional. The starting phase of the rollout created by this operation. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this 'Release' is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine if the target is one of the stages in the promotion sequence defined in the pipeline. * "@next", the next target in the promotion sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_target_id GoogleClouddeployAutomation#destination_target_id}
        :param wait: Optional. How long the release need to be paused until being promoted to the next target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        value = GoogleClouddeployAutomationRulesPromoteReleaseRule(
            id=id,
            destination_phase=destination_phase,
            destination_target_id=destination_target_id,
            wait=wait,
        )

        return typing.cast(None, jsii.invoke(self, "putPromoteReleaseRule", [value]))

    @jsii.member(jsii_name="putRepairRolloutRule")
    def put_repair_rollout_rule(
        self,
        *,
        id: builtins.str,
        jobs: typing.Optional[typing.Sequence[builtins.str]] = None,
        phases: typing.Optional[typing.Sequence[builtins.str]] = None,
        repair_phases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jobs: Optional. Jobs to repair. Proceeds only after job name matched any one in the list, or for all jobs if unspecified or empty. The phase that includes the job must match the phase ID specified in sourcePhase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#jobs GoogleClouddeployAutomation#jobs}
        :param phases: Optional. Phases within which jobs are subject to automatic repair actions on failure. Proceeds only after phase name matched any one in the list, or for all phases if unspecified. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#phases GoogleClouddeployAutomation#phases}
        :param repair_phases: repair_phases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#repair_phases GoogleClouddeployAutomation#repair_phases}
        '''
        value = GoogleClouddeployAutomationRulesRepairRolloutRule(
            id=id, jobs=jobs, phases=phases, repair_phases=repair_phases
        )

        return typing.cast(None, jsii.invoke(self, "putRepairRolloutRule", [value]))

    @jsii.member(jsii_name="putTimedPromoteReleaseRule")
    def put_timed_promote_release_rule(
        self,
        *,
        id: builtins.str,
        schedule: builtins.str,
        time_zone: builtins.str,
        destination_phase: typing.Optional[builtins.str] = None,
        destination_target_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: Required. Schedule in crontab format. e.g. '0 9 * * 1' for every Monday at 9am. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#schedule GoogleClouddeployAutomation#schedule}
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#time_zone GoogleClouddeployAutomation#time_zone}
        :param destination_phase: Optional. The starting phase of the rollout created by this rule. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this Release is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: - The last segment of a target name - "@next", the next target in the promotion sequence" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_target_id GoogleClouddeployAutomation#destination_target_id}
        '''
        value = GoogleClouddeployAutomationRulesTimedPromoteReleaseRule(
            id=id,
            schedule=schedule,
            time_zone=time_zone,
            destination_phase=destination_phase,
            destination_target_id=destination_target_id,
        )

        return typing.cast(None, jsii.invoke(self, "putTimedPromoteReleaseRule", [value]))

    @jsii.member(jsii_name="resetAdvanceRolloutRule")
    def reset_advance_rollout_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvanceRolloutRule", []))

    @jsii.member(jsii_name="resetPromoteReleaseRule")
    def reset_promote_release_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPromoteReleaseRule", []))

    @jsii.member(jsii_name="resetRepairRolloutRule")
    def reset_repair_rollout_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepairRolloutRule", []))

    @jsii.member(jsii_name="resetTimedPromoteReleaseRule")
    def reset_timed_promote_release_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimedPromoteReleaseRule", []))

    @builtins.property
    @jsii.member(jsii_name="advanceRolloutRule")
    def advance_rollout_rule(
        self,
    ) -> GoogleClouddeployAutomationRulesAdvanceRolloutRuleOutputReference:
        return typing.cast(GoogleClouddeployAutomationRulesAdvanceRolloutRuleOutputReference, jsii.get(self, "advanceRolloutRule"))

    @builtins.property
    @jsii.member(jsii_name="promoteReleaseRule")
    def promote_release_rule(
        self,
    ) -> "GoogleClouddeployAutomationRulesPromoteReleaseRuleOutputReference":
        return typing.cast("GoogleClouddeployAutomationRulesPromoteReleaseRuleOutputReference", jsii.get(self, "promoteReleaseRule"))

    @builtins.property
    @jsii.member(jsii_name="repairRolloutRule")
    def repair_rollout_rule(
        self,
    ) -> "GoogleClouddeployAutomationRulesRepairRolloutRuleOutputReference":
        return typing.cast("GoogleClouddeployAutomationRulesRepairRolloutRuleOutputReference", jsii.get(self, "repairRolloutRule"))

    @builtins.property
    @jsii.member(jsii_name="timedPromoteReleaseRule")
    def timed_promote_release_rule(
        self,
    ) -> "GoogleClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference":
        return typing.cast("GoogleClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference", jsii.get(self, "timedPromoteReleaseRule"))

    @builtins.property
    @jsii.member(jsii_name="advanceRolloutRuleInput")
    def advance_rollout_rule_input(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesAdvanceRolloutRule]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesAdvanceRolloutRule], jsii.get(self, "advanceRolloutRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="promoteReleaseRuleInput")
    def promote_release_rule_input(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesPromoteReleaseRule"]:
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesPromoteReleaseRule"], jsii.get(self, "promoteReleaseRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="repairRolloutRuleInput")
    def repair_rollout_rule_input(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRule"]:
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRule"], jsii.get(self, "repairRolloutRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="timedPromoteReleaseRuleInput")
    def timed_promote_release_rule_input(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesTimedPromoteReleaseRule"]:
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesTimedPromoteReleaseRule"], jsii.get(self, "timedPromoteReleaseRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33e117d8f748280c9059ead9d48a1a9552902a10df372c9d379f3df8a24e81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesPromoteReleaseRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "destination_phase": "destinationPhase",
        "destination_target_id": "destinationTargetId",
        "wait": "wait",
    },
)
class GoogleClouddeployAutomationRulesPromoteReleaseRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        destination_phase: typing.Optional[builtins.str] = None,
        destination_target_id: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param destination_phase: Optional. The starting phase of the rollout created by this operation. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this 'Release' is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine if the target is one of the stages in the promotion sequence defined in the pipeline. * "@next", the next target in the promotion sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_target_id GoogleClouddeployAutomation#destination_target_id}
        :param wait: Optional. How long the release need to be paused until being promoted to the next target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5953546fa592dd33a363ebf199968d9125a66e3c52f1b65fe1e2865892b0e5d4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument destination_phase", value=destination_phase, expected_type=type_hints["destination_phase"])
            check_type(argname="argument destination_target_id", value=destination_target_id, expected_type=type_hints["destination_target_id"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if destination_phase is not None:
            self._values["destination_phase"] = destination_phase
        if destination_target_id is not None:
            self._values["destination_target_id"] = destination_target_id
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_phase(self) -> typing.Optional[builtins.str]:
        '''Optional. The starting phase of the rollout created by this operation. Default to the first phase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        '''
        result = self._values.get("destination_phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_target_id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The ID of the stage in the pipeline to which this 'Release' is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine if the target is one of the stages in the promotion sequence defined in the pipeline. * "@next", the next target in the promotion sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_target_id GoogleClouddeployAutomation#destination_target_id}
        '''
        result = self._values.get("destination_target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.str]:
        '''Optional. How long the release need to be paused until being promoted to the next target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesPromoteReleaseRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesPromoteReleaseRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesPromoteReleaseRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0127d2342f42ff9b8e2379b53fe51277947abcc34db889d911d44f3c564db3c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationPhase")
    def reset_destination_phase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPhase", []))

    @jsii.member(jsii_name="resetDestinationTargetId")
    def reset_destination_target_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationTargetId", []))

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

    @builtins.property
    @jsii.member(jsii_name="destinationPhaseInput")
    def destination_phase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPhaseInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTargetIdInput")
    def destination_target_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTargetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="waitInput")
    def wait_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPhase")
    def destination_phase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPhase"))

    @destination_phase.setter
    def destination_phase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff364d752d0f4adec6ffed9354acf9d9d685c617f9cd319539a97c79f668bd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationTargetId")
    def destination_target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationTargetId"))

    @destination_target_id.setter
    def destination_target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9df39ce44445b4e0be486a6d1b9650e06d533cfa15a72a2c55910002753dac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationTargetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b34db7def834c0f977dc988f62ec72e271155d0e4b4dcb4b5886339f1d560f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wait"))

    @wait.setter
    def wait(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89defd2c47a59f286e33133e2ed51bf61409bdff4cfd57732ad3b0c8349b24b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesPromoteReleaseRule]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesPromoteReleaseRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationRulesPromoteReleaseRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d0f81d57c7e9b242554bd0d781ede0c7411b67d4f25eaf6ccf8a89de19ccea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "jobs": "jobs",
        "phases": "phases",
        "repair_phases": "repairPhases",
    },
)
class GoogleClouddeployAutomationRulesRepairRolloutRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        jobs: typing.Optional[typing.Sequence[builtins.str]] = None,
        phases: typing.Optional[typing.Sequence[builtins.str]] = None,
        repair_phases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jobs: Optional. Jobs to repair. Proceeds only after job name matched any one in the list, or for all jobs if unspecified or empty. The phase that includes the job must match the phase ID specified in sourcePhase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#jobs GoogleClouddeployAutomation#jobs}
        :param phases: Optional. Phases within which jobs are subject to automatic repair actions on failure. Proceeds only after phase name matched any one in the list, or for all phases if unspecified. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#phases GoogleClouddeployAutomation#phases}
        :param repair_phases: repair_phases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#repair_phases GoogleClouddeployAutomation#repair_phases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541af22afc229e81c46229b2b10586a2f11b94cbdd21666ddbb75829b46b3d98)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument phases", value=phases, expected_type=type_hints["phases"])
            check_type(argname="argument repair_phases", value=repair_phases, expected_type=type_hints["repair_phases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if jobs is not None:
            self._values["jobs"] = jobs
        if phases is not None:
            self._values["phases"] = phases
        if repair_phases is not None:
            self._values["repair_phases"] = repair_phases

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jobs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Jobs to repair. Proceeds only after job name matched any one in the list, or for all jobs if unspecified or empty. The phase that includes the job must match the phase ID specified in sourcePhase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#jobs GoogleClouddeployAutomation#jobs}
        '''
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def phases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Phases within which jobs are subject to automatic repair actions on failure. Proceeds only after phase name matched any one in the list, or for all phases if unspecified. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#phases GoogleClouddeployAutomation#phases}
        '''
        result = self._values.get("phases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def repair_phases(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]]:
        '''repair_phases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#repair_phases GoogleClouddeployAutomation#repair_phases}
        '''
        result = self._values.get("repair_phases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesRepairRolloutRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesRepairRolloutRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae72535382647ff0ff71c56edc875815811143c757f28e02ef26937a447acbbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepairPhases")
    def put_repair_phases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b2e70acce94b8bfb5e7755d17a6d376e5730103febce0848899cfe6e18b1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRepairPhases", [value]))

    @jsii.member(jsii_name="resetJobs")
    def reset_jobs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobs", []))

    @jsii.member(jsii_name="resetPhases")
    def reset_phases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhases", []))

    @jsii.member(jsii_name="resetRepairPhases")
    def reset_repair_phases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepairPhases", []))

    @builtins.property
    @jsii.member(jsii_name="repairPhases")
    def repair_phases(
        self,
    ) -> "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList":
        return typing.cast("GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList", jsii.get(self, "repairPhases"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jobsInput")
    def jobs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jobsInput"))

    @builtins.property
    @jsii.member(jsii_name="phasesInput")
    def phases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "phasesInput"))

    @builtins.property
    @jsii.member(jsii_name="repairPhasesInput")
    def repair_phases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]], jsii.get(self, "repairPhasesInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc7be8540d8797d79d019a59fab59bf871c3c32eaeb67a437a4226cfe41e457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jobs"))

    @jobs.setter
    def jobs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09f02b0b5c40b5ccd881f94066518bb6683f2349484804df083784b07665e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phases")
    def phases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "phases"))

    @phases.setter
    def phases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4294dc77d79663a2b77ebb4eeaee9452b03faaaa3d99fa4f3e636916fbf95058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRule]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa941f18b5b8f887ddf50f641d53c232a5a03fd64052ee84579330a2dc46cb88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases",
    jsii_struct_bases=[],
    name_mapping={"retry": "retry", "rollback": "rollback"},
)
class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases:
    def __init__(
        self,
        *,
        retry: typing.Optional[typing.Union["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry", typing.Dict[builtins.str, typing.Any]]] = None,
        rollback: typing.Optional[typing.Union["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param retry: retry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#retry GoogleClouddeployAutomation#retry}
        :param rollback: rollback block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#rollback GoogleClouddeployAutomation#rollback}
        '''
        if isinstance(retry, dict):
            retry = GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry(**retry)
        if isinstance(rollback, dict):
            rollback = GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback(**rollback)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd8104a726b33f08dd2e339eb168b861aaf547eda241ea83bd2709ed18e83f8)
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
            check_type(argname="argument rollback", value=rollback, expected_type=type_hints["rollback"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retry is not None:
            self._values["retry"] = retry
        if rollback is not None:
            self._values["rollback"] = rollback

    @builtins.property
    def retry(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"]:
        '''retry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#retry GoogleClouddeployAutomation#retry}
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"], result)

    @builtins.property
    def rollback(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"]:
        '''rollback block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#rollback GoogleClouddeployAutomation#rollback}
        '''
        result = self._values.get("rollback")
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c06ac213afd2ce962112d17e3aa26bca61a1289366a40896c6c6ba2f5d3aa40a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f90c83deb08309a68c9080884d970edb2b11afbd0187003df1125666e34c064)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094846d355b51cab143900f6bda626043b98f88e82f5e33cdd9373cd46c0341a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dbc4a0d39a68cf2b125f90fd98d9f6df020444e3be6978f79d72da149ed0129)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d457d91de816408523f0bbcf1dafe22fdb66601cb6e18cee659c7aec87342103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199bb5af725b204eb8fbf8b881959a52b5a001a95a99816d44515511f1f94799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83807c97d41710ed708c29fdcb6489d2fae4313af8d67e14a289315b168ecbbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRetry")
    def put_retry(
        self,
        *,
        attempts: builtins.str,
        backoff_mode: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attempts: Required. Total number of retries. Retry is skipped if set to 0; The minimum value is 1, and the maximum value is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#attempts GoogleClouddeployAutomation#attempts}
        :param backoff_mode: Optional. The pattern of how wait time will be increased. Default is linear. Backoff mode will be ignored if wait is 0. Possible values: ["BACKOFF_MODE_UNSPECIFIED", "BACKOFF_MODE_LINEAR", "BACKOFF_MODE_EXPONENTIAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#backoff_mode GoogleClouddeployAutomation#backoff_mode}
        :param wait: Optional. How long to wait for the first retry. Default is 0, and the maximum value is 14d. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        value = GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry(
            attempts=attempts, backoff_mode=backoff_mode, wait=wait
        )

        return typing.cast(None, jsii.invoke(self, "putRetry", [value]))

    @jsii.member(jsii_name="putRollback")
    def put_rollback(
        self,
        *,
        destination_phase: typing.Optional[builtins.str] = None,
        disable_rollback_if_rollout_pending: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_phase: Optional. The starting phase ID for the Rollout. If unspecified, the Rollout will start in the stable phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        :param disable_rollback_if_rollout_pending: Optional. If pending rollout exists on the target, the rollback operation will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#disable_rollback_if_rollout_pending GoogleClouddeployAutomation#disable_rollback_if_rollout_pending}
        '''
        value = GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback(
            destination_phase=destination_phase,
            disable_rollback_if_rollout_pending=disable_rollback_if_rollout_pending,
        )

        return typing.cast(None, jsii.invoke(self, "putRollback", [value]))

    @jsii.member(jsii_name="resetRetry")
    def reset_retry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetry", []))

    @jsii.member(jsii_name="resetRollback")
    def reset_rollback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollback", []))

    @builtins.property
    @jsii.member(jsii_name="retry")
    def retry(
        self,
    ) -> "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference":
        return typing.cast("GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference", jsii.get(self, "retry"))

    @builtins.property
    @jsii.member(jsii_name="rollback")
    def rollback(
        self,
    ) -> "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference":
        return typing.cast("GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference", jsii.get(self, "rollback"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"]:
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackInput")
    def rollback_input(
        self,
    ) -> typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"]:
        return typing.cast(typing.Optional["GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"], jsii.get(self, "rollbackInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc1f59e8a5b007dde78c045c18ec41a0642fec3d5578528dbf187d2038a0a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry",
    jsii_struct_bases=[],
    name_mapping={
        "attempts": "attempts",
        "backoff_mode": "backoffMode",
        "wait": "wait",
    },
)
class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry:
    def __init__(
        self,
        *,
        attempts: builtins.str,
        backoff_mode: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attempts: Required. Total number of retries. Retry is skipped if set to 0; The minimum value is 1, and the maximum value is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#attempts GoogleClouddeployAutomation#attempts}
        :param backoff_mode: Optional. The pattern of how wait time will be increased. Default is linear. Backoff mode will be ignored if wait is 0. Possible values: ["BACKOFF_MODE_UNSPECIFIED", "BACKOFF_MODE_LINEAR", "BACKOFF_MODE_EXPONENTIAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#backoff_mode GoogleClouddeployAutomation#backoff_mode}
        :param wait: Optional. How long to wait for the first retry. Default is 0, and the maximum value is 14d. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4e762b87dcacc36fedd0ef151936a75d8e84ac76b117b12c2a2ecab66d1ca1)
            check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
            check_type(argname="argument backoff_mode", value=backoff_mode, expected_type=type_hints["backoff_mode"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attempts": attempts,
        }
        if backoff_mode is not None:
            self._values["backoff_mode"] = backoff_mode
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def attempts(self) -> builtins.str:
        '''Required.

        Total number of retries. Retry is skipped if set to 0; The minimum value is 1, and the maximum value is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#attempts GoogleClouddeployAutomation#attempts}
        '''
        result = self._values.get("attempts")
        assert result is not None, "Required property 'attempts' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backoff_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The pattern of how wait time will be increased. Default is linear. Backoff mode will be ignored if wait is 0. Possible values: ["BACKOFF_MODE_UNSPECIFIED", "BACKOFF_MODE_LINEAR", "BACKOFF_MODE_EXPONENTIAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#backoff_mode GoogleClouddeployAutomation#backoff_mode}
        '''
        result = self._values.get("backoff_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.str]:
        '''Optional.

        How long to wait for the first retry. Default is 0, and the maximum value is 14d. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#wait GoogleClouddeployAutomation#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57ba0d5c59f412379886453d6eb8f846a6e000052d5ececccbb696413fc2cb5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackoffMode")
    def reset_backoff_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackoffMode", []))

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

    @builtins.property
    @jsii.member(jsii_name="attemptsInput")
    def attempts_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="backoffModeInput")
    def backoff_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backoffModeInput"))

    @builtins.property
    @jsii.member(jsii_name="waitInput")
    def wait_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="attempts")
    def attempts(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attempts"))

    @attempts.setter
    def attempts(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8088930786814796620cd06cbdc67222006b6481286fa6c47dded4ac3476c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backoffMode")
    def backoff_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backoffMode"))

    @backoff_mode.setter
    def backoff_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0470d950521e8463206e5c3e8eb6393883bdf2f508b27b78127c812af25fd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backoffMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wait"))

    @wait.setter
    def wait(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e563f944f6f0d3a08d75a5fb6059bcc943e06f8b6ada549bac3a779023a1fc65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdb3d7fb58d0382e0c300880961d39d5465d9674bdd9360e5ae30079fd38c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback",
    jsii_struct_bases=[],
    name_mapping={
        "destination_phase": "destinationPhase",
        "disable_rollback_if_rollout_pending": "disableRollbackIfRolloutPending",
    },
)
class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback:
    def __init__(
        self,
        *,
        destination_phase: typing.Optional[builtins.str] = None,
        disable_rollback_if_rollout_pending: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_phase: Optional. The starting phase ID for the Rollout. If unspecified, the Rollout will start in the stable phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        :param disable_rollback_if_rollout_pending: Optional. If pending rollout exists on the target, the rollback operation will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#disable_rollback_if_rollout_pending GoogleClouddeployAutomation#disable_rollback_if_rollout_pending}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3de260bff188bf1c55c7ae8ab8ccff1dbf49c83b1fc46145bcfd61e20d805e)
            check_type(argname="argument destination_phase", value=destination_phase, expected_type=type_hints["destination_phase"])
            check_type(argname="argument disable_rollback_if_rollout_pending", value=disable_rollback_if_rollout_pending, expected_type=type_hints["disable_rollback_if_rollout_pending"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_phase is not None:
            self._values["destination_phase"] = destination_phase
        if disable_rollback_if_rollout_pending is not None:
            self._values["disable_rollback_if_rollout_pending"] = disable_rollback_if_rollout_pending

    @builtins.property
    def destination_phase(self) -> typing.Optional[builtins.str]:
        '''Optional. The starting phase ID for the Rollout. If unspecified, the Rollout will start in the stable phase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        '''
        result = self._values.get("destination_phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_rollback_if_rollout_pending(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If pending rollout exists on the target, the rollback operation will be aborted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#disable_rollback_if_rollout_pending GoogleClouddeployAutomation#disable_rollback_if_rollout_pending}
        '''
        result = self._values.get("disable_rollback_if_rollout_pending")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__443dfdba32f424e5c7f1329b1face36f61fcc6a8f1189dcf07a84ee82f79366b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationPhase")
    def reset_destination_phase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPhase", []))

    @jsii.member(jsii_name="resetDisableRollbackIfRolloutPending")
    def reset_disable_rollback_if_rollout_pending(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableRollbackIfRolloutPending", []))

    @builtins.property
    @jsii.member(jsii_name="destinationPhaseInput")
    def destination_phase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPhaseInput"))

    @builtins.property
    @jsii.member(jsii_name="disableRollbackIfRolloutPendingInput")
    def disable_rollback_if_rollout_pending_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableRollbackIfRolloutPendingInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPhase")
    def destination_phase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPhase"))

    @destination_phase.setter
    def destination_phase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad60492066f3bc7d6b2a3b8a5f5ccf55972df3fed45723ccad224bf93d9e9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableRollbackIfRolloutPending")
    def disable_rollback_if_rollout_pending(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableRollbackIfRolloutPending"))

    @disable_rollback_if_rollout_pending.setter
    def disable_rollback_if_rollout_pending(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62be8fefd8c6335ef3b58ed03b63a57d5b30085118eb8afab452486eefafc340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableRollbackIfRolloutPending", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e1f9d032cb6fe78953ee816c08232a9628e5bd986951eb1c5ea42b106054a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesTimedPromoteReleaseRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "schedule": "schedule",
        "time_zone": "timeZone",
        "destination_phase": "destinationPhase",
        "destination_target_id": "destinationTargetId",
    },
)
class GoogleClouddeployAutomationRulesTimedPromoteReleaseRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        schedule: builtins.str,
        time_zone: builtins.str,
        destination_phase: typing.Optional[builtins.str] = None,
        destination_target_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: Required. Schedule in crontab format. e.g. '0 9 * * 1' for every Monday at 9am. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#schedule GoogleClouddeployAutomation#schedule}
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#time_zone GoogleClouddeployAutomation#time_zone}
        :param destination_phase: Optional. The starting phase of the rollout created by this rule. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this Release is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: - The last segment of a target name - "@next", the next target in the promotion sequence" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_target_id GoogleClouddeployAutomation#destination_target_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f1390020872938bcd9fee9018f5cb8d64077a5e5c2483667a7c0969a8219fa7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument destination_phase", value=destination_phase, expected_type=type_hints["destination_phase"])
            check_type(argname="argument destination_target_id", value=destination_target_id, expected_type=type_hints["destination_target_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "schedule": schedule,
            "time_zone": time_zone,
        }
        if destination_phase is not None:
            self._values["destination_phase"] = destination_phase
        if destination_target_id is not None:
            self._values["destination_target_id"] = destination_target_id

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Required. Schedule in crontab format. e.g. '0 9 * * 1' for every Monday at 9am.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#schedule GoogleClouddeployAutomation#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#time_zone GoogleClouddeployAutomation#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_phase(self) -> typing.Optional[builtins.str]:
        '''Optional. The starting phase of the rollout created by this rule. Default to the first phase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_phase GoogleClouddeployAutomation#destination_phase}
        '''
        result = self._values.get("destination_phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_target_id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The ID of the stage in the pipeline to which this Release is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following:

        - The last segment of a target name
        - "@next", the next target in the promotion sequence"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#destination_target_id GoogleClouddeployAutomation#destination_target_id}
        '''
        result = self._values.get("destination_target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationRulesTimedPromoteReleaseRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e47de236d9f8fe28c40581994d194a56a34e95a7692156c7c3b9820812dc89b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationPhase")
    def reset_destination_phase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationPhase", []))

    @jsii.member(jsii_name="resetDestinationTargetId")
    def reset_destination_target_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationTargetId", []))

    @builtins.property
    @jsii.member(jsii_name="destinationPhaseInput")
    def destination_phase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationPhaseInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTargetIdInput")
    def destination_target_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTargetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationPhase")
    def destination_phase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationPhase"))

    @destination_phase.setter
    def destination_phase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b309925febdaa98601469edacf6f4b8a4b96907fe481f2138a0f7d3bf534e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationTargetId")
    def destination_target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationTargetId"))

    @destination_target_id.setter
    def destination_target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb610b151d5966e3fd35d3d5cf64a347c8d2c15efb63e31758af75ea072b157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationTargetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d461d58c3d3d931bedf1bfff787c4b5aad050052983cdc7192e9927b16e16610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e220dc37958d9cbedd6f40feafd63fa3aed1be6a0a0a24eb4b041284aebe89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0857699deffa057255bc9e6882ede68fc67f500baf37ef2d7a65f0564b6dd9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployAutomationRulesTimedPromoteReleaseRule]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationRulesTimedPromoteReleaseRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationRulesTimedPromoteReleaseRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7135bc23aa4e0735f6ea7e9b0231f5c3153c85ed23c6928146c82133c69ac4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationSelector",
    jsii_struct_bases=[],
    name_mapping={"targets": "targets"},
)
class GoogleClouddeployAutomationSelector:
    def __init__(
        self,
        *,
        targets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationSelectorTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#targets GoogleClouddeployAutomation#targets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6791ee4793c4521926c204c31248dced50eb8fd4acf67798340cc6208a51e5ea)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
        }

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationSelectorTargets"]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#targets GoogleClouddeployAutomation#targets}
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationSelectorTargets"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80e141e1a8b150f4656a27b013a8133284d8acdadec05599a892a6a47a24cf09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployAutomationSelectorTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22167447e3d9e054ee7326e63ce61201737136ba8d1c813ba1852f814ebbba7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "GoogleClouddeployAutomationSelectorTargetsList":
        return typing.cast("GoogleClouddeployAutomationSelectorTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationSelectorTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployAutomationSelectorTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleClouddeployAutomationSelector]:
        return typing.cast(typing.Optional[GoogleClouddeployAutomationSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployAutomationSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbeda017af10b1a9b35def1a88dfdc288e2ac394d22b0ec61cc365c241622da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationSelectorTargets",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "labels": "labels"},
)
class GoogleClouddeployAutomationSelectorTargets:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: ID of the 'Target'. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Target labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#labels GoogleClouddeployAutomation#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2196bfafe48be48252828e67dbe6313da1eed49e4b16ccc94a62e41870db60ae)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''ID of the 'Target'.

        The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#id GoogleClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Target labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#labels GoogleClouddeployAutomation#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationSelectorTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationSelectorTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationSelectorTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbe63fa364690134747e8c646bb7487528c9a8e45a0affb307846e11d4d06570)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployAutomationSelectorTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101960dc7372dd08f5262114c77efd2f2fb00a603e215119ba3a699ea4bcb377)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployAutomationSelectorTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6b3adea45dfbcc574c12445fe15d8d76bfe14d0a1a1580b3e4df5fbe67486a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2af91d5741d6bc456031000e5949f6482437b22313b3f10f967402b1f616f09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49caf869a9ccb6da337f6e29d8f6e03508968a2a6650a42fc50f79dfea1aa08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationSelectorTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationSelectorTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationSelectorTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190684a0c0113ec5bf1c0dda2a57b254240a512e4c0925d67cdde5ff4e69444d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployAutomationSelectorTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationSelectorTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb34bf39215942861a9dc6ec823e15422f19ede578fdf45003e7e9c86916c372)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a42322924189ad4083d1dd92765a16a579fb9b26afd741faf3dfb5dd116950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0985e40341c1ac505b20b3d9129529eb926d41f78fd1b0f4124b5dd42cd5fc7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationSelectorTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationSelectorTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationSelectorTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6746a98218f4bcbc3729805b47656c8980617d51c15c2768bf68db78a12c5f3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleClouddeployAutomationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#create GoogleClouddeployAutomation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#delete GoogleClouddeployAutomation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#update GoogleClouddeployAutomation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d6e87da6838c3dd8bf7da798c0a2fef3d714e800598f0299c91bda35c728cf6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#create GoogleClouddeployAutomation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#delete GoogleClouddeployAutomation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_automation#update GoogleClouddeployAutomation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployAutomationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployAutomationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployAutomation.GoogleClouddeployAutomationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d85446428989e7ece37923576fa6ca1fda017299b5913265619358049199d8d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39a574897c1d434143198cda8cd3cd895cf9292a814cec693dd2732fb6700343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c475b01b2c1ee1fb51a5203988adb52f9668f46d2e8c4e79ca406e69e466d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a7d9c51e533885d8b29c990a7e45491c1b5649543350ba5e0b1c93a29ad9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e375a492ab3e05801afb4aedfb6d88fa057c0b146fd030a6a5699c99a0293ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleClouddeployAutomation",
    "GoogleClouddeployAutomationConfig",
    "GoogleClouddeployAutomationRules",
    "GoogleClouddeployAutomationRulesAdvanceRolloutRule",
    "GoogleClouddeployAutomationRulesAdvanceRolloutRuleOutputReference",
    "GoogleClouddeployAutomationRulesList",
    "GoogleClouddeployAutomationRulesOutputReference",
    "GoogleClouddeployAutomationRulesPromoteReleaseRule",
    "GoogleClouddeployAutomationRulesPromoteReleaseRuleOutputReference",
    "GoogleClouddeployAutomationRulesRepairRolloutRule",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleOutputReference",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback",
    "GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference",
    "GoogleClouddeployAutomationRulesTimedPromoteReleaseRule",
    "GoogleClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference",
    "GoogleClouddeployAutomationSelector",
    "GoogleClouddeployAutomationSelectorOutputReference",
    "GoogleClouddeployAutomationSelectorTargets",
    "GoogleClouddeployAutomationSelectorTargetsList",
    "GoogleClouddeployAutomationSelectorTargetsOutputReference",
    "GoogleClouddeployAutomationTimeouts",
    "GoogleClouddeployAutomationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d1d56e6e797ed752a1201533b0a9b6d733ad865c5aa2df3661f218f8e98aeb7a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    delivery_pipeline: builtins.str,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationRules, typing.Dict[builtins.str, typing.Any]]]],
    selector: typing.Union[GoogleClouddeployAutomationSelector, typing.Dict[builtins.str, typing.Any]],
    service_account: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployAutomationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6df2000a1b8422b9ba5183b15ca493634b11b27e7be406da05935a3cdceac0b0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d86b79c5dc673bb8fb58c88b83ef0f9d014b35973258e621b764580a049a5e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b367d629a689d3173e8d9762799be6b4a091818f3573a5a1a1113ee3076ce2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ad7d3d7f76654484641123901fc6876e6124230d8f32b0aa391bcf954e8a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8802c2a4e9d44d626c1df03e6ac181b19a09a324fb9c0b1c4077c74382f20b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b3739623cad3ce5490badd5ed5965d90f4ee0920075c95c749815503740b5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9b7749994ebb7118ede9cc4f8bbd970b64a05fceb942b5e6a62e10e6bed7d5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ff6445a9332a500e1f8fbe34135b1184a4b4acecc16a7d3698b75eff49c736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dfe2517a78f3a31f70f86411625a0a66a88080b017cb529df9d3bd305baab4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78ab66e6a2769359c3d9b56f88d83b1a8be745258e9c3fe98b1857f7f1ae08a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07ab6a2718a3dca031d074023c889b36ee56305ecbb620bd528719c7c0ae98e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97364d2c0969369f11cf3b2a6d4c2dd0fde82100c8e4502c26d0d1725532194(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8923f77a4a01e94e4743f23627dec202502d72011f15aa8778403c4d132f6c82(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    delivery_pipeline: builtins.str,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationRules, typing.Dict[builtins.str, typing.Any]]]],
    selector: typing.Union[GoogleClouddeployAutomationSelector, typing.Dict[builtins.str, typing.Any]],
    service_account: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployAutomationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118d5e9a961af4ede2eddd87b76b9c2cb28de5793102746f66a5ff81b2c9fba4(
    *,
    advance_rollout_rule: typing.Optional[typing.Union[GoogleClouddeployAutomationRulesAdvanceRolloutRule, typing.Dict[builtins.str, typing.Any]]] = None,
    promote_release_rule: typing.Optional[typing.Union[GoogleClouddeployAutomationRulesPromoteReleaseRule, typing.Dict[builtins.str, typing.Any]]] = None,
    repair_rollout_rule: typing.Optional[typing.Union[GoogleClouddeployAutomationRulesRepairRolloutRule, typing.Dict[builtins.str, typing.Any]]] = None,
    timed_promote_release_rule: typing.Optional[typing.Union[GoogleClouddeployAutomationRulesTimedPromoteReleaseRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95afd554d2cf1a265746e79fa5152f1e2e195d9f8815229dc9c37d8e5ffdc47f(
    *,
    id: builtins.str,
    source_phases: typing.Optional[typing.Sequence[builtins.str]] = None,
    wait: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ffecbd803eef8f44d6a21cee2e1f54418b672080a51bd22f800e40ce809e99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a584ef90b1e8277fc0d14c6de41a250c98a7720cce521b530c73fdb1b9873f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a19a69c3a6fe00bf2115f396a51c6e7d81d6b2f17dea2b3dbd5b697c5cf88b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a425019fbb60e79fff01b98fd41df2e3e774927a5728ed192f332f20c18b33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9399a7099cd0fcc0b8e027a5bc50d226e4e4ce6df68750afea0575b304e0e22a(
    value: typing.Optional[GoogleClouddeployAutomationRulesAdvanceRolloutRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403dafbc4721793ad4fc21f1b46ce07ffb88084abb27c30d9834440cd33b440c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d52ec4ba64a6149eff796168baf94cc59dc3b1980d6b3a2d6fcdb4bcc9efcc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19571f1731b72ca4cc0490e7d702674d664cc10aa253560c4b158f016f92e990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b25766acc93e06ec94e32ad0f131ac08e2d94d1dc200bde044c1a1a3209c5b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c998155ff6ff5f2b1cfd215b3547a4aaf9f3b22c5a37fcdbd6d081f7d32a0261(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f218430e5f0b0d416fd2db5d93fa52839181a3f40ba2c6d2689e400c450fed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602425dc1aebe7cd3e37d91aeed77ca30bd785b995f92ce51a5c00406e916802(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33e117d8f748280c9059ead9d48a1a9552902a10df372c9d379f3df8a24e81d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5953546fa592dd33a363ebf199968d9125a66e3c52f1b65fe1e2865892b0e5d4(
    *,
    id: builtins.str,
    destination_phase: typing.Optional[builtins.str] = None,
    destination_target_id: typing.Optional[builtins.str] = None,
    wait: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0127d2342f42ff9b8e2379b53fe51277947abcc34db889d911d44f3c564db3c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff364d752d0f4adec6ffed9354acf9d9d685c617f9cd319539a97c79f668bd31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9df39ce44445b4e0be486a6d1b9650e06d533cfa15a72a2c55910002753dac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b34db7def834c0f977dc988f62ec72e271155d0e4b4dcb4b5886339f1d560f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89defd2c47a59f286e33133e2ed51bf61409bdff4cfd57732ad3b0c8349b24b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d0f81d57c7e9b242554bd0d781ede0c7411b67d4f25eaf6ccf8a89de19ccea(
    value: typing.Optional[GoogleClouddeployAutomationRulesPromoteReleaseRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541af22afc229e81c46229b2b10586a2f11b94cbdd21666ddbb75829b46b3d98(
    *,
    id: builtins.str,
    jobs: typing.Optional[typing.Sequence[builtins.str]] = None,
    phases: typing.Optional[typing.Sequence[builtins.str]] = None,
    repair_phases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae72535382647ff0ff71c56edc875815811143c757f28e02ef26937a447acbbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b2e70acce94b8bfb5e7755d17a6d376e5730103febce0848899cfe6e18b1d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc7be8540d8797d79d019a59fab59bf871c3c32eaeb67a437a4226cfe41e457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09f02b0b5c40b5ccd881f94066518bb6683f2349484804df083784b07665e3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4294dc77d79663a2b77ebb4eeaee9452b03faaaa3d99fa4f3e636916fbf95058(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa941f18b5b8f887ddf50f641d53c232a5a03fd64052ee84579330a2dc46cb88(
    value: typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd8104a726b33f08dd2e339eb168b861aaf547eda241ea83bd2709ed18e83f8(
    *,
    retry: typing.Optional[typing.Union[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry, typing.Dict[builtins.str, typing.Any]]] = None,
    rollback: typing.Optional[typing.Union[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06ac213afd2ce962112d17e3aa26bca61a1289366a40896c6c6ba2f5d3aa40a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f90c83deb08309a68c9080884d970edb2b11afbd0187003df1125666e34c064(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094846d355b51cab143900f6bda626043b98f88e82f5e33cdd9373cd46c0341a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbc4a0d39a68cf2b125f90fd98d9f6df020444e3be6978f79d72da149ed0129(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d457d91de816408523f0bbcf1dafe22fdb66601cb6e18cee659c7aec87342103(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199bb5af725b204eb8fbf8b881959a52b5a001a95a99816d44515511f1f94799(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83807c97d41710ed708c29fdcb6489d2fae4313af8d67e14a289315b168ecbbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc1f59e8a5b007dde78c045c18ec41a0642fec3d5578528dbf187d2038a0a89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4e762b87dcacc36fedd0ef151936a75d8e84ac76b117b12c2a2ecab66d1ca1(
    *,
    attempts: builtins.str,
    backoff_mode: typing.Optional[builtins.str] = None,
    wait: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ba0d5c59f412379886453d6eb8f846a6e000052d5ececccbb696413fc2cb5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8088930786814796620cd06cbdc67222006b6481286fa6c47dded4ac3476c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0470d950521e8463206e5c3e8eb6393883bdf2f508b27b78127c812af25fd91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e563f944f6f0d3a08d75a5fb6059bcc943e06f8b6ada549bac3a779023a1fc65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdb3d7fb58d0382e0c300880961d39d5465d9674bdd9360e5ae30079fd38c2b(
    value: typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3de260bff188bf1c55c7ae8ab8ccff1dbf49c83b1fc46145bcfd61e20d805e(
    *,
    destination_phase: typing.Optional[builtins.str] = None,
    disable_rollback_if_rollout_pending: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443dfdba32f424e5c7f1329b1face36f61fcc6a8f1189dcf07a84ee82f79366b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad60492066f3bc7d6b2a3b8a5f5ccf55972df3fed45723ccad224bf93d9e9c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62be8fefd8c6335ef3b58ed03b63a57d5b30085118eb8afab452486eefafc340(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e1f9d032cb6fe78953ee816c08232a9628e5bd986951eb1c5ea42b106054a4(
    value: typing.Optional[GoogleClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1390020872938bcd9fee9018f5cb8d64077a5e5c2483667a7c0969a8219fa7(
    *,
    id: builtins.str,
    schedule: builtins.str,
    time_zone: builtins.str,
    destination_phase: typing.Optional[builtins.str] = None,
    destination_target_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47de236d9f8fe28c40581994d194a56a34e95a7692156c7c3b9820812dc89b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b309925febdaa98601469edacf6f4b8a4b96907fe481f2138a0f7d3bf534e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb610b151d5966e3fd35d3d5cf64a347c8d2c15efb63e31758af75ea072b157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d461d58c3d3d931bedf1bfff787c4b5aad050052983cdc7192e9927b16e16610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e220dc37958d9cbedd6f40feafd63fa3aed1be6a0a0a24eb4b041284aebe89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0857699deffa057255bc9e6882ede68fc67f500baf37ef2d7a65f0564b6dd9d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7135bc23aa4e0735f6ea7e9b0231f5c3153c85ed23c6928146c82133c69ac4b(
    value: typing.Optional[GoogleClouddeployAutomationRulesTimedPromoteReleaseRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6791ee4793c4521926c204c31248dced50eb8fd4acf67798340cc6208a51e5ea(
    *,
    targets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationSelectorTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e141e1a8b150f4656a27b013a8133284d8acdadec05599a892a6a47a24cf09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22167447e3d9e054ee7326e63ce61201737136ba8d1c813ba1852f814ebbba7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployAutomationSelectorTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeda017af10b1a9b35def1a88dfdc288e2ac394d22b0ec61cc365c241622da1(
    value: typing.Optional[GoogleClouddeployAutomationSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2196bfafe48be48252828e67dbe6313da1eed49e4b16ccc94a62e41870db60ae(
    *,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe63fa364690134747e8c646bb7487528c9a8e45a0affb307846e11d4d06570(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101960dc7372dd08f5262114c77efd2f2fb00a603e215119ba3a699ea4bcb377(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6b3adea45dfbcc574c12445fe15d8d76bfe14d0a1a1580b3e4df5fbe67486a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2af91d5741d6bc456031000e5949f6482437b22313b3f10f967402b1f616f09(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49caf869a9ccb6da337f6e29d8f6e03508968a2a6650a42fc50f79dfea1aa08d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190684a0c0113ec5bf1c0dda2a57b254240a512e4c0925d67cdde5ff4e69444d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployAutomationSelectorTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb34bf39215942861a9dc6ec823e15422f19ede578fdf45003e7e9c86916c372(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a42322924189ad4083d1dd92765a16a579fb9b26afd741faf3dfb5dd116950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0985e40341c1ac505b20b3d9129529eb926d41f78fd1b0f4124b5dd42cd5fc7b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6746a98218f4bcbc3729805b47656c8980617d51c15c2768bf68db78a12c5f3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationSelectorTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6e87da6838c3dd8bf7da798c0a2fef3d714e800598f0299c91bda35c728cf6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85446428989e7ece37923576fa6ca1fda017299b5913265619358049199d8d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a574897c1d434143198cda8cd3cd895cf9292a814cec693dd2732fb6700343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c475b01b2c1ee1fb51a5203988adb52f9668f46d2e8c4e79ca406e69e466d73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a7d9c51e533885d8b29c990a7e45491c1b5649543350ba5e0b1c93a29ad9f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e375a492ab3e05801afb4aedfb6d88fa057c0b146fd030a6a5699c99a0293ba9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployAutomationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
