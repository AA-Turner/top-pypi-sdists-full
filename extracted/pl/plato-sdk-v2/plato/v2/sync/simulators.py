"""Plato SDK v2 - Sync Simulator operations."""

from __future__ import annotations

import httpx
from pydantic import BaseModel

from plato._generated.errors import raise_for_status


class SimulatorArtifact(BaseModel):
    """An artifact belonging to a simulator."""

    artifact_id: str
    simulator_name: str


class SimulatorsManager:
    """Manager for simulator operations, accessed via plato.simulators."""

    def __init__(self, http_client: httpx.Client, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def list_artifacts(
        self,
        simulator_name: str,
        *,
        testcases_only: bool = False,
    ) -> list[SimulatorArtifact]:
        """List artifacts for a simulator.

        Args:
            simulator_name: The simulator name (e.g. "espocrm", "gitea").
            testcases_only: If True, return only artifacts linked to at least one
                testcase via the test_case_artifacts table. If False (default),
                return all artifacts for the simulator.

        Returns:
            List of SimulatorArtifact objects, newest first.

        Raises:
            plato._generated.errors.NotFoundError: If simulator does not exist.
            plato._generated.errors.APIError: On other API errors.

        Examples:
            >>> from plato.v2 import Plato, Env
            >>> plato = Plato()
            >>> # All artifacts for a simulator
            >>> artifacts = plato.simulators.list_artifacts("espocrm")
            >>> # Only artifacts that have testcases linked
            >>> tc_artifacts = plato.simulators.list_artifacts("espocrm", testcases_only=True)
            >>> env = Env.artifact(tc_artifacts[0].artifact_id)
        """
        response = self._http.get(
            f"/api/v2/simulators/{simulator_name}/artifacts",
            headers={"X-API-Key": self._api_key},
            params={"testcases_only": "true" if testcases_only else "false"},
        )
        raise_for_status(response)
        data = response.json()
        return [SimulatorArtifact.model_validate(a) for a in data["artifacts"]]
