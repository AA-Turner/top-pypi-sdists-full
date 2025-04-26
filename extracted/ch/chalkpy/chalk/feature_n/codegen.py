import os
import shutil
from pathlib import Path


def generate_feature_n(n: int, preamble: str) -> str:
    typevars = "\n".join([f"T{str(i)} = TypeVar('T{str(i)}')" for i in range(1, n + 1)])

    all_types = [f"T{str(i)}" for i in range(1, n + 1)]
    all_types_str = ", ".join(all_types)

    cls = f"""


class Features(Generic[{all_types_str}]):
    pass


class DataFrame(Generic[{all_types_str}], metaclass=DataFrameMeta):
    def __getitem__(self, item):
        pass
"""

    return f"{preamble}{typevars}{cls}"


def codegen(num_classes: int):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    codegen_filename = f"{dir_path}/codegen.py".split("cli", 1)[1]
    preamble = f"""# AUTO-GENERATED FILE.
# Re-run {codegen_filename} to regenerate contents.

"""
    for i in range(1, num_classes + 1):
        file_content = generate_feature_n(i, preamble)
        feature_n_dir = f"{dir_path}/feature_{str(i)}/"
        shutil.rmtree(feature_n_dir, ignore_errors=True)
        Path(feature_n_dir).mkdir()
        Path(f"{feature_n_dir}/__init__.py").touch()
        Path(f"{feature_n_dir}/feature.py").write_text(file_content)

    init_text = "\n".join(
        [f"from .feature_{str(i)}.feature import Features as Feature{str(i)}" for i in range(1, num_classes + 1)]
    )
    Path(f"{dir_path}/__init__.py").write_text(f"{preamble}{init_text}")


if __name__ == "__main__":
    codegen(num_classes=256)
