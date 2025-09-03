from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Union

from bigeye_sdk.bigconfig_validation.validation_models import FileMatchResult, ValidationError
from bigeye_sdk.exceptions.exceptions import FileLoadException
from bigeye_sdk.functions.search_and_match_functions import search_lines_in_source_lines
from bigeye_sdk.log import get_logger

log = get_logger(__name__)

"{ file_name: { line_number: line }}"
_BIGEYE_YAML_FILE_IX: Dict[str, Dict[int, str]] = {}

"{erroneous_configuration_cls_name: ValidationError}"
_VALIDATION_ERROR_IX: Dict[str, List[ValidationError]] = {}

"{file_name: {file_start_loc: file_match_results}}"
_FILE_ERROR_MATCH_RESULT_IX: Dict[str, Dict[int, List[FileMatchResult]]] = {}


def register_validation_error(cls, error_lines: List[str], error_message: str,
                              error_context_lines: List[str] = None):
    """
    Appends a validation error to the _Validator_Context by instantiating a ValidationError.
    YamlModelWithValidatorContext has this built in as a class method.
    Args:
        cls: the class to which the registration error will be registered
        error_lines: lines of the exact error
        error_context_lines: lines of the broader section of yaml containing error
        error_message: error message to log as a warning.

    Returns: None

    """
    ve = ValidationError(error_lines=error_lines,
                         erroneous_configuration_cls_name=cls.__name__,
                         error_message=error_message,
                         error_context_lines=error_context_lines)

    put_validation_error_to_ix(ve)


def _testcase_support_clear_validation_context():
    _VALIDATION_ERROR_IX.clear()
    _BIGEYE_YAML_FILE_IX.clear()
    _FILE_ERROR_MATCH_RESULT_IX.clear()


def put_bigeye_yaml_file_to_ix(file_name: str) -> Dict[str, Dict[int, str]]:
    current_line_number = 0

    file_contents: Dict[int, str] = {}

    with open(file_name, 'r') as fin:
        for line in fin:
            current_line_number = current_line_number + 1
            file_contents[current_line_number] = line

    if file_name in _BIGEYE_YAML_FILE_IX.keys():
        raise FileLoadException(f"Duplicate file found: {file_name}")

    _BIGEYE_YAML_FILE_IX[file_name] = file_contents

    return _BIGEYE_YAML_FILE_IX


def process_validation_errors(output_path: str = None) -> list[str]:
    """

    Args:
        output_path: path where error reports will be dumped.  Defaults to current working directory.

    Returns: list of generated fix-me files.

    """
    if not output_path:
        output_path = Path.cwd()

    _search_validation_errors_in_files()
    return _generate_fixmes(output_path=output_path)


def put_validation_error_to_ix(ve: ValidationError):
    if ve.erroneous_configuration_cls_name in _VALIDATION_ERROR_IX.keys():
        _VALIDATION_ERROR_IX[ve.erroneous_configuration_cls_name].append(ve)
    else:
        _VALIDATION_ERROR_IX[ve.erroneous_configuration_cls_name] = [ve]


def put_file_error_match_result_to_ix(fmr: FileMatchResult):
    line_number = min(fmr.lines)
    if fmr.file_name in _FILE_ERROR_MATCH_RESULT_IX.keys():
        """if file name key exists?"""
        if min(fmr.lines) in _FILE_ERROR_MATCH_RESULT_IX[fmr.file_name]:
            _FILE_ERROR_MATCH_RESULT_IX[fmr.file_name][line_number].append(fmr)
        else:
            _FILE_ERROR_MATCH_RESULT_IX[fmr.file_name][min(fmr.lines)] = [fmr]
    else:
        """if file name key does not exist"""
        _FILE_ERROR_MATCH_RESULT_IX[fmr.file_name] = {}
        _FILE_ERROR_MATCH_RESULT_IX[fmr.file_name][line_number] = [fmr]


