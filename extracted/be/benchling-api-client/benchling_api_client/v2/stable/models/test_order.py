import datetime
from typing import Any, cast, Dict, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.test_definition import TestDefinition
from ..models.test_order_status import TestOrderStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestOrder")


@attr.s(auto_attribs=True, repr=False)
class TestOrder:
    """  """

    _analysis_comment: Union[Unset, None, str] = UNSET
    _container_id: Union[Unset, None, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _dilution_factor: Union[Unset, None, int] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name: Union[Unset, str] = UNSET
    _result_id: Union[Unset, None, str] = UNSET
    _sample_id: Union[Unset, None, str] = UNSET
    _status: Union[Unset, TestOrderStatus] = UNSET
    _test_definition: Union[Unset, TestDefinition] = UNSET

    def __repr__(self):
        fields = []
        fields.append("analysis_comment={}".format(repr(self._analysis_comment)))
        fields.append("container_id={}".format(repr(self._container_id)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("dilution_factor={}".format(repr(self._dilution_factor)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("result_id={}".format(repr(self._result_id)))
        fields.append("sample_id={}".format(repr(self._sample_id)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("test_definition={}".format(repr(self._test_definition)))
        return "TestOrder({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        analysis_comment = self._analysis_comment
        container_id = self._container_id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        dilution_factor = self._dilution_factor
        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        name = self._name
        result_id = self._result_id
        sample_id = self._sample_id
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        test_definition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._test_definition, Unset):
            test_definition = self._test_definition.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if analysis_comment is not UNSET:
            field_dict["analysisComment"] = analysis_comment
        if container_id is not UNSET:
            field_dict["containerId"] = container_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if dilution_factor is not UNSET:
            field_dict["dilutionFactor"] = dilution_factor
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if result_id is not UNSET:
            field_dict["resultId"] = result_id
        if sample_id is not UNSET:
            field_dict["sampleId"] = sample_id
        if status is not UNSET:
            field_dict["status"] = status
        if test_definition is not UNSET:
            field_dict["testDefinition"] = test_definition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_analysis_comment() -> Union[Unset, None, str]:
            analysis_comment = d.pop("analysisComment")
            return analysis_comment

        try:
            analysis_comment = get_analysis_comment()
        except KeyError:
            if strict:
                raise
            analysis_comment = cast(Union[Unset, None, str], UNSET)

        def get_container_id() -> Union[Unset, None, str]:
            container_id = d.pop("containerId")
            return container_id

        try:
            container_id = get_container_id()
        except KeyError:
            if strict:
                raise
            container_id = cast(Union[Unset, None, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_dilution_factor() -> Union[Unset, None, int]:
            dilution_factor = d.pop("dilutionFactor")
            return dilution_factor

        try:
            dilution_factor = get_dilution_factor()
        except KeyError:
            if strict:
                raise
            dilution_factor = cast(Union[Unset, None, int], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_result_id() -> Union[Unset, None, str]:
            result_id = d.pop("resultId")
            return result_id

        try:
            result_id = get_result_id()
        except KeyError:
            if strict:
                raise
            result_id = cast(Union[Unset, None, str], UNSET)

        def get_sample_id() -> Union[Unset, None, str]:
            sample_id = d.pop("sampleId")
            return sample_id

        try:
            sample_id = get_sample_id()
        except KeyError:
            if strict:
                raise
            sample_id = cast(Union[Unset, None, str], UNSET)

        def get_status() -> Union[Unset, TestOrderStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = TestOrderStatus(_status)
                except ValueError:
                    status = TestOrderStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, TestOrderStatus], UNSET)

        def get_test_definition() -> Union[Unset, TestDefinition]:
            test_definition: Union[Unset, Union[Unset, TestDefinition]] = UNSET
            _test_definition = d.pop("testDefinition")

            if not isinstance(_test_definition, Unset):
                test_definition = TestDefinition.from_dict(_test_definition)

            return test_definition

        try:
            test_definition = get_test_definition()
        except KeyError:
            if strict:
                raise
            test_definition = cast(Union[Unset, TestDefinition], UNSET)

        test_order = cls(
            analysis_comment=analysis_comment,
            container_id=container_id,
            created_at=created_at,
            dilution_factor=dilution_factor,
            id=id,
            modified_at=modified_at,
            name=name,
            result_id=result_id,
            sample_id=sample_id,
            status=status,
            test_definition=test_definition,
        )

        return test_order

    @property
    def analysis_comment(self) -> Optional[str]:
        """ Additional comments provided for a test order with a status of blocked, invalid, or cancelled. """
        if isinstance(self._analysis_comment, Unset):
            raise NotPresentError(self, "analysis_comment")
        return self._analysis_comment

    @analysis_comment.setter
    def analysis_comment(self, value: Optional[str]) -> None:
        self._analysis_comment = value

    @analysis_comment.deleter
    def analysis_comment(self) -> None:
        self._analysis_comment = UNSET

    @property
    def container_id(self) -> Optional[str]:
        """ The ID of the container associated with the sample being tested. """
        if isinstance(self._container_id, Unset):
            raise NotPresentError(self, "container_id")
        return self._container_id

    @container_id.setter
    def container_id(self, value: Optional[str]) -> None:
        self._container_id = value

    @container_id.deleter
    def container_id(self) -> None:
        self._container_id = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ Datetime the test order was created. """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def dilution_factor(self) -> Optional[int]:
        """ The dilution factor of the test order. """
        if isinstance(self._dilution_factor, Unset):
            raise NotPresentError(self, "dilution_factor")
        return self._dilution_factor

    @dilution_factor.setter
    def dilution_factor(self, value: Optional[int]) -> None:
        self._dilution_factor = value

    @dilution_factor.deleter
    def dilution_factor(self) -> None:
        self._dilution_factor = UNSET

    @property
    def id(self) -> str:
        """ ID of the test order. """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        """ Datetime the test order was last modified. """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def name(self) -> str:
        """ Name of the test order. """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def result_id(self) -> Optional[str]:
        """ The ID of the result associated with this test order """
        if isinstance(self._result_id, Unset):
            raise NotPresentError(self, "result_id")
        return self._result_id

    @result_id.setter
    def result_id(self, value: Optional[str]) -> None:
        self._result_id = value

    @result_id.deleter
    def result_id(self) -> None:
        self._result_id = UNSET

    @property
    def sample_id(self) -> Optional[str]:
        """ The ID of the sample being tested. """
        if isinstance(self._sample_id, Unset):
            raise NotPresentError(self, "sample_id")
        return self._sample_id

    @sample_id.setter
    def sample_id(self, value: Optional[str]) -> None:
        self._sample_id = value

    @sample_id.deleter
    def sample_id(self) -> None:
        self._sample_id = UNSET

    @property
    def status(self) -> TestOrderStatus:
        """The status of a test order."""
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: TestOrderStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def test_definition(self) -> TestDefinition:
        """The test definition for a test order."""
        if isinstance(self._test_definition, Unset):
            raise NotPresentError(self, "test_definition")
        return self._test_definition

    @test_definition.setter
    def test_definition(self, value: TestDefinition) -> None:
        self._test_definition = value

    @test_definition.deleter
    def test_definition(self) -> None:
        self._test_definition = UNSET
