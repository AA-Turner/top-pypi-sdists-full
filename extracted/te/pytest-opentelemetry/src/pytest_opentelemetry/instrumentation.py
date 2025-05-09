import os
from typing import Any, Dict, Iterator, Optional, Union

import pytest
from _pytest.config import Config
from _pytest.fixtures import FixtureDef, FixtureRequest, SubRequest
from _pytest.main import Session
from _pytest.nodes import Item, Node
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from opentelemetry import propagate, trace
from opentelemetry.context.context import Context
from opentelemetry.sdk.resources import OTELResourceDetector
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode
from opentelemetry_container_distro import (
    OpenTelemetryContainerConfigurator,
    OpenTelemetryContainerDistro,
)

from .resource import CodebaseResourceDetector

tracer = trace.get_tracer('pytest-opentelemetry')


class PerTestOpenTelemetryPlugin:
    """base logic for all otel pytest integration"""

    @property
    def item_parent(self) -> Union[str, None]:
        return self.trace_parent

    @classmethod
    def get_trace_parent(cls, config: Config) -> Optional[Context]:
        if trace_parent := config.getvalue('--trace-parent'):
            return propagate.extract({'traceparent': trace_parent})

        if trace_parent := os.environ.get('TRACEPARENT'):
            return propagate.extract({'traceparent': trace_parent})

        return None

    @classmethod
    def try_force_flush(cls) -> bool:
        provider = trace.get_tracer_provider()

        # Not all providers (e.g. ProxyTraceProvider) implement force flush
        if hasattr(provider, 'force_flush'):
            provider.force_flush()
            return True
        else:
            return False

    def pytest_configure(self, config: Config) -> None:
        self.trace_parent = self.get_trace_parent(config)

        # This can't be tested both ways in one process
        if config.getoption('--export-traces'):  # pragma: no cover
            OpenTelemetryContainerDistro().configure()

        configurator = OpenTelemetryContainerConfigurator()
        configurator.resource_detectors.append(CodebaseResourceDetector(config))
        configurator.resource_detectors.append(OTELResourceDetector())
        configurator.configure()

    def pytest_sessionfinish(self, session: Session) -> None:
        self.try_force_flush()

    def _attributes_from_item(self, item: Item) -> Dict[str, Union[str, int]]:
        filepath, line_number, _ = item.location
        attributes: Dict[str, Union[str, int]] = {
            SpanAttributes.CODE_FILEPATH: filepath,
            SpanAttributes.CODE_FUNCTION: item.name,
            "pytest.nodeid": item.nodeid,
            "pytest.span_type": "test",
        }
        # In some cases like tavern, line_number can be 0
        if line_number:
            attributes[SpanAttributes.CODE_LINENO] = line_number
        return attributes

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item: Item) -> Iterator[None]:
        with tracer.start_as_current_span(
            item.nodeid,
            attributes=self._attributes_from_item(item),
            context=self.item_parent,
        ):
            yield

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_setup(self, item: Item) -> Iterator[None]:
        with tracer.start_as_current_span(
            f'{item.nodeid}::setup',
            attributes=self._attributes_from_item(item),
        ):
            yield

    def _attributes_from_fixturedef(
        self, fixturedef: FixtureDef
    ) -> Dict[str, Union[str, int]]:
        return {
            SpanAttributes.CODE_FILEPATH: fixturedef.func.__code__.co_filename,
            SpanAttributes.CODE_FUNCTION: fixturedef.argname,
            SpanAttributes.CODE_LINENO: fixturedef.func.__code__.co_firstlineno,
            "pytest.fixture_scope": fixturedef.scope,
            "pytest.span_type": "fixture",
        }

    def _name_from_fixturedef(self, fixturedef: FixtureDef, request: FixtureRequest):
        if fixturedef.params and 'request' in fixturedef.argnames:
            try:
                parameter = str(request.param)
            except Exception:
                parameter = str(
                    request.param_index if isinstance(request, SubRequest) else '?'
                )
            return f"{fixturedef.argname}[{parameter}]"
        return fixturedef.argname

    @pytest.hookimpl(hookwrapper=True)
    def pytest_fixture_setup(
        self, fixturedef: FixtureDef, request: FixtureRequest
    ) -> Iterator[None]:
        with tracer.start_as_current_span(
            name=f'{self._name_from_fixturedef(fixturedef, request)} setup',
            attributes=self._attributes_from_fixturedef(fixturedef),
        ):
            yield

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item: Item) -> Iterator[None]:
        with tracer.start_as_current_span(
            name=f'{item.nodeid}::call',
            attributes=self._attributes_from_item(item),
        ):
            yield

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_teardown(self, item: Item) -> Iterator[None]:
        with tracer.start_as_current_span(
            name=f'{item.nodeid}::teardown',
            attributes=self._attributes_from_item(item),
        ):
            # Since there is no pytest_fixture_teardown hook, we have to be a
            # little clever to capture the spans for each fixture's teardown.
            # The pytest_fixture_post_finalizer hook is called at the end of a
            # fixture's teardown, but we don't know when the fixture actually
            # began tearing down.
            #
            # Instead start a span here for the first fixture to be torn down,
            # but give it a temporary name, since we don't know which fixture it
            # will be. Then, in pytest_fixture_post_finalizer, when we do know
            # which fixture is being torn down, update the name and attributes
            # to the actual fixture, end the span, and create the span for the
            # next fixture in line to be torn down.
            self._fixture_teardown_span = tracer.start_span("fixture teardown")
            yield

        # The last call to pytest_fixture_post_finalizer will create
        # a span that is unneeded, so delete it.
        del self._fixture_teardown_span

    @pytest.hookimpl(hookwrapper=True)
    def pytest_fixture_post_finalizer(
        self, fixturedef: FixtureDef, request: SubRequest
    ) -> Iterator[None]:
        """When the span for a fixture teardown is created by
        pytest_runtest_teardown or a previous pytest_fixture_post_finalizer, we
        need to update the name and attributes now that we know which fixture it
        was for."""

        # If the fixture has already been torn down, then it will have no cached
        # result, so we can skip this one.
        if fixturedef.cached_result is None:
            yield
        # Passing `-x` option to pytest can cause it to exit early so it may not
        # have this span attribute.
        elif not hasattr(self, "_fixture_teardown_span"):  # pragma: no cover
            yield
        else:
            # If we've gotten here, we have a real fixture about to be torn down.
            name = f'{self._name_from_fixturedef(fixturedef, request)} teardown'
            self._fixture_teardown_span.update_name(name)
            attributes = self._attributes_from_fixturedef(fixturedef)
            self._fixture_teardown_span.set_attributes(attributes)
            yield
            self._fixture_teardown_span.end()

        # Create the span for the next fixture to be torn down. When there are
        # no more fixtures remaining, this will be an empty, useless span, so it
        # needs to be deleted by pytest_runtest_teardown.
        self._fixture_teardown_span = tracer.start_span("fixture teardown")

    @staticmethod
    def pytest_exception_interact(
        node: Node,
        call: CallInfo[Any],
        report: TestReport,
    ) -> None:
        excinfo = call.excinfo
        assert excinfo
        assert isinstance(excinfo.value, BaseException)

        test_span = trace.get_current_span()

        test_span.record_exception(
            # Interface says Exception, but BaseException seems to work fine
            # This is needed because pytest's Failed exception inherits from
            # BaseException, not Exception
            exception=excinfo.value,  # type: ignore[arg-type]
            attributes={
                SpanAttributes.EXCEPTION_STACKTRACE: str(report.longrepr),
            },
        )
        test_span.set_status(
            Status(
                status_code=StatusCode.ERROR,
                description=f"{excinfo.type}: {excinfo.value}",
            )
        )

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        if report.when != 'call':
            return

        has_error = report.outcome == 'failed'
        status_code = StatusCode.ERROR if has_error else StatusCode.OK
        trace.get_current_span().set_status(status_code)


