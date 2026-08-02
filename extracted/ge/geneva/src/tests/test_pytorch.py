# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# Test data lake works with PyTorch

from pathlib import Path

import lance
import pyarrow as pa

try:
    import lance.torch.data
    import torch
except ImportError:
    import pytest

    pytest.skip("failed to import torch", allow_module_level=True)

from geneva import connect


def test_torch_dataset(tmp_path: Path) -> None:
    db = connect(tmp_path)
    data = pa.Table.from_pydict({"a": [1, 2, 3], "b": [4, 5, 6]})

    tbl = db.create_table("test", data)

    ds = lance.torch.data.LanceDataset(tbl.to_lance(), batch_size=2)

    tensor = next(iter(ds))
    assert torch.equal(tensor["a"], torch.tensor([1, 2]))
    assert torch.equal(tensor["b"], torch.tensor([4, 5]))
