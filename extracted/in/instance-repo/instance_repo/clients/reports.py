"""clients/reports.py — 质检 RolloutReport 的存取（OSS，走通用对象接口）。

report 只存 OSS（`{version}-report/{id}/report.jsonl`），不写 apiserver DB。
put/get 单实例；assemble_jsonl 把一批实例的 report 拼成数据集级 verl 训练 jsonl。
content_store 的 OSS 访问一律用 apiserver 签发的 STS（按对象 key 收窄），无长期 AK/SK。
"""
from __future__ import annotations

from pathlib import Path

from .. import paths as P
from ..layout import Layout
from ..models import RolloutReport
from .config import business_metadata_model


class ReportsClient:
    def __init__(self, content_store, profile=None) -> None:
        self._c = content_store
        self._p = profile

    def _layout(self) -> Layout:
        model = business_metadata_model(
            getattr(self._p, "metadata_model", None))
        prefix = getattr(self._p, "oss_prefix", None) or P.DEFAULT_PREFIX
        return Layout(model, prefix=prefix)

    def put(self, report: RolloutReport, version: str, *,
            split: str = "default", overwrite: bool = False) -> dict:
        """上传单实例 report.jsonl（一行）。dataset/instance 取自 report 本身。
        默认 overwrite=False：同实例 report 已存在则跳过（返回 skipped）；质检重跑刷新
        分数需显式 overwrite=True，否则新分不会覆盖旧 report。"""
        report.validate()
        lay = self._layout()
        key = lay.report_key(report.datasetname, report.instanceid,
                             version=version, split=split)
        line = (report.to_jsonl_line() + "\n").encode("utf-8")
        return self._c.put_object(key, line, overwrite=overwrite,
                                  sts_prefix=lay.sts_prefix(report.datasetname),
                                  dataset=report.datasetname)

    def get(self, dataset: str, version: str, instance_id: str,
            split: str = "default") -> RolloutReport:
        """下载并解析单实例 report。"""
        import tempfile
        lay = self._layout()
        key = lay.report_key(dataset, instance_id, version=version, split=split)
        with tempfile.TemporaryDirectory(prefix="irepo_rpt_") as td:
            dest = Path(td) / "report.jsonl"
            self._c.get_object(key, dest,
                               sts_prefix=lay.sts_prefix(dataset),
                               dataset=dataset)
            line = dest.read_text(encoding="utf-8").strip()
        return RolloutReport.from_jsonl_line(line)

    def assemble_jsonl(self, dataset: str, version: str, instances: list[str],
                       dest, split: str = "default") -> Path:
        """把多个实例的 report 拼成数据集级 verl 训练 jsonl（每实例一行）到 dest。"""
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            for iid in instances:
                rpt = self.get(dataset, version, iid, split)
                f.write(rpt.to_jsonl_line() + "\n")
        return dest
