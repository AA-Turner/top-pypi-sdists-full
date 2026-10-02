"""Infosec manager (IstariAdmin surface).

``Infosec`` manages infosec level configuration.
"""

from __future__ import annotations

from istari_digital_client.sdk._base import _Manager
from istari_digital_client.sdk._generated.v2.models.infosec_level import InfosecLevel
from istari_digital_client.sdk._generated.v2.models.infosec_level_object_type import InfosecLevelObjectType
from istari_digital_client.sdk._generated.v2.models.assign_infosec_level import AssignInfosecLevel


class Infosec(_Manager):
    """Manage security classification (infosec) levels.

    Aliases: security classification clearance sensitivity infosec level


    Reached via ``admin.infosec``. Infosec levels control data classification
    and access policies.

    Usage::

        # List available infosec levels
        levels = admin.infosec.list_levels()
        for level in levels:
            print(f"{level.name}: {level.description}")

        # Assign an infosec level to a resource
        admin.infosec.assign(
            subject_type=InfosecLevelObjectType.MODEL,
            subject_id="resource-uuid",
            level_id="level-uuid",
        )
    """

    def list_levels(self) -> list[InfosecLevel]:
        """List available security classification levels (infosec levels).

        Returns:
            A list of InfosecLevel objects.
        """
        return self._call(self._engine.v2_api.list_infosec_levels)

    def assign(
        self,
        *,
        subject_type: InfosecLevelObjectType,
        subject_id: str,
        level_id: str,
    ) -> None:
        """Set a security classification level on a subject (model, artifact, system, user).

        Mutates: true

        Aliases: set classify security classification clearance


        Args:
            subject_type: The subject to label -- InfosecLevelObjectType.MODEL,
                ARTIFACT, SYSTEM or USER.
            subject_id: The UUID of the resource.
            level_id: The UUID of the infosec level to assign.
        """
        self._call(
            self._engine.v2_api.assign_infosec_level,
            subject_type,
            subject_id,
            assign_infosec_level=AssignInfosecLevel(infosec_level_id=level_id),
        )
