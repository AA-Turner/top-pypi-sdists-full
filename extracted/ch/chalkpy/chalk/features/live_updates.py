from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

import cloudpickle

from chalk.utils import notebook
from chalk.utils.log_with_context import get_logger

if TYPE_CHECKING:
    import IPython
    import IPython.core.interactiveshell
    import pydantic.fields as pydantic_fields

    from chalk.client.models import UpdateGraphEntityResponse
    from chalk.features.feature_set import Features
    from chalk.features.resolver import OfflineResolver, OnlineResolver, Resolver

else:
    try:
        import pydantic.v1.fields as pydantic_fields
    except ImportError:
        import pydantic.fields as pydantic_fields

_logger = get_logger(__name__)

NO_CLIENT_HELPTEXT = """A Chalk client has not yet been initialized in this notebook.
This means that you can create resolvers and features and test them locally, but
they will not be synced to Chalk's servers. To create a client, run the following
in your notebook:

>>> from chalk.client import ChalkClient
>>> client = ChalkClient(branch="my_branch_name")

This will create a Chalk connection pointed at the branch of your choice. New resolvers
or features that you create will be automatically uploaded to that branch. To create a
new branch, use the Chalk CLI:

$ chalk apply --branch my_branch_name
"""

NO_BRANCH_HELPTEXT = """The Chalk client on this notebook does not have a branch set.
Modifications to resolvers or features cannot be uploaded to Chalk until a branch is
specified. You can create a new branch via the Chalk CLI by running:

$ chalk apply --branch my_branch_name

Then, in Python you can point a Chalk client at an existing branch with the following code:

>>> from chalk.client import ChalkClient
>>> client = ChalkClient(branch="my_branch_name")
"""


def serialize_entity(obj: Any) -> bytes:
    """
    Special logic for making sure resolvers/features are serializable.
    We attach a lot of fancy state to these objects which isn't always pickle-able.
    """
    from chalk.features.resolver import Resolver

    if isinstance(obj, Resolver):
        # Replace lazy callable for parsing (which isn't pickle-able) with the computed value
        obj._do_parse()  # pyright: ignore[reportPrivateUsage]
    return cloudpickle.dumps(obj)


def _upload_object(obj: Any) -> UpdateGraphEntityResponse:
    pickled_obj = serialize_entity(obj)

    from chalk.client.client_impl import ChalkAPIClientImpl

    client = ChalkAPIClientImpl.latest_client
    if client is None:
        raise RuntimeError(NO_CLIENT_HELPTEXT)
    if client.get_branch() is None:
        raise RuntimeError(NO_BRANCH_HELPTEXT)
    try:
        resp = client.send_updated_entity(environment=None, pickled_entity=pickled_obj)
    except:
        _logger.error(
            f"Failed to upload features/resolvers to branch server on branch '{client.get_branch()}'.", exc_info=True
        )
        raise
    return resp


def _print_responses(responses: list[UpdateGraphEntityResponse]):
    from chalk.client.models import SingleEntityUpdate

    all_errors = [e for r in responses for e in (r.errors or [])]
    if all_errors:
        for e in all_errors:
            _logger.error(e.message)
        return

    all_updated_objects: list[tuple[str, SingleEntityUpdate]] = []
    for resp in responses:
        all_updated_objects.extend(("+", o) for o in (resp.added or []))
        all_updated_objects.extend(("*", o) for o in (resp.modified or []))
        all_updated_objects.extend(("-", o) for o in (resp.removed or []))
        all_updated_objects.sort(key=lambda p: p[1].entity_fqn)
    for update_char, update_resp in all_updated_objects:
        if update_resp.entity_fqn.split(".")[-1].startswith("__chalk"):
            continue
        print(f"{update_char}\t{update_resp.entity_type}: {update_resp.entity_fqn}")


def _add_object_to_cache(obj: OnlineResolver | OfflineResolver | type[Features]):
    if notebook.is_defined_in_module(obj) and not notebook.is_defined_in_cell_magic(obj):
        # If resolver is defined in a module that's imported by a notebook, don't deploy it.
        # This is to avoid re-deploying every feature if customer imports their existing codebase into a notebook.
        return
    from chalk.features.feature_set import is_features_cls
    from chalk.features.resolver import OfflineResolver, OnlineResolver

    if isinstance(obj, (OnlineResolver, OfflineResolver)):
        _UPDATED_RESOLVERS_CACHE[obj.fqn] = obj
    elif is_features_cls(obj):
        _UPDATED_FEATURES_CACHE[obj.namespace] = obj
    else:
        raise ValueError(f"Unsupported entity type: {obj}")


# features.namespace => features
_UPDATED_FEATURES_CACHE: dict[str, type["Features"]] = {}
# resolver.fqn => resolver
_UPDATED_RESOLVERS_CACHE: dict[str, OnlineResolver | OfflineResolver] = {}


