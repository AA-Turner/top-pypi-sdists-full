import re
from matrx_files.file_handler import FileHandler


class MarkdownHandler(FileHandler):
    def __init__(self, app_name, batch_print=False):
        super().__init__(app_name, batch_print=batch_print)
        self.xhtml_output = True

    # Custom Methods
    def custom_read_markdown(self, path):
        return self.read(path)

    def custom_write_markdown(self, path, content):
        return self.write(path, content)

    def custom_append_markdown(self, path, content):
        return self.append(path, content)

    def custom_delete_markdown(self, path):
        return self.delete(path)

    # Core Methods
    def read_markdown(self, root, path):
        return self.read_from_base(root, path)

    def write_markdown(self, root, path, content, clean=True):
        return self.write_to_base(root, path, content, clean=clean)

    def append_markdown(self, root, path, content):
        return self.append_to_base(root, path, content)

    def delete_markdown(self, root, path):
        return self.delete_from_base(root, path)

    # File Type-specific Methods
    def read_lines(self, root, path):
        content = self.read_markdown(root, path)
        return content.split('\n') if content else []

    def write_lines(self, root, path, lines, clean=True):
        content = '\n'.join(lines)
        return self.write_markdown(root, path, content, clean=clean)

    def read_words(self, root, path):
        content = self.read_markdown(root, path)
        return content.split() if content else []

    # Markdown-specific Methods
    def extract_sections(self, root, path):
        content = self.read_markdown(root, path)
        sections = re.split(r'(?m)^# ', content)
        return sections if content else []

    def extract_headers(self, root, path, level=1):
        content = self.read_markdown(root, path)
        if level < 1:
            raise ValueError("Header level must be 1 or greater.")
        header_pattern = f'(?m)^{"#" * level} (.+)$'
        headers = re.findall(header_pattern, content)
        return headers if content else []

    # Configuration for XHTML or HTML Output
    def set_xhtml_output(self, xhtml=True):
        self.xhtml_output = xhtml

    # New methods based on Markdown documentation
    def get_paragraphs(self, root, path):
        content = self.read_markdown(root, path)
        paragraphs = content.split('\n\n') if content else []
        return [para.strip() for para in paragraphs]

    def get_blockquotes(self, root, path):
        content = self.read_markdown(root, path)
        blockquotes = re.findall(r'(?m)^> (.+)', content)
        return blockquotes if content else []

    def get_lists(self, root, path):
        content = self.read_markdown(root, path)
        unordered_list_pattern = r'(?m)^(\*|\+|\-) (.+)$'
        ordered_list_pattern = r'(?m)^\d+\. (.+)$'
        unordered_lists = re.findall(unordered_list_pattern, content)
        ordered_lists = re.findall(ordered_list_pattern, content)
        return {
            "unordered": [item[1] for item in unordered_lists],
            "ordered": ordered_lists} if content else {
            "unordered": [],
            "ordered": []}

    def get_code_blocks(self, root, path):
        content = self.read_markdown(root, path)
        code_blocks = re.findall(r'(?m)^(    |\t)(.+)$', content)
        return [cb[1] for cb in code_blocks] if content else []

    def get_horizontal_rules(self, root, path):
        content = self.read_markdown(root, path)
        horizontal_rule_pattern = r'(?m)^(---|\*\*\*|___)$'
        horizontal_rules = re.findall(horizontal_rule_pattern, content)
        return horizontal_rules if content else []

    def get_links(self, root, path):
        content = self.read_markdown(root, path)
        inline_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        reference_links = re.findall(r'\[([^\]]+)\]: ([^\s]+)', content)
        return {
            "inline": inline_links,
            "reference": reference_links} if content else {
            "inline": [],
            "reference": []}

    def get_images(self, root, path):
        content = self.read_markdown(root, path)
        inline_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        reference_images = re.findall(r'!\[([^\]]*)\]\[([^\]]+)\]', content)
        return {
            "inline": inline_images,
            "reference": reference_images} if content else {
            "inline": [],
            "reference": []}

    def get_automatic_links(self, root, path):
        content = self.read_markdown(root, path)
        auto_links = re.findall(r'<(http[s]?://[^>]+)>', content)
        return auto_links if content else []

    def escape_special_characters(self, text):
        escape_chars = r'\\`*_{}[]()#+-.!'
        escape_pattern = re.compile(f'([{re.escape(escape_chars)}])')
        return escape_pattern.sub(r'\\\1', text)

