import base64
import dataclasses
import enum
import io
import os
import typing
import warnings

import httpx
from typing import cast, List, Tuple, Union, Optional
from typing_extensions import TypeVar, ParamSpec
from langserve import RemoteRunnable

from . import core
from .base_client import BaseAthena, AsyncBaseAthena
from .environment import AthenaEnvironment
from .tools.client import AsyncToolsClient, ToolsClient
from .query.client import AsyncQueryClient, QueryClient
from .types.data_frame_request_out import DataFrameRequestOut
from .types.save_asset_request_out import SaveAssetRequestOut

if typing.TYPE_CHECKING:
    import pandas as pd


P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")


def _inherit_signature_and_doc(
    f: typing.Callable[P, T], replace_in_doc: typing.Dict[str, str]
) -> typing.Callable[..., typing.Callable[P, U]]:
    def decorator(decorated):
        for old, new in replace_in_doc.items():
            assert old in f.__doc__
            decorated.__doc__ = f.__doc__.replace(old, new)
        return decorated

    return decorator


class SpecialEnvironments(enum.Enum):
    AUTODETECT_ENVIRONMENT = "AUTO"


@dataclasses.dataclass
class AthenaAsset:
    asset_id: str
    data: bytes
    media_type: str

    def _repr_mimebundle_(self, include=None, exclude=None):
        if self.media_type == "application/sql":
            # it is safe to import IPython in `_repr_mimebundle_`
            # as this is only intended to be invoked by IPython.
            from IPython import display  # type: ignore[import]

            code = display.Code(
                data=self.data.decode(),
                language="sql",
            )
            return {"text/html": code._repr_html_()}
        return {self.media_type: self.data}


class WrappedToolsClient(ToolsClient):

    def get_file(self, asset_id: str) -> io.BytesIO:
        """
        Parameters
        ----------
        asset_id : str

        Returns
        -------
        io.BytesIO

        Examples
        --------
        import polars as pl
        from athena.client import Athena

        client = Athena(api_key="YOUR_API_KEY")
        file_io = client.tools.get_file(asset_id="asset_id")
        pl.read_csv(file_io)
        """
        file_bytes = b"".join(self.raw_data(asset_id=asset_id))
        bytes_io = io.BytesIO(file_bytes)
        return bytes_io

    @_inherit_signature_and_doc(
        ToolsClient.data_frame, {"DataFrameRequestOut": "pd.DataFrame"}
    )
    def data_frame(self, *, asset_id: str, **kwargs) -> "pd.DataFrame":
        _check_pandas_installed()
        model = super().data_frame(asset_id=asset_id, **kwargs)
        return _read_json_frame(model)

    def read_data_frame(self, asset_id: str, *args, **kwargs) -> "pd.DataFrame":
        """
        Parameters
        ----------
        asset_id : str

        **kwargs : dict
          keyword arguments passed to pandas `read_csv` or `read_excel` function,
          depending on the file type of the document identified by `asset_id`.

        Returns
        -------
        pd.DataFrame

        Examples
        --------
        from athena.client import Athena

        client = Athena(api_key="YOUR_API_KEY")
        client.tools.read_data_frame(asset_id="asset_id")
        """
        _check_pandas_installed()
        file_bytes, media_type = self._get_file_and_media_type(asset_id=asset_id)
        return _to_pandas_df(file_bytes, *args, media_type=media_type, **kwargs)

    def save_asset(  # type: ignore[override]
        self,
        asset_object: Union["pd.DataFrame", "pd.Series", core.File],
        *,
        parent_folder_id: Union[str, None] = None,
        name: Union[str, None] = None,
        **kwargs,
    ) -> SaveAssetRequestOut:
        """
        Parameters
        ----------
        asset_object : pd.DataFrame | pd.Series | matplotlib.figure.Figure | core.File
            A pandas data frame, series, matplotlib figure, or core.File

        parent_folder_id : typing.Optional[str]
            Identifier of the folder into which the asset should be saved

        name : typing.Optional[str]
            The name for the asset

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        **kwargs : passed down to conversion methods

        Returns
        -------
        SaveAssetRequestOut
            Successful Response

        Examples
        --------
        from athena.client import Athena

        client = Athena(api_key="YOUR_API_KEY")
        client.tools.save_asset(df)
        """
        asset_object = _convert_asset_object(
            asset_object=asset_object, name=name, **kwargs
        )
        return super().save_asset(file=asset_object, parent_folder_id=parent_folder_id)

    def _get_file_and_media_type(self, asset_id: str) -> Tuple[io.BytesIO, str]:
        """
        Gets the file togehter with media type returned by server
        """
        # while we wait for https://github.com/fern-api/fern/issues/4316
        result = self.with_raw_response._client_wrapper.httpx_client.request(
            "api/v0/tools/file/raw-data", method="GET", params={"asset_id": asset_id}
        )
        if result.status_code != 200:
            # let fern handle errors codes
            self.raw_data(asset_id=asset_id)
            raise Exception(
                f"Could not get assset - unhandled error code: {result.status_code}"
            )

        file_bytes = io.BytesIO(result.read())

        media_type = result.headers.get("content-type", "").split(";")[0]

        if media_type == "":
            # fallback to `libmagic` inference
            media_type = _infer_media_type(bytes_io=file_bytes)

        return file_bytes, media_type

    def get_asset(self, asset_id: str) -> Union["pd.DataFrame", AthenaAsset]:
        """
        Parameters
        ----------
        asset_id : str

        Returns
        -------
        pd.DataFrame or AthenaAsset

        Examples
        --------
        from athena.client import Athena

        client = Athena(api_key="YOUR_API_KEY")
        client.tools.get_asset(asset_id="asset_id")
        """
        file_bytes, media_type = self._get_file_and_media_type(asset_id=asset_id)

        media_type_aliases = {"image/jpg": "image/jpeg"}
        media_type = media_type_aliases.get(media_type, media_type)

        supported_media_types = {
            "application/json",
            "application/pdf",
            "image/jpeg",
            "image/gif",
            "image/png",
            "image/svg+xml",
            "image/webp",
            "text/html",
            "text/latex",
            "text/markdown",
            "text/plain",
            "application/sql",
        }

        if media_type in supported_media_types:
            data = file_bytes.read()
            return AthenaAsset(
                asset_id=asset_id,
                data=data,
                media_type=media_type,
            )

        if media_type in _pandas_media_types:
            return _to_pandas_df(file_bytes, media_type=media_type)

        raise NotImplementedError("Assets of `{media_type}` type are not yet supported")


