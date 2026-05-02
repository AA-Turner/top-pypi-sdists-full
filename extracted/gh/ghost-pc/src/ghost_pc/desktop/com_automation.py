"""Office COM Automation for direct document control.

Uses pywin32's COM interface to control Microsoft Office applications
(Word, Excel, Outlook) without pixel clicking. This is 10-100x faster
and more reliable than visual interaction for document operations.

Windows-only. Requires pywin32 and the target Office application installed.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

logger = logging.getLogger(__name__)


def _require_win32() -> None:
    if sys.platform != "win32":
        raise RuntimeError("COM automation requires Windows")


# ── Word ────────────────────────────────────────────────────────────────────


async def word_get_text() -> dict[str, Any]:
    """Get the full text content of the active Word document."""
    _require_win32()
    try:
        import win32com.client

        word = win32com.client.GetActiveObject("Word.Application")
        doc = word.ActiveDocument
        text = doc.Content.Text
        return {"status": "ok", "text": text[:5000]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def word_insert_table(rows: int, cols: int) -> dict[str, Any]:
    """Insert a table at the cursor position in the active Word document.

    Args:
        rows: Number of rows.
        cols: Number of columns.
    """
    _require_win32()
    try:
        import win32com.client

        word = win32com.client.GetActiveObject("Word.Application")
        doc = word.ActiveDocument
        selection = word.Selection
        table = doc.Tables.Add(selection.Range, rows, cols)
        table.Style = "Table Grid"
        return {"status": "ok", "rows": str(rows), "cols": str(cols)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def word_find_replace(find: str, replace: str) -> dict[str, Any]:
    """Find and replace text in the active Word document.

    Args:
        find: Text to find.
        replace: Replacement text.
    """
    _require_win32()
    try:
        import win32com.client

        word = win32com.client.GetActiveObject("Word.Application")
        doc = word.ActiveDocument

        find_obj = doc.Content.Find
        count = 0
        while find_obj.Execute(FindText=find, ReplaceWith=replace, Replace=1):
            count += 1
            if count > 1000:
                break

        return {"status": "ok", "replacements": count}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def word_save_as(path: str, file_format: str = "docx") -> dict[str, Any]:
    """Save the active Word document to a new path.

    Args:
        path: Full file path to save to.
        file_format: "docx" (default) or "pdf".
    """
    _require_win32()
    try:
        import win32com.client

        word = win32com.client.GetActiveObject("Word.Application")
        doc = word.ActiveDocument

        # WdSaveFormat: 16 = docx, 17 = pdf
        fmt_map = {"docx": 16, "pdf": 17}
        fmt = fmt_map.get(file_format, 16)

        doc.SaveAs2(path, FileFormat=fmt)
        return {"status": "ok", "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Excel ───────────────────────────────────────────────────────────────────


async def excel_read_range(range_str: str) -> dict[str, Any]:
    """Read a range of cells from the active Excel worksheet.

    Args:
        range_str: Excel range notation (e.g., "A1:C10", "B2").
    """
    _require_win32()
    try:
        import win32com.client

        excel = win32com.client.GetActiveObject("Excel.Application")
        sheet = excel.ActiveSheet
        rng = sheet.Range(range_str)
        values = rng.Value

        # Convert to list of lists for serialization
        if isinstance(values, tuple):
            data = [list(row) if isinstance(row, tuple) else [row] for row in values]
        else:
            data = [[values]]

        return {"status": "ok", "range": range_str, "data": data}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def excel_write_cell(cell: str, value: str) -> dict[str, Any]:
    """Write a value to a specific cell in the active Excel worksheet.

    Args:
        cell: Cell reference (e.g., "A1", "B5").
        value: Value to write.
    """
    _require_win32()
    try:
        import win32com.client

        excel = win32com.client.GetActiveObject("Excel.Application")
        sheet = excel.ActiveSheet
        sheet.Range(cell).Value = value
        return {"status": "ok", "cell": cell, "value": value}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def excel_get_sheet_as_markdown() -> dict[str, Any]:
    """Export the active Excel worksheet as a Markdown table."""
    _require_win32()
    try:
        import win32com.client

        excel = win32com.client.GetActiveObject("Excel.Application")
        sheet = excel.ActiveSheet
        used = sheet.UsedRange
        values = used.Value

        if not values:
            return {"status": "ok", "markdown": "(empty sheet)"}

        rows = [list(row) if isinstance(row, tuple) else [row] for row in values]

        # Build markdown table
        lines: list[str] = []
        if rows:
            header = [str(c) if c is not None else "" for c in rows[0]]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("| " + " | ".join(["---"] * len(header)) + " |")
            for row in rows[1:]:
                cells = [str(c) if c is not None else "" for c in row]
                # Pad if row is shorter than header
                while len(cells) < len(header):
                    cells.append("")
                lines.append("| " + " | ".join(cells[: len(header)]) + " |")

        return {"status": "ok", "markdown": "\n".join(lines)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Outlook ─────────────────────────────────────────────────────────────────


async def outlook_send_email(to: str, subject: str, body: str) -> dict[str, Any]:
    """Send an email via Outlook.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Email body text.
    """
    _require_win32()
    try:
        import win32com.client

        outlook = win32com.client.GetActiveObject("Outlook.Application")
        mail = outlook.CreateItem(0)  # olMailItem
        mail.To = to
        mail.Subject = subject
        mail.Body = body
        mail.Send()
        return {"status": "ok", "to": to, "subject": subject}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def outlook_get_unread() -> dict[str, Any]:
    """Get unread emails from the Outlook inbox."""
    _require_win32()
    try:
        import win32com.client

        outlook = win32com.client.GetActiveObject("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        inbox = namespace.GetDefaultFolder(6)  # olFolderInbox

        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        unread: list[dict[str, Any]] = []
        for msg in messages:
            if msg.UnRead and len(unread) < 10:
                unread.append(
                    {
                        "from": str(msg.SenderName),
                        "subject": str(msg.Subject),
                        "received": str(msg.ReceivedTime),
                        "preview": str(msg.Body)[:200],
                    }
                )
            if len(unread) >= 10:
                break

        return {"status": "ok", "count": len(unread), "emails": unread}
    except Exception as e:
        return {"status": "error", "error": str(e)}
