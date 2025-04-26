from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.nucleotide_alignment_base_algorithm import NucleotideAlignmentBaseAlgorithm
from ..models.nucleotide_alignment_base_clustalo_options import NucleotideAlignmentBaseClustaloOptions
from ..models.nucleotide_alignment_base_files_item import NucleotideAlignmentBaseFilesItem
from ..models.nucleotide_alignment_base_mafft_options import NucleotideAlignmentBaseMafftOptions
from ..models.nucleotide_alignment_file import NucleotideAlignmentFile
from ..models.nucleotide_consensus_alignment_create_new_sequence import (
    NucleotideConsensusAlignmentCreateNewSequence,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="NucleotideConsensusAlignmentCreate")


@attr.s(auto_attribs=True, repr=False)
class NucleotideConsensusAlignmentCreate:
    """  """

    _algorithm: NucleotideAlignmentBaseAlgorithm
    _files: List[Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]]
    _new_sequence: Union[Unset, NucleotideConsensusAlignmentCreateNewSequence] = UNSET
    _sequence_id: Union[Unset, str] = UNSET
    _clustalo_options: Union[Unset, NucleotideAlignmentBaseClustaloOptions] = UNSET
    _mafft_options: Union[Unset, NucleotideAlignmentBaseMafftOptions] = UNSET
    _name: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("algorithm={}".format(repr(self._algorithm)))
        fields.append("files={}".format(repr(self._files)))
        fields.append("new_sequence={}".format(repr(self._new_sequence)))
        fields.append("sequence_id={}".format(repr(self._sequence_id)))
        fields.append("clustalo_options={}".format(repr(self._clustalo_options)))
        fields.append("mafft_options={}".format(repr(self._mafft_options)))
        fields.append("name={}".format(repr(self._name)))
        return "NucleotideConsensusAlignmentCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        algorithm = self._algorithm.value

        files = []
        for files_item_data in self._files:
            if isinstance(files_item_data, UnknownType):
                files_item = files_item_data.value
            elif isinstance(files_item_data, NucleotideAlignmentBaseFilesItem):
                files_item = files_item_data.to_dict()

            else:
                files_item = files_item_data.to_dict()

            files.append(files_item)

        new_sequence: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._new_sequence, Unset):
            new_sequence = self._new_sequence.to_dict()

        sequence_id = self._sequence_id
        clustalo_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._clustalo_options, Unset):
            clustalo_options = self._clustalo_options.to_dict()

        mafft_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._mafft_options, Unset):
            mafft_options = self._mafft_options.to_dict()

        name = self._name

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if algorithm is not UNSET:
            field_dict["algorithm"] = algorithm
        if files is not UNSET:
            field_dict["files"] = files
        if new_sequence is not UNSET:
            field_dict["newSequence"] = new_sequence
        if sequence_id is not UNSET:
            field_dict["sequenceId"] = sequence_id
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

        def get_algorithm() -> NucleotideAlignmentBaseAlgorithm:
            _algorithm = d.pop("algorithm")
            try:
                algorithm = NucleotideAlignmentBaseAlgorithm(_algorithm)
            except ValueError:
                algorithm = NucleotideAlignmentBaseAlgorithm.of_unknown(_algorithm)

            return algorithm

        try:
            algorithm = get_algorithm()
        except KeyError:
            if strict:
                raise
            algorithm = cast(NucleotideAlignmentBaseAlgorithm, UNSET)

        def get_files() -> List[
            Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]
        ]:
            files = []
            _files = d.pop("files")
            for files_item_data in _files:

                def _parse_files_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]:
                    files_item: Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        files_item = NucleotideAlignmentBaseFilesItem.from_dict(data, strict=True)

                        return files_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        files_item = NucleotideAlignmentFile.from_dict(data, strict=True)

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
            files = cast(
                List[Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]], UNSET
            )

        def get_new_sequence() -> Union[Unset, NucleotideConsensusAlignmentCreateNewSequence]:
            new_sequence: Union[Unset, Union[Unset, NucleotideConsensusAlignmentCreateNewSequence]] = UNSET
            _new_sequence = d.pop("newSequence")

            if not isinstance(_new_sequence, Unset):
                new_sequence = NucleotideConsensusAlignmentCreateNewSequence.from_dict(_new_sequence)

            return new_sequence

        try:
            new_sequence = get_new_sequence()
        except KeyError:
            if strict:
                raise
            new_sequence = cast(Union[Unset, NucleotideConsensusAlignmentCreateNewSequence], UNSET)

        def get_sequence_id() -> Union[Unset, str]:
            sequence_id = d.pop("sequenceId")
            return sequence_id

        try:
            sequence_id = get_sequence_id()
        except KeyError:
            if strict:
                raise
            sequence_id = cast(Union[Unset, str], UNSET)

        def get_clustalo_options() -> Union[Unset, NucleotideAlignmentBaseClustaloOptions]:
            clustalo_options: Union[Unset, Union[Unset, NucleotideAlignmentBaseClustaloOptions]] = UNSET
            _clustalo_options = d.pop("clustaloOptions")

            if not isinstance(_clustalo_options, Unset):
                clustalo_options = NucleotideAlignmentBaseClustaloOptions.from_dict(_clustalo_options)

            return clustalo_options

        try:
            clustalo_options = get_clustalo_options()
        except KeyError:
            if strict:
                raise
            clustalo_options = cast(Union[Unset, NucleotideAlignmentBaseClustaloOptions], UNSET)

        def get_mafft_options() -> Union[Unset, NucleotideAlignmentBaseMafftOptions]:
            mafft_options: Union[Unset, Union[Unset, NucleotideAlignmentBaseMafftOptions]] = UNSET
            _mafft_options = d.pop("mafftOptions")

            if not isinstance(_mafft_options, Unset):
                mafft_options = NucleotideAlignmentBaseMafftOptions.from_dict(_mafft_options)

            return mafft_options

        try:
            mafft_options = get_mafft_options()
        except KeyError:
            if strict:
                raise
            mafft_options = cast(Union[Unset, NucleotideAlignmentBaseMafftOptions], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        nucleotide_consensus_alignment_create = cls(
            algorithm=algorithm,
            files=files,
            new_sequence=new_sequence,
            sequence_id=sequence_id,
            clustalo_options=clustalo_options,
            mafft_options=mafft_options,
            name=name,
        )

        return nucleotide_consensus_alignment_create

    @property
    def algorithm(self) -> NucleotideAlignmentBaseAlgorithm:
        if isinstance(self._algorithm, Unset):
            raise NotPresentError(self, "algorithm")
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value: NucleotideAlignmentBaseAlgorithm) -> None:
        self._algorithm = value

    @property
    def files(self) -> List[Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]]:
        if isinstance(self._files, Unset):
            raise NotPresentError(self, "files")
        return self._files

    @files.setter
    def files(
        self, value: List[Union[NucleotideAlignmentBaseFilesItem, NucleotideAlignmentFile, UnknownType]]
    ) -> None:
        self._files = value

    @property
    def new_sequence(self) -> NucleotideConsensusAlignmentCreateNewSequence:
        if isinstance(self._new_sequence, Unset):
            raise NotPresentError(self, "new_sequence")
        return self._new_sequence

    @new_sequence.setter
    def new_sequence(self, value: NucleotideConsensusAlignmentCreateNewSequence) -> None:
        self._new_sequence = value

    @new_sequence.deleter
    def new_sequence(self) -> None:
        self._new_sequence = UNSET

    @property
    def sequence_id(self) -> str:
        if isinstance(self._sequence_id, Unset):
            raise NotPresentError(self, "sequence_id")
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, value: str) -> None:
        self._sequence_id = value

    @sequence_id.deleter
    def sequence_id(self) -> None:
        self._sequence_id = UNSET

    @property
    def clustalo_options(self) -> NucleotideAlignmentBaseClustaloOptions:
        """ Options to pass to the ClustalO algorithm, only applicable for ClustalO. """
        if isinstance(self._clustalo_options, Unset):
            raise NotPresentError(self, "clustalo_options")
        return self._clustalo_options

    @clustalo_options.setter
    def clustalo_options(self, value: NucleotideAlignmentBaseClustaloOptions) -> None:
        self._clustalo_options = value

    @clustalo_options.deleter
    def clustalo_options(self) -> None:
        self._clustalo_options = UNSET

    @property
    def mafft_options(self) -> NucleotideAlignmentBaseMafftOptions:
        """ Options to pass to the MAFFT algorithm, only applicable for MAFFT. """
        if isinstance(self._mafft_options, Unset):
            raise NotPresentError(self, "mafft_options")
        return self._mafft_options

    @mafft_options.setter
    def mafft_options(self, value: NucleotideAlignmentBaseMafftOptions) -> None:
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
