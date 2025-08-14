from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.clustalo_options import ClustaloOptions
from ..models.dna_alignment_base_algorithm import DnaAlignmentBaseAlgorithm
from ..models.dna_alignment_base_files_item import DnaAlignmentBaseFilesItem
from ..models.dna_template_alignment_file import DnaTemplateAlignmentFile
from ..models.mafft_options import MafftOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaTemplateAlignmentCreate")


@attr.s(auto_attribs=True, repr=False)
class DnaTemplateAlignmentCreate:
    """  """

    _template_sequence_id: str
    _algorithm: DnaAlignmentBaseAlgorithm
    _files: List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]]
    _should_disable_circular_sequence_rotation: Union[Unset, bool] = False
    _clustalo_options: Union[Unset, ClustaloOptions] = UNSET
    _mafft_options: Union[Unset, MafftOptions] = UNSET
    _name: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("template_sequence_id={}".format(repr(self._template_sequence_id)))
        fields.append("algorithm={}".format(repr(self._algorithm)))
        fields.append("files={}".format(repr(self._files)))
        fields.append(
            "should_disable_circular_sequence_rotation={}".format(
                repr(self._should_disable_circular_sequence_rotation)
            )
        )
        fields.append("clustalo_options={}".format(repr(self._clustalo_options)))
        fields.append("mafft_options={}".format(repr(self._mafft_options)))
        fields.append("name={}".format(repr(self._name)))
        return "DnaTemplateAlignmentCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        template_sequence_id = self._template_sequence_id
        algorithm = self._algorithm.value

        files = []
        for files_item_data in self._files:
            if isinstance(files_item_data, UnknownType):
                files_item = files_item_data.value
            elif isinstance(files_item_data, DnaAlignmentBaseFilesItem):
                files_item = files_item_data.to_dict()

            else:
                files_item = files_item_data.to_dict()

            files.append(files_item)

        should_disable_circular_sequence_rotation = self._should_disable_circular_sequence_rotation
        clustalo_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._clustalo_options, Unset):
            clustalo_options = self._clustalo_options.to_dict()

        mafft_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._mafft_options, Unset):
            mafft_options = self._mafft_options.to_dict()

        name = self._name

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if template_sequence_id is not UNSET:
            field_dict["templateSequenceId"] = template_sequence_id
        if algorithm is not UNSET:
            field_dict["algorithm"] = algorithm
        if files is not UNSET:
            field_dict["files"] = files
        if should_disable_circular_sequence_rotation is not UNSET:
            field_dict["shouldDisableCircularSequenceRotation"] = should_disable_circular_sequence_rotation
        if clustalo_options is not UNSET:
            field_dict["clustaloOptions"] = clustalo_options
        if mafft_options is not UNSET:
            field_dict["mafftOptions"] = mafft_options
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_template_sequence_id() -> str:
            template_sequence_id = d.pop("templateSequenceId")
            return template_sequence_id

        try:
            template_sequence_id = get_template_sequence_id()
        except KeyError:
            if strict:
                raise
            template_sequence_id = cast(str, UNSET)

        def get_algorithm() -> DnaAlignmentBaseAlgorithm:
            _algorithm = d.pop("algorithm")
            try:
                algorithm = DnaAlignmentBaseAlgorithm(_algorithm)
            except ValueError:
                algorithm = DnaAlignmentBaseAlgorithm.of_unknown(_algorithm)

            return algorithm

        try:
            algorithm = get_algorithm()
        except KeyError:
            if strict:
                raise
            algorithm = cast(DnaAlignmentBaseAlgorithm, UNSET)

        def get_files() -> List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]]:
            files = []
            _files = d.pop("files")
            for files_item_data in _files:

                def _parse_files_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]:
                    files_item: Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        files_item = DnaAlignmentBaseFilesItem.from_dict(data, strict=True)

                        return files_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        files_item = DnaTemplateAlignmentFile.from_dict(data, strict=True)

                        return files_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                files_item = _parse_files_item(files_item_data)

                files.append(files_item)

            return files

        try:
            files = get_files()
        except KeyError:
            if strict:
                raise
            files = cast(List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]], UNSET)

        def get_should_disable_circular_sequence_rotation() -> Union[Unset, bool]:
            should_disable_circular_sequence_rotation = d.pop("shouldDisableCircularSequenceRotation")
            return should_disable_circular_sequence_rotation

        try:
            should_disable_circular_sequence_rotation = get_should_disable_circular_sequence_rotation()
        except KeyError:
            if strict:
                raise
            should_disable_circular_sequence_rotation = cast(Union[Unset, bool], UNSET)

        def get_clustalo_options() -> Union[Unset, ClustaloOptions]:
            clustalo_options: Union[Unset, Union[Unset, ClustaloOptions]] = UNSET
            _clustalo_options = d.pop("clustaloOptions")

            if not isinstance(_clustalo_options, Unset):
                clustalo_options = ClustaloOptions.from_dict(_clustalo_options)

            return clustalo_options

        try:
            clustalo_options = get_clustalo_options()
        except KeyError:
            if strict:
                raise
            clustalo_options = cast(Union[Unset, ClustaloOptions], UNSET)

        def get_mafft_options() -> Union[Unset, MafftOptions]:
            mafft_options: Union[Unset, Union[Unset, MafftOptions]] = UNSET
            _mafft_options = d.pop("mafftOptions")

            if not isinstance(_mafft_options, Unset):
                mafft_options = MafftOptions.from_dict(_mafft_options)

            return mafft_options

        try:
            mafft_options = get_mafft_options()
        except KeyError:
            if strict:
                raise
            mafft_options = cast(Union[Unset, MafftOptions], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        dna_template_alignment_create = cls(
            template_sequence_id=template_sequence_id,
            algorithm=algorithm,
            files=files,
            should_disable_circular_sequence_rotation=should_disable_circular_sequence_rotation,
            clustalo_options=clustalo_options,
            mafft_options=mafft_options,
            name=name,
        )

        return dna_template_alignment_create

    @property
    def template_sequence_id(self) -> str:
        if isinstance(self._template_sequence_id, Unset):
            raise NotPresentError(self, "template_sequence_id")
        return self._template_sequence_id

    @template_sequence_id.setter
    def template_sequence_id(self, value: str) -> None:
        self._template_sequence_id = value

    @property
    def algorithm(self) -> DnaAlignmentBaseAlgorithm:
        if isinstance(self._algorithm, Unset):
            raise NotPresentError(self, "algorithm")
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: DnaAlignmentBaseAlgorithm) -> None:
        self._algorithm = value

    @property
    def files(self) -> List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]]:
        if isinstance(self._files, Unset):
            raise NotPresentError(self, "files")
        return self._files

    @files.setter
    def files(
        self, value: List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile, UnknownType]]
    ) -> None:
        self._files = value

    @property
    def should_disable_circular_sequence_rotation(self) -> bool:
        """ Whether to disable circular sequence rotation. """
        if isinstance(self._should_disable_circular_sequence_rotation, Unset):
            raise NotPresentError(self, "should_disable_circular_sequence_rotation")
        return self._should_disable_circular_sequence_rotation

    @should_disable_circular_sequence_rotation.setter
    def should_disable_circular_sequence_rotation(self, value: bool) -> None:
        self._should_disable_circular_sequence_rotation = value

    @should_disable_circular_sequence_rotation.deleter
    def should_disable_circular_sequence_rotation(self) -> None:
        self._should_disable_circular_sequence_rotation = UNSET

    @property
    def clustalo_options(self) -> ClustaloOptions:
        """ Options to pass to the ClustalO algorithm, only applicable for ClustalO. """
        if isinstance(self._clustalo_options, Unset):
            raise NotPresentError(self, "clustalo_options")
        return self._clustalo_options

    @clustalo_options.setter
    def clustalo_options(self, value: ClustaloOptions) -> None:
        self._clustalo_options = value

    @clustalo_options.deleter
    def clustalo_options(self) -> None:
        self._clustalo_options = UNSET

    @property
    def mafft_options(self) -> MafftOptions:
        """ Options to pass to the MAFFT algorithm, only applicable for MAFFT. """
        if isinstance(self._mafft_options, Unset):
            raise NotPresentError(self, "mafft_options")
        return self._mafft_options

    @mafft_options.setter
    def mafft_options(self, value: MafftOptions) -> None:
        self._mafft_options = value

    @mafft_options.deleter
    def mafft_options(self) -> None:
        self._mafft_options = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
