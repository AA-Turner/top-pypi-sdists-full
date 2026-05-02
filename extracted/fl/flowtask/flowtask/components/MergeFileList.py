import os
import asyncio
import logging
from collections.abc import Callable
from pathlib import Path
from tqdm import tqdm
from threading import Semaphore
from asyncdb.exceptions import ProviderError
from ..exceptions import ComponentError, NotSupported, FileNotFound
from ..utils import check_empty
from .IteratorBase import IteratorBase, ThreadJob


class MergeFileList(IteratorBase):
    """
    MergeFileList with optional Parallelization Support.

    Overview

    This component extracts and merges lists of files from multiple upstream components.
    It consolidates the locations into a flat list, removes duplicates, and
    if `iterate: true` is passed, iterates each element spawning the next component sequentially
    (similar to FileList).

    :widths: auto

    | iterate (bool)      |    No    | Flag indicating whether to iterate through the files and process them sequentially (defaults to True).|
    | generator (bool)    |    No    | Flag controlling the output format: `True` returns a generator, `False` (default) returns a list.     |
    | parallelize         |    No    | If True, the iterator will process rows in parallel. Default is False.                                |
    | num_threads         |    No    | Number of threads to use if parallelize is True. Default is 10.                                       |


        Example:

        ```yaml
          MergeFileList:
            depends:
              - DownloadFromSharepoint_1
              - DownloadFromSharepoint_2
            iterate: true
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
        """Init Method."""
        self.generator: bool = False
        self.data = None
        self._files = []
        self._num_threads: int = kwargs.pop("num_threads", 10)
        self._parallelize: bool = kwargs.pop("parallelize", False)
        super(MergeFileList, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Extract files from upstream dependencies."""
        await super(MergeFileList, self).start()

        # In Flowtask, previous output is found in self.input
        if getattr(self, "previous", None):
            self._files = self._extract_list(self.input)

        return True

    def _extract_list(self, element) -> list:
        """Recursively extract files resolving dicts, paths and lists to a flat list of Path."""
        result = []
        if not element:
            return result

        if isinstance(element, list):
            for item in element:
                result.extend(self._extract_list(item))
        elif isinstance(element, dict):
            # If the dict resembles a File structure (common from DownloadFromSharepoint)
            if "filename" in element and "directory" in element:
                path = os.path.join(element["directory"], element["filename"])
                result.append(Path(path))
            # Or if it simply contains a 'files' key
            elif "files" in element and isinstance(element["files"], list):
                result.extend(self._extract_list(element["files"]))
            else:
                # If we received multiple dependencies it's usually { component_name: result... }
                for k, v in element.items():
                    result.extend(self._extract_list(v))
        elif isinstance(element, (str, Path)):
            result.append(Path(element))

        # Deduplicate preserving order
        seen = set()
        final_result = []
        for r in result:
            if r not in seen:
                seen.add(r)
                final_result.append(r)

        return final_result

    def get_filelist(self):
        """Returns generator of identical files."""
        return (f for f in self._files)

    async def run(self):
        status = False
        if not self._files:
            return False

        if self.iterate:
            files = list(self.get_filelist())
            step, target, params = self.get_step()
            step_name = step.name

            if self._parallelize:
                # Parallelized execution
                threads = []
                semaphore = Semaphore(self._num_threads)
                with tqdm(total=len(files)) as pbar:
                    for file in files:
                        self._result = file
                        params["filename"] = file
                        # Provide parent directory dynamically from the current file
                        params["directory"] = str(file.parent)
                        job = self.get_job(target, **params)
                        if job:
                            pbar.set_description(f"Processing {file.name}")
                            thread = ThreadJob(job, step_name, semaphore)
                            threads.append(thread)
                            thread.start()
                    # wait for all threads to finish
                    results = []
                    for thread in threads:
                        thread.join()
                        # check if thread raised any exceptions
                        if thread.exc:
                            raise thread.exc
                        pbar.update(1)
                        results.append(thread.result)
                if check_empty(results):
                    return False
                else:
                    self._result = results
                    return self._result
            else:
                # Sequential execution
                with tqdm(total=len(files)) as pbar:
                    for file in files:
                        self._result = file
                        params["filename"] = file
                        # Provide parent directory dynamically from the current file
                        params["directory"] = str(file.parent)
                        logging.debug(f" :: Loading File: {file}")
                        status = False
                        job = self.get_job(target, **params)
                        if job:
                            pbar.set_description(f"Processing {file.name}")
                            try:
                                status = await self.async_job(job, step_name)
                                pbar.update(1)
                            except (ProviderError, ComponentError, NotSupported) as err:
                                raise NotSupported(
                                    f"Error running Component {step_name}, error: {err}"
                                ) from err
                            except Exception as err:
                                raise ComponentError(
                                    f"Generic Component Error on {step_name}, error: {err}"
                                ) from err
                if check_empty(status):
                    return False
                else:
                    return status
        else:
            files = self.get_filelist()
            if files:
                if self.generator is False:
                    self._result = list(files)
                else:
                    self._result = files
                if len(self._result) < 100:
                    self.add_metric("FILE_LIST", self._result)
                self.add_metric("FILE_LIST_COUNT", len(self._result))
                return self._result
            else:
                raise FileNotFound(
                    f"MergeFileList: No files found in inputs {self.input}"
                )

    async def close(self):
        pass
