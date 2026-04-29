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

def _fetch_latest_bulletin(country, crop, category="AMIS"):
    """Download the latest Crop Monitor bulletin and extract text.

    Bulletin types on cropmonitor.org:
    - CM4AMIS: Crop Monitor for AMIS countries
    - CM4EW: Crop Monitor for Early Warning (EWCM countries)
    - Global CM: Global Crop Monitor

    Tries the category-specific bulletin first, then Global CM as fallback.
    Supports both PDF downloads and HTML web reports.
    """
    try:
        import requests
    except ImportError:
        logger.warning("requests not installed — skipping bulletin fetch")
        return ""

    # Map category to bulletin URL patterns
    # Recent bulletins use this URL pattern (YYYYMM format)
    bulletin_urls = []
    if category == "EWCM":
        bulletin_urls.append("https://www.cropmonitor.org/crop-monitor-for-early-warning-{ym}")
    elif category == "AMIS":
        bulletin_urls.append("https://www.cropmonitor.org/crop-monitor-for-amis-{ym}")
    # Always try Global CM as fallback
    bulletin_urls.append("https://www.cropmonitor.org/global-crop-monitor-{ym}")

    import arrow as ar
    now = ar.utcnow()

    # Try current season (last 4 months) + same month from up to 5 prior years
    # This enables apples-to-apples temporal comparison in the narrative
    months_to_try = [now.shift(months=-i).format("YYYYMM") for i in range(4)]
    current_month = now.month
    for yr_offset in range(1, 6):
        months_to_try.append(now.shift(years=-yr_offset).format("YYYY") + f"{current_month:02d}")

    all_texts = {}  # {YYYYMM: text} for all found bulletins
    all_urls = {}   # {YYYYMM: url} for citation

    for url_template in bulletin_urls:
        for ym in months_to_try:
            if ym in all_texts:
                continue
            url = url_template.format(ym=ym)
            try:
                resp = requests.get(url, timeout=15)
                if resp.status_code == 200:
                    text = _extract_html_text(resp.text)
                    country_text = _filter_country_text(text, country)
                    if country_text:
                        all_texts[ym] = country_text
                        all_urls[ym] = url
                        logger.info(f"Found bulletin {ym}: {url}")
            except Exception:
                continue

    if all_texts:
        # Combine all texts with year headers for temporal comparison
        parts = []
        sources = []
        for ym in sorted(all_texts.keys(), reverse=True):
            month_name = ar.get(f"{ym}01", "YYYYMMDD").format("MMMM YYYY")
            parts.append(f"[{month_name} Bulletin]\n{all_texts[ym]}")
            sources.append(f"GEOGLAM Crop Monitor, {month_name} ({all_urls[ym]})")
        combined_text = "\n\n".join(parts)
        citation = "; ".join(sources)
        return combined_text, citation

    # Fallback: try archive page for PDF links
    try:
        archive_url = "https://www.cropmonitor.org/archive/"
        resp = requests.get(archive_url, timeout=15)
        if resp.status_code == 200:
            # Look for PDF links matching the category
            pdf_tag = "CM4EW" if category == "EWCM" else "CM4AMIS"
            pdf_links = re.findall(
                rf'href="([^"]*{pdf_tag}[^"]*\.pdf)"', resp.text, re.IGNORECASE
            )
            if not pdf_links:
                # Try Global CM
                pdf_links = re.findall(
                    r'href="([^"]*Global[^"]*CM[^"]*\.pdf)"', resp.text, re.IGNORECASE
                )

            if pdf_links:
                from urllib.parse import urljoin
                pdf_url = pdf_links[-1]
                if not pdf_url.startswith("http"):
                    pdf_url = urljoin(archive_url, pdf_url)

                logger.info(f"Downloading bulletin PDF: {pdf_url}")
                pdf_resp = requests.get(pdf_url, timeout=30)
                pdf_resp.raise_for_status()

                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                    f.write(pdf_resp.content)
                    tmp_path = f.name

                text = _extract_pdf_text(tmp_path)
                os.unlink(tmp_path)
                filtered = _filter_country_text(text, country)
                citation = f"GEOGLAM Crop Monitor PDF ({pdf_url})"
                return filtered, citation

    except Exception as e:
        logger.warning(f"Failed to fetch crop monitor bulletin: {e}")

    return "", ""


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