def get_validation_errors(
        configuration_cls_name: str = None
) -> Union[Dict[str, List[ValidationError]], List[ValidationError]]:
    if not configuration_cls_name:
        return _VALIDATION_ERROR_IX
    else:
        return _VALIDATION_ERROR_IX.get(configuration_cls_name, [])


def get_all_validation_errors_flat(only_unmatched: bool = False) -> List[ValidationError]:
    if only_unmatched:
        return [ve for i in _VALIDATION_ERROR_IX.values() for ve in i if not ve.matched_in_file]
    else:
        return [ve for i in _VALIDATION_ERROR_IX.values() for ve in i]


def get_validation_error_cnt() -> int:
    return sum([1 for i in _VALIDATION_ERROR_IX.values() for ve in i])


def get_file_error_match_cnt() -> int:
    return sum([len(fmr) for flix in _FILE_ERROR_MATCH_RESULT_IX.values() for fmr in flix.values()])


def get_file_error_match_results(
        file_name: str = None
) -> Union[
    Dict[str, Dict[int, List[FileMatchResult]]],
    Dict[int, List[FileMatchResult]]
]:
    """

    Args:
        file_name: If present, will return the index of matches for that specific file.  If not present, will
        return

    Returns: Either:
                An index of matching lines keyed by the first line of the match OR
                An index the index of matching lines nested in an index of files keyed by file name.

    """
    if not file_name:
        return _FILE_ERROR_MATCH_RESULT_IX
    else:
        return _FILE_ERROR_MATCH_RESULT_IX[file_name]


def _generate_fixmes(output_path: str) -> List[str]:
    """

    Args:
        output_path: path to output fix-me files.

    Returns: list of fix-me files generated.

    """
    os.makedirs(output_path, exist_ok=True)

    fixme_files: List[str] = []
    for file_name, file_match_result_ix in _FILE_ERROR_MATCH_RESULT_IX.items():
        fixme_file = f'{output_path}/FIXME_{Path(file_name).name}'
        with open(fixme_file, 'w') as fout:
            for line_number, line in _BIGEYE_YAML_FILE_IX[file_name].items():
                if line_number in file_match_result_ix.keys():
                    """If error exists for line then print report inline."""
                    fout.write('>>>>')

                    fmr: FileMatchResult

                    written_error_messages: List[str] = []

                    for fmr in file_match_result_ix[line_number]:
                        if fmr.error_message not in written_error_messages:
                            fout.write('\n')
                            fout.write(fmr.error_message)
                            fout.write('\n')
                            written_error_messages.append(fmr.error_message)

                    fout.write('<<<<')
                    fout.write('\n')

                fout.write(line)

        fixme_files.append(fixme_file)

    return fixme_files


def _search_validation_errors_in_files():
    for err_class, ves in _VALIDATION_ERROR_IX.items():
        for ve in ves:
            _search_validation_error_in_files(ve)


def _search_validation_error_in_files(ve: ValidationError) -> ValidationError:
    file_match_results: List[FileMatchResult] = []

    if ve.error_context_lines:
        search_lines = ve.error_context_lines
        is_error_context_search = True
    else:
        search_lines = ve.error_lines
        is_error_context_search = False

    for file_name, file_content in _BIGEYE_YAML_FILE_IX.items():
        matching_lines_sets = search_lines_in_source_lines(search_lines=search_lines,
                                                           source_lines=file_content)

        if is_error_context_search:
            """Match all error_lines to each matched error_content_lines."""
            context_sets = matching_lines_sets
            matching_lines_sets: List[Dict[int, str]] = []

            for mls in context_sets:
                found_sub_matches = search_lines_in_source_lines(
                    search_lines=ve.error_lines,
                    source_lines=mls
                )
                matching_lines_sets.extend(found_sub_matches)

        fmrs: List[FileMatchResult] = []

        for m in matching_lines_sets:
            fmr = FileMatchResult(file_name=file_name, lines=m, error_message=ve.error_message)
            fmrs.append(fmr)
            put_file_error_match_result_to_ix(fmr)

        file_match_results.extend(fmrs)

    if file_match_results:
        ve.matched_in_file = True

    return ve
