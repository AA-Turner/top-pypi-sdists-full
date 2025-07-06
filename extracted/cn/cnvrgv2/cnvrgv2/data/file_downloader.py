import json
import os

from cnvrgv2.data.remote_files_handler import RemoteFilesHandler
from cnvrgv2.proxy import HTTP
from cnvrgv2.utils.storage_utils import create_dir_if_not_exists
from cnvrgv2.utils.url_utils import urljoin


class FileDownloader(RemoteFilesHandler):
    def __init__(self, data_owner, use_cached=False, num_workers=40, queue_size=5000, chunk_size=1000,
                 override=False, progress_bar_enabled=False, query_slug=None, fullpath_filter=None):
        """
        Multithreaded file bucket_downloader.py - download files from server
        @param data_owner: Cnvrg dataset / project object
        @param num_workers: Number of threads to handle files
        @param queue_size: Max number of file meta to put in queue
        @param chunk_size: File meta chunk size to fetch from the server
        @param override: Override existing files
        """
        self.mode = "files"
        self.commits_url = urljoin(data_owner._route, "commits", data_owner.last_commit,
                                   "files") + "?" + "page[after]={}&page[size]={}&sort=id&mode={}"

        self.query_slug = query_slug

        # Default filter matches all files
        self.filter = {
            "operator": 'OR',
            "conditions": [
                {
                    "key": 'fullpath',
                    "operator": 'like',
                    "value": "*",
                }
            ],
        }

        total_files_query_url = self.commits_url.format('', 0, "files")
        total_folders_query_url = self.commits_url.format('', 0, "folders")

        if fullpath_filter:
            self.filter["conditions"][0]["value"] = fullpath_filter
            total_files_query_url += "&filter={}".format(json.dumps(self.filter))
            total_folders_query_url += "&filter={}".format(json.dumps(self.filter))

        if query_slug:
            total_files_query_url += "&query_slug={}".format(query_slug)
            total_folders_query_url += "&query_slug={}".format(query_slug)

        super().__init__(
            data_owner,
            num_workers=num_workers,
            queue_size=queue_size,
            chunk_size=chunk_size,
            override=override,
            use_cached=use_cached,
            progress_bar_enabled=progress_bar_enabled
        )

        total_files = data_owner._proxy.call_api(
            route=total_files_query_url,
            http_method=HTTP.GET
        ).meta["total"]

        total_folders = data_owner._proxy.call_api(
            route=total_folders_query_url,
            http_method=HTTP.GET
        ).meta["total"]

        self.total_files = total_files + total_folders

    def _collector_function(self, page_after=None):
        """
        Function to collect files that should be downloaded
        @param page_after: The id of the next file that the iteration of the pagination should start from
        @return: Should return array of files metadata
        """

        data = {
            "filter": json.dumps(self.filter),
            "query_slug": self.query_slug,
            "cache_link": self.use_cached
        }

        response = self.data_owner._proxy.call_api(
            route=self.commits_url.format(page_after, self.chunk_size, self.mode),
            http_method=HTTP.GET,
            payload=data
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
            "next": response.meta["next"],
            "total_files_size": response.meta["total_files_size"]
        }

    def _handle_file_function(self, local_path, progress_bar=None, **kwargs):
        """
        Function that download single file
        @param local_path: File location locally
        @param progress_bar: A progress bar object to be used during the download
        @param kwargs: Needs to be object_path of the file in the bucket
        @return: None
        """
        is_cached = False
        if self.use_cached:
            is_cached = cache_file(self.data_owner.title, local_path, kwargs["fullpath"],
                                   kwargs.get("cached_commits", []))

        if not is_cached and (self.override or not os.path.exists(local_path)):
            self.storage_client.download_single_file(local_path, kwargs["object_path"], progress_bar=progress_bar)

        self.handle_queue.task_done()
        self.progress_queue.put(local_path)


def cache_file(dataset, local_path, fullpath, commits, back_path="/nfs-disk/"):
    is_cached = False
    for commit in commits:
        nfs_path = "{}{}/{}/{}".format(back_path, commit, dataset, fullpath)
        if os.path.exists(nfs_path):
            is_cached = True
            create_dir_if_not_exists(local_path)
            os.link(os.path.abspath(nfs_path), local_path)

    return is_cached
