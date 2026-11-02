from enum import StrEnum
from typing import Optional

class Status(StrEnum):
    READ = "read"
    DELIVERED = "delivered"
    SENT = "sent"
    WAITING = "waiting" #user started the action but we still haven't received the confirmation from the external API
    FAILED = "failed"
    META_API_CALL_SUCCESS = "success" #The META api call was succesfull but still haven't received a webhook notification with a new status
    PENDING = "pending" #For template campaigns, when the recipient is pending to be processed
    PLAYED = "played" #WhatsApp voice-note "played" receipt. WEBHOOK-ONLY: it arrives as a status notification but is NEVER persisted to Message.status — the receiver maps it to Message.played_at. update_status() rejects it; see docs/played-voice-note-status.md.
    # ANSWERED = "answered"
    # INTERACTION = "interaction"

    def supersedes(self, current: Optional["Status"], *, confirmed_by_meta: bool = True) -> bool:
        """¿Este estado puede reemplazar a `current`? Sólo si AVANZA en el ciclo de vida.

        Meta manda `sent`, `delivered` y `read` casi juntos —muchas veces en el mismo
        segundo—, como webhooks separados que nada ordena entre sí. Aplicar el último que se
        procesaba dejaba con una sola tilde un mensaje entregado: un `sent` que llegaba
        tarde pisaba al `delivered`.

        `confirmed_by_meta=False` es un mensaje que Meta nunca identificó: el envío dio
        timeout o 5xx, lo guardamos `failed` con nuestro propio id, y Meta igual pudo
        aceptarlo (sus estados llegan después, reconciliados por `biz_opaque_callback_data`).
        Esa falla es una suposición nuestra, así que cualquier estado de Meta la corrige.
        """
        rank = _DELIVERY_RANK.get(self)
        if rank is None:
            return False
        if current is None:
            return True
        if current == Status.FAILED and not confirmed_by_meta:
            return rank > _UNCONFIRMED_FAILURE_RANK
        return rank > _DELIVERY_RANK.get(current, -1)

    def superseded_statuses(self, *, confirmed_by_meta: bool = True) -> list["Status"]:
        """Los estados que éste puede reemplazar: el filtro de la escritura condicional."""
        return [status for status in _DELIVERY_RANK if self.supersedes(status, confirmed_by_meta=confirmed_by_meta)]


def is_meta_message_id(message_id: str) -> bool:
    """Los ids que asigna Meta empiezan con `wamid.`. Un mensaje saliente con otro id es uno
    que guardamos con el nuestro porque el envío falló antes de que Meta respondiera."""
    return str(message_id).startswith("wamid.")


# El ciclo de vida de un mensaje saliente. `failed` va entre `sent` y `delivered`: Meta
# puede avisar que falló después de aceptarlo, así que un `sent` tardío no lo tapa; pero
# un `delivered` o `read` es la prueba de que sí llegó. `played` no está: no es un estado
# de entrega.
_DELIVERY_RANK = {
    Status.WAITING: 0,
    Status.PENDING: 0,
    Status.META_API_CALL_SUCCESS: 0,
    Status.SENT: 1,
    Status.FAILED: 2,
    Status.DELIVERED: 3,
    Status.READ: 4,
}
# Una falla que Meta no confirmó vale lo mismo que un envío en curso.
_UNCONFIRMED_FAILURE_RANK = 0
