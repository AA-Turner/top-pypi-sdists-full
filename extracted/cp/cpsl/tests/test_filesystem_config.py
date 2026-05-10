import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.typestubs import generate_type_stubs
from cpsl.utils import build_filesystem_mount_specs


class FileSystemConfigTests(unittest.TestCase):
    def test_filesystem_serializes_sources_and_tools(self):
        fs = (
            cpsl.FileSystem("customer-data")
            .smart_source("gmail", "priority-mail", guidance="Important customers")
            .source_query("gdrive", "contracts", filter={"mimeType": "application/pdf"})
            .mcp("browser", command="npx", args=["browser-mcp"], env={"TOKEN": "secret"})
        )

        data = fs.to_dict()

        self.assertEqual(data["name"], "customer-data")
        self.assertEqual(data["sources"][0]["mode"], "smart")
        self.assertEqual(data["sources"][1]["mode"], "query")
        self.assertEqual(data["sources"][1]["filter"], {"mimeType": "application/pdf"})
        self.assertEqual(data["tools"][0]["kind"], "mcp")

    def test_build_filesystem_mount_specs(self):
        fs = cpsl.FileSystem("customer-data").source_query(
            "gmail",
            "vip-mail",
            filter={"q": "from:vip@example.com"},
            cache_ttl=60,
        )

        mounts = build_filesystem_mount_specs({"/data": fs.to_dict()})

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0].mount_path, "/data")
        self.assertEqual(mounts[0].name, "customer-data")
        self.assertEqual(mounts[0].sources[0].filter, '{"q": "from:vip@example.com"}')
        self.assertEqual(mounts[0].sources[0].cache_ttl, 60)

    def test_file_helper_returns_json_safe_reference(self):
        ref = cpsl.file("/reports/q1.pdf", label="PDF Report")

        self.assertEqual(
            ref,
            {
                "_type": "file",
                "path": "/reports/q1.pdf",
                "label": "PDF Report",
            },
        )
        self.assertEqual(json.loads(json.dumps(ref))["path"], "/reports/q1.pdf")

    def test_filesystem_link_uses_bound_mount_path(self):
        reports = cpsl.FileSystem("reports")
        app = cpsl.App(
            name="reports-app",
            image=cpsl.Image(),
            filesystems={"/reports": reports},
        )

        ref = reports.link("q1.pdf", label="PDF Report")

        self.assertEqual(ref["path"], "/reports/q1.pdf")
        self.assertEqual(ref["label"], "PDF Report")
        self.assertEqual(app._serialize()["filesystems"]["/reports"]["name"], "reports")

    def test_filesystem_link_requires_mount_path(self):
        reports = cpsl.FileSystem("reports")

        with self.assertRaises(RuntimeError):
            reports.link("q1.pdf")

    def test_react_type_stubs_include_file_helpers(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                generate_type_stubs([{"type": "react", "packages": []}], ["lucide-react"])
                dts = Path(".capsule/types/capsule-page.d.ts").read_text()
                packages = Path(".capsule/types/packages.d.ts").read_text()
            finally:
                os.chdir(cwd)

        self.assertIn("export function fileUrl(path: string): string;", dts)
        self.assertIn("export function useFileUrl(path: string): string;", dts)
        self.assertIn("export const FileLink: FC<FileLinkProps>;", dts)
        self.assertIn('declare module "lucide-react";', packages)


if __name__ == "__main__":
    unittest.main()
