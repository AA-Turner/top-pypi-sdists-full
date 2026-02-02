def get_next_highest_power_of_2(value: int) -> int:
    return 1 << (value - 1).bit_length()
