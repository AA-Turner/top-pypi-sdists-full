r'''
# AWS::Location Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

Amazon Location Service lets you add location data and functionality to applications, which
includes capabilities such as maps, points of interest, geocoding, routing, geofences, and
tracking. Amazon Location provides location-based services (LBS) using high-quality data from
global, trusted providers Esri and HERE. With affordable data, tracking and geofencing
capabilities, and built-in metrics for health monitoring, you can build sophisticated
location-enabled applications.

## Geofence Collection

Geofence collection resources allow you to store and manage geofences—virtual boundaries on a map.
You can evaluate locations against a geofence collection resource and get notifications when the location
update crosses the boundary of any of the geofences in the geofence collection.

```python
# key: kms.Key


location.GeofenceCollection(self, "GeofenceCollection",
    geofence_collection_name="MyGeofenceCollection",  # optional, defaults to a generated name
    kms_key=key
)
```

Use the `grant()` or `grantRead()` method to grant the given identity permissions to perform actions
on the geofence collection:

```python
# role: iam.Role


geofence_collection = location.GeofenceCollection(self, "GeofenceCollection",
    geofence_collection_name="MyGeofenceCollection"
)

geofence_collection.grant_read(role)
```

## Tracker

A tracker stores position updates for a collection of devices. The tracker can be used to query the devices' current location or location history. It stores the updates, but reduces storage space and visual noise by filtering the locations before storing them.

For more information, see [Trackers](https://docs.aws.amazon.com/location/latest/developerguide/geofence-tracker-concepts.html#tracking-overview).

To create a tracker, define a `Tracker`:

```python
# key: kms.Key


location.Tracker(self, "Tracker",
    tracker_name="MyTracker",  # optional, defaults to a generated name
    kms_key=key
)
```

Use the `grant()`, `grantUpdateDevicePositions()` or `grantRead()` method to grant the given identity permissions to perform actions
on the geofence collection:

```python
# role: iam.Role


tracker = location.Tracker(self, "Tracker",
    tracker_name="MyTracker"
)

tracker.grant_read(role)
```

If you want to associate a tracker with geofence collections, define a `geofenceCollections` property or use the `addGeofenceCollections()` method.

```python
# geofence_collection: location.GeofenceCollection
# geofence_collection_for_add: location.GeofenceCollection
# tracker: location.Tracker


tracker = location.Tracker(self, "Tracker",
    tracker_name="MyTracker",
    geofence_collections=[geofence_collection]
)

tracker.add_geofence_collections(geofence_collection_for_add)
```

## API key

API keys are a key value that is associated with specific Amazon Location Service resources or API in your AWS account, and specific actions that you can perform on those resources.
You can use an API key in your application to make unauthenticated calls to the Amazon Location APIs for those resources.

For more information, see [Use API keys to authenticate](https://docs.aws.amazon.com/location/latest/developerguide/using-apikeys.html).

To create an API key, define an `ApiKey`:

```python
location.ApiKey(self, "APIKeyAny",
    # specify allowed actions
    allow_maps_actions=[location.AllowMapsAction.GET_STATIC_MAP
    ],
    allow_places_actions=[location.AllowPlacesAction.GET_PLACE
    ],
    allow_routes_actions=[location.AllowRoutesAction.CALCULATE_ISOLINES
    ]
)
```

> Note: `ApiKey` construct only supports [Enhanced Places, Routes, and Maps](https://aws.amazon.com/blogs/aws/announcing-new-apis-for-amazon-location-service-routes-places-and-maps/) This API key grants access to AWS-managed Places, Routes, and Maps.

## Legacy Resources

AWS has released new [Enhanced Places, Routes, and Maps](https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-location-service-enhanced-places-routes-maps/?nc1=h_ls). Since these use AWS-managed resources, users no longer need to create Maps, Places, and Routes resources themselves.

As a result, the following constructs are now considered legacy.

For more information, see [developer guide](https://docs.aws.amazon.com/location/latest/developerguide/what-is.html).

### Map

The Amazon Location Service Map resource gives you access to the underlying basemap data for a map.
You use the Map resource with a map rendering library to add an interactive map to your application.
You can add other functionality to your map, such as markers (or pins), routes, and polygon areas, as needed for your application.

For information about how to use map resources in practice, see [Using Amazon Location Maps in your application](https://docs.aws.amazon.com/location/latest/developerguide/using-maps.html).

To create a map, define a `Map`:

```python
location.Map(self, "Map",
    map_name="my-map",
    style=location.Style.VECTOR_ESRI_NAVIGATION,
    custom_layers=[location.CustomLayer.POI]
)
```

Use the `grant()` or `grantRendering()` method to grant the given identity permissions to perform actions
on the map:

```python
# role: iam.Role


map = location.Map(self, "Map",
    style=location.Style.VECTOR_ESRI_NAVIGATION
)
map.grant_rendering(role)
```

### Place Index

A key function of Amazon Location Service is the ability to search the geolocation information.
Amazon Location provides this functionality via the Place index resource. The place index includes
which [data provider](https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html)
to use for the search.

To create a place index, define a `PlaceIndex`:

```python
location.PlaceIndex(self, "PlaceIndex",
    place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
    data_source=location.DataSource.HERE
)
```

Use the `grant()` or `grantSearch()` method to grant the given identity permissions to perform actions
on the place index:

```python
# role: iam.Role


place_index = location.PlaceIndex(self, "PlaceIndex")
place_index.grant_search(role)
```

### Route Calculator

Route calculator resources allow you to find routes and estimate travel time based on up-to-date road network and live traffic information from your chosen data provider.

For more information, see [Routes](https://docs.aws.amazon.com/location/latest/developerguide/route-concepts.html).

To create a route calculator, define a `RouteCalculator`:

```python
location.RouteCalculator(self, "RouteCalculator",
    route_calculator_name="MyRouteCalculator",  # optional, defaults to a generated name
    data_source=location.DataSource.ESRI
)
```

Use the `grant()` or `grantRead()` method to grant the given identity permissions to perform actions
on the route calculator:

```python
# role: iam.Role


route_calculator = location.RouteCalculator(self, "RouteCalculator",
    data_source=location.DataSource.ESRI
)
route_calculator.grant_read(role)
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
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.interfaces.aws_kms as _aws_cdk_interfaces_aws_kms_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.AllowMapsAction")
class AllowMapsAction(enum.Enum):
    '''(experimental) Actions for Maps that an API key resource grants permissions to perform.

    :see: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlocationservicemaps.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.ApiKey(self, "APIKeyAny",
            # specify allowed actions
            allow_maps_actions=[location.AllowMapsAction.GET_STATIC_MAP
            ],
            allow_places_actions=[location.AllowPlacesAction.GET_PLACE
            ],
            allow_routes_actions=[location.AllowRoutesAction.CALCULATE_ISOLINES
            ]
        )
    '''

    GET_STATIC_MAP = "GET_STATIC_MAP"
    '''(experimental) Allows getting static map images.

    :stability: experimental
    '''
    GET_TILE = "GET_TILE"
    '''(experimental) Allows getting map tiles for rendering.

    :stability: experimental
    '''
    ANY = "ANY"
    '''(experimental) Allows any maps actions.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.AllowPlacesAction")
