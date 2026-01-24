import os
from pybind11_stubgen import main

for p in os.environ.get("PATH", "").split(";"):
    try:
        os.add_dll_directory(p)
    except:  # noqa: E722
        print(f"Failed adding this dll directory: {p}")
        print("Continuing...")

main()