def _clear_entity_update_cache(*args: Any, **kwargs: Any):
    """
    :param _, __: IPython runtime might pass in some objects; ignored
    """
    del args, kwargs
    _UPDATED_RESOLVERS_CACHE.clear()
    _UPDATED_FEATURES_CACHE.clear()


def _deploy_objects(entities: Sequence[type[Features] | Resolver]):
    from chalk.features.feature_set import is_features_cls
    from chalk.features.resolver import Resolver

    # Upload
    resps: list[UpdateGraphEntityResponse] = []
    num_resolvers = len([e for e in entities if isinstance(e, Resolver)])
    num_feature_classes = len([e for e in entities if is_features_cls(e)])
    log_messages = filter(
        None,
        [
            _pluralize(num_feature_classes, "feature class", "feature classes"),
            _pluralize(num_resolvers, "resolver", "resolvers"),
        ],
    )
    log_message_combined = " and ".join(log_messages)
    print(f"Uploading {log_message_combined} to branch server...")
    for e in entities:
        resps.append(_upload_object(e))
    _print_responses(resps)


def _pluralize(count: int, singular_word: str, plural_word: str) -> str | None:
    if count == 0:
        return None
    return f"{count} {singular_word if count == 1 else plural_word}"


def _deploy_objects_from_cache(result: IPython.core.interactiveshell.ExecutionResult):
    """
    Runs after a Jupyter cell has finished execution.
    Validates and deploys any new entities defined in the cell to the branch server.
    TODO (rkargon): Currently this uploads objects one at a time.
    This works and should still avoid the forward reference/validation issues in the client.
    :param result: IPython result object.
    """
    from chalk.client.client_impl import ChalkAPIClientImpl

    if result.error_in_exec is not None:
        return
    if len(_UPDATED_FEATURES_CACHE) == 0 and len(_UPDATED_RESOLVERS_CACHE) == 0:
        return

    if ChalkAPIClientImpl.latest_client and ChalkAPIClientImpl.latest_client.get_branch() is None:
        from IPython.core.display import display_markdown

        display_markdown(
            "Chalk client has no branch set, not updating resolvers/features to server.",
            raw=True,
        )
        return
    _deploy_objects(list(_UPDATED_FEATURES_CACHE.values()) + list(_UPDATED_RESOLVERS_CACHE.values()))
    _clear_entity_update_cache()


def register_cell_hooks():
    # noinspection PyUnresolvedReferences
    ip = get_ipython()  # type: ignore -- this will be defined if in an interactive environment
    ip.events.register(notebook.IPythonEvents.PRE_RUN_CELL.value, _clear_entity_update_cache)
    ip.events.register(notebook.IPythonEvents.POST_RUN_CELL.value, _deploy_objects_from_cache)


def register_pydantic_serializer():
    """
    Cython-enabled Pydantic doesn't interact properly with cloudpickle.
    (https://github.com/cloudpipe/cloudpickle/issues/408)

    Sometimes a customer will try to create a Pydantic model in a notebook
    to use as a struct in a feature class, in which case updating features
    will fail due to a pickling error. As a result, we need to register a
    customer (de)serializer with cloudpickle for Pydantic models.

    Borrowed from: https://github.com/ray-project/ray/blob/master/python/ray/util/serialization_addons.py
    """

    def _custom_serializer(o: pydantic_fields.ModelField):
        return {
            "name": o.name,
            # outer_type_ is the original type for ModelFields,
            # while type_ can be updated later with the nested type
            # like int for List[int].
            "type_": o.outer_type_,
            "class_validators": o.class_validators,
            "model_config": o.model_config,
            "default": o.default,
            "default_factory": o.default_factory,
            "required": o.required,
            "alias": o.alias,
            "field_info": o.field_info,
        }

    def _custom_deserializer(kwargs: dict[str, Any]):
        return (pydantic_fields.ModelField(**kwargs),)

    def _cloud_pickler_reducer(obj: Any):
        return _custom_deserializer, (_custom_serializer(obj),)

    # See https://github.com/ray-project/ray/blob/7fe451a8b83ea789d17fef3b8a954164008bf8a8/python/ray/_private/serialization.py#L168
    cloudpickle.CloudPickler.dispatch[pydantic_fields.ModelField] = _cloud_pickler_reducer  # type: ignore


def register_live_updates_if_in_notebook(cls: Any):
    """
    This is called manually by the modules containing FeatureSetBase and Resolver due to circular imports
    :param cls:
    :return:
    """
    if notebook.is_notebook():
        if not hasattr(cls, "hook"):
            raise TypeError(f"{cls} has no hook attribute")
        setattr(cls, "hook", _add_object_to_cache)


def initialize_live_updates_if_in_notebook():
    if not notebook.is_notebook():
        return

    register_cell_hooks()
    register_pydantic_serializer()


# initialize_live_updates_if_in_notebook() # Deprecated for now, will re-enable once we support live updates on the new branch server