class AllowPlacesAction(enum.Enum):
    '''(experimental) Actions for Places that an API key resource grants permissions to perform.

    :see: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlocationserviceplaces.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.ApiKey(self, "APIKeyAny",
            # specify allowed actions
            allow_maps_actions=[location.AllowMapsAction.GET_STATIC_MAP
            ],
            allow_places_actions=[location.AllowPlacesAction.GET_PLACE
            ],
            allow_routes_actions=[location.AllowRoutesAction.CALCULATE_ISOLINES
            ]
        )
    '''

    AUTOCOMPLETE = "AUTOCOMPLETE"
    '''(experimental) Allows auto-completion of search text.

    :stability: experimental
    '''
    GEOCODE = "GEOCODE"
    '''(experimental) Allows finding geo coordinates of a known place.

    :stability: experimental
    '''
    GET_PLACE = "GET_PLACE"
    '''(experimental) Allows getting details of a place.

    :stability: experimental
    '''
    REVERSE_GEOCODE = "REVERSE_GEOCODE"
    '''(experimental) Allows getting nearest address to geo coordinates.

    :stability: experimental
    '''
    SEARCH_NEARBY = "SEARCH_NEARBY"
    '''(experimental) Allows category based places search around geo coordinates.

    :stability: experimental
    '''
    SEARCH_TEXT = "SEARCH_TEXT"
    '''(experimental) Allows place or address search based on free-form text.

    :stability: experimental
    '''
    SUGGEST = "SUGGEST"
    '''(experimental) Allows suggestions based on an incomplete or misspelled query.

    :stability: experimental
    '''
    ANY = "ANY"
    '''(experimental) Allows any places actions.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.AllowRoutesAction")
class AllowRoutesAction(enum.Enum):
    '''(experimental) Actions for Routes that an API key resource grants permissions to perform.

    :see: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonlocationserviceroutes.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.ApiKey(self, "APIKeyAny",
            # specify allowed actions
            allow_maps_actions=[location.AllowMapsAction.GET_STATIC_MAP
            ],
            allow_places_actions=[location.AllowPlacesAction.GET_PLACE
            ],
            allow_routes_actions=[location.AllowRoutesAction.CALCULATE_ISOLINES
            ]
        )
    '''

    CALCULATE_ISOLINES = "CALCULATE_ISOLINES"
    '''(experimental) Allows isoline calculation.

    :stability: experimental
    '''
    CALCULATE_ROUTES = "CALCULATE_ROUTES"
    '''(experimental) Allows point to point routing.

    :stability: experimental
    '''
    CALCULATE_ROUTE_MATRIX = "CALCULATE_ROUTE_MATRIX"
    '''(experimental) Allows matrix routing.

    :stability: experimental
    '''
    OPTIMIZE_WAYPOINTS = "OPTIMIZE_WAYPOINTS"
    '''(experimental) Allows computing the best sequence of waypoints.

    :stability: experimental
    '''
    SNAP_TO_ROADS = "SNAP_TO_ROADS"
    '''(experimental) Allows snapping GPS points to a likely route.

    :stability: experimental
    '''
    ANY = "ANY"
    '''(experimental) Allows any routes actions.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.ApiKeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_maps_actions": "allowMapsActions",
        "allow_places_actions": "allowPlacesActions",
        "allow_referers": "allowReferers",
        "allow_routes_actions": "allowRoutesActions",
        "api_key_name": "apiKeyName",
        "description": "description",
        "expire_time": "expireTime",
        "force_delete": "forceDelete",
        "force_update": "forceUpdate",
        "no_expiry": "noExpiry",
    },
)
class ApiKeyProps:
    def __init__(
        self,
        *,
        allow_maps_actions: typing.Optional[typing.Sequence["AllowMapsAction"]] = None,
        allow_places_actions: typing.Optional[typing.Sequence["AllowPlacesAction"]] = None,
        allow_referers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_routes_actions: typing.Optional[typing.Sequence["AllowRoutesAction"]] = None,
        api_key_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[datetime.datetime] = None,
        force_delete: typing.Optional[builtins.bool] = None,
        force_update: typing.Optional[builtins.bool] = None,
        no_expiry: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for an API Key.

        :param allow_maps_actions: (experimental) A list of allowed actions for Maps that an API key resource grants permissions to perform. Default: - no actions for Maps are permitted
        :param allow_places_actions: (experimental) A list of allowed actions for Places that an API key resource grants permissions to perform. Default: - no actions for Places are permitted
        :param allow_referers: (experimental) An optional list of allowed HTTP referers for which requests must originate from. Requests using this API key from other domains will not be allowed. Default: - no Referer
        :param allow_routes_actions: (experimental) A list of allowed actions for Routes that an API key resource grants permissions to perform. Default: - no actions for Routes are permitted
        :param api_key_name: (experimental) A name for the api key. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Must be a unique API key name. Default: - A name is automatically generated
        :param description: (experimental) A description for the api key. Default: - no description
        :param expire_time: (experimental) The optional timestamp for when the API key resource will expire. ``expireTime`` must be set when ``noExpiry`` is false or undefined. When ``expireTime`` is not set, ``noExpiry`` must be ``true``. Default: undefined - The API Key never expires
        :param force_delete: (experimental) ``forceDelete`` bypasses an API key's expiry conditions and deletes the key. Set the parameter true to delete the key or to false to not preemptively delete the API key. Default: undefined - not force delete
        :param force_update: (experimental) The boolean flag to be included for updating ExpireTime or Restrictions details. Must be set to true to update an API key resource that has been used in the past 7 days. False if force update is not preferred. Default: undefined - not force update
        :param no_expiry: (experimental) Whether the API key should expire. Set to ``true`` when ``expireTime`` is not set. When you set ``expireTime``, ``noExpiry`` must be ``false`` or ``undefined``. Default: undefined - The API Key expires at ``expireTime``

        :stability: experimental
        :exampleMetadata: infused

        Example::

            location.ApiKey(self, "APIKeyAny",
                # specify allowed actions
                allow_maps_actions=[location.AllowMapsAction.GET_STATIC_MAP
                ],
                allow_places_actions=[location.AllowPlacesAction.GET_PLACE
                ],
                allow_routes_actions=[location.AllowRoutesAction.CALCULATE_ISOLINES
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fefe79c3c3f11720df74a6b3ca3ee04549f9cebd75d8bb48ff783b2661ff94c5)
            check_type(argname="argument allow_maps_actions", value=allow_maps_actions, expected_type=type_hints["allow_maps_actions"])
            check_type(argname="argument allow_places_actions", value=allow_places_actions, expected_type=type_hints["allow_places_actions"])
            check_type(argname="argument allow_referers", value=allow_referers, expected_type=type_hints["allow_referers"])
            check_type(argname="argument allow_routes_actions", value=allow_routes_actions, expected_type=type_hints["allow_routes_actions"])
            check_type(argname="argument api_key_name", value=api_key_name, expected_type=type_hints["api_key_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument no_expiry", value=no_expiry, expected_type=type_hints["no_expiry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_maps_actions is not None:
            self._values["allow_maps_actions"] = allow_maps_actions
        if allow_places_actions is not None:
            self._values["allow_places_actions"] = allow_places_actions
        if allow_referers is not None:
            self._values["allow_referers"] = allow_referers
        if allow_routes_actions is not None:
            self._values["allow_routes_actions"] = allow_routes_actions
        if api_key_name is not None:
            self._values["api_key_name"] = api_key_name
        if description is not None:
            self._values["description"] = description
        if expire_time is not None:
            self._values["expire_time"] = expire_time
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if force_update is not None:
            self._values["force_update"] = force_update
        if no_expiry is not None:
            self._values["no_expiry"] = no_expiry

    @builtins.property
    def allow_maps_actions(self) -> typing.Optional[typing.List["AllowMapsAction"]]:
        '''(experimental) A list of allowed actions for Maps that an API key resource grants permissions to perform.

        :default: - no actions for Maps are permitted

        :stability: experimental
        '''
        result = self._values.get("allow_maps_actions")
        return typing.cast(typing.Optional[typing.List["AllowMapsAction"]], result)

    @builtins.property
    def allow_places_actions(self) -> typing.Optional[typing.List["AllowPlacesAction"]]:
        '''(experimental) A list of allowed actions for Places that an API key resource grants permissions to perform.

        :default: - no actions for Places are permitted

        :stability: experimental
        '''
        result = self._values.get("allow_places_actions")
        return typing.cast(typing.Optional[typing.List["AllowPlacesAction"]], result)

    @builtins.property
    def allow_referers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An optional list of allowed HTTP referers for which requests must originate from.

        Requests using this API key from other domains will not be allowed.

        :default: - no Referer

        :see: https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html#cfn-location-apikey-apikeyrestrictions-allowreferers
        :stability: experimental
        '''
        result = self._values.get("allow_referers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_routes_actions(self) -> typing.Optional[typing.List["AllowRoutesAction"]]:
        '''(experimental) A list of allowed actions for Routes that an API key resource grants permissions to perform.

        :default: - no actions for Routes are permitted

        :stability: experimental
        '''
        result = self._values.get("allow_routes_actions")
        return typing.cast(typing.Optional[typing.List["AllowRoutesAction"]], result)

    @builtins.property
    def api_key_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the api key.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        Must be a unique API key name.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("api_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the api key.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_time(self) -> typing.Optional[datetime.datetime]:
        '''(experimental) The optional timestamp for when the API key resource will expire.

        ``expireTime`` must be set when ``noExpiry`` is false or undefined.
        When ``expireTime`` is not set, ``noExpiry`` must be ``true``.

        :default: undefined - The API Key never expires

        :stability: experimental
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def force_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) ``forceDelete`` bypasses an API key's expiry conditions and deletes the key.

        Set the parameter true to delete the key or to false to not preemptively delete the API key.

        :default: undefined - not force delete

        :stability: experimental
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def force_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The boolean flag to be included for updating ExpireTime or Restrictions details.

        Must be set to true to update an API key resource that has been used in the past 7 days.
        False if force update is not preferred.

        :default: undefined - not force update

        :stability: experimental
        '''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def no_expiry(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the API key should expire.

        Set to ``true`` when ``expireTime`` is not set.
        When you set ``expireTime``, ``noExpiry`` must be ``false`` or ``undefined``.

        :default: undefined - The API Key expires at ``expireTime``

        :stability: experimental
        '''
        result = self._values.get("no_expiry")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.CustomLayer")
class CustomLayer(enum.Enum):
    '''(experimental) An additional layer you can enable for a map style.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.Map(self, "Map",
            map_name="my-map",
            style=location.Style.VECTOR_ESRI_NAVIGATION,
            custom_layers=[location.CustomLayer.POI]
        )
    '''

    POI = "POI"
    '''(experimental) The POI custom layer adds a richer set of places, such as shops, services, restaurants, attractions, and other points of interest to your map.

    Currently only the VectorEsriNavigation map style supports the POI custom layer.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.DataSource")
class DataSource(enum.Enum):
    '''(experimental) Data source for a place index.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.PlaceIndex(self, "PlaceIndex",
            place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
            data_source=location.DataSource.HERE
        )
    '''

    ESRI = "ESRI"
    '''(experimental) Esri.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/esri.html
    :stability: experimental
    '''
    GRAB = "GRAB"
    '''(experimental) Grab provides routing functionality for Southeast Asia.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/grab.html
    :stability: experimental
    '''
    HERE = "HERE"
    '''(experimental) HERE.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/HERE.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.GeofenceCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "geofence_collection_name": "geofenceCollectionName",
        "kms_key": "kmsKey",
    },
)
class GeofenceCollectionProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        geofence_collection_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"] = None,
    ) -> None:
        '''(experimental) Properties for a geofence collection.

        :param description: (experimental) A description for the geofence collection. Default: - no description
        :param geofence_collection_name: (experimental) A name for the geofence collection. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated
        :param kms_key: (experimental) The customer managed to encrypt your data. Default: - Use an AWS managed key

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # key: kms.Key
            
            
            location.GeofenceCollection(self, "GeofenceCollection",
                geofence_collection_name="MyGeofenceCollection",  # optional, defaults to a generated name
                kms_key=key
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdd3197c12b6d89ece6dfce72294a7f00d61e7a28da5918141a6d8e57c35fc5)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument geofence_collection_name", value=geofence_collection_name, expected_type=type_hints["geofence_collection_name"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if geofence_collection_name is not None:
            self._values["geofence_collection_name"] = geofence_collection_name
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the geofence collection.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geofence_collection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the geofence collection.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("geofence_collection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(
        self,
    ) -> typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"]:
        '''(experimental) The customer managed to encrypt your data.

        :default: - Use an AWS managed key

        :see: https://docs.aws.amazon.com/location/latest/developerguide/encryption-at-rest.html
        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GeofenceCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IApiKey")
class IApiKey(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An API Key.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="apiKeyArn")
    def api_key_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the api key resource.

        :stability: experimental
        :attribute: Arn, apiKeyArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="apiKeyName")
    def api_key_name(self) -> builtins.str:
        '''(experimental) The name of the api key.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IApiKeyProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An API Key.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IApiKey"

    @builtins.property
    @jsii.member(jsii_name="apiKeyArn")
    def api_key_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the api key resource.

        :stability: experimental
        :attribute: Arn, apiKeyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKeyArn"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyName")
    def api_key_name(self) -> builtins.str:
        '''(experimental) The name of the api key.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKeyName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApiKey).__jsii_proxy_class__ = lambda : _IApiKeyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IGeofenceCollection")
