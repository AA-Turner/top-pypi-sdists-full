import re


class Php:

    def __init__(self):
        self.php_vars_by_file_name = {}

    def get_variable_from_file(self, var_name, file):
        file_lines = ''
        for line in open(file):
            file_lines += line

        if file in self.php_vars_by_file_name:
            php_vars = self.php_vars_by_file_name[file]
        else:
            php_vars = re.findall(r"""^define\(\s*['"]*(.*?)['"]*[\s,]+['"]*(.*?)['"]*\s*\)""",
                                  file_lines,
                                  re.IGNORECASE | re.DOTALL | re.MULTILINE)
            php_vars = dict(php_vars)
            self.php_vars_by_file_name[file] = php_vars

        var_value = ''
        if var_name in php_vars:
            var_value = php_vars[var_name]

        return var_value
