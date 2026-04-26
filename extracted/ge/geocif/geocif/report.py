"""PDF Report Generator for Yield Outlook.

Compiles yield outlook maps, diagnostic plots, agmet graphics, and
model comparison into a single professional PDF report.

Usage::

    from geocif.report import generate_report
    generate_report(dir_outlook, parser, current_year, ...)
"""

import logging
import os
from pathlib import Path

import arrow as ar
import pandas as pd

from geocif import __version__

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Section descriptions — generic explanations for each graphic type
# ---------------------------------------------------------------------------

_DESC = {
    "yield_table": (
        "This table shows the predicted yield (tn/ha) for each region with "
        "confidence intervals (lower CI and upper CI). Regions are ordered "
        "by their share of national production."
    ),
    "yield_ci": (
        "The forest plot shows the predicted yield for the current season "
        "(blue dots with horizontal error bars representing confidence "
        "intervals). Black diamond markers show observed yields from the "
        "last 5 available years for comparison."
    ),
    "outlook_map": (
        "This choropleth map shows the forecast yield as a percentage "
        "departure from the historical mean. Green indicates above-average "
        "and red/orange indicates below-average expected yields."
    ),
    "predicted_map": (
        "This map shows the absolute predicted yield (tn/ha) for the "
        "current forecast season. Darker shades indicate higher yields."
    ),
    "scatter": (
        "The scatter plot shows observed vs. predicted yield across all "
        "hindcast years. Points close to the diagonal line indicate good "
        "model performance. R², RMSE, and MAPE metrics are annotated."
    ),
    "mape_bar": (
        "This horizontal bar chart shows the Mean Absolute Percentage Error "
        "(MAPE) for each region. Lower values indicate better model "
        "accuracy. Regions are labeled with their share of national "
        "production in parentheses."
    ),
    "mape_year": (
        "This bar chart shows how model accuracy (MAPE) varies across "
        "years. The dashed line indicates a 20% MAPE threshold. Years "
        "with higher bars had larger prediction errors."
    ),
    "mape_map": (
        "This choropleth map shows the spatial distribution of MAPE "
        "across regions. Darker shades indicate higher prediction errors."
    ),
    "combined": (
        "This combined view shows the predicted yield map alongside a "
        "MAPE bar chart, allowing comparison of where yields are highest "
        "and where model accuracy is best or worst."
    ),
    "progression": (
        "These progression plots show how model accuracy evolves as more "
        "months of data become available during the growing season. Each "
        "line represents a region, with the bold black line showing the "
        "area-weighted national average."
    ),
    "model_comparison": (
        "These grouped bar charts compare model performance across "
        "regions and years. The legend shows each model's national "
        "area-weighted metric in parentheses."
    ),
    "best_model_map": (
        "This map shows which model has the lowest MAPE (best accuracy) "
        "in each region. Consistent colors are used across all comparison "
        "plots."
    ),
    "agmet": (
        "The agricultural meteorology plot shows time-series of climate "
        "and vegetation indicators throughout the growing season, with "
        "crop calendar phases marked. The current season (colored) is "
        "compared against the historical range (gray envelope). "
        "Source: GEOGLAM Crop Monitor Tools (https://cropmonitortools.org/tools/agmet/)."
    ),
    "narrative": (
        "This narrative is generated using AI analysis of model outputs "
        "and the latest Crop Monitor bulletins from GEOGLAM "
        "(https://cropmonitor.org/). It compares model predictions with "
        "reported crop conditions and highlights key climate drivers."
    ),
}


def _find_images(base_dir, pattern="*.png"):
    """Find all PNGs matching pattern under base_dir, sorted."""
    base = Path(base_dir)
    if not base.exists():
        return []
    return sorted(base.glob(pattern))


def _find_agmet_dir(parser, country, crop, season, year):
    """Locate agmet output directory for a country/crop/season/year."""
    dir_output = Path(parser.get("PATHS", "dir_output"))
    category = parser.get(country, "category", fallback="AMIS")
    crop_short = crop[:2]
    folder = f"{crop_short}_s{season}_{year}"

    base = dir_output / "crop_condition"
    if not base.exists():
        return None

    dated_dirs = sorted(base.iterdir(), reverse=True)
    for d in dated_dirs:
        candidate = d / "plots" / category / country / folder / "condition"
        if candidate.exists():
            return candidate
        candidate2 = d / "plots" / category / country / folder
        if candidate2.exists():
            return candidate2

    return None


