"""Operator script: dump every engine-side signal about the worker runtime.

Run inside a DataNotebook cell against each engine you care about::

    from sagemaker_studio.utils.udf.probe_engine import report
    print(report(spark))

It prints, for one live connection:

  * ``session.version`` (the engine's Spark version, server round trip);
  * every candidate runtime-conf key that might name the worker interpreter,
    plus anything conf-like whose value looks like a versioned python path;
  * the outcome of the one-shot worker probe, including the raw error text.

Use it to confirm which conf keys a given engine actually publishes before
relying on them, and to capture the "worker X vs driver Y" numbers for bug
reports (including the separate Glue-6-then-Glue-5 session-poisoning issue).
This module is NOT imported by library code.
"""

from __future__ import annotations

from typing import Any, Dict, List

from sagemaker_studio.utils.udf import runtime as rt

# Beyond SERVER_CONF_PYTHON_KEYS, keys worth checking by hand on a new engine.
EXTRA_CONF_KEYS: List[str] = [
    # Reported but NOT part of the resolution ladder: it names the driver's
    # interpreter, not the workers' (see SERVER_CONF_PYTHON_KEYS' comment). Still
    # worth seeing when characterising a new engine.
    "spark.pyspark.driver.python",
    "spark.sql.execution.pythonUDF.arrow.enabled",
    "spark.sql.execution.arrow.pyspark.enabled",
    "spark.executorEnv.PYTHONPATH",
    "spark.pyspark.virtualenv.enabled",
    "spark.glue.pythonVersion",
    "spark.emr-serverless.pythonVersion",
]


def report(spark: Any) -> str:
    """Human-readable dump of every worker-runtime signal this engine exposes."""
    lines: List[str] = []

    lines.append("== engine ==")
    try:
        lines.append(f"session.version (server Spark) = {spark.version}")
    except Exception as e:
        lines.append(f"session.version FAILED: {type(e).__name__}: {e}")

    lines.append("")
    lines.append("== candidate runtime conf keys ==")
    conf_values: Dict[str, Any] = {}
    for key in list(rt.SERVER_CONF_PYTHON_KEYS) + EXTRA_CONF_KEYS:
        try:
            value = spark.conf.get(key, None)
        except Exception as e:
            value = f"<error: {type(e).__name__}: {e}>"
        conf_values[key] = value
        parsed = rt.python_version_from_path(str(value or ""))
        suffix = f"   -> python {parsed}" if parsed else ""
        lines.append(f"{key} = {value!r}{suffix}")

    lines.append("")
    lines.append("== worker probe ==")
    try:
        from pyspark.sql.connect.functions import udf as upstream_udf
        from pyspark.sql.types import IntegerType

        probe = upstream_udf(lambda _: 1, returnType=IntegerType())
        spark.range(1).select(probe("id")).collect()
        lines.append("probe SUCCEEDED -> the worker Python matches this client")
    except Exception as e:
        text = f"{e}"
        lines.append(f"probe RAISED {type(e).__name__}")
        lines.append(f"  worker version parsed: {rt.parse_worker_version(text)}")
        lines.append("  raw message:")
        lines.append(f"    {text}")

    lines.append("")
    lines.append("== resolver verdict ==")
    resolved = rt.resolve_for_session(spark)
    lines.append(
        f"python={resolved.python_version} spark={resolved.spark_version} "
        f"source={resolved.source} ({resolved.detail})"
    )
    return "\n".join(lines)
