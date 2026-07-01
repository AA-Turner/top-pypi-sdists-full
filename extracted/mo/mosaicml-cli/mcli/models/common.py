""" Common models
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generic, Iterator, List, TypeVar

O = TypeVar('O', bound=type(dataclass))


def generate_html_table(data: List[O], columns: Dict[str, str]):
    res = []
    res.append("<table border=\"1\" class=\"dataframe\">")

    # header
    res.append("<thead>")
    res.append("<tr style=\"text-align: right;\">")
    for col in columns.values():
        res.append(f"<th>{col}</th>")
    res.append("</tr>")
    res.append("</thead>")

    # body
    res.append("<tbody>")
    for row in data:
        res.append("<tr>")
        for col in columns:
            value = getattr(row, col, '')
            res.append(f"<td>{value}</td>")
        res.append("</tr>")
    res.append("</tbody>")

    res.append("</table>")
    return "\n".join(res)


class ObjectType(Enum):
    """ Enum for Types of Objects Allowed """

    CLUSTER = 'cluster'
    FORMATTED_RUN_EVENT = 'formatted_run_event'
    DEPLOYMENT = 'deployment'
    RUN = 'run'
    RUN_DEBUG_INFO = 'run_debug_info'
    SECRET = 'secret'
    USER = 'user'

    UNKNOWN = 'unknown'

    def get_display_columns(self) -> Dict[str, str]:
        """
        This is currently used only for html display (inside a notebook)

        Ideally the CLI & notebook display will be unified

        Returns:
            Dict[str, str]: Mapping of class column name to display name
        """

        if self == ObjectType.CLUSTER:
            return {
                'name': 'Name',
                'provider': 'Provider',
            }

        if self == ObjectType.DEPLOYMENT:
            return {
                'name': 'Name',
                'status': 'Status',
                'created_at': 'Created At',
                'cluster': 'Cluster',
            }

        if self == ObjectType.FORMATTED_RUN_EVENT:
            return {
                'event_type': 'Type',
                'event_time': 'Time',
                'event_message': 'Message',
            }

        if self == ObjectType.RUN:
            return {
                'name': 'Name',
                'status': 'Status',
                'created_at': 'Created At',
                'cluster': 'Cluster',
            }

        if self == ObjectType.RUN_DEBUG_INFO:
            return {
                # TODO: Support nested format of CSU & PSUs
                'id': 'Run ID',
            }

        if self == ObjectType.SECRET:
            return {
                'name': 'Name',
                'secret_type': 'Type',
                'created_at': 'Created At',
            }

        if self == ObjectType.USER:
            return {
                'email': 'Email',
                'name': 'Name',
            }

        return {}

    @classmethod
    def from_model_type(cls, model) -> ObjectType:
        # pylint: disable=import-outside-toplevel
        from mcli.api.model.cluster_details import ClusterDetails
        from mcli.api.model.inference_deployment import InferenceDeployment
        from mcli.api.model.run import Run
        from mcli.api.model.run_debug_info import RunDebugInfo
        from mcli.api.model.run_event import FormattedRunEvent
        from mcli.api.model.user import User
        from mcli.models.mcli_secret import Secret

        if model == ClusterDetails:
            return ObjectType.CLUSTER
        if model == InferenceDeployment:
            return ObjectType.DEPLOYMENT
        if model == FormattedRunEvent:
            return ObjectType.FORMATTED_RUN_EVENT
        if model == Run:
            return ObjectType.RUN
        if model == RunDebugInfo:
            return ObjectType.RUN_DEBUG_INFO
        if model == Secret:
            return ObjectType.SECRET
        if model == User:
            return ObjectType.USER
        return ObjectType.UNKNOWN


class ObjectList(list, Generic[O]):
    """Common helper for list of objects
    """

    def __init__(self, data: List[O], obj_type: ObjectType):
        self.data = data
        self.type = obj_type

    def __repr__(self) -> str:
        return f"List{self.data}"

    def __iter__(self) -> Iterator[O]:
        return iter(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def insert(self, index, item):
        self.data.insert(index, item)

    def append(self, item):
        self.data.append(item)

    def extend(self, item):
        self.data.extend(item)

    def __len__(self) -> int:
        return len(self.data)

    @property
    def display_columns(self) -> Dict[str, str]:
        return self.type.get_display_columns()

    def _repr_html_(self) -> str:
        return generate_html_table(self.data, self.display_columns)

    def to_pandas(self):
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd  # type: ignore
        except ImportError as e:
            raise ImportError("Please install pandas to use this feature") from e

        cols = self.display_columns
        res = {col: [] for col in cols}
        for row in self.data:
            for col in cols:
                value = getattr(row, col)
                res[col].append(value)

        return pd.DataFrame(data=res)
