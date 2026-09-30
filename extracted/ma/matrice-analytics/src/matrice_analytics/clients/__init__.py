"""Backend HTTP clients for py_analytics.

**"Producer" throughout this package means the service that answers a call** -- the
far side of the wire, never anything in this repository. Five of them serve the
twenty-four endpoints, and :mod:`.models` names each one per endpoint:

producer     what answers                            endpoints       unwrap
-----------  --------------------------------------  --------------  -----------------
actions      be-actions, via the platform gateway    1, 9-12         unwrap_platform
application  be-application, same gateway            3, 6, 7         unwrap_platform
inference    be-inference, same gateway              2, 4, 5, 8, 13  unwrap_platform
fr-sidecar   the facial-recognition sidecar process  14-23           unwrap_fr_sidecar
lpr-server   the LPR server                          24              unwrap_lpr_server

There are five producers but only three unwraps, because unwrapping follows the
shape of the reply rather than the service. Two words for that shape are used
throughout:

* the **payload** is the part a caller wants -- the record, the list, the result.
* the **envelope** is the wrapper a producer puts around it, carrying whether the
  call succeeded and why not. The three behind the platform gateway all send
  ``{success, message, data}`` and the payload is under ``data``; the FR sidecar
  does the same on every route but one, which answers with a bare JSON string;
  lpr-server is inverted, sending the payload bare and a wrapper only to report
  failure.

Taking the payload out of the envelope is *unwrapping*, and it happens in exactly
one place -- :mod:`.response`. The models in :mod:`.models` describe payloads, never
envelopes.

The callers are the other direction, and are never producers here: the
facial-recognition and licence-plate usecases, and every other usecase, which
reaches the platform alone. **Client and producer do not line up**, and the three
routes where they part are why an unwrap is bound per *route* and not per client:
``FRClient`` owns two ``actions`` routes and ``LPRClient`` one, and a sidecar
unwrap on a platform reply does not raise -- it quietly returns the wrong shape.

Method names state what a call costs, so a reader need not open the file:

* ``fetch_*`` -- one route, one round trip, **every call**.
* ``get_*`` -- already in hand, or kept from an earlier call; free once the process
  is warm. Inside this package only; ``get_`` elsewhere in ``matrice_analytics``
  carries no such promise.
* ``resolve_*`` -- applies an ordered-source policy to derive a value. No I/O.
* ``mint_*`` -- obtains a grant, and **the result expires**.
* a write is named for its effect -- ``create_``, ``update_``, ``enroll_``,
  ``store_``, ``shutdown_``, ``search_``.

A ``fetch_``/``get_`` pair over one resource ships both halves only when both have
a caller; otherwise the convention becomes a way to pick the expensive one by
mistake.

This package is an **import leaf**. It may import ``matrice_common`` and the
standard library, and nothing else from ``matrice_analytics``. Everything here
is meant to be usable without dragging the rest of the SDK into the import
graph, which is what lets runtime modules depend on it rather than the reverse.

Importing anything from ``matrice_analytics.runtime`` or
``matrice_analytics.post_processing`` here would create an import cycle, because
those modules import this package. The direction is one-way by design:
``runtime`` may import ``clients``; ``clients`` may never import ``runtime``.

Submodules are imported explicitly by their users rather than re-exported here,
so that importing the package costs nothing a caller did not ask for.
"""
