r'''
# AWS::AppFabric Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_appfabric as appfabric
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AppFabric construct libraries](https://constructs.dev/search?q=appfabric)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AppFabric resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppFabric.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AppFabric](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppFabric.html).

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
    import aws_cdk.interfaces.aws_appfabric as _aws_appfabric_09bd86cb
    import constructs as _constructs_77d1e7e8
else:

    _aws_appfabric_09bd86cb = _LazyImport("aws_cdk.interfaces.aws_appfabric")
    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_appfabric_09bd86cb.IAppAuthorizationRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnAppAuthorization(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_appfabric.CfnAppAuthorization",
):
    '''Creates an app authorization within an app bundle, which allows AppFabric to connect to an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html
    :cloudformationResource: AWS::AppFabric::AppAuthorization
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_appfabric as appfabric
        
        cfn_app_authorization = appfabric.CfnAppAuthorization(self, "MyCfnAppAuthorization",
            app="app",
            app_bundle_identifier="appBundleIdentifier",
            auth_type="authType",
            tenant=appfabric.CfnAppAuthorization.TenantProperty(
                tenant_display_name="tenantDisplayName",
                tenant_identifier="tenantIdentifier"
            ),
        
            # the properties below are optional
            credential=appfabric.CfnAppAuthorization.CredentialProperty(
                api_key_credential=appfabric.CfnAppAuthorization.ApiKeyCredentialProperty(
                    api_key="apiKey"
                ),
                oauth2_credential=appfabric.CfnAppAuthorization.Oauth2CredentialProperty(
                    client_id="clientId",
                    client_secret="clientSecret"
                )
            ),
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
        app: builtins.str,
        app_bundle_identifier: builtins.str,
        auth_type: builtins.str,
        tenant: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppAuthorization.TenantProperty", typing.Dict[builtins.str, typing.Any]]],
        credential: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppAuthorization.CredentialProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppFabric::AppAuthorization``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param app: The name of the application.
        :param app_bundle_identifier: The Amazon Resource Name (ARN) or Universal Unique Identifier (UUID) of the app bundle to use for the request.
        :param auth_type: The authorization type.
        :param tenant: Contains information about an application tenant.
        :param credential: Contains credential information for the application.
        :param tags: Tags to apply to the app authorization.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e12909d0c7ca35d743d93519a7d4405f3120d32c5a26e6f239eaca61d1ef5a44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppAuthorizationProps(
            app=app,
            app_bundle_identifier=app_bundle_identifier,
            auth_type=auth_type,
            tenant=tenant,
            credential=credential,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAppAuthorization")
    @builtins.classmethod
    def arn_for_app_authorization(
        cls,
        resource: "_aws_appfabric_09bd86cb.IAppAuthorizationRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7ce115e88f391c1771b6f6a929951c75a05f3393dbc4e25aac30a65891885fb3)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAppAuthorization", [resource]))

    @jsii.member(jsii_name="isCfnAppAuthorization")
    @builtins.classmethod
    def is_cfn_app_authorization(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAppAuthorization.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b165b7cd6fcdbbbecc8ecf3c4f9f3d19744619ef2cfdcea27e0d4664145cfc1e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAppAuthorization", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1d52289e4d0efa512b5d0361547375936d4c2d7427eab6ede50e448cc3aefe46)
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
            type_hints = cached_type_hints(_typecheckingstub__6c0ddada5f0bb35cc5ee33b676284e95b652f112aeb3de6441898446e0da3e52)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="appAuthorizationRef")
    def app_authorization_ref(
        self,
    ) -> "_aws_appfabric_09bd86cb.AppAuthorizationReference":
        '''A reference to a AppAuthorization resource.'''
        return typing.cast("_aws_appfabric_09bd86cb.AppAuthorizationReference", jsii.get(self, "appAuthorizationRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAppAuthorizationArn")
    def attr_app_authorization_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the app authorization.

        :cloudformationAttribute: AppAuthorizationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppAuthorizationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAppAuthorizationIdentifier")
    def attr_app_authorization_identifier(self) -> builtins.str:
        '''The unique identifier of the app authorization.

        :cloudformationAttribute: AppAuthorizationIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppAuthorizationIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="attrAppBundleArn")
    def attr_app_bundle_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the app bundle for the app authorization.

        :cloudformationAttribute: AppBundleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppBundleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp of when the app authorization was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrPersona")
    def attr_persona(self) -> builtins.str:
        '''The user persona of the app authorization.

        :cloudformationAttribute: Persona
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPersona"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The state of the app authorization.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp of when the app authorization was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

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
    @jsii.member(jsii_name="app")
    def app(self) -> builtins.str:
        '''The name of the application.'''
        return typing.cast(builtins.str, jsii.get(self, "app"))

    @app.setter
    def app(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__af75cefc1eac3043e9595b2871148ae23ff4c53db801ed09e9f46abe7b5cf124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "app", value)

    @builtins.property
    @jsii.member(jsii_name="appBundleIdentifier")
    def app_bundle_identifier(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) or Universal Unique Identifier (UUID) of the app bundle to use for the request.'''
        return typing.cast(builtins.str, jsii.get(self, "appBundleIdentifier"))

    @app_bundle_identifier.setter
    def app_bundle_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f2b6984a49d513d9f5e4f015dea43ab391f055cede9af681b7a1b15a88d0716e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appBundleIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        '''The authorization type.'''
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b4d7476f9181c3e9c2a407648bbfde2a42d8da9d241bde4a857bdafd2a29827e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="tenant")
    def tenant(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.TenantProperty"]:
        '''Contains information about an application tenant.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.TenantProperty"], jsii.get(self, "tenant"))

    @tenant.setter
    def tenant(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.TenantProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f4c4193ac61adbc5dd44c570222434a7c62d8eefa41efaa28dd2351284e14308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenant", value)

    @builtins.property
    @jsii.member(jsii_name="credential")
    def credential(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.CredentialProperty"]]:
        '''Contains credential information for the application.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.CredentialProperty"]], jsii.get(self, "credential"))

    @credential.setter
    def credential(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.CredentialProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0fe8e050a5434452f52e90d67f54b3bccec37eb061b6f9b2bc5384a1c252f6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credential", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to apply to the app authorization.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0ebf4f36e4e4db8e95130058fa75e4a1352483f135485b1748fa18956fbdf150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnAppAuthorization.ApiKeyCredentialProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey"},
    )
    class ApiKeyCredentialProperty:
        def __init__(self, *, api_key: builtins.str) -> None:
            '''Contains API key credential information.

            :param api_key: An API key for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-apikeycredential.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                api_key_credential_property = appfabric.CfnAppAuthorization.ApiKeyCredentialProperty(
                    api_key="apiKey"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__c5d2c3224c6ad552e4e46080b761e62579e4968b0d76ff4f7f8395450c325d66)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_key": api_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''An API key for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-apikeycredential.html#cfn-appfabric-appauthorization-apikeycredential-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiKeyCredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnAppAuthorization.CredentialProperty",
        jsii_struct_bases=[],
        name_mapping={
            "api_key_credential": "apiKeyCredential",
            "oauth2_credential": "oauth2Credential",
        },
    )
    class CredentialProperty:
        def __init__(
            self,
            *,
            api_key_credential: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppAuthorization.ApiKeyCredentialProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            oauth2_credential: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppAuthorization.Oauth2CredentialProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains credential information for the application.

            :param api_key_credential: Contains API key credential information.
            :param oauth2_credential: Contains OAuth2 client credential information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-credential.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                credential_property = appfabric.CfnAppAuthorization.CredentialProperty(
                    api_key_credential=appfabric.CfnAppAuthorization.ApiKeyCredentialProperty(
                        api_key="apiKey"
                    ),
                    oauth2_credential=appfabric.CfnAppAuthorization.Oauth2CredentialProperty(
                        client_id="clientId",
                        client_secret="clientSecret"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__84faeb75d6298bf9948011d4db0b72e5ebe75349e74e39c838cc7771b029f6de)
                check_type(argname="argument api_key_credential", value=api_key_credential, expected_type=type_hints["api_key_credential"])
                check_type(argname="argument oauth2_credential", value=oauth2_credential, expected_type=type_hints["oauth2_credential"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_key_credential is not None:
                self._values["api_key_credential"] = api_key_credential
            if oauth2_credential is not None:
                self._values["oauth2_credential"] = oauth2_credential

        @builtins.property
        def api_key_credential(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.ApiKeyCredentialProperty"]]:
            '''Contains API key credential information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-credential.html#cfn-appfabric-appauthorization-credential-apikeycredential
            '''
            result = self._values.get("api_key_credential")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.ApiKeyCredentialProperty"]], result)

        @builtins.property
        def oauth2_credential(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.Oauth2CredentialProperty"]]:
            '''Contains OAuth2 client credential information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-credential.html#cfn-appfabric-appauthorization-credential-oauth2credential
            '''
            result = self._values.get("oauth2_credential")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.Oauth2CredentialProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnAppAuthorization.Oauth2CredentialProperty",
        jsii_struct_bases=[],
        name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
    )
    class Oauth2CredentialProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
        ) -> None:
            '''Contains OAuth2 client credential information.

            :param client_id: The client ID of the client application.
            :param client_secret: The client secret of the client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-oauth2credential.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                oauth2_credential_property = appfabric.CfnAppAuthorization.Oauth2CredentialProperty(
                    client_id="clientId",
                    client_secret="clientSecret"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__6e74f3fb472cabbe881a8e2243bef02c68261dadb95fd9741571a594ef06a75d)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }

        @builtins.property
        def client_id(self) -> builtins.str:
            '''The client ID of the client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-oauth2credential.html#cfn-appfabric-appauthorization-oauth2credential-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''The client secret of the client application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-oauth2credential.html#cfn-appfabric-appauthorization-oauth2credential-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Oauth2CredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnAppAuthorization.TenantProperty",
        jsii_struct_bases=[],
        name_mapping={
            "tenant_display_name": "tenantDisplayName",
            "tenant_identifier": "tenantIdentifier",
        },
    )
    class TenantProperty:
        def __init__(
            self,
            *,
            tenant_display_name: builtins.str,
            tenant_identifier: builtins.str,
        ) -> None:
            '''Contains information about an application tenant.

            :param tenant_display_name: The display name of the tenant.
            :param tenant_identifier: The ID of the application tenant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-tenant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                tenant_property = appfabric.CfnAppAuthorization.TenantProperty(
                    tenant_display_name="tenantDisplayName",
                    tenant_identifier="tenantIdentifier"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__8fa2478bf489d3a22216c2f91653582809acc357df17414cfac32c1472f970aa)
                check_type(argname="argument tenant_display_name", value=tenant_display_name, expected_type=type_hints["tenant_display_name"])
                check_type(argname="argument tenant_identifier", value=tenant_identifier, expected_type=type_hints["tenant_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "tenant_display_name": tenant_display_name,
                "tenant_identifier": tenant_identifier,
            }

        @builtins.property
        def tenant_display_name(self) -> builtins.str:
            '''The display name of the tenant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-tenant.html#cfn-appfabric-appauthorization-tenant-tenantdisplayname
            '''
            result = self._values.get("tenant_display_name")
            assert result is not None, "Required property 'tenant_display_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def tenant_identifier(self) -> builtins.str:
            '''The ID of the application tenant.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-appauthorization-tenant.html#cfn-appfabric-appauthorization-tenant-tenantidentifier
            '''
            result = self._values.get("tenant_identifier")
            assert result is not None, "Required property 'tenant_identifier' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TenantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_appfabric.CfnAppAuthorizationProps",
    jsii_struct_bases=[],
    name_mapping={
        "app": "app",
        "app_bundle_identifier": "appBundleIdentifier",
        "auth_type": "authType",
        "tenant": "tenant",
        "credential": "credential",
        "tags": "tags",
    },
)
class CfnAppAuthorizationProps:
    def __init__(
        self,
        *,
        app: builtins.str,
        app_bundle_identifier: builtins.str,
        auth_type: builtins.str,
        tenant: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppAuthorization.TenantProperty", typing.Dict[builtins.str, typing.Any]]],
        credential: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppAuthorization.CredentialProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAppAuthorization``.

        :param app: The name of the application.
        :param app_bundle_identifier: The Amazon Resource Name (ARN) or Universal Unique Identifier (UUID) of the app bundle to use for the request.
        :param auth_type: The authorization type.
        :param tenant: Contains information about an application tenant.
        :param credential: Contains credential information for the application.
        :param tags: Tags to apply to the app authorization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_appfabric as appfabric
            
            cfn_app_authorization_props = appfabric.CfnAppAuthorizationProps(
                app="app",
                app_bundle_identifier="appBundleIdentifier",
                auth_type="authType",
                tenant=appfabric.CfnAppAuthorization.TenantProperty(
                    tenant_display_name="tenantDisplayName",
                    tenant_identifier="tenantIdentifier"
                ),
            
                # the properties below are optional
                credential=appfabric.CfnAppAuthorization.CredentialProperty(
                    api_key_credential=appfabric.CfnAppAuthorization.ApiKeyCredentialProperty(
                        api_key="apiKey"
                    ),
                    oauth2_credential=appfabric.CfnAppAuthorization.Oauth2CredentialProperty(
                        client_id="clientId",
                        client_secret="clientSecret"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__388a6fb0339d38a0dafbb279f8d16f746564b5d7e13eae6116eaee441e1579d7)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument app_bundle_identifier", value=app_bundle_identifier, expected_type=type_hints["app_bundle_identifier"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument tenant", value=tenant, expected_type=type_hints["tenant"])
            check_type(argname="argument credential", value=credential, expected_type=type_hints["credential"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
            "app_bundle_identifier": app_bundle_identifier,
            "auth_type": auth_type,
            "tenant": tenant,
        }
        if credential is not None:
            self._values["credential"] = credential
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app(self) -> builtins.str:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html#cfn-appfabric-appauthorization-app
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_bundle_identifier(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) or Universal Unique Identifier (UUID) of the app bundle to use for the request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html#cfn-appfabric-appauthorization-appbundleidentifier
        '''
        result = self._values.get("app_bundle_identifier")
        assert result is not None, "Required property 'app_bundle_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''The authorization type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html#cfn-appfabric-appauthorization-authtype
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.TenantProperty"]:
        '''Contains information about an application tenant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html#cfn-appfabric-appauthorization-tenant
        '''
        result = self._values.get("tenant")
        assert result is not None, "Required property 'tenant' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.TenantProperty"], result)

    @builtins.property
    def credential(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.CredentialProperty"]]:
        '''Contains credential information for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html#cfn-appfabric-appauthorization-credential
        '''
        result = self._values.get("credential")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppAuthorization.CredentialProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to apply to the app authorization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-appauthorization.html#cfn-appfabric-appauthorization-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppAuthorizationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_appfabric_09bd86cb.IIngestionDestinationRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnIngestionDestination(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination",
):
    '''Creates an ingestion destination, which specifies how an application's ingested data is processed by Amazon Web Services AppFabric and where it's delivered.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html
    :cloudformationResource: AWS::AppFabric::IngestionDestination
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_appfabric as appfabric
        
        cfn_ingestion_destination = appfabric.CfnIngestionDestination(self, "MyCfnIngestionDestination",
            app_bundle_arn="appBundleArn",
            destination_configuration=appfabric.CfnIngestionDestination.DestinationConfigurationProperty(
                audit_log=appfabric.CfnIngestionDestination.AuditLogDestinationConfigurationProperty(
                    destination=appfabric.CfnIngestionDestination.DestinationProperty(
                        firehose_stream=appfabric.CfnIngestionDestination.FirehoseStreamProperty(
                            stream_name="streamName"
                        ),
                        s3_bucket=appfabric.CfnIngestionDestination.S3BucketProperty(
                            bucket_name="bucketName",
        
                            # the properties below are optional
                            prefix="prefix"
                        )
                    )
                )
            ),
            ingestion_arn="ingestionArn",
            processing_configuration=appfabric.CfnIngestionDestination.ProcessingConfigurationProperty(
                audit_log=appfabric.CfnIngestionDestination.AuditLogProcessingConfigurationProperty(
                    format="format",
                    schema="schema"
                )
            ),
        
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
        app_bundle_arn: builtins.str,
        destination_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ingestion_arn: builtins.str,
        processing_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppFabric::IngestionDestination``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param app_bundle_arn: The Amazon Resource Name (ARN) of the app bundle.
        :param destination_configuration: Contains information about the destination of ingested data.
        :param ingestion_arn: The Amazon Resource Name (ARN) of the ingestion.
        :param processing_configuration: Contains information about how ingested data is processed.
        :param tags: A map of the key-value pairs of the tag or tags to assign to the resource.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ae501bc58182dab91c5fee489eab8790640444e50d34466c6b64140a78f88b98)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIngestionDestinationProps(
            app_bundle_arn=app_bundle_arn,
            destination_configuration=destination_configuration,
            ingestion_arn=ingestion_arn,
            processing_configuration=processing_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForIngestionDestination")
    @builtins.classmethod
    def arn_for_ingestion_destination(
        cls,
        resource: "_aws_appfabric_09bd86cb.IIngestionDestinationRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7645490b621581569c4406465f19dc9e7723e98c31a914ff72575efe2834e306)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForIngestionDestination", [resource]))

    @jsii.member(jsii_name="isCfnIngestionDestination")
    @builtins.classmethod
    def is_cfn_ingestion_destination(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnIngestionDestination.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__67beb28d62c51d438281e9853942ea6aca72ab603860b1eda3eeb0ef504fb788)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnIngestionDestination", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__53921df123fb4875310687fca8fe945635df5b4420f0f19396b9948c771b6c34)
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
            type_hints = cached_type_hints(_typecheckingstub__cc87b1164694177642a0abdf8ae4b84c571eb0b9b449ea02ebda59949b101efd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ingestion destination.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp of when the ingestion destination was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The state of the ingestion destination.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp of when the ingestion destination was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

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
    @jsii.member(jsii_name="ingestionDestinationRef")
    def ingestion_destination_ref(
        self,
    ) -> "_aws_appfabric_09bd86cb.IngestionDestinationReference":
        '''A reference to a IngestionDestination resource.'''
        return typing.cast("_aws_appfabric_09bd86cb.IngestionDestinationReference", jsii.get(self, "ingestionDestinationRef"))

    @builtins.property
    @jsii.member(jsii_name="appBundleArn")
    def app_bundle_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the app bundle.'''
        return typing.cast(builtins.str, jsii.get(self, "appBundleArn"))

    @app_bundle_arn.setter
    def app_bundle_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d1b1e9dd7ac174bbf14b6a453db88d6d0fb66e0bfdc1a7977184b9132e5c00f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appBundleArn", value)

    @builtins.property
    @jsii.member(jsii_name="destinationConfiguration")
    def destination_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationConfigurationProperty"]:
        '''Contains information about the destination of ingested data.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationConfigurationProperty"], jsii.get(self, "destinationConfiguration"))

    @destination_configuration.setter
    def destination_configuration(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9f92ca8cba8051515fe759460c78aef780741ffeb4cf50ff221c337ee7570201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="ingestionArn")
    def ingestion_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ingestion.'''
        return typing.cast(builtins.str, jsii.get(self, "ingestionArn"))

    @ingestion_arn.setter
    def ingestion_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__62c65ca9cfead37d91c5466ba81571ddf04bc1dede1d674a36a32afff2d03ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestionArn", value)

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.ProcessingConfigurationProperty"]:
        '''Contains information about how ingested data is processed.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.ProcessingConfigurationProperty"], jsii.get(self, "processingConfiguration"))

    @processing_configuration.setter
    def processing_configuration(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.ProcessingConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b8a4b948db37f1ca07911973f0dfdccbd37aa54afb230d894b3df63867c84431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A map of the key-value pairs of the tag or tags to assign to the resource.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c168b802d78806313d2c0e9abfc17a5ceea98ed055723d074e27f1188e8b7885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.AuditLogDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination"},
    )
    class AuditLogDestinationConfigurationProperty:
        def __init__(
            self,
            *,
            destination: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.DestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Contains information about an audit log destination configuration.

            :param destination: Contains information about an audit log destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-auditlogdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                audit_log_destination_configuration_property = appfabric.CfnIngestionDestination.AuditLogDestinationConfigurationProperty(
                    destination=appfabric.CfnIngestionDestination.DestinationProperty(
                        firehose_stream=appfabric.CfnIngestionDestination.FirehoseStreamProperty(
                            stream_name="streamName"
                        ),
                        s3_bucket=appfabric.CfnIngestionDestination.S3BucketProperty(
                            bucket_name="bucketName",
                
                            # the properties below are optional
                            prefix="prefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__2b21664d03076a2c751f4fb77406d50c6b4239f4c7adf3848e68d021f975914e)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationProperty"]:
            '''Contains information about an audit log destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-auditlogdestinationconfiguration.html#cfn-appfabric-ingestiondestination-auditlogdestinationconfiguration-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuditLogDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.AuditLogProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"format": "format", "schema": "schema"},
    )
    class AuditLogProcessingConfigurationProperty:
        def __init__(self, *, format: builtins.str, schema: builtins.str) -> None:
            '''Contains information about an audit log processing configuration.

            :param format: The format in which the audit logs need to be formatted.
            :param schema: The event schema in which the audit logs need to be formatted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-auditlogprocessingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                audit_log_processing_configuration_property = appfabric.CfnIngestionDestination.AuditLogProcessingConfigurationProperty(
                    format="format",
                    schema="schema"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__87c37b144ce96638bd3daabc0c194aff3cc1c1d016a5ea2309d5bcb40353640b)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "format": format,
                "schema": schema,
            }

        @builtins.property
        def format(self) -> builtins.str:
            '''The format in which the audit logs need to be formatted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-auditlogprocessingconfiguration.html#cfn-appfabric-ingestiondestination-auditlogprocessingconfiguration-format
            '''
            result = self._values.get("format")
            assert result is not None, "Required property 'format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def schema(self) -> builtins.str:
            '''The event schema in which the audit logs need to be formatted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-auditlogprocessingconfiguration.html#cfn-appfabric-ingestiondestination-auditlogprocessingconfiguration-schema
            '''
            result = self._values.get("schema")
            assert result is not None, "Required property 'schema' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuditLogProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audit_log": "auditLog"},
    )
    class DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            audit_log: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.AuditLogDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Contains information about the destination of ingested data.

            :param audit_log: Contains information about an audit log destination configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                destination_configuration_property = appfabric.CfnIngestionDestination.DestinationConfigurationProperty(
                    audit_log=appfabric.CfnIngestionDestination.AuditLogDestinationConfigurationProperty(
                        destination=appfabric.CfnIngestionDestination.DestinationProperty(
                            firehose_stream=appfabric.CfnIngestionDestination.FirehoseStreamProperty(
                                stream_name="streamName"
                            ),
                            s3_bucket=appfabric.CfnIngestionDestination.S3BucketProperty(
                                bucket_name="bucketName",
                
                                # the properties below are optional
                                prefix="prefix"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__a8cf2ac4ab85207ce46e3368243cab97cb5145d298b7738e6ca2b16946179e09)
                check_type(argname="argument audit_log", value=audit_log, expected_type=type_hints["audit_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "audit_log": audit_log,
            }

        @builtins.property
        def audit_log(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.AuditLogDestinationConfigurationProperty"]:
            '''Contains information about an audit log destination configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-destinationconfiguration.html#cfn-appfabric-ingestiondestination-destinationconfiguration-auditlog
            '''
            result = self._values.get("audit_log")
            assert result is not None, "Required property 'audit_log' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.AuditLogDestinationConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"firehose_stream": "firehoseStream", "s3_bucket": "s3Bucket"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            firehose_stream: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.FirehoseStreamProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_bucket: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.S3BucketProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about an audit log destination.

            :param firehose_stream: Contains information about an Amazon Kinesis Data Firehose delivery stream.
            :param s3_bucket: Contains information about an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                destination_property = appfabric.CfnIngestionDestination.DestinationProperty(
                    firehose_stream=appfabric.CfnIngestionDestination.FirehoseStreamProperty(
                        stream_name="streamName"
                    ),
                    s3_bucket=appfabric.CfnIngestionDestination.S3BucketProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__9cbbbf5e2fad49f50257e8a0c35c5b9ab89b77f61dc98394599c5ebb9ee13ef1)
                check_type(argname="argument firehose_stream", value=firehose_stream, expected_type=type_hints["firehose_stream"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if firehose_stream is not None:
                self._values["firehose_stream"] = firehose_stream
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket

        @builtins.property
        def firehose_stream(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.FirehoseStreamProperty"]]:
            '''Contains information about an Amazon Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-destination.html#cfn-appfabric-ingestiondestination-destination-firehosestream
            '''
            result = self._values.get("firehose_stream")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.FirehoseStreamProperty"]], result)

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.S3BucketProperty"]]:
            '''Contains information about an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-destination.html#cfn-appfabric-ingestiondestination-destination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.S3BucketProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.FirehoseStreamProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName"},
    )
    class FirehoseStreamProperty:
        def __init__(self, *, stream_name: builtins.str) -> None:
            '''Contains information about an Amazon Kinesis Data Firehose delivery stream.

            :param stream_name: The name of the Amazon Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-firehosestream.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                firehose_stream_property = appfabric.CfnIngestionDestination.FirehoseStreamProperty(
                    stream_name="streamName"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__8f8ce3be19df0dc3ebbe51e81ddb02f1bf4395983987772d6c3600c415544a9a)
                check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_name": stream_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''The name of the Amazon Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-firehosestream.html#cfn-appfabric-ingestiondestination-firehosestream-streamname
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseStreamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.ProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"audit_log": "auditLog"},
    )
    class ProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            audit_log: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.AuditLogProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Contains information about how ingested data is processed.

            :param audit_log: Contains information about an audit log processing configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-processingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                processing_configuration_property = appfabric.CfnIngestionDestination.ProcessingConfigurationProperty(
                    audit_log=appfabric.CfnIngestionDestination.AuditLogProcessingConfigurationProperty(
                        format="format",
                        schema="schema"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__3f9c0fd952ed901182ce981a4a8e44882429afce16b3e1e46587ba61c448c1d0)
                check_type(argname="argument audit_log", value=audit_log, expected_type=type_hints["audit_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "audit_log": audit_log,
            }

        @builtins.property
        def audit_log(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.AuditLogProcessingConfigurationProperty"]:
            '''Contains information about an audit log processing configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-processingconfiguration.html#cfn-appfabric-ingestiondestination-processingconfiguration-auditlog
            '''
            result = self._values.get("audit_log")
            assert result is not None, "Required property 'audit_log' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.AuditLogProcessingConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestination.S3BucketProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
    )
    class S3BucketProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an Amazon S3 bucket.

            :param bucket_name: The name of the Amazon S3 bucket.
            :param prefix: The object key to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-s3bucket.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_appfabric as appfabric
                
                s3_bucket_property = appfabric.CfnIngestionDestination.S3BucketProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__98afc4156c1b0f187f1def3a8200c66bef745632e8d6b79f6a9495b63ecde775)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The name of the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-s3bucket.html#cfn-appfabric-ingestiondestination-s3bucket-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The object key to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appfabric-ingestiondestination-s3bucket.html#cfn-appfabric-ingestiondestination-s3bucket-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_appfabric.CfnIngestionDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_bundle_arn": "appBundleArn",
        "destination_configuration": "destinationConfiguration",
        "ingestion_arn": "ingestionArn",
        "processing_configuration": "processingConfiguration",
        "tags": "tags",
    },
)
class CfnIngestionDestinationProps:
    def __init__(
        self,
        *,
        app_bundle_arn: builtins.str,
        destination_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ingestion_arn: builtins.str,
        processing_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnIngestionDestination.ProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnIngestionDestination``.

        :param app_bundle_arn: The Amazon Resource Name (ARN) of the app bundle.
        :param destination_configuration: Contains information about the destination of ingested data.
        :param ingestion_arn: The Amazon Resource Name (ARN) of the ingestion.
        :param processing_configuration: Contains information about how ingested data is processed.
        :param tags: A map of the key-value pairs of the tag or tags to assign to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_appfabric as appfabric
            
            cfn_ingestion_destination_props = appfabric.CfnIngestionDestinationProps(
                app_bundle_arn="appBundleArn",
                destination_configuration=appfabric.CfnIngestionDestination.DestinationConfigurationProperty(
                    audit_log=appfabric.CfnIngestionDestination.AuditLogDestinationConfigurationProperty(
                        destination=appfabric.CfnIngestionDestination.DestinationProperty(
                            firehose_stream=appfabric.CfnIngestionDestination.FirehoseStreamProperty(
                                stream_name="streamName"
                            ),
                            s3_bucket=appfabric.CfnIngestionDestination.S3BucketProperty(
                                bucket_name="bucketName",
            
                                # the properties below are optional
                                prefix="prefix"
                            )
                        )
                    )
                ),
                ingestion_arn="ingestionArn",
                processing_configuration=appfabric.CfnIngestionDestination.ProcessingConfigurationProperty(
                    audit_log=appfabric.CfnIngestionDestination.AuditLogProcessingConfigurationProperty(
                        format="format",
                        schema="schema"
                    )
                ),
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7c8e3d8056274d5a562bb923d805c164d97a0aa5bed801619798ec4ad809907b)
            check_type(argname="argument app_bundle_arn", value=app_bundle_arn, expected_type=type_hints["app_bundle_arn"])
            check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
            check_type(argname="argument ingestion_arn", value=ingestion_arn, expected_type=type_hints["ingestion_arn"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_bundle_arn": app_bundle_arn,
            "destination_configuration": destination_configuration,
            "ingestion_arn": ingestion_arn,
            "processing_configuration": processing_configuration,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_bundle_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the app bundle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html#cfn-appfabric-ingestiondestination-appbundlearn
        '''
        result = self._values.get("app_bundle_arn")
        assert result is not None, "Required property 'app_bundle_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationConfigurationProperty"]:
        '''Contains information about the destination of ingested data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html#cfn-appfabric-ingestiondestination-destinationconfiguration
        '''
        result = self._values.get("destination_configuration")
        assert result is not None, "Required property 'destination_configuration' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.DestinationConfigurationProperty"], result)

    @builtins.property
    def ingestion_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ingestion.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html#cfn-appfabric-ingestiondestination-ingestionarn
        '''
        result = self._values.get("ingestion_arn")
        assert result is not None, "Required property 'ingestion_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.ProcessingConfigurationProperty"]:
        '''Contains information about how ingested data is processed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html#cfn-appfabric-ingestiondestination-processingconfiguration
        '''
        result = self._values.get("processing_configuration")
        assert result is not None, "Required property 'processing_configuration' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnIngestionDestination.ProcessingConfigurationProperty"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A map of the key-value pairs of the tag or tags to assign to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appfabric-ingestiondestination.html#cfn-appfabric-ingestiondestination-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIngestionDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAppAuthorization",
    "CfnAppAuthorizationProps",
    "CfnIngestionDestination",
    "CfnIngestionDestinationProps",
]

publication.publish()

def _typecheckingstub__e12909d0c7ca35d743d93519a7d4405f3120d32c5a26e6f239eaca61d1ef5a44(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: builtins.str,
    app_bundle_identifier: builtins.str,
    auth_type: builtins.str,
    tenant: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppAuthorization.TenantProperty, typing.Dict[builtins.str, typing.Any]]],
    credential: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppAuthorization.CredentialProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce115e88f391c1771b6f6a929951c75a05f3393dbc4e25aac30a65891885fb3(
    resource: _aws_appfabric_09bd86cb.IAppAuthorizationRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b165b7cd6fcdbbbecc8ecf3c4f9f3d19744619ef2cfdcea27e0d4664145cfc1e(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d52289e4d0efa512b5d0361547375936d4c2d7427eab6ede50e448cc3aefe46(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0ddada5f0bb35cc5ee33b676284e95b652f112aeb3de6441898446e0da3e52(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af75cefc1eac3043e9595b2871148ae23ff4c53db801ed09e9f46abe7b5cf124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b6984a49d513d9f5e4f015dea43ab391f055cede9af681b7a1b15a88d0716e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d7476f9181c3e9c2a407648bbfde2a42d8da9d241bde4a857bdafd2a29827e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c4193ac61adbc5dd44c570222434a7c62d8eefa41efaa28dd2351284e14308(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnAppAuthorization.TenantProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe8e050a5434452f52e90d67f54b3bccec37eb061b6f9b2bc5384a1c252f6e0(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnAppAuthorization.CredentialProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebf4f36e4e4db8e95130058fa75e4a1352483f135485b1748fa18956fbdf150(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d2c3224c6ad552e4e46080b761e62579e4968b0d76ff4f7f8395450c325d66(
    *,
    api_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84faeb75d6298bf9948011d4db0b72e5ebe75349e74e39c838cc7771b029f6de(
    *,
    api_key_credential: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppAuthorization.ApiKeyCredentialProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    oauth2_credential: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppAuthorization.Oauth2CredentialProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e74f3fb472cabbe881a8e2243bef02c68261dadb95fd9741571a594ef06a75d(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa2478bf489d3a22216c2f91653582809acc357df17414cfac32c1472f970aa(
    *,
    tenant_display_name: builtins.str,
    tenant_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388a6fb0339d38a0dafbb279f8d16f746564b5d7e13eae6116eaee441e1579d7(
    *,
    app: builtins.str,
    app_bundle_identifier: builtins.str,
    auth_type: builtins.str,
    tenant: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppAuthorization.TenantProperty, typing.Dict[builtins.str, typing.Any]]],
    credential: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppAuthorization.CredentialProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae501bc58182dab91c5fee489eab8790640444e50d34466c6b64140a78f88b98(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_bundle_arn: builtins.str,
    destination_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    ingestion_arn: builtins.str,
    processing_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7645490b621581569c4406465f19dc9e7723e98c31a914ff72575efe2834e306(
    resource: _aws_appfabric_09bd86cb.IIngestionDestinationRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67beb28d62c51d438281e9853942ea6aca72ab603860b1eda3eeb0ef504fb788(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53921df123fb4875310687fca8fe945635df5b4420f0f19396b9948c771b6c34(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc87b1164694177642a0abdf8ae4b84c571eb0b9b449ea02ebda59949b101efd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b1e9dd7ac174bbf14b6a453db88d6d0fb66e0bfdc1a7977184b9132e5c00f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f92ca8cba8051515fe759460c78aef780741ffeb4cf50ff221c337ee7570201(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnIngestionDestination.DestinationConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c65ca9cfead37d91c5466ba81571ddf04bc1dede1d674a36a32afff2d03ac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a4b948db37f1ca07911973f0dfdccbd37aa54afb230d894b3df63867c84431(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnIngestionDestination.ProcessingConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c168b802d78806313d2c0e9abfc17a5ceea98ed055723d074e27f1188e8b7885(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b21664d03076a2c751f4fb77406d50c6b4239f4c7adf3848e68d021f975914e(
    *,
    destination: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.DestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c37b144ce96638bd3daabc0c194aff3cc1c1d016a5ea2309d5bcb40353640b(
    *,
    format: builtins.str,
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cf2ac4ab85207ce46e3368243cab97cb5145d298b7738e6ca2b16946179e09(
    *,
    audit_log: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.AuditLogDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbbbf5e2fad49f50257e8a0c35c5b9ab89b77f61dc98394599c5ebb9ee13ef1(
    *,
    firehose_stream: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.FirehoseStreamProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_bucket: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.S3BucketProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8ce3be19df0dc3ebbe51e81ddb02f1bf4395983987772d6c3600c415544a9a(
    *,
    stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9c0fd952ed901182ce981a4a8e44882429afce16b3e1e46587ba61c448c1d0(
    *,
    audit_log: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.AuditLogProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98afc4156c1b0f187f1def3a8200c66bef745632e8d6b79f6a9495b63ecde775(
    *,
    bucket_name: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8e3d8056274d5a562bb923d805c164d97a0aa5bed801619798ec4ad809907b(
    *,
    app_bundle_arn: builtins.str,
    destination_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    ingestion_arn: builtins.str,
    processing_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnIngestionDestination.ProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
