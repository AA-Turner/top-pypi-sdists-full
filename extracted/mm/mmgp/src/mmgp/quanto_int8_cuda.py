from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace

import torch
from torch.utils import cpp_extension

_STATE = SimpleNamespace(module=None)

def _maybe_set_msvc_env() -> None:
    if os.name != "nt":
        return
    if os.environ.get("VCToolsInstallDir") and os.environ.get("INCLUDE"):
        return
    vs_root = Path(os.environ.get("VSINSTALLDIR", r"C:\Program Files\Microsoft Visual Studio\2022\Community"))
    msvc_root = vs_root / "VC" / "Tools" / "MSVC"
    sdk_root = Path(r"C:\Program Files (x86)\Windows Kits\10")
    if not msvc_root.exists() or not sdk_root.exists():
        return
    msvc_versions = sorted(msvc_root.iterdir(), reverse=True)
    sdk_includes = sorted((sdk_root / "Include").iterdir(), reverse=True)
    if not msvc_versions or not sdk_includes:
        return
    vc_tools = msvc_versions[0]
    sdk_ver = sdk_includes[0].name
    os.environ.setdefault("VCToolsInstallDir", str(vc_tools) + os.sep)
    os.environ.setdefault("VCINSTALLDIR", str(vs_root / "VC") + os.sep)
    os.environ.setdefault("WindowsSdkDir", str(sdk_root) + os.sep)
    os.environ.setdefault("WindowsSDKVersion", sdk_ver + os.sep)
    os.environ["PATH"] = f"{vc_tools}\\bin\\Hostx64\\x64;{sdk_root}\\bin\\{sdk_ver}\\x64;" + os.environ.get("PATH", "")
    os.environ["INCLUDE"] = (
        f"{vc_tools}\\include;{sdk_root}\\Include\\{sdk_ver}\\ucrt;{sdk_root}\\Include\\{sdk_ver}\\shared;"
        f"{sdk_root}\\Include\\{sdk_ver}\\um;{sdk_root}\\Include\\{sdk_ver}\\winrt;{sdk_root}\\Include\\{sdk_ver}\\cppwinrt"
    )
    os.environ["LIB"] = (
        f"{vc_tools}\\lib\\x64;{sdk_root}\\Lib\\{sdk_ver}\\ucrt\\x64;{sdk_root}\\Lib\\{sdk_ver}\\um\\x64"
    )


def _extra_cflags() -> list[str]:
    if os.name == "nt":
        return ["/O2"]
    return ["-O3"]


def _extra_cuda_cflags() -> list[str]:
    flags = [
        "-O3",
        "--use_fast_math",
        "--expt-relaxed-constexpr",
        "--expt-extended-lambda",
    ]
    return flags


def _sources() -> list[str]:
    src_dir = Path(__file__).parent / "quanto_int8_kernels"
    return [
        str(src_dir / "int8_scaled_mm.cpp"),
        str(src_dir / "int8_scaled_mm.cu"),
    ]


def _build_dir() -> str:
    build_dir = Path(__file__).parent / "quanto_int8_kernels" / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    return str(build_dir)


def load() -> object:
    if _STATE.module is not None:
        return _STATE.module
    _maybe_set_msvc_env()
    name = "mmgp_quanto_int8_cuda"
    _STATE.module = cpp_extension.load(
        name=name,
        sources=_sources(),
        build_directory=_build_dir(),
        extra_cflags=_extra_cflags(),
        extra_cuda_cflags=_extra_cuda_cflags(),
        verbose=True,
    )
    return _STATE.module


def int8_scaled_mm(a: torch.Tensor, b: torch.Tensor, a_scale: torch.Tensor, b_scale: torch.Tensor) -> torch.Tensor:
    return load().int8_scaled_mm(a, b, a_scale, b_scale)


def quantize_per_row_int8(a: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    return load().quantize_per_row_int8(a)


def scale_int32_to(acc: torch.Tensor, a_scale: torch.Tensor, b_scale: torch.Tensor) -> torch.Tensor:
    return load().scale_int32_to(acc, a_scale, b_scale)
