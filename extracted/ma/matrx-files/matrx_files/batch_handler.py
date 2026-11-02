
from collections import defaultdict
from matrx_utils import vcprint, print_link
from pathlib import Path

class BatchHandler:
    _default_instance = None
    _log_intro = "[MATRIX BATCH HANDLER]"

    def __init__(self, enable_batch=False):
        self._batch_prints = set()
        self._batch_print_enabled = enable_batch

    @classmethod
    def get_instance(cls, enable_batch=False):
        if cls._default_instance is None:
            cls._default_instance = cls(enable_batch)
        return cls._default_instance

    def add_print(self, path, message=None, color=None):
        """
        This method adds (path, message, color) directly to the set.
        This mimics the original behavior from the old FileHandler implementation.
        """
        self._batch_prints.add((path, message, color))

    def _print(self, path, message=None, color=None):
        if color == "red":
            vcprint(data="\n" + "=" * 35 + f"  {self._log_intro} ERROR!  " + "=" * 35 + "\n", color=color)
        if message is not None:
            vcprint(data=f"{self._log_intro} {message}:", color=color)
        print_link(path)
        if color == "red":
            vcprint(data="=" * 102 + "\n", color=color)

    def _print_link(self, path, message=None, color=None):
        self._print(path=path, message=message, color=color)

    def print_batch(self):
        """
        Processes the _batch_prints set, which contains (path, message, color) tuples,
        and prints the batched messages as in the original implementation.
        """
        normal_prints = defaultdict(lambda: defaultdict(list))
        error_prints = []

        for path, message, color in self._batch_prints:
            # print(f"DEBUG... Batch: {path}, {message}, {color}") # Commented out by Armani, because I don't think we need it, but if you do, just add it back.

            if color == "red":
                error_prints.append((path, message))
            else:
                normal_prints[message][Path(path).suffix].append((path, color))

        # Print normal messages
        vcprint(data=f"\n{'=' * 25}  {self._log_intro} BATCHED RESULTS  {'=' * 25}", color="cyan")

        for message, extensions in normal_prints.items():
            vcprint(data=f"ACTION: {message}", color="cyan")
            for ext, paths in extensions.items():
                ext_name = f"\nExtension {ext}" if ext else "Files without extension"
                vcprint(data=f"  {ext_name}:", color="cyan")
                for path, color in paths:
                    print_link(path)
            vcprint(data="-" * 40 + "\n", color="cyan")

        vcprint(data=f"{'=' * 25}  {self._log_intro} End Batch print  {'=' * 25}\n", color="cyan")

        # Print errors
        if error_prints:
            for path, message in error_prints:
                vcprint(data=f"\n{'=' * 35}  {self._log_intro} ERROR!  {'=' * 35}\n", color="red")
                vcprint(data=f"{self._log_intro} {message}", color="red")
                print_link(path)
                vcprint(data="\n" + "=" * 102 + "\n", color="red")

        self._batch_prints.clear()

    def enable_batch(self):
        """Enable batch mode, matching the original FileHandler behavior."""
        self._batch_print_enabled = True

    def disable_batch(self):
        """Disable batch mode, matching the original FileHandler behavior."""
        self._batch_print_enabled = False

    def is_batch_print_enabled(self):
        """Returns the current batch print enabled status."""
        return self._batch_print_enabled
