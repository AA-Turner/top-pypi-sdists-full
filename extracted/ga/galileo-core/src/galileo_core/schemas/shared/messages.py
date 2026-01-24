from typing import Generator, List

from pydantic import RootModel

from galileo_core.schemas.shared.message import Message


class Messages(RootModel[List[Message]]):
    def __len__(self) -> int:
        return len(self.root)

    def __iter__(self) -> Generator[Message, None, None]:  # type: ignore[override]
        yield from self.root

    def __getitem__(self, item: int) -> Message:
        return self.root[item]
