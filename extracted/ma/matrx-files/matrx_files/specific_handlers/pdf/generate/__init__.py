"""HTML/Markdown/URL → PDF generation (Phase 8).

Will host:
- ``from_html`` — WeasyPrint or PyMuPDF Story dispatch by CSS-fidelity need
- ``from_markdown`` — Markdown via WeasyPrint with our theme CSS
- ``from_url`` — Playwright print-to-PDF (reuses scraper's browser pool)
- ``from_template`` — ReportLab-style programmatic generation
"""
