from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, Sequence, Tuple, TypeVar, Union

import click
from tabulate import tabulate

from launchable.testpath import unparse_test_path
from launchable.utils.launchable_client import LaunchableClient


@dataclass(frozen=True)
class SubsetResultBase:
    order: int
    name: str


@dataclass(frozen=True)
class SubsetResult(SubsetResultBase):
    density: float
    reason: str
    duration_sec: float

    @classmethod
    def from_inspect_api(cls, result: Dict[str, Any], order: int) -> "SubsetResult":
        test_path = result.get("testPath", []) or []
        name = unparse_test_path(test_path)
        density = float(result.get("density") or 0.0)
        reason = result.get("reason", "")
        duration_sec = float(result.get("duration") or 0.0) / 1000.0  # convert to sec from msec
        return cls(order=order, name=name, density=density, reason=reason, duration_sec=duration_sec)


TSubsetResult = TypeVar("TSubsetResult", bound="SubsetResultBase")


class SubsetResultBases(Generic[TSubsetResult]):
    def __init__(self, results: Sequence[TSubsetResult]):
        self._results: List[TSubsetResult] = list(results)
        self._index_map = {r.name: r.order for r in self._results}

    @property
    def results(self) -> List[TSubsetResult]:
        return self._results

    def get_order(self, name: str) -> Optional[int]:
        return self._index_map.get(name)

    @staticmethod
    def from_file(file_path: Path) -> "SubsetResultBases[SubsetResultBase]":
        with open(file_path, "r", encoding="utf-8") as subset_file:
            results = subset_file.read().splitlines()
        entries = [SubsetResultBase(order=order, name=result) for order, result in enumerate(results, start=1)]
        return SubsetResultBases(entries)


class SubsetResults(SubsetResultBases[SubsetResult]):
    def __init__(self, results: Sequence[SubsetResult]):
        super().__init__(results)

    @property
    def results(self) -> List[SubsetResult]:
        return super().results

    @classmethod
    def load(cls, client: LaunchableClient, subset_id: int) -> "SubsetResults":
        try:
            response = client.request("get", f"subset/{subset_id}")
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise click.ClickException(
                    f"Subset {subset_id} not found. Check subset ID and try again."
                )
            response.raise_for_status()
        except Exception as exc:
            client.print_exception_and_recover(exc, "Warning: failed to load subset results")
            raise click.ClickException("Failed to load subset results") from exc

        payload = response.json()
        order = 1
        results: List[SubsetResult] = []
        entries = (payload.get("testPaths", []) or []) + (payload.get("rest", []) or [])
        for entry in entries:
            results.append(SubsetResult.from_inspect_api(entry, order))
            order += 1
        return cls(results)


@click.command()
@click.argument('file_before', type=click.Path(exists=True), required=False)
@click.argument('file_after', type=click.Path(exists=True), required=False)
@click.option(
    '--subset-id-before',
    'subset_id_before',
    type=int,
    help='Subset ID for the first subset to compare',
    metavar="SUBSET_ID")
@click.option(
    '--subset-id-after',
    'subset_id_after',
    type=int,
    help='Subset ID for the second subset to compare',
    metavar="SUBSET_ID")
@click.pass_context
def subsets(context: click.core.Context, file_before, file_after, subset_id_before, subset_id_after):
    """Compare subsets sourced from files or remote subset IDs."""

    if (file_before is not None) ^ (file_after is not None):
        raise click.ClickException("Provide both subset files when using file arguments.")
    if (subset_id_before is not None) ^ (subset_id_after is not None):
        raise click.ClickException("Provide both subset IDs when using --subset-id options.")

    from_file = file_before is not None and file_after is not None
    from_subset_id = subset_id_before is not None and subset_id_after is not None

    if from_file and from_subset_id:
        raise click.ClickException("Specify either both subset files or both subset IDs, not both.")
    if not from_file and not from_subset_id:
        raise click.ClickException("You must specify either both subset files or both subset IDs.")

    if from_subset_id:

        client = LaunchableClient(app=context.obj)
        # for type check
        assert subset_id_before is not None and subset_id_after is not None
        _from_subset_ids(client=client, subset_id_before=subset_id_before, subset_id_after=subset_id_after)
        return

    # for type check
    assert file_before is not None and file_after is not None
    _from_files(file_before=file_before, file_after=file_after)


