import os
from typing import Literal, cast, get_args

from setuptools import find_packages, setup
from setuptools.command.sdist import sdist
from setuptools.dist import Distribution

try:
    from setuptools.command.bdist_wheel import bdist_wheel
except ImportError:
    from wheel.bdist_wheel import bdist_wheel  # type: ignore

# clone from importer.py due to import issues in isolated setup environment
SYSTEMS = Literal["Windows", "Linux", "Darwin"]
ARCHS = Literal["x64", "x86", "arm", "arm64"]


def get_fmod_path_for_config(
    system: SYSTEMS,
    arch: ARCHS,
) -> str:
    if system == "Darwin":
        # universal dylib
        return "libfmod/Darwin/libfmod.dylib"
    if system == "Windows":
        return f"libfmod/Windows/{arch}/fmod.dll"
    if system == "Linux":
        arch_f = arch if arch != "x64" else "x86_64"
        return f"libfmod/Linux/{arch_f}/libfmod.so"

    raise NotImplementedError(f"Unsupported system: {system}")


BDIST_TAG_FMOD_MAP = {
    # Windows
    "win32": "x86",
    "win_amd64": "x64",
    "win_arm64": "arm",
    # Linux and Mac endings
    "arm64": "arm64",  # Mac
    "x86_64": "x64",
    "aarch64": "arm64",  # Linux
    "i686": "x86",
    "armv7l": "arm",  # armhf
}


class SDist(sdist):
    def make_distribution(self) -> None:
        # add all fmod libraries to the distribution
        self.filelist.files.extend(
            [
                f"{root}/{file}".replace("\\", "/")
                for root, _, files in os.walk("fmod_toolkit/libfmod")
                for file in files
                if file.endswith((".dll", ".so", ".dylib"))
            ]
        )
        return super().make_distribution()


class BDistWheel(bdist_wheel):  # type: ignore
    def run(self):
        # Determine platform-specific binary for this wheel
        platform_tag = self.get_tag()[2]
        if platform_tag.startswith("win"):
            system = "Windows"
            arch = BDIST_TAG_FMOD_MAP[platform_tag]
        else:
            arch = next(
                (v for k, v in BDIST_TAG_FMOD_MAP.items() if platform_tag.endswith(k)),
                None,
            )
            system = "Darwin" if platform_tag.startswith("macosx") else "Linux"

        if arch in get_args(ARCHS):
            fmod_path = get_fmod_path_for_config(system, cast(ARCHS, arch))
            self.distribution.package_data["fmod_toolkit"].append(fmod_path)

        super().run()

    def get_tag(self):
        self.root_is_pure = False
        impl, abi_tag, plat_name = super().get_tag()
        self.root_is_pure = True
        if impl.startswith("cp"):
            # hard set 3.8 for CPython
            return "cp38", "abi3", plat_name
        return impl, abi_tag, plat_name


def cleanup():
    import shutil

    root_dir = os.path.abspath(os.path.dirname(__file__))
    build_dir = os.path.join(root_dir, "build")
    egg_info_dir = os.path.join(root_dir, "fmod_toolkit.egg-info")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(egg_info_dir):
        shutil.rmtree(egg_info_dir)


class UnpureDistribution(Distribution):
    """Distribution which is not marked as pure, so that wheels are built as platform-specific"""

    def is_pure(self) -> bool:
        return False


setup(
    name="fmod_toolkit",
    packages=find_packages(),
    package_data={"fmod_toolkit": []},
    cmdclass={"sdist": SDist, "bdist_wheel": BDistWheel},
    distclass=UnpureDistribution,
    zip_safe=False,
)
if os.environ.get("PY_SETUP_CLEANUP", "1") != "0":
    cleanup()
