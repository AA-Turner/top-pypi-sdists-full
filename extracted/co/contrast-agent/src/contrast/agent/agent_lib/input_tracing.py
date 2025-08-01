# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


import ctypes
from dataclasses import dataclass, replace
import functools
from enum import IntEnum
from typing import Callable

from contrast.agent import agent_lib
from contrast.api.user_input import InputType, UserInput
from contrast_vendor import structlog as logging
from contrast_agent_lib import lib_contrast, constants

logger = logging.getLogger("contrast")

# These are rules we do not have an implementation for yet
# Other rule IDs where added directly into the protect rule class
SSJS_INJECTION_RULE_ID = 1 << 7

# This should not be used directly. It's used to construct INPUT_TYPE_LOOKUP below.
_AGENT_LIB_TO_TS_INPUT_TYPE = {
    "CookieName": InputType.COOKIE_NAME,
    "CookieValue": InputType.COOKIE_VALUE,
    "HeaderKey": InputType.HEADER,
    "HeaderValue": InputType.HEADER,
    "JsonKey": InputType.JSON_VALUE,  # there is no such thing as InputType.JSON_KEY
    "JsonValue": InputType.JSON_VALUE,
    "Method": InputType.METHOD,
    "ParameterKey": InputType.PARAMETER_NAME,
    "ParameterValue": InputType.PARAMETER_VALUE,
    "UriPath": InputType.URI,
    "UrlParameter": InputType.URL_PARAMETER,
    "MultipartName": InputType.MULTIPART_NAME,
    "XmlValue": InputType.XML_VALUE,
}

_RULE_ID_LOOKUP = {
    rule_int: rule_str for rule_str, rule_int in constants.RuleType.items()
}


class DBType(IntEnum):
    DB2 = 1
    MYSQL = 2
    ORACLE = 3
    POSTGRES = 4
    SQLITE = 5
    SQL_SERVER = 6
    UNKNOWN = 7

    @staticmethod
    def from_str(label: str):
        label = label.upper()
        try:
            return DBType[label]
        except KeyError:
            if label == "SQLITE3":
                return DBType.SQLITE
            if label == "POSTGRESQL":
                return DBType.POSTGRES
            if label in ("SQL SERVER", "SQL_SERVER", "SQLSERVER"):
                return DBType.SQL_SERVER

            return DBType.UNKNOWN


@functools.lru_cache(maxsize=1)
def input_type_lookup() -> dict[int, InputType]:
    """
    agent lib input type int -> InputType enum (TS representation)

    we'd like this to be a module-level dict, but we need to load this after agent_lib
    initialization
    """
    return {
        input_type_int: _AGENT_LIB_TO_TS_INPUT_TYPE.get(
            input_type_str, InputType.UNKNOWN
        )
        for input_type_str, input_type_int in constants.InputType.items()
    }


@dataclass
class InputAnalysisResult:
    input: UserInput
    rule_id: str
    score: float
    attack_count: int = 0

    @classmethod
    def from_ceval_result(cls, input: UserInput, ceval_result: constants.CEvalResult):
        return cls(
            input=replace(
                input,
                matcher_ids=InputAnalysisResult._extract_matcher_ids(ceval_result),
            ),
            rule_id=_RULE_ID_LOOKUP[ceval_result.rule_id],
            score=ceval_result.score,
        )

    @staticmethod
    def _extract_matcher_ids(ceval_result: constants.CEvalResult) -> list[str]:
        matched_ids_buf = bytes(ceval_result.matched_ids)
        return [
            match.decode()
            for match in matched_ids_buf[: matched_ids_buf.find(b"\0\0")].split(b"\0")
            if match
        ]

    def fully_evaluate(self) -> list[InputAnalysisResult]:
        """
        Evaluates the input using the same rule and input type, but without
        optimizations such as worth watching preferences. This is slower, but
        more accurate.
        """
        return (
            evaluate_header_input(
                self.input.name,
                self.input.value,
                constants.RuleType[self.rule_id],
                prefer_worth_watching=False,
            )
            if self.input.type == InputType.HEADER
            else evaluate_input_by_type(
                self.input.type.agent_lib_type,
                self.input.value,
                self.input.name,
                constants.RuleType[self.rule_id],
                prefer_worth_watching=False,
            )
        )


class InjectionResult:
    def __init__(
        self,
        user_input: str,
        input_index: int,
        input_len: int,
        ccheck_query_sink_result: agent_lib.CCheckQuerySinkResult,
    ):
        self.boundary_overrun_index = ccheck_query_sink_result.boundary_overrun_index
        self.end_index = ccheck_query_sink_result.end_index
        self.input_boundary_index = ccheck_query_sink_result.input_boundary_index
        self.start_index = ccheck_query_sink_result.start_index
        self.user_input = user_input
        self.input_index = input_index
        self.input_len = input_len


