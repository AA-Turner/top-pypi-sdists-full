import os
import shutil
from pathlib import Path
from zipfile import ZipFile
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name != 'wheel':
            return

        dicdir = 'ipadic'
        zip_path = os.path.join(dicdir, 'sysdic.zip')
        extract_target = Path("src/janome")

        if os.path.exists(zip_path):
            if os.path.exists('sysdic'):
                shutil.rmtree('sysdic')
            target_sysdic = extract_target / 'sysdic'
            if target_sysdic.exists():
                shutil.rmtree(target_sysdic)
            with ZipFile(zip_path) as zf:
                zf.extractall(extract_target)
            for path in target_sysdic.rglob('*'):
                if path.is_file():
                    rel = path.relative_to('src')
                    build_data.setdefault('force_include', {})[path.as_posix()] = rel.as_posix()
