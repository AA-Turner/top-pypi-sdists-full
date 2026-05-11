"""Run evaluator on a single benchmark with full debug."""
import json
import os
import subprocess
import sys
import tempfile

task = sys.argv[1] if len(sys.argv) > 1 else "factsgrounding"

# 1. Generate pairs
with tempfile.TemporaryDirectory() as tmpdir:
    pairs_file = os.path.join(tmpdir, "pairs.json")
    print(f"=== Extracting {task} ===", flush=True)
    subprocess.run([
        sys.executable, "-m", "wisent.core.primitives.model_interface.core.main",
        "generate-pairs-from-task", task,
        "--output", pairs_file, "--limit", "5", "--allow-subtasks",
    ], check=True, capture_output=False)

    with open(pairs_file) as f:
        data = json.load(f)
    pairs = data["pairs"] if isinstance(data, dict) else data
    print(f"Loaded {len(pairs)} pairs", flush=True)

    # 2. Build responses
    responses = []
    for pair in pairs:
        positive = pair["positive_response"]["model_response"]
        negative = pair["negative_response"]["model_response"]
        responses.append({
            "prompt": pair["prompt"],
            "generated_response": positive,
            "positive_reference": positive,
            "correct_answers": [positive],
            "incorrect_answers": [negative],
        })

    input_file = os.path.join(tmpdir, "responses.json")
    output_file = os.path.join(tmpdir, "out.json")
    with open(input_file, "w") as f:
        json.dump(responses, f)

    # 3. Run evaluator with all args
    print(f"\n=== Evaluating {task} ===", flush=True)
    proc = subprocess.run([
        sys.executable, "-m", "wisent.core.primitives.model_interface.core.main",
        "evaluate-responses",
        "--input", input_file,
        "--output", output_file,
        "--task", task,
        "--subprocess-timeout", "120",
        "--personalization-good-threshold", "50",
        "--fast-diversity-seed", "42",
        "--diversity-max-sample-size", "100",
        "--min-sentence-length", "5",
        "--nonsense-min-tokens", "3",
        "--quality-min-response-length", "10",
        "--quality-repetition-ratio-threshold", "0.5",
        "--quality-bigram-repeat-threshold", "3",
        "--quality-bigram-repeat-penalty", "0.1",
        "--quality-special-char-ratio-threshold", "0.3",
        "--quality-special-char-penalty", "0.1",
        "--quality-char-repeat-count", "4",
        "--quality-char-repeat-penalty", "0.1",
        "--f1-threshold", "0.5",
        "--generation-embedding-weight", "0.5",
        "--generation-nli-weight", "0.5",
        "--personalization-difference-weight", "0.33",
        "--personalization-quality-weight", "0.33",
        "--personalization-alignment-weight", "0.34",
        "--verbose",
    ], capture_output=True, text=True)
    print("STDOUT:")
    print(proc.stdout[-3000:])
    print("\nSTDERR:")
    print(proc.stderr[-3000:])
    print(f"\nreturncode: {proc.returncode}")

    if os.path.exists(output_file):
        with open(output_file) as f:
            out = json.load(f)
        print(f"\nOutput summary: num_evaluated={out.get('num_evaluated')} num_total={out.get('num_total')}")
        if out.get("evaluations"):
            for i, e in enumerate(out["evaluations"][:2]):
                print(f"  eval[{i}]: {json.dumps(e.get('evaluation', {}))[:300]}")
