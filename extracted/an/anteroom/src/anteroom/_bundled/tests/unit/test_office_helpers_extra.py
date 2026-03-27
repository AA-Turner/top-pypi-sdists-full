"""Additional unit tests for Office helper and dispatch wrappers."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.tools import office_docx, office_pptx, office_xlsx


class TestDocxHelpers:
    def test_open_document_lib_not_found(self) -> None:
        fake_mod = SimpleNamespace(Document=MagicMock())

        with patch.dict("sys.modules", {"docx": fake_mod}):
            doc, err = office_docx._open_document_lib("/missing.docx", "missing.docx")

        assert doc is None
        assert err == "File not found: missing.docx"

    def test_open_document_lib_success(self, tmp_path) -> None:
        path = tmp_path / "ok.docx"
        path.write_text("x")
        fake_doc = object()
        fake_mod = SimpleNamespace(Document=MagicMock(return_value=fake_doc))

        with patch.dict("sys.modules", {"docx": fake_mod}):
            doc, err = office_docx._open_document_lib(str(path), "ok.docx")

        assert doc is fake_doc
        assert err is None

    def test_open_document_lib_wraps_read_error(self, tmp_path) -> None:
        path = tmp_path / "broken.docx"
        path.write_text("x")
        fake_mod = SimpleNamespace(Document=MagicMock(side_effect=ValueError("bad doc")))

        with patch.dict("sys.modules", {"docx": fake_mod}):
            doc, err = office_docx._open_document_lib(str(path), "broken.docx")

        assert doc is None
        assert "Unable to read DOCX file: broken.docx" in err

    def test_open_document_com_not_found(self) -> None:
        word, doc, err = office_docx._open_document_com(MagicMock(), "/missing.docx", "missing.docx")
        assert word is None
        assert doc is None
        assert err == "File not found: missing.docx"

    def test_open_document_com_success(self, tmp_path) -> None:
        path = tmp_path / "ok.docx"
        path.write_text("x")
        doc = object()
        manager = MagicMock()
        word = MagicMock()
        word.Documents.Open.return_value = doc
        manager.get_app.return_value = word

        got_word, got_doc, err = office_docx._open_document_com(manager, str(path), "ok.docx", read_only=True)

        assert got_word is word
        assert got_doc is doc
        assert err is None
        word.Documents.Open.assert_called_once()

    @pytest.mark.asyncio
    async def test_dispatch_com_unknown_action(self) -> None:
        with patch.object(office_docx, "_com_mod", SimpleNamespace(get_manager=lambda: MagicMock())):
            result = await office_docx._dispatch_com("unknown", "/tmp/x.docx", "x.docx", working_dir="/tmp")
        assert "Unknown action" in result["error"]

    @pytest.mark.asyncio
    async def test_dispatch_com_wraps_handler_exception(self) -> None:
        manager = MagicMock()
        manager.run_com = AsyncMock(side_effect=RuntimeError("boom"))

        with patch.object(office_docx, "_com_mod", SimpleNamespace(get_manager=lambda: manager)):
            result = await office_docx._dispatch_com("read", "/tmp/x.docx", "x.docx", working_dir="/tmp")

        assert result["error"] == "COM read failed on x.docx: RuntimeError: boom"


class TestXlsxHelpers:
    def test_open_workbook_lib_not_found(self) -> None:
        fake_mod = SimpleNamespace(load_workbook=MagicMock())

        with patch.dict("sys.modules", {"openpyxl": fake_mod}):
            wb, err = office_xlsx._open_workbook_lib("/missing.xlsx", "missing.xlsx")

        assert wb is None
        assert err == "File not found: missing.xlsx"

    def test_open_workbook_lib_success(self, tmp_path) -> None:
        path = tmp_path / "ok.xlsx"
        path.write_text("x")
        wb = object()
        fake_mod = SimpleNamespace(load_workbook=MagicMock(return_value=wb))

        with patch.dict("sys.modules", {"openpyxl": fake_mod}):
            got_wb, err = office_xlsx._open_workbook_lib(str(path), "ok.xlsx", read_only=True)

        assert got_wb is wb
        assert err is None

    def test_open_workbook_lib_wraps_load_error(self, tmp_path) -> None:
        path = tmp_path / "broken.xlsx"
        path.write_text("x")
        fake_mod = SimpleNamespace(load_workbook=MagicMock(side_effect=ValueError("bad book")))

        with patch.dict("sys.modules", {"openpyxl": fake_mod}):
            wb, err = office_xlsx._open_workbook_lib(str(path), "broken.xlsx")

        assert wb is None
        assert "Unable to read XLSX file: broken.xlsx" in err

    def test_get_sheet_lib_missing_named_sheet(self) -> None:
        wb = SimpleNamespace(sheetnames=["Data", "Other"], active=object())
        ws, err = office_xlsx._get_sheet_lib(wb, "Missing")
        assert ws is None
        assert "Sheet 'Missing' not found" in err

    def test_get_sheet_lib_missing_active_sheet(self) -> None:
        wb = SimpleNamespace(sheetnames=["Data"], active=None)
        ws, err = office_xlsx._get_sheet_lib(wb, None)
        assert ws is None
        assert err == "No active sheet found"

    @pytest.mark.asyncio
    async def test_dispatch_com_wraps_handler_exception(self) -> None:
        manager = MagicMock()
        manager.run_com = AsyncMock(side_effect=RuntimeError("boom"))

        with patch.object(office_xlsx, "_com_mod", SimpleNamespace(get_manager=lambda: manager)):
            result = await office_xlsx._dispatch_com("read", "/tmp/x.xlsx", "x.xlsx", working_dir="/tmp")

        assert result["error"] == "COM read failed on x.xlsx: RuntimeError: boom"


class TestPptxHelpers:
    def test_working_dir_round_trip(self) -> None:
        original = office_pptx._get_working_dir()
        try:
            office_pptx.set_working_dir("/tmp/pptx")
            assert office_pptx._get_working_dir() == "/tmp/pptx"
        finally:
            office_pptx.set_working_dir(original)

    def test_com_only_error(self) -> None:
        assert office_pptx._com_only_error("headers_footers") == {
            "error": "Action 'headers_footers' requires Windows with Office installed (COM backend)"
        }

    def test_open_pres_com_not_found(self) -> None:
        ppt, prs, err = office_pptx._open_pres_com(MagicMock(), "/missing.pptx", "missing.pptx")
        assert ppt is None
        assert prs is None
        assert err == "File not found: missing.pptx"

    def test_open_pres_com_success(self, tmp_path) -> None:
        path = tmp_path / "ok.pptx"
        path.write_text("x")
        prs = object()
        ppt = MagicMock()
        ppt.Presentations.Open.return_value = prs
        manager = MagicMock()
        manager.get_app.return_value = ppt

        got_ppt, got_prs, err = office_pptx._open_pres_com(manager, str(path), "ok.pptx", read_only=True)

        assert got_ppt is ppt
        assert got_prs is prs
        assert err is None

    def test_open_pres_com_wraps_open_error(self, tmp_path) -> None:
        path = tmp_path / "bad.pptx"
        path.write_text("x")
        ppt = MagicMock()
        ppt.Presentations.Open.side_effect = ValueError("bad pres")
        manager = MagicMock()
        manager.get_app.return_value = ppt

        got_ppt, got_prs, err = office_pptx._open_pres_com(manager, str(path), "bad.pptx")

        assert got_ppt is None
        assert got_prs is None
        assert "Unable to open PPTX file: bad.pptx" in err

    def test_get_slide_com_requires_index(self) -> None:
        slide, err = office_pptx._get_slide_com(SimpleNamespace(Slides=SimpleNamespace(Count=3)), None)
        assert slide is None
        assert err == "slide_index is required"

    def test_get_slide_com_rejects_out_of_range_index(self) -> None:
        prs = SimpleNamespace(Slides=SimpleNamespace(Count=3))
        slide, err = office_pptx._get_slide_com(prs, 4)
        assert slide is None
        assert err == "slide_index 4 out of range (1-3)"

    @pytest.mark.asyncio
    async def test_dispatch_com_wraps_handler_exception(self) -> None:
        manager = MagicMock()
        manager.run_com = AsyncMock(side_effect=RuntimeError("boom"))

        with patch.object(office_pptx, "_com_mod", SimpleNamespace(get_manager=lambda: manager)):
            result = await office_pptx._dispatch_com("read", "/tmp/x.pptx", "x.pptx", working_dir="/tmp")

        assert result["error"] == "COM read failed on x.pptx: RuntimeError: boom"
