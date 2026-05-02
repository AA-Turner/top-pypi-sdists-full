import asyncio
import gc
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any
from tqdm import tqdm
from PIL import Image, UnidentifiedImageError
import pyheif
from pillow_heif import register_heif_opener
from io import BytesIO
import filetype
from ..flow import FlowComponent
from ...exceptions import (
    ConfigError,
    ComponentError,
    FileError
)
# Parrot Image Processing plug-ins
from parrot.interfaces.images.plugins import PLUGINS, ImagePlugin

register_heif_opener()  # HEIF support

class ImageFeatures(FlowComponent):
    """
    ImageFeatures is a component for extracting image features.
    It extends the FlowComponent class and implements a Plugin system for various image processing tasks.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        _model_name (str): The name of the model used for feature extraction.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ImageFeatures:
          # attributes here
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._plugins_list: list = kwargs.get("plugins")
        self._plugins: list = []
        self._semaphore = asyncio.Semaphore(8)   # limit GPU tasks
        self.chunk_size: int = kwargs.get("chunk_size", 200)
        if not self._plugins_list:
            raise ConfigError("Plugins list is required.")
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')

    async def start(self, **kwargs):
        """
        start.

            Initialize Task.
        """
        if self.previous:
            self.data = self.input
        if self.data_column not in self.data.columns:
            raise ValueError(
                f'Data column {self.data_column} not found in data.'
            )
        # Check plugin Names:
        plugins = []
        for n in self._plugins_list:
            # n is a dictionary with the plugin name and args
            if isinstance(n, dict):
                name = list(n.keys())[0].lower()
                args = n[name]
            plugin = PLUGINS.get(name)
            if not plugin:
                raise ConfigError(
                    f'Plugin {n} not found in available plugins.'
                )
            if not issubclass(plugin, ImagePlugin):
                raise ConfigError(
                    f'Plugin {n} is not a subclass of ImagePlugin.'
                )
            if not args:
                args = {}
            if not isinstance(args, dict):
                raise ConfigError(
                    f'Plugin {n} args must be a dictionary.'
                )
            args['prompt_path'] = self.prompt_path
            plugins.append(
                {
                    "plugin": plugin,
                    "args": args
                }
            )
        self._plugins = plugins

    async def close(self):
        pass

    def get_bio(self, bio: Any) -> BytesIO:
        """Return a BytesIO object for a payload."""
        if isinstance(bio, Image.Image):
            return bio
        if isinstance(bio, bytes):
            bio = BytesIO(bio)
        if isinstance(bio, str):
            bio = BytesIO(bio.encode('utf-8'))
        if isinstance(bio, BytesIO):
            return bio
        if hasattr(bio, "read"):
            bio = BytesIO(bio.read())
        if hasattr(bio, "getvalue"):
            bio = BytesIO(bio.getvalue())
        else:
            raise TypeError(
                f"Expected bytes, str, or BytesIO, got {type(bio)}"
            )
        if not bio.readable():
            raise TypeError("BytesIO is not readable.")
        bio.seek(0)
        return bio

    async def _run_plugin(self, plugin, img: Image.Image, heif: Any = None, **kwargs):
        """
        Call plugin.analyze(); transparently await if it's an async def.
        """
        if asyncio.iscoroutinefunction(plugin.analyze):
            return await plugin.analyze(img, heif=heif, **kwargs)
        return plugin.analyze(img, heif)

    async def run(self):
        """
        run.

            Execute the plugin List to extract image features.
        """
        # Iterate over all plugins (create one single instance of each plugin):
        _plugins = []
        async with AsyncExitStack() as stack:
            for spec in self._plugins:
                cls, args = spec["plugin"], spec["args"]
                if cls.column_name not in self.data.columns:
                    # Create a new column in the DataFrame for the plugin's results
                    self.data[cls.column_name] = None
                plugin = cls(**args)
                try:
                    await plugin.start()
                except Exception as e:
                    raise ComponentError(
                        f"Error starting plugin {plugin}: {str(e)}"
                    ) from e
                # If the plugin implements .open() returning an async‑context
                if hasattr(plugin, "open"):
                    plugin = await stack.enter_async_context(plugin)  # ⇦ one‑time open
                _plugins.append(plugin)

        # Iterate over all rows in the DataFrame:
        # - Convert the image to a PIL Image
        # - Call the plugin's analyze method
        # - Store the result in the DataFrame
        # - Use a semaphore to limit concurrent tasks
        # - Use asyncio.gather to run the tasks concurrently
        # - Use a memoryview to avoid copying the image data
        # Convert BytesIO → bytes/PIL *one* time per row.
        async def process_row(idx, row):
            bio = row[self.data_column]
            if not bio:
                return
            async with self._semaphore:
                try:
                    try:
                        bio = self.get_bio(bio)
                    except Exception as e:
                        self._logger.error(
                            f"Error getting BytesIO from {bio}: {e}"
                        )
                        return
                    kind = filetype.guess(bio)
                    heic = None
                    if kind == 'image/heic':
                        try:
                            heic = pyheif.read_heif(bio)
                        except Exception as e:
                            self._logger.error(
                                "Unable to parse Apple Heic Photo"
                            )
                            return
                    if isinstance(bio, Image.Image):
                        image = bio
                    elif kind == 'image/heic':
                        image = Image.frombytes(
                            mode=heic.mode,
                            size=heic.size,
                            data=heic.data
                        )
                    else:
                        # Decode the image once
                        try:
                            image = Image.open(bio)
                        except UnidentifiedImageError:
                            raise FileError(
                                f"PIL cannot identify image file. MIME: {kind.mime}"
                            )
                    # Results from all plugins for this row
                    current_row_data = {}  # Track updates for shared columns
                    for plugin in _plugins:
                        plugin_kwargs = {
                            "row": row,
                            "idx": idx
                        }
                        if hasattr(plugin, 'column_name'):
                            column_name = plugin.column_name
                            # Check if we've already updated this column in this row
                            if column_name in current_row_data:
                                plugin_kwargs[column_name] = current_row_data[column_name]
                            elif column_name in row and row[column_name] is not None:
                                plugin_kwargs[column_name] = row[column_name]
                        result = await self._run_plugin(
                            plugin,
                            image,
                            heic,
                            **plugin_kwargs
                        )
                        # Update both tracking and DataFrame
                        current_row_data[plugin.column_name] = result
                        self.data.at[idx, plugin.column_name] = result
                except FileError as e:
                    self._logger.error(
                        f"Image Error on {row}: {e}"
                    )
                    return
                except Exception as e:
                    self._logger.error(
                        f'Error processing image at index {idx}: {e}'
                    )
                    return
        # Process in chunks to avoid loading all images into memory at once.
        # After each chunk, raw image bytes are cleared from the DataFrame and
        # gc.collect() is called to free RAM before loading the next batch.
        indices = list(self.data.index)
        total = len(indices)
        try:
            for chunk_start in range(0, total, self.chunk_size):
                chunk_indices = indices[chunk_start:chunk_start + self.chunk_size]
                chunk_end = min(chunk_start + self.chunk_size, total)
                self._logger.info(
                    f"ImageFeatures: processing rows {chunk_start + 1}-{chunk_end} / {total}"
                )
                tasks = []
                for idx in chunk_indices:
                    row = self.data.loc[idx]
                    tasks.append(process_row(idx, row))
                try:
                    await self._processing_tasks(
                        tasks, ': ImageFeatures :', show_progress=True
                    )
                except Exception as e:
                    raise ComponentError(
                        f"Error in ImageFeatures chunk {chunk_start}-{chunk_end}: {str(e)}"
                    ) from e
                finally:
                    # Free raw image bytes for processed rows — features are already
                    # stored in their plugin columns, bytes are no longer needed.
                    self.data.loc[chunk_indices, self.data_column] = None
                    gc.collect()

            self._print_data_(self.data, ':: Image Features ::')
            self._result = self.data
            return self._result
        finally:
            # Dispose of all plugins
            for plugin in _plugins:
                if hasattr(plugin, "dispose"):
                    try:
                        await plugin.dispose()
                    except Exception as e:
                        self._logger.error(
                            f"Error disposing plugin {plugin}: {str(e)}"
                        )
