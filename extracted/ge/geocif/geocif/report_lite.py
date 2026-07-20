"""Report Lite — one lightweight per-country yield-outlook PDF.

A trimmed sibling of :func:`geocif.report.generate_report`. For each country
it emits a short PDF with a cover page, a genuinely clickable Table of
Contents, and one numbered section per crop. Each crop section leads with
accuracy, then shows the forecast, as "how-to-read" captioned figures for the
*best* model (lowest ``rrmsep_mean``):

    (a) the rRMSEp model-accuracy scorecard,
    (b) the best-model predicted-vs-observed scatter,
    (c) a per-region predicted-yield table,
    (d) predicted-yield choropleth (sequential), and
    (e) the non-filtered yield-outlook index map (diverging).

The reportlab / PIL scaffold (TOC heading, aspect-ratio image scaler, footer
with logos + page number, cover page, TableOfContents, and the two-pass
``multiBuild`` that resolves TOC page numbers) is LIFTED verbatim from
:mod:`geocif.report` into a module-level :class:`_LiteReport` builder. The
original :func:`geocif.report.generate_report` is left untouched; this module
only reuses its module-level ``_DESC`` and ``_find_images`` helpers.

Usage::

    from geocif.report_lite import generate_report_lite
    generate_report_lite(dir_outlook, parser, current_year,
                         countries, crops, models)
"""

import ast
import logging
from pathlib import Path

import arrow as ar
import pandas as pd

from geocif import __version__
from geocif.report import _DESC, _find_images

logger = logging.getLogger(__name__)

# reportlab / PIL are soft dependencies: importing this module must never fail
# just because reportlab is absent. When it is missing, generate_report_lite
# logs a warning and returns an empty list.
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch, cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak,
        KeepTogether, LongTable, TableStyle,
    )
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.lib import colors as rl_colors

    _HAS_REPORTLAB = True
except ImportError:  # pragma: no cover — exercised only where reportlab absent
    _HAS_REPORTLAB = False


# ---------------------------------------------------------------------------
# How-to-read descriptions (never state findings/results — only how to read).
# _desc() prefers these and falls back to report._DESC where a key is absent.
# ---------------------------------------------------------------------------

_LITE_DESC = {
    "predicted_yield": (
        "Sequential choropleth of model-predicted yield per admin region; "
        "darker = higher on the colorbar. Unshaded regions have no "
        "cropmask/yield coverage."
    ),
    # {year} is filled in per section.
    "outlook_index": (
        "Diverging choropleth of the outlook index = percent deviation of the "
        "{year} predicted yield from the region's own multi-year mean "
        "prediction, on a fixed -40 to +40% scale (green above the region's "
        "baseline, brown below). This is an anomaly versus each region's own "
        "normal, not an absolute yield."
    ),
    "rrmsep": (
        "rRMSEp (relative root-mean-square error of prediction, %) is the "
        "forecast error expressed as a percentage of the mean observed yield "
        "— lower is better, and it is comparable across regions of differing "
        "yield levels. It is computed as, for each year, the RMSE across "
        "regions divided by the crop's mean observed yield, then averaged over "
        "the leave-one-year-out hindcast years. Each bar is one model's "
        "rRMSEp, sorted best-first; the whisker is plus/minus one standard "
        "deviation across years."
    ),
    "predicted_table": (
        "Per-region forecast for the best model by rRMSEp: the predicted yield "
        "alongside the last observed yield (and its year) and the recent median "
        "yield for context."
    ),
}


def _desc(key):
    """How-to-read text for ``key``: prefer the lite copy, fall back to
    :data:`geocif.report._DESC` (e.g. ``predicted_map`` / ``outlook_map``)."""
    return _LITE_DESC.get(key) or _DESC.get(key, "")


# ---------------------------------------------------------------------------
# References / data sources — rendered as the final TOC-registered section.
# Each entry: (label, one-line description, URL). Edit here to add sources.
# ---------------------------------------------------------------------------

_REFERENCES = [
    (
        "HarvestStat Africa",
        "Subnational crop yield, area and production statistics — the yield "
        "data used to train and validate the models. Nature Scientific Data (2025).",
        "https://www.nature.com/articles/s41597-025-05001-z",
    ),
    (
        "Crop calendars",
        "GEOGLAM Crop Monitor — AgMet & Earth-observation indicators; defines "
        "each crop's growing-season window per region.",
        "https://www.cropmonitor.org/agmet-eo-indicators-explained",
    ),
    (
        "Crop masks",
        "Cropland / crop-type masks used to aggregate the Earth-observation "
        "indicators to each admin region. Nature Scientific Data (2023).",
        "https://www.nature.com/articles/s41597-023-02047-9",
    ),
]


# ---------------------------------------------------------------------------
# "About GEOCIF" intro section — plain-language summary of the model, drawn
# from the GEOCIF description document. Rendered as the first numbered section.
# ---------------------------------------------------------------------------

