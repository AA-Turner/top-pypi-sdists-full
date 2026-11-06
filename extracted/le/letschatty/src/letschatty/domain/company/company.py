"""The company document (`empresas`): the port of how it is stored, and of what remembers it.

A change has a name, not a path: each method writes the fields of ONE change a caller makes today, with the values the
model it receives holds now (ADR-017). Everything else in the stored document stays as it is, because the caller read
its copy before seconds of work (HTTP to Meta or Shopify, S3) that someone else may have raced: a make_default that
re-mirrored another number, the staff switching off a beta.

Every change bumps `updated_at`, and answers the company as Mongo has it AFTER the write, not the caller's copy.
Everything that caches the company has forgotten it by then.
"""
from __future__ import annotations

from typing import List, Optional, Protocol, Sequence

from ...models.company.empresa import EmpresaModel


class CompanyChangedMeanwhile(Exception):
    """A partial write was conditioned on the company still being as it was read (`only_if`) and it
    no longer is: someone else (e.g. a make_default that re-mirrored another number) changed it
    during the slow work in between. The write was NOT applied."""


class CompanyRepository(Protocol):
    async def get(self, company_id: str, *, ignore_cache: bool = False) -> EmpresaModel:
        """The company, deleted or not. Raises `NotFoundError` when there is none."""
        ...

    async def live(self, *, ignore_cache: bool = False) -> List[EmpresaModel]:
        """Every company whose `deleted_at` is null or missing."""
        ...

    async def deleted(self) -> List[EmpresaModel]:
        """Every soft-deleted company."""
        ...

    async def by_shopify_domain(self, shop_domain: str) -> Optional[EmpresaModel]:
        """The first company bound to that store, deleted or not."""
        ...

    async def create(self, company: EmpresaModel) -> None: ...

    async def soft_delete(self, company: EmpresaModel) -> None: ...

    async def restore(self, company_id: str) -> EmpresaModel:
        """Clears `deleted_at`, stamps `updated_at` and answers the company as written."""
        ...

    async def save_name(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_test_group(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_organization(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_internal_use(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_executive_chatty(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_chattyless(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_hammer_credentials(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_messaging_settings(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_display_phone_number(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_friendly_aliases(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_allowed_origins(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_cc_template_name(self, company: EmpresaModel) -> EmpresaModel: ...

    async def save_registration_extras(self, company: EmpresaModel, *, display_phone_number: bool,
                                       industry: bool) -> EmpresaModel:
        """The extras of a company a mega-admin creates: only the ones that came."""
        ...

    async def save_integration(self, company: EmpresaModel, field: str) -> EmpresaModel:
        """The subdocument of one store integration, by the name of its field on the company."""
        ...

    async def save_connection(self, company: EmpresaModel, *, waba: bool, display_phone_number: bool,
                              executive_chatty: bool) -> EmpresaModel:
        """The mirror of the default account on a (re)connection: number, token, `disconnected_at`, coexistence, and
        only what this connection owns of the rest."""
        ...

    async def save_resolved_waba(self, company: EmpresaModel, *, only_if_phone: str) -> EmpresaModel:
        """The WABA, if the company still has the number it was resolved from: `CompanyChangedMeanwhile` otherwise."""
        ...

    async def save_meta_profile(self, company: EmpresaModel, fields: Sequence[str], *,
                                only_if_phone: str) -> EmpresaModel:
        """The fields of the company that the refresh of its Meta profile owns, if the company still has that number:
        `CompanyChangedMeanwhile` otherwise."""
        ...

    async def add_beta(self, company_id: str, beta: str) -> EmpresaModel:
        """Turns one beta on without rewriting the others (no duplicates)."""
        ...

    async def remove_beta(self, company_id: str, beta: str) -> EmpresaModel: ...


class CompanyCaches(Protocol):
    """What remembers a company outside Mongo: the asset, its settings and betas, its routing keys, and the version each
    worker compares its `Empresa` in memory against (api-chatty `docs/empresa-en-memoria.md`)."""

    async def forget(self, company: EmpresaModel) -> None:
        """Forgets it, with the version LAST. A failure clearing the settings or the betas goes up, and the version is
        marked anyway."""
        ...

    async def forget_quietly(self, company: EmpresaModel) -> None:
        """`forget`, with its failure a WARNING."""
        ...

    async def version(self, company_id: str) -> Optional[str]:
        """The company's version, None if it never changed since the key exists. Raises if Redis fails: the caller
        decides (the instantiator serves its copy in memory)."""
        ...


class RoutingIndex(Protocol):
    """The keys that find a company by number, alias or origin (`company_routing:*`). Each holds the whole company."""

    def keys_of(self, company: EmpresaModel) -> List[str]:
        """The keys `company` routes by as it is now, to drop them after it changed."""
        ...

    async def index(self, company: EmpresaModel) -> None:
        """Writes its keys, 24 h. A failure is a WARNING. A deleted company only keeps the one of its number."""
        ...

    async def drop(self, company: EmpresaModel) -> None:
        """Deletes its keys. A failure is a WARNING."""
        ...

    async def drop_previous(self, keys: Sequence[str]) -> None:
        """Deletes keys read before a change. A failure goes up."""
        ...
