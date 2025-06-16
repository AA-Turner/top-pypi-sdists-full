from datetime import datetime
import os
import shutil, errno

class FileManager:
    LICENCE = """/**
 * Aheadworks Inc.
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the EULA
 * that is bundled with this package in the file LICENSE.txt.
 * It is also available through the world-wide-web at this URL:
 * https://aheadworks.com/end-user-license-agreement/
 *
 * @package    <PACKAGE_NAME>
 * @version    <VERSION>
 * @copyright  Copyright (c) <COPYRIGHT_YEAR> Aheadworks Inc. (https://aheadworks.com/)
 * @license    https://aheadworks.com/end-user-license-agreement/
 */\n"""

    def remove_files_and_dirs_ignore_case(self, path, files_to_remove, dirs_to_remove):
        for f in os.listdir(path):
            f_path = os.path.join(path, f)
            if os.path.isfile(f_path) and f.lower() in files_to_remove:
                os.remove(f_path)

            if os.path.isdir(f_path) and f.lower() in dirs_to_remove:
                os.system('rm -rf ' + f_path)

    def create_dir_by_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def create_empty_dir(self, path):
        os.system(f"rm -rf {path} && mkdir -p {path}")

    def find_all(self, name, path):
        """ Recoursively find all files in path by name.
        """
        result = []
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        return result

    def add_license_to_php_files(self, path, module_name, version):
        # TODO: check if add_info_to_file_header could do this
        license_text = self.get_legal_header(module_name, version)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".php"):
                    with open(os.path.join(root, file)) as f:
                        original_lines = f.readlines()
                    result_lines = list()
                    if len(original_lines):
                        result_lines.append(original_lines[0])
                        result_lines.append(license_text)
                    else:
                        print(f'WARNING: file {os.path.join(root, file)} is empty')
                    for line in original_lines[1:]:
                        result_lines.append(line)
                    result = open(os.path.join(root, file), 'w')
                    result.writelines([item for item in result_lines])
                    result.close()

    def get_legal_header(self, module_name, version, year=None):
        if not year:
            year = str(datetime.now().year)
        license_text = self.LICENCE.replace("<PACKAGE_NAME>", module_name)
        license_text = license_text.replace("<VERSION>", version)
        license_text = license_text.replace("<COPYRIGHT_YEAR>", year)
        return license_text
