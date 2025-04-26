import datetime as dt
from typing import Any, Dict, Optional, Sequence, Tuple

from rich import box
from rich.jupyter import JupyterMixin
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

from chalk._reporting.rich.color import CHALK_WEBSITE_GREEN
from chalk.parsed.duplicate_input_gql import UpsertFeatureGQL, UpsertFilterGQL, UpsertResolverGQL
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)


class RichDisplayMixin:
    def _to_rich_obj(self) -> JupyterMixin:
        raise NotImplementedError()

    def _repr_mimebundle_(
        self,
        include: Sequence[str],
        exclude: Sequence[str],
        **kwargs: Any,
    ) -> Dict[str, str]:
        return self._to_rich_obj()._repr_mimebundle_(include, exclude, **kwargs)  # pyright: ignore


def get_default_table_with_panel(title: str) -> Tuple[Panel, Table]:
    table = Table.grid()
    panel = Panel.fit(
        table, border_style=Style(color=CHALK_WEBSITE_GREEN), box=box.ROUNDED, padding=(1, 2), title=title
    )
    return panel, table


def _print_timedelta(delta: dt.timedelta):
    if delta.days > 1:
        original_time = dt.datetime.now() - delta
        return "on " + original_time.strftime("%Y-%m-%d %H:%M").lower()
    elif delta.seconds >= 3600:
        return f"{delta.seconds // 3600}h{(delta.seconds % 3600) // 60}m ago"
    elif delta.seconds >= 60:
        return f"{delta.seconds // 60}m{delta.seconds % 60}s ago"
    elif delta.seconds > 1:
        return f"{delta.seconds} seconds ago"
    else:
        return "just now"


def _get_last_updated_markdown(last_update: Optional[dt.datetime]):
    if last_update is None:
        msg = "(from deployment source)"
    else:
        delta_text = _print_timedelta(dt.datetime.now(tz=dt.timezone.utc) - last_update)
        msg = f"(updated from notebook {delta_text})"
    return msg


class ResolverRichSummary(RichDisplayMixin):
    def __init__(self, gql: UpsertResolverGQL, last_update: Optional[dt.datetime]):
        super().__init__()
        self.gql: UpsertResolverGQL = gql
        self.last_update = last_update

    def _to_rich_obj(self) -> JupyterMixin:
        panel, table = get_default_table_with_panel(
            title=f"Resolver: {self.gql.fqn} {_get_last_updated_markdown(last_update=self.last_update)}"
        )
        # TODO detect if we need sql highlighting
        table.add_row(Markdown(f"""```python\n{self.gql.functionDefinition}\n```"""))

        return panel


class FeatureFieldRichSummary(RichDisplayMixin):
    def __init__(self, gql: UpsertFeatureGQL, last_update: Optional[dt.datetime]):
        super().__init__()
        self.gql: UpsertFeatureGQL = gql
        self.last_update = last_update

    def _to_rich_obj(self) -> JupyterMixin:
        panel, table = get_default_table_with_panel(
            title=f"Feature: {self.gql.id.fqn} {_get_last_updated_markdown(last_update=self.last_update)}"
        )
        table.add_row(
            Markdown(
                f"""**{self.gql.id.fqn}**\n
- _type:_\t{self._print_type()}\n
- _owner:_\t{self.gql.owner}\n
- _description:_\t{self.gql.description}\n
        """
            )
        )

        return panel

    def _print_type(self):
        # type_str = f"{self.gql.scalarKind}"
        # if self.gql.id.is_primary

        if kind := self.gql.scalarKind:
            return f"{kind.scalarKind}"
        elif kind := self.gql.featureTimeKind:
            return f"FeatureTime"
        elif kind := self.gql.hasOneKind:
            filt = self._print_filter(kind.join)
            return f"has_one: {filt}"
        elif kind := self.gql.hasManyKind:
            filt = self._print_filter(kind.join)
            return f"has_many: {filt}"

    def _print_filter(self, filter: UpsertFilterGQL) -> str:
        return f"{filter.lhs.fqn} {filter.op} {filter.rhs.fqn}"
