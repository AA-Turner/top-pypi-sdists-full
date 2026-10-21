r'''
# Amazon WorkSpaces Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_workspaces as workspaces
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for WorkSpaces construct libraries](https://constructs.dev/search?q=workspaces)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::WorkSpaces resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WorkSpaces.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::WorkSpaces](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WorkSpaces.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from .._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk as _aws_cdk_0cae9daa
    import aws_cdk.interfaces.aws_workspaces as _aws_workspaces_4620141e
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_workspaces_4620141e = _LazyImport("aws_cdk.interfaces.aws_workspaces")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_workspaces_4620141e.IConnectionAliasRef, _aws_cdk_0cae9daa.ITaggable)
class CfnConnectionAlias(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_workspaces.CfnConnectionAlias",
):
    '''The ``AWS::WorkSpaces::ConnectionAlias`` resource specifies a connection alias.

    Connection aliases are used for cross-Region redirection. For more information, see `Cross-Region Redirection for Amazon WorkSpaces <https://docs.aws.amazon.com/workspaces/latest/adminguide/cross-region-redirection.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html
    :cloudformationResource: AWS::WorkSpaces::ConnectionAlias
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_workspaces as workspaces
        
        cfn_connection_alias = workspaces.CfnConnectionAlias(self, "MyCfnConnectionAlias",
            connection_string="connectionString",
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        connection_string: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WorkSpaces::ConnectionAlias``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param connection_string: The connection string specified for the connection alias. The connection string must be in the form of a fully qualified domain name (FQDN), such as ``www.example.com`` .
        :param tags: The tags to associate with the connection alias.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3fd73d00432c1164a74beb35acf6162e3d82fa91d51a0edf8c896028b6e3c6d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectionAliasProps(connection_string=connection_string, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnConnectionAlias")
    @builtins.classmethod
    def is_cfn_connection_alias(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnConnectionAlias.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__76f39ec24ce0950d3ba9ddf713f5b5c8349a489a83df314a68c350efb2fde838)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnConnectionAlias", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__70d07e3ef46b7d1868d493367bae11c00c38fa0bb35cfa4e162e97b1482bf156)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5d590d73fb55367a8be64477837c062053aa020d8931e1f1983124013786434f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAliasId")
    def attr_alias_id(self) -> builtins.str:
        '''The identifier of the connection alias, returned as a string.

        :cloudformationAttribute: AliasId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAliasId"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociations")
    def attr_associations(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The association status of the connection alias.

        :cloudformationAttribute: Associations
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrAssociations"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectionAliasState")
    def attr_connection_alias_state(self) -> builtins.str:
        '''The current state of the connection alias, returned as a string.

        :cloudformationAttribute: ConnectionAliasState
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectionAliasState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="connectionAliasRef")
    def connection_alias_ref(
        self,
    ) -> "_aws_workspaces_4620141e.ConnectionAliasReference":
        '''A reference to a ConnectionAlias resource.'''
        return typing.cast("_aws_workspaces_4620141e.ConnectionAliasReference", jsii.get(self, "connectionAliasRef"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> builtins.str:
        '''The connection string specified for the connection alias.'''
        return typing.cast(builtins.str, jsii.get(self, "connectionString"))

    @connection_string.setter
    def connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ac8b72c0a6880f896fe31f0555dd87dfdcce86c05579ff4a417ab736a03b4fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsRaw")
    def tags_raw(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags to associate with the connection alias.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tagsRaw"))

    @tags_raw.setter
    def tags_raw(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6cf34741743106631ede324d61fdd5ed726b94e64d09574347d59201303db6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsRaw", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnConnectionAlias.ConnectionAliasAssociationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "associated_account_id": "associatedAccountId",
            "association_status": "associationStatus",
            "connection_identifier": "connectionIdentifier",
            "resource_id": "resourceId",
        },
    )
    class ConnectionAliasAssociationProperty:
        def __init__(
            self,
            *,
            associated_account_id: typing.Optional[builtins.str] = None,
            association_status: typing.Optional[builtins.str] = None,
            connection_identifier: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a connection alias association that is used for cross-Region redirection.

            For more information, see `Cross-Region Redirection for Amazon WorkSpaces <https://docs.aws.amazon.com/workspaces/latest/adminguide/cross-region-redirection.html>`_ .

            :param associated_account_id: The identifier of the AWS account that associated the connection alias with a directory.
            :param association_status: The association status of the connection alias.
            :param connection_identifier: The identifier of the connection alias association. You use the connection identifier in the DNS TXT record when you're configuring your DNS routing policies.
            :param resource_id: The identifier of the directory associated with a connection alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                connection_alias_association_property = workspaces.CfnConnectionAlias.ConnectionAliasAssociationProperty(
                    associated_account_id="associatedAccountId",
                    association_status="associationStatus",
                    connection_identifier="connectionIdentifier",
                    resource_id="resourceId"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__614a827f45558e3ee89a9937d774dc07580e2d2d88ccf9a78ea211acad9d7c19)
                check_type(argname="argument associated_account_id", value=associated_account_id, expected_type=type_hints["associated_account_id"])
                check_type(argname="argument association_status", value=association_status, expected_type=type_hints["association_status"])
                check_type(argname="argument connection_identifier", value=connection_identifier, expected_type=type_hints["connection_identifier"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if associated_account_id is not None:
                self._values["associated_account_id"] = associated_account_id
            if association_status is not None:
                self._values["association_status"] = association_status
            if connection_identifier is not None:
                self._values["connection_identifier"] = connection_identifier
            if resource_id is not None:
                self._values["resource_id"] = resource_id

        @builtins.property
        def associated_account_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS account that associated the connection alias with a directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-associatedaccountid
            '''
            result = self._values.get("associated_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def association_status(self) -> typing.Optional[builtins.str]:
            '''The association status of the connection alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-associationstatus
            '''
            result = self._values.get("association_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_identifier(self) -> typing.Optional[builtins.str]:
            '''The identifier of the connection alias association.

            You use the connection identifier in the DNS TXT record when you're configuring your DNS routing policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-connectionidentifier
            '''
            result = self._values.get("connection_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the directory associated with a connection alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-connectionalias-connectionaliasassociation.html#cfn-workspaces-connectionalias-connectionaliasassociation-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionAliasAssociationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_workspaces.CfnConnectionAliasProps",
    jsii_struct_bases=[],
    name_mapping={"connection_string": "connectionString", "tags": "tags"},
)
class CfnConnectionAliasProps:
    def __init__(
        self,
        *,
        connection_string: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnectionAlias``.

        :param connection_string: The connection string specified for the connection alias. The connection string must be in the form of a fully qualified domain name (FQDN), such as ``www.example.com`` .
        :param tags: The tags to associate with the connection alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_workspaces as workspaces
            
            cfn_connection_alias_props = workspaces.CfnConnectionAliasProps(
                connection_string="connectionString",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__33d1c548638caf6c8699dd74d5bcc8d8df516e1a0738521496aee37402727de8)
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_string": connection_string,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_string(self) -> builtins.str:
        '''The connection string specified for the connection alias.

        The connection string must be in the form of a fully qualified domain name (FQDN), such as ``www.example.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html#cfn-workspaces-connectionalias-connectionstring
        '''
        result = self._values.get("connection_string")
        assert result is not None, "Required property 'connection_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags to associate with the connection alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-connectionalias.html#cfn-workspaces-connectionalias-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_workspaces_4620141e.IDirectoryRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnDirectory(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory",
):
    '''Resource Type definition for AWS::WorkSpaces::Directory.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html
    :cloudformationResource: AWS::WorkSpaces::Directory
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_workspaces as workspaces
        
        cfn_directory = workspaces.CfnDirectory(self, "MyCfnDirectory",
            active_directory_config=workspaces.CfnDirectory.ActiveDirectoryConfigProperty(
                domain_name="domainName",
                service_account_secret_arn="serviceAccountSecretArn"
            ),
            certificate_based_auth_properties=workspaces.CfnDirectory.CertificateBasedAuthPropertiesProperty(
                certificate_authority_arn="certificateAuthorityArn",
                status="status"
            ),
            enable_self_service=False,
            endpoint_encryption_mode="endpointEncryptionMode",
            idc_instance_arn="idcInstanceArn",
            ip_group_ids=["ipGroupIds"],
            microsoft_entra_config=workspaces.CfnDirectory.MicrosoftEntraConfigProperty(
                application_config_secret_arn="applicationConfigSecretArn",
                tenant_id="tenantId"
            ),
            saml_properties=workspaces.CfnDirectory.SamlPropertiesProperty(
                relay_state_parameter_name="relayStateParameterName",
                status="status",
                user_access_url="userAccessUrl"
            ),
            selfservice_permissions=workspaces.CfnDirectory.SelfservicePermissionsProperty(
                change_compute_type="changeComputeType",
                increase_volume_size="increaseVolumeSize",
                rebuild_workspace="rebuildWorkspace",
                restart_workspace="restartWorkspace",
                switch_running_mode="switchRunningMode"
            ),
            streaming_properties=workspaces.CfnDirectory.StreamingPropertiesProperty(
                global_accelerator=workspaces.CfnDirectory.GlobalAcceleratorForDirectoryProperty(
                    mode="mode",
        
                    # the properties below are optional
                    preferred_protocol="preferredProtocol"
                ),
                storage_connectors=[workspaces.CfnDirectory.StorageConnectorProperty(
                    connector_type="connectorType",
                    status="status"
                )],
                streaming_experience_preferred_protocol="streamingExperiencePreferredProtocol",
                user_settings=[workspaces.CfnDirectory.UserSettingProperty(
                    action="action",
                    permission="permission",
        
                    # the properties below are optional
                    maximum_length=123
                )]
            ),
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tenancy="tenancy",
            user_identity_type="userIdentityType",
            workspace_access_properties=workspaces.CfnDirectory.WorkspaceAccessPropertiesProperty(
                access_endpoint_config=workspaces.CfnDirectory.AccessEndpointConfigProperty(
                    access_endpoints=[workspaces.CfnDirectory.AccessEndpointProperty(
                        access_endpoint_type="accessEndpointType",
                        vpc_endpoint_id="vpcEndpointId"
                    )],
        
                    # the properties below are optional
                    internet_fallback_protocols=["internetFallbackProtocols"]
                ),
                device_type_android="deviceTypeAndroid",
                device_type_chrome_os="deviceTypeChromeOs",
                device_type_ios="deviceTypeIos",
                device_type_linux="deviceTypeLinux",
                device_type_osx="deviceTypeOsx",
                device_type_web="deviceTypeWeb",
                device_type_windows="deviceTypeWindows",
                device_type_work_spaces_thin_client="deviceTypeWorkSpacesThinClient",
                device_type_zero_client="deviceTypeZeroClient"
            ),
            workspace_creation_properties=workspaces.CfnDirectory.DefaultWorkspaceCreationPropertiesProperty(
                custom_security_group_id="customSecurityGroupId",
                default_ou="defaultOu",
                enable_internet_access=False,
                enable_maintenance_mode=False,
                instance_iam_role_arn="instanceIamRoleArn",
                user_enabled_as_local_administrator=False
            ),
            workspace_directory_description="workspaceDirectoryDescription",
            workspace_directory_name="workspaceDirectoryName",
            workspace_type="workspaceType"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        active_directory_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.ActiveDirectoryConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate_based_auth_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.CertificateBasedAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_self_service: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        endpoint_encryption_mode: typing.Optional[builtins.str] = None,
        idc_instance_arn: typing.Optional[builtins.str] = None,
        ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        microsoft_entra_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.MicrosoftEntraConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        saml_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.SamlPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        selfservice_permissions: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.SelfservicePermissionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        streaming_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.StreamingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        tenancy: typing.Optional[builtins.str] = None,
        user_identity_type: typing.Optional[builtins.str] = None,
        workspace_access_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.WorkspaceAccessPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace_creation_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.DefaultWorkspaceCreationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace_directory_description: typing.Optional[builtins.str] = None,
        workspace_directory_name: typing.Optional[builtins.str] = None,
        workspace_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::WorkSpaces::Directory``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param active_directory_config: Information about the Active Directory config.
        :param certificate_based_auth_properties: Describes the properties of the certificate-based authentication you want to use with your WorkSpaces.
        :param enable_self_service: Indicates whether self-service capabilities are enabled or disabled.
        :param endpoint_encryption_mode: Endpoint encryption mode that allows you to configure the specified directory between Standard TLS and FIPS 140-2 validated mode.
        :param idc_instance_arn: The Amazon Resource Name (ARN) of the identity center instance.
        :param ip_group_ids: The identifiers of the IP access control groups associated with the directory.
        :param microsoft_entra_config: Specifies the configurations of the Microsoft Entra.
        :param saml_properties: Describes the enablement status, user access URL, and relay state parameter name that are used for configuring federation with an SAML 2.0 identity provider.
        :param selfservice_permissions: Describes the self-service permissions for a directory.
        :param streaming_properties: Describes the streaming properties.
        :param subnet_ids: The identifiers of the subnets for your virtual private cloud (VPC).
        :param tags: The tags associated with the directory.
        :param tenancy: Indicates whether your WorkSpace directory is dedicated or shared.
        :param user_identity_type: The type of identity management the user is using.
        :param workspace_access_properties: The device types and operating systems that can be used to access a WorkSpace.
        :param workspace_creation_properties: The default values that are used to create WorkSpaces.
        :param workspace_directory_description: Description of the directory to register.
        :param workspace_directory_name: The name of the directory to register.
        :param workspace_type: Indicates whether the directory's WorkSpace type is personal or pools.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__97d2fd090a322f0e86011be41549fee5ba73daf4f5f02076bb14f2e5c613cc90)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDirectoryProps(
            active_directory_config=active_directory_config,
            certificate_based_auth_properties=certificate_based_auth_properties,
            enable_self_service=enable_self_service,
            endpoint_encryption_mode=endpoint_encryption_mode,
            idc_instance_arn=idc_instance_arn,
            ip_group_ids=ip_group_ids,
            microsoft_entra_config=microsoft_entra_config,
            saml_properties=saml_properties,
            selfservice_permissions=selfservice_permissions,
            streaming_properties=streaming_properties,
            subnet_ids=subnet_ids,
            tags=tags,
            tenancy=tenancy,
            user_identity_type=user_identity_type,
            workspace_access_properties=workspace_access_properties,
            workspace_creation_properties=workspace_creation_properties,
            workspace_directory_description=workspace_directory_description,
            workspace_directory_name=workspace_directory_name,
            workspace_type=workspace_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForDirectory")
    @builtins.classmethod
    def arn_for_directory(
        cls,
        resource: "_aws_workspaces_4620141e.IDirectoryRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cdffabab5518c6dfd10b6189ff95a9b939ec41d46c84120537446c0b207aa3f4)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForDirectory", [resource]))

    @jsii.member(jsii_name="isCfnDirectory")
    @builtins.classmethod
    def is_cfn_directory(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnDirectory.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__12748995b26571c6b584a78b311a91b4858d813a9de56630d9cc8a06efa30670)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnDirectory", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7d63a54fc0f25eb54b703a8b2271391a2de4dccf825da047fe18cc0e3bacac8)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c6bd5c53c0844aa7f2f45f96592d3cbb86fe27c7c773eede54fa6b91cd0c7f27)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAlias")
    def attr_alias(self) -> builtins.str:
        '''The directory alias.

        :cloudformationAttribute: Alias
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAlias"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the WorkSpace directory.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCustomerUserName")
    def attr_customer_user_name(self) -> builtins.str:
        '''The user name for the service account.

        :cloudformationAttribute: CustomerUserName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCustomerUserName"))

    @builtins.property
    @jsii.member(jsii_name="attrDirectoryId")
    def attr_directory_id(self) -> builtins.str:
        '''The directory identifier.

        :cloudformationAttribute: DirectoryId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDirectoryId"))

    @builtins.property
    @jsii.member(jsii_name="attrDirectoryName")
    def attr_directory_name(self) -> builtins.str:
        '''The name of the directory.

        :cloudformationAttribute: DirectoryName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDirectoryName"))

    @builtins.property
    @jsii.member(jsii_name="attrDirectoryType")
    def attr_directory_type(self) -> builtins.str:
        '''The directory type.

        :cloudformationAttribute: DirectoryType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDirectoryType"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsIpAddresses")
    def attr_dns_ip_addresses(self) -> typing.List[builtins.str]:
        '''The IP addresses of the DNS servers for the directory.

        :cloudformationAttribute: DnsIpAddresses
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrDnsIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsIpv6Addresses")
    def attr_dns_ipv6_addresses(self) -> typing.List[builtins.str]:
        '''The IPv6 addresses of the DNS servers for the directory.

        :cloudformationAttribute: DnsIpv6Addresses
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrDnsIpv6Addresses"))

    @builtins.property
    @jsii.member(jsii_name="attrIamRoleId")
    def attr_iam_role_id(self) -> builtins.str:
        '''The identifier of the IAM role.

        :cloudformationAttribute: IamRoleId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIamRoleId"))

    @builtins.property
    @jsii.member(jsii_name="attrIdcConfig")
    def attr_idc_config(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Specifies the configurations of the identity center.

        :cloudformationAttribute: IDCConfig
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrIdcConfig"))

    @builtins.property
    @jsii.member(jsii_name="attrRegistrationCode")
    def attr_registration_code(self) -> builtins.str:
        '''The registration code for the directory.

        :cloudformationAttribute: RegistrationCode
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegistrationCode"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the directory's registration with Amazon WorkSpaces.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrWorkspaceSecurityGroupId")
    def attr_workspace_security_group_id(self) -> builtins.str:
        '''The identifier of the security group that is assigned to new WorkSpaces.

        :cloudformationAttribute: WorkspaceSecurityGroupId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWorkspaceSecurityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="directoryRef")
    def directory_ref(self) -> "_aws_workspaces_4620141e.DirectoryReference":
        '''A reference to a Directory resource.'''
        return typing.cast("_aws_workspaces_4620141e.DirectoryReference", jsii.get(self, "directoryRef"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryConfig")
    def active_directory_config(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.ActiveDirectoryConfigProperty"]]:
        '''Information about the Active Directory config.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.ActiveDirectoryConfigProperty"]], jsii.get(self, "activeDirectoryConfig"))

    @active_directory_config.setter
    def active_directory_config(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.ActiveDirectoryConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d5935083ae4bb3e24425d51af0007be0cd0d57e8ff8ff72702ac9593e3f928cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateBasedAuthProperties")
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.CertificateBasedAuthPropertiesProperty"]]:
        '''Describes the properties of the certificate-based authentication you want to use with your WorkSpaces.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.CertificateBasedAuthPropertiesProperty"]], jsii.get(self, "certificateBasedAuthProperties"))

    @certificate_based_auth_properties.setter
    def certificate_based_auth_properties(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.CertificateBasedAuthPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c14bd4bcf3be59597cc94b6622b6d08872f213251205ed7e8ac43e7cd343d0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateBasedAuthProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSelfService")
    def enable_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Indicates whether self-service capabilities are enabled or disabled.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "enableSelfService"))

    @enable_self_service.setter
    def enable_self_service(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1d5b380d1fadf9673790a641ab3bc2d51de5797c899e2b3fd2d11f04cfd41aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSelfService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointEncryptionMode")
    def endpoint_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Endpoint encryption mode that allows you to configure the specified directory between Standard TLS and FIPS 140-2 validated mode.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointEncryptionMode"))

    @endpoint_encryption_mode.setter
    def endpoint_encryption_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d48bd075e1d5f4e21bd96297cef42d2f7dcd3b3b0b09282064e75850711378bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointEncryptionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idcInstanceArn")
    def idc_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the identity center instance.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idcInstanceArn"))

    @idc_instance_arn.setter
    def idc_instance_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3d199dd5b9442a70e651b9c77f9fa0566e1d9960e98c9c8baea8f22ee9287a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idcInstanceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipGroupIds")
    def ip_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identifiers of the IP access control groups associated with the directory.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipGroupIds"))

    @ip_group_ids.setter
    def ip_group_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c12cd311ffce9568cff4f9a934712be539ba52685ec7024f986cd60c7c1f3d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microsoftEntraConfig")
    def microsoft_entra_config(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.MicrosoftEntraConfigProperty"]]:
        '''Specifies the configurations of the Microsoft Entra.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.MicrosoftEntraConfigProperty"]], jsii.get(self, "microsoftEntraConfig"))

    @microsoft_entra_config.setter
    def microsoft_entra_config(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.MicrosoftEntraConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7c1c4fc7c0c44f9f4a3d44936bef556cf289dc3adb77a8f5f4eee4dac8dfc9b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microsoftEntraConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samlProperties")
    def saml_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SamlPropertiesProperty"]]:
        '''Describes the enablement status, user access URL, and relay state parameter name that are used for configuring federation with an SAML 2.0 identity provider.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SamlPropertiesProperty"]], jsii.get(self, "samlProperties"))

    @saml_properties.setter
    def saml_properties(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SamlPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1e9476ef4c83098329845a817adfab1e370a5ee7ed7efc8ef90ee6b255ea7f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selfservicePermissions")
    def selfservice_permissions(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SelfservicePermissionsProperty"]]:
        '''Describes the self-service permissions for a directory.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SelfservicePermissionsProperty"]], jsii.get(self, "selfservicePermissions"))

    @selfservice_permissions.setter
    def selfservice_permissions(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SelfservicePermissionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d850202b4b1b5c70f0967ed877c9383134b8b4322c36f14fa5a82730ae0e648a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selfservicePermissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamingProperties")
    def streaming_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StreamingPropertiesProperty"]]:
        '''Describes the streaming properties.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StreamingPropertiesProperty"]], jsii.get(self, "streamingProperties"))

    @streaming_properties.setter
    def streaming_properties(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StreamingPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b7f1f768604605fd8c2f117048afe270d2a8c642cf2f27bad1281c65a58b5feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identifiers of the subnets for your virtual private cloud (VPC).'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5bd17e443fdeffd0d8f357751e184e1e851c50a732595b91eec1b8bf5eb0ca0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the directory.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a0b57d5e0d13092d1ac273dd853c173fae7fcaba6c8767a4be90933c4e5df709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''Indicates whether your WorkSpace directory is dedicated or shared.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__edb1af56f4750cefa6bb0b0a5b6d97e4eee63424bda5338ea220b885617a0c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userIdentityType")
    def user_identity_type(self) -> typing.Optional[builtins.str]:
        '''The type of identity management the user is using.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdentityType"))

    @user_identity_type.setter
    def user_identity_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__23c9fb93d4661ad4bfb38b4968e127400e5a702021709244b6d658c01dbcfb7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIdentityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceAccessProperties")
    def workspace_access_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.WorkspaceAccessPropertiesProperty"]]:
        '''The device types and operating systems that can be used to access a WorkSpace.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.WorkspaceAccessPropertiesProperty"]], jsii.get(self, "workspaceAccessProperties"))

    @workspace_access_properties.setter
    def workspace_access_properties(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.WorkspaceAccessPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8724beb6e6ee10070a868ef023abdb06e729abd29cc0b01ac20a32b2c1bc1697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceAccessProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceCreationProperties")
    def workspace_creation_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.DefaultWorkspaceCreationPropertiesProperty"]]:
        '''The default values that are used to create WorkSpaces.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.DefaultWorkspaceCreationPropertiesProperty"]], jsii.get(self, "workspaceCreationProperties"))

    @workspace_creation_properties.setter
    def workspace_creation_properties(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.DefaultWorkspaceCreationPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__216b29943227b73b434fdf6b0fec0183add3a5cde23dcdc1d4fff9a5b8a97c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceCreationProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceDirectoryDescription")
    def workspace_directory_description(self) -> typing.Optional[builtins.str]:
        '''Description of the directory to register.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceDirectoryDescription"))

    @workspace_directory_description.setter
    def workspace_directory_description(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__098e67aa24151ba52b4a187547fe3bfe6102d7d77ffe9f5407daa4c43b979ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceDirectoryDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceDirectoryName")
    def workspace_directory_name(self) -> typing.Optional[builtins.str]:
        '''The name of the directory to register.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceDirectoryName"))

    @workspace_directory_name.setter
    def workspace_directory_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__87b41ec10b32352bd312188184670dee7448018cddc80956a217145e754c071e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceDirectoryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceType")
    def workspace_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the directory's WorkSpace type is personal or pools.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceType"))

    @workspace_type.setter
    def workspace_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__62a158204c3529104edbe60ac679af107f42bb82458981aeb6a21c799e00e3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceType", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.AccessEndpointConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_endpoints": "accessEndpoints",
            "internet_fallback_protocols": "internetFallbackProtocols",
        },
    )
    class AccessEndpointConfigProperty:
        def __init__(
            self,
            *,
            access_endpoints: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]],
            internet_fallback_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes the access endpoint configuration for a WorkSpace.

            :param access_endpoints: Indicates a list of access endpoints associated with this directory.
            :param internet_fallback_protocols: Indicates a list of protocols that fallback to using the public Internet when streaming over a VPC endpoint is not available.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-accessendpointconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                access_endpoint_config_property = workspaces.CfnDirectory.AccessEndpointConfigProperty(
                    access_endpoints=[workspaces.CfnDirectory.AccessEndpointProperty(
                        access_endpoint_type="accessEndpointType",
                        vpc_endpoint_id="vpcEndpointId"
                    )],
                
                    # the properties below are optional
                    internet_fallback_protocols=["internetFallbackProtocols"]
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__9ba9a18ad9d6cd68b06909aaad77c534309ec8d39f744baad2f2c7a8aae55852)
                check_type(argname="argument access_endpoints", value=access_endpoints, expected_type=type_hints["access_endpoints"])
                check_type(argname="argument internet_fallback_protocols", value=internet_fallback_protocols, expected_type=type_hints["internet_fallback_protocols"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "access_endpoints": access_endpoints,
            }
            if internet_fallback_protocols is not None:
                self._values["internet_fallback_protocols"] = internet_fallback_protocols

        @builtins.property
        def access_endpoints(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.AccessEndpointProperty"]]]:
            '''Indicates a list of access endpoints associated with this directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-accessendpointconfig.html#cfn-workspaces-directory-accessendpointconfig-accessendpoints
            '''
            result = self._values.get("access_endpoints")
            assert result is not None, "Required property 'access_endpoints' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.AccessEndpointProperty"]]], result)

        @builtins.property
        def internet_fallback_protocols(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates a list of protocols that fallback to using the public Internet when streaming over a VPC endpoint is not available.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-accessendpointconfig.html#cfn-workspaces-directory-accessendpointconfig-internetfallbackprotocols
            '''
            result = self._values.get("internet_fallback_protocols")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_endpoint_type": "accessEndpointType",
            "vpc_endpoint_id": "vpcEndpointId",
        },
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            access_endpoint_type: typing.Optional[builtins.str] = None,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the access type and endpoint for a WorkSpace.

            :param access_endpoint_type: Indicates the type of access endpoint.
            :param vpc_endpoint_id: Indicates the VPC endpoint to use for access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-accessendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                access_endpoint_property = workspaces.CfnDirectory.AccessEndpointProperty(
                    access_endpoint_type="accessEndpointType",
                    vpc_endpoint_id="vpcEndpointId"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__39185f9119f3d0883d05448778c03e1be9e3752bc4640c32fbd98609b6805ebf)
                check_type(argname="argument access_endpoint_type", value=access_endpoint_type, expected_type=type_hints["access_endpoint_type"])
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_endpoint_type is not None:
                self._values["access_endpoint_type"] = access_endpoint_type
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id

        @builtins.property
        def access_endpoint_type(self) -> typing.Optional[builtins.str]:
            '''Indicates the type of access endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-accessendpoint.html#cfn-workspaces-directory-accessendpoint-accessendpointtype
            '''
            result = self._values.get("access_endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''Indicates the VPC endpoint to use for access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-accessendpoint.html#cfn-workspaces-directory-accessendpoint-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.ActiveDirectoryConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "service_account_secret_arn": "serviceAccountSecretArn",
        },
    )
    class ActiveDirectoryConfigProperty:
        def __init__(
            self,
            *,
            domain_name: builtins.str,
            service_account_secret_arn: builtins.str,
        ) -> None:
            '''Information about the Active Directory config.

            :param domain_name: The name of the domain.
            :param service_account_secret_arn: Indicates the secret ARN on the service account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-activedirectoryconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                active_directory_config_property = workspaces.CfnDirectory.ActiveDirectoryConfigProperty(
                    domain_name="domainName",
                    service_account_secret_arn="serviceAccountSecretArn"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e4ea3bc303fd18efdf01d9d0ed5f93e34d450353289262313dca3511076eee9d)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument service_account_secret_arn", value=service_account_secret_arn, expected_type=type_hints["service_account_secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "domain_name": domain_name,
                "service_account_secret_arn": service_account_secret_arn,
            }

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''The name of the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-activedirectoryconfig.html#cfn-workspaces-directory-activedirectoryconfig-domainname
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_account_secret_arn(self) -> builtins.str:
            '''Indicates the secret ARN on the service account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-activedirectoryconfig.html#cfn-workspaces-directory-activedirectoryconfig-serviceaccountsecretarn
            '''
            result = self._values.get("service_account_secret_arn")
            assert result is not None, "Required property 'service_account_secret_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActiveDirectoryConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.CertificateBasedAuthPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_authority_arn": "certificateAuthorityArn",
            "status": "status",
        },
    )
    class CertificateBasedAuthPropertiesProperty:
        def __init__(
            self,
            *,
            certificate_authority_arn: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the properties of the certificate-based authentication you want to use with your WorkSpaces.

            :param certificate_authority_arn: The Amazon Resource Name (ARN) of the Amazon Web Services Certificate Manager Private CA resource.
            :param status: The status of the certificate-based authentication properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-certificatebasedauthproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                certificate_based_auth_properties_property = workspaces.CfnDirectory.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__8d5b4bd7bf8f7b42c1b026907d8b0c63a5212a29cec1f1dfe5d4e506ff2f338c)
                check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arn is not None:
                self._values["certificate_authority_arn"] = certificate_authority_arn
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Web Services Certificate Manager Private CA resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-certificatebasedauthproperties.html#cfn-workspaces-directory-certificatebasedauthproperties-certificateauthorityarn
            '''
            result = self._values.get("certificate_authority_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the certificate-based authentication properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-certificatebasedauthproperties.html#cfn-workspaces-directory-certificatebasedauthproperties-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateBasedAuthPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.DefaultWorkspaceCreationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_security_group_id": "customSecurityGroupId",
            "default_ou": "defaultOu",
            "enable_internet_access": "enableInternetAccess",
            "enable_maintenance_mode": "enableMaintenanceMode",
            "instance_iam_role_arn": "instanceIamRoleArn",
            "user_enabled_as_local_administrator": "userEnabledAsLocalAdministrator",
        },
    )
    class DefaultWorkspaceCreationPropertiesProperty:
        def __init__(
            self,
            *,
            custom_security_group_id: typing.Optional[builtins.str] = None,
            default_ou: typing.Optional[builtins.str] = None,
            enable_internet_access: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
            enable_maintenance_mode: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
            instance_iam_role_arn: typing.Optional[builtins.str] = None,
            user_enabled_as_local_administrator: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        ) -> None:
            '''The default values that are used to create WorkSpaces.

            :param custom_security_group_id: The identifier of the default security group to apply to WorkSpaces when they are created.
            :param default_ou: The organizational unit (OU) in the directory for the WorkSpace machine accounts.
            :param enable_internet_access: Specifies whether to automatically assign an Elastic public IP address to WorkSpaces in this directory by default.
            :param enable_maintenance_mode: Specifies whether maintenance mode is enabled for WorkSpaces.
            :param instance_iam_role_arn: Indicates the IAM role ARN of the instance.
            :param user_enabled_as_local_administrator: Specifies whether WorkSpace users are local administrators on their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                default_workspace_creation_properties_property = workspaces.CfnDirectory.DefaultWorkspaceCreationPropertiesProperty(
                    custom_security_group_id="customSecurityGroupId",
                    default_ou="defaultOu",
                    enable_internet_access=False,
                    enable_maintenance_mode=False,
                    instance_iam_role_arn="instanceIamRoleArn",
                    user_enabled_as_local_administrator=False
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__9ad3786ebe3af46bd62ca671ef7d20163db404055c890619acac286bc6b5ba71)
                check_type(argname="argument custom_security_group_id", value=custom_security_group_id, expected_type=type_hints["custom_security_group_id"])
                check_type(argname="argument default_ou", value=default_ou, expected_type=type_hints["default_ou"])
                check_type(argname="argument enable_internet_access", value=enable_internet_access, expected_type=type_hints["enable_internet_access"])
                check_type(argname="argument enable_maintenance_mode", value=enable_maintenance_mode, expected_type=type_hints["enable_maintenance_mode"])
                check_type(argname="argument instance_iam_role_arn", value=instance_iam_role_arn, expected_type=type_hints["instance_iam_role_arn"])
                check_type(argname="argument user_enabled_as_local_administrator", value=user_enabled_as_local_administrator, expected_type=type_hints["user_enabled_as_local_administrator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_security_group_id is not None:
                self._values["custom_security_group_id"] = custom_security_group_id
            if default_ou is not None:
                self._values["default_ou"] = default_ou
            if enable_internet_access is not None:
                self._values["enable_internet_access"] = enable_internet_access
            if enable_maintenance_mode is not None:
                self._values["enable_maintenance_mode"] = enable_maintenance_mode
            if instance_iam_role_arn is not None:
                self._values["instance_iam_role_arn"] = instance_iam_role_arn
            if user_enabled_as_local_administrator is not None:
                self._values["user_enabled_as_local_administrator"] = user_enabled_as_local_administrator

        @builtins.property
        def custom_security_group_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the default security group to apply to WorkSpaces when they are created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html#cfn-workspaces-directory-defaultworkspacecreationproperties-customsecuritygroupid
            '''
            result = self._values.get("custom_security_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_ou(self) -> typing.Optional[builtins.str]:
            '''The organizational unit (OU) in the directory for the WorkSpace machine accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html#cfn-workspaces-directory-defaultworkspacecreationproperties-defaultou
            '''
            result = self._values.get("default_ou")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_internet_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Specifies whether to automatically assign an Elastic public IP address to WorkSpaces in this directory by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html#cfn-workspaces-directory-defaultworkspacecreationproperties-enableinternetaccess
            '''
            result = self._values.get("enable_internet_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        @builtins.property
        def enable_maintenance_mode(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Specifies whether maintenance mode is enabled for WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html#cfn-workspaces-directory-defaultworkspacecreationproperties-enablemaintenancemode
            '''
            result = self._values.get("enable_maintenance_mode")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        @builtins.property
        def instance_iam_role_arn(self) -> typing.Optional[builtins.str]:
            '''Indicates the IAM role ARN of the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html#cfn-workspaces-directory-defaultworkspacecreationproperties-instanceiamrolearn
            '''
            result = self._values.get("instance_iam_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_enabled_as_local_administrator(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Specifies whether WorkSpace users are local administrators on their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-defaultworkspacecreationproperties.html#cfn-workspaces-directory-defaultworkspacecreationproperties-userenabledaslocaladministrator
            '''
            result = self._values.get("user_enabled_as_local_administrator")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultWorkspaceCreationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.GlobalAcceleratorForDirectoryProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode", "preferred_protocol": "preferredProtocol"},
    )
    class GlobalAcceleratorForDirectoryProperty:
        def __init__(
            self,
            *,
            mode: builtins.str,
            preferred_protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the Global Accelerator for directory.

            :param mode: Indicates if Global Accelerator for directory is enabled or disabled.
            :param preferred_protocol: Indicates the preferred protocol for Global Accelerator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-globalacceleratorfordirectory.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                global_accelerator_for_directory_property = workspaces.CfnDirectory.GlobalAcceleratorForDirectoryProperty(
                    mode="mode",
                
                    # the properties below are optional
                    preferred_protocol="preferredProtocol"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__199ae25c0d1364aa0c94b7ad03fd0a32f19a6cc84de14a43cfb585d4720859a0)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument preferred_protocol", value=preferred_protocol, expected_type=type_hints["preferred_protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mode": mode,
            }
            if preferred_protocol is not None:
                self._values["preferred_protocol"] = preferred_protocol

        @builtins.property
        def mode(self) -> builtins.str:
            '''Indicates if Global Accelerator for directory is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-globalacceleratorfordirectory.html#cfn-workspaces-directory-globalacceleratorfordirectory-mode
            '''
            result = self._values.get("mode")
            assert result is not None, "Required property 'mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def preferred_protocol(self) -> typing.Optional[builtins.str]:
            '''Indicates the preferred protocol for Global Accelerator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-globalacceleratorfordirectory.html#cfn-workspaces-directory-globalacceleratorfordirectory-preferredprotocol
            '''
            result = self._values.get("preferred_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalAcceleratorForDirectoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.IDCConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_arn": "applicationArn",
            "instance_arn": "instanceArn",
        },
    )
    class IDCConfigProperty:
        def __init__(
            self,
            *,
            application_arn: typing.Optional[builtins.str] = None,
            instance_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configurations of the identity center.

            :param application_arn: The Amazon Resource Name (ARN) of the application.
            :param instance_arn: The Amazon Resource Name (ARN) of the identity center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-idcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                i_dc_config_property = {
                    "application_arn": "applicationArn",
                    "instance_arn": "instanceArn"
                }
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__92a78b77bd8100ad2ae337b65f5313eafa1832bc96163e7746e0f48d219ecb2d)
                check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
                check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_arn is not None:
                self._values["application_arn"] = application_arn
            if instance_arn is not None:
                self._values["instance_arn"] = instance_arn

        @builtins.property
        def application_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-idcconfig.html#cfn-workspaces-directory-idcconfig-applicationarn
            '''
            result = self._values.get("application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the identity center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-idcconfig.html#cfn-workspaces-directory-idcconfig-instancearn
            '''
            result = self._values.get("instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IDCConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.MicrosoftEntraConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_config_secret_arn": "applicationConfigSecretArn",
            "tenant_id": "tenantId",
        },
    )
    class MicrosoftEntraConfigProperty:
        def __init__(
            self,
            *,
            application_config_secret_arn: typing.Optional[builtins.str] = None,
            tenant_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configurations of the Microsoft Entra.

            :param application_config_secret_arn: The Amazon Resource Name (ARN) of the application config.
            :param tenant_id: The identifier of the tenant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-microsoftentraconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                microsoft_entra_config_property = workspaces.CfnDirectory.MicrosoftEntraConfigProperty(
                    application_config_secret_arn="applicationConfigSecretArn",
                    tenant_id="tenantId"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__d9940a6ad225287b5d67e7486f545651568899a168da4936344e76bb6ba8f3aa)
                check_type(argname="argument application_config_secret_arn", value=application_config_secret_arn, expected_type=type_hints["application_config_secret_arn"])
                check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_config_secret_arn is not None:
                self._values["application_config_secret_arn"] = application_config_secret_arn
            if tenant_id is not None:
                self._values["tenant_id"] = tenant_id

        @builtins.property
        def application_config_secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the application config.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-microsoftentraconfig.html#cfn-workspaces-directory-microsoftentraconfig-applicationconfigsecretarn
            '''
            result = self._values.get("application_config_secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tenant_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the tenant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-microsoftentraconfig.html#cfn-workspaces-directory-microsoftentraconfig-tenantid
            '''
            result = self._values.get("tenant_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MicrosoftEntraConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.SamlPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relay_state_parameter_name": "relayStateParameterName",
            "status": "status",
            "user_access_url": "userAccessUrl",
        },
    )
    class SamlPropertiesProperty:
        def __init__(
            self,
            *,
            relay_state_parameter_name: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            user_access_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the enablement status, user access URL, and relay state parameter name that are used for configuring federation with an SAML 2.0 identity provider.

            :param relay_state_parameter_name: The relay state parameter name supported by the SAML 2.0 identity provider (IdP).
            :param status: Indicates the status of SAML 2.0 authentication.
            :param user_access_url: The SAML 2.0 identity provider (IdP) user access URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-samlproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                saml_properties_property = workspaces.CfnDirectory.SamlPropertiesProperty(
                    relay_state_parameter_name="relayStateParameterName",
                    status="status",
                    user_access_url="userAccessUrl"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c2504bb91b90dedcd987a0e28039477a816c525ee82f3f6e6485d89be3f46e3e)
                check_type(argname="argument relay_state_parameter_name", value=relay_state_parameter_name, expected_type=type_hints["relay_state_parameter_name"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument user_access_url", value=user_access_url, expected_type=type_hints["user_access_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if relay_state_parameter_name is not None:
                self._values["relay_state_parameter_name"] = relay_state_parameter_name
            if status is not None:
                self._values["status"] = status
            if user_access_url is not None:
                self._values["user_access_url"] = user_access_url

        @builtins.property
        def relay_state_parameter_name(self) -> typing.Optional[builtins.str]:
            '''The relay state parameter name supported by the SAML 2.0 identity provider (IdP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-samlproperties.html#cfn-workspaces-directory-samlproperties-relaystateparametername
            '''
            result = self._values.get("relay_state_parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates the status of SAML 2.0 authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-samlproperties.html#cfn-workspaces-directory-samlproperties-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_access_url(self) -> typing.Optional[builtins.str]:
            '''The SAML 2.0 identity provider (IdP) user access URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-samlproperties.html#cfn-workspaces-directory-samlproperties-useraccessurl
            '''
            result = self._values.get("user_access_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamlPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.SelfservicePermissionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "change_compute_type": "changeComputeType",
            "increase_volume_size": "increaseVolumeSize",
            "rebuild_workspace": "rebuildWorkspace",
            "restart_workspace": "restartWorkspace",
            "switch_running_mode": "switchRunningMode",
        },
    )
    class SelfservicePermissionsProperty:
        def __init__(
            self,
            *,
            change_compute_type: typing.Optional[builtins.str] = None,
            increase_volume_size: typing.Optional[builtins.str] = None,
            rebuild_workspace: typing.Optional[builtins.str] = None,
            restart_workspace: typing.Optional[builtins.str] = None,
            switch_running_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the self-service permissions for a directory.

            :param change_compute_type: Specifies whether users can change the compute type (bundle) for their WorkSpace.
            :param increase_volume_size: Specifies whether users can increase the volume size of the drives on their WorkSpace.
            :param rebuild_workspace: Specifies whether users can rebuild the operating system of a WorkSpace to its original state.
            :param restart_workspace: Specifies whether users can restart their WorkSpace.
            :param switch_running_mode: Specifies whether users can switch the running mode of their WorkSpace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-selfservicepermissions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                selfservice_permissions_property = workspaces.CfnDirectory.SelfservicePermissionsProperty(
                    change_compute_type="changeComputeType",
                    increase_volume_size="increaseVolumeSize",
                    rebuild_workspace="rebuildWorkspace",
                    restart_workspace="restartWorkspace",
                    switch_running_mode="switchRunningMode"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__a1115704039492fa3d660af1d1f5a4e708fca100ec9218943f42baf272258d6c)
                check_type(argname="argument change_compute_type", value=change_compute_type, expected_type=type_hints["change_compute_type"])
                check_type(argname="argument increase_volume_size", value=increase_volume_size, expected_type=type_hints["increase_volume_size"])
                check_type(argname="argument rebuild_workspace", value=rebuild_workspace, expected_type=type_hints["rebuild_workspace"])
                check_type(argname="argument restart_workspace", value=restart_workspace, expected_type=type_hints["restart_workspace"])
                check_type(argname="argument switch_running_mode", value=switch_running_mode, expected_type=type_hints["switch_running_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if change_compute_type is not None:
                self._values["change_compute_type"] = change_compute_type
            if increase_volume_size is not None:
                self._values["increase_volume_size"] = increase_volume_size
            if rebuild_workspace is not None:
                self._values["rebuild_workspace"] = rebuild_workspace
            if restart_workspace is not None:
                self._values["restart_workspace"] = restart_workspace
            if switch_running_mode is not None:
                self._values["switch_running_mode"] = switch_running_mode

        @builtins.property
        def change_compute_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether users can change the compute type (bundle) for their WorkSpace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-selfservicepermissions.html#cfn-workspaces-directory-selfservicepermissions-changecomputetype
            '''
            result = self._values.get("change_compute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def increase_volume_size(self) -> typing.Optional[builtins.str]:
            '''Specifies whether users can increase the volume size of the drives on their WorkSpace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-selfservicepermissions.html#cfn-workspaces-directory-selfservicepermissions-increasevolumesize
            '''
            result = self._values.get("increase_volume_size")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rebuild_workspace(self) -> typing.Optional[builtins.str]:
            '''Specifies whether users can rebuild the operating system of a WorkSpace to its original state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-selfservicepermissions.html#cfn-workspaces-directory-selfservicepermissions-rebuildworkspace
            '''
            result = self._values.get("rebuild_workspace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def restart_workspace(self) -> typing.Optional[builtins.str]:
            '''Specifies whether users can restart their WorkSpace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-selfservicepermissions.html#cfn-workspaces-directory-selfservicepermissions-restartworkspace
            '''
            result = self._values.get("restart_workspace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def switch_running_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether users can switch the running mode of their WorkSpace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-selfservicepermissions.html#cfn-workspaces-directory-selfservicepermissions-switchrunningmode
            '''
            result = self._values.get("switch_running_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfservicePermissionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.StorageConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={"connector_type": "connectorType", "status": "status"},
    )
    class StorageConnectorProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            status: builtins.str,
        ) -> None:
            '''Describes the storage connector.

            :param connector_type: The type of connector used to save user files.
            :param status: Indicates if the storage connector is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-storageconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                storage_connector_property = workspaces.CfnDirectory.StorageConnectorProperty(
                    connector_type="connectorType",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__27aefaf54a243cf84a711ce534a88e0a0216741f4075781e1ad2694063c21b2a)
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connector_type": connector_type,
                "status": status,
            }

        @builtins.property
        def connector_type(self) -> builtins.str:
            '''The type of connector used to save user files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-storageconnector.html#cfn-workspaces-directory-storageconnector-connectortype
            '''
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def status(self) -> builtins.str:
            '''Indicates if the storage connector is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-storageconnector.html#cfn-workspaces-directory-storageconnector-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.StreamingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "global_accelerator": "globalAccelerator",
            "storage_connectors": "storageConnectors",
            "streaming_experience_preferred_protocol": "streamingExperiencePreferredProtocol",
            "user_settings": "userSettings",
        },
    )
    class StreamingPropertiesProperty:
        def __init__(
            self,
            *,
            global_accelerator: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.GlobalAcceleratorForDirectoryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_connectors: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.StorageConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            streaming_experience_preferred_protocol: typing.Optional[builtins.str] = None,
            user_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.UserSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the streaming properties.

            :param global_accelerator: Describes the Global Accelerator for directory.
            :param storage_connectors: Indicates the storage connector used.
            :param streaming_experience_preferred_protocol: Indicates the type of preferred protocol for the streaming experience.
            :param user_settings: Indicates the permission settings associated with the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-streamingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                streaming_properties_property = workspaces.CfnDirectory.StreamingPropertiesProperty(
                    global_accelerator=workspaces.CfnDirectory.GlobalAcceleratorForDirectoryProperty(
                        mode="mode",
                
                        # the properties below are optional
                        preferred_protocol="preferredProtocol"
                    ),
                    storage_connectors=[workspaces.CfnDirectory.StorageConnectorProperty(
                        connector_type="connectorType",
                        status="status"
                    )],
                    streaming_experience_preferred_protocol="streamingExperiencePreferredProtocol",
                    user_settings=[workspaces.CfnDirectory.UserSettingProperty(
                        action="action",
                        permission="permission",
                
                        # the properties below are optional
                        maximum_length=123
                    )]
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__f2c1eddaaf1b110af530faff46ca41d24fb665c60dc4e97bf9dd1ff14b443e3d)
                check_type(argname="argument global_accelerator", value=global_accelerator, expected_type=type_hints["global_accelerator"])
                check_type(argname="argument storage_connectors", value=storage_connectors, expected_type=type_hints["storage_connectors"])
                check_type(argname="argument streaming_experience_preferred_protocol", value=streaming_experience_preferred_protocol, expected_type=type_hints["streaming_experience_preferred_protocol"])
                check_type(argname="argument user_settings", value=user_settings, expected_type=type_hints["user_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if global_accelerator is not None:
                self._values["global_accelerator"] = global_accelerator
            if storage_connectors is not None:
                self._values["storage_connectors"] = storage_connectors
            if streaming_experience_preferred_protocol is not None:
                self._values["streaming_experience_preferred_protocol"] = streaming_experience_preferred_protocol
            if user_settings is not None:
                self._values["user_settings"] = user_settings

        @builtins.property
        def global_accelerator(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.GlobalAcceleratorForDirectoryProperty"]]:
            '''Describes the Global Accelerator for directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-streamingproperties.html#cfn-workspaces-directory-streamingproperties-globalaccelerator
            '''
            result = self._values.get("global_accelerator")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.GlobalAcceleratorForDirectoryProperty"]], result)

        @builtins.property
        def storage_connectors(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StorageConnectorProperty"]]]]:
            '''Indicates the storage connector used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-streamingproperties.html#cfn-workspaces-directory-streamingproperties-storageconnectors
            '''
            result = self._values.get("storage_connectors")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StorageConnectorProperty"]]]], result)

        @builtins.property
        def streaming_experience_preferred_protocol(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Indicates the type of preferred protocol for the streaming experience.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-streamingproperties.html#cfn-workspaces-directory-streamingproperties-streamingexperiencepreferredprotocol
            '''
            result = self._values.get("streaming_experience_preferred_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_settings(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.UserSettingProperty"]]]]:
            '''Indicates the permission settings associated with the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-streamingproperties.html#cfn-workspaces-directory-streamingproperties-usersettings
            '''
            result = self._values.get("user_settings")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.UserSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.UserSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "permission": "permission",
            "maximum_length": "maximumLength",
        },
    )
    class UserSettingProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            permission: builtins.str,
            maximum_length: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the user's permission settings.

            :param action: Indicates the type of action.
            :param permission: Indicates if the setting is enabled or disabled.
            :param maximum_length: Indicates the maximum character length for the specified user setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-usersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                user_setting_property = workspaces.CfnDirectory.UserSettingProperty(
                    action="action",
                    permission="permission",
                
                    # the properties below are optional
                    maximum_length=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__68b5fa4de3d1090575ac74178ddc5102bf004f716f9a3cb09a3ee34a79a84e1f)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
                check_type(argname="argument maximum_length", value=maximum_length, expected_type=type_hints["maximum_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "permission": permission,
            }
            if maximum_length is not None:
                self._values["maximum_length"] = maximum_length

        @builtins.property
        def action(self) -> builtins.str:
            '''Indicates the type of action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-usersetting.html#cfn-workspaces-directory-usersetting-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def permission(self) -> builtins.str:
            '''Indicates if the setting is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-usersetting.html#cfn-workspaces-directory-usersetting-permission
            '''
            result = self._values.get("permission")
            assert result is not None, "Required property 'permission' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def maximum_length(self) -> typing.Optional[jsii.Number]:
            '''Indicates the maximum character length for the specified user setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-usersetting.html#cfn-workspaces-directory-usersetting-maximumlength
            '''
            result = self._values.get("maximum_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectory.WorkspaceAccessPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_endpoint_config": "accessEndpointConfig",
            "device_type_android": "deviceTypeAndroid",
            "device_type_chrome_os": "deviceTypeChromeOs",
            "device_type_ios": "deviceTypeIos",
            "device_type_linux": "deviceTypeLinux",
            "device_type_osx": "deviceTypeOsx",
            "device_type_web": "deviceTypeWeb",
            "device_type_windows": "deviceTypeWindows",
            "device_type_work_spaces_thin_client": "deviceTypeWorkSpacesThinClient",
            "device_type_zero_client": "deviceTypeZeroClient",
        },
    )
    class WorkspaceAccessPropertiesProperty:
        def __init__(
            self,
            *,
            access_endpoint_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.AccessEndpointConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            device_type_android: typing.Optional[builtins.str] = None,
            device_type_chrome_os: typing.Optional[builtins.str] = None,
            device_type_ios: typing.Optional[builtins.str] = None,
            device_type_linux: typing.Optional[builtins.str] = None,
            device_type_osx: typing.Optional[builtins.str] = None,
            device_type_web: typing.Optional[builtins.str] = None,
            device_type_windows: typing.Optional[builtins.str] = None,
            device_type_work_spaces_thin_client: typing.Optional[builtins.str] = None,
            device_type_zero_client: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The device types and operating systems that can be used to access a WorkSpace.

            :param access_endpoint_config: Describes the access endpoint configuration for a WorkSpace.
            :param device_type_android: Indicates whether users can use Android and Android-compatible Chrome OS devices to access their WorkSpaces.
            :param device_type_chrome_os: Indicates whether users can use Chromebooks to access their WorkSpaces.
            :param device_type_ios: Indicates whether users can use iOS devices to access their WorkSpaces.
            :param device_type_linux: Indicates whether users can use Linux clients to access their WorkSpaces.
            :param device_type_osx: Indicates whether users can use macOS clients to access their WorkSpaces.
            :param device_type_web: Indicates whether users can access their WorkSpaces through a web browser.
            :param device_type_windows: Indicates whether users can use Windows clients to access their WorkSpaces.
            :param device_type_work_spaces_thin_client: Indicates whether users can access their WorkSpaces through a WorkSpaces Thin Client.
            :param device_type_zero_client: Indicates whether users can use zero client devices to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                workspace_access_properties_property = workspaces.CfnDirectory.WorkspaceAccessPropertiesProperty(
                    access_endpoint_config=workspaces.CfnDirectory.AccessEndpointConfigProperty(
                        access_endpoints=[workspaces.CfnDirectory.AccessEndpointProperty(
                            access_endpoint_type="accessEndpointType",
                            vpc_endpoint_id="vpcEndpointId"
                        )],
                
                        # the properties below are optional
                        internet_fallback_protocols=["internetFallbackProtocols"]
                    ),
                    device_type_android="deviceTypeAndroid",
                    device_type_chrome_os="deviceTypeChromeOs",
                    device_type_ios="deviceTypeIos",
                    device_type_linux="deviceTypeLinux",
                    device_type_osx="deviceTypeOsx",
                    device_type_web="deviceTypeWeb",
                    device_type_windows="deviceTypeWindows",
                    device_type_work_spaces_thin_client="deviceTypeWorkSpacesThinClient",
                    device_type_zero_client="deviceTypeZeroClient"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__73d70f5a7d065768e4f5eddf82eafb687010b12c5844026538a57ca21f74af95)
                check_type(argname="argument access_endpoint_config", value=access_endpoint_config, expected_type=type_hints["access_endpoint_config"])
                check_type(argname="argument device_type_android", value=device_type_android, expected_type=type_hints["device_type_android"])
                check_type(argname="argument device_type_chrome_os", value=device_type_chrome_os, expected_type=type_hints["device_type_chrome_os"])
                check_type(argname="argument device_type_ios", value=device_type_ios, expected_type=type_hints["device_type_ios"])
                check_type(argname="argument device_type_linux", value=device_type_linux, expected_type=type_hints["device_type_linux"])
                check_type(argname="argument device_type_osx", value=device_type_osx, expected_type=type_hints["device_type_osx"])
                check_type(argname="argument device_type_web", value=device_type_web, expected_type=type_hints["device_type_web"])
                check_type(argname="argument device_type_windows", value=device_type_windows, expected_type=type_hints["device_type_windows"])
                check_type(argname="argument device_type_work_spaces_thin_client", value=device_type_work_spaces_thin_client, expected_type=type_hints["device_type_work_spaces_thin_client"])
                check_type(argname="argument device_type_zero_client", value=device_type_zero_client, expected_type=type_hints["device_type_zero_client"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_endpoint_config is not None:
                self._values["access_endpoint_config"] = access_endpoint_config
            if device_type_android is not None:
                self._values["device_type_android"] = device_type_android
            if device_type_chrome_os is not None:
                self._values["device_type_chrome_os"] = device_type_chrome_os
            if device_type_ios is not None:
                self._values["device_type_ios"] = device_type_ios
            if device_type_linux is not None:
                self._values["device_type_linux"] = device_type_linux
            if device_type_osx is not None:
                self._values["device_type_osx"] = device_type_osx
            if device_type_web is not None:
                self._values["device_type_web"] = device_type_web
            if device_type_windows is not None:
                self._values["device_type_windows"] = device_type_windows
            if device_type_work_spaces_thin_client is not None:
                self._values["device_type_work_spaces_thin_client"] = device_type_work_spaces_thin_client
            if device_type_zero_client is not None:
                self._values["device_type_zero_client"] = device_type_zero_client

        @builtins.property
        def access_endpoint_config(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.AccessEndpointConfigProperty"]]:
            '''Describes the access endpoint configuration for a WorkSpace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-accessendpointconfig
            '''
            result = self._values.get("access_endpoint_config")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.AccessEndpointConfigProperty"]], result)

        @builtins.property
        def device_type_android(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use Android and Android-compatible Chrome OS devices to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypeandroid
            '''
            result = self._values.get("device_type_android")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_chrome_os(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use Chromebooks to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypechromeos
            '''
            result = self._values.get("device_type_chrome_os")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_ios(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use iOS devices to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypeios
            '''
            result = self._values.get("device_type_ios")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_linux(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use Linux clients to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypelinux
            '''
            result = self._values.get("device_type_linux")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_osx(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use macOS clients to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypeosx
            '''
            result = self._values.get("device_type_osx")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_web(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can access their WorkSpaces through a web browser.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypeweb
            '''
            result = self._values.get("device_type_web")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_windows(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use Windows clients to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypewindows
            '''
            result = self._values.get("device_type_windows")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_work_spaces_thin_client(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can access their WorkSpaces through a WorkSpaces Thin Client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypeworkspacesthinclient
            '''
            result = self._values.get("device_type_work_spaces_thin_client")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_type_zero_client(self) -> typing.Optional[builtins.str]:
            '''Indicates whether users can use zero client devices to access their WorkSpaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-directory-workspaceaccessproperties.html#cfn-workspaces-directory-workspaceaccessproperties-devicetypezeroclient
            '''
            result = self._values.get("device_type_zero_client")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkspaceAccessPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_workspaces.CfnDirectoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "active_directory_config": "activeDirectoryConfig",
        "certificate_based_auth_properties": "certificateBasedAuthProperties",
        "enable_self_service": "enableSelfService",
        "endpoint_encryption_mode": "endpointEncryptionMode",
        "idc_instance_arn": "idcInstanceArn",
        "ip_group_ids": "ipGroupIds",
        "microsoft_entra_config": "microsoftEntraConfig",
        "saml_properties": "samlProperties",
        "selfservice_permissions": "selfservicePermissions",
        "streaming_properties": "streamingProperties",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "tenancy": "tenancy",
        "user_identity_type": "userIdentityType",
        "workspace_access_properties": "workspaceAccessProperties",
        "workspace_creation_properties": "workspaceCreationProperties",
        "workspace_directory_description": "workspaceDirectoryDescription",
        "workspace_directory_name": "workspaceDirectoryName",
        "workspace_type": "workspaceType",
    },
)
class CfnDirectoryProps:
    def __init__(
        self,
        *,
        active_directory_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.ActiveDirectoryConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate_based_auth_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.CertificateBasedAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_self_service: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        endpoint_encryption_mode: typing.Optional[builtins.str] = None,
        idc_instance_arn: typing.Optional[builtins.str] = None,
        ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        microsoft_entra_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.MicrosoftEntraConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        saml_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.SamlPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        selfservice_permissions: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.SelfservicePermissionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        streaming_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.StreamingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        tenancy: typing.Optional[builtins.str] = None,
        user_identity_type: typing.Optional[builtins.str] = None,
        workspace_access_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.WorkspaceAccessPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace_creation_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnDirectory.DefaultWorkspaceCreationPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        workspace_directory_description: typing.Optional[builtins.str] = None,
        workspace_directory_name: typing.Optional[builtins.str] = None,
        workspace_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDirectory``.

        :param active_directory_config: Information about the Active Directory config.
        :param certificate_based_auth_properties: Describes the properties of the certificate-based authentication you want to use with your WorkSpaces.
        :param enable_self_service: Indicates whether self-service capabilities are enabled or disabled.
        :param endpoint_encryption_mode: Endpoint encryption mode that allows you to configure the specified directory between Standard TLS and FIPS 140-2 validated mode.
        :param idc_instance_arn: The Amazon Resource Name (ARN) of the identity center instance.
        :param ip_group_ids: The identifiers of the IP access control groups associated with the directory.
        :param microsoft_entra_config: Specifies the configurations of the Microsoft Entra.
        :param saml_properties: Describes the enablement status, user access URL, and relay state parameter name that are used for configuring federation with an SAML 2.0 identity provider.
        :param selfservice_permissions: Describes the self-service permissions for a directory.
        :param streaming_properties: Describes the streaming properties.
        :param subnet_ids: The identifiers of the subnets for your virtual private cloud (VPC).
        :param tags: The tags associated with the directory.
        :param tenancy: Indicates whether your WorkSpace directory is dedicated or shared.
        :param user_identity_type: The type of identity management the user is using.
        :param workspace_access_properties: The device types and operating systems that can be used to access a WorkSpace.
        :param workspace_creation_properties: The default values that are used to create WorkSpaces.
        :param workspace_directory_description: Description of the directory to register.
        :param workspace_directory_name: The name of the directory to register.
        :param workspace_type: Indicates whether the directory's WorkSpace type is personal or pools.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_workspaces as workspaces
            
            cfn_directory_props = workspaces.CfnDirectoryProps(
                active_directory_config=workspaces.CfnDirectory.ActiveDirectoryConfigProperty(
                    domain_name="domainName",
                    service_account_secret_arn="serviceAccountSecretArn"
                ),
                certificate_based_auth_properties=workspaces.CfnDirectory.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                ),
                enable_self_service=False,
                endpoint_encryption_mode="endpointEncryptionMode",
                idc_instance_arn="idcInstanceArn",
                ip_group_ids=["ipGroupIds"],
                microsoft_entra_config=workspaces.CfnDirectory.MicrosoftEntraConfigProperty(
                    application_config_secret_arn="applicationConfigSecretArn",
                    tenant_id="tenantId"
                ),
                saml_properties=workspaces.CfnDirectory.SamlPropertiesProperty(
                    relay_state_parameter_name="relayStateParameterName",
                    status="status",
                    user_access_url="userAccessUrl"
                ),
                selfservice_permissions=workspaces.CfnDirectory.SelfservicePermissionsProperty(
                    change_compute_type="changeComputeType",
                    increase_volume_size="increaseVolumeSize",
                    rebuild_workspace="rebuildWorkspace",
                    restart_workspace="restartWorkspace",
                    switch_running_mode="switchRunningMode"
                ),
                streaming_properties=workspaces.CfnDirectory.StreamingPropertiesProperty(
                    global_accelerator=workspaces.CfnDirectory.GlobalAcceleratorForDirectoryProperty(
                        mode="mode",
            
                        # the properties below are optional
                        preferred_protocol="preferredProtocol"
                    ),
                    storage_connectors=[workspaces.CfnDirectory.StorageConnectorProperty(
                        connector_type="connectorType",
                        status="status"
                    )],
                    streaming_experience_preferred_protocol="streamingExperiencePreferredProtocol",
                    user_settings=[workspaces.CfnDirectory.UserSettingProperty(
                        action="action",
                        permission="permission",
            
                        # the properties below are optional
                        maximum_length=123
                    )]
                ),
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tenancy="tenancy",
                user_identity_type="userIdentityType",
                workspace_access_properties=workspaces.CfnDirectory.WorkspaceAccessPropertiesProperty(
                    access_endpoint_config=workspaces.CfnDirectory.AccessEndpointConfigProperty(
                        access_endpoints=[workspaces.CfnDirectory.AccessEndpointProperty(
                            access_endpoint_type="accessEndpointType",
                            vpc_endpoint_id="vpcEndpointId"
                        )],
            
                        # the properties below are optional
                        internet_fallback_protocols=["internetFallbackProtocols"]
                    ),
                    device_type_android="deviceTypeAndroid",
                    device_type_chrome_os="deviceTypeChromeOs",
                    device_type_ios="deviceTypeIos",
                    device_type_linux="deviceTypeLinux",
                    device_type_osx="deviceTypeOsx",
                    device_type_web="deviceTypeWeb",
                    device_type_windows="deviceTypeWindows",
                    device_type_work_spaces_thin_client="deviceTypeWorkSpacesThinClient",
                    device_type_zero_client="deviceTypeZeroClient"
                ),
                workspace_creation_properties=workspaces.CfnDirectory.DefaultWorkspaceCreationPropertiesProperty(
                    custom_security_group_id="customSecurityGroupId",
                    default_ou="defaultOu",
                    enable_internet_access=False,
                    enable_maintenance_mode=False,
                    instance_iam_role_arn="instanceIamRoleArn",
                    user_enabled_as_local_administrator=False
                ),
                workspace_directory_description="workspaceDirectoryDescription",
                workspace_directory_name="workspaceDirectoryName",
                workspace_type="workspaceType"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1b02a6e4a9c5198c9a5097f9f8bf2dda738ab763e2710273958ea729227a0502)
            check_type(argname="argument active_directory_config", value=active_directory_config, expected_type=type_hints["active_directory_config"])
            check_type(argname="argument certificate_based_auth_properties", value=certificate_based_auth_properties, expected_type=type_hints["certificate_based_auth_properties"])
            check_type(argname="argument enable_self_service", value=enable_self_service, expected_type=type_hints["enable_self_service"])
            check_type(argname="argument endpoint_encryption_mode", value=endpoint_encryption_mode, expected_type=type_hints["endpoint_encryption_mode"])
            check_type(argname="argument idc_instance_arn", value=idc_instance_arn, expected_type=type_hints["idc_instance_arn"])
            check_type(argname="argument ip_group_ids", value=ip_group_ids, expected_type=type_hints["ip_group_ids"])
            check_type(argname="argument microsoft_entra_config", value=microsoft_entra_config, expected_type=type_hints["microsoft_entra_config"])
            check_type(argname="argument saml_properties", value=saml_properties, expected_type=type_hints["saml_properties"])
            check_type(argname="argument selfservice_permissions", value=selfservice_permissions, expected_type=type_hints["selfservice_permissions"])
            check_type(argname="argument streaming_properties", value=streaming_properties, expected_type=type_hints["streaming_properties"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
            check_type(argname="argument user_identity_type", value=user_identity_type, expected_type=type_hints["user_identity_type"])
            check_type(argname="argument workspace_access_properties", value=workspace_access_properties, expected_type=type_hints["workspace_access_properties"])
            check_type(argname="argument workspace_creation_properties", value=workspace_creation_properties, expected_type=type_hints["workspace_creation_properties"])
            check_type(argname="argument workspace_directory_description", value=workspace_directory_description, expected_type=type_hints["workspace_directory_description"])
            check_type(argname="argument workspace_directory_name", value=workspace_directory_name, expected_type=type_hints["workspace_directory_name"])
            check_type(argname="argument workspace_type", value=workspace_type, expected_type=type_hints["workspace_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_directory_config is not None:
            self._values["active_directory_config"] = active_directory_config
        if certificate_based_auth_properties is not None:
            self._values["certificate_based_auth_properties"] = certificate_based_auth_properties
        if enable_self_service is not None:
            self._values["enable_self_service"] = enable_self_service
        if endpoint_encryption_mode is not None:
            self._values["endpoint_encryption_mode"] = endpoint_encryption_mode
        if idc_instance_arn is not None:
            self._values["idc_instance_arn"] = idc_instance_arn
        if ip_group_ids is not None:
            self._values["ip_group_ids"] = ip_group_ids
        if microsoft_entra_config is not None:
            self._values["microsoft_entra_config"] = microsoft_entra_config
        if saml_properties is not None:
            self._values["saml_properties"] = saml_properties
        if selfservice_permissions is not None:
            self._values["selfservice_permissions"] = selfservice_permissions
        if streaming_properties is not None:
            self._values["streaming_properties"] = streaming_properties
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if tenancy is not None:
            self._values["tenancy"] = tenancy
        if user_identity_type is not None:
            self._values["user_identity_type"] = user_identity_type
        if workspace_access_properties is not None:
            self._values["workspace_access_properties"] = workspace_access_properties
        if workspace_creation_properties is not None:
            self._values["workspace_creation_properties"] = workspace_creation_properties
        if workspace_directory_description is not None:
            self._values["workspace_directory_description"] = workspace_directory_description
        if workspace_directory_name is not None:
            self._values["workspace_directory_name"] = workspace_directory_name
        if workspace_type is not None:
            self._values["workspace_type"] = workspace_type

    @builtins.property
    def active_directory_config(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.ActiveDirectoryConfigProperty"]]:
        '''Information about the Active Directory config.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-activedirectoryconfig
        '''
        result = self._values.get("active_directory_config")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.ActiveDirectoryConfigProperty"]], result)

    @builtins.property
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.CertificateBasedAuthPropertiesProperty"]]:
        '''Describes the properties of the certificate-based authentication you want to use with your WorkSpaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-certificatebasedauthproperties
        '''
        result = self._values.get("certificate_based_auth_properties")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.CertificateBasedAuthPropertiesProperty"]], result)

    @builtins.property
    def enable_self_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Indicates whether self-service capabilities are enabled or disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-enableselfservice
        '''
        result = self._values.get("enable_self_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def endpoint_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Endpoint encryption mode that allows you to configure the specified directory between Standard TLS and FIPS 140-2 validated mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-endpointencryptionmode
        '''
        result = self._values.get("endpoint_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idc_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the identity center instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-idcinstancearn
        '''
        result = self._values.get("idc_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identifiers of the IP access control groups associated with the directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-ipgroupids
        '''
        result = self._values.get("ip_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def microsoft_entra_config(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.MicrosoftEntraConfigProperty"]]:
        '''Specifies the configurations of the Microsoft Entra.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-microsoftentraconfig
        '''
        result = self._values.get("microsoft_entra_config")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.MicrosoftEntraConfigProperty"]], result)

    @builtins.property
    def saml_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SamlPropertiesProperty"]]:
        '''Describes the enablement status, user access URL, and relay state parameter name that are used for configuring federation with an SAML 2.0 identity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-samlproperties
        '''
        result = self._values.get("saml_properties")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SamlPropertiesProperty"]], result)

    @builtins.property
    def selfservice_permissions(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SelfservicePermissionsProperty"]]:
        '''Describes the self-service permissions for a directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-selfservicepermissions
        '''
        result = self._values.get("selfservice_permissions")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.SelfservicePermissionsProperty"]], result)

    @builtins.property
    def streaming_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StreamingPropertiesProperty"]]:
        '''Describes the streaming properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-streamingproperties
        '''
        result = self._values.get("streaming_properties")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.StreamingPropertiesProperty"]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identifiers of the subnets for your virtual private cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags associated with the directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''Indicates whether your WorkSpace directory is dedicated or shared.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-tenancy
        '''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_identity_type(self) -> typing.Optional[builtins.str]:
        '''The type of identity management the user is using.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-useridentitytype
        '''
        result = self._values.get("user_identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_access_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.WorkspaceAccessPropertiesProperty"]]:
        '''The device types and operating systems that can be used to access a WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-workspaceaccessproperties
        '''
        result = self._values.get("workspace_access_properties")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.WorkspaceAccessPropertiesProperty"]], result)

    @builtins.property
    def workspace_creation_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.DefaultWorkspaceCreationPropertiesProperty"]]:
        '''The default values that are used to create WorkSpaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-workspacecreationproperties
        '''
        result = self._values.get("workspace_creation_properties")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnDirectory.DefaultWorkspaceCreationPropertiesProperty"]], result)

    @builtins.property
    def workspace_directory_description(self) -> typing.Optional[builtins.str]:
        '''Description of the directory to register.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-workspacedirectorydescription
        '''
        result = self._values.get("workspace_directory_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_directory_name(self) -> typing.Optional[builtins.str]:
        '''The name of the directory to register.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-workspacedirectoryname
        '''
        result = self._values.get("workspace_directory_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the directory's WorkSpace type is personal or pools.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-directory.html#cfn-workspaces-directory-workspacetype
        '''
        result = self._values.get("workspace_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_workspaces_4620141e.IWorkspaceRef, _aws_cdk_0cae9daa.ITaggable)
class CfnWorkspace(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspace",
):
    '''The ``AWS::WorkSpaces::Workspace`` resource specifies a WorkSpace.

    Updates are not supported for the ``BundleId`` , ``RootVolumeEncryptionEnabled`` , ``UserVolumeEncryptionEnabled`` , or ``VolumeEncryptionKey`` properties. To update these properties, you must also update a property that triggers a replacement, such as the ``UserName`` property.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html
    :cloudformationResource: AWS::WorkSpaces::Workspace
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_workspaces as workspaces
        
        cfn_workspace = workspaces.CfnWorkspace(self, "MyCfnWorkspace",
            bundle_id="bundleId",
            directory_id="directoryId",
            user_name="userName",
        
            # the properties below are optional
            root_volume_encryption_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_volume_encryption_enabled=False,
            volume_encryption_key="volumeEncryptionKey",
            workspace_properties=workspaces.CfnWorkspace.WorkspacePropertiesProperty(
                compute_type_name="computeTypeName",
                root_volume_size_gib=123,
                running_mode="runningMode",
                running_mode_auto_stop_timeout_in_minutes=123,
                user_volume_size_gib=123
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        bundle_id: builtins.str,
        directory_id: builtins.str,
        user_name: builtins.str,
        root_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        volume_encryption_key: typing.Optional[builtins.str] = None,
        workspace_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspace.WorkspacePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WorkSpaces::Workspace``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param bundle_id: The identifier of the bundle for the WorkSpace.
        :param directory_id: The identifier of the Directory Service directory for the WorkSpace.
        :param user_name: The user name of the user for the WorkSpace. This user name must exist in the Directory Service directory for the WorkSpace.
        :param root_volume_encryption_enabled: Indicates whether the data stored on the root volume is encrypted.
        :param tags: The tags for the WorkSpace.
        :param user_volume_encryption_enabled: Indicates whether the data stored on the user volume is encrypted.
        :param volume_encryption_key: The symmetric AWS KMS key used to encrypt data stored on your WorkSpace. Amazon WorkSpaces does not support asymmetric KMS keys.
        :param workspace_properties: The WorkSpace properties.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ecf9321ac6e165dfc96d72b093b8636e1ff9e82acf9cea2e5176beb79bb65839)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceProps(
            bundle_id=bundle_id,
            directory_id=directory_id,
            user_name=user_name,
            root_volume_encryption_enabled=root_volume_encryption_enabled,
            tags=tags,
            user_volume_encryption_enabled=user_volume_encryption_enabled,
            volume_encryption_key=volume_encryption_key,
            workspace_properties=workspace_properties,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForWorkspace")
    @builtins.classmethod
    def arn_for_workspace(
        cls,
        resource: "_aws_workspaces_4620141e.IWorkspaceRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8d6d998e49570cc52ccb0ecfad0db07c3b31d793cd316fcd6de9bd3cde91f30e)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForWorkspace", [resource]))

    @jsii.member(jsii_name="fromWorkspaceId")
    @builtins.classmethod
    def from_workspace_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        workspace_id: builtins.str,
    ) -> "_aws_workspaces_4620141e.IWorkspaceRef":
        '''Creates a new IWorkspaceRef from a workspaceId.

        :param scope: -
        :param id: -
        :param workspace_id: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4d89928bc3143b40dfcbe60436eb821c87d4ca5d7e96d4ce7e5b5f26125f7d08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        return typing.cast("_aws_workspaces_4620141e.IWorkspaceRef", jsii.sinvoke(cls, "fromWorkspaceId", [scope, id, workspace_id]))

    @jsii.member(jsii_name="isCfnWorkspace")
    @builtins.classmethod
    def is_cfn_workspace(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnWorkspace.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0189c0ab3f83c44331c574b9d6fa036f364fb409d35f51f73b8fba8ae858db28)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnWorkspace", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e772192f4dd8e60f99b92beca96b37f99aca30dac13f906848601f52405c8d90)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4902c0d49db4502ddf5bb0c1b99a8dd9ce3aa66f14904ef46eb1b040033e0f6f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier of the WorkSpace, returned as a string.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrWorkspaceId")
    def attr_workspace_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: WorkspaceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWorkspaceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="workspaceRef")
    def workspace_ref(self) -> "_aws_workspaces_4620141e.WorkspaceReference":
        '''A reference to a Workspace resource.'''
        return typing.cast("_aws_workspaces_4620141e.WorkspaceReference", jsii.get(self, "workspaceRef"))

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> builtins.str:
        '''The identifier of the bundle for the WorkSpace.'''
        return typing.cast(builtins.str, jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f2f2e671a0d784d1293a9f59800a4ee9327ac8c35d2975eb4bccf99d78c24ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        '''The identifier of the Directory Service directory for the WorkSpace.'''
        return typing.cast(builtins.str, jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__098a48aaecf371ba14035ae50fde38957b608503f7c78dc0f9568806cd61b926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The user name of the user for the WorkSpace.'''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__225037370c6d4ae1d7c6fb794db70699fb16815233054c687f769b05c6298ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootVolumeEncryptionEnabled")
    def root_volume_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Indicates whether the data stored on the root volume is encrypted.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "rootVolumeEncryptionEnabled"))

    @root_volume_encryption_enabled.setter
    def root_volume_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bb29c66862be75fab751682c7102c72c4846798afbc12b529f0ece9b38719128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootVolumeEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsRaw")
    def tags_raw(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the WorkSpace.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tagsRaw"))

    @tags_raw.setter
    def tags_raw(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1f2a501e8ab3d90f102a797f62bdece7b78195c5b29e714a25825ca056f061c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsRaw", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userVolumeEncryptionEnabled")
    def user_volume_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Indicates whether the data stored on the user volume is encrypted.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "userVolumeEncryptionEnabled"))

    @user_volume_encryption_enabled.setter
    def user_volume_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8bd38103f5213efdd25dca3a2f0c8dcbf665bbcfb052ef6f4c929ce79e0719d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userVolumeEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeEncryptionKey")
    def volume_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The symmetric AWS KMS key used to encrypt data stored on your WorkSpace.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeEncryptionKey"))

    @volume_encryption_key.setter
    def volume_encryption_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0670847357c5e2a262f5f7ce5cb07d9b48f5d29700739766ad22e91419e89b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeEncryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceProperties")
    def workspace_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspace.WorkspacePropertiesProperty"]]:
        '''The WorkSpace properties.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspace.WorkspacePropertiesProperty"]], jsii.get(self, "workspaceProperties"))

    @workspace_properties.setter
    def workspace_properties(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspace.WorkspacePropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cbfa33f0e5fe13fa6e31e4fac282721ea7584fa1e07cea2b5dc3a6a41028a2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceProperties", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspace.WorkspacePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_type_name": "computeTypeName",
            "root_volume_size_gib": "rootVolumeSizeGib",
            "running_mode": "runningMode",
            "running_mode_auto_stop_timeout_in_minutes": "runningModeAutoStopTimeoutInMinutes",
            "user_volume_size_gib": "userVolumeSizeGib",
        },
    )
    class WorkspacePropertiesProperty:
        def __init__(
            self,
            *,
            compute_type_name: typing.Optional[builtins.str] = None,
            root_volume_size_gib: typing.Optional[jsii.Number] = None,
            running_mode: typing.Optional[builtins.str] = None,
            running_mode_auto_stop_timeout_in_minutes: typing.Optional[jsii.Number] = None,
            user_volume_size_gib: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about a WorkSpace.

            :param compute_type_name: The compute type. For more information, see `Amazon WorkSpaces Bundles <https://docs.aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles>`_ .
            :param root_volume_size_gib: The size of the root volume. For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .
            :param running_mode: The running mode. For more information, see `Manage the WorkSpace Running Mode <https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html>`_ .
            :param running_mode_auto_stop_timeout_in_minutes: The time after a user logs off when WorkSpaces are automatically stopped. Configured in 60-minute intervals.
            :param user_volume_size_gib: The size of the user storage. For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                workspace_properties_property = workspaces.CfnWorkspace.WorkspacePropertiesProperty(
                    compute_type_name="computeTypeName",
                    root_volume_size_gib=123,
                    running_mode="runningMode",
                    running_mode_auto_stop_timeout_in_minutes=123,
                    user_volume_size_gib=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__2ba35df0c40a72c6300f0149e43d82fc399d7f07da77a68563d45ca0546db330)
                check_type(argname="argument compute_type_name", value=compute_type_name, expected_type=type_hints["compute_type_name"])
                check_type(argname="argument root_volume_size_gib", value=root_volume_size_gib, expected_type=type_hints["root_volume_size_gib"])
                check_type(argname="argument running_mode", value=running_mode, expected_type=type_hints["running_mode"])
                check_type(argname="argument running_mode_auto_stop_timeout_in_minutes", value=running_mode_auto_stop_timeout_in_minutes, expected_type=type_hints["running_mode_auto_stop_timeout_in_minutes"])
                check_type(argname="argument user_volume_size_gib", value=user_volume_size_gib, expected_type=type_hints["user_volume_size_gib"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_type_name is not None:
                self._values["compute_type_name"] = compute_type_name
            if root_volume_size_gib is not None:
                self._values["root_volume_size_gib"] = root_volume_size_gib
            if running_mode is not None:
                self._values["running_mode"] = running_mode
            if running_mode_auto_stop_timeout_in_minutes is not None:
                self._values["running_mode_auto_stop_timeout_in_minutes"] = running_mode_auto_stop_timeout_in_minutes
            if user_volume_size_gib is not None:
                self._values["user_volume_size_gib"] = user_volume_size_gib

        @builtins.property
        def compute_type_name(self) -> typing.Optional[builtins.str]:
            '''The compute type.

            For more information, see `Amazon WorkSpaces Bundles <https://docs.aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-computetypename
            '''
            result = self._values.get("compute_type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def root_volume_size_gib(self) -> typing.Optional[jsii.Number]:
            '''The size of the root volume.

            For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-rootvolumesizegib
            '''
            result = self._values.get("root_volume_size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def running_mode(self) -> typing.Optional[builtins.str]:
            '''The running mode.

            For more information, see `Manage the WorkSpace Running Mode <https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-runningmode
            '''
            result = self._values.get("running_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def running_mode_auto_stop_timeout_in_minutes(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The time after a user logs off when WorkSpaces are automatically stopped.

            Configured in 60-minute intervals.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-runningmodeautostoptimeoutinminutes
            '''
            result = self._values.get("running_mode_auto_stop_timeout_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_volume_size_gib(self) -> typing.Optional[jsii.Number]:
            '''The size of the user storage.

            For important information about how to modify the size of the root and user volumes, see `Modify a WorkSpace <https://docs.aws.amazon.com/workspaces/latest/adminguide/modify-workspaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspace-workspaceproperties.html#cfn-workspaces-workspace-workspaceproperties-uservolumesizegib
            '''
            result = self._values.get("user_volume_size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkspacePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_workspaces_4620141e.IWorkspaceIpGroupRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnWorkspaceIpGroup(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspaceIpGroup",
):
    '''Resource Type definition for an IP access control group for Amazon WorkSpaces.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspaceipgroup.html
    :cloudformationResource: AWS::WorkSpaces::WorkspaceIpGroup
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_workspaces as workspaces
        
        cfn_workspace_ip_group = workspaces.CfnWorkspaceIpGroup(self, "MyCfnWorkspaceIpGroup",
            group_name="groupName",
        
            # the properties below are optional
            group_desc="groupDesc",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_rules=[workspaces.CfnWorkspaceIpGroup.IpRuleItemProperty(
                ip_rule="ipRule",
        
                # the properties below are optional
                rule_desc="ruleDesc"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        group_name: builtins.str,
        group_desc: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_rules: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspaceIpGroup.IpRuleItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WorkSpaces::WorkspaceIpGroup``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param group_name: The name of the group.
        :param group_desc: The description of the group.
        :param tags: The tags for the IP access control group.
        :param user_rules: The rules for the IP access control group.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a4ad7b8ae0ab90e6cccba48331cf2278b942c4e2286ff003c7c5d3d01eb23328)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceIpGroupProps(
            group_name=group_name,
            group_desc=group_desc,
            tags=tags,
            user_rules=user_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForWorkspaceIpGroup")
    @builtins.classmethod
    def arn_for_workspace_ip_group(
        cls,
        resource: "_aws_workspaces_4620141e.IWorkspaceIpGroupRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6173be321bf1f4583b718296cd816a36887510f673584b9755d887f8328a075b)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForWorkspaceIpGroup", [resource]))

    @jsii.member(jsii_name="isCfnWorkspaceIpGroup")
    @builtins.classmethod
    def is_cfn_workspace_ip_group(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnWorkspaceIpGroup.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9132cdbc4b4e441b9b431185b1b82925c868d98f9de4a66ab2372c7dee556bb9)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnWorkspaceIpGroup", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7a38c23726b5bd916d89720d7358c4e2dd6101aa955590a0d66b5ab633960c13)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bf0b5471f4e6c8a14b058cc3fccd30854f815a8bbe8e7da1a194ce1c392aecb6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IP access control group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrGroupId")
    def attr_group_id(self) -> builtins.str:
        '''The identifier of the IP access control group.

        :cloudformationAttribute: GroupId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGroupId"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIpGroupRef")
    def workspace_ip_group_ref(
        self,
    ) -> "_aws_workspaces_4620141e.WorkspaceIpGroupReference":
        '''A reference to a WorkspaceIpGroup resource.'''
        return typing.cast("_aws_workspaces_4620141e.WorkspaceIpGroupReference", jsii.get(self, "workspaceIpGroupRef"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''The name of the group.'''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__76e4d60d6ae5674582b5244ffdabad710288b71a02010f9b8622243f01194ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupDesc")
    def group_desc(self) -> typing.Optional[builtins.str]:
        '''The description of the group.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupDesc"))

    @group_desc.setter
    def group_desc(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b48e0db76d8f4fa74fb3edf59e6f0ed00c82f7f491a236618982a4f0c084951a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupDesc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the IP access control group.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e9a29bad2cf4dbccb24edf13ca2ba3777f254924581e693a9b2c1a384d3b6ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userRules")
    def user_rules(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspaceIpGroup.IpRuleItemProperty"]]]]:
        '''The rules for the IP access control group.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspaceIpGroup.IpRuleItemProperty"]]]], jsii.get(self, "userRules"))

    @user_rules.setter
    def user_rules(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspaceIpGroup.IpRuleItemProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__523c626d42fae94b47c0403319513a730cd38c8b35b9fadd760de3c0007f0c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRules", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspaceIpGroup.IpRuleItemProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_rule": "ipRule", "rule_desc": "ruleDesc"},
    )
    class IpRuleItemProperty:
        def __init__(
            self,
            *,
            ip_rule: builtins.str,
            rule_desc: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a rule for an IP access control group.

            :param ip_rule: The IP address range, in CIDR notation.
            :param rule_desc: The description of the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspaceipgroup-ipruleitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                ip_rule_item_property = workspaces.CfnWorkspaceIpGroup.IpRuleItemProperty(
                    ip_rule="ipRule",
                
                    # the properties below are optional
                    rule_desc="ruleDesc"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__f873d26323a491ea3042f52973cfd827eb9aee1985f5153152030dd4dec84b61)
                check_type(argname="argument ip_rule", value=ip_rule, expected_type=type_hints["ip_rule"])
                check_type(argname="argument rule_desc", value=rule_desc, expected_type=type_hints["rule_desc"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "ip_rule": ip_rule,
            }
            if rule_desc is not None:
                self._values["rule_desc"] = rule_desc

        @builtins.property
        def ip_rule(self) -> builtins.str:
            '''The IP address range, in CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspaceipgroup-ipruleitem.html#cfn-workspaces-workspaceipgroup-ipruleitem-iprule
            '''
            result = self._values.get("ip_rule")
            assert result is not None, "Required property 'ip_rule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rule_desc(self) -> typing.Optional[builtins.str]:
            '''The description of the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspaceipgroup-ipruleitem.html#cfn-workspaces-workspaceipgroup-ipruleitem-ruledesc
            '''
            result = self._values.get("rule_desc")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpRuleItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspaceIpGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "group_desc": "groupDesc",
        "tags": "tags",
        "user_rules": "userRules",
    },
)
class CfnWorkspaceIpGroupProps:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        group_desc: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_rules: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspaceIpGroup.IpRuleItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspaceIpGroup``.

        :param group_name: The name of the group.
        :param group_desc: The description of the group.
        :param tags: The tags for the IP access control group.
        :param user_rules: The rules for the IP access control group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspaceipgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_workspaces as workspaces
            
            cfn_workspace_ip_group_props = workspaces.CfnWorkspaceIpGroupProps(
                group_name="groupName",
            
                # the properties below are optional
                group_desc="groupDesc",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_rules=[workspaces.CfnWorkspaceIpGroup.IpRuleItemProperty(
                    ip_rule="ipRule",
            
                    # the properties below are optional
                    rule_desc="ruleDesc"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a067f55bd2dfbd47a99ad5bd1bd5de5846bb18a8d6b194cee5d30f8efa814bd8)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument group_desc", value=group_desc, expected_type=type_hints["group_desc"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_rules", value=user_rules, expected_type=type_hints["user_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
        }
        if group_desc is not None:
            self._values["group_desc"] = group_desc
        if tags is not None:
            self._values["tags"] = tags
        if user_rules is not None:
            self._values["user_rules"] = user_rules

    @builtins.property
    def group_name(self) -> builtins.str:
        '''The name of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspaceipgroup.html#cfn-workspaces-workspaceipgroup-groupname
        '''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_desc(self) -> typing.Optional[builtins.str]:
        '''The description of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspaceipgroup.html#cfn-workspaces-workspaceipgroup-groupdesc
        '''
        result = self._values.get("group_desc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the IP access control group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspaceipgroup.html#cfn-workspaces-workspaceipgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def user_rules(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspaceIpGroup.IpRuleItemProperty"]]]]:
        '''The rules for the IP access control group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspaceipgroup.html#cfn-workspaces-workspaceipgroup-userrules
        '''
        result = self._values.get("user_rules")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspaceIpGroup.IpRuleItemProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceIpGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_id": "bundleId",
        "directory_id": "directoryId",
        "user_name": "userName",
        "root_volume_encryption_enabled": "rootVolumeEncryptionEnabled",
        "tags": "tags",
        "user_volume_encryption_enabled": "userVolumeEncryptionEnabled",
        "volume_encryption_key": "volumeEncryptionKey",
        "workspace_properties": "workspaceProperties",
    },
)
class CfnWorkspaceProps:
    def __init__(
        self,
        *,
        bundle_id: builtins.str,
        directory_id: builtins.str,
        user_name: builtins.str,
        root_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        user_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        volume_encryption_key: typing.Optional[builtins.str] = None,
        workspace_properties: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspace.WorkspacePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspace``.

        :param bundle_id: The identifier of the bundle for the WorkSpace.
        :param directory_id: The identifier of the Directory Service directory for the WorkSpace.
        :param user_name: The user name of the user for the WorkSpace. This user name must exist in the Directory Service directory for the WorkSpace.
        :param root_volume_encryption_enabled: Indicates whether the data stored on the root volume is encrypted.
        :param tags: The tags for the WorkSpace.
        :param user_volume_encryption_enabled: Indicates whether the data stored on the user volume is encrypted.
        :param volume_encryption_key: The symmetric AWS KMS key used to encrypt data stored on your WorkSpace. Amazon WorkSpaces does not support asymmetric KMS keys.
        :param workspace_properties: The WorkSpace properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_workspaces as workspaces
            
            cfn_workspace_props = workspaces.CfnWorkspaceProps(
                bundle_id="bundleId",
                directory_id="directoryId",
                user_name="userName",
            
                # the properties below are optional
                root_volume_encryption_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_volume_encryption_enabled=False,
                volume_encryption_key="volumeEncryptionKey",
                workspace_properties=workspaces.CfnWorkspace.WorkspacePropertiesProperty(
                    compute_type_name="computeTypeName",
                    root_volume_size_gib=123,
                    running_mode="runningMode",
                    running_mode_auto_stop_timeout_in_minutes=123,
                    user_volume_size_gib=123
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a25f87093526ea01aa087ea6dc9cc539b9abec4e01cf4bf21ae13159b6e31d52)
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument root_volume_encryption_enabled", value=root_volume_encryption_enabled, expected_type=type_hints["root_volume_encryption_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_volume_encryption_enabled", value=user_volume_encryption_enabled, expected_type=type_hints["user_volume_encryption_enabled"])
            check_type(argname="argument volume_encryption_key", value=volume_encryption_key, expected_type=type_hints["volume_encryption_key"])
            check_type(argname="argument workspace_properties", value=workspace_properties, expected_type=type_hints["workspace_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle_id": bundle_id,
            "directory_id": directory_id,
            "user_name": user_name,
        }
        if root_volume_encryption_enabled is not None:
            self._values["root_volume_encryption_enabled"] = root_volume_encryption_enabled
        if tags is not None:
            self._values["tags"] = tags
        if user_volume_encryption_enabled is not None:
            self._values["user_volume_encryption_enabled"] = user_volume_encryption_enabled
        if volume_encryption_key is not None:
            self._values["volume_encryption_key"] = volume_encryption_key
        if workspace_properties is not None:
            self._values["workspace_properties"] = workspace_properties

    @builtins.property
    def bundle_id(self) -> builtins.str:
        '''The identifier of the bundle for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-bundleid
        '''
        result = self._values.get("bundle_id")
        assert result is not None, "Required property 'bundle_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def directory_id(self) -> builtins.str:
        '''The identifier of the Directory Service directory for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-directoryid
        '''
        result = self._values.get("directory_id")
        assert result is not None, "Required property 'directory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The user name of the user for the WorkSpace.

        This user name must exist in the Directory Service directory for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_volume_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Indicates whether the data stored on the root volume is encrypted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-rootvolumeencryptionenabled
        '''
        result = self._values.get("root_volume_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the WorkSpace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def user_volume_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Indicates whether the data stored on the user volume is encrypted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-uservolumeencryptionenabled
        '''
        result = self._values.get("user_volume_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def volume_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The symmetric AWS KMS key used to encrypt data stored on your WorkSpace.

        Amazon WorkSpaces does not support asymmetric KMS keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-volumeencryptionkey
        '''
        result = self._values.get("volume_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_properties(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspace.WorkspacePropertiesProperty"]]:
        '''The WorkSpace properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspace.html#cfn-workspaces-workspace-workspaceproperties
        '''
        result = self._values.get("workspace_properties")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspace.WorkspacePropertiesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_workspaces_4620141e.IWorkspacesPoolRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnWorkspacesPool(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspacesPool",
):
    '''Describes a pool of WorkSpaces.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html
    :cloudformationResource: AWS::WorkSpaces::WorkspacesPool
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_workspaces as workspaces
        
        cfn_workspaces_pool = workspaces.CfnWorkspacesPool(self, "MyCfnWorkspacesPool",
            bundle_id="bundleId",
            capacity=workspaces.CfnWorkspacesPool.CapacityProperty(
                desired_user_sessions=123
            ),
            directory_id="directoryId",
            pool_name="poolName",
        
            # the properties below are optional
            application_settings=workspaces.CfnWorkspacesPool.ApplicationSettingsProperty(
                status="status",
        
                # the properties below are optional
                settings_group="settingsGroup"
            ),
            description="description",
            running_mode="runningMode",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            timeout_settings=workspaces.CfnWorkspacesPool.TimeoutSettingsProperty(
                disconnect_timeout_in_seconds=123,
                idle_disconnect_timeout_in_seconds=123,
                max_user_duration_in_seconds=123
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        bundle_id: builtins.str,
        capacity: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspacesPool.CapacityProperty", typing.Dict[builtins.str, typing.Any]]],
        directory_id: builtins.str,
        pool_name: builtins.str,
        application_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspacesPool.ApplicationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        running_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspacesPool.TimeoutSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WorkSpaces::WorkspacesPool``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param bundle_id: The identifier of the bundle used by the pool.
        :param capacity: Describes the user capacity for the pool.
        :param directory_id: The identifier of the directory used by the pool.
        :param pool_name: The name of the pool.
        :param application_settings: The persistent application settings for users of the pool.
        :param description: The description of the pool.
        :param running_mode: The running mode of the pool.
        :param tags: 
        :param timeout_settings: The amount of time that a pool session remains active after users disconnect. If they try to reconnect to the pool session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new pool instance.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2d46eb37beb6bc915a0a0c68f02dfa689a2d725a4252e6874da1ed60602a91e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspacesPoolProps(
            bundle_id=bundle_id,
            capacity=capacity,
            directory_id=directory_id,
            pool_name=pool_name,
            application_settings=application_settings,
            description=description,
            running_mode=running_mode,
            tags=tags,
            timeout_settings=timeout_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForWorkspacesPool")
    @builtins.classmethod
    def arn_for_workspaces_pool(
        cls,
        resource: "_aws_workspaces_4620141e.IWorkspacesPoolRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c2dbd5f4064559f5e78985e554d7a34aa799b2798c681d557e9855c751c0916f)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForWorkspacesPool", [resource]))

    @jsii.member(jsii_name="fromPoolId")
    @builtins.classmethod
    def from_pool_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        pool_id: builtins.str,
    ) -> "_aws_workspaces_4620141e.IWorkspacesPoolRef":
        '''Creates a new IWorkspacesPoolRef from a poolId.

        :param scope: -
        :param id: -
        :param pool_id: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aca13282ecc7b7c8ac155574994d5d8d845bec6aa4ca0daf161949c9810e9624)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
        return typing.cast("_aws_workspaces_4620141e.IWorkspacesPoolRef", jsii.sinvoke(cls, "fromPoolId", [scope, id, pool_id]))

    @jsii.member(jsii_name="fromWorkspacesPoolArn")
    @builtins.classmethod
    def from_workspaces_pool_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        arn: builtins.str,
    ) -> "_aws_workspaces_4620141e.IWorkspacesPoolRef":
        '''Creates a new IWorkspacesPoolRef from an ARN.

        :param scope: -
        :param id: -
        :param arn: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__465631994003e79f30cef2521513b6f1d5f50c2aa738f7e794eda5bec14dc824)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast("_aws_workspaces_4620141e.IWorkspacesPoolRef", jsii.sinvoke(cls, "fromWorkspacesPoolArn", [scope, id, arn]))

    @jsii.member(jsii_name="isCfnWorkspacesPool")
    @builtins.classmethod
    def is_cfn_workspaces_pool(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnWorkspacesPool.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d95fd45f53c6dbbf035cfa65feb9e596460f33a7c75ea9712267b2a083e3d9e0)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnWorkspacesPool", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f53d77ec5dfd335f69439256c79f2f3c6b1b45896c302f8bc1c0ec35d59c6d29)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6572b9ddfe4047dc8ae204de87ae166ce2e8e400e06ba8974d92873782c30b29)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time the pool was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrPoolArn")
    def attr_pool_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the pool.

        :cloudformationAttribute: PoolArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPoolArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPoolId")
    def attr_pool_id(self) -> builtins.str:
        '''The identifier of the pool.

        :cloudformationAttribute: PoolId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPoolId"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="workspacesPoolRef")
    def workspaces_pool_ref(self) -> "_aws_workspaces_4620141e.WorkspacesPoolReference":
        '''A reference to a WorkspacesPool resource.'''
        return typing.cast("_aws_workspaces_4620141e.WorkspacesPoolReference", jsii.get(self, "workspacesPoolRef"))

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> builtins.str:
        '''The identifier of the bundle used by the pool.'''
        return typing.cast(builtins.str, jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0452074a51df88aa4932643faa31ebd1eccc5cee06312ade358694132b52084a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.CapacityProperty"]:
        '''Describes the user capacity for the pool.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.CapacityProperty"], jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.CapacityProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6c57f030f2306ece2ea0c01485d454bac3da27c5dc44bd0b7ba4d7e46018432e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        '''The identifier of the directory used by the pool.'''
        return typing.cast(builtins.str, jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b8d6e0e3699724e780725f41f79c5fa5a20dddef0c63fb39c3b1dc0ad1f999af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolName")
    def pool_name(self) -> builtins.str:
        '''The name of the pool.'''
        return typing.cast(builtins.str, jsii.get(self, "poolName"))

    @pool_name.setter
    def pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__be64bf569690a63465e1cb83bfe620df5dc0e4eb9288b061c8c5ce9acc7ed6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.ApplicationSettingsProperty"]]:
        '''The persistent application settings for users of the pool.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.ApplicationSettingsProperty"]], jsii.get(self, "applicationSettings"))

    @application_settings.setter
    def application_settings(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.ApplicationSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__910fbbdd803ad5d164bc189f1acae9c33a7b4357cf407bdba7e99d2fa0824bb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the pool.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c0a41c1359bb84431b1e88b8ac1a3bbf0d34dc2ab1b9004f79a2f0891725fd76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runningMode")
    def running_mode(self) -> typing.Optional[builtins.str]:
        '''The running mode of the pool.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runningMode"))

    @running_mode.setter
    def running_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__360e48883f6f5eb30b47d1d804ac1d51f3162354f1b454a279520a266673b89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runningMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''
        :deprecated: this property has been deprecated

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a940a91e0c4bd8a1424475cae423b68c22b5107bb7454e6d62fa5d1a232ac829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSettings")
    def timeout_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.TimeoutSettingsProperty"]]:
        '''The amount of time that a pool session remains active after users disconnect.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.TimeoutSettingsProperty"]], jsii.get(self, "timeoutSettings"))

    @timeout_settings.setter
    def timeout_settings(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.TimeoutSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1878f21dfd9d97896d58974c22ca93f62dbad42d1696ecad5a5dd10ef4d5a465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSettings", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspacesPool.ApplicationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "settings_group": "settingsGroup"},
    )
    class ApplicationSettingsProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            settings_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The persistent application settings for users in the pool.

            :param status: Enables or disables persistent application settings for users during their pool sessions.
            :param settings_group: The path prefix for the S3 bucket where users’ persistent application settings are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-applicationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                application_settings_property = workspaces.CfnWorkspacesPool.ApplicationSettingsProperty(
                    status="status",
                
                    # the properties below are optional
                    settings_group="settingsGroup"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e13c075b4f811931f6538f282bd7fba14fae39c758507a1d16dca095b2fec9f7)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument settings_group", value=settings_group, expected_type=type_hints["settings_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "status": status,
            }
            if settings_group is not None:
                self._values["settings_group"] = settings_group

        @builtins.property
        def status(self) -> builtins.str:
            '''Enables or disables persistent application settings for users during their pool sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-applicationsettings.html#cfn-workspaces-workspacespool-applicationsettings-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def settings_group(self) -> typing.Optional[builtins.str]:
            '''The path prefix for the S3 bucket where users’ persistent application settings are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-applicationsettings.html#cfn-workspaces-workspacespool-applicationsettings-settingsgroup
            '''
            result = self._values.get("settings_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspacesPool.CapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"desired_user_sessions": "desiredUserSessions"},
    )
    class CapacityProperty:
        def __init__(self, *, desired_user_sessions: jsii.Number) -> None:
            '''Describes the user capacity for the pool.

            :param desired_user_sessions: The desired number of user sessions for the WorkSpaces in the pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-capacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                capacity_property = workspaces.CfnWorkspacesPool.CapacityProperty(
                    desired_user_sessions=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c51935746c4546a0264ecc802bfcdee7763273ebc05cf76e764d89dabc01d24d)
                check_type(argname="argument desired_user_sessions", value=desired_user_sessions, expected_type=type_hints["desired_user_sessions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "desired_user_sessions": desired_user_sessions,
            }

        @builtins.property
        def desired_user_sessions(self) -> jsii.Number:
            '''The desired number of user sessions for the WorkSpaces in the pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-capacity.html#cfn-workspaces-workspacespool-capacity-desiredusersessions
            '''
            result = self._values.get("desired_user_sessions")
            assert result is not None, "Required property 'desired_user_sessions' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspacesPool.TimeoutSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disconnect_timeout_in_seconds": "disconnectTimeoutInSeconds",
            "idle_disconnect_timeout_in_seconds": "idleDisconnectTimeoutInSeconds",
            "max_user_duration_in_seconds": "maxUserDurationInSeconds",
        },
    )
    class TimeoutSettingsProperty:
        def __init__(
            self,
            *,
            disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the timeout settings for the pool.

            :param disconnect_timeout_in_seconds: Specifies the amount of time, in seconds, that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within the time set, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.
            :param idle_disconnect_timeout_in_seconds: The amount of time in seconds a connection will stay active while idle.
            :param max_user_duration_in_seconds: Specifies the maximum amount of time, in seconds, that a streaming session can remain active. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_workspaces as workspaces
                
                timeout_settings_property = workspaces.CfnWorkspacesPool.TimeoutSettingsProperty(
                    disconnect_timeout_in_seconds=123,
                    idle_disconnect_timeout_in_seconds=123,
                    max_user_duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__57bd34e59b9d7d1fcbeb50272ac7cbdec29ebf1c3f4ef3146b6cddd5bf9cf52e)
                check_type(argname="argument disconnect_timeout_in_seconds", value=disconnect_timeout_in_seconds, expected_type=type_hints["disconnect_timeout_in_seconds"])
                check_type(argname="argument idle_disconnect_timeout_in_seconds", value=idle_disconnect_timeout_in_seconds, expected_type=type_hints["idle_disconnect_timeout_in_seconds"])
                check_type(argname="argument max_user_duration_in_seconds", value=max_user_duration_in_seconds, expected_type=type_hints["max_user_duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disconnect_timeout_in_seconds is not None:
                self._values["disconnect_timeout_in_seconds"] = disconnect_timeout_in_seconds
            if idle_disconnect_timeout_in_seconds is not None:
                self._values["idle_disconnect_timeout_in_seconds"] = idle_disconnect_timeout_in_seconds
            if max_user_duration_in_seconds is not None:
                self._values["max_user_duration_in_seconds"] = max_user_duration_in_seconds

        @builtins.property
        def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the amount of time, in seconds, that a streaming session remains active after users disconnect.

            If users try to reconnect to the streaming session after a disconnection or network interruption within the time set, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html#cfn-workspaces-workspacespool-timeoutsettings-disconnecttimeoutinseconds
            '''
            result = self._values.get("disconnect_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time in seconds a connection will stay active while idle.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html#cfn-workspaces-workspacespool-timeoutsettings-idledisconnecttimeoutinseconds
            '''
            result = self._values.get("idle_disconnect_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum amount of time, in seconds, that a streaming session can remain active.

            If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspaces-workspacespool-timeoutsettings.html#cfn-workspaces-workspacespool-timeoutsettings-maxuserdurationinseconds
            '''
            result = self._values.get("max_user_duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeoutSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_workspaces.CfnWorkspacesPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_id": "bundleId",
        "capacity": "capacity",
        "directory_id": "directoryId",
        "pool_name": "poolName",
        "application_settings": "applicationSettings",
        "description": "description",
        "running_mode": "runningMode",
        "tags": "tags",
        "timeout_settings": "timeoutSettings",
    },
)
class CfnWorkspacesPoolProps:
    def __init__(
        self,
        *,
        bundle_id: builtins.str,
        capacity: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspacesPool.CapacityProperty", typing.Dict[builtins.str, typing.Any]]],
        directory_id: builtins.str,
        pool_name: builtins.str,
        application_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspacesPool.ApplicationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        running_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnWorkspacesPool.TimeoutSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspacesPool``.

        :param bundle_id: The identifier of the bundle used by the pool.
        :param capacity: Describes the user capacity for the pool.
        :param directory_id: The identifier of the directory used by the pool.
        :param pool_name: The name of the pool.
        :param application_settings: The persistent application settings for users of the pool.
        :param description: The description of the pool.
        :param running_mode: The running mode of the pool.
        :param tags: 
        :param timeout_settings: The amount of time that a pool session remains active after users disconnect. If they try to reconnect to the pool session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new pool instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_workspaces as workspaces
            
            cfn_workspaces_pool_props = workspaces.CfnWorkspacesPoolProps(
                bundle_id="bundleId",
                capacity=workspaces.CfnWorkspacesPool.CapacityProperty(
                    desired_user_sessions=123
                ),
                directory_id="directoryId",
                pool_name="poolName",
            
                # the properties below are optional
                application_settings=workspaces.CfnWorkspacesPool.ApplicationSettingsProperty(
                    status="status",
            
                    # the properties below are optional
                    settings_group="settingsGroup"
                ),
                description="description",
                running_mode="runningMode",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                timeout_settings=workspaces.CfnWorkspacesPool.TimeoutSettingsProperty(
                    disconnect_timeout_in_seconds=123,
                    idle_disconnect_timeout_in_seconds=123,
                    max_user_duration_in_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cb4cf19658d50453aaf837ebc448848141de5ab5627b58be920162b658ff8854)
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument application_settings", value=application_settings, expected_type=type_hints["application_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument running_mode", value=running_mode, expected_type=type_hints["running_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_settings", value=timeout_settings, expected_type=type_hints["timeout_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle_id": bundle_id,
            "capacity": capacity,
            "directory_id": directory_id,
            "pool_name": pool_name,
        }
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if description is not None:
            self._values["description"] = description
        if running_mode is not None:
            self._values["running_mode"] = running_mode
        if tags is not None:
            self._values["tags"] = tags
        if timeout_settings is not None:
            self._values["timeout_settings"] = timeout_settings

    @builtins.property
    def bundle_id(self) -> builtins.str:
        '''The identifier of the bundle used by the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-bundleid
        '''
        result = self._values.get("bundle_id")
        assert result is not None, "Required property 'bundle_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.CapacityProperty"]:
        '''Describes the user capacity for the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-capacity
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.CapacityProperty"], result)

    @builtins.property
    def directory_id(self) -> builtins.str:
        '''The identifier of the directory used by the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-directoryid
        '''
        result = self._values.get("directory_id")
        assert result is not None, "Required property 'directory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_name(self) -> builtins.str:
        '''The name of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-poolname
        '''
        result = self._values.get("pool_name")
        assert result is not None, "Required property 'pool_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.ApplicationSettingsProperty"]]:
        '''The persistent application settings for users of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-applicationsettings
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.ApplicationSettingsProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def running_mode(self) -> typing.Optional[builtins.str]:
        '''The running mode of the pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-runningmode
        '''
        result = self._values.get("running_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-tags
        :stability: deprecated
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def timeout_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.TimeoutSettingsProperty"]]:
        '''The amount of time that a pool session remains active after users disconnect.

        If they try to reconnect to the pool session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new pool instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspaces-workspacespool.html#cfn-workspaces-workspacespool-timeoutsettings
        '''
        result = self._values.get("timeout_settings")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnWorkspacesPool.TimeoutSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspacesPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnectionAlias",
    "CfnConnectionAliasProps",
    "CfnDirectory",
    "CfnDirectoryProps",
    "CfnWorkspace",
    "CfnWorkspaceIpGroup",
    "CfnWorkspaceIpGroupProps",
    "CfnWorkspaceProps",
    "CfnWorkspacesPool",
    "CfnWorkspacesPoolProps",
]

publication.publish()

def _typecheckingstub__3fd73d00432c1164a74beb35acf6162e3d82fa91d51a0edf8c896028b6e3c6d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    connection_string: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f39ec24ce0950d3ba9ddf713f5b5c8349a489a83df314a68c350efb2fde838(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d07e3ef46b7d1868d493367bae11c00c38fa0bb35cfa4e162e97b1482bf156(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d590d73fb55367a8be64477837c062053aa020d8931e1f1983124013786434f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8b72c0a6880f896fe31f0555dd87dfdcce86c05579ff4a417ab736a03b4fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf34741743106631ede324d61fdd5ed726b94e64d09574347d59201303db6f9(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614a827f45558e3ee89a9937d774dc07580e2d2d88ccf9a78ea211acad9d7c19(
    *,
    associated_account_id: typing.Optional[builtins.str] = None,
    association_status: typing.Optional[builtins.str] = None,
    connection_identifier: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d1c548638caf6c8699dd74d5bcc8d8df516e1a0738521496aee37402727de8(
    *,
    connection_string: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d2fd090a322f0e86011be41549fee5ba73daf4f5f02076bb14f2e5c613cc90(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    active_directory_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.ActiveDirectoryConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_self_service: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    endpoint_encryption_mode: typing.Optional[builtins.str] = None,
    idc_instance_arn: typing.Optional[builtins.str] = None,
    ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    microsoft_entra_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.MicrosoftEntraConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    saml_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.SamlPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    selfservice_permissions: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.SelfservicePermissionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    streaming_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.StreamingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tenancy: typing.Optional[builtins.str] = None,
    user_identity_type: typing.Optional[builtins.str] = None,
    workspace_access_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.WorkspaceAccessPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace_creation_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.DefaultWorkspaceCreationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace_directory_description: typing.Optional[builtins.str] = None,
    workspace_directory_name: typing.Optional[builtins.str] = None,
    workspace_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdffabab5518c6dfd10b6189ff95a9b939ec41d46c84120537446c0b207aa3f4(
    resource: _aws_workspaces_4620141e.IDirectoryRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12748995b26571c6b584a78b311a91b4858d813a9de56630d9cc8a06efa30670(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d63a54fc0f25eb54b703a8b2271391a2de4dccf825da047fe18cc0e3bacac8(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bd5c53c0844aa7f2f45f96592d3cbb86fe27c7c773eede54fa6b91cd0c7f27(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5935083ae4bb3e24425d51af0007be0cd0d57e8ff8ff72702ac9593e3f928cc(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.ActiveDirectoryConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14bd4bcf3be59597cc94b6622b6d08872f213251205ed7e8ac43e7cd343d0f0(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.CertificateBasedAuthPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5b380d1fadf9673790a641ab3bc2d51de5797c899e2b3fd2d11f04cfd41aaf(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48bd075e1d5f4e21bd96297cef42d2f7dcd3b3b0b09282064e75850711378bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d199dd5b9442a70e651b9c77f9fa0566e1d9960e98c9c8baea8f22ee9287a2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12cd311ffce9568cff4f9a934712be539ba52685ec7024f986cd60c7c1f3d45(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1c4fc7c0c44f9f4a3d44936bef556cf289dc3adb77a8f5f4eee4dac8dfc9b9(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.MicrosoftEntraConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9476ef4c83098329845a817adfab1e370a5ee7ed7efc8ef90ee6b255ea7f7c(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.SamlPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d850202b4b1b5c70f0967ed877c9383134b8b4322c36f14fa5a82730ae0e648a(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.SelfservicePermissionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f1f768604605fd8c2f117048afe270d2a8c642cf2f27bad1281c65a58b5feb(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.StreamingPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd17e443fdeffd0d8f357751e184e1e851c50a732595b91eec1b8bf5eb0ca0e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b57d5e0d13092d1ac273dd853c173fae7fcaba6c8767a4be90933c4e5df709(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb1af56f4750cefa6bb0b0a5b6d97e4eee63424bda5338ea220b885617a0c89(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c9fb93d4661ad4bfb38b4968e127400e5a702021709244b6d658c01dbcfb7b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8724beb6e6ee10070a868ef023abdb06e729abd29cc0b01ac20a32b2c1bc1697(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.WorkspaceAccessPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216b29943227b73b434fdf6b0fec0183add3a5cde23dcdc1d4fff9a5b8a97c9d(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnDirectory.DefaultWorkspaceCreationPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098e67aa24151ba52b4a187547fe3bfe6102d7d77ffe9f5407daa4c43b979ac7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b41ec10b32352bd312188184670dee7448018cddc80956a217145e754c071e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a158204c3529104edbe60ac679af107f42bb82458981aeb6a21c799e00e3ab(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba9a18ad9d6cd68b06909aaad77c534309ec8d39f744baad2f2c7a8aae55852(
    *,
    access_endpoints: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]],
    internet_fallback_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39185f9119f3d0883d05448778c03e1be9e3752bc4640c32fbd98609b6805ebf(
    *,
    access_endpoint_type: typing.Optional[builtins.str] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ea3bc303fd18efdf01d9d0ed5f93e34d450353289262313dca3511076eee9d(
    *,
    domain_name: builtins.str,
    service_account_secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5b4bd7bf8f7b42c1b026907d8b0c63a5212a29cec1f1dfe5d4e506ff2f338c(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad3786ebe3af46bd62ca671ef7d20163db404055c890619acac286bc6b5ba71(
    *,
    custom_security_group_id: typing.Optional[builtins.str] = None,
    default_ou: typing.Optional[builtins.str] = None,
    enable_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    enable_maintenance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    instance_iam_role_arn: typing.Optional[builtins.str] = None,
    user_enabled_as_local_administrator: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199ae25c0d1364aa0c94b7ad03fd0a32f19a6cc84de14a43cfb585d4720859a0(
    *,
    mode: builtins.str,
    preferred_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a78b77bd8100ad2ae337b65f5313eafa1832bc96163e7746e0f48d219ecb2d(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9940a6ad225287b5d67e7486f545651568899a168da4936344e76bb6ba8f3aa(
    *,
    application_config_secret_arn: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2504bb91b90dedcd987a0e28039477a816c525ee82f3f6e6485d89be3f46e3e(
    *,
    relay_state_parameter_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    user_access_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1115704039492fa3d660af1d1f5a4e708fca100ec9218943f42baf272258d6c(
    *,
    change_compute_type: typing.Optional[builtins.str] = None,
    increase_volume_size: typing.Optional[builtins.str] = None,
    rebuild_workspace: typing.Optional[builtins.str] = None,
    restart_workspace: typing.Optional[builtins.str] = None,
    switch_running_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27aefaf54a243cf84a711ce534a88e0a0216741f4075781e1ad2694063c21b2a(
    *,
    connector_type: builtins.str,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c1eddaaf1b110af530faff46ca41d24fb665c60dc4e97bf9dd1ff14b443e3d(
    *,
    global_accelerator: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.GlobalAcceleratorForDirectoryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_connectors: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    streaming_experience_preferred_protocol: typing.Optional[builtins.str] = None,
    user_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.UserSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b5fa4de3d1090575ac74178ddc5102bf004f716f9a3cb09a3ee34a79a84e1f(
    *,
    action: builtins.str,
    permission: builtins.str,
    maximum_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d70f5a7d065768e4f5eddf82eafb687010b12c5844026538a57ca21f74af95(
    *,
    access_endpoint_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.AccessEndpointConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    device_type_android: typing.Optional[builtins.str] = None,
    device_type_chrome_os: typing.Optional[builtins.str] = None,
    device_type_ios: typing.Optional[builtins.str] = None,
    device_type_linux: typing.Optional[builtins.str] = None,
    device_type_osx: typing.Optional[builtins.str] = None,
    device_type_web: typing.Optional[builtins.str] = None,
    device_type_windows: typing.Optional[builtins.str] = None,
    device_type_work_spaces_thin_client: typing.Optional[builtins.str] = None,
    device_type_zero_client: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b02a6e4a9c5198c9a5097f9f8bf2dda738ab763e2710273958ea729227a0502(
    *,
    active_directory_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.ActiveDirectoryConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_self_service: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    endpoint_encryption_mode: typing.Optional[builtins.str] = None,
    idc_instance_arn: typing.Optional[builtins.str] = None,
    ip_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    microsoft_entra_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.MicrosoftEntraConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    saml_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.SamlPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    selfservice_permissions: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.SelfservicePermissionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    streaming_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.StreamingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tenancy: typing.Optional[builtins.str] = None,
    user_identity_type: typing.Optional[builtins.str] = None,
    workspace_access_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.WorkspaceAccessPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace_creation_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnDirectory.DefaultWorkspaceCreationPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workspace_directory_description: typing.Optional[builtins.str] = None,
    workspace_directory_name: typing.Optional[builtins.str] = None,
    workspace_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf9321ac6e165dfc96d72b093b8636e1ff9e82acf9cea2e5176beb79bb65839(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bundle_id: builtins.str,
    directory_id: builtins.str,
    user_name: builtins.str,
    root_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    volume_encryption_key: typing.Optional[builtins.str] = None,
    workspace_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspace.WorkspacePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6d998e49570cc52ccb0ecfad0db07c3b31d793cd316fcd6de9bd3cde91f30e(
    resource: _aws_workspaces_4620141e.IWorkspaceRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d89928bc3143b40dfcbe60436eb821c87d4ca5d7e96d4ce7e5b5f26125f7d08(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0189c0ab3f83c44331c574b9d6fa036f364fb409d35f51f73b8fba8ae858db28(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e772192f4dd8e60f99b92beca96b37f99aca30dac13f906848601f52405c8d90(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4902c0d49db4502ddf5bb0c1b99a8dd9ce3aa66f14904ef46eb1b040033e0f6f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f2e671a0d784d1293a9f59800a4ee9327ac8c35d2975eb4bccf99d78c24ba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098a48aaecf371ba14035ae50fde38957b608503f7c78dc0f9568806cd61b926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225037370c6d4ae1d7c6fb794db70699fb16815233054c687f769b05c6298ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb29c66862be75fab751682c7102c72c4846798afbc12b529f0ece9b38719128(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2a501e8ab3d90f102a797f62bdece7b78195c5b29e714a25825ca056f061c4(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd38103f5213efdd25dca3a2f0c8dcbf665bbcfb052ef6f4c929ce79e0719d6(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0670847357c5e2a262f5f7ce5cb07d9b48f5d29700739766ad22e91419e89b88(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfa33f0e5fe13fa6e31e4fac282721ea7584fa1e07cea2b5dc3a6a41028a2ad(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnWorkspace.WorkspacePropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba35df0c40a72c6300f0149e43d82fc399d7f07da77a68563d45ca0546db330(
    *,
    compute_type_name: typing.Optional[builtins.str] = None,
    root_volume_size_gib: typing.Optional[jsii.Number] = None,
    running_mode: typing.Optional[builtins.str] = None,
    running_mode_auto_stop_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    user_volume_size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ad7b8ae0ab90e6cccba48331cf2278b942c4e2286ff003c7c5d3d01eb23328(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_name: builtins.str,
    group_desc: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_rules: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspaceIpGroup.IpRuleItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6173be321bf1f4583b718296cd816a36887510f673584b9755d887f8328a075b(
    resource: _aws_workspaces_4620141e.IWorkspaceIpGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9132cdbc4b4e441b9b431185b1b82925c868d98f9de4a66ab2372c7dee556bb9(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a38c23726b5bd916d89720d7358c4e2dd6101aa955590a0d66b5ab633960c13(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0b5471f4e6c8a14b058cc3fccd30854f815a8bbe8e7da1a194ce1c392aecb6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e4d60d6ae5674582b5244ffdabad710288b71a02010f9b8622243f01194ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48e0db76d8f4fa74fb3edf59e6f0ed00c82f7f491a236618982a4f0c084951a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a29bad2cf4dbccb24edf13ca2ba3777f254924581e693a9b2c1a384d3b6ca6(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523c626d42fae94b47c0403319513a730cd38c8b35b9fadd760de3c0007f0c03(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnWorkspaceIpGroup.IpRuleItemProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f873d26323a491ea3042f52973cfd827eb9aee1985f5153152030dd4dec84b61(
    *,
    ip_rule: builtins.str,
    rule_desc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a067f55bd2dfbd47a99ad5bd1bd5de5846bb18a8d6b194cee5d30f8efa814bd8(
    *,
    group_name: builtins.str,
    group_desc: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_rules: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspaceIpGroup.IpRuleItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25f87093526ea01aa087ea6dc9cc539b9abec4e01cf4bf21ae13159b6e31d52(
    *,
    bundle_id: builtins.str,
    directory_id: builtins.str,
    user_name: builtins.str,
    root_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_volume_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    volume_encryption_key: typing.Optional[builtins.str] = None,
    workspace_properties: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspace.WorkspacePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d46eb37beb6bc915a0a0c68f02dfa689a2d725a4252e6874da1ed60602a91e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bundle_id: builtins.str,
    capacity: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspacesPool.CapacityProperty, typing.Dict[builtins.str, typing.Any]]],
    directory_id: builtins.str,
    pool_name: builtins.str,
    application_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspacesPool.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    running_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspacesPool.TimeoutSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dbd5f4064559f5e78985e554d7a34aa799b2798c681d557e9855c751c0916f(
    resource: _aws_workspaces_4620141e.IWorkspacesPoolRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca13282ecc7b7c8ac155574994d5d8d845bec6aa4ca0daf161949c9810e9624(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465631994003e79f30cef2521513b6f1d5f50c2aa738f7e794eda5bec14dc824(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95fd45f53c6dbbf035cfa65feb9e596460f33a7c75ea9712267b2a083e3d9e0(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53d77ec5dfd335f69439256c79f2f3c6b1b45896c302f8bc1c0ec35d59c6d29(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6572b9ddfe4047dc8ae204de87ae166ce2e8e400e06ba8974d92873782c30b29(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0452074a51df88aa4932643faa31ebd1eccc5cee06312ade358694132b52084a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c57f030f2306ece2ea0c01485d454bac3da27c5dc44bd0b7ba4d7e46018432e(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnWorkspacesPool.CapacityProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d6e0e3699724e780725f41f79c5fa5a20dddef0c63fb39c3b1dc0ad1f999af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be64bf569690a63465e1cb83bfe620df5dc0e4eb9288b061c8c5ce9acc7ed6cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910fbbdd803ad5d164bc189f1acae9c33a7b4357cf407bdba7e99d2fa0824bb7(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnWorkspacesPool.ApplicationSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a41c1359bb84431b1e88b8ac1a3bbf0d34dc2ab1b9004f79a2f0891725fd76(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360e48883f6f5eb30b47d1d804ac1d51f3162354f1b454a279520a266673b89b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a940a91e0c4bd8a1424475cae423b68c22b5107bb7454e6d62fa5d1a232ac829(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1878f21dfd9d97896d58974c22ca93f62dbad42d1696ecad5a5dd10ef4d5a465(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnWorkspacesPool.TimeoutSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13c075b4f811931f6538f282bd7fba14fae39c758507a1d16dca095b2fec9f7(
    *,
    status: builtins.str,
    settings_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51935746c4546a0264ecc802bfcdee7763273ebc05cf76e764d89dabc01d24d(
    *,
    desired_user_sessions: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bd34e59b9d7d1fcbeb50272ac7cbdec29ebf1c3f4ef3146b6cddd5bf9cf52e(
    *,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4cf19658d50453aaf837ebc448848141de5ab5627b58be920162b658ff8854(
    *,
    bundle_id: builtins.str,
    capacity: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspacesPool.CapacityProperty, typing.Dict[builtins.str, typing.Any]]],
    directory_id: builtins.str,
    pool_name: builtins.str,
    application_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspacesPool.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    running_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnWorkspacesPool.TimeoutSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
