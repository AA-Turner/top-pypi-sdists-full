from __future__ import annotations

from typing import Mapping

from typing_extensions import final

from chalk.operators import StaticOperator


@final
class RenameOperator(StaticOperator):
    _chalk__operator_name = StaticOperator._chalk__operator_prefix + "rename_columns"

    def __init__(
        self,
        parent: StaticOperator,
        column_names: tuple[str, ...],
        old_name_to_new_name_map: Mapping[str, str],
    ):
        super().__init__(
            parent=parent,
            column_names=column_names,
            old_name_to_new_name_map=old_name_to_new_name_map,
        )
        self.column_names = column_names
        self.parent = parent
        self.old_name_to_new_name_map = old_name_to_new_name_map
