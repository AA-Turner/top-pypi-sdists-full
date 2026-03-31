"""Main Panel application for the GeoCIF dashboard.

Wires together the data layer, auth, and conditional tabs into a
FastListTemplate.

Usage:
    # Local DB:
    panel serve geocif/dashboard/app.py --args --db /path/to/geocif.db

    # With OAuth:
    panel serve geocif/dashboard/app.py \
        --oauth-provider=google \
        --cookie-secret=$PANEL_COOKIE_SECRET \
        --args --db /path/to/geocif.db --agmet /path/to/agmet

    # Via env vars:
    GEOCIF_DB_PATH=/path/to/db panel serve geocif/dashboard/app.py
"""

import argparse
import os
import sys

import panel as pn

from geocif.dashboard.auth import authorize
from geocif.dashboard.data import DashboardData
from geocif.dashboard.tabs import (
    agmet_graphics,
    historical_accuracy,
    shap_explanation,
    yield_predictions,
)

pn.config.authorize_callback = authorize


def _parse_args():
    """Parse CLI args (from --args when using `panel serve`)."""
    parser = argparse.ArgumentParser(description="GeoCIF Dashboard")
    parser.add_argument("--db", type=str, default=os.environ.get("GEOCIF_DB_PATH"))
    parser.add_argument("--hf-repo", type=str, default=os.environ.get("GEOCIF_HF_REPO"))
    parser.add_argument("--agmet", type=str, default=os.environ.get("GEOCIF_AGMET_ROOT"))
    parser.add_argument("--outlook", type=str, default=os.environ.get("GEOCIF_OUTLOOK_ROOT"))

    # When panel serve passes --args, the extra args are in sys.argv
    # Filter out bokeh/panel internal args
    known, _ = parser.parse_known_args()
    return known


def create_app(db_path=None, hf_repo_id=None, agmet_root=None, outlook_root=None):
    """Build and return the Panel template."""
    data = DashboardData(
        db_path=db_path,
        hf_repo_id=hf_repo_id,
        agmet_root=agmet_root,
        outlook_root=outlook_root,
    )

    template = pn.template.FastListTemplate(
        title="GeoCIF — Crop Yield Forecasting Dashboard",
        accent_base_color="#1f77b4",
        header_background="#2c3e50",
    )

    tabs = pn.Tabs(dynamic=True)

    if data.has_predictions:
        tabs.append(("Yield Predictions", yield_predictions.create_tab(data)))

    if data.has_agmet:
        tabs.append(("AgMet Graphics", agmet_graphics.create_tab(data)))

    if data.has_shap:
        tabs.append(("Model Explanation", shap_explanation.create_tab(data)))

    if data.has_metrics:
        tabs.append(("Historical Accuracy", historical_accuracy.create_tab(data)))

    if len(tabs) == 0:
        template.main.append(
            pn.pane.Markdown(
                "## No data found\n\n"
                "Provide a valid SQLite database path (`--db`) or "
                "HuggingFace repo ID (`--hf-repo`) with geocif output data.\n\n"
                "Optionally provide `--agmet` for agmet PNG browsing and "
                "`--outlook` for yield outlook maps."
            )
        )
    else:
        template.main.append(tabs)

    return template


# ── Entrypoint for `panel serve` ─────────────────────────────────────
if __name__.startswith("bokeh") or __name__ == "__main__":
    args = _parse_args()
    app = create_app(
        db_path=args.db,
        hf_repo_id=args.hf_repo,
        agmet_root=args.agmet,
        outlook_root=args.outlook,
    )
    app.servable()
