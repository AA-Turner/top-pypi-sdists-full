import os
import asyncio
import logging
from collections.abc import Callable
from pathlib import Path
from tqdm import tqdm
from threading import Semaphore
from asyncdb.exceptions import NoDataFound, ProviderError
from ..exceptions import ComponentError, NotSupported, FileNotFound, DataNotFound
from .IteratorBase import IteratorBase, ThreadJob
from ..interfaces.skip_policy import (
    ConsecutiveFailureTracker,
    SKIPPED_ITERATION,
)


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
                tracker = ConsecutiveFailureTracker(self.max_consecutive_failures)
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
                        if thread.exc is not None:
                            if isinstance(thread.exc, (NoDataFound, DataNotFound, FileNotFound)):
                                # D3: continue INCONDICIONAL, y NO cuenta
                                # para el umbral — paridad con el camino
                                # secuencial.
                                self._logger.debug(
                                    f"Data not Found for {step_name}, got: {thread.exc}"
                                )
                                continue
                            raise thread.exc
                        # check if iteration was skipped
                        if thread.result is SKIPPED_ITERATION:
                            should_abort = tracker.record_skip(ComponentError("Skipped iteration for file"))
                            if should_abort:
                                tracker.publish(self)
                                raise ComponentError(
                                    f"MergeFileList: Aborted due to {tracker.consecutive} consecutive failures. Last error: {tracker.last_error}"
                                ) from tracker.last_error
                        else:
                            tracker.record_success()
                            results.append(thread.result)
                        pbar.update(1)
                tracker.publish(self)
                if not results:
                    return False
                else:
                    self._result = results
                    return self._result
            else:
                # Sequential execution
                tracker = ConsecutiveFailureTracker(self.max_consecutive_failures)
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
                            except (NoDataFound, DataNotFound, FileNotFound) as err:
                                # D3: continue INCONDICIONAL, y NO cuenta para el umbral.
                                self._logger.debug(f"Data not Found for {step_name}, got: {err}")
                                continue
                            except (ProviderError, ComponentError, NotSupported):
                                # async_job ya consulto skipError: si llega aqui era ENFORCE.
                                raise
                            except Exception as err:
                                raise ComponentError(
                                    f"Component Error on {step_name}, error: {err}"
                                ) from err
                            
                            if status is SKIPPED_ITERATION:
                                should_abort = tracker.record_skip(ComponentError(f"Skipped iteration for file {file.name}"))
                                if should_abort:
                                    tracker.publish(self)
                                    raise ComponentError(
                                        f"MergeFileList: Aborted due to {tracker.consecutive} consecutive failures at file {file.name}. Last error: {tracker.last_error}"
                                    ) from tracker.last_error
                            else:
                                tracker.record_success()
                            pbar.update(1)
                tracker.publish(self)
                return tracker.successes > 0
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
