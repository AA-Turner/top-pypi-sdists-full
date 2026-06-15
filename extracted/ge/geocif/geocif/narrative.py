"""AI-generated narrative for yield outlook reports.

Fetches the latest Crop Monitor bulletin from cropmonitor.org,
extracts country-relevant text, and uses Claude API to generate
a narrative comparing model results with reported conditions.

Usage::

    from geocif.narrative import generate_narrative
    paragraphs = generate_narrative(country, crop, current_year, model_summary, ...)
"""

import logging
import os
import re
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

def _fetch_latest_bulletin(country, crop, category="AMIS", n_months=60):
    """Download recent Crop Monitor bulletins for the country and
    combine country-relevant text from each into one block.

    The GEOGLAM Crop Monitor publishes monthly bulletins under stable
    slug URLs containing a ``YYYYMM`` token, one per category:

      - CM4AMIS    https://www.cropmonitor.org/crop-monitor-for-amis-YYYYMM
      - CM4EW      https://www.cropmonitor.org/crop-monitor-for-early-warning-YYYYMM
      - Global CM  https://www.cropmonitor.org/global-crop-monitor-YYYYMM

    The archive index at https://www.cropmonitor.org/archive lists every
    bulletin but renders the (PDF | Web) links via JavaScript, so the
    static HTML doesn't expose the YYYYMM Web URLs we need. We probe
    the slug URLs directly for the past ``n_months``, which is cheap
    and reliable (~60 GETs per category, most returning quickly with
    HTTP 200; missing months 404 silently).

    For each successful month we extract the HTML body text, filter to
    paragraphs that mention the target country, and accumulate the
    findings. Returns ``(combined_text, combined_citation)``.

    Why 60 months: covers the entire growing season for every season
    in the last five years, so Claude can compare current-season
    conditions month-by-month against the same month in prior years.
    """
    try:
        import requests
    except ImportError:
        logger.warning("requests not installed — skipping bulletin fetch")
        return "", ""

    import arrow as ar

    # Try the category-specific slug first; fall back to Global CM if
    # the category-specific URL doesn't resolve for that month.
    if category == "EWCM":
        url_templates = [
            "https://www.cropmonitor.org/crop-monitor-for-early-warning-{ym}",
            "https://www.cropmonitor.org/global-crop-monitor-{ym}",
        ]
    elif category == "AMIS":
        url_templates = [
            "https://www.cropmonitor.org/crop-monitor-for-amis-{ym}",
            "https://www.cropmonitor.org/global-crop-monitor-{ym}",
        ]
    else:
        url_templates = [
            "https://www.cropmonitor.org/global-crop-monitor-{ym}",
        ]

    now = ar.utcnow()
    months_to_try = [now.shift(months=-i).format("YYYYMM") for i in range(n_months)]

    all_texts = {}   # {YYYYMM: country-filtered text}
    all_urls = {}    # {YYYYMM: source URL for citation}

    for ym in months_to_try:
        for url_template in url_templates:
            if ym in all_texts:
                break
            url = url_template.format(ym=ym)
            try:
                resp = requests.get(url, timeout=15)
            except Exception:
                continue
            if resp.status_code != 200:
                continue
            text = _extract_html_text(resp.text)
            country_text = _filter_country_text(text, country)
            if not country_text:
                continue
            all_texts[ym] = country_text
            all_urls[ym] = url
            logger.info(f"Found bulletin {ym}: {url}")

    if not all_texts:
        logger.warning(
            f"No Crop Monitor bulletins resolved for {country} ({category}) "
            f"across the last {n_months} months"
        )
        return "", ""

    parts = []
    sources = []
    for ym in sorted(all_texts.keys(), reverse=True):
        month_name = ar.get(f"{ym}01", "YYYYMMDD").format("MMMM YYYY")
        parts.append(f"[{month_name} Bulletin]\n{all_texts[ym]}")
        sources.append(f"GEOGLAM Crop Monitor, {month_name} ({all_urls[ym]})")
    combined_text = "\n\n".join(parts)
    citation = "; ".join(sources)
    logger.info(
        f"Crop monitor: combined {len(all_texts)} bulletins "
        f"({category}) for {country} into {len(combined_text)} chars"
    )
    return combined_text, citation


def _extract_html_text(html):
    """Extract readable text from an HTML bulletin page."""
    # Remove script/style tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Decode HTML entities
    try:
        import html as html_mod
        text = html_mod.unescape(text)
    except Exception:
        pass
    return text


