"""V2: iframe a11y trees are grafted under their host <iframe> AX node."""
from testmu_selenium._helpers import iframe_a11y


def _dom():
    # doc 0 hosts an <iframe> (node idx 1, backend 11) whose content is doc 1;
    # doc 1 hosts a nested <iframe> (node idx 0, backend 21) whose content is doc 2.
    return {"documents": [
        {"nodes": {"backendNodeId": [10, 11], "contentDocumentIndex": {"index": [1], "value": [1]}}},
        {"nodes": {"backendNodeId": [21], "contentDocumentIndex": {"index": [0], "value": [2]}}},
        {"nodes": {"backendNodeId": [30]}},
    ]}


def _tree():
    return {"frameTree": {"frame": {"id": "M"}, "childFrames": [
        {"frame": {"id": "F1"}, "childFrames": [{"frame": {"id": "F2"}}]},
    ]}}


def test_merge_wires_nested_iframes_and_shifts_ids():
    main = {"nodes": [
        {"nodeId": "1", "childIds": ["2"], "backendDOMNodeId": 10},
        {"nodeId": "2", "parentId": "1", "backendDOMNodeId": 11, "frameId": "F1"},
    ]}
    f1 = {"nodes": [
        {"nodeId": "1", "childIds": ["2"]},
        {"nodeId": "2", "parentId": "1", "backendDOMNodeId": 21, "frameId": "F2"},
    ]}
    f2 = {"nodes": [{"nodeId": "1", "role": {"value": "Date"}, "value": {"value": "2026-09-21"}}]}

    frames = iframe_a11y.frame_ids_with_parents(_tree())
    assert frames == [("M", None), ("F1", "M"), ("F2", "F1")]
    frame_ax = {"M": main, "F1": f1, "F2": f2}
    owners = iframe_a11y.owners_from_parent_ax(frames, frame_ax)
    assert owners == {"F1": 11, "F2": 21}

    merged = iframe_a11y.merge_iframe_a11y(main, _dom(), frames, frame_ax, owners)
    assert merged == 3
    ids = [n["nodeId"] for n in main["nodes"]]
    assert len(ids) == len(set(ids))  # no collisions
    by_id = {n["nodeId"]: n for n in main["nodes"]}
    f1_root = next(n for n in f1["nodes"] if n.get("childIds"))
    assert f1_root["parentId"] == "2" and f1_root["nodeId"] in by_id["2"]["childIds"]
    date = f2["nodes"][0]
    host2 = next(n for n in f1["nodes"] if n.get("backendDOMNodeId") == 21)
    assert date["parentId"] == host2["nodeId"] and date["nodeId"] in host2["childIds"]


def test_merge_is_a_noop_without_iframes_or_unmatched_owner():
    main = {"nodes": [{"nodeId": "1"}]}
    assert iframe_a11y.merge_iframe_a11y(main, {"documents": [{}]}, [], {}, {}) == 0
    frames = [("M", None), ("F1", "M")]
    assert iframe_a11y.merge_iframe_a11y(
        main, _dom(), frames, {"F1": {"nodes": [{"nodeId": "1"}]}}, {"F1": 999}) == 0
    assert main["nodes"] == [{"nodeId": "1"}]
