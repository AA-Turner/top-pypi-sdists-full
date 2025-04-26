r'''
# cdk8s

### Cloud Development Kit for Kubernetes

[![build](https://github.com/cdk8s-team/cdk8s-core/workflows/release/badge.svg)](https://github.com/cdk8s-team/cdk8s-core/actions/workflows/release.yml)
[![npm version](https://badge.fury.io/js/cdk8s.svg)](https://badge.fury.io/js/cdk8s)
[![PyPI version](https://badge.fury.io/py/cdk8s.svg)](https://badge.fury.io/py/cdk8s)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/org.cdk8s/cdk8s/badge.svg)](https://maven-badges.herokuapp.com/maven-central/org.cdk8s/cdk8s)

**cdk8s** is a software development framework for defining Kubernetes
applications using rich object-oriented APIs. It allows developers to leverage
the full power of software in order to define abstract components called
"constructs" which compose Kubernetes resources or other constructs into
higher-level abstractions.

> **Note:** This repository is the "core library" of cdk8s, with logic for synthesizing Kubernetes manifests using the [constructs framework](https://github.com/aws/constructs). It is published to NPM as [`cdk8s`](https://www.npmjs.com/package/cdk8s) and should not be confused with the cdk8s command-line tool [`cdk8s-cli`](https://www.npmjs.com/package/cdk8s-cli). For more general information about cdk8s, please see [cdk8s.io](https://cdk8s.io), or visit the umbrella repository located at [cdk8s-team/cdk8s](https://github.com/cdk8s-team/cdk8s).

## Documentation

See [cdk8s.io](https://cdk8s.io).

## License

This project is distributed under the [Apache License, Version 2.0](./LICENSE).

This module is part of the [cdk8s project](https://github.com/cdk8s-team/cdk8s).
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

import constructs as _constructs_77d1e7e8


class ApiObject(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.ApiObject",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        metadata: typing.Optional[typing.Union["ApiObjectMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Defines an API object.

        :param scope: the construct scope.
        :param id: namespace.
        :param api_version: API version.
        :param kind: Resource kind.
        :param metadata: Object metadata. If ``name`` is not specified, an app-unique name will be allocated by the framework based on the path of the construct within thes construct tree.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3471c86f94453ef4d9efec6bd8f9cf9dbac2f11db69184e091d0a4f6d502be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApiObjectProps(api_version=api_version, kind=kind, metadata=metadata)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isApiObject")
    @builtins.classmethod
    def is_api_object(cls, o: typing.Any) -> builtins.bool:
        '''Return whether the given object is an ``ApiObject``.

        We do attribute detection since we can't reliably use 'instanceof'.

        :param o: The object to check.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1861e2a67b17cc03b65ec7686045b40569487efa29052a042f312c20d14b2c)
            check_type(argname="argument o", value=o, expected_type=type_hints["o"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isApiObject", [o]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, c: _constructs_77d1e7e8.IConstruct) -> "ApiObject":
        '''Returns the ``ApiObject`` named ``Resource`` which is a child of the given construct.

        If ``c`` is an ``ApiObject``, it is returned directly. Throws an
        exception if the construct does not have a child named ``Default`` *or* if
        this child is not an ``ApiObject``.

        :param c: The higher-level construct.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c55b2fcd45f38255c26ac00ed411c9af6ec5ea8ba6920c18afedcc214149a4e)
            check_type(argname="argument c", value=c, expected_type=type_hints["c"])
        return typing.cast("ApiObject", jsii.sinvoke(cls, "of", [c]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: _constructs_77d1e7e8.IConstruct) -> None:
        '''Create a dependency between this ApiObject and other constructs.

        These can be other ApiObjects, Charts, or custom.

        :param dependencies: the dependencies to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82881106c470fdf7ed8e821d53730213ae34215c35ed597f7708178c0df728bf)
            check_type(argname="argument dependencies", value=dependencies, expected_type=typing.Tuple[type_hints["dependencies"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDependency", [*dependencies]))

    @jsii.member(jsii_name="addJsonPatch")
    def add_json_patch(self, *ops: "JsonPatch") -> None:
        '''Applies a set of RFC-6902 JSON-Patch operations to the manifest synthesized for this API object.

        :param ops: The JSON-Patch operations to apply.

        Example::

              kubePod.addJsonPatch(JsonPatch.replace('/spec/enableServiceLinks', true));
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161731dd57929dbfaf25c8720b0e1ddbb543e720daf53247296b6d94a9976531)
            check_type(argname="argument ops", value=ops, expected_type=typing.Tuple[type_hints["ops"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addJsonPatch", [*ops]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        '''Renders the object to Kubernetes JSON.

        To disable sorting of dictionary keys in output object set the
        ``CDK8S_DISABLE_SORT`` environment variable to any non-empty value.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJson", []))

    @builtins.property
    @jsii.member(jsii_name="apiGroup")
    def api_group(self) -> builtins.str:
        '''The group portion of the API version (e.g. ``authorization.k8s.io``).'''
        return typing.cast(builtins.str, jsii.get(self, "apiGroup"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        '''The object's API version (e.g. ``authorization.k8s.io/v1``).'''
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @builtins.property
    @jsii.member(jsii_name="chart")
    def chart(self) -> "Chart":
        '''The chart in which this object is defined.'''
        return typing.cast("Chart", jsii.get(self, "chart"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        '''The object kind.'''
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "ApiObjectMetadataDefinition":
        '''Metadata associated with this API object.'''
        return typing.cast("ApiObjectMetadataDefinition", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the API object.

        If a name is specified in ``metadata.name`` this will be the name returned.
        Otherwise, a name will be generated by calling
        ``Chart.of(this).generatedObjectName(this)``, which by default uses the
        construct path to generate a DNS-compatible name for the resource.
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk8s.ApiObjectMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "finalizers": "finalizers",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
        "owner_references": "ownerReferences",
    },
)
class ApiObjectMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        finalizers: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        owner_references: typing.Optional[typing.Sequence[typing.Union["OwnerReference", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Metadata associated with this object.

        :param annotations: Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. Default: - No annotations.
        :param finalizers: Namespaced keys that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for deletion. Must be empty before the object is deleted from the registry. Each entry is an identifier for the responsible component that will remove the entry from the list. If the deletionTimestamp of the object is non-nil, entries in this list can only be removed. Finalizers may be processed and removed in any order. Order is NOT enforced because it introduces significant risk of stuck finalizers. finalizers is a shared field, any actor with permission can reorder it. If the finalizer list is processed in order, then this can lead to a situation in which the component responsible for the first finalizer in the list is waiting for a signal (field value, external system, or other) produced by a component responsible for a finalizer later in the list, resulting in a deadlock. Without enforced ordering finalizers are free to order amongst themselves and are not vulnerable to ordering changes in the list. Default: - No finalizers.
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. Default: - No labels.
        :param name: The unique, namespace-global, name of this object inside the Kubernetes cluster. Normally, you shouldn't specify names for objects and let the CDK generate a name for you that is application-unique. The names CDK generates are composed from the construct path components, separated by dots and a suffix that is based on a hash of the entire path, to ensure uniqueness. You can supply custom name allocation logic by overriding the ``chart.generateObjectName`` method. If you use an explicit name here, bear in mind that this reduces the composability of your construct because it won't be possible to include more than one instance in any app. Therefore it is highly recommended to leave this unspecified. Default: - an app-unique name generated by the chart
        :param namespace: Namespace defines the space within each name must be unique. An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces Default: undefined (will be assigned to the 'default' namespace)
        :param owner_references: List of objects depended by this object. If ALL objects in the list have been deleted, this object will be garbage collected. If this object is managed by a controller, then an entry in this list will point to this controller, with the controller field set to true. There cannot be more than one managing controller. Kubernetes sets the value of this field automatically for objects that are dependents of other objects like ReplicaSets, DaemonSets, Deployments, Jobs and CronJobs, and ReplicationControllers. You can also configure these relationships manually by changing the value of this field. However, you usually don't need to and can allow Kubernetes to automatically manage the relationships. Default: - automatically set by Kubernetes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f4c3c7639bc9b50e949af73521350fa15fe4a126bddfdabcac5172638d132d)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument finalizers", value=finalizers, expected_type=type_hints["finalizers"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument owner_references", value=owner_references, expected_type=type_hints["owner_references"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if finalizers is not None:
            self._values["finalizers"] = finalizers
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if owner_references is not None:
            self._values["owner_references"] = owner_references

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata.

        They are not queryable and should be
        preserved when modifying objects.

        :default: - No annotations.

        :see: http://kubernetes.io/docs/user-guide/annotations
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def finalizers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Namespaced keys that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for deletion.

        Must be empty before the object is deleted from the registry. Each entry is
        an identifier for the responsible component that will remove the entry from
        the list. If the deletionTimestamp of the object is non-nil, entries in
        this list can only be removed. Finalizers may be processed and removed in
        any order.  Order is NOT enforced because it introduces significant risk of
        stuck finalizers. finalizers is a shared field, any actor with permission
        can reorder it. If the finalizer list is processed in order, then this can
        lead to a situation in which the component responsible for the first
        finalizer in the list is waiting for a signal (field value, external
        system, or other) produced by a component responsible for a finalizer later
        in the list, resulting in a deadlock. Without enforced ordering finalizers
        are free to order amongst themselves and are not vulnerable to ordering
        changes in the list.

        :default: - No finalizers.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
        '''
        result = self._values.get("finalizers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        May match selectors of replication controllers and services.

        :default: - No labels.

        :see: http://kubernetes.io/docs/user-guide/labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique, namespace-global, name of this object inside the Kubernetes cluster.

        Normally, you shouldn't specify names for objects and let the CDK generate
        a name for you that is application-unique. The names CDK generates are
        composed from the construct path components, separated by dots and a suffix
        that is based on a hash of the entire path, to ensure uniqueness.

        You can supply custom name allocation logic by overriding the
        ``chart.generateObjectName`` method.

        If you use an explicit name here, bear in mind that this reduces the
        composability of your construct because it won't be possible to include
        more than one instance in any app. Therefore it is highly recommended to
        leave this unspecified.

        :default: - an app-unique name generated by the chart
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within each name must be unique.

        An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation.
        Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces

        :default: undefined (will be assigned to the 'default' namespace)
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_references(self) -> typing.Optional[typing.List["OwnerReference"]]:
        '''List of objects depended by this object.

        If ALL objects in the list have
        been deleted, this object will be garbage collected. If this object is
        managed by a controller, then an entry in this list will point to this
        controller, with the controller field set to true. There cannot be more
        than one managing controller.

        Kubernetes sets the value of this field automatically for objects that are
        dependents of other objects like ReplicaSets, DaemonSets, Deployments, Jobs
        and CronJobs, and ReplicationControllers. You can also configure these
        relationships manually by changing the value of this field. However, you
        usually don't need to and can allow Kubernetes to automatically manage the
        relationships.

        :default: - automatically set by Kubernetes

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/
        '''
        result = self._values.get("owner_references")
        return typing.cast(typing.Optional[typing.List["OwnerReference"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiObjectMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiObjectMetadataDefinition(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.ApiObjectMetadataDefinition",
):
    '''Object metadata.'''

    def __init__(
        self,
        *,
        api_object: ApiObject,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        finalizers: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        owner_references: typing.Optional[typing.Sequence[typing.Union["OwnerReference", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param api_object: Which ApiObject instance is the metadata attached to.
        :param annotations: Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. Default: - No annotations.
        :param finalizers: Namespaced keys that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for deletion. Must be empty before the object is deleted from the registry. Each entry is an identifier for the responsible component that will remove the entry from the list. If the deletionTimestamp of the object is non-nil, entries in this list can only be removed. Finalizers may be processed and removed in any order. Order is NOT enforced because it introduces significant risk of stuck finalizers. finalizers is a shared field, any actor with permission can reorder it. If the finalizer list is processed in order, then this can lead to a situation in which the component responsible for the first finalizer in the list is waiting for a signal (field value, external system, or other) produced by a component responsible for a finalizer later in the list, resulting in a deadlock. Without enforced ordering finalizers are free to order amongst themselves and are not vulnerable to ordering changes in the list. Default: - No finalizers.
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. Default: - No labels.
        :param name: The unique, namespace-global, name of this object inside the Kubernetes cluster. Normally, you shouldn't specify names for objects and let the CDK generate a name for you that is application-unique. The names CDK generates are composed from the construct path components, separated by dots and a suffix that is based on a hash of the entire path, to ensure uniqueness. You can supply custom name allocation logic by overriding the ``chart.generateObjectName`` method. If you use an explicit name here, bear in mind that this reduces the composability of your construct because it won't be possible to include more than one instance in any app. Therefore it is highly recommended to leave this unspecified. Default: - an app-unique name generated by the chart
        :param namespace: Namespace defines the space within each name must be unique. An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces Default: undefined (will be assigned to the 'default' namespace)
        :param owner_references: List of objects depended by this object. If ALL objects in the list have been deleted, this object will be garbage collected. If this object is managed by a controller, then an entry in this list will point to this controller, with the controller field set to true. There cannot be more than one managing controller. Kubernetes sets the value of this field automatically for objects that are dependents of other objects like ReplicaSets, DaemonSets, Deployments, Jobs and CronJobs, and ReplicationControllers. You can also configure these relationships manually by changing the value of this field. However, you usually don't need to and can allow Kubernetes to automatically manage the relationships. Default: - automatically set by Kubernetes
        '''
        options = ApiObjectMetadataDefinitionOptions(
            api_object=api_object,
            annotations=annotations,
            finalizers=finalizers,
            labels=labels,
            name=name,
            namespace=namespace,
            owner_references=owner_references,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="add")
    def add(self, key: builtins.str, value: typing.Any) -> None:
        '''Adds an arbitrary key/value to the object metadata.

        :param key: Metadata key.
        :param value: Metadata value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9def3e3bd00bf53cb37a2e0644831b7d89d8821a115c8d269a7d9e2d4531bb4d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "add", [key, value]))

    @jsii.member(jsii_name="addAnnotation")
    def add_annotation(self, key: builtins.str, value: builtins.str) -> None:
        '''Add an annotation.

        :param key: - The key.
        :param value: - The value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca708eae375d08efb85cb3aa3ab3facc98cc64a3ab5ae313448e08b7d5029c5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addAnnotation", [key, value]))

    @jsii.member(jsii_name="addFinalizers")
    def add_finalizers(self, *finalizers: builtins.str) -> None:
        '''Add one or more finalizers.

        :param finalizers: the finalizers.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dc63d8c5b395973d6bc1d0cdc1e1b5026ce0e8147949b44197244e4156f74e)
            check_type(argname="argument finalizers", value=finalizers, expected_type=typing.Tuple[type_hints["finalizers"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addFinalizers", [*finalizers]))

    @jsii.member(jsii_name="addLabel")
    def add_label(self, key: builtins.str, value: builtins.str) -> None:
        '''Add a label.

        :param key: - The key.
        :param value: - The value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63f1a5223c791fe2ed2391972064b7664d61556144b09da9c6bc83a0328cefe)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addLabel", [key, value]))

    @jsii.member(jsii_name="addOwnerReference")
    def add_owner_reference(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        uid: builtins.str,
        block_owner_deletion: typing.Optional[builtins.bool] = None,
        controller: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Add an owner.

        :param api_version: API version of the referent.
        :param kind: Kind of the referent.
        :param name: Name of the referent.
        :param uid: UID of the referent.
        :param block_owner_deletion: If true, AND if the owner has the "foregroundDeletion" finalizer, then the owner cannot be deleted from the key-value store until this reference is removed. Defaults to false. To set this field, a user needs "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be returned. Default: false. To set this field, a user needs "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be returned.
        :param controller: If true, this reference points to the managing controller.
        '''
        owner = OwnerReference(
            api_version=api_version,
            kind=kind,
            name=name,
            uid=uid,
            block_owner_deletion=block_owner_deletion,
            controller=controller,
        )

        return typing.cast(None, jsii.invoke(self, "addOwnerReference", [owner]))

    @jsii.member(jsii_name="getLabel")
    def get_label(self, key: builtins.str) -> typing.Optional[builtins.str]:
        '''
        :param key: the label.

        :return: a value of a label or undefined
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec412ec90f3d03be3378cbdee675bf84860bff9d43c0328f5c1508f82ce2e6b)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getLabel", [key]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        '''Synthesizes a k8s ObjectMeta for this metadata set.'''
        return typing.cast(typing.Any, jsii.invoke(self, "toJson", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the API object.

        If a name is specified in ``metadata.name`` this will be the name returned.
        Otherwise, a name will be generated by calling
        ``Chart.of(this).generatedObjectName(this)``, which by default uses the
        construct path to generate a DNS-compatible name for the resource.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The object's namespace.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))


@jsii.data_type(
    jsii_type="cdk8s.ApiObjectMetadataDefinitionOptions",
    jsii_struct_bases=[ApiObjectMetadata],
    name_mapping={
        "annotations": "annotations",
        "finalizers": "finalizers",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
        "owner_references": "ownerReferences",
        "api_object": "apiObject",
    },
)
class ApiObjectMetadataDefinitionOptions(ApiObjectMetadata):
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        finalizers: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        owner_references: typing.Optional[typing.Sequence[typing.Union["OwnerReference", typing.Dict[builtins.str, typing.Any]]]] = None,
        api_object: ApiObject,
    ) -> None:
        '''Options for ``ApiObjectMetadataDefinition``.

        :param annotations: Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. Default: - No annotations.
        :param finalizers: Namespaced keys that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for deletion. Must be empty before the object is deleted from the registry. Each entry is an identifier for the responsible component that will remove the entry from the list. If the deletionTimestamp of the object is non-nil, entries in this list can only be removed. Finalizers may be processed and removed in any order. Order is NOT enforced because it introduces significant risk of stuck finalizers. finalizers is a shared field, any actor with permission can reorder it. If the finalizer list is processed in order, then this can lead to a situation in which the component responsible for the first finalizer in the list is waiting for a signal (field value, external system, or other) produced by a component responsible for a finalizer later in the list, resulting in a deadlock. Without enforced ordering finalizers are free to order amongst themselves and are not vulnerable to ordering changes in the list. Default: - No finalizers.
        :param labels: Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. Default: - No labels.
        :param name: The unique, namespace-global, name of this object inside the Kubernetes cluster. Normally, you shouldn't specify names for objects and let the CDK generate a name for you that is application-unique. The names CDK generates are composed from the construct path components, separated by dots and a suffix that is based on a hash of the entire path, to ensure uniqueness. You can supply custom name allocation logic by overriding the ``chart.generateObjectName`` method. If you use an explicit name here, bear in mind that this reduces the composability of your construct because it won't be possible to include more than one instance in any app. Therefore it is highly recommended to leave this unspecified. Default: - an app-unique name generated by the chart
        :param namespace: Namespace defines the space within each name must be unique. An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces Default: undefined (will be assigned to the 'default' namespace)
        :param owner_references: List of objects depended by this object. If ALL objects in the list have been deleted, this object will be garbage collected. If this object is managed by a controller, then an entry in this list will point to this controller, with the controller field set to true. There cannot be more than one managing controller. Kubernetes sets the value of this field automatically for objects that are dependents of other objects like ReplicaSets, DaemonSets, Deployments, Jobs and CronJobs, and ReplicationControllers. You can also configure these relationships manually by changing the value of this field. However, you usually don't need to and can allow Kubernetes to automatically manage the relationships. Default: - automatically set by Kubernetes
        :param api_object: Which ApiObject instance is the metadata attached to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941a97ef4e3f244aec7e1e661b3ea14853c24d8af07fc02fa36831237c09dff3)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument finalizers", value=finalizers, expected_type=type_hints["finalizers"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument owner_references", value=owner_references, expected_type=type_hints["owner_references"])
            check_type(argname="argument api_object", value=api_object, expected_type=type_hints["api_object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_object": api_object,
        }
        if annotations is not None:
            self._values["annotations"] = annotations
        if finalizers is not None:
            self._values["finalizers"] = finalizers
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if owner_references is not None:
            self._values["owner_references"] = owner_references

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata.

        They are not queryable and should be
        preserved when modifying objects.

        :default: - No annotations.

        :see: http://kubernetes.io/docs/user-guide/annotations
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def finalizers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Namespaced keys that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for deletion.

        Must be empty before the object is deleted from the registry. Each entry is
        an identifier for the responsible component that will remove the entry from
        the list. If the deletionTimestamp of the object is non-nil, entries in
        this list can only be removed. Finalizers may be processed and removed in
        any order.  Order is NOT enforced because it introduces significant risk of
        stuck finalizers. finalizers is a shared field, any actor with permission
        can reorder it. If the finalizer list is processed in order, then this can
        lead to a situation in which the component responsible for the first
        finalizer in the list is waiting for a signal (field value, external
        system, or other) produced by a component responsible for a finalizer later
        in the list, resulting in a deadlock. Without enforced ordering finalizers
        are free to order amongst themselves and are not vulnerable to ordering
        changes in the list.

        :default: - No finalizers.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
        '''
        result = self._values.get("finalizers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        May match selectors of replication controllers and services.

        :default: - No labels.

        :see: http://kubernetes.io/docs/user-guide/labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique, namespace-global, name of this object inside the Kubernetes cluster.

        Normally, you shouldn't specify names for objects and let the CDK generate
        a name for you that is application-unique. The names CDK generates are
        composed from the construct path components, separated by dots and a suffix
        that is based on a hash of the entire path, to ensure uniqueness.

        You can supply custom name allocation logic by overriding the
        ``chart.generateObjectName`` method.

        If you use an explicit name here, bear in mind that this reduces the
        composability of your construct because it won't be possible to include
        more than one instance in any app. Therefore it is highly recommended to
        leave this unspecified.

        :default: - an app-unique name generated by the chart
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace defines the space within each name must be unique.

        An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation.
        Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces

        :default: undefined (will be assigned to the 'default' namespace)
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_references(self) -> typing.Optional[typing.List["OwnerReference"]]:
        '''List of objects depended by this object.

        If ALL objects in the list have
        been deleted, this object will be garbage collected. If this object is
        managed by a controller, then an entry in this list will point to this
        controller, with the controller field set to true. There cannot be more
        than one managing controller.

        Kubernetes sets the value of this field automatically for objects that are
        dependents of other objects like ReplicaSets, DaemonSets, Deployments, Jobs
        and CronJobs, and ReplicationControllers. You can also configure these
        relationships manually by changing the value of this field. However, you
        usually don't need to and can allow Kubernetes to automatically manage the
        relationships.

        :default: - automatically set by Kubernetes

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/
        '''
        result = self._values.get("owner_references")
        return typing.cast(typing.Optional[typing.List["OwnerReference"]], result)

    @builtins.property
    def api_object(self) -> ApiObject:
        '''Which ApiObject instance is the metadata attached to.'''
        result = self._values.get("api_object")
        assert result is not None, "Required property 'api_object' is missing"
        return typing.cast(ApiObject, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiObjectMetadataDefinitionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s.ApiObjectProps",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "kind": "kind", "metadata": "metadata"},
)
class ApiObjectProps:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        metadata: typing.Optional[typing.Union[ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Options for defining API objects.

        :param api_version: API version.
        :param kind: Resource kind.
        :param metadata: Object metadata. If ``name`` is not specified, an app-unique name will be allocated by the framework based on the path of the construct within thes construct tree.
        '''
        if isinstance(metadata, dict):
            metadata = ApiObjectMetadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd25b85d2368c9440a32a95c8f2442d5db4cc9bc422486dd10cfc51448222d8)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_version": api_version,
            "kind": kind,
        }
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def api_version(self) -> builtins.str:
        '''API version.'''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Resource kind.'''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> typing.Optional[ApiObjectMetadata]:
        '''Object metadata.

        If ``name`` is not specified, an app-unique name will be allocated by the
        framework based on the path of the construct within thes construct tree.
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[ApiObjectMetadata], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiObjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class App(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.App",
):
    '''Represents a cdk8s application.'''

    def __init__(
        self,
        *,
        outdir: typing.Optional[builtins.str] = None,
        output_file_extension: typing.Optional[builtins.str] = None,
        record_construct_metadata: typing.Optional[builtins.bool] = None,
        resolvers: typing.Optional[typing.Sequence["IResolver"]] = None,
        yaml_output_type: typing.Optional["YamlOutputType"] = None,
    ) -> None:
        '''Defines an app.

        :param outdir: The directory to output Kubernetes manifests. If you synthesize your application using ``cdk8s synth``, you must also pass this value to the CLI using the ``--output`` option or the ``output`` property in the ``cdk8s.yaml`` configuration file. Otherwise, the CLI will not know about the output directory, and synthesis will fail. This property is intended for internal and testing use. Default: - CDK8S_OUTDIR if defined, otherwise "dist"
        :param output_file_extension: The file extension to use for rendered YAML files. Default: .k8s.yaml
        :param record_construct_metadata: When set to true, the output directory will contain a ``construct-metadata.json`` file that holds construct related metadata on every resource in the app. Default: false
        :param resolvers: A list of resolvers that can be used to replace property values before they are written to the manifest file. When multiple resolvers are passed, they are invoked by order in the list, and only the first one that applies (e.g calls ``context.replaceValue``) is invoked. Default: - no resolvers.
        :param yaml_output_type: How to divide the YAML output into files. Default: YamlOutputType.FILE_PER_CHART
        '''
        props = AppProps(
            outdir=outdir,
            output_file_extension=output_file_extension,
            record_construct_metadata=record_construct_metadata,
            resolvers=resolvers,
            yaml_output_type=yaml_output_type,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, c: _constructs_77d1e7e8.IConstruct) -> "App":
        '''
        :param c: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d69a701ccbd6d4fe53a9f9a1243ebfef02b200d6c47aaee4e0ecb22fc803d4)
            check_type(argname="argument c", value=c, expected_type=type_hints["c"])
        return typing.cast("App", jsii.sinvoke(cls, "of", [c]))

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        '''Synthesizes all manifests to the output directory.'''
        return typing.cast(None, jsii.invoke(self, "synth", []))

    @jsii.member(jsii_name="synthYaml")
    def synth_yaml(self) -> builtins.str:
        '''Synthesizes the app into a YAML string.

        :return: A string with all YAML objects across all charts in this app.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "synthYaml", []))

    @builtins.property
    @jsii.member(jsii_name="charts")
    def charts(self) -> typing.List["Chart"]:
        '''Returns all the charts in this app, sorted topologically.'''
        return typing.cast(typing.List["Chart"], jsii.get(self, "charts"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''The output directory into which manifests will be synthesized.'''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="outputFileExtension")
    def output_file_extension(self) -> builtins.str:
        '''The file extension to use for rendered YAML files.

        :default: .k8s.yaml
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputFileExtension"))

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(self) -> typing.List["IResolver"]:
        '''Resolvers used by this app.

        This includes both custom resolvers
        passed by the ``resolvers`` property, as well as built-in resolvers.
        '''
        return typing.cast(typing.List["IResolver"], jsii.get(self, "resolvers"))

    @builtins.property
    @jsii.member(jsii_name="yamlOutputType")
    def yaml_output_type(self) -> "YamlOutputType":
        '''How to divide the YAML output into files.

        :default: YamlOutputType.FILE_PER_CHART
        '''
        return typing.cast("YamlOutputType", jsii.get(self, "yamlOutputType"))


@jsii.data_type(
    jsii_type="cdk8s.AppProps",
    jsii_struct_bases=[],
    name_mapping={
        "outdir": "outdir",
        "output_file_extension": "outputFileExtension",
        "record_construct_metadata": "recordConstructMetadata",
        "resolvers": "resolvers",
        "yaml_output_type": "yamlOutputType",
    },
)
class AppProps:
    def __init__(
        self,
        *,
        outdir: typing.Optional[builtins.str] = None,
        output_file_extension: typing.Optional[builtins.str] = None,
        record_construct_metadata: typing.Optional[builtins.bool] = None,
        resolvers: typing.Optional[typing.Sequence["IResolver"]] = None,
        yaml_output_type: typing.Optional["YamlOutputType"] = None,
    ) -> None:
        '''
        :param outdir: The directory to output Kubernetes manifests. If you synthesize your application using ``cdk8s synth``, you must also pass this value to the CLI using the ``--output`` option or the ``output`` property in the ``cdk8s.yaml`` configuration file. Otherwise, the CLI will not know about the output directory, and synthesis will fail. This property is intended for internal and testing use. Default: - CDK8S_OUTDIR if defined, otherwise "dist"
        :param output_file_extension: The file extension to use for rendered YAML files. Default: .k8s.yaml
        :param record_construct_metadata: When set to true, the output directory will contain a ``construct-metadata.json`` file that holds construct related metadata on every resource in the app. Default: false
        :param resolvers: A list of resolvers that can be used to replace property values before they are written to the manifest file. When multiple resolvers are passed, they are invoked by order in the list, and only the first one that applies (e.g calls ``context.replaceValue``) is invoked. Default: - no resolvers.
        :param yaml_output_type: How to divide the YAML output into files. Default: YamlOutputType.FILE_PER_CHART
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef9f0e4cd886d9d12fc1e1bb666e5a9f09404abbdcba465301b3dc064ecfde4)
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument output_file_extension", value=output_file_extension, expected_type=type_hints["output_file_extension"])
            check_type(argname="argument record_construct_metadata", value=record_construct_metadata, expected_type=type_hints["record_construct_metadata"])
            check_type(argname="argument resolvers", value=resolvers, expected_type=type_hints["resolvers"])
            check_type(argname="argument yaml_output_type", value=yaml_output_type, expected_type=type_hints["yaml_output_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if outdir is not None:
            self._values["outdir"] = outdir
        if output_file_extension is not None:
            self._values["output_file_extension"] = output_file_extension
        if record_construct_metadata is not None:
            self._values["record_construct_metadata"] = record_construct_metadata
        if resolvers is not None:
            self._values["resolvers"] = resolvers
        if yaml_output_type is not None:
            self._values["yaml_output_type"] = yaml_output_type

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The directory to output Kubernetes manifests.

        If you synthesize your application using ``cdk8s synth``, you must
        also pass this value to the CLI using the ``--output`` option or
        the ``output`` property in the ``cdk8s.yaml`` configuration file.
        Otherwise, the CLI will not know about the output directory,
        and synthesis will fail.

        This property is intended for internal and testing use.

        :default: - CDK8S_OUTDIR if defined, otherwise "dist"
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_file_extension(self) -> typing.Optional[builtins.str]:
        '''The file extension to use for rendered YAML files.

        :default: .k8s.yaml
        '''
        result = self._values.get("output_file_extension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_construct_metadata(self) -> typing.Optional[builtins.bool]:
        '''When set to true, the output directory will contain a ``construct-metadata.json`` file that holds construct related metadata on every resource in the app.

        :default: false
        '''
        result = self._values.get("record_construct_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resolvers(self) -> typing.Optional[typing.List["IResolver"]]:
        '''A list of resolvers that can be used to replace property values before they are written to the manifest file.

        When multiple resolvers are passed,
        they are invoked by order in the list, and only the first one that applies
        (e.g calls ``context.replaceValue``) is invoked.

        :default: - no resolvers.

        :see: https://cdk8s.io/docs/latest/basics/app/#resolvers
        '''
        result = self._values.get("resolvers")
        return typing.cast(typing.Optional[typing.List["IResolver"]], result)

    @builtins.property
    def yaml_output_type(self) -> typing.Optional["YamlOutputType"]:
        '''How to divide the YAML output into files.

        :default: YamlOutputType.FILE_PER_CHART
        '''
        result = self._values.get("yaml_output_type")
        return typing.cast(typing.Optional["YamlOutputType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Chart(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.Chart",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param disable_resource_name_hashes: The autogenerated resource name by default is suffixed with a stable hash of the construct path. Setting this property to true drops the hash suffix. Default: false
        :param labels: Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac62dbd05c99a5228dff367434c3e3fca0fb00c841ecd71382b9acd3fc1e30d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ChartProps(
            disable_resource_name_hashes=disable_resource_name_hashes,
            labels=labels,
            namespace=namespace,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isChart")
    @builtins.classmethod
    def is_chart(cls, x: typing.Any) -> builtins.bool:
        '''Return whether the given object is a Chart.

        We do attribute detection since we can't reliably use 'instanceof'.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac1ee14ad96a56047185b46392b2fba722962d47ed4174705c5dc48101cec6e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isChart", [x]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, c: _constructs_77d1e7e8.IConstruct) -> "Chart":
        '''Finds the chart in which a node is defined.

        :param c: a construct node.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3591e786c1053dcfd71742c41befcbdacfce2fb416c37a182e0cdd7968ae81)
            check_type(argname="argument c", value=c, expected_type=type_hints["c"])
        return typing.cast("Chart", jsii.sinvoke(cls, "of", [c]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: _constructs_77d1e7e8.IConstruct) -> None:
        '''Create a dependency between this Chart and other constructs.

        These can be other ApiObjects, Charts, or custom.

        :param dependencies: the dependencies to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__932e2ddf3b649962a0914218bc529f30c50bf5d7ca654cc994f8a3084c93c717)
            check_type(argname="argument dependencies", value=dependencies, expected_type=typing.Tuple[type_hints["dependencies"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDependency", [*dependencies]))

    @jsii.member(jsii_name="generateObjectName")
    def generate_object_name(self, api_object: ApiObject) -> builtins.str:
        '''Generates a app-unique name for an object given it's construct node path.

        Different resource types may have different constraints on names
        (``metadata.name``). The previous version of the name generator was
        compatible with DNS_SUBDOMAIN but not with DNS_LABEL.

        For example, ``Deployment`` names must comply with DNS_SUBDOMAIN while
        ``Service`` names must comply with DNS_LABEL.

        Since there is no formal specification for this, the default name
        generation scheme for kubernetes objects in cdk8s was changed to DNS_LABEL,
        since it’s the common denominator for all kubernetes resources
        (supposedly).

        You can override this method if you wish to customize object names at the
        chart level.

        :param api_object: The API object to generate a name for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15771e9e29c981b37d0997432bf0647e396050fd6c07b9241625bfb3e542d7ec)
            check_type(argname="argument api_object", value=api_object, expected_type=type_hints["api_object"])
        return typing.cast(builtins.str, jsii.invoke(self, "generateObjectName", [api_object]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        '''Renders this chart to a set of Kubernetes JSON resources.

        :return: array of resource manifests
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "toJson", []))

    @builtins.property
    @jsii.member(jsii_name="apiObjects")
    def api_objects(self) -> typing.List[ApiObject]:
        '''Returns all the included API objects.'''
        return typing.cast(typing.List[ApiObject], jsii.get(self, "apiObjects"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Labels applied to all resources in this chart.

        This is an immutable copy.
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The default namespace for all objects in this chart.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespace"))


@jsii.data_type(
    jsii_type="cdk8s.ChartProps",
    jsii_struct_bases=[],
    name_mapping={
        "disable_resource_name_hashes": "disableResourceNameHashes",
        "labels": "labels",
        "namespace": "namespace",
    },
)
class ChartProps:
    def __init__(
        self,
        *,
        disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable_resource_name_hashes: The autogenerated resource name by default is suffixed with a stable hash of the construct path. Setting this property to true drops the hash suffix. Default: false
        :param labels: Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__587cc3f5a3d7a6cc9a5690888b75875a8059bcf784bfae23dedf362a06743ee3)
            check_type(argname="argument disable_resource_name_hashes", value=disable_resource_name_hashes, expected_type=type_hints["disable_resource_name_hashes"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_resource_name_hashes is not None:
            self._values["disable_resource_name_hashes"] = disable_resource_name_hashes
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def disable_resource_name_hashes(self) -> typing.Optional[builtins.bool]:
        '''The autogenerated resource name by default is suffixed with a stable hash of the construct path.

        Setting this property to true drops the hash suffix.

        :default: false
        '''
        result = self._values.get("disable_resource_name_hashes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to all resources in this chart.

        :default: - no common labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The default namespace for all objects defined in this chart (directly or indirectly).

        This namespace will only apply to objects that don't have a
        ``namespace`` explicitly defined for them.

        :default: - no namespace is synthesized (usually this implies "default")
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChartProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Cron(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Cron"):
    '''Represents a cron schedule.'''

    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        '''
        cron_options = CronOptions(
            day=day, hour=hour, minute=minute, month=month, week_day=week_day
        )

        jsii.create(self.__class__, self, [cron_options])

    @jsii.member(jsii_name="annually")
    @builtins.classmethod
    def annually(cls) -> "Cron":
        '''Create a cron schedule which runs first day of January every year.'''
        return typing.cast("Cron", jsii.sinvoke(cls, "annually", []))

    @jsii.member(jsii_name="daily")
    @builtins.classmethod
    def daily(cls) -> "Cron":
        '''Create a cron schedule which runs every day at midnight.'''
        return typing.cast("Cron", jsii.sinvoke(cls, "daily", []))

    @jsii.member(jsii_name="everyMinute")
    @builtins.classmethod
    def every_minute(cls) -> "Cron":
        '''Create a cron schedule which runs every minute.'''
        return typing.cast("Cron", jsii.sinvoke(cls, "everyMinute", []))

    @jsii.member(jsii_name="hourly")
    @builtins.classmethod
    def hourly(cls) -> "Cron":
        '''Create a cron schedule which runs every hour.'''
        return typing.cast("Cron", jsii.sinvoke(cls, "hourly", []))

    @jsii.member(jsii_name="monthly")
    @builtins.classmethod
    def monthly(cls) -> "Cron":
        '''Create a cron schedule which runs first day of every month.'''
        return typing.cast("Cron", jsii.sinvoke(cls, "monthly", []))

    @jsii.member(jsii_name="schedule")
    @builtins.classmethod
    def schedule(
        cls,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> "Cron":
        '''Create a custom cron schedule from a set of cron fields.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        '''
        options = CronOptions(
            day=day, hour=hour, minute=minute, month=month, week_day=week_day
        )

        return typing.cast("Cron", jsii.sinvoke(cls, "schedule", [options]))

    @jsii.member(jsii_name="weekly")
    @builtins.classmethod
    def weekly(cls) -> "Cron":
        '''Create a cron schedule which runs every week on Sunday.'''
        return typing.cast("Cron", jsii.sinvoke(cls, "weekly", []))

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        '''Retrieve the expression for this schedule.'''
        return typing.cast(builtins.str, jsii.get(self, "expressionString"))


@jsii.data_type(
    jsii_type="cdk8s.CronOptions",
    jsii_struct_bases=[],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
    },
)
class CronOptions:
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*'

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2c750519e19d88bad3a5fad0784148fee43e03a55bddfc61438556ab6bb698)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''The day of the month to run this rule at.

        :default: - Every day of the month
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''The hour to run this rule at.

        :default: - Every hour
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''The minute to run this rule at.

        :default: - Every minute
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''The month to run this rule at.

        :default: - Every month
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''The day of the week to run this rule at.

        :default: - Any day of the week
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DependencyGraph(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.DependencyGraph"):
    '''Represents the dependency graph for a given Node.

    This graph includes the dependency relationships between all nodes in the
    node (construct) sub-tree who's root is this Node.

    Note that this means that lonely nodes (no dependencies and no dependants) are also included in this graph as
    childless children of the root node of the graph.

    The graph does not include cross-scope dependencies. That is, if a child on the current scope depends on a node
    from a different scope, that relationship is not represented in this graph.
    '''

    def __init__(self, node: _constructs_77d1e7e8.Node) -> None:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e42df9fe8e54748af3dd0e25616d4ea57a51e241dfc6972407f4bce78ced02)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        jsii.create(self.__class__, self, [node])

    @jsii.member(jsii_name="topology")
    def topology(self) -> typing.List[_constructs_77d1e7e8.IConstruct]:
        '''
        :see: Vertex.topology ()
        '''
        return typing.cast(typing.List[_constructs_77d1e7e8.IConstruct], jsii.invoke(self, "topology", []))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "DependencyVertex":
        '''Returns the root of the graph.

        Note that this vertex will always have ``null`` as its ``.value`` since it is an artifical root
        that binds all the connected spaces of the graph.
        '''
        return typing.cast("DependencyVertex", jsii.get(self, "root"))


class DependencyVertex(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.DependencyVertex"):
    '''Represents a vertex in the graph.

    The value of each vertex is an ``IConstruct`` that is accessible via the ``.value`` getter.
    '''

    def __init__(
        self,
        value: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7903f01cf4bab7177bfc66d8e5acb3e99c019af8082b816e72beee89ab639c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.member(jsii_name="addChild")
    def add_child(self, dep: "DependencyVertex") -> None:
        '''Adds a vertex as a dependency of the current node.

        Also updates the parents of ``dep``, so that it contains this node as a parent.

        This operation will fail in case it creates a cycle in the graph.

        :param dep: The dependency.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3c1a1b4df66c2406e31123378a2ba7139aab5e261b7253d3771af9c0ed2922)
            check_type(argname="argument dep", value=dep, expected_type=type_hints["dep"])
        return typing.cast(None, jsii.invoke(self, "addChild", [dep]))

    @jsii.member(jsii_name="topology")
    def topology(self) -> typing.List[_constructs_77d1e7e8.IConstruct]:
        '''Returns a topologically sorted array of the constructs in the sub-graph.'''
        return typing.cast(typing.List[_constructs_77d1e7e8.IConstruct], jsii.invoke(self, "topology", []))

    @builtins.property
    @jsii.member(jsii_name="inbound")
    def inbound(self) -> typing.List["DependencyVertex"]:
        '''Returns the parents of the vertex (i.e dependants).'''
        return typing.cast(typing.List["DependencyVertex"], jsii.get(self, "inbound"))

    @builtins.property
    @jsii.member(jsii_name="outbound")
    def outbound(self) -> typing.List["DependencyVertex"]:
        '''Returns the children of the vertex (i.e dependencies).'''
        return typing.cast(typing.List["DependencyVertex"], jsii.get(self, "outbound"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[_constructs_77d1e7e8.IConstruct]:
        '''Returns the IConstruct this graph vertex represents.

        ``null`` in case this is the root of the graph.
        '''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.IConstruct], jsii.get(self, "value"))


class Duration(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Duration"):
    '''Represents a length of time.

    The amount can be specified either as a literal value (e.g: ``10``) which
    cannot be negative.
    '''

    @jsii.member(jsii_name="days")
    @builtins.classmethod
    def days(cls, amount: jsii.Number) -> "Duration":
        '''Create a Duration representing an amount of days.

        :param amount: the amount of Days the ``Duration`` will represent.

        :return: a new ``Duration`` representing ``amount`` Days.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ce164c8ddb62412fbc9134b2a57787b49dbf637a9072ddd8cb35ef9545a083)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Duration", jsii.sinvoke(cls, "days", [amount]))

    @jsii.member(jsii_name="hours")
    @builtins.classmethod
    def hours(cls, amount: jsii.Number) -> "Duration":
        '''Create a Duration representing an amount of hours.

        :param amount: the amount of Hours the ``Duration`` will represent.

        :return: a new ``Duration`` representing ``amount`` Hours.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49be32303a4d56be9a6c9d9fb6e759ce5a4a30d954642474baf29f1b47d6e5bb)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Duration", jsii.sinvoke(cls, "hours", [amount]))

    @jsii.member(jsii_name="millis")
    @builtins.classmethod
    def millis(cls, amount: jsii.Number) -> "Duration":
        '''Create a Duration representing an amount of milliseconds.

        :param amount: the amount of Milliseconds the ``Duration`` will represent.

        :return: a new ``Duration`` representing ``amount`` ms.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8a2ef493eb7238ccbd43ee0e3ff2da5e62c5d6d51fc2d127776eba261980e5)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Duration", jsii.sinvoke(cls, "millis", [amount]))

    @jsii.member(jsii_name="minutes")
    @builtins.classmethod
    def minutes(cls, amount: jsii.Number) -> "Duration":
        '''Create a Duration representing an amount of minutes.

        :param amount: the amount of Minutes the ``Duration`` will represent.

        :return: a new ``Duration`` representing ``amount`` Minutes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65e8ee772805167d1dcc9fe3132d51039baf5cc182a0d12041c68495d4a3661)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Duration", jsii.sinvoke(cls, "minutes", [amount]))

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, duration: builtins.str) -> "Duration":
        '''Parse a period formatted according to the ISO 8601 standard.

        :param duration: an ISO-formtted duration to be parsed.

        :return: the parsed ``Duration``.

        :see: https://www.iso.org/fr/standard/70907.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0db6a272abc31ecb50e8a143af3a1c2e63de57d4793ad8a17a96d0454f2037)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast("Duration", jsii.sinvoke(cls, "parse", [duration]))

    @jsii.member(jsii_name="seconds")
    @builtins.classmethod
    def seconds(cls, amount: jsii.Number) -> "Duration":
        '''Create a Duration representing an amount of seconds.

        :param amount: the amount of Seconds the ``Duration`` will represent.

        :return: a new ``Duration`` representing ``amount`` Seconds.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c36c45ae685aa42e43f0df90cff9bc72a4d096750fe1eb4ba29aef794d09410)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Duration", jsii.sinvoke(cls, "seconds", [amount]))

    @jsii.member(jsii_name="toDays")
    def to_days(
        self,
        *,
        integral: typing.Optional[builtins.bool] = None,
    ) -> jsii.Number:
        '''Return the total number of days in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        :return: the value of this ``Duration`` expressed in Days.
        '''
        opts = TimeConversionOptions(integral=integral)

        return typing.cast(jsii.Number, jsii.invoke(self, "toDays", [opts]))

    @jsii.member(jsii_name="toHours")
    def to_hours(
        self,
        *,
        integral: typing.Optional[builtins.bool] = None,
    ) -> jsii.Number:
        '''Return the total number of hours in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        :return: the value of this ``Duration`` expressed in Hours.
        '''
        opts = TimeConversionOptions(integral=integral)

        return typing.cast(jsii.Number, jsii.invoke(self, "toHours", [opts]))

    @jsii.member(jsii_name="toHumanString")
    def to_human_string(self) -> builtins.str:
        '''Turn this duration into a human-readable string.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toHumanString", []))

    @jsii.member(jsii_name="toIsoString")
    def to_iso_string(self) -> builtins.str:
        '''Return an ISO 8601 representation of this period.

        :return: a string starting with 'PT' describing the period

        :see: https://www.iso.org/fr/standard/70907.html
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toIsoString", []))

    @jsii.member(jsii_name="toMilliseconds")
    def to_milliseconds(
        self,
        *,
        integral: typing.Optional[builtins.bool] = None,
    ) -> jsii.Number:
        '''Return the total number of milliseconds in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        :return: the value of this ``Duration`` expressed in Milliseconds.
        '''
        opts = TimeConversionOptions(integral=integral)

        return typing.cast(jsii.Number, jsii.invoke(self, "toMilliseconds", [opts]))

    @jsii.member(jsii_name="toMinutes")
    def to_minutes(
        self,
        *,
        integral: typing.Optional[builtins.bool] = None,
    ) -> jsii.Number:
        '''Return the total number of minutes in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        :return: the value of this ``Duration`` expressed in Minutes.
        '''
        opts = TimeConversionOptions(integral=integral)

        return typing.cast(jsii.Number, jsii.invoke(self, "toMinutes", [opts]))

    @jsii.member(jsii_name="toSeconds")
    def to_seconds(
        self,
        *,
        integral: typing.Optional[builtins.bool] = None,
    ) -> jsii.Number:
        '''Return the total number of seconds in this Duration.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true

        :return: the value of this ``Duration`` expressed in Seconds.
        '''
        opts = TimeConversionOptions(integral=integral)

        return typing.cast(jsii.Number, jsii.invoke(self, "toSeconds", [opts]))

    @jsii.member(jsii_name="unitLabel")
    def unit_label(self) -> builtins.str:
        '''Return unit of Duration.'''
        return typing.cast(builtins.str, jsii.invoke(self, "unitLabel", []))


@jsii.data_type(
    jsii_type="cdk8s.GroupVersionKind",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "kind": "kind"},
)
class GroupVersionKind:
    def __init__(self, *, api_version: builtins.str, kind: builtins.str) -> None:
        '''
        :param api_version: The object's API version (e.g. ``authorization.k8s.io/v1``).
        :param kind: The object kind.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5654dc50c8f0fc983e64c60bc59a01c4a0ebeb3357670346908003a338a42d2d)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_version": api_version,
            "kind": kind,
        }

    @builtins.property
    def api_version(self) -> builtins.str:
        '''The object's API version (e.g. ``authorization.k8s.io/v1``).'''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''The object kind.'''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupVersionKind(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s.HelmProps",
    jsii_struct_bases=[],
    name_mapping={
        "chart": "chart",
        "helm_executable": "helmExecutable",
        "helm_flags": "helmFlags",
        "namespace": "namespace",
        "release_name": "releaseName",
        "repo": "repo",
        "values": "values",
        "version": "version",
    },
)
class HelmProps:
    def __init__(
        self,
        *,
        chart: builtins.str,
        helm_executable: typing.Optional[builtins.str] = None,
        helm_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        release_name: typing.Optional[builtins.str] = None,
        repo: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for ``Helm``.

        :param chart: The chart name to use. It can be a chart from a helm repository or a local directory. This name is passed to ``helm template`` and has all the relevant semantics.
        :param helm_executable: The local helm executable to use in order to create the manifest the chart. Default: "helm"
        :param helm_flags: Additional flags to add to the ``helm`` execution. Default: []
        :param namespace: Scope all resources in to a given namespace.
        :param release_name: The release name. Default: - if unspecified, a name will be allocated based on the construct path
        :param repo: Chart repository url where to locate the requested chart.
        :param values: Values to pass to the chart. Default: - If no values are specified, chart will use the defaults.
        :param version: Version constraint for the chart version to use. This constraint can be a specific tag (e.g. 1.1.1) or it may reference a valid range (e.g. ^2.0.0). If this is not specified, the latest version is used This name is passed to ``helm template --version`` and has all the relevant semantics.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d491a2276602d3378938ffe40a1ca86f3a51816e3a51fd829aeb41e96630e966)
            check_type(argname="argument chart", value=chart, expected_type=type_hints["chart"])
            check_type(argname="argument helm_executable", value=helm_executable, expected_type=type_hints["helm_executable"])
            check_type(argname="argument helm_flags", value=helm_flags, expected_type=type_hints["helm_flags"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument release_name", value=release_name, expected_type=type_hints["release_name"])
            check_type(argname="argument repo", value=repo, expected_type=type_hints["repo"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "chart": chart,
        }
        if helm_executable is not None:
            self._values["helm_executable"] = helm_executable
        if helm_flags is not None:
            self._values["helm_flags"] = helm_flags
        if namespace is not None:
            self._values["namespace"] = namespace
        if release_name is not None:
            self._values["release_name"] = release_name
        if repo is not None:
            self._values["repo"] = repo
        if values is not None:
            self._values["values"] = values
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def chart(self) -> builtins.str:
        '''The chart name to use. It can be a chart from a helm repository or a local directory.

        This name is passed to ``helm template`` and has all the relevant semantics.

        Example::

            "bitnami/redis"
        '''
        result = self._values.get("chart")
        assert result is not None, "Required property 'chart' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def helm_executable(self) -> typing.Optional[builtins.str]:
        '''The local helm executable to use in order to create the manifest the chart.

        :default: "helm"
        '''
        result = self._values.get("helm_executable")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def helm_flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional flags to add to the ``helm`` execution.

        :default: []
        '''
        result = self._values.get("helm_flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Scope all resources in to a given namespace.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_name(self) -> typing.Optional[builtins.str]:
        '''The release name.

        :default: - if unspecified, a name will be allocated based on the construct path

        :see: https://helm.sh/docs/intro/using_helm/#three-big-concepts
        '''
        result = self._values.get("release_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo(self) -> typing.Optional[builtins.str]:
        '''Chart repository url where to locate the requested chart.'''
        result = self._values.get("repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Values to pass to the chart.

        :default: - If no values are specified, chart will use the defaults.
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version constraint for the chart version to use.

        This constraint can be a specific tag (e.g. 1.1.1)
        or it may reference a valid range (e.g. ^2.0.0).
        If this is not specified, the latest version is used

        This name is passed to ``helm template --version`` and has all the relevant semantics.

        Example::

            "^2.0.0"
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk8s.IAnyProducer")
class IAnyProducer(typing_extensions.Protocol):
    @jsii.member(jsii_name="produce")
    def produce(self) -> typing.Any:
        ...


class _IAnyProducerProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk8s.IAnyProducer"

    @jsii.member(jsii_name="produce")
    def produce(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "produce", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAnyProducer).__jsii_proxy_class__ = lambda : _IAnyProducerProxy


@jsii.interface(jsii_type="cdk8s.IResolver")
class IResolver(typing_extensions.Protocol):
    '''Contract for resolver objects.'''

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "ResolutionContext") -> None:
        '''This function is invoked on every property during cdk8s synthesis.

        To replace a value, implementations must invoke ``context.replaceValue``.

        :param context: -
        '''
        ...


class _IResolverProxy:
    '''Contract for resolver objects.'''

    __jsii_type__: typing.ClassVar[str] = "cdk8s.IResolver"

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "ResolutionContext") -> None:
        '''This function is invoked on every property during cdk8s synthesis.

        To replace a value, implementations must invoke ``context.replaceValue``.

        :param context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5ca202bc9e3dd6c5b464aae10cd956d0ccfeabb617701f2f25c6845a60289e)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(None, jsii.invoke(self, "resolve", [context]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResolver).__jsii_proxy_class__ = lambda : _IResolverProxy


@jsii.implements(IResolver)
class ImplicitTokenResolver(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.ImplicitTokenResolver",
):
    '''Resolves implicit tokens.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "ResolutionContext") -> None:
        '''This function is invoked on every property during cdk8s synthesis.

        To replace a value, implementations must invoke ``context.replaceValue``.

        :param context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6e42d5af180bdfb92d72b8157aae3261fc21d0f10885350023690febf6cbae)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(None, jsii.invoke(self, "resolve", [context]))


class Include(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.Include",
):
    '''Reads a YAML manifest from a file or a URL and defines all resources as API objects within the defined scope.

    The names (``metadata.name``) of imported resources will be preserved as-is
    from the manifest.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        url: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param url: Local file path or URL which includes a Kubernetes YAML manifest.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7ad4649d7e1e318f4c5cfd1b6f285d8481cd49825b775d4fcdc15c2f1257c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IncludeProps(url=url)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiObjects")
    def api_objects(self) -> typing.List[ApiObject]:
        '''Returns all the included API objects.'''
        return typing.cast(typing.List[ApiObject], jsii.get(self, "apiObjects"))


@jsii.data_type(
    jsii_type="cdk8s.IncludeProps",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class IncludeProps:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: Local file path or URL which includes a Kubernetes YAML manifest.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a5cdbd9f75abfa5f7670e54b759fcd6f7c402051f050a5e1aa1f73ac5eaf3e)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''Local file path or URL which includes a Kubernetes YAML manifest.

        Example::

            mymanifest.yaml
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JsonPatch(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.JsonPatch"):
    '''Utility for applying RFC-6902 JSON-Patch to a document.

    Use the the ``JsonPatch.apply(doc, ...ops)`` function to apply a set of
    operations to a JSON document and return the result.

    Operations can be created using the factory methods ``JsonPatch.add()``,
    ``JsonPatch.remove()``, etc.

    Example::

        const output = JsonPatch.apply(input,
         JsonPatch.replace('/world/hi/there', 'goodbye'),
         JsonPatch.add('/world/foo/', 'boom'),
         JsonPatch.remove('/hello'));
    '''

    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''Adds a value to an object or inserts it into an array.

        In the case of an
        array, the value is inserted before the given index. The - character can be
        used instead of an index to insert at the end of an array.

        :param path: -
        :param value: -

        Example::

            JsonPatch.add('/biscuits/1', { "name": "Ginger Nut" })
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e51633af9c45ea1ac2cc618c9ade6d085cb4b0e47240e794a287cacb94a4c59)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "add", [path, value]))

    @jsii.member(jsii_name="apply")
    @builtins.classmethod
    def apply(cls, document: typing.Any, *ops: "JsonPatch") -> typing.Any:
        '''Applies a set of JSON-Patch (RFC-6902) operations to ``document`` and returns the result.

        :param document: The document to patch.
        :param ops: The operations to apply.

        :return: The result document
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cc5db94fd68d7c20469e460e266007085d6d5b5e8541e8796ba2c1c8106dd8)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument ops", value=ops, expected_type=typing.Tuple[type_hints["ops"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.Any, jsii.sinvoke(cls, "apply", [document, *ops]))

    @jsii.member(jsii_name="copy")
    @builtins.classmethod
    def copy(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''Copies a value from one location to another within the JSON document.

        Both
        from and path are JSON Pointers.

        :param from_: -
        :param path: -

        Example::

            JsonPatch.copy('/biscuits/0', '/best_biscuit')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad568ab5b16454e5e827da5f437072e9e3555ccc7b7553a697903192a1b3eb5)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "copy", [from_, path]))

    @jsii.member(jsii_name="move")
    @builtins.classmethod
    def move(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''Moves a value from one location to the other.

        Both from and path are JSON Pointers.

        :param from_: -
        :param path: -

        Example::

            JsonPatch.move('/biscuits', '/cookies')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de55a7c5105ba84ccdf0e9638671d4816ff4422d1895bef75b8aa1047454ad69)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "move", [from_, path]))

    @jsii.member(jsii_name="remove")
    @builtins.classmethod
    def remove(cls, path: builtins.str) -> "JsonPatch":
        '''Removes a value from an object or array.

        :param path: -

        Example::

            JsonPatch.remove('/biscuits/0')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aed01338ac97e26df8aa53e7f354b7fc10275fcf1d9814b024cc78d755f21ed)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "remove", [path]))

    @jsii.member(jsii_name="replace")
    @builtins.classmethod
    def replace(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''Replaces a value.

        Equivalent to a “remove” followed by an “add”.

        :param path: -
        :param value: -

        Example::

            JsonPatch.replace('/biscuits/0/name', 'Chocolate Digestive')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b103a48708f207593ef910f1bddfd661aef834c5086afbbdba659c0103dfcab)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "replace", [path, value]))

    @jsii.member(jsii_name="test")
    @builtins.classmethod
    def test(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''Tests that the specified value is set in the document.

        If the test fails,
        then the patch as a whole should not apply.

        :param path: -
        :param value: -

        Example::

            JsonPatch.test('/best_biscuit/name', 'Choco Leibniz')
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9005a324c07bb509dbb3733b53e421cbf2e1220e48c561f969d97268d097c69e)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "test", [path, value]))


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Lazy"):
    @jsii.member(jsii_name="any")
    @builtins.classmethod
    def any(cls, producer: IAnyProducer) -> typing.Any:
        '''
        :param producer: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66ad4b91ba96e5ece2b03dda56e66ac135a52e42ec1dc812633365d043b45da)
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        return typing.cast(typing.Any, jsii.sinvoke(cls, "any", [producer]))

    @jsii.member(jsii_name="produce")
    def produce(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "produce", []))


@jsii.implements(IResolver)
class LazyResolver(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.LazyResolver"):
    '''Resolvers instanecs of ``Lazy``.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "ResolutionContext") -> None:
        '''This function is invoked on every property during cdk8s synthesis.

        To replace a value, implementations must invoke ``context.replaceValue``.

        :param context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af8596daa9e070048c5bd02166ac52f48073da14c659b03be91af3d002a76b8)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(None, jsii.invoke(self, "resolve", [context]))


@jsii.data_type(
    jsii_type="cdk8s.NameOptions",
    jsii_struct_bases=[],
    name_mapping={
        "delimiter": "delimiter",
        "extra": "extra",
        "include_hash": "includeHash",
        "max_len": "maxLen",
    },
)
class NameOptions:
    def __init__(
        self,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        extra: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_hash: typing.Optional[builtins.bool] = None,
        max_len: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Options for name generation.

        :param delimiter: Delimiter to use between components. Default: "-"
        :param extra: Extra components to include in the name. Default: [] use the construct path components
        :param include_hash: Include a short hash as last part of the name. Default: true
        :param max_len: Maximum allowed length for the name. Default: 63
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ff5aa57fdaa34956720956edd71f9da68fb2936d50787accb5cd16713811035)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument extra", value=extra, expected_type=type_hints["extra"])
            check_type(argname="argument include_hash", value=include_hash, expected_type=type_hints["include_hash"])
            check_type(argname="argument max_len", value=max_len, expected_type=type_hints["max_len"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if extra is not None:
            self._values["extra"] = extra
        if include_hash is not None:
            self._values["include_hash"] = include_hash
        if max_len is not None:
            self._values["max_len"] = max_len

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Delimiter to use between components.

        :default: "-"
        '''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Extra components to include in the name.

        :default: [] use the construct path components
        '''
        result = self._values.get("extra")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_hash(self) -> typing.Optional[builtins.bool]:
        '''Include a short hash as last part of the name.

        :default: true
        '''
        result = self._values.get("include_hash")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_len(self) -> typing.Optional[jsii.Number]:
        '''Maximum allowed length for the name.

        :default: 63
        '''
        result = self._values.get("max_len")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NameOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Names(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Names"):
    '''Utilities for generating unique and stable names.'''

    @jsii.member(jsii_name="toDnsLabel")
    @builtins.classmethod
    def to_dns_label(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        extra: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_hash: typing.Optional[builtins.bool] = None,
        max_len: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''Generates a unique and stable name compatible DNS_LABEL from RFC-1123 from a path.

        The generated name will:

        - contain at most 63 characters
        - contain only lowercase alphanumeric characters or ‘-’
        - start with an alphanumeric character
        - end with an alphanumeric character

        The generated name will have the form:
        --..--

        Where  are the path components (assuming they are is separated by
        "/").

        Note that if the total length is longer than 63 characters, we will trim
        the first components since the last components usually encode more meaning.

        :param scope: The construct for which to render the DNS label.
        :param delimiter: Delimiter to use between components. Default: "-"
        :param extra: Extra components to include in the name. Default: [] use the construct path components
        :param include_hash: Include a short hash as last part of the name. Default: true
        :param max_len: Maximum allowed length for the name. Default: 63

        :link: https://tools.ietf.org/html/rfc1123
        :throws:

        if any of the components do not adhere to naming constraints or
        length.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2694a7308fa083bea22907798345bf812c9e9a723f8832b8f0a8bbef8565f836)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = NameOptions(
            delimiter=delimiter,
            extra=extra,
            include_hash=include_hash,
            max_len=max_len,
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "toDnsLabel", [scope, options]))

    @jsii.member(jsii_name="toLabelValue")
    @builtins.classmethod
    def to_label_value(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        *,
        delimiter: typing.Optional[builtins.str] = None,
        extra: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_hash: typing.Optional[builtins.bool] = None,
        max_len: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        '''Generates a unique and stable name compatible label key name segment and label value from a path.

        The name segment is required and must be 63 characters or less, beginning
        and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-),
        underscores (_), dots (.), and alphanumerics between.

        Valid label values must be 63 characters or less and must be empty or
        begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes
        (-), underscores (_), dots (.), and alphanumerics between.

        The generated name will have the form:
        ..

        Where  are the path components (assuming they are is separated by
        "/").

        Note that if the total length is longer than 63 characters, we will trim
        the first components since the last components usually encode more meaning.

        :param scope: The construct for which to render the DNS label.
        :param delimiter: Delimiter to use between components. Default: "-"
        :param extra: Extra components to include in the name. Default: [] use the construct path components
        :param include_hash: Include a short hash as last part of the name. Default: true
        :param max_len: Maximum allowed length for the name. Default: 63

        :link: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set
        :throws:

        if any of the components do not adhere to naming constraints or
        length.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b42b2ea1a8f79926d2acae92335ea6375b89dbd75da580f0ded3902cfce829)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = NameOptions(
            delimiter=delimiter,
            extra=extra,
            include_hash=include_hash,
            max_len=max_len,
        )

        return typing.cast(builtins.str, jsii.sinvoke(cls, "toLabelValue", [scope, options]))


@jsii.implements(IResolver)
class NumberStringUnionResolver(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.NumberStringUnionResolver",
):
    '''Resolves union types that allow using either number or string (as generated by the CLI).

    E.g IntOrString, Quantity, ...
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "ResolutionContext") -> None:
        '''This function is invoked on every property during cdk8s synthesis.

        To replace a value, implementations must invoke ``context.replaceValue``.

        :param context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0e0eaeefa0726153706af3c2183eab46ff6dadfe4d6d943600131d6bf2657e)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(None, jsii.invoke(self, "resolve", [context]))


@jsii.data_type(
    jsii_type="cdk8s.OwnerReference",
    jsii_struct_bases=[],
    name_mapping={
        "api_version": "apiVersion",
        "kind": "kind",
        "name": "name",
        "uid": "uid",
        "block_owner_deletion": "blockOwnerDeletion",
        "controller": "controller",
    },
)
class OwnerReference:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        uid: builtins.str,
        block_owner_deletion: typing.Optional[builtins.bool] = None,
        controller: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''OwnerReference contains enough information to let you identify an owning object.

        An owning object must be in the same namespace as the dependent, or
        be cluster-scoped, so there is no namespace field.

        :param api_version: API version of the referent.
        :param kind: Kind of the referent.
        :param name: Name of the referent.
        :param uid: UID of the referent.
        :param block_owner_deletion: If true, AND if the owner has the "foregroundDeletion" finalizer, then the owner cannot be deleted from the key-value store until this reference is removed. Defaults to false. To set this field, a user needs "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be returned. Default: false. To set this field, a user needs "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be returned.
        :param controller: If true, this reference points to the managing controller.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cfb6f34de5a3f7c962fcc2da2dfae03bc583bfafc2393157bd81af722b432b)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            check_type(argname="argument block_owner_deletion", value=block_owner_deletion, expected_type=type_hints["block_owner_deletion"])
            check_type(argname="argument controller", value=controller, expected_type=type_hints["controller"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_version": api_version,
            "kind": kind,
            "name": name,
            "uid": uid,
        }
        if block_owner_deletion is not None:
            self._values["block_owner_deletion"] = block_owner_deletion
        if controller is not None:
            self._values["controller"] = controller

    @builtins.property
    def api_version(self) -> builtins.str:
        '''API version of the referent.'''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Kind of the referent.

        :see: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the referent.

        :see: http://kubernetes.io/docs/user-guide/identifiers#names
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uid(self) -> builtins.str:
        '''UID of the referent.

        :see: http://kubernetes.io/docs/user-guide/identifiers#uids
        '''
        result = self._values.get("uid")
        assert result is not None, "Required property 'uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def block_owner_deletion(self) -> typing.Optional[builtins.bool]:
        '''If true, AND if the owner has the "foregroundDeletion" finalizer, then the owner cannot be deleted from the key-value store until this reference is removed.

        Defaults to false. To set this field, a user needs "delete"
        permission of the owner, otherwise 422 (Unprocessable Entity) will be
        returned.

        :default:

        false. To set this field, a user needs "delete" permission of the
        owner, otherwise 422 (Unprocessable Entity) will be returned.
        '''
        result = self._values.get("block_owner_deletion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def controller(self) -> typing.Optional[builtins.bool]:
        '''If true, this reference points to the managing controller.'''
        result = self._values.get("controller")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OwnerReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResolutionContext(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.ResolutionContext"):
    '''Context object for a specific resolution process.'''

    def __init__(
        self,
        obj: ApiObject,
        key: typing.Sequence[builtins.str],
        value: typing.Any,
    ) -> None:
        '''
        :param obj: Which ApiObject is currently being resolved.
        :param key: Which key is currently being resolved.
        :param value: The value associated to the key currently being resolved.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6d87f260728f933d112797dca80dbcf9281ea35eadb4bff9f6a38a1cf78a1e)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [obj, key, value])

    @jsii.member(jsii_name="replaceValue")
    def replace_value(self, new_value: typing.Any) -> None:
        '''Replaces the original value in this resolution context with a new value.

        The new value is what will end up in the manifest.

        :param new_value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0dc17edb4458da9d06ff82b9c151690ce17fbe2dfdfe623b5f7415cdcd5071)
            check_type(argname="argument new_value", value=new_value, expected_type=type_hints["new_value"])
        return typing.cast(None, jsii.invoke(self, "replaceValue", [new_value]))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.List[builtins.str]:
        '''Which key is currently being resolved.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="obj")
    def obj(self) -> ApiObject:
        '''Which ApiObject is currently being resolved.'''
        return typing.cast(ApiObject, jsii.get(self, "obj"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''The value associated to the key currently being resolved.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="replaced")
    def replaced(self) -> builtins.bool:
        '''Whether or not the value was replaced by invoking the ``replaceValue`` method.'''
        return typing.cast(builtins.bool, jsii.get(self, "replaced"))

    @replaced.setter
    def replaced(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46fc386c510b2c1129687fab66a5d8b73e229013d9438613e42b2b93bab2701f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaced", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replacedValue")
    def replaced_value(self) -> typing.Any:
        '''The replaced value that was set via the ``replaceValue`` method.'''
        return typing.cast(typing.Any, jsii.get(self, "replacedValue"))

    @replaced_value.setter
    def replaced_value(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2dafc483ec1b162f3ac5314f24a646833af290785fa69fee4e9a54bd10e1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacedValue", value) # pyright: ignore[reportArgumentType]


class Size(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Size"):
    '''Represents the amount of digital storage.

    The amount can be specified either as a literal value (e.g: ``10``) which
    cannot be negative.

    When the amount is passed as a token, unit conversion is not possible.
    '''

    @jsii.member(jsii_name="gibibytes")
    @builtins.classmethod
    def gibibytes(cls, amount: jsii.Number) -> "Size":
        '''Create a Storage representing an amount gibibytes.

        1 GiB = 1024 MiB

        :param amount: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6e3e4f8a439c63e3ed083e0d76fba9fe218a2f3f2a47515af3732dcf82fcce)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Size", jsii.sinvoke(cls, "gibibytes", [amount]))

    @jsii.member(jsii_name="kibibytes")
    @builtins.classmethod
    def kibibytes(cls, amount: jsii.Number) -> "Size":
        '''Create a Storage representing an amount kibibytes.

        1 KiB = 1024 bytes

        :param amount: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fd48faa9e664bcd03923015ba048b929be4a547ac0a2f1ef83a7bcf2a6ef88)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Size", jsii.sinvoke(cls, "kibibytes", [amount]))

    @jsii.member(jsii_name="mebibytes")
    @builtins.classmethod
    def mebibytes(cls, amount: jsii.Number) -> "Size":
        '''Create a Storage representing an amount mebibytes.

        1 MiB = 1024 KiB

        :param amount: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eecf102c3a7a867995cb1f2e0ca44a97d0c853897af7d1da6d92ea170aad88c0)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Size", jsii.sinvoke(cls, "mebibytes", [amount]))

    @jsii.member(jsii_name="pebibyte")
    @builtins.classmethod
    def pebibyte(cls, amount: jsii.Number) -> "Size":
        '''Create a Storage representing an amount pebibytes.

        1 PiB = 1024 TiB

        :param amount: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd978397137248b8c68fd5ef41aad7818510368daf79092fb8e1ff9a0478e5f)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Size", jsii.sinvoke(cls, "pebibyte", [amount]))

    @jsii.member(jsii_name="tebibytes")
    @builtins.classmethod
    def tebibytes(cls, amount: jsii.Number) -> "Size":
        '''Create a Storage representing an amount tebibytes.

        1 TiB = 1024 GiB

        :param amount: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f658d6703486a9fb30a5fb73df83a10f792ba95cd2ae69ba6436614be70497)
            check_type(argname="argument amount", value=amount, expected_type=type_hints["amount"])
        return typing.cast("Size", jsii.sinvoke(cls, "tebibytes", [amount]))

    @jsii.member(jsii_name="asString")
    def as_string(self) -> builtins.str:
        '''Returns amount with abbreviated storage unit.'''
        return typing.cast(builtins.str, jsii.invoke(self, "asString", []))

    @jsii.member(jsii_name="toGibibytes")
    def to_gibibytes(
        self,
        *,
        rounding: typing.Optional["SizeRoundingBehavior"] = None,
    ) -> jsii.Number:
        '''Return this storage as a total number of gibibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL
        '''
        opts = SizeConversionOptions(rounding=rounding)

        return typing.cast(jsii.Number, jsii.invoke(self, "toGibibytes", [opts]))

    @jsii.member(jsii_name="toKibibytes")
    def to_kibibytes(
        self,
        *,
        rounding: typing.Optional["SizeRoundingBehavior"] = None,
    ) -> jsii.Number:
        '''Return this storage as a total number of kibibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL
        '''
        opts = SizeConversionOptions(rounding=rounding)

        return typing.cast(jsii.Number, jsii.invoke(self, "toKibibytes", [opts]))

    @jsii.member(jsii_name="toMebibytes")
    def to_mebibytes(
        self,
        *,
        rounding: typing.Optional["SizeRoundingBehavior"] = None,
    ) -> jsii.Number:
        '''Return this storage as a total number of mebibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL
        '''
        opts = SizeConversionOptions(rounding=rounding)

        return typing.cast(jsii.Number, jsii.invoke(self, "toMebibytes", [opts]))

    @jsii.member(jsii_name="toPebibytes")
    def to_pebibytes(
        self,
        *,
        rounding: typing.Optional["SizeRoundingBehavior"] = None,
    ) -> jsii.Number:
        '''Return this storage as a total number of pebibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL
        '''
        opts = SizeConversionOptions(rounding=rounding)

        return typing.cast(jsii.Number, jsii.invoke(self, "toPebibytes", [opts]))

    @jsii.member(jsii_name="toTebibytes")
    def to_tebibytes(
        self,
        *,
        rounding: typing.Optional["SizeRoundingBehavior"] = None,
    ) -> jsii.Number:
        '''Return this storage as a total number of tebibytes.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL
        '''
        opts = SizeConversionOptions(rounding=rounding)

        return typing.cast(jsii.Number, jsii.invoke(self, "toTebibytes", [opts]))


