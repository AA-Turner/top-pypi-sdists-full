def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """
    This method enables state specific implementation of is_pending logic,
    based on resource specific attribute(s).
    Usage 'idem state <sls-file> --reconciler=basic --pending=aws'

    :param hub: The hub
    :param ret: The returned dictionary of the last run
    :param state: The name of the state
    :param pending_kwargs: (dict, Optional) May include 'ctx' and 'reruns_wo_change_count'
    :return: True | False
    """

    # Limiting reconciliation to up to three consecutive imes w/o change
    if pending_kwargs and pending_kwargs.get("reruns_wo_change_count", 0) >= 3:
        return False

    if (
        state is not None
        and hub.states[state] is not None
        and callable(getattr(hub.states[state], "is_pending", None))
    ):
        return hub.states[state].is_pending(ret=ret)
    else:
        # Default is_pending
        return not ret["result"] is True or bool(ret["changes"])