def generate_report(
    dir_outlook,
    parser,
    current_year,
    countries,
    crops,
    models,
    dir_output=None,
):
    """Generate a PDF report from yield outlook outputs."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import inch, cm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
            PageBreak, Table, TableStyle, KeepTogether,
        )
        from reportlab.platypus.tableofcontents import TableOfContents
        from reportlab.lib import colors as rl_colors
    except ImportError:
        logger.warning("reportlab not installed — skipping PDF report generation")
        return

    dir_outlook = Path(dir_outlook)
    if dir_output is None:
        dir_output = dir_outlook

    pdf_path = Path(dir_output) / f"yield_outlook_report_{current_year}.pdf"
    logger.info(f"Generating PDF report: {pdf_path}")

    page_w = A4[0] - 3 * cm
    page_h = A4[1]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "SectionTitle", parent=styles["Heading1"],
        fontSize=16, spaceAfter=12, textColor=rl_colors.HexColor("#1a5276"),
    ))
    styles.add(ParagraphStyle(
        "SubSection", parent=styles["Heading2"],
        fontSize=13, spaceAfter=8, textColor=rl_colors.HexColor("#2e86c1"),
    ))
    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Title"],
        fontSize=28, alignment=TA_CENTER, spaceAfter=20,
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
    styles.add(ParagraphStyle(
        "Footer", parent=styles["Normal"],
        fontSize=7, alignment=TA_CENTER, textColor=rl_colors.HexColor("#999999"),
    ))

    elements = []
    section_counter = [0]  # mutable for nested functions

    # ---- Logos ----
    dir_images = Path(parser.get("PATHS", "dir_metadata", fallback="")) / "images"
    logo_harvest = dir_images / parser.get("AGMET", "logo_harvest", fallback="harvest.png")
    logo_geoglam = dir_images / parser.get("AGMET", "logo_geoglam", fallback="geoglam.png")

    def _add_image(path, max_width=None, max_height=None, caption=None, description=None):
        """Add an image scaled to fit, preserving aspect ratio."""
        path = Path(path)
        if not path.exists():
            return
        max_w = max_width or page_w
        max_h = max_height or (page_h * 0.42)

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

        img = RLImage(str(path), width=w, height=h)
        elements.append(img)
        if caption:
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(caption, styles["Italic"]))
        if description:
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(description, styles["Description"]))
        elements.append(Spacer(1, 12))

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
                "TOCEntry", (self._toc_level, self._toc_text, self.canv.getPageNumber(), key)
            )

    def _section(title, desc_key=None):
        section_counter[0] += 1
        elements.append(PageBreak())
        numbered = f"{section_counter[0]}. {title}"
        elements.append(_TOCHeading(numbered, styles["SectionTitle"], level=0))
        elements.append(Spacer(1, 8))
        if desc_key and desc_key in _DESC:
            elements.append(Paragraph(_DESC[desc_key], styles["Description"]))
            elements.append(Spacer(1, 6))

    subsection_counter = [0]

    def _subsection(title):
        subsection_counter[0] += 1
        numbered = f"{section_counter[0]}.{subsection_counter[0]} {title}"
        elements.append(Paragraph(numbered, styles["SubSection"]))
        elements.append(Spacer(1, 6))

    def _reset_subsection():
        subsection_counter[0] = 0

    # ---- Page template with footer (logos + page number) ----
    def _footer(canvas, doc):
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
        for lp in [logo_harvest, logo_geoglam]:
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

    # ========================================
    # Cover Page
    # ========================================
    elements.append(Spacer(1, 2.5 * inch))

    elements.append(Paragraph("Crop Yield Forecast Report", styles["CoverTitle"]))

    countries_display = [c.title().replace("_", " ") for c in countries]
    crops_display = [c.title().replace("_", " ") for c in crops]
    today_str = ar.utcnow().to("America/New_York").format("MMMM DD, YYYY")

    for line in [
        f"{'  |  '.join(countries_display)}",
        f"{'  |  '.join(crops_display)}",
        f"Models: {', '.join(models)}",
        f"Forecast Year: {current_year}",
        f"Date: {today_str}",
        f"Generated by GEOCIF (version {__version__})",
    ]:
        elements.append(Paragraph(line, styles["CoverSubtitle"]))

    # ========================================
    # Table of Contents
    # ========================================
    elements.append(PageBreak())
    elements.append(Paragraph("Table of Contents", styles["SectionTitle"]))
    elements.append(Spacer(1, 12))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOCLevel0", parent=styles["Normal"], fontSize=12,
                       leftIndent=0, spaceAfter=6,
                       textColor=rl_colors.HexColor("#1a5276")),
    ]
    elements.append(toc)

    # ========================================
    # AI Narrative
    # ========================================
    from .narrative import generate_narrative

    paragraphs = []
    for model in models:
        for country in countries:
            csv_files = list(dir_outlook.glob(f"yield_outlook_*_{current_year}.csv"))
            yield_data = {}
            metrics_data = {}
            if csv_files:
                try:
                    df_csv = pd.read_csv(csv_files[0])
                    df_model = df_csv[df_csv["Model"] == model] if "Model" in df_csv.columns else df_csv
                    if "current_predicted" in df_model.columns and "Region" in df_model.columns:
                        yield_data = df_model.set_index("Region")["current_predicted"].to_dict()
                    if "outlook_index" in df_model.columns:
                        metrics_data["Mean Outlook Index"] = df_model["outlook_index"].mean()
                except Exception:
                    pass

            category = parser.get(country, "category", fallback="AMIS")
            paragraphs = generate_narrative(
                country, crop=crops[0] if crops else "maize",
                current_year=current_year,
                yield_data=yield_data,
                metrics=metrics_data,
                category=category,
                parser=parser,
            )
            if paragraphs:
                break
        if paragraphs:
            break

    if paragraphs:
        _section("Season Assessment", "narrative")
        _reset_subsection()
        for para in paragraphs:
            elements.append(Paragraph(para, styles["Normal"]))
            elements.append(Spacer(1, 10))

    # ========================================
    # Executive Summary
    # ========================================
    _section("Executive Summary")
    _reset_subsection()

    for model in models:
        for country in countries:
            country_lower = country.lower().replace(" ", "_")
            plot_dir = dir_outlook / "plots" / model / country_lower

            yt = list(plot_dir.glob(f"yield_table_*_{model}.png"))
            if yt:
                _subsection(f"{country.title().replace('_', ' ')} — {model}")
                _add_image(yt[0], caption="Yield forecast summary",
                           description=_DESC["yield_table"])

            ci = list(plot_dir.glob(f"yield_ci_*_{model}.png"))
            if ci:
                _add_image(ci[0], caption="Predicted yield with confidence intervals",
                           description=_DESC["yield_ci"])

    # ========================================
    # Current Season Forecast
    # ========================================
    _section("Current Season Forecast", "outlook_map")
    _reset_subsection()

    for model in models:
        map_dir = dir_outlook / "maps" / model
        _subsection(f"Model: {model}")

        outlook_maps = _find_images(map_dir, f"yield_outlook_*_{current_year}.png")
        for m in outlook_maps[:1]:
            _add_image(m, caption="Yield outlook — % departure from historical mean",
                       description=_DESC["outlook_map"])

        pred_maps = _find_images(map_dir, f"predicted_yield_*_{current_year}.png")
        for m in pred_maps[:1]:
            _add_image(m, caption="Predicted yield (tn/ha)",
                       description=_DESC["predicted_map"])

        obs_dir = map_dir / "obs_anomaly"
        if obs_dir.exists():
            for period_dir in sorted(obs_dir.iterdir()):
                if period_dir.is_dir():
                    obs_maps = _find_images(period_dir, f"yield_outlook_*_{current_year}.png")
                    for m in obs_maps[:1]:
                        _add_image(m, caption=f"Observed anomaly — {period_dir.name}")

    # ========================================
    # Model Performance
    # ========================================
    _section("Model Performance")
    _reset_subsection()

    for model in models:
        for country in countries:
            country_lower = country.lower().replace(" ", "_")
            plot_dir = dir_outlook / "plots" / model / country_lower
            map_dir = dir_outlook / "maps" / model

            _subsection(f"{country.title().replace('_', ' ')} — {model}")

            # Show per-stage scatter plots (in stage subdirectories)
            stage_scatters = []
            if plot_dir.exists():
                for stage_dir in sorted(plot_dir.iterdir()):
                    if stage_dir.is_dir():
                        scatters = sorted(stage_dir.glob(f"scatter_*_{model}*.png"))
                        for s in scatters:
                            stage_scatters.append((stage_dir.name.replace("_", " "), s))
            if stage_scatters:
                for stage_label, s in stage_scatters:
                    _add_image(s, caption=f"Observed vs Predicted — {stage_label}",
                               description=_DESC["scatter"])
            else:
                # Fallback: non-staged scatter in top-level dir
                scatter = list(plot_dir.glob(f"scatter_*_{model}.png"))
                if scatter:
                    _add_image(scatter[0], caption="Observed vs Predicted yield",
                               description=_DESC["scatter"])

            mape_bar = list(plot_dir.glob(f"mape_bar_*_{model}.png"))
            if mape_bar:
                _add_image(mape_bar[0], caption="MAPE by region",
                           description=_DESC["mape_bar"])

            mape_year = list(plot_dir.glob(f"mape_year_*_{model}.png"))
            if mape_year:
                _add_image(mape_year[0], caption="MAPE by year",
                           description=_DESC["mape_year"])

            combined = list(plot_dir.glob(f"combined_*_{model}.png"))
            if combined:
                _add_image(combined[0], caption="Predicted yield map with MAPE by region",
                           description=_DESC["combined"])

            mape_maps = _find_images(map_dir, f"mape_map_*_{model}.png")
            if mape_maps:
                _add_image(mape_maps[0], caption="MAPE choropleth map",
                           description=_DESC["mape_map"])

    # ========================================
    # Multi-Step Progression
    # ========================================
    has_progression = False
    for model in models:
        for country in countries:
            country_lower = country.lower().replace(" ", "_")
            prog_dir = dir_outlook / "plots" / model / country_lower / "progression"
            if prog_dir.exists() and list(prog_dir.glob("*.png")):
                has_progression = True
                break
        if has_progression:
            break

    if has_progression:
        _section("Forecast Skill Progression", "progression")
        _reset_subsection()

        for model in models:
            for country in countries:
                country_lower = country.lower().replace(" ", "_")
                prog_dir = dir_outlook / "plots" / model / country_lower / "progression"
                if not prog_dir.exists():
                    continue

                _subsection(f"{country.title().replace('_', ' ')} — {model}")

                for metric, caption in [
                    ("mape", "MAPE progression across growing season"),
                    ("r2", "R² progression across growing season"),
                    ("rmse", "RMSE progression across growing season"),
                ]:
                    imgs = _find_images(prog_dir, f"{metric}_progression_*.png")
                    for img in imgs[:1]:
                        _add_image(img, caption=caption)

    # ========================================
    # Model Comparison
    # ========================================
    comp_dir = dir_outlook / "plots" / "model_comparison"
    if comp_dir.exists() and len(models) > 1:
        _section("Model Comparison", "model_comparison")
        _reset_subsection()

        for country_dir in sorted(comp_dir.iterdir()):
            if not country_dir.is_dir():
                continue

            _subsection(country_dir.name.title().replace("_", " "))

            best_map = list(country_dir.glob("best_model_map_*.png"))
            if best_map:
                _add_image(best_map[0], caption="Best model by region (lowest MAPE)",
                           description=_DESC["best_model_map"])

            for metric, caption in [
                ("mape", "MAPE comparison"),
                ("rmse", "RMSE comparison"),
                ("r2", "R² comparison"),
            ]:
                by_region = list(country_dir.glob(f"{metric}_by_region_*.png"))
                if by_region:
                    _add_image(by_region[0], caption=f"{caption} by region")

                by_year = list(country_dir.glob(f"{metric}_by_year_*.png"))
                if by_year:
                    _add_image(by_year[0], caption=f"{caption} by year")

    # ========================================
    # Agmet Monitoring
    # ========================================
    agmet_found = False
    for country in countries:
        for crop in crops:
            agmet_dir = _find_agmet_dir(parser, country, crop, 1, current_year)
            if agmet_dir and list(Path(agmet_dir).glob("*.png")):
                agmet_found = True
                break
        if agmet_found:
            break

    if agmet_found:
        _section("Agricultural Meteorology Monitoring", "agmet")
        _reset_subsection()

        for country in countries:
            for crop in crops:
                agmet_dir = _find_agmet_dir(parser, country, crop, 1, current_year)
                if not agmet_dir:
                    continue

                agmet_pngs = sorted(Path(agmet_dir).glob("*.png"))
                if not agmet_pngs:
                    continue

                _subsection(f"{country.title().replace('_', ' ')} — {crop.title().replace('_', ' ')}")

                for png in agmet_pngs:
                    region_name = png.stem.replace("_", " ").title()
                    _add_image(png, caption=f"Agmet monitoring — {region_name}")

    # ========================================
    # Explainability (SHAP)
    # ========================================
    xai_dir = dir_outlook.parent / "xai" if dir_outlook.parent.exists() else None
    if xai_dir and xai_dir.exists():
        shap_pngs = _find_images(xai_dir, "**/*.png")
        if shap_pngs:
            _section("Model Explainability (SHAP)")
            _reset_subsection()
            for png in shap_pngs[:10]:
                _add_image(png, caption=png.stem.replace("_", " ").title())

    # ---- Build PDF with footer ----
    try:
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            topMargin=1.5 * cm,
            bottomMargin=2 * cm,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
        )
        doc.multiBuild(elements, onFirstPage=_footer, onLaterPages=_footer)
        logger.info(f"Report saved to {pdf_path}")
    except Exception as e:
        logger.error(f"Failed to build PDF report: {e}")