@jsii.data_type(
    jsii_type="cdk8s.SizeConversionOptions",
    jsii_struct_bases=[],
    name_mapping={"rounding": "rounding"},
)
class SizeConversionOptions:
    def __init__(
        self,
        *,
        rounding: typing.Optional["SizeRoundingBehavior"] = None,
    ) -> None:
        '''Options for how to convert size to a different unit.

        :param rounding: How conversions should behave when it encounters a non-integer result. Default: SizeRoundingBehavior.FAIL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74d8c5389abc7998df4e40c89a04d6708f914ec430a67d4de594f36ede0a385)
            check_type(argname="argument rounding", value=rounding, expected_type=type_hints["rounding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rounding is not None:
            self._values["rounding"] = rounding

    @builtins.property
    def rounding(self) -> typing.Optional["SizeRoundingBehavior"]:
        '''How conversions should behave when it encounters a non-integer result.

        :default: SizeRoundingBehavior.FAIL
        '''
        result = self._values.get("rounding")
        return typing.cast(typing.Optional["SizeRoundingBehavior"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SizeConversionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk8s.SizeRoundingBehavior")
class SizeRoundingBehavior(enum.Enum):
    '''Rounding behaviour when converting between units of ``Size``.'''

    FAIL = "FAIL"
    '''Fail the conversion if the result is not an integer.'''
    FLOOR = "FLOOR"
    '''If the result is not an integer, round it to the closest integer less than the result.'''
    NONE = "NONE"
    '''Don't round.

    Return even if the result is a fraction.
    '''


class Testing(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Testing"):
    '''Testing utilities for cdk8s applications.'''

    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(
        cls,
        *,
        outdir: typing.Optional[builtins.str] = None,
        output_file_extension: typing.Optional[builtins.str] = None,
        record_construct_metadata: typing.Optional[builtins.bool] = None,
        resolvers: typing.Optional[typing.Sequence[IResolver]] = None,
        yaml_output_type: typing.Optional["YamlOutputType"] = None,
    ) -> App:
        '''Returns an app for testing with the following properties: - Output directory is a temp dir.

        :param outdir: The directory to output Kubernetes manifests. If you synthesize your application using ``cdk8s synth``, you must also pass this value to the CLI using the ``--output`` option or the ``output`` property in the ``cdk8s.yaml`` configuration file. Otherwise, the CLI will not know about the output directory, and synthesis will fail. This property is intended for internal and testing use. Default: - CDK8S_OUTDIR if defined, otherwise "dist"
        :param output_file_extension: The file extension to use for rendered YAML files. Default: .k8s.yaml
        :param record_construct_metadata: When set to true, the output directory will contain a ``construct-metadata.json`` file that holds construct related metadata on every resource in the app. Default: false
        :param resolvers: A list of resolvers that can be used to replace property values before they are written to the manifest file. When multiple resolvers are passed, they are invoked by order in the list, and only the first one that applies (e.g calls ``context.replaceValue``) is invoked. Default: - no resolvers.
        :param yaml_output_type: How to divide the YAML output into files. Default: YamlOutputType.FILE_PER_CHART
        '''
        props = AppProps(
            outdir=outdir,
            output_file_extension=output_file_extension,
            record_construct_metadata=record_construct_metadata,
            resolvers=resolvers,
            yaml_output_type=yaml_output_type,
        )

        return typing.cast(App, jsii.sinvoke(cls, "app", [props]))

    @jsii.member(jsii_name="chart")
    @builtins.classmethod
    def chart(cls) -> Chart:
        '''
        :return: a Chart that can be used for tests
        '''
        return typing.cast(Chart, jsii.sinvoke(cls, "chart", []))

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, chart: Chart) -> typing.List[typing.Any]:
        '''Returns the Kubernetes manifest synthesized from this chart.

        :param chart: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657f8eacff995e51f091bb334052923572b19da3a7b5ee11827c7b1c681b474f)
            check_type(argname="argument chart", value=chart, expected_type=type_hints["chart"])
        return typing.cast(typing.List[typing.Any], jsii.sinvoke(cls, "synth", [chart]))


