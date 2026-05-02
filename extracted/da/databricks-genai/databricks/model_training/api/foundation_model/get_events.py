"""List events for a model training run"""

from time import sleep
from typing import Union, cast

from IPython import get_ipython  # type: ignore
from IPython.core.display import HTML, clear_output, display

from databricks.model_training.api.engine import get_return_response, run_plural_mapi_request
from databricks.model_training.types import TrainingEvent, TrainingRun
from databricks.model_training.types.common import ObjectList

QUERY_FUNCTION = 'getFinetuneEvents'
VARIABLE_DATA_NAME = 'getFinetuneEventsData'
# This returns the same data that the create_run function returns
# for consistency when rendering the describe output

QUERY = f"""
query GetFinetuneEvents(${VARIABLE_DATA_NAME}: GetFinetuneEventsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    eventType
    eventTime
    eventMessage
  }}
}}"""


def is_running_in_notebook() -> bool:
    """
    Tested that this holds true for Databricks, Colab, and Jupyter notebooks
    Tested this is false when ran from python or from an ipython shell.

    Returns:
        bool: True if running in a notebook, False otherwise.
    """
    try:
        # Check if not in IPython shell
        if 'IPKernelApp' not in get_ipython().config:  # type: ignore
            return False
    except Exception:  # pylint: disable=W0718
        return False
    return True


def get_events(training_run: Union[str, TrainingRun], follow: bool = False) -> ObjectList[TrainingEvent]:
    """List model training runs

    Args:
        training_run (Union[str, TrainingRun]): The training run to get events for.
        follow (bool): Follow the events for the run while it is in-progress.

    Returns:
        List[TrainingEvent]: A list of training run events. Each event has an event
            type, time, and message.
    """
    training_run_name = training_run.name if isinstance(training_run, TrainingRun) else training_run

    variables = {
        VARIABLE_DATA_NAME: {
            'name': training_run_name,
        },
    }

    if follow:
        ft_events = cast(ObjectList[TrainingEvent], [])
        while len(ft_events) == 0 or not ft_events[-1].is_terminal_state():  # pylint: disable=unsubscriptable-object,no-member
            new_events = get_events(training_run)
            if len(new_events) > len(ft_events):
                if is_running_in_notebook():
                    clear_output()
                    display(HTML(new_events._repr_html_()))  # pylint: disable=protected-access
                else:
                    for event in new_events[len(ft_events):]:
                        print(event)

            ft_events = new_events

            # don't unnecessarily sleep if run has completed
            if not ft_events[-1].is_terminal_state():
                sleep(5)

        # final cleanup before displaying in notebook
        if is_running_in_notebook():
            clear_output()

    else:
        response = run_plural_mapi_request(
            query=QUERY,
            query_function=QUERY_FUNCTION,
            return_model_type=TrainingEvent,
            variables=variables,
        )
        ft_events = get_return_response(response)

    return ft_events
