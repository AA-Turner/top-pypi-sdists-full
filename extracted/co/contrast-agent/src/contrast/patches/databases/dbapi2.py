# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements a single API for instrumenting all dbapi2-compliant modules
"""

from contextlib import contextmanager
from contrast_fireball import AppActivityComponentType, ArchitectureComponent, SpanType
import contrast
from contrast.agent import scope
from contrast.applies.sqli import apply_rule
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    pack_self,
    wrap_and_watermark,
)
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")


VENDOR_TO_DB_SYSTEM = {
    "MySQL": "mysql",
    "PostgreSQL": "postgresql",
    "SQLite3": "sqlite",
}


class Dbapi2Patcher:
    """
    Do not instantiate this class; call `instrument_adapter` or subclass it.

    This class provides machinery to instrument a totally generic, PEP-249 compliant
    adapter. We only have a reference to the adapter module, and we can't make any
    assumptions about the existence of `adapter.Cursor`, since this is not guaranteed
    by the spec.

    We are only guaranteed the following:
    - the adapter has a `connection()` method, which returns an instance of Connection
    - the Connection object has a `cursor()` method, which returns an instance of Cursor
    - the Cursor has `execute()` and `executemany()` methods

    This requires a somewhat roundabout instrumentation strategy:
    - on the first call to adapter.connect(), we can instrument the Connection class
    - on the first call to Connection.cursor(), we can instrument the Cursor class
    - this lets us instrument Cursor.execute() and Cursor.executemany()
    """

    def __init__(self, adapter, vendor: str):
        self.vendor: str = vendor
        self.system: str = VENDOR_TO_DB_SYSTEM.get(vendor, "")
        self.db_name: str = ""
        self.user: str = ""
        self.host: str = ""
        self.port: str = ""

        self._adapter = adapter
        # this module name must match a policy node; we need to fake sqlalchemy
        self._adapter_name = (
            "sqlalchemy" if self.vendor == "sqlalchemy" else self._adapter.__name__
        )
        self._connect_called = False
        self._cursor_called = False

    @fail_quietly("failed to instrument database adapter")
    def instrument(self, extra_cursors):
        build_and_apply_patch(self._adapter, "connect", self._build_connect_patch)
        for cursor in extra_cursors:
            self._safe_instrument_cursor(cursor)

    @fail_quietly()
    def extract_connection_attributes(self, connection, connect_args, connect_kwargs):
        """
        This method is intended to be overridden by subclasses if necessary. It must
        either assign `self.db_name` or do nothing if the database name cannot be
        determined. "database name" is different depending on the adapter. Often this is
        a URL, but it can also be a path (sqlite3).

        Takes the arguments from a call to connect() and extracts information for
        database inventory reporting. By default only works with kwargs - we expect this
        to be by far the most common case.

        This follows the conventions laid out in the footnotes of dbapi2:
        https://peps.python.org/pep-0249/#id48

        In SQLAlchemy, see create_connect_args() for each dialect to get an idea of how
        different adapters are used. Most, if not all, use kwargs. Some adapters support
        a DSN connection string, but that should be handled by subclasses (if at all).
        """
        if not self.db_name:
            # the database name argument has several variations
            for key in ["database", "dbname", "db"]:
                if key in connect_kwargs:
                    self.db_name = str(connect_kwargs[key])
                    break
        self.user = self.user or connect_kwargs.get("user", "")
        self.host = self.host or connect_kwargs.get("host", "")
        self.port = self.port or connect_kwargs.get("port", "")

    @fail_quietly("failed to instrument database cursor class")
    def _safe_instrument_cursor(self, cursor_class):
        """
        Instruments a dbapi2-compliant database cursor class

        @param cursor_class: Reference to cursor class to be instrumented
        """
        self._instrument_cursor_method(cursor_class, "execute")
        self._instrument_cursor_method(cursor_class, "executemany")
        if hasattr(cursor_class, "executescript"):
            # non-standard, but provided by some adapters such as sqlite3
            self._instrument_cursor_method(cursor_class, "executescript")

    def _instrument_cursor_method(self, cursor, method_name):
        build_and_apply_patch(
            cursor,
            method_name,
            self._build_execute_patch,
        )

    @fail_quietly("failed to instrument database connection object")
    def _safe_instrument_connection(self, connection_instance):
        """
        Instruments a dbapi2-compliant database connection class, given an instance

        @param connection_instance: dbapi2 Connection instance
        """
        connection_class = type(connection_instance)
        build_and_apply_patch(connection_class, "cursor", self._build_cursor_patch)

    @contextmanager
    def _storage_query_span(self):
        context = contrast.REQUEST_CONTEXT.get()
        if context is None or not context.observe_enabled or scope.in_observe_scope():
            yield
            return

        with scope.observe_scope():
            if (trace := context.observability_trace) is None:
                yield
                return

            with trace.child_span(SpanType.StorageQuery) as span:
                logger.debug(
                    "entered new child span",
                    child_span=span,
                    action_type=SpanType.StorageQuery,
                )
                try:
                    yield
                finally:
                    if span:
                        db_attrs = {
                            "db.system": self.system,
                            "db.user": self.user,
                            "db.name": self.db_name,
                            "server.address": self.host,
                            "server.port": self.port,
                        }
                        db_attrs = {
                            name: value for name, value in db_attrs.items() if value
                        }
                        span.update(db_attrs)
                        logger.debug(
                            "updated child_span attributes",
                            child_span=span,
                            action_attrs=db_attrs,
                        )

    @property
    def _build_execute_patch(self):
        """
        See `_build_connect_patch`
        """

        def build_execute_patch(orig_func, _):
            def patched_method(wrapper, instance, args, kwargs):
                """
                Patch for dbapi_adapter.connection().cursor().execute*()
                """
                with self._storage_query_span():
                    return apply_rule(
                        self._adapter_name,
                        wrapper,
                        pack_self(instance, args),
                        kwargs,
                    )

            return wrap_and_watermark(orig_func, patched_method)

        return build_execute_patch

    @property
    def _build_cursor_patch(self):
        """
        See `_build_connect_patch`
        """

        def build_cursor_patch(orig_func, _):
            def cursor_patch(wrapped, instance, args, kwargs):
                """
                Patch for dbapi_adapter.connection().cursor()

                This patch will ensure that the returned Cursor object's class will have
                `execute` and `executemany` instrumented.
                """
                del instance

                cursor = wrapped(*args, **kwargs)
                if not self._cursor_called:
                    try:
                        cursor_class = type(cursor)
                        self._safe_instrument_cursor(cursor_class)
                        self._cursor_called = True
                    except Exception:
                        pass
                return cursor

            return wrap_and_watermark(orig_func, cursor_patch)

        return build_cursor_patch

    @property
    def _build_connect_patch(self):
        """
        Getter for `build_connect_patch`. We can't just make `build_connect_patch` an
        instance method because of the added `self` argument.
        """

        def build_connect_patch(orig_func, _):
            def connect_patch(wrapped, instance, args, kwargs):
                """
                Patch for dbapi_adapter.connection()

                This patch will ensure that the returned Connection object's class will
                have `cursor_patch` applied to its cursor() method.
                """
                del instance

                connection = wrapped(*args, **kwargs)
                if not self._connect_called:
                    self.extract_connection_attributes(connection, args, kwargs)
                    self._safe_instrument_connection(connection)
                    self._connect_called = True
                self._safe_send_architecture_component()
                return connection

            return wrap_and_watermark(orig_func, connect_patch)

        return build_connect_patch

    @fail_quietly()
    def _safe_send_architecture_component(self):
        """
        Report the current database information as an inventory component
        """
        from contrast.agent import agent_state

        if not (reporting_client := agent_state.module.reporting_client):
            return

        component = ArchitectureComponent(
            type=AppActivityComponentType.DB,
            url=(self.db_name or self.vendor or "default"),
            vendor=self.vendor,
        )
        reporting_client.new_inventory_components([component])


@fail_quietly("failed to instrument database adapter")
def instrument_adapter(adapter, vendor, patcher_cls=Dbapi2Patcher, extra_cursors=None):
    """
    Instrument the provided dbapi2 adapter.

    `vendor` must be a string that exactly matches a value from Teamserver's
    flowmap/technologies.json > service > one of "name".

    References to cursors to instrument explicitly can be passed in via extra_cursors.
    If we could guarantee patches were applied before any calls to `adapter.connect()`,
    we wouldn't need to directly patch extra cursors - unfortunately, this probably
    means we'd need to be a runner.
    """
    patcher_cls(adapter, vendor).instrument(extra_cursors or [])
