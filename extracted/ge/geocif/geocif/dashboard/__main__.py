"""Allow running: python -m geocif.dashboard"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="GeoCIF Dashboard")
    parser.add_argument("--db", type=str, default=os.environ.get("GEOCIF_DB_PATH"),
                        help="Path to SQLite database")
    parser.add_argument("--hf-repo", type=str, default=os.environ.get("GEOCIF_HF_REPO"),
                        help="HuggingFace dataset repo ID")
    parser.add_argument("--agmet", type=str, default=os.environ.get("GEOCIF_AGMET_ROOT"),
                        help="Root directory of agmet PNGs")
    parser.add_argument("--outlook", type=str, default=os.environ.get("GEOCIF_OUTLOOK_ROOT"),
                        help="Root directory of outlook PNGs/CSVs")
    parser.add_argument("--port", type=int, default=5006, help="Port to serve on")
    parser.add_argument("--no-browser", action="store_true",
                        help="Don't open browser on start")
    args = parser.parse_args()

    from geocif.dashboard import serve

    serve(
        db_path=args.db,
        hf_repo_id=args.hf_repo,
        agmet_root=args.agmet,
        outlook_root=args.outlook,
        port=args.port,
        show=not args.no_browser,
    )


if __name__ == "__main__":
    main()
