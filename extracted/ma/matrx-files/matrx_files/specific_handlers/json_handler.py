import json

from matrx_utils import vcprint
from matrx_files.file_handler import FileHandler


class JsonHandler(FileHandler):
    def __init__(self, app_name, batch_print=False):
        super().__init__(app_name, batch_print=batch_print)

    def custom_read_json(self, path):
        content = self.read(path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {path}")
                return None
        return None

    def custom_write_json(self, path, data, clean=True):
        try:
            if clean:
                data = self.clean(data)
            content = json.dumps(data, ensure_ascii=False, indent=4)
            return self.write(path, content)
        except Exception as e:
            print(f"Error encoding JSON for {path}: {str(e)}")
            return False

    def custom_append_json(self, path, data, clean=True):
        existing_data = self.custom_read_json(path) or {}
        existing_data.update(data)
        return self.custom_write_json(path, existing_data, clean=clean)

    def custom_delete_json(self, path):
        return self.delete(path)

    # Core Methods
    def read_json(self, root, path):
        vcprint(f"Triggered with {root} {path}", "Read JSON", verbose=self.verbose, color="yellow")
        content = self.read_from_base(root, path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {path}")
                return None
        return None

    def write_json(self, root, path, data, clean=True, report_errors=True):
        try:
            path = self.ensure_json_extension(path)

            if clean:
                data = self.clean(data)

            content = self._log_and_serialize(data)
            vcprint(content, "Data From Custom Write JSON", pretty=True, verbose=self.debug, color="yellow")

            return self.write_to_base(root, path, content, clean=False)
        except Exception as e:
            vcprint(f"Error encoding JSON for {path}: {str(e)}", color="red")
            return False

    def append_json(self, root, path, data, clean=True):
        existing_data = self.read_json(root, path) or {}
        existing_data.update(data)
        return self.write_json(root, path, existing_data, clean=clean)

    def delete_json(self, root, path):
        return self.delete_from_base(root, path)

    # File Type-specific Methods
    def get_keys(self, root, path):
        data = self.read_json(root, path)
        return list(data.keys()) if data else []

    def get_values(self, root, path):
        data = self.read_json(root, path)
        return list(data.values()) if data else []

    def get_items(self, root, path):
        data = self.read_json(root, path)
        return list(data.items()) if data else []

    def ensure_json_extension(self, path):
        if not path.lower().endswith('.json'):
            return f"{path}.json"
        return path

    def make_serializable(self, data, report_errors=False):
        if isinstance(data, dict):
            return {k: self.make_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.make_serializable(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(self.make_serializable(item) for item in data)
        elif isinstance(data, set):
            return {self.make_serializable(item) for item in data}
        else:
            try:
                json.dumps(data)
                return data
            except (TypeError, OverflowError) as e:
                data_type = type(data).__name__
                if hasattr(data, '__dict__'):
                    attributes = data.__dict__
                else:
                    attributes = str(data)

                if self.debug:
                    vcprint(
                        data=attributes,
                        title=f"Non-serializable data encountered and converted to string. Error: {e}",
                        verbose=self.debug,
                        color="red"
                    )
                else:
                    vcprint(
                        title=f"Non-serializable data of type '{data_type}' encountered. Error: {e}",
                        verbose=report_errors,
                        color="red"
                    )

                return str(data)

    def _log_and_serialize(self, data):
        serializable_data = self.make_serializable(data)
        return json.dumps(serializable_data, ensure_ascii=False, indent=4)
