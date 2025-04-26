from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.test_order import TestOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestOrdersPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class TestOrdersPaginatedList:
    """  """

    _test_orders: Union[Unset, List[TestOrder]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("test_orders={}".format(repr(self._test_orders)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "TestOrdersPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        test_orders: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._test_orders, Unset):
            test_orders = []
            for test_orders_item_data in self._test_orders:
                test_orders_item = test_orders_item_data.to_dict()

                test_orders.append(test_orders_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if test_orders is not UNSET:
            field_dict["testOrders"] = test_orders
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_test_orders() -> Union[Unset, List[TestOrder]]:
            test_orders = []
            _test_orders = d.pop("testOrders")
            for test_orders_item_data in _test_orders or []:
                test_orders_item = TestOrder.from_dict(test_orders_item_data, strict=False)

                test_orders.append(test_orders_item)

            return test_orders

        try:
            test_orders = get_test_orders()
        except KeyError:
            if strict:
                raise
            test_orders = cast(Union[Unset, List[TestOrder]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        test_orders_paginated_list = cls(
            test_orders=test_orders,
            next_token=next_token,
        )

        return test_orders_paginated_list

    @property
    def test_orders(self) -> List[TestOrder]:
        if isinstance(self._test_orders, Unset):
            raise NotPresentError(self, "test_orders")
        return self._test_orders

    @test_orders.setter
    def test_orders(self, value: List[TestOrder]) -> None:
        self._test_orders = value

    @test_orders.deleter
    def test_orders(self) -> None:
        self._test_orders = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
