"""Thin Workday component — flow orchestrator (TASK-105 / FEAT-026).

``Workday(FlowComponent)`` no longer inherits ``SOAPClient``.  All SOAP
operational logic was moved to ``WorkdayService`` in FEAT-026.  This class
keeps only the flow concerns:

- YAML-attribute binding (self.type, self.worker_id, date params, …)
- Mask substitution on ``start_date``, ``end_date``, ``storage_path``.
- CSV storage cache: hit returns immediately without touching the service.
- Lifecycle: ``start()`` → ``service.start()``; ``close()`` → ``service.close()``.
- ``run()``: build params from component attrs → ``service.fetch()`` → DataFrame
  → write CSV → record metrics.
- ``add_metric`` / metrics dict (used by the flow engine).
"""

import logging
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

from flowtask.interfaces.flow import FlowComponent
from flowtask.interfaces.workday.config import WorkdayConfig
from flowtask.interfaces.workday.service import WorkdayService

# FEAT-027: write-op model imports (used inside run() for validation)
_WRITE_TYPES = frozenset(
    {"put_time_clock_events", "import_time_clock_events", "import_reported_time_blocks"}
)


class Workday(FlowComponent):
    """
    Workday Component — thin flow orchestrator.

    Overview:
        Composes ``WorkdayService`` and delegates all SOAP operational logic to
        it.  Keeps only flow concerns: mask substitution, CSV storage cache,
        ``add_metric``, and lifecycle coordination.

    YAML surface (unchanged from pre-refactor, G6):
        type                     Operation key (default: get_workers)
        worker_id / start_date / end_date / …
        use_storage / storage_path
        tenant / report_owner / workday_url / timeout
        report_username / report_password
        env                      Target environment (see below)
        zeep_debug

    Environment selection (prod vs sandbox) — FEAT-027:
        Which Workday tenant this component talks to is controlled by ``env``
        (or the ``WORKDAY_ENV`` setting), and defaults to PRODUCTION. You do NOT
        normally set this — leave it unset for prod.

        - unset / "prod" (default):
              credentials  → WORKDAY_CLIENT_ID / _SECRET / _TOKEN_URL / _REFRESH_TOKEN
              SOAP host     → workday_url (default services1.wd501 = production)
        - "sandbox" (or "impl"):
              credentials  → WORKDAY_CLIENT_ID_IMPL / _SECRET_IMPL / _TOKEN_URL_IMPL
                             / _REFRESH_TOKEN_IMPL
              SOAP host     → derived from the impl token_url (impl-services1.wd501),
                             so the call NEVER lands on production by accident.

        The shipped WSDLs hardcode the production SOAP endpoint;
        ``WorkdayService.bind_service`` rewrites the host to match the resolved
        environment. Credentials and host are always aligned — you cannot
        authenticate against sandbox and write to prod.

        Set it in YAML per-task::

            - Workday:
                type: put_time_clock_events
                env: sandbox          # omit for production

        or globally in the env file::

            WORKDAY_ENV=sandbox       # default is prod

        Workday hosts: UI=impl.wd501, login=impl-identity.wd501,
        API/SOAP=impl-services1.wd501.
    """

    _version = "1.0.0"

    def __init__(self, *, loop=None, job=None, stat=None, **kwargs):
        """Initialise attributes from YAML kwargs and compose WorkdayService."""

        # ---- Flow-concern attributes (YAML bindings) ----------------------
        self.type: str = kwargs.get("type", "get_workers")
        self.worker_id = kwargs.get("worker_id")
        self.start_date = kwargs.get("start_date")
        self.end_date = kwargs.get("end_date")

        # Storage parameters
        self.use_storage: bool = kwargs.get("use_storage", False)
        self.storage_path: str = kwargs.get("storage_path")
        if self.use_storage and not self.storage_path:
            raise ValueError(
                "Workday: storage_path is required when use_storage is True"
            )

        # Location parameters
        self.location_id = kwargs.get("location_id")
        self.location_name = kwargs.get("location_name")
        self.location_type = kwargs.get("location_type")
        self.location_usage = kwargs.get("location_usage")
        self.inactive = kwargs.get("inactive")

        # Time Request parameters
        self.time_request_id = kwargs.get("time_request_id")
        self.supervisory_organization_id = kwargs.get("supervisory_organization_id")

        # Organization parameters
        self.organization_id = kwargs.get("organization_id")
        self.organization_id_type = kwargs.get(
            "organization_id_type", "Organization_Reference_ID"
        )
        self.organization_type = kwargs.get("organization_type")
        self.include_inactive = kwargs.get("include_inactive")
        self.enable_transaction_log_lite = kwargs.get("enable_transaction_log_lite")

        # Cost center parameters
        self.cost_center_id = kwargs.get("cost_center_id")
        self.cost_center_id_type = kwargs.get(
            "cost_center_id_type", "Cost_Center_Reference_ID"
        )
        self.updated_from_date = kwargs.get("updated_from_date")
        self.updated_to_date = kwargs.get("updated_to_date")
        # FEAT-192: optional recursive Cost_Center_Hierarchy chain; organization
        # enrichment itself always runs (no opt-in flag) — this only controls
        # whether org_hierarchy_chain is also built. Defaults to None (not
        # forwarded) so the handler's own default (False) applies.
        self.include_hierarchy_chain = kwargs.get("include_hierarchy_chain")

        # Applicant parameters
        self.applicant_id = kwargs.get("applicant_id")
        self.job_requisition_id = kwargs.get("job_requisition_id")
        self.application_date_from = kwargs.get("application_date_from")
        self.application_date_to = kwargs.get("application_date_to")
        self.is_pre_hire = kwargs.get("is_pre_hire")

        # Candidate parameters
        self.candidate_id = kwargs.get("candidate_id")
        self.applied_from_date = kwargs.get("applied_from_date")
        self.applied_to_date = kwargs.get("applied_to_date")
        self.created_from_date = kwargs.get("created_from_date")
        self.created_to_date = kwargs.get("created_to_date")
        self.pdf_directory = kwargs.get("pdf_directory")
        self.exclude_all_attachments = kwargs.get("exclude_all_attachments", False)

        # Job Requisition parameters
        self.job_requisition_status = kwargs.get("job_requisition_status")

        # Job Posting parameters
        self.job_posting_id = kwargs.get("job_posting_id")
        self.job_posting_site_id = kwargs.get("job_posting_site_id")
        self.posting_status = kwargs.get("posting_status")
        self.posted_from_date = kwargs.get("posted_from_date")
        self.posted_to_date = kwargs.get("posted_to_date")

        # Job Posting Site parameters
        self.is_active = kwargs.get("is_active")

        # Time Block parameters
        self.time_block_id = kwargs.get("time_block_id")
        self.time_block_wid = kwargs.get("time_block_wid")
        self.status = kwargs.get("status")
        self.supervisory_org = kwargs.get("supervisory_org")
        self.include_deleted = kwargs.get("include_deleted")

        # Time Off Balance parameters
        self.time_off_plan_id = kwargs.get("time_off_plan_id")

        # Extract / Time Block Report parameters
        self.supervisory_organization = kwargs.get("supervisory_organization")
        self.worker = kwargs.get("worker")

        # Custom report parameters
        self.report_name = kwargs.get("report_name")

        # References (Integrations service) parameters
        self.reference_id_type = kwargs.get("reference_id_type")

        # FEAT-027: write-type parameters
        # events: list of dicts from YAML (fallback when no upstream DataFrame)
        self.events = kwargs.get("events", None)
        # auto_submit: optional service-level override for all clock events
        self.auto_submit = kwargs.get("auto_submit", None)
        # batch_id: optional batch identifier for import operations
        self.batch_id = kwargs.get("batch_id", None)

        # Debug parameters
        self.zeep_debug = kwargs.get("zeep_debug", False)
        _zeep_loggers = ("zeep", "zeep.transports", "zeep.wsdl", "httpx", "httpcore")
        if self.zeep_debug:
            for _name in _zeep_loggers:
                logging.getLogger(_name).setLevel(logging.DEBUG)
        else:
            # Authoritative OFF (parity with main: `getLogger("zeep").setLevel(INFO)`):
            # pin these loggers to INFO so the raw zeep request/response XML stays
            # silent even when the app runs with --debug. The FEAT-026 refactor
            # dropped this `else`, so the toggle only ever turned debug ON and zeep
            # output leaked under a DEBUG root logger. We reset all five (not just
            # `zeep`) in case a prior zeep_debug=True run pinned a child to DEBUG.
            for _name in _zeep_loggers:
                logging.getLogger(_name).setLevel(logging.INFO)

        # ---- Initialise FlowComponent (handles masks, job/loop/stat) -------
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

        # ---- Logger and metrics --------------------------------------------
        self._logger = logging.getLogger("flowtask.workday")
        self.metrics: dict = {}
        self._result = None

        # ---- Compose WorkdayService ----------------------------------------
        config = WorkdayConfig(
            client_id=kwargs.get("client_id"),
            client_secret=kwargs.get("client_secret"),
            token_url=kwargs.get("token_url"),
            refresh_token=kwargs.get("refresh_token"),
            report_username=kwargs.get("report_username"),
            report_password=kwargs.get("report_password"),
            tenant=kwargs.get("tenant", "troc"),
            report_owner=kwargs.get("report_owner", "jtorres@trocglobal.com"),
            workday_url=kwargs.get(
                "workday_url", "https://services1.wd501.myworkday.com"
            ),
            timeout=int(kwargs.get("timeout", 300)),
            # Environment selector (FEAT-027): None → WORKDAY_ENV (default "prod").
            # "sandbox"/"impl" makes WorkdayConfig resolve the WORKDAY_*_IMPL
            # credentials and point the SOAP host at the impl tenant.
            env=kwargs.get("env"),
        )
        self.service: WorkdayService = WorkdayService(
            config=config,
            operation_type=self.type,
        )

        if self.use_storage:
            self._logger.info("Storage enabled. Data will be saved in: %s", self.storage_path)

    # -----------------------------------------------------------------------
    # Flow concerns
    # -----------------------------------------------------------------------

    def _get_storage_file(self) -> str:
        """Return the CSV cache path for the current execution date + type."""
        today = datetime.now().strftime("%Y%m%d")
        filename = f"workday_{self.type}_{today}.csv"
        storage_dir = Path(self.storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)
        return str(storage_dir / filename)

    def add_metric(self, key: str, value) -> None:
        """Record a flow metric (e.g. row count)."""
        self.metrics[key] = value

    # -----------------------------------------------------------------------
    # FEAT-027: write-operation helper
    # -----------------------------------------------------------------------

    async def _run_write_operation(self) -> pd.DataFrame:
        """Marshal input events, validate, delegate to service, merge status cols.

        Input sources (in priority order):
          1. Upstream DataFrame (``self.data``) — one row per event.
          2. YAML ``events`` list (``self.events``) — list of dicts.

        Validation: every row/dict is validated to ClockEvent or ReportedTimeBlock
        BEFORE any SOAP call (G7). Invalid rows raise a ValueError immediately.

        Returns:
            Input rows annotated with ``submitted``, ``event_id``, ``error`` columns.
        """
        from flowtask.interfaces.workday.models.clock_event import (
            ClockEvent,
            ReportedTimeBlock,
        )
        from pydantic import ValidationError

        is_reported_blocks = self.type == "import_reported_time_blocks"

        # 1. Collect raw records
        input_df: pd.DataFrame | None = None

        if self.previous is not None:
            # Primary: upstream DataFrame
            self.data = self.input
            if isinstance(self.data, pd.DataFrame) and not self.data.empty:
                input_df = self.data.reset_index(drop=True)
                raw_records = input_df.to_dict("records")
            else:
                raw_records = []
        elif self.events:
            # Fallback: YAML events list
            raw_records = list(self.events)
            input_df = pd.DataFrame(raw_records)
        else:
            raise ValueError(
                "Workday write operation requires either an upstream DataFrame "
                "or a YAML 'events' list."
            )

        if not raw_records:
            raise ValueError(
                f"No events to submit for operation '{self.type}'."
            )

        # 2. Validate to model list (G7 — fail fast, before any SOAP call)
        model_list = []
        for idx, record in enumerate(raw_records):
            # Drop NaN/None values so optional fields aren't forced to None strings
            clean = {k: v for k, v in record.items() if v is not None and v == v}
            try:
                if is_reported_blocks:
                    model_list.append(ReportedTimeBlock(**clean))
                else:
                    model_list.append(ClockEvent(**clean))
            except ValidationError as exc:
                raise ValueError(
                    f"Invalid event at row {idx} for operation '{self.type}': {exc}"
                ) from exc

        # 3. Delegate to service method
        self._logger.info(
            "Workday write operation '%s' — submitting %d event(s).",
            self.type,
            len(model_list),
        )

        if self.type == "put_time_clock_events":
            status_df = await self.service.put_time_clock_events(
                model_list,
                auto_submit=self.auto_submit,
            )
        elif self.type == "import_time_clock_events":
            status_df = await self.service.import_time_clock_events(
                model_list,
                batch_id=self.batch_id,
            )
        else:  # import_reported_time_blocks
            status_df = await self.service.import_reported_time_blocks(model_list)

        # 4. Merge status columns back onto the input rows
        if input_df is not None and not input_df.empty:
            result = input_df.copy()
            for col in ("submitted", "event_id", "error"):
                if col in status_df.columns:
                    result[col] = status_df[col].values
        else:
            result = status_df

        # 5. Storage (reuse existing branch)
        if self.use_storage and isinstance(result, pd.DataFrame):
            try:
                storage_file = self._get_storage_file()
                result.to_csv(storage_file, index=False)
                self._logger.info("Write results saved to: %s", storage_file)
            except Exception as exc:
                self._logger.error("Error saving write results to storage: %s", exc)

        # 6. Metrics
        if isinstance(result, pd.DataFrame):
            self.add_metric("NUMROWS", len(result.index))
            self.add_metric("NUMCOLS", len(result.columns))

        return result

    # -----------------------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------------------

    async def start(self, **_kwargs) -> None:
        """Apply masks then start the composed WorkdayService."""
        await super().start()

        # Mask substitution for date/path parameters
        if hasattr(self, "_mask") and self._mask:
            self._logger.info("Processing masks: %s", list(self._mask.keys()))

            for attr in ("start_date", "end_date", "updated_from_date", "updated_to_date"):
                val = getattr(self, attr, None)
                if val:
                    resolved = self.mask_replacement(val)
                    if resolved != val:
                        self._logger.info(
                            "Processed %s with masks: %s -> %s", attr, val, resolved
                        )
                    setattr(self, attr, resolved)

            if getattr(self, "storage_path", None):
                resolved = self.mask_replacement(self.storage_path)
                if resolved != self.storage_path:
                    self._logger.info(
                        "Processed storage_path with masks: %s -> %s",
                        self.storage_path, resolved,
                    )
                self.storage_path = resolved

        await self.service.start()

    async def run(self, operation: str = None, **kwargs):
        """Flow-level entry point.

        1. If a raw ``operation`` string is provided, delegate directly to
           ``service.call_operation`` (preserves the dual-mode contract).
        2. Check CSV storage cache; return cached DataFrame on hit.
        3. Build params from component attributes (YAML bindings).
        4. Delegate to ``service.fetch(self.type, **params)``.
        5. Save DataFrame to CSV cache if enabled.
        6. Record metrics.
        """
        # Dual-mode: raw SOAP passthrough (preserves workday.py:581-583)
        if operation:
            return await self.service.call_operation(operation=operation, **kwargs)

        # CSV cache check (must NOT touch the service on hit)
        if self.use_storage:
            storage_file = self._get_storage_file()
            if os.path.exists(storage_file):
                self._logger.info(
                    "Found existing data file: %s. Using stored data.", storage_file
                )
                try:
                    self._result = pd.read_csv(storage_file)
                    return self._result
                except Exception as exc:
                    self._logger.error("Error loading storage file: %s", exc)
            else:
                self._logger.info(
                    "No existing data file found. Will generate new file: %s",
                    storage_file,
                )

        self._logger.info("Starting Workday operation: %s", self.type)

        # ---- Build params from YAML-bound component attributes -------------
        params: dict = dict(kwargs)

        if self.worker_id:
            params["worker_id"] = self.worker_id

        if hasattr(self, "document_directory") and self.document_directory:
            params["document_directory"] = self.document_directory

        if self.type == "get_workers":
            if self.start_date:
                from datetime import timezone, timedelta
                updated_through = self.end_date or (
                    datetime.now(timezone.utc) - timedelta(minutes=5)
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
                self._logger.info(
                    "📅 Incremental load: Updated_From=%s, Updated_Through=%s",
                    self.start_date, updated_through,
                )
                # Inject directly into handler's request_payload
                handler = self.service._type_handlers.get("get_workers")
                if handler:
                    handler.request_payload["Request_Criteria"][
                        "Transaction_Log_Criteria_Data"
                    ] = [
                        {
                            "Transaction_Date_Range_Data": {
                                "Updated_From": self.start_date,
                                "Updated_Through": updated_through,
                            }
                        }
                    ]
        else:
            if self.start_date:
                params["start_date"] = self.start_date
            if self.end_date:
                params["end_date"] = self.end_date

        if self.type == "get_time_blocks":
            for attr in ("time_block_id", "time_block_wid", "status",
                         "supervisory_org", "include_deleted"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_locations":
            for attr in ("location_id", "location_name", "location_type",
                         "location_usage", "inactive"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_time_requests":
            for attr in ("time_request_id", "supervisory_organization_id"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_organizations":
            for attr in ("organization_id", "organization_id_type", "organization_type",
                         "include_inactive", "enable_transaction_log_lite"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_organization":
            for attr in ("organization_id", "organization_id_type"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_cost_centers":
            for attr in ("cost_center_id", "cost_center_id_type",
                         "updated_from_date", "updated_to_date", "include_inactive",
                         "include_hierarchy_chain"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_applicants":
            for attr in ("applicant_id", "job_requisition_id",
                         "application_date_from", "application_date_to", "is_pre_hire"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_candidates":
            for attr in ("candidate_id", "job_requisition_id",
                         "applied_from_date", "applied_to_date",
                         "created_from_date", "created_to_date",
                         "pdf_directory"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val
            params["exclude_all_attachments"] = self.exclude_all_attachments

        if self.type == "get_job_requisitions":
            for attr in ("job_requisition_id", "job_requisition_status",
                         "supervisory_organization_id", "location_id",
                         "updated_from_date", "updated_to_date"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_job_postings":
            for attr in ("job_posting_id", "job_requisition_id",
                         "job_posting_site_id", "posting_status",
                         "posted_from_date", "posted_to_date"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_job_posting_sites":
            for attr in ("job_posting_site_id", "is_active"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "get_references":
            val = getattr(self, "reference_id_type", None)
            if val:
                params["reference_id_type"] = val

        if self.type == "get_time_off_balances":
            for attr in ("time_off_plan_id", "organization_id"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "extract_time_blocks_report":
            for attr in ("supervisory_organization", "worker", "start_date", "end_date"):
                val = getattr(self, attr, None)
                if val is not None:
                    params[attr] = val

        if self.type == "custom_report":
            if getattr(self, "report_name", None):
                params["report_name"] = self.report_name
            if getattr(self, "report_owner", None):
                params["report_owner"] = self.report_owner

            # Pass through any extra simple-value component attributes as
            # query params (mirrors workday.py:840-853)
            excluded_attrs = {
                "type", "report_name", "report_owner", "run", "close",
                "add_metric", "credentials", "arguments", "loop", "job", "stat",
                "client_id", "client_secret", "refresh_token", "token_url",
                "report_username", "report_password",
                "tenant", "workday_url", "zeep_debug",
                "timeout", "encoding", "use_memory", "use_storage", "storage_path",
                "redis_url", "redis_key",
                "cost_center_id_type", "organization_id_type", "worker_id_type",
                "exclude_all_attachments", "exclude_employees", "exclude_contingent_workers",
                "StepName", "TaskName", "debug", "step_name", "task_name",
            }
            for attr_name in dir(self):
                if attr_name.startswith("_") or attr_name in excluded_attrs:
                    continue
                attr_val = getattr(self, attr_name, None)
                if attr_val is not None and not callable(attr_val):
                    if isinstance(attr_val, (str, int, float, bool)):
                        params[attr_name] = attr_val

        # ---- FEAT-027: write-type handling ---------------------------------
        if self.type in _WRITE_TYPES:
            result = await self._run_write_operation()
            self._result = result
            return self._result

        # ---- Delegate to service -------------------------------------------
        result = None
        try:
            result = await self.service.fetch(self.type, **params)

            if self.use_storage and result is not None and isinstance(result, pd.DataFrame):
                try:
                    storage_file = self._get_storage_file()
                    result.to_csv(storage_file, index=False)
                    self._logger.info("Successfully saved data to: %s", storage_file)
                except Exception as exc:
                    self._logger.error("Error saving to storage: %s", exc)

        except Exception as exc:
            self._logger.error("Error during Workday operation: %s", exc)
            raise

        if isinstance(result, pd.DataFrame):
            self.add_metric("NUMROWS", len(result.index))
            self.add_metric("NUMCOLS", len(result.columns))

        self._result = result
        self._logger.info("Workday operation finished successfully")
        return self._result

    async def get_custom_report(
        self,
        report_name: str,
        report_owner: str = None,
        **query_params,
    ) -> pd.DataFrame:
        """Convenience method — delegates to service.get_custom_report."""
        return await self.service.get_custom_report(
            report_name=report_name,
            report_owner=report_owner,
            **query_params,
        )

    async def close(self) -> None:
        """Clean up resources by closing the service."""
        await self.service.close()
