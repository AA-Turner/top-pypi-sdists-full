from nexuscli.api.base_model import BaseModel


class CleanupPolicy(BaseModel):
    """
    Represents a Nexus Cleanup Policy.

    Example structure and attributes common to all repositories:

        >>> kwargs = {
        >>>     'name': 'my-policy',
        >>>     'format': 'bower',
        >>>     'notes': 'Some comment',
        >>>     'criteria': {
        >>>         'lastDownloaded': 172800,
        >>>         'lastBlobUpdated': 86400,
        >>>         'regex': 'matchthis'
        >>>     }
        >>> }

    Args:
        client (nexuscli.nexus_client.NexusClient): the client instance that
            will be used to perform operations against the Nexus 3 service. You
            must provide this at instantiation or set it before calling any
            methods that require connectivity to Nexus.
        name (str): name of the new policy.
        format (str): 'all' or the format of the repository this policy applies to.
        lastDownloaded (int): deletion criterion: days since artefact last downloaded
        lastBlobUpdated (int): deletion criterion: days since last update to artefact
        regex (str): deletion criterion: only delete artefacts that match this regular expression
    """
    def _validate_params(self) -> None:
        if self._raw['format'] == 'maven':
            self._raw['format'] = 'maven2'

        super()._validate_params()