@jsii.data_type(
    jsii_type="cdk8s.TimeConversionOptions",
    jsii_struct_bases=[],
    name_mapping={"integral": "integral"},
)
class TimeConversionOptions:
    def __init__(self, *, integral: typing.Optional[builtins.bool] = None) -> None:
        '''Options for how to convert time to a different unit.

        :param integral: If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202179ea2e21ed97cbc9ef1e98318b5d41feee4298b72f63a9d7495a60551470)
            check_type(argname="argument integral", value=integral, expected_type=type_hints["integral"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if integral is not None:
            self._values["integral"] = integral

    @builtins.property
    def integral(self) -> typing.Optional[builtins.bool]:
        '''If ``true``, conversions into a larger time unit (e.g. ``Seconds`` to ``Minutes``) will fail if the result is not an integer.

        :default: true
        '''
        result = self._values.get("integral")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TimeConversionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Yaml(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Yaml"):
    '''YAML utilities.'''

    @jsii.member(jsii_name="formatObjects")
    @builtins.classmethod
    def format_objects(cls, docs: typing.Sequence[typing.Any]) -> builtins.str:
        '''
        :param docs: -

        :deprecated: use ``stringify(doc[, doc, ...])``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea0571de9ead9ae671cf61531de5cfac77b27994c5f5491a9889702153838eb)
            check_type(argname="argument docs", value=docs, expected_type=type_hints["docs"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "formatObjects", [docs]))

    @jsii.member(jsii_name="load")
    @builtins.classmethod
    def load(cls, url_or_file: builtins.str) -> typing.List[typing.Any]:
        '''Downloads a set of YAML documents (k8s manifest for example) from a URL or a file and returns them as javascript objects.

        Empty documents are filtered out.

        :param url_or_file: a URL of a file path to load from.

        :return: an array of objects, each represents a document inside the YAML
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c990285959004a4192b7c194b2879b1515f72a1d8f0705ea3e1631f4267aad85)
            check_type(argname="argument url_or_file", value=url_or_file, expected_type=type_hints["url_or_file"])
        return typing.cast(typing.List[typing.Any], jsii.sinvoke(cls, "load", [url_or_file]))

    @jsii.member(jsii_name="save")
    @builtins.classmethod
    def save(cls, file_path: builtins.str, docs: typing.Sequence[typing.Any]) -> None:
        '''Saves a set of objects as a multi-document YAML file.

        :param file_path: The output path.
        :param docs: The set of objects.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c22a324dc074a1a13ef8e272543e01de272575028e4edd16b312cbc791dbaa)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument docs", value=docs, expected_type=type_hints["docs"])
        return typing.cast(None, jsii.sinvoke(cls, "save", [file_path, docs]))

    @jsii.member(jsii_name="stringify")
    @builtins.classmethod
    def stringify(cls, *docs: typing.Any) -> builtins.str:
        '''Stringify a document (or multiple documents) into YAML.

        We convert undefined values to null, but ignore any documents that are
        undefined.

        :param docs: A set of objects to convert to YAML.

        :return: a YAML string. Multiple docs are separated by ``---``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bba1c53df20fc40a3cce3fb70d981ea0d1fbeb521d6b0507d3415cdcd311aad)
            check_type(argname="argument docs", value=docs, expected_type=typing.Tuple[type_hints["docs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringify", [*docs]))

    @jsii.member(jsii_name="tmp")
    @builtins.classmethod
    def tmp(cls, docs: typing.Sequence[typing.Any]) -> builtins.str:
        '''Saves a set of YAML documents into a temp file (in /tmp).

        :param docs: the set of documents to save.

        :return: the path to the temporary file
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7ee4a0dedcd4c38cd685fc630a0ba5acf4fac661d411a0699db4e04ddd3de5)
            check_type(argname="argument docs", value=docs, expected_type=type_hints["docs"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "tmp", [docs]))


