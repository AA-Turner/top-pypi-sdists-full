"""Categoría de recordatorios: describe el TIPO DE TAREA, no al cliente.

Por eso no se reusan las etiquetas —una etiqueta describe al chat, esto describe qué hay
que hacer— y por eso no lleva color: la fila del recordatorio ya usa cuatro colores con
significado (vencido, para hoy, hecho, BETA) y un color libre por categoría los volvería
ilegibles.

Se borra lógico (`deleted_at`, heredado de `ChattyAssetModel`): deja de OFRECERSE para
elegir en un recordatorio nuevo, pero un recordatorio que ya la tenía la sigue mostrando
—nombrarla con su `RecordatorioCategoriaPreview` no depende de que siga activa—.
"""
from __future__ import annotations

from typing import ClassVar

from ...base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel


class RecordatorioCategoriaPreview(ChattyAssetPreview):
    """Lo que necesita un selector o un chip: id, nombre y si está borrada.

    `deleted_at` ya viaja en `ChattyAssetPreview`: es justo lo que permite nombrar una
    categoría borrada sin tener que ir a buscar el asset completo.
    """


class RecordatorioCategoria(CompanyAssetModel):
    """Una categoría de recordatorios de una empresa ("Cobranza", "Presupuestos")."""

    name: str
    preview_class: ClassVar[type[RecordatorioCategoriaPreview]] = RecordatorioCategoriaPreview