def _from_subset_ids(client: LaunchableClient, subset_id_before: int, subset_id_after: int):
    before_subset = SubsetResults.load(client, subset_id_before)
    after_subset = SubsetResults.load(client, subset_id_after)

    total = 0
    promoted = 0
    demoted = 0
    affected = set()
    # List of tuples representing test order changes
    # (Rank, Subset Rank, Test Path, Reason, Density)
    rows: List[Tuple[str, Union[int, str], str, str, Union[float, str]]] = []

    # Calculate order difference and add each test in file_after to changes
    for result in after_subset.results:
        total += 1
        if result.reason.startswith("Changed file: "):
            affected.add(result.reason[len("Changed file: "):])

        test_name = result.name
        after_order = result.order
        before_order = before_subset.get_order(test_name)
        if before_order is None:
            rows.append(('NEW', after_order, test_name, result.reason, result.density))
        else:
            diff = after_order - before_order
            rank = "±0"
            if diff > 0:
                rank = "↓" + str(diff)
                demoted += 1
            elif diff < 0:
                rank = "↑" + str(-diff)
                promoted += 1

            rows.append((rank, after_order, test_name, result.reason, result.density))

    # Add all deleted tests to changes
    for result in before_subset.results:
        test_name = result.name
        before_order = result.order
        if after_subset.get_order(test_name) is None:
            rows.append(("DELETED", '-', test_name, "", ""))

    summary = f"""PTS subset change summary:
────────────────────────────────
-> {total} tests analyzed | {promoted} ↑ promoted | {demoted} ↓ demoted
-> Code files affected: {', '.join(sorted(affected)) if len(affected) < 10 else str(len(affected)) + ' files'}
────────────────────────────────
"""

    # Display results in a tabular format
    headers = ["Δ Rank", "Subset Rank", "Test Name", "Reason", "Density"]
    tabular_data = [
        (rank, after, test_name, reason, density)
        for rank, after, test_name, reason, density in rows
    ]
    click.echo_via_pager(summary + "\n" + tabulate(tabular_data, headers=headers, tablefmt="simple"))


def _from_files(file_before: Path, file_after: Path):
    before_subset = SubsetResultBases.from_file(file_before)
    after_subset = SubsetResultBases.from_file(file_after)

    # List of tuples representing test order changes (before, after, diff, test)
    rows: List[Tuple[Union[int, str], Union[int, str], Union[int, str], str]] = []

    # Calculate order difference and add each test in file_after to changes
    for result in after_subset.results:
        test_name = result.name
        after_order = result.order
        before_order = before_subset.get_order(test_name)
        if before_order is not None:
            diff = after_order - before_order
            rows.append((before_order, after_order, diff, test_name))
        else:
            rows.append(('-', after_order, 'NEW', test_name))

    # Add all deleted tests to changes
    for result in before_subset.results:
        test_name = result.name
        before_order = result.order
        if after_subset.get_order(test_name) is None:
            rows.append((before_order, '-', 'DELETED', test_name))

    # Sort changes by the order diff
    rows.sort(key=lambda x: (0 if isinstance(x[2], str) else 1, x[2]))

    # Display results in a tabular format
    headers = ["Before", "After", "After - Before", "Test"]
    tabular_data = [
        (before, after, f"{diff:+}" if isinstance(diff, int) else diff, test)
        for before, after, diff, test in rows
    ]
    click.echo_via_pager(tabulate(tabular_data, headers=headers, tablefmt="github"))
