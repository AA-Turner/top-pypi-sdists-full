import os


class FileManager:
    """Manager for working with filesystem"""

    def __init__(self):
        pass

    @staticmethod
    def add_info_to_file_header(directories: list, file_extensions: list, info_string: str):
        # todo fix for <?php
        # todo fix for comments for different file types
        log = list()
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.split('.')[-1] in file_extensions:
                        with open(os.path.join(root, file)) as f:
                            original_lines = f.readlines()
                        result_lines = list()
                        if original_lines[0].find(info_string) == -1:
                            result_lines.extend(['/*', info_string, '*/', '\n'])
                        for line in original_lines:
                            result_lines.append(line)
                        result = open(os.path.join(root, file), 'w')
                        result.writelines([item for item in result_lines])
                        result.close()
                        log.append(file)
        return log