class WrappedQueryClient(QueryClient):

    @_inherit_signature_and_doc(
        QueryClient.execute, {"DataFrameRequestOut": "pd.DataFrame"}
    )
    def execute(
        self, *, sql_command: str, database_asset_ids: Union[str, List[str]], **kwargs
    ) -> "pd.DataFrame":
        _check_pandas_installed()
        model = super().execute(
            sql_command=sql_command, database_asset_ids=database_asset_ids, **kwargs
        )
        return _read_json_frame(model)

    @_inherit_signature_and_doc(
        QueryClient.execute_snippet, {"DataFrameRequestOut": "pd.DataFrame"}
    )
    def execute_snippet(self, *, snippet_asset_id: str, **kwargs) -> "pd.DataFrame":
        _check_pandas_installed()
        model = super().execute_snippet(snippet_asset_id=snippet_asset_id, **kwargs)
        return _read_json_frame(model)


def _add_docs_for_async_variant(obj):
    def decorator(decorated):
        doc = obj.__doc__
        name = obj.__name__
        decorated.__doc__ = doc.replace(
            "client = Athena", "client = AsyncAthena"
        ).replace(f"client.tools.{name}", f"await client.tools.{name}")
        return decorated

    return decorator


class WrappedAsyncToolsClient(AsyncToolsClient):

    @_add_docs_for_async_variant(WrappedToolsClient.get_file)
    async def get_file(self, asset_id: str) -> io.BytesIO:
        file_bytes = b"".join([gen async for gen in self.raw_data(asset_id=asset_id)])
        bytes_io = io.BytesIO(file_bytes)
        return bytes_io

    @_inherit_signature_and_doc(
        AsyncToolsClient.data_frame, {"DataFrameRequestOut": "pd.DataFrame"}
    )
    async def data_frame(self, *, asset_id: str, **kwargs) -> "pd.DataFrame":
        _check_pandas_installed()
        model = await super().data_frame(asset_id=asset_id, **kwargs)
        return _read_json_frame(model)

    @_add_docs_for_async_variant(WrappedToolsClient.read_data_frame)
    async def read_data_frame(self, asset_id: str, *args, **kwargs) -> "pd.DataFrame":
        _check_pandas_installed()
        file_bytes = await self.get_file(asset_id)
        return _to_pandas_df(file_bytes, *args, **kwargs)

    @_add_docs_for_async_variant(WrappedToolsClient.save_asset)
    async def save_asset(
        self,
        asset_object: Union["pd.DataFrame", "pd.Series", core.File],
        *,
        parent_folder_id: Union[str, None] = None,
        name: Union[str, None] = None,
        **kwargs,
    ) -> SaveAssetRequestOut:
        asset_object = _convert_asset_object(
            asset_object=asset_object, name=name, **kwargs
        )
        return await super().save_asset(
            file=asset_object, parent_folder_id=parent_folder_id
        )