def _build_model_summary(yield_data, metrics, top_features=None):
    """Format model results into a text summary for the prompt."""
    parts = []

    if yield_data:
        parts.append("Yield Predictions by Region:")
        for region, pred in yield_data.items():
            parts.append(f"  {region}: {pred:.2f} tn/ha")

    if metrics:
        parts.append("\nModel Performance Metrics:")
        for key, val in metrics.items():
            parts.append(f"  {key}: {val:.1f}")

    if top_features:
        parts.append("\nTop Climate Drivers (from SHAP analysis):")
        for feat in top_features[:10]:
            parts.append(f"  {feat}")

    return "\n".join(parts)


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

    # Read model settings from config (fallback to sensible defaults)
    claude_model = "claude-sonnet-4-6-20250514"
    max_tokens = 1500
    if parser is not None:
        if parser.has_section("NARRATIVE"):
            claude_model = parser.get("NARRATIVE", "claude_model", fallback=claude_model)
            max_tokens = parser.getint("NARRATIVE", "max_tokens", fallback=max_tokens)
    logger.info(f"Narrative LLM: model={claude_model}, max_tokens={max_tokens}")

    # Fetch bulletin if not provided
    bulletin_citation = ""
    if bulletin_text is None:
        bulletin_text, bulletin_citation = _fetch_latest_bulletin(country, crop, category)

    model_summary = _build_model_summary(yield_data, metrics, top_features)
    country_display = country.replace("_", " ").title()
    crop_display = crop.replace("_", " ").title()

    bulletin_section = ""
    if bulletin_text:
        # Truncate to avoid token limits
        bulletin_text = bulletin_text[:3000]
        bulletin_section = f"""
The latest GEOGLAM Crop Monitor bulletin mentions the following about {country_display}:
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
Write a concise report narrative (3-4 paragraphs). You MUST adhere strictly to the
data provided above — do not invent numbers, conditions, or events not present in
the model results or the Crop Monitor bulletin text. Every claim must be directly
traceable to the data above. If no bulletin text is available, say so explicitly
rather than speculating about field conditions.

Follow the GEOGLAM Crop Monitor reporting style: factual, measured, region-specific.

1. **Current Season Assessment**: Report the model's yield predictions for {current_year}
   using the exact numbers provided. State which regions are predicted above or below
   average and by how much. Do not editorialize beyond what the numbers show.

2. **Climate Drivers**: If top features/CIDs are listed above, explain which climate
   factors are most influencing the forecast. Use plain language suitable for
   agronomists and policy makers. If no features are listed, skip this paragraph
   entirely — do not guess at climate drivers.

3. **Comparison with Crop Monitor Reports**: If bulletin text is provided, compare
   the model predictions with the reported conditions. You MUST include direct
   quotes from the bulletin text (use quotation marks) and cite the source provided.
   For example: According to the GEOGLAM Crop Monitor (April 2026), "quoted text
   from the bulletin." Note agreements or discrepancies between the bulletin
   and model predictions. If no bulletin data is available, discuss predictions
   only in the context of historical model performance (MAPE, R²) without
   speculating about field conditions.

4. **Regional Highlights and Risks**: Flag regions with unusually low predicted
   yields, high uncertainty, or divergence from historical patterns — but only
   based on the data provided above. Do not fabricate risk scenarios.

Write in a professional, factual tone matching GEOGLAM Crop Monitor reports.
Use specific numbers from the data. Do not use markdown headers — just flowing
paragraphs. Do not add disclaimers about being an AI."""

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