def _extract_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        pass

    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except ImportError:
        pass

    logger.warning("Neither PyMuPDF nor pdfplumber available for PDF text extraction")
    return ""


def _filter_country_text(text, country):
    """Extract paragraphs mentioning the country from bulletin text."""
    if not text:
        return ""

    country_display = country.replace("_", " ").title()
    lines = text.split("\n")
    relevant = []
    window = 3  # include N lines before/after a mention

    for i, line in enumerate(lines):
        if country_display.lower() in line.lower():
            start = max(0, i - window)
            end = min(len(lines), i + window + 1)
            relevant.extend(lines[start:end])

    if not relevant:
        return ""

    # Deduplicate preserving order
    seen = set()
    unique = []
    for line in relevant:
        if line.strip() and line.strip() not in seen:
            seen.add(line.strip())
            unique.append(line.strip())

    return "\n".join(unique)


def _build_model_summary(yield_data, metrics, top_features=None,
                          historic_yields=None,
                          primary_model_name=None,
                          other_model_predictions=None):
    """Format model results into a text summary for the prompt.

    historic_yields, when given, is a ``{region: {year: yield}}`` dict.
    The block is emitted only for regions that also appear in the
    current-year predictions, so Claude can compare each region's
    forecast against its OWN multi-year history rather than against a
    cross-region average. The historic block enables the "compare with
    region's own historic yields" instruction in the prompt.

    other_model_predictions, when non-empty, is
    ``{model_name: {region: predicted_yield}}`` for additional ML models
    that produced forecasts for the same (country, crop, year). The
    "Other Model Predictions" block lets Claude write a cross-model
    comparison section (which regions agree, where they diverge, by
    how much). primary_model_name identifies which model produced
    ``yield_data`` so Claude can refer to it by name in the narrative.
    """
    parts = []

    primary_label = (
        f" (model: {primary_model_name})" if primary_model_name else ""
    )
    if yield_data:
        parts.append(f"Yield Predictions by Region (current year){primary_label}:")
        for region, pred in yield_data.items():
            parts.append(f"  {region}: {pred:.2f} tn/ha")

    if other_model_predictions:
        parts.append(
            "\nOther Model Predictions (for cross-model comparison; one block "
            "per additional model, same regions where available):"
        )
        for model_name, preds in other_model_predictions.items():
            if not preds:
                continue
            parts.append(f"  {model_name}:")
            # Only emit regions that are also in the primary set so the
            # comparison is apples-to-apples (skip extra regions that
            # one model produced and another didn't).
            for region in (yield_data or {}).keys():
                if region in preds:
                    parts.append(f"    {region}: {preds[region]:.2f} tn/ha")

    if historic_yields:
        parts.append("\nHistoric Yields by Region (tn/ha; recent years):")
        for region in (yield_data or {}).keys():
            hist = historic_yields.get(region) or {}
            if not hist:
                continue
            # Stable chronological order; skip NaN years for compactness.
            year_strs = ", ".join(
                f"{int(y)}: {float(v):.2f}"
                for y, v in sorted(hist.items())
                if v is not None and not _isnan(v)
            )
            if not year_strs:
                continue
            parts.append(f"  {region}: {year_strs}")
            # Mean of available years — handy for Claude to anchor
            # comparisons without recomputing.
            vals = [
                float(v) for v in hist.values()
                if v is not None and not _isnan(v)
            ]
            if len(vals) >= 3:
                mean = sum(vals) / len(vals)
                parts.append(f"    {region} multi-year mean = {mean:.2f} tn/ha")

    if metrics:
        parts.append("\nModel Performance Metrics:")
        for key, val in metrics.items():
            parts.append(f"  {key}: {val:.1f}")

    if top_features:
        parts.append("\nTop Climate Drivers (from SHAP analysis):")
        for feat in top_features[:10]:
            parts.append(f"  {feat}")

    return "\n".join(parts)


def _isnan(x):
    try:
        return x != x  # NaN != NaN by IEEE 754
    except Exception:
        return False