@jsii.enum(jsii_type="cdk8s.YamlOutputType")
class YamlOutputType(enum.Enum):
    '''The method to divide YAML output into files.'''

    FILE_PER_APP = "FILE_PER_APP"
    '''All resources are output into a single YAML file.'''
    FILE_PER_CHART = "FILE_PER_CHART"
    '''Resources are split into seperate files by chart.'''
    FILE_PER_RESOURCE = "FILE_PER_RESOURCE"
    '''Each resource is output to its own file.'''
    FOLDER_PER_CHART_FILE_PER_RESOURCE = "FOLDER_PER_CHART_FILE_PER_RESOURCE"
    '''Each chart in its own folder and each resource in its own file.'''


class Helm(Include, metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Helm"):
    '''Represents a Helm deployment.

    Use this construct to import an existing Helm chart and incorporate it into your constructs.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        chart: builtins.str,
        helm_executable: typing.Optional[builtins.str] = None,
        helm_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        release_name: typing.Optional[builtins.str] = None,
        repo: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param chart: The chart name to use. It can be a chart from a helm repository or a local directory. This name is passed to ``helm template`` and has all the relevant semantics.
        :param helm_executable: The local helm executable to use in order to create the manifest the chart. Default: "helm"
        :param helm_flags: Additional flags to add to the ``helm`` execution. Default: []
        :param namespace: Scope all resources in to a given namespace.
        :param release_name: The release name. Default: - if unspecified, a name will be allocated based on the construct path
        :param repo: Chart repository url where to locate the requested chart.
        :param values: Values to pass to the chart. Default: - If no values are specified, chart will use the defaults.
        :param version: Version constraint for the chart version to use. This constraint can be a specific tag (e.g. 1.1.1) or it may reference a valid range (e.g. ^2.0.0). If this is not specified, the latest version is used This name is passed to ``helm template --version`` and has all the relevant semantics.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190f4a5d85ecb3182d8df49a55454bd5cce993c692349125ced9593e6aa96c77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HelmProps(
            chart=chart,
            helm_executable=helm_executable,
            helm_flags=helm_flags,
            namespace=namespace,
            release_name=release_name,
            repo=repo,
            values=values,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="releaseName")
    def release_name(self) -> builtins.str:
        '''The helm release name.'''
        return typing.cast(builtins.str, jsii.get(self, "releaseName"))


__all__ = [
    "ApiObject",
    "ApiObjectMetadata",
    "ApiObjectMetadataDefinition",
    "ApiObjectMetadataDefinitionOptions",
    "ApiObjectProps",
    "App",
    "AppProps",
    "Chart",
    "ChartProps",
    "Cron",
    "CronOptions",
    "DependencyGraph",
    "DependencyVertex",
    "Duration",
    "GroupVersionKind",
    "Helm",
    "HelmProps",
    "IAnyProducer",
    "IResolver",
    "ImplicitTokenResolver",
    "Include",
    "IncludeProps",
    "JsonPatch",
    "Lazy",
    "LazyResolver",
    "NameOptions",
    "Names",
    "NumberStringUnionResolver",
    "OwnerReference",
    "ResolutionContext",
    "Size",
    "SizeConversionOptions",
    "SizeRoundingBehavior",
    "Testing",
    "TimeConversionOptions",
    "Yaml",
    "YamlOutputType",
]

publication.publish()

def _typecheckingstub__7c3471c86f94453ef4d9efec6bd8f9cf9dbac2f11db69184e091d0a4f6d502be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api_version: builtins.str,
    kind: builtins.str,
    metadata: typing.Optional[typing.Union[ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1861e2a67b17cc03b65ec7686045b40569487efa29052a042f312c20d14b2c(
    o: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c55b2fcd45f38255c26ac00ed411c9af6ec5ea8ba6920c18afedcc214149a4e(
    c: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82881106c470fdf7ed8e821d53730213ae34215c35ed597f7708178c0df728bf(
    *dependencies: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161731dd57929dbfaf25c8720b0e1ddbb543e720daf53247296b6d94a9976531(
    *ops: JsonPatch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f4c3c7639bc9b50e949af73521350fa15fe4a126bddfdabcac5172638d132d(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    finalizers: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    owner_references: typing.Optional[typing.Sequence[typing.Union[OwnerReference, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9def3e3bd00bf53cb37a2e0644831b7d89d8821a115c8d269a7d9e2d4531bb4d(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca708eae375d08efb85cb3aa3ab3facc98cc64a3ab5ae313448e08b7d5029c5(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dc63d8c5b395973d6bc1d0cdc1e1b5026ce0e8147949b44197244e4156f74e(
    *finalizers: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63f1a5223c791fe2ed2391972064b7664d61556144b09da9c6bc83a0328cefe(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec412ec90f3d03be3378cbdee675bf84860bff9d43c0328f5c1508f82ce2e6b(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941a97ef4e3f244aec7e1e661b3ea14853c24d8af07fc02fa36831237c09dff3(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    finalizers: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    owner_references: typing.Optional[typing.Sequence[typing.Union[OwnerReference, typing.Dict[builtins.str, typing.Any]]]] = None,
    api_object: ApiObject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd25b85d2368c9440a32a95c8f2442d5db4cc9bc422486dd10cfc51448222d8(
    *,
    api_version: builtins.str,
    kind: builtins.str,
    metadata: typing.Optional[typing.Union[ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d69a701ccbd6d4fe53a9f9a1243ebfef02b200d6c47aaee4e0ecb22fc803d4(
    c: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef9f0e4cd886d9d12fc1e1bb666e5a9f09404abbdcba465301b3dc064ecfde4(
    *,
    outdir: typing.Optional[builtins.str] = None,
    output_file_extension: typing.Optional[builtins.str] = None,
    record_construct_metadata: typing.Optional[builtins.bool] = None,
    resolvers: typing.Optional[typing.Sequence[IResolver]] = None,
    yaml_output_type: typing.Optional[YamlOutputType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac62dbd05c99a5228dff367434c3e3fca0fb00c841ecd71382b9acd3fc1e30d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac1ee14ad96a56047185b46392b2fba722962d47ed4174705c5dc48101cec6e(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3591e786c1053dcfd71742c41befcbdacfce2fb416c37a182e0cdd7968ae81(
    c: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932e2ddf3b649962a0914218bc529f30c50bf5d7ca654cc994f8a3084c93c717(
    *dependencies: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15771e9e29c981b37d0997432bf0647e396050fd6c07b9241625bfb3e542d7ec(
    api_object: ApiObject,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587cc3f5a3d7a6cc9a5690888b75875a8059bcf784bfae23dedf362a06743ee3(
    *,
    disable_resource_name_hashes: typing.Optional[builtins.bool] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2c750519e19d88bad3a5fad0784148fee43e03a55bddfc61438556ab6bb698(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e42df9fe8e54748af3dd0e25616d4ea57a51e241dfc6972407f4bce78ced02(
    node: _constructs_77d1e7e8.Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7903f01cf4bab7177bfc66d8e5acb3e99c019af8082b816e72beee89ab639c47(
    value: typing.Optional[_constructs_77d1e7e8.IConstruct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3c1a1b4df66c2406e31123378a2ba7139aab5e261b7253d3771af9c0ed2922(
    dep: DependencyVertex,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ce164c8ddb62412fbc9134b2a57787b49dbf637a9072ddd8cb35ef9545a083(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49be32303a4d56be9a6c9d9fb6e759ce5a4a30d954642474baf29f1b47d6e5bb(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8a2ef493eb7238ccbd43ee0e3ff2da5e62c5d6d51fc2d127776eba261980e5(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65e8ee772805167d1dcc9fe3132d51039baf5cc182a0d12041c68495d4a3661(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0db6a272abc31ecb50e8a143af3a1c2e63de57d4793ad8a17a96d0454f2037(
    duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c36c45ae685aa42e43f0df90cff9bc72a4d096750fe1eb4ba29aef794d09410(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5654dc50c8f0fc983e64c60bc59a01c4a0ebeb3357670346908003a338a42d2d(
    *,
    api_version: builtins.str,
    kind: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d491a2276602d3378938ffe40a1ca86f3a51816e3a51fd829aeb41e96630e966(
    *,
    chart: builtins.str,
    helm_executable: typing.Optional[builtins.str] = None,
    helm_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    release_name: typing.Optional[builtins.str] = None,
    repo: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5ca202bc9e3dd6c5b464aae10cd956d0ccfeabb617701f2f25c6845a60289e(
    context: ResolutionContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6e42d5af180bdfb92d72b8157aae3261fc21d0f10885350023690febf6cbae(
    context: ResolutionContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7ad4649d7e1e318f4c5cfd1b6f285d8481cd49825b775d4fcdc15c2f1257c3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a5cdbd9f75abfa5f7670e54b759fcd6f7c402051f050a5e1aa1f73ac5eaf3e(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e51633af9c45ea1ac2cc618c9ade6d085cb4b0e47240e794a287cacb94a4c59(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cc5db94fd68d7c20469e460e266007085d6d5b5e8541e8796ba2c1c8106dd8(
    document: typing.Any,
    *ops: JsonPatch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad568ab5b16454e5e827da5f437072e9e3555ccc7b7553a697903192a1b3eb5(
    from_: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de55a7c5105ba84ccdf0e9638671d4816ff4422d1895bef75b8aa1047454ad69(
    from_: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aed01338ac97e26df8aa53e7f354b7fc10275fcf1d9814b024cc78d755f21ed(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b103a48708f207593ef910f1bddfd661aef834c5086afbbdba659c0103dfcab(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9005a324c07bb509dbb3733b53e421cbf2e1220e48c561f969d97268d097c69e(
    path: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66ad4b91ba96e5ece2b03dda56e66ac135a52e42ec1dc812633365d043b45da(
    producer: IAnyProducer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af8596daa9e070048c5bd02166ac52f48073da14c659b03be91af3d002a76b8(
    context: ResolutionContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff5aa57fdaa34956720956edd71f9da68fb2936d50787accb5cd16713811035(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    extra: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_hash: typing.Optional[builtins.bool] = None,
    max_len: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2694a7308fa083bea22907798345bf812c9e9a723f8832b8f0a8bbef8565f836(
    scope: _constructs_77d1e7e8.Construct,
    *,
    delimiter: typing.Optional[builtins.str] = None,
    extra: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_hash: typing.Optional[builtins.bool] = None,
    max_len: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b42b2ea1a8f79926d2acae92335ea6375b89dbd75da580f0ded3902cfce829(
    scope: _constructs_77d1e7e8.Construct,
    *,
    delimiter: typing.Optional[builtins.str] = None,
    extra: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_hash: typing.Optional[builtins.bool] = None,
    max_len: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0e0eaeefa0726153706af3c2183eab46ff6dadfe4d6d943600131d6bf2657e(
    context: ResolutionContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cfb6f34de5a3f7c962fcc2da2dfae03bc583bfafc2393157bd81af722b432b(
    *,
    api_version: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    uid: builtins.str,
    block_owner_deletion: typing.Optional[builtins.bool] = None,
    controller: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6d87f260728f933d112797dca80dbcf9281ea35eadb4bff9f6a38a1cf78a1e(
    obj: ApiObject,
    key: typing.Sequence[builtins.str],
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0dc17edb4458da9d06ff82b9c151690ce17fbe2dfdfe623b5f7415cdcd5071(
    new_value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46fc386c510b2c1129687fab66a5d8b73e229013d9438613e42b2b93bab2701f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2dafc483ec1b162f3ac5314f24a646833af290785fa69fee4e9a54bd10e1af(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6e3e4f8a439c63e3ed083e0d76fba9fe218a2f3f2a47515af3732dcf82fcce(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fd48faa9e664bcd03923015ba048b929be4a547ac0a2f1ef83a7bcf2a6ef88(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecf102c3a7a867995cb1f2e0ca44a97d0c853897af7d1da6d92ea170aad88c0(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd978397137248b8c68fd5ef41aad7818510368daf79092fb8e1ff9a0478e5f(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f658d6703486a9fb30a5fb73df83a10f792ba95cd2ae69ba6436614be70497(
    amount: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74d8c5389abc7998df4e40c89a04d6708f914ec430a67d4de594f36ede0a385(
    *,
    rounding: typing.Optional[SizeRoundingBehavior] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657f8eacff995e51f091bb334052923572b19da3a7b5ee11827c7b1c681b474f(
    chart: Chart,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202179ea2e21ed97cbc9ef1e98318b5d41feee4298b72f63a9d7495a60551470(
    *,
    integral: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea0571de9ead9ae671cf61531de5cfac77b27994c5f5491a9889702153838eb(
    docs: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c990285959004a4192b7c194b2879b1515f72a1d8f0705ea3e1631f4267aad85(
    url_or_file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c22a324dc074a1a13ef8e272543e01de272575028e4edd16b312cbc791dbaa(
    file_path: builtins.str,
    docs: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bba1c53df20fc40a3cce3fb70d981ea0d1fbeb521d6b0507d3415cdcd311aad(
    *docs: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7ee4a0dedcd4c38cd685fc630a0ba5acf4fac661d411a0699db4e04ddd3de5(
    docs: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190f4a5d85ecb3182d8df49a55454bd5cce993c692349125ced9593e6aa96c77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    chart: builtins.str,
    helm_executable: typing.Optional[builtins.str] = None,
    helm_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    release_name: typing.Optional[builtins.str] = None,
    repo: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
