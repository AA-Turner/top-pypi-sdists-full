"""SAM3 CLI — plato sam3 predict / plato sam3 health."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

sam3_app = typer.Typer(help="SAM3 segmentation commands.")
console = Console()


@sam3_app.command()
def health(
    url: str = typer.Option(
        None,
        "--url",
        "-u",
        help="SAM3 server URL (default: $SAM3_BASE_URL or http://localhost:8100).",
    ),
) -> None:
    """Ping the SAM3 server health endpoint."""
    from plato.sam3 import Sam3

    client = Sam3(base_url=url)
    try:
        info = client.health()
        console.print(f"[green]OK[/green]  {info}")
    except Exception as exc:
        console.print(f"[red]FAIL[/red]  {exc}")
        raise typer.Exit(1) from exc
    finally:
        client.close()


@sam3_app.command()
def predict(
    images: list[str] = typer.Argument(..., help="Image file path(s)."),
    prompt: str = typer.Option(..., "--prompt", "-p", help="Text prompt."),
    output: str = typer.Option("sam3_output", "--output", "-o", help="Output directory."),
    confidence: float = typer.Option(0.5, "--confidence", "-c", help="Score threshold."),
    url: str = typer.Option(None, "--url", "-u", help="SAM3 server URL."),
    overlay: bool = typer.Option(True, "--overlay/--no-overlay", help="Save overlay images."),
    segments: bool = typer.Option(True, "--segments/--no-segments", help="Save segment extractions."),
    alpha: float = typer.Option(0.5, "--alpha", help="Overlay alpha."),
    output_json: bool = typer.Option(False, "--json", "-j", help="Print JSON results to stdout."),
) -> None:
    """Run SAM3 text-prompted segmentation on one or more images."""
    from PIL import Image

    from plato.sam3 import PredictionResult, Sam3
    from plato.sam3.visualization import render_overlay, save_extractions

    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)

    client = Sam3(base_url=url)

    try:
        for img_path in images:
            path = Path(img_path)
            if not path.exists():
                console.print(f"[red]File not found: {img_path}[/red]")
                continue

            stem = path.stem

            with console.status(f"[cyan]Predicting {path.name}..."):
                resp = client.predict(str(path), prompt, confidence_threshold=confidence)
                assert isinstance(resp, PredictionResult)
                result = resp

            console.print(
                f"[bold]{path.name}[/bold]: "
                f"{result.num_detections} detection(s), "
                f"scores={[round(s, 3) for s in result.scores]}, "
                f"{result.elapsed_ms:.0f} ms"
            )

            if output_json:
                console.print_json(data=result.model_dump())

            if result.num_detections == 0:
                continue

            source_image = Image.open(path).convert("RGB")

            if overlay:
                overlay_path = out_dir / f"{stem}_overlay.png"
                render_overlay(source_image, result, alpha=alpha).save(overlay_path)
                console.print(f"  overlay  -> {overlay_path}")

            if segments:
                seg_dir = out_dir / f"{stem}_segments"
                paths = save_extractions(source_image, result, seg_dir, prefix=stem)
                console.print(f"  segments -> {seg_dir}/ ({len(paths)} files)")
    finally:
        client.close()
