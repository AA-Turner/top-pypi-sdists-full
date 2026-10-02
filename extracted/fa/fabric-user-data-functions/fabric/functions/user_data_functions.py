"""
This module defines the UserDataFunctions class, which is used to define User Data Functions in Fabric.
You can use this class by importing it from the fabric.functions module
(e.g. `from fabric.functions import UserDataFunctions`, or `import fabric.functions as fn` -> `fn.UserDataFunctions()`).
"""

# flake8: noqa: I005
import copy
import os
import sys
from typing import Any, Callable, Optional, Type
from azure.functions.decorators.http import HttpTrigger, HttpOutput, HttpMethod
from azure.functions.decorators.core import AuthLevel
from azure.functions import FunctionApp
import fabric.internal.decorators as fabric_decorators
from fabric.internal.decorators.constants import SpecConstants, BatchConstants
from typing_extensions import deprecated

from fabric.internal.item_binding import FabricItemInput

from fabric.internal.user_data_function_context_binding import (
    UserDataFunctionContextInput,
)
from fabric.internal.logging import UdfLogger
from fabric.internal.openapi_spec_generator import (
    FunctionMetadata,
    OpenAPISpecification,
    OpenAPISpecificationBuilder,
)

from fabric.internal.providers import ProviderMetadata, ProviderFactory

from typing import Callable, TypeVar
import importlib

T = TypeVar("T")

# This will prevent a user from writing a function with a 'context' parameter
CONTEXT_PARAMETER = "context"
UNUSED_FABRIC_CONTEXT_PARAMETER = "notusedfabriccontext"
REQ_PARAMETER = "req"


