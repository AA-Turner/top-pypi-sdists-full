r'''
# `google_compute_preview_feature`

Refer to the Terraform Registry for docs: [`google_compute_preview_feature`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature).
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


class GoogleComputePreviewFeature(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeature",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature google_compute_preview_feature}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        activation_status: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rollout_operation: typing.Optional[typing.Union["GoogleComputePreviewFeatureRolloutOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputePreviewFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature google_compute_preview_feature} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param activation_status: The activation status of the preview feature. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#activation_status GoogleComputePreviewFeature#activation_status}
        :param name: The name of the preview feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#name GoogleComputePreviewFeature#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#id GoogleComputePreviewFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#project GoogleComputePreviewFeature#project}.
        :param rollout_operation: rollout_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#rollout_operation GoogleComputePreviewFeature#rollout_operation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#timeouts GoogleComputePreviewFeature#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e81c37e78235e055cd1fcd3bf33f738671fae9c88d385a1e4836bdb6e9e0246)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputePreviewFeatureConfig(
            activation_status=activation_status,
            name=name,
            id=id,
            project=project,
            rollout_operation=rollout_operation,
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
        '''Generates CDKTF code for importing a GoogleComputePreviewFeature resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputePreviewFeature to import.
        :param import_from_id: The id of the existing GoogleComputePreviewFeature that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputePreviewFeature to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71660f02df3a8d79fafca10e879aee4f2921c0f7d7d730859de8f2bd168db8d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRolloutOperation")
    def put_rollout_operation(
        self,
        *,
        rollout_input: typing.Optional[typing.Union["GoogleComputePreviewFeatureRolloutOperationRolloutInput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param rollout_input: rollout_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#rollout_input GoogleComputePreviewFeature#rollout_input}
        '''
        value = GoogleComputePreviewFeatureRolloutOperation(
            rollout_input=rollout_input
        )

        return typing.cast(None, jsii.invoke(self, "putRolloutOperation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#create GoogleComputePreviewFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#delete GoogleComputePreviewFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#update GoogleComputePreviewFeature#update}.
        '''
        value = GoogleComputePreviewFeatureTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRolloutOperation")
    def reset_rollout_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutOperation", []))

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
    @jsii.member(jsii_name="rolloutOperation")
    def rollout_operation(
        self,
    ) -> "GoogleComputePreviewFeatureRolloutOperationOutputReference":
        return typing.cast("GoogleComputePreviewFeatureRolloutOperationOutputReference", jsii.get(self, "rolloutOperation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputePreviewFeatureTimeoutsOutputReference":
        return typing.cast("GoogleComputePreviewFeatureTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="activationStatusInput")
    def activation_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activationStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutOperationInput")
    def rollout_operation_input(
        self,
    ) -> typing.Optional["GoogleComputePreviewFeatureRolloutOperation"]:
        return typing.cast(typing.Optional["GoogleComputePreviewFeatureRolloutOperation"], jsii.get(self, "rolloutOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputePreviewFeatureTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputePreviewFeatureTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="activationStatus")
    def activation_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activationStatus"))

    @activation_status.setter
    def activation_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9f4179bd8628ff2369715c27c0ce6126b00dae7a282c314d79e55e04eec46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f411c725f6e5cef05f77cdbb69b922b6641ed03e7dfe3c63205fe3f2210636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e26f7d3f95e759a6a59c2b1ebc71fa05cd767914225778d77dfed4b8e3b09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6629207d73a3f409d9e1d20dadc54a2055131d5d617cc6da99a4c6a85300143e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "activation_status": "activationStatus",
        "name": "name",
        "id": "id",
        "project": "project",
        "rollout_operation": "rolloutOperation",
        "timeouts": "timeouts",
    },
)
class GoogleComputePreviewFeatureConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        activation_status: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        rollout_operation: typing.Optional[typing.Union["GoogleComputePreviewFeatureRolloutOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputePreviewFeatureTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param activation_status: The activation status of the preview feature. Possible values: ["ENABLED", "DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#activation_status GoogleComputePreviewFeature#activation_status}
        :param name: The name of the preview feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#name GoogleComputePreviewFeature#name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#id GoogleComputePreviewFeature#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#project GoogleComputePreviewFeature#project}.
        :param rollout_operation: rollout_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#rollout_operation GoogleComputePreviewFeature#rollout_operation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#timeouts GoogleComputePreviewFeature#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rollout_operation, dict):
            rollout_operation = GoogleComputePreviewFeatureRolloutOperation(**rollout_operation)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputePreviewFeatureTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d84e57ce5badf67e50ab61a575ea099dad7bff526b8d2bb12915822e69c22a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument activation_status", value=activation_status, expected_type=type_hints["activation_status"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument rollout_operation", value=rollout_operation, expected_type=type_hints["rollout_operation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "activation_status": activation_status,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if rollout_operation is not None:
            self._values["rollout_operation"] = rollout_operation
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
    def activation_status(self) -> builtins.str:
        '''The activation status of the preview feature. Possible values: ["ENABLED", "DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#activation_status GoogleComputePreviewFeature#activation_status}
        '''
        result = self._values.get("activation_status")
        assert result is not None, "Required property 'activation_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the preview feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#name GoogleComputePreviewFeature#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#id GoogleComputePreviewFeature#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#project GoogleComputePreviewFeature#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollout_operation(
        self,
    ) -> typing.Optional["GoogleComputePreviewFeatureRolloutOperation"]:
        '''rollout_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#rollout_operation GoogleComputePreviewFeature#rollout_operation}
        '''
        result = self._values.get("rollout_operation")
        return typing.cast(typing.Optional["GoogleComputePreviewFeatureRolloutOperation"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputePreviewFeatureTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#timeouts GoogleComputePreviewFeature#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputePreviewFeatureTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputePreviewFeatureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureRolloutOperation",
    jsii_struct_bases=[],
    name_mapping={"rollout_input": "rolloutInput"},
)
class GoogleComputePreviewFeatureRolloutOperation:
    def __init__(
        self,
        *,
        rollout_input: typing.Optional[typing.Union["GoogleComputePreviewFeatureRolloutOperationRolloutInput", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param rollout_input: rollout_input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#rollout_input GoogleComputePreviewFeature#rollout_input}
        '''
        if isinstance(rollout_input, dict):
            rollout_input = GoogleComputePreviewFeatureRolloutOperationRolloutInput(**rollout_input)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8da80aa39ed087359a905e89eb9d4d733dcb591e60f1bc45ce8090326d9859)
            check_type(argname="argument rollout_input", value=rollout_input, expected_type=type_hints["rollout_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rollout_input is not None:
            self._values["rollout_input"] = rollout_input

    @builtins.property
    def rollout_input(
        self,
    ) -> typing.Optional["GoogleComputePreviewFeatureRolloutOperationRolloutInput"]:
        '''rollout_input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#rollout_input GoogleComputePreviewFeature#rollout_input}
        '''
        result = self._values.get("rollout_input")
        return typing.cast(typing.Optional["GoogleComputePreviewFeatureRolloutOperationRolloutInput"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputePreviewFeatureRolloutOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputePreviewFeatureRolloutOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureRolloutOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff4475b68d240dc9691aa8641c96172c074f553c16abe7299e62cb62ba2e7694)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRolloutInput")
    def put_rollout_input(self, *, predefined_rollout_plan: builtins.str) -> None:
        '''
        :param predefined_rollout_plan: Predefined rollout plans. Possible values: ["ROLLOUT_PLAN_FAST_ROLLOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#predefined_rollout_plan GoogleComputePreviewFeature#predefined_rollout_plan}
        '''
        value = GoogleComputePreviewFeatureRolloutOperationRolloutInput(
            predefined_rollout_plan=predefined_rollout_plan
        )

        return typing.cast(None, jsii.invoke(self, "putRolloutInput", [value]))

    @jsii.member(jsii_name="resetRolloutInput")
    def reset_rollout_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutInput", []))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(
        self,
    ) -> "GoogleComputePreviewFeatureRolloutOperationRolloutInputOutputReference":
        return typing.cast("GoogleComputePreviewFeatureRolloutOperationRolloutInputOutputReference", jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInputInput")
    def rollout_input_input(
        self,
    ) -> typing.Optional["GoogleComputePreviewFeatureRolloutOperationRolloutInput"]:
        return typing.cast(typing.Optional["GoogleComputePreviewFeatureRolloutOperationRolloutInput"], jsii.get(self, "rolloutInputInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputePreviewFeatureRolloutOperation]:
        return typing.cast(typing.Optional[GoogleComputePreviewFeatureRolloutOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputePreviewFeatureRolloutOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44438b73f5d392fdfc43da1c91a7f62b49cefa7cf80943eab7a2bf201d3f1adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureRolloutOperationRolloutInput",
    jsii_struct_bases=[],
    name_mapping={"predefined_rollout_plan": "predefinedRolloutPlan"},
)
class GoogleComputePreviewFeatureRolloutOperationRolloutInput:
    def __init__(self, *, predefined_rollout_plan: builtins.str) -> None:
        '''
        :param predefined_rollout_plan: Predefined rollout plans. Possible values: ["ROLLOUT_PLAN_FAST_ROLLOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#predefined_rollout_plan GoogleComputePreviewFeature#predefined_rollout_plan}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e20c8c1902c0444062c40f3841dc1772982046cac153817ebd213382a9e730)
            check_type(argname="argument predefined_rollout_plan", value=predefined_rollout_plan, expected_type=type_hints["predefined_rollout_plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "predefined_rollout_plan": predefined_rollout_plan,
        }

    @builtins.property
    def predefined_rollout_plan(self) -> builtins.str:
        '''Predefined rollout plans. Possible values: ["ROLLOUT_PLAN_FAST_ROLLOUT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#predefined_rollout_plan GoogleComputePreviewFeature#predefined_rollout_plan}
        '''
        result = self._values.get("predefined_rollout_plan")
        assert result is not None, "Required property 'predefined_rollout_plan' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputePreviewFeatureRolloutOperationRolloutInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputePreviewFeatureRolloutOperationRolloutInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureRolloutOperationRolloutInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d05e665d0da037caaf94a2b5b2c55555089498d02649a4d029df28099440fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="predefinedRolloutPlanInput")
    def predefined_rollout_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "predefinedRolloutPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="predefinedRolloutPlan")
    def predefined_rollout_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predefinedRolloutPlan"))

    @predefined_rollout_plan.setter
    def predefined_rollout_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd4fbda469c444182ec36c591205e06c5dfe27f98987f5dcede9b0a68266e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predefinedRolloutPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputePreviewFeatureRolloutOperationRolloutInput]:
        return typing.cast(typing.Optional[GoogleComputePreviewFeatureRolloutOperationRolloutInput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputePreviewFeatureRolloutOperationRolloutInput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b63ec40f1a05c1aaee29f51b5ad777c42844f66eec50f916c4c9008834c6d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputePreviewFeatureTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#create GoogleComputePreviewFeature#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#delete GoogleComputePreviewFeature#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#update GoogleComputePreviewFeature#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264ef8616c024388d0d24f2d53d1115aa0798c2a8284eb64b7404bb8aa20a140)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#create GoogleComputePreviewFeature#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#delete GoogleComputePreviewFeature#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_compute_preview_feature#update GoogleComputePreviewFeature#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputePreviewFeatureTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputePreviewFeatureTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputePreviewFeature.GoogleComputePreviewFeatureTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d968d562d6e291dcbd7c835203c905988544e32d2c4d3662dfa837f778827c0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e275ac074c33679808c41c3540d20f5719f8d20b478d3b94873f3b9bbf0aa71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72abe8de8a3040ac2b435130d6ac98e367545604cb2ab67141c6b0b5e0291002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cfe668cf22faccc09cb6f362f2a412e32fae7c593868a25644bead49575423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputePreviewFeatureTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputePreviewFeatureTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputePreviewFeatureTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262735f657b95267c88fe5d8dff4fa821539512ae271b3f071194323e554045d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputePreviewFeature",
    "GoogleComputePreviewFeatureConfig",
    "GoogleComputePreviewFeatureRolloutOperation",
    "GoogleComputePreviewFeatureRolloutOperationOutputReference",
    "GoogleComputePreviewFeatureRolloutOperationRolloutInput",
    "GoogleComputePreviewFeatureRolloutOperationRolloutInputOutputReference",
    "GoogleComputePreviewFeatureTimeouts",
    "GoogleComputePreviewFeatureTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4e81c37e78235e055cd1fcd3bf33f738671fae9c88d385a1e4836bdb6e9e0246(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    activation_status: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rollout_operation: typing.Optional[typing.Union[GoogleComputePreviewFeatureRolloutOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputePreviewFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__71660f02df3a8d79fafca10e879aee4f2921c0f7d7d730859de8f2bd168db8d4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9f4179bd8628ff2369715c27c0ce6126b00dae7a282c314d79e55e04eec46d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f411c725f6e5cef05f77cdbb69b922b6641ed03e7dfe3c63205fe3f2210636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e26f7d3f95e759a6a59c2b1ebc71fa05cd767914225778d77dfed4b8e3b09a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6629207d73a3f409d9e1d20dadc54a2055131d5d617cc6da99a4c6a85300143e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d84e57ce5badf67e50ab61a575ea099dad7bff526b8d2bb12915822e69c22a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    activation_status: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    rollout_operation: typing.Optional[typing.Union[GoogleComputePreviewFeatureRolloutOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputePreviewFeatureTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8da80aa39ed087359a905e89eb9d4d733dcb591e60f1bc45ce8090326d9859(
    *,
    rollout_input: typing.Optional[typing.Union[GoogleComputePreviewFeatureRolloutOperationRolloutInput, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4475b68d240dc9691aa8641c96172c074f553c16abe7299e62cb62ba2e7694(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44438b73f5d392fdfc43da1c91a7f62b49cefa7cf80943eab7a2bf201d3f1adc(
    value: typing.Optional[GoogleComputePreviewFeatureRolloutOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e20c8c1902c0444062c40f3841dc1772982046cac153817ebd213382a9e730(
    *,
    predefined_rollout_plan: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d05e665d0da037caaf94a2b5b2c55555089498d02649a4d029df28099440fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd4fbda469c444182ec36c591205e06c5dfe27f98987f5dcede9b0a68266e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b63ec40f1a05c1aaee29f51b5ad777c42844f66eec50f916c4c9008834c6d6d(
    value: typing.Optional[GoogleComputePreviewFeatureRolloutOperationRolloutInput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264ef8616c024388d0d24f2d53d1115aa0798c2a8284eb64b7404bb8aa20a140(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d968d562d6e291dcbd7c835203c905988544e32d2c4d3662dfa837f778827c0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e275ac074c33679808c41c3540d20f5719f8d20b478d3b94873f3b9bbf0aa71d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72abe8de8a3040ac2b435130d6ac98e367545604cb2ab67141c6b0b5e0291002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cfe668cf22faccc09cb6f362f2a412e32fae7c593868a25644bead49575423(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262735f657b95267c88fe5d8dff4fa821539512ae271b3f071194323e554045d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputePreviewFeatureTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
