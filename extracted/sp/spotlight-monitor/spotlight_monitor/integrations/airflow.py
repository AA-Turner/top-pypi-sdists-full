"""
Spotlight Airflow Integration

Monitor Apache Airflow DAGs and tasks with Spotlight.

Usage:
    from spotlight_monitor import Spotlight
    from spotlight_monitor.integrations.airflow import AirflowIntegration

    spotlight = Spotlight(api_key="sp_xxx", service_slug="daily-etl")
    airflow = AirflowIntegration(spotlight)

    @dag(on_failure_callback=airflow.on_failure)
    def my_dag():
        ...

    # Or validate task outputs
    @task
    def extract():
        data = fetch_data()
        airflow.capture_output("extract", {"row_count": len(data)})
        return data
"""

import os
import traceback
import hashlib
from datetime import datetime
from typing import Any, Dict, Optional, Callable, TYPE_CHECKING
from functools import wraps

if TYPE_CHECKING:
    from ..client import Spotlight


class AirflowIntegration:
    """Spotlight integration for Apache Airflow."""

    def __init__(self, spotlight: "Spotlight"):
        """
        Initialize Airflow integration.

        Args:
            spotlight: Spotlight client instance
        """
        self.spotlight = spotlight

    # =========================================
    # FAILURE CALLBACKS
    # =========================================

    def on_failure(self, context: Dict[str, Any]) -> None:
        """
        Use as on_failure_callback for DAGs or tasks.

        Example:
            @dag(on_failure_callback=airflow_integration.on_failure)
            def my_dag():
                ...

            @task(on_failure_callback=airflow_integration.on_failure)
            def my_task():
                ...
        """
        exception = context.get("exception")
        if not exception:
            return

        ti = context.get("task_instance")
        dag_id = context.get("dag").dag_id if context.get("dag") else "unknown"
        task_id = ti.task_id if ti else "unknown"
        run_id = context.get("run_id")
        execution_date = context.get("execution_date")

        # Build extra context
        extra = {
            "dag_id": dag_id,
            "task_id": task_id,
            "run_id": run_id,
            "execution_date": execution_date.isoformat() if execution_date else None,
            "try_number": ti.try_number if ti else None,
            "max_tries": ti.max_tries if ti else None,
            "operator": ti.operator if ti else None,
            "state": str(ti.state) if ti else None,
        }

        self.spotlight.capture_exception(
            exception,
            tags={"dag_id": dag_id, "task_id": task_id},
            extra=extra
        )

    def on_success(self, context: Dict[str, Any]) -> None:
        """
        Use as on_success_callback to track successful runs.

        Example:
            @dag(on_success_callback=airflow_integration.on_success)
            def my_dag():
                ...
        """
        ti = context.get("task_instance")
        dag_id = context.get("dag").dag_id if context.get("dag") else "unknown"
        task_id = ti.task_id if ti else "unknown"
        run_id = context.get("run_id")
        execution_date = context.get("execution_date")

        self.spotlight.track_request(
            endpoint=f"/{dag_id}/{task_id}",
            method="RUN",
            status_code=200,
            latency_ms=int((ti.duration or 0) * 1000) if ti else 0,
            metadata={
                "dag_id": dag_id,
                "task_id": task_id,
                "run_id": run_id,
                "execution_date": execution_date.isoformat() if execution_date else None,
                "operator": ti.operator if ti else None,
                "try_number": ti.try_number if ti else None,
            }
        )

    # =========================================
    # OUTPUT VALIDATION
    # =========================================

    def capture_output(
            self,
            task_id: str,
            data: Dict[str, Any],
            dag_id: Optional[str] = None,
            run_id: Optional[str] = None
    ) -> None:
        """
        Capture task output for validation.

        Example:
            @task
            def extract():
                df = pd.read_sql("SELECT * FROM users", conn)

                airflow.capture_output("extract", {
                    "row_count": len(df),
                    "columns": list(df.columns),
                    "null_counts": df.isnull().sum().to_dict()
                })

                return df

        Then create validators in Spotlight UI:
            - JSON Schema: row_count must be integer
            - Range: row_count > 0
            - Keyword: columns must contain "user_id"
        """
        # Try to get dag_id from Airflow context
        if not dag_id:
            try:
                from airflow.operators.python import get_current_context
                context = get_current_context()
                dag_id = context["dag"].dag_id
                run_id = run_id or context.get("run_id")
            except:
                dag_id = "unknown"

        # Send as a tracked request with response data for validation
        self.spotlight.track_request(
            endpoint=f"/{dag_id}/{task_id}/output",
            method="OUTPUT",
            status_code=200,
            latency_ms=0,
            response_data=data,
            metadata={
                "dag_id": dag_id,
                "task_id": task_id,
                "run_id": run_id,
                "captured_at": datetime.utcnow().isoformat()
            }
        )

    def validate(
            self,
            task_id: str,
            data: Dict[str, Any],
            dag_id: Optional[str] = None
    ) -> None:
        """Alias for capture_output."""
        self.capture_output(task_id=task_id, data=data, dag_id=dag_id)

    # =========================================
    # TASK DECORATOR
    # =========================================

    def monitor(
            self,
            capture_output: bool = False,
            output_extractor: Optional[Callable] = None
    ):
        """
        Decorator to monitor a task function.

        Example:
            @task
            @airflow.monitor(capture_output=True)
            def extract():
                return {"users": [...], "count": 100}

            # With custom output extractor
            @task
            @airflow.monitor(
                capture_output=True,
                output_extractor=lambda result: {"row_count": len(result)}
            )
            def extract():
                return pd.DataFrame(...)
        """

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                task_id = func.__name__
                dag_id = None
                start_time = datetime.utcnow()

                # Try to get context
                try:
                    from airflow.operators.python import get_current_context
                    context = get_current_context()
                    dag_id = context["dag"].dag_id
                except:
                    pass

                try:
                    result = func(*args, **kwargs)

                    # Calculate duration
                    duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

                    # Track success
                    self.spotlight.track_request(
                        endpoint=f"/{dag_id or 'unknown'}/{task_id}",
                        method="RUN",
                        status_code=200,
                        latency_ms=duration_ms,
                    )

                    # Capture output if enabled
                    if capture_output and result is not None:
                        if output_extractor:
                            output_data = output_extractor(result)
                        elif isinstance(result, dict):
                            output_data = result
                        else:
                            output_data = {"result": str(result)[:1000]}

                        self.capture_output(
                            task_id=task_id,
                            data=output_data,
                            dag_id=dag_id
                        )

                    return result

                except Exception as e:
                    # Calculate duration
                    duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

                    # Track failure
                    self.spotlight.track_request(
                        endpoint=f"/{dag_id or 'unknown'}/{task_id}",
                        method="RUN",
                        status_code=500,
                        latency_ms=duration_ms,
                        error_type=type(e).__name__,
                        error_message=str(e),
                    )

                    self.spotlight.capture_exception(
                        e,
                        tags={"dag_id": dag_id or "unknown", "task_id": task_id},
                    )
                    raise

            return wrapper

        return decorator

    # =========================================
    # DATA QUALITY CHECKS
    # =========================================

    def check_row_count(
            self,
            task_id: str,
            actual: int,
            min_rows: Optional[int] = None,
            max_rows: Optional[int] = None,
            dag_id: Optional[str] = None
    ) -> bool:
        """
        Quick data quality check for row counts.

        Example:
            df = pd.read_sql(query, conn)
            airflow.check_row_count("extract", actual=len(df), min_rows=100)
        """
        passed = True
        message = None

        if min_rows is not None and actual < min_rows:
            passed = False
            message = f"Row count {actual} below minimum {min_rows}"

        if max_rows is not None and actual > max_rows:
            passed = False
            message = f"Row count {actual} exceeds maximum {max_rows}"

        self.capture_output(
            task_id=task_id,
            data={
                "check_type": "row_count",
                "actual": actual,
                "min_rows": min_rows,
                "max_rows": max_rows,
                "passed": passed,
                "message": message
            },
            dag_id=dag_id
        )

        return passed

    def check_not_null(
            self,
            task_id: str,
            column: str,
            null_count: int,
            total_rows: int,
            max_null_pct: float = 0.0,
            dag_id: Optional[str] = None
    ) -> bool:
        """
        Check for null values in a column.

        Example:
            null_count = df["email"].isnull().sum()
            airflow.check_not_null("extract", "email", null_count, len(df), max_null_pct=0.01)
        """
        null_pct = null_count / total_rows if total_rows > 0 else 0
        passed = null_pct <= max_null_pct

        self.capture_output(
            task_id=task_id,
            data={
                "check_type": "not_null",
                "column": column,
                "null_count": null_count,
                "null_pct": null_pct,
                "max_null_pct": max_null_pct,
                "passed": passed,
                "message": f"Column '{column}' has {null_pct:.2%} nulls" if not passed else None
            },
            dag_id=dag_id
        )

        return passed

    def check_unique(
            self,
            task_id: str,
            column: str,
            total_rows: int,
            unique_count: int,
            dag_id: Optional[str] = None
    ) -> bool:
        """
        Check if a column has all unique values.

        Example:
            airflow.check_unique("extract", "user_id", len(df), df["user_id"].nunique())
        """
        passed = unique_count == total_rows
        duplicate_count = total_rows - unique_count

        self.capture_output(
            task_id=task_id,
            data={
                "check_type": "unique",
                "column": column,
                "total_rows": total_rows,
                "unique_count": unique_count,
                "duplicate_count": duplicate_count,
                "passed": passed,
                "message": f"Column '{column}' has {duplicate_count} duplicates" if not passed else None
            },
            dag_id=dag_id
        )

        return passed

    def metric(
            self,
            name: str,
            value: float,
            dag_id: Optional[str] = None,
            task_id: Optional[str] = None,
            tags: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Send a custom metric.

        Example:
            airflow.metric("rows_processed", 5000, dag_id="daily_etl")
        """
        self.capture_output(
            task_id=task_id or "metric",
            data={
                "metric_name": name,
                "metric_value": value,
                "tags": tags or {}
            },
            dag_id=dag_id
        )