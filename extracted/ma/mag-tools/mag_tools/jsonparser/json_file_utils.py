import json
import os

from mag_tools.jsonparser.json_encoder import JsonEncoder


class JsonFileUtils:
    @staticmethod
    def update_params(file_path: str, new_params: dict[str, str]):
        """
            从 JSON 文件中读取参数，替代其中部分参数，并保存回文件
            :param file_path: JSON 文件路径
            :param new_params: 需要更新的参数字典 """

        with open(file_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.update(new_params)

        new_data_str = json.dumps(data, ensure_ascii=False, indent=4, cls=JsonEncoder)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_data_str)

    @staticmethod
    def save_as_json(json_file, data):
        """
        将字典保存为 JSON 文件
        :param data: 数据对象
        :param json_file: JSON文件路径
        """
        filtered_data = JsonFileUtils.__remove_none(data)
        data_str = json.dumps(filtered_data, ensure_ascii=False, indent=4, cls=JsonEncoder)

        # 如果目录不存在，则创建目录
        os.makedirs(os.path.dirname(json_file), exist_ok=True)

        with open(json_file, 'w', encoding='utf-8') as jf:
            jf.write(data_str)

    @staticmethod
    def load_json(json_file) -> dict:
        with open(json_file, encoding='utf-8') as jf:
            data = json.load(jf)
            return data

    @staticmethod
    def load_json_string(json_file) -> str:
        with open(json_file, encoding='utf-8') as jf:
            data = json.load(jf)
            json_str = json.dumps(data, ensure_ascii=False, indent=4, cls=JsonEncoder)
        return json_str

    # 递归过滤掉值为 None 的键
    @staticmethod
    def __remove_none(d):
        if isinstance(d, dict):
            return {k: JsonFileUtils.__remove_none(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return [JsonFileUtils.__remove_none(i) for i in d if i is not None]
        else:
            return d
