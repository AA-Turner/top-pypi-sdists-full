"""GeoCIF interactive dashboard.

Quick start:
    python -m geocif.dashboard --db /path/to/geocif.db --agmet /path/to/agmet
"""

from geocif.dashboard.app import create_app


def serve(db_path=None, hf_repo_id=None, agmet_root=None,
          outlook_root=None, port=5006, show=True):
    """Launch the dashboard on a local server."""
    import panel as pn

    app = create_app(
        db_path=db_path,
        hf_repo_id=hf_repo_id,
        agmet_root=agmet_root,
        outlook_root=outlook_root,
    )
    pn.serve(app.servable(), port=port, show=show)