class WrappedAsyncQueryClient(AsyncQueryClient):

    @_inherit_signature_and_doc(
        AsyncQueryClient.execute, {"DataFrameRequestOut": "pd.DataFrame"}
    )
    async def execute(
        self, *, sql_command: str, database_asset_ids: Union[str, List[str]], **kwargs
    ) -> "pd.DataFrame":
        _check_pandas_installed()
        model = await super().execute(
            sql_command=sql_command, database_asset_ids=database_asset_ids, **kwargs
        )
        return _read_json_frame(model)

    @_inherit_signature_and_doc(
        AsyncQueryClient.execute_snippet, {"DataFrameRequestOut": "pd.DataFrame"}
    )
    async def execute_snippet(
        self, *, snippet_asset_id: str, **kwargs
    ) -> "pd.DataFrame":
        _check_pandas_installed()
        model = await super().execute_snippet(
            snippet_asset_id=snippet_asset_id, **kwargs
        )
        return _read_json_frame(model)


class AthenaModel(RemoteRunnable):
    """Use Athena's models directly with a Langchain-compatible client.

    The Langchain Runnable interface is supported:
    - `invoke`: Invoke the model with a string or a Langchain message.
    - `batch`: Batch invoke the model on multiple inputs.
    - `astream_events`: Streaming for real-time applications.

    See Langchain documentation for more details.

    Examples
    --------
    from src.athena.client import Athena
    import asyncio
    from langchain_core.messages import HumanMessage

    client = Athena()
    llm = client.llm

    # sync invoke -- use strings or langchain messages
    result = llm.invoke("Hello")
    print(result.content)

    result = llm.invoke("Hello")
    print(result.content)

    # choose the model explicitly
    claude = llm.with_config(configurable={"model": "claude_3_7_sonnet"})
    print(claude.invoke("Who are you?").content)

    # batch (for multiple parallel requests)
    results = llm.batch(["Hello", "World"] * 5)
    print([r.content for r in results])

    # handle stream events
    async def stream_response():
        separator = "---------------------------------------"
        print(separator)
        print("Starting stream")
        print(separator)
        async for event in llm.astream_events("Hello.  Please respond in 5 sentences."):
            data = event["data"]
            if "chunk" in data:
                print(data["chunk"].content)
            elif "output" in data:
                print(separator)
                print("Final response")
                print(separator)
                print(data["output"].content)
            else:
                print("(other event) ", event.keys())


    asyncio.run(stream_response())
    from athena.client import Athena
    client = Athena()
    llm = client.llm

    # sync invoke -- use strings or langchain messages
    result = llm.invoke("Hello")
    print(result.content)

    # batch
    results = llm.batch(["Hello", "World"])
    print(r.content for r in results)
    """

    def __init__(self, base_url: str, api_key: str, timeout: Optional[float] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        super().__init__(
            base_url + "/api/v0/agents/general",
            headers={"X-API-KEY": api_key},
            timeout=timeout,
        )


class Athena(BaseAthena):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : AthenaEnvironment
        The environment to use for requests from the client.

        Defaults to `AthenaEnvironment.PRODUCTION` when outside of athena notebook environment.

    api_key: typing.Optional[str].  The API key. Required when used outside of the athena notebook environment.
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from athena.client import Athena

    client = Athena(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: Union[AthenaEnvironment, SpecialEnvironments] = SpecialEnvironments.AUTODETECT_ENVIRONMENT,  # type: ignore[arg-type]
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        if api_key is None:
            try:
                api_key = os.environ["ATHENA_API_KEY"]
            except KeyError:
                raise TypeError(
                    "Athena() missing 1 required keyword-only argument: 'api_key'"
                    " (ATHENA_API_KEY environment variable not found)"
                )
        if environment == SpecialEnvironments.AUTODETECT_ENVIRONMENT:
            current_url = os.environ.get("ATHENA_API_URL", "https://api.athenaintel.com")

            class _CurrentEnv(enum.Enum):
                CURRENT = current_url

            environment = cast(AthenaEnvironment, _CurrentEnv.CURRENT)
        super().__init__(
            base_url=base_url,
            environment=environment,  # type: ignore[arg-type]
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client,
        )
        self._tools: typing.Optional[WrappedToolsClient] = None
        self.llm = AthenaModel(
            base_url=base_url or environment.value, api_key=api_key, timeout=timeout
        )

    @property
    def tools(self) -> WrappedToolsClient:
        if self._tools is None:
            self._tools = WrappedToolsClient(client_wrapper=self._client_wrapper)
        return self._tools


class AsyncAthena(AsyncBaseAthena):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.


    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : AthenaEnvironment
        The environment to use for requests from the client.

        Defaults to `AthenaEnvironment.PRODUCTION` when outside of athena notebook environment.

    api_key: typing.Optional[str].  The API key. Required when used outside of the athena notebook environment.
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from athena.client import AsyncAthena

    client = AsyncAthena(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: Union[AthenaEnvironment, SpecialEnvironments] = SpecialEnvironments.AUTODETECT_ENVIRONMENT,  # type: ignore[arg-type]
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        if api_key is None:
            try:
                api_key = os.environ["ATHENA_API_KEY"]
            except KeyError:
                raise TypeError(
                    "AsyncAthena() missing 1 required keyword-only argument: 'api_key'"
                    " (ATHENA_API_KEY environment variable not found)"
                )
        if environment == SpecialEnvironments.AUTODETECT_ENVIRONMENT:
            current_url = os.environ.get("ATHENA_API_URL", "https://api.athenaintel.com")

            class _CurrentEnv(enum.Enum):
                CURRENT = current_url

            environment = cast(AthenaEnvironment, _CurrentEnv.CURRENT)
        self._tools: typing.Optional[WrappedAsyncToolsClient] = None
        super().__init__(
            base_url=base_url,
            environment=environment,  # type: ignore[arg-type]
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client,
        )

    @property
    def tools(self) -> WrappedAsyncToolsClient:
        if self._tools is None:
            self._tools = WrappedAsyncToolsClient(client_wrapper=self._client_wrapper)
        return self._tools


def _read_json_frame(model: DataFrameRequestOut) -> "pd.DataFrame":
    import pandas as pd

    string_io = io.StringIO(model.json())

    with warnings.catch_warnings():
        # Filter warnings due to https://github.com/pandas-dev/pandas/issues/59511
        warnings.simplefilter(action="ignore", category=FutureWarning)
        return pd.read_json(string_io, orient="split")


def _check_pandas_installed():
    import pandas

    assert pandas


def _infer_media_type(bytes_io: io.BytesIO) -> str:
    import magic

    # ideally this would be read from response header, but fern SDK for Python hides this info from us
    media_type = magic.from_buffer(bytes_io.read(2048), mime=True)
    bytes_io.seek(0)
    return media_type


_pandas_media_types = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.apache.parquet",
    "application/octet-stream",
    "application/vnd.ms-excel",
    "text/csv",
    "application/csv",
}


def _to_pandas_df(
    bytes_io: io.BytesIO, *args, media_type: Union[str, None] = None, **kwargs
):
    import pandas as pd

    if media_type is None:
        media_type = _infer_media_type(bytes_io)

    if (
        media_type
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        return pd.read_excel(bytes_io, *args, engine="openpyxl", **kwargs)
    elif media_type in {"application/vnd.apache.parquet", "application/octet-stream"}:
        return pd.read_parquet(bytes_io, *args, **kwargs)
    elif media_type == "application/vnd.ms-excel":
        return pd.read_excel(bytes_io, *args, **kwargs)
    elif media_type in {"text/csv", "text/plain", "application/csv"}:
        return pd.read_csv(bytes_io, *args, **kwargs)
    else:
        raise Exception(f"Unknown media type: {media_type}")


def _convert_asset_object(
    asset_object: Union["pd.DataFrame", "pd.Series", core.File],
    name: Union[str, None] = None,
    **kwargs,
) -> core.File:
    import pandas as pd

    try:
        from IPython.core.formatters import format_display_data  # type: ignore[import]
    except ImportError:
        format_display_data = None

    if isinstance(asset_object, pd.Series):
        asset_object = asset_object.to_frame()
    if isinstance(asset_object, pd.DataFrame):
        return (
            name or "Uploaded data frame",
            asset_object.to_parquet(path=None, **kwargs),
            "application/vnd.apache.parquet",
        )
    if format_display_data:
        data, _metadata = format_display_data(asset_object)
        image_types = {
            "image/png": "Plot",
            "image/jpeg": "Image",
            "image/gif": "Gif",
        }
        for media_type, label in image_types.items():
            if media_type in data:
                extension = media_type.split("/")[-1]
                image_bytes = base64.b64decode(data[media_type])
                name = name or f"Untitled {label}"
                if not name.endswith(f".{extension}"):
                    name = f"{name}.{extension}"
                return (
                    name,
                    image_bytes,
                    media_type,
                )
    return asset_object  # type: ignore[return-value]
