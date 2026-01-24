from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.aa_sequence_with_entity_type import AaSequenceWithEntityType
from ..models.batch import Batch
from ..models.custom_entity_with_entity_type import CustomEntityWithEntityType
from ..models.dna_oligo_with_entity_type import DnaOligoWithEntityType
from ..models.dna_sequence_with_entity_type import DnaSequenceWithEntityType
from ..models.inaccessible_resource import InaccessibleResource
from ..models.measurement import Measurement
from ..models.mixture_with_entity_type import MixtureWithEntityType
from ..models.molecule_with_entity_type import MoleculeWithEntityType
from ..models.rna_oligo_with_entity_type import RnaOligoWithEntityType
from ..models.rna_sequence_with_entity_type import RnaSequenceWithEntityType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerContent")


@attr.s(auto_attribs=True, repr=False)
class ContainerContent:
    """  """

    _batch: Union[Unset, None, Batch, InaccessibleResource, UnknownType] = UNSET
    _concentration: Union[Unset, Measurement] = UNSET
    _entity: Union[
        Unset,
        None,
        Union[
            DnaSequenceWithEntityType,
            RnaSequenceWithEntityType,
            AaSequenceWithEntityType,
            MixtureWithEntityType,
            DnaOligoWithEntityType,
            RnaOligoWithEntityType,
            MoleculeWithEntityType,
            CustomEntityWithEntityType,
            UnknownType,
        ],
        InaccessibleResource,
        UnknownType,
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("batch={}".format(repr(self._batch)))
        fields.append("concentration={}".format(repr(self._concentration)))
        fields.append("entity={}".format(repr(self._entity)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ContainerContent({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        batch: Union[Unset, None, Dict[str, Any]]
        if isinstance(self._batch, Unset):
            batch = UNSET
        elif self._batch is None:
            batch = None
        elif isinstance(self._batch, UnknownType):
            batch = self._batch.value
        elif isinstance(self._batch, Batch):
            batch = self._batch.to_dict()

        else:
            batch = self._batch.to_dict()

        concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._concentration, Unset):
            concentration = self._concentration.to_dict()

        entity: Union[Unset, None, Union[Dict[str, Any]], Dict[str, Any]]
        if isinstance(self._entity, Unset):
            entity = UNSET
        elif self._entity is None:
            entity = None
        elif isinstance(self._entity, UnknownType):
            entity = self._entity.value
        elif isinstance(self._entity, object):
            if isinstance(self._entity, UnknownType):
                entity = self._entity.value
            elif isinstance(self._entity, DnaSequenceWithEntityType):
                entity = self._entity.to_dict()

            elif isinstance(self._entity, RnaSequenceWithEntityType):
                entity = self._entity.to_dict()

            elif isinstance(self._entity, AaSequenceWithEntityType):
                entity = self._entity.to_dict()

            elif isinstance(self._entity, MixtureWithEntityType):
                entity = self._entity.to_dict()

            elif isinstance(self._entity, DnaOligoWithEntityType):
                entity = self._entity.to_dict()

            elif isinstance(self._entity, RnaOligoWithEntityType):
                entity = self._entity.to_dict()

            elif isinstance(self._entity, MoleculeWithEntityType):
                entity = self._entity.to_dict()

            else:
                entity = self._entity.to_dict()

        else:
            entity = self._entity.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if batch is not UNSET:
            field_dict["batch"] = batch
        if concentration is not UNSET:
            field_dict["concentration"] = concentration
        if entity is not UNSET:
            field_dict["entity"] = entity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_batch() -> Union[Unset, None, Batch, InaccessibleResource, UnknownType]:
            def _parse_batch(
                data: Union[Unset, None, Dict[str, Any]]
            ) -> Union[Unset, None, Batch, InaccessibleResource, UnknownType]:
                batch: Union[Unset, None, Batch, InaccessibleResource, UnknownType]
                if data is None:
                    return data
                if isinstance(data, Unset):
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    batch_or_inaccessible_resource = Batch.from_dict(data, strict=True)

                    return batch_or_inaccessible_resource
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    batch_or_inaccessible_resource = InaccessibleResource.from_dict(data, strict=True)

                    return batch_or_inaccessible_resource
                except:  # noqa: E722
                    pass
                return UnknownType(data)

            batch = _parse_batch(d.pop("batch"))

            return batch

        try:
            batch = get_batch()
        except KeyError:
            if strict:
                raise
            batch = cast(Union[Unset, None, Batch, InaccessibleResource, UnknownType], UNSET)

        def get_concentration() -> Union[Unset, Measurement]:
            concentration: Union[Unset, Union[Unset, Measurement]] = UNSET
            _concentration = d.pop("concentration")

            if not isinstance(_concentration, Unset):
                concentration = Measurement.from_dict(_concentration)

            return concentration

        try:
            concentration = get_concentration()
        except KeyError:
            if strict:
                raise
            concentration = cast(Union[Unset, Measurement], UNSET)

        def get_entity() -> Union[
            Unset,
            None,
            Union[
                DnaSequenceWithEntityType,
                RnaSequenceWithEntityType,
                AaSequenceWithEntityType,
                MixtureWithEntityType,
                DnaOligoWithEntityType,
                RnaOligoWithEntityType,
                MoleculeWithEntityType,
                CustomEntityWithEntityType,
                UnknownType,
            ],
            InaccessibleResource,
            UnknownType,
        ]:
            def _parse_entity(
                data: Union[Unset, None, Union[Dict[str, Any]], Dict[str, Any]]
            ) -> Union[
                Unset,
                None,
                Union[
                    DnaSequenceWithEntityType,
                    RnaSequenceWithEntityType,
                    AaSequenceWithEntityType,
                    MixtureWithEntityType,
                    DnaOligoWithEntityType,
                    RnaOligoWithEntityType,
                    MoleculeWithEntityType,
                    CustomEntityWithEntityType,
                    UnknownType,
                ],
                InaccessibleResource,
                UnknownType,
            ]:
                entity: Union[
                    Unset,
                    None,
                    Union[
                        DnaSequenceWithEntityType,
                        RnaSequenceWithEntityType,
                        AaSequenceWithEntityType,
                        MixtureWithEntityType,
                        DnaOligoWithEntityType,
                        RnaOligoWithEntityType,
                        MoleculeWithEntityType,
                        CustomEntityWithEntityType,
                        UnknownType,
                    ],
                    InaccessibleResource,
                    UnknownType,
                ]
                if data is None:
                    return data
                if isinstance(data, Unset):
                    return data
                try:

                    def _parse_entity_or_inaccessible_resource(
                        data: Union[Dict[str, Any]]
                    ) -> Union[
                        DnaSequenceWithEntityType,
                        RnaSequenceWithEntityType,
                        AaSequenceWithEntityType,
                        MixtureWithEntityType,
                        DnaOligoWithEntityType,
                        RnaOligoWithEntityType,
                        MoleculeWithEntityType,
                        CustomEntityWithEntityType,
                        UnknownType,
                    ]:
                        entity_or_inaccessible_resource: Union[
                            DnaSequenceWithEntityType,
                            RnaSequenceWithEntityType,
                            AaSequenceWithEntityType,
                            MixtureWithEntityType,
                            DnaOligoWithEntityType,
                            RnaOligoWithEntityType,
                            MoleculeWithEntityType,
                            CustomEntityWithEntityType,
                            UnknownType,
                        ]
                        discriminator_value: str = cast(str, data.get("entityType"))
                        if discriminator_value is not None:
                            entity: Union[
                                DnaSequenceWithEntityType,
                                RnaSequenceWithEntityType,
                                AaSequenceWithEntityType,
                                MixtureWithEntityType,
                                DnaOligoWithEntityType,
                                RnaOligoWithEntityType,
                                MoleculeWithEntityType,
                                CustomEntityWithEntityType,
                                UnknownType,
                            ]
                            if discriminator_value == "aa_sequence":
                                entity = AaSequenceWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "custom_entity":
                                entity = CustomEntityWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "dna_oligo":
                                entity = DnaOligoWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "dna_sequence":
                                entity = DnaSequenceWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "mixture":
                                entity = MixtureWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "molecule":
                                entity = MoleculeWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "rna_oligo":
                                entity = RnaOligoWithEntityType.from_dict(data, strict=False)

                                return entity
                            if discriminator_value == "rna_sequence":
                                entity = RnaSequenceWithEntityType.from_dict(data, strict=False)

                                return entity

                            return UnknownType(value=data)
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = DnaSequenceWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = RnaSequenceWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = AaSequenceWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = MixtureWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = DnaOligoWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = RnaOligoWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = MoleculeWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            entity = CustomEntityWithEntityType.from_dict(data, strict=True)

                            return entity
                        except:  # noqa: E722
                            pass
                        raise ValueError("Unrecognized data type")

                    entity_or_inaccessible_resource = _parse_entity_or_inaccessible_resource(data)

                    return entity_or_inaccessible_resource
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    entity_or_inaccessible_resource = InaccessibleResource.from_dict(data, strict=True)

                    return entity_or_inaccessible_resource
                except:  # noqa: E722
                    pass
                return UnknownType(data)

            entity = _parse_entity(d.pop("entity"))

            return entity

        try:
            entity = get_entity()
        except KeyError:
            if strict:
                raise
            entity = cast(
                Union[
                    Unset,
                    None,
                    Union[
                        DnaSequenceWithEntityType,
                        RnaSequenceWithEntityType,
                        AaSequenceWithEntityType,
                        MixtureWithEntityType,
                        DnaOligoWithEntityType,
                        RnaOligoWithEntityType,
                        MoleculeWithEntityType,
                        CustomEntityWithEntityType,
                        UnknownType,
                    ],
                    InaccessibleResource,
                    UnknownType,
                ],
                UNSET,
            )

        container_content = cls(
            batch=batch,
            concentration=concentration,
            entity=entity,
        )

        container_content.additional_properties = d
        return container_content

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def batch(self) -> Optional[Union[Batch, InaccessibleResource, UnknownType]]:
        if isinstance(self._batch, Unset):
            raise NotPresentError(self, "batch")
        return self._batch

    @batch.setter
    def batch(self, value: Optional[Union[Batch, InaccessibleResource, UnknownType]]) -> None:
        self._batch = value

    @batch.deleter
    def batch(self) -> None:
        self._batch = UNSET

    @property
    def concentration(self) -> Measurement:
        if isinstance(self._concentration, Unset):
            raise NotPresentError(self, "concentration")
        return self._concentration

    @concentration.setter
    def concentration(self, value: Measurement) -> None:
        self._concentration = value

    @concentration.deleter
    def concentration(self) -> None:
        self._concentration = UNSET

    @property
    def entity(
        self,
    ) -> Optional[
        Union[
            Union[
                DnaSequenceWithEntityType,
                RnaSequenceWithEntityType,
                AaSequenceWithEntityType,
                MixtureWithEntityType,
                DnaOligoWithEntityType,
                RnaOligoWithEntityType,
                MoleculeWithEntityType,
                CustomEntityWithEntityType,
                UnknownType,
            ],
            InaccessibleResource,
            UnknownType,
        ]
    ]:
        if isinstance(self._entity, Unset):
            raise NotPresentError(self, "entity")
        return self._entity

    @entity.setter
    def entity(
        self,
        value: Optional[
            Union[
                Union[
                    DnaSequenceWithEntityType,
                    RnaSequenceWithEntityType,
                    AaSequenceWithEntityType,
                    MixtureWithEntityType,
                    DnaOligoWithEntityType,
                    RnaOligoWithEntityType,
                    MoleculeWithEntityType,
                    CustomEntityWithEntityType,
                    UnknownType,
                ],
                InaccessibleResource,
                UnknownType,
            ]
        ],
    ) -> None:
        self._entity = value

    @entity.deleter
    def entity(self) -> None:
        self._entity = UNSET
