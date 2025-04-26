r'''
# Amazon Cognito Identity Pool Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to `aws-cdk-lib/aws-cognito-identitypool`.

> **Identity Pools are in a separate module while the API is being stabilized. Once we stabilize the module, they will**
> **be included into the stable [aws-cognito](../aws-cognito) library. Please provide feedback on this experience by**
> **creating an [issue here](https://github.com/aws/aws-cdk/issues/new/choose)**

[Amazon Cognito Identity Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html) enable you to grant your users access to other AWS services.

Identity Pools are one of the two main components of [Amazon Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html), which provides authentication, authorization, and
user management for your web and mobile apps. Your users can sign in through a a trusted identity provider, like a user
pool or a SAML 2.0 service, as well as with third party providers such as Facebook, Amazon, Google or Apple.

The other main component in Amazon Cognito is [user pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html). User Pools are user directories that provide sign-up and
sign-in options for your app users.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
from aws_cdk.aws_cognito_identitypool_alpha import IdentityPool, UserPoolAuthenticationProvider
```

## Table of Contents

* [Identity Pools](#identity-pools)

  * [Authenticated and Unauthenticated Identities](#authenticated-and-unauthenticated-identities)
  * [Authentication Providers](#authentication-providers)

    * [User Pool Authentication Provider](#user-pool-authentication-provider)
    * [Server Side Token Check](#server-side-token-check)
    * [Associating an External Provider Directly](#associating-an-external-provider-directly)
    * [OpenIdConnect and Saml](#openid-connect-and-saml)
    * [Custom Providers](#custom-providers)
  * [Role Mapping](#role-mapping)

    * [Provider Urls](#provider-urls)
  * [Authentication Flow](#authentication-flow)
  * [Cognito Sync](#cognito-sync)
  * [Importing Identity Pools](#importing-identity-pools)

## Identity Pools

Identity pools provide temporary AWS credentials for users who are guests (unauthenticated) and for users who have
authenticated by presenting a token from another identity provider. An identity pool is a store of user identity data
specific to an account.

Identity pools can be used in conjunction with Cognito User Pools or by accessing external federated identity providers
directly. Learn more at [Amazon Cognito Identity Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html).

### Authenticated and Unauthenticated Identities

Identity pools define two types of identities: authenticated(`user`) and unauthenticated (`guest`). Every identity in
an identity pool is either authenticated or unauthenticated. Each identity pool has a default role for authenticated
identities, and a default role for unauthenticated identities. Absent other overriding rules (see below), these are the
roles that will be assumed by the corresponding users in the authentication process.

A basic Identity Pool with minimal configuration has no required props, with default authenticated (user) and
unauthenticated (guest) roles applied to the identity pool:

```python
IdentityPool(self, "myIdentityPool")
```

By default, both the authenticated and unauthenticated roles will have no permissions attached. When granting permissions,
you should ensure that you are granting the least privileged permissions required for your use case. Grant permissions
to roles using the public `authenticatedRole` and `unauthenticatedRole` properties:

```python
import aws_cdk.aws_dynamodb as dynamodb
# table: dynamodb.Table


identity_pool = IdentityPool(self, "myIdentityPool")

# Grant permissions to authenticated users
table.grant_read_write_data(identity_pool.authenticated_role)
# Grant permissions to unauthenticated guest users
table.grant_read_data(identity_pool.unauthenticated_role)

# Or add policy statements straight to the role
identity_pool.authenticated_role.add_to_principal_policy(iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["dynamodb:UpdateItem"],
    resources=[table.table_arn]
))
```

The default roles can also be supplied in `IdentityPoolProps`:

```python
stack = Stack()
authenticated_role = iam.Role(self, "authRole",
    assumed_by=iam.ServicePrincipal("service.amazonaws.com")
)
unauthenticated_role = iam.Role(self, "unauthRole",
    assumed_by=iam.ServicePrincipal("service.amazonaws.com")
)
identity_pool = IdentityPool(self, "TestIdentityPoolActions",
    authenticated_role=authenticated_role,
    unauthenticated_role=unauthenticated_role
)
```

### Authentication Providers

Authenticated identities belong to users who are authenticated by a public login provider (Amazon Cognito user pools,
Login with Amazon, Sign in with Apple, Facebook, Google, SAML, or any OpenID Connect Providers) or a developer provider
(your own backend authentication process).

[Authentication providers](https://docs.aws.amazon.com/cognito/latest/developerguide/external-identity-providers.html) can be associated with an Identity Pool by first associating them with a Cognito User Pool or by
associating the provider directly with the identity pool.

#### User Pool Authentication Provider

In order to attach a user pool to an identity pool as an authentication provider, the identity pool needs properties
from both the user pool and the user pool client. For this reason identity pools use a `UserPoolAuthenticationProvider`
to gather the necessary properties from the user pool constructs.

```python
user_pool = cognito.UserPool(self, "Pool")

IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    authentication_providers=IdentityPoolAuthenticationProviders(
        user_pools=[UserPoolAuthenticationProvider(user_pool=user_pool)]
    )
)
```

User pools can also be associated with an identity pool after instantiation. The Identity Pool's `addUserPoolAuthentication` method
returns the User Pool Client that has been created:

```python
# identity_pool: IdentityPool

user_pool = cognito.UserPool(self, "Pool")
user_pool_client = identity_pool.add_user_pool_authentication(UserPoolAuthenticationProvider(
    user_pool=user_pool
))
```

#### Server Side Token Check

With the `IdentityPool` CDK Construct, by default the pool is configured to check with the integrated user pools to
make sure that the user has not been globally signed out or deleted before the identity pool provides an OIDC token or
AWS credentials for the user.

If the user is signed out or deleted, the identity pool will return a 400 Not Authorized error. This setting can be
disabled, however, in several ways.

Setting `disableServerSideTokenCheck` to true will change the default behavior to no server side token check. Learn
more [here](https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_CognitoIdentityProvider.html#CognitoIdentity-Type-CognitoIdentityProvider-ServerSideTokenCheck):

```python
# identity_pool: IdentityPool

user_pool = cognito.UserPool(self, "Pool")
identity_pool.add_user_pool_authentication(UserPoolAuthenticationProvider(
    user_pool=user_pool,
    disable_server_side_token_check=True
))
```

#### Associating an External Provider Directly

One or more [external identity providers](https://docs.aws.amazon.com/cognito/latest/developerguide/external-identity-providers.html) can be associated with an identity pool directly using
`authenticationProviders`:

```python
IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    authentication_providers=IdentityPoolAuthenticationProviders(
        amazon=IdentityPoolAmazonLoginProvider(
            app_id="amzn1.application.12312k3j234j13rjiwuenf"
        ),
        facebook=IdentityPoolFacebookLoginProvider(
            app_id="1234567890123"
        ),
        google=IdentityPoolGoogleLoginProvider(
            client_id="12345678012.apps.googleusercontent.com"
        ),
        apple=IdentityPoolAppleLoginProvider(
            services_id="com.myappleapp.auth"
        ),
        twitter=IdentityPoolTwitterLoginProvider(
            consumer_key="my-twitter-id",
            consumer_secret="my-twitter-secret"
        )
    )
)
```

To associate more than one provider of the same type with the identity pool, use User
Pools, OpenIdConnect, or SAML. Only one provider per external service can be attached directly to the identity pool.

#### OpenId Connect and Saml

[OpenID Connect](https://docs.aws.amazon.com/cognito/latest/developerguide/open-id.html) is an open standard for
authentication that is supported by a number of login providers. Amazon Cognito supports linking of identities with
OpenID Connect providers that are configured through [AWS Identity and Access Management](http://aws.amazon.com/iam/).

An identity provider that supports [Security Assertion Markup Language 2.0 (SAML 2.0)](https://docs.aws.amazon.com/cognito/latest/developerguide/saml-identity-provider.html) can be used to provide a simple
onboarding flow for users. The SAML-supporting identity provider specifies the IAM roles that can be assumed by users
so that different users can be granted different sets of permissions. Associating an OpenId Connect or Saml provider
with an identity pool:

```python
# open_id_connect_provider: iam.OpenIdConnectProvider
# saml_provider: iam.SamlProvider


IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    authentication_providers=IdentityPoolAuthenticationProviders(
        open_id_connect_providers=[open_id_connect_provider],
        saml_providers=[saml_provider]
    )
)
```

#### Custom Providers

The identity pool's behavior can be customized further using custom [developer authenticated identities](https://docs.aws.amazon.com/cognito/latest/developerguide/developer-authenticated-identities.html).
With developer authenticated identities, users can be registered and authenticated via an existing authentication
process while still using Amazon Cognito to synchronize user data and access AWS resources.

Like the supported external providers, though, only one custom provider can be directly associated with the identity
pool.

```python
# open_id_connect_provider: iam.OpenIdConnectProvider

IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    authentication_providers=IdentityPoolAuthenticationProviders(
        google=IdentityPoolGoogleLoginProvider(
            client_id="12345678012.apps.googleusercontent.com"
        ),
        open_id_connect_providers=[open_id_connect_provider],
        custom_provider="my-custom-provider.example.com"
    )
)
```

### Role Mapping

In addition to setting default roles for authenticated and unauthenticated users, identity pools can also be used to
define rules to choose the role for each user based on claims in the user's ID token by using Role Mapping. When using
role mapping, it's important to be aware of some of the permissions the role will need, and that the least privileged
roles necessary are given for your specific use case. An in depth
review of roles and role mapping can be found [here](https://docs.aws.amazon.com/cognito/latest/developerguide/role-based-access-control.html).

Using a [token-based approach](https://docs.aws.amazon.com/cognito/latest/developerguide/role-based-access-control.html#using-tokens-to-assign-roles-to-users) to role mapping will allow mapped roles to be passed through the `cognito:roles` or
`cognito:preferred_role` claims from the identity provider:

```python
from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl


IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    role_mappings=[IdentityPoolRoleMapping(
        provider_url=IdentityPoolProviderUrl.AMAZON,
        use_token=True
    )]
)
```

Using a rule-based approach to role mapping allows roles to be assigned based on custom claims passed from the identity provider:

```python
from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl, RoleMappingMatchType

# admin_role: iam.Role
# non_admin_role: iam.Role

IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    # Assign specific roles to users based on whether or not the custom admin claim is passed from the identity provider
    role_mappings=[IdentityPoolRoleMapping(
        provider_url=IdentityPoolProviderUrl.AMAZON,
        rules=[RoleMappingRule(
            claim="custom:admin",
            claim_value="admin",
            mapped_role=admin_role
        ), RoleMappingRule(
            claim="custom:admin",
            claim_value="admin",
            match_type=RoleMappingMatchType.NOTEQUAL,
            mapped_role=non_admin_role
        )
        ]
    )]
)
```

#### Provider Urls

Role mappings must be associated with the url of an Identity Provider which can be supplied
`IdentityPoolProviderUrl`. Supported Providers have static Urls that can be used:

```python
from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl


IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    role_mappings=[IdentityPoolRoleMapping(
        provider_url=IdentityPoolProviderUrl.FACEBOOK,
        use_token=True
    )]
)
```

For identity providers that don't have static Urls, a custom Url can be supplied:

```python
from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl


IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    role_mappings=[IdentityPoolRoleMapping(
        provider_url=IdentityPoolProviderUrl.custom("my-custom-provider.com"),
        use_token=True
    )
    ]
)
```

If a provider URL is a CDK Token, as it will be if you are trying to use a previously defined Cognito User Pool, you will need to also provide a mappingKey.
This is because by default, the key in the Cloudformation role mapping hash is the providerUrl, and Cloudformation map keys must be concrete strings, they
cannot be references. For example:

```python
from aws_cdk.aws_cognito import UserPool, UserPoolClient
from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl

# user_pool: UserPool
# user_pool_client: UserPoolClient

IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    role_mappings=[IdentityPoolRoleMapping(
        mapping_key="cognito",
        provider_url=IdentityPoolProviderUrl.user_pool(user_pool, user_pool_client),
        use_token=True
    )]
)
```

See [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypoolroleattachment-rolemapping.html#cfn-cognito-identitypoolroleattachment-rolemapping-identityprovider) for more information.

### Authentication Flow

Identity Pool [Authentication Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/authentication-flow.html) defaults to the enhanced, simplified flow. The Classic (basic) Authentication Flow
can also be implemented using `allowClassicFlow`:

```python
IdentityPool(self, "myidentitypool",
    identity_pool_name="myidentitypool",
    allow_classic_flow=True
)
```

### Cognito Sync

It's now recommended to integrate [AWS AppSync](https://aws.amazon.com/appsync/) for synchronizing app data across devices, so
Cognito Sync features like `PushSync`, `CognitoEvents`, and `CognitoStreams` are not a part of `IdentityPool`. More
information can be found [here](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sync.html).

### Importing Identity Pools

You can import existing identity pools into your stack using Identity Pool static methods with the Identity Pool Id or
Arn:

```python
IdentityPool.from_identity_pool_id(self, "my-imported-identity-pool", "us-east-1:dj2823ryiwuhef937")
IdentityPool.from_identity_pool_arn(self, "my-imported-identity-pool", "arn:aws:cognito-identity:us-east-1:123456789012:identitypool/us-east-1:dj2823ryiwuhef937")
```
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cognito as _aws_cdk_aws_cognito_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IIdentityPool")
class IIdentityPool(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(deprecated) Represents a Cognito Identity Pool.

    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="identityPoolArn")
    def identity_pool_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the Identity Pool.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        '''(deprecated) The ID of the Identity Pool in the format REGION:GUID.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="identityPoolName")
    def identity_pool_name(self) -> builtins.str:
        '''(deprecated) Name of the Identity Pool.

        :stability: deprecated
        :attribute: true
        '''
        ...


