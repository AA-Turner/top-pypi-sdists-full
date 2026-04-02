import importlib.util
import inspect
import os
import sys

from seshat.general.command.base import BaseTyperCommand
from seshat.utils.jobignore import JobIgnoreHandler


class CodeInspectCommand(BaseTyperCommand):
    ctx: dict

    def __init__(self, config, report=True):
        super().__init__(report)

        self.config = config
        self.report = report

        self.ignore_file = config.get("code", {}).get("ignore_file", ".jobignore")

    def find_complexity_factor(self, filename, filepath, max_complexity, relative_path):
        if filename.endswith(".py"):
            try:
                # Quick check if file mentions FeatureView
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "FeatureView" in content and "class" in content:
                        # Import the module
                        max_complexity = self._import_and_run_feature_view(
                            filepath, max_complexity, relative_path
                        )
            except Exception as e:
                self.echo(f"Failed to import file: {str(e)}")
        return max_complexity

    def _import_and_run_feature_view(self, filepath, max_complexity, relative_path):
        module_name = os.path.splitext(relative_path.replace(os.sep, "."))[0]
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Find FeatureView subclasses
            for name, obj in inspect.getmembers(module, inspect.isclass):
                max_complexity = self._call_complexity_calculator(
                    max_complexity, name, obj
                )
            # Clean up
            if module_name in sys.modules:
                del sys.modules[module_name]
        return max_complexity

    def _call_complexity_calculator(self, max_complexity, member_name, obj):
        if hasattr(obj, "__bases__"):
            # Check if it's a FeatureView subclass
            for base in obj.__bases__:
                if "FeatureView" in str(base):
                    # Found a FeatureView subclass
                    if hasattr(obj, "calculate_complexity"):
                        instance = obj()
                        complexity = instance.calculate_complexity()
                        if complexity > max_complexity:
                            max_complexity = complexity
                            self.echo(
                                f"📊 Found {member_name} with complexity: {complexity}"
                            )
        return max_complexity

    def handle(
        self,
        directory: str,
    ):
        self.echo(f"👁️Inspecting code from {directory}")

        job_ignore_handler = JobIgnoreHandler(
            ignore_file=os.path.join(directory, self.ignore_file)
            if os.path.exists(os.path.join(directory, self.ignore_file))
            else None
        )

        total_size = 0
        max_complexity = 0.0

        sys.path.insert(0, directory)

        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                total_size += os.path.getsize(filepath)
                relative_path = os.path.relpath(filepath, directory)

                if job_ignore_handler.match_gitignore_like_path(relative_path):
                    continue

                max_complexity = self.find_complexity_factor(
                    filename, filepath, max_complexity, relative_path
                )

        self.echo(f"📈 Maximum complexity factor: {max_complexity}")

        return max_complexity
