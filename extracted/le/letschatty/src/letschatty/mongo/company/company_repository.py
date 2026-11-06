"""The company document in `empresas` (`CompanyRepository`). The one writer of the collection in the app, on the
service's own collection, so the document is the `EmpresaModel` serialized `SerializerType.DATABASE` as always.

A change is `_save` with the fields it owns. `AssetService.partial_update` is not enough here: it would only drop the
asset's key, so `company_version`, the routing keys, the settings and the betas would stay stale; that is why the
company is read back (the decorator forgets THAT copy).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence
from zoneinfo import ZoneInfo

from bson.objectid import ObjectId

from ...domain.company.company import CompanyChangedMeanwhile
from ...models.company.empresa import EmpresaModel
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types.deletion_type import DeletionType
from ...models.utils.types.serializer_type import SerializerType


def _value_at(document: Dict[str, Any], path: str) -> Any:
    node: Any = document
    for part in path.split("."):
        node = node[part]  # KeyError: the stored shape has no such field. Never silently skipped
    return node


class MongoCompanyRepository:
    def __init__(self, collection: Any):
        self.collection = collection

    async def get(self, company_id: str, *, ignore_cache: bool = False) -> EmpresaModel:
        return await self.collection.get_by_id(company_id)

    async def live(self, *, ignore_cache: bool = False) -> List[EmpresaModel]:
        return await self.collection.get_docs(company_id=None, query={"deleted_at": None})

    async def deleted(self) -> List[EmpresaModel]:
        return await self.collection.get_docs(query={"deleted_at": {"$ne": None}}, company_id=None)

    async def by_shopify_domain(self, shop_domain: str) -> Optional[EmpresaModel]:
        results = await self.collection.get_docs(query={"shopify_integration.shopify_store_url": shop_domain},
                                                 company_id=None)
        return results[0] if results else None

    async def create(self, company: EmpresaModel) -> None:
        await self.collection.insert(company)

    async def soft_delete(self, company: EmpresaModel) -> None:
        await self.collection.delete(company.id, DeletionType.LOGICAL)

    async def restore(self, company_id: str) -> EmpresaModel:
        company = await self.collection.get_by_id(company_id)
        if company is None:
            raise NotFoundError(f"Item with id {company_id} not found in collection DB")
        company.deleted_at = None
        company.update_now()
        await self.collection.update(company)
        return company

    async def _repair_null_container(self, oid: ObjectId, path: str, empty: Any) -> None:
        """`{"a": null}` makes `$set: {"a.b": ...}` / `$addToSet: {"a": ...}` fail. Turn a null or missing container into
        an empty one first. Matches nothing on a healthy document."""
        await self.collection.collection.update_one({"_id": oid, path: None}, {"$set": {path: empty}})

    async def _apply(self, company_id: str, update: Dict[str, Dict[str, Any]], *,
                     only_if: Optional[Dict[str, Any]] = None, containers: Optional[Dict[str, Any]] = None) -> EmpresaModel:
        """A Mongo update of ONE company, with `updated_at`. `only_if` adds equality conditions to the filter;
        `containers` maps a path to the empty value to create when it is null or missing, so the operators apply."""
        oid = ObjectId(company_id)
        document: Dict[str, Dict[str, Any]] = {op: dict(fields) for op, fields in update.items()}
        document.setdefault("$set", {})["updated_at"] = datetime.now(ZoneInfo("UTC"))
        for path, empty in (containers or {}).items():
            await self._repair_null_container(oid, path, empty)
        result = await self.collection.collection.update_one({"_id": oid, **(only_if or {})}, document)
        if result.matched_count == 0:
            if only_if and await self.collection.collection.count_documents({"_id": oid}, limit=1):
                raise CompanyChangedMeanwhile(f"Company {company_id} no longer matches {only_if}")
            raise NotFoundError(f"No document found with id {company_id}")
        return await self.collection.get_by_id(company_id)

    async def _save(self, company: EmpresaModel, paths: Sequence[str],
                    only_if: Optional[Dict[str, Any]] = None) -> EmpresaModel:
        """`$set` only `paths` (top-level fields or dotted paths) with the values `company` holds now, serialized exactly
        as a whole-document save would have."""
        stored = company.model_dump_json(serializer=SerializerType.DATABASE)
        fields = {path: _value_at(stored, path) for path in paths}
        parents = {path.split(".")[0]: {} for path in paths if "." in path}
        return await self._apply(company.id, {"$set": fields}, only_if=only_if, containers=parents)

    async def save_name(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["name"])

    async def save_test_group(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["is_test_group", "test_label"])

    async def save_organization(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["organization_id", "organization_relation", "organization_note"])

    async def save_internal_use(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["internal_use", "internal_note"])

    async def save_executive_chatty(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["messaging_settings.is_executive_chatty", "messaging_settings.hide_chats"])

    async def save_chattyless(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["messaging_settings.is_chattyless"])

    async def save_hammer_credentials(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["hammer_credentials"])

    async def save_messaging_settings(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["messaging_settings"])

    async def save_display_phone_number(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["display_phone_number"])

    async def save_friendly_aliases(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["friendly_aliases"])

    async def save_allowed_origins(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["allowed_origins"])

    async def save_cc_template_name(self, company: EmpresaModel) -> EmpresaModel:
        return await self._save(company, ["continuous_conversation_template_name"])

    async def save_registration_extras(self, company: EmpresaModel, *, display_phone_number: bool,
                                       industry: bool) -> EmpresaModel:
        paths = ["display_phone_number"] if display_phone_number else []
        if industry:
            paths.append("industry")
        return await self._save(company, paths)

    async def save_integration(self, company: EmpresaModel, field: str) -> EmpresaModel:
        return await self._save(company, [field])

    async def save_connection(self, company: EmpresaModel, *, waba: bool, display_phone_number: bool,
                              executive_chatty: bool) -> EmpresaModel:
        paths = ["phone_number_id", "meta_token", "disconnected_at", "messaging_settings.is_coexistence"]
        if waba:
            paths.append("business_account_id")
        if display_phone_number:
            paths.append("display_phone_number")
        if executive_chatty:
            paths += ["messaging_settings.is_executive_chatty", "messaging_settings.hide_chats"]
        return await self._save(company, paths)

    async def save_resolved_waba(self, company: EmpresaModel, *, only_if_phone: str) -> EmpresaModel:
        return await self._save(company, ["business_account_id"], only_if={"phone_number_id": only_if_phone})

    async def save_meta_profile(self, company: EmpresaModel, fields: Sequence[str], *,
                                only_if_phone: str) -> EmpresaModel:
        return await self._save(company, fields, only_if={"phone_number_id": only_if_phone})

    async def add_beta(self, company_id: str, beta: str) -> EmpresaModel:
        return await self._apply(company_id, {"$addToSet": {"betas": beta}}, containers={"betas": []})

    async def remove_beta(self, company_id: str, beta: str) -> EmpresaModel:
        return await self._apply(company_id, {"$pull": {"betas": beta}}, containers={"betas": []})
