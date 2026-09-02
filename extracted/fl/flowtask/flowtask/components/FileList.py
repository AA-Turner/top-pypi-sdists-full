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


class FileList(IteratorBase):
    """
    FileList with optional Parallelization Support.

    Overview

    This component iterates through a specified directory and returns a list of files based on a provided pattern or individual files.
    It supports asynchronous processing and offers options for managing empty results and detailed error handling.


    :widths: auto

    | directory (str)     |   Yes    | Path to the directory containing the files to be listed.                                              |
    | pattern (str)       |    No    | Optional glob pattern for filtering files (overrides individual files if provided).                   |
    | filename (str)      |    No    | Name of the files                                                                                     |
    | iterate (bool)      |    No    | Flag indicating whether to iterate through the files and process them sequentially (defaults to True).|
    | generator (bool)    |    No    | Flag controlling the output format: `True` returns a generator, `False` (default) returns a list.     |
    | file (dict)         |    No    | A dictionary containing two values, "pattern" and "value", "pattern" and "value",                     |
    |                     |          | "pattern" contains the path of the file on the server, If it contains the mask "{value}",             |
    |                     |          | then "value" is used to set the value of that mask                                                    |
    | parallelize         |    No    | If True, the iterator will process rows in parallel. Default is False.                                |
    | num_threads         |    No    | Number of threads to use if parallelize is True. Default is 10.                                       |

    Return the list of files in a Directory


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FileList:
          directory: /home/ubuntu/symbits/bayardad/files/job_advertising/bulk/
          pattern: '*.csv'
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
        self._path = None
        self.pattern = None
        self.data = None
        self.directory: str = None
        self._num_threads: int = kwargs.pop("num_threads", 10)
        self._parallelize: bool = kwargs.pop("parallelize", False)
        super(FileList, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Check if Directory exists."""
        await super(FileList, self).start()
        if not self.directory:
            raise ComponentError("Error: need to specify a Directory")
        if isinstance(self.directory, str) and "{" in self.directory:
            self.directory = self.mask_replacement(self.directory)
            print(f"Directory: {self.directory}")
        # check if directory exists
        p = Path(self.directory)
        if p.exists() and p.is_dir():
            self._path = p
        else:
            raise ComponentError("Error: Directory doesn't exist!")
        return True

    def get_filelist(self):
        if self.pattern:
            value = self.pattern
            if "{" in value:
                value = self.mask_replacement(value)
            if self._variables:
                value = value.format(**self._variables)
            files = (f for f in self._path.glob(value))
        elif hasattr(self, "file"):
            # using pattern/file version
            value = self.get_filepattern()
            files = (f for f in self._path.glob(value) if f.is_file())
        else:
            files = (f for f in self._path.iterdir() if f.is_file())
        files = sorted(files, key=os.path.getmtime)
        return files

    async def run(self):
        status = False
        if not self._path:
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
                        params["directory"] = self.directory
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
                # generate and iterator
                with tqdm(total=len(files)) as pbar:
                    for file in files:
                        self._result = file
                        params["filename"] = file
                        params["directory"] = self.directory
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
                self.add_metric(
                    "FILE_LIST_COUNT", len(self._result)
                )
                return self._result
            else:
                raise FileNotFound(f"FileList: No files found {files}")

    async def close(self):
        pass
