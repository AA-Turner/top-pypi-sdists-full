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

import aws_cdk.aws_directoryservice as _aws_cdk_aws_directoryservice_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..compute import DomainWindowsNode as _DomainWindowsNode_bbfd2a18


class AwsManagedMicrosoftAd(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skylight.authentication.AwsManagedMicrosoftAd",
):
    '''A Ad Authentication represents an integration pattern of Managed AD and Route 53 Resolver in a specific VPC.

    The Construct creates Managed AD with the provided Secret (Secrets Manager) or generates a new Secret.
    The secret saved to SSM parameter store so others can use it with other Constructs (Such as Windows node or FSx)
    The provided VPC or the new created VPC will be configured to forward DNS requests to the Managed AD with Route53 Resolvers
    The construct also creates (optionally) t3.nano machine that is part of the domain that can be used to run admin-tasks (such as createADGroup)

    The createADGroup() method creates an Active Directory permission group in the domain, using the domain admin user.
    Please note: When calling createADGroup() API, a Lambda will be created to start the worker machine (Using AWS-SDK),
    then each command will be scheduled with State Manager, and the instance will be shut down after complete.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "IAwsManagedMicrosoftAdProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38e7a75a9f7876e1cbbb507dc08ece7cc040cdffc7512e5f46037f458dfa62a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createADGroup")
    def create_ad_group(
        self,
        group_name: builtins.str,
        group_description: builtins.str,
    ) -> None:
        '''
        :param group_name: -
        :param group_description: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1139b21194a3c69f830cf3ea44f95ccdf847a3b3affc95e81e582ddf4abc56e4)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument group_description", value=group_description, expected_type=type_hints["group_description"])
        return typing.cast(None, jsii.invoke(self, "createADGroup", [group_name, group_description]))

    @jsii.member(jsii_name="createServiceAccount")
    def create_service_account(
        self,
        ad_service_account_name: builtins.str,
        service_principal_names: builtins.str,
        principals_allowed_to_retrieve_managed_password: builtins.str,
    ) -> None:
        '''
        :param ad_service_account_name: -
        :param service_principal_names: -
        :param principals_allowed_to_retrieve_managed_password: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44921307fff68f74cf5ab0d84be4605afdaf4836bfe498f0e2a0c0f076a741c4)
            check_type(argname="argument ad_service_account_name", value=ad_service_account_name, expected_type=type_hints["ad_service_account_name"])
            check_type(argname="argument service_principal_names", value=service_principal_names, expected_type=type_hints["service_principal_names"])
            check_type(argname="argument principals_allowed_to_retrieve_managed_password", value=principals_allowed_to_retrieve_managed_password, expected_type=type_hints["principals_allowed_to_retrieve_managed_password"])
        return typing.cast(None, jsii.invoke(self, "createServiceAccount", [ad_service_account_name, service_principal_names, principals_allowed_to_retrieve_managed_password]))

    @jsii.member(jsii_name="createWorker")
    def create_worker(
        self,
        domain_name: builtins.str,
        domain_password: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> _DomainWindowsNode_bbfd2a18:
        '''
        :param domain_name: -
        :param domain_password: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f4b5a799c2202da37d9cadd76bcb86fac0c40cac75961545fe61285ffe93c9)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_password", value=domain_password, expected_type=type_hints["domain_password"])
        return typing.cast(_DomainWindowsNode_bbfd2a18, jsii.invoke(self, "createWorker", [domain_name, domain_password]))

    @builtins.property
    @jsii.member(jsii_name="adParameters")
    def ad_parameters(self) -> "IAwsManagedMicrosoftAdParameters":
        return typing.cast("IAwsManagedMicrosoftAdParameters", jsii.get(self, "adParameters"))

    @builtins.property
    @jsii.member(jsii_name="microsoftAD")
    def microsoft_ad(self) -> _aws_cdk_aws_directoryservice_ceddda9d.CfnMicrosoftAD:
        return typing.cast(_aws_cdk_aws_directoryservice_ceddda9d.CfnMicrosoftAD, jsii.get(self, "microsoftAD"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "IAwsManagedMicrosoftAdProps":
        return typing.cast("IAwsManagedMicrosoftAdProps", jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="domainWindowsNode")
    def domain_windows_node(self) -> typing.Optional[_DomainWindowsNode_bbfd2a18]:
        return typing.cast(typing.Optional[_DomainWindowsNode_bbfd2a18], jsii.get(self, "domainWindowsNode"))


class AwsManagedMicrosoftAdR53(
    AwsManagedMicrosoftAd,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-skylight.authentication.AwsManagedMicrosoftAdR53",
):
    '''A Ad Authentication represents an integration pattern of Managed AD and Route 53 Resolver in a specific VPC.

    The Construct creates Managed AD with the provided Secret (Secrets Manager) or generates a new Secret.
    The secret saved to SSM parameter store so others can use it with other Constructs (Such as Windows node or FSx)
    The provided VPC or the new created VPC will be configured to forward DNS requests to the Managed AD with Route53 Resolvers
    The construct also creates (optionally) t3.nano machine that is part of the domain that can be used to run admin-tasks (such as createADGroup)

    The createADGroup() method creates an Active Directory permission group in the domain, using the domain admin user.
    Please note: When calling createADGroup() API, a Lambda will be created to start the worker machine (Using AWS-SDK),
    then each command will be scheduled with State Manager, and the instance will be shut down after complete.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "IAwsManagedMicrosoftAdProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69889897ced96a4b8f59248f8da70219591966027b33d24ec4aba108d5b5c1f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])


@jsii.enum(
    jsii_type="cdk-skylight.authentication.AwsManagedMicrosoftConfigurationStoreType"
)
class AwsManagedMicrosoftConfigurationStoreType(enum.Enum):
    SSM = "SSM"


@jsii.interface(
    jsii_type="cdk-skylight.authentication.IAwsManagedMicrosoftAdParameters"
)
class IAwsManagedMicrosoftAdParameters(typing_extensions.Protocol):
    '''The properties of an DomainWindowsNodeProps, requires Active Directory parameter to read the Secret to join the domain Default setting: Domain joined, m5.2xlarge, latest windows, Managed by SSM.'''

    @builtins.property
    @jsii.member(jsii_name="configurationStoreType")
    def configuration_store_type(
        self,
    ) -> typing.Optional[AwsManagedMicrosoftConfigurationStoreType]:
        '''The name of the Configuration Store Type to use.

        :default: - 'AWS Systems Manager Parameter Store'.
        '''
        ...

    @configuration_store_type.setter
    def configuration_store_type(
        self,
        value: typing.Optional[AwsManagedMicrosoftConfigurationStoreType],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="directoryIDPointer")
    def directory_id_pointer(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Object that contains the Directory ID.

        :default: - 'directoryID'.
        '''
        ...

    @directory_id_pointer.setter
    def directory_id_pointer(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to read/write parameters to.

        :default: - 'cdk-skylight'.
        '''
        ...

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="secretPointer")
    def secret_pointer(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Object that contains the secret name in Secrets Manager.

        :default: - 'domain-secret'.
        '''
        ...

    @secret_pointer.setter
    def secret_pointer(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IAwsManagedMicrosoftAdParametersProxy:
    '''The properties of an DomainWindowsNodeProps, requires Active Directory parameter to read the Secret to join the domain Default setting: Domain joined, m5.2xlarge, latest windows, Managed by SSM.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.authentication.IAwsManagedMicrosoftAdParameters"

    @builtins.property
    @jsii.member(jsii_name="configurationStoreType")
    def configuration_store_type(
        self,
    ) -> typing.Optional[AwsManagedMicrosoftConfigurationStoreType]:
        '''The name of the Configuration Store Type to use.

        :default: - 'AWS Systems Manager Parameter Store'.
        '''
        return typing.cast(typing.Optional[AwsManagedMicrosoftConfigurationStoreType], jsii.get(self, "configurationStoreType"))

    @configuration_store_type.setter
    def configuration_store_type(
        self,
        value: typing.Optional[AwsManagedMicrosoftConfigurationStoreType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2279b4c2d40cbb12f44404fdf7d5840008040d0c79519c30e262903045ac3a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryIDPointer")
    def directory_id_pointer(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Object that contains the Directory ID.

        :default: - 'directoryID'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryIDPointer"))

    @directory_id_pointer.setter
    def directory_id_pointer(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633466d3b2dfab6adeb64dbce18f61ad4edaee3b53ffa9ee152147057076cbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryIDPointer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The SSM namespace to read/write parameters to.

        :default: - 'cdk-skylight'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ba2dd002e0fe0dadd76a35a1b858ac2a6062eae689be9460568363068a8eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretPointer")
    def secret_pointer(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM Object that contains the secret name in Secrets Manager.

        :default: - 'domain-secret'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretPointer"))

    @secret_pointer.setter
    def secret_pointer(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c63d218984df0c7dbcefed6370d070fe429f8dc04d027c434f0848e4678654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretPointer", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAwsManagedMicrosoftAdParameters).__jsii_proxy_class__ = lambda : _IAwsManagedMicrosoftAdParametersProxy


@jsii.interface(jsii_type="cdk-skylight.authentication.IAwsManagedMicrosoftAdProps")
class IAwsManagedMicrosoftAdProps(typing_extensions.Protocol):
    '''The properties for the AwsManagedMicrosoftAd class.'''

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to use, must have private subnets.'''
        ...

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="configurationStore")
    def configuration_store(self) -> typing.Optional[IAwsManagedMicrosoftAdParameters]:
        '''The configuration store to save the directory parameters (After deployed).'''
        ...

    @configuration_store.setter
    def configuration_store(
        self,
        value: typing.Optional[IAwsManagedMicrosoftAdParameters],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="createWorker")
    def create_worker(self) -> typing.Optional[builtins.bool]:
        '''Create Domain joined machine to be used to run Powershell commands to that directory.

        (i.e Create Ad Group)

        :default: - 'true'.
        '''
        ...

    @create_worker.setter
    def create_worker(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the Active Directory Domain.

        :default: - 'domain.aws'.
        '''
        ...

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition to use for the Active Directory Domain.

        Allowed values: Enterprise | Standard
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-edition

        :default: - 'Standard'.
        '''
        ...

    @edition.setter
    def edition(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''The secrets manager secret to use must be in format: '{Domain: <domain.name>, UserID: 'Admin', Password: ''}'.

        :default: - 'Randomly generated and stored in Secret Manager'.
        '''
        ...

    @secret.setter
    def secret(
        self,
        value: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''The secret name to save the Domain Admin object.

        :default: - '<domain.name>-secret'.
        '''
        ...

    @secret_name.setter
    def secret_name(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcSubnets")
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets]:
        '''VPC subnet selection, subnets must be private and exactly 2.'''
        ...

    @vpc_subnets.setter
    def vpc_subnets(
        self,
        value: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets],
    ) -> None:
        ...


class _IAwsManagedMicrosoftAdPropsProxy:
    '''The properties for the AwsManagedMicrosoftAd class.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-skylight.authentication.IAwsManagedMicrosoftAdProps"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to use, must have private subnets.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1356ea88b0b9a92664a4b1c8bb4a1d972f617ee283fed1f9f3142a6d12ef19e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configurationStore")
    def configuration_store(self) -> typing.Optional[IAwsManagedMicrosoftAdParameters]:
        '''The configuration store to save the directory parameters (After deployed).'''
        return typing.cast(typing.Optional[IAwsManagedMicrosoftAdParameters], jsii.get(self, "configurationStore"))

    @configuration_store.setter
    def configuration_store(
        self,
        value: typing.Optional[IAwsManagedMicrosoftAdParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8d32fea33eaab65d8be890ca7fb92fd8a0e0cf559598bbfa265c25f772140e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createWorker")
    def create_worker(self) -> typing.Optional[builtins.bool]:
        '''Create Domain joined machine to be used to run Powershell commands to that directory.

        (i.e Create Ad Group)

        :default: - 'true'.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createWorker"))

    @create_worker.setter
    def create_worker(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477a29e6d3779d450a5f7bdd3b7a65de55f678acad3a65ee443c88c012f22873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createWorker", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the Active Directory Domain.

        :default: - 'domain.aws'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202094da47b871396b3c62310c4b5c240dbf330e68dd5e32764b016f65fffd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition to use for the Active Directory Domain.

        Allowed values: Enterprise | Standard
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-edition

        :default: - 'Standard'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4bb1c822e8f8abfd4350babf18ed4138e7afbf9cab1c6e1fe2ad170f0e3ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''The secrets manager secret to use must be in format: '{Domain: <domain.name>, UserID: 'Admin', Password: ''}'.

        :default: - 'Randomly generated and stored in Secret Manager'.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "secret"))

    @secret.setter
    def secret(
        self,
        value: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390bcec06ac0feadc81e3e773c72c4b25c4cb61803536184b886b44e42dee6c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''The secret name to save the Domain Admin object.

        :default: - '<domain.name>-secret'.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549ced8bf27406c4f678bb63944c066c80ecf74f9c70372c5d0a936e6c0633a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcSubnets")
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets]:
        '''VPC subnet selection, subnets must be private and exactly 2.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets], jsii.get(self, "vpcSubnets"))

    @vpc_subnets.setter
    def vpc_subnets(
        self,
        value: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8928970163b927f4599b947dc4936f00af446c321bb87dbfc44b30fd670f2c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSubnets", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAwsManagedMicrosoftAdProps).__jsii_proxy_class__ = lambda : _IAwsManagedMicrosoftAdPropsProxy


__all__ = [
    "AwsManagedMicrosoftAd",
    "AwsManagedMicrosoftAdR53",
    "AwsManagedMicrosoftConfigurationStoreType",
    "IAwsManagedMicrosoftAdParameters",
    "IAwsManagedMicrosoftAdProps",
]

publication.publish()

def _typecheckingstub__b38e7a75a9f7876e1cbbb507dc08ece7cc040cdffc7512e5f46037f458dfa62a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IAwsManagedMicrosoftAdProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1139b21194a3c69f830cf3ea44f95ccdf847a3b3affc95e81e582ddf4abc56e4(
    group_name: builtins.str,
    group_description: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44921307fff68f74cf5ab0d84be4605afdaf4836bfe498f0e2a0c0f076a741c4(
    ad_service_account_name: builtins.str,
    service_principal_names: builtins.str,
    principals_allowed_to_retrieve_managed_password: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f4b5a799c2202da37d9cadd76bcb86fac0c40cac75961545fe61285ffe93c9(
    domain_name: builtins.str,
    domain_password: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69889897ced96a4b8f59248f8da70219591966027b33d24ec4aba108d5b5c1f9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IAwsManagedMicrosoftAdProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2279b4c2d40cbb12f44404fdf7d5840008040d0c79519c30e262903045ac3a8d(
    value: typing.Optional[AwsManagedMicrosoftConfigurationStoreType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633466d3b2dfab6adeb64dbce18f61ad4edaee3b53ffa9ee152147057076cbaa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ba2dd002e0fe0dadd76a35a1b858ac2a6062eae689be9460568363068a8eba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c63d218984df0c7dbcefed6370d070fe429f8dc04d027c434f0848e4678654(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1356ea88b0b9a92664a4b1c8bb4a1d972f617ee283fed1f9f3142a6d12ef19e9(
    value: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8d32fea33eaab65d8be890ca7fb92fd8a0e0cf559598bbfa265c25f772140e(
    value: typing.Optional[IAwsManagedMicrosoftAdParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477a29e6d3779d450a5f7bdd3b7a65de55f678acad3a65ee443c88c012f22873(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202094da47b871396b3c62310c4b5c240dbf330e68dd5e32764b016f65fffd16(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4bb1c822e8f8abfd4350babf18ed4138e7afbf9cab1c6e1fe2ad170f0e3ebb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390bcec06ac0feadc81e3e773c72c4b25c4cb61803536184b886b44e42dee6c4(
    value: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549ced8bf27406c4f678bb63944c066c80ecf74f9c70372c5d0a936e6c0633a7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8928970163b927f4599b947dc4936f00af446c321bb87dbfc44b30fd670f2c11(
    value: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets],
) -> None:
    """Type checking stubs"""
    pass
