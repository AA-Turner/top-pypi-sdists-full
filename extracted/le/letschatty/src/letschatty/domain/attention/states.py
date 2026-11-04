"""The stored states of the attention runtime that the repositories read (api-chatty `docs/atencion/reglas.md`).

The values are the strings Mongo already holds: they never change, only their names are English. They live in the
domain because the repositories (the stores of `atencion_en_chat` and `clasificaciones_de_motivo`) filter by them
and letschatty cannot import api-chatty's `application/`.

- The AI on the reason (`atencion_en_chat.ia.estado`): active or finished.
- A classification request (`clasificaciones_de_motivo.estado`):

      gathering ──silence──▶ classifying ──▶ resolved
      classifying ──▶ asking ──▶ classifying (round 2)
      classifying ──▶ in_general_inquiry ──▶ classifying (reclassifies)
      any active ──expires──▶ resolved · any active ──another entry of the same chat──▶ replaced

  `waiting_for_a_message` is only for requests created before 2026-10-01 (F3); it is no longer created.
- How a learned phrase resolved a reason (`chatty_asset_triggers`, the shortcut): exact or similar.
- Who cut the follow-ups of a chat (`atencion_en_chat.cortados.por`): a person with «Cortar», «No contactar», the chat
  archived or blocked when the closing came, or the system.
"""
from __future__ import annotations

AI_ACTIVE = "activa"
AI_FINISHED = "terminada"

GATHERING = "juntando"
CLASSIFYING = "clasificando"
WAITING_FOR_A_MESSAGE = "esperando_mensaje"
ASKING = "preguntando"
IN_GENERAL_INQUIRY = "en_consulta_general"
CORRECTABLE = "corregible"
RESOLVED = "resuelto"
REPLACED = "reemplazado"
ACTIVE_REQUEST_STATES = (GATHERING, CLASSIFYING, WAITING_FOR_A_MESSAGE, ASKING, IN_GENERAL_INQUIRY, CORRECTABLE)

SHORTCUT_PHRASE = "frase"
SHORTCUT_SIMILAR = "similar"

CUT_BY = ("usuario", "no_contactar", "archivado", "bloqueado", "sistema")
