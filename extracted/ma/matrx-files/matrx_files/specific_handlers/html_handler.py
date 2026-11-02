import re
from matrx_files.file_handler import FileHandler


class HtmlHandler(FileHandler):
    def __init__(self, app_name, batch_print=False):
        super().__init__(app_name, batch_print=batch_print)

    # Custom Methods allow for access to any path.
    def custom_read_html(self, path):
        return self.read(path)

    def custom_write_html(self, path, content):
        return self.write(path, content)

    def custom_append_html(self, path, content):
        return self.append(path, content)

    def custom_delete_html(self, path):
        return self.delete(path)

    # Core Methods allow a root, path and possibly other args to be provided
    def read_html(self, root, path):
        return self.read_from_base(root, path)

    def write_html(self, root, path, content, clean=False):
        return self.write_to_base(root, path, content, clean=clean)

    def append_html(self, root, path, content):
        return self.append_to_base(root, path, content)

    def delete_html(self, root, path):
        return self.delete_from_base(root, path)

    def extract_links(self, root, path):
        content = self.read_html(root, path)
        if content:
            return re.findall(r'href=[\'"]?([^\'" >]+)', content)
        return []

    def extract_text(self, root, path):
        content = self.read_html(root, path)
        if content:
            return re.sub(r'<[^>]+>', '', content)
        return ""
