from __future__ import annotations

import json
import threading
from urllib import request

from cortex.fabric import FabricConfig, FabricFamilyConfig, init_fabric
from cortex.visualization.fabric import (
    FabricVisualizerControls,
    build_fabric_scene,
    render_fabric_html,
    serve_fabric_visualizer,
    write_fabric_html,
)


def test_build_fabric_scene_tracks_ports_and_edge_families():
    spec = init_fabric(
        FabricConfig(
            width=5,
            height=4,
            hidden_size=8,
            families={
                "slstm": FabricFamilyConfig(family_type="slstm"),
                "axoncell": FabricFamilyConfig(family_type="axoncell"),
            },
            cell_mix={"slstm": 0.5, "axoncell": 0.5},
            patch_edges_per_cell=1,
            projection_region_shape=(2, 2),
            input_band_width=1,
            output_band_width=1,
            seed=13,
        )
    )

    scene = build_fabric_scene(spec, title="Frontal Fabric", max_edges=512)

    assert scene.coord_dim == 2
    assert scene.metrics.num_cells == spec.anatomy.num_cells
    assert scene.metrics.num_input_cells == int(spec.input_cell_idx.numel())
    assert scene.metrics.num_output_cells == int(spec.output_cell_idx.numel())
    assert len(scene.nodes) == spec.anatomy.num_cells
    assert len(scene.edges) > 0
    assert any(node.role == "input" for node in scene.nodes)
    assert any(node.role == "output" for node in scene.nodes)
    assert any(edge.edge_type == "local" for edge in scene.edges)
    assert scene.metrics.num_wraparound_edges >= 0


def test_build_fabric_scene_marks_wraparound_edges():
    wrapped = build_fabric_scene(
        init_fabric(
            FabricConfig(
                width=4,
                height=4,
                hidden_size=8,
                families={"slstm": FabricFamilyConfig(family_type="slstm")},
                cell_mix={"slstm": 1.0},
                patch_edges_per_cell=0,
                input_band_width=1,
                output_band_width=1,
                local_radius=1.5,
                wrap=True,
                seed=3,
            )
        ),
        max_edges=1024,
    )
    unwrapped = build_fabric_scene(
        init_fabric(
            FabricConfig(
                width=4,
                height=4,
                hidden_size=8,
                families={"slstm": FabricFamilyConfig(family_type="slstm")},
                cell_mix={"slstm": 1.0},
                patch_edges_per_cell=0,
                input_band_width=1,
                output_band_width=1,
                local_radius=1.5,
                wrap=False,
                seed=3,
            )
        ),
        max_edges=1024,
    )

    assert wrapped.metrics.num_wraparound_edges > 0
    assert unwrapped.metrics.num_wraparound_edges == 0
    assert any(edge.wraparound for edge in wrapped.edges)
    assert all(not edge.wraparound for edge in unwrapped.edges)


def test_build_fabric_scene_projects_3d_geometry():
    spec = init_fabric(
        FabricConfig(
            width=3,
            height=3,
            depth=2,
            hidden_size=4,
            families={"slstm": FabricFamilyConfig(family_type="slstm")},
            cell_mix={"slstm": 1.0},
            projection_region_shape=(1, 1, 1),
            wrap=False,
        )
    )

    scene = build_fabric_scene(spec, title="Volumetric Fabric", max_edges=256)

    assert scene.coord_dim == 3
    assert any(node.depth > 0.0 for node in scene.nodes)
    assert all(0.0 <= node.x <= 1.0 for node in scene.nodes)
    assert all(0.0 <= node.y <= 1.0 for node in scene.nodes)
    assert all(len(node.space) == 3 for node in scene.nodes)
    assert any(node.space[2] > 0.0 for node in scene.nodes)
    assert any(node.space[2] < 0.0 for node in scene.nodes)


def test_render_fabric_html_embeds_scene_json_and_styles(tmp_path):
    spec = init_fabric(FabricConfig(width=4, height=4, hidden_size=8))
    scene = build_fabric_scene(spec, title="Neural Atlas", max_edges=128)

    html = render_fabric_html(scene)

    assert "Neural Atlas" in html
    assert "fabric-scene-data" in html
    assert "synaptic-haze" in html
    assert 'id="scene-form"' in html
    assert "Render fabric" in html
    assert "Reset orbit" in html
    assert "Drag to orbit" in html
    assert "stopPropagation" in html
    assert "Wrap loop" in html
    assert "num_wraparound_edges" in html

    json_payload = html.split('<script type="application/json" id="fabric-scene-data">', 1)[1].split("</script>", 1)[0]
    loaded = json.loads(json_payload)
    assert loaded["title"] == "Neural Atlas"
    assert loaded["metrics"]["num_cells"] == spec.anatomy.num_cells

    output_path = tmp_path / "fabric.html"
    write_fabric_html(spec, output_path, title="Neural Atlas", max_edges=128)
    assert output_path.exists()
    assert "Neural Atlas" in output_path.read_text()


def test_fabric_visualizer_server_serves_page_and_scene_json():
    controls = FabricVisualizerControls(width=4, height=4, hidden_size=8, max_edges=128, title="Interactive Atlas")
    server = serve_fabric_visualizer(host="127.0.0.1", port=0, controls=controls)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        page = request.urlopen(f"http://127.0.0.1:{port}/").read().decode("utf-8")
        assert "Interactive Atlas" in page
        payload = json.dumps(
            {
                "title": "Volumetric Atlas",
                "max_edges": 160,
                "width": 4,
                "height": 3,
                "depth": 2,
                "hidden_size": 8,
                "local_radius": 1.75,
                "patch_edges_per_cell": 1,
                "patch_min_dist": 2.0,
                "patch_max_dist": 6.0,
                "wrap": False,
                "input_band_width": 1,
                "output_band_width": 1,
                "cell_arrangement": "random",
                "family_mode": "mixed",
                "slstm_mix": 0.5,
                "seed": 5,
            }
        ).encode("utf-8")
        response = request.urlopen(
            request.Request(
                f"http://127.0.0.1:{port}/api/scene",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
        )
        scene = json.loads(response.read().decode("utf-8"))
        assert scene["title"] == "Volumetric Atlas"
        assert scene["coord_dim"] == 3
        assert scene["metrics"]["num_edges"] > 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
