from typing import Required, Union, List, TypedDict


class IncidentOccurrence(TypedDict, total=False):
    """
    incident_occurrence.

    A message containing the intent to create an issue occurrence for a monitor incident.
    """

    clock_tick_ts: Required[Union[int, float]]
    """
    Timestamp of the clock-tick which triggered this occurrence.

    Required property
    """

    received_ts: Required[Union[int, float]]
    """
    Timestamp indicating when the offending check-in was recieved.

    Required property
    """

    failed_checkin_id: Required[Union[int, float]]
    """
    Database id of the offending check-in

    Required property
    """

    incident_id: Union[int, float]
    """ Database id of the incident assoicated to this failure. """

    previous_checkin_ids: Required[List[Union[int, float]]]
    """
    Database ids of previously failed check-ins which led to the production of this occurrence.

    Required property
    """

