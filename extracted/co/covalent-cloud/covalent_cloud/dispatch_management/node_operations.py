# Copyright 2023 Agnostiq Inc.

"""Node operations for Covalent Cloud dispatching."""

from typing import List, Optional, Union

from covalent_cloud.dispatch_management import results_manager as rm
from covalent_cloud.shared.classes.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    handle_error,
)
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud.shared.schemas.node import (
    NodeError,
    NodeFailure,
    NodeOutput,
    NodeResult,
    NodeStderr,
)


def get_node_results(
    dispatch_id: str,
    node: Optional[Union[int, str]] = None,
    settings: Settings = settings,
) -> List[NodeResult]:
    """
    Get results for node(s) in a dispatch.

    Args:
        dispatch_id: Dispatch identifier
        node: Node ID (int) or function name (str). If None, returns all nodes.
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        List of NodeResult objects for matching nodes

    Raises:
        ResourceNotFoundError: If dispatch or node doesn't exist
        AuthenticationError: If authentication fails
        ValidationError: If parameters are invalid
        CovalentCloudError: For other API errors

    Examples:
        Get results by function name:
        >>> results = get_node_results("dispatch-123", node="calculate_metrics")

        Get results by node ID:
        >>> results = get_node_results("dispatch-123", node=5)

        Get all node results:
        >>> all_results = get_node_results("dispatch-123")
    """
    try:
        # Get the result manager which has access to all node information
        result_manager = rm.get_result_manager(dispatch_id, None, True, settings)
        result_manager._populate_result_object()

        # Get the transport graph which contains all nodes
        tg = result_manager.result_object.lattice.transport_graph
        results = []

        # Get all node IDs from the transport graph
        all_node_ids = list(tg._graph.nodes)

        if node is None:
            # Return results for all nodes
            target_node_ids = all_node_ids
        elif isinstance(node, int):
            # Specific node ID requested
            if node not in all_node_ids:
                raise ResourceNotFoundError(f"Node {node} not found in dispatch {dispatch_id}")
            target_node_ids = [node]
        else:
            # Function name requested - find all matching nodes
            target_node_ids = []
            for node_id in all_node_ids:
                node_name = tg.get_node_value(node_id, "name")
                if node_name == node:
                    target_node_ids.append(node_id)

            if not target_node_ids:
                raise ResourceNotFoundError(
                    f"No nodes found with function name '{node}' in dispatch {dispatch_id}"
                )

        # For each target node, get its result
        for node_id in target_node_ids:
            try:
                # Get node metadata
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                # Get the result FutureVar and load it
                result_future_var = tg.get_node_value(node_id, "output")

                # Load the actual result content
                if result_future_var is not None:
                    actual_result = result_future_var.load()
                else:
                    actual_result = None

                results.append(
                    NodeResult(
                        node_id=node_id,
                        function_name=function_name,
                        result=actual_result,
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

            except Exception as e:
                # If we can't load the result for this node, include it with None result
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                results.append(
                    NodeResult(
                        node_id=node_id,
                        function_name=function_name,
                        result=None,
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

        return results

    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Dispatch {dispatch_id} not found") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e
            elif e.response.status_code == 400:
                raise ValidationError("Invalid parameters provided") from e

        # Re-raise known exceptions
        if isinstance(e, (ResourceNotFoundError, AuthenticationError, ValidationError)):
            raise e

        handle_error(e)


def get_node_errors(
    dispatch_id: str,
    node: Optional[Union[int, str]] = None,
    settings: Settings = settings,
) -> List[NodeError]:
    """
    Get error information for node(s) in a dispatch.

    Args:
        dispatch_id: Dispatch identifier
        node: Node ID (int) or function name (str). If None, returns all nodes.
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        List of NodeError objects for matching nodes

    Raises:
        ResourceNotFoundError: If dispatch or node doesn't exist
        AuthenticationError: If authentication fails
        ValidationError: If parameters are invalid
        CovalentCloudError: For other API errors

    Examples:
        Check for errors:
        >>> errors = get_node_errors("dispatch-123")
        >>> for error in errors:
        ...     if error.error:
        ...         print(f"Error in {error.function_name}: {error.error}")
    """
    try:
        # Get the result manager which has access to all node information
        result_manager = rm.get_result_manager(dispatch_id, None, True, settings)
        result_manager._populate_result_object()

        # Get the transport graph which contains all nodes
        tg = result_manager.result_object.lattice.transport_graph
        results = []

        # Get all node IDs from the transport graph
        all_node_ids = list(tg._graph.nodes)

        if node is None:
            # Return errors for all nodes
            target_node_ids = all_node_ids
        elif isinstance(node, int):
            # Specific node ID requested
            if node not in all_node_ids:
                raise ResourceNotFoundError(f"Node {node} not found in dispatch {dispatch_id}")
            target_node_ids = [node]
        else:
            # Function name requested - find all matching nodes
            target_node_ids = []
            for node_id in all_node_ids:
                node_name = tg.get_node_value(node_id, "name")
                if node_name == node:
                    target_node_ids.append(node_id)

            if not target_node_ids:
                raise ResourceNotFoundError(
                    f"No nodes found with function name '{node}' in dispatch {dispatch_id}"
                )

        # For each target node, get its error information
        for node_id in target_node_ids:
            try:
                # Get node metadata
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                # Get the error FutureVar and load it
                error_future_var = tg.get_node_value(node_id, "error")

                # Load the actual error content
                if error_future_var is not None:
                    actual_error = error_future_var.load()
                    if actual_error is not None:
                        actual_error = str(actual_error)
                    else:
                        actual_error = ""
                else:
                    actual_error = ""

                results.append(
                    NodeError(
                        node_id=node_id,
                        function_name=function_name,
                        error=actual_error,
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

            except Exception as e:
                # If we can't load the error for this node, include it with empty error
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                results.append(
                    NodeError(
                        node_id=node_id,
                        function_name=function_name,
                        error="",
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

        return results

    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Dispatch {dispatch_id} not found") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e
            elif e.response.status_code == 400:
                raise ValidationError("Invalid parameters provided") from e

        # Re-raise known exceptions
        if isinstance(e, (ResourceNotFoundError, AuthenticationError, ValidationError)):
            raise e

        handle_error(e)


def get_node_stdout(
    dispatch_id: str,
    node: Optional[Union[int, str]] = None,
    settings: Settings = settings,
) -> List[NodeOutput]:
    """
    Get stdout output for node(s) in a dispatch.

    Args:
        dispatch_id: Dispatch identifier
        node: Node ID (int) or function name (str). If None, returns all nodes.
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        List of NodeOutput objects for matching nodes

    Raises:
        ResourceNotFoundError: If dispatch or node doesn't exist
        AuthenticationError: If authentication fails
        ValidationError: If parameters are invalid
        CovalentCloudError: For other API errors

    Examples:
        Get stdout for debugging:
        >>> stdout = get_node_stdout("dispatch-123", node="train_model")
        >>> for output in stdout:
        ...     print(f"Node {output.node_id}: {output.stdout}")
    """
    try:
        # Get the result manager which has access to all node information
        result_manager = rm.get_result_manager(dispatch_id, None, True, settings)
        result_manager._populate_result_object()

        # Get the transport graph which contains all nodes
        tg = result_manager.result_object.lattice.transport_graph
        results = []

        # Get all node IDs from the transport graph
        all_node_ids = list(tg._graph.nodes)

        if node is None:
            # Return stdout for all nodes
            target_node_ids = all_node_ids
        elif isinstance(node, int):
            # Specific node ID requested
            if node not in all_node_ids:
                raise ResourceNotFoundError(f"Node {node} not found in dispatch {dispatch_id}")
            target_node_ids = [node]
        else:
            # Function name requested - find all matching nodes
            target_node_ids = []
            for node_id in all_node_ids:
                node_name = tg.get_node_value(node_id, "name")
                if node_name == node:
                    target_node_ids.append(node_id)

            if not target_node_ids:
                raise ResourceNotFoundError(
                    f"No nodes found with function name '{node}' in dispatch {dispatch_id}"
                )

        # For each target node, get its stdout
        for node_id in target_node_ids:
            try:
                # Get node metadata
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                # Get the stdout FutureVar and load it
                stdout_future_var = tg.get_node_value(node_id, "stdout")

                # Load the actual stdout content
                if stdout_future_var is not None:
                    actual_stdout = stdout_future_var.load()
                    if actual_stdout is not None:
                        actual_stdout = str(actual_stdout)
                    else:
                        actual_stdout = ""
                else:
                    actual_stdout = ""

                results.append(
                    NodeOutput(
                        node_id=node_id,
                        function_name=function_name,
                        stdout=actual_stdout,
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

            except Exception as e:
                # If we can't load the stdout for this node, include it with empty stdout
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                results.append(
                    NodeOutput(
                        node_id=node_id,
                        function_name=function_name,
                        stdout="",
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

        return results

    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Dispatch {dispatch_id} not found") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e
            elif e.response.status_code == 400:
                raise ValidationError("Invalid parameters provided") from e

        # Re-raise known exceptions
        if isinstance(e, (ResourceNotFoundError, AuthenticationError, ValidationError)):
            raise e

        handle_error(e)


def get_node_stderr(
    dispatch_id: str,
    node: Optional[Union[int, str]] = None,
    settings: Settings = settings,
) -> List[NodeStderr]:
    """
    Get stderr output for node(s) in a dispatch.

    Args:
        dispatch_id: Dispatch identifier
        node: Node ID (int) or function name (str). If None, returns all nodes.
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        List of NodeStderr objects for matching nodes

    Raises:
        ResourceNotFoundError: If dispatch or node doesn't exist
        AuthenticationError: If authentication fails
        ValidationError: If parameters are invalid
        CovalentCloudError: For other API errors

    Examples:
        Check for warnings/errors:
        >>> stderr = get_node_stderr("dispatch-123")
        >>> for output in stderr:
        ...     if output.stderr:
        ...         print(f"Warning in {output.function_name}: {output.stderr}")
    """
    try:
        # Get the result manager which has access to all node information
        result_manager = rm.get_result_manager(dispatch_id, None, True, settings)
        result_manager._populate_result_object()

        # Get the transport graph which contains all nodes
        tg = result_manager.result_object.lattice.transport_graph
        results = []

        # Get all node IDs from the transport graph
        all_node_ids = list(tg._graph.nodes)

        if node is None:
            # Return stderr for all nodes
            target_node_ids = all_node_ids
        elif isinstance(node, int):
            # Specific node ID requested
            if node not in all_node_ids:
                raise ResourceNotFoundError(f"Node {node} not found in dispatch {dispatch_id}")
            target_node_ids = [node]
        else:
            # Function name requested - find all matching nodes
            target_node_ids = []
            for node_id in all_node_ids:
                node_name = tg.get_node_value(node_id, "name")
                if node_name == node:
                    target_node_ids.append(node_id)

            if not target_node_ids:
                raise ResourceNotFoundError(
                    f"No nodes found with function name '{node}' in dispatch {dispatch_id}"
                )

        # For each target node, get its stderr
        for node_id in target_node_ids:
            try:
                # Get node metadata
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                # Get the stderr FutureVar and load it
                stderr_future_var = tg.get_node_value(node_id, "stderr")

                # Load the actual stderr content
                if stderr_future_var is not None:
                    actual_stderr = stderr_future_var.load()
                    if actual_stderr is not None:
                        actual_stderr = str(actual_stderr)
                    else:
                        actual_stderr = ""
                else:
                    actual_stderr = ""

                results.append(
                    NodeStderr(
                        node_id=node_id,
                        function_name=function_name,
                        stderr=actual_stderr,
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

            except Exception as e:
                # If we can't load the stderr for this node, include it with empty stderr
                function_name = tg.get_node_value(node_id, "name")
                status = tg.get_node_value(node_id, "status")

                results.append(
                    NodeStderr(
                        node_id=node_id,
                        function_name=function_name,
                        stderr="",
                        status=str(status) if status is not None else "UNKNOWN",
                    )
                )

        return results

    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Dispatch {dispatch_id} not found") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e
            elif e.response.status_code == 400:
                raise ValidationError("Invalid parameters provided") from e

        # Re-raise known exceptions
        if isinstance(e, (ResourceNotFoundError, AuthenticationError, ValidationError)):
            raise e

        handle_error(e)


def get_first_failure(
    dispatch_id: str,
    settings: Settings = settings,
) -> Optional[NodeFailure]:
    """
    Get the first node failure in a dispatch (chronologically by start time).

    Args:
        dispatch_id: Dispatch identifier
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        NodeFailure object for the first failed node, or None if no failures

    Raises:
        ResourceNotFoundError: If dispatch doesn't exist
        AuthenticationError: If authentication fails
        CovalentCloudError: For other API errors

    Examples:
        Get first failure to understand root cause:
        >>> failure = get_first_failure("dispatch-123")
        >>> if failure:
        ...     print(f"First failure: {failure.function_name} at {failure.started_at}")
        ...     print(f"Error: {failure.error_detail}")
    """
    try:
        # Get the result manager which has access to all node information
        result_manager = rm.get_result_manager(dispatch_id, None, True, settings)
        result_manager._populate_result_object()

        # Get the transport graph which contains all nodes
        tg = result_manager.result_object.lattice.transport_graph

        # Get all node IDs from the transport graph
        all_node_ids = list(tg._graph.nodes)

        failed_nodes = []

        # Find all failed nodes and their start times
        for node_id in all_node_ids:
            try:
                status = tg.get_node_value(node_id, "status")

                # Check if node has failed
                if status and str(status).upper() in ["FAILED", "CANCELLED"]:
                    function_name = tg.get_node_value(node_id, "name")

                    # Get timing information
                    start_time = tg.get_node_value(node_id, "start_time")
                    end_time = tg.get_node_value(node_id, "end_time")

                    # Get error information
                    error_future_var = tg.get_node_value(node_id, "error")
                    error_detail = ""

                    if error_future_var is not None:
                        try:
                            error_obj = error_future_var.load()
                            if error_obj is not None:
                                error_detail = str(error_obj)
                        except Exception:
                            error_detail = "Error details unavailable"

                    failed_nodes.append(
                        {
                            "node_id": node_id,
                            "function_name": function_name,
                            "status": str(status),
                            "started_at": start_time,
                            "ended_at": end_time,
                            "error_detail": error_detail,
                        }
                    )

            except Exception:
                # Skip nodes we can't process
                continue

        if not failed_nodes:
            return None

        # Sort by start time to find the first failure
        # Handle cases where start_time might be None
        failed_nodes.sort(key=lambda x: x["started_at"] if x["started_at"] is not None else "")

        # Return the first failed node
        first_failure = failed_nodes[0]

        return NodeFailure(
            node_id=first_failure["node_id"],
            function_name=first_failure["function_name"],
            status=first_failure["status"],
            started_at=first_failure["started_at"],
            ended_at=first_failure["ended_at"],
            error_detail=first_failure["error_detail"],
        )

    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Dispatch {dispatch_id} not found") from e
            elif e.response.status_code == 401:
                raise AuthenticationError("Authentication failed") from e

        # Re-raise known exceptions
        if isinstance(e, (ResourceNotFoundError, AuthenticationError)):
            raise e

        handle_error(e)
