import os
from matrx_files.file_manager import FileManager
from datetime import datetime


class CodeHandler(FileManager):
    def __init__(self, batch_print=True, save_direct=False):
        super().__init__("code_generator", batch_print=batch_print)
        self.code_root = "code"
        self.data_root = "data"
        self.reports_root = "reports"
        self.batch_print = batch_print
        self.technologies = {}
        self.tables = {}
        self.code_objects = {}
        self.save_direct = save_direct
        self.verbose = False
        self.session_filename = self._generate_session_filename()

    def print_all_batched(self):
        self.file_handler.print_batch()

    def _generate_session_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.data_root}/json_code_{timestamp}.json"

    def _validate_filename_extension(self, filename):
        if not filename.rsplit(".", 1)[-1]:
            raise ValueError(
                f"Filename '{filename}' must have an extension indicating the file type (e.g., .py, .ts, .js).")

    def add_generated_code(self, code_object):
        self._validate_filename_extension(code_object["filename"])
        file_save_path = code_object["save_path"]
        file_name = code_object["filename"]
        code_subdirectory = f"{self.code_root}/{file_save_path}/{file_name}"
        self.file_handler.write_to_base("temp", code_subdirectory, code_object["code"], clean=False)

        self.append_json(root="temp", path=self.session_filename, data={"generated_code": [code_object]})

    def get_json(self, file_name):
        return self.read("temp", file_name, "json")

    def save_json(self, file_name, data):
        return self.write("temp", file_name, data, "json")

    def write_to_json(self, path, data, root="temp", clean=True):
        return self.write_json(root=root, path=path, data=data, clean=clean)


    def get_list(self, directory, file_type="json"):
        path = f"{directory}"
        return self.list_files("temp", path, file_type)

    def save_code_file(self, file_path, content):
        path = f"{self.code_root}/{file_path}"
        return self.file_handler.write_to_base("temp", path, content, clean=False)

    def save_code_anywhere(self, path, content):
        return self.file_handler.write(path, content, clean=False)

    def read_code_file(self, file_path):
        path = f"{self.code_root}/{file_path}"
        return self.file_handler.read_from_base("temp", path)

    def append_code_file(self, file_path, content):
        path = f"{self.code_root}/{file_path}"
        return self.file_handler.append_to_base("temp", path, content)

    def delete_code_file(self, file_path):
        path = f"{self.code_root}/{file_path}"
        return self.file_handler.delete_from_base("temp", path)

    def code_file_exists(self, file_path):
        path = f"{self.code_root}/{file_path}"
        return self.file_handler._get_full_path("temp", path).exists()

    def generate_and_save_code(self, temp_path, main_code, file_location=None, import_lines=None,
                               additional_top_lines=None, additional_bottom_lines=None, additional_code=None,
                               path=None):
        sections = []
        if file_location:
            sections.append(file_location)
        for section in [import_lines, additional_top_lines, [main_code], additional_code, additional_bottom_lines]:
            if section:
                if isinstance(section, str):
                    section = [section]
                sections.extend(section)
                sections.append('')
        code_content = '\n'.join(sections).strip()

        if self.save_direct:
            self.save_code_anywhere(path, code_content)
        else:
            self.save_code_file(temp_path, code_content)

    def generate_and_save_code_from_object(self, config_obj, main_code, additional_code=None):
        temp_path = config_obj["temp_path"]
        root = config_obj["root"]
        path = os.path.join(root, temp_path)
        file_location = config_obj.get("file_location")
        import_lines = config_obj.get("import_lines")
        additional_top_lines = config_obj.get("additional_top_lines")
        additional_bottom_lines = config_obj.get("additional_bottom_lines")
        self.generate_and_save_code(temp_path, main_code, file_location, import_lines, additional_top_lines,
                                    additional_bottom_lines, additional_code, path)
