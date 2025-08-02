# arpakit
import hashlib
import json
import os
import pathlib
from importlib.util import spec_from_file_location, module_from_spec
from typing import NamedTuple, Any, Iterator, Optional

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class ArpakitLibModule(NamedTuple):
    module_name: str
    module_version: Optional[str]
    module_content: str
    module_hash: str
    module_has_error: bool
    module_exception: Exception | None
    filename: str
    filepath: str

    def simple_dict(self) -> dict[str, Any]:
        return {
            "module_name": self.module_name,
            "module_version": self.module_version,
            "module_content": self.module_content,
            "module_hash": self.module_hash,
            "module_has_error": self.module_has_error,
            "module_exception": self.module_exception,
            "filename": self.filename,
            "filepath": self.filepath,
        }


class ArpakitLibModules(NamedTuple):
    arpakit_lib_modules: list[ArpakitLibModule]

    def __len__(self):
        return len(self.arpakit_lib_modules)

    def __repr__(self):
        return f"ArpakitLibModules (len={len(self.arpakit_lib_modules)})"

    def __iter__(self) -> Iterator[ArpakitLibModule]:
        for arpakit_lib_module in self.arpakit_lib_modules:
            yield arpakit_lib_module

    def __hash__(self) -> str:
        return self.modules_hash()

    def modules_hash(self) -> str:
        return hashlib.sha256(
            json.dumps(self.module_name_to_module_hash()).encode("utf-8")
        ).hexdigest()

    def simple_dict(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "arpakit_lib_modules": [arpakit_lib_module.simple_dict() for arpakit_lib_module in self.arpakit_lib_modules]
        }

    def module_name_to_module_simple_dict(self) -> dict[str, dict]:
        return {module.module_name: module.simple_dict() for module in self.arpakit_lib_modules}

    def module_name_to_module_version(self) -> dict[str, str]:
        return {module.module_name: module.module_version for module in self.arpakit_lib_modules}

    def module_name_to_module_version_and_module_has_errors(self) -> dict[str, dict[str, Any]]:
        return {
            module.module_name: {
                "module_version": module.module_version,
                "module_has_errors": module.module_has_error,
            } for module in self.arpakit_lib_modules
        }

    def module_names_who_has_errors(self) -> list[str]:
        return [
            arpakit_lib_module.module_name
            for arpakit_lib_module in self.arpakit_lib_modules
            if arpakit_lib_module.module_has_error
        ]

    def have_modules_with_error(self) -> bool:
        for arpakit_lib_module in self.arpakit_lib_modules:
            if arpakit_lib_module.module_has_error:
                return True
        return False

    def module_name_to_module_exception(self, *, filter_module_has_error: bool = False) -> dict[str, Exception]:
        if filter_module_has_error:
            return {
                module.module_name: module.module_exception
                for module in self.arpakit_lib_modules if module.module_has_error
            }
        else:
            return {
                module.module_name: module.module_exception
                for module in self.arpakit_lib_modules
            }

    def module_name_to_module_hash(self) -> dict[str, str]:
        return {module.module_name: module.module_hash for module in self.arpakit_lib_modules}

    def module_name_to_module_content(self) -> dict[str, str]:
        return {module.module_name: module.module_content for module in self.arpakit_lib_modules}


def get_arpakit_lib_modules() -> ArpakitLibModules:
    base_dirpath: str = str(pathlib.Path(__file__).parent)

    filenames: list[str] = os.listdir(base_dirpath)
    filenames.sort()

    arpakit_lib_modules = ArpakitLibModules(arpakit_lib_modules=[])

    for filename in filenames:
        if not filename.endswith(".py") or filename == "__init__.py":
            continue
        module_name = filename.replace(".py", "")
        module_version: Optional[str] = None
        try:
            spec = spec_from_file_location(module_name, os.path.join(base_dirpath, filename))
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            module_version = getattr(module, "_ARPAKIT_LIB_MODULE_VERSION", None)
            module_has_error = False
            module_exception = None
        except Exception as error:
            module_has_error = True
            module_exception = error
        if module_version is not None and not isinstance(module_version, str):
            continue
        if module_name in [
            arpakit_lib_module.module_name for arpakit_lib_module in arpakit_lib_modules.arpakit_lib_modules
        ]:
            raise KeyError(f"module_name {module_name} is duplicated")
        module_content = open(file=os.path.join(base_dirpath, filename), mode="r").read().strip()
        module_hash = hashlib.sha256(module_content.encode('utf-8')).hexdigest()
        arpakit_lib_modules.arpakit_lib_modules.append(ArpakitLibModule(
            module_name=module_name,
            module_version=module_version,
            module_content=module_content,
            module_hash=module_hash,
            module_has_error=module_has_error,
            module_exception=module_exception,
            filename=filename,
            filepath=os.path.join(base_dirpath, filename)
        ))

    return arpakit_lib_modules


def __example():
    for module_name, d in (
            get_arpakit_lib_modules().module_name_to_module_version_and_module_has_errors().items()
    ):
        print(module_name)
        print(d)
        print()
    print("have_modules_with_error", get_arpakit_lib_modules().have_modules_with_error())


if __name__ == '__main__':
    __example()