class IGeofenceCollection(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Geofence Collection.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionArn")
    def geofence_collection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the geofence collection resource.

        :stability: experimental
        :attribute: Arn, CollectionArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionName")
    def geofence_collection_name(self) -> builtins.str:
        '''(experimental) The name of the geofence collection.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IGeofenceCollectionProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Geofence Collection.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IGeofenceCollection"

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionArn")
    def geofence_collection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the geofence collection resource.

        :stability: experimental
        :attribute: Arn, CollectionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionArn"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionName")
    def geofence_collection_name(self) -> builtins.str:
        '''(experimental) The name of the geofence collection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGeofenceCollection).__jsii_proxy_class__ = lambda : _IGeofenceCollectionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IMap")
class IMap(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents the Amazon Location Service Map.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="mapArn")
    def map_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the Map.

        :stability: experimental
        :attribute: Arn, MapArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="mapName")
    def map_name(self) -> builtins.str:
        '''(experimental) The name of the map.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IMapProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents the Amazon Location Service Map.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IMap"

    @builtins.property
    @jsii.member(jsii_name="mapArn")
    def map_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the Map.

        :stability: experimental
        :attribute: Arn, MapArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapArn"))

    @builtins.property
    @jsii.member(jsii_name="mapName")
    def map_name(self) -> builtins.str:
        '''(experimental) The name of the map.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMap).__jsii_proxy_class__ = lambda : _IMapProxy


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IPlaceIndex")
class IPlaceIndex(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Place Index.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        :attribute: Arn,IndexArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPlaceIndexProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Place Index.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IPlaceIndex"

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        :attribute: Arn,IndexArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPlaceIndex).__jsii_proxy_class__ = lambda : _IPlaceIndexProxy


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IRouteCalculator")
class IRouteCalculator(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Route Calculator.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorArn")
    def route_calculator_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the route calculator resource.

        :stability: experimental
        :attribute: Arn,CalculatorArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorName")
    def route_calculator_name(self) -> builtins.str:
        '''(experimental) The name of the route calculator.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IRouteCalculatorProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Route Calculator.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IRouteCalculator"

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorArn")
    def route_calculator_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the route calculator resource.

        :stability: experimental
        :attribute: Arn,CalculatorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeCalculatorArn"))

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorName")
    def route_calculator_name(self) -> builtins.str:
        '''(experimental) The name of the route calculator.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeCalculatorName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRouteCalculator).__jsii_proxy_class__ = lambda : _IRouteCalculatorProxy


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.ITracker")
class ITracker(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Tracker.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="trackerArn")
    def tracker_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the tracker resource.

        :stability: experimental
        :attribute: Arn, TrackerArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="trackerName")
    def tracker_name(self) -> builtins.str:
        '''(experimental) The name of the tracker.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ITrackerProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Tracker.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.ITracker"

    @builtins.property
    @jsii.member(jsii_name="trackerArn")
    def tracker_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the tracker resource.

        :stability: experimental
        :attribute: Arn, TrackerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerArn"))

    @builtins.property
    @jsii.member(jsii_name="trackerName")
    def tracker_name(self) -> builtins.str:
        '''(experimental) The name of the tracker.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITracker).__jsii_proxy_class__ = lambda : _ITrackerProxy


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.IntendedUse")
class IntendedUse(enum.Enum):
    '''(experimental) Intend use for the results of an operation.

    :stability: experimental
    '''

    SINGLE_USE = "SINGLE_USE"
    '''(experimental) The results won't be stored.

    :stability: experimental
    '''
    STORAGE = "STORAGE"
    '''(experimental) The result can be cached or stored in a database.

    :stability: experimental
    '''


@jsii.implements(IMap)
class Map(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.Map",
):
    '''(experimental) The Amazon Location Service Map.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/map-concepts.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.Map(self, "Map",
            map_name="my-map",
            style=location.Style.VECTOR_ESRI_NAVIGATION,
            custom_layers=[location.CustomLayer.POI]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        style: "Style",
        custom_layers: typing.Optional[typing.Sequence["CustomLayer"]] = None,
        description: typing.Optional[builtins.str] = None,
        map_name: typing.Optional[builtins.str] = None,
        political_view: typing.Optional["PoliticalView"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param style: (experimental) Specifies the map style selected from an available data provider.
        :param custom_layers: (experimental) Specifies the custom layers for the style. Default: - no custom layers
        :param description: (experimental) A description for the map. Default: - no description
        :param map_name: (experimental) A name for the map. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated
        :param political_view: (experimental) Specifies the map political view selected from an available data provider. The political view must be used in compliance with applicable laws, including those laws about mapping of the country or region where the maps, images, and other data and third-party content which you access through Amazon Location Service is made available. Default: - no political view

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eadf3225dad1551d12c46d02a8cc99fbedbc63844ea7721e06578672f9d6ec8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MapProps(
            style=style,
            custom_layers=custom_layers,
            description=description,
            map_name=map_name,
            political_view=political_view,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromMapArn")
    @builtins.classmethod
    def from_map_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        map_arn: builtins.str,
    ) -> "IMap":
        '''(experimental) Use an existing map by ARN.

        :param scope: -
        :param id: -
        :param map_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f608f3b299254757f5028a9f2e4f5929f7b7427cbe4e467211bda7962954150d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument map_arn", value=map_arn, expected_type=type_hints["map_arn"])
        return typing.cast("IMap", jsii.sinvoke(cls, "fromMapArn", [scope, id, map_arn]))

    @jsii.member(jsii_name="fromMapName")
    @builtins.classmethod
    def from_map_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        map_name: builtins.str,
    ) -> "IMap":
        '''(experimental) Use an existing map by name.

        :param scope: -
        :param id: -
        :param map_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7019e487b4362e4e8d871612adfc04be5a9738c6cab349a06b8592cc88ba9266)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument map_name", value=map_name, expected_type=type_hints["map_name"])
        return typing.cast("IMap", jsii.sinvoke(cls, "fromMapName", [scope, id, map_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given principal identity permissions to perform the actions on this map.

        [disable-awslint:no-grants]

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4809bc2f3cfb1477d362738d53375b214633eb839957012fb44961fd99084aa6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRendering")
    def grant_rendering(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given identity permissions to rendering a map resource [disable-awslint:no-grants].

        :param grantee: -

        :stability: experimental
        :See: https://docs.aws.amazon.com/location/latest/developerguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-get-map-tiles
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e6cb38b13b5146f675aba863b0eee89900e770c744b3787f12fb9d74532e14)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRendering", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="mapArn")
    def map_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the Map.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapArn"))

    @builtins.property
    @jsii.member(jsii_name="mapCreateTime")
    def map_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the map resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="mapName")
    def map_name(self) -> builtins.str:
        '''(experimental) The name of the map.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapName"))

    @builtins.property
    @jsii.member(jsii_name="mapUpdateTime")
    def map_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the map resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "mapUpdateTime"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.MapProps",
    jsii_struct_bases=[],
    name_mapping={
        "style": "style",
        "custom_layers": "customLayers",
        "description": "description",
        "map_name": "mapName",
        "political_view": "politicalView",
    },
)
class MapProps:
    def __init__(
        self,
        *,
        style: "Style",
        custom_layers: typing.Optional[typing.Sequence["CustomLayer"]] = None,
        description: typing.Optional[builtins.str] = None,
        map_name: typing.Optional[builtins.str] = None,
        political_view: typing.Optional["PoliticalView"] = None,
    ) -> None:
        '''(experimental) Properties for the Amazon Location Service Map.

        :param style: (experimental) Specifies the map style selected from an available data provider.
        :param custom_layers: (experimental) Specifies the custom layers for the style. Default: - no custom layers
        :param description: (experimental) A description for the map. Default: - no description
        :param map_name: (experimental) A name for the map. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated
        :param political_view: (experimental) Specifies the map political view selected from an available data provider. The political view must be used in compliance with applicable laws, including those laws about mapping of the country or region where the maps, images, and other data and third-party content which you access through Amazon Location Service is made available. Default: - no political view

        :stability: experimental
        :exampleMetadata: infused

        Example::

            location.Map(self, "Map",
                map_name="my-map",
                style=location.Style.VECTOR_ESRI_NAVIGATION,
                custom_layers=[location.CustomLayer.POI]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1be245b764afdcc2db39c787bcdecaadb897250339c996f9d1a627507694f0)
            check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            check_type(argname="argument custom_layers", value=custom_layers, expected_type=type_hints["custom_layers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument map_name", value=map_name, expected_type=type_hints["map_name"])
            check_type(argname="argument political_view", value=political_view, expected_type=type_hints["political_view"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "style": style,
        }
        if custom_layers is not None:
            self._values["custom_layers"] = custom_layers
        if description is not None:
            self._values["description"] = description
        if map_name is not None:
            self._values["map_name"] = map_name
        if political_view is not None:
            self._values["political_view"] = political_view

    @builtins.property
    def style(self) -> "Style":
        '''(experimental) Specifies the map style selected from an available data provider.

        :stability: experimental
        '''
        result = self._values.get("style")
        assert result is not None, "Required property 'style' is missing"
        return typing.cast("Style", result)

    @builtins.property
    def custom_layers(self) -> typing.Optional[typing.List["CustomLayer"]]:
        '''(experimental) Specifies the custom layers for the style.

        :default: - no custom layers

        :stability: experimental
        '''
        result = self._values.get("custom_layers")
        return typing.cast(typing.Optional[typing.List["CustomLayer"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the map.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def map_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the map.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("map_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def political_view(self) -> typing.Optional["PoliticalView"]:
        '''(experimental) Specifies the map political view selected from an available data provider.

        The political view must be used in compliance with applicable laws, including those laws about mapping of the country or region where the maps,
        images, and other data and third-party content which you access through Amazon Location Service is made available.

        :default: - no political view

        :see: https://docs.aws.amazon.com/location/latest/developerguide/map-concepts.html#political-views
        :stability: experimental
        '''
        result = self._values.get("political_view")
        return typing.cast(typing.Optional["PoliticalView"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MapProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPlaceIndex)
class PlaceIndex(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.PlaceIndex",
):
    '''(experimental) A Place Index.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/places-concepts.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.PlaceIndex(self, "PlaceIndex",
            place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
            data_source=location.DataSource.HERE
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        data_source: typing.Optional["DataSource"] = None,
        description: typing.Optional[builtins.str] = None,
        intended_use: typing.Optional["IntendedUse"] = None,
        place_index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data_source: (experimental) Data source for the place index. Default: DataSource.ESRI
        :param description: (experimental) A description for the place index. Default: - no description
        :param intended_use: (experimental) Intend use for the results of an operation. Default: IntendedUse.SINGLE_USE
        :param place_index_name: (experimental) A name for the place index. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45352af3f6c713374f537c829e98f8db51c9684d0ccc55eedcc24f34b4115a7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PlaceIndexProps(
            data_source=data_source,
            description=description,
            intended_use=intended_use,
            place_index_name=place_index_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPlaceIndexArn")
    @builtins.classmethod
    def from_place_index_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        place_index_arn: builtins.str,
    ) -> "IPlaceIndex":
        '''(experimental) Use an existing place index by ARN.

        :param scope: -
        :param id: -
        :param place_index_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248ee08bccad0771877a2fcc90a9b08d64668a1cf797c90deb8c53fec79af85d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument place_index_arn", value=place_index_arn, expected_type=type_hints["place_index_arn"])
        return typing.cast("IPlaceIndex", jsii.sinvoke(cls, "fromPlaceIndexArn", [scope, id, place_index_arn]))

    @jsii.member(jsii_name="fromPlaceIndexName")
    @builtins.classmethod
    def from_place_index_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        place_index_name: builtins.str,
    ) -> "IPlaceIndex":
        '''(experimental) Use an existing place index by name.

        :param scope: -
        :param id: -
        :param place_index_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8d45231ce3a808cab553413e12ee6462eb276374dc71795aae0d1b4cbc7651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument place_index_name", value=place_index_name, expected_type=type_hints["place_index_name"])
        return typing.cast("IPlaceIndex", jsii.sinvoke(cls, "fromPlaceIndexName", [scope, id, place_index_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given principal identity permissions to perform the actions on this place index.

        [disable-awslint:no-grants]

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f4422a489b304c7bbc9bfabd28b7282eb0ff8e5a625351b01c27528783eef2)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantSearch")
    def grant_search(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given identity permissions to search using this index [disable-awslint:no-grants].

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d5a407a04ad6cfe5d7ad704c60c4485d954e37151f87d42b4a0f8aae3e8fcf)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantSearch", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexCreateTime")
    def place_index_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the place index resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexName"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexUpdateTime")
    def place_index_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the place index resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexUpdateTime"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.PlaceIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "description": "description",
        "intended_use": "intendedUse",
        "place_index_name": "placeIndexName",
    },
)
class PlaceIndexProps:
    def __init__(
        self,
        *,
        data_source: typing.Optional["DataSource"] = None,
        description: typing.Optional[builtins.str] = None,
        intended_use: typing.Optional["IntendedUse"] = None,
        place_index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a place index.

        :param data_source: (experimental) Data source for the place index. Default: DataSource.ESRI
        :param description: (experimental) A description for the place index. Default: - no description
        :param intended_use: (experimental) Intend use for the results of an operation. Default: IntendedUse.SINGLE_USE
        :param place_index_name: (experimental) A name for the place index. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        :exampleMetadata: infused

        Example::

            location.PlaceIndex(self, "PlaceIndex",
                place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
                data_source=location.DataSource.HERE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e973a0eacea346fe0253fb892d398121998cd91fd16cfdf5bb8eef740a62ae)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument intended_use", value=intended_use, expected_type=type_hints["intended_use"])
            check_type(argname="argument place_index_name", value=place_index_name, expected_type=type_hints["place_index_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_source is not None:
            self._values["data_source"] = data_source
        if description is not None:
            self._values["description"] = description
        if intended_use is not None:
            self._values["intended_use"] = intended_use
        if place_index_name is not None:
            self._values["place_index_name"] = place_index_name

    @builtins.property
    def data_source(self) -> typing.Optional["DataSource"]:
        '''(experimental) Data source for the place index.

        :default: DataSource.ESRI

        :stability: experimental
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional["DataSource"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the place index.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def intended_use(self) -> typing.Optional["IntendedUse"]:
        '''(experimental) Intend use for the results of an operation.

        :default: IntendedUse.SINGLE_USE

        :stability: experimental
        '''
        result = self._values.get("intended_use")
        return typing.cast(typing.Optional["IntendedUse"], result)

    @builtins.property
    def place_index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the place index.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("place_index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlaceIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.PoliticalView")
class PoliticalView(enum.Enum):
    '''(experimental) The map political view.

    :stability: experimental
    '''

    INDIA = "INDIA"
    '''(experimental) An India (IND) political view.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.PositionFiltering")
class PositionFiltering(enum.Enum):
    '''(experimental) The position filtering for the tracker resource.

    :stability: experimental
    '''

    TIME_BASED = "TIME_BASED"
    '''(experimental) Location updates are evaluated against linked geofence collections, but not every location update is stored.

    If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID.

    :stability: experimental
    '''
    DISTANCE_BASED = "DISTANCE_BASED"
    '''(experimental) If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map.

    :stability: experimental
    '''
    ACCURACY_BASED = "ACCURACY_BASED"
    '''(experimental) If the device has moved less than the measured accuracy, location updates are ignored.

    For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m,
    the second update is ignored if the device has moved less than 15 m.
    Ignored location updates are neither evaluated against linked geofence collections, nor stored.
    This can reduce the effects of GPS noise when displaying device trajectories on a map,
    and can help control your costs by reducing the number of geofence evaluations.

    :stability: experimental
    '''


@jsii.implements(IRouteCalculator)
class RouteCalculator(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.RouteCalculator",
):
    '''(experimental) A Route Calculator.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/places-concepts.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.RouteCalculator(self, "RouteCalculator",
            route_calculator_name="MyRouteCalculator",  # optional, defaults to a generated name
            data_source=location.DataSource.ESRI
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        data_source: "DataSource",
        description: typing.Optional[builtins.str] = None,
        route_calculator_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data_source: (experimental) Data source for the route calculator.
        :param description: (experimental) A description for the route calculator. Default: - no description
        :param route_calculator_name: (experimental) A name for the route calculator. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af41e5356dde101b2f7d28e76f19330d092400bd851a479a7c51d4b70d6ac1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RouteCalculatorProps(
            data_source=data_source,
            description=description,
            route_calculator_name=route_calculator_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRouteCalculatorArn")
    @builtins.classmethod
    def from_route_calculator_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        route_calculator_arn: builtins.str,
    ) -> "IRouteCalculator":
        '''(experimental) Use an existing route calculator by ARN.

        :param scope: -
        :param id: -
        :param route_calculator_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0d60ea9b320e4df73bddc9f80af1bcfeaa74f622e88af28e53323441a3387c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument route_calculator_arn", value=route_calculator_arn, expected_type=type_hints["route_calculator_arn"])
        return typing.cast("IRouteCalculator", jsii.sinvoke(cls, "fromRouteCalculatorArn", [scope, id, route_calculator_arn]))

    @jsii.member(jsii_name="fromRouteCalculatorName")
    @builtins.classmethod
    def from_route_calculator_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        route_calculator_name: builtins.str,
    ) -> "IRouteCalculator":
        '''(experimental) Use an existing route calculator by name.

        :param scope: -
        :param id: -
        :param route_calculator_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ef972620710e32d97c1d2b6fa9ebfc34b54c1c88a8f8c80857c7fdebbde2c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument route_calculator_name", value=route_calculator_name, expected_type=type_hints["route_calculator_name"])
        return typing.cast("IRouteCalculator", jsii.sinvoke(cls, "fromRouteCalculatorName", [scope, id, route_calculator_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given principal identity permissions to perform the actions on this route calculator.

        [disable-awslint:no-grants]

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3391610111a73c6ee96e73f5e17a3c9cddb23b67d8a28e1805bf8faaa22bc8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given identity permissions to access to a route calculator resource to calculate a route.

        [disable-awslint:no-grants]

        :param grantee: -

        :see: https://docs.aws.amazon.com/location/latest/developerguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-calculate-route
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c86b7ba6b7e16aa871608205c39da05ef7d2d1b2ada137a5f97dd34cb28c376)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorArn")
    def route_calculator_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the route calculator resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeCalculatorArn"))

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorCreateTime")
    def route_calculator_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the route calculator resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeCalculatorCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorName")
    def route_calculator_name(self) -> builtins.str:
        '''(experimental) The name of the route calculator.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeCalculatorName"))

    @builtins.property
    @jsii.member(jsii_name="routeCalculatorUpdateTime")
    def route_calculator_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the route calculator resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "routeCalculatorUpdateTime"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.RouteCalculatorProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "description": "description",
        "route_calculator_name": "routeCalculatorName",
    },
)
class RouteCalculatorProps:
    def __init__(
        self,
        *,
        data_source: "DataSource",
        description: typing.Optional[builtins.str] = None,
        route_calculator_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a route calculator.

        :param data_source: (experimental) Data source for the route calculator.
        :param description: (experimental) A description for the route calculator. Default: - no description
        :param route_calculator_name: (experimental) A name for the route calculator. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        :exampleMetadata: infused

        Example::

            location.RouteCalculator(self, "RouteCalculator",
                route_calculator_name="MyRouteCalculator",  # optional, defaults to a generated name
                data_source=location.DataSource.ESRI
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b8eda31c4f31d27ee29d731ed37fab83bdc7ebef9e0313fc6f1b2a411cf11c)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument route_calculator_name", value=route_calculator_name, expected_type=type_hints["route_calculator_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source": data_source,
        }
        if description is not None:
            self._values["description"] = description
        if route_calculator_name is not None:
            self._values["route_calculator_name"] = route_calculator_name

    @builtins.property
    def data_source(self) -> "DataSource":
        '''(experimental) Data source for the route calculator.

        :stability: experimental
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast("DataSource", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the route calculator.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_calculator_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the route calculator.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("route_calculator_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RouteCalculatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.Style")
class Style(enum.Enum):
    '''(experimental) The map style selected from an available data provider.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.Map(self, "Map",
            map_name="my-map",
            style=location.Style.VECTOR_ESRI_NAVIGATION,
            custom_layers=[location.CustomLayer.POI]
        )
    '''

    VECTOR_ESRI_NAVIGATION = "VECTOR_ESRI_NAVIGATION"
    '''(experimental) The Esri Navigation map style, which provides a detailed basemap for the world symbolized with a custom navigation map style that's designed for use during the day in mobile devices.

    It also includes a richer set of places, such as shops, services, restaurants, attractions,
    and other points of interest. Enable the POI layer by setting it in CustomLayers to leverage
    the additional places data.

    :stability: experimental
    '''
    RASTER_ESRI_IMAGERY = "RASTER_ESRI_IMAGERY"
    '''(experimental) The Esri Imagery map style.

    A raster basemap that provides one meter or better
    satellite and aerial imagery in many parts of the world and lower resolution
    satellite imagery worldwide.

    :stability: experimental
    '''
    VECTOR_ESRI_LIGHT_GRAY_CANVAS = "VECTOR_ESRI_LIGHT_GRAY_CANVAS"
    '''(experimental) The Esri Light Gray Canvas map style, which provides a detailed vector basemap with a light gray, neutral background style with minimal colors, labels, and features that's designed to draw attention to your thematic content.

    :stability: experimental
    '''
    VECTOR_ESRI_TOPOGRAPHIC = "VECTOR_ESRI_TOPOGRAPHIC"
    '''(experimental) The Esri Light map style, which provides a detailed vector basemap with a classic Esri map style.

    :stability: experimental
    '''
    VECTOR_ESRI_STREETS = "VECTOR_ESRI_STREETS"
    '''(experimental) The Esri Street Map style, which provides a detailed vector basemap for the world symbolized with a classic Esri street map style.

    The vector tile layer is similar
    in content and style to the World Street Map raster map.

    :stability: experimental
    '''
    VECTOR_ESRI_DARK_GRAY_CANVAS = "VECTOR_ESRI_DARK_GRAY_CANVAS"
    '''(experimental) The Esri Dark Gray Canvas map style.

    A vector basemap with a dark gray,
    neutral background with minimal colors, labels, and features that's designed
    to draw attention to your thematic content.

    :stability: experimental
    '''
    VECTOR_HERE_EXPLORE = "VECTOR_HERE_EXPLORE"
    '''(experimental) A default HERE map style containing a neutral, global map and its features including roads, buildings, landmarks, and water features.

    It also now includes
    a fully designed map of Japan.

    :stability: experimental
    '''
    RASTER_HERE_EXPLORE_SATELLITE = "RASTER_HERE_EXPLORE_SATELLITE"
    '''(experimental) A global map containing high resolution satellite imagery.

    :stability: experimental
    '''
    HYBRID_HERE_EXPLORE_SATELLITE = "HYBRID_HERE_EXPLORE_SATELLITE"
    '''(experimental) A global map displaying the road network, street names, and city labels over satellite imagery.

    This style will automatically retrieve both raster
    and vector tiles, and your charges will be based on total tiles retrieved.

    :stability: experimental
    '''
    VECTOR_HERE_CONTRAST = "VECTOR_HERE_CONTRAST"
    '''(experimental) The HERE Contrast (Berlin) map style is a high contrast detailed base map of the world that blends 3D and 2D rendering.

    :stability: experimental
    '''
    VECTOR_HERE_EXPLORE_TRUCK = "VECTOR_HERE_EXPLORE_TRUCK"
    '''(experimental) A global map containing truck restrictions and attributes (e.g. width / height / HAZMAT) symbolized with highlighted segments and icons on top of HERE Explore to support use cases within transport and logistics.

    :stability: experimental
    '''
    VECTOR_GRAB_STANDARD_LIGHT = "VECTOR_GRAB_STANDARD_LIGHT"
    '''(experimental) The Grab Standard Light map style provides a basemap with detailed land use coloring, area names, roads, landmarks, and points of interest covering Southeast Asia.

    :stability: experimental
    '''
    VECTOR_GRAB_STANDARD_DARK = "VECTOR_GRAB_STANDARD_DARK"
    '''(experimental) The Grab Standard Dark map style provides a dark variation of the standard basemap covering Southeast Asia.

    :stability: experimental
    '''
    VECTOR_OPEN_DATA_STANDARD_LIGHT = "VECTOR_OPEN_DATA_STANDARD_LIGHT"
    '''(experimental) The Open Data Standard Light map style provides a detailed basemap for the world suitable for website and mobile application use.

    The map includes highways major roads,
    minor roads, railways, water features, cities, parks, landmarks, building footprints,
    and administrative boundaries.

    :stability: experimental
    '''
    VECTOR_OPEN_DATA_STANDARD_DARK = "VECTOR_OPEN_DATA_STANDARD_DARK"
    '''(experimental) Open Data Standard Dark is a dark-themed map style that provides a detailed basemap for the world suitable for website and mobile application use.

    The map includes highways
    major roads, minor roads, railways, water features, cities, parks, landmarks,
    building footprints, and administrative boundaries.

    :stability: experimental
    '''
    VECTOR_OPEN_DATA_VISUALIZATION_LIGHT = "VECTOR_OPEN_DATA_VISUALIZATION_LIGHT"
    '''(experimental) The Open Data Visualization Light map style is a light-themed style with muted colors and fewer features that aids in understanding overlaid data.

    :stability: experimental
    '''
    VECTOR_OPEN_DATA_VISUALIZATION_DARK = "VECTOR_OPEN_DATA_VISUALIZATION_DARK"
    '''(experimental) The Open Data Visualization Dark map style is a dark-themed style with muted colors and fewer features that aids in understanding overlaid data.

    :stability: experimental
    '''


@jsii.implements(ITracker)
class Tracker(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.Tracker",
):
    '''(experimental) A Tracker.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/geofence-tracker-concepts.html#tracking-overview
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # role: iam.Role
        
        
        tracker = location.Tracker(self, "Tracker",
            tracker_name="MyTracker"
        )
        
        tracker.grant_read(role)
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        geofence_collections: typing.Optional[typing.Sequence["IGeofenceCollection"]] = None,
        kms_key: typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"] = None,
        kms_key_enable_geospatial_queries: typing.Optional[builtins.bool] = None,
        position_filtering: typing.Optional["PositionFiltering"] = None,
        tracker_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) A description for the tracker. Default: - no description
        :param event_bridge_enabled: (experimental) Send filtered device position updates to default EventBridge bus. Default: false
        :param geofence_collections: (experimental) An optional list of geofence collections to associate with the tracker resource. Default: - no geofence collections are associated
        :param kms_key: (experimental) The customer managed key to encrypt data. If you set customer managed key, the Bounding Polygon Queries feature will be disabled by default. You can choose to opt-in to the Bounding Polygon Queries feature by setting the kmsKeyEnableGeospatialQueries parameter to true. Default: - Use an AWS managed key
        :param kms_key_enable_geospatial_queries: (experimental) Whether to opt-in to the Bounding Polygon Queries feature with customer managed key. Default: false
        :param position_filtering: (experimental) The position filtering for the tracker resource. Default: PositionFiltering.TIME_BASED
        :param tracker_name: (experimental) A name for the tracker. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2211a106e7e5710c4de360395860635ff3245ee6a83d2bf78c7eeb37b0e6f79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TrackerProps(
            description=description,
            event_bridge_enabled=event_bridge_enabled,
            geofence_collections=geofence_collections,
            kms_key=kms_key,
            kms_key_enable_geospatial_queries=kms_key_enable_geospatial_queries,
            position_filtering=position_filtering,
            tracker_name=tracker_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTrackerArn")
    @builtins.classmethod
    def from_tracker_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        tracker_arn: builtins.str,
    ) -> "ITracker":
        '''(experimental) Use an existing tracker by ARN.

        :param scope: -
        :param id: -
        :param tracker_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aaf78e9d6747e25be75a149cccb6a48e78969dea61646f87e4af65300cfe442)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tracker_arn", value=tracker_arn, expected_type=type_hints["tracker_arn"])
        return typing.cast("ITracker", jsii.sinvoke(cls, "fromTrackerArn", [scope, id, tracker_arn]))

    @jsii.member(jsii_name="fromTrackerName")
    @builtins.classmethod
    def from_tracker_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        tracker_name: builtins.str,
    ) -> "ITracker":
        '''(experimental) Use an existing tracker by name.

        :param scope: -
        :param id: -
        :param tracker_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecfa3fa986d96f28caf6d0a033616b0ad71938a8fde3a6d61857cd92df89d01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tracker_name", value=tracker_name, expected_type=type_hints["tracker_name"])
        return typing.cast("ITracker", jsii.sinvoke(cls, "fromTrackerName", [scope, id, tracker_name]))

    @jsii.member(jsii_name="addGeofenceCollections")
    def add_geofence_collections(
        self,
        *geofence_collections: "IGeofenceCollection",
    ) -> None:
        '''(experimental) Add Geofence Collections which are associated to the tracker resource.

        :param geofence_collections: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c67f04e3612462490f986f42955ba19b27bf0ec5bf1600668e3ca817696f2a)
            check_type(argname="argument geofence_collections", value=geofence_collections, expected_type=typing.Tuple[type_hints["geofence_collections"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addGeofenceCollections", [*geofence_collections]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given principal identity permissions to perform the actions on this tracker.

        [disable-awslint:no-grants]

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b320ed516d390c019ee16a3586fa4951639478b393bbffb39f4520f1a3659257)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given identity permissions to read device positions from a tracker [disable-awslint:no-grants].

        :param grantee: -

        :see: https://docs.aws.amazon.com/location/latest/developerguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-read-only-trackers
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b001f1b18f9c1f021c2dddea61f197114a6e228ae3d252b1435029a865e6a5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantUpdateDevicePositions")
    def grant_update_device_positions(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given identity permissions to update device positions for a tracker [disable-awslint:no-grants].

        :param grantee: -

        :see: https://docs.aws.amazon.com/location/latest/developerguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-read-only-trackers
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ff8457f8444ff5ff29f27ab6030e3a070222cfdd44c714ced8ef9fed0916b5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantUpdateDevicePositions", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="trackerArn")
    def tracker_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the tracker resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerArn"))

    @builtins.property
    @jsii.member(jsii_name="trackerCreateTime")
    def tracker_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the tracker resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="trackerName")
    def tracker_name(self) -> builtins.str:
        '''(experimental) The name of the tracker.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerName"))

    @builtins.property
    @jsii.member(jsii_name="trackerUpdateTime")
    def tracker_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the tracker resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackerUpdateTime"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.TrackerProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_bridge_enabled": "eventBridgeEnabled",
        "geofence_collections": "geofenceCollections",
        "kms_key": "kmsKey",
        "kms_key_enable_geospatial_queries": "kmsKeyEnableGeospatialQueries",
        "position_filtering": "positionFiltering",
        "tracker_name": "trackerName",
    },
)
class TrackerProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        geofence_collections: typing.Optional[typing.Sequence["IGeofenceCollection"]] = None,
        kms_key: typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"] = None,
        kms_key_enable_geospatial_queries: typing.Optional[builtins.bool] = None,
        position_filtering: typing.Optional["PositionFiltering"] = None,
        tracker_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a tracker.

        :param description: (experimental) A description for the tracker. Default: - no description
        :param event_bridge_enabled: (experimental) Send filtered device position updates to default EventBridge bus. Default: false
        :param geofence_collections: (experimental) An optional list of geofence collections to associate with the tracker resource. Default: - no geofence collections are associated
        :param kms_key: (experimental) The customer managed key to encrypt data. If you set customer managed key, the Bounding Polygon Queries feature will be disabled by default. You can choose to opt-in to the Bounding Polygon Queries feature by setting the kmsKeyEnableGeospatialQueries parameter to true. Default: - Use an AWS managed key
        :param kms_key_enable_geospatial_queries: (experimental) Whether to opt-in to the Bounding Polygon Queries feature with customer managed key. Default: false
        :param position_filtering: (experimental) The position filtering for the tracker resource. Default: PositionFiltering.TIME_BASED
        :param tracker_name: (experimental) A name for the tracker. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # role: iam.Role
            
            
            tracker = location.Tracker(self, "Tracker",
                tracker_name="MyTracker"
            )
            
            tracker.grant_read(role)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599de512474f3cd3fd707f8824c641cdab90d7a71bfa4bb5c4de59d0e1575deb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            check_type(argname="argument geofence_collections", value=geofence_collections, expected_type=type_hints["geofence_collections"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument kms_key_enable_geospatial_queries", value=kms_key_enable_geospatial_queries, expected_type=type_hints["kms_key_enable_geospatial_queries"])
            check_type(argname="argument position_filtering", value=position_filtering, expected_type=type_hints["position_filtering"])
            check_type(argname="argument tracker_name", value=tracker_name, expected_type=type_hints["tracker_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_bridge_enabled is not None:
            self._values["event_bridge_enabled"] = event_bridge_enabled
        if geofence_collections is not None:
            self._values["geofence_collections"] = geofence_collections
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if kms_key_enable_geospatial_queries is not None:
            self._values["kms_key_enable_geospatial_queries"] = kms_key_enable_geospatial_queries
        if position_filtering is not None:
            self._values["position_filtering"] = position_filtering
        if tracker_name is not None:
            self._values["tracker_name"] = tracker_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the tracker.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_bridge_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Send filtered device position updates to default EventBridge bus.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("event_bridge_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def geofence_collections(
        self,
    ) -> typing.Optional[typing.List["IGeofenceCollection"]]:
        '''(experimental) An optional list of geofence collections to associate with the tracker resource.

        :default: - no geofence collections are associated

        :stability: experimental
        '''
        result = self._values.get("geofence_collections")
        return typing.cast(typing.Optional[typing.List["IGeofenceCollection"]], result)

    @builtins.property
    def kms_key(
        self,
    ) -> typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"]:
        '''(experimental) The customer managed key to encrypt data.

        If you set customer managed key, the Bounding Polygon Queries feature will be disabled by default.
        You can choose to opt-in to the Bounding Polygon Queries feature by setting the kmsKeyEnableGeospatialQueries parameter to true.

        :default: - Use an AWS managed key

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"], result)

    @builtins.property
    def kms_key_enable_geospatial_queries(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to opt-in to the Bounding Polygon Queries feature with customer managed key.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("kms_key_enable_geospatial_queries")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def position_filtering(self) -> typing.Optional["PositionFiltering"]:
        '''(experimental) The position filtering for the tracker resource.

        :default: PositionFiltering.TIME_BASED

        :stability: experimental
        '''
        result = self._values.get("position_filtering")
        return typing.cast(typing.Optional["PositionFiltering"], result)

    @builtins.property
    def tracker_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the tracker.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("tracker_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrackerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApiKey)
class ApiKey(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.ApiKey",
):
    '''(experimental) An API Key.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/using-apikeys.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.ApiKey(self, "APIKeyAny",
            # specify allowed actions
            allow_maps_actions=[location.AllowMapsAction.GET_STATIC_MAP
            ],
            allow_places_actions=[location.AllowPlacesAction.GET_PLACE
            ],
            allow_routes_actions=[location.AllowRoutesAction.CALCULATE_ISOLINES
            ]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        allow_maps_actions: typing.Optional[typing.Sequence["AllowMapsAction"]] = None,
        allow_places_actions: typing.Optional[typing.Sequence["AllowPlacesAction"]] = None,
        allow_referers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_routes_actions: typing.Optional[typing.Sequence["AllowRoutesAction"]] = None,
        api_key_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[datetime.datetime] = None,
        force_delete: typing.Optional[builtins.bool] = None,
        force_update: typing.Optional[builtins.bool] = None,
        no_expiry: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_maps_actions: (experimental) A list of allowed actions for Maps that an API key resource grants permissions to perform. Default: - no actions for Maps are permitted
        :param allow_places_actions: (experimental) A list of allowed actions for Places that an API key resource grants permissions to perform. Default: - no actions for Places are permitted
        :param allow_referers: (experimental) An optional list of allowed HTTP referers for which requests must originate from. Requests using this API key from other domains will not be allowed. Default: - no Referer
        :param allow_routes_actions: (experimental) A list of allowed actions for Routes that an API key resource grants permissions to perform. Default: - no actions for Routes are permitted
        :param api_key_name: (experimental) A name for the api key. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Must be a unique API key name. Default: - A name is automatically generated
        :param description: (experimental) A description for the api key. Default: - no description
        :param expire_time: (experimental) The optional timestamp for when the API key resource will expire. ``expireTime`` must be set when ``noExpiry`` is false or undefined. When ``expireTime`` is not set, ``noExpiry`` must be ``true``. Default: undefined - The API Key never expires
        :param force_delete: (experimental) ``forceDelete`` bypasses an API key's expiry conditions and deletes the key. Set the parameter true to delete the key or to false to not preemptively delete the API key. Default: undefined - not force delete
        :param force_update: (experimental) The boolean flag to be included for updating ExpireTime or Restrictions details. Must be set to true to update an API key resource that has been used in the past 7 days. False if force update is not preferred. Default: undefined - not force update
        :param no_expiry: (experimental) Whether the API key should expire. Set to ``true`` when ``expireTime`` is not set. When you set ``expireTime``, ``noExpiry`` must be ``false`` or ``undefined``. Default: undefined - The API Key expires at ``expireTime``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21e5d885f8c36b7fe1d50d74aa35023dd7a4c6fe81403cef115f4af8c904e42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApiKeyProps(
            allow_maps_actions=allow_maps_actions,
            allow_places_actions=allow_places_actions,
            allow_referers=allow_referers,
            allow_routes_actions=allow_routes_actions,
            api_key_name=api_key_name,
            description=description,
            expire_time=expire_time,
            force_delete=force_delete,
            force_update=force_update,
            no_expiry=no_expiry,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromApiKeyArn")
    @builtins.classmethod
    def from_api_key_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        api_key_arn: builtins.str,
    ) -> "IApiKey":
        '''(experimental) Use an existing api key by ARN.

        :param scope: -
        :param id: -
        :param api_key_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e119dff406ab60af0446492eed2f6ee397c8dad047df9c4776789c0a34217449)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument api_key_arn", value=api_key_arn, expected_type=type_hints["api_key_arn"])
        return typing.cast("IApiKey", jsii.sinvoke(cls, "fromApiKeyArn", [scope, id, api_key_arn]))

    @jsii.member(jsii_name="fromApiKeyName")
    @builtins.classmethod
    def from_api_key_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        api_key_name: builtins.str,
    ) -> "IApiKey":
        '''(experimental) Use an existing api key by name.

        :param scope: -
        :param id: -
        :param api_key_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96466e2c8f7620fd4ea0ee3983e5c26d20f7708c9f013a3c40dea56272fc0afe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument api_key_name", value=api_key_name, expected_type=type_hints["api_key_name"])
        return typing.cast("IApiKey", jsii.sinvoke(cls, "fromApiKeyName", [scope, id, api_key_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyArn")
    def api_key_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the api key resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKeyArn"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyCreateTime")
    def api_key_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the api key resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKeyCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyName")
    def api_key_name(self) -> builtins.str:
        '''(experimental) The name of the api key.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKeyName"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyUpdateTime")
    def api_key_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the api key resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiKeyUpdateTime"))


@jsii.implements(IGeofenceCollection)
class GeofenceCollection(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.GeofenceCollection",
):
    '''(experimental) A Geofence Collection.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/geofence-tracker-concepts.html#geofence-overview
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # key: kms.Key
        
        
        location.GeofenceCollection(self, "GeofenceCollection",
            geofence_collection_name="MyGeofenceCollection",  # optional, defaults to a generated name
            kms_key=key
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        geofence_collection_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional["_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) A description for the geofence collection. Default: - no description
        :param geofence_collection_name: (experimental) A name for the geofence collection. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated
        :param kms_key: (experimental) The customer managed to encrypt your data. Default: - Use an AWS managed key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46515b575b3aea76a1e7b6fb58cf0b2fb74b8eab224b06940310470f76183f7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GeofenceCollectionProps(
            description=description,
            geofence_collection_name=geofence_collection_name,
            kms_key=kms_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGeofenceCollectionArn")
    @builtins.classmethod
    def from_geofence_collection_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        geofence_collection_arn: builtins.str,
    ) -> "IGeofenceCollection":
        '''(experimental) Use an existing geofence collection by ARN.

        :param scope: -
        :param id: -
        :param geofence_collection_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb916f69d0fe4399d9278aecbd25559dc350b950a717f4bd2cbd4262712301a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument geofence_collection_arn", value=geofence_collection_arn, expected_type=type_hints["geofence_collection_arn"])
        return typing.cast("IGeofenceCollection", jsii.sinvoke(cls, "fromGeofenceCollectionArn", [scope, id, geofence_collection_arn]))

    @jsii.member(jsii_name="fromGeofenceCollectionName")
    @builtins.classmethod
    def from_geofence_collection_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        geofence_collection_name: builtins.str,
    ) -> "IGeofenceCollection":
        '''(experimental) Use an existing geofence collection by name.

        :param scope: -
        :param id: -
        :param geofence_collection_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d0b73947b903aff64888db96cb07d68b0f8e10dea23e7b62d37c937970f738)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument geofence_collection_name", value=geofence_collection_name, expected_type=type_hints["geofence_collection_name"])
        return typing.cast("IGeofenceCollection", jsii.sinvoke(cls, "fromGeofenceCollectionName", [scope, id, geofence_collection_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        *actions: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given principal identity permissions to perform the actions on this geofence collection.

        [disable-awslint:no-grants]

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2b0b7d842c9c09abfd524da8f0b754d8bd5dac77b3ac3c48fa2e42486e2816)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant the given identity permissions to read this geofence collection [disable-awslint:no-grants].

        :param grantee: -

        :see: https://docs.aws.amazon.com/location/latest/developerguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-read-only-geofences
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75e3f479665495211d879861c613331d0480d70c6adba492329ff9bc728ba0d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [grantee]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionArn")
    def geofence_collection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the geofence collection resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionArn"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionCreateTime")
    def geofence_collection_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the geofence collection resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionName")
    def geofence_collection_name(self) -> builtins.str:
        '''(experimental) The name of the geofence collection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionName"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionUpdateTime")
    def geofence_collection_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the geofence collection resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionUpdateTime"))


__all__ = [
    "AllowMapsAction",
    "AllowPlacesAction",
    "AllowRoutesAction",
    "ApiKey",
    "ApiKeyProps",
    "CustomLayer",
    "DataSource",
    "GeofenceCollection",
    "GeofenceCollectionProps",
    "IApiKey",
    "IGeofenceCollection",
    "IMap",
    "IPlaceIndex",
    "IRouteCalculator",
    "ITracker",
    "IntendedUse",
    "Map",
    "MapProps",
    "PlaceIndex",
    "PlaceIndexProps",
    "PoliticalView",
    "PositionFiltering",
    "RouteCalculator",
    "RouteCalculatorProps",
    "Style",
    "Tracker",
    "TrackerProps",
]

publication.publish()

def _typecheckingstub__fefe79c3c3f11720df74a6b3ca3ee04549f9cebd75d8bb48ff783b2661ff94c5(
    *,
    allow_maps_actions: typing.Optional[typing.Sequence[AllowMapsAction]] = None,
    allow_places_actions: typing.Optional[typing.Sequence[AllowPlacesAction]] = None,
    allow_referers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_routes_actions: typing.Optional[typing.Sequence[AllowRoutesAction]] = None,
    api_key_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[datetime.datetime] = None,
    force_delete: typing.Optional[builtins.bool] = None,
    force_update: typing.Optional[builtins.bool] = None,
    no_expiry: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdd3197c12b6d89ece6dfce72294a7f00d61e7a28da5918141a6d8e57c35fc5(
    *,
    description: typing.Optional[builtins.str] = None,
    geofence_collection_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eadf3225dad1551d12c46d02a8cc99fbedbc63844ea7721e06578672f9d6ec8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    style: Style,
    custom_layers: typing.Optional[typing.Sequence[CustomLayer]] = None,
    description: typing.Optional[builtins.str] = None,
    map_name: typing.Optional[builtins.str] = None,
    political_view: typing.Optional[PoliticalView] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f608f3b299254757f5028a9f2e4f5929f7b7427cbe4e467211bda7962954150d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    map_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7019e487b4362e4e8d871612adfc04be5a9738c6cab349a06b8592cc88ba9266(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    map_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4809bc2f3cfb1477d362738d53375b214633eb839957012fb44961fd99084aa6(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e6cb38b13b5146f675aba863b0eee89900e770c744b3787f12fb9d74532e14(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1be245b764afdcc2db39c787bcdecaadb897250339c996f9d1a627507694f0(
    *,
    style: Style,
    custom_layers: typing.Optional[typing.Sequence[CustomLayer]] = None,
    description: typing.Optional[builtins.str] = None,
    map_name: typing.Optional[builtins.str] = None,
    political_view: typing.Optional[PoliticalView] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45352af3f6c713374f537c829e98f8db51c9684d0ccc55eedcc24f34b4115a7d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_source: typing.Optional[DataSource] = None,
    description: typing.Optional[builtins.str] = None,
    intended_use: typing.Optional[IntendedUse] = None,
    place_index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248ee08bccad0771877a2fcc90a9b08d64668a1cf797c90deb8c53fec79af85d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    place_index_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8d45231ce3a808cab553413e12ee6462eb276374dc71795aae0d1b4cbc7651(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    place_index_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f4422a489b304c7bbc9bfabd28b7282eb0ff8e5a625351b01c27528783eef2(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d5a407a04ad6cfe5d7ad704c60c4485d954e37151f87d42b4a0f8aae3e8fcf(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e973a0eacea346fe0253fb892d398121998cd91fd16cfdf5bb8eef740a62ae(
    *,
    data_source: typing.Optional[DataSource] = None,
    description: typing.Optional[builtins.str] = None,
    intended_use: typing.Optional[IntendedUse] = None,
    place_index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af41e5356dde101b2f7d28e76f19330d092400bd851a479a7c51d4b70d6ac1f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_source: DataSource,
    description: typing.Optional[builtins.str] = None,
    route_calculator_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0d60ea9b320e4df73bddc9f80af1bcfeaa74f622e88af28e53323441a3387c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    route_calculator_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ef972620710e32d97c1d2b6fa9ebfc34b54c1c88a8f8c80857c7fdebbde2c7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    route_calculator_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3391610111a73c6ee96e73f5e17a3c9cddb23b67d8a28e1805bf8faaa22bc8(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c86b7ba6b7e16aa871608205c39da05ef7d2d1b2ada137a5f97dd34cb28c376(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b8eda31c4f31d27ee29d731ed37fab83bdc7ebef9e0313fc6f1b2a411cf11c(
    *,
    data_source: DataSource,
    description: typing.Optional[builtins.str] = None,
    route_calculator_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2211a106e7e5710c4de360395860635ff3245ee6a83d2bf78c7eeb37b0e6f79(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    geofence_collections: typing.Optional[typing.Sequence[IGeofenceCollection]] = None,
    kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    kms_key_enable_geospatial_queries: typing.Optional[builtins.bool] = None,
    position_filtering: typing.Optional[PositionFiltering] = None,
    tracker_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaf78e9d6747e25be75a149cccb6a48e78969dea61646f87e4af65300cfe442(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    tracker_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecfa3fa986d96f28caf6d0a033616b0ad71938a8fde3a6d61857cd92df89d01(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    tracker_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c67f04e3612462490f986f42955ba19b27bf0ec5bf1600668e3ca817696f2a(
    *geofence_collections: IGeofenceCollection,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b320ed516d390c019ee16a3586fa4951639478b393bbffb39f4520f1a3659257(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b001f1b18f9c1f021c2dddea61f197114a6e228ae3d252b1435029a865e6a5(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ff8457f8444ff5ff29f27ab6030e3a070222cfdd44c714ced8ef9fed0916b5(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599de512474f3cd3fd707f8824c641cdab90d7a71bfa4bb5c4de59d0e1575deb(
    *,
    description: typing.Optional[builtins.str] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    geofence_collections: typing.Optional[typing.Sequence[IGeofenceCollection]] = None,
    kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
    kms_key_enable_geospatial_queries: typing.Optional[builtins.bool] = None,
    position_filtering: typing.Optional[PositionFiltering] = None,
    tracker_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21e5d885f8c36b7fe1d50d74aa35023dd7a4c6fe81403cef115f4af8c904e42(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_maps_actions: typing.Optional[typing.Sequence[AllowMapsAction]] = None,
    allow_places_actions: typing.Optional[typing.Sequence[AllowPlacesAction]] = None,
    allow_referers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_routes_actions: typing.Optional[typing.Sequence[AllowRoutesAction]] = None,
    api_key_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[datetime.datetime] = None,
    force_delete: typing.Optional[builtins.bool] = None,
    force_update: typing.Optional[builtins.bool] = None,
    no_expiry: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e119dff406ab60af0446492eed2f6ee397c8dad047df9c4776789c0a34217449(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    api_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96466e2c8f7620fd4ea0ee3983e5c26d20f7708c9f013a3c40dea56272fc0afe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    api_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46515b575b3aea76a1e7b6fb58cf0b2fb74b8eab224b06940310470f76183f7c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    geofence_collection_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_interfaces_aws_kms_ceddda9d.IKeyRef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb916f69d0fe4399d9278aecbd25559dc350b950a717f4bd2cbd4262712301a0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    geofence_collection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d0b73947b903aff64888db96cb07d68b0f8e10dea23e7b62d37c937970f738(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    geofence_collection_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2b0b7d842c9c09abfd524da8f0b754d8bd5dac77b3ac3c48fa2e42486e2816(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75e3f479665495211d879861c613331d0480d70c6adba492329ff9bc728ba0d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IApiKey, IGeofenceCollection, IMap, IPlaceIndex, IRouteCalculator, ITracker]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
