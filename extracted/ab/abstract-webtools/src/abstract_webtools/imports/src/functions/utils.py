from ..imports import *
def is_cap(string):
    string_lower = string.lower()
    return False if (string == string_lower) else True
def choose_single_or_cap(string,list_objs,reserve_variants):
    string_lower = string.lower()
    is_string_cap = is_cap(string)
    for list_obj in list_objs:
        is_list_obj_cap = is_cap(list_obj)
        list_obj_lower = list_obj.lower()
        if string_lower == list_obj_lower:
            if is_string_cap and is_list_obj_cap:
                return string,reserve_variants
            if is_string_cap and list_obj not in reserve_variants:
                reserve_variants.append(list_obj)
                string = list_obj
            if is_list_obj_cap and string not in reserve_variants:
                reserve_variants.append(string)
            return string,reserve_variants
    return string,reserve_variants
def organize_title_variants(title_variants):
    nu_title_variants = []
    reserve_variants = []
    for i,title_variant in enumerate(title_variants):
        if title_variant not in reserve_variants+nu_title_variants:
            string,reserve_variants = choose_single_or_cap(title_variant,title_variants[i:],reserve_variants)
            nu_title_variants.append(string)
    return nu_title_variants+reserve_variants


