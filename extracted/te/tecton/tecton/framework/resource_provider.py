import inspect
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

import attrs
from typeguard import typechecked

from tecton._internals import errors
from tecton._internals import sdk_decorators
from tecton._internals import validations_api
from tecton._internals.repo import function_serialization
from tecton.framework import base_tecton_object
from tecton.framework.configs import Secret
from tecton.framework.configs import convert_secret_to_sanitized_reference
from tecton_core import conf
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.repo_file_handler import construct_fco_source_info
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import fco_args__client_pb2 as fco_args_pb2
from tecton_proto.args import resource_provider__client_pb2 as resource_provider__args_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


RESOURCE_CONTEXT_PARAM_NAME = "context"


@attrs.define(eq=False)
class ResourceProvider(base_tecton_object.BaseTectonObject):
    """
    A `ResourceProvider` provides a stateful resource in Tecton, It is initialized in advance so it can be reused among certain computations such as materialization job.

    ```python
    from tecton import resource_provider, Secret

    @resource_provider(
        tags = {"environment":"staging"},
        owner = "tom@tecton.ai",
        secrets = {"api_key": Secret(scope="scope", key="api_key")}
    )
    def resource(context):
        return APIClient(api_key = context.secrets["api_key"])
    ```

    """

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and fetched
    # from the Tecton backend.
    _args: Optional[resource_provider__args_pb2.ResourceProviderArgs] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    _spec: Optional[specs.ResourceProviderSpec] = attrs.field(repr=False)

    def __init__(
        self,
        *,
        name: str,
        function: Callable,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        secrets: Optional[Dict[str, Union[Secret, str]]] = None,
    ):
        param_names = [param.name for param in inspect.signature(function).parameters.values()]
        if param_names and param_names != [RESOURCE_CONTEXT_PARAM_NAME]:
            raise errors.INVALID_INPUTS_RESOURCE_PROVIDER(name)

        serialized_function = None
        if function_serialization.should_serialize_function(function):
            serialized_function = function_serialization.to_proto(function)
        secret_references = {}
        if secrets:
            for secret_name, secret in secrets.items():
                secret_references[secret_name] = convert_secret_to_sanitized_reference(secret)

        args = resource_provider__args_pb2.ResourceProviderArgs(
            resource_provider_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            secrets=secret_references,
            function=serialized_function,
        )
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.resource_provider_id)
        source_info = construct_fco_source_info(args.resource_provider_id)
        self.__attrs_init__(
            info=info,
            args=args,
            source_info=source_info,
            spec=None,
        )
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._spec = specs.ResourceProviderSpec.from_args_proto(self._args, function)
        base_tecton_object._register_local_object(self)

    def _validate(self) -> None:
        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
        )

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.ResourceProviderSpec) -> "ResourceProvider":
        """Create an ResourceProvider directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)
        # Instantiate the object. Does not call init.
        obj = cls.__new__(cls)  # pylint: disable=no-value-for-parameter
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None)
        return obj

    @sdk_decorators.assert_local_object
    def _build_and_resolve_args(self, objects) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(resource_provider=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                resource_provider=validator_pb2.ResourceProviderArgs(
                    args=self._args,
                )
            )
        else:
            return self._spec.validation_args


def resource_provider(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    secrets: Optional[Dict[str, Union[Secret, str]]] = None,
):
    """
    Declare a ResourceProvider

    :param name: Unique name for resource provider, Defaults to function name.
    :param description: Description of Resource Provider
    :param owner: Owner of resource provider (typically email)
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param secrets: A dictionary of Secret references that will be resolved and provided to the resource provider at runtime of the Feature View that this resource is used in. During local development and testing, strings may be used instead Secret references.

    :return: An object of type `ResourceProvider`
    """

    def decorator(function):
        return ResourceProvider(
            name=name or function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            secrets=secrets,
            function=function,
        )

    return decorator
