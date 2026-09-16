from asyncdb.exceptions import NoDataFound, ProviderError
from ..exceptions import ComponentError, NotSupported, DataNotFound, FileNotFound
from .IteratorBase import IteratorBase
from ..interfaces.skip_policy import (
    ConsecutiveFailureTracker,
    SKIPPED_ITERATION,
)


class ParamIterator(IteratorBase):
    """
    ParamIterator.

    Overview

        This component iterates over a set of parameters and executes a job for each set of parameters.


       :widths: auto


    |  _init_      |   Yes    | This attribute is to initialize the component methods             |
    |  start       |   Yes    | We start by validating if the file exists, then the function      |
    |              |          | to get the data is started                                        |
    |  close       |   Yes    | This attribute allows me to close the process                     |
    |  create_job  |   Yes    | This metod create the job component                               |
    |  run         |   Yes    | This method creates the job component by assigning parameters     |
    |              |          | to it                                                             |


    Return the list of arbitrary days


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ParamIterator:
          params:
          formid:
          - 2552
          - 2567
          - 2569
        ```
    """
    _version = "1.0.0"
    """
    ParamIterator


        Overview

            This component iterates over a set of parameters and executes a job for each set of parameters.

        .. table:: Properties
        :widths: auto


        +------------------------+----------+-----------+-------------------------------------------------------+
        | Name                   | Required | Summary                                                           |
        +------------------------+----------+-----------+-------------------------------------------------------+
        | params                 |   Yes    | Dictionary containing parameters to iterate over.                 |
        +------------------------+----------+-----------+-------------------------------------------------------+

        Returns

        This component returns a status indicating the success or failure of the iteration process.
    """
    async def start(self, **kwargs):
        """Check if exists Parameters."""
        super(ParamIterator, self).start()
        if self.previous:
            self.data = self.input
        return True

    def get_iterator(self):
        lst = []
        try:
            if self.params:
                for item, val in self.params.items():
                    for value in val:
                        a = {item: value}
                        lst.append(a)
                return lst
            else:
                raise ComponentError("Error: Doesnt exists Parameters!")
        except Exception as err:
            raise ComponentError(f"Error: Generating Iterator: {err}") from err

    async def run(self):
        iterator = self.get_iterator()
        step, target, params = self.get_step()
        step_name = step.name
        tracker = ConsecutiveFailureTracker(self.max_consecutive_failures)
        for item in iterator:
            params["parameters"] = item
            self._result = item
            job = self.get_job(target, **params)
            if job:
                try:
                    status = await self.async_job(job, step_name)
                except (NoDataFound, DataNotFound, FileNotFound) as err:
                    # D3: continue INCONDICIONAL, y NO cuenta para el umbral.
                    self._logger.debug(f"Data not Found for {step_name}, got: {err}")
                    continue
                except (ProviderError, ComponentError, NotSupported):
                    # async_job ya consulto skipError: si llega aqui era ENFORCE.
                    raise
                except Exception as err:
                    raise ComponentError(
                        f"Generic Component Error on {step_name}, error: {err}"
                    ) from err
                
                if status is SKIPPED_ITERATION:
                    should_abort = tracker.record_skip(ComponentError(f"Skipped iteration for item {item}"))
                    if should_abort:
                        tracker.publish(self)
                        raise ComponentError(
                            f"ParamIterator: Aborted due to {tracker.consecutive} consecutive failures at item {item}. Last error: {tracker.last_error}"
                        ) from tracker.last_error
                else:
                    tracker.record_success()
        tracker.publish(self)
        return tracker.successes > 0

    async def close(self):
        pass