_ABOUT_GEOCIF = [
    "GEOCIF (Global Earth Observations for Crop Inventory Forecasting) is a "
    "machine-learning yield-forecasting system. It ingests Earth-observation "
    "(EO) datasets and applies the Climatic-Impact-Driver (CID) framework to "
    "derive indicators of both mean climate conditions (e.g. seasonal "
    "temperature and precipitation) and extreme events (heat waves, cold snaps, "
    "droughts, and compound hazards).",
    "These CID indicators, together with vegetation-health metrics, feed "
    "Tabular Foundation Models and CatBoost-based ensembles that learn "
    "crop-specific, regionally tuned relationships between climate, vegetation, "
    "and historical yield. The system delivers probabilistic, admin-level "
    "(county / state) yield forecasts two to three months before harvest, with "
    "explainable-AI diagnostics that highlight the dominant CIDs driving each "
    "forecast.",
    "GEOCIF has been operationally deployed for the Food and Agriculture "
    "Organization (FAO), the Alliance for a Green Revolution in Africa (AGRA), "
    "and the United Nations Office on Drugs and Crime (UNODC). The methodology "
    "references are listed at the end of this report.",
]


# ---------------------------------------------------------------------------
# GEOCIF / methodology references — rendered under the References section
# (emphasis on the underlying method papers). Each entry: (citation, url|'').
# ---------------------------------------------------------------------------

_METHOD_REFERENCES = [
    (
        "Sahajpal, R., Fontana, L., Lafluf, P., Leale, G., Puricelli, E., "
        "O'Neill, D., Hosseini, M., Varela, M., and Becker-Reshef, I. (2020). "
        "Using Machine-Learning Models for Field-Scale Crop Yield and Condition "
        "Modeling in Argentina.",
        "https://doi.org/10.31223/x52595",
    ),
    (
        "Sahajpal, R., and Coutu, S. (2020). Optimizing Crop Cut Collection for "
        "Determining Field-Scale Yields in an Insurance Context.",
        "https://doi.org/10.31223/x5j59h",
    ),
    (
        "Nhu, A. N., Sahajpal, R., Justice, C., and Becker-Reshef, I. (2023). "
        "Improving State-Level Wheat Yield Forecasts in Kazakhstan on GEOGLAM's "
        "EO Data by Leveraging a Simple Spatial-Aware Technique. arXiv:2306.04646.",
        "https://arxiv.org/abs/2306.04646",
    ),
    (
        "Becker-Reshef, I., Bandaru, V., Barker, B., Coutu, S., Deines, J. M., "
        "et al. (2022). The NASA Harvest Program on Agriculture and Food "
        "Security. In Remote Sensing of Agriculture and Land Cover / Land Use "
        "Changes in South and Southeast Asian Countries (pp. 53-80). Springer.",
        "",
    ),
    (
        "Ostroumova, L., Gusev, G., Vorobev, A., Dorogush, A. V., and Gulin, A. "
        "(2017). CatBoost: Unbiased Boosting with Categorical Features. "
        "Neural Information Processing Systems, 31, 6639-6649.",
        "",
    ),
]


# ---------------------------------------------------------------------------
# TOC heading — lifted verbatim from report.generate_report so the two-pass
# multiBuild resolves page numbers and the entries are clickable bookmarks.
# ---------------------------------------------------------------------------

if _HAS_REPORTLAB:

    class _TOCHeading(Paragraph):
        """Paragraph that notifies the TOC when drawn."""

        def __init__(self, text, style, level=0):
            super().__init__(text, style)
            self._toc_level = level
            self._toc_text = text

        def draw(self):
            super().draw()
            key = f"toc-{self._toc_text}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(self._toc_text, key, level=self._toc_level)
            # Notify TOC so it picks up this heading
            self.canv._doctemplate.notify(
                "TOCEntry",
                (self._toc_level, self._toc_text, self.canv.getPageNumber(), key),
            )


