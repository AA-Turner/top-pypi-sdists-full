from arpakitlib.ar_json_util import transfer_json_str_to_data_to_json_str


def __command():
    s = input("JSON:\n")
    print(transfer_json_str_to_data_to_json_str(s))


if __name__ == '__main__':
    __command()
