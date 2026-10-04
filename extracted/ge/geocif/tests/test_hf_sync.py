"""Regression test: hf_sync must upload AgMet PNGs from where geoagmet writes
them, ``<[PATHS] dir_output>/<project_name>/crop_condition/``. No network: the
huggingface_hub module is replaced by a fake that records the upload calls.
"""
import configparser
import sys
import types

from geocif import hf_sync


def test_hf_sync_globs_crop_condition_not_agmet(tmp_path, monkeypatch):
    # 2026-10-03: G3, introduced in ff1ac0d (0.4.256) — globbed <project>/agmet,
    # a folder geoagmet never creates.
    proj = tmp_path / "outputs" / "agmet"
    db = proj / "ml" / "db" / "outlook.db"
    db.parent.mkdir(parents=True)
    db.write_bytes(b"")
    png = (proj / "crop_condition" / "October_03_2026" / "plots" / "AMIS" / "kenya"
           / "mz_s1_2026" / "condition" / "adm1" / "nakuru.png")
    png.parent.mkdir(parents=True)
    png.write_bytes(b"")

    folder_uploads = []

    class FakeApi:
        def create_repo(self, *args, **kwargs):
            pass

        def upload_file(self, **kwargs):
            pass

        def upload_folder(self, **kwargs):
            folder_uploads.append(kwargs)

    def no_manifest(**kwargs):
        raise FileNotFoundError("no manifest.json yet")

    fake_hub = types.ModuleType("huggingface_hub")
    fake_hub.HfApi = FakeApi
    fake_hub.hf_hub_download = no_manifest
    monkeypatch.setitem(sys.modules, "huggingface_hub", fake_hub)

    parser = configparser.ConfigParser()
    parser.read_dict({
        "DEFAULT": {"project_name": "agmet", "db": "outlook.db", "countries": "['kenya']"},
        "PATHS": {"dir_output": str(tmp_path / "outputs")},
        "ML": {"hf_repo_id": "test/geocif-data"},
    })
    hf_sync.upload_to_hf(parser)

    agmet_uploads = [u for u in folder_uploads if u["path_in_repo"] == "agmet"]
    assert [u["folder_path"] for u in agmet_uploads] == [str(proj / "crop_condition")]