class _LiteReport:
    """Small reportlab builder for a single per-country lite PDF.

    Encapsulates the styles, elements list, logos, footer, cover, TOC and
    numbered-section/image helpers lifted from
    :func:`geocif.report.generate_report`.
    """

    def __init__(self, pdf_path, parser):
        self.pdf_path = Path(pdf_path)
        self.page_w = A4[0] - 3 * cm
        self.page_h = A4[1]
        self.elements = []
        self.section_counter = 0

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            "SectionTitle", parent=styles["Heading1"],
            fontSize=16, spaceAfter=12, textColor=rl_colors.HexColor("#1a5276"),
        ))
        styles.add(ParagraphStyle(
            "CoverTitle", parent=styles["Title"],
            fontSize=26, alignment=TA_CENTER, spaceAfter=20,
        ))
        styles.add(ParagraphStyle(
            "CoverSubtitle", parent=styles["Normal"],
            fontSize=14, alignment=TA_CENTER, spaceAfter=8,
            textColor=rl_colors.HexColor("#555555"),
        ))
        styles.add(ParagraphStyle(
            "Description", parent=styles["Normal"],
            fontSize=9, spaceAfter=6, textColor=rl_colors.HexColor("#666666"),
            fontName="Helvetica-Oblique",
        ))
        self.styles = styles

        # ---- Logos ----
        dir_images = Path(parser.get("PATHS", "dir_metadata", fallback="")) / "images"
        self.logo_harvest = dir_images / parser.get(
            "AGMET", "logo_harvest", fallback="harvest.png")
        self.logo_geoglam = dir_images / parser.get(
            "AGMET", "logo_geoglam", fallback="geoglam.png")

    # ---- Page template with footer (logos + page number) ----
    def _footer(self, canvas, doc):
        canvas.saveState()
        # Page number
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(rl_colors.HexColor("#999999"))
        canvas.drawCentredString(A4[0] / 2, 0.8 * cm, f"Page {doc.page}")
        # Logos in footer — both on the left side, side by side
        logo_h = 0.4 * inch
        max_logo_w = 1.2 * inch
        y_logo = 0.3 * cm
        x_cursor = 1.5 * cm
        for lp in [self.logo_harvest, self.logo_geoglam]:
            if lp.exists():
                try:
                    from PIL import Image as PILImage
                    with PILImage.open(lp) as pil_img:
                        iw, ih = pil_img.size
                    aspect = iw / ih
                    w = min(logo_h * aspect, max_logo_w)
                    h = w / aspect
                    canvas.drawImage(str(lp), x_cursor, y_logo, width=w, height=h,
                                     preserveAspectRatio=True, mask="auto")
                    x_cursor += w + 0.3 * cm
                except Exception:
                    pass
        canvas.restoreState()

    def add_image(self, path, caption=None, description=None, page_break_before=False):
        """Add an image scaled to fit, preserving aspect ratio, followed by an
        italic caption and a grey oblique 'how to read' description. The image
        and its caption/description are wrapped in a ``KeepTogether`` so the
        caption never orphans onto a separate page from its figure. Pass
        ``page_break_before=True`` to start the figure on a fresh page."""
        path = Path(path)
        if not path.exists():
            return
        max_w = self.page_w
        max_h = self.page_h * 0.42

        try:
            from PIL import Image as PILImage
            with PILImage.open(path) as pil_img:
                img_w, img_h = pil_img.size
            aspect = img_w / img_h
            if max_w / aspect <= max_h:
                w = max_w
                h = max_w / aspect
            else:
                h = max_h
                w = max_h * aspect
        except ImportError:
            w, h = max_w, max_h

        block = [RLImage(str(path), width=w, height=h)]
        if caption:
            block.append(Spacer(1, 4))
            block.append(Paragraph(caption, self.styles["Italic"]))
        if description:
            block.append(Spacer(1, 4))
            block.append(Paragraph(description, self.styles["Description"]))
        if page_break_before:
            self.elements.append(PageBreak())
        self.elements.append(KeepTogether(block))
        self.elements.append(Spacer(1, 12))

    def add_table(self, header, rows, caption=None, description=None,
                  page_break_before=True):
        """Add a native reportlab :class:`LongTable` (paginates across pages,
        repeating the header row) followed by an italic caption and a grey
        oblique 'how to read' description. A LongTable that spans pages must
        NOT be wrapped in ``KeepTogether`` (which forces a single frame), so the
        table is appended directly; only the caption/description follow it.

        ``header`` is a list of column labels; ``rows`` a list of row lists
        (already string-formatted). Pass ``page_break_before=True`` (the
        default) to start the table on a fresh page."""
        if not rows:
            return
        ncols = len(header)
        # Header + Region cells are wrapping Paragraphs so long labels (e.g.
        # "Predicted yield (Mg/ha)") and long region names wrap WITHIN the
        # column instead of overflowing into their neighbours (the previous
        # plain-string header cells overlapped). Numeric cells stay plain
        # strings, right-aligned via the TableStyle.
        hdr_l = ParagraphStyle(
            "tblHeadL", parent=self.styles["Normal"], fontSize=8, leading=9,
            fontName="Helvetica-Bold", textColor=rl_colors.white, alignment=TA_LEFT)
        hdr_r = ParagraphStyle("tblHeadR", parent=hdr_l, alignment=TA_RIGHT)
        cell_l = ParagraphStyle(
            "tblCellL", parent=self.styles["Normal"], fontSize=8, leading=9,
            alignment=TA_LEFT)
        head_row = [Paragraph(str(header[0]), hdr_l)] + \
            [Paragraph(str(h), hdr_r) for h in header[1:]]
        data = [head_row]
        for r in rows:
            data.append([Paragraph(str(r[0]), cell_l)] + [str(c) for c in r[1:]])
        # Narrow the first (Region) column so the numeric columns keep enough
        # width for their (now wrapping) headers.
        if ncols <= 1:
            col_widths = [self.page_w]
        elif ncols == 2:
            col_widths = [self.page_w * 0.42, self.page_w * 0.58]
        else:
            first = self.page_w * 0.26
            rest = (self.page_w - first) / (ncols - 1)
            col_widths = [first] + [rest] * (ncols - 1)

        table = LongTable(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#1a5276")),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.25, rl_colors.HexColor("#bbbbbb")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [rl_colors.white, rl_colors.HexColor("#f2f6f9")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            # Numeric data cells (plain strings) right-aligned; Region + all
            # header cells are Paragraphs carrying their own alignment.
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))

        if page_break_before:
            self.elements.append(PageBreak())
        self.elements.append(table)
        if caption:
            self.elements.append(Spacer(1, 4))
            self.elements.append(Paragraph(caption, self.styles["Italic"]))
        if description:
            self.elements.append(Spacer(1, 4))
            self.elements.append(Paragraph(description, self.styles["Description"]))
        self.elements.append(Spacer(1, 12))

    def add_cover(self, title, subtitle_lines):
        self.elements.append(Spacer(1, 2.5 * inch))
        self.elements.append(Paragraph(title, self.styles["CoverTitle"]))
        for line in subtitle_lines:
            self.elements.append(Paragraph(line, self.styles["CoverSubtitle"]))

    def add_toc(self):
        self.elements.append(PageBreak())
        self.elements.append(Paragraph("Table of Contents", self.styles["SectionTitle"]))
        self.elements.append(Spacer(1, 12))
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle("TOCLevel0", parent=self.styles["Normal"], fontSize=12,
                           leftIndent=0, spaceAfter=6,
                           textColor=rl_colors.HexColor("#1a5276")),
        ]
        self.elements.append(toc)

    def section(self, title):
        """Numbered section heading registered in the TOC (clickable)."""
        self.section_counter += 1
        self.elements.append(PageBreak())
        numbered = f"{self.section_counter}. {title}"
        self.elements.append(_TOCHeading(numbered, self.styles["SectionTitle"], level=0))
        self.elements.append(Spacer(1, 8))

    def add_about(self, paragraphs):
        """Intro 'About GEOCIF' section (registered in the TOC)."""
        self.section("About GEOCIF")
        for para in paragraphs:
            self.elements.append(Paragraph(para, self.styles["Normal"]))
            self.elements.append(Spacer(1, 8))

    def add_references(self, references, method_references=None):
        """Final 'References / Data sources' section (registered in the TOC)
        with clickable hyperlinks. ``references`` = list of (label, desc, url);
        ``method_references`` = optional list of (citation, url|'') rendered under
        a 'GEOCIF & methodology' sub-heading."""
        self.section("References / Data sources")
        for label, desc, url in references:
            self.elements.append(
                Paragraph(f"<b>{label}</b> &mdash; {desc}", self.styles["Normal"]))
            self.elements.append(
                Paragraph(f'<a href="{url}" color="blue">{url}</a>',
                          self.styles["Normal"]))
            self.elements.append(Spacer(1, 12))
        if method_references:
            self.elements.append(Spacer(1, 6))
            self.elements.append(
                Paragraph("<b>GEOCIF &amp; methodology</b>", self.styles["Normal"]))
            self.elements.append(Spacer(1, 8))
            for citation, url in method_references:
                if url:
                    self.elements.append(Paragraph(
                        f'{citation} <a href="{url}" color="blue">{url}</a>',
                        self.styles["Normal"]))
                else:
                    self.elements.append(Paragraph(citation, self.styles["Normal"]))
                self.elements.append(Spacer(1, 8))

    def build(self):
        doc = SimpleDocTemplate(
            str(self.pdf_path),
            pagesize=A4,
            topMargin=1.5 * cm,
            bottomMargin=2 * cm,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
        )
        # Two-pass build resolves TOC page numbers.
        doc.multiBuild(self.elements, onFirstPage=self._footer, onLaterPages=self._footer)


