import os
import re
from pathlib import Path

import unicodedata

from matrx_utils import print_link, vcprint
from matrx_files.base_handler import BaseHandler
from matrx_files.batch_handler import BatchHandler
from matrx_files.cloud_mixin import CloudMixin
from matrx_utils.conf import settings


class FileHandler(CloudMixin, BaseHandler):
    _instances = {}
    _log_intro = "[MATRIX FILE HANDLER]"

    def __init__(
        self,
        app_name,
        new_instance=False,
        batch_print=False,
        print_errors=True,
        batch_handler=None,
    ):
        self.base_dir = Path(settings.BASE_DIR)
        self.app_name = app_name
        self.temp_dir = self.base_dir / "temp" / app_name
        self.data_dir = self.base_dir / "data" / app_name
        self.config_dir = self.base_dir / "config" / app_name
        self.verbose = False
        self.debug = False
        self.batch_print = batch_print
        self.print_errors = print_errors
        self.batch_handler = batch_handler or BatchHandler.get_instance(
            enable_batch=batch_print
        )
        self.batch_print_enabled = (
            self.batch_handler.is_batch_print_enabled()
        )  # Use method instead of accessing private variable
        if batch_print:
            self.batch_handler.enable_batch()

    @classmethod
    def get_instance(
        cls,
        app_name,
        new_instance=False,
        batch_print=False,
        print_errors=True,
        batch_handler=None,
    ):
        key = (app_name, batch_print, print_errors, id(batch_handler))
        if not new_instance and key in cls._instances:
            return cls._instances[key]

        instance = cls(app_name, new_instance, batch_print, print_errors, batch_handler)
        if not new_instance:
            cls._instances[key] = instance
        return instance

    def _get_full_path(self, root, path):
        root_map = {
            "base": self.base_dir,
            "temp": self.temp_dir,
            "data": self.data_dir,
            "config": self.config_dir,
        }
        if root not in root_map:
            raise ValueError(
                f"[FILE HANDLER ERROR!] Invalid root: {root}. Valid 'root' options are: 'base', 'temp', 'data' or 'config'."
            )
        full_path = root_map[root] / path
        return Path(os.path.normpath(str(full_path)))

    def public_get_full_path(self, root, path):
        return self._get_full_path(root=root, path=path)

    def _ensure_directory(self, path):
        directory = path.parent
        directory.mkdir(parents=True, exist_ok=True)

    def _print(self, path, message=None, color=None):
        if color == "red":
            vcprint(
                data="\n"
                + "=" * 35
                + f"  {self._log_intro} ERROR!  "
                + "=" * 35
                + "\n",
                color=color,
            )
        if message is not None:
            vcprint(data=f"{self._log_intro} {message}:", color=color)
        print_link(path)
        if color == "red":
            vcprint(data="=" * 102 + "\n", color=color)

    def _print_link(self, path, message=None, color=None):
        # Pass path, message, and color as separate arguments (not as a tuple) to add_print
        # Todo fix: Here is a bug which causes errors printed twice.
        self.batch_handler.add_print(path, message, color)
        if not self.batch_print_enabled:
            self._print(path=path, message=message, color=color)
        elif color == "red":
            self._print(path=path, message=message, color=color)

    def print_batch(self):
        # This looks correct; we delegate to the batch handler to print all batched messages
        self.batch_handler.print_batch()

    def enable_batch_print(self):
        """Delegate enabling batch prints to the BatchHandler."""
        self.batch_handler.enable_batch()
        self.batch_print_enabled = True  # Keep local state in sync with BatchHandler

    def disable_batch_print(self):
        """Delegate disabling batch prints to the BatchHandler."""
        self.batch_handler.disable_batch()
        self.batch_print_enabled = False  # Keep local state in sync with BatchHandler

    def read(self, path, mode="r", encoding="utf-8"):
        try:
            with open(path, mode, encoding=encoding) as file:
                content = file.read()
            self._print_link(path=path, message="Read file")
            return content
        except FileNotFoundError:
            self._print_link(
                path=path, message="READ FILE ERROR! File not found at", color="red"
            )
            return None
        except Exception as e:
            self._print_link(path=path, message="Error reading file", color="red")
            print(f" Error: {str(e)}")
            return None

    def write(self, path, content, **kwargs):
        self._ensure_directory(Path(path))
        try:
            if isinstance(content, bytes):
                with open(path, "wb") as file:
                    file.write(content)
            elif isinstance(content, str):
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)

            self._print_link(path=path, message="File written")
            return True
        except Exception as e:
            self._print_link(path=path, message="Error writing to file", color="red")
            print(f" Error: {str(e)}")
            return False

    def append(self, path, content):
        self._ensure_directory(Path(path))
        try:
            with open(path, "a", encoding="utf-8") as file:
                file.write(content)
            self._print_link(path=path, message="Appended to file")
            return True
        except Exception as e:
            self._print_link(path=path, message="Error appending to file", color="red")
            print(f" Error: {str(e)}")
            return False

    def delete(self, path):
        try:
            Path(path).unlink()
            self._print_link(path=path, message="File deleted")
            return True
        except FileNotFoundError:
            self._print_link(
                path=path, message="DELETE FILE ERROR! File not found at ", color="red"
            )
            return False
        except Exception as e:
            self._print_link(path=path, message="Error deleting file", color="red")
            print(f" Error: {str(e)}")
            return False

    def read_from_base(
        self,
        root,
        path,
    ):
        full_path = self._get_full_path(root, path)
        return self.read(str(full_path))

    def write_to_base(
        self,
        root,
        path,
        content,
        clean=True,
        remove_html=False,
        normalize_whitespace=False,
    ):
        full_path = self._get_full_path(root, path)
        if clean:
            content = self.clean(
                content,
                remove_html=remove_html,
                normalize_whitespace=normalize_whitespace,
            )
        return self.write(str(full_path), content)

    def append_to_base(self, root, path, content):
        full_path = self._get_full_path(root, path)
        return self.append(str(full_path), content)

    def delete_from_base(self, root, path):
        full_path = self._get_full_path(root, path)
        return self.delete(str(full_path))

    def clean(self, content, remove_html=False, normalize_whitespace=False):
        if isinstance(content, str):
            if remove_html:
                content = self._remove_html_tags(content)
            content = self._normalize_unicode(content)
            # Jatin made changes here.
            content = self._filter_unwanted_characters(content)
            if normalize_whitespace:
                content = self._normalize_whitespace(content)
        elif isinstance(content, dict):
            return {
                k: self.clean(v, remove_html, normalize_whitespace)
                for k, v in content.items()
            }
        elif isinstance(content, list):
            return [
                self.clean(item, remove_html, normalize_whitespace) for item in content
            ]
        return content

    def _remove_html_tags(self, content):
        content = re.sub(r"(<[^>]+>)", r" \1 ", content)
        return re.sub(r"<[^>]+>", "", content)

    def _normalize_unicode(self, content):
        return unicodedata.normalize("NFKC", content)

    def _filter_unwanted_characters(self, content):
        return "".join(
            char if char.isprintable() or char in ["\n", "\t"] else " "
            for char in content
        )

    def _normalize_whitespace(self, content):
        content = re.sub(r"\s+", " ", content)
        return content.strip()

    def file_exists(self, root, path):
        full_path = self._get_full_path(root, path)
        exists = full_path.exists()
        if exists:
            self._print_link(full_path, message="File exists")
        else:
            self._print_link(full_path, message="File does not exist")
        return exists

    def delete_file(self, root, path):
        full_path = self._get_full_path(root, path)
        try:
            full_path.unlink()
            self._print_link(full_path, message="File deleted")
            return True
        except FileNotFoundError:
            self._print_link(
                full_path, message="DELETE FILE ERROR! File not found at ", color="red"
            )
            return False
        except Exception as e:
            self._print_link(full_path, message="Error deleting file", color="red")
            print(f" Error: {str(e)}")
            return False

    def list_files(self, root, path=""):
        full_path = self._get_full_path(root, path)
        try:
            files = [f.name for f in full_path.iterdir() if f.is_file()]
            return files
        except Exception as e:
            self._print_link(full_path, message="Error listing files in ", color="red")
            print(f" Error: {str(e)}")
            return []

    def add_to_batch(self, full_path, message=None, color=None):
        _message = "Manual Batch Print "
        if message:
            _message += message

        full_path = str(full_path)

        self.batch_handler.add_print(full_path, _message, color)

        if not self.batch_print_enabled:
            self._print(path=full_path, message=_message, color=color)
