"""
   UpdateOperationalVars

    Overview

        This component updates operational variables stored in the `process_variables` table within the `troc` schema.
        It supports dynamic variable replacement and mask application, making it versatile for runtime updates in task flows.

    .. table:: Properties
       :widths: auto

        +--------------+----------+-----------+---------------------------------------------------------------+
        | Name         | Required | Summary                                                                |
        +--------------+----------+-----------+---------------------------------------------------------------+
        | name         |   Yes    | The name of the variable to update.                                     |
        +--------------+----------+-----------+---------------------------------------------------------------+
        | value        |   Yes    | The new value to assign to the variable after the update.               |
        +--------------+----------+-----------+---------------------------------------------------------------+
        | masks        |   Yes    | Defines a section for dynamically setting the value of the variable.    |
        +--------------+----------+-----------+---------------------------------------------------------------+

    Returns

        This component does not return data directly. Instead, it updates specified variables in the database and
        records metrics on the update status. Additionally, logging is provided for SQL execution, and potential errors
        are managed with detailed logging and exception handling for effective debugging.


        Example:

        ```yaml
        UpdateOperationalVars:
          name: EPSON_SALES
          value: '{saturday}'
          masks:
            '{saturday}':
            - date_diff_dow
            - diff: 2
              day_of_week: monday
              mask: '%Y-%m-%d'
        ```

    """ #noqa

import asyncio
import logging
from typing import Any
from collections.abc import Callable
from ..exceptions import ComponentError
from .flow import FlowComponent
from ..interfaces import DBSupport


class UpdateOperationalVars(DBSupport, FlowComponent):
    """
    UpdateOperationalVars.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UpdateOperationalVars:
          name: EPSON_SALES
          value: '{saturday}'
          masks:
          '{saturday}':
          - date_diff_dow
          - diff: 2
          day_of_week: monday
          mask: '%Y-%m-%d'
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.value: Any = None
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        await super().start(**kwargs)
        self.processing_credentials()
        try:
            self.value = self.mask_replacement(self.value)
        except Exception as err:
            raise ComponentError(
                f"Error adding mask [{err.__class__.__name__}]: {err}"
            ) from err
        return True

    async def close(self):
        pass

    async def set_variable(self, variable, value, program: str = None):
        if not program:
            program = self._program
        sql = f"""UPDATE troc.process_variables SET raw_value = '{value}', \
        updated_at = CURRENT_DATE
        WHERE program_slug = '{program}' AND variable_name = '{variable}'"""
        logging.debug(f"VAR SQL: {sql}")
        try:
            connection = self.default_connection('pg')
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise
        async with await connection.connection() as conn:
            try:
                ok = await conn.execute(sql)
                if ok:
                    self.add_metric("SET_VARIABLE", f"{variable}={value}")
                    return True
                else:
                    return False
            except Exception as err:
                logging.exception(err)
                return False

    async def run(self):
        self._result = self.data
        try:
            # Replace variables
            for val in self._variables:
                if isinstance(self._variables[val], list):
                    if isinstance(self._variables[val], int):
                        self._variables[val] = ", ".join(self._variables[val])
                    else:
                        self._variables[val] = ", ".join(
                            "'{}'".format(v) for v in self._variables[val]
                        )
                self.value = self.value.replace(
                    "{{{}}}".format(str(val)), str(self._variables[val])
                )
            if hasattr(self, "program_slug"):
                program = self.program_slug
            else:
                program = self._program
            if hasattr(self, "name"):
                self._environment.set(self.name, self.value)
                value = self._environment.get(self.name)
                if value == self.value:
                    await self.set_variable(self.name, value, program)
            elif hasattr(self, "names"):
                value = None
                for name in self.names:
                    try:
                        self._environment.set(name, self.value)
                        value = self._environment.get(name)
                    except Exception as err:
                        print(err)
                    if value == self.value:
                        await self.set_variable(name, value, program)
            return self._result
        except Exception as err:
            print(err)
            raise ComponentError(
                f"Error setting operational variable [{err.__class__.__name__}]: {err}"
            ) from err