# ---------------------------------------------------------------------------
# Resolution helpers
# ---------------------------------------------------------------------------

def _country_crops(parser, country, fallback_crops):
    """Per-country crops from ``[country] crops`` (ast.literal_eval), mirroring
    yield_outlook; falls back to the passed global crops list on any failure."""
    try:
        parsed = ast.literal_eval(parser.get(country, "crops"))
        if isinstance(parsed, (list, tuple)) and parsed:
            return list(parsed)
    except Exception:
        pass
    return list(fallback_crops)


def _best_model(dir_outlook, country, crop, models):
    """Best model for (country, crop) = row with min ``rrmsep_mean`` in the
    rRMSEp ranking CSV. Falls back to ``models[0]`` if the CSV is missing/empty.
    """
    csv_path = (
        dir_outlook / "csvs" / "model_comparison" / country
        / f"rrmsep_summary_{country}_{crop}.csv"
    )
    fallback = models[0] if models else "model"
    if not csv_path.is_file():
        logger.warning(
            f"rRMSEp ranking CSV not found for {country}/{crop} "
            f"({csv_path}); falling back to best model = {fallback}"
        )
        return fallback
    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            f"Could not read rRMSEp ranking CSV {csv_path}: {exc}; "
            f"falling back to best model = {fallback}"
        )
        return fallback
    if df.empty or "rrmsep_mean" not in df.columns or "Model" not in df.columns:
        logger.warning(
            f"rRMSEp ranking CSV {csv_path} empty or missing Model/rrmsep_mean "
            f"columns; falling back to best model = {fallback}"
        )
        return fallback
    # Restrict to the real candidate models. The ranking CSV also lists blend /
    # ensemble pseudo-models (e.g. inv_rmse, bma, ensemble) which can top the
    # table but do not have the full per-model map set (no predicted_yield map),
    # so selecting one leaves an incomplete section. Rank among ``models`` only.
    if models:
        df_real = df[df["Model"].isin(models)]
        if not df_real.empty:
            df = df_real
    best_row = df.loc[df["rrmsep_mean"].idxmin()]
    best = str(best_row["Model"])
    logger.info(
        f"Best model for {country}/{crop} by rRMSEp: {best} "
        f"(rrmsep_mean={best_row['rrmsep_mean']:.2f})"
    )
    return best