class UserDataFunctions(FunctionApp):
    """
    This class is necessary to define User Data Functions in Fabric. Please ensure an instantiation of this class exists in your code before any User Data Functions are defined.

    .. remarks::
        This class is used to define User Data Functions in Fabric. The class must be instantiated before any User Data Functions are defined. The instantiation of this class is required.

        .. code-block:: python
            import fabric.functions as fn

            udf = fn.UserDataFunctions() # This is the instantiation of the class that is required to define User Data Functions

            @udf.function()
            def my_function() -> None:
                pass
    """

    def __init__(self):
        """ """
        self.logger = UdfLogger(__name__)
        try:
            self.__version__ = importlib.metadata.version("fabric_user_data_functions")
        except Exception as e:
            self.__version__ = "(version not found)"
        
        is_hosted_environment = os.environ.get('PYTHON_ENABLE_WORKER_EXTENSIONS') is not None
        if is_hosted_environment:
            self.logger.error(f"Fabric Python Worker Version: {self.__version__}")
        
        self._initialize_spec_generation()
        self._function_args_metadata: ProviderMetadata = ProviderMetadata()
        self._provider_factory = ProviderFactory()

        super().__init__(AuthLevel.ANONYMOUS)

    def register_provider(self, type: Type, provider: Type):
        self._provider_factory.register_provider(type, provider)

    def _validate_max_batch_size(self, max_batch_size):
        """Validate and return the max batch size, applying defaults and constraints.
        
        :param max_batch_size: The max batch size to validate (None means not a batched function)
        :return: The validated max batch size, or None if not a batched function
        :raises ValueError: If max_batch_size is invalid
        """
        # If max_batch_size is None, this is not a batched function
        if max_batch_size is None:
            return None
        
        # Validate max_batch_size is an integer
        if not isinstance(max_batch_size, int):
            raise ValueError(f"max_batch_size must be an integer, got {type(max_batch_size).__name__}")
        
        # Validate max_batch_size is within allowed range
        if max_batch_size < BatchConstants.MIN_BATCH_SIZE or max_batch_size > BatchConstants.MAX_BATCH_SIZE:
            raise ValueError(f"max_batch_size must be between {BatchConstants.MIN_BATCH_SIZE} and {BatchConstants.MAX_BATCH_SIZE}, got {max_batch_size}")
        
        return max_batch_size

    def function(self, name=None, max_batch_size=None):
        """
        This decorator is used to define a User Data Function in Fabric. The function must be decorated with this decorator in order to be recognized as a User Data Function.

        :param name: The name of the function. This parameter is not used in the current version of Fabric.
        :type name: str
        :param max_batch_size: The maximum number of items that can be processed in a single batch execution. If not specified, the function will process single items (scalar mode). If specified, must be between 1-900.
        :type max_batch_size: int

        .. remarks::

            .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()

                @udf.function() # This is the decorator that is required to define a User Data Function
                def my_function() -> None:
                    pass
        """
        if not self._spec_function_created:
            self._create_spec_function()

        def wrap(fb, user_func):
            # Add HTTP Trigger
            fb.add_trigger(
                trigger=HttpTrigger(
                    name=REQ_PARAMETER,
                    methods=[HttpMethod.POST],
                    auth_level=AuthLevel.ANONYMOUS,
                )
            )
            fb.add_binding(binding=HttpOutput(name="$return"))
            # Force one of our bindings to ensure the Host Extension is loaded
            fb.add_binding(
                binding=UserDataFunctionContextInput(
                    name=UNUSED_FABRIC_CONTEXT_PARAMETER
                )
            )
            # self.log_openapi_spec()
            return fb
        
        validated_max_batch_size = self._validate_max_batch_size(max_batch_size)
        return fabric_decorators.configure_fabric_function_builder(self, wrap, self._functions_metadata, validated_max_batch_size)


    def streaming_function(self, name=None):
        """
        Define a **streaming** User Data Function whose HTTP response is flushed
        to the caller incrementally instead of being buffered into a single body.

        The decorated function must return a
        :class:`fabric.functions.StreamResponse` wrapping an iterator (sync or
        async) of ``bytes``/``str`` chunks. Each chunk is streamed to the client
        as it is produced — enabling true end-to-end HTTP streaming (e.g.
        relaying an Apache Arrow stream from Power BI ``executeDaxQueries``).

        :param name: Optional function/route name. Defaults to the function name.
        :type name: str

        .. important::
            Streaming uses the Azure Functions **HTTP streams** feature and
            requires the ``azurefunctions-extensions-http-fastapi`` package in
            your ``requirements.txt`` plus the app setting
            ``PYTHON_ENABLE_INIT_INDEXING=1``. When a streaming function is
            present the app runs in ASGI mode app-wide, so it cannot also host
            classic (buffered) ``@udf.function()`` functions in the same app.

        .. remarks::

            .. code-block:: python
                import fabric.functions as fn

                udf = fn.UserDataFunctions()

                @udf.streaming_function()
                def stream_numbers(count: int) -> fn.StreamResponse:
                    def gen():
                        for i in range(count):
                            yield f"chunk {i}\\n".encode()
                    return fn.StreamResponse(gen(), media_type="text/plain")
        """
        return fabric_decorators.configure_streaming_function_builder(self, name)


    def connection(self, 
                   alias:Optional[str] = None, 
                   argName: Optional[str] = None, 
                   **kwargs) -> Callable[..., Any]:
        """
        This decorator is used to tell a User Data Function that there is a connection to a data source. This decorator must be used in tandem with a parameter of type :class:`fabric.functions.FabricSqlConnection` or :class:`fabric.functions.FabricLakehouseClient` (see the example under `Remarks`).

        :param alias: The alias of the data connection that is being used.
        :type alias: str
        :param argName: The name of the parameter in the function signature. If not provided, the alias will be used.
        :type argName: str

        .. remarks::

            .. code-block:: python
                    import fabric.functions as fn

                    udf = fn.UserDataFunctions()

                    @udf.connection("<data connection alias>", "<argName>") # This is the decorator that is required to define a connection to a data source
                    @udf.function()
                    def my_function(<argName>: fn.FabricSqlConnection) -> None:
                        conn = <argName>.connect()
                        pass
        """
        
        # If no alias, try to see if there is a type to validate for generic connections
        if alias is None:
            audienceType = kwargs.get("audienceType")
            if audienceType is None:
                raise ValueError("Either alias or audienceType must be provided.")
            return self.generic_connection(argName, **kwargs)

        # If no argName provided, use the alias
        if argName is None:
            argName = alias

        return self.alias_connection(alias, argName, **kwargs)

    # The decorator that will be used to tell the function we want a fabric item
    def alias_connection(
        self, alias: str, argName: Optional[str] = None, **kwargs
    ) -> Callable[..., Any]:
        """
        This decorator is used to tell a User Data Function that there is a connection to a data source. This decorator must be used in tandem with a parameter of type :class:`fabric.functions.FabricSqlConnection` or :class:`fabric.functions.FabricLakehouseClient` (see the example under `Remarks`).

        :param alias: The alias of the data connection that is being used.
        :type alias: str
        :param argName: The name of the parameter in the function signature. If not provided, the alias will be used.
        :type argName: str

        .. remarks::

            .. code-block:: python
                    import fabric.functions as fn

                    udf = fn.UserDataFunctions()

                    @udf.connection("<data connection alias>", "<argName>") # This is the decorator that is required to define a connection to a data source
                    @udf.function()
                    def my_function(<argName>: fn.FabricSqlConnection) -> None:
                        conn = <argName>.connect()
                        pass
        """

        @self._configure_function_builder
        def wrap(fb):
            binding_name = argName if argName is not None else alias
            
            # Store kwargs in ProviderMetadata for provider to retrieve later
            if kwargs:
                self._function_args_metadata.add_kwargs(
                    funcName=fb._function.get_function_name(),
                    argName=binding_name,
                    **kwargs
                )

            fb.add_binding(
                binding=FabricItemInput(
                    name=binding_name,
                    alias=alias,
                    **kwargs,
                )
            )
            return fb

        return wrap

    # The decorator that will be used to tell the function we want a fabric item
    def generic_connection(
        self, argName: str, **kwargs
    ) -> Callable[..., Any]:
        """
        This decorator is used to tell a User Data Function that there is a connection to a data source. This decorator must be used in tandem with a parameter of type :class:`fabric.functions.FabricSqlConnection` or :class:`fabric.functions.FabricLakehouseClient` (see the example under `Remarks`).

        :param audienceType: The audience type of the data connection that is being used.
        :type audienceType: str
        :param argName: The name of the parameter in the function signature. If not provided, the audience type will be used.
        :type argName: str

        .. remarks::

            .. code-block:: python
                    import fabric.functions as fn

                    udf = fn.UserDataFunctions()

                    @udf.connection("<data connection audienceType>", "<argName>") # This is the decorator that is required to define a connection to a data source
                    @udf.function()
                    def my_function(<argName>: fn.FabricItem) -> None:
                        
                        pass
        """

        audienceType = kwargs.pop("audienceType", None)

        # Register DI types and optional libraries
        self.register_needed_modules(audienceType)

        @self._configure_function_builder
        def wrap(fb):

            # register custom kwargs for each new argument
            self._function_args_metadata.add_kwargs(
                funcName=fb._function.get_function_name(),
                argName=argName,
                **kwargs
            )

            fb.add_binding(
                binding=FabricItemInput(
                    name=argName,
                    audienceType=audienceType,
                    **kwargs,
                )
            )
            return fb

        return wrap

    def register_needed_modules(self, audienceType: str):
        """ Register needed modules for the specified audience type.

        If the audience type is 'CosmosDB', the CosmosDB module will be imported.
        If the audience type is 'KeyVault', the KeyVault module will be imported.

        More will be added as needed.
        """

        if audienceType == 'CosmosDB':
            mod = sys.modules.get('fabric.functions.cosmos')
            if mod is None:
                mod = importlib.import_module('fabric.functions.cosmos')

            if not getattr(mod, "_fabric_cosmos_initialized", False):
                mod.use_cosmosdb(self)
                setattr(mod, "_fabric_cosmos_initialized", True)

        if audienceType == 'KeyVault':
            mod = sys.modules.get('fabric.functions.keyvault')
            if mod is None:
                mod = importlib.import_module('fabric.functions.keyvault')

            if not getattr(mod, "_fabric_keyvault_initialized", False):
                mod.use_keyvault(self)
                setattr(mod, "_fabric_keyvault_initialized", True)

    def context(self, argName, **kwargs) -> Callable[..., Any]:
        """
        This decorator is used to tell a User Data Function that there is a :class:`fabric.functions.UserDataFunctionContext` parameter.
        This decorator must be used in tandem with a parameter of type :class:`fabric.functions.UserDataFunctionContext`.

        :param argName: The name of the parameter in the function signature.
        :type argName: str

        .. remarks::

            .. code-block:: python
                    import fabric.functions as fn

                    udf = fn.UserDataFunctions()

                    @udf.context("<argName>") # This is the decorator that is required
                    @udf.function()
                    def my_function(<argName>: fn.UserDataFunctionContext) -> None:
                        pass
        """

        @self._configure_function_builder
        def wrap(fb):
            fb.add_binding(binding=UserDataFunctionContextInput(name=argName, **kwargs))
            return fb

        return wrap

    @deprecated(
        "This function is deprecated. Please use 'connection' instead. Note the alias parameter in 'connection' is now the first parameter."
    )
    def fabric_item_input(self, argName, alias: str, **kwargs) -> Callable[..., Any]:
        """
        This decorator is deprecated. Please use :meth:`connection` instead. Note the alias parameter in :meth:`connection` is now the first parameter.
        """
        return self.connection(alias=alias, argName=argName, **kwargs)

    @deprecated("This function is deprecated. Please use 'context' instead.")
    def user_data_function_context_input(self, argName, **kwargs) -> Callable[..., Any]:
        """
        This decorator is deprecated. Please use :meth:`context` instead.
        """
        return self.context(argName, **kwargs)
    
    def _create_spec_function(self):
        """
        This creates a function that is used to define the OpenAPI Specification for the User Data Functions.
        """
        self._spec_function_created = True
        @self.function()
        def get_udf_oai_spec_json(publicUrl: str, privateFunctions: list, specFormat: str = "yaml") -> str:
            """
            This function is used to generate the OpenAPI Specification for the User Data Functions in JSON format.

            :param publicUrl: The public URL of the User Data Functions.
            :type publicUrl: str
            :param privateFunctions: A list of private functions that should not be included in the OpenAPI Specification.
            :type privateFunctions: list
            :param specFormat: The format of the OpenAPI Specification. Defaults to 'yaml'.
            :type specFormat: str

            :return: The OpenAPI Specification for the User Data Functions in JSON format.
            :rtype: str
            """
            return self.get_udf_oai_spec(publicUrl, privateFunctions, specFormat)
        
        @self.function()
        def get_udf_oai_spec_yaml(publicUrl: str, privateFunctions: list, specFormat: str = "yaml") -> str:
            """
            This function is used to generate the OpenAPI Specification for the User Data Functions in YAML format.

            :param publicUrl: The public URL of the User Data Functions.
            :type publicUrl: str
            :param privateFunctions: A list of private functions that should not be included in the OpenAPI Specification.
            :type privateFunctions: list
            :param specFormat: The format of the OpenAPI Specification. Defaults to 'yaml'.
            :type specFormat: str

            :return: The OpenAPI Specification for the User Data Functions in YAML format.
            :rtype: str
            """
            return self.get_udf_oai_spec(publicUrl, privateFunctions, specFormat)

    def get_udf_oai_spec(self, publicUrl: str, privateFunctions: list, specFormat: str = "yaml") -> str:
        # Validation
        if specFormat not in ["json", "yaml"]:
            raise ValueError(
                f"Invalid specFormat: {specFormat}. Must be 'json' or 'yaml'."
            )
        
        if not publicUrl:
            publicUrl = SpecConstants.LOCAL_HOST_URL

        openapi_spec = OpenAPISpecification()
        _openapi_spec_builder = OpenAPISpecificationBuilder(openapi_spec)
        _openapi_spec_builder.with_openapi("3.0.0").with_info(
            title="Fabric User Data Functions",
            version="0.1.0",
            description="This is the OpenAPI Specification for Fabric User Data Functions.",
        ).add_security_scheme(
            name="bearerAuth",
            definition={
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        ).add_security_requirement(
            {"bearerAuth": []}
        ).build()
        
        
        _functions_metadata_copy = copy.deepcopy(self._functions_metadata)
        
        # Remove private functions from the OpenAPI Spec
        for function in privateFunctions:
            self.logger.error(f"Probing function: {function}")
            for function_metadata in _functions_metadata_copy:
                self.logger.error(f"Function Metadata: {function_metadata.function_name}")
                if function_metadata.function_name == function:
                    self.logger.error(f"Removing function: {function}")
                    _functions_metadata_copy.remove(function_metadata)
        
        for function_metadata in _functions_metadata_copy:
            # For every key in the function_metadata path, add openapi spec path
            for key, value in function_metadata.paths.items():
                _openapi_spec_builder.add_path(key, value)
            for key, value in function_metadata.components.items():
                _openapi_spec_builder.add_schema_from_model(key, value)
    
        _openapi_spec_builder.add_server(publicUrl, SpecConstants.PUBLIC_URL_DESC).build()
        self.logger.error(f"OpenAPI Spec: {openapi_spec.serialize(specFormat)}")
        return openapi_spec.serialize(specFormat)
    
    def _initialize_spec_generation(self):
        self._spec_function_created = False
        self._functions_metadata: list[FunctionMetadata] = []
        
