"""Game build pipeline — scaffold → scripts → assets → build → heal.

Mirrors `principal_builder._heal_until_green`: the pipeline NEVER returns
silently with a broken build. If the build fails, we ask the LLM to
regenerate the offending scripts using the build log as context, then
rebuild. Cap 6 rounds. On exhaustion, raise `GameBuildIncomplete`.

Asset generators run concurrently — Imagen calls are network-bound and
benefit from parallelism. Mesh + audio are usually fast enough that
serial is fine, but we use the same ThreadPoolExecutor for uniformity.
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from .assets import (
    AssetManifest,
    AudioGenerator,
    MeshGenerator,
    SpriteGenerator,
)
from .engines import get_adapter
from .engines.base import GamePlan, GameRequest
from .exceptions import (
    BuildNotSupported,
    EngineNotInstalled,
    GameBuildIncomplete,
    ScaffoldPollution,
)


# Per-engine "this directory was scaffolded by us" signature files. Used
# by `_detect_existing_engine` to spot a previous run's leftovers before
# we clobber them with a different engine.
_ENGINE_SIGNATURE_FILES: dict[str, tuple[str, ...]] = {
    "godot":   ("project.godot", ".godot"),
    "unity":   ("Assets/Editor/SageBuilder.cs", "ProjectSettings/ProjectVersion.txt"),
    "unreal":  ("Source",),    # plus a *.uproject sibling; checked separately
    "bevy":    ("Cargo.toml", "src/main.rs"),
    "phaser":  ("package.json", "src/main.ts"),
    "love2d":  ("conf.lua", "main.lua"),
    "pygame":  ("requirements.txt", "main.py"),
    # GUI-only engines scaffold a README + assets/ dir only — too generic
    # to fingerprint, so we skip them in pollution detection.
}


def _detect_existing_engine(out_dir: Path) -> Optional[str]:
    """Return the engine name of an existing scaffold in `out_dir`, or
    None if the directory has no recognizable engine layout.

    Uses signature files unique to each engine. A directory with both
    Godot AND Unity signatures returns whichever has more matches —
    indicates that mixing has already happened and the user is one
    re-run away from total project corruption."""
    matches: list[tuple[int, str]] = []
    for engine, sigs in _ENGINE_SIGNATURE_FILES.items():
        hits = sum(1 for sig in sigs if (out_dir / sig).exists())
        # Unreal also needs a *.uproject file at the root
        if engine == "unreal" and not list(out_dir.glob("*.uproject")):
            hits = 0
        if hits > 0:
            matches.append((hits, engine))
    if not matches:
        return None
    # If only one engine matches → that's the existing engine.
    # If multiple → the one with the most signature hits wins (the dir
    # is already polluted; we surface whatever has more presence).
    matches.sort(reverse=True)
    return matches[0][1]


GenerateFn = Callable[[str], str]
ProgressFn = Callable[[str], None]


@dataclass
class GameBuildReport:
    """What the pipeline returns on success — and what's attached to
    GameBuildIncomplete on terminal failure."""

    engine: str
    out_dir: str
    target: str
    sprite_count: int = 0
    mesh_count: int = 0
    audio_count: int = 0
    scripts_written: list[str] = field(default_factory=list)
    build_artifact: Optional[str] = None
    build_size_bytes: int = 0
    build_duration_s: float = 0.0
    heal_rounds: int = 0
    install_hint: Optional[str] = None     # set when EngineNotInstalled raised

    def as_dict(self) -> dict:
        return {
            "engine": self.engine,
            "out_dir": self.out_dir,
            "target": self.target,
            "sprite_count": self.sprite_count,
            "mesh_count": self.mesh_count,
            "audio_count": self.audio_count,
            "scripts_written": self.scripts_written,
            "build_artifact": self.build_artifact,
            "build_size_bytes": self.build_size_bytes,
            "build_duration_s": self.build_duration_s,
            "heal_rounds": self.heal_rounds,
            "install_hint": self.install_hint,
        }


# Two LLM calls per build, both small:
#   1) Decompose: "this is a platformer about X, here are the entities + features"
#   2) (Per heal round) "the build failed with <log>, regen these files"

_DECOMPOSE_PROMPT = """A user wants to make a game. Extract the spec.

Prompt: {prompt!r}
Engine: {engine}
Detected genre: {genre}
Detected perspective: {perspective}

Output JSON with these keys:
  title         — short title for the game
  description   — 1–2 sentence pitch
  features      — list of 3–6 short gameplay features
  sprites       — list of {{"role": "<id>", "prompt": "<imagen prompt>"}} entries
                  for every sprite the game will need
  meshes        — same shape, for 3D meshes (empty list for 2D games)
  audio         — list of {{"role": "<id>", "prompt": "<music/sfx prompt>",
                  "kind": "music" | "sfx"}}