def _first_map(base_dir, prefix, country, crop, best, year,
               exclude_path_substr=(), exclude_name_substr=()):
    """First PNG under ``base_dir`` (recursive) matching the outlook map naming
    convention, skipping any whose path/name contains an excluded token.

    Tries the spec-literal single-country pattern first, then a country-token
    wildcard so combined-country filenames (``country1_country2``) still match.
    """
    base = Path(base_dir)
    if not base.exists():
        return None
    patterns = [
        f"{prefix}_{country}_{crop}_{best}_*_{year}.png",  # single-country
        f"{prefix}_*_{crop}_{best}_*_{year}.png",          # multi-country token
    ]
    for pattern in patterns:
        for match in sorted(base.rglob(pattern)):
            path_str = str(match).replace("\\", "/")
            if any(sub in path_str for sub in exclude_path_substr):
                continue
            if any(sub in match.name for sub in exclude_name_substr):
                continue
            return match
    return None


def _scatter_plot(dir_outlook, country, crop, best):
    """Best-model predicted-vs-observed scatter PNG at
    ``plots/{best}/{country}/scatter_{country}_{crop}_{best}.png``.

    Excludes the national (``scatter_national_``) and per-year
    (``scatter_by_year/``) variants. Returns the :class:`~pathlib.Path` or
    ``None`` when absent."""
    base = Path(dir_outlook) / "plots" / best / country / crop
    if not base.exists():
        return None
    exact = base / f"scatter_{country}_{crop}_{best}.png"
    if exact.is_file():
        return exact
    # Fallback glob (still direct children only), skipping the excluded twins.
    for match in sorted(base.glob(f"scatter_{country}_{crop}_{best}*.png")):
        path_str = str(match).replace("\\", "/")
        if "scatter_national_" in match.name or "scatter_by_year" in path_str:
            continue
        return match
    return None


# ---------------------------------------------------------------------------
# Season names — resolve CID Season integers (1, 2) to HarvestStat season_name
# strings (e.g. Gu / Deyr / Wet) for the section title and the yield table.
# ---------------------------------------------------------------------------

# Canonical outlook-DB column names (mirror yield_outlook._CANON_*). Kept as
# local literals so this module needs no import of the heavy yield_outlook
# module. The forecast year has predicted / last-observed / median populated,
# while CI + current-year observed are NULL (estimate_ci=False), so those are
# deliberately NOT read here.
_PRED_COL = "Predicted Yield (tn per ha)"
_LAST_OBS_YIELD_COL = "Last Observed Yield (tn per ha)"
_LAST_OBS_YEAR_COL = "Last Observed Year"
_MEDIAN_YIELD_COL = "Median Yield (tn per ha)"

# Module-level cache so the HarvestStat CSV is read at most once, even across
# many (country, crop) calls. Keyed by the resolved CSV path string.
_HVSTAT_CACHE = {}


def _load_hvstat(parser):
    """Load + cache the HarvestStat Africa CSV (``country``, ``product``,
    ``season_name`` columns only). Returns a DataFrame, or ``None`` if the path
    is unconfigured / the file is missing / it cannot be read. Read at most once
    per resolved path."""
    try:
        csv_path = (
            Path(parser.get("PATHS", "dir_production_statistics"))
            / "hvstat_africa_data_v1.0.csv"
        )
    except Exception:  # noqa: BLE001 — missing section/option
        return None
    key = str(csv_path)
    if key not in _HVSTAT_CACHE:
        df = None
        if csv_path.is_file():
            try:
                df = pd.read_csv(
                    csv_path,
                    usecols=lambda c: c in ("country", "product", "season_name"),
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"Could not read HarvestStat CSV {csv_path}: {exc}")
                df = None
        else:
            logger.warning(
                f"HarvestStat CSV not found ({csv_path}); "
                f"season names unavailable"
            )
        _HVSTAT_CACHE[key] = df
    return _HVSTAT_CACHE[key]


def _hvstat_season_set(parser, country, crop):
    """Set of HarvestStat ``season_name`` values for a (country, crop).

    Matches country case-insensitively (underscores treated as spaces) and crop
    by ``crop.replace("_", " ").title()``. Returns an empty set when the CSV or
    the requested columns are unavailable."""
    df = _load_hvstat(parser)
    if df is None or df.empty:
        return set()
    if not {"country", "product", "season_name"}.issubset(df.columns):
        return set()
    product = crop.replace("_", " ").title()
    country_norm = country.lower().replace("_", " ").strip()
    country_col = (
        df["country"].astype(str).str.lower().str.replace("_", " ", regex=False).str.strip()
    )
    product_col = df["product"].astype(str).str.strip().str.lower()
    mask = (country_col == country_norm) & (product_col == product.lower())
    return set(df.loc[mask, "season_name"].dropna().astype(str).unique())


