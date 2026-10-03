"""raindrop-evals: JSON output and the same exit semantics as the JS CLI."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import sys
import json
import os
from pathlib import Path

from .client import EvalClient
from .datasets import publish_eval_suite, read_evaluator
from .models import Destination, EvalSuite
from .runner import compare_eval_runs, run_eval_suite


async def _main(args: argparse.Namespace) -> int:
    client = EvalClient(
        project_id=args.project,
        query_url=args.query_url
        or os.getenv("RAINDROP_QUERY_URL", "https://query.raindrop.ai"),
    )
    if args.command == "read":
        result = (await read_evaluator(client, args.file)).wire()
    elif args.command == "compare":
        if not args.after:
            raise ValueError("Compare requires before and after run ids")
        result = await compare_eval_runs(
            client,
            before_run_id=args.file,
            after_run_id=args.after,
            evaluator=args.evaluator,
        )
    else:
        path = Path(args.file).resolve()
        spec = importlib.util.spec_from_file_location("raindrop_eval_suite", path)
        if spec is None or spec.loader is None:
            raise ValueError("Expected a Python suite module")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        # Match Python script imports, including imports made later by run callbacks.
        if str(path.parent) not in sys.path:
            sys.path.insert(0, str(path.parent))
        spec.loader.exec_module(module)
        suite = module.suite
        if not isinstance(suite, EvalSuite):
            raise ValueError("Module must export suite = define_eval_suite(...)")
        if args.command == "publish":
            published = await publish_eval_suite(
                client,
                suite,
                expected_current_dataset_version_id=args.expected_dataset_version,
            )
            result = {
                "name": published.name,
                "dataset": published.dataset,
                "datasetVersionId": str(published.dataset_version_id),
                "evaluators": [
                    {"slug": entry.evaluator.slug, "output": entry.evaluator.output}
                    for entry in published.evaluators
                ],
            }
        else:
            run = await run_eval_suite(
                client,
                suite,
                run_id=args.run_id,
                destination=Destination(replay_ingest_url=args.replay_ingest_url),
                expected_current_dataset_version_id=args.expected_dataset_version,
            )
            print(json.dumps(run.wire(), ensure_ascii=False))
            return 0 if run.passed else 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run local agents and evaluators; save results in Raindrop."
    )
    parser.add_argument("command", choices=("publish", "run", "read", "compare"))
    parser.add_argument(
        "file", help="Suite Python file, evaluator slug, or before run id"
    )
    parser.add_argument("after", nargs="?")
    parser.add_argument(
        "--project", default=os.getenv("RAINDROP_PROJECT_ID", "default")
    )
    parser.add_argument("--query-url")
    parser.add_argument("--replay-ingest-url")
    parser.add_argument("--expected-dataset-version")
    parser.add_argument("--run-id")
    parser.add_argument("--evaluator")
    parser.add_argument("--json", action="store_true", help="Output is always JSON")
    try:
        code = asyncio.run(_main(parser.parse_args()))
    except Exception as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        code = 2
    raise SystemExit(code)
