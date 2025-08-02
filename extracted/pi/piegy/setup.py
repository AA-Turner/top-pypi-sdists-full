import subprocess
import sys
import os
import re
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
import platform
import datetime
import textwrap


class BuildSharedLib(build_ext):
    def run(self):
        # Build your shared lib first
        subprocess.check_call(['make', '-C', 'src/piegy/C_core', 'clean', 'so'])
        # Then continue with normal build_ext run
        super().run()

    def build_extension(self, ext):
        if sys.platform == 'win32':
            lib_name = 'piegyc.pyd'
        else:
            lib_name = 'piegyc.so'
        so_path = os.path.abspath(f'src/piegy/C_core/{lib_name}')
        target_path = self.get_ext_fullpath(ext.name)

        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        self.copy_file(so_path, target_path)
        self.rm_duplicate()

    def rm_duplicate(self):
        C_core_path = os.path.abspath(f'src/piegy/C_core')
        so_name = 'piegyc.so'
        if sys.platform == 'win32':
            so_name = 'piegyc.pyd'
        try:
            os.remove(os.path.join(C_core_path, so_name))
        except OSError:
            pass



class AddCompileInfo(build_py):

    def get_version(self):
        version_file = os.path.join('src', 'piegy', '__version__.py')
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # Regex to extract __version__ = '...'
        version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

    def generate_build_info(self):
        version = self.get_version()
        build_info_content = f'''
        """
        Contains build info, whether it's local built, or a pre-compiled wheel.
        Auto-generated at compile time.
        """

        build_info = {{
            "version": "{version}",
            "build date": "{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
            "python used": "{platform.python_version()}",
            "platform": "{sys.platform}"
        }}
        '''
        return textwrap.dedent(build_info_content[1:])
    
    
    def run(self):
        # Write build_info.py directly before building python files
        build_info_path = os.path.abspath(os.path.join('src/piegy/build_info.py'))
        with open(build_info_path, 'w') as f:
            f.write(self.generate_build_info())
        super().run()


# Declare the extension module (empty sources)
ext_modules = [
    Extension('piegy.C_core.piegyc', sources=[])
]

setup(
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildSharedLib, 
              'build_py': AddCompileInfo,},
    package_data={"piegy": ["build_info.py"]},
    include_package_data=True,
)

