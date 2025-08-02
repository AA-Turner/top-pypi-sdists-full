import difflib
import json
import logging
import math
import sys
import unittest
from dataclasses import dataclass
from operator import itemgetter
from statistics import mean, median
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from humanfriendly import format_size
from requests import Response

from tinybird.datafile.common import normalize_array
from tinybird.tb.modules.common import getenv_bool

PIPE_CHECKER_RETRIES: int = 3


class PipeChecker(unittest.TestCase):
    RETRIES_LIMIT = PIPE_CHECKER_RETRIES

    current_response_time: float = 0
    checker_response_time: float = 0

    current_read_bytes: int = 0
    checker_read_bytes: int = 0

    def __init__(
        self,
        request: Dict[str, Any],
        pipe_name: str,
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        relative_change: float,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if request.get("http_method") == "POST":
            self.http_method = "POST"
            self.current_pipe_url, self.pipe_request_params = self._prepare_current_pipe_for_post_request(request)
        else:
            self.http_method = "GET"
            self.current_pipe_url, self.pipe_request_params = self._prepare_current_pipe_url_for_get_request(request)

        self._process_params()
        self.checker_pipe_name = checker_pipe_name
        self.pipe_name = pipe_name
        self.token = token
        self.only_response_times = only_response_times
        self.ignore_order = ignore_order
        self.validate_processed_bytes = validate_processed_bytes
        self.relative_change = relative_change

        parsed = urlparse(self.current_pipe_url)
        self.checker_pipe_url = f"{parsed.scheme}://{parsed.netloc}/v0/pipes/{self.checker_pipe_name}.json"
        self.checker_pipe_url += f"?{parsed.query}" if parsed.query is not None and parsed.query != "" else ""

    def _process_params(self) -> None:
        for key in self.pipe_request_params.keys():
            try:
                self.pipe_request_params[key] = json.loads(self.pipe_request_params[key])
            except Exception:
                pass

    def _prepare_current_pipe_url_for_get_request(self, request) -> Tuple[str, Dict[str, str]]:
        current_pipe_url = request.get("endpoint_url", "")
        current_pipe_url = (
            current_pipe_url.replace(".ndjson", ".json").replace(".csv", ".json").replace(".parquet", ".json")
        )
        current_pipe_url = drop_token(current_pipe_url)
        current_pipe_url += ("&" if "?" in current_pipe_url else "?") + "pipe_checker=true"
        return current_pipe_url, request.get("pipe_request_params", {})

    def _prepare_current_pipe_for_post_request(self, request) -> Tuple[str, Dict[str, str]]:
        current_pipe_url = request.get("endpoint_url", "")
        current_pipe_url = (
            current_pipe_url.replace(".ndjson", ".json").replace(".csv", ".json").replace(".parquet", ".json")
        )
        all_parameters = request.get("pipe_request_params")
        all_parameters.pop("token", None)
        all_parameters["pipe_checker"] = "true"

        return current_pipe_url, all_parameters

    def __str__(self):
        post_values = f" - POST Body: {self.pipe_request_params}" if self.http_method == "POST" else ""

        return f"current {self.current_pipe_url}{post_values}\n    new {self.checker_pipe_url}{post_values}"

    def diff(self, a: Dict[str, Any], b: Dict[str, Any]) -> str:
        a_properties = list(map(lambda x: f"{x}:{a[x]}\n", a.keys()))
        b_properties = list(map(lambda x: f"{x}:{b[x]}\n", b.keys()))

        return "".join(difflib.context_diff(a_properties, b_properties, self.pipe_name, self.checker_pipe_name))

    def _do_request_to_pipe(self, pipe_url: str) -> Response:
        headers = {"Authorization": f"Bearer {self.token}"}
        if self.http_method == "GET":
            return requests.get(pipe_url, headers=headers, verify=not getenv_bool("TB_DISABLE_SSL_CHECKS", False))
        else:
            return requests.post(
                pipe_url,
                headers=headers,
                verify=not getenv_bool("TB_DISABLE_SSL_CHECKS", False),
                data=self.pipe_request_params,
            )

    def _write_performance(self):
        return ""

    def _runTest(self) -> None:
        current_r = self._do_request_to_pipe(self.current_pipe_url)
        checker_r = self._do_request_to_pipe(self.checker_pipe_url)

        try:
            self.current_response_time = current_r.elapsed.total_seconds()
            self.checker_response_time = checker_r.elapsed.total_seconds()
        except Exception:
            pass

        current_response: Dict[str, Any] = current_r.json()
        checker_response: Dict[str, Any] = checker_r.json()

        current_data: List[Dict[str, Any]] = current_response.get("data", [])
        checker_data: List[Dict[str, Any]] = checker_response.get("data", [])

        self.current_read_bytes = current_response.get("statistics", {}).get("bytes_read", 0)
        self.checker_read_bytes = checker_response.get("statistics", {}).get("bytes_read", 0)

        error_check_fixtures_data: Optional[str] = checker_response.get("error", None)
        self.assertIsNone(
            error_check_fixtures_data,
            "You are trying to push a pipe with errors, please check the output or run with --no-check",
        )

        increase_response_time = (
            checker_r.elapsed.total_seconds() - current_r.elapsed.total_seconds()
        ) / current_r.elapsed.total_seconds()
        if self.only_response_times:
            self.assertLess(
                increase_response_time, 0.25, msg=f"response time has increased {round(increase_response_time * 100)}%"
            )
            return

        self.assertEqual(len(current_data), len(checker_data), "Number of elements does not match")

        if self.validate_processed_bytes:
            increase_read_bytes = (self.checker_read_bytes - self.current_read_bytes) / self.current_read_bytes
            self.assertLess(
                round(increase_read_bytes, 2),
                0.25,
                msg=f"The number of processed bytes has increased {round(increase_read_bytes * 100)}%",
            )

        if self.ignore_order:
            current_data = (
                sorted(normalize_array(current_data), key=itemgetter(*[k for k in current_data[0].keys()]))
                if len(current_data) > 0
                else current_data
            )
            checker_data = (
                sorted(normalize_array(checker_data), key=itemgetter(*[k for k in checker_data[0].keys()]))
                if len(checker_data) > 0
                else checker_data
            )

        for _, (current_data_e, check_fixtures_data_e) in enumerate(zip(current_data, checker_data)):
            self.assertEqual(list(current_data_e.keys()), list(check_fixtures_data_e.keys()))
            for x in current_data_e.keys():
                if isinstance(current_data_e[x], (float, int)):
                    d = abs(current_data_e[x] - check_fixtures_data_e[x])

                    try:
                        self.assertLessEqual(
                            d / current_data_e[x],
                            self.relative_change,
                            f"key {x}. old value: {current_data_e[x]}, new value: {check_fixtures_data_e[x]}\n{self.diff(current_data_e, check_fixtures_data_e)}",
                        )
                    except ZeroDivisionError:
                        self.assertEqual(
                            d,
                            0,
                            f"key {x}. old value: {current_data_e[x]}, new value: {check_fixtures_data_e[x]}\n{self.diff(current_data_e, check_fixtures_data_e)}",
                        )
                elif (
                    not isinstance(current_data_e[x], (str, bytes))
                    and isinstance(current_data_e[x], Iterable)
                    and self.ignore_order
                ):

                    def flatten(items):
                        """Yield items from any nested iterable; see Reference."""
                        output = []
                        for x in items:
                            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                                output.extend(flatten(x))
                            else:
                                output.append(x)
                        return output

                    self.assertEqual(
                        flatten(current_data_e[x]).sort(),
                        flatten(check_fixtures_data_e[x]).sort(),
                        "\n" + self.diff(current_data_e, check_fixtures_data_e),
                    )
                else:
                    self.assertEqual(
                        current_data_e[x],
                        check_fixtures_data_e[x],
                        "\n" + self.diff(current_data_e, check_fixtures_data_e),
                    )

    def runTest(self) -> None:
        if "debug" in self.pipe_request_params or (
            "from" in self.pipe_request_params and self.pipe_request_params["from"] == "ui"
        ):
            self.skipTest("found debug param")

        # Let's retry the validation to avoid false alerts when dealing with endpoints that have continuos ingestion
        retries = 0
        while retries < self.RETRIES_LIMIT:
            try:
                self._runTest()
            except AssertionError as e:
                retries += 1
                if retries >= self.RETRIES_LIMIT:
                    raise e
            else:
                break


@dataclass
class PipeCheckerRunnerResponse:
    pipe_name: str
    test_type: str
    output: str
    metrics_summary: Optional[Dict[str, Any]]
    metrics_timing: Dict[str, Tuple[float, float, float]]
    failed: List[Dict[str, str]]
    was_successfull: bool


class PipeCheckerRunner:
    checker_stream_result_class = unittest.runner._WritelnDecorator

    def __init__(self, pipe_name: str, host: str):
        self.pipe_name = pipe_name
        self.host = host

    def get_sqls_for_requests_to_check(
        self,
        matches: List[str],
        sample_by_params: int,
        limit: int,
        pipe_stats_rt_table: str = "",
        extra_where_clause: str = "",
    ):
        pipe_stats_rt = pipe_stats_rt_table or "tinybird.pipe_stats_rt"
        # TODO it may not be needed to extract token, pipe_checker, form or debug. They may be used in next steps
        # TODO extractURLParameter(assumeNotNull(url), 'from') <> 'ui' should read from request_param_names.
        sql_for_coverage = f"""
                    SELECT
                        groupArraySample({sample_by_params if sample_by_params > 0 else 1})(url) as endpoint_url,
                        groupArraySample({sample_by_params if sample_by_params > 0 else 1})(pipe_request_params) as pipe_request_params,
                        http_method
                    FROM
                        (
                        Select
                            url,
                            mapFilter((k, v) -> (k not IN ('token', 'pipe_checker', 'from', 'debug')), parameters) AS pipe_request_params,
                            mapKeys(pipe_request_params) request_param_names,
                            extractURLParameterNames(assumeNotNull(url)) as url_param_names,
                            method as http_method
                        FROM {pipe_stats_rt}
                        WHERE
                            pipe_name = '{self.pipe_name}'
                            AND url IS NOT NULL
                            AND extractURLParameter(assumeNotNull(url), 'from') <> 'ui'
                            AND extractURLParameter(assumeNotNull(url), 'pipe_checker') <> 'true'
                            AND extractURLParameter(assumeNotNull(url), 'debug') <> 'query'
                            AND error = 0
                            AND not mapContains(parameters, '__tb__semver')
                            {" AND " + " AND ".join([f"mapContains(pipe_request_params, '{match}')" for match in matches]) if matches and len(matches) > 0 else ""}
                            {extra_where_clause}
                        Limit 5000000 -- Enough to bring data while not processing all requests from highly used pipes
                        )
                    group by request_param_names, http_method
                    FORMAT JSON
                    """
        sql_latest_requests = f"""
                                SELECT
                                    [first_value(url)] as endpoint_url,
                                    [pipe_request_params] as pipe_request_params,
                                    http_method
                                FROM (
                                    SELECT assumeNotNull(url) as url,
                                        mapFilter((k, v) -> (k not IN ('token', 'pipe_checker', 'from', 'debug')), parameters) AS pipe_request_params,
                                        mapKeys(pipe_request_params) request_param_names,
                                        extractURLParameterNames(assumeNotNull(url)) as url_param_names,
                                        method as http_method
                                    FROM {pipe_stats_rt}
                                    WHERE
                                        pipe_name = '{self.pipe_name}'
                                        AND url IS NOT NULL
                                        AND extractURLParameter(assumeNotNull(url), 'from') <> 'ui'
                                        AND extractURLParameter(assumeNotNull(url), 'pipe_checker') <> 'true'
                                        AND extractURLParameter(assumeNotNull(url), 'debug') <> 'query'
                                        AND error = 0
                                        AND not mapContains(parameters, '__tb__semver')
                                        {" AND " + " AND ".join([f"mapContains(pipe_request_params, '{match}')" for match in matches]) if matches and len(matches) > 0 else ""}
                                        {extra_where_clause}
                                    LIMIT {limit}
                                )
                                GROUP BY pipe_request_params, http_method
                                FORMAT JSON
                            """
        return sql_for_coverage, sql_latest_requests

    def _get_checker(
        self,
        request: Dict[str, Any],
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        relative_change: float,
    ) -> PipeChecker:
        return PipeChecker(
            request,
            self.pipe_name,
            checker_pipe_name,
            token,
            only_response_times,
            ignore_order,
            validate_processed_bytes,
            relative_change,
        )

    def _delta_percentage(self, checker: float, current: float) -> float:
        try:
            if current == 0.0:
                return 0.0
            return round(((checker - current) / current) * 100, 2)
        except Exception as exc:
            logging.warning(f"Error calculating delta: {exc}")
            return 0.0

    def run_pipe_checker(
        self,
        pipe_requests_to_check: List[Dict[str, Any]],
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        relative_change: float,
        failfast: bool,
        custom_output: bool = False,
        debug: bool = False,
    ) -> PipeCheckerRunnerResponse:
        class PipeCheckerTextTestResult(unittest.TextTestResult):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                self.custom_output = kwargs.pop("custom_output", False)
                super().__init__(*args, **kwargs)
                self.success: List[PipeChecker] = []

            def addSuccess(self, test: PipeChecker):  # type: ignore
                super().addSuccess(test)
                self.success.append(test)

            def startTest(self, test):
                if not self.custom_output:
                    super().startTest(test)
                else:
                    super(unittest.TextTestResult, self).startTest(test)

            def _write_status(self, test, status):
                if self.custom_output:
                    self.stream.write(status.upper())
                    self.stream.write(" - ")
                    self.stream.write(str(test))
                    self.stream.write(" - ")
                    self.stream.writeln(test._write_performance())

                else:
                    self.stream.writeln(status)
                self.stream.flush()
                self._newline = True

        suite = unittest.TestSuite()

        for _, request in enumerate(pipe_requests_to_check):
            suite.addTest(
                self._get_checker(
                    request,
                    checker_pipe_name,
                    token,
                    only_response_times,
                    ignore_order,
                    validate_processed_bytes,
                    relative_change,
                )
            )

        result = PipeCheckerTextTestResult(
            self.checker_stream_result_class(sys.stdout),
            descriptions=True,
            verbosity=2,
            custom_output=custom_output,
        )
        result.failfast = failfast
        suite.run(result)

        metrics_summary: Optional[Dict[str, Any]] = None
        metrics_timing: Dict[str, Tuple[float, float, float]] = {}

        try:
            current_response_times: List[float] = []
            checker_response_times: List[float] = []

            current_read_bytes: List[int] = []
            checker_read_bytes: List[int] = []
            if result.success:
                for test in result.success:
                    current_response_times.append(test.current_response_time)
                    checker_response_times.append(test.checker_response_time)

                    current_read_bytes.append(test.current_read_bytes)
                    checker_read_bytes.append(test.checker_read_bytes)

                for test, _ in result.failures:  # type: ignore
                    current_response_times.append(test.current_response_time)
                    checker_response_times.append(test.checker_response_time)

                    current_read_bytes.append(test.current_read_bytes)
                    checker_read_bytes.append(test.checker_read_bytes)
            else:
                # if we do not have any successful execution, let's just return a table with dummy metrics https://gitlab.com/tinybird/analytics/-/issues/10875
                current_response_times = [0]
                checker_response_times = [0]

                current_read_bytes = [0]
                checker_read_bytes = [0]

            metrics_summary = {
                "run": result.testsRun,
                "passed": len(result.success),
                "failed": len(result.failures),
                "percentage_passed": len(result.success) * 100 / result.testsRun,
                "percentage_failed": len(result.failures) * 100 / result.testsRun,
            }
            metrics_timing = {
                "min response time": (
                    min(current_response_times),
                    min(checker_response_times),
                    self._delta_percentage(min(checker_response_times), min(current_response_times)),
                ),
                "max response time": (
                    max(current_response_times),
                    max(checker_response_times),
                    self._delta_percentage(max(checker_response_times), max(current_response_times)),
                ),
                "mean response time": (
                    float(format(mean(current_response_times), ".6f")),
                    float(format(mean(checker_response_times), ".6f")),
                    self._delta_percentage(
                        float(format(mean(checker_response_times), ".6f")),
                        float(format(mean(current_response_times), ".6f")),
                    ),
                ),
                "median response time": (
                    median(current_response_times),
                    median(checker_response_times),
                    self._delta_percentage(median(checker_response_times), median(current_response_times)),
                ),
                "p90 response time": (
                    sorted(current_response_times)[math.ceil(len(current_response_times) * 0.9) - 1],
                    sorted(checker_response_times)[math.ceil(len(checker_response_times) * 0.9) - 1],
                    self._delta_percentage(
                        sorted(checker_response_times)[math.ceil(len(checker_response_times) * 0.9) - 1],
                        sorted(current_response_times)[math.ceil(len(current_response_times) * 0.9) - 1],
                    ),
                ),
                "min read bytes": (
                    format_size(min(current_read_bytes)),
                    format_size(min(checker_read_bytes)),
                    self._delta_percentage(min(checker_read_bytes), min(current_read_bytes)),
                ),
                "max read bytes": (
                    format_size(max(current_read_bytes)),
                    format_size(max(checker_read_bytes)),
                    self._delta_percentage(max(checker_read_bytes), max(current_read_bytes)),
                ),
                "mean read bytes": (
                    format_size(mean(current_read_bytes)),
                    format_size(mean(checker_read_bytes)),
                    self._delta_percentage(mean(checker_read_bytes), mean(current_read_bytes)),
                ),
                "median read bytes": (
                    format_size(median(current_read_bytes)),
                    format_size(median(checker_read_bytes)),
                    self._delta_percentage(median(checker_read_bytes), median(current_read_bytes)),
                ),
                "p90 read bytes": (
                    format_size(sorted(current_read_bytes)[math.ceil(len(current_read_bytes) * 0.9) - 1]),
                    format_size(sorted(checker_read_bytes)[math.ceil(len(checker_read_bytes) * 0.9) - 1]),
                    self._delta_percentage(
                        sorted(checker_read_bytes)[math.ceil(len(checker_read_bytes) * 0.9) - 1],
                        sorted(current_read_bytes)[math.ceil(len(current_read_bytes) * 0.9) - 1],
                    ),
                ),
            }
        except Exception as e:
            if debug:
                logging.exception(e)

        failures = []
        if not result.wasSuccessful():
            for _test, err in result.failures:
                try:
                    i = err.index("AssertionError") + len("AssertionError :")
                    failures.append({"name": str(_test), "error": err[i:]})
                except Exception as e:
                    if debug:
                        logging.exception(e)

        return PipeCheckerRunnerResponse(
            pipe_name=checker_pipe_name,
            test_type=getattr(self, "test_type", ""),
            output=getattr(result.stream, "_buffer", ""),
            metrics_summary=metrics_summary,
            metrics_timing=metrics_timing,
            failed=failures,
            was_successfull=result.wasSuccessful(),
        )


def drop_token(url: str) -> str:
    """
    drops token param from the url query string
    >>> drop_token('https://api.tinybird.co/v0/pipes/aaa.json?token=abcd&a=1')
    'https://api.tinybird.co/v0/pipes/aaa.json?a=1'
    >>> drop_token('https://api.tinybird.co/v0/pipes/aaa.json?a=1')
    'https://api.tinybird.co/v0/pipes/aaa.json?a=1'
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs_simplify = {k: v[0] for k, v in qs.items()}  # change several arguments to single one
    qs_simplify.pop("token", None)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(qs_simplify)}"