Output ONLY the JSON. No prose, no markdown."""


def _decompose(
    request: GameRequest,
    *,
    generate: GenerateFn,
    log: ProgressFn,
) -> GamePlan:
    """Ask the LLM to flesh out the request into a buildable plan."""
    prompt = _DECOMPOSE_PROMPT.format(
        prompt=request.raw_prompt,
        engine=request.engine or "auto",
        genre=request.genre or "(unspecified)",
        perspective=request.perspective or "(unspecified)",
    )
    raw = generate(prompt)   # exceptions propagate — no silent fallback

    data: dict = {}
    start, end = raw.find("{"), raw.rfind("}")
    if start != -1 and end != -1:
        try:
            data = json.loads(raw[start : end + 1])
        except (json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError(
                f"decompose: LLM returned unparseable JSON. "
                f"Head:\n{raw[:600]!r}"
            ) from exc
    if not data:
        raise RuntimeError(
            "decompose: LLM response had no JSON object. "
            f"Head:\n{raw[:600]!r}"
        )

    title = data.get("title")
    desc = data.get("description") or request.raw_prompt
    features = data.get("features") or []
    if not title:
        # An LLM that can't pick a title for a game is failing its job.
        raise RuntimeError(
            f"decompose: LLM omitted required 'title' field. "
            f"Keys returned: {list(data.keys())}"
        )

    # Asset roles must come from the LLM — no synthetic 'player' /
    # 'ambient' fallbacks. If the LLM didn't list any sprites for a 2D
    # game (or any meshes for a 3D game), surface that as a real error.
    sprites = [
        (s["role"], s["prompt"])
        for s in (data.get("sprites") or []) if isinstance(s, dict)
        and s.get("role") and s.get("prompt")
    ]
    meshes = [
        (m["role"], m["prompt"])
        for m in (data.get("meshes") or []) if isinstance(m, dict)
        and m.get("role") and m.get("prompt")
    ]
    audio = [
        (a["role"], a["prompt"], a.get("kind", "music"))
        for a in (data.get("audio") or []) if isinstance(a, dict)
        and a.get("role") and a.get("prompt")
    ]

    return GamePlan(
        request=request, title=title, description=desc, features=features,
        sprite_roles=sprites, mesh_roles=meshes, audio_roles=audio,
        target=request.target,
    )


def _generate_assets(
    plan: GamePlan,
    out_dir: Path,
    *,
    log: ProgressFn,
) -> AssetManifest:
    """Run sprite/mesh/audio generators in parallel, return manifest.

    Animated assets are emitted alongside static ones — the manifest
    keeps them in separate dicts so engine adapters can decide which
    convention fits (Godot SpriteFrames vs Phaser TextureAtlas vs Unity
    Animator). Mesh animation tracks ride inside the GLB itself; we just
    record which roles have which clips in `manifest.mesh_animations`.
    """
    manifest = AssetManifest()
    asset_root = out_dir / ".sage_assets"
    sprite_gen = SpriteGenerator(asset_root / "sprites",
                                   style=plan.request.art_style or "pixel")
    mesh_gen = MeshGenerator(asset_root / "meshes")
    audio_gen = AudioGenerator(asset_root / "audio")

    futures: dict = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        for role, prompt in plan.sprite_roles:
            futures[pool.submit(sprite_gen.generate, role, prompt)] = ("sprite", role)
        # Animated sprites: emit the static base PNG + one strip per state.
        # Engine adapters that don't know about animations still get the
        # base sprite; ones that do can read the strips from the manifest.
        for role, prompt, states in plan.animated_sprite_roles:
            if (role, "_static_base") not in futures.values():
                futures[pool.submit(sprite_gen.generate, role, prompt)] = ("sprite", role)
            for state in (states or ["idle", "walk"]):
                futures[pool.submit(
                    sprite_gen.generate_animated, role, prompt, state,
                )] = ("sprite_anim", (role, state))
        for role, prompt in plan.mesh_roles:
            futures[pool.submit(mesh_gen.generate, role, prompt)] = ("mesh", role)
        for role, prompt, kind in plan.audio_roles:
            fn = audio_gen.generate_music if kind == "music" else audio_gen.generate_sfx
            futures[pool.submit(fn, role, prompt)] = ("audio", role)

        for future in as_completed(futures):
            kind, key = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # noqa: BLE001 — never fail whole build for one asset
                log(f"  [assets] {kind}:{key} failed: {exc}")
                continue
            if kind == "sprite":
                manifest.sprites[key] = result.path
            elif kind == "sprite_anim":
                # key is (role, state); result is SpriteAnimationResult
                manifest.sprite_animations[key] = result.path
            elif kind == "mesh":
                manifest.meshes[key] = result.path
                # If this was a character role with animations baked into
                # the GLB, record the clip names so engine adapters can
                # wire AnimationPlayer / Animator hookups.
                if getattr(result, "animations", None):
                    manifest.mesh_animations[key] = list(result.animations)
            else:
                manifest.audio[key] = result.path

    log(f"  [assets] {manifest.total_count()} files: "
        f"{len(manifest.sprites)} sprites, "
        f"{len(manifest.sprite_animations)} sprite-anim strips, "
        f"{len(manifest.meshes)} meshes "
        f"({sum(len(a) for a in manifest.mesh_animations.values())} mesh-anim clips), "
        f"{len(manifest.audio)} audio")
    return manifest


def _heal_round(
    plan: GamePlan,
    adapter,
    out_dir: Path,
    error_log: str,
    *,
    generate: GenerateFn,
    log: ProgressFn,
) -> None:
    """Ask the LLM to repair the scripts using the build log as context."""
    log("  [heal] regenerating scripts with build log as context...")
    # We re-issue the engine's script emission with the failure log appended
    # to the description, so the model sees what to fix.
    augmented_plan = GamePlan(
        request=plan.request,
        title=plan.title,
        description=(
            f"{plan.description}\n\n"
            f"PREVIOUS BUILD FAILED. Engine error log (tail):\n"
            f"```\n{error_log[-2000:]}\n```\n"
            f"Fix the scripts so the build succeeds."
        ),
        features=plan.features,
        sprite_roles=plan.sprite_roles,
        mesh_roles=plan.mesh_roles,
        audio_roles=plan.audio_roles,
        target=plan.target,
    )
    adapter.emit_scripts(augmented_plan, out_dir, generate=generate, log=log)


def build_game(
    request: GameRequest,
    out_dir: Path,
    generate: GenerateFn,
    *,
    progress: Optional[ProgressFn] = None,
    heal_rounds: int = 6,
) -> GameBuildReport:
    """End-to-end build.

    Caller (principal_builder or CLI) catches `GameBuildIncomplete` and
    surfaces a clear error. Caller catches `EngineNotInstalled` separately
    so we can prompt for install (or fall back to Godot).
    """
    log = progress or (lambda _m: None)
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    adapter = get_adapter(request.engine)
    log(f"[1/5] adapter: {adapter.name}")

    # Pollution guard: if the directory already has a DIFFERENT engine's
    # scaffold, refuse rather than mix. Real-world: a user re-ran sage
    # in HoleGame/ once with Godot (the buggy auto-pick) and once with
    # Unity (the corrected pick) — the result was a hybrid project that
    # neither editor could open.
    existing = _detect_existing_engine(out_dir)
    if existing and existing != adapter.name:
        raise ScaffoldPollution(
            requested_engine=adapter.name,
            existing_engine=existing,
            out_dir=str(out_dir),
        )

    # Detection runs first so we never burn LLM tokens on a build that
    # can't possibly produce a binary.
    binary = adapter.detect()
    if binary is None and adapter.capabilities & adapter.capabilities.BUILD:
        # Scaffold-only adapters (GameMaker/Construct/RPGMaker) have no
        # BUILD capability so detect() returning None is fine for them.
        raise EngineNotInstalled(adapter.name, adapter.install_hint())

    log("[2/5] decomposing prompt into plan...")
    plan = _decompose(request, generate=generate, log=log)

    log("[3/5] scaffolding + generating scripts + assets in parallel...")
    adapter.scaffold(plan, out_dir, log=log)
    written = adapter.emit_scripts(plan, out_dir, generate=generate, log=log)

    manifest = _generate_assets(plan, out_dir, log=log)
    adapter.consume_assets(manifest, out_dir, log=log)

    report = GameBuildReport(
        engine=adapter.name,
        out_dir=str(out_dir),
        target=plan.target,
        sprite_count=len(manifest.sprites),
        mesh_count=len(manifest.meshes),
        audio_count=len(manifest.audio),
        scripts_written=[str(p.relative_to(out_dir)) for p in written],
    )

    # ── Build + heal loop ─────────────────────────────────────────────
    if not (adapter.capabilities & adapter.capabilities.BUILD):
        log("[4/5] adapter doesn't support headless build — scaffold complete")
        return report

    log("[4/5] headless build...")
    last_error = ""
    for round_idx in range(heal_rounds + 1):
        try:
            artifact = adapter.build(out_dir, target=plan.target, log=log)
        except BuildNotSupported as exc:
            log(f"[build] {exc}")
            return report
        except (RuntimeError, Exception) as exc:  # noqa: BLE001 — heal on any failure
            last_error = str(exc)
            if round_idx >= heal_rounds:
                report.heal_rounds = round_idx
                raise GameBuildIncomplete(
                    f"build did not converge after {heal_rounds} heal rounds. "
                    f"Last error: {last_error[-300:]}",
                    report.as_dict(),
                ) from exc
            _heal_round(plan, adapter, out_dir, last_error,
                        generate=generate, log=log)
            continue

        report.build_artifact = str(artifact.output_path)
        report.build_size_bytes = artifact.size_bytes
        report.build_duration_s = artifact.duration_s
        report.heal_rounds = round_idx
        log(f"[5/5] complete: {artifact.output_path.name} "
            f"({artifact.size_bytes:,} bytes)")
        return report

    return report