def evaluate_header_input(
    header_name: str, header_value: str, rules: int, prefer_worth_watching: bool
) -> list[InputAnalysisResult]:
    evaluations = []

    if not agent_lib.IS_INITIALIZED:
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    name = ctypes.c_char_p(bytes(str(header_name), "utf8"))
    value = ctypes.c_char_p(bytes(str(header_value), "utf8"))
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(constants.CEvalResult)()

    ret = agent_lib.call(
        lib_contrast.evaluate_header_input,
        is_valid_return,
        name,
        value,
        rules,
        prefer_worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_eval_result(
        ret,
        results,
        results_len,
        InputType.HEADER,
        header_name,
        header_value,
        is_valid_return,
        evaluations,
    )
    return evaluations


def evaluate_input_by_type(
    input_type: int,
    input_value: str,
    input_key: str | None,
    rules: int,
    prefer_worth_watching: bool,
) -> list[InputAnalysisResult]:
    evaluations = []

    if not agent_lib.IS_INITIALIZED:
        return evaluations

    if rules == 0:
        return evaluations

    def is_valid_return(code):
        return code == 0

    if not isinstance(input_value, str):
        input = ctypes.c_char_p(bytes(str(input_value), "utf8"))
    else:
        input = ctypes.c_char_p(bytes(input_value, "utf8"))
    long_input_type = ctypes.c_long(input_type)
    results_len = ctypes.c_size_t()
    results = ctypes.POINTER(constants.CEvalResult)()

    ret = agent_lib.call(
        lib_contrast.evaluate_input,
        is_valid_return,
        input,
        long_input_type,
        rules,
        prefer_worth_watching,
        ctypes.byref(results_len),
        ctypes.byref(results),
    )

    map_result_and_free_eval_result(
        ret,
        results,
        results_len,
        InputType.from_agent_lib_type(input_type),
        input_key,
        input_value,
        is_valid_return,
        evaluations,
    )
    return evaluations


def check_method_tampering(method: str) -> list[InputAnalysisResult]:
    evaluations = []

    if not agent_lib.IS_INITIALIZED:
        return evaluations

    # These codes should match https://agent-lib.prod.dotnet.contsec.com/src/contrast_c/method_tampering.rs.html#11-28
    IS_TAMPERING = 1
    IS_NOT_TAMPERING = 0

    def is_valid_return(code):
        return code in (IS_TAMPERING, IS_NOT_TAMPERING)

    name = ctypes.c_char_p(bytes(method, "utf8"))

    ret = agent_lib.call(
        lib_contrast.is_method_tampering,
        is_valid_return,
        name,
    )

    if ret != IS_TAMPERING:
        return []

    c_eval_res = constants.CEvalResult()
    c_eval_res.rule_id = constants.RuleType.get("method-tampering")
    c_eval_res.input_type = constants.InputType.get("Method")
    c_eval_res.score = 100

    return [
        InputAnalysisResult.from_ceval_result(
            UserInput(
                type=InputType.METHOD,
                value=method,
                name=method,  # name is needed for CEF logging
            ),
            c_eval_res,
        )
    ]


def check_sql_injection_query(
    user_input_start_index: int,
    user_input_len: int,
    db_type: DBType,
    built_sql_query: str,
) -> InjectionResult | None:
    if not agent_lib.IS_INITIALIZED:
        return None

    def is_valid_return(code):
        return -1 <= code <= 0

    input_index = ctypes.c_uint32(user_input_start_index)
    input_len = ctypes.c_uint32(user_input_len)
    c_db_type = ctypes.c_uint32(int(db_type))
    sql_query = ctypes.c_char_p(bytes(built_sql_query, "utf8"))
    results = ctypes.pointer(agent_lib.CCheckQuerySinkResult())

    ret = agent_lib.call(
        lib_contrast.check_sql_injection_query,
        is_valid_return,
        input_index,
        input_len,
        c_db_type,
        sql_query,
        ctypes.byref(results),
    )

    evaluation = map_result_and_free_check_query_sink_result(
        ret,
        results,
        built_sql_query,
        user_input_start_index,
        user_input_len,
        is_valid_return,
    )
    return evaluation


def check_cmd_injection_query(
    user_input_start_index: int, user_input_len: int, user_input_txt: str
) -> InjectionResult | None:
    if not agent_lib.IS_INITIALIZED:
        return None

    def is_valid_return(code):
        return -1 <= code <= 0

    input_index = ctypes.c_uint32(user_input_start_index)
    input_len = ctypes.c_uint32(user_input_len)
    cmd_text = ctypes.c_char_p(bytes(user_input_txt, "utf8"))
    results = ctypes.POINTER(agent_lib.CCheckQuerySinkResult)()

    ret = agent_lib.call(
        lib_contrast.check_cmd_injection_query,
        is_valid_return,
        input_index,
        input_len,
        cmd_text,
        ctypes.byref(results),
    )

    evaluation = map_result_and_free_check_query_sink_result(
        ret,
        results,
        user_input_txt,
        user_input_start_index,
        user_input_len,
        is_valid_return,
    )
    return evaluation


def map_result_and_free_eval_result(
    ret: int,
    results: ctypes._Pointer[constants.CEvalResult],
    results_len: ctypes.c_size_t,
    type: InputType,
    key: str | None,
    value: str,
    is_valid_return: Callable[[int], bool],
    evaluations: list[InputAnalysisResult],
) -> None:
    if ret == 0 and bool(results) and results_len.value > 0:
        evaluations.extend(
            InputAnalysisResult.from_ceval_result(
                UserInput(type=type, name=key, value=value), results[i]
            )
            for i in range(results_len.value)
        )

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            lib_contrast.free_eval_result,
            is_valid_return,
            results,
        )


def map_result_and_free_check_query_sink_result(
    ret: int,
    results: ctypes._Pointer[agent_lib.CCheckQuerySinkResult],
    user_input: str,
    input_index: int,
    input_len: int,
    is_valid_return: Callable[[int], bool],
) -> InjectionResult | None:
    if ret == 0 and bool(results):
        evaluation = InjectionResult(
            user_input, input_index, input_len, results.contents
        )

        # ctypes does not have OOR (original object return), it constructs a new,
        # equivalent object each time you retrieve an attribute.
        # So we can free right after we create our list
        agent_lib.call(
            lib_contrast.free_check_query_sink_result,
            is_valid_return,
            results,
        )

        return evaluation
    return None
