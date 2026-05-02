from navconfig.logging import logging
from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase


class ICIMS(QSBase):
    """
    ICIMS

    Overview

        The ICIMS class is a specialized component for handling form data interactions within the ICIMS system.
        It extends the QSBase class and provides methods for retrieving people data, individual person data,
        lists of forms, and form data with specific metrics mappings.

    :widths: auto

        | type             |   Yes    | Defines the type of data handled by the component.                                   |
        | conditions       |    No    | If any condition is required to do the work.                                         |

    Methods

    people

        Retrieves a list of people data from the ICIMS system.

        Raises:
            DataNotFound: If no data is found.
            ComponentError: If any other error occurs during execution.

    person

        Retrieves individual person data from the ICIMS system and adds a person_id to the data.

        Raises:
            DataNotFound: If no data is found.
            ComponentError: If any other error occurs during execution.

    forms_list

        Retrieves a list of forms from the ICIMS system.

        Raises:
            DataNotFound: If no data is found.
            ComponentError: If any other error occurs during execution.

    form_data

        Retrieves form data from the ICIMS system and maps internal metrics to output names.

        Raises:
            DataNotFound: If no data is found.
            ComponentError: If any other error occurs during execution.

    Return

    The methods in this class return the requested data from the ICIMS system, formatted according to the
    specific requirements of each method.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ICIMS:
          type: people
        ```
    """
    _version = "1.0.0"

    type = "form_data"
    _driver = "icims"
    _metrics: dict = {
        "requestedby": "requested_by",
        "updatedby": "updated_by",
        "formname": "form_name",
        "updateddate": "updated_date",
        "completeddate": "completed_date",
        "completedby": "completed_by",
    }

    async def people(self):
        try:
            row = await self._qs.people()
            if row:
                return row
            else:
                return []
        except QSNotFound as err:
            raise DataNotFound(f"ICIMS Not Found: {err}") from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(f"ICIMS ERROR: {err!s}") from err

    async def person(self):
        try:
            row = await self._qs.person()
            if row:
                row["person_id"] = self._variables["person_id"]
                return [row]
            else:
                return []
        except QSNotFound as err:
            raise DataNotFound(f"ICIMS Not Found: {err}") from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(f"ICIMS ERROR: {err!s}") from err

    async def forms_list(self):
        try:
            row = await self._qs.forms_list()
            if row:
                return row["forms"]
            else:
                return []
        except QSNotFound as err:
            raise DataNotFound(f"ICIMS Not Found: {err}") from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(f"ICIMS ERROR: {err!s}") from err

    async def form_data(self):
        try:
            row = await self._qs.form_data()
            if row:
                for key, name in self._metrics.items():
                    try:
                        row[name] = row[key]
                        del row[key]
                    except (TypeError, KeyError):
                        pass
                return [row]
            else:
                return []
        except QSNotFound as err:
            raise DataNotFound(f"ICIMS Not Found: {err}") from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(f"ICIMS ERROR: {err!s}") from err
