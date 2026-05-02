def train_test_split(data, test_size):

    data_count = len(data)

    if isinstance(test_size, float):
        test_count = int(data_count * test_size)
    elif isinstance(test_size, int):
        test_count = test_size
    else:
        test_count = int(data_count * 0.5)

    train_count = data_count - test_count

    train_data = data.iloc[0:train_count, :]
    test_data = data.iloc[train_count:, :]

    return train_data, test_data
