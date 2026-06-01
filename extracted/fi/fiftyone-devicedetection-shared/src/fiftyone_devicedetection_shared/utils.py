# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2026 51 Degrees Mobile Experts Limited, Davidson House,
# Forbury Square, Reading, Berkshire, United Kingdom RG1 3EU.
#
# This Original Work is licensed under the European Union Public Licence
# (EUPL) v.1.2 and is subject to its terms as set out below.
#
# If a copy of the EUPL was not distributed with this file, You can obtain
# one at https://opensource.org/licenses/EUPL-1.2.
#
# The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
# amended by the European Commission) shall be deemed incompatible for
# the purposes of the Work and the provisions of the compatibility
# clause in Article 5 of the EUPL shall not apply.
#
# If using the Work as, or as part of, a network application, by
# including the attribution notice(s) required under Article 5 of the EUPL
# in the end user terms of the application under an appropriate heading,
# such notice(s) shall fulfill the requirements of that article.
# *********************************************************************
def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_value_type(value):
    if type(value) is bool:
        value_type = "Boolean"
    elif type(value) is int:
        value_type = "Int32"
    elif type(value) is str:
        value_type = "String"
    elif type(value) is float:
        value_type = "Double"
    elif type(value) is list:
        value_type = "Array"
    elif isinstance(type(value), list):
        value_type = "String[]"
    else:
        value_type = ""
    return value_type

def is_same_type(value, expected_type):
    valueType = get_value_type(value)
    valid = (valueType == expected_type)

    if not valid:
        valid = True if valueType == "String" and expected_type == "JavaScript" else False
    return valid

def get_properties_from_header_file(file_path):
    # Parse header file to get the list of properties
    with open(file_path) as f:
        header = f.readline() \
        .replace(" ", "") \
        .replace("\"", "") \
        .replace("\n", "") \
        .replace("\\", "")  \
        .replace("//", "")
    properties_list = header.split(",")
    return properties_list
