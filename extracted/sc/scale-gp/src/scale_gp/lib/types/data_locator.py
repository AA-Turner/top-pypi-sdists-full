from typing import List, Union
from typing_extensions import override

from pydantic import RootModel


class BaseDataLocator(RootModel[List[str]]):
    root: List[str] = []

    def __getitem__(self, key: Union[int, str]) -> List[str]:
        return self.root + [str(key)]

    @override
    def __iter__(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        return iter(self.root)

    @override
    def __repr__(self):
        return repr(self.root)

    def __len__(self):
        return len(self.root)

    def __contains__(self, item: object) -> bool:
        return item in self.root


class TestCaseDataLocator(BaseDataLocator):
    @property
    def input(self) -> BaseDataLocator:
        return BaseDataLocator(self.root + ["input"])

    @property
    def expected_output(self) -> BaseDataLocator:
        return BaseDataLocator(self.root + ["expected_output"])


class TestCaseOutputLocator(BaseDataLocator):
    @property
    def output(self) -> BaseDataLocator:
        return BaseDataLocator(self.root + ["output"])


class TraceLocator(BaseDataLocator):
    @override
    def __getitem__(self, key: Union[int, str]) -> "TraceNodeLocator":  # type: ignore
        return TraceNodeLocator(self.root + [str(key)])


class TraceNodeLocator(BaseDataLocator):
    @property
    def input(self) -> BaseDataLocator:
        return BaseDataLocator(self.root + ["input"])

    @property
    def output(self) -> BaseDataLocator:
        return BaseDataLocator(self.root + ["output"])

    @property
    def expected(self) -> BaseDataLocator:
        return BaseDataLocator(self.root + ["expected"])


class DataLocator:
    @property
    def test_case_data(self) -> TestCaseDataLocator:
        return TestCaseDataLocator(["test_case_data"])

    @property
    def test_case_output(self) -> TestCaseOutputLocator:
        return TestCaseOutputLocator(["test_case_output"])

    @property
    def trace(self) -> TraceLocator:
        return TraceLocator(["trace"])


data_locator = DataLocator()
