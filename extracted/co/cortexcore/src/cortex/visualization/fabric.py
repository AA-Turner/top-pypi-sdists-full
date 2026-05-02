from __future__ import annotations

import argparse
import html
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Literal

import torch
from pydantic import BaseModel, Field

from cortex.fabric.anatomy import FabricSpec, init_fabric
from cortex.fabric.config import FabricConfig, FabricFamilyConfig


class FabricSceneNode(BaseModel):
    cell_id: int
    role: Literal["input", "output", "recurrent"]
    family: str
    x: float
    y: float
    depth: float
    space: tuple[float, float, float]
    fan_in: int
    kv_group: int
    coord: tuple[float, ...]


class FabricSceneEdge(BaseModel):
    source: int
    target: int
    edge_type: Literal["local", "patch"]
    distance: float
    delay: int
    strength: float
    wraparound: bool


class FabricSceneMetrics(BaseModel):
    coord_shape: tuple[int, ...]
    num_cells: int
    num_edges: int
    num_input_cells: int
    num_output_cells: int
    num_recurrent_cells: int
    num_local_edges: int
    num_patch_edges: int
    num_wraparound_edges: int
    wrap: bool
    family_counts: dict[str, int]


class FabricScene(BaseModel):
    title: str
    coord_dim: int
    nodes: list[FabricSceneNode]
    edges: list[FabricSceneEdge]
    metrics: FabricSceneMetrics


class FabricVisualizerControls(BaseModel):
    title: str = Field(default="Cortex Fabric Atlas")
    max_edges: int = Field(default=4000, ge=64)
    width: int = Field(default=16, ge=1)
    height: int = Field(default=12, ge=1)
    depth: int = Field(default=1, ge=1)
    hidden_size: int = Field(default=8, ge=1)
    local_radius: float = Field(default=1.5, gt=0.0)
    patch_edges_per_cell: int = Field(default=1, ge=0)
    patch_min_dist: float = Field(default=4.0, ge=0.0)
    patch_max_dist: float = Field(default=12.0, ge=0.0)
    wrap: bool = True
    input_band_width: int = Field(default=1, ge=1)
    output_band_width: int = Field(default=1, ge=1)
    cell_arrangement: Literal["random", "x_bands"] = "x_bands"
    family_mode: Literal["slstm", "axoncell", "mixed"] = "mixed"
    slstm_mix: float = Field(default=0.65, ge=0.0, le=1.0)
    seed: int = 0

    def to_fabric_config(self) -> FabricConfig:
        if self.family_mode == "slstm":
            families = {"slstm": FabricFamilyConfig(family_type="slstm")}
            cell_mix = {"slstm": 1.0}
        elif self.family_mode == "axoncell":
            families = {"axoncell": FabricFamilyConfig(family_type="axoncell")}
            cell_mix = {"axoncell": 1.0}
        else:
            slstm_mix = float(self.slstm_mix)
            axon_mix = 1.0 - slstm_mix
            if slstm_mix == 0.0:
                families = {"axoncell": FabricFamilyConfig(family_type="axoncell")}
                cell_mix = {"axoncell": 1.0}
            elif axon_mix == 0.0:
                families = {"slstm": FabricFamilyConfig(family_type="slstm")}
                cell_mix = {"slstm": 1.0}
            else:
                families = {
                    "slstm": FabricFamilyConfig(family_type="slstm"),
                    "axoncell": FabricFamilyConfig(family_type="axoncell"),
                }
                cell_mix = {"slstm": slstm_mix, "axoncell": axon_mix}
        return FabricConfig(
            width=self.width,
            height=self.height,
            depth=self.depth,
            hidden_size=self.hidden_size,
            local_radius=self.local_radius,
            patch_edges_per_cell=self.patch_edges_per_cell,
            patch_min_dist=self.patch_min_dist,
            patch_max_dist=self.patch_max_dist,
            wrap=self.wrap,
            input_band_width=self.input_band_width,
            output_band_width=self.output_band_width,
            cell_arrangement=self.cell_arrangement,
            families=families,
            cell_mix=cell_mix,
            seed=self.seed,
        )

    @classmethod
    def from_fabric_spec(
        cls,
        spec: FabricSpec,
        *,
        title: str = "Cortex Fabric Atlas",
        max_edges: int = 4000,
    ) -> FabricVisualizerControls:
        family_mode = "mixed"
        slstm_mix = float(spec.config.cell_mix.get("slstm", 0.0))
        if tuple(spec.family_names) == ("slstm",):
            family_mode = "slstm"
            slstm_mix = 1.0
        elif tuple(spec.family_names) == ("axoncell",):
            family_mode = "axoncell"
            slstm_mix = 0.0
        return cls(
            title=title,
            max_edges=max_edges,
            width=spec.config.width,
            height=spec.config.height,
            depth=spec.config.depth,
            hidden_size=spec.config.hidden_size,
            local_radius=spec.config.local_radius,
            patch_edges_per_cell=spec.config.patch_edges_per_cell,
            patch_min_dist=spec.config.patch_min_dist,
            patch_max_dist=spec.config.patch_max_dist,
            wrap=spec.config.wrap,
            input_band_width=spec.config.input_band_width,
            output_band_width=spec.config.output_band_width,
            cell_arrangement=spec.config.cell_arrangement,
            family_mode=family_mode,
            slstm_mix=slstm_mix,
            seed=spec.config.seed,
        )


def build_fabric_scene(spec: FabricSpec, *, title: str = "Cortex Fabric Atlas", max_edges: int = 4000) -> FabricScene:
    projected_xy, depth, space = _project_coords(spec)
    nodes = _build_scene_nodes(spec, projected_xy, depth, space)
    edges = _build_scene_edges(spec, max_edges=max_edges)
    num_local_edges = sum(1 for edge in edges if edge.edge_type == "local")
    num_patch_edges = sum(1 for edge in edges if edge.edge_type == "patch")
    num_wraparound_edges = sum(1 for edge in edges if edge.wraparound)
    metrics = FabricSceneMetrics(
        coord_shape=tuple(int(v) for v in spec.config.coord_shape),
        num_cells=int(spec.anatomy.num_cells),
        num_edges=len(edges),
        num_input_cells=int(spec.input_cell_idx.numel()),
        num_output_cells=int(spec.output_cell_idx.numel()),
        num_recurrent_cells=int(spec.recurrent_cell_idx.numel()),
        num_local_edges=num_local_edges,
        num_patch_edges=num_patch_edges,
        num_wraparound_edges=num_wraparound_edges,
        wrap=bool(spec.config.wrap),
        family_counts=_family_counts(spec),
    )
    return FabricScene(
        title=title,
        coord_dim=int(spec.anatomy.coord_dim),
        nodes=nodes,
        edges=edges,
        metrics=metrics,
    )


def render_fabric_html(
    scene: FabricScene,
    *,
    controls: FabricVisualizerControls | None = None,
    api_path: str | None = None,
) -> str:
    visualizer_controls = controls or FabricVisualizerControls(title=scene.title)
    html_text = _HTML_TEMPLATE
    html_text = html_text.replace("__TITLE__", html.escape(scene.title))
    html_text = html_text.replace("__SCENE_JSON__", scene.model_dump_json(indent=2))
    html_text = html_text.replace("__CONTROLS_JSON__", visualizer_controls.model_dump_json(indent=2))
    html_text = html_text.replace("__API_PATH__", json.dumps(api_path))
    return html_text


