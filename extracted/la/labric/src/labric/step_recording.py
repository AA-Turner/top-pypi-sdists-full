from __future__ import annotations

from typing import Any

from .write_wrappers import WriteWrappers


class StepRecording(WriteWrappers):
    """Recording of process and measurement steps, mixed into the exported client.

    Built on `WriteWrappers` because every step is ultimately a pair of writes: the
    procedurestep/operation that describes what happened, then the rows it produced.
    """

    def get_or_create_operation(
        self,
        step_name: str,
        step_params: dict[str, Any],
        organization_id: str,
        table_id: int,
        start_time: str,
        end_time: str | None = None,
        has_effect: bool = True,
        job_execution_id: str | None = None,
    ) -> dict[str, Any]:
        """Create (or reuse) the procedurestep + operation pair backing a process step or measurement."""
        end_time = end_time or start_time
        step = self.write_core_table(
            "procedurestep",
            data=[
                {
                    "name": step_name,
                    "parameters": step_params,
                    "organization_id": organization_id,
                    "table_id": table_id,
                    "has_effect": has_effect,
                }
            ],
            params_to_match_for_update=[
                "name",
                "parameters",
                "table_id",
                "has_effect",
            ],
            defaults={
                "id": "UUID4",
                "date_created": "DATETIME_NOW",
                "date_updated": "DATETIME_NOW",
            },
            job_execution_id=job_execution_id,
        )[0]
        return self.write_core_table(
            "operation",
            data=[
                {
                    "name": f"{step_name} {start_time}",
                    "step_id": step["id"],
                    "status": "completed",
                    "organization_id": organization_id,
                    "is_atomic": True,
                    "start_time": start_time,
                    "end_time": end_time,
                }
            ],
            params_to_match_for_update=[
                "name",
                "step_id",
                "organization_id",
                "start_time",
                "end_time",
                "is_atomic",
            ],
            defaults={
                "id": "UUID4",
                "date_created": "DATETIME_NOW",
                "date_updated": "DATETIME_NOW",
            },
            job_execution_id=job_execution_id,
        )[0]

    def record_process_step(
        self,
        table_name: str,
        step_name: str,
        step_params: dict[str, Any],
        rows: list[dict[str, Any]],
        organization_id: str,
        table_id: int,
        start_time: str,
        end_time: str | None = None,
        has_effect: bool = True,
        params_to_match_for_update: list[str] | None = None,
        job_execution_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Record a process step: create its operation, then write rows to table_name with operation_id merged in.

        Set has_effect=False (or use record_measurement_step) for characterizations that don't
        change sample state.
        """
        if not rows:
            return []
        operation = self.get_or_create_operation(
            step_name,
            step_params,
            organization_id,
            table_id,
            start_time,
            end_time,
            has_effect,
            job_execution_id,
        )
        data = [{**row, "operation_id": operation["id"]} for row in rows]
        return self.write_labric_table(
            table_name,
            data=data,
            params_to_match_for_update=params_to_match_for_update
            or list(data[0].keys()),
            defaults={"id": "UUID4"},
            job_execution_id=job_execution_id,
        )

    def record_measurement_step(
        self,
        table_name: str,
        step_name: str,
        step_params: dict[str, Any],
        rows: list[dict[str, Any]],
        organization_id: str,
        table_id: int,
        start_time: str,
        end_time: str | None = None,
        params_to_match_for_update: list[str] | None = None,
        job_execution_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Record a measurement/characterization step (has_effect=False process step)."""
        return self.record_process_step(
            table_name,
            step_name,
            step_params,
            rows,
            organization_id,
            table_id,
            start_time,
            end_time,
            has_effect=False,
            params_to_match_for_update=params_to_match_for_update,
            job_execution_id=job_execution_id,
        )
