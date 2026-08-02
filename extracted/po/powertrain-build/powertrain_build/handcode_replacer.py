# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Script to replace pragmas in hand written c-code."""

import re
import os
import sys
import shutil

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


class CodeReplacer:
    """Class to replace code in hand written c-code."""

    def replace_line(self, line):
        """Replace line."""
        raise NotImplementedError

    def replace_file(self, file_name):
        """Go through all lines in the file and replace pragmas."""
        tmp_file = file_name + '.tmp'
        with open(file_name, 'r', encoding='ascii', errors='ignore') as old_file:
            with open(tmp_file, 'w', encoding='ascii', errors='ignore') as new_file:
                for line in old_file.readlines():
                    line = self.replace_line(line)
                    new_file.write(line)
        shutil.move(tmp_file, file_name)


class PragmaReplacer(CodeReplacer):
    """Class to replace pragmas in hand written c-code."""

    def __init__(self):
        """Init."""
        self.cvc_started = False
        self.cvc = None
        self.regex = re.compile(r'^\s*#pragma section\s*(CVC(?P<cvc>[a-zA-Z0-9_]*))*\s*$')
        self.template = '#include "CVC_{cvc}_{start_or_end}.h"\n'

    def replace_line(self, line):
        """Replace line (if it has a pragma)."""
        match = self.regex.match(line)
        if match:
            if self.cvc_started:
                line = self.template.format(cvc=self.cvc,
                                            start_or_end='END')
                self.cvc = None
            else:
                self.cvc = match.group('cvc') or 'CODE'
                line = self.template.format(cvc=self.cvc,
                                            start_or_end='START')
            self.cvc_started = not self.cvc_started
        return line


class CodeSwitchReplacer(CodeReplacer):
    """Class to replace code switch includes in hand written c-code."""

    def __init__(self):
        """Init."""
        self.regex = re.compile(r'(.*)SPM_Codeswitch_Setup(_PVC)?(.*)')
        self.template = '{}VcCodeSwDefines{}\n'

    def replace_line(self, line):
        """Replace include code switch file."""
        match = self.regex.match(line)
        if match:
            return self.template.format(match.group(1), match.group(3))
        return line


def update_files(files):
    """Replace code in handwritten file."""
    for file_path in files:
        PragmaReplacer().replace_file(file_path)
        CodeSwitchReplacer().replace_file(file_path)


def update_test_files(files):
    """Replace code in handwritten file."""
    for file_path in files:
        CodeSwitchReplacer().replace_file(file_path)


def get_files_to_update(source_dir_name):
    """Get files to update."""
    files = [os.path.join('./Models/SSPCECD/VcTqReq__DIESEL', source_dir_name, 'invTab2_UInt16_func.c'),
             os.path.join('./Models/SSPCECD/VcCmbNOx__DIESEL', source_dir_name, 'NNEval15x8_func.c'),
             os.path.join('./Models/SSPCECD/VcTqEff__DIESEL', source_dir_name, 'NNEval15x8_func.c')]
    for path, _, filenames in os.walk(os.path.join(REPO_ROOT, 'Models', 'SSPDL')):
        if path.endswith(os.path.join('Mdl', source_dir_name)) or\
                path.endswith(os.path.join('Mdl__denso', source_dir_name)):
            for filename in filenames:
                if (filename.endswith('.c') and not filename.endswith('Mdl.c')) or \
                   (filename.endswith('.h') and not filename.endswith('Mdl.h')):
                    file_path = os.path.relpath(os.path.join(path, filename))
                    files.append(file_path)
    return files


def get_test_files_to_update():
    """Get files to update."""
    files = []
    for path, _, filenames in os.walk(os.path.join(REPO_ROOT, 'Models')):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.relpath(os.path.join(path, filename))
                files.append(file_path)
    return files


def main():
    """Replace incorrect pragmas in handwritten c-code."""
    files_to_update = get_files_to_update('pybuild_src')
    update_files(files_to_update)
    test_files_to_update = get_test_files_to_update()
    update_test_files(test_files_to_update)
    return 0


if __name__ == '__main__':
    sys.exit(main())