class OpenTelemetryPlugin(PerTestOpenTelemetryPlugin):
    """A pytest plugin which produces OpenTelemetry spans around test sessions and
    individual test runs."""

    @property
    def session_name(self):
        # Lazy initialise session name
        if not hasattr(self, '_session_name'):
            self._session_name = os.environ.get('PYTEST_RUN_NAME', 'test run')
        return self._session_name

    @session_name.setter
    def session_name(self, name):
        self._session_name = name

    @property
    def item_parent(self) -> Union[str, None]:
        context = trace.set_span_in_context(self.session_span)
        return context

    def pytest_sessionstart(self, session: Session) -> None:
        self.session_span = tracer.start_span(
            self.session_name,
            context=self.trace_parent,
            attributes={
                "pytest.span_type": "run",
            },
        )
        self.has_error = False

    def pytest_sessionfinish(self, session: Session) -> None:
        self.session_span.set_status(
            StatusCode.ERROR if self.has_error else StatusCode.OK
        )

        self.session_span.end()
        super().pytest_sessionfinish(session)

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        super().pytest_runtest_logreport(report)
        self.has_error |= report.when == 'call' and report.outcome == 'failed'


try:
    from xdist.workermanage import WorkerController  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    WorkerController = None


class XdistOpenTelemetryPlugin(OpenTelemetryPlugin):
    """An xdist-aware version of the OpenTelemetryPlugin"""

    @classmethod
    def get_trace_parent(cls, config: Config) -> Optional[Context]:
        if workerinput := getattr(config, 'workerinput', None):
            return propagate.extract(workerinput)

        return super().get_trace_parent(config)

    def pytest_configure(self, config: Config) -> None:
        super().pytest_configure(config)
        worker_id = getattr(config, 'workerinput', {}).get('workerid')
        self.session_name = (
            f'test worker {worker_id}' if worker_id else self.session_name
        )

    def pytest_configure_node(self, node: WorkerController) -> None:  # pragma: no cover
        with trace.use_span(self.session_span, end_on_exit=False):
            propagate.inject(node.workerinput)

    def pytest_xdist_node_collection_finished(node, ids):  # pragma: no cover
        super().try_force_flush()
