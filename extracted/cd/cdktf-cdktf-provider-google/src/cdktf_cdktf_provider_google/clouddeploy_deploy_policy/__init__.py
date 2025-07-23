r'''
# `google_clouddeploy_deploy_policy`

Refer to the Terraform Registry for docs: [`google_clouddeploy_deploy_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy).
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


class ClouddeployDeployPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy google_clouddeploy_deploy_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicySelectors", typing.Dict[builtins.str, typing.Any]]]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployDeployPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy google_clouddeploy_deploy_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#location ClouddeployDeployPolicy#location}
        :param name: Name of the 'DeployPolicy'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#name ClouddeployDeployPolicy#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#rules ClouddeployDeployPolicy#rules}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#selectors ClouddeployDeployPolicy#selectors}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#annotations ClouddeployDeployPolicy#annotations}
        :param description: Optional. Description of the 'DeployPolicy'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#description ClouddeployDeployPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#project ClouddeployDeployPolicy#project}.
        :param suspended: Optional. When suspended, the policy will not prevent actions from occurring, even if the action violates the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#suspended ClouddeployDeployPolicy#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#timeouts ClouddeployDeployPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637ffeba99fffc2804dc7e01e112111b3aa0d33bed282eebd98358a84dae4eab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ClouddeployDeployPolicyConfig(
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
        '''Generates CDKTF code for importing a ClouddeployDeployPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ClouddeployDeployPolicy to import.
        :param import_from_id: The id of the existing ClouddeployDeployPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ClouddeployDeployPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2136135f8a534856c69cbc9bfca1dcf281e8be73fc21f1999a533b7a864f7512)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7bff269b1a8232ea0d2c9edd1154456ff4152b6628f371454284c931164659b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicySelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e6c71928146979b7656ac45da0f07c49b1e30e58830647f3921b45fa40e4fd)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#create ClouddeployDeployPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#delete ClouddeployDeployPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#update ClouddeployDeployPolicy#update}.
        '''
        value = ClouddeployDeployPolicyTimeouts(
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
    def rules(self) -> "ClouddeployDeployPolicyRulesList":
        return typing.cast("ClouddeployDeployPolicyRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> "ClouddeployDeployPolicySelectorsList":
        return typing.cast("ClouddeployDeployPolicySelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ClouddeployDeployPolicyTimeoutsOutputReference":
        return typing.cast("ClouddeployDeployPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicySelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicySelectors"]]], jsii.get(self, "selectorsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployDeployPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ClouddeployDeployPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d9c157d56cce89ffb82771a4bcf341c4b35a951ce8aa776a44741807bee7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c4ab34253de6157f1242b28e33e8b19a57b26a132ae425202ea6bcba663b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf429f54bd81a11f86e7a79d1e7348579f15e2bb1e8b2cf48031b7b9aded51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d61af977805f82849c8acb965fbd958c192164eeebd3a03661829fd427a956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3d348dbb1f55e82e1951156fc69fd73e7bbc8162551308bbca935974f5d0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332d73f5221b8ba126c1c63bdce73fc4ba7c8634c62ad88716391d22c61554ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e2c3ff4831eba9f8563ef95669989c74e45cd25007390057f7b10907297bab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__483107422ddf5ac01db11ed6d2c51cd272c0dd3b1103269f8bd0a92c6396f6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspended", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyConfig",
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
class ClouddeployDeployPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
        selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicySelectors", typing.Dict[builtins.str, typing.Any]]]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ClouddeployDeployPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#location ClouddeployDeployPolicy#location}
        :param name: Name of the 'DeployPolicy'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#name ClouddeployDeployPolicy#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#rules ClouddeployDeployPolicy#rules}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#selectors ClouddeployDeployPolicy#selectors}
        :param annotations: Optional. User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#annotations ClouddeployDeployPolicy#annotations}
        :param description: Optional. Description of the 'DeployPolicy'. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#description ClouddeployDeployPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels are attributes that can be set and used by both the user and by Cloud Deploy. Labels must meet the following constraints: * Keys and values can contain only lowercase letters, numeric characters, underscores, and dashes. * All characters must use UTF-8 encoding, and international characters are allowed. * Keys must start with a lowercase letter or international character. * Each resource is limited to a maximum of 64 labels. Both keys and values are additionally constrained to be <= 63 characters. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#project ClouddeployDeployPolicy#project}.
        :param suspended: Optional. When suspended, the policy will not prevent actions from occurring, even if the action violates the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#suspended ClouddeployDeployPolicy#suspended}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#timeouts ClouddeployDeployPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ClouddeployDeployPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34024ea54ad9dc762216ad43c8466cc5084996a0992b944ced63de4199ef464)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#location ClouddeployDeployPolicy#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the 'DeployPolicy'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#name ClouddeployDeployPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#rules ClouddeployDeployPolicy#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRules"]], result)

    @builtins.property
    def selectors(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicySelectors"]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#selectors ClouddeployDeployPolicy#selectors}
        '''
        result = self._values.get("selectors")
        assert result is not None, "Required property 'selectors' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicySelectors"]], result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        User annotations. These attributes can only be set and used by the user, and not by Cloud Deploy. Annotations must meet the following constraints: * Annotations are key/value pairs. * Valid annotation keys have two segments: an optional prefix and name, separated by a slash ('/'). * The name segment is required and must be 63 characters or less, beginning and ending with an alphanumeric character ('[a-z0-9A-Z]') with dashes ('-'), underscores ('_'), dots ('.'), and alphanumerics between. * The prefix is optional. If specified, the prefix must be a DNS subdomain: a series of DNS labels separated by dots('.'), not longer than 253 characters in total, followed by a slash ('/'). See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/#syntax-and-character-set for more details.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#annotations ClouddeployDeployPolicy#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the 'DeployPolicy'. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#description ClouddeployDeployPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#project ClouddeployDeployPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspended(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. When suspended, the policy will not prevent actions from occurring, even if the action violates the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#suspended ClouddeployDeployPolicy#suspended}
        '''
        result = self._values.get("suspended")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ClouddeployDeployPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#timeouts ClouddeployDeployPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ClouddeployDeployPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRules",
    jsii_struct_bases=[],
    name_mapping={"rollout_restriction": "rolloutRestriction"},
)
class ClouddeployDeployPolicyRules:
    def __init__(
        self,
        *,
        rollout_restriction: typing.Optional[typing.Union["ClouddeployDeployPolicyRulesRolloutRestriction", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param rollout_restriction: rollout_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#rollout_restriction ClouddeployDeployPolicy#rollout_restriction}
        '''
        if isinstance(rollout_restriction, dict):
            rollout_restriction = ClouddeployDeployPolicyRulesRolloutRestriction(**rollout_restriction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b677af31ca12f156d276b04aac9a815aff5440d2277664448978106a50368988)
            check_type(argname="argument rollout_restriction", value=rollout_restriction, expected_type=type_hints["rollout_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rollout_restriction is not None:
            self._values["rollout_restriction"] = rollout_restriction

    @builtins.property
    def rollout_restriction(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestriction"]:
        '''rollout_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#rollout_restriction ClouddeployDeployPolicy#rollout_restriction}
        '''
        result = self._values.get("rollout_restriction")
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestriction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a363ad49bc5664d3104ed2dfb20ab264887a0232cc947b925896e2a516c33a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ClouddeployDeployPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa4e2dfd0469eb70c29f58696d171f64318667a69277919b5b32f16b5b0f6cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeployPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c8cbfb7b70c7fffd6df1b6fb8227d6d3de73c012bb33411a4eeb816d03621a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04745be7f52f53dfa8cba4e1d5cbd81f5e8e8d3bd2db935e9304db0becb4a1cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94141e2bf9b6805cda347a2c93670c06cef6da9742e886179985e0c695abd375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b68f844f508f0f9d84e59abae170ac0c5d6821d747663be09877cf6c8cafd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bed57c9e144863f451a45714f48e6a7ba7304f16c23b2cbcf406cf04df7e1bfd)
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
        time_windows: typing.Optional[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'DeployPolicy' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param actions: Optional. Rollout actions to be restricted as part of the policy. If left empty, all actions will be restricted. Possible values: ["ADVANCE", "APPROVE", "CANCEL", "CREATE", "IGNORE_JOB", "RETRY_JOB", "ROLLBACK", "TERMINATE_JOBRUN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#actions ClouddeployDeployPolicy#actions}
        :param invokers: Optional. What invoked the action. If left empty, all invoker types will be restricted. Possible values: ["USER", "DEPLOY_AUTOMATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#invokers ClouddeployDeployPolicy#invokers}
        :param time_windows: time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#time_windows ClouddeployDeployPolicy#time_windows}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestriction(
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
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionOutputReference":
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionOutputReference", jsii.get(self, "rolloutRestriction"))

    @builtins.property
    @jsii.member(jsii_name="rolloutRestrictionInput")
    def rollout_restriction_input(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestriction"]:
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestriction"], jsii.get(self, "rolloutRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ef64a643e816f091b49bb40b56f6832082d623807a9c32eaa955f6fa5463b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "actions": "actions",
        "invokers": "invokers",
        "time_windows": "timeWindows",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestriction:
    def __init__(
        self,
        *,
        id: builtins.str,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        invokers: typing.Optional[typing.Sequence[builtins.str]] = None,
        time_windows: typing.Optional[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Required. ID of the rule. This id must be unique in the 'DeployPolicy' resource to which this rule belongs. The format is 'a-z{0,62}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param actions: Optional. Rollout actions to be restricted as part of the policy. If left empty, all actions will be restricted. Possible values: ["ADVANCE", "APPROVE", "CANCEL", "CREATE", "IGNORE_JOB", "RETRY_JOB", "ROLLBACK", "TERMINATE_JOBRUN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#actions ClouddeployDeployPolicy#actions}
        :param invokers: Optional. What invoked the action. If left empty, all invoker types will be restricted. Possible values: ["USER", "DEPLOY_AUTOMATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#invokers ClouddeployDeployPolicy#invokers}
        :param time_windows: time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#time_windows ClouddeployDeployPolicy#time_windows}
        '''
        if isinstance(time_windows, dict):
            time_windows = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows(**time_windows)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f247b5d4edf5c763867d9803b1de824ac549e1a15884d72857bc6d6447936ad1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id}

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#actions ClouddeployDeployPolicy#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def invokers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. What invoked the action. If left empty, all invoker types will be restricted. Possible values: ["USER", "DEPLOY_AUTOMATION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#invokers ClouddeployDeployPolicy#invokers}
        '''
        result = self._values.get("invokers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def time_windows(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"]:
        '''time_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#time_windows ClouddeployDeployPolicy#time_windows}
        '''
        result = self._values.get("time_windows")
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0edddcb6f62586dc0634ba69afde34031b676498b25d119e1e2de8bdc8f7ddf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimeWindows")
    def put_time_windows(
        self,
        *,
        time_zone: builtins.str,
        one_time_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#time_zone ClouddeployDeployPolicy#time_zone}
        :param one_time_windows: one_time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#one_time_windows ClouddeployDeployPolicy#one_time_windows}
        :param weekly_windows: weekly_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#weekly_windows ClouddeployDeployPolicy#weekly_windows}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows(
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
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference":
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference", jsii.get(self, "timeWindows"))

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
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"]:
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows"], jsii.get(self, "timeWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1436cd2d0c0f00610f034fcac8a28d825b784b4b8a7476b4590188a67df89b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f870dcbf70ca764f3b4e91fe99cdcb68421e8c7370c6af719e60d1388974796f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invokers")
    def invokers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "invokers"))

    @invokers.setter
    def invokers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae65cc264fe5ec5b7006c5b088410fcb52a72f9c987c3a64bba74e216387dbfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestriction]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestriction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestriction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054ee155290c9a37af7a460e1a1b8cdc620683c5ca5a198ae37fb4a1fcb56755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "one_time_windows": "oneTimeWindows",
        "weekly_windows": "weeklyWindows",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        one_time_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param time_zone: Required. The time zone in IANA format IANA Time Zone Database (e.g. America/New_York). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#time_zone ClouddeployDeployPolicy#time_zone}
        :param one_time_windows: one_time_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#one_time_windows ClouddeployDeployPolicy#one_time_windows}
        :param weekly_windows: weekly_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#weekly_windows ClouddeployDeployPolicy#weekly_windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787dea6c48c946cc01f50a5669a9b35df4e066464e52592c736cc026a438181c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#time_zone ClouddeployDeployPolicy#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def one_time_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows"]]]:
        '''one_time_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#one_time_windows ClouddeployDeployPolicy#one_time_windows}
        '''
        result = self._values.get("one_time_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows"]]], result)

    @builtins.property
    def weekly_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]]:
        '''weekly_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#weekly_windows ClouddeployDeployPolicy#weekly_windows}
        '''
        result = self._values.get("weekly_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows",
    jsii_struct_bases=[],
    name_mapping={
        "end_date": "endDate",
        "end_time": "endTime",
        "start_date": "startDate",
        "start_time": "startTime",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows:
    def __init__(
        self,
        *,
        end_date: typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate", typing.Dict[builtins.str, typing.Any]],
        end_time: typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime", typing.Dict[builtins.str, typing.Any]],
        start_date: typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate", typing.Dict[builtins.str, typing.Any]],
        start_time: typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#end_date ClouddeployDeployPolicy#end_date}
        :param end_time: end_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#end_time ClouddeployDeployPolicy#end_time}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#start_date ClouddeployDeployPolicy#start_date}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#start_time ClouddeployDeployPolicy#start_time}
        '''
        if isinstance(end_date, dict):
            end_date = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate(**end_date)
        if isinstance(end_time, dict):
            end_time = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime(**end_time)
        if isinstance(start_date, dict):
            start_date = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate(**start_date)
        if isinstance(start_time, dict):
            start_time = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205a5d353b1f83e0b31b725e325cbc3ee80e0abb36bb652db092f99e2ff49185)
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
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate":
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#end_date ClouddeployDeployPolicy#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate", result)

    @builtins.property
    def end_time(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime":
        '''end_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#end_time ClouddeployDeployPolicy#end_time}
        '''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime", result)

    @builtins.property
    def start_date(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#start_date ClouddeployDeployPolicy#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate", result)

    @builtins.property
    def start_time(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#start_time ClouddeployDeployPolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#day ClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#month ClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#year ClouddeployDeployPolicy#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3c64d1b0f55e4bed6585aa7c6f26de9a5c02a05ebdfab9a8b2a3f759b46144)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#day ClouddeployDeployPolicy#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year. Must be from 1 to 12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#month ClouddeployDeployPolicy#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#year ClouddeployDeployPolicy#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf38b448e368560a7ad42239b10fdcf923edd9845b2a62e86a19fea7f0b2d056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db1fd87c68dfd1de3b92372947d820dfbb68f5941e3f4f47775e3decd68c0788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0e9a270b7467b6be21a57c4d22ef2fc6e96674afd18016775fa7f22477a126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a7526cc22c8f672d42c8548d14b0114e98055fc235e1d0c0ea3deb51e8a2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b0e1d7c12b166b69f1410feee380e97140a7dcc1f39f639b965b57ef3f5372b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fbb27af1cb3e64d7dbe731b43cfb16bad2319d8545fb5b089a32cc3a64e300)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a96eea87197eb46ad445812fb1df1b753bc3a00464c87735ddac74c6e0d57e77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63671a9def00d94816bfda41a7d6951ae974169d4fc20e5e245e76acea8f5275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82816bdad36b2ff6056e742d814af506940f8f895367a314fcb8ed401ecb642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda6972f93df1f2b26307a526dd5556ac649cbc221cbc9cc180460c9af9fdb87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e458bafac86ffe337b8fd4aa4f11bf951653e60c997910231b8dc11e3369bbe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6e2264822f14fdbc983084b9f40c9b5e67591d707c9489050deac7bcfd466c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c177d4d868eb59df9dfc730a2cac1c07518d9f26bf9a7153480deb4005b6f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d038944fdd2ef164bbbbaa9604daa8c57f118e1c9e702c1a8a42a33822608f45)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40ce64e94c78f9358b82feb7e64f6c8d2b0217e53c85b0ae3f43b1751412bcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3d6928037573f3de278c131ca59b8acfb1882944df7714fe6cdbd283bf7e25e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ddc3a7c779c4ba84069e940f32689574b603c668f164c4b49832b6a8ad4cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ea952fafcea8acd68802ea740b65542581a787a76ec0d2ad2842991b589dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fec283f74df601b20917e554b601241e6cc4f74e7170c6c796c6e9f0ed11e13)
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
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#day ClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#month ClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#year ClouddeployDeployPolicy#year}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate(
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
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime(
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
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#day ClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#month ClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#year ClouddeployDeployPolicy#year}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate(
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
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(
        self,
    ) -> ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference:
        return typing.cast(ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(
        self,
    ) -> ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference:
        return typing.cast(ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference":
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference":
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate"]:
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime"]:
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c01ac322e689601932b06d6901333413f0e09279129d356d413de2321303360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#day ClouddeployDeployPolicy#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#month ClouddeployDeployPolicy#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#year ClouddeployDeployPolicy#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6323ae3a86d2599cc0006f3de54cc77138de9c5af4cffa025a687821d96060)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#day ClouddeployDeployPolicy#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Must be from 1 to 12, or 0 to specify a year without a month and day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#month ClouddeployDeployPolicy#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#year ClouddeployDeployPolicy#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a975c544fa9dddcbf3fc4b71f5fcbcb5ec45e3bc359bd49d13fe83646913de1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4acc5d2dbd62dd22e742d49a96428f997503c463f1cf11249c6f96cd747fab54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af9d5119fb9a8cb735583a1c4991424596a8137f3923f31730e11b2281a7ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1db3435b9022855c28c38acc569d065c31e2374fff0cc484873d61720a3362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdad936e2342a48ce3c08b99f94cd90002ba373f32120aa1a6a8edd820408c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec54b99b3841b08de2462fd2eb172626ae0b9facd1c3cfbd9b4a5e2eb69e3f1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2026e8c8c082afd267b0e0156d79d3bd926c1a05ec61326546b895eb349bec09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1278667fc36f7c3fff8d2a13ecf2f46dcacc17069c4b793bffb08b30a74ad2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad00e2f36d63c1327d62c2fd282586fc264b87218810cc814c611cfafa6597e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323b9255cced3edf259567b762aa0d4b660d59cec55446437d75c5f0586c6167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a606a77b9b73123ebb1bccd4b3d1343b30411119fe9c89158984821776aee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad29d4d62c86f43c5c3273b6a5977042542b30b283caca80109278913185b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce12560d4d9b7b54be22004d998fe938e3ece5fa52a5d39675c0ba3359e15189)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOneTimeWindows")
    def put_one_time_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75447c6347b7debb57b7b54f5f76eaa24e91965465d94e1cbb5a4c213bb6eb8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOneTimeWindows", [value]))

    @jsii.member(jsii_name="putWeeklyWindows")
    def put_weekly_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e672560bb1f612cb087e27117e53f96f5ca7325a671f5e84509d9f12b5b5ade5)
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
    ) -> ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList:
        return typing.cast(ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList, jsii.get(self, "oneTimeWindows"))

    @builtins.property
    @jsii.member(jsii_name="weeklyWindows")
    def weekly_windows(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList":
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList", jsii.get(self, "weeklyWindows"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeWindowsInput")
    def one_time_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]], jsii.get(self, "oneTimeWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyWindowsInput")
    def weekly_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows"]]], jsii.get(self, "weeklyWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ee6701bb54028ff991cc9b26eb80f5c03f711b62cdab389da2e56c93c8bd8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee920efb981606342a22532a4aa8d1372078f2fa783c38b7b3e4d2678324061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows:
    def __init__(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        end_time: typing.Optional[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime", typing.Dict[builtins.str, typing.Any]]] = None,
        start_time: typing.Optional[typing.Union["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param days_of_week: Optional. Days of week. If left empty, all days of the week will be included. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#days_of_week ClouddeployDeployPolicy#days_of_week}
        :param end_time: end_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#end_time ClouddeployDeployPolicy#end_time}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#start_time ClouddeployDeployPolicy#start_time}
        '''
        if isinstance(end_time, dict):
            end_time = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime(**end_time)
        if isinstance(start_time, dict):
            start_time = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cc9bb9704a3f8088c5dbdd07eaae1a6b8024b870ae40bdf19d2b42103211bb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#days_of_week ClouddeployDeployPolicy#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def end_time(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime"]:
        '''end_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#end_time ClouddeployDeployPolicy#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime"], result)

    @builtins.property
    def start_time(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"]:
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#start_time ClouddeployDeployPolicy#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabc7accb97aeaf6799f3bf82e762251da94613dc230a6771104245ccf123be1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82a042975ffd461dd2a624adf87de5795bc833d7478205a6d52b0190969fca8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__484255be57c44a7ccfc4ed1a4e6333868743b70652032cdbf6fbaeba519dba2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdaff1a1da5746816cb01f7e6a8c10d3a0acd057fdf5f77f955e179d207e770d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773243064d5a4eadaedd87a14f5ef0b826f72be5a97f1fb5897e5dc550133038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774e64f967588fb275ddcd27a2f5a55af3f8507fc44bc04797ea3ac542ae20de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e573cb4398fc41bfd58738cc7b8d91e72eb7477482807c456131f8b8b31b5af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66403e4cc60448471bf31bc56f3df7e1b9ce2db69808021035265f342ce29da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693c65d58f441e605698275c5f5951371bc37fa98648d1f8394f1097d3dd089f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b822b9ff1b9b665353b8d31f32a680eb4fdf37a018f77b8eee04434e88e054d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cff677deb13d5010a6fbccf50aabf3b32c788133fc7228ba4abee01ee928dad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4bf7d17d14a694dd480724380e2af9735b12b1c368d8b57ea872b8ba682be05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61355b6276df59fe3773c7b02a0ec0585d789a72564cf0c073e28704ecceacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97e55bcff529d4166003a50929bcc91bca1e564800a4964b9eebc33da3c46973)
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
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime(
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
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        value = ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime(
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
    ) -> ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference:
        return typing.cast(ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference":
        return typing.cast("ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"]:
        return typing.cast(typing.Optional["ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a99ae5d2e51e368b4fc8df3359e4cf3979bfa0a235dbf58d1be3a5796e72527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e8af24b4fbcca260d12d2538a6990f3d2ff848fd5984c6abcc96c04177012b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        :param minutes: Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        :param nanos: Fractions of seconds, in nanoseconds. Must be greater than or equal to 0 and less than or equal to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        :param seconds: Seconds of a minute. Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c75ad4714faa4da0563f773429f5f9b3c2a8e6a37392eaa949392f02a8e582)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#hours ClouddeployDeployPolicy#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of an hour. Must be greater than or equal to 0 and less than or equal to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#minutes ClouddeployDeployPolicy#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds, in nanoseconds.

        Must be greater than or equal to 0 and less than or equal to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#nanos ClouddeployDeployPolicy#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of a minute.

        Must be greater than or equal to 0 and typically must be less than or equal to 59. An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#seconds ClouddeployDeployPolicy#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6900521c5fe0dad48270e6fd8e330c0604fdb5650779f149f0f6be35afec751f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bbf57ebc3ecade879e38f2eef249df4a111ca98f33c1a51d14dab451e4e5d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bded77947d933b013757e489ad6e0142ca18600e3da4e33525191f2c28ad13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb72b6d400fc27cba940b1b3890cf5e4e09cb3d6e699045b7ea230a6b006805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad48bfe9a0564140853f9b82591a9031710b5b76942f9a885c4cf87edd6ba6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f74f8292f004b2cacb2b6602e4041c6b4a0169df1017b0512496fcc04da396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectors",
    jsii_struct_bases=[],
    name_mapping={"delivery_pipeline": "deliveryPipeline", "target": "target"},
)
class ClouddeployDeployPolicySelectors:
    def __init__(
        self,
        *,
        delivery_pipeline: typing.Optional[typing.Union["ClouddeployDeployPolicySelectorsDeliveryPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        target: typing.Optional[typing.Union["ClouddeployDeployPolicySelectorsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param delivery_pipeline: delivery_pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#delivery_pipeline ClouddeployDeployPolicy#delivery_pipeline}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#target ClouddeployDeployPolicy#target}
        '''
        if isinstance(delivery_pipeline, dict):
            delivery_pipeline = ClouddeployDeployPolicySelectorsDeliveryPipeline(**delivery_pipeline)
        if isinstance(target, dict):
            target = ClouddeployDeployPolicySelectorsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fbe8d6d18209dc4893386f44b81e893bb9cd6dc92eae432e7e84e6a9479d22)
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
    ) -> typing.Optional["ClouddeployDeployPolicySelectorsDeliveryPipeline"]:
        '''delivery_pipeline block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#delivery_pipeline ClouddeployDeployPolicy#delivery_pipeline}
        '''
        result = self._values.get("delivery_pipeline")
        return typing.cast(typing.Optional["ClouddeployDeployPolicySelectorsDeliveryPipeline"], result)

    @builtins.property
    def target(self) -> typing.Optional["ClouddeployDeployPolicySelectorsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#target ClouddeployDeployPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["ClouddeployDeployPolicySelectorsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicySelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectorsDeliveryPipeline",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "labels": "labels"},
)
class ClouddeployDeployPolicySelectorsDeliveryPipeline:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the DeliveryPipeline. The value of this field could be one of the following: - The last segment of a pipeline name - "*", all delivery pipelines in a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: DeliveryPipeline labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b81bdd580e0bf974368693287075d8720db920c6f3f617b6f5f8bb00807c04)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''DeliveryPipeline labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicySelectorsDeliveryPipeline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c8b6a289b1e780569c5070c546559df85a0d56c1500f1ce0f84cc21a4d8a258)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2d348ae443aab5c6637eb109a79364427b88f9e692e03e88294c348610146e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530612b6af00388384b1cd5647870b9947656edbbf640ca0195f85a908e1807d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicySelectorsDeliveryPipeline]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicySelectorsDeliveryPipeline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicySelectorsDeliveryPipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e236dccf7916df8301231fe29d5de886cbd0708f82d37ed7d11f117bcb26295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicySelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d70a13c76340dfd2f854fd1bd6e9d90201bcf0bfd7349f4f8370dd1c5b78c38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ClouddeployDeployPolicySelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96e25254fa263e5f1a065ebaa28e7d3ab316970f08777324cbd6aaae1618b27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ClouddeployDeployPolicySelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2132466f817bc3c22ae0491e7ea8509303160c0ea2113a0dd86515a0209620da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa08956144beab7c5fa523d21a59d6ba2e7fd0395f7e446a7b266d489cdf5f75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3202e7ac51edd9be34249b061788018308d85817165af60c92f75c6fc4f33000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicySelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicySelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicySelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f87f308208ee99d165c8c7492f7546337ecabda463394e2c1bddbde293ccab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ClouddeployDeployPolicySelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23a581d2723f44e022f8cace0e382e9bc2a9c11d278d1966e14456330952fa00)
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
        :param id: Optional. ID of the DeliveryPipeline. The value of this field could be one of the following: - The last segment of a pipeline name - "*", all delivery pipelines in a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: DeliveryPipeline labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        value = ClouddeployDeployPolicySelectorsDeliveryPipeline(id=id, labels=labels)

        return typing.cast(None, jsii.invoke(self, "putDeliveryPipeline", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: ID of the 'Target'. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Target labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        value = ClouddeployDeployPolicySelectorsTarget(id=id, labels=labels)

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
    ) -> ClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference:
        return typing.cast(ClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference, jsii.get(self, "deliveryPipeline"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "ClouddeployDeployPolicySelectorsTargetOutputReference":
        return typing.cast("ClouddeployDeployPolicySelectorsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="deliveryPipelineInput")
    def delivery_pipeline_input(
        self,
    ) -> typing.Optional[ClouddeployDeployPolicySelectorsDeliveryPipeline]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicySelectorsDeliveryPipeline], jsii.get(self, "deliveryPipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional["ClouddeployDeployPolicySelectorsTarget"]:
        return typing.cast(typing.Optional["ClouddeployDeployPolicySelectorsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicySelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicySelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicySelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee802b37448bff90309c80d1b0d5daad66d007c608c9e5c9e70bf22bdabb3f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectorsTarget",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "labels": "labels"},
)
class ClouddeployDeployPolicySelectorsTarget:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: ID of the 'Target'. The value of this field could be one of the following: * The last segment of a target name. It only needs the ID to determine which target is being referred to * "*", all targets in a location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Target labels. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f928d834be11bdac2dcd60966664bb79466172da9fd86672f32e359ab780d749)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#id ClouddeployDeployPolicy#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Target labels.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#labels ClouddeployDeployPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicySelectorsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicySelectorsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicySelectorsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57939da2b78830e899348b3554f7f9d9cc15082f0b4e94901636ecc2236cf757)
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
            type_hints = typing.get_type_hints(_typecheckingstub__720b6e9f86be3838af6e64d3fdf60f42fe7210bd150b2e17e36e43aa4d56703b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3061e0c46cbec072abd41f1ca57be50899537f3b726e715faa14e39ea09652d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ClouddeployDeployPolicySelectorsTarget]:
        return typing.cast(typing.Optional[ClouddeployDeployPolicySelectorsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ClouddeployDeployPolicySelectorsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a1a573cf5463f686bf6fcf2d6fa866fe79b9dc59e3c52cb376621880b0191d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ClouddeployDeployPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#create ClouddeployDeployPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#delete ClouddeployDeployPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#update ClouddeployDeployPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1979da5efdcb52e94bccf8468a4b1740b0f43255e6586a720305ab782adf01c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#create ClouddeployDeployPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#delete ClouddeployDeployPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/clouddeploy_deploy_policy#update ClouddeployDeployPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClouddeployDeployPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClouddeployDeployPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.clouddeployDeployPolicy.ClouddeployDeployPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e6e93bf22e1c7b832bb305d8df7017719bae5c087a2650c64bacbce841b1b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73b19e35d02db8993429ab677781c75aa748a87a318acd70cdf9a8b1ef960be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6986142f61cc6b02aa05f2a0c250b167ddfd50d3d6f7267d8057903802ba6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af099b6900a9e71e74e039fc67251a3042caa55bee360ec4a122b90e8be9e458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd7294295d96e92d9fd04ab7569ba457a3f8dfec4a68167d5e07864fc682806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ClouddeployDeployPolicy",
    "ClouddeployDeployPolicyConfig",
    "ClouddeployDeployPolicyRules",
    "ClouddeployDeployPolicyRulesList",
    "ClouddeployDeployPolicyRulesOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestriction",
    "ClouddeployDeployPolicyRulesRolloutRestrictionOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDateOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTimeOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsList",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDateOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTimeOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTimeOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsList",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsOutputReference",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime",
    "ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTimeOutputReference",
    "ClouddeployDeployPolicySelectors",
    "ClouddeployDeployPolicySelectorsDeliveryPipeline",
    "ClouddeployDeployPolicySelectorsDeliveryPipelineOutputReference",
    "ClouddeployDeployPolicySelectorsList",
    "ClouddeployDeployPolicySelectorsOutputReference",
    "ClouddeployDeployPolicySelectorsTarget",
    "ClouddeployDeployPolicySelectorsTargetOutputReference",
    "ClouddeployDeployPolicyTimeouts",
    "ClouddeployDeployPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__637ffeba99fffc2804dc7e01e112111b3aa0d33bed282eebd98358a84dae4eab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicySelectors, typing.Dict[builtins.str, typing.Any]]]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployDeployPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2136135f8a534856c69cbc9bfca1dcf281e8be73fc21f1999a533b7a864f7512(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bff269b1a8232ea0d2c9edd1154456ff4152b6628f371454284c931164659b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e6c71928146979b7656ac45da0f07c49b1e30e58830647f3921b45fa40e4fd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicySelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d9c157d56cce89ffb82771a4bcf341c4b35a951ce8aa776a44741807bee7cd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c4ab34253de6157f1242b28e33e8b19a57b26a132ae425202ea6bcba663b17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf429f54bd81a11f86e7a79d1e7348579f15e2bb1e8b2cf48031b7b9aded51d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d61af977805f82849c8acb965fbd958c192164eeebd3a03661829fd427a956(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3d348dbb1f55e82e1951156fc69fd73e7bbc8162551308bbca935974f5d0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332d73f5221b8ba126c1c63bdce73fc4ba7c8634c62ad88716391d22c61554ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e2c3ff4831eba9f8563ef95669989c74e45cd25007390057f7b10907297bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483107422ddf5ac01db11ed6d2c51cd272c0dd3b1103269f8bd0a92c6396f6ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34024ea54ad9dc762216ad43c8466cc5084996a0992b944ced63de4199ef464(
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
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
    selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicySelectors, typing.Dict[builtins.str, typing.Any]]]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    suspended: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ClouddeployDeployPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b677af31ca12f156d276b04aac9a815aff5440d2277664448978106a50368988(
    *,
    rollout_restriction: typing.Optional[typing.Union[ClouddeployDeployPolicyRulesRolloutRestriction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a363ad49bc5664d3104ed2dfb20ab264887a0232cc947b925896e2a516c33a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa4e2dfd0469eb70c29f58696d171f64318667a69277919b5b32f16b5b0f6cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c8cbfb7b70c7fffd6df1b6fb8227d6d3de73c012bb33411a4eeb816d03621a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04745be7f52f53dfa8cba4e1d5cbd81f5e8e8d3bd2db935e9304db0becb4a1cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94141e2bf9b6805cda347a2c93670c06cef6da9742e886179985e0c695abd375(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b68f844f508f0f9d84e59abae170ac0c5d6821d747663be09877cf6c8cafd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed57c9e144863f451a45714f48e6a7ba7304f16c23b2cbcf406cf04df7e1bfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ef64a643e816f091b49bb40b56f6832082d623807a9c32eaa955f6fa5463b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f247b5d4edf5c763867d9803b1de824ac549e1a15884d72857bc6d6447936ad1(
    *,
    id: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    invokers: typing.Optional[typing.Sequence[builtins.str]] = None,
    time_windows: typing.Optional[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0edddcb6f62586dc0634ba69afde34031b676498b25d119e1e2de8bdc8f7ddf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1436cd2d0c0f00610f034fcac8a28d825b784b4b8a7476b4590188a67df89b29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f870dcbf70ca764f3b4e91fe99cdcb68421e8c7370c6af719e60d1388974796f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae65cc264fe5ec5b7006c5b088410fcb52a72f9c987c3a64bba74e216387dbfe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054ee155290c9a37af7a460e1a1b8cdc620683c5ca5a198ae37fb4a1fcb56755(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestriction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787dea6c48c946cc01f50a5669a9b35df4e066464e52592c736cc026a438181c(
    *,
    time_zone: builtins.str,
    one_time_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weekly_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205a5d353b1f83e0b31b725e325cbc3ee80e0abb36bb652db092f99e2ff49185(
    *,
    end_date: typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate, typing.Dict[builtins.str, typing.Any]],
    end_time: typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime, typing.Dict[builtins.str, typing.Any]],
    start_date: typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate, typing.Dict[builtins.str, typing.Any]],
    start_time: typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3c64d1b0f55e4bed6585aa7c6f26de9a5c02a05ebdfab9a8b2a3f759b46144(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf38b448e368560a7ad42239b10fdcf923edd9845b2a62e86a19fea7f0b2d056(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1fd87c68dfd1de3b92372947d820dfbb68f5941e3f4f47775e3decd68c0788(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0e9a270b7467b6be21a57c4d22ef2fc6e96674afd18016775fa7f22477a126(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a7526cc22c8f672d42c8548d14b0114e98055fc235e1d0c0ea3deb51e8a2f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0e1d7c12b166b69f1410feee380e97140a7dcc1f39f639b965b57ef3f5372b(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fbb27af1cb3e64d7dbe731b43cfb16bad2319d8545fb5b089a32cc3a64e300(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96eea87197eb46ad445812fb1df1b753bc3a00464c87735ddac74c6e0d57e77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63671a9def00d94816bfda41a7d6951ae974169d4fc20e5e245e76acea8f5275(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82816bdad36b2ff6056e742d814af506940f8f895367a314fcb8ed401ecb642(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda6972f93df1f2b26307a526dd5556ac649cbc221cbc9cc180460c9af9fdb87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e458bafac86ffe337b8fd4aa4f11bf951653e60c997910231b8dc11e3369bbe8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6e2264822f14fdbc983084b9f40c9b5e67591d707c9489050deac7bcfd466c(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsEndTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c177d4d868eb59df9dfc730a2cac1c07518d9f26bf9a7153480deb4005b6f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d038944fdd2ef164bbbbaa9604daa8c57f118e1c9e702c1a8a42a33822608f45(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40ce64e94c78f9358b82feb7e64f6c8d2b0217e53c85b0ae3f43b1751412bcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d6928037573f3de278c131ca59b8acfb1882944df7714fe6cdbd283bf7e25e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ddc3a7c779c4ba84069e940f32689574b603c668f164c4b49832b6a8ad4cc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ea952fafcea8acd68802ea740b65542581a787a76ec0d2ad2842991b589dc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fec283f74df601b20917e554b601241e6cc4f74e7170c6c796c6e9f0ed11e13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c01ac322e689601932b06d6901333413f0e09279129d356d413de2321303360(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6323ae3a86d2599cc0006f3de54cc77138de9c5af4cffa025a687821d96060(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a975c544fa9dddcbf3fc4b71f5fcbcb5ec45e3bc359bd49d13fe83646913de1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acc5d2dbd62dd22e742d49a96428f997503c463f1cf11249c6f96cd747fab54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af9d5119fb9a8cb735583a1c4991424596a8137f3923f31730e11b2281a7ac3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1db3435b9022855c28c38acc569d065c31e2374fff0cc484873d61720a3362(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdad936e2342a48ce3c08b99f94cd90002ba373f32120aa1a6a8edd820408c4(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec54b99b3841b08de2462fd2eb172626ae0b9facd1c3cfbd9b4a5e2eb69e3f1(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2026e8c8c082afd267b0e0156d79d3bd926c1a05ec61326546b895eb349bec09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1278667fc36f7c3fff8d2a13ecf2f46dcacc17069c4b793bffb08b30a74ad2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad00e2f36d63c1327d62c2fd282586fc264b87218810cc814c611cfafa6597e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323b9255cced3edf259567b762aa0d4b660d59cec55446437d75c5f0586c6167(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a606a77b9b73123ebb1bccd4b3d1343b30411119fe9c89158984821776aee1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad29d4d62c86f43c5c3273b6a5977042542b30b283caca80109278913185b64(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce12560d4d9b7b54be22004d998fe938e3ece5fa52a5d39675c0ba3359e15189(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75447c6347b7debb57b7b54f5f76eaa24e91965465d94e1cbb5a4c213bb6eb8d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsOneTimeWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e672560bb1f612cb087e27117e53f96f5ca7325a671f5e84509d9f12b5b5ade5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ee6701bb54028ff991cc9b26eb80f5c03f711b62cdab389da2e56c93c8bd8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee920efb981606342a22532a4aa8d1372078f2fa783c38b7b3e4d2678324061(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindows],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cc9bb9704a3f8088c5dbdd07eaae1a6b8024b870ae40bdf19d2b42103211bb(
    *,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    end_time: typing.Optional[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime, typing.Dict[builtins.str, typing.Any]]] = None,
    start_time: typing.Optional[typing.Union[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabc7accb97aeaf6799f3bf82e762251da94613dc230a6771104245ccf123be1(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a042975ffd461dd2a624adf87de5795bc833d7478205a6d52b0190969fca8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484255be57c44a7ccfc4ed1a4e6333868743b70652032cdbf6fbaeba519dba2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaff1a1da5746816cb01f7e6a8c10d3a0acd057fdf5f77f955e179d207e770d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773243064d5a4eadaedd87a14f5ef0b826f72be5a97f1fb5897e5dc550133038(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774e64f967588fb275ddcd27a2f5a55af3f8507fc44bc04797ea3ac542ae20de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e573cb4398fc41bfd58738cc7b8d91e72eb7477482807c456131f8b8b31b5af2(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsEndTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66403e4cc60448471bf31bc56f3df7e1b9ce2db69808021035265f342ce29da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693c65d58f441e605698275c5f5951371bc37fa98648d1f8394f1097d3dd089f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b822b9ff1b9b665353b8d31f32a680eb4fdf37a018f77b8eee04434e88e054d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cff677deb13d5010a6fbccf50aabf3b32c788133fc7228ba4abee01ee928dad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bf7d17d14a694dd480724380e2af9735b12b1c368d8b57ea872b8ba682be05(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61355b6276df59fe3773c7b02a0ec0585d789a72564cf0c073e28704ecceacf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e55bcff529d4166003a50929bcc91bca1e564800a4964b9eebc33da3c46973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a99ae5d2e51e368b4fc8df3359e4cf3979bfa0a235dbf58d1be3a5796e72527(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e8af24b4fbcca260d12d2538a6990f3d2ff848fd5984c6abcc96c04177012b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c75ad4714faa4da0563f773429f5f9b3c2a8e6a37392eaa949392f02a8e582(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6900521c5fe0dad48270e6fd8e330c0604fdb5650779f149f0f6be35afec751f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbf57ebc3ecade879e38f2eef249df4a111ca98f33c1a51d14dab451e4e5d0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bded77947d933b013757e489ad6e0142ca18600e3da4e33525191f2c28ad13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb72b6d400fc27cba940b1b3890cf5e4e09cb3d6e699045b7ea230a6b006805(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad48bfe9a0564140853f9b82591a9031710b5b76942f9a885c4cf87edd6ba6d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f74f8292f004b2cacb2b6602e4041c6b4a0169df1017b0512496fcc04da396(
    value: typing.Optional[ClouddeployDeployPolicyRulesRolloutRestrictionTimeWindowsWeeklyWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fbe8d6d18209dc4893386f44b81e893bb9cd6dc92eae432e7e84e6a9479d22(
    *,
    delivery_pipeline: typing.Optional[typing.Union[ClouddeployDeployPolicySelectorsDeliveryPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    target: typing.Optional[typing.Union[ClouddeployDeployPolicySelectorsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b81bdd580e0bf974368693287075d8720db920c6f3f617b6f5f8bb00807c04(
    *,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8b6a289b1e780569c5070c546559df85a0d56c1500f1ce0f84cc21a4d8a258(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d348ae443aab5c6637eb109a79364427b88f9e692e03e88294c348610146e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530612b6af00388384b1cd5647870b9947656edbbf640ca0195f85a908e1807d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e236dccf7916df8301231fe29d5de886cbd0708f82d37ed7d11f117bcb26295(
    value: typing.Optional[ClouddeployDeployPolicySelectorsDeliveryPipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d70a13c76340dfd2f854fd1bd6e9d90201bcf0bfd7349f4f8370dd1c5b78c38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96e25254fa263e5f1a065ebaa28e7d3ab316970f08777324cbd6aaae1618b27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2132466f817bc3c22ae0491e7ea8509303160c0ea2113a0dd86515a0209620da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa08956144beab7c5fa523d21a59d6ba2e7fd0395f7e446a7b266d489cdf5f75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3202e7ac51edd9be34249b061788018308d85817165af60c92f75c6fc4f33000(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f87f308208ee99d165c8c7492f7546337ecabda463394e2c1bddbde293ccab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ClouddeployDeployPolicySelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a581d2723f44e022f8cace0e382e9bc2a9c11d278d1966e14456330952fa00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee802b37448bff90309c80d1b0d5daad66d007c608c9e5c9e70bf22bdabb3f6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicySelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f928d834be11bdac2dcd60966664bb79466172da9fd86672f32e359ab780d749(
    *,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57939da2b78830e899348b3554f7f9d9cc15082f0b4e94901636ecc2236cf757(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720b6e9f86be3838af6e64d3fdf60f42fe7210bd150b2e17e36e43aa4d56703b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3061e0c46cbec072abd41f1ca57be50899537f3b726e715faa14e39ea09652d8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a1a573cf5463f686bf6fcf2d6fa866fe79b9dc59e3c52cb376621880b0191d(
    value: typing.Optional[ClouddeployDeployPolicySelectorsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1979da5efdcb52e94bccf8468a4b1740b0f43255e6586a720305ab782adf01c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6e93bf22e1c7b832bb305d8df7017719bae5c087a2650c64bacbce841b1b75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73b19e35d02db8993429ab677781c75aa748a87a318acd70cdf9a8b1ef960be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6986142f61cc6b02aa05f2a0c250b167ddfd50d3d6f7267d8057903802ba6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af099b6900a9e71e74e039fc67251a3042caa55bee360ec4a122b90e8be9e458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd7294295d96e92d9fd04ab7569ba457a3f8dfec4a68167d5e07864fc682806(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ClouddeployDeployPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
