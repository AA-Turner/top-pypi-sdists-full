"""Shared fakes for macOS installer tests."""

from pathlib import Path
import subprocess

from tests.platform_installer_helpers import RecordingRunner


AIWATCH_PACKAGE_ID = "com.runlayer.aiwatch"


class ExpandingMacPackageRunner(RecordingRunner):
    def __init__(
        self,
        package_id: str,
        *responses: subprocess.CompletedProcess[str] | BaseException,
        version: str = "2.0.0",
        arch: str = "arm64",
        component_ids: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__(*responses)
        self.package_id = package_id
        self.version = version
        self.arch = arch
        self.component_ids = (package_id,) if component_ids is None else component_ids

    def __call__(self, argv: list[str], **kwargs: object):
        if argv[:2] == ["/usr/sbin/pkgutil", "--expand"]:
            for index, identifier in enumerate(self.component_ids):
                component = Path(argv[-1]) / f"component-{index}.pkg"
                component.mkdir(parents=True)
                (component / "PackageInfo").write_text(
                    f'<pkg-info identifier="{identifier}" version="{self.version}"/>'
                )
            (Path(argv[-1]) / "Distribution").write_text(
                "<installer-gui-script>"
                f'<options hostArchitectures="{self.arch}"/>'
                "</installer-gui-script>"
            )
        return super().__call__(argv, **kwargs)
