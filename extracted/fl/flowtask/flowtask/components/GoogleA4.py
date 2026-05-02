from typing import Dict
from navconfig.logging import logging
from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase


class GoogleA4(QSBase):
    """
    GoogleA4

    Overview

        The GoogleA4 class is a component for interacting with Google Analytics 4 (GA4) to fetch and transform report data.
        It extends the QSBase class and provides methods for retrieving reports and transforming the data into a specified format.

       :widths: auto

    | datalist     |   Yes    |  Method for reports                                                  |
    | subtask      |   Yes    |  Identifiers of property and metrics                                 |
    | type         |   Yes    | Defines the type of data handled by the component, set to "report".  |
    | _driver      |   Yes    | Specifies the driver used by the component, set to "ga".             |
    | _metrics     |   Yes    | A dictionary mapping GA4 metrics to their corresponding output names.|
    | _qs          |   Yes    | Instance of the QSBase class used to interact with the data source.  |

        Raises:
            DataNotFound: If no data is found.
            ComponentError: If any other error occurs during execution.

    Return

    The methods in this class return the requested report data from Google Analytics 4, formatted according to the specific requirements of the component.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GoogleA4:
          type: report
          property_id: '306735132'
          pattern:
          start_date:
          - date_diff
          - value: now
          diff: 14
          mode: days
          mask: '%Y-%m-%d'
          end_date:
          - today
          - mask: '%Y-%m-%d'
          dimensions:
          - mobileDeviceBranding
          - mobileDeviceModel
          metric:
          - sessions
          - totalUsers
          - newUsers
          - engagedSessions
          - sessionsPerUser
          company_id: 52
          ga4_dimension: 10
        ```
    """
    _version = "1.0.0"
    type = "report"
    _driver = "ga"
    _metrics: Dict = {
        "sessions": "sessions",
        "totalUsers": "total_users",
        "newUsers": "new_users",
        "engagedSessions": "engaged_users",
        "sessionsPerUser": "per_user",
    }

    async def report(self):
        try:
            resultset = await self._qs.report()
            if not resultset:
                raise DataNotFound(
                    "No data found on GA4."
                )
            result = []
            # TODO: making a better data-transformation
            conditions = self._kwargs.get('conditions', {})
            start_date = conditions.get('start_date', None)
            end_date = conditions.get('end_date', None)
            dimensions = conditions.get('dimensions', [])
            if not start_date or not end_date:
                raise ComponentError(
                    "Google Analytics 4 ERROR: Start and end dates are required."
                )
            company_id = conditions.get('company_id', None)
            if not company_id:
                raise ComponentError(
                    "Google Analytics 4 ERROR: Company ID is required."
                )
            ga4_dimension = conditions.get('ga4_dimension', None)
            self.add_metric(
                "START_DATE", start_date
            )
            self.add_metric("END_DATE", end_date)
            self.add_metric("COMPANY", company_id)
            self.add_metric("DIMENSION", ga4_dimension)
            for row in resultset:
                res = {}
                res["start_date"] = start_date
                res["end_date"] = end_date
                res["company_id"] = company_id
                res["dimension"] = dimensions
                if "ga4_dimension" in self._variables:
                    res["ga4_dimension"] = self._variables["ga4_dimension"]
                elif "ga4_dimension" in conditions:
                    res["ga4_dimension"] = ga4_dimension
                d = {}
                for dimension in conditions.get('dimensions', []):
                    d[dimension] = row[dimension]
                res["dimensions"] = d
                metrics = {}
                for metric in conditions["metric"]:
                    metrics[metric] = row[metric]
                    try:
                        new_metric = self._metrics[metric]
                        res[new_metric] = row[metric]
                    except KeyError:
                        pass
                res["metric"] = metrics
                result.append(res)
            return result
        except DataNotFound:
            raise
        except QSNotFound as err:
            raise DataNotFound(
                f"GA4 Not Found: {err}"
            ) from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(
                f"Google Analytics 4 ERROR: {err!s}"
            ) from err
