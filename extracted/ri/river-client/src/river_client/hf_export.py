"""Convert downloaded River LoRA adapters to the base model's HF/PEFT layout.

Only safetensors headers are fetched for the base model; its weights are never
loaded. Conversion runs on CPU and leaves the source checkpoint unchanged.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path

from huggingface_hub import get_safetensors_metadata

_PEFT_PREFIX = "base_model.model."
_LORA_KEY = re.compile(r"^base_model\.model\.(.+)\.lora_([AB])\.weight$")
_TEXT_PREFIXES = (
    "model.language_model.model.",
    "model.language_model.",
    "language_model.model.",
    "language_model.",
    "model.",
)


def _contained_path(root: Path, name: str) -> Path:
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Checkpoint file escapes its directory: {name}")
    # HF snapshots use shard symlinks into ../../blobs. Validate the index
    # filename, but preserve the symlink path for weight-map comparisons.
    return root / path


def _weight_files(root: Path, stem: str) -> tuple[list[Path], dict[str, str] | None]:
    index_path = root / f"{stem}.safetensors.index.json"
    single_path = root / f"{stem}.safetensors"
    if index_path.exists() and single_path.exists():
        raise ValueError(f"Ambiguous checkpoint: both {single_path} and {index_path}")
    if index_path.exists():
        weight_map = json.loads(index_path.read_text())["weight_map"]
        if not weight_map:
            raise ValueError(f"Empty weight map: {index_path}")
        return [
            _contained_path(root, name) for name in sorted(set(weight_map.values()))
        ], weight_map
    if not single_path.is_file():
        raise FileNotFoundError(f"No {stem} safetensors checkpoint in {root}")
    return [single_path], None


def _base_shapes(base_model: str, revision: str | None) -> dict[str, tuple[int, ...]]:
    from safetensors import safe_open

    root = Path(base_model).resolve()
    if root.is_dir():
        files, weight_map = _weight_files(root, "model")
        shapes = {}
        for path in files:
            with safe_open(path, framework="pt", device="cpu") as shard:
                for key in shard.keys():
                    if key in shapes:
                        raise ValueError(f"Duplicate base tensor: {key}")
                    if (
                        weight_map is not None
                        and weight_map.get(key)
                        != path.relative_to(root.resolve()).as_posix()
                    ):
                        raise ValueError(
                            f"Base weight index disagrees with shard for {key}"
                        )
                    shapes[key] = tuple(shard.get_slice(key).get_shape())
        if weight_map is not None and shapes.keys() != weight_map.keys():
            raise ValueError("Base checkpoint is missing indexed tensors")
        return shapes
    metadata = get_safetensors_metadata(base_model, revision=revision)
    return {
        key: tuple(info.shape)
        for file in metadata.files_metadata.values()
        for key, info in file.tensors.items()
    }


def _text_path(module: str) -> str:
    for prefix in _TEXT_PREFIXES:
        if module.startswith(prefix):
            return module.removeprefix(prefix)
    return module


def _matching_modules(module: str, shapes: dict[str, tuple[int, ...]]) -> list[str]:
    if f"{module}.weight" in shapes:
        return [module]
    # River strips the text-model wrapper. Match only the documented wrappers,
    # never an arbitrary suffix that could accidentally select the vision tower.
    return [
        name.removesuffix(".weight")
        for name in shapes
        if name.endswith(".weight")
        and _text_path(name.removesuffix(".weight")) == _text_path(module)
    ]


def _resolve_module(module: str, shapes: dict[str, tuple[int, ...]]) -> str:
    candidates = _matching_modules(module, shapes)
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one HF base module for {module}, found {candidates}"
        )
    return candidates[0]


def _pattern_value(patterns: dict, module: str, default: float) -> float:
    for pattern, value in patterns.items():
        if re.match(rf"(.*\.)?({pattern})$", module):
            return value
    return default


def _export_fused_experts(pairs, shapes, config):
    """Map independent expert updates to PEFT's 3D parameter adapters.

    Qwen's fused expert Parameters are [experts, out, in]. PEFT 0.18
    factors a 3D Parameter as einsum("ore,eri->eio"), so its factors
    are the transposes of the ordinary Linear factors. Independent gate
    and up updates occupy disjoint rank blocks; sharing A would change
    the trained function.
    """
    groups = {}
    for module in list(pairs):
        match = re.fullmatch(r"(.+\.experts)\.(\d+)\.(gate|up|down)_proj", module)
        if match is None or _matching_modules(module, shapes):
            continue
        owner, expert, projection = match.groups()
        groups.setdefault(owner, {})[(int(expert), projection)] = (
            module,
            pairs.pop(module),
        )
    tensors, parameters, ranks, alphas = {}, [], {}, {}
    for owner, experts in sorted(groups.items()):
        if config.get("lora_dropout", 0):
            raise ValueError(
                "HF fused expert parameter adapters require lora_dropout=0"
            )
        targets = []
        for parameter, projections in (
            ("gate_up_proj", ("gate", "up")),
            ("down_proj", ("down",)),
        ):
            if not any(projection in projections for expert, projection in experts):
                continue
            candidates = [
                name
                for name in shapes
                if _text_path(name) == _text_path(f"{owner}.{parameter}")
            ]
            if len(candidates) != 1:
                raise ValueError(
                    f"Expected one fused HF expert parameter for {owner}.{parameter}, found {candidates}"
                )
            target = candidates[0]
            shape = shapes[target]
            if len(shape) != 3:
                raise ValueError(f"Fused expert parameter must be 3D: {target}")
            count, rows, columns = shape
            block_rows = rows // len(projections)
            factors = {}
            projection_ranks = {}
            for projection in projections:
                projection_ranks[projection] = 0
                for expert in range(count):
                    source = experts.get((expert, projection))
                    if source is None:
                        continue
                    module, pair = source
                    if pair.keys() != {"A", "B"}:
                        raise ValueError(f"Missing LoRA A/B pair for {module}")
                    a, b = pair["A"], pair["B"]
                    rank = _pattern_value(
                        config.get("rank_pattern", {}), module, config["r"]
                    )
                    alpha = _pattern_value(
                        config.get("alpha_pattern", {}), module, config["lora_alpha"]
                    )
                    if tuple(a.shape) != (rank, columns) or tuple(b.shape) != (
                        block_rows,
                        rank,
                    ):
                        raise ValueError(
                            f"LoRA dimensions for {module} do not match fused HF base {target}: {shape}"
                        )
                    factors[(expert, projection)] = (a, b, rank, alpha)
                    projection_ranks[projection] = max(
                        projection_ranks[projection], rank
                    )
            if any(expert < 0 or expert >= count for expert, projection in experts):
                raise ValueError(f"Expert id outside fused HF parameter: {target}")
            rank = sum(projection_ranks.values())
            if not rank:
                raise ValueError(f"No adapter factors for fused HF parameter: {target}")
            sample = next(iter(factors.values()))[0]
            if any(
                a.dtype != sample.dtype or b.dtype != sample.dtype
                for a, b, rank, alpha in factors.values()
            ):
                raise ValueError(
                    f"Mixed expert adapter dtypes for fused HF parameter: {target}"
                )
            a_peft = sample.new_zeros(count, rank, rows)
            b_peft = sample.new_zeros(columns, rank, count)
            denominator = rank ** (0.5 if config.get("use_rslora", False) else 1)
            first = next(iter(factors.values()))
            output_scale = first[3] / first[2] ** (
                0.5 if config.get("use_rslora", False) else 1
            )
            output_scale = output_scale or 1.0
            output_alpha = output_scale * denominator
            offset = 0
            for block, projection in enumerate(projections):
                for expert in range(count):
                    if (expert, projection) not in factors:
                        continue
                    a, b, source_rank, alpha = factors[(expert, projection)]
                    source_scale = alpha / source_rank ** (
                        0.5 if config.get("use_rslora", False) else 1
                    )
                    a_peft[
                        expert,
                        offset : offset + source_rank,
                        block * block_rows : (block + 1) * block_rows,
                    ] = b.T
                    b_peft[:, offset : offset + source_rank, expert] = a.T * (
                        source_scale / output_scale
                    )
                offset += projection_ranks[projection]
            targets.append(
                (target, a_peft.flatten(0, 1), b_peft.flatten(1, 2), rank, output_alpha)
            )
        # PEFT nests a wrapper for each target parameter on the same module,
        # in Qwen's declaration order (gate/up then down), outermost last.
        for index, (target, a, b, rank, alpha) in enumerate(targets):
            module = target.rsplit(".", 1)[0] + ".base_layer" * (
                len(targets) - index - 1
            )
            tensors[f"{_PEFT_PREFIX}{module}.lora_A.weight"] = a.contiguous()
            tensors[f"{_PEFT_PREFIX}{module}.lora_B.weight"] = b.contiguous()
            parameters.append(target)
            ranks[target] = rank
            alphas[target] = alpha
    return tensors, parameters, ranks, alphas


def export_hf_adapter(
    source_dir: str | Path,
    output_dir: str | Path,
    *,
    base_model: str | None = None,
    revision: str | None = None,
) -> Path:
    """Write a validated HF/PEFT adapter to a new directory, atomically.

    Resolve every module against the base checkpoint's safetensors metadata.
    Split River's Qwen Q/K/V/Z LoRA B rows into Q/K/V and Z, duplicating A so
    the effective update B @ A (including rank/alpha scaling) is unchanged.
    Indexed River adapter shards are consolidated for PEFT's single-file loader.
    Install ``river-client[hf-export]`` to use this CPU-only conversion path.
    """
    from safetensors.torch import load_file, save_file

    source = Path(source_dir).resolve()
    output = Path(output_dir).resolve()
    if output.exists():
        raise FileExistsError(f"HF export destination already exists: {output}")
    config = json.loads((source / "adapter_config.json").read_text())
    if config.get("peft_type") != "LORA":
        raise ValueError("HF export requires a LoRA adapter checkpoint")
    # These alter the tensor layout or scaling beyond the standard A/B update.
    for option in (
        "use_dora",
        "fan_in_fan_out",
        "modules_to_save",
        "target_parameters",
        "lora_bias",
    ):
        if config.get(option):
            raise ValueError(f"HF export does not support {option}")
    if config.get("bias", "none") != "none":
        raise ValueError("HF export requires bias='none'")
    base_model = base_model or config.get("base_model_name_or_path")
    if not base_model:
        raise ValueError(
            "Specify base_model or set base_model_name_or_path in adapter_config.json"
        )
    revision = revision if revision is not None else config.get("revision")
    shapes = _base_shapes(base_model, revision)
    files, weight_map = _weight_files(source, "adapter_model")
    pairs = {}
    seen = set()
    for path in files:
        for key, tensor in load_file(path, device="cpu").items():
            if key in seen:
                raise ValueError(f"Duplicate adapter tensor: {key}")
            seen.add(key)
            if (
                weight_map is not None
                and weight_map.get(key) != path.relative_to(source).as_posix()
            ):
                raise ValueError(f"Adapter weight index disagrees with shard for {key}")
            match = _LORA_KEY.fullmatch(key)
            if match is None:
                raise ValueError(f"Unsupported adapter tensor: {key}")
            module, factor = match.groups()
            pairs.setdefault(module, {})[factor] = tensor
    if weight_map is not None and seen != weight_map.keys():
        raise ValueError("Adapter checkpoint is missing indexed tensors")
    if not pairs:
        raise ValueError("Adapter checkpoint has no LoRA tensors")

    tensors, parameters, ranks, alphas = _export_fused_experts(pairs, shapes, config)
    targets = set()
    for module, pair in pairs.items():
        if pair.keys() != {"A", "B"}:
            raise ValueError(f"Missing LoRA A/B pair for {module}")
        a, b = pair["A"], pair["B"]
        rank = _pattern_value(config.get("rank_pattern", {}), module, config["r"])
        alpha = _pattern_value(
            config.get("alpha_pattern", {}), module, config["lora_alpha"]
        )
        if a.ndim != 2 or b.ndim != 2 or a.shape[0] != rank or b.shape[1] != rank:
            raise ValueError(
                f"Invalid LoRA shapes/rank for {module}: A={tuple(a.shape)}, B={tuple(b.shape)}, r={rank}"
            )
        if module.endswith(".linear_attn.in_proj_qkvz") and not _matching_modules(
            module, shapes
        ):
            outputs = [
                _resolve_module(module.removesuffix("in_proj_qkvz") + suffix, shapes)
                for suffix in ("in_proj_qkv", "in_proj_z")
            ]
        else:
            outputs = [_resolve_module(module, shapes)]
        sizes = [shapes[f"{target}.weight"] for target in outputs]
        if (
            any(len(shape) != 2 or shape[1] != a.shape[1] for shape in sizes)
            or sum(shape[0] for shape in sizes) != b.shape[0]
        ):
            raise ValueError(
                f"LoRA dimensions for {module} do not match HF base weights: A={tuple(a.shape)}, B={tuple(b.shape)}, base={sizes}"
            )
        offset = 0
        for target, shape in zip(outputs, sizes, strict=True):
            if target in targets:
                raise ValueError(f"Multiple source modules map to {target}")
            targets.add(target)
            prefix = f"{_PEFT_PREFIX}{target}"
            # Clone A for split projections: safetensors forbids shared storage.
            tensors[f"{prefix}.lora_A.weight"] = a.clone().contiguous()
            tensors[f"{prefix}.lora_B.weight"] = (
                b[offset : offset + shape[0]].clone().contiguous()
            )
            offset += shape[0]
            if rank != config["r"]:
                ranks[target] = rank
            if alpha != config["lora_alpha"]:
                alphas[target] = alpha

    config = {
        key: value for key, value in config.items() if not key.startswith("_river_")
    }
    config.update(
        base_model_name_or_path=base_model,
        revision=revision,
        target_modules=sorted(targets),
        rank_pattern=ranks,
        alpha_pattern=alphas,
        layers_pattern=None,
        layers_to_transform=None,
        exclude_modules=None,
        inference_mode=True,
    )
    if parameters:
        config["target_parameters"] = parameters
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{output.name}-", dir=output.parent
    ) as staging:
        staged = Path(staging) / "adapter"
        staged.mkdir()
        save_file(
            tensors, staged / "adapter_model.safetensors", metadata={"format": "pt"}
        )
        (staged / "adapter_config.json").write_text(json.dumps(config, indent=2) + "\n")
        # A nonempty existing destination must never be replaced on a retry.
        if output.exists():
            raise FileExistsError(f"HF export destination already exists: {output}")
        os.rename(staged, output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--base-model")
    parser.add_argument("--revision")
    args = parser.parse_args()
    output = export_hf_adapter(
        args.source, args.output, base_model=args.base_model, revision=args.revision
    )
    print(f"HF adapter saved to {output}")


if __name__ == "__main__":
    main()
