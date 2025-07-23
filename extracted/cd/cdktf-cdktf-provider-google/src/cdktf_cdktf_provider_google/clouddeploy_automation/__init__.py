r'''
# `google_clouddeploy_automation`

Refer to the Terraform Registry for docs: [`google_clouddeploy_automation`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation).
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


class ClouddeployAutomation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation google_clouddeploy_automation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        delivery_pipeline: builtins.str,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationRules", typing.Dict[builtins.str, typing.Any]]]],
        selector: typing.Union["ClouddeployAutomationSelector", typing.Dict[builtins.str, typing.Any]],
        service_account: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployAutomationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation google_clouddeploy_automation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param delivery_pipeline: The delivery_pipeline for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#delivery_pipeline ClouddeployAutomation#delivery_pipeline}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#location ClouddeployAutomation#location}
        :param name: Name of the 'Automation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#name ClouddeployAutomation#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#rules ClouddeployAutomation#rules}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#selector ClouddeployAutomation#selector}
        :param service_account: Required. Email address of the user-managed IAM service account that creates Cloud Deploy release and rollout resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#service_account ClouddeployAutomation#service_account}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#annotations ClouddeployAutomation#annotations}
        :param description: Optional. Description of the 'Automation'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#description ClouddeployAutomation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#labels ClouddeployAutomation#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#project ClouddeployAutomation#project}.
        :param suspended: Optional. When Suspended, automation is deactivated from execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#suspended ClouddeployAutomation#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#timeouts ClouddeployAutomation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa8939f427f6bdf7e4d3c31afc8862f6dab70787b2c8c7591ccbbe45de66672)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddeployAutomationConfig(
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
        '''Generates CDKTF code for importing a ClouddeployAutomation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ClouddeployAutomation to import.
        :param import_from_id: The id of the existing ClouddeployAutomation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ClouddeployAutomation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b25a33b884c5b5b0f225601d5d7a9ad6b4b10ec75eb9dc644d66c9d9482a22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c03f8e900f493a0b6d602af7d1a90336add42bdafc68421fed110d81e67c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putSelector")
    def put_selector(
        self,
        *,
        targets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationSelectorTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#targets ClouddeployAutomation#targets}
        '''
        value = ClouddeployAutomationSelector(targets=targets)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#create ClouddeployAutomation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#delete ClouddeployAutomation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#update ClouddeployAutomation#update}.
        '''
        value = ClouddeployAutomationTimeouts(
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
    def rules(self) -> "ClouddeployAutomationRulesList":
        return typing.cast("ClouddeployAutomationRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> "ClouddeployAutomationSelectorOutputReference":
        return typing.cast("ClouddeployAutomationSelectorOutputReference", jsii.get(self, "selector"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ClouddeployAutomationTimeoutsOutputReference":
        return typing.cast("ClouddeployAutomationTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional["ClouddeployAutomationSelector"]:
        return typing.cast(typing.Optional["ClouddeployAutomationSelector"], jsii.get(self, "selectorInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployAutomationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployAutomationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef752f4d194b7cd658d332e53b4f0263aa4f51cb8f5c7875585373e06fed96ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryPipeline")
    def delivery_pipeline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryPipeline"))

    @delivery_pipeline.setter
    def delivery_pipeline(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4af964fb6f130fc3530aead6713d095314d28f89c329c98669e6d2d8230591e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryPipeline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732692ecaaa7a85e626583ebb0925bc5822d1fcc2e73d04728a9150d88ffd10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ad08163de01929b7dabcd25df381b51bf2725e13262ad9160292806376f180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70195901df586a5195b5b4bb76118cd167ef7048cd430c25242bdf75fe0b11b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63708260d863ca1cf4f585ed1376386c843dd393c480012bee010c99bc95a9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c520fe84b0c12abbca783c2c25263dea7e17fc46c76f4969a363d76840476b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180239bbf2101b1ab4ce364129329956ad3aa732ce8b89f37149e2d822bb9c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaa192d8ddd78c23a32b24b650e0a5d40fba7034c81cd5d1ae8a96a67562c0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc3f754d412fbab43232a4deaf12ee45d9ba900744707b572f5a4b6099919f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationConfig",
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
class ClouddeployAutomationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationRules", typing.Dict[builtins.str, typing.Any]]]],
        selector: typing.Union["ClouddeployAutomationSelector", typing.Dict[builtins.str, typing.Any]],
        service_account: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployAutomationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param delivery_pipeline: The delivery_pipeline for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#delivery_pipeline ClouddeployAutomation#delivery_pipeline}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#location ClouddeployAutomation#location}
        :param name: Name of the 'Automation'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#name ClouddeployAutomation#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#rules ClouddeployAutomation#rules}
        :param selector: selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#selector ClouddeployAutomation#selector}
        :param service_account: Required. Email address of the user-managed IAM service account that creates Cloud Deploy release and rollout resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#service_account ClouddeployAutomation#service_account}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#annotations ClouddeployAutomation#annotations}
        :param description: Optional. Description of the 'Automation'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#description ClouddeployAutomation#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#labels ClouddeployAutomation#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#project ClouddeployAutomation#project}.
        :param suspended: Optional. When Suspended, automation is deactivated from execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#suspended ClouddeployAutomation#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#timeouts ClouddeployAutomation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(selector, dict):
            selector = ClouddeployAutomationSelector(**selector)
        if isinstance(timeouts, dict):
            timeouts = ClouddeployAutomationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9d7aaeb92d7576c277c37e89d8b9c0fc78da858370056391bf233b3c47fdbb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#delivery_pipeline ClouddeployAutomation#delivery_pipeline}
        '''
        result = self._values.get("delivery_pipeline")
        assert result is not None, "Required property 'delivery_pipeline' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#location ClouddeployAutomation#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the 'Automation'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#name ClouddeployAutomation#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#rules ClouddeployAutomation#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRules"]], result)

    @builtins.property
    def selector(self) -> "ClouddeployAutomationSelector":
        '''selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#selector ClouddeployAutomation#selector}
        '''
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast("ClouddeployAutomationSelector", result)

    @builtins.property
    def service_account(self) -> builtins.str:
        '''Required. Email address of the user-managed IAM service account that creates Cloud Deploy release and rollout resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#service_account ClouddeployAutomation#service_account}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#annotations ClouddeployAutomation#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the 'Automation'. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#description ClouddeployAutomation#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#labels ClouddeployAutomation#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#project ClouddeployAutomation#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When Suspended, automation is deactivated from execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#suspended ClouddeployAutomation#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddeployAutomationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#timeouts ClouddeployAutomation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddeployAutomationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRules",
    jsii_struct_bases=[],
    name_mapping={
        "advance_rollout_rule": "advanceRolloutRule",
        "promote_release_rule": "promoteReleaseRule",
        "repair_rollout_rule": "repairRolloutRule",
        "timed_promote_release_rule": "timedPromoteReleaseRule",
    },
)
class ClouddeployAutomationRules:
    def __init__(
        self,
        *,
        advance_rollout_rule: typing.Optional[typing.Union["ClouddeployAutomationRulesAdvanceRolloutRule", typing.Dict[builtins.str, typing.Any]]] = None,
        promote_release_rule: typing.Optional[typing.Union["ClouddeployAutomationRulesPromoteReleaseRule", typing.Dict[builtins.str, typing.Any]]] = None,
        repair_rollout_rule: typing.Optional[typing.Union["ClouddeployAutomationRulesRepairRolloutRule", typing.Dict[builtins.str, typing.Any]]] = None,
        timed_promote_release_rule: typing.Optional[typing.Union["ClouddeployAutomationRulesTimedPromoteReleaseRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advance_rollout_rule: advance_rollout_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#advance_rollout_rule ClouddeployAutomation#advance_rollout_rule}
        :param promote_release_rule: promote_release_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#promote_release_rule ClouddeployAutomation#promote_release_rule}
        :param repair_rollout_rule: repair_rollout_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#repair_rollout_rule ClouddeployAutomation#repair_rollout_rule}
        :param timed_promote_release_rule: timed_promote_release_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#timed_promote_release_rule ClouddeployAutomation#timed_promote_release_rule}
        '''
        if isinstance(advance_rollout_rule, dict):
            advance_rollout_rule = ClouddeployAutomationRulesAdvanceRolloutRule(**advance_rollout_rule)
        if isinstance(promote_release_rule, dict):
            promote_release_rule = ClouddeployAutomationRulesPromoteReleaseRule(**promote_release_rule)
        if isinstance(repair_rollout_rule, dict):
            repair_rollout_rule = ClouddeployAutomationRulesRepairRolloutRule(**repair_rollout_rule)
        if isinstance(timed_promote_release_rule, dict):
            timed_promote_release_rule = ClouddeployAutomationRulesTimedPromoteReleaseRule(**timed_promote_release_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5da34f27805d0170177814107088ab4d5186ae9e4435af726a0a3e91d131778)
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
    ) -> typing.Optional["ClouddeployAutomationRulesAdvanceRolloutRule"]:
        '''advance_rollout_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#advance_rollout_rule ClouddeployAutomation#advance_rollout_rule}
        '''
        result = self._values.get("advance_rollout_rule")
        return typing.cast(typing.Optional["ClouddeployAutomationRulesAdvanceRolloutRule"], result)

    @builtins.property
    def promote_release_rule(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesPromoteReleaseRule"]:
        '''promote_release_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#promote_release_rule ClouddeployAutomation#promote_release_rule}
        '''
        result = self._values.get("promote_release_rule")
        return typing.cast(typing.Optional["ClouddeployAutomationRulesPromoteReleaseRule"], result)

    @builtins.property
    def repair_rollout_rule(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesRepairRolloutRule"]:
        '''repair_rollout_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#repair_rollout_rule ClouddeployAutomation#repair_rollout_rule}
        '''
        result = self._values.get("repair_rollout_rule")
        return typing.cast(typing.Optional["ClouddeployAutomationRulesRepairRolloutRule"], result)

    @builtins.property
    def timed_promote_release_rule(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesTimedPromoteReleaseRule"]:
        '''timed_promote_release_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#timed_promote_release_rule ClouddeployAutomation#timed_promote_release_rule}
        '''
        result = self._values.get("timed_promote_release_rule")
        return typing.cast(typing.Optional["ClouddeployAutomationRulesTimedPromoteReleaseRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesAdvanceRolloutRule",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "source_phases": "sourcePhases", "wait": "wait"},
)
class ClouddeployAutomationRulesAdvanceRolloutRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        source_phases: typing.Optional[typing.Sequence[builtins.str]] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source_phases: Optional. Proceeds only after phase name matched any one in the list. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#source_phases ClouddeployAutomation#source_phases}
        :param wait: Optional. How long to wait after a rollout is finished. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16bc7ae9e7f27b656aa35e658f8e873b23753a79016214a445c7e8c350c7711f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#source_phases ClouddeployAutomation#source_phases}
        '''
        result = self._values.get("source_phases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.str]:
        '''Optional. How long to wait after a rollout is finished.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesAdvanceRolloutRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesAdvanceRolloutRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesAdvanceRolloutRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad5952b1c7d937ee84595616e0cacad2017e478306f82c61f0b3edb5fba5fdae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f71308f94c5b777bda49770b0bfb3110b2e8cc5b8d6cb13107b11c8115f906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourcePhases")
    def source_phases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourcePhases"))

    @source_phases.setter
    def source_phases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccae325d4f88e44a138742653e0a891cba1b1828b16e8b967fdeb91b2237039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePhases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wait"))

    @wait.setter
    def wait(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566a81258f6ae5f0916dff06286ff1021879dc1a273207f871ed38f10c5d77d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesAdvanceRolloutRule]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesAdvanceRolloutRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationRulesAdvanceRolloutRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecf4d0585b13216fc28fa13f83585fdb1ac405493701703cc42a723877fd6cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployAutomationRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba3fea8a1d70cb67e9fec2b97654abd5ff014be2b9976ec6afd9334f69116622)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ClouddeployAutomationRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23cf8d0e4ef5d07f19de74482a3b23e5c25ad5d0fee3475fd853a989b757cd7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployAutomationRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7032b8a5c8dfbf14559573625c39bdbd20fb69287eae1ab853fe603c26f852)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f52ac1af59133043df0ca9ad77f4efdd9131547e10c6595f37f498064f766232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77dfa5471441c1fbb15afd6fdef4f9ed8febf8f1e5a854995f18400911bbeb2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353b9caa4b781d7ea9f79f393991473279950919152bf4e6b2626b9f428a6d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployAutomationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f950b4b33dbd40ca9d7116cc9df2f485af70fac88fe4f1cf430228f68baa194)
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
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source_phases: Optional. Proceeds only after phase name matched any one in the list. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: '^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#source_phases ClouddeployAutomation#source_phases}
        :param wait: Optional. How long to wait after a rollout is finished. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        value = ClouddeployAutomationRulesAdvanceRolloutRule(
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
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param destination_phase: Optional. The starting phase of the rollout created by this operation. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this 'Release' is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine if the target is one of the stages in the promotion sequence defined in the pipeline. * "@next", the next target in the promotion sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_target_id ClouddeployAutomation#destination_target_id}
        :param wait: Optional. How long the release need to be paused until being promoted to the next target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        value = ClouddeployAutomationRulesPromoteReleaseRule(
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
        repair_phases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jobs: Optional. Jobs to repair. Proceeds only after job name matched any one in the list, or for all jobs if unspecified or empty. The phase that includes the job must match the phase ID specified in sourcePhase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#jobs ClouddeployAutomation#jobs}
        :param phases: Optional. Phases within which jobs are subject to automatic repair actions on failure. Proceeds only after phase name matched any one in the list, or for all phases if unspecified. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#phases ClouddeployAutomation#phases}
        :param repair_phases: repair_phases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#repair_phases ClouddeployAutomation#repair_phases}
        '''
        value = ClouddeployAutomationRulesRepairRolloutRule(
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
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: Required. Schedule in crontab format. e.g. '0 9 * * 1' for every Monday at 9am. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#schedule ClouddeployAutomation#schedule}
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#time_zone ClouddeployAutomation#time_zone}
        :param destination_phase: Optional. The starting phase of the rollout created by this rule. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this Release is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: - The last segment of a target name - "@next", the next target in the promotion sequence" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_target_id ClouddeployAutomation#destination_target_id}
        '''
        value = ClouddeployAutomationRulesTimedPromoteReleaseRule(
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
    ) -> ClouddeployAutomationRulesAdvanceRolloutRuleOutputReference:
        return typing.cast(ClouddeployAutomationRulesAdvanceRolloutRuleOutputReference, jsii.get(self, "advanceRolloutRule"))

    @builtins.property
    @jsii.member(jsii_name="promoteReleaseRule")
    def promote_release_rule(
        self,
    ) -> "ClouddeployAutomationRulesPromoteReleaseRuleOutputReference":
        return typing.cast("ClouddeployAutomationRulesPromoteReleaseRuleOutputReference", jsii.get(self, "promoteReleaseRule"))

    @builtins.property
    @jsii.member(jsii_name="repairRolloutRule")
    def repair_rollout_rule(
        self,
    ) -> "ClouddeployAutomationRulesRepairRolloutRuleOutputReference":
        return typing.cast("ClouddeployAutomationRulesRepairRolloutRuleOutputReference", jsii.get(self, "repairRolloutRule"))

    @builtins.property
    @jsii.member(jsii_name="timedPromoteReleaseRule")
    def timed_promote_release_rule(
        self,
    ) -> "ClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference":
        return typing.cast("ClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference", jsii.get(self, "timedPromoteReleaseRule"))

    @builtins.property
    @jsii.member(jsii_name="advanceRolloutRuleInput")
    def advance_rollout_rule_input(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesAdvanceRolloutRule]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesAdvanceRolloutRule], jsii.get(self, "advanceRolloutRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="promoteReleaseRuleInput")
    def promote_release_rule_input(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesPromoteReleaseRule"]:
        return typing.cast(typing.Optional["ClouddeployAutomationRulesPromoteReleaseRule"], jsii.get(self, "promoteReleaseRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="repairRolloutRuleInput")
    def repair_rollout_rule_input(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesRepairRolloutRule"]:
        return typing.cast(typing.Optional["ClouddeployAutomationRulesRepairRolloutRule"], jsii.get(self, "repairRolloutRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="timedPromoteReleaseRuleInput")
    def timed_promote_release_rule_input(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesTimedPromoteReleaseRule"]:
        return typing.cast(typing.Optional["ClouddeployAutomationRulesTimedPromoteReleaseRule"], jsii.get(self, "timedPromoteReleaseRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8fcc5452563aa539c118f23c674de6a7604f303bd59ff09a5ca2f3cf51ff94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesPromoteReleaseRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "destination_phase": "destinationPhase",
        "destination_target_id": "destinationTargetId",
        "wait": "wait",
    },
)
class ClouddeployAutomationRulesPromoteReleaseRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        destination_phase: typing.Optional[builtins.str] = None,
        destination_target_id: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param destination_phase: Optional. The starting phase of the rollout created by this operation. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this 'Release' is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine if the target is one of the stages in the promotion sequence defined in the pipeline. * "@next", the next target in the promotion sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_target_id ClouddeployAutomation#destination_target_id}
        :param wait: Optional. How long the release need to be paused until being promoted to the next target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e4667230722f895ffc58785f907aa909e4bd8bedfc5d87d48072ceecc151b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_phase(self) -> typing.Optional[builtins.str]:
        '''Optional. The starting phase of the rollout created by this operation. Default to the first phase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        '''
        result = self._values.get("destination_phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_target_id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The ID of the stage in the pipeline to which this 'Release' is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine if the target is one of the stages in the promotion sequence defined in the pipeline. * "@next", the next target in the promotion sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_target_id ClouddeployAutomation#destination_target_id}
        '''
        result = self._values.get("destination_target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.str]:
        '''Optional. How long the release need to be paused until being promoted to the next target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesPromoteReleaseRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesPromoteReleaseRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesPromoteReleaseRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11509ff31bbfcd511f797076f4249172e031e9d7bc36c5adeb422f8ab122566a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dbf50560dd60fe31481db7628e676649896f454c85d693d3c4b48d6aad51c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationTargetId")
    def destination_target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationTargetId"))

    @destination_target_id.setter
    def destination_target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db988146ec0beeceb83c34bb96bb3bd8ce1000d4e3544444cb3bbbc7d5aae3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationTargetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fea08c79b13a68bf0a35959f038719e33ec046b1319978bbd91a5e5566b2def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wait"))

    @wait.setter
    def wait(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37aba57501d3e1a8f39e372f887bd066da5e90f87647ee9ad68c49a4471210e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesPromoteReleaseRule]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesPromoteReleaseRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationRulesPromoteReleaseRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef4ff297cbd6544f56105494f725ccfcaa4034c6bbd90feb7b5066bf2e1291f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "jobs": "jobs",
        "phases": "phases",
        "repair_phases": "repairPhases",
    },
)
class ClouddeployAutomationRulesRepairRolloutRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        jobs: typing.Optional[typing.Sequence[builtins.str]] = None,
        phases: typing.Optional[typing.Sequence[builtins.str]] = None,
        repair_phases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jobs: Optional. Jobs to repair. Proceeds only after job name matched any one in the list, or for all jobs if unspecified or empty. The phase that includes the job must match the phase ID specified in sourcePhase. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#jobs ClouddeployAutomation#jobs}
        :param phases: Optional. Phases within which jobs are subject to automatic repair actions on failure. Proceeds only after phase name matched any one in the list, or for all phases if unspecified. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#phases ClouddeployAutomation#phases}
        :param repair_phases: repair_phases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#repair_phases ClouddeployAutomation#repair_phases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c7bdee5891ca7742ded128b5d863866540e88edd3b79cb41332bc64d709585)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#jobs ClouddeployAutomation#jobs}
        '''
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def phases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Phases within which jobs are subject to automatic repair actions on failure. Proceeds only after phase name matched any one in the list, or for all phases if unspecified. This value must consist of lower-case letters, numbers, and hyphens, start with a letter and end with a letter or a number, and have a max length of 63 characters. In other words, it must match the following regex: ^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#phases ClouddeployAutomation#phases}
        '''
        result = self._values.get("phases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def repair_phases(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]]:
        '''repair_phases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#repair_phases ClouddeployAutomation#repair_phases}
        '''
        result = self._values.get("repair_phases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesRepairRolloutRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesRepairRolloutRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d90bee06127379f530866ba360eefd016b01b0ed93c2246357cd20c10855bf95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRepairPhases")
    def put_repair_phases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a836bd699df4ec55a75daca608dcd153a3e391e18d997861839f73fab2f95e8f)
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
    ) -> "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList":
        return typing.cast("ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList", jsii.get(self, "repairPhases"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationRulesRepairRolloutRuleRepairPhases"]]], jsii.get(self, "repairPhasesInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b0f2373abcab2fe4e59c5ebe27531e8bad36e67474f8d1025c8db6df701705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jobs"))

    @jobs.setter
    def jobs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405387712c2d65866ae6d6c65f4744bd6bbf745a2c5166259d09ca4e5fedf872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phases")
    def phases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "phases"))

    @phases.setter
    def phases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f87d8448691b4f6cce709aee32b492f6dedcf54999ddb2e56593ef1ed286f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesRepairRolloutRule]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesRepairRolloutRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationRulesRepairRolloutRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b125742b9147d64338c98c9a743f70abd15a07a20a0869a5dbf32c80adb90280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhases",
    jsii_struct_bases=[],
    name_mapping={"retry": "retry", "rollback": "rollback"},
)
class ClouddeployAutomationRulesRepairRolloutRuleRepairPhases:
    def __init__(
        self,
        *,
        retry: typing.Optional[typing.Union["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry", typing.Dict[builtins.str, typing.Any]]] = None,
        rollback: typing.Optional[typing.Union["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param retry: retry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#retry ClouddeployAutomation#retry}
        :param rollback: rollback block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#rollback ClouddeployAutomation#rollback}
        '''
        if isinstance(retry, dict):
            retry = ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry(**retry)
        if isinstance(rollback, dict):
            rollback = ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback(**rollback)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafd710b54e66a8c86952ab9cea1b10af4ddb6617021af1b407cbbed00cacaad)
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
    ) -> typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"]:
        '''retry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#retry ClouddeployAutomation#retry}
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"], result)

    @builtins.property
    def rollback(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"]:
        '''rollback block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#rollback ClouddeployAutomation#rollback}
        '''
        result = self._values.get("rollback")
        return typing.cast(typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesRepairRolloutRuleRepairPhases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f564dd19953d5e5aacddd5350afe3859dc954ee15f0164a962c799c693e7016e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1646e37b3b8554b1cb112f54fc1a7ade3e4289945cb73f9bc3a6b56b43517b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe8dbe5c4b0a341ab92fbfa3396bacfb8ab496d20e2756d933e677417020ca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af93b5fdc30f985bee5e4e374388a5931949b02bbf55299c0559211048187747)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76481d1e0ab53cf092970d7a4209e7deba9da734541a67eb80389601e9dcb67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd2181673a2c65efc96440e13750debf8f7ad431eb279b4595f516f3f753ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a513c1ddb2aa1d0e4d2673b3a8b30d0720e55a0c385cad58b00be979ecd587e6)
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
        :param attempts: Required. Total number of retries. Retry is skipped if set to 0; The minimum value is 1, and the maximum value is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#attempts ClouddeployAutomation#attempts}
        :param backoff_mode: Optional. The pattern of how wait time will be increased. Default is linear. Backoff mode will be ignored if wait is 0. Possible values: ["BACKOFF_MODE_UNSPECIFIED", "BACKOFF_MODE_LINEAR", "BACKOFF_MODE_EXPONENTIAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#backoff_mode ClouddeployAutomation#backoff_mode}
        :param wait: Optional. How long to wait for the first retry. Default is 0, and the maximum value is 14d. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        value = ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry(
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
        :param destination_phase: Optional. The starting phase ID for the Rollout. If unspecified, the Rollout will start in the stable phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        :param disable_rollback_if_rollout_pending: Optional. If pending rollout exists on the target, the rollback operation will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#disable_rollback_if_rollout_pending ClouddeployAutomation#disable_rollback_if_rollout_pending}
        '''
        value = ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback(
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
    ) -> "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference":
        return typing.cast("ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference", jsii.get(self, "retry"))

    @builtins.property
    @jsii.member(jsii_name="rollback")
    def rollback(
        self,
    ) -> "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference":
        return typing.cast("ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference", jsii.get(self, "rollback"))

    @builtins.property
    @jsii.member(jsii_name="retryInput")
    def retry_input(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"]:
        return typing.cast(typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry"], jsii.get(self, "retryInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackInput")
    def rollback_input(
        self,
    ) -> typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"]:
        return typing.cast(typing.Optional["ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback"], jsii.get(self, "rollbackInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c747311f15c795921f0f95a1604a4a82d40353fe21d8b242f0339579b506d78c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry",
    jsii_struct_bases=[],
    name_mapping={
        "attempts": "attempts",
        "backoff_mode": "backoffMode",
        "wait": "wait",
    },
)
class ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry:
    def __init__(
        self,
        *,
        attempts: builtins.str,
        backoff_mode: typing.Optional[builtins.str] = None,
        wait: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attempts: Required. Total number of retries. Retry is skipped if set to 0; The minimum value is 1, and the maximum value is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#attempts ClouddeployAutomation#attempts}
        :param backoff_mode: Optional. The pattern of how wait time will be increased. Default is linear. Backoff mode will be ignored if wait is 0. Possible values: ["BACKOFF_MODE_UNSPECIFIED", "BACKOFF_MODE_LINEAR", "BACKOFF_MODE_EXPONENTIAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#backoff_mode ClouddeployAutomation#backoff_mode}
        :param wait: Optional. How long to wait for the first retry. Default is 0, and the maximum value is 14d. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3c5715adc1703dd5b27e763993ba64be42ad71a66abaab1346beddd727113b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#attempts ClouddeployAutomation#attempts}
        '''
        result = self._values.get("attempts")
        assert result is not None, "Required property 'attempts' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backoff_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The pattern of how wait time will be increased. Default is linear. Backoff mode will be ignored if wait is 0. Possible values: ["BACKOFF_MODE_UNSPECIFIED", "BACKOFF_MODE_LINEAR", "BACKOFF_MODE_EXPONENTIAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#backoff_mode ClouddeployAutomation#backoff_mode}
        '''
        result = self._values.get("backoff_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait(self) -> typing.Optional[builtins.str]:
        '''Optional.

        How long to wait for the first retry. Default is 0, and the maximum value is 14d. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#wait ClouddeployAutomation#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0702fbdd91c8ca8dada680666bdebdbd6e53a72eabebdcfc0d78a4586faa632b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__850fae33bde27192d966585b19dd14d4cc769eefb91fa49b5de7fa4cfa4cdfc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backoffMode")
    def backoff_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backoffMode"))

    @backoff_mode.setter
    def backoff_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85a38e106323ba7bbe3d0629ad3975fe878e71b7b35a2ef66f872153ad9e2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backoffMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wait"))

    @wait.setter
    def wait(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d943a91c14b5939deb33227eaad7073e4b23792df002180fdbf921a191fb37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98ac667a55524c07f33ab86fb0a51aacad6e17ada0b7cd20070b6e49f214a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback",
    jsii_struct_bases=[],
    name_mapping={
        "destination_phase": "destinationPhase",
        "disable_rollback_if_rollout_pending": "disableRollbackIfRolloutPending",
    },
)
class ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback:
    def __init__(
        self,
        *,
        destination_phase: typing.Optional[builtins.str] = None,
        disable_rollback_if_rollout_pending: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param destination_phase: Optional. The starting phase ID for the Rollout. If unspecified, the Rollout will start in the stable phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        :param disable_rollback_if_rollout_pending: Optional. If pending rollout exists on the target, the rollback operation will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#disable_rollback_if_rollout_pending ClouddeployAutomation#disable_rollback_if_rollout_pending}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2680c99d09754ee4dafc4b2a2effe8e108ee7fb9dacb4cce6ad5055e29890564)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        '''
        result = self._values.get("destination_phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_rollback_if_rollout_pending(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If pending rollout exists on the target, the rollback operation will be aborted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#disable_rollback_if_rollout_pending ClouddeployAutomation#disable_rollback_if_rollout_pending}
        '''
        result = self._values.get("disable_rollback_if_rollout_pending")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3de5009e817ccd49e08608e58215e47add75500648c59c5abff9d006f15431ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e21fea05f8abae98244a26cd7ddb3235b838dd12928bff497adbcc7813a1beb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ee1dca2fbbe81ed0c38e28312fd5ef0427efce8eb5497f52aeef601b77f387c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableRollbackIfRolloutPending", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b453575372cae8cc798a0441a57f73122dd7379fd0ca081ca7c6c9ec0200c97e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesTimedPromoteReleaseRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "schedule": "schedule",
        "time_zone": "timeZone",
        "destination_phase": "destinationPhase",
        "destination_target_id": "destinationTargetId",
    },
)
class ClouddeployAutomationRulesTimedPromoteReleaseRule:
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
        :param id: Required. ID of the rule. This id must be unique in the 'Automation' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: Required. Schedule in crontab format. e.g. '0 9 * * 1' for every Monday at 9am. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#schedule ClouddeployAutomation#schedule}
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#time_zone ClouddeployAutomation#time_zone}
        :param destination_phase: Optional. The starting phase of the rollout created by this rule. Default to the first phase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        :param destination_target_id: Optional. The ID of the stage in the pipeline to which this Release is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following: - The last segment of a target name - "@next", the next target in the promotion sequence" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_target_id ClouddeployAutomation#destination_target_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af84f94134588c804c445787df94c4f6a0434d25942fd36c061ce76fddded40)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Required. Schedule in crontab format. e.g. '0 9 * * 1' for every Monday at 9am.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#schedule ClouddeployAutomation#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#time_zone ClouddeployAutomation#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_phase(self) -> typing.Optional[builtins.str]:
        '''Optional. The starting phase of the rollout created by this rule. Default to the first phase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_phase ClouddeployAutomation#destination_phase}
        '''
        result = self._values.get("destination_phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_target_id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The ID of the stage in the pipeline to which this Release is deploying. If unspecified, default it to the next stage in the promotion flow. The value of this field could be one of the following:

        - The last segment of a target name
        - "@next", the next target in the promotion sequence"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#destination_target_id ClouddeployAutomation#destination_target_id}
        '''
        result = self._values.get("destination_target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationRulesTimedPromoteReleaseRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eaf51289e6d30eb86c090952759aa4f92328ea292a491dd65945f7c804272fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f1a372a06ff55674392e8ad3f9a059e8a3884af32c6be69f89c1ff19cc36e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationTargetId")
    def destination_target_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationTargetId"))

    @destination_target_id.setter
    def destination_target_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1fe64cf3fc37aa3b434f2133a657ca4db88f025b86152046645ee313025380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationTargetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111222a1c95d6cf4c6ef10d0acb200d2946f2325dc82d5a468ed8036f900576c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162df256db0d53edccae3882a327d2b4f92686bccfa1a071d9eca1c3735acab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abef933cd51617017d14debea3911c11c36c544ccc9bda94bbb60a1549614398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployAutomationRulesTimedPromoteReleaseRule]:
        return typing.cast(typing.Optional[ClouddeployAutomationRulesTimedPromoteReleaseRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationRulesTimedPromoteReleaseRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a256025428e31775d3d689abf65864302d225181b5ab2986f2cad2833c711b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationSelector",
    jsii_struct_bases=[],
    name_mapping={"targets": "targets"},
)
class ClouddeployAutomationSelector:
    def __init__(
        self,
        *,
        targets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationSelectorTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#targets ClouddeployAutomation#targets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1fd35c9c5fad5ee5f98b07b38ad7b0f51757a15d2fba30001cff2e9325a292)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
        }

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationSelectorTargets"]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#targets ClouddeployAutomation#targets}
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationSelectorTargets"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0871f01cc21a405ab09857adc9dd35ed5dfeb56a188318b8dc5e614133a3b5dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployAutomationSelectorTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73e2fbf9d8e3f674dc054107d63d64ddafcf92ec7b846e0e2ebdfa1fd709df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "ClouddeployAutomationSelectorTargetsList":
        return typing.cast("ClouddeployAutomationSelectorTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationSelectorTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployAutomationSelectorTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployAutomationSelector]:
        return typing.cast(typing.Optional[ClouddeployAutomationSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployAutomationSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66f7480acffcf499e658e2c3536ea11a168e36de0ee33238c547dc9fa20411a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationSelectorTargets",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "labels": "labels"},
)
class ClouddeployAutomationSelectorTargets:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: ID of the 'Target'. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Target labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#labels ClouddeployAutomation#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15df7da09cfe5f4c7d8feb1eb6dbab0316673ab2ec4e9775f0eff7f6ab5e84e0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#id ClouddeployAutomation#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Target labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#labels ClouddeployAutomation#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationSelectorTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationSelectorTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationSelectorTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff1a88b33b31a5cd6d42548c50bddce5a823ecd477ae8d58bdba915921ef0468)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployAutomationSelectorTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c6bc1f5c8f124f3ce7a871d6ed464fceef8ba1a0af36799a30c473071ecfd1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployAutomationSelectorTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d437307d19b965de467565aadc2a87dba325df33299adefd0d2b7ad9817d1ddd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ce3db635dae417b7f3bb1baad2f893eafd7c0d5c50d7e2c4cd2b830a4df8136)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74d775306f091bc2bd3d18f129ac5b74da66d7577ddda493f9b8d9df89910728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationSelectorTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationSelectorTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationSelectorTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b898e1c48ed344b55c189fe1a50d44a7ea7fba8ad591d4c96e1d5fb7d3d0d4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployAutomationSelectorTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationSelectorTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d84a9648a3aaf245c5399359fdb4ff93fa770f0a60dec3cae0baf31eb34ff1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d717273ab05da2b725153b8aeb67ad23377d9ad2e2ea8a52375924aad85038f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d74451a6d56faacd723e2b4f2ff11fce71306724fb89799d68f495307bd496c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationSelectorTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationSelectorTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationSelectorTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55c257ba363cf9d24adb7d96b113f682fc874a22fbceff2f3ebf9efbc5e9d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddeployAutomationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#create ClouddeployAutomation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#delete ClouddeployAutomation#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#update ClouddeployAutomation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbcbc3ea7c727d07c3579b458f850cba5d2ff0c6a358db00c5cdf9b819a5558b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#create ClouddeployAutomation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#delete ClouddeployAutomation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_automation#update ClouddeployAutomation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployAutomationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployAutomationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployAutomation.ClouddeployAutomationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e62367fa6d4dd1aa4bac487ef739bebd834d7ee226e77eeefcdf9478e56321e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf88a9bebfe4dee08e909186ac6b02c6b16368721fc9d20f9393124fc9f69344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79616fa8a9a0b62fffc348c1f6dee0711e6de4b51992f7940d5b73d2a9696dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda09ee6e657fe8bab1bcac77d914d9ca7c6c89de1b60f63a6ed78bce6b4a46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402029e5b55228648276614a82907a0db8de00d5c27ddb2c6759829c523a1115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ClouddeployAutomation",
    "ClouddeployAutomationConfig",
    "ClouddeployAutomationRules",
    "ClouddeployAutomationRulesAdvanceRolloutRule",
    "ClouddeployAutomationRulesAdvanceRolloutRuleOutputReference",
    "ClouddeployAutomationRulesList",
    "ClouddeployAutomationRulesOutputReference",
    "ClouddeployAutomationRulesPromoteReleaseRule",
    "ClouddeployAutomationRulesPromoteReleaseRuleOutputReference",
    "ClouddeployAutomationRulesRepairRolloutRule",
    "ClouddeployAutomationRulesRepairRolloutRuleOutputReference",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhases",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesList",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesOutputReference",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetryOutputReference",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback",
    "ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollbackOutputReference",
    "ClouddeployAutomationRulesTimedPromoteReleaseRule",
    "ClouddeployAutomationRulesTimedPromoteReleaseRuleOutputReference",
    "ClouddeployAutomationSelector",
    "ClouddeployAutomationSelectorOutputReference",
    "ClouddeployAutomationSelectorTargets",
    "ClouddeployAutomationSelectorTargetsList",
    "ClouddeployAutomationSelectorTargetsOutputReference",
    "ClouddeployAutomationTimeouts",
    "ClouddeployAutomationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7aa8939f427f6bdf7e4d3c31afc8862f6dab70787b2c8c7591ccbbe45de66672(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    delivery_pipeline: builtins.str,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationRules, typing.Dict[builtins.str, typing.Any]]]],
    selector: typing.Union[ClouddeployAutomationSelector, typing.Dict[builtins.str, typing.Any]],
    service_account: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployAutomationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__82b25a33b884c5b5b0f225601d5d7a9ad6b4b10ec75eb9dc644d66c9d9482a22(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c03f8e900f493a0b6d602af7d1a90336add42bdafc68421fed110d81e67c83(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef752f4d194b7cd658d332e53b4f0263aa4f51cb8f5c7875585373e06fed96ec(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4af964fb6f130fc3530aead6713d095314d28f89c329c98669e6d2d8230591e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732692ecaaa7a85e626583ebb0925bc5822d1fcc2e73d04728a9150d88ffd10d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ad08163de01929b7dabcd25df381b51bf2725e13262ad9160292806376f180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70195901df586a5195b5b4bb76118cd167ef7048cd430c25242bdf75fe0b11b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63708260d863ca1cf4f585ed1376386c843dd393c480012bee010c99bc95a9e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c520fe84b0c12abbca783c2c25263dea7e17fc46c76f4969a363d76840476b3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180239bbf2101b1ab4ce364129329956ad3aa732ce8b89f37149e2d822bb9c6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaa192d8ddd78c23a32b24b650e0a5d40fba7034c81cd5d1ae8a96a67562c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3f754d412fbab43232a4deaf12ee45d9ba900744707b572f5a4b6099919f30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9d7aaeb92d7576c277c37e89d8b9c0fc78da858370056391bf233b3c47fdbb(
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
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationRules, typing.Dict[builtins.str, typing.Any]]]],
    selector: typing.Union[ClouddeployAutomationSelector, typing.Dict[builtins.str, typing.Any]],
    service_account: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployAutomationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5da34f27805d0170177814107088ab4d5186ae9e4435af726a0a3e91d131778(
    *,
    advance_rollout_rule: typing.Optional[typing.Union[ClouddeployAutomationRulesAdvanceRolloutRule, typing.Dict[builtins.str, typing.Any]]] = None,
    promote_release_rule: typing.Optional[typing.Union[ClouddeployAutomationRulesPromoteReleaseRule, typing.Dict[builtins.str, typing.Any]]] = None,
    repair_rollout_rule: typing.Optional[typing.Union[ClouddeployAutomationRulesRepairRolloutRule, typing.Dict[builtins.str, typing.Any]]] = None,
    timed_promote_release_rule: typing.Optional[typing.Union[ClouddeployAutomationRulesTimedPromoteReleaseRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16bc7ae9e7f27b656aa35e658f8e873b23753a79016214a445c7e8c350c7711f(
    *,
    id: builtins.str,
    source_phases: typing.Optional[typing.Sequence[builtins.str]] = None,
    wait: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5952b1c7d937ee84595616e0cacad2017e478306f82c61f0b3edb5fba5fdae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f71308f94c5b777bda49770b0bfb3110b2e8cc5b8d6cb13107b11c8115f906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccae325d4f88e44a138742653e0a891cba1b1828b16e8b967fdeb91b2237039(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566a81258f6ae5f0916dff06286ff1021879dc1a273207f871ed38f10c5d77d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecf4d0585b13216fc28fa13f83585fdb1ac405493701703cc42a723877fd6cd(
    value: typing.Optional[ClouddeployAutomationRulesAdvanceRolloutRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3fea8a1d70cb67e9fec2b97654abd5ff014be2b9976ec6afd9334f69116622(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23cf8d0e4ef5d07f19de74482a3b23e5c25ad5d0fee3475fd853a989b757cd7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7032b8a5c8dfbf14559573625c39bdbd20fb69287eae1ab853fe603c26f852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52ac1af59133043df0ca9ad77f4efdd9131547e10c6595f37f498064f766232(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dfa5471441c1fbb15afd6fdef4f9ed8febf8f1e5a854995f18400911bbeb2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353b9caa4b781d7ea9f79f393991473279950919152bf4e6b2626b9f428a6d5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f950b4b33dbd40ca9d7116cc9df2f485af70fac88fe4f1cf430228f68baa194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8fcc5452563aa539c118f23c674de6a7604f303bd59ff09a5ca2f3cf51ff94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e4667230722f895ffc58785f907aa909e4bd8bedfc5d87d48072ceecc151b2(
    *,
    id: builtins.str,
    destination_phase: typing.Optional[builtins.str] = None,
    destination_target_id: typing.Optional[builtins.str] = None,
    wait: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11509ff31bbfcd511f797076f4249172e031e9d7bc36c5adeb422f8ab122566a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dbf50560dd60fe31481db7628e676649896f454c85d693d3c4b48d6aad51c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db988146ec0beeceb83c34bb96bb3bd8ce1000d4e3544444cb3bbbc7d5aae3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fea08c79b13a68bf0a35959f038719e33ec046b1319978bbd91a5e5566b2def(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37aba57501d3e1a8f39e372f887bd066da5e90f87647ee9ad68c49a4471210e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef4ff297cbd6544f56105494f725ccfcaa4034c6bbd90feb7b5066bf2e1291f(
    value: typing.Optional[ClouddeployAutomationRulesPromoteReleaseRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c7bdee5891ca7742ded128b5d863866540e88edd3b79cb41332bc64d709585(
    *,
    id: builtins.str,
    jobs: typing.Optional[typing.Sequence[builtins.str]] = None,
    phases: typing.Optional[typing.Sequence[builtins.str]] = None,
    repair_phases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationRulesRepairRolloutRuleRepairPhases, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90bee06127379f530866ba360eefd016b01b0ed93c2246357cd20c10855bf95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a836bd699df4ec55a75daca608dcd153a3e391e18d997861839f73fab2f95e8f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationRulesRepairRolloutRuleRepairPhases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b0f2373abcab2fe4e59c5ebe27531e8bad36e67474f8d1025c8db6df701705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405387712c2d65866ae6d6c65f4744bd6bbf745a2c5166259d09ca4e5fedf872(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f87d8448691b4f6cce709aee32b492f6dedcf54999ddb2e56593ef1ed286f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b125742b9147d64338c98c9a743f70abd15a07a20a0869a5dbf32c80adb90280(
    value: typing.Optional[ClouddeployAutomationRulesRepairRolloutRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafd710b54e66a8c86952ab9cea1b10af4ddb6617021af1b407cbbed00cacaad(
    *,
    retry: typing.Optional[typing.Union[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry, typing.Dict[builtins.str, typing.Any]]] = None,
    rollback: typing.Optional[typing.Union[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f564dd19953d5e5aacddd5350afe3859dc954ee15f0164a962c799c693e7016e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1646e37b3b8554b1cb112f54fc1a7ade3e4289945cb73f9bc3a6b56b43517b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe8dbe5c4b0a341ab92fbfa3396bacfb8ab496d20e2756d933e677417020ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af93b5fdc30f985bee5e4e374388a5931949b02bbf55299c0559211048187747(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76481d1e0ab53cf092970d7a4209e7deba9da734541a67eb80389601e9dcb67a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd2181673a2c65efc96440e13750debf8f7ad431eb279b4595f516f3f753ee9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a513c1ddb2aa1d0e4d2673b3a8b30d0720e55a0c385cad58b00be979ecd587e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c747311f15c795921f0f95a1604a4a82d40353fe21d8b242f0339579b506d78c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationRulesRepairRolloutRuleRepairPhases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3c5715adc1703dd5b27e763993ba64be42ad71a66abaab1346beddd727113b(
    *,
    attempts: builtins.str,
    backoff_mode: typing.Optional[builtins.str] = None,
    wait: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0702fbdd91c8ca8dada680666bdebdbd6e53a72eabebdcfc0d78a4586faa632b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850fae33bde27192d966585b19dd14d4cc769eefb91fa49b5de7fa4cfa4cdfc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85a38e106323ba7bbe3d0629ad3975fe878e71b7b35a2ef66f872153ad9e2bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d943a91c14b5939deb33227eaad7073e4b23792df002180fdbf921a191fb37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98ac667a55524c07f33ab86fb0a51aacad6e17ada0b7cd20070b6e49f214a4b(
    value: typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRetry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2680c99d09754ee4dafc4b2a2effe8e108ee7fb9dacb4cce6ad5055e29890564(
    *,
    destination_phase: typing.Optional[builtins.str] = None,
    disable_rollback_if_rollout_pending: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de5009e817ccd49e08608e58215e47add75500648c59c5abff9d006f15431ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21fea05f8abae98244a26cd7ddb3235b838dd12928bff497adbcc7813a1beb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee1dca2fbbe81ed0c38e28312fd5ef0427efce8eb5497f52aeef601b77f387c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b453575372cae8cc798a0441a57f73122dd7379fd0ca081ca7c6c9ec0200c97e(
    value: typing.Optional[ClouddeployAutomationRulesRepairRolloutRuleRepairPhasesRollback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af84f94134588c804c445787df94c4f6a0434d25942fd36c061ce76fddded40(
    *,
    id: builtins.str,
    schedule: builtins.str,
    time_zone: builtins.str,
    destination_phase: typing.Optional[builtins.str] = None,
    destination_target_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eaf51289e6d30eb86c090952759aa4f92328ea292a491dd65945f7c804272fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f1a372a06ff55674392e8ad3f9a059e8a3884af32c6be69f89c1ff19cc36e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1fe64cf3fc37aa3b434f2133a657ca4db88f025b86152046645ee313025380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111222a1c95d6cf4c6ef10d0acb200d2946f2325dc82d5a468ed8036f900576c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162df256db0d53edccae3882a327d2b4f92686bccfa1a071d9eca1c3735acab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abef933cd51617017d14debea3911c11c36c544ccc9bda94bbb60a1549614398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a256025428e31775d3d689abf65864302d225181b5ab2986f2cad2833c711b6(
    value: typing.Optional[ClouddeployAutomationRulesTimedPromoteReleaseRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1fd35c9c5fad5ee5f98b07b38ad7b0f51757a15d2fba30001cff2e9325a292(
    *,
    targets: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationSelectorTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0871f01cc21a405ab09857adc9dd35ed5dfeb56a188318b8dc5e614133a3b5dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73e2fbf9d8e3f674dc054107d63d64ddafcf92ec7b846e0e2ebdfa1fd709df2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployAutomationSelectorTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66f7480acffcf499e658e2c3536ea11a168e36de0ee33238c547dc9fa20411a(
    value: typing.Optional[ClouddeployAutomationSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15df7da09cfe5f4c7d8feb1eb6dbab0316673ab2ec4e9775f0eff7f6ab5e84e0(
    *,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1a88b33b31a5cd6d42548c50bddce5a823ecd477ae8d58bdba915921ef0468(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c6bc1f5c8f124f3ce7a871d6ed464fceef8ba1a0af36799a30c473071ecfd1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d437307d19b965de467565aadc2a87dba325df33299adefd0d2b7ad9817d1ddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce3db635dae417b7f3bb1baad2f893eafd7c0d5c50d7e2c4cd2b830a4df8136(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d775306f091bc2bd3d18f129ac5b74da66d7577ddda493f9b8d9df89910728(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b898e1c48ed344b55c189fe1a50d44a7ea7fba8ad591d4c96e1d5fb7d3d0d4e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployAutomationSelectorTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d84a9648a3aaf245c5399359fdb4ff93fa770f0a60dec3cae0baf31eb34ff1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d717273ab05da2b725153b8aeb67ad23377d9ad2e2ea8a52375924aad85038f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d74451a6d56faacd723e2b4f2ff11fce71306724fb89799d68f495307bd496c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55c257ba363cf9d24adb7d96b113f682fc874a22fbceff2f3ebf9efbc5e9d0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationSelectorTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbcbc3ea7c727d07c3579b458f850cba5d2ff0c6a358db00c5cdf9b819a5558b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e62367fa6d4dd1aa4bac487ef739bebd834d7ee226e77eeefcdf9478e56321e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf88a9bebfe4dee08e909186ac6b02c6b16368721fc9d20f9393124fc9f69344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79616fa8a9a0b62fffc348c1f6dee0711e6de4b51992f7940d5b73d2a9696dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda09ee6e657fe8bab1bcac77d914d9ca7c6c89de1b60f63a6ed78bce6b4a46d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402029e5b55228648276614a82907a0db8de00d5c27ddb2c6759829c523a1115(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployAutomationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
