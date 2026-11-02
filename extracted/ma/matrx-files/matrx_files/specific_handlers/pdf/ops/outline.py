"""Bookmarks: read, and write the whole outline (PDF-PLAN U11), through ``pikepdf``.

The outline is a tree of ``{title, page, children}`` where ``page`` is 1-based (or ``None`` for a
heading that goes nowhere). Add, rename, move and delete are edits to that tree made by the caller
(the tools rail, an agent); ``set_outline_bytes`` replaces the document's outline with the tree it is
given, validating every page, so the stored outline is always one the file can honour.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from ._pike import is_signed, load_pikepdf, open_pdf, save_pdf

MAX_OUTLINE_ITEMS = 5000
MAX_OUTLINE_DEPTH = 8


class PdfOutlineNode(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    page: int | None = Field(default=None, ge=1)
    children: list["PdfOutlineNode"] = Field(default_factory=list)


PdfOutlineNode.model_rebuild()


def _page_index(pdf: Any, dest: Any, names: Any) -> int | None:
    """0-based page index a destination points at, or None when it cannot be resolved."""
    pikepdf = load_pikepdf()
    try:
        if dest is None:
            return None
        if isinstance(dest, (pikepdf.String, pikepdf.Name)) and names is not None:
            key = str(dest) if isinstance(dest, pikepdf.String) else str(dest)[1:]
            found = names.get(key) if hasattr(names, "get") else None
            dest = found
            if isinstance(dest, pikepdf.Dictionary) and "/D" in dest:
                dest = dest["/D"]
        if isinstance(dest, pikepdf.Array) and len(dest) > 0:
            target = dest[0]
            if isinstance(target, pikepdf.Object) and hasattr(target, "objgen"):
                for i, page in enumerate(pdf.pages):
                    if page.obj.objgen == target.objgen:
                        return i
            if isinstance(target, int):
                return int(target) if 0 <= int(target) < len(pdf.pages) else None
    except Exception:
        return None
    return None


def _read_node(pdf: Any, item: Any, names: Any, depth: int, counter: list[int]) -> dict[str, Any]:
    counter[0] += 1
    dest = item.destination
    if dest is None and item.action is not None:
        action = item.action
        if "/D" in action:
            dest = action["/D"]
    index = _page_index(pdf, dest, names)
    node: dict[str, Any] = {"title": str(item.title), "page": None if index is None else index + 1, "children": []}
    if depth < MAX_OUTLINE_DEPTH:
        for child in item.children:
            if counter[0] >= MAX_OUTLINE_ITEMS:
                break
            node["children"].append(_read_node(pdf, child, names, depth + 1, counter))
    return node


def read_outline_bytes(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    pikepdf = load_pikepdf()
    with open_pdf(pdf_bytes, password) as pdf:
        names = None
        try:
            if "/Names" in pdf.Root and "/Dests" in pdf.Root.Names:
                tree = pikepdf.NameTree(pdf.Root.Names.Dests)
                names = {str(k): v for k, v in tree.items()}
            elif "/Dests" in pdf.Root:
                names = {str(k)[1:]: v for k, v in pdf.Root.Dests.items()}
        except Exception:
            names = None
        counter = [0]
        with pdf.open_outline() as outline:
            nodes = [_read_node(pdf, it, names, 1, counter) for it in outline.root]
        return {"page_count": len(pdf.pages), "items": nodes, "count": counter[0]}


def _validate(nodes: list[PdfOutlineNode], page_count: int, depth: int, counter: list[int]) -> None:
    if depth > MAX_OUTLINE_DEPTH:
        raise ValueError(f"Bookmarks can nest {MAX_OUTLINE_DEPTH} levels deep at most.")
    for node in nodes:
        counter[0] += 1
        if counter[0] > MAX_OUTLINE_ITEMS:
            raise ValueError(f"A PDF can carry {MAX_OUTLINE_ITEMS} bookmarks at most.")
        if node.page is not None and node.page > page_count:
            raise ValueError(f'The bookmark "{node.title}" points at page {node.page}, but this PDF has {page_count} pages.')
        _validate(node.children, page_count, depth + 1, counter)


def set_outline_bytes(
    pdf_bytes: bytes,
    items: list[PdfOutlineNode | dict[str, Any]],
    *,
    password: str = "",
) -> PdfBinaryResult:
    """Replace the outline with ``items`` (an empty list removes every bookmark)."""
    pikepdf = load_pikepdf()
    nodes = [n if isinstance(n, PdfOutlineNode) else PdfOutlineNode(**n) for n in items]
    with open_pdf(pdf_bytes, password) as pdf:
        total = len(pdf.pages)
        counter = [0]
        _validate(nodes, total, 1, counter)
        signed = is_signed(pdf)

        def build(node: PdfOutlineNode) -> Any:
            entry = pikepdf.OutlineItem(node.title, node.page - 1 if node.page is not None else None)
            entry.children.extend(build(c) for c in node.children)
            return entry

        with pdf.open_outline() as outline:
            outline.root[:] = [build(n) for n in nodes]
        if not nodes and "/Outlines" in pdf.Root:
            del pdf.Root["/Outlines"]
        content = save_pdf(pdf)
    return PdfBinaryResult(
        content=content,
        page_count=total,
        operation="set_outline",
        metadata={"bookmarks": counter[0], "signed": signed},
    )


async def read_outline_bytes_async(pdf_bytes: bytes, *, password: str = "") -> dict[str, Any]:
    return await run_in_cpu_executor(lambda: read_outline_bytes(pdf_bytes, password=password))


async def set_outline_bytes_async(pdf_bytes: bytes, items: list[Any], *, password: str = "") -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: set_outline_bytes(pdf_bytes, items, password=password))


__all__ = [
    "MAX_OUTLINE_DEPTH",
    "MAX_OUTLINE_ITEMS",
    "PdfOutlineNode",
    "read_outline_bytes",
    "read_outline_bytes_async",
    "set_outline_bytes",
    "set_outline_bytes_async",
]