def _fetch_historic_yields(country, crop, regions, current_year, parser,
                            n_years=10, season=1):
    """Pull per-region historical observed yields for the past
    ``n_years`` from the AMIS / HarvestStat path that the rest of
    geocif uses (``geocif.ml.stats.add_statistics``).

    Returns ``{region: {year: yield_tnha}}`` (NaN-tolerant). On any
    failure — parser missing PATHS, file not found, slug mismatch —
    returns ``{}`` so the caller can skip the historic block cleanly
    rather than crash the narrative.
    """
    try:
        import pandas as pd
        from pathlib import Path
        from geocif.ml import stats as ml_stats
        from geocif.agmet import utils as agmet_utils
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"historic-yield fetch skipped — import failed: {exc}")
        return {}

    if not regions or parser is None:
        return {}

    try:
        dir_stats = Path(parser.get("PATHS", "dir_production_statistics"))
    except Exception:
        try:
            dir_metadata = Path(parser.get("PATHS", "dir_metadata"))
            dir_stats = dir_metadata / "production_statistics"
        except Exception:
            logger.warning(
                "historic-yield fetch skipped — could not resolve "
                "dir_production_statistics from parser"
            )
            return {}
    if not dir_stats.exists():
        logger.warning(
            f"historic-yield fetch skipped — {dir_stats} does not exist"
        )
        return {}

    country_str = str(country).replace("_", " ").title()
    try:
        crop_str = agmet_utils.get_crop_name(crop)
    except Exception:
        crop_str = str(crop).replace("_", " ").title()

    # Resolve admin_zone from the country's config section; default to
    # admin_1 since most AMIS / HarvestStat tables are admin-1 keyed.
    country_key = str(country).lower().replace(" ", "_")
    if parser.has_option(country_key, "admin_level"):
        admin_zone = parser.get(country_key, "admin_level")
    elif parser.has_option("DEFAULT", "admin_level"):
        admin_zone = parser.get("DEFAULT", "admin_level")
    else:
        admin_zone = "admin_1"

    years = list(range(current_year - n_years, current_year))
    rows = [
        {"Region": r, "Harvest Year": y, "Season": int(season)}
        for r in regions for y in years
    ]
    if not rows:
        return {}
    df_in = pd.DataFrame(rows)
    try:
        df_out = ml_stats.add_statistics(
            dir_stats=dir_stats,
            df=df_in,
            country=country_str,
            crop=crop_str,
            admin_zone=admin_zone,
            stats=["Yield (tn per ha)"],
            method="",
            parser=parser,
            label=f"narrative-historic/{country}/{crop}",
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"historic-yield fetch failed for {country}/{crop}: {exc}")
        return {}

    out = {}
    yield_col = "Yield (tn per ha)"
    if yield_col not in df_out.columns:
        return {}
    for region in regions:
        sub = df_out[df_out["Region"] == region]
        if sub.empty:
            continue
        # Keep only years with a real (non-NaN) yield value.
        year_yield = {
            int(y): float(v)
            for y, v in zip(sub["Harvest Year"], sub[yield_col])
            if v is not None and not _isnan(v)
        }
        if year_yield:
            out[region] = year_yield
    return out


