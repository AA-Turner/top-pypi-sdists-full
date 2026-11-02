from matrx_files.file_handler import FileHandler


class TextHandler(FileHandler):
    def __init__(self, app_name, batch_print=False):
        super().__init__(app_name, batch_print=batch_print)

    # Custom Methods
    def custom_read_text(self, path):
        return self.read(path)

    def custom_write_text(self, path, content):
        return self.write(path, content)

    def custom_append_text(self, path, content):
        return self.append(path, content)

    def custom_delete_text(self, path):
        return self.delete(path)

    # Core Methods
    def read_text(self, root, path):
        return self.read_from_base(root, path)

    def write_text(self, root, path, content, clean=True):
        return self.write_to_base(root, path, content, clean=clean)

    def append_text(self, root, path, content):
        return self.append_to_base(root, path, content)

    def delete_text(self, root, path):
        return self.delete_from_base(root, path)

    # File Type-specific Methods
    def read_lines(self, root, path):
        content = self.read_text(root, path)
        return content.split('\n') if content else []

    def write_lines(self, root, path, lines, clean=True):
        content = '\n'.join(lines)
        return self.write_text(root, path, content, clean=clean)

    def read_words(self, root, path):
        content = self.read_text(root, path)
        return content.split() if content else []
