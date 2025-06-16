import xml.etree.ElementTree as ET


class Xml:

    def __init__(self):
        self.xml_by_path = {}

    def get_variable_from_file(self, var_path, var_name, file):
        if file in self.xml_by_path:
            xml_content = self.xml_by_path[file]
        else:
            xml_content = ET.parse(file).getroot()
            self.xml_by_path[file] = xml_content

        var_value = None
        for type_tag in xml_content.findall(var_path):
            var_value = type_tag.get(var_name)

        if var_value is None:
            raise Exception('Var name: {} by path: {} not found.'.format(var_name, var_path))

        return var_value