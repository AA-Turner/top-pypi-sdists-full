# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import uuid

import pyarrow as pa
import pytest

from geneva import connect
from geneva.udfs.embeddings import sentence_transformer_udf
from integ_tests.utils import safe_drop_table


@pytest.mark.skip(reason="Moving to e2e tests, this takes too long")
def test_sentence_transformer_real_model(
    geneva_test_bucket: str,
    standard_cluster,
) -> None:
    db = connect(geneva_test_bucket)
    table_name = f"documents-{uuid.uuid4().hex}"
    table = db.create_table(
        table_name,
        pa.Table.from_pydict(
            {
                "body": [
                    "Hello",
                    None,  # Check null handling
                    "Embeddings let us search",
                    "",
                    " ",
                    "Vectors are great",
                ]
            }
        ),
    )

    try:
        udf = sentence_transformer_udf(
            model="sentence-transformers/all-MiniLM-L6-v2",
            column="body",
            normalize=True,
            trust_remote_code=True,
        )

        table.add_columns({"embedding": udf})
        with standard_cluster:
            table.backfill("embedding", batch_size=2)

        embeddings = table.to_arrow().column("embedding")
        assert embeddings.length() == 6
        first_vector = embeddings[0].as_py()
        assert isinstance(first_vector, list)
        assert all(isinstance(value, float) for value in first_vector)
        # all vectors should be 384 dimensions for this model
        assert all(len(vec) == 384 for vec in embeddings if vec.as_py() is not None)
    finally:
        safe_drop_table(db, table_name)
