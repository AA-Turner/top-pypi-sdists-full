import os
import shutil
import tarfile

import requests

from cnvrgv2.cli.utils.progress_bar_utils import init_progress_bar_for_cli
from cnvrgv2.config.routes import LIBRARY_VERSION_BASE, USE_LIBRARY_SUFFIX
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.url_utils import urljoin


class LibraryVersion(DynamicAttributes):
    available_attributes = {
        "version": str,
        "summary": str,
        "author": str,
        "home_page": str,
        "author_email": str,
        "library_id": int,
        "schema_link": str,
        "dependency_link": str,
        "description_link": str,
        "files_download_link": str
    }

    def __init__(self, context=None, version=None, attributes=None):
        # Init data attributes
        super().__init__()

        self._context = Context(context=context)
        self.progress_bar = None

        # Set current context scope to current project
        if version:
            self._context.set_scope(SCOPE.LIBRARY_VERSION, version)

        scope = self._context.get_scope(SCOPE.LIBRARY_VERSION)

        self._proxy = Proxy(context=self._context)
        self._route = LIBRARY_VERSION_BASE.format(scope["organization"], scope["library"], scope["library_version"])
        self._attributes = attributes or {}
        self.version = scope["library_version"]

    def clone(self, progress_bar_enabled=False, working_dir=None):
        """
        Clones the remote library
        @param progress_bar_enabled: Boolean indicating whenever or not to print a progress bar. In use of the cli
        @param working_dir: String the directory that the library will be cloned to
        @return: None
        """
        destination_prefix = './{0}/'.format(working_dir) if working_dir else './'
        destination = "{0}{1}".format(destination_prefix, self._context.library)

        if not os.path.isdir(destination):
            os.mkdir(destination)

        response = requests.get(self.files_download_link, allow_redirects=True, stream=True)
        total_length = response.headers.get('content-length')

        # TODO: Check download counter goes up every clone

        try:
            self._proxy.call_api(
                route=urljoin(self._route, USE_LIBRARY_SUFFIX),
                http_method=HTTP.PUT,
            )
        except Exception:
            pass  # if libhub failed - I don't care

        tar_path = "{0}.tar.gz".format(self.version)
        file = open(tar_path, 'wb')

        total_length = int(total_length)

        if progress_bar_enabled:
            self.progress_bar = init_progress_bar_for_cli("Downloading", total_length)

        self.progress_bar.start()
        for chunk in response.iter_content(chunk_size=32000):
            delta = len(chunk)
            file.write(chunk)
            if progress_bar_enabled:
                self.progress_bar.throttled_next(delta)
        self.progress_bar.finish()

        file.close()

        tar = tarfile.open(tar_path)
        tar.extractall(destination)
        tar.close()

        if len(os.listdir(destination)) == 1:
            source_dir = os.path.join(destination, os.listdir(destination)[0])
            if os.path.isdir(source_dir):
                file_names = os.listdir(source_dir)

                for file_name in file_names:
                    shutil.move(os.path.join(source_dir, file_name), destination)

                os.removedirs(source_dir)

        if not os.path.isfile(os.path.join(destination, "__init__.py")):
            file = open(os.path.join(destination, "__init__.py"), "w+")
            file.close()

        os.remove(tar_path)
