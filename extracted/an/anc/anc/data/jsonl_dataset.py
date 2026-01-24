import json


class JsonlDataset:
    def __init__(self, filepath, decode_fn=None):
        self.filepath = filepath
        self.data = None
        with open(filepath) as f:
            lines = f.readlines()
            if decode_fn is None:
                self.data = [json.loads(i) for i in lines]
            else:
                self.data = []
                # decode_fn should return a list
                for i in lines:
                    self.data += decode_fn(i)
        assert self.data is not None, f"Invalid jsonl file path {filepath}"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        assert 0 <= idx < len(self.data), f"idx shoud be in [0, {len(self.data)}) but get {idx}"
        return self.data[idx]

    def get_sub_lengths(self, level="file"):
        return [len(self.data)]