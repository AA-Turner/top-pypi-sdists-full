from setuptools import setup
from setuptools.command.install import install
import glob
import os
import shutil
import site

class CustomInstallCommand(install):
    """Custom installation command that copies stub files to site-packages root."""

    def run(self):
        # Run the normal installation
        install.run(self)

        # Then copy stub files to the right location
        self.copy_stubs_to_site_packages()

    def copy_stubs_to_site_packages(self):
        """Copy stub files from idapro/stubs to site-packages root."""
        try:
            # Find the target site-packages directory
            target_dir = self.prefix
            if hasattr(self, 'install_purelib'):
                target_dir = self.install_purelib
            elif hasattr(self, 'install_platlib'):
                target_dir = self.install_platlib

            # Fallback to finding site-packages manually
            if not target_dir or not os.path.exists(target_dir):
                site_packages_dirs = site.getsitepackages()
                if hasattr(site, 'getusersitepackages'):
                    site_packages_dirs.append(site.getusersitepackages())

                for sp_dir in site_packages_dirs:
                    if os.path.exists(sp_dir) and os.access(sp_dir, os.W_OK):
                        target_dir = sp_dir
                        break

            if not target_dir:
                print("Warning: Could not find site-packages directory")
                return

            # Find stub files in the installed idapro package
            idapro_dir = os.path.join(target_dir, 'idapro')
            stubs_dir = os.path.join(idapro_dir, 'stubs')

            if not os.path.exists(stubs_dir):
                print("Warning: stubs directory not found")
                return

            # Copy each stub file to site-packages root
            stub_files = glob.glob(os.path.join(stubs_dir, "*.pyi"))
            copied_count = 0

            for stub_file in stub_files:
                stub_name = os.path.basename(stub_file)
                dest_path = os.path.join(target_dir, stub_name)

                try:
                    shutil.copy2(stub_file, dest_path)
                    print(f"Installed stub: {stub_name} -> {dest_path}")
                    copied_count += 1
                except Exception as e:
                    print(f"Failed to copy {stub_name}: {e}")

            if copied_count > 0:
                print(f"✓ Successfully installed {copied_count} IDA Python stub files")
                print("  Restart your IDE to enable autocompletion")

        except Exception as e:
            print(f"Warning: Could not install stub files: {e}")

example_code = "#!/usr/bin/env python3\n\"\"\"\nIDA Pro Python Library Usage Example\nThis example demonstrates how to analyze a binary file using IDA Pro Python library.\n\"\"\"\n\nimport argparse\nimport importlib.metadata\n\n# You need to import first idapro module\nimport idapro\n\n# After idapro module was loaded, you can simply import IDA Python modules\nimport ida_entry\nimport ida_nalt\nimport idaapi\nimport idc\nimport idautils\nimport ida_ida\nimport ida_funcs\nimport ida_name\nimport ida_bytes\nimport ida_typeinf\n\n# Read versions, configured IDA pro kernel and python package\nkern_major, kern_minor, kern_build = idapro.get_library_version()\nidapro_version = importlib.metadata.version('idapro')\nkernel_path = idapro.get_ida_install_dir()\n\n# Parse input arguments\nparser = argparse.ArgumentParser(description=f\"IDA Library usage example, idapro version: {idapro_version}, \"\n    f\"kernel version: {kern_major}.{kern_minor}.{kern_build}, kernel libraries path: {kernel_path}\")\nparser.add_argument(\n    \"-f\",\n    \"--input-file\",\n    help=\"Binary input file to be loaded\",\n    type=str,\n    required=True,\n    default=None\n)\nargs = parser.parse_args()\n\n# Print banner with components versions\nprint(f\"{parser.description}\\n\")\n\n# Open database\nif idapro.open_database(args.input_file, True) == 0:\n    # Extract minimum/maxim addresses\n    min_ea = ida_ida.inf_get_min_ea()\n    max_ea = ida_ida.inf_get_max_ea()\n    print(f\"Addresses range: {hex(min_ea)} - {hex(max_ea)}\")\n\n    # Print entry point\n    entry_point = ida_entry.get_entry_ordinal(0)\n    if entry_point != idaapi.BADADDR:\n        entry_addr = ida_entry.get_entry(entry_point)\n        print(f\"Entry point: {hex(entry_addr)}\")\n\n    # Print some metadata\n    print(f\"Metadata:\")\n    print(f\" path: {idaapi.get_input_file_path()}\")\n    print(f\" module: {idaapi.get_root_filename()}\")\n    print(f\" base: {hex(idaapi.get_imagebase())}\")\n    print(f\" filesize: {hex(ida_nalt.retrieve_input_file_size())}\")\n    print(f\" md5: {ida_nalt.retrieve_input_file_md5()}\")\n    print(f\" sha256: {ida_nalt.retrieve_input_file_sha256()}\")\n    print(f\" crc32: {hex(ida_nalt.retrieve_input_file_crc32())}\")\n\n    # Iterate functions\n    for func_ea in idautils.Functions():\n        f = ida_funcs.get_func(func_ea)\n        print(f\"Function - name {f.name}, start ea {hex(f.start_ea)}, end ea {hex(f.end_ea)}\")\n\n    for seg_ea in idautils.Segments():\n        name = idc.get_segm_name(seg_ea)\n        print(f\"Segment - name {name}\")\n\n    # Iterate types\n    til = ida_typeinf.get_idati()\n    if til:\n      max_ord = ida_typeinf.get_ordinal_limit(til)\n      current_index = -1\n      current_named_type = None\n\n      while current_index < max_ord - 1:\n          current_index += 1\n          tinfo = ida_typeinf.tinfo_t()\n          if tinfo.get_numbered_type(til, current_index):\n              print(f\"Type - id {tinfo.get_tid()}\")\n\n      while True:\n          if current_named_type is None:\n              current_named_type = ida_typeinf.first_named_type(til, ida_typeinf.NTF_TYPE)\n          else:\n              current_named_type = ida_typeinf.next_named_type(til, current_named_type, ida_typeinf.NTF_TYPE)\n\n          if not current_named_type:\n              break\n\n          tinfo = ida_typeinf.tinfo_t()\n          if tinfo.get_named_type(til, current_named_type):\n              print(f\"Type - name {tinfo.get_type_name()}, id {tinfo.get_tid()}\")\n\n    # Iterate comments\n    for ea in idautils.Heads(min_ea, max_ea):\n        cmt = idc.get_cmt(ea, 0)\n        if cmt:\n            print(f\"Comment - value {cmt}\")\n\n    # Iterate strings\n    for s in idautils.Strings():\n        print(f\"String - value {s}\")\n\n    for ea, name in idautils.Names():\n        print(f\"Name - value {name}\")\n\n    # Iterate basic blocks\n    for func_ea in idautils.Functions():\n        func = ida_funcs.get_func(func_ea)\n        if func:\n            fc = idaapi.FlowChart(func)\n            for b in fc:\n                print(f\"Basic block - start ea {hex(b.start_ea)}, end ea {hex(b.end_ea)}\")\n\n    # Iterate binary instructions\n    for ea in idautils.Heads(min_ea, max_ea):\n        if ida_bytes.is_code(ida_bytes.get_flags(ea)):\n            disasm = idc.generate_disasm_line(ea, 0)\n            print(f\"Instruction - ea {hex(ea)}, asm {disasm}\")\n\n    # Close database discarding the changes\n    idapro.close_database(False)"

setup(
    name="idapro",
    version="0.0.8",
    author="Hex-Rays SA",
    author_email="support@hex-rays.com",
    description="IDA Library Python module",
    long_description=f"""
# IDA Library Python Module
The IDA Library Python module enables running IDA Pro as an independent Python package outside the IDA UI environment, allowing for programmatic binary analysis and reverse engineering tasks.

## Prerequisites
### Environment Setup
Set the `IDADIR` environment variable to point to your IDA installation directory:

**Linux/macOS:**
```bash
export IDADIR="/path/to/your/ida/installation"
```

**Windows:**
```cmd
set IDADIR="C:\Program Files\IDA Pro 9.1"
```

**Example paths:**
- **macOS:** `/Applications/IDA Professional 9.1.app/Contents/MacOS/`
- **Windows:** `C:\Program Files\IDA Pro 9.1\`
- **Linux:** `/opt/ida-9.1/`

> **Note:** If you have already installed and configured the `idapro` Python package in the past using script provided with IDA installation package, setting `IDADIR` is not required.

## Usage example:
```python
{example_code}
```

## Type Hints
This package automatically installs type stubs for all IDA Python modules, providing IDE support with autocompletion and type checking for IDA Python modules

Type hints are installed automatically during package installation!

## Troubleshooting
### Common Issues
**ModuleNotFoundError: No module named 'idapro'**
- Ensure `IDADIR` is set correctly
- Verify IDA Pro is properly installed

**License Issues**
- Ensure you have a valid IDA Pro license
- Check that IDA can run normally in GUI mode first

**Type hints not working**
- Restart your IDE after installation
- Check that .pyi files exist in your site-packages directory

## API Reference
For detailed API documentation, refer to:
- IDA Python documentation at https://python.docs.hex-rays.com/
- Built-in help: `help(idapro)` after importing
- IDA Pro SDK documentation https://docs.hex-rays.com/developer-guide/c++-sdk
""",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Disassemblers",
    ],
    python_requires=">=3.8",
    packages=["idapro"],
    package_data={
        "idapro": ["*.py", "py.typed", "stubs/*.pyi"]
    },
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'install': CustomInstallCommand,
    },
)
