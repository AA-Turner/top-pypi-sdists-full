r'''
# `google_clouddeploy_deploy_policy`

Refer to the Terraform Registry for docs: [`google_clouddeploy_deploy_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy).
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


class GoogleClouddeployDeployPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy google_clouddeploy_deploy_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicySelectors", typing.Dict[builtins.str, typing.Any]]]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy google_clouddeploy_deploy_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#location GoogleClouddeployDeployPolicy#location}
        :param name: Name of the 'DeployPolicy'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#name GoogleClouddeployDeployPolicy#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#rules GoogleClouddeployDeployPolicy#rules}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#selectors GoogleClouddeployDeployPolicy#selectors}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#annotations GoogleClouddeployDeployPolicy#annotations}
        :param description: Optional. Description of the 'DeployPolicy'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#description GoogleClouddeployDeployPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#project GoogleClouddeployDeployPolicy#project}.
        :param suspended: Optional. When suspended, the policy will not prevent actions from occurring, even if the action violates the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#suspended GoogleClouddeployDeployPolicy#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#timeouts GoogleClouddeployDeployPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5b3dd484e1c6e54eada24dfaee86cac78adb7851efe6e640580a6ccd6bec3e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleClouddeployDeployPolicyConfig(
            location=location,
            name=name,
            rules=rules,
            selectors=selectors,
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
        '''Generates CDKTF code for importing a GoogleClouddeployDeployPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleClouddeployDeployPolicy to import.
        :param import_from_id: The id of the existing GoogleClouddeployDeployPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleClouddeployDeployPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c9008f13dfb492dfb3fc6a89b197ef13c19d28eff0578edd6bcdcd4b8d5918)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd6fcd38ae1a0bf6c94d92ee768165fec7350e94829e7918aad41c1fcf25778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicySelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7489a25df16d8df71f74ee46425e961b713914bafb9414e2cec7cd8f672ebb57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#create GoogleClouddeployDeployPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#delete GoogleClouddeployDeployPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#update GoogleClouddeployDeployPolicy#update}.
        '''
        value = GoogleClouddeployDeployPolicyTimeouts(
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
    def rules(self) -> "GoogleClouddeployDeployPolicyRulesList":
        return typing.cast("GoogleClouddeployDeployPolicyRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> "GoogleClouddeployDeployPolicySelectorsList":
        return typing.cast("GoogleClouddeployDeployPolicySelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleClouddeployDeployPolicyTimeoutsOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicySelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicySelectors"]]], jsii.get(self, "selectorsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployDeployPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleClouddeployDeployPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c0228e376326b42605d6070d044599754dfeb0e963856e17dde62ee528106f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1970f9e434b8513080cf2eff17e0de4ec61186826bfcacb09ea5f16311ad95fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175772635ff786bf56a338448522fa137d5e7aa799b0816a2f68332ad2fe405e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28149ca78b6d6582f40315fb6f81bc4651a086a5000d4ffd122c92880479d35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f13764d24293e624c93eea9e3824feb0d10953c5a12d38f0e4572ec808c673b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effe422c5812f9e1a7f2b020c3ffcd70615b28bf1ac3e3dbba3bfc87b75efcc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f886eee6967a998903ef2fd949bb1efd90ecff67db455f697beb4a6b3017b4e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__75dab0b57eae957d5913bde0056be8471dc9b03445bf54a92456e2d3eacd8d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "rules": "rules",
        "selectors": "selectors",
        "annotations": "annotations",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "suspended": "suspended",
        "timeouts": "timeouts",
    },
)
class GoogleClouddeployDeployPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicySelectors", typing.Dict[builtins.str, typing.Any]]]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#location GoogleClouddeployDeployPolicy#location}
        :param name: Name of the 'DeployPolicy'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#name GoogleClouddeployDeployPolicy#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#rules GoogleClouddeployDeployPolicy#rules}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#selectors GoogleClouddeployDeployPolicy#selectors}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#annotations GoogleClouddeployDeployPolicy#annotations}
        :param description: Optional. Description of the 'DeployPolicy'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#description GoogleClouddeployDeployPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#project GoogleClouddeployDeployPolicy#project}.
        :param suspended: Optional. When suspended, the policy will not prevent actions from occurring, even if the action violates the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#suspended GoogleClouddeployDeployPolicy#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#timeouts GoogleClouddeployDeployPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleClouddeployDeployPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ba198cb4e0976ded9008ceabbe7904df05a1cfaf71e483361df99e7e3b085d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument suspended", value=suspended, expected_type=type_hints["suspended"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "rules": rules,
            "selectors": selectors,
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#location GoogleClouddeployDeployPolicy#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the 'DeployPolicy'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#name GoogleClouddeployDeployPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#rules GoogleClouddeployDeployPolicy#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRules"]], result)

    @builtins.property
    def selectors(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicySelectors"]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#selectors GoogleClouddeployDeployPolicy#selectors}
        '''
        result = self._values.get("selectors")
        assert result is not None, "Required property 'selectors' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicySelectors"]], result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#annotations GoogleClouddeployDeployPolicy#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the 'DeployPolicy'. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#description GoogleClouddeployDeployPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#project GoogleClouddeployDeployPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When suspended, the policy will not prevent actions from occurring, even if the action violates the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#suspended GoogleClouddeployDeployPolicy#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleClouddeployDeployPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#timeouts GoogleClouddeployDeployPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRules",
    jsii_struct_bases=[],
    name_mapping={"rollout_restriction": "rolloutRestriction"},
)
class GoogleClouddeployDeployPolicyRules:
    def __init__(
        self,
        *,
        rollout_restriction: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestriction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param rollout_restriction: rollout_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#rollout_restriction GoogleClouddeployDeployPolicy#rollout_restriction}
        '''
        if isinstance(rollout_restriction, dict):
            rollout_restriction = GoogleClouddeployDeployPolicyRulesRolloutRestriction(**rollout_restriction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f76c77c7ad283890a8de50760794efc9b5e5d554f06250fa669277da2735e5)
            check_type(argname="argument rollout_restriction", value=rollout_restriction, expected_type=type_hints["rollout_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rollout_restriction is not None:
            self._values["rollout_restriction"] = rollout_restriction

    @builtins.property
    def rollout_restriction(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestriction"]:
        '''rollout_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#rollout_restriction GoogleClouddeployDeployPolicy#rollout_restriction}
        '''
        result = self._values.get("rollout_restriction")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestriction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__911fc3d72ebf34d17f1de27037ad897aaec9ee75ae224677e9371b754c598d94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeployPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381f4f627f5c72e71b9d7973b9409c8de8adfc33f06d34667adee90fcaa1e4b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeployPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb684fc9dbf888d0c729a1661caa75c46d8d31aa2b9682dddd4f667cb4cbecf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__021d8e9eb16a51542155fb1b61d8d5abf70fc0f28b90e8a2bd95696f910ed515)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f63bbabbe2e2980ba1337acfa5b4f240c6bab9bf4f1610eb17c6a8784f804486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac144fd86279d759ef839573c592fc7dc60373f0291c5fecd2c79f24e721aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9d6315d27b6a1c0b3ddc44e2ca140a6c3d356f51e40df3adba0f35ab1d766d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRolloutRestriction")
    def put_rollout_restriction(
        self,
        *,
        id: builtins.str,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        invokers: typing.Optional[typing.Sequence[builtins.str]] = None,
        time_windows: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'DeployPolicy' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param actions: Optional. Rollout actions to be restricted as part of the policy. If left empty, all actions will be restricted. Possible values: ["ADVANCE", "APPROVE", "CANCEL", "CREATE", "IGNORE_JOB", "RETRY_JOB", "ROLLBACK", "TERMINATE_JOBRUN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#actions GoogleClouddeployDeployPolicy#actions}
        :param invokers: Optional. What invoked the action. If left empty, all invoker types will be restricted. Possible values: ["USER", "DEPLOY_AUTOMATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#invokers GoogleClouddeployDeployPolicy#invokers}
        :param time_windows: time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#time_windows GoogleClouddeployDeployPolicy#time_windows}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestriction(
            id=id, actions=actions, invokers=invokers, time_windows=time_windows
        )

        return typing.cast(None, jsii.invoke(self, "putRolloutRestriction", [value]))

    @jsii.member(jsii_name="resetRolloutRestriction")
    def reset_rollout_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="rolloutRestriction")
    def rollout_restriction(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionOutputReference", jsii.get(self, "rolloutRestriction"))

    @builtins.property
    @jsii.member(jsii_name="rolloutRestrictionInput")
    def rollout_restriction_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestriction"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestriction"], jsii.get(self, "rolloutRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e4654409c366f7a76497852e77e9b3e17ccf24bbf38d8f4990ca622aed4d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "actions": "actions",
        "invokers": "invokers",
        "time_windows": "timeWindows",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestriction:
    def __init__(
        self,
        *,
        id: builtins.str,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        invokers: typing.Optional[typing.Sequence[builtins.str]] = None,
        time_windows: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'DeployPolicy' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param actions: Optional. Rollout actions to be restricted as part of the policy. If left empty, all actions will be restricted. Possible values: ["ADVANCE", "APPROVE", "CANCEL", "CREATE", "IGNORE_JOB", "RETRY_JOB", "ROLLBACK", "TERMINATE_JOBRUN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#actions GoogleClouddeployDeployPolicy#actions}
        :param invokers: Optional. What invoked the action. If left empty, all invoker types will be restricted. Possible values: ["USER", "DEPLOY_AUTOMATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#invokers GoogleClouddeployDeployPolicy#invokers}
        :param time_windows: time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#time_windows GoogleClouddeployDeployPolicy#time_windows}
        '''
        if isinstance(time_windows, dict):
            time_windows = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows(**time_windows)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9f81b0707ead221f2e8ed5c4aa5de6978e932420f01ae6d2202a6939771117)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument invokers", value=invokers, expected_type=type_hints["invokers"])
            check_type(argname="argument time_windows", value=time_windows, expected_type=type_hints["time_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if actions is not None:
            self._values["actions"] = actions
        if invokers is not None:
            self._values["invokers"] = invokers
        if time_windows is not None:
            self._values["time_windows"] = time_windows

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        ID of the rule. This id must be unique in the 'DeployPolicy' resource to which this rule belongs. The format is 'a-z{0,62}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Rollout actions to be restricted as part of the policy. If left empty, all actions will be restricted. Possible values: ["ADVANCE", "APPROVE", "CANCEL", "CREATE", "IGNORE_JOB", "RETRY_JOB", "ROLLBACK", "TERMINATE_JOBRUN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#actions GoogleClouddeployDeployPolicy#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def invokers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. What invoked the action. If left empty, all invoker types will be restricted. Possible values: ["USER", "DEPLOY_AUTOMATION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#invokers GoogleClouddeployDeployPolicy#invokers}
        '''
        result = self._values.get("invokers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def time_windows(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"]:
        '''time_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#time_windows GoogleClouddeployDeployPolicy#time_windows}
        '''
        result = self._values.get("time_windows")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__451830136f440a66661b6cbe14801d12ca9b92fd81bac47af08153961ce5ae9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimeWindows")
    def put_time_windows(
        self,
        *,
        time_zone: builtins.str,
        one_time_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#time_zone GoogleClouddeployDeployPolicy#time_zone}
        :param one_time_windows: one_time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#one_time_windows GoogleClouddeployDeployPolicy#one_time_windows}
        :param weekly_windows: weekly_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#weekly_windows GoogleClouddeployDeployPolicy#weekly_windows}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows(
            time_zone=time_zone,
            one_time_windows=one_time_windows,
            weekly_windows=weekly_windows,
        )

        return typing.cast(None, jsii.invoke(self, "putTimeWindows", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetInvokers")
    def reset_invokers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvokers", []))

    @jsii.member(jsii_name="resetTimeWindows")
    def reset_time_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeWindows", []))

    @builtins.property
    @jsii.member(jsii_name="timeWindows")
    def time_windows(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference", jsii.get(self, "timeWindows"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="invokersInput")
    def invokers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "invokersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowsInput")
    def time_windows_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"], jsii.get(self, "timeWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c469f2365908da386714b6b4b41cde6e0b4f1f236f1010759a547eb0559039f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7a23ee74e6952b3a121194e42ee9efab529490b2679a7ebc3f566c44ce752e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invokers")
    def invokers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "invokers"))

    @invokers.setter
    def invokers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3706e83e50d69c7c752153afc9bd005f61d9a623c1f73ee7196378bd34d995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestriction]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestriction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestriction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7a9db1ac62c38bad7753343903e5338275d003b7e521ba0c2c625efe1016fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "one_time_windows": "oneTimeWindows",
        "weekly_windows": "weeklyWindows",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        one_time_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#time_zone GoogleClouddeployDeployPolicy#time_zone}
        :param one_time_windows: one_time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#one_time_windows GoogleClouddeployDeployPolicy#one_time_windows}
        :param weekly_windows: weekly_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#weekly_windows GoogleClouddeployDeployPolicy#weekly_windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6617a42532704a956923cf0f18978ba1a87c2c09b6e5988bdd224e27d634adf3)
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument one_time_windows", value=one_time_windows, expected_type=type_hints["one_time_windows"])
            check_type(argname="argument weekly_windows", value=weekly_windows, expected_type=type_hints["weekly_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_zone": time_zone,
        }
        if one_time_windows is not None:
            self._values["one_time_windows"] = one_time_windows
        if weekly_windows is not None:
            self._values["weekly_windows"] = weekly_windows

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#time_zone GoogleClouddeployDeployPolicy#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def one_time_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows"]]]:
        '''one_time_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#one_time_windows GoogleClouddeployDeployPolicy#one_time_windows}
        '''
        result = self._values.get("one_time_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows"]]], result)

    @builtins.property
    def weekly_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]]:
        '''weekly_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#weekly_windows GoogleClouddeployDeployPolicy#weekly_windows}
        '''
        result = self._values.get("weekly_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows",
    jsii_struct_bases=[],
    name_mapping={
        "end_date": "endDate",
        "end_time": "endTime",
        "start_date": "startDate",
        "start_time": "startTime",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows:
    def __init__(
        self,
        *,
        end_date: typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate", typing.Dict[builtins.str, typing.Any]],
        end_time: typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime", typing.Dict[builtins.str, typing.Any]],
        start_date: typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate", typing.Dict[builtins.str, typing.Any]],
        start_time: typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#end_date GoogleClouddeployDeployPolicy#end_date}
        :param end_time: end_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#end_time GoogleClouddeployDeployPolicy#end_time}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#start_date GoogleClouddeployDeployPolicy#start_date}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#start_time GoogleClouddeployDeployPolicy#start_time}
        '''
        if isinstance(end_date, dict):
            end_date = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate(**end_date)
        if isinstance(end_time, dict):
            end_time = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime(**end_time)
        if isinstance(start_date, dict):
            start_date = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate(**start_date)
        if isinstance(start_time, dict):
            start_time = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa853fbae7ebb32b458c8113f6b65e9f56546a77a07dc2c0088ddbbd2a8705d1)
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date": end_date,
            "end_time": end_time,
            "start_date": start_date,
            "start_time": start_time,
        }

    @builtins.property
    def end_date(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate":
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#end_date GoogleClouddeployDeployPolicy#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate", result)

    @builtins.property
    def end_time(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime":
        '''end_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#end_time GoogleClouddeployDeployPolicy#end_time}
        '''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime", result)

    @builtins.property
    def start_date(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#start_date GoogleClouddeployDeployPolicy#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate", result)

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#start_time GoogleClouddeployDeployPolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#day GoogleClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#month GoogleClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#year GoogleClouddeployDeployPolicy#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a7daa2c3f7211cd4adc8caeea31a771a386826294d545bb45e05f1af58beb7)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month. Must be from 1 to 31 and valid for the year and month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#day GoogleClouddeployDeployPolicy#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#month GoogleClouddeployDeployPolicy#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#year GoogleClouddeployDeployPolicy#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c669ecbe5d7b88f128e9a9e1f35ef47c9bc4470777a5c72a4c9dd4cb43351fb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d65ee96a00827f30c1856be54c9e28930e7078818bab3d6b77483b4245bb1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a3fb204e12b69a07abd9867b0e1aa2ce52ad8e9417a8101e280f931cd2339a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54471af8dab67ca91e02c52eda592ca844bd40834bde94ad955c47d28bd93b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ecbee0cffa52f9ff04aeb3a1c213982e2976d8cd6a2c0aafd0349ffecc81d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb62231d09b03d46f4b3257274e2b7700dea6f3f3f0ae9336e8e18a02347ced)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a887d44350365e02e7f1718642ef3aac2e3224e4244d85bc6485e30e88629f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3633a5a2ebc56ca05d21438de5ecf21ad0839a05611b4fa5ba01a589974ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f52f2a4588ac7144419c7885d19de097549de165650792cdde4db5ada5402f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc02195677b3e21bcc75e6780d99d2f77bdaa0b8b22bc065853049a26d0831b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab016bd06d38b1521a341f831296748db4660e1e6a7b6797a8d489fa564f4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514ef7d2a648bdf848a935bc03e04e63ba4920c913c64287c1234fafa7f21f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38145838bda942e22733a43857eeee448a5a3fde8943bc072093da5fdc7f1e92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694ff0ddfd1eb227a1650eab26e1de9bc6f02268d7dd0d08c502fc46d06ddfa4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296a38f1cc4d81451758ea72691e8bb2798862293ff8a3756b565ccf544948af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f30c3c90043d0322ee2014de3cd4db5056019c4d2ff3ffedf4087e6c03a168a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f321d1207cf90176ac1c6400ef7207b3cae7a020efbe7682bc14326161038df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8f66a9b3becc516fcd27d0149a5177ff384ec89f072ce60bda678a5b9e9c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc48b732698e73659b140a531ce3109bfc882b834d3065f272aab66e17e938b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEndDate")
    def put_end_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#day GoogleClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#month GoogleClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#year GoogleClouddeployDeployPolicy#year}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putEndDate", [value]))

    @jsii.member(jsii_name="putEndTime")
    def put_end_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putEndTime", [value]))

    @jsii.member(jsii_name="putStartDate")
    def put_start_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#day GoogleClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#month GoogleClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#year GoogleClouddeployDeployPolicy#year}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(
        self,
    ) -> GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference:
        return typing.cast(GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(
        self,
    ) -> GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference:
        return typing.cast(GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59e1b2a087d4c8490221eba63e47df49a1bc352c47b96651368ad59db2e90c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#day GoogleClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#month GoogleClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#year GoogleClouddeployDeployPolicy#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e2af5eac8ed76ed0878f71446f4ec56661d059149e88447b4c685a142b26af)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month.

        Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#day GoogleClouddeployDeployPolicy#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Must be from 1 to 12, or 0 to specify a year without a month and day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#month GoogleClouddeployDeployPolicy#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#year GoogleClouddeployDeployPolicy#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07028ea0f189fec12e42175914eecf8c18409c88dcf69413be9c35683ba72c66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ae75f16fd00b78ed3534ad2f00301a1a09288c2254482126bd4f0386c0560b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc0e7129abef05eafbcbe83e05b9a6aab57774df1c81ff174db21e8ba080bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01286eff24f8dd38797c4b35d71c3237c52ec806ab0f9b4cc1ec59464087d604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289b39b586706fe56d7d24cfed23922889f1ec16099ebe522d22a93e8ec9a576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefcea184ac69c189c4c67b18b41c7686a7e2ec412b0724a2d300a17d15185be)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87942b9e71c2c14bc395d7d1dec8cb0dd92abf67b579115d8beccf5f709cee81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab1dfb8b6fdf78e30653c6f82f4b39614f22e173f32d91837544025243fcc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7cb8f7ce56ffde664fd50ad02b57d62a47a00779372c2e0a77f1efed33c5fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8720b0ff551c37b2ee6e50f52c6f151347abbccddb0c6efbaa7ce3df5eacc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7495e3aad985244f08d738c4675567c9c347c9aaa613c88bf6ea514f3c90cabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7eb8966a1a3fdc9163ddb37878b226010ae6e5ef0c857c23c5f03343c9326a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97355cec76984059237764267e7e84b10a296a2d092f2628cf89fc803642c88d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOneTimeWindows")
    def put_one_time_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28730df09dccab02cf77a93f56f67136605f24f64b5acdbf8a3f14b0fb91b5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOneTimeWindows", [value]))

    @jsii.member(jsii_name="putWeeklyWindows")
    def put_weekly_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61426cbbeadb925ee10ce5a6c04a56222b96345929d12dd7b6389a535276ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeeklyWindows", [value]))

    @jsii.member(jsii_name="resetOneTimeWindows")
    def reset_one_time_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneTimeWindows", []))

    @jsii.member(jsii_name="resetWeeklyWindows")
    def reset_weekly_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyWindows", []))

    @builtins.property
    @jsii.member(jsii_name="oneTimeWindows")
    def one_time_windows(
        self,
    ) -> GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList:
        return typing.cast(GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList, jsii.get(self, "oneTimeWindows"))

    @builtins.property
    @jsii.member(jsii_name="weeklyWindows")
    def weekly_windows(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList":
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList", jsii.get(self, "weeklyWindows"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeWindowsInput")
    def one_time_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]], jsii.get(self, "oneTimeWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyWindowsInput")
    def weekly_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]], jsii.get(self, "weeklyWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b52f5ef29d27f78d22c23962b6e989b049f12e9bca4ae63b91f0798779ca08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffef0ff980f66e518c366bc80afc0d89654d5b9234fbafbd678573106be577f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows:
    def __init__(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_time: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[typing.Union["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param days_of_week: Optional. Days of week. If left empty, all days of the week will be included. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#days_of_week GoogleClouddeployDeployPolicy#days_of_week}
        :param end_time: end_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#end_time GoogleClouddeployDeployPolicy#end_time}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#start_time GoogleClouddeployDeployPolicy#start_time}
        '''
        if isinstance(end_time, dict):
            end_time = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime(**end_time)
        if isinstance(start_time, dict):
            start_time = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__386bd7f25c8d9c40227dc62342acdb875dfe9a36c863bd196163a3d0b6cc7a94)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Days of week. If left empty, all days of the week will be included. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#days_of_week GoogleClouddeployDeployPolicy#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def end_time(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime"]:
        '''end_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#end_time GoogleClouddeployDeployPolicy#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime"], result)

    @builtins.property
    def start_time(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"]:
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#start_time GoogleClouddeployDeployPolicy#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e74bf6baa19c0af497d67ca62e2168d02352548b2ec70d02ee56e44b4b98b4)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f1e1d7aaa965551794676f80c4446062d398198e14d955be256969e00a7078)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d260c238b191883ded86fbc4e1e0025399177fb77255b8903c8a93a314a7bc72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f221292f054e3e2799450a749144e83bdd98dbced0a252407df704f5b75f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d791d30a4ab9805b7dfcb082a2164ab353d5c24dd31db539f1f2ad05fc55b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d737e4d18dce8424aa0cfa24bed092fd2371d955a9947b9c8be1de3bc8768c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a48bef9200bc79c7a52e86cb520df27e8bffa9a412ece61b334d85bf29df2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ec4f14df17ec3fe48a1f48752960538397c6abc4ef70ed2c1c41a0e3d111d12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407f24700daa93f50678d2fcd15ac63c0b711400dde1537b4fbccd8b35ba66d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aafd0c99347acfab9e15fd4ce992cddb761604c07af6a45c9a6b0a7e0acceae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c5a243e90c7f75bd629c70930aaa16dac0e284d4fbe7e025dda922f3341971)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b9f63848a4a25e00374d5c7b7dc51d69c1ed3579f877ed2c43c6b82d7d14e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df25e53e157d1776d055ba432e2b686829d85d5013f9f489021167182c9529c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c795b727314313d0c7b0a7726c2c6275a6ca2f107091eb8de81af907f73b8c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEndTime")
    def put_end_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putEndTime", [value]))

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        value = GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(
        self,
    ) -> GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference:
        return typing.cast(GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa976711087b01cbcd957e741a527db85560ca3bbaeec4d6ac95122a251dcff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f01da341f907623c1ff5dfe240626c37e6934b313feb0076d5078b7aeab98be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b557bdea088e6013ecd73a3ad59860d6e2866b3a8b01e6278eae54dc0c62c1d1)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#hours GoogleClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#minutes GoogleClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#nanos GoogleClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#seconds GoogleClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b61a6a276c6e4d83ff86322b7f0ff83fd6f7cd3762d01afc153c57dc4579ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a58dd8931e494e2a9138e64341e60ea7892962730734b2fca4dcd31d69e8cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255c38c239bdd71889c5878ac1c9a83c3e42337a3e5e8a122616777d1400adab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e935dabaaab562abf327f22c940deb8cc8ec9f63ebaf359f04d0e368f763e01e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e1eb45a482c72d5b91b699a13df820d5e18836f4c6840177c5de94fbb40527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9eb7575cb5822e5ec78c234be2a119771e89591e8a8597bfc332e842aa645ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectors",
    jsii_struct_bases=[],
    name_mapping={"delivery_pipeline": "deliveryPipeline", "target": "target"},
)
class GoogleClouddeployDeployPolicySelectors:
    def __init__(
        self,
        *,
        delivery_pipeline: typing.Optional[typing.Union["GoogleClouddeployDeployPolicySelectorsDeliveryPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Union["GoogleClouddeployDeployPolicySelectorsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param delivery_pipeline: delivery_pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#delivery_pipeline GoogleClouddeployDeployPolicy#delivery_pipeline}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#target GoogleClouddeployDeployPolicy#target}
        '''
        if isinstance(delivery_pipeline, dict):
            delivery_pipeline = GoogleClouddeployDeployPolicySelectorsDeliveryPipeline(**delivery_pipeline)
        if isinstance(target, dict):
            target = GoogleClouddeployDeployPolicySelectorsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fda9c144e7dedf36769dcd5191878dc2a178895c3fffeef127ad9a74933d3dc)
            check_type(argname="argument delivery_pipeline", value=delivery_pipeline, expected_type=type_hints["delivery_pipeline"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_pipeline is not None:
            self._values["delivery_pipeline"] = delivery_pipeline
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def delivery_pipeline(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicySelectorsDeliveryPipeline"]:
        '''delivery_pipeline block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#delivery_pipeline GoogleClouddeployDeployPolicy#delivery_pipeline}
        '''
        result = self._values.get("delivery_pipeline")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicySelectorsDeliveryPipeline"], result)

    @builtins.property
    def target(self) -> typing.Optional["GoogleClouddeployDeployPolicySelectorsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#target GoogleClouddeployDeployPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicySelectorsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicySelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectorsDeliveryPipeline",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "labels": "labels"},
)
class GoogleClouddeployDeployPolicySelectorsDeliveryPipeline:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the DeliveryPipeline. The value of this field could be one of the following: - The last segment of a pipeline name - "*", all delivery pipelines in a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: DeliveryPipeline labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d410c8048998632f95dcf79512fd3f70d935ff6443d4e6fc239559955b7db2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Optional.

        ID of the DeliveryPipeline. The value of this field could be one of the following:

        - The last segment of a pipeline name
        - "*", all delivery pipelines in a location

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''DeliveryPipeline labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicySelectorsDeliveryPipeline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22de548eaf8867e4f27eb1498a0d659d112a52e77b1ccec05a34becbc06a634a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__30ff8020df83943e6429f98885a5529ab8ef4cd3ccf4d76c635282e0df4918c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d07058621fbead25da48b160257cf6e4bc97f2600dae6fdd682a850941b33b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d57e94769d97addaa21ff4b5a5666231633c6b843488c4b98a613f9aa28bc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicySelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42926b94690f86af477f9d3535aa0d1d1e77c778a1ad3b6700478d1305de7b11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleClouddeployDeployPolicySelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b576364efb3bfacd6d28ba98feda1373007d98b04cf273766cc6fd02ec7dd866)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleClouddeployDeployPolicySelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6105730b0cf8176b111d036011b998a86503a8427fe8c0302e6b9670976ed1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b75aea0f23722bb2a18e4e81169d59d0715672a2b6f69906fa92723f4a126c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ae8f0dcd881fd0e90e57617e0a6c0ba68998e1d510732652f7c0e8b38371fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicySelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicySelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicySelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fe6ca801bc39a77f9c214b1831b4d8dfd5d4cd8fd97089a37fd670c60e36de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleClouddeployDeployPolicySelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__007bc7b733b98e78ed367bcc381ea3faeee482bb6a0215537343a2cc108f8795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDeliveryPipeline")
    def put_delivery_pipeline(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the DeliveryPipeline. The value of this field could be one of the following: - The last segment of a pipeline name - "*", all delivery pipelines in a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: DeliveryPipeline labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        value = GoogleClouddeployDeployPolicySelectorsDeliveryPipeline(
            id=id, labels=labels
        )

        return typing.cast(None, jsii.invoke(self, "putDeliveryPipeline", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: ID of the 'Target'. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Target labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        value = GoogleClouddeployDeployPolicySelectorsTarget(id=id, labels=labels)

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetDeliveryPipeline")
    def reset_delivery_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryPipeline", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="deliveryPipeline")
    def delivery_pipeline(
        self,
    ) -> GoogleClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference:
        return typing.cast(GoogleClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference, jsii.get(self, "deliveryPipeline"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "GoogleClouddeployDeployPolicySelectorsTargetOutputReference":
        return typing.cast("GoogleClouddeployDeployPolicySelectorsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="deliveryPipelineInput")
    def delivery_pipeline_input(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline], jsii.get(self, "deliveryPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["GoogleClouddeployDeployPolicySelectorsTarget"]:
        return typing.cast(typing.Optional["GoogleClouddeployDeployPolicySelectorsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicySelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicySelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicySelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c9417772e292bb5f7c54f87e86413c5a01d63692be123f00c3dc2719c91351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectorsTarget",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "labels": "labels"},
)
class GoogleClouddeployDeployPolicySelectorsTarget:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: ID of the 'Target'. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Target labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4e45fec760a5cdfb4890993281d52b6cb3fc7684161579144efa6a9e6aeaea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#id GoogleClouddeployDeployPolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Target labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#labels GoogleClouddeployDeployPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicySelectorsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicySelectorsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicySelectorsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e72bbec0587b2f0ee9afd4c1cf193cac9e94c88bdbfafce952d1915d1bdd0df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a73d0de2fcca9fbf8902355812a94375461adf9d734f5a47391b96791c20473b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cfa767c8a7d9925c73f4b181389a86bf456d46fa90f5dc12c0e08ba64044d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleClouddeployDeployPolicySelectorsTarget]:
        return typing.cast(typing.Optional[GoogleClouddeployDeployPolicySelectorsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleClouddeployDeployPolicySelectorsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2855d75ef3802b84ebc9d244bb7a8f122a352f05893783368c3f06baa39bb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleClouddeployDeployPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#create GoogleClouddeployDeployPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#delete GoogleClouddeployDeployPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#update GoogleClouddeployDeployPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd54c39878837872a3ae1acea88cec081ff4dc128a90bb51b48d69c54921977)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#create GoogleClouddeployDeployPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#delete GoogleClouddeployDeployPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_clouddeploy_deploy_policy#update GoogleClouddeployDeployPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleClouddeployDeployPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleClouddeployDeployPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleClouddeployDeployPolicy.GoogleClouddeployDeployPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c62a8675e56448a9f82c2ef933f42339e46d908d8562c9a51df4ae621f28568)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a2833965d880a16f53385e808f98e6787d666858577a956265cd473559a1182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f17abcb25d837da84035fafad6712467146fa8329bf13d85cab203a084e79b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa76096f5f54139d97e56495ecb39139c167d850acb0b300bbc1ddfeaf66b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079890aec831c5050c34bb509ae46de365a899b6ae229a42668d3e9114a60326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleClouddeployDeployPolicy",
    "GoogleClouddeployDeployPolicyConfig",
    "GoogleClouddeployDeployPolicyRules",
    "GoogleClouddeployDeployPolicyRulesList",
    "GoogleClouddeployDeployPolicyRulesOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestriction",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime",
    "GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference",
    "GoogleClouddeployDeployPolicySelectors",
    "GoogleClouddeployDeployPolicySelectorsDeliveryPipeline",
    "GoogleClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference",
    "GoogleClouddeployDeployPolicySelectorsList",
    "GoogleClouddeployDeployPolicySelectorsOutputReference",
    "GoogleClouddeployDeployPolicySelectorsTarget",
    "GoogleClouddeployDeployPolicySelectorsTargetOutputReference",
    "GoogleClouddeployDeployPolicyTimeouts",
    "GoogleClouddeployDeployPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8c5b3dd484e1c6e54eada24dfaee86cac78adb7851efe6e640580a6ccd6bec3e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicySelectors, typing.Dict[builtins.str, typing.Any]]]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployDeployPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__82c9008f13dfb492dfb3fc6a89b197ef13c19d28eff0578edd6bcdcd4b8d5918(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd6fcd38ae1a0bf6c94d92ee768165fec7350e94829e7918aad41c1fcf25778(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7489a25df16d8df71f74ee46425e961b713914bafb9414e2cec7cd8f672ebb57(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicySelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c0228e376326b42605d6070d044599754dfeb0e963856e17dde62ee528106f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1970f9e434b8513080cf2eff17e0de4ec61186826bfcacb09ea5f16311ad95fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175772635ff786bf56a338448522fa137d5e7aa799b0816a2f68332ad2fe405e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28149ca78b6d6582f40315fb6f81bc4651a086a5000d4ffd122c92880479d35b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f13764d24293e624c93eea9e3824feb0d10953c5a12d38f0e4572ec808c673b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effe422c5812f9e1a7f2b020c3ffcd70615b28bf1ac3e3dbba3bfc87b75efcc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f886eee6967a998903ef2fd949bb1efd90ecff67db455f697beb4a6b3017b4e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75dab0b57eae957d5913bde0056be8471dc9b03445bf54a92456e2d3eacd8d52(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ba198cb4e0976ded9008ceabbe7904df05a1cfaf71e483361df99e7e3b085d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicySelectors, typing.Dict[builtins.str, typing.Any]]]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[GoogleClouddeployDeployPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f76c77c7ad283890a8de50760794efc9b5e5d554f06250fa669277da2735e5(
    *,
    rollout_restriction: typing.Optional[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestriction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911fc3d72ebf34d17f1de27037ad897aaec9ee75ae224677e9371b754c598d94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381f4f627f5c72e71b9d7973b9409c8de8adfc33f06d34667adee90fcaa1e4b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb684fc9dbf888d0c729a1661caa75c46d8d31aa2b9682dddd4f667cb4cbecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021d8e9eb16a51542155fb1b61d8d5abf70fc0f28b90e8a2bd95696f910ed515(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63bbabbe2e2980ba1337acfa5b4f240c6bab9bf4f1610eb17c6a8784f804486(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac144fd86279d759ef839573c592fc7dc60373f0291c5fecd2c79f24e721aec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d6315d27b6a1c0b3ddc44e2ca140a6c3d356f51e40df3adba0f35ab1d766d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e4654409c366f7a76497852e77e9b3e17ccf24bbf38d8f4990ca622aed4d45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9f81b0707ead221f2e8ed5c4aa5de6978e932420f01ae6d2202a6939771117(
    *,
    id: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    invokers: typing.Optional[typing.Sequence[builtins.str]] = None,
    time_windows: typing.Optional[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__451830136f440a66661b6cbe14801d12ca9b92fd81bac47af08153961ce5ae9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c469f2365908da386714b6b4b41cde6e0b4f1f236f1010759a547eb0559039f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7a23ee74e6952b3a121194e42ee9efab529490b2679a7ebc3f566c44ce752e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3706e83e50d69c7c752153afc9bd005f61d9a623c1f73ee7196378bd34d995(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7a9db1ac62c38bad7753343903e5338275d003b7e521ba0c2c625efe1016fd(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestriction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6617a42532704a956923cf0f18978ba1a87c2c09b6e5988bdd224e27d634adf3(
    *,
    time_zone: builtins.str,
    one_time_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weekly_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa853fbae7ebb32b458c8113f6b65e9f56546a77a07dc2c0088ddbbd2a8705d1(
    *,
    end_date: typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate, typing.Dict[builtins.str, typing.Any]],
    end_time: typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime, typing.Dict[builtins.str, typing.Any]],
    start_date: typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate, typing.Dict[builtins.str, typing.Any]],
    start_time: typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a7daa2c3f7211cd4adc8caeea31a771a386826294d545bb45e05f1af58beb7(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c669ecbe5d7b88f128e9a9e1f35ef47c9bc4470777a5c72a4c9dd4cb43351fb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d65ee96a00827f30c1856be54c9e28930e7078818bab3d6b77483b4245bb1f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a3fb204e12b69a07abd9867b0e1aa2ce52ad8e9417a8101e280f931cd2339a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54471af8dab67ca91e02c52eda592ca844bd40834bde94ad955c47d28bd93b7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ecbee0cffa52f9ff04aeb3a1c213982e2976d8cd6a2c0aafd0349ffecc81d5(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb62231d09b03d46f4b3257274e2b7700dea6f3f3f0ae9336e8e18a02347ced(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a887d44350365e02e7f1718642ef3aac2e3224e4244d85bc6485e30e88629f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3633a5a2ebc56ca05d21438de5ecf21ad0839a05611b4fa5ba01a589974ec7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f52f2a4588ac7144419c7885d19de097549de165650792cdde4db5ada5402f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc02195677b3e21bcc75e6780d99d2f77bdaa0b8b22bc065853049a26d0831b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab016bd06d38b1521a341f831296748db4660e1e6a7b6797a8d489fa564f4b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514ef7d2a648bdf848a935bc03e04e63ba4920c913c64287c1234fafa7f21f07(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38145838bda942e22733a43857eeee448a5a3fde8943bc072093da5fdc7f1e92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694ff0ddfd1eb227a1650eab26e1de9bc6f02268d7dd0d08c502fc46d06ddfa4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296a38f1cc4d81451758ea72691e8bb2798862293ff8a3756b565ccf544948af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30c3c90043d0322ee2014de3cd4db5056019c4d2ff3ffedf4087e6c03a168a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f321d1207cf90176ac1c6400ef7207b3cae7a020efbe7682bc14326161038df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8f66a9b3becc516fcd27d0149a5177ff384ec89f072ce60bda678a5b9e9c69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc48b732698e73659b140a531ce3109bfc882b834d3065f272aab66e17e938b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59e1b2a087d4c8490221eba63e47df49a1bc352c47b96651368ad59db2e90c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e2af5eac8ed76ed0878f71446f4ec56661d059149e88447b4c685a142b26af(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07028ea0f189fec12e42175914eecf8c18409c88dcf69413be9c35683ba72c66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ae75f16fd00b78ed3534ad2f00301a1a09288c2254482126bd4f0386c0560b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc0e7129abef05eafbcbe83e05b9a6aab57774df1c81ff174db21e8ba080bcb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01286eff24f8dd38797c4b35d71c3237c52ec806ab0f9b4cc1ec59464087d604(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289b39b586706fe56d7d24cfed23922889f1ec16099ebe522d22a93e8ec9a576(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefcea184ac69c189c4c67b18b41c7686a7e2ec412b0724a2d300a17d15185be(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87942b9e71c2c14bc395d7d1dec8cb0dd92abf67b579115d8beccf5f709cee81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab1dfb8b6fdf78e30653c6f82f4b39614f22e173f32d91837544025243fcc0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7cb8f7ce56ffde664fd50ad02b57d62a47a00779372c2e0a77f1efed33c5fc6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8720b0ff551c37b2ee6e50f52c6f151347abbccddb0c6efbaa7ce3df5eacc4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7495e3aad985244f08d738c4675567c9c347c9aaa613c88bf6ea514f3c90cabe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7eb8966a1a3fdc9163ddb37878b226010ae6e5ef0c857c23c5f03343c9326a(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97355cec76984059237764267e7e84b10a296a2d092f2628cf89fc803642c88d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28730df09dccab02cf77a93f56f67136605f24f64b5acdbf8a3f14b0fb91b5cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61426cbbeadb925ee10ce5a6c04a56222b96345929d12dd7b6389a535276ea0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b52f5ef29d27f78d22c23962b6e989b049f12e9bca4ae63b91f0798779ca08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffef0ff980f66e518c366bc80afc0d89654d5b9234fbafbd678573106be577f(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386bd7f25c8d9c40227dc62342acdb875dfe9a36c863bd196163a3d0b6cc7a94(
    *,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time: typing.Optional[typing.Union[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e74bf6baa19c0af497d67ca62e2168d02352548b2ec70d02ee56e44b4b98b4(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f1e1d7aaa965551794676f80c4446062d398198e14d955be256969e00a7078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d260c238b191883ded86fbc4e1e0025399177fb77255b8903c8a93a314a7bc72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f221292f054e3e2799450a749144e83bdd98dbced0a252407df704f5b75f96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d791d30a4ab9805b7dfcb082a2164ab353d5c24dd31db539f1f2ad05fc55b9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d737e4d18dce8424aa0cfa24bed092fd2371d955a9947b9c8be1de3bc8768c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a48bef9200bc79c7a52e86cb520df27e8bffa9a412ece61b334d85bf29df2b(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec4f14df17ec3fe48a1f48752960538397c6abc4ef70ed2c1c41a0e3d111d12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407f24700daa93f50678d2fcd15ac63c0b711400dde1537b4fbccd8b35ba66d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aafd0c99347acfab9e15fd4ce992cddb761604c07af6a45c9a6b0a7e0acceae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c5a243e90c7f75bd629c70930aaa16dac0e284d4fbe7e025dda922f3341971(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9f63848a4a25e00374d5c7b7dc51d69c1ed3579f877ed2c43c6b82d7d14e55(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df25e53e157d1776d055ba432e2b686829d85d5013f9f489021167182c9529c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c795b727314313d0c7b0a7726c2c6275a6ca2f107091eb8de81af907f73b8c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa976711087b01cbcd957e741a527db85560ca3bbaeec4d6ac95122a251dcff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f01da341f907623c1ff5dfe240626c37e6934b313feb0076d5078b7aeab98be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b557bdea088e6013ecd73a3ad59860d6e2866b3a8b01e6278eae54dc0c62c1d1(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b61a6a276c6e4d83ff86322b7f0ff83fd6f7cd3762d01afc153c57dc4579ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a58dd8931e494e2a9138e64341e60ea7892962730734b2fca4dcd31d69e8cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255c38c239bdd71889c5878ac1c9a83c3e42337a3e5e8a122616777d1400adab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e935dabaaab562abf327f22c940deb8cc8ec9f63ebaf359f04d0e368f763e01e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e1eb45a482c72d5b91b699a13df820d5e18836f4c6840177c5de94fbb40527(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9eb7575cb5822e5ec78c234be2a119771e89591e8a8597bfc332e842aa645ad(
    value: typing.Optional[GoogleClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fda9c144e7dedf36769dcd5191878dc2a178895c3fffeef127ad9a74933d3dc(
    *,
    delivery_pipeline: typing.Optional[typing.Union[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Union[GoogleClouddeployDeployPolicySelectorsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d410c8048998632f95dcf79512fd3f70d935ff6443d4e6fc239559955b7db2(
    *,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22de548eaf8867e4f27eb1498a0d659d112a52e77b1ccec05a34becbc06a634a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ff8020df83943e6429f98885a5529ab8ef4cd3ccf4d76c635282e0df4918c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d07058621fbead25da48b160257cf6e4bc97f2600dae6fdd682a850941b33b8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d57e94769d97addaa21ff4b5a5666231633c6b843488c4b98a613f9aa28bc71(
    value: typing.Optional[GoogleClouddeployDeployPolicySelectorsDeliveryPipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42926b94690f86af477f9d3535aa0d1d1e77c778a1ad3b6700478d1305de7b11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b576364efb3bfacd6d28ba98feda1373007d98b04cf273766cc6fd02ec7dd866(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6105730b0cf8176b111d036011b998a86503a8427fe8c0302e6b9670976ed1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b75aea0f23722bb2a18e4e81169d59d0715672a2b6f69906fa92723f4a126c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ae8f0dcd881fd0e90e57617e0a6c0ba68998e1d510732652f7c0e8b38371fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fe6ca801bc39a77f9c214b1831b4d8dfd5d4cd8fd97089a37fd670c60e36de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleClouddeployDeployPolicySelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007bc7b733b98e78ed367bcc381ea3faeee482bb6a0215537343a2cc108f8795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c9417772e292bb5f7c54f87e86413c5a01d63692be123f00c3dc2719c91351(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicySelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4e45fec760a5cdfb4890993281d52b6cb3fc7684161579144efa6a9e6aeaea(
    *,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e72bbec0587b2f0ee9afd4c1cf193cac9e94c88bdbfafce952d1915d1bdd0df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73d0de2fcca9fbf8902355812a94375461adf9d734f5a47391b96791c20473b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cfa767c8a7d9925c73f4b181389a86bf456d46fa90f5dc12c0e08ba64044d4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2855d75ef3802b84ebc9d244bb7a8f122a352f05893783368c3f06baa39bb94(
    value: typing.Optional[GoogleClouddeployDeployPolicySelectorsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd54c39878837872a3ae1acea88cec081ff4dc128a90bb51b48d69c54921977(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c62a8675e56448a9f82c2ef933f42339e46d908d8562c9a51df4ae621f28568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2833965d880a16f53385e808f98e6787d666858577a956265cd473559a1182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f17abcb25d837da84035fafad6712467146fa8329bf13d85cab203a084e79b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa76096f5f54139d97e56495ecb39139c167d850acb0b300bbc1ddfeaf66b46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079890aec831c5050c34bb509ae46de365a899b6ae229a42668d3e9114a60326(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleClouddeployDeployPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
