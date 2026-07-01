from __future__ import annotations

from typing import Iterator

from typing_extensions import Annotated

from wireup import Inject, injectable


class SearchClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def describe(self) -> str:
        return f"search:{self.base_url}"


@injectable
def make_search_client(
    search_url: Annotated[str, Inject(config="services.search.base_url")],
) -> Iterator[SearchClient]:
    yield SearchClient(search_url)
