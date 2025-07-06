import json
import os

from cnvrgv2.data.remote_files_handler import RemoteFilesHandler
from cnvrgv2.proxy import HTTP
from cnvrgv2.utils.url_utils import urljoin


class ArtifactsDownloader(RemoteFilesHandler):
    def __init__(
        self,
        data_owner,
        num_workers=40,
        queue_size=5000,
        chunk_size=1000,
        override=False,
        base_commit_sha1=None,
        commit_sha1=None,
        progress_bar_enabled=False,
        ignore_branches=False,
    ):
        """
        Multithreaded file downloader - download artifacts files from server (by compare commit to base_commit)
        @param data_owner: Cnvrg dataset / project object
        @param num_workers: Number of threads to handle files
        @param queue_size: Max number of file meta to put in queue
        @param chunk_size: File meta chunk size to fetch from the server
        @param override: Override existing files
        @param base_commit_sha1: Base commit sha1 of the comparision
        @param commit_sha1: Commit sha1 of the comparision
        @param progress_bar_enabled: Boolean indicating whenever or not to print a progress bar. In use of the cli
        """
        self.mode = "files"
        self.compare_url = urljoin(data_owner._route, "commits", commit_sha1,
                                   "compare") + "?page[after]={}&page[size]={}&sort=id&mode={}"

        self.compare_request_data = {
            "base_commit_sha1": base_commit_sha1,
            "ignore_branches": ignore_branches,
            "filter": json.dumps({
                "operator": 'OR',
                "conditions": [
                    {
                        "key": 'fullpath',
                        "operator": 'like',
                        "value": "*",
                    }
                ],
            })
        }

        super().__init__(
            data_owner,
            num_workers=num_workers,
            queue_size=queue_size,
            chunk_size=chunk_size,
            override=override,
            base_commit_sha1=base_commit_sha1,
            commit_sha1=commit_sha1,
            progress_bar_enabled=progress_bar_enabled
        )

        total_files = data_owner._proxy.call_api(
            route=self.compare_url.format('', 0, "files"),
            http_method=HTTP.GET,
            payload=self.compare_request_data
        ).meta["total"]

        total_folders = data_owner._proxy.call_api(
            route=self.compare_url.format('', 0, "folders"),
            http_method=HTTP.GET,
            payload=self.compare_request_data
        ).meta["total"]

        self.total_files = total_files + total_folders

    def _collector_function(self, page_after=None):
        """
        Function to collect files that should be downloaded
        @param page_after: The id of the next file that the iteration of the pagination should start from
        @return: Should return array of files metadata
        """

        response = self.data_owner._proxy.call_api(
            route=self.compare_url.format(page_after, 1000, self.mode),
            http_method=HTTP.GET,
            payload=self.compare_request_data
        )

        # Once we are out of files we want to move to downloading (empty) folders
        if response.meta["next"] == '' and self.mode == "files":
            self.mode = "folders"
            return {
                "file_dict": [],
                "total_files": self.total_files,
                "total_files_size": 0,
                "next": -100  # placeholder in order to nullify the cursor
            }

        file_dict = []
        for file in response.items:
            file_dict.append(dict(file.attributes))

        return {
            "file_dict": file_dict,
            "total_files": self.total_files,
            "total_files_size": response.meta["total_files_size"],
            "next": response.meta["next"]
        }

    def _handle_file_function(self, local_path, progress_bar=None, **kwargs):
        """
        Function that download single file
        @param local_path: File location locally
        @param progress_bar: A progress bar object to be used during the download
        @param kwargs: Needs to be object_path of the file in the bucket
        @return: None
        """
        if self.override or not os.path.exists(local_path):
            self.storage_client.download_single_file(local_path, kwargs["object_path"], progress_bar)

        self.handle_queue.task_done()
        self.progress_queue.put(local_path)
