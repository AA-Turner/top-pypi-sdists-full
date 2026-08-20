"""Privacy-aware bug-report form, diagnostics review, and receipt screen."""

import asyncio
import typing as t
from dataclasses import replace

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Checkbox, Input, Static, Switch, TextArea

from dreadnode.app.api.client import ApiClient
from dreadnode.app.api.models import FeedbackReceipt
from dreadnode.app.tui.bug_report import (
    BugReportContext,
    BugReportDraft,
    DiagnosticBundle,
    DiagnosticCategory,
    build_diagnostic_bundle,
    collect_diagnostic_categories,
    save_diagnostic_bundle,
)
from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import FG, FG_FAINTEST, FG_MUTED, INFO, SUCCESS, WARNING
from dreadnode.core.log import LogEntry


def _format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size / (1024 * 1024):.1f} MiB"


def _category_label(category: DiagnosticCategory) -> str:
    sensitivity = " · may contain customer content" if category.requires_explicit_consent else ""
    return (
        f"{category.label}  {_format_bytes(category.size_bytes)}\n"
        f"{category.description}{sensitivity}"
    )


class ReportBugScreen(DreadnodeScreen):
    """Collect a report, let the customer review data, then save or send it."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "back", "Back", show=True),
        Binding("ctrl+enter", "review", "Review", show=True),
        Binding("ctrl+s", "save_bundle", "Save bundle", show=True),
    ]

    DEFAULT_CSS = f"""
    ReportBugScreen {{
        layout: vertical;
    }}
    ReportBugScreen #report-header {{
        height: auto;
        padding: 1 2 0 2;
        color: {FG};
    }}
    ReportBugScreen #report-subtitle,
    ReportBugScreen .report-help {{
        height: auto;
        color: {FG_FAINTEST};
        margin-bottom: 1;
    }}
    ReportBugScreen #report-form,
    ReportBugScreen #report-review,
    ReportBugScreen #report-receipt {{
        height: 1fr;
        padding: 0 2;
    }}
    ReportBugScreen .field-label {{
        height: 1;
        margin-top: 1;
        color: {FG_MUTED};
    }}
    ReportBugScreen Input,
    ReportBugScreen TextArea {{
        border: tall {FG_FAINTEST};
        background: transparent;
    }}
    ReportBugScreen TextArea {{
        height: 5;
    }}
    ReportBugScreen .report-buttons {{
        height: 3;
        margin-top: 1;
    }}
    ReportBugScreen #report-consent-row {{
        height: 3;
        margin-top: 1;
    }}
    ReportBugScreen #report-consent-row Static {{
        width: 1fr;
        height: 3;
        content-align: left middle;
    }}
    ReportBugScreen Button {{
        margin-right: 1;
    }}
    ReportBugScreen .diagnostic-category {{
        height: auto;
        margin-bottom: 1;
    }}
    ReportBugScreen #report-submit-status,
    ReportBugScreen #report-validation,
    ReportBugScreen #report-receipt-content {{
        height: auto;
        margin-top: 1;
    }}
    """

    def __init__(
        self,
        *,
        context: BugReportContext,
        log_entries: list[LogEntry],
        conversation: str,
        api: ApiClient | None,
        organization_key: str | None,
        workspace_name: str | None,
    ) -> None:
        super().__init__()
        self._report_context = context
        self._log_entries = log_entries
        self._conversation = conversation
        self._api = api
        self._organization_key = organization_key
        self._workspace_name = workspace_name
        self._view: t.Literal["form", "review", "receipt"] = "form"
        self._feedback_enabled = False
        self._categories = self._collect_categories()
        self._last_bundle: DiagnosticBundle | None = None

    def _collect_categories(self) -> list[DiagnosticCategory]:
        return collect_diagnostic_categories(
            context=self._report_context,
            log_entries=self._log_entries,
            conversation=self._conversation,
        )

    def compose_content(self) -> ComposeResult:
        yield Static("[bold]Report a bug[/bold]", id="report-header")
        yield Static(
            "Describe what happened, then choose exactly which diagnostics to include.",
            id="report-subtitle",
        )
        with VerticalScroll(id="report-form"):
            yield Static("Short title", classes="field-label")
            yield Input(placeholder="What went wrong?", id="report-title")
            yield Static("Steps to reproduce", classes="field-label")
            yield TextArea(id="report-steps")
            yield Static("Expected result", classes="field-label")
            yield TextArea(id="report-expected")
            yield Static("Actual result", classes="field-label")
            yield TextArea(id="report-actual")
            yield Static("Additional context (optional)", classes="field-label")
            yield TextArea(id="report-additional")
            with Horizontal(id="report-consent-row"):
                yield Switch(value=False, id="report-contact-consent")
                yield Static("Dreadnode may contact me about this report")
            yield Static("", id="report-validation")
            with Horizontal(classes="report-buttons"):
                yield Button("Review diagnostics", id="report-review-button", variant="primary")
        with Vertical(id="report-review", classes="-hidden"):
            yield Static(
                "Safe runtime metadata and recent INFO/DEBUG logs are selected. "
                "TRACE, conversation, and component logs stay off until you select them.",
                classes="report-help",
            )
            with VerticalScroll(id="report-categories"):
                for category in self._categories:
                    yield Checkbox(
                        _category_label(category),
                        value=category.selected_by_default,
                        id=f"report-category-{category.category_id}",
                        classes="diagnostic-category",
                    )
            yield Static("Checking platform feedback availability…", id="report-submit-status")
            with Horizontal(classes="report-buttons"):
                yield Button("Edit report", id="report-edit-button")
                yield Button("Save bundle", id="report-save-button", variant="primary")
                yield Button(
                    "Send report", id="report-send-button", variant="success", disabled=True
                )
        with Vertical(id="report-receipt", classes="-hidden"):
            yield Static("", id="report-receipt-content")
            with Horizontal(classes="report-buttons"):
                yield Button("Save another copy", id="report-receipt-save")
                yield Button("Done", id="report-done-button", variant="primary")

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#report-title", Input).focus()
        if self._api is None:
            self._set_submission_availability(
                enabled=False,
                message="Offline or not authenticated — local bundle save is available.",
            )
        else:
            self._load_platform_config()

    @work(exclusive=True, group="report-config")
    async def _load_platform_config(self) -> None:
        assert self._api is not None
        try:
            config = await asyncio.to_thread(self._api.get_config)
        except Exception:
            if not self.is_mounted:
                return
            self._set_submission_availability(
                enabled=False,
                message="Platform unavailable — local bundle save is available.",
            )
            return
        # The screen may have been popped while the fetch was in flight —
        # rendering would query_one against a dead widget tree (NoMatches).
        if not self.is_mounted:
            return
        self._report_context = replace(
            self._report_context,
            deployment_mode=config.deployment_mode,
        )
        if self._view != "receipt":
            self._refresh_categories()
        if config.feedback_enabled and config.feedback_diagnostics:
            self._set_submission_availability(
                enabled=True,
                message="Send report is configured for this deployment.",
            )
        elif config.feedback_enabled:
            self._set_submission_availability(
                enabled=False,
                message=(
                    "This platform version does not accept diagnostic reports — "
                    "local bundle save is available."
                ),
            )
        else:
            self._set_submission_availability(
                enabled=False,
                message=(
                    "Feedback submission is disabled — save the bundle and "
                    "share it with your platform operator."
                ),
            )

    def _set_submission_availability(self, *, enabled: bool, message: str) -> None:
        self._feedback_enabled = enabled
        self.query_one("#report-send-button", Button).disabled = not enabled
        self.query_one("#report-submit-status", Static).update(message)

    def _draft(self) -> BugReportDraft:
        return BugReportDraft(
            title=self.query_one("#report-title", Input).value.strip(),
            steps_to_reproduce=self.query_one("#report-steps", TextArea).text.strip(),
            expected_result=self.query_one("#report-expected", TextArea).text.strip(),
            actual_result=self.query_one("#report-actual", TextArea).text.strip(),
            additional_context=self.query_one("#report-additional", TextArea).text.strip(),
            contact_consent=self.query_one("#report-contact-consent", Switch).value,
        )

    def _validate_draft(self, draft: BugReportDraft) -> str | None:
        missing: list[str] = []
        if not draft.title:
            missing.append("title")
        if not draft.steps_to_reproduce:
            missing.append("steps to reproduce")
        if not draft.expected_result:
            missing.append("expected result")
        if not draft.actual_result:
            missing.append("actual result")
        if missing:
            return "Complete: " + ", ".join(missing)
        if len(draft.title) > 200:
            return "Keep the title under 200 characters."
        if len(draft.description()) > 5000:
            return "Keep the combined report details under 5,000 characters."
        return None

    def _selected_category_ids(self) -> set[str]:
        return {
            category.category_id
            for category in self._categories
            if self.query_one(f"#report-category-{category.category_id}", Checkbox).value
        }

    def _refresh_categories(self) -> None:
        selected: dict[str, bool] = {}
        if self.is_mounted:
            selected = {
                category.category_id: self.query_one(
                    f"#report-category-{category.category_id}", Checkbox
                ).value
                for category in self._categories
            }
        self._categories = self._collect_categories()
        if not self.is_mounted:
            return
        for category in self._categories:
            checkbox = self.query_one(f"#report-category-{category.category_id}", Checkbox)
            checkbox.label = _category_label(category)
            checkbox.value = selected.get(
                category.category_id,
                category.selected_by_default,
            )

    def _build_bundle(self) -> DiagnosticBundle:
        bundle = build_diagnostic_bundle(
            self._draft(),
            self._categories,
            self._selected_category_ids(),
        )
        self._last_bundle = bundle
        return bundle

    def action_review(self) -> None:
        if self._view != "form":
            return
        error = self._validate_draft(self._draft())
        if error:
            self.query_one("#report-validation", Static).update(f"[{WARNING}]{error}[/]")
            return
        self.query_one("#report-validation", Static).update("")
        self._refresh_categories()
        self._show_view("review")

    def action_save_bundle(self) -> None:
        if self._view == "form":
            self.action_review()
            if self._view == "form":
                return
        try:
            bundle = (
                self._last_bundle
                if self._view == "receipt" and self._last_bundle is not None
                else self._build_bundle()
            )
            output_path = save_diagnostic_bundle(bundle)
        except Exception as exc:
            self.notify(f"Unable to save bundle: {exc}", severity="error")
            return
        self.query_one("#report-submit-status", Static).update(f"[{SUCCESS}]Saved {output_path}[/]")

    @work(exclusive=True, group="report-submit")
    async def _send_report(self) -> None:
        if self._api is None or not self._feedback_enabled:
            return
        send_button = self.query_one("#report-send-button", Button)
        send_button.disabled = True
        self.query_one("#report-submit-status", Static).update(f"[{INFO}]Sending report…[/]")
        draft = self._draft()
        try:
            bundle = self._build_bundle()
            payload = {
                "category": "bug",
                "severity": "medium",
                "title": draft.title,
                "description": draft.description(),
                "organization_key": self._organization_key,
                "workspace_name": self._workspace_name,
                "app_version": self._report_context.runtime_version,
                "contact_consent": draft.contact_consent,
                "source": "tui",
                "steps_to_reproduce": draft.steps_to_reproduce,
                "expected_result": draft.expected_result,
                "actual_result": draft.actual_result,
                "additional_context": draft.additional_context or None,
                "diagnostic_bundle": bundle.as_upload(),
            }
            receipt = await asyncio.to_thread(self._api.submit_feedback, payload)
        except Exception as exc:
            if not self.is_mounted:
                return
            self.query_one("#report-submit-status", Static).update(
                f"[{WARNING}]Send failed: {exc}. You can still save the bundle locally.[/]"
            )
            send_button.disabled = False
            return
        # The screen may have been popped while the upload was in flight —
        # rendering would query_one against a dead widget tree (NoMatches).
        if not self.is_mounted:
            return
        # Reset the review view so returning from the receipt allows edits and resends.
        send_button.disabled = False
        self.query_one("#report-submit-status", Static).update(
            f"[{SUCCESS}]Report {receipt.report_id} sent.[/]"
        )
        self._show_receipt(receipt)

    def _show_receipt(self, receipt: FeedbackReceipt) -> None:
        status_color = SUCCESS if receipt.delivery_status == "delivered" else WARNING
        self.query_one("#report-receipt-content", Static).update(
            f"[bold {status_color}]Report {receipt.report_id}[/]\n\n"
            f"{receipt.message}\n\n"
            f"Delivery: {receipt.delivery_status}\n"
            f"Retained until: {receipt.retained_until}"
        )
        self._show_view("receipt")

    def _show_view(self, view: t.Literal["form", "review", "receipt"]) -> None:
        self._view = view
        for name in ("form", "review", "receipt"):
            self.query_one(f"#report-{name}").set_class(name != view, "-hidden")

    @on(Button.Pressed)
    def _on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "report-review-button":
            self.action_review()
        elif button_id == "report-edit-button":
            self._show_view("form")
        elif button_id in {"report-save-button", "report-receipt-save"}:
            self.action_save_bundle()
        elif button_id == "report-send-button":
            self._send_report()
        elif button_id == "report-done-button":
            self.dismiss()

    def action_back(self) -> None:
        if self._view == "form":
            self.dismiss()
        elif self._view == "review":
            self._show_view("form")
        else:
            self._show_view("review")
