from typing import Any, Dict, Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.molecules import (
    archive_molecules,
    bulk_create_molecules,
    bulk_update_molecules,
    bulk_upsert_molecules,
    create_molecule,
    get_molecule,
    list_molecules,
    unarchive_molecules,
    update_molecule,
    upsert_molecule,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.logging_helpers import check_for_csv_bug_fix
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import (
    none_as_unset,
    optional_array_query_param,
    schema_fields_query_param,
)
from benchling_sdk.models import (
    AsyncTaskLink,
    ListMoleculesSort,
    Molecule,
    MoleculeBulkUpdate,
    MoleculeCreate,
    MoleculesArchivalChange,
    MoleculesArchive,
    MoleculesArchiveReason,
    MoleculesBulkCreateRequest,
    MoleculesBulkUpdateRequest,
    MoleculesBulkUpsertRequest,
    MoleculesPaginatedList,
    MoleculesUnarchive,
    MoleculeUpdate,
    MoleculeUpsertRequest,
)
from benchling_sdk.services.v2.base_service import BaseService


class MoleculeService(BaseService):
    """
    Molecules.

    Molecules are groups of atoms held together by bonds, representing entities smaller than DNA
    Sequences and AA Sequences. Just like other entities, they support schemas, tags, and aliases.

    See https://benchling.com/api/reference#/Molecules
    """

    @api_method
    def get_by_id(self, molecule_id: str) -> Molecule:
        """
        Get a molecule.

        See https://benchling.com/api/reference#/Molecules/getMolecule
        """
        response = get_molecule.sync_detailed(client=self.client, molecule_id=molecule_id)
        return model_from_detailed(response)

    @api_method
    def _molecules_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[ListMoleculesSort] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        names_any_of: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        chemical_substructuremol: Optional[str] = None,
        chemical_substructuresmiles: Optional[str] = None,
    ) -> Response[MoleculesPaginatedList]:
        response = list_molecules.sync_detailed(
            client=self.client,
            modified_at=none_as_unset(modified_at),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            folder_id=none_as_unset(folder_id),
            mentioned_in=none_as_unset(mentioned_in),
            project_id=none_as_unset(project_id),
            registry_id=none_as_unset(registry_id),
            schema_id=none_as_unset(schema_id),
            archive_reason=none_as_unset(archive_reason),
            sort=none_as_unset(sort),
            ids=none_as_unset(optional_array_query_param(ids)),
            mentions=none_as_unset(mentions),
            schema_fields=none_as_unset(schema_fields_query_param(schema_fields)),
            entity_registry_idsany_of=none_as_unset(optional_array_query_param(entity_registry_ids_any_of)),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            author_idsany_of=none_as_unset(optional_array_query_param(author_idsany_of)),
            chemical_substructuremol=none_as_unset(chemical_substructuremol),
            chemical_substructuresmiles=none_as_unset(chemical_substructuresmiles),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[Union[str, ListMoleculesSort]] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        names_any_of: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        chemical_substructuremol: Optional[str] = None,
        chemical_substructuresmiles: Optional[str] = None,
    ) -> PageIterator[Molecule]:
        """
        List molecules.

        See https://benchling.com/api/reference#/Molecules/listMolecules
        """
        check_for_csv_bug_fix("mentioned_in", mentioned_in)
        check_for_csv_bug_fix("mentions", mentions)

        def api_call(next_token: NextToken) -> Response[MoleculesPaginatedList]:
            return self._molecules_page(
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                project_id=project_id,
                registry_id=registry_id,
                schema_id=schema_id,
                archive_reason=archive_reason,
                mentions=mentions,
                ids=ids,
                entity_registry_ids_any_of=entity_registry_ids_any_of,
                names_any_of=names_any_of,
                schema_fields=schema_fields,
                sort=_translate_to_string_enum(ListMoleculesSort, sort),
                page_size=page_size,
                next_token=next_token,
                author_idsany_of=author_idsany_of,
                chemical_substructuremol=chemical_substructuremol,
                chemical_substructuresmiles=chemical_substructuresmiles,
            )

        def results_extractor(body: MoleculesPaginatedList) -> Optional[List[Molecule]]:
            return body.molecules

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, molecule: MoleculeCreate) -> Molecule:
        """
        Create a molecule.

        See https://benchling.com/api/reference#/Molecules/createMolecule
        """
        response = create_molecule.sync_detailed(client=self.client, json_body=molecule)
        return model_from_detailed(response)

    @api_method
    def update(self, molecule_id: str, molecule: MoleculeUpdate) -> Molecule:
        """
        Update a molecule.

        See https://benchling.com/api/reference#/Molecules/updateMolecule
        """
        response = update_molecule.sync_detailed(
            client=self.client, molecule_id=molecule_id, json_body=molecule
        )
        return model_from_detailed(response)

    @api_method
    def archive(self, molecule_ids: Iterable[str], reason: MoleculesArchiveReason) -> MoleculesArchivalChange:
        """
        Archive molecules.

        See https://benchling.com/api/reference#/Molecules/archiveMolecules
        """
        archive_request = MoleculesArchive(reason=reason, molecule_ids=list(molecule_ids))
        response = archive_molecules.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, molecule_ids: Iterable[str]) -> MoleculesArchivalChange:
        """
        Unarchive molecules.

        See https://benchling.com/api/reference#/Molecules/unarchiveMolecules
        """
        unarchive_request = MoleculesUnarchive(molecule_ids=list(molecule_ids))
        response = unarchive_molecules.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_create(self, molecules: Iterable[MoleculeCreate]) -> AsyncTaskLink:
        """
        Bulk create molecules.

        See https://benchling.com/api/reference#/Molecules/bulkCreateMolecules
        """
        body = MoleculesBulkCreateRequest(list(molecules))
        response = bulk_create_molecules.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_update(self, molecules: Iterable[MoleculeBulkUpdate]) -> AsyncTaskLink:
        """
        Bulk update molecules.

        See https://benchling.com/api/reference#/Molecules/bulkUpdateMolecules
        """
        body = MoleculesBulkUpdateRequest(list(molecules))
        response = bulk_update_molecules.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def upsert(self, entity_registry_id: str, molecule: MoleculeUpsertRequest) -> Molecule:
        """
        Create or modify a Molecule.

        See https://benchling.com/api/reference#/Molecules/upsertMolecule
        """
        response = upsert_molecule.sync_detailed(
            client=self.client, entity_registry_id=entity_registry_id, json_body=molecule
        )
        return model_from_detailed(response)

    @api_method
    def bulk_upsert(
        self, body: MoleculesBulkUpsertRequest, returning: Optional[Iterable[str]] = None
    ) -> AsyncTaskLink:
        """
        Bulk create or update Molecules.

        See https://benchling.com/api/reference#/Molecules/bulkUpsertMolecules
        """
        returning_string = optional_array_query_param(returning)
        response = bulk_upsert_molecules.sync_detailed(
            client=self.client, json_body=body, returning=none_as_unset(returning_string)
        )
        return model_from_detailed(response)
