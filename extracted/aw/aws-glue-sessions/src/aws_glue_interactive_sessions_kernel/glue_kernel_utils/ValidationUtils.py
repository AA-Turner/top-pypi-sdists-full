
def convert_list_to_string(array_list):
    if not array_list:
        return None
    try:
        line = array_list.strip("[]")
        value_list = line.split(",")
        # create new list and strip leading and trailing spaces
        values = []
        for val in list(value_list):
            next_val = str(val).strip()
            if not next_val:
                return None
            elif " " in next_val:
                if "--" in next_val:
                    pass
                else:
                    return None
            values.append(next_val)
    except Exception as e:
        return None
    return ",".join(values)
