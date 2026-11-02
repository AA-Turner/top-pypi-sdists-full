"""Multi-document composition: merge and split."""

from __future__ import annotations

from typing import Any

from ..concurrency import run_in_cpu_executor
from ..internal import open_unprotected, load_pymupdf, normalise_page_ranges, save_pymupdf_doc
from ..models import PdfBinaryResult, PdfSplitPart


def merge_pdfs_from_bytes(sources: list[dict[str, Any]]) -> PdfBinaryResult:
    if not sources:
        raise ValueError("Provide at least one source PDF to merge.")

    pymupdf = load_pymupdf()
    source_metadata: list[dict[str, Any]] = []
    with pymupdf.open() as out:
        for index, source in enumerate(sources):
            content = source.get("content")
            if not isinstance(content, bytes):
                raise ValueError(f"Merge source {index} is missing PDF bytes.")

            with pymupdf.open(stream=content, filetype="pdf") as src:
                selected = normalise_page_ranges(
                    src.page_count,
                    source.get("pages"),
                    source.get("page_ranges"),
                    default_all=True,
                )
                for page_num in selected:
                    page_idx = page_num - 1
                    out.insert_pdf(src, from_page=page_idx, to_page=page_idx)
                source_metadata.append({"index": index, "pages": selected})

        return PdfBinaryResult(
            content=save_pymupdf_doc(out),
            page_count=out.page_count,
            operation="merge_pdfs",
            metadata={"sources": source_metadata},
        )


async def merge_pdfs_from_bytes_async(sources: list[dict[str, Any]]) -> PdfBinaryResult:
    return await run_in_cpu_executor(merge_pdfs_from_bytes, sources)


def split_pdf_bytes(
    pdf_bytes: bytes,
    parts: list[dict[str, Any]] | None = None,
    max_pages_per_part: int | None = None,
) -> list[PdfSplitPart]:
    pymupdf = load_pymupdf()
    with open_unprotected(pymupdf, pdf_bytes) as src:
        split_specs: list[dict[str, Any]] = []
        if parts:
            split_specs = list(parts)
        elif max_pages_per_part:
            if max_pages_per_part < 1:
                raise ValueError("max_pages_per_part must be >= 1.")
            for start in range(1, src.page_count + 1, max_pages_per_part):
                end = min(start + max_pages_per_part - 1, src.page_count)
                split_specs.append({"page_ranges": [{"start": start, "end": end}]})
        else:
            split_specs = [
                {"pages": [page_num]} for page_num in range(1, src.page_count + 1)
            ]

        results: list[PdfSplitPart] = []
        for index, spec in enumerate(split_specs, start=1):
            selected = normalise_page_ranges(
                src.page_count,
                spec.get("pages"),
                spec.get("page_ranges"),
                default_all=False,
            )
            if not selected:
                raise ValueError(f"Split part {index} has no selected pages.")

            with pymupdf.open() as out:
                for page_num in selected:
                    page_idx = page_num - 1
                    out.insert_pdf(src, from_page=page_idx, to_page=page_idx)
                filename = str(spec.get("filename") or f"part_{index}.pdf")
                if not filename.lower().endswith(".pdf"):
                    filename += ".pdf"
                results.append(
                    PdfSplitPart(
                        content=save_pymupdf_doc(out),
                        filename=filename,
                        page_count=out.page_count,
                        page_numbers=selected,
                    )
                )

        return results


async def split_pdf_bytes_async(
    pdf_bytes: bytes,
    parts: list[dict[str, Any]] | None = None,
    max_pages_per_part: int | None = None,
) -> list[PdfSplitPart]:
    return await run_in_cpu_executor(
        split_pdf_bytes, pdf_bytes, parts, max_pages_per_part
    )


__all__ = [
    "merge_pdfs_from_bytes",
    "merge_pdfs_from_bytes_async",
    "split_pdf_bytes",
    "split_pdf_bytes_async",
]