def generate_narrative(
    country,
    crop,
    current_year,
    yield_data=None,
    metrics=None,
    top_features=None,
    bulletin_text=None,
    category="AMIS",
    parser=None,
    historic_yields=None,
    n_historic_years=10,
    primary_model_name=None,
    other_model_predictions=None,
):
    """Generate an AI narrative about crop conditions and forecast.

    Args:
        country: Country name.
        crop: Crop name.
        current_year: Forecast year.
        yield_data: Dict of {region: predicted_yield}.
        metrics: Dict of metric values (e.g. {"National MAPE": 12.5}).
        top_features: List of top feature names from SHAP.
        bulletin_text: Pre-fetched bulletin text (fetched automatically if None).
        category: Crop monitor category (AMIS or EWCM).
        parser: ConfigParser instance (reads [NARRATIVE] section for
            ``claude_model`` and ``max_tokens``).
        historic_yields: Optional {region: {year: yield}} dict. When
            None and ``parser`` + ``yield_data`` are both available,
            this is auto-fetched via :func:`_fetch_historic_yields`
            for the past ``n_historic_years`` years so Claude can
            compare each region's prediction against its OWN history
            rather than the cross-region average.
        n_historic_years: Look-back window for auto-fetched history.

    Returns:
        List of paragraph strings, or empty list on failure.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        logger.info("ANTHROPIC_API_KEY not set — skipping narrative generation")
        return []

    try:
        import anthropic
    except ImportError:
        logger.warning("anthropic SDK not installed — skipping narrative generation")
        return []

    # Read model settings from config (fallback to sensible defaults).
    # Canonical Claude 4.x IDs:
    #   claude-opus-4-7    — best quality, slower
    #   claude-sonnet-4-6  — balanced (default here)
    #   claude-haiku-4-5   — fastest / cheapest
    # The previous default ("claude-sonnet-4-6-20250514") was a dated
    # alias whose support is being phased out; the un-suffixed alias
    # always points at the latest snapshot of the same family.
    claude_model = "claude-sonnet-4-6"
    # 4000-token default supports a 2-3 page narrative (~800-1500 words,
    # 6-10 paragraphs). Previous 1500-token default targeted 3-4
    # paragraphs and was insufficient for the longer-form report style.
    max_tokens = 4000
    if parser is not None:
        if parser.has_section("NARRATIVE"):
            claude_model = parser.get("NARRATIVE", "claude_model", fallback=claude_model)
            max_tokens = parser.getint("NARRATIVE", "max_tokens", fallback=max_tokens)
    logger.info(f"Narrative LLM: model={claude_model}, max_tokens={max_tokens}")

    # Fetch bulletin if not provided
    bulletin_citation = ""
    if bulletin_text is None:
        bulletin_text, bulletin_citation = _fetch_latest_bulletin(country, crop, category)

    # Auto-fetch per-region historic yields if not provided and we have
    # enough context to look them up. Enables the per-region "compare
    # against its own history" instruction in the prompt below.
    if historic_yields is None and yield_data and parser is not None:
        historic_yields = _fetch_historic_yields(
            country=country, crop=crop,
            regions=list(yield_data.keys()),
            current_year=int(current_year),
            parser=parser, n_years=n_historic_years,
        )
        if historic_yields:
            logger.info(
                f"Historic yields loaded for {len(historic_yields)} regions "
                f"over up to {n_historic_years} years"
            )

    model_summary = _build_model_summary(
        yield_data, metrics, top_features,
        historic_yields=historic_yields,
        primary_model_name=primary_model_name,
        other_model_predictions=other_model_predictions,
    )
    # Track whether we have enough other-model data to instruct Claude
    # to emit the Model Comparison section. Bare empty-dict / single-
    # model runs should NOT produce that section (it would be filler).
    _have_other_models = bool(
        other_model_predictions
        and any(other_model_predictions.values())
    )
    if _have_other_models:
        # Local rebind so the type-checker can see this is non-None;
        # the _have_other_models flag already proves it.
        _others = other_model_predictions or {}
        _primary_label = (
            primary_model_name if primary_model_name else "the primary model"
        )
        _other_names = ", ".join(
            m for m, p in _others.items() if p
        )
        model_comparison_instruction = (
            f"Compare the forecasts produced by the different ML models for "
            f"{current_year}. The primary model is `{_primary_label}` (its "
            f"per-region predictions are in 'Yield Predictions by Region' "
            f"above). The other models — {_other_names} — appear in the "
            f"'Other Model Predictions' block above. Discuss:\n"
            f"  (a) Cross-model agreement: which regions agree within ~5% "
            f"across all models?\n"
            f"  (b) Disagreement: which regions show meaningful divergence "
            f"(>10% spread between the highest and lowest model), and what "
            f"is the spread (state both extremes with model names)?\n"
            f"  (c) Outlier behaviour: is any one model systematically "
            f"higher or lower than the others across most regions, or is "
            f"the disagreement region-specific?\n"
            f"  (d) Where models disagree, which prediction does the "
            f"historic-yield context or bulletin observations support, "
            f"if anything?\n"
            f"Use the exact per-model numbers from the data above. Do not "
            f"invent model names or predictions not listed."
        )
    else:
        # Single-model run — instruct Claude to omit the section
        # entirely (header included) so the report doesn't carry an
        # empty Model Comparison subsection.
        model_comparison_instruction = (
            "Only one ML model contributed predictions for this run. Omit "
            "this section entirely — do NOT emit the `## Model Comparison` "
            "header at all, and do not write any prose for it. Skip directly "
            "to the next section."
        )
    country_display = country.replace("_", " ").title()
    crop_display = crop.replace("_", " ").title()

    bulletin_section = ""
    if bulletin_text:
        # Cap the combined bulletin text. 5-year lookback produces a
        # much larger payload than the original same-month-only one;
        # 20000 chars (~5000 tokens) leaves comfortable headroom on a
        # 200K-context model while giving Claude enough multi-year
        # material to cite from across seasons.
        bulletin_text = bulletin_text[:20000]
        bulletin_section = f"""
