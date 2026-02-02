
# THIS FILE IS GENERATED - DO NOT EDIT #
import sysconfig
from pathlib import Path
from setuptools import setup, Extension
from Cython.Build import cythonize, BuildExecutable
from Cython.Compiler import Options
try:
    from numpy import get_include
except:
    def get_include():
        try:
            return sysconfig.get_config_vars()['CONFINCLUDEPY']
        except KeyError:
            return ''
Options.annotate=False
Options.annotate_coverage_xml=None
Options.buffer_max_dims=8
Options.cache_builtins=True
Options.cimport_from_pyx=False
Options.clear_to_none=True
Options.closure_freelist_size=8
Options.convert_range=True
Options.docstrings=True
Options.embed_pos_in_docstring=False
Options.generate_cleanup_code=False
Options.fast_fail=False
Options.warning_errors=False
Options.error_on_unknown_names=True
Options.error_on_uninitialized=True
Options.gcc_branch_hints=True
Options.lookup_module_cpdef=False
Options.embed=None
ext = cythonize('Aspidites/woma/library.pyx', include_path=[get_include()], quiet=True)
setup(name='Aspidites.woma.library',ext_modules=ext)
if Options.embed: BuildExecutable.build('Aspidites/woma/library.pyx')

