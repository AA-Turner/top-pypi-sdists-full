# -*- coding: utf-8 -*-
import os
import time

from behavex.execution_singleton import ExecutionSingleton


class GlobalVars(metaclass=ExecutionSingleton):
    def __init__(self):
        # Ensure BEHAVEX_PATH is set if not already
        if 'BEHAVEX_PATH' not in os.environ:
            os.environ['BEHAVEX_PATH'] = os.path.dirname(os.path.realpath(__file__))
        self._execution_path = os.environ.get('BEHAVEX_PATH')
        self._report_filenames = {
            'report_json': 'report.json',
            'report_overall': 'overall_status.json',
            'report_failures': 'failing_scenarios.txt',
        }
        self._behave_tags_file = os.path.join('behave', 'behave.tags')
        self._jinja_templates_path = os.path.join(
            self._execution_path, 'outputs', 'jinja'
        )
        self._jinja_templates = {
            'main': 'main.jinja2',
            'steps': 'steps.jinja2',
            'xml': 'xml.jinja2',
            'xml_json': 'xml_json.jinja2',
            'manifest': 'manifest.jinja2',
        }
        self._retried_scenarios = {}
        self._steps_definitions = {}
        self._rerun_failures = False
        self._progress_bar_instance = None
        self._execution_start_time = time.time()
        self._execution_end_time = None

        # Behave version detection (lazy loaded)
        self._behave_version = None

        # Tag expression version detection (lazy loaded)
        self._tag_expression_version = None


    @property
    def execution_path(self):
        return self._execution_path

    @property
    def report_filenames(self):
        return self._report_filenames

    @property
    def behave_tags_file(self):
        return self._behave_tags_file

    @property
    def jinja_templates_path(self):
        return self._jinja_templates_path

    @property
    def jinja_templates(self):
        return self._jinja_templates

    @property
    def retried_scenarios(self):
        return self._retried_scenarios

    @retried_scenarios.setter
    def retried_scenarios(self, feature_name):
        self._retried_scenarios[feature_name] = []

    @property
    def steps_definitions(self):
        return self._steps_definitions

    @property
    def rerun_failures(self):
        return self._rerun_failures

    @rerun_failures.setter
    def rerun_failures(self, rerun_failures):
        self._rerun_failures = rerun_failures

    @property
    def progress_bar_instance(self):
        return self._progress_bar_instance

    @progress_bar_instance.setter
    def progress_bar_instance(self, progress_bar_instance):
        self._progress_bar_instance = progress_bar_instance

    @property
    def execution_start_time(self):
        return self._execution_start_time

    @execution_start_time.setter
    def execution_start_time(self, execution_start_time):
        self._execution_start_time = execution_start_time

    @property
    def execution_elapsed_time(self):
        return time.time() - self._execution_start_time

    @property
    def execution_end_time(self):
        if not self._execution_end_time:
            self._execution_end_time = time.time()
        return self._execution_end_time

    @property
    def behave_version(self):
        """
        Get the Behave version (lazy loaded, calculated only once).

        Returns:
            tuple: Version tuple (major, minor, patch)
        """
        if self._behave_version is None:
            self._behave_version = _detect_behave_version()
        return self._behave_version

    @property
    def tag_expression_version(self):
        """
        Get the tag expression version (lazy loaded, calculated only once).

        Analyzes all tag arguments to determine if they use v1 (legacy) or v2 (Behave 1.3.0+) syntax.

        Returns:
            str: 'v1' for legacy format, 'v2' for Behave 1.3.0+ format, 'v1' as default
        """
        if self._tag_expression_version is None:
            self._tag_expression_version = _detect_tag_expression_version()
        return self._tag_expression_version


def _detect_behave_version():
    """
    Detect the installed Behave version.

    Returns:
        tuple: Version tuple (major, minor, patch) or (0, 0, 0) if not available
    """
    try:
        import behave
        version_str = behave.__version__
        version_parts = version_str.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        patch = int(version_parts[2]) if len(version_parts) > 2 else 0
        return (major, minor, patch)
    except (ImportError, AttributeError, ValueError, IndexError):
        return (0, 0, 0)


def _detect_tag_expression_version():
    """
    Detect tag expression version by analyzing all tag arguments.

    Simple but efficient algorithm that checks for v2 syntax patterns:
    - Keywords: 'and', 'or', 'not' (case-insensitive)
    - Parentheses for grouping: '(', ')'

    If any v2 patterns are found, returns 'v2', otherwise 'v1'.

    Returns:
        str: 'v1' for legacy format, 'v2' for Behave 1.3.0+ format
    """
    try:
        # Import here to avoid circular imports
        from behavex.conf_mgr import get_env

        # Get all tag expressions from environment
        tags_env = get_env('tags')
        if not tags_env:
            return 'v1'  # Default to v1 if no tags

        # Combine all tag arguments into a single string for analysis
        all_tags = tags_env.replace(';', ' ').lower()

        # v2 syntax indicators (case-insensitive)
        v2_patterns = [
            ' and ',     # Boolean AND operator
            ' or ',      # Boolean OR operator
            ' not ',     # Boolean NOT operator
            '(',         # Grouping with parentheses
            ')',         # Grouping with parentheses
            '*',         # Wildcard matching (v2 feature)
        ]

        # Check for v2 patterns
        for pattern in v2_patterns:
            if pattern in all_tags:
                return 'v2'

        # Additional check: if it starts with 'not ' (beginning of string)
        if all_tags.strip().startswith('not '):
            return 'v2'

        # If no v2 patterns found, it's v1 (legacy)
        return 'v1'

    except Exception:
        # If any error occurs, default to v1 (safe fallback)
        return 'v1'



global_vars = GlobalVars()