class _IIdentityPoolProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(deprecated) Represents a Cognito Identity Pool.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito-identitypool-alpha.IIdentityPool"

    @builtins.property
    @jsii.member(jsii_name="identityPoolArn")
    def identity_pool_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the Identity Pool.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolArn"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        '''(deprecated) The ID of the Identity Pool in the format REGION:GUID.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolName")
    def identity_pool_name(self) -> builtins.str:
        '''(deprecated) Name of the Identity Pool.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIdentityPool).__jsii_proxy_class__ = lambda : _IIdentityPoolProxy


@jsii.interface(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IUserPoolAuthenticationProvider"
)
class IUserPoolAuthenticationProvider(typing_extensions.Protocol):
    '''(deprecated) Represents the concept of a User Pool Authentication Provider.

    You use user pool authentication providers to configure User Pools
    and User Pool Clients for use with Identity Pools

    :stability: deprecated
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        identity_pool: IIdentityPool,
    ) -> "UserPoolAuthenticationProviderBindConfig":
        '''(deprecated) The method called when a given User Pool Authentication Provider is added (for the first time) to an Identity Pool.

        :param scope: -
        :param identity_pool: -

        :stability: deprecated
        '''
        ...


class _IUserPoolAuthenticationProviderProxy:
    '''(deprecated) Represents the concept of a User Pool Authentication Provider.

    You use user pool authentication providers to configure User Pools
    and User Pool Clients for use with Identity Pools

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cognito-identitypool-alpha.IUserPoolAuthenticationProvider"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        identity_pool: IIdentityPool,
    ) -> "UserPoolAuthenticationProviderBindConfig":
        '''(deprecated) The method called when a given User Pool Authentication Provider is added (for the first time) to an Identity Pool.

        :param scope: -
        :param identity_pool: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07632ef1025feb6e05894b02941c351317dc03c46357f2c76f22433d4b28396c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument identity_pool", value=identity_pool, expected_type=type_hints["identity_pool"])
        options = UserPoolAuthenticationProviderBindOptions()

        return typing.cast("UserPoolAuthenticationProviderBindConfig", jsii.invoke(self, "bind", [scope, identity_pool, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUserPoolAuthenticationProvider).__jsii_proxy_class__ = lambda : _IUserPoolAuthenticationProviderProxy


@jsii.implements(IIdentityPool)
class IdentityPool(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPool",
):
    '''(deprecated) Define a Cognito Identity Pool.

    :stability: deprecated
    :resource: AWS::Cognito::IdentityPool
    :exampleMetadata: infused

    Example::

        # open_id_connect_provider: iam.OpenIdConnectProvider
        
        IdentityPool(self, "myidentitypool",
            identity_pool_name="myidentitypool",
            authentication_providers=IdentityPoolAuthenticationProviders(
                google=IdentityPoolGoogleLoginProvider(
                    client_id="12345678012.apps.googleusercontent.com"
                ),
                open_id_connect_providers=[open_id_connect_provider],
                custom_provider="my-custom-provider.example.com"
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_classic_flow: typing.Optional[builtins.bool] = None,
        allow_unauthenticated_identities: typing.Optional[builtins.bool] = None,
        authenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        authentication_providers: typing.Optional[typing.Union["IdentityPoolAuthenticationProviders", typing.Dict[builtins.str, typing.Any]]] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        role_mappings: typing.Optional[typing.Sequence[typing.Union["IdentityPoolRoleMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
        unauthenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_classic_flow: (deprecated) Enables the Basic (Classic) authentication flow. Default: - Classic Flow not allowed
        :param allow_unauthenticated_identities: (deprecated) Whether the Identity Pool supports unauthenticated logins. Default: - false
        :param authenticated_role: (deprecated) The default Role to be assumed by authenticated users. Default: - A default authenticated Role will be added
        :param authentication_providers: (deprecated) Authentication Providers for using in Identity Pool. Default: - No Authentication Providers passed directly to Identity Pool
        :param identity_pool_name: (deprecated) The name of the Identity Pool. Default: - Automatically generated name by CloudFormation at deploy time
        :param role_mappings: (deprecated) Rules for mapping roles to users. Default: - no role mappings
        :param unauthenticated_role: (deprecated) The default Role to be assumed by unauthenticated users. Default: - A default unauthenticated Role will be added

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2f072d5cac259fbc65a0c4a6a8cb785ff9ebcf2da91f9184be84a22820a980)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IdentityPoolProps(
            allow_classic_flow=allow_classic_flow,
            allow_unauthenticated_identities=allow_unauthenticated_identities,
            authenticated_role=authenticated_role,
            authentication_providers=authentication_providers,
            identity_pool_name=identity_pool_name,
            role_mappings=role_mappings,
            unauthenticated_role=unauthenticated_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromIdentityPoolArn")
    @builtins.classmethod
    def from_identity_pool_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        identity_pool_arn: builtins.str,
    ) -> IIdentityPool:
        '''(deprecated) Import an existing Identity Pool from its ARN.

        :param scope: -
        :param id: -
        :param identity_pool_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95e191d26141b46fee8d2cdcabc0803b18860942f1a248701db0dae81123def)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_pool_arn", value=identity_pool_arn, expected_type=type_hints["identity_pool_arn"])
        return typing.cast(IIdentityPool, jsii.sinvoke(cls, "fromIdentityPoolArn", [scope, id, identity_pool_arn]))

    @jsii.member(jsii_name="fromIdentityPoolId")
    @builtins.classmethod
    def from_identity_pool_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        identity_pool_id: builtins.str,
    ) -> IIdentityPool:
        '''(deprecated) Import an existing Identity Pool from its ID.

        :param scope: -
        :param id: -
        :param identity_pool_id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5abb9f2926d1e1f17a15fd6b4211f8951279c31ec22f381103f75200b458fa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
        return typing.cast(IIdentityPool, jsii.sinvoke(cls, "fromIdentityPoolId", [scope, id, identity_pool_id]))

    @jsii.member(jsii_name="addUserPoolAuthentication")
    def add_user_pool_authentication(
        self,
        user_pool: IUserPoolAuthenticationProvider,
    ) -> None:
        '''(deprecated) Add a User Pool to the Identity Pool and configure the User Pool client to handle identities.

        :param user_pool: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd9ea8a4c738095932e3cf624c6eb098117704692279323d27952d6b2df0e00)
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
        return typing.cast(None, jsii.invoke(self, "addUserPoolAuthentication", [user_pool]))

    @builtins.property
    @jsii.member(jsii_name="authenticatedRole")
    def authenticated_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(deprecated) Default Role for authenticated users.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "authenticatedRole"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolArn")
    def identity_pool_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the Identity Pool.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolArn"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        '''(deprecated) The ID of the Identity Pool in the format REGION:GUID.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolName")
    def identity_pool_name(self) -> builtins.str:
        '''(deprecated) The name of the Identity Pool.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityPoolName"))

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedRole")
    def unauthenticated_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(deprecated) Default Role for unauthenticated users.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "unauthenticatedRole"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolAmazonLoginProvider",
    jsii_struct_bases=[],
    name_mapping={"app_id": "appId"},
)
class IdentityPoolAmazonLoginProvider:
    def __init__(self, *, app_id: builtins.str) -> None:
        '''(deprecated) Login Provider for identity federation using Amazon credentials.

        :param app_id: (deprecated) App ID for Amazon identity federation.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    amazon=IdentityPoolAmazonLoginProvider(
                        app_id="amzn1.application.12312k3j234j13rjiwuenf"
                    ),
                    facebook=IdentityPoolFacebookLoginProvider(
                        app_id="1234567890123"
                    ),
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    apple=IdentityPoolAppleLoginProvider(
                        services_id="com.myappleapp.auth"
                    ),
                    twitter=IdentityPoolTwitterLoginProvider(
                        consumer_key="my-twitter-id",
                        consumer_secret="my-twitter-secret"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e283aa49d3946357252123279fe3e514c02786d6dbaf36c03180cb06444fd8)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
        }

    @builtins.property
    def app_id(self) -> builtins.str:
        '''(deprecated) App ID for Amazon identity federation.

        :stability: deprecated
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolAmazonLoginProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolAppleLoginProvider",
    jsii_struct_bases=[],
    name_mapping={"services_id": "servicesId"},
)
class IdentityPoolAppleLoginProvider:
    def __init__(self, *, services_id: builtins.str) -> None:
        '''(deprecated) Login Provider for identity federation using Apple credentials.

        :param services_id: (deprecated) Services ID for Apple identity federation.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    amazon=IdentityPoolAmazonLoginProvider(
                        app_id="amzn1.application.12312k3j234j13rjiwuenf"
                    ),
                    facebook=IdentityPoolFacebookLoginProvider(
                        app_id="1234567890123"
                    ),
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    apple=IdentityPoolAppleLoginProvider(
                        services_id="com.myappleapp.auth"
                    ),
                    twitter=IdentityPoolTwitterLoginProvider(
                        consumer_key="my-twitter-id",
                        consumer_secret="my-twitter-secret"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c9040769cdc703f1660cd3e3da515a34764b5e7c1c0fe8e072609ef85af66f)
            check_type(argname="argument services_id", value=services_id, expected_type=type_hints["services_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "services_id": services_id,
        }

    @builtins.property
    def services_id(self) -> builtins.str:
        '''(deprecated) Services ID for Apple identity federation.

        :stability: deprecated
        '''
        result = self._values.get("services_id")
        assert result is not None, "Required property 'services_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolAppleLoginProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolAuthenticationProviders",
    jsii_struct_bases=[],
    name_mapping={
        "amazon": "amazon",
        "apple": "apple",
        "custom_provider": "customProvider",
        "facebook": "facebook",
        "google": "google",
        "open_id_connect_providers": "openIdConnectProviders",
        "saml_providers": "samlProviders",
        "twitter": "twitter",
        "user_pools": "userPools",
    },
)
class IdentityPoolAuthenticationProviders:
    def __init__(
        self,
        *,
        amazon: typing.Optional[typing.Union[IdentityPoolAmazonLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
        apple: typing.Optional[typing.Union[IdentityPoolAppleLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["IdentityPoolFacebookLoginProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["IdentityPoolGoogleLoginProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        open_id_connect_providers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]] = None,
        saml_providers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.ISamlProvider]] = None,
        twitter: typing.Optional[typing.Union["IdentityPoolTwitterLoginProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pools: typing.Optional[typing.Sequence[IUserPoolAuthenticationProvider]] = None,
    ) -> None:
        '''(deprecated) External Authentication Providers for usage in Identity Pool.

        :param amazon: (deprecated) The Amazon Authentication Provider associated with this Identity Pool. Default: - No Amazon Authentication Provider used without OpenIdConnect or a User Pool
        :param apple: (deprecated) The Apple Authentication Provider associated with this Identity Pool. Default: - No Apple Authentication Provider used without OpenIdConnect or a User Pool
        :param custom_provider: (deprecated) The developer provider name to associate with this Identity Pool. Default: - no custom provider
        :param facebook: (deprecated) The Facebook Authentication Provider associated with this Identity Pool. Default: - No Facebook Authentication Provider used without OpenIdConnect or a User Pool
        :param google: (deprecated) The Google Authentication Provider associated with this Identity Pool. Default: - No Google Authentication Provider used without OpenIdConnect or a User Pool
        :param open_id_connect_providers: (deprecated) The OpenIdConnect Provider associated with this Identity Pool. Default: - no OpenIdConnectProvider
        :param saml_providers: (deprecated) The Security Assertion Markup Language provider associated with this Identity Pool. Default: - no SamlProvider
        :param twitter: (deprecated) The Twitter Authentication Provider associated with this Identity Pool. Default: - No Twitter Authentication Provider used without OpenIdConnect or a User Pool
        :param user_pools: (deprecated) The User Pool Authentication Providers associated with this Identity Pool. Default: - no User Pools associated

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/external-identity-providers.html
        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # open_id_connect_provider: iam.OpenIdConnectProvider
            
            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    open_id_connect_providers=[open_id_connect_provider],
                    custom_provider="my-custom-provider.example.com"
                )
            )
        '''
        if isinstance(amazon, dict):
            amazon = IdentityPoolAmazonLoginProvider(**amazon)
        if isinstance(apple, dict):
            apple = IdentityPoolAppleLoginProvider(**apple)
        if isinstance(facebook, dict):
            facebook = IdentityPoolFacebookLoginProvider(**facebook)
        if isinstance(google, dict):
            google = IdentityPoolGoogleLoginProvider(**google)
        if isinstance(twitter, dict):
            twitter = IdentityPoolTwitterLoginProvider(**twitter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e83f8914cae586eb38cf0016d133dd934c291cad25f28b936d459ade0c5d887)
            check_type(argname="argument amazon", value=amazon, expected_type=type_hints["amazon"])
            check_type(argname="argument apple", value=apple, expected_type=type_hints["apple"])
            check_type(argname="argument custom_provider", value=custom_provider, expected_type=type_hints["custom_provider"])
            check_type(argname="argument facebook", value=facebook, expected_type=type_hints["facebook"])
            check_type(argname="argument google", value=google, expected_type=type_hints["google"])
            check_type(argname="argument open_id_connect_providers", value=open_id_connect_providers, expected_type=type_hints["open_id_connect_providers"])
            check_type(argname="argument saml_providers", value=saml_providers, expected_type=type_hints["saml_providers"])
            check_type(argname="argument twitter", value=twitter, expected_type=type_hints["twitter"])
            check_type(argname="argument user_pools", value=user_pools, expected_type=type_hints["user_pools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon is not None:
            self._values["amazon"] = amazon
        if apple is not None:
            self._values["apple"] = apple
        if custom_provider is not None:
            self._values["custom_provider"] = custom_provider
        if facebook is not None:
            self._values["facebook"] = facebook
        if google is not None:
            self._values["google"] = google
        if open_id_connect_providers is not None:
            self._values["open_id_connect_providers"] = open_id_connect_providers
        if saml_providers is not None:
            self._values["saml_providers"] = saml_providers
        if twitter is not None:
            self._values["twitter"] = twitter
        if user_pools is not None:
            self._values["user_pools"] = user_pools

    @builtins.property
    def amazon(self) -> typing.Optional[IdentityPoolAmazonLoginProvider]:
        '''(deprecated) The Amazon Authentication Provider associated with this Identity Pool.

        :default: - No Amazon Authentication Provider used without OpenIdConnect or a User Pool

        :stability: deprecated
        '''
        result = self._values.get("amazon")
        return typing.cast(typing.Optional[IdentityPoolAmazonLoginProvider], result)

    @builtins.property
    def apple(self) -> typing.Optional[IdentityPoolAppleLoginProvider]:
        '''(deprecated) The Apple Authentication Provider associated with this Identity Pool.

        :default: - No Apple Authentication Provider used without OpenIdConnect or a User Pool

        :stability: deprecated
        '''
        result = self._values.get("apple")
        return typing.cast(typing.Optional[IdentityPoolAppleLoginProvider], result)

    @builtins.property
    def custom_provider(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The developer provider name to associate with this Identity Pool.

        :default: - no custom provider

        :stability: deprecated
        '''
        result = self._values.get("custom_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def facebook(self) -> typing.Optional["IdentityPoolFacebookLoginProvider"]:
        '''(deprecated) The Facebook Authentication Provider associated with this Identity Pool.

        :default: - No Facebook Authentication Provider used without OpenIdConnect or a User Pool

        :stability: deprecated
        '''
        result = self._values.get("facebook")
        return typing.cast(typing.Optional["IdentityPoolFacebookLoginProvider"], result)

    @builtins.property
    def google(self) -> typing.Optional["IdentityPoolGoogleLoginProvider"]:
        '''(deprecated) The Google Authentication Provider associated with this Identity Pool.

        :default: - No Google Authentication Provider used without OpenIdConnect or a User Pool

        :stability: deprecated
        '''
        result = self._values.get("google")
        return typing.cast(typing.Optional["IdentityPoolGoogleLoginProvider"], result)

    @builtins.property
    def open_id_connect_providers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]]:
        '''(deprecated) The OpenIdConnect Provider associated with this Identity Pool.

        :default: - no OpenIdConnectProvider

        :stability: deprecated
        '''
        result = self._values.get("open_id_connect_providers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]], result)

    @builtins.property
    def saml_providers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ISamlProvider]]:
        '''(deprecated) The Security Assertion Markup Language provider associated with this Identity Pool.

        :default: - no SamlProvider

        :stability: deprecated
        '''
        result = self._values.get("saml_providers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ISamlProvider]], result)

    @builtins.property
    def twitter(self) -> typing.Optional["IdentityPoolTwitterLoginProvider"]:
        '''(deprecated) The Twitter Authentication Provider associated with this Identity Pool.

        :default: - No Twitter Authentication Provider used without OpenIdConnect or a User Pool

        :stability: deprecated
        '''
        result = self._values.get("twitter")
        return typing.cast(typing.Optional["IdentityPoolTwitterLoginProvider"], result)

    @builtins.property
    def user_pools(
        self,
    ) -> typing.Optional[typing.List[IUserPoolAuthenticationProvider]]:
        '''(deprecated) The User Pool Authentication Providers associated with this Identity Pool.

        :default: - no User Pools associated

        :stability: deprecated
        '''
        result = self._values.get("user_pools")
        return typing.cast(typing.Optional[typing.List[IUserPoolAuthenticationProvider]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolAuthenticationProviders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolFacebookLoginProvider",
    jsii_struct_bases=[],
    name_mapping={"app_id": "appId"},
)
class IdentityPoolFacebookLoginProvider:
    def __init__(self, *, app_id: builtins.str) -> None:
        '''(deprecated) Login Provider for identity federation using Facebook credentials.

        :param app_id: (deprecated) App ID for Facebook identity federation.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    amazon=IdentityPoolAmazonLoginProvider(
                        app_id="amzn1.application.12312k3j234j13rjiwuenf"
                    ),
                    facebook=IdentityPoolFacebookLoginProvider(
                        app_id="1234567890123"
                    ),
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    apple=IdentityPoolAppleLoginProvider(
                        services_id="com.myappleapp.auth"
                    ),
                    twitter=IdentityPoolTwitterLoginProvider(
                        consumer_key="my-twitter-id",
                        consumer_secret="my-twitter-secret"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553a6105b1cc099f5bb05790fda107ae2e28e4a5891f7d4400f19cddf53e926e)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
        }

    @builtins.property
    def app_id(self) -> builtins.str:
        '''(deprecated) App ID for Facebook identity federation.

        :stability: deprecated
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolFacebookLoginProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolGoogleLoginProvider",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId"},
)
class IdentityPoolGoogleLoginProvider:
    def __init__(self, *, client_id: builtins.str) -> None:
        '''(deprecated) Login Provider for identity federation using Google credentials.

        :param client_id: (deprecated) Client ID for Google identity federation.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    amazon=IdentityPoolAmazonLoginProvider(
                        app_id="amzn1.application.12312k3j234j13rjiwuenf"
                    ),
                    facebook=IdentityPoolFacebookLoginProvider(
                        app_id="1234567890123"
                    ),
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    apple=IdentityPoolAppleLoginProvider(
                        services_id="com.myappleapp.auth"
                    ),
                    twitter=IdentityPoolTwitterLoginProvider(
                        consumer_key="my-twitter-id",
                        consumer_secret="my-twitter-secret"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7d7863b86c1b6983201a7e628ab0bb505b6719534f708df8a6c31427dbb5bb)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''(deprecated) Client ID for Google identity federation.

        :stability: deprecated
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolGoogleLoginProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_classic_flow": "allowClassicFlow",
        "allow_unauthenticated_identities": "allowUnauthenticatedIdentities",
        "authenticated_role": "authenticatedRole",
        "authentication_providers": "authenticationProviders",
        "identity_pool_name": "identityPoolName",
        "role_mappings": "roleMappings",
        "unauthenticated_role": "unauthenticatedRole",
    },
)
class IdentityPoolProps:
    def __init__(
        self,
        *,
        allow_classic_flow: typing.Optional[builtins.bool] = None,
        allow_unauthenticated_identities: typing.Optional[builtins.bool] = None,
        authenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        authentication_providers: typing.Optional[typing.Union[IdentityPoolAuthenticationProviders, typing.Dict[builtins.str, typing.Any]]] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        role_mappings: typing.Optional[typing.Sequence[typing.Union["IdentityPoolRoleMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
        unauthenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(deprecated) Props for the Identity Pool construct.

        :param allow_classic_flow: (deprecated) Enables the Basic (Classic) authentication flow. Default: - Classic Flow not allowed
        :param allow_unauthenticated_identities: (deprecated) Whether the Identity Pool supports unauthenticated logins. Default: - false
        :param authenticated_role: (deprecated) The default Role to be assumed by authenticated users. Default: - A default authenticated Role will be added
        :param authentication_providers: (deprecated) Authentication Providers for using in Identity Pool. Default: - No Authentication Providers passed directly to Identity Pool
        :param identity_pool_name: (deprecated) The name of the Identity Pool. Default: - Automatically generated name by CloudFormation at deploy time
        :param role_mappings: (deprecated) Rules for mapping roles to users. Default: - no role mappings
        :param unauthenticated_role: (deprecated) The default Role to be assumed by unauthenticated users. Default: - A default unauthenticated Role will be added

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # open_id_connect_provider: iam.OpenIdConnectProvider
            
            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    open_id_connect_providers=[open_id_connect_provider],
                    custom_provider="my-custom-provider.example.com"
                )
            )
        '''
        if isinstance(authentication_providers, dict):
            authentication_providers = IdentityPoolAuthenticationProviders(**authentication_providers)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b8242ca2e55a1962a36ef0e9c4b94eae811b93839b5e265f5743512e5ca12b)
            check_type(argname="argument allow_classic_flow", value=allow_classic_flow, expected_type=type_hints["allow_classic_flow"])
            check_type(argname="argument allow_unauthenticated_identities", value=allow_unauthenticated_identities, expected_type=type_hints["allow_unauthenticated_identities"])
            check_type(argname="argument authenticated_role", value=authenticated_role, expected_type=type_hints["authenticated_role"])
            check_type(argname="argument authentication_providers", value=authentication_providers, expected_type=type_hints["authentication_providers"])
            check_type(argname="argument identity_pool_name", value=identity_pool_name, expected_type=type_hints["identity_pool_name"])
            check_type(argname="argument role_mappings", value=role_mappings, expected_type=type_hints["role_mappings"])
            check_type(argname="argument unauthenticated_role", value=unauthenticated_role, expected_type=type_hints["unauthenticated_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_classic_flow is not None:
            self._values["allow_classic_flow"] = allow_classic_flow
        if allow_unauthenticated_identities is not None:
            self._values["allow_unauthenticated_identities"] = allow_unauthenticated_identities
        if authenticated_role is not None:
            self._values["authenticated_role"] = authenticated_role
        if authentication_providers is not None:
            self._values["authentication_providers"] = authentication_providers
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if role_mappings is not None:
            self._values["role_mappings"] = role_mappings
        if unauthenticated_role is not None:
            self._values["unauthenticated_role"] = unauthenticated_role

    @builtins.property
    def allow_classic_flow(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Enables the Basic (Classic) authentication flow.

        :default: - Classic Flow not allowed

        :stability: deprecated
        '''
        result = self._values.get("allow_classic_flow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_unauthenticated_identities(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether the Identity Pool supports unauthenticated logins.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("allow_unauthenticated_identities")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def authenticated_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) The default Role to be assumed by authenticated users.

        :default: - A default authenticated Role will be added

        :stability: deprecated
        '''
        result = self._values.get("authenticated_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def authentication_providers(
        self,
    ) -> typing.Optional[IdentityPoolAuthenticationProviders]:
        '''(deprecated) Authentication Providers for using in Identity Pool.

        :default: - No Authentication Providers passed directly to Identity Pool

        :stability: deprecated
        '''
        result = self._values.get("authentication_providers")
        return typing.cast(typing.Optional[IdentityPoolAuthenticationProviders], result)

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the Identity Pool.

        :default: - Automatically generated name by CloudFormation at deploy time

        :stability: deprecated
        '''
        result = self._values.get("identity_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_mappings(self) -> typing.Optional[typing.List["IdentityPoolRoleMapping"]]:
        '''(deprecated) Rules for mapping roles to users.

        :default: - no role mappings

        :stability: deprecated
        '''
        result = self._values.get("role_mappings")
        return typing.cast(typing.Optional[typing.List["IdentityPoolRoleMapping"]], result)

    @builtins.property
    def unauthenticated_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) The default Role to be assumed by unauthenticated users.

        :default: - A default unauthenticated Role will be added

        :stability: deprecated
        '''
        result = self._values.get("unauthenticated_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolProviderType"
)
class IdentityPoolProviderType(enum.Enum):
    '''(deprecated) Types of Identity Pool Login Providers.

    :stability: deprecated
    '''

    FACEBOOK = "FACEBOOK"
    '''(deprecated) Facebook provider type.

    :stability: deprecated
    '''
    GOOGLE = "GOOGLE"
    '''(deprecated) Google provider type.

    :stability: deprecated
    '''
    AMAZON = "AMAZON"
    '''(deprecated) Amazon provider type.

    :stability: deprecated
    '''
    APPLE = "APPLE"
    '''(deprecated) Apple provider type.

    :stability: deprecated
    '''
    TWITTER = "TWITTER"
    '''(deprecated) Twitter provider type.

    :stability: deprecated
    '''
    OPEN_ID = "OPEN_ID"
    '''(deprecated) Open Id provider type.

    :stability: deprecated
    '''
    SAML = "SAML"
    '''(deprecated) Saml provider type.

    :stability: deprecated
    '''
    USER_POOL = "USER_POOL"
    '''(deprecated) User Pool provider type.

    :stability: deprecated
    '''
    CUSTOM = "CUSTOM"
    '''(deprecated) Custom provider type.

    :stability: deprecated
    '''


class IdentityPoolProviderUrl(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolProviderUrl",
):
    '''(deprecated) Keys for Login Providers - each correspond to the client IDs of their respective federation Identity Providers.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl
        
        
        IdentityPool(self, "myidentitypool",
            identity_pool_name="myidentitypool",
            role_mappings=[IdentityPoolRoleMapping(
                provider_url=IdentityPoolProviderUrl.custom("my-custom-provider.com"),
                use_token=True
            )
            ]
        )
    '''

    def __init__(self, type: IdentityPoolProviderType, value: builtins.str) -> None:
        '''
        :param type: The type of Identity Pool Provider.
        :param value: The value of the Identity Pool Provider.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423f3af9588f321b47a169a44fe143eb961b0377418e1736dde381403db8730e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [type, value])

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, url: builtins.str) -> "IdentityPoolProviderUrl":
        '''(deprecated) Custom Provider url.

        :param url: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba4eac2376a67f469d725ea627955e1696d934a6d0601d7e4873d8b2b48d749)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast("IdentityPoolProviderUrl", jsii.sinvoke(cls, "custom", [url]))

    @jsii.member(jsii_name="openId")
    @builtins.classmethod
    def open_id(cls, url: builtins.str) -> "IdentityPoolProviderUrl":
        '''(deprecated) OpenId Provider url.

        :param url: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d161a44d12cc621bec8346b7a54def25199238af1ee02be289568c2abb4aed2)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast("IdentityPoolProviderUrl", jsii.sinvoke(cls, "openId", [url]))

    @jsii.member(jsii_name="saml")
    @builtins.classmethod
    def saml(cls, url: builtins.str) -> "IdentityPoolProviderUrl":
        '''(deprecated) Saml Provider url.

        :param url: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbf2fc0f2dbf61ab8ba7e761e45e78a8d5d3bbfa64ccc8f8d93bff656c1a825)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast("IdentityPoolProviderUrl", jsii.sinvoke(cls, "saml", [url]))

    @jsii.member(jsii_name="userPool")
    @builtins.classmethod
    def user_pool(
        cls,
        user_pool: _aws_cdk_aws_cognito_ceddda9d.IUserPool,
        user_pool_client: _aws_cdk_aws_cognito_ceddda9d.IUserPoolClient,
    ) -> "IdentityPoolProviderUrl":
        '''(deprecated) User Pool Provider Url.

        :param user_pool: -
        :param user_pool_client: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7531b9fff4293227d6e5c746c9e82a2d3b5164eaf82e984877f422ff7de768c9)
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
            check_type(argname="argument user_pool_client", value=user_pool_client, expected_type=type_hints["user_pool_client"])
        return typing.cast("IdentityPoolProviderUrl", jsii.sinvoke(cls, "userPool", [user_pool, user_pool_client]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON")
    def AMAZON(cls) -> "IdentityPoolProviderUrl":
        '''(deprecated) Amazon Provider url.

        :stability: deprecated
        '''
        return typing.cast("IdentityPoolProviderUrl", jsii.sget(cls, "AMAZON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLE")
    def APPLE(cls) -> "IdentityPoolProviderUrl":
        '''(deprecated) Apple Provider url.

        :stability: deprecated
        '''
        return typing.cast("IdentityPoolProviderUrl", jsii.sget(cls, "APPLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FACEBOOK")
    def FACEBOOK(cls) -> "IdentityPoolProviderUrl":
        '''(deprecated) Facebook Provider url.

        :stability: deprecated
        '''
        return typing.cast("IdentityPoolProviderUrl", jsii.sget(cls, "FACEBOOK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GOOGLE")
    def GOOGLE(cls) -> "IdentityPoolProviderUrl":
        '''(deprecated) Google Provider url.

        :stability: deprecated
        '''
        return typing.cast("IdentityPoolProviderUrl", jsii.sget(cls, "GOOGLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TWITTER")
    def TWITTER(cls) -> "IdentityPoolProviderUrl":
        '''(deprecated) Twitter Provider url.

        :stability: deprecated
        '''
        return typing.cast("IdentityPoolProviderUrl", jsii.sget(cls, "TWITTER"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> IdentityPoolProviderType:
        '''(deprecated) The type of Identity Pool Provider.

        :stability: deprecated
        '''
        return typing.cast(IdentityPoolProviderType, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(deprecated) The value of the Identity Pool Provider.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolRoleMapping",
    jsii_struct_bases=[],
    name_mapping={
        "provider_url": "providerUrl",
        "mapping_key": "mappingKey",
        "resolve_ambiguous_roles": "resolveAmbiguousRoles",
        "rules": "rules",
        "use_token": "useToken",
    },
)
class IdentityPoolRoleMapping:
    def __init__(
        self,
        *,
        provider_url: IdentityPoolProviderUrl,
        mapping_key: typing.Optional[builtins.str] = None,
        resolve_ambiguous_roles: typing.Optional[builtins.bool] = None,
        rules: typing.Optional[typing.Sequence[typing.Union["RoleMappingRule", typing.Dict[builtins.str, typing.Any]]]] = None,
        use_token: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(deprecated) Map roles to users in the Identity Pool based on claims from the Identity Provider.

        :param provider_url: (deprecated) The url of the Provider for which the role is mapped.
        :param mapping_key: (deprecated) The key used for the role mapping in the role mapping hash. Required if the providerUrl is a token. Default: - The provided providerUrl
        :param resolve_ambiguous_roles: (deprecated) Allow for role assumption when results of role mapping are ambiguous. Default: false - Ambiguous role resolutions will lead to requester being denied
        :param rules: (deprecated) The claim and value that must be matched in order to assume the role. Required if useToken is false Default: - No role mapping rule
        :param use_token: (deprecated) If true then mapped roles must be passed through the cognito:roles or cognito:preferred_role claims from Identity Provider. Default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html
        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cognito_identitypool_alpha as cognito_identitypool_alpha
            from aws_cdk import aws_iam as iam
            
            # identity_pool_provider_url: cognito_identitypool_alpha.IdentityPoolProviderUrl
            # role: iam.Role
            
            identity_pool_role_mapping = cognito_identitypool_alpha.IdentityPoolRoleMapping(
                provider_url=identity_pool_provider_url,
            
                # the properties below are optional
                mapping_key="mappingKey",
                resolve_ambiguous_roles=False,
                rules=[cognito_identitypool_alpha.RoleMappingRule(
                    claim="claim",
                    claim_value="claimValue",
                    mapped_role=role,
            
                    # the properties below are optional
                    match_type=cognito_identitypool_alpha.RoleMappingMatchType.EQUALS
                )],
                use_token=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650ad537013ada6fb730b758a9cc04e3e889c73469adb530187b60e65137d653)
            check_type(argname="argument provider_url", value=provider_url, expected_type=type_hints["provider_url"])
            check_type(argname="argument mapping_key", value=mapping_key, expected_type=type_hints["mapping_key"])
            check_type(argname="argument resolve_ambiguous_roles", value=resolve_ambiguous_roles, expected_type=type_hints["resolve_ambiguous_roles"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument use_token", value=use_token, expected_type=type_hints["use_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_url": provider_url,
        }
        if mapping_key is not None:
            self._values["mapping_key"] = mapping_key
        if resolve_ambiguous_roles is not None:
            self._values["resolve_ambiguous_roles"] = resolve_ambiguous_roles
        if rules is not None:
            self._values["rules"] = rules
        if use_token is not None:
            self._values["use_token"] = use_token

    @builtins.property
    def provider_url(self) -> IdentityPoolProviderUrl:
        '''(deprecated) The url of the Provider for which the role is mapped.

        :stability: deprecated
        '''
        result = self._values.get("provider_url")
        assert result is not None, "Required property 'provider_url' is missing"
        return typing.cast(IdentityPoolProviderUrl, result)

    @builtins.property
    def mapping_key(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The key used for the role mapping in the role mapping hash.

        Required if the providerUrl is a token.

        :default: - The provided providerUrl

        :stability: deprecated
        '''
        result = self._values.get("mapping_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolve_ambiguous_roles(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Allow for role assumption when results of role mapping are ambiguous.

        :default: false - Ambiguous role resolutions will lead to requester being denied

        :stability: deprecated
        '''
        result = self._values.get("resolve_ambiguous_roles")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["RoleMappingRule"]]:
        '''(deprecated) The claim and value that must be matched in order to assume the role.

        Required if useToken is false

        :default: - No role mapping rule

        :stability: deprecated
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["RoleMappingRule"]], result)

    @builtins.property
    def use_token(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) If true then mapped roles must be passed through the cognito:roles or cognito:preferred_role claims from Identity Provider.

        :default: false

        :see: https://docs.aws.amazon.com/cognito/latest/developerguide/role-based-access-control.html#using-tokens-to-assign-roles-to-users
        :stability: deprecated
        '''
        result = self._values.get("use_token")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolRoleMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.IdentityPoolTwitterLoginProvider",
    jsii_struct_bases=[],
    name_mapping={"consumer_key": "consumerKey", "consumer_secret": "consumerSecret"},
)
class IdentityPoolTwitterLoginProvider:
    def __init__(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret: builtins.str,
    ) -> None:
        '''(deprecated) Login Provider for identity federation using Twitter credentials.

        :param consumer_key: (deprecated) Consumer key for Twitter identity federation.
        :param consumer_secret: (deprecated) Consumer secret for identity federation.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            IdentityPool(self, "myidentitypool",
                identity_pool_name="myidentitypool",
                authentication_providers=IdentityPoolAuthenticationProviders(
                    amazon=IdentityPoolAmazonLoginProvider(
                        app_id="amzn1.application.12312k3j234j13rjiwuenf"
                    ),
                    facebook=IdentityPoolFacebookLoginProvider(
                        app_id="1234567890123"
                    ),
                    google=IdentityPoolGoogleLoginProvider(
                        client_id="12345678012.apps.googleusercontent.com"
                    ),
                    apple=IdentityPoolAppleLoginProvider(
                        services_id="com.myappleapp.auth"
                    ),
                    twitter=IdentityPoolTwitterLoginProvider(
                        consumer_key="my-twitter-id",
                        consumer_secret="my-twitter-secret"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91153aca8aea767279ad014c0a8369ca2e36afc6e9b02f0111bc64f713b104f)
            check_type(argname="argument consumer_key", value=consumer_key, expected_type=type_hints["consumer_key"])
            check_type(argname="argument consumer_secret", value=consumer_secret, expected_type=type_hints["consumer_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
        }

    @builtins.property
    def consumer_key(self) -> builtins.str:
        '''(deprecated) Consumer key for Twitter identity federation.

        :stability: deprecated
        '''
        result = self._values.get("consumer_key")
        assert result is not None, "Required property 'consumer_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_secret(self) -> builtins.str:
        '''(deprecated) Consumer secret for identity federation.

        :stability: deprecated
        '''
        result = self._values.get("consumer_secret")
        assert result is not None, "Required property 'consumer_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPoolTwitterLoginProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.RoleMappingMatchType")
class RoleMappingMatchType(enum.Enum):
    '''(deprecated) Types of matches allowed for role mapping.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_cognito_identitypool_alpha import IdentityPoolProviderUrl, RoleMappingMatchType
        
        # admin_role: iam.Role
        # non_admin_role: iam.Role
        
        IdentityPool(self, "myidentitypool",
            identity_pool_name="myidentitypool",
            # Assign specific roles to users based on whether or not the custom admin claim is passed from the identity provider
            role_mappings=[IdentityPoolRoleMapping(
                provider_url=IdentityPoolProviderUrl.AMAZON,
                rules=[RoleMappingRule(
                    claim="custom:admin",
                    claim_value="admin",
                    mapped_role=admin_role
                ), RoleMappingRule(
                    claim="custom:admin",
                    claim_value="admin",
                    match_type=RoleMappingMatchType.NOTEQUAL,
                    mapped_role=non_admin_role
                )
                ]
            )]
        )
    '''

    EQUALS = "EQUALS"
    '''(deprecated) The claim from the token must equal the given value in order for a match.

    :stability: deprecated
    '''
    CONTAINS = "CONTAINS"
    '''(deprecated) The claim from the token must contain the given value in order for a match.

    :stability: deprecated
    '''
    STARTS_WITH = "STARTS_WITH"
    '''(deprecated) The claim from the token must start with the given value in order for a match.

    :stability: deprecated
    '''
    NOTEQUAL = "NOTEQUAL"
    '''(deprecated) The claim from the token must not equal the given value in order for a match.

    :stability: deprecated
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.RoleMappingRule",
    jsii_struct_bases=[],
    name_mapping={
        "claim": "claim",
        "claim_value": "claimValue",
        "mapped_role": "mappedRole",
        "match_type": "matchType",
    },
)
class RoleMappingRule:
    def __init__(
        self,
        *,
        claim: builtins.str,
        claim_value: builtins.str,
        mapped_role: _aws_cdk_aws_iam_ceddda9d.IRole,
        match_type: typing.Optional[RoleMappingMatchType] = None,
    ) -> None:
        '''(deprecated) Represents an Identity Pool Role Attachment role mapping rule.

        :param claim: (deprecated) The key sent in the token by the federated Identity Provider.
        :param claim_value: (deprecated) The value of the claim that must be matched.
        :param mapped_role: (deprecated) The role to be assumed when the claim value is matched.
        :param match_type: (deprecated) How to match with the claim value. Default: RoleMappingMatchType.EQUALS

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cognito_identitypool_alpha as cognito_identitypool_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            role_mapping_rule = cognito_identitypool_alpha.RoleMappingRule(
                claim="claim",
                claim_value="claimValue",
                mapped_role=role,
            
                # the properties below are optional
                match_type=cognito_identitypool_alpha.RoleMappingMatchType.EQUALS
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77869f331952f425fa372fe2f927e6224793554cefa649c244780e367abe94a9)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument claim_value", value=claim_value, expected_type=type_hints["claim_value"])
            check_type(argname="argument mapped_role", value=mapped_role, expected_type=type_hints["mapped_role"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim": claim,
            "claim_value": claim_value,
            "mapped_role": mapped_role,
        }
        if match_type is not None:
            self._values["match_type"] = match_type

    @builtins.property
    def claim(self) -> builtins.str:
        '''(deprecated) The key sent in the token by the federated Identity Provider.

        :stability: deprecated
        '''
        result = self._values.get("claim")
        assert result is not None, "Required property 'claim' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def claim_value(self) -> builtins.str:
        '''(deprecated) The value of the claim that must be matched.

        :stability: deprecated
        '''
        result = self._values.get("claim_value")
        assert result is not None, "Required property 'claim_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mapped_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(deprecated) The role to be assumed when the claim value is matched.

        :stability: deprecated
        '''
        result = self._values.get("mapped_role")
        assert result is not None, "Required property 'mapped_role' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, result)

    @builtins.property
    def match_type(self) -> typing.Optional[RoleMappingMatchType]:
        '''(deprecated) How to match with the claim value.

        :default: RoleMappingMatchType.EQUALS

        :stability: deprecated
        '''
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[RoleMappingMatchType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleMappingRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IUserPoolAuthenticationProvider)
class UserPoolAuthenticationProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.UserPoolAuthenticationProvider",
):
    '''(deprecated) Defines a User Pool Authentication Provider.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # identity_pool: IdentityPool
        
        user_pool = cognito.UserPool(self, "Pool")
        identity_pool.add_user_pool_authentication(UserPoolAuthenticationProvider(
            user_pool=user_pool,
            disable_server_side_token_check=True
        ))
    '''

    def __init__(
        self,
        *,
        user_pool: _aws_cdk_aws_cognito_ceddda9d.IUserPool,
        disable_server_side_token_check: typing.Optional[builtins.bool] = None,
        user_pool_client: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.IUserPoolClient] = None,
    ) -> None:
        '''
        :param user_pool: (deprecated) The User Pool of the Associated Identity Providers.
        :param disable_server_side_token_check: (deprecated) Setting this to true turns off identity pool checks for this user pool to make sure the user has not been globally signed out or deleted before the identity pool provides an OIDC token or AWS credentials for the user. Default: false
        :param user_pool_client: (deprecated) The User Pool Client for the provided User Pool. Default: - A default user pool client will be added to User Pool

        :stability: deprecated
        '''
        props = UserPoolAuthenticationProviderProps(
            user_pool=user_pool,
            disable_server_side_token_check=disable_server_side_token_check,
            user_pool_client=user_pool_client,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        identity_pool: IIdentityPool,
    ) -> "UserPoolAuthenticationProviderBindConfig":
        '''(deprecated) The method called when a given User Pool Authentication Provider is added (for the first time) to an Identity Pool.

        :param scope: -
        :param identity_pool: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c3e4f47b37f4d3265edfa6c7ad01b5c1409a21b5450216878fdce228df9f72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument identity_pool", value=identity_pool, expected_type=type_hints["identity_pool"])
        _options = UserPoolAuthenticationProviderBindOptions()

        return typing.cast("UserPoolAuthenticationProviderBindConfig", jsii.invoke(self, "bind", [scope, identity_pool, _options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.UserPoolAuthenticationProviderBindConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "provider_name": "providerName",
        "server_side_token_check": "serverSideTokenCheck",
    },
)
class UserPoolAuthenticationProviderBindConfig:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        provider_name: builtins.str,
        server_side_token_check: builtins.bool,
    ) -> None:
        '''(deprecated) Represents a UserPoolAuthenticationProvider Bind Configuration.

        :param client_id: (deprecated) Client Id of the Associated User Pool Client.
        :param provider_name: (deprecated) The identity providers associated with the UserPool.
        :param server_side_token_check: (deprecated) Whether to enable the identity pool's server side token check.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cognito_identitypool_alpha as cognito_identitypool_alpha
            
            user_pool_authentication_provider_bind_config = cognito_identitypool_alpha.UserPoolAuthenticationProviderBindConfig(
                client_id="clientId",
                provider_name="providerName",
                server_side_token_check=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b8fa9dab857d092fcc38b5be232ff1c0998d006d07c8ef726d2a6530e5df52)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument server_side_token_check", value=server_side_token_check, expected_type=type_hints["server_side_token_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "provider_name": provider_name,
            "server_side_token_check": server_side_token_check,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''(deprecated) Client Id of the Associated User Pool Client.

        :stability: deprecated
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''(deprecated) The identity providers associated with the UserPool.

        :stability: deprecated
        '''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_side_token_check(self) -> builtins.bool:
        '''(deprecated) Whether to enable the identity pool's server side token check.

        :stability: deprecated
        '''
        result = self._values.get("server_side_token_check")
        assert result is not None, "Required property 'server_side_token_check' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolAuthenticationProviderBindConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.UserPoolAuthenticationProviderBindOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserPoolAuthenticationProviderBindOptions:
    def __init__(self) -> None:
        '''(deprecated) Represents UserPoolAuthenticationProvider Bind Options.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cognito_identitypool_alpha as cognito_identitypool_alpha
            
            user_pool_authentication_provider_bind_options = cognito_identitypool_alpha.UserPoolAuthenticationProviderBindOptions()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolAuthenticationProviderBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cognito-identitypool-alpha.UserPoolAuthenticationProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool": "userPool",
        "disable_server_side_token_check": "disableServerSideTokenCheck",
        "user_pool_client": "userPoolClient",
    },
)
class UserPoolAuthenticationProviderProps:
    def __init__(
        self,
        *,
        user_pool: _aws_cdk_aws_cognito_ceddda9d.IUserPool,
        disable_server_side_token_check: typing.Optional[builtins.bool] = None,
        user_pool_client: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.IUserPoolClient] = None,
    ) -> None:
        '''(deprecated) Props for the User Pool Authentication Provider.

        :param user_pool: (deprecated) The User Pool of the Associated Identity Providers.
        :param disable_server_side_token_check: (deprecated) Setting this to true turns off identity pool checks for this user pool to make sure the user has not been globally signed out or deleted before the identity pool provides an OIDC token or AWS credentials for the user. Default: false
        :param user_pool_client: (deprecated) The User Pool Client for the provided User Pool. Default: - A default user pool client will be added to User Pool

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # identity_pool: IdentityPool
            
            user_pool = cognito.UserPool(self, "Pool")
            identity_pool.add_user_pool_authentication(UserPoolAuthenticationProvider(
                user_pool=user_pool,
                disable_server_side_token_check=True
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdefc66d6c0c410084a508326629a8119aadc43267abbb8e697b3b9be03f9561)
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
            check_type(argname="argument disable_server_side_token_check", value=disable_server_side_token_check, expected_type=type_hints["disable_server_side_token_check"])
            check_type(argname="argument user_pool_client", value=user_pool_client, expected_type=type_hints["user_pool_client"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool": user_pool,
        }
        if disable_server_side_token_check is not None:
            self._values["disable_server_side_token_check"] = disable_server_side_token_check
        if user_pool_client is not None:
            self._values["user_pool_client"] = user_pool_client

    @builtins.property
    def user_pool(self) -> _aws_cdk_aws_cognito_ceddda9d.IUserPool:
        '''(deprecated) The User Pool of the Associated Identity Providers.

        :stability: deprecated
        '''
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.IUserPool, result)

    @builtins.property
    def disable_server_side_token_check(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Setting this to true turns off identity pool checks for this user pool to make sure the user has not been globally signed out or deleted before the identity pool provides an OIDC token or AWS credentials for the user.

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cognito-identitypool-cognitoidentityprovider.html
        :stability: deprecated
        '''
        result = self._values.get("disable_server_side_token_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def user_pool_client(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.IUserPoolClient]:
        '''(deprecated) The User Pool Client for the provided User Pool.

        :default: - A default user pool client will be added to User Pool

        :stability: deprecated
        '''
        result = self._values.get("user_pool_client")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.IUserPoolClient], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolAuthenticationProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IIdentityPool",
    "IUserPoolAuthenticationProvider",
    "IdentityPool",
    "IdentityPoolAmazonLoginProvider",
    "IdentityPoolAppleLoginProvider",
    "IdentityPoolAuthenticationProviders",
    "IdentityPoolFacebookLoginProvider",
    "IdentityPoolGoogleLoginProvider",
    "IdentityPoolProps",
    "IdentityPoolProviderType",
    "IdentityPoolProviderUrl",
    "IdentityPoolRoleMapping",
    "IdentityPoolTwitterLoginProvider",
    "RoleMappingMatchType",
    "RoleMappingRule",
    "UserPoolAuthenticationProvider",
    "UserPoolAuthenticationProviderBindConfig",
    "UserPoolAuthenticationProviderBindOptions",
    "UserPoolAuthenticationProviderProps",
]

publication.publish()

def _typecheckingstub__07632ef1025feb6e05894b02941c351317dc03c46357f2c76f22433d4b28396c(
    scope: _constructs_77d1e7e8.Construct,
    identity_pool: IIdentityPool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2f072d5cac259fbc65a0c4a6a8cb785ff9ebcf2da91f9184be84a22820a980(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_classic_flow: typing.Optional[builtins.bool] = None,
    allow_unauthenticated_identities: typing.Optional[builtins.bool] = None,
    authenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    authentication_providers: typing.Optional[typing.Union[IdentityPoolAuthenticationProviders, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    role_mappings: typing.Optional[typing.Sequence[typing.Union[IdentityPoolRoleMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
    unauthenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95e191d26141b46fee8d2cdcabc0803b18860942f1a248701db0dae81123def(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    identity_pool_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5abb9f2926d1e1f17a15fd6b4211f8951279c31ec22f381103f75200b458fa1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    identity_pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd9ea8a4c738095932e3cf624c6eb098117704692279323d27952d6b2df0e00(
    user_pool: IUserPoolAuthenticationProvider,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e283aa49d3946357252123279fe3e514c02786d6dbaf36c03180cb06444fd8(
    *,
    app_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c9040769cdc703f1660cd3e3da515a34764b5e7c1c0fe8e072609ef85af66f(
    *,
    services_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e83f8914cae586eb38cf0016d133dd934c291cad25f28b936d459ade0c5d887(
    *,
    amazon: typing.Optional[typing.Union[IdentityPoolAmazonLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    apple: typing.Optional[typing.Union[IdentityPoolAppleLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_provider: typing.Optional[builtins.str] = None,
    facebook: typing.Optional[typing.Union[IdentityPoolFacebookLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    google: typing.Optional[typing.Union[IdentityPoolGoogleLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    open_id_connect_providers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]] = None,
    saml_providers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.ISamlProvider]] = None,
    twitter: typing.Optional[typing.Union[IdentityPoolTwitterLoginProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pools: typing.Optional[typing.Sequence[IUserPoolAuthenticationProvider]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553a6105b1cc099f5bb05790fda107ae2e28e4a5891f7d4400f19cddf53e926e(
    *,
    app_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7d7863b86c1b6983201a7e628ab0bb505b6719534f708df8a6c31427dbb5bb(
    *,
    client_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b8242ca2e55a1962a36ef0e9c4b94eae811b93839b5e265f5743512e5ca12b(
    *,
    allow_classic_flow: typing.Optional[builtins.bool] = None,
    allow_unauthenticated_identities: typing.Optional[builtins.bool] = None,
    authenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    authentication_providers: typing.Optional[typing.Union[IdentityPoolAuthenticationProviders, typing.Dict[builtins.str, typing.Any]]] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    role_mappings: typing.Optional[typing.Sequence[typing.Union[IdentityPoolRoleMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
    unauthenticated_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423f3af9588f321b47a169a44fe143eb961b0377418e1736dde381403db8730e(
    type: IdentityPoolProviderType,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba4eac2376a67f469d725ea627955e1696d934a6d0601d7e4873d8b2b48d749(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d161a44d12cc621bec8346b7a54def25199238af1ee02be289568c2abb4aed2(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbf2fc0f2dbf61ab8ba7e761e45e78a8d5d3bbfa64ccc8f8d93bff656c1a825(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7531b9fff4293227d6e5c746c9e82a2d3b5164eaf82e984877f422ff7de768c9(
    user_pool: _aws_cdk_aws_cognito_ceddda9d.IUserPool,
    user_pool_client: _aws_cdk_aws_cognito_ceddda9d.IUserPoolClient,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650ad537013ada6fb730b758a9cc04e3e889c73469adb530187b60e65137d653(
    *,
    provider_url: IdentityPoolProviderUrl,
    mapping_key: typing.Optional[builtins.str] = None,
    resolve_ambiguous_roles: typing.Optional[builtins.bool] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[RoleMappingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_token: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91153aca8aea767279ad014c0a8369ca2e36afc6e9b02f0111bc64f713b104f(
    *,
    consumer_key: builtins.str,
    consumer_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77869f331952f425fa372fe2f927e6224793554cefa649c244780e367abe94a9(
    *,
    claim: builtins.str,
    claim_value: builtins.str,
    mapped_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    match_type: typing.Optional[RoleMappingMatchType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c3e4f47b37f4d3265edfa6c7ad01b5c1409a21b5450216878fdce228df9f72(
    scope: _constructs_77d1e7e8.Construct,
    identity_pool: IIdentityPool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b8fa9dab857d092fcc38b5be232ff1c0998d006d07c8ef726d2a6530e5df52(
    *,
    client_id: builtins.str,
    provider_name: builtins.str,
    server_side_token_check: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdefc66d6c0c410084a508326629a8119aadc43267abbb8e697b3b9be03f9561(
    *,
    user_pool: _aws_cdk_aws_cognito_ceddda9d.IUserPool,
    disable_server_side_token_check: typing.Optional[builtins.bool] = None,
    user_pool_client: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.IUserPoolClient] = None,
) -> None:
    """Type checking stubs"""
    pass
