from fray.interactive import GuidedPipeline


def test_guided_pipeline_includes_share_metadata():
    pipeline = GuidedPipeline("https://target.test", quiet=True)
    pipeline.recon_result = {"host": "target.test"}

    share_id = "share123"
    share_url = "https://share.example/view?id=share123"
    share_info = {
        "domain": "target.test",
        "shared_at": "2025-01-01T00:00:00Z",
        "expires_at": "2999-01-01T00:00:00Z",
    }

    pipeline.share_url = share_url
    pipeline._record_share_metadata(share_id, share_url, share_info)

    summary = pipeline._serialize_summary({"target": pipeline.target, "phases": []})

    assert summary["share_url"] == share_url
    assert summary["share"]["id"] == share_id
    assert summary["share"]["domain"] == "target.test"
    assert summary["share"]["status"]["state"] == "ok"
    assert pipeline.recon_result["_share"]["expires_at"] == share_info["expires_at"]
