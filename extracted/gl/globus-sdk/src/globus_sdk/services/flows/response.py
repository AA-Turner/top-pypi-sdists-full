from globus_sdk import response


class IterableFlowsResponse(response.IterableResponse):
    """
    An iterable response containing a "flows" array of flow definitions.

    This response type is returned by :meth:`FlowsClient.list_flows` and provides
    iteration over individual flow objects from a single page of results.

    When iterated over, yields individual flow dictionaries, where each flow
    typically contains:

    - ``id``: UUID of the flow
    - ``title``: Display title of the flow
    - ``definition``: The flow's JSON definition
    - ``input_schema``: JSON Schema for flow inputs
    - ``globus_auth_scope``: Auth scope string for the flow
    - ``created_at``: Timestamp of flow creation
    - ``updated_at``: Timestamp of last update
    """

    default_iter_key = "flows"


class IterableWebInputsResponse(response.IterableResponse):
    """
    An iterable response containing a "web_input_summaries" array of web input
    summaries.

    This response type is returned by :meth:`FlowsClient.list_web_inputs` and
    provides iteration over individual web input summary objects from a single page
    of results.

    When iterated over, yields individual web input summary dictionaries, where each
    summary typically contains:

    - ``id``: UUID of the web input
    - ``status``: Current status of the web input (``"open"`` or ``"closed"``)
    - ``user_roles``: The roles (``"viewer"``, ``"respondent"``) the caller has on
      the web input
    - ``input_type``: The type of the web input (e.g. ``"selection"``)
    - ``title``: Display title of the web input
    - ``flow``: The associated flow's ``id`` and ``title``
    - ``run``: The associated run's ``id`` and ``label``
    - ``created_timestamp``: Timestamp of web input creation
    - ``edited_timestamp``: Timestamp of last edit
    - ``closed_timestamp``: Timestamp the web input was closed, if applicable
    """

    default_iter_key = "web_input_summaries"


class IterableRunsResponse(response.IterableResponse):
    """
    An iterable response containing a "runs" array of flow run records.

    This response type is returned by :meth:`FlowsClient.list_runs` and provides
    iteration over individual run objects from a single page of results.

    When iterated over, yields individual run dictionaries, where each run
    typically contains:

    - ``run_id``: UUID of the run
    - ``flow_id``: UUID of the flow this run belongs to
    - ``flow_title``: Title of the flow
    - ``status``: Current status of the run (e.g., "ACTIVE", "INACTIVE",
      "SUCCEEDED", "FAILED", "ENDED")
    - ``start_time``: Timestamp when the run was started
    - ``completion_time``: Timestamp when the run completed (if applicable)
    - ``run_owner``: Identity URN of the user who started the run
    """

    default_iter_key = "runs"


class IterableRunLogsResponse(response.IterableResponse):
    """
    An iterable response containing an "entries" array of log entries.

    This response type is returned by :meth:`FlowsClient.get_run_logs` and provides
    iteration over individual log entries from a single page of results.

    When iterated over, yields individual log entry dictionaries, where each entry
    typically contains:

    - ``time``: Timestamp of the log entry
    - ``code``: Event code (e.g., "FlowStarted", "ActionStarted", "ActionCompleted")
    - ``description``: Human-readable description of the event
    - ``details``: Additional nested information about the event
    """

    default_iter_key = "entries"


class IterableRegisteredAPIsResponse(response.IterableResponse):
    """
    An iterable response containing a "registered_apis" array of registered API records.

    This response type is returned by :meth:`FlowsClient.list_registered_apis` and
    provides iteration over individual registered API objects from a single page of
    results.

    When iterated over, yields individual registered API dictionaries, where each
    registered API typically contains:

    - ``id``: UUID of the registered API
    - ``name``: Display name of the registered API
    - ``description``: Description of the registered API
    - ``created_timestamp``: Timestamp of registered API creation
    - ``updated_timestamp``: Timestamp of last update
    """

    default_iter_key = "registered_apis"
