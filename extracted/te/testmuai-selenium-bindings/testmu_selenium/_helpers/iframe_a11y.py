"""Merge each iframe's a11y tree into the main-frame a11y snapshot.

``Accessibility.getFullAXTree`` without a ``frameId`` covers the main frame
only, so iframe-resident controls and their runtime values (e.g. an
``<input type="date">`` that only the iframe's a11y exposes as role=Date,
value=...) never reached the textual-query endpoint. V2's
``_merge_iframe_a11y_into_main`` fetches every frame's tree and grafts it under
its host ``<iframe>`` node. Ported here as a pure merge over pre-fetched CDP
results, so the sync (Selenium) and async (Playwright) callers share one body.

Caller flow (see ``snapshot._merge_iframe_a11y``):
  1. ``Page.getFrameTree`` -> ``frame_ids_with_parents``
  2. ``Accessibility.getFullAXTree({frameId})`` for every non-main frame
  3. ``owners_from_parent_ax``; ``DOM.getFrameOwner`` only for frames it misses
  4. ``merge_iframe_a11y`` (mutates ``a11y_snapshot`` in place)
"""

import logging

_log = logging.getLogger(__name__)


def frame_ids_with_parents(frame_tree_resp):
    """``Page.getFrameTree`` response -> ``[(frame_id, parent_id)]``, main frame first."""
    out = []

    def walk(node, parent):
        fid = ((node or {}).get("frame") or {}).get("id")
        if fid:
            out.append((fid, parent))
        for child in (node or {}).get("childFrames") or []:
            walk(child, fid)

    walk((frame_tree_resp or {}).get("frameTree"), None)
    return out


def owners_from_parent_ax(frames, frame_ax):
    """Host ``<iframe>`` backend ids read off each parent frame's AX tree.

    Saves a ``DOM.getFrameOwner`` round-trip per iframe; the caller falls back
    to that call only for frames missing from the result.
    """
    owners = {}
    for fid, parent in frames[1:]:
        for node in ((frame_ax.get(parent) or {}).get("nodes") or []):
            if node.get("frameId") == fid and node.get("backendDOMNodeId") is not None:
                owners[fid] = node["backendDOMNodeId"]
                break
    return owners


def _max_node_id(nodes):
    m = 0
    for n in nodes:
        try:
            m = max(m, int(n.get("nodeId", 0)))
        except (TypeError, ValueError):
            pass
    return m


def merge_iframe_a11y(a11y_snapshot, dom_snapshot, frames, frame_ax, owners):
    """Graft every iframe's AX nodes into ``a11y_snapshot["nodes"]`` in place.

    ``frames``: ``frame_ids_with_parents`` output. ``frame_ax``: frame id ->
    ``getFullAXTree`` response. ``owners``: frame id -> host ``<iframe>``
    backend node id. Iframe node ids are shifted past the main tree's so they
    never collide, and each iframe root is re-parented onto its host's AX node
    so the tree formatter walks into it. Frames whose host cannot be matched to
    a DOM-snapshot document are skipped (V2 behaviour).
    """
    documents = (dom_snapshot or {}).get("documents") or []
    main_nodes = (a11y_snapshot or {}).get("nodes")
    if len(documents) < 2 or not main_nodes:
        return 0

    # DOM-snapshot doc index -> host <iframe> backend id. Every doc is scanned
    # so nested iframes (host lives in the parent iframe's document) map too.
    doc_to_host_bid = {}
    for parent_doc in documents:
        nodes = parent_doc.get("nodes") or {}
        bids = nodes.get("backendNodeId") or []
        cdi = nodes.get("contentDocumentIndex") or {}
        if not isinstance(cdi, dict):
            continue
        for host_idx, child_doc in zip(cdi.get("index") or [], cdi.get("value") or []):
            if 0 <= host_idx < len(bids):
                doc_to_host_bid[child_doc] = bids[host_idx]
    host_bid_to_doc = {bid: d for d, bid in doc_to_host_bid.items()}

    # Real frame id per doc, via the host backend id.
    doc_to_fid = {}
    for fid, _ in frames[1:]:
        doc = host_bid_to_doc.get(owners.get(fid))
        if doc is not None:
            doc_to_fid[doc] = fid

    bid_to_axid = {}
    for n in main_nodes:
        if n.get("backendDOMNodeId") is not None:
            bid_to_axid[n["backendDOMNodeId"]] = n.get("nodeId")

    next_offset = _max_node_id(main_nodes) + 1
    merged = 0
    for doc_idx in range(1, len(documents)):
        fid = doc_to_fid.get(doc_idx)
        iframe_nodes = ((frame_ax.get(fid) or {}).get("nodes") or []) if fid else []
        if not iframe_nodes:
            continue

        def shift(nid, off=next_offset):
            if nid is None:
                return None
            try:
                return str(int(nid) + off)
            except (TypeError, ValueError):
                return nid

        root_old = next((n.get("nodeId") for n in iframe_nodes if n.get("parentId") is None), None)
        local_max = _max_node_id(iframe_nodes)
        for n in iframe_nodes:
            n["nodeId"] = shift(n.get("nodeId"))
            if "parentId" in n:
                n["parentId"] = shift(n["parentId"])
            if "childIds" in n:
                n["childIds"] = [shift(c) for c in (n.get("childIds") or [])]
        root_new = shift(root_old)

        host_axid = bid_to_axid.get(doc_to_host_bid.get(doc_idx))
        if host_axid is not None and root_new is not None:
            for n in main_nodes:
                if n.get("nodeId") == host_axid:
                    n.setdefault("childIds", []).append(root_new)
                    break
            for n in iframe_nodes:
                if n.get("nodeId") == root_new:
                    n["parentId"] = host_axid
                    break

        main_nodes.extend(iframe_nodes)
        # A nested iframe processed later can wire onto an <iframe> AX node
        # this iframe just contributed.
        for n in iframe_nodes:
            if n.get("backendDOMNodeId") is not None:
                bid_to_axid.setdefault(n["backendDOMNodeId"], n.get("nodeId"))
        next_offset += local_max + 1
        merged += len(iframe_nodes)

    _log.info("[iframe-a11y] merged %d node(s) from %d iframe doc(s)", merged, len(documents) - 1)
    return merged
