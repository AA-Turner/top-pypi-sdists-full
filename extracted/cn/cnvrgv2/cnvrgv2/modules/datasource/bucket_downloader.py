import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List

from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.datasource.datasource_operations_interface import DatasourceOperationsInterface


class BucketDownloader:
    def __init__(self, datasource: DatasourceOperationsInterface, destination_folder: str, page_size: int = 100,
                 max_workers: Optional[int] = None) -> None:
        self.datasource = datasource
        self.destination_folder = os.path.abspath(destination_folder)
        self.max_workers = max_workers if max_workers is not None else get_max_workers()
        self.page_size = page_size
        self.page_iterator = self.datasource.list_objects(page_size=page_size)
        os.makedirs(self.destination_folder, exist_ok=True)

    def download_objects(self, objects: List[dict]) -> None:
        """Download multiple objects from S3 using a thread pool."""
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all download tasks and collect Future objects
                # Submit datasource.download_file foreach file_name in the list
                future_to_file = {
                    executor.submit(self.pre_download, file_path): file_path
                    for file_path in objects
                }

                # Iterate over the Future objects as they complete
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        # This will raise an exception if the task raised one
                        future.result()
                    except Exception as error:
                        raise CnvrgError(f"An error occurred while processing {file_path}: {error}")
                        # Cancel remaining futures
                        for pending_future in future_to_file:
                            if not pending_future.done():
                                pending_future.cancel()
                        break  # Exit the loop after canceling the remaining tasks
        except Exception as exc:
            raise CnvrgError(f"Clone error: {exc}")

    def pre_download(self, file_path):
        # destination_path is: self.destination_folder + file_name
        # (where destination_folder should be the datasource slug)
        destination = self._calc_destination_file_path(file_name=file_path)
        directory = os.path.dirname(destination)
        # Prepare destination folder if it doesn't exist: it might be path1/path2/file_name.txt.
        # In this cas we would need to create path1/ and path1/path2/
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not file_path.endswith('/'):
            self.datasource.download_file(file_path=file_path, destination_path=destination)

    def _calc_destination_file_path(self, file_name):
        relative_path = file_name.lstrip('/')  # if file_name is an absolute path, join will ignore self.destination_folder
        return os.path.join(self.destination_folder, relative_path)


def get_max_workers() -> int:
    """
    For IO-bound tasks ( e.g., downloading files from S3),
    a commonly used formula is: max_workers = 2 × number_of_cores + 1
    @return: num of recommended workers
    """
    return 2 * os.cpu_count() + 1
