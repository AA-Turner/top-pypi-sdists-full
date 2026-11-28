"""Stage normalized rollout evidence and publish or restore an immutable historical revision (twin: app/runs/samples/evidence)."""

from __future__ import annotations

from urllib.parse import quote


def _quote(value):
    return quote(str(value), safe="")


class SampleEvidenceMixin:
    def sample_evidence_head(self, run_id):
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/evidence/head")

    def sample_evidence_owners(self, run_id, sample_ids):
        return self.transport.post(
            f"/v1/runs/{_quote(run_id)}/samples/evidence/owners",
            {"sample_ids": [str(key) for key in sample_ids]},
            idempotent=True,
        )

    def stage_sample_evidence(self, run_id, sample_id, *, write_epoch, sample_key, document):
        from probe.generated.samples.evidence import SampleEvidence
        from probe.sdk.redaction import default_scrub

        value = (
            document.model_dump(mode="json", exclude_none=True)
            if hasattr(document, "model_dump")
            else document
        )
        clean = SampleEvidence.model_validate(default_scrub(value))
        body = dict(
            write_epoch=write_epoch,
            sample_key=sample_key,
            document=clean.model_dump(mode="json", exclude_none=True),
        )
        return self.transport.post(
            f"/v1/runs/{_quote(run_id)}/samples/evidence/documents/{_quote(sample_id)}",
            body,
            idempotent=True,
        )

    def publish_sample_evidence(self, run_id, *, expected_generation, members):
        items = [
            m.model_dump(mode="json", exclude_none=True) if hasattr(m, "model_dump") else m
            for m in members
        ]
        return self.transport.request(
            "POST",
            f"/v1/runs/{_quote(run_id)}/samples/evidence/publish",
            json_body=dict(expected_generation=expected_generation, members=items),
            idempotent=True,
            timeout=600,
        ).json()

    def restore_sample_evidence(self, run_id, *, expected_generation, revision):
        return self.transport.request(
            "POST",
            f"/v1/runs/{_quote(run_id)}/samples/evidence/restore",
            json_body=dict(expected_generation=expected_generation, revision=revision),
            idempotent=True,
            timeout=600,
        ).json()

    def get_sample_evidence(self, run_id, sample_id, *, generation=None, watermark=None):
        query = {
            k: v for k, v in (("generation", generation), ("watermark", watermark)) if v is not None
        }
        return self.transport.get(
            f"/v1/runs/{_quote(run_id)}/samples/evidence/documents/{_quote(sample_id)}",
            params=query or None,
        )
