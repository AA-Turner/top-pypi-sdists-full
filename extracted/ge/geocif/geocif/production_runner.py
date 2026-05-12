"""Production Analysis (BEAST) Pipeline Runner.

Runs the three BEAST changepoint-detection stages end-to-end:
  1. Detection   - beast_runner    -> beast_results.csv, beast_top_cps.csv
  2. Plots       - beast_plots     -> fig1-fig4 PNGs
  3. Sensitivity - beast_sensitivity -> sensitivity_raw/summary.csv, fig5

Stage toggles live in the ``[BEAST]`` section of geocif.txt:
  run_detection, run_plots, run_sensitivity  (default all True)

Usage::

    from geocif import production_runner
    production_runner.run(cfg_geocif)
"""
from pathlib import Path

from geocif.production_analysis.config import load_config
from geocif.production_analysis import beast_runner, beast_plots, beast_sensitivity


def run(path_config_files=[Path("../config/geocif.txt")]):
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("Usage", "from geocif import production_runner; production_runner.run(cfg)")
    table.add_row("cfg", "[geobase.txt, countries.txt, crops.txt, geocif.txt]")
    console.print(Panel(table, title="[bold bright_white]Production Analysis (BEAST) Runner[/]",
                        border_style="bright_blue", padding=(1, 2)))

    cfg = load_config(path_config_files)

    stages = [
        ("Detection",   cfg.run_detection,   beast_runner.run),
        ("Plots",       cfg.run_plots,       beast_plots.run),
        ("Sensitivity", cfg.run_sensitivity, beast_sensitivity.run),
    ]
    for name, enabled, fn in stages:
        if not enabled:
            console.print(f"[yellow]Skipping stage: {name}[/]")
            continue
        console.rule(f"[bold]Stage: {name}")
        fn(path_config_files)


if __name__ == "__main__":
    run()
