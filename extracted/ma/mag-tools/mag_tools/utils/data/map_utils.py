import json

from mag_tools.utils.data.string_utils import StringUtils


class MapUtils:
    @staticmethod
    def to_property(obj: dict[str, str]):
        return '\n'.join(MapUtils.keypair_to_string((k, v)) for k, v in obj.items())

    @staticmethod
    def keypair_to_string(keypair: tuple[str, str]) -> str:
        return f'{keypair[0]} = {keypair[1]}'

    @staticmethod
    def keys_to_underline(obj: tuple):
        """
        将对象中的键值转换为下划线格式
        """
        if isinstance(obj, dict):
            new_map = {}
            for k, v in obj.items():
                new_map[StringUtils.hump2underline(k)] = MapUtils.keys_to_underline(v)
            obj = new_map
        elif isinstance(obj, list):
            obj = [MapUtils.keys_to_underline(i) for i in obj]
        elif isinstance(obj, tuple):
            obj = MapUtils.keys_to_underline(obj)

        return obj

    @staticmethod
    def keys_to_hump(obj: tuple):
        """
        将对象中的键值转换为驼峰格式
        """
        if isinstance(obj, dict):
            new_map = {}
            for k, v in obj.items():
                new_map[StringUtils.underline2hump(k)] = MapUtils.keys_to_hump(v)
            obj = new_map
        elif isinstance(obj, list):
            obj = [MapUtils.keys_to_hump(i) for i in obj]
        elif isinstance(obj, tuple):
            obj = MapUtils.keys_to_hump(obj)

        return obj

    @staticmethod
    def bytes_to_map(byte_data: bytes):
        str_data = byte_data.decode('utf-8')
        return json.loads(str_data)

if __name__ == '__main__':
    # 示例使用
    _s = '{"code":200,"message":"OK","timestamp":"2025-02-13T18:25:39.843341498","totalCount":1,"data":[{"userSn":1,"secret":null,"hashCount":162706,"salt":"kWmg_tX*JWrL0EK-","makeTime":"2024-07-26T16:03:19","errorCount":0,"nextChangeTime":"2024-10-24T16:03:19"}],"success":true}'
    _map = json.loads(_s)
    print(MapUtils.keys_to_underline(_map))