# This package is built to improve the error message of typeguard 2.0. We can deprecate this module once we upgrade the
# `typeguard` to 4.0+. Details are avaiable in https://tecton.atlassian.net/browse/TEC-19929.

from functools import wraps

from typeguard import typechecked

from tecton.framework import feature


_BATCH_FEATURE_VIEW = "batch_feature_view"
_STREAM_FEATURE_VIEW = "stream_feature_view"
_REALTIME_FEATURE_VIEW = "realtime_feature_view"


def batch_feature_view_typechecked(f):
    return _internal_typechecked(f, _BATCH_FEATURE_VIEW)


def stream_feature_view_typechecked(f):
    return _internal_typechecked(f, _STREAM_FEATURE_VIEW)


def realtime_feature_view_typechecked(f):
    return _internal_typechecked(f, _REALTIME_FEATURE_VIEW)


def _internal_typechecked(f, fco_type):
    decorated_func = typechecked(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs.get("features"):
            for i, item in enumerate(kwargs["features"]):
                if fco_type == _BATCH_FEATURE_VIEW and not isinstance(item, feature.Feature):
                    msg = f"`features` expects a list of `Aggregate` or a list of `Union[Attribute, Embedding]`, but features[{i}] is '${item.__class__}'"
                    raise TypeError(msg)
                if fco_type == _STREAM_FEATURE_VIEW and not isinstance(item, feature.Feature):
                    msg = f"`features` expects a list of `Aggregate` or a list of `Attribute`, but features[{i}] is '${item.__class__}'"
                    raise TypeError(msg)
                if fco_type == _REALTIME_FEATURE_VIEW and not isinstance(
                    item, (feature.Attribute, feature.Calculation)
                ):
                    msg = f"`features` expects a list of `Union[Attribute, Calculation]`, but features[{i}] is '${item.__class__}'"
                    raise TypeError(msg)
        return decorated_func(*args, **kwargs)

    return wrapper