def write_fabric_html(
    spec: FabricSpec,
    path: str | Path,
    *,
    title: str = "Cortex Fabric Atlas",
    max_edges: int = 4000,
) -> Path:
    output_path = Path(path)
    scene = build_fabric_scene(spec, title=title, max_edges=max_edges)
    controls = FabricVisualizerControls.from_fabric_spec(spec, title=title, max_edges=max_edges)
    output_path.write_text(render_fabric_html(scene, controls=controls), encoding="utf-8")
    return output_path


def serve_fabric_visualizer(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    controls: FabricVisualizerControls | None = None,
) -> ThreadingHTTPServer:
    initial_controls = controls or FabricVisualizerControls()

    class FabricVisualizerHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path not in {"/", "/index.html"}:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            scene = build_fabric_scene(
                init_fabric(initial_controls.to_fabric_config()),
                title=initial_controls.title,
                max_edges=initial_controls.max_edges,
            )
            page = render_fabric_html(scene, controls=initial_controls, api_path="/api/scene")
            body = page.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self) -> None:
            if self.path != "/api/scene":
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            length = int(self.headers["Content-Length"])
            payload = self.rfile.read(length)
            controls = FabricVisualizerControls.model_validate_json(payload)
            scene = build_fabric_scene(
                init_fabric(controls.to_fabric_config()),
                title=controls.title,
                max_edges=controls.max_edges,
            )
            body = scene.model_dump_json(indent=2).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    return ThreadingHTTPServer((host, port), FabricVisualizerHandler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render or serve a futuristic Cortex fabric anatomy visualizer.")
    parser.add_argument("--output", type=Path, default=Path("fabric_visualizer.html"))
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--title", default="Cortex Fabric Atlas")
    parser.add_argument("--max-edges", type=int, default=4000)
    parser.add_argument("--width", type=int, default=16)
    parser.add_argument("--height", type=int, default=12)
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--hidden-size", type=int, default=8)
    parser.add_argument("--local-radius", type=float, default=1.5)
    parser.add_argument("--patch-edges-per-cell", type=int, default=1)
    parser.add_argument("--patch-min-dist", type=float, default=4.0)
    parser.add_argument("--patch-max-dist", type=float, default=12.0)
    parser.add_argument("--wrap", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--input-band-width", type=int, default=1)
    parser.add_argument("--output-band-width", type=int, default=1)
    parser.add_argument("--cell-arrangement", choices=("random", "x_bands"), default="x_bands")
    parser.add_argument("--family-mode", choices=("slstm", "axoncell", "mixed"), default="mixed")
    parser.add_argument("--slstm-mix", type=float, default=0.65)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)
    controls = FabricVisualizerControls(
        title=args.title,
        max_edges=args.max_edges,
        width=args.width,
        height=args.height,
        depth=args.depth,
        hidden_size=args.hidden_size,
        local_radius=args.local_radius,
        patch_edges_per_cell=args.patch_edges_per_cell,
        patch_min_dist=args.patch_min_dist,
        patch_max_dist=args.patch_max_dist,
        wrap=args.wrap,
        input_band_width=args.input_band_width,
        output_band_width=args.output_band_width,
        cell_arrangement=args.cell_arrangement,
        family_mode=args.family_mode,
        slstm_mix=args.slstm_mix,
        seed=args.seed,
    )
    if args.serve:
        server = serve_fabric_visualizer(host=args.host, port=args.port, controls=controls)
        print(f"Fabric visualizer listening at http://{args.host}:{args.port}")
        server.serve_forever()
        return 0
    spec = init_fabric(controls.to_fabric_config())
    output = write_fabric_html(spec, args.output, title=controls.title, max_edges=controls.max_edges)
    print(f"Wrote fabric visualizer to {output}")
    return 0


def _build_scene_nodes(
    spec: FabricSpec,
    projected_xy: torch.Tensor,
    depth: torch.Tensor,
    space: torch.Tensor,
) -> list[FabricSceneNode]:
    family_names = spec.family_names
    fan_in = spec.anatomy.neighbor_valid.sum(dim=1)
    input_mask = torch.zeros(spec.anatomy.num_cells, dtype=torch.bool)
    output_mask = torch.zeros(spec.anatomy.num_cells, dtype=torch.bool)
    input_mask[spec.input_cell_idx] = True
    output_mask[spec.output_cell_idx] = True
    nodes: list[FabricSceneNode] = []
    for cell_id in range(spec.anatomy.num_cells):
        if bool(input_mask[cell_id]):
            role = "input"
            family = "input-shell"
        elif bool(output_mask[cell_id]):
            role = "output"
            family = "output-shell"
        else:
            role = "recurrent"
            family_idx = int(spec.anatomy.cell_layout[cell_id].item())
            family = family_names[family_idx]
        coord = tuple(float(v) for v in spec.anatomy.coords[cell_id].tolist())
        nodes.append(
            FabricSceneNode(
                cell_id=cell_id,
                role=role,
                family=family,
                x=float(projected_xy[cell_id, 0].item()),
                y=float(projected_xy[cell_id, 1].item()),
                depth=float(depth[cell_id].item()),
                space=tuple(float(v) for v in space[cell_id].tolist()),
                fan_in=int(fan_in[cell_id].item()),
                kv_group=int(spec.kv_group_id[cell_id].item()),
                coord=coord,
            )
        )
    return nodes


def _build_scene_edges(spec: FabricSpec, *, max_edges: int) -> list[FabricSceneEdge]:
    valid = torch.nonzero(spec.anatomy.neighbor_valid, as_tuple=False)
    if valid.numel() == 0:
        return []
    edge_records = []
    for recv_idx, slot_idx in valid.tolist():
        send_idx = int(spec.anatomy.neighbor_idx[recv_idx, slot_idx].item())
        edge_kind = "patch" if int(spec.anatomy.edge_type[recv_idx, slot_idx].item()) == 1 else "local"
        distance = float(spec.anatomy.edge_distance[recv_idx, slot_idx].item())
        delay = int(spec.anatomy.edge_delay[recv_idx, slot_idx].item()) if spec.anatomy.edge_delay is not None else 1
        edge_records.append(
            FabricSceneEdge(
                source=send_idx,
                target=int(recv_idx),
                edge_type=edge_kind,
                distance=distance,
                delay=delay,
                strength=float(1.0 / (1.0 + distance)),
                wraparound=_is_wraparound_edge(spec, recv_idx=int(recv_idx), send_idx=send_idx),
            )
        )
    if len(edge_records) <= max_edges:
        return edge_records
    patch_indices = [idx for idx, edge in enumerate(edge_records) if edge.edge_type == "patch"]
    local_indices = [idx for idx, edge in enumerate(edge_records) if edge.edge_type == "local"]
    patch_quota = min(len(patch_indices), max(0, max_edges // 3))
    local_quota = max_edges - patch_quota
    if local_quota > len(local_indices):
        patch_quota = min(len(patch_indices), patch_quota + (local_quota - len(local_indices)))
        local_quota = min(len(local_indices), local_quota)
    selected = _sample_indices(local_indices, local_quota) + _sample_indices(patch_indices, patch_quota)
    selected.sort()
    return [edge_records[idx] for idx in selected]


def _sample_indices(indices: list[int], count: int) -> list[int]:
    if count <= 0 or not indices:
        return []
    if count >= len(indices):
        return indices
    positions = torch.linspace(0, len(indices) - 1, steps=count).round().to(torch.long)
    unique_positions = torch.unique(positions, sorted=True).tolist()
    sampled = [indices[pos] for pos in unique_positions]
    if len(sampled) < count:
        for idx in indices:
            if idx not in sampled:
                sampled.append(idx)
            if len(sampled) == count:
                break
    return sampled[:count]


def _project_coords(spec: FabricSpec) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    coords = spec.anatomy.coords.to(torch.float32)
    extent = torch.tensor([max(size - 1, 1) for size in spec.config.coord_shape], dtype=torch.float32)
    norm = coords / extent.view(1, -1)
    if spec.anatomy.coord_dim == 2:
        space = torch.stack(
            (
                1.65 * (norm[:, 0] - 0.5),
                1.35 * (0.5 - norm[:, 1]),
                0.06 * torch.sin(torch.pi * norm[:, 0]) * torch.cos(torch.pi * norm[:, 1]),
            ),
            dim=-1,
        )
        warped = torch.stack(
            (
                norm[:, 0] + 0.045 * torch.sin(torch.pi * norm[:, 1]),
                norm[:, 1] + 0.035 * torch.sin(2.0 * torch.pi * norm[:, 0]),
            ),
            dim=-1,
        )
        depth = torch.full((coords.shape[0],), 0.45, dtype=torch.float32)
    else:
        space = torch.stack(
            (
                1.65 * (norm[:, 0] - 0.5) + 0.12 * torch.sin(torch.pi * norm[:, 2]),
                1.35 * (0.5 - norm[:, 1]) + 0.08 * torch.sin(torch.pi * norm[:, 0]),
                1.55 * (norm[:, 2] - 0.5),
            ),
            dim=-1,
        )
        warped = torch.stack(
            (
                norm[:, 0] + 0.42 * norm[:, 2] + 0.03 * torch.sin(torch.pi * norm[:, 1]),
                0.82 * norm[:, 1] + 0.18 * (1.0 - norm[:, 2]) + 0.05 * torch.sin(torch.pi * norm[:, 0]),
            ),
            dim=-1,
        )
        depth = norm[:, 2]
    min_xy = warped.min(dim=0).values
    max_xy = warped.max(dim=0).values
    projected = (warped - min_xy) / (max_xy - min_xy).clamp_min(1e-6)
    projected = 0.08 + 0.84 * projected
    return projected, depth, space


def _is_wraparound_edge(spec: FabricSpec, *, recv_idx: int, send_idx: int) -> bool:
    if not spec.config.wrap:
        return False
    recv = spec.anatomy.coords[recv_idx]
    send = spec.anatomy.coords[send_idx]
    extent = torch.tensor([max(size - 1, 1) for size in spec.config.coord_shape], dtype=recv.dtype)
    diff = (recv - send).abs()
    return bool((diff > (0.5 * extent)).any().item())


def _family_counts(spec: FabricSpec) -> dict[str, int]:
    counts: dict[str, int] = {}
    for family_idx, family_name in enumerate(spec.family_names):
        counts[family_name] = int((spec.anatomy.cell_layout == family_idx).sum().item())
    return counts


_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {
      --bg-0: #040913;
      --bg-1: #071427;
      --bg-2: #11253f;
      --panel: rgba(10, 19, 34, 0.84);
      --panel-border: rgba(127, 182, 255, 0.18);
      --text: #e8f1ff;
      --muted: #90a4c7;
      --input: #62f3ff;
      --output: #ff8cab;
      --slstm: #8fff76;
      --axoncell: #ffd666;
      --local-edge: rgba(102, 227, 255, 0.23);
      --patch-edge: rgba(255, 138, 187, 0.34);
      --halo: rgba(116, 229, 255, 0.18);
      --accent: #a6c5ff;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at 20% 20%, rgba(92, 143, 255, 0.16), transparent 28%),
        radial-gradient(circle at 78% 18%, rgba(255, 127, 188, 0.14), transparent 26%),
        radial-gradient(circle at 50% 80%, rgba(114, 255, 214, 0.12), transparent 24%),
        linear-gradient(145deg, var(--bg-0), var(--bg-1) 48%, var(--bg-2));
      color: var(--text);
      font-family: "Space Grotesk", "IBM Plex Sans", "Segoe UI", sans-serif;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
      background-size: 28px 28px;
      mask-image: radial-gradient(circle at center, rgba(0, 0, 0, 0.8), transparent 85%);
    }

    .app-shell {
      display: grid;
      grid-template-columns: minmax(320px, 380px) minmax(0, 1fr);
      gap: 24px;
      padding: 24px;
      min-height: 100vh;
    }

    .panel {
      position: relative;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 28px;
      box-shadow:
        0 20px 80px rgba(0, 0, 0, 0.36),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
      backdrop-filter: blur(18px);
      overflow: hidden;
    }

    .panel::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), transparent 22%);
      pointer-events: none;
    }

    .control-panel {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .eyebrow {
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: var(--muted);
      font-size: 11px;
      margin-bottom: 6px;
    }

    h1 {
      margin: 0;
      font-size: clamp(28px, 4vw, 40px);
      line-height: 0.95;
      letter-spacing: -0.04em;
    }

    .subtext {
      color: var(--muted);
      line-height: 1.5;
      margin: 0;
    }

    .synaptic-haze {
      position: absolute;
      inset: -20% 10% auto -10%;
      height: 220px;
      background:
        radial-gradient(circle, rgba(98, 243, 255, 0.22), transparent 55%),
        radial-gradient(circle at 68% 36%, rgba(255, 140, 171, 0.22), transparent 44%);
      filter: blur(48px);
      pointer-events: none;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .field.span-2 {
      grid-column: span 2;
    }

    label {
      font-size: 12px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }

    input,
    select,
    button {
      appearance: none;
      border: 1px solid rgba(163, 190, 255, 0.18);
      border-radius: 14px;
      background: rgba(6, 14, 28, 0.82);
      color: var(--text);
      padding: 12px 14px;
      font: inherit;
    }

    input[type="range"] {
      padding: 8px 0;
      background: transparent;
      border: none;
    }

    input[type="checkbox"] {
      inline-size: 18px;
      block-size: 18px;
      padding: 0;
      border-radius: 5px;
    }

    .checkbox-row {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text);
    }

    .button-row {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    button {
      cursor: pointer;
      background: linear-gradient(135deg, rgba(97, 156, 255, 0.9), rgba(255, 110, 170, 0.9));
      box-shadow: 0 8px 24px rgba(89, 132, 255, 0.26);
      border: none;
      font-weight: 600;
    }

    button.secondary {
      background: rgba(10, 18, 33, 0.72);
      border: 1px solid rgba(163, 190, 255, 0.18);
      box-shadow: none;
    }

    .live-value {
      color: var(--accent);
      font-weight: 600;
      margin-left: 6px;
    }

    .main-panel {
      display: grid;
      grid-template-rows: auto auto minmax(0, 1fr);
      gap: 18px;
      padding: 24px;
    }

    .topline {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      flex-wrap: wrap;
    }

    .chips {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .chip {
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(8, 16, 28, 0.78);
      border: 1px solid rgba(163, 190, 255, 0.14);
      color: var(--muted);
      font-size: 13px;
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }

    .metric-card {
      padding: 16px;
      border-radius: 18px;
      background: rgba(7, 14, 26, 0.76);
      border: 1px solid rgba(163, 190, 255, 0.12);
    }

    .metric-label {
      color: var(--muted);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 10px;
    }

    .metric-value {
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.04em;
    }

    .scene-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 18px;
      min-height: 620px;
    }

    .viewport {
      position: relative;
      overflow: hidden;
      border-radius: 24px;
      border: 1px solid rgba(163, 190, 255, 0.14);
      background:
        radial-gradient(circle at center, rgba(23, 46, 72, 0.72), rgba(5, 10, 20, 0.94)),
        linear-gradient(180deg, rgba(255, 255, 255, 0.02), transparent);
    }

    .viewport.orbit-enabled {
      cursor: grab;
      touch-action: none;
    }

    .viewport.is-orbiting {
      cursor: grabbing;
    }

    .viewport svg {
      width: 100%;
      height: 100%;
      display: block;
    }

    .viewport-hud {
      position: absolute;
      inset: 14px 14px auto 14px;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      z-index: 2;
      pointer-events: none;
    }

    .camera-hint {
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(6, 13, 25, 0.72);
      border: 1px solid rgba(163, 190, 255, 0.18);
      color: var(--muted);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      backdrop-filter: blur(14px);
    }

    .hud-button {
      pointer-events: auto;
      padding: 10px 14px;
    }

    .hud-button:disabled {
      opacity: 0.5;
      cursor: default;
    }

    .sidebar {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .info-card,
    .legend-card,
    .status-card {
      padding: 16px 18px;
      border-radius: 20px;
      background: rgba(7, 14, 26, 0.76);
      border: 1px solid rgba(163, 190, 255, 0.12);
    }

    .legend-list,
    .info-grid {
      display: grid;
      gap: 10px;
      margin-top: 10px;
    }

    .legend-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
    }

    .legend-swatch {
      inline-size: 12px;
      block-size: 12px;
      border-radius: 999px;
      box-shadow: 0 0 12px currentColor;
      margin-right: 10px;
      flex: 0 0 auto;
    }

    .legend-label {
      display: flex;
      align-items: center;
      color: var(--text);
    }

    .info-row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
    }

    .info-row strong {
      color: var(--text);
    }

    .status-card {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.5;
    }

    .stage-line {
      stroke-linecap: round;
      stroke-width: 1.25;
      fill: none;
      animation: pulseFlow 7s linear infinite;
    }

    .stage-line.local {
      stroke: var(--local-edge);
    }

    .stage-line.patch {
      stroke: var(--patch-edge);
      stroke-width: 1.6;
      stroke-dasharray: 6 10;
    }

    .stage-line.wrap {
      stroke: rgba(255, 214, 102, 0.72);
      stroke-dasharray: 2 7;
    }

    .stage-line.hidden {
      opacity: 0;
    }

    .stage-line.active {
      stroke-width: 2.4;
      opacity: 0.96;
    }

    .node-group {
      cursor: pointer;
    }

    .node-halo {
      opacity: 0.3;
      filter: blur(8px);
      animation: haloPulse 4.8s ease-in-out infinite;
    }

    .node-core {
      stroke: rgba(255, 255, 255, 0.55);
      stroke-width: 0.8;
    }

    .node-group.dimmed {
      opacity: 0.18;
    }

    .node-group.active .node-core {
      stroke: rgba(255, 255, 255, 0.95);
      stroke-width: 1.5;
    }

    .node-group.active .node-halo {
      opacity: 0.66;
    }

    @keyframes pulseFlow {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: -64; }
    }

    @keyframes haloPulse {
      0%, 100% { transform: scale(1); opacity: 0.24; }
      50% { transform: scale(1.12); opacity: 0.52; }
    }

    @media (max-width: 1180px) {
      .app-shell {
        grid-template-columns: 1fr;
      }

      .metrics-grid,
      .scene-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="app-shell">
    <section class="panel control-panel">
      <div class="synaptic-haze"></div>
      <div>
        <div class="eyebrow">Cortex Fabric Visualizer</div>
        <h1>Neural atlas for living lattice anatomy</h1>
        <p class="subtext">
          Tune a fabric spec, regenerate the anatomy in place, and inspect how local and patch connections braid into a
          brain-like cortical sheet.
        </p>
      </div>

      <form id="scene-form">
        <div class="form-grid">
          <div class="field span-2">
            <label for="title">Scene title</label>
            <input id="title" name="title" type="text">
          </div>

          <div class="field">
            <label for="width">Width</label>
            <input id="width" name="width" type="number" min="1" step="1">
          </div>
          <div class="field">
            <label for="height">Height</label>
            <input id="height" name="height" type="number" min="1" step="1">
          </div>
          <div class="field">
            <label for="depth">Depth</label>
            <input id="depth" name="depth" type="number" min="1" step="1">
          </div>
          <div class="field">
            <label for="hidden-size">Hidden size</label>
            <input id="hidden-size" name="hidden_size" type="number" min="1" step="1">
          </div>
          <div class="field">
            <label for="local-radius">Local radius</label>
            <input id="local-radius" name="local_radius" type="number" min="0.25" step="0.25">
          </div>
          <div class="field">
            <label for="patch-edges">Patch edges / cell</label>
            <input id="patch-edges" name="patch_edges_per_cell" type="number" min="0" step="1">
          </div>
          <div class="field">
            <label for="patch-min-dist">Patch min dist</label>
            <input id="patch-min-dist" name="patch_min_dist" type="number" min="0" step="0.5">
          </div>
          <div class="field">
            <label for="patch-max-dist">Patch max dist</label>
            <input id="patch-max-dist" name="patch_max_dist" type="number" min="0" step="0.5">
          </div>
          <div class="field">
            <label for="input-band-width">Input band</label>
            <input id="input-band-width" name="input_band_width" type="number" min="1" step="1">
          </div>
          <div class="field">
            <label for="output-band-width">Output band</label>
            <input id="output-band-width" name="output_band_width" type="number" min="1" step="1">
          </div>
          <div class="field">
            <label for="family-mode">Family mode</label>
            <select id="family-mode" name="family_mode">
              <option value="mixed">Mixed</option>
              <option value="slstm">sLSTM only</option>
              <option value="axoncell">AxonCell only</option>
            </select>
          </div>
          <div class="field">
            <label for="cell-arrangement">Cell arrangement</label>
            <select id="cell-arrangement" name="cell_arrangement">
              <option value="x_bands">x_bands</option>
              <option value="random">random</option>
            </select>
          </div>
          <div class="field span-2">
            <label for="slstm-mix">sLSTM share <span id="slstm-mix-value" class="live-value"></span></label>
            <input id="slstm-mix" name="slstm_mix" type="range" min="0" max="1" step="0.01">
          </div>
          <div class="field">
            <label for="max-edges">Visible edges</label>
            <input id="max-edges" name="max_edges" type="number" min="64" step="64">
          </div>
          <div class="field">
            <label for="seed">Seed</label>
            <input id="seed" name="seed" type="number" step="1">
          </div>
          <div class="field span-2">
            <div class="checkbox-row">
              <input id="wrap" name="wrap" type="checkbox">
              <label for="wrap">Wraparound boundaries</label>
            </div>
          </div>
        </div>

        <div class="button-row" style="margin-top: 18px;">
          <button type="submit">Render fabric</button>
          <button type="button" class="secondary" data-preset="cortical-sheet">Cortical sheet</button>
          <button type="button" class="secondary" data-preset="sensory-ribbon">Sensory ribbon</button>
          <button type="button" class="secondary" data-preset="wrap-loop">Wrap loop</button>
          <button type="button" class="secondary" data-preset="patch-mosaic">Patch mosaic</button>
          <button type="button" class="secondary" data-preset="relay-column">Relay column</button>
          <button type="button" class="secondary" data-preset="volumetric">Volumetric lobe</button>
          <button type="button" class="secondary" data-preset="deep-cube">Deep cube</button>
          <button type="button" class="secondary" data-preset="laminar-stack">Laminar stack</button>
          <button type="button" class="secondary" data-preset="torus-lobe">Torus lobe</button>
        </div>
      </form>
    </section>

    <section class="panel main-panel">
      <div class="topline">
        <div>
          <div class="eyebrow">Anatomy stage</div>
          <h1 id="scene-title">__TITLE__</h1>
        </div>
        <div class="chips">
          <div class="chip">Hover cells to inspect fan-in and region</div>
          <div class="chip">Click a cell to trace its synapses</div>
          <div class="chip">Live config panel at left</div>
        </div>
      </div>

      <div id="metrics" class="metrics-grid"></div>

      <div class="scene-grid">
        <div class="viewport" id="viewport">
          <svg id="fabric-stage" viewBox="0 0 1200 760" preserveAspectRatio="xMidYMid meet" aria-label="Fabric anatomy">
            <defs>
              <filter id="softBlur">
                <feGaussianBlur stdDeviation="5"></feGaussianBlur>
              </filter>
            </defs>
            <rect x="0" y="0" width="1200" height="760" fill="transparent"></rect>
            <g id="edge-layer"></g>
            <g id="node-layer"></g>
          </svg>
          <div class="viewport-hud">
            <div id="camera-hint" class="camera-hint">Drag to orbit 3D fabrics</div>
            <button type="button" id="reset-camera" class="hud-button secondary">Reset orbit</button>
          </div>
        </div>

        <div class="sidebar">
          <div class="legend-card">
            <div class="eyebrow">Legend</div>
            <div id="legend" class="legend-list"></div>
          </div>
          <div class="info-card">
            <div class="eyebrow">Cell focus</div>
            <div id="cell-info" class="info-grid"></div>
          </div>
          <div class="status-card">
            <div class="eyebrow">Render status</div>
            <div id="status-text">Ready. Tune the fabric spec and re-render.</div>
          </div>
        </div>
      </div>
    </section>
  </div>

  <script type="application/json" id="fabric-scene-data">__SCENE_JSON__</script>
  <script type="application/json" id="visualizer-controls-data">__CONTROLS_JSON__</script>
  <script>
    const apiPath = __API_PATH__;
    let currentScene = JSON.parse(document.getElementById('fabric-scene-data').textContent);
    let currentControls = JSON.parse(document.getElementById('visualizer-controls-data').textContent);
    let activeNodeId = null;

    const stage = document.getElementById('fabric-stage');
    const viewportEl = document.getElementById('viewport');
    const edgeLayer = document.getElementById('edge-layer');
    const nodeLayer = document.getElementById('node-layer');
    const metricsEl = document.getElementById('metrics');
    const legendEl = document.getElementById('legend');
    const infoEl = document.getElementById('cell-info');
    const statusEl = document.getElementById('status-text');
    const titleEl = document.getElementById('scene-title');
    const formEl = document.getElementById('scene-form');
    const slstmMixEl = document.getElementById('slstm-mix');
    const slstmMixValueEl = document.getElementById('slstm-mix-value');
    const cameraHintEl = document.getElementById('camera-hint');
    const resetCameraButton = document.getElementById('reset-camera');
    const STAGE_WIDTH = 1200;
    const STAGE_HEIGHT = 760;
    let currentNodeById = new Map();
    let cameraState = defaultCameraStateForScene(currentScene);
    let currentProjection = new Map();
    let dragState = null;

    const palette = {
      input: '#62f3ff',
      output: '#ff8cab',
      'input-shell': '#62f3ff',
      'output-shell': '#ff8cab',
      slstm: '#8fff76',
      axoncell: '#ffd666',
      recurrent: '#a6c5ff',
      local: 'rgba(102, 227, 255, 0.28)',
      patch: 'rgba(255, 138, 187, 0.4)',
      wrap: 'rgba(255, 214, 102, 0.74)',
    };

    const presets = {
      'cortical-sheet': {
        title: 'Cortical Sheet',
        width: 24,
        height: 16,
        depth: 1,
        hidden_size: 8,
        local_radius: 1.5,
        patch_edges_per_cell: 2,
        patch_min_dist: 4,
        patch_max_dist: 12,
        wrap: true,
        input_band_width: 2,
        output_band_width: 2,
        family_mode: 'mixed',
        slstm_mix: 0.65,
        cell_arrangement: 'x_bands',
        max_edges: 5000,
      },
      'sensory-ribbon': {
        title: 'Sensory Ribbon',
        width: 30,
        height: 10,
        depth: 1,
        hidden_size: 8,
        local_radius: 1.75,
        patch_edges_per_cell: 1,
        patch_min_dist: 6,
        patch_max_dist: 16,
        wrap: false,
        input_band_width: 2,
        output_band_width: 2,
        family_mode: 'mixed',
        slstm_mix: 0.72,
        cell_arrangement: 'x_bands',
        max_edges: 4200,
      },
      'wrap-loop': {
        title: 'Wrap Loop',
        width: 20,
        height: 12,
        depth: 1,
        hidden_size: 8,
        local_radius: 1.5,
        patch_edges_per_cell: 0,
        patch_min_dist: 4,
        patch_max_dist: 12,
        wrap: true,
        input_band_width: 1,
        output_band_width: 1,
        family_mode: 'slstm',
        slstm_mix: 1.0,
        cell_arrangement: 'random',
        max_edges: 3600,
      },
      'patch-mosaic': {
        title: 'Patch Mosaic',
        width: 18,
        height: 18,
        depth: 1,
        hidden_size: 8,
        local_radius: 2.0,
        patch_edges_per_cell: 4,
        patch_min_dist: 5,
        patch_max_dist: 14,
        wrap: false,
        input_band_width: 2,
        output_band_width: 2,
        family_mode: 'mixed',
        slstm_mix: 0.5,
        cell_arrangement: 'random',
        max_edges: 6200,
      },
      'relay-column': {
        title: 'Relay Column',
        width: 12,
        height: 24,
        depth: 1,
        hidden_size: 8,
        local_radius: 2.5,
        patch_edges_per_cell: 1,
        patch_min_dist: 6,
        patch_max_dist: 16,
        wrap: false,
        input_band_width: 1,
        output_band_width: 1,
        family_mode: 'mixed',
        slstm_mix: 0.4,
        cell_arrangement: 'x_bands',
        max_edges: 4000,
      },
      volumetric: {
        title: 'Volumetric Lobe',
        width: 12,
        height: 10,
        depth: 6,
        hidden_size: 8,
        local_radius: 1.75,
        patch_edges_per_cell: 2,
        patch_min_dist: 3,
        patch_max_dist: 9,
        wrap: false,
        input_band_width: 1,
        output_band_width: 1,
        family_mode: 'mixed',
        slstm_mix: 0.55,
        cell_arrangement: 'random',
        max_edges: 6500,
      },
      'deep-cube': {
        title: 'Deep Cube',
        width: 8,
        height: 8,
        depth: 8,
        hidden_size: 8,
        local_radius: 1.75,
        patch_edges_per_cell: 2,
        patch_min_dist: 3,
        patch_max_dist: 8,
        wrap: false,
        input_band_width: 1,
        output_band_width: 1,
        family_mode: 'mixed',
        slstm_mix: 0.45,
        cell_arrangement: 'random',
        max_edges: 7000,
      },
      'laminar-stack': {
        title: 'Laminar Stack',
        width: 16,
        height: 8,
        depth: 4,
        hidden_size: 8,
        local_radius: 1.5,
        patch_edges_per_cell: 1,
        patch_min_dist: 4,
        patch_max_dist: 10,
        wrap: false,
        input_band_width: 2,
        output_band_width: 2,
        family_mode: 'mixed',
        slstm_mix: 0.68,
        cell_arrangement: 'x_bands',
        max_edges: 6200,
      },
      'torus-lobe': {
        title: 'Torus Lobe',
        width: 12,
        height: 8,
        depth: 5,
        hidden_size: 8,
        local_radius: 1.75,
        patch_edges_per_cell: 2,
        patch_min_dist: 3,
        patch_max_dist: 9,
        wrap: true,
        input_band_width: 1,
        output_band_width: 1,
        family_mode: 'mixed',
        slstm_mix: 0.52,
        cell_arrangement: 'random',
        max_edges: 6400,
      },
    };

    function populateForm(controls) {
      titleEl.textContent = controls.title;
      document.getElementById('title').value = controls.title;
      document.getElementById('width').value = controls.width;
      document.getElementById('height').value = controls.height;
      document.getElementById('depth').value = controls.depth;
      document.getElementById('hidden-size').value = controls.hidden_size;
      document.getElementById('local-radius').value = controls.local_radius;
      document.getElementById('patch-edges').value = controls.patch_edges_per_cell;
      document.getElementById('patch-min-dist').value = controls.patch_min_dist;
      document.getElementById('patch-max-dist').value = controls.patch_max_dist;
      document.getElementById('input-band-width').value = controls.input_band_width;
      document.getElementById('output-band-width').value = controls.output_band_width;
      document.getElementById('family-mode').value = controls.family_mode;
      document.getElementById('cell-arrangement').value = controls.cell_arrangement;
      document.getElementById('max-edges').value = controls.max_edges;
      document.getElementById('seed').value = controls.seed;
      document.getElementById('wrap').checked = Boolean(controls.wrap);
      slstmMixEl.value = controls.slstm_mix;
      updateMixLabel();
    }

    function updateMixLabel() {
      slstmMixValueEl.textContent = `${Math.round(Number(slstmMixEl.value) * 100)}%`;
    }

    function nodeColor(node) {
      return palette[node.family] || palette[node.role] || palette.recurrent;
    }

    function clamp(value, minValue, maxValue) {
      return Math.max(minValue, Math.min(maxValue, value));
    }

    function defaultCameraStateForScene(scene) {
      if (scene && scene.coord_dim === 3) {
        return { yaw: -0.82, pitch: 0.48, zoom: 1.02 };
      }
      return { yaw: 0.0, pitch: 0.0, zoom: 1.0 };
    }

    function updateCameraHint() {
      if (currentScene.coord_dim !== 3) {
        viewportEl.classList.remove('orbit-enabled', 'is-orbiting');
        resetCameraButton.disabled = true;
        cameraHintEl.textContent = '2D fabric projection';
        return;
      }
      viewportEl.classList.add('orbit-enabled');
      resetCameraButton.disabled = false;
      const yawDeg = Math.round(cameraState.yaw * 57.2958);
      const pitchDeg = Math.round(cameraState.pitch * 57.2958);
      const zoomText = cameraState.zoom.toFixed(2);
      cameraHintEl.textContent = `Drag to orbit | yaw ${yawDeg}° | pitch ${pitchDeg}° | zoom ${zoomText}x`;
    }

    function projectNode(node) {
      if (currentScene.coord_dim !== 3) {
        return {
          x: node.x * STAGE_WIDTH,
          y: node.y * STAGE_HEIGHT,
          depth: node.depth,
          scale: 1.0,
        };
      }
      const [sx, sy, sz] = node.space;
      const cosYaw = Math.cos(cameraState.yaw);
      const sinYaw = Math.sin(cameraState.yaw);
      const cosPitch = Math.cos(cameraState.pitch);
      const sinPitch = Math.sin(cameraState.pitch);
      const x1 = sx * cosYaw - sz * sinYaw;
      const z1 = sx * sinYaw + sz * cosYaw;
      const y1 = sy * cosPitch - z1 * sinPitch;
      const z2 = sy * sinPitch + z1 * cosPitch;
      const cameraDistance = 3.1;
      const perspective = cameraDistance / (cameraDistance - z2);
      return {
        x: STAGE_WIDTH * 0.5 + x1 * 330 * perspective * cameraState.zoom,
        y: STAGE_HEIGHT * 0.52 - y1 * 290 * perspective * cameraState.zoom,
        depth: clamp((z2 + 1.9) / 3.8, 0.0, 1.0),
        scale: perspective,
      };
    }

    function layoutStage() {
      if (!currentScene) {
        return;
      }
      updateCameraHint();
      currentProjection = new Map(currentScene.nodes.map((node) => [node.cell_id, projectNode(node)]));
      Array.from(edgeLayer.children).forEach((line) => {
        const source = currentProjection.get(Number(line.dataset.source));
        const target = currentProjection.get(Number(line.dataset.target));
        const meanDepth = 0.5 * (source.depth + target.depth);
        const baseOpacity = Number(line.dataset.baseOpacity);
        const baseWidth = Number(line.dataset.baseWidth);
        line.setAttribute('x1', String(source.x));
        line.setAttribute('y1', String(source.y));
        line.setAttribute('x2', String(target.x));
        line.setAttribute('y2', String(target.y));
        line.setAttribute(
          'stroke-opacity',
          String(currentScene.coord_dim === 3 ? baseOpacity * (0.4 + meanDepth * 0.8) : baseOpacity)
        );
        line.setAttribute(
          'stroke-width',
          String(currentScene.coord_dim === 3 ? baseWidth * (0.72 + meanDepth * 0.72) : baseWidth)
        );
      });
      Array.from(nodeLayer.children).forEach((group) => {
        const nodeId = Number(group.dataset.nodeId);
        const node = currentNodeById.get(nodeId);
        const projection = currentProjection.get(nodeId);
        const halo = group.querySelector('.node-halo');
        const core = group.querySelector('.node-core');
        const coreRadius = currentScene.coord_dim === 3
          ? 3.0 + projection.depth * 2.8 + (projection.scale - 1.0) * 1.6
          : 3.3 + node.depth * 2.2;
        const haloRadius = currentScene.coord_dim === 3
          ? 12.0 + projection.depth * 10.0 + (projection.scale - 1.0) * 6.0
          : 11.0 + node.depth * 9.0;
        halo.setAttribute('cx', String(projection.x));
        halo.setAttribute('cy', String(projection.y));
        halo.setAttribute('r', String(haloRadius));
        halo.setAttribute(
          'fill-opacity',
          String(currentScene.coord_dim === 3 ? 0.1 + projection.depth * 0.24 : 0.14 + node.depth * 0.14)
        );
        core.setAttribute('cx', String(projection.x));
        core.setAttribute('cy', String(projection.y));
        core.setAttribute('r', String(coreRadius));
      });
    }

    function renderMetrics(scene) {
      metricsEl.innerHTML = '';
      const entries = [
        ['Cells', scene.metrics.num_cells],
        ['Visible edges', scene.metrics.num_edges],
        ['Local / patch', `${scene.metrics.num_local_edges} / ${scene.metrics.num_patch_edges}`],
        ['Wrap edges', scene.metrics.num_wraparound_edges],
        ['Boundary', scene.metrics.wrap ? 'Wraparound' : 'Open'],
        ['Shape', scene.metrics.coord_shape.join(' × ')],
      ];
      entries.forEach(([label, value]) => {
        const card = document.createElement('div');
        card.className = 'metric-card';
        card.innerHTML = `<div class="metric-label">${label}</div><div class="metric-value">${value}</div>`;
        metricsEl.appendChild(card);
      });
    }

    function renderLegend(scene) {
      legendEl.innerHTML = '';
      const items = [
        ['Input shell', palette['input-shell'], `${scene.metrics.num_input_cells} cells`],
        ['Output shell', palette['output-shell'], `${scene.metrics.num_output_cells} cells`],
        ['sLSTM', palette.slstm, `${scene.metrics.family_counts.slstm || 0} cells`],
        ['AxonCell', palette.axoncell, `${scene.metrics.family_counts.axoncell || 0} cells`],
        ['Local synapse', '#66e3ff', `${scene.metrics.num_local_edges} edges`],
        ['Patch synapse', '#ff8abb', `${scene.metrics.num_patch_edges} edges`],
        ['Wrap synapse', '#ffd666', `${scene.metrics.num_wraparound_edges} edges`],
      ];
      items.forEach(([label, color, value]) => {
        const row = document.createElement('div');
        row.className = 'legend-item';
        row.innerHTML = `
          <div class="legend-label">
            <span class="legend-swatch" style="color: ${color}; background: ${color};"></span>${label}
          </div>
          <div>${value}</div>
        `;
        legendEl.appendChild(row);
      });
    }

    function renderInfo(node) {
      if (!node) {
        const viewHintLabel = currentScene.coord_dim === 3 ? 'Drag to orbit' : 'Depth';
        const viewHintValue = currentScene.coord_dim === 3 ? 'Volumetric view' : 'Layer glow';
        infoEl.innerHTML = `
          <div class="info-row"><span>Hover</span><strong>Cell metadata</strong></div>
          <div class="info-row"><span>Click</span><strong>Trace synapses</strong></div>
          <div class="info-row"><span>${viewHintLabel}</span><strong>${viewHintValue}</strong></div>
        `;
        return;
      }
      infoEl.innerHTML = `
        <div class="info-row"><span>Cell</span><strong>#${node.cell_id}</strong></div>
        <div class="info-row"><span>Role</span><strong>${node.role}</strong></div>
        <div class="info-row"><span>Family</span><strong>${node.family}</strong></div>
        <div class="info-row"><span>Coord</span><strong>${node.coord.join(', ')}</strong></div>
        <div class="info-row"><span>Fan-in</span><strong>${node.fan_in}</strong></div>
        <div class="info-row"><span>KV group</span><strong>${node.kv_group}</strong></div>
      `;
    }

    function renderScene(scene) {
      const previousDim = currentScene ? currentScene.coord_dim : scene.coord_dim;
      currentScene = scene;
      currentNodeById = new Map(scene.nodes.map((node) => [node.cell_id, node]));
      if (scene.coord_dim !== 3) {
        cameraState = defaultCameraStateForScene(scene);
      } else if (previousDim !== 3) {
        cameraState = defaultCameraStateForScene(scene);
      }
      titleEl.textContent = scene.title;
      renderMetrics(scene);
      renderLegend(scene);
      renderInfo(scene.nodes.find((node) => node.cell_id === activeNodeId) || null);

      edgeLayer.innerHTML = '';
      nodeLayer.innerHTML = '';

      const edgeFragment = document.createDocumentFragment();
      scene.edges.forEach((edge) => {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('class', `stage-line ${edge.edge_type}${edge.wraparound ? ' wrap' : ''}`);
        line.dataset.source = String(edge.source);
        line.dataset.target = String(edge.target);
        line.dataset.edgeType = edge.edge_type;
        line.dataset.wraparound = edge.wraparound ? '1' : '0';
        line.dataset.baseOpacity = String(Math.min(0.95, 0.18 + edge.strength * 0.55));
        line.dataset.baseWidth = edge.edge_type === 'patch' ? '1.6' : '1.25';
        edgeFragment.appendChild(line);
      });
      edgeLayer.appendChild(edgeFragment);

      const nodeFragment = document.createDocumentFragment();
      scene.nodes.forEach((node) => {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.setAttribute('class', 'node-group');
        group.dataset.nodeId = String(node.cell_id);
        group.dataset.role = node.role;
        group.dataset.family = node.family;

        const halo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        halo.setAttribute('class', 'node-halo');
        halo.setAttribute('fill', nodeColor(node));

        const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        core.setAttribute('class', 'node-core');
        core.setAttribute('fill', nodeColor(node));

        group.appendChild(halo);
        group.appendChild(core);
        group.addEventListener('pointerdown', (event) => {
          event.stopPropagation();
        });
        group.addEventListener('mouseenter', () => {
          renderInfo(node);
        });
        group.addEventListener('mouseleave', () => {
          if (activeNodeId === null) {
            renderInfo(null);
          } else {
            renderInfo(currentNodeById.get(activeNodeId));
          }
        });
        group.addEventListener('click', () => {
          activeNodeId = node.cell_id === activeNodeId ? null : node.cell_id;
          applyHighlighting();
        });
        nodeFragment.appendChild(group);
      });
      nodeLayer.appendChild(nodeFragment);
      layoutStage();
      applyHighlighting();
    }

    function applyHighlighting() {
      const nodeGroups = Array.from(nodeLayer.querySelectorAll('.node-group'));
      const lines = Array.from(edgeLayer.querySelectorAll('.stage-line'));
      if (activeNodeId === null) {
        nodeGroups.forEach((group) => group.classList.remove('dimmed', 'active'));
        lines.forEach((line) => line.classList.remove('active', 'hidden'));
        renderInfo(null);
        return;
      }
      const node = currentNodeById.get(activeNodeId) || null;
      renderInfo(node);
      nodeGroups.forEach((group) => {
        const nodeId = Number(group.dataset.nodeId);
        const connected = currentScene.edges.some((edge) => edge.source === activeNodeId && edge.target === nodeId)
          || currentScene.edges.some((edge) => edge.target === activeNodeId && edge.source === nodeId)
          || nodeId === activeNodeId;
        group.classList.toggle('active', nodeId === activeNodeId);
        group.classList.toggle('dimmed', !connected);
      });
      lines.forEach((line) => {
        const source = Number(line.dataset.source);
        const target = Number(line.dataset.target);
        const connected = source === activeNodeId || target === activeNodeId;
        line.classList.toggle('active', connected);
        line.classList.toggle('hidden', !connected && activeNodeId !== null);
      });
    }

    function finishOrbiting(event) {
      if (!dragState) {
        return;
      }
      dragState = null;
      viewportEl.classList.remove('is-orbiting');
      if (event && event.pointerId !== undefined && viewportEl.hasPointerCapture(event.pointerId)) {
        viewportEl.releasePointerCapture(event.pointerId);
      }
      statusEl.textContent = currentScene.coord_dim === 3
        ? '3D fabric orbit ready. Drag to rotate or scroll to zoom.'
        : '2D fabric projection ready.';
    }

    function readControls() {
      return {
        title: document.getElementById('title').value,
        max_edges: Number(document.getElementById('max-edges').value),
        width: Number(document.getElementById('width').value),
        height: Number(document.getElementById('height').value),
        depth: Number(document.getElementById('depth').value),
        hidden_size: Number(document.getElementById('hidden-size').value),
        local_radius: Number(document.getElementById('local-radius').value),
        patch_edges_per_cell: Number(document.getElementById('patch-edges').value),
        patch_min_dist: Number(document.getElementById('patch-min-dist').value),
        patch_max_dist: Number(document.getElementById('patch-max-dist').value),
        wrap: document.getElementById('wrap').checked,
        input_band_width: Number(document.getElementById('input-band-width').value),
        output_band_width: Number(document.getElementById('output-band-width').value),
        family_mode: document.getElementById('family-mode').value,
        slstm_mix: Number(document.getElementById('slstm-mix').value),
        cell_arrangement: document.getElementById('cell-arrangement').value,
        seed: Number(document.getElementById('seed').value),
      };
    }

    async function requestScene(controls) {
      currentControls = controls;
      titleEl.textContent = controls.title;
      if (!apiPath) {
        statusEl.textContent = 'Static export loaded. Start the visualizer with --serve to regenerate anatomy live.';
        return;
      }
      statusEl.textContent = 'Rendering fresh fabric anatomy...';
      const response = await fetch(apiPath, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(controls),
      });
      if (!response.ok) {
        statusEl.textContent = `Render failed: ${response.status}`;
        return;
      }
      const scene = await response.json();
      const cellCount = scene.metrics.num_cells;
      const wrapEdgeCount = scene.metrics.num_wraparound_edges;
      const edgeCount = scene.metrics.num_edges;
      statusEl.textContent = `Rendered ${cellCount} cells, ${edgeCount} visible edges, ${wrapEdgeCount} wrap edges.`;
      activeNodeId = null;
      renderScene(scene);
    }

    formEl.addEventListener('submit', (event) => {
      event.preventDefault();
      requestScene(readControls());
    });

    slstmMixEl.addEventListener('input', updateMixLabel);
    document.getElementById('wrap').addEventListener('change', () => {
      requestScene(readControls());
    });

    viewportEl.addEventListener('pointerdown', (event) => {
      if (currentScene.coord_dim !== 3 || event.button !== 0) {
        return;
      }
      dragState = {
        pointerId: event.pointerId,
        x: event.clientX,
        y: event.clientY,
        yaw: cameraState.yaw,
        pitch: cameraState.pitch,
      };
      viewportEl.classList.add('is-orbiting');
      viewportEl.setPointerCapture(event.pointerId);
      statusEl.textContent = 'Orbiting fabric volume...';
    });

    viewportEl.addEventListener('pointermove', (event) => {
      if (!dragState || currentScene.coord_dim !== 3) {
        return;
      }
      const dx = event.clientX - dragState.x;
      const dy = event.clientY - dragState.y;
      cameraState.yaw = dragState.yaw + dx * 0.0065;
      cameraState.pitch = clamp(dragState.pitch + dy * 0.0052, -1.18, 1.18);
      layoutStage();
    });

    viewportEl.addEventListener('pointerup', finishOrbiting);
    viewportEl.addEventListener('pointercancel', finishOrbiting);
    viewportEl.addEventListener('lostpointercapture', finishOrbiting);
    viewportEl.addEventListener(
      'wheel',
      (event) => {
        if (currentScene.coord_dim !== 3) {
          return;
        }
        event.preventDefault();
        const scale = event.deltaY < 0 ? 1.08 : 0.92;
        cameraState.zoom = clamp(cameraState.zoom * scale, 0.55, 2.4);
        layoutStage();
        statusEl.textContent = `Zoom ${cameraState.zoom.toFixed(2)}x`;
      },
      { passive: false }
    );

    resetCameraButton.addEventListener('click', () => {
      cameraState = defaultCameraStateForScene(currentScene);
      layoutStage();
      statusEl.textContent = currentScene.coord_dim === 3
        ? 'Camera reset to default orbit.'
        : '2D fabrics use a flat projection.';
    });

    document.querySelectorAll('[data-preset]').forEach((button) => {
      button.addEventListener('click', () => {
        const preset = presets[button.dataset.preset];
        currentControls = { ...currentControls, ...preset };
        populateForm(currentControls);
        requestScene(readControls());
      });
    });

    populateForm(currentControls);
    renderScene(currentScene);
    updateMixLabel();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "FabricScene",
    "FabricSceneEdge",
    "FabricSceneMetrics",
    "FabricSceneNode",
    "FabricVisualizerControls",
    "build_fabric_scene",
    "main",
    "render_fabric_html",
    "serve_fabric_visualizer",
    "write_fabric_html",
]