GEOGLAM Crop Monitor bulletins for {country_display} (last ~5 years; most recent first):
---
{bulletin_text}
---
Source: {bulletin_citation}
"""

    prompt = f"""You are an agricultural analyst writing a section for a GEOGLAM-style crop yield forecast report.

Country: {country_display}
Crop: {crop_display}
Forecast Year: {current_year}

Model Results:
{model_summary}
{bulletin_section}
Write a report narrative spanning 2-3 pages (approximately 800-1500 words, organized
as 6-10 paragraphs). You MUST adhere strictly to the data provided above — do not
invent numbers, conditions, or events not present in the model results or the
Crop Monitor bulletin text. Every claim must be directly traceable to the data above.
If no bulletin text is available, say so explicitly rather than speculating about
field conditions.

Follow the GEOGLAM Crop Monitor reporting style: factual, measured, region-specific.

REQUIRED OUTPUT STRUCTURE — emit the six sections below in order. Each section
MUST begin with a markdown subsection header on its own line, formatted exactly as:

    ## Section Name

with no extra punctuation, no bold/italic, no leading numbering, and nothing else
on the header line. The PDF report renderer uses this marker to render the section
header as a styled subsection heading. After the header line, write 1-3 paragraphs
of prose for that section. Use a blank line between header and body, and between
paragraphs.

## Current Season Assessment
Report the model's yield predictions for {current_year} using the exact numbers
provided. State which regions are predicted above or below average and by how much.
Do not editorialize beyond what the numbers show.

## Regional Historic Context
For each major region (and especially any that are flagged as high or low in the
forecast), compare the {current_year} prediction against THAT REGION'S OWN historic
yields shown above. Use the per-region multi-year mean when given. Phrase
comparisons as percentage deviations from the region's own history (e.g. "Free
State's 5.82 tn/ha is +5% above its 9-year mean of 5.54 tn/ha"). Do NOT compare a
region's prediction against the country average when its own history is available —
that obscures regional variability. If a region has no historic data in the block
above, say so explicitly and skip the comparison for that region.

## Climate Drivers
If top features/CIDs are listed above, explain which climate factors are most
influencing the forecast. Use plain language suitable for agronomists and policy
makers. If no features are listed, omit this section entirely (do not emit the
## Climate Drivers header) — do not guess at climate drivers.

## Model Comparison
{model_comparison_instruction}

## Comparison with Crop Monitor Reports
The bulletin block above contains monthly GEOGLAM Crop Monitor entries from the
past ~5 years (most recent first). Use this multi-year span to:
  (a) Describe how reported conditions evolved across the CURRENT growing season
      (planting → emergence → vegetative → reproductive → harvest, as applicable).
  (b) Compare the current-season trajectory to the same-month entries from prior
      years where available (e.g. "Conditions in May 2026 are described as
      'favourable' compared with 'moisture-stressed' in May 2024").
  (c) Note agreements or discrepancies between bulletin-reported conditions and
      the model's regional predictions.
You MUST include direct quotes from the bulletin text (use quotation marks) and
cite the source provided. For example: According to the GEOGLAM Crop Monitor
(April 2026), "quoted text from the bulletin." If no bulletin data is available,
discuss predictions only in the context of historical model performance (MAPE, R²)
without speculating about field conditions.

## Regional Highlights and Risks
Flag regions with unusually low or high predicted yields relative to their own
historic average. For each flagged region, state (a) the predicted value, (b) the
region's multi-year mean, (c) the percent deviation, and (d) any bulletin
observations that corroborate or contradict the model's flag. Do not fabricate
risk scenarios. If a flagged region has no historic data, say so explicitly.

## Outlook Summary
A short closing paragraph summarizing the season's overall standing for
{country_display} and the regions to watch as the season progresses.

Write in a professional, factual tone matching GEOGLAM Crop Monitor reports. Use
specific numbers from the data. Do not add disclaimers about being an AI. Do not
restate the section instructions in the output. Section header lines must use
exactly the `## Section Name` format described above; do not use a single `#`,
do not use HTML, do not bold/italic the header text."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        with client.messages.stream(
            model=claude_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            text = stream.get_final_text()

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        logger.info(f"Generated {len(paragraphs)} narrative paragraphs")
        return paragraphs

    except Exception as e:
        logger.warning(f"Claude API call failed: {e}")
        return []
