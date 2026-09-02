"""Evaluation harness for the agent-detection acceptance gate.

Test-only (no production callers): scores a list of
:class:`~runlayer_cli.scan.agents.detect.DiscoveredAgent` results against a
``labels.json`` answer key. Detections match labels by ``id`` == agent directory
basename (e.g. ``sample_01``); the harness compares the predicted framework
display name and language to the label.

Lives beside the tests (not in ``runlayer_cli``) so it never ships in the frozen
``aiwatch`` bundle. Standard-library only.
"""

from __future__ import annotations

import json
from pathlib import Path

from runlayer_cli.scan.agents.detect import DiscoveredAgent


def _load_labels(labels_path: str | Path) -> dict[str, dict]:
    data = json.loads(Path(labels_path).read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in data.get("samples", [])}


def evaluate_detections(
    detections: list[DiscoveredAgent], labels_path: str | Path
) -> dict:
    """Compare detections to labels; return accuracy metrics and per-sample rows."""
    labels = _load_labels(labels_path)
    detections_by_name = {d.name: d for d in detections}

    results: list[dict] = []
    framework_correct = 0
    language_correct = 0

    for sample_id, label in sorted(labels.items()):
        detection = detections_by_name.get(sample_id)
        predicted_fw = detection.display_name if detection else None
        predicted_lang = detection.language if detection else None
        fw_ok = predicted_fw == label.get("framework")
        lang_ok = predicted_lang == label.get("language")
        framework_correct += int(fw_ok)
        language_correct += int(lang_ok)
        results.append(
            {
                "id": sample_id,
                "expected_framework": label.get("framework"),
                "predicted_framework": predicted_fw,
                "framework_correct": fw_ok,
                "expected_language": label.get("language"),
                "predicted_language": predicted_lang,
                "language_correct": lang_ok,
                "confidence": round(detection.confidence, 3) if detection else 0.0,
            }
        )

    total = len(labels)
    unlabeled = sorted(set(detections_by_name) - set(labels))
    mismatches = [
        r for r in results if not (r["framework_correct"] and r["language_correct"])
    ]

    return {
        "labels_path": str(labels_path),
        "total_labeled": total,
        "framework": {
            "correct": framework_correct,
            "total": total,
            "accuracy": (framework_correct / total) if total else 0.0,
        },
        "language": {
            "correct": language_correct,
            "total": total,
            "accuracy": (language_correct / total) if total else 0.0,
        },
        "results": results,
        "mismatches": mismatches,
        "missing": [r["id"] for r in results if r["predicted_framework"] is None],
        "unlabeled": unlabeled,
    }


def format_evaluation(result: dict) -> str:
    fw = result["framework"]
    lang = result["language"]
    lines = [
        f"Evaluation vs {result['labels_path']}",
        f"  framework accuracy: {fw['correct']}/{fw['total']} "
        f"({fw['accuracy'] * 100:.1f}%)",
        f"  language  accuracy: {lang['correct']}/{lang['total']} "
        f"({lang['accuracy'] * 100:.1f}%)",
    ]

    mismatches = result["mismatches"]
    if not mismatches:
        lines.append("  all samples classified correctly")
    else:
        lines.append(f"  {len(mismatches)} mismatch(es):")
        for r in mismatches:
            fw_flag = (
                ""
                if r["framework_correct"]
                else (
                    f" framework: expected {r['expected_framework']!r}, "
                    f"got {r['predicted_framework']!r}"
                )
            )
            lang_flag = (
                ""
                if r["language_correct"]
                else (
                    f" language: expected {r['expected_language']!r}, "
                    f"got {r['predicted_language']!r}"
                )
            )
            lines.append(f"    {r['id']}:{fw_flag}{lang_flag}")

    if result["unlabeled"]:
        lines.append(
            f"  note: {len(result['unlabeled'])} detected unit(s) had no label: "
            + ", ".join(result["unlabeled"])
        )
    return "\n".join(lines)
