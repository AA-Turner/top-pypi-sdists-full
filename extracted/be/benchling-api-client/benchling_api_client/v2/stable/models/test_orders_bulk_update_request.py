from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.test_order_bulk_update import TestOrderBulkUpdate
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestOrdersBulkUpdateRequest")


@attr.s(auto_attribs=True, repr=False)
class TestOrdersBulkUpdateRequest:
    """  """

    _test_orders: Union[Unset, List[TestOrderBulkUpdate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("test_orders={}".format(repr(self._test_orders)))
        return "TestOrdersBulkUpdateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        test_orders: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._test_orders, Unset):
            test_orders = []
            for test_orders_item_data in self._test_orders:
                test_orders_item = test_orders_item_data.to_dict()

                test_orders.append(test_orders_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if test_orders is not UNSET:
            field_dict["testOrders"] = test_orders

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_test_orders() -> Union[Unset, List[TestOrderBulkUpdate]]:
            test_orders = []
            _test_orders = d.pop("testOrders")
            for test_orders_item_data in _test_orders or []:
                test_orders_item = TestOrderBulkUpdate.from_dict(test_orders_item_data, strict=False)

                test_orders.append(test_orders_item)

            return test_orders

        try:
            test_orders = get_test_orders()
        except KeyError:
            if strict:
                raise
            test_orders = cast(Union[Unset, List[TestOrderBulkUpdate]], UNSET)

        test_orders_bulk_update_request = cls(
            test_orders=test_orders,
        )

        return test_orders_bulk_update_request

    @property
    def test_orders(self) -> List[TestOrderBulkUpdate]:
        if isinstance(self._test_orders, Unset):
            raise NotPresentError(self, "test_orders")
        return self._test_orders

    @test_orders.setter
    def test_orders(self, value: List[TestOrderBulkUpdate]) -> None:
        self._test_orders = value

    @test_orders.deleter
    def test_orders(self) -> None:
        self._test_orders = UNSET
