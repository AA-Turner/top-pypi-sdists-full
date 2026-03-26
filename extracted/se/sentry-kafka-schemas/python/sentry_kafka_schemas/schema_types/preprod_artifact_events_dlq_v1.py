from typing import List, TypedDict, Required


class PreprodArtifactEvents(TypedDict, total=False):
    """
    preprod_artifact_events.

    Preprod artifact events
    """

    artifact_id: Required[str]
    """ Required property """

    project_id: Required[str]
    """ Required property """

    organization_id: Required[str]
    """ Required property """

    requested_features: List[str]
