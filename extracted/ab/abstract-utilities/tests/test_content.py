from src.abstract_utilities import *

def main():
    params = {
        'directory': '/run/user/1000/gvfs/sftp:host=192.168.1.100,user=solcatcher/srv/pyit/dev/abstract_utilities/tests/test_content',
        'get_lines': True, 'spec_line': False, 'parse_lines': False,
        'total_strings': False, 'strings': ['test'], 'recursive': True,
        'cfg': ScanConfig(
            allowed_exts={'.py'}, exclude_exts=False, allowed_types=False,
            exclude_types=False, allowed_dirs=False, exclude_dirs=False,
            allowed_patterns=False, exclude_patterns={'lib', 'build'},
        ),
    }
    content = findContent(**params)
    input(content)


if __name__ == '__main__':
    main()
