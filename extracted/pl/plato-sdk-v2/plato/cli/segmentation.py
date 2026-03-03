"""Segmentation CLI — plato segmentation predict / plato segmentation health / plato segmentation parse-ui."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

segmentation_app = typer.Typer(help="Segmentation commands (SAM3 + OmniParser).")
console = Console()


@segmentation_app.command()
def health(
    url: str = typer.Option(
        None,
        "--url",
        "-u",
        help="Server URL (default: $SEGMENTATION_BASE_URL or http://localhost:8100).",
    ),
) -> None:
    """Ping the segmentation server health endpoint."""
    from plato.segmentation import Segmentation

    client = Segmentation(base_url=url)
    try:
        info = client.health()
        console.print(f"[green]OK[/green]  {info}")
    except Exception as exc:
        console.print(f"[red]FAIL[/red]  {exc}")
        raise typer.Exit(1) from exc
    finally:
        client.close()


@segmentation_app.command()
def predict(
    images: list[str] = typer.Argument(..., help="Image file path(s)."),
    prompt: str = typer.Option(..., "--prompt", "-p", help="Text prompt."),
    output: str = typer.Option("segmentation_output", "--output", "-o", help="Output directory."),
    confidence: float = typer.Option(0.5, "--confidence", "-c", help="Score threshold."),
    url: str = typer.Option(None, "--url", "-u", help="Server URL."),
    overlay: bool = typer.Option(True, "--overlay/--no-overlay", help="Save overlay images."),
    segments: bool = typer.Option(True, "--segments/--no-segments", help="Save segment extractions."),
    alpha: float = typer.Option(0.5, "--alpha", help="Overlay alpha."),
    masks: bool = typer.Option(True, "--masks/--no-masks", help="Request segmentation masks (disable for boxes-only)."),
    output_json: bool = typer.Option(False, "--json", "-j", help="Print JSON results to stdout."),
) -> None:
    """Run text-prompted segmentation on one or more images."""
    from PIL import Image

    from plato.segmentation import PredictionResult, Segmentation
    from plato.segmentation.visualization import render_overlay, save_extractions

    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)

    client = Segmentation(base_url=url)

    try:
        for img_path in images:
            path = Path(img_path)
            if not path.exists():
                console.print(f"[red]File not found: {img_path}[/red]")
                continue

            stem = path.stem

            with console.status(f"[cyan]Predicting {path.name}..."):
                resp = client.predict(str(path), prompt, confidence_threshold=confidence, return_masks=masks)
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


@segmentation_app.command("parse-ui")
def parse_ui(
    images: list[str] = typer.Argument(..., help="Screenshot file path(s)."),
    url: str = typer.Option(None, "--url", "-u", help="Server URL."),
    output: str = typer.Option("parse_ui_output", "--output", "-o", help="Output directory."),
    box_threshold: float = typer.Option(0.05, "--box-threshold", help="YOLO confidence threshold."),
    iou_threshold: float = typer.Option(0.1, "--iou-threshold", help="IoU dedup threshold."),
    imgsz: int = typer.Option(640, "--imgsz", help="YOLO input image size."),
    overlay: bool = typer.Option(True, "--overlay/--no-overlay", help="Save annotated overlay image."),
    crops: bool = typer.Option(True, "--crops/--no-crops", help="Save individual element crops."),
    output_json: bool = typer.Option(False, "--json", "-j", help="Print JSON results to stdout."),
) -> None:
    """Parse UI elements from screenshots using OmniParser."""
    from PIL import Image

    from plato.segmentation import Segmentation
    from plato.segmentation.visualization import render_ui_overlay, save_ui_crops

    client = Segmentation(base_url=url)
    out_dir = Path(output)

    try:
        for img_path in images:
            path = Path(img_path)
            if not path.exists():
                console.print(f"[red]File not found: {img_path}[/red]")
                continue

            with console.status(f"[cyan]Parsing UI in {path.name}..."):
                result = client.parse_ui(
                    str(path), box_threshold=box_threshold, iou_threshold=iou_threshold, imgsz=imgsz
                )

            console.print(
                f"[bold]{path.name}[/bold]: "
                f"{result.num_icons} icon(s), {result.num_text_regions} text region(s), "
                f"{result.elapsed_ms:.0f} ms"
            )

            if output_json:
                console.print_json(data=result.model_dump())

            for el in result:
                icon_marker = "[blue]icon[/blue]" if el.element_type == "icon" else "[green]text[/green]"
                console.print(f"  {icon_marker} {el.content!r}  conf={el.confidence:.2f}  {el.bbox_pixels}")

            if len(result) == 0:
                continue

            source_image = Image.open(path).convert("RGB")
            stem = path.stem
            out_dir.mkdir(parents=True, exist_ok=True)

            if overlay:
                overlay_path = out_dir / f"{stem}_ui_overlay.png"
                render_ui_overlay(source_image, result).save(overlay_path)
                console.print(f"  overlay -> {overlay_path}")

            if crops:
                crop_dir = out_dir / f"{stem}_crops"
                paths = save_ui_crops(source_image, result, crop_dir)
                console.print(f"  crops   -> {crop_dir}/ ({len(paths)} files)")
    finally:
        client.close()
