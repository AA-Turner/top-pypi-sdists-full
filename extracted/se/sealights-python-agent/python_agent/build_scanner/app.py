import fnmatch
import logging
import os
import re
import time

from python_agent.build_scanner.entities.v3.build_mapping_request import (
    BuildMappingRequest,
)
from python_agent.build_scanner.file_scanner import FileScanner
from python_agent.build_scanner.scm.git_integration import GitIntegration
from python_agent.build_scanner.slignore_parser import SLIgnoreParser
from python_agent.common import constants
from python_agent.common.constants import DEFAULT_WORKSPACEPATH, SLIGNORE_FILENAME
from python_agent.common.constants import MetadataKeys
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.utils import retries, get_top_relative_path
from python_agent.utils import to_str_list

log = logging.getLogger(__name__)


def prepare_build_request(scanned_files, config_data):
    log.debug(
        "Filling build request: scanned files size=%s, %s"
        % (len(scanned_files), config_data)
    )
    git_integration = GitIntegration(config_data, scanned_files)
    scm_info = git_integration.collect_scm_info()
    meta = create_meta_data(scm_info, config_data)
    request = BuildMappingRequest(
        meta,
        config_data,
        [filename for filename in git_integration.scanned_files.values()],
    )
    return request


def create_meta_data(scm_info, config_data):
    meta = {
        MetadataKeys.GENERATED: int(time.time() * 1000),
        MetadataKeys.CUSTOMER_ID: config_data.customerId,
        MetadataKeys.APP_NAME: config_data.appName,
        MetadataKeys.BUILD: config_data.buildName,
        MetadataKeys.BRANCH: config_data.branchName,
        MetadataKeys.TECHNOLOGY: constants.TECHNOLOGY,
        MetadataKeys.SCM_PROVIDER: config_data.scmProvider,
        MetadataKeys.SCM_BASE_URL: config_data.scmBaseUrl,
        MetadataKeys.SCM_VERSION: config_data.scmVersion,
        MetadataKeys.SCM: scm_info.scm_type,
        MetadataKeys.COMMIT: scm_info.head_commit,
        MetadataKeys.HISTORY: scm_info.commit_history,
        MetadataKeys.COMMIT_LOG: scm_info.commit_log,
        MetadataKeys.CONTRIBUTORS: scm_info.contributors,
        MetadataKeys.REPOSITORY_URL: scm_info.repo_url,
    }
    return meta


@retries(log)
def send_build(body, config_data):
    if config_data.server:
        backend_proxy = BackendProxy(config_data)
        backend_proxy.submit_build_mapping(config_data, body)
    else:
        log.warning("Server url is undefined, cannot send request to server")


def filter_by_pattern(patterns, source_dir, subdir, files):
    filtered_files = set()
    for pattern in patterns:
        for basename in files:
            full_path = os.path.join(subdir, basename)
            if fnmatch.fnmatch(full_path, pattern):
                filtered_files.add(full_path)
    return filtered_files


def canonical_files(subdir, files):
    return [os.path.join(subdir, filename) for filename in files]


def get_all_files(workspacepath, includes=None, excludes=None):
    """
    :param workspacepath: A list of directories or package names.
    If specified, only source inside these directories or packages will be scanned.

    :param includes: A list of file name patterns. If specified, only files matching those patterns will be measured

    :param excludes: A list of file name patterns, specifying files not to scan.

    If both include and omit are specified,
    first the set of files is reduced to only those that match the include patterns,
    then any files that match the omit pattern are removed from the set.

    :return: A list of full path python only files to be scanned
    """
    all_files = []
    if not workspacepath:
        log.warning("Argument 'workspacepath' is null or empty. Skipping files scan")
    if os.path.isfile(workspacepath):
        all_files.append(workspacepath)
    for subdir, dirs, files in os.walk(workspacepath):
        included_files = set(canonical_files(subdir, files))
        excluded_files = set()
        if includes:
            included_files = filter_by_pattern(includes, workspacepath, subdir, files)
        if excludes:
            excluded_files.update(
                filter_by_pattern(excludes, workspacepath, subdir, files)
            )

        included_files = list(included_files - excluded_files)
        included_files = [
            os.path.abspath(filename)
            for filename in included_files
            if re.match(constants.PYTHON_FILES_REG, os.path.split(filename)[1])
        ]
        all_files.extend(included_files)

    return all_files


def _resolve_file_filters(workspacepath, include, exclude):
    """
    Resolve file filters based on .slignore precedence.

    If .slignore exists in the workspace:
        - Use patterns from .slignore as exclude list
        - Ignore CLI include/exclude parameters
        - Log warning if CLI params were provided

    If .slignore does not exist:
        - Use CLI include/exclude parameters as-is

    Args:
        workspacepath: Path to the workspace root
        include: CLI include patterns (or None)
        exclude: CLI exclude patterns (or None)

    Returns:
        Tuple of (resolved_include, resolved_exclude)
    """
    parser = SLIgnoreParser(workspacepath)

    if parser.exists():
        # .slignore takes precedence
        if include or exclude:
            log.warning(
                f"{SLIGNORE_FILENAME} found in workspace. "
                f"CLI --include/--exclude parameters will be ignored."
            )

        slignore_patterns = parser.parse()
        return [], slignore_patterns  # No includes, only excludes from .slignore
    else:
        # No .slignore - use CLI params
        return include or [], exclude or []


def scan_files(workspacepath, include, exclude):
    workspacepath = workspacepath or DEFAULT_WORKSPACEPATH

    # Check for .slignore file - it takes precedence over CLI params
    include, exclude = _resolve_file_filters(workspacepath, include, exclude)

    log.info(
        "Filtering files for workspacepath=%s, include=%s, exclude=%s"
        % (workspacepath, include, exclude)
    )
    files = get_all_files(workspacepath, include, exclude)
    log.info("Number of files for scanning:%s" % len(files))
    log.debug(to_str_list("Files to be scanned", files))
    file_scanner = FileScanner()
    scanned_files = dict()
    total_methods = 0
    total_lines = 0
    for full_path in files:
        scanned = file_scanner.calculate_file_signature(
            full_path, get_top_relative_path(full_path, workspacepath=workspacepath)
        )
        if scanned:
            if scanned.methods:
                scanned_files[full_path] = scanned
                total_methods += len(scanned.methods)
                total_lines += sum([len(method.lines) for method in scanned.methods])
            else:
                log.debug(
                    "File %s was scanned but no methods were found, coverage will be ignored for this file."
                    % full_path
                )
        else:
            log.debug(
                "File %s was not scanned, coverage will be ignored for this file."
                % full_path
            )

    if len(scanned_files) != len(files):
        log.warning(
            "Not all files have methods: files with methods=%s, total files=%s (set debug mode for more info)"
            % (len(scanned_files), len(files))
        )

    log.info(
        "Scan results: total files: %s, total methods: %s, total lines: %s"
        % (len(scanned_files), total_methods, total_lines)
    )
    ConsoleMessageTemplates.render_and_print(
        "common.build-scanner.scanner-scanning-result",
        filesScannedCount=len(scanned_files),
        filesReportedCount=len(scanned_files),
        includedMethodsCount=total_methods,
    )
    return scanned_files


def main(config_data=None, workspacepath=None, include=None, exclude=None):
    scanned_files = scan_files(workspacepath, include, exclude)
    if not scanned_files or len(scanned_files) == 0:
        log.warning("Total scanned files is 0. Skip sending build to server")
        return
    body = prepare_build_request(scanned_files, config_data)
    send_build(body, config_data)