def _resolve_season_name(available, season):
    """First priority-list name present in ``available`` for CID ``season``:
    season 1 -> PRIMARY_SEASON_NAMES, else SECONDARY_SEASON_NAMES. ``None`` if
    none match."""
    from geocif.utils import PRIMARY_SEASON_NAMES, SECONDARY_SEASON_NAMES

    priority = PRIMARY_SEASON_NAMES if int(season) == 1 else SECONDARY_SEASON_NAMES
    return next((n for n in priority if n in available), None)


def _season_names(parser, country, crop, seasons_present):
    """Ordered HarvestStat ``season_name`` strings for the CID Season integers
    in ``seasons_present``. Season 1 maps to the first
    :data:`geocif.utils.PRIMARY_SEASON_NAMES` entry present in the HarvestStat
    season_names for that (country, crop); season 2 to the first
    ``SECONDARY_SEASON_NAMES`` entry. Unresolvable seasons are skipped; returns
    ``[]`` when nothing resolves (title then omits the season suffix)."""
    available = _hvstat_season_set(parser, country, crop)
    if not available:
        return []
    names = []
    for season in seasons_present:
        picked = _resolve_season_name(available, season)
        if picked is not None:
            names.append(picked)
        else:
            logger.debug(
                f"No HarvestStat season_name for {country}/{crop} season {season}"
            )
    return names


def _season_suffix(names):
    """Parenthesised season suffix for the section title: '' for no names,
    '(Wet Season)' for one, '(Gu & Deyr Seasons)' for several."""
    if not names:
        return ""
    label = " & ".join(names)
    word = "Season" if len(names) == 1 else "Seasons"
    return f" ({label} {word})"


def _config_seasons(parser, country):
    """CID Season integers from the ``[country] seasons`` config list (fallback
    when the outlook DB is unavailable). Returns a sorted list, or ``[]`` on any
    failure."""
    try:
        parsed = ast.literal_eval(parser.get(country, "seasons"))
        if isinstance(parsed, (list, tuple)) and parsed:
            return sorted({int(s) for s in parsed})
    except Exception:  # noqa: BLE001
        pass
    return []


# ---------------------------------------------------------------------------
# Per-region predicted-yield table — read the forecast-year predictions for the
# best model out of the outlook SQLite DB.
# ---------------------------------------------------------------------------

def _read_predicted_yield_table(outlook_db, country, crop, best, year):
    """Read the forecast-year (``year``) per-region predictions for the best
    model from table ``{country}_{crop}`` in the outlook SQLite DB.

    Returns ``(df, seasons_present)`` where ``df`` has columns ``Region``,
    (optionally) ``Season``, ``Predicted Yield (tn per ha)`` and — when present
    in the table — ``Last Observed Yield (tn per ha)``, ``Last Observed Year``
    and ``Median Yield (tn per ha)``. ``seasons_present`` is the sorted list of
    distinct Season integers found. Returns ``(None, [])`` when ``outlook_db``
    is falsy or the DB / table / rows are missing (caller then skips the table
    and falls back for the title)."""
    if not outlook_db:
        return None, []
    import sqlite3

    db_path = Path(outlook_db)
    if not db_path.is_file():
        logger.warning(
            f"Outlook DB not found ({db_path}); skipping predicted-yield table "
            f"for {country}/{crop}"
        )
        return None, []

    table = f"{country}_{crop}"
    con = sqlite3.connect(str(db_path))
    try:
        table_cols = pd.read_sql(
            f'PRAGMA table_info("{table}")', con
        )["name"].tolist()
        if not table_cols:
            logger.warning(
                f"Outlook DB table '{table}' not found; "
                f"skipping predicted-yield table"
            )
            return None, []
        if _PRED_COL not in table_cols:
            logger.warning(
                f"Outlook DB table '{table}' has no '{_PRED_COL}' column; "
                f"skipping predicted-yield table"
            )
            return None, []

        select_cols = ["Region"]
        if "Season" in table_cols:
            select_cols.append("Season")
        select_cols.append(_PRED_COL)
        # Context columns — each guarded so a missing column never crashes the
        # query. Order here == display order (yield, its year, median).
        for extra in (_LAST_OBS_YIELD_COL, _LAST_OBS_YEAR_COL, _MEDIAN_YIELD_COL):
            if extra in table_cols:
                select_cols.append(extra)
        cols_sql = ",".join(f'"{c}"' for c in select_cols)

        where, params = [], []
        if "Harvest Year" in table_cols:
            # Harvest Year is stored as TEXT in some DBs; CAST makes the year
            # filter robust to TEXT/INTEGER storage.
            where.append('CAST("Harvest Year" AS INTEGER) = ?')
            params.append(int(year))
        if "Model" in table_cols:
            where.append('"Model" = ?')
            params.append(best)
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""

        df = pd.read_sql(
            f'SELECT {cols_sql} FROM "{table}"{where_sql}',
            con, params=params if params else None,
        )
    except (pd.errors.DatabaseError, sqlite3.OperationalError) as exc:
        logger.warning(f"Failed to read predicted-yield table '{table}': {exc}")
        return None, []
    finally:
        con.close()

    if df is None or df.empty:
        logger.warning(
            f"No {year} rows for {country}/{crop}/{best} in outlook DB; "
            f"skipping predicted-yield table"
        )
        return None, []

    seasons_present = []
    if "Season" in df.columns:
        seasons = pd.to_numeric(df["Season"], errors="coerce").dropna()
        seasons_present = sorted({int(s) for s in seasons.unique()})
    return df, seasons_present


def _build_yield_table_rows(pred_df, seasons_present, parser, country, crop, unit):
    """Build ``(header, rows)`` for the predicted-yield table.

    Columns: Region, [Season], Predicted yield (``unit``), Last observed yield
    (``unit``), Last obs. year, Median yield (``unit``). Multi-season tables
    keep the Season column (holding the season NAME, e.g. Gu / Deyr);
    single-season tables drop it. Rows are ordered by Season, then by predicted
    yield DESCENDING within season (single-season: predicted yield descending).
    Yields are formatted to 2 decimals and the year to an integer; a NULL value
    renders as a blank cell."""
    df = pred_df.copy()
    for col in (_PRED_COL, _LAST_OBS_YIELD_COL, _MEDIAN_YIELD_COL):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if _LAST_OBS_YEAR_COL in df.columns:
        df[_LAST_OBS_YEAR_COL] = pd.to_numeric(df[_LAST_OBS_YEAR_COL], errors="coerce")

    def _fmt_yld(v):
        return f"{v:.2f}" if pd.notna(v) else ""

    def _fmt_year(v):
        return f"{int(v)}" if pd.notna(v) else ""

    def _context_cells(r):
        return [
            _fmt_yld(r[_LAST_OBS_YIELD_COL]) if _LAST_OBS_YIELD_COL in df.columns else "",
            _fmt_year(r[_LAST_OBS_YEAR_COL]) if _LAST_OBS_YEAR_COL in df.columns else "",
            _fmt_yld(r[_MEDIAN_YIELD_COL]) if _MEDIAN_YIELD_COL in df.columns else "",
        ]

    context_header = [
        f"Last observed yield ({unit})",
        "Last obs. year",
        f"Median yield ({unit})",
    ]

    multi_season = "Season" in df.columns and len(seasons_present) > 1

    if multi_season:
        df["Season"] = pd.to_numeric(df["Season"], errors="coerce").astype("Int64")
        available = _hvstat_season_set(parser, country, crop)
        name_map = {}
        for s in seasons_present:
            picked = _resolve_season_name(available, s)
            name_map[s] = picked if picked is not None else f"Season {s}"
        df = df.sort_values(
            ["Season", _PRED_COL], ascending=[True, False], kind="mergesort"
        )
        header = ["Region", "Season", f"Predicted yield ({unit})"] + context_header
        rows = []
        for _, r in df.iterrows():
            season_int = int(r["Season"]) if pd.notna(r["Season"]) else None
            season_lbl = name_map.get(
                season_int, "" if season_int is None else f"Season {season_int}"
            )
            rows.append(
                [str(r["Region"]), season_lbl, _fmt_yld(r[_PRED_COL])]
                + _context_cells(r)
            )
        return header, rows

    df = df.sort_values(_PRED_COL, ascending=False, kind="mergesort")
    header = ["Region", f"Predicted yield ({unit})"] + context_header
    rows = []
    for _, r in df.iterrows():
        rows.append(
            [str(r["Region"]), _fmt_yld(r[_PRED_COL])] + _context_cells(r)
        )
    return header, rows


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_report_lite(
    dir_outlook,
    parser,
    current_year,
    countries,
    crops,
    models,
    dir_output=None,
    outlook_db=None,
):
    """Generate one lightweight PDF per country from yield-outlook outputs.

    When ``outlook_db`` points at a readable outlook SQLite DB, each crop
    section also gains a per-region predicted-yield table (forecast year, best
    model) and the distinct Season integers found there drive the section-title
    season suffix. When it is ``None`` / unreadable the table is skipped and the
    suffix falls back to the ``[country] seasons`` config (or is omitted).

    Returns the list of written PDF :class:`pathlib.Path` objects (empty if
    reportlab is unavailable).
    """
    if not _HAS_REPORTLAB:
        logger.warning("reportlab not installed — skipping lite PDF report generation")
        return []

    dir_outlook = Path(dir_outlook)
    if dir_output is None:
        dir_output = dir_outlook
    dir_output = Path(dir_output)
    dir_output.mkdir(parents=True, exist_ok=True)

    today_str = ar.utcnow().to("America/New_York").format("MMMM DD, YYYY HH:mm")
    # Display unit for yields (values are identical; the DB columns stay
    # "(tn per ha)"). Read once — used in captions + the table header.
    unit = parser.get("ML", "yield_units", fallback="Mg/ha")
    written = []

    for country in countries:
        country_lower = country.lower().replace(" ", "_")
        country_display = country.title().replace("_", " ")
        country_crops = _country_crops(parser, country, crops)
        crops_display = [c.title().replace("_", " ") for c in country_crops]

        pdf_path = dir_output / f"yield_outlook_report_lite_{country_lower}_{current_year}.pdf"
        logger.info(f"Generating lite PDF report: {pdf_path}")

        report = _LiteReport(pdf_path, parser)

        # ---- Cover ----
        report.add_cover(
            f"GEOCIF Yield Outlook — {country_display} {current_year}",
            [
                f"Crops: {', '.join(crops_display) if crops_display else 'n/a'}",
                f"Models: {', '.join(models) if models else 'n/a'}",
                f"Generated: {today_str}",
                f"GEOCIF version {__version__}",
            ],
        )

        # ---- TOC ----
        report.add_toc()

        # ---- About GEOCIF (intro section) ----
        report.add_about(_ABOUT_GEOCIF)

        # ---- One numbered section per crop ----
        for crop, crop_display in zip(country_crops, crops_display):
            best = _best_model(dir_outlook, country, crop, models)

            # Read the forecast-year per-region predictions (best model). The
            # distinct Season integers found here drive the title suffix; on
            # miss we fall back to the [country] seasons config.
            pred_df, seasons_present = _read_predicted_yield_table(
                outlook_db, country, crop, best, current_year
            )
            if not seasons_present:
                seasons_present = _config_seasons(parser, country)
            season_names = (
                _season_names(parser, country, crop, seasons_present)
                if seasons_present else []
            )
            suffix = _season_suffix(season_names)

            report.section(f"{country_display} — {crop_display}{suffix}")

            base_maps = dir_outlook / "maps" / best / country / crop

            # Accuracy first, then the forecast. Order within a section:
            #   (a) rRMSEp scorecard  (b) best-model scatter
            #   (c) predicted-yield table  (d) predicted-yield map
            #   (e) outlook-index map
            # (a) sits under the section heading; (b)-(e) each start a new page.

            # (a) rRMSEp scorecard
            scorecard = (
                dir_outlook / "plots" / "model_comparison" / country
                / f"rrmsep_summary_{country}_{crop}.png"
            )
            score_hits = _find_images(scorecard.parent, scorecard.name)
            if score_hits:
                report.add_image(
                    score_hits[0],
                    caption=f"Model accuracy — rRMSEp, {country_display} {crop_display}.",
                    description=_desc("rrmsep"),
                )
            else:
                logger.warning(
                    f"No rRMSEp scorecard for {country}/{crop} "
                    f"({scorecard}); skipping image"
                )

            # (b) Best-model predicted-vs-observed scatter (accuracy)
            scatter = _scatter_plot(dir_outlook, country, crop, best)
            if scatter is not None:
                report.add_image(
                    scatter,
                    caption=f"Predicted vs. observed {crop_display} yield — {best}.",
                    description=_desc("scatter"),
                    page_break_before=True,
                )
            else:
                logger.warning(
                    f"No best-model scatter for {country}/{crop}/{best} "
                    f"(plots/{best}/{country}); skipping image"
                )

            # (c) Per-region predicted-yield TABLE (own page)
            if pred_df is not None and not pred_df.empty:
                header, table_rows = _build_yield_table_rows(
                    pred_df, seasons_present, parser, country, crop, unit
                )
                report.add_table(
                    header, table_rows,
                    caption=(
                        f"Predicted {crop_display} yield ({unit}) by region, "
                        f"{current_year} — {best}."
                    ),
                    description=_desc("predicted_table"),
                    page_break_before=True,
                )
            else:
                logger.warning(
                    f"No predicted-yield table for {country}/{crop}/{best} "
                    f"({current_year}); skipping table"
                )

            # (d) Predicted-yield map (sequential)
            pred = _first_map(base_maps, "predicted_yield", country, crop, best,
                              current_year)
            if pred is not None:
                report.add_image(
                    pred,
                    caption=(
                        f"Predicted {crop_display} yield ({unit}), {current_year} "
                        f"— best model by rRMSEp: {best}."
                    ),
                    description=_desc("predicted_yield"),
                    page_break_before=True,
                )
            else:
                logger.warning(
                    f"No predicted-yield map for {country}/{crop}/{best} "
                    f"({current_year}) under {base_maps}; skipping image"
                )

            # (e) Non-filtered outlook-index map (diverging) — exclude the
            # obs_anomaly variants and the *_filtered twins.
            outlook = _first_map(
                base_maps, "yield_outlook", country, crop, best, current_year,
                exclude_path_substr=("obs_anomaly",),
                exclude_name_substr=("_filtered",),
            )
            if outlook is not None:
                report.add_image(
                    outlook,
                    caption=f"Yield outlook index, {current_year} — {best}.",
                    description=_desc("outlook_index").format(year=current_year),
                    page_break_before=True,
                )
            else:
                logger.warning(
                    f"No non-filtered outlook-index map for {country}/{crop}/{best} "
                    f"({current_year}) under {base_maps}; skipping image"
                )

        # ---- References / Data sources (final section) ----
        report.add_references(_REFERENCES, _METHOD_REFERENCES)

        # ---- Build ----
        try:
            report.build()
            logger.info(f"Lite report saved to {pdf_path}")
            written.append(pdf_path)
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Failed to build lite PDF report for {country}: {exc}")

    return written
