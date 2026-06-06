"""Generate a PyInstaller VSVersionInfo file for Windows PE resources.

VS_FIXEDFILEINFO requires a 4-tuple of ints; pre-release suffixes
(rc1, dev0, a1, ...) only appear in the string-form FileVersion / ProductVersion.
"""

from pathlib import Path

from packaging.version import Version

_TEMPLATE = """\
VSVersionInfo(
  ffi=FixedFileInfo(filevers={tup}, prodvers={tup}, mask=0x3f, flags=0x0,
                    OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable("040904B0", [
      StringStruct("CompanyName", "Runlayer Inc."),
      StringStruct("FileDescription", {description!r}),
      StringStruct("FileVersion", {version!r}),
      StringStruct("InternalName", {name!r}),
      StringStruct("OriginalFilename", {filename!r}),
      StringStruct("ProductName", {product_name!r}),
      StringStruct("ProductVersion", {version!r}),
    ])]),
    VarFileInfo([VarStruct("Translation", [0x409, 1200])]),
  ],
)
"""


def write_version_file(
    *,
    name: str,
    description: str,
    build_dir: Path,
    product_name: str = "Runlayer AI Watch",
) -> str:
    pyproject = (Path(__file__).parent.parent / "pyproject.toml").read_text()
    raw = next(
        line for line in pyproject.splitlines() if line.startswith("version = ")
    ).split('"')[1]
    parsed = Version(raw)
    release = (*parsed.release, 0, 0, 0, 0)[:4]
    out = build_dir / f"{name}_version_info.txt"
    out.write_text(
        _TEMPLATE.format(
            tup=release,
            version=raw,
            name=name,
            filename=f"{name}.exe",
            description=description,
            product_name=product_name,
        )
    )
    return str(out)
