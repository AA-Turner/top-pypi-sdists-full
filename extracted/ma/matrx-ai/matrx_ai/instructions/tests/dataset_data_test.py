import json
from typing import Any, Literal

from matrx_utils import clear_terminal, vcprint
from matrx_ai.db._registry import get_model

UdtDatasetRows = get_model("UdtDatasetRows")


def get_table_data(table_id: str) -> list[dict[str, Any]]:
    full_table_data = UdtDatasetRows.filter(table_id=table_id).values_list_sync(
        "data", flat=True
    )
    parsed_data = [
        json.loads(row) if isinstance(row, str) else row for row in full_table_data
    ]
    return parsed_data


def get_table_row_data(row_id: str) -> dict[str, Any]:
    row_data = UdtDatasetRows.filter_sync(id=row_id)
    data = row_data[0].data
    parsed_data = json.loads(data) if isinstance(data, str) else data

    return parsed_data


def get_table_cell_data(row_id: str, column_name: str) -> Any:
    row_data = get_table_row_data(row_id)
    data = row_data.get(column_name)
    return data


def filter_table_data_by_row_value(
    table_id: str, filter_key: str, filter_value: str
) -> list[dict[str, Any]]:
    full_table_data = get_table_data(table_id)
    vcprint(full_table_data, "Full Table Data", color="blue")
    filtered_table_data = [
        row for row in full_table_data if row[filter_key] == filter_value
    ]
    return filtered_table_data


def filter_table_data_by_column_name(table_id: str, filter_key: str) -> list[Any]:
    full_table_data = get_table_data(table_id)
    filtered_table_data = [row.get(filter_key) for row in full_table_data]
    for row in filtered_table_data:
        print("--------------------------------")
        print(row)
        print("--------------------------------")

    return filtered_table_data


def sample_exercises() -> list[dict[str, Any]]:
    table_id = "274f7555-c6b0-4dac-b21b-3770d89cb10f"
    column = "Exercise"
    value = "Dumbbell Shoulder Press"
    filtered_table_data = filter_table_data_by_row_value(table_id, column, value)

    return filtered_table_data


def sample_research() -> list[dict[str, Any]]:
    full_table_data = get_table_data("c0b129d4-12bb-435d-8157-3e9da7659ad7")

    vcprint(full_table_data, "Full Table Data", color="blue")

    return full_table_data


def sample_research_findings_summary() -> list[Any]:
    table_id = "c0b129d4-12bb-435d-8157-3e9da7659ad7"
    column_name = "research_findings_summary"
    filtered_table_data = filter_table_data_by_column_name(table_id, column_name)
    return filtered_table_data


sample_cell_reference: dict[str, Any] = {
    "type": "table_cell",
    "table_id": "c0b129d4-12bb-435d-8157-3e9da7659ad7",
    "table_name": "CIC Research",
    "row_id": "de9d2ebf-7d76-4dc4-b435-b1788cad5f9f",
    "column_name": "research_findings_summary",
    "column_display_name": "Research Findings Summary",
    "description": 'Reference to cell "Research Findings Summary" in row de9d2ebf-7d76-4dc4-b435-b1788cad5f9f of table "CIC Research"',
}

sample_bookmark_2: dict[str, Any] = {
    "type": "table_cell",
    "table_id": "bd23d097-9b8e-45d5-b651-de5d32a68134",
    "table_name": "Ellie Workout Progress",
    "row_id": "257cc431-965b-46e3-af72-5e97c7a9e662",
    "column_name": "Exercise",
    "column_display_name": "Exercise",
    "description": 'Reference to cell "Exercise" in row 257cc431-965b-46e3-af72-5e97c7a9e662 of table "Ellie Workout Progress"',
}

sample_bookmark_3: dict[str, Any] = {
    "type": "full_table",
    "table_id": "4fa26d5e-9e85-4d0d-8ce8-31fe9d0efb9b",
    "table_name": "CIC Brand Profile",
    "description": 'Reference to entire table "CIC Brand Profile"',
}


def get_data_with_bookmark(
    bookmark: dict[str, Any], item_type: Literal["table", "column", "row", "cell"]
) -> Any:
    if item_type == "cell":
        return get_table_cell_data(bookmark["row_id"], bookmark["column_name"])  # Works
    elif item_type == "row":
        return get_table_row_data(bookmark["row_id"])  # Works
    elif item_type == "column":
        return filter_table_data_by_column_name(
            bookmark["table_id"], bookmark["column_name"]
        )  # Works
    elif item_type == "table":
        return get_table_data(bookmark["table_id"])  # Works
    else:
        raise ValueError(f"Invalid item type: {item_type}")
    return None


if __name__ == "__main__":
    clear_terminal()
    # datasets = UdtDatasets.objects.all()
    # vcprint(datasets, "Datasets", color="blue")
    # rows = UdtDatasetRows.objects.all()
    # vcprint(rows, "Dataset Rows", color="blue")

    # data = sample_exercises()
    # data = sample_research()
    # data = sample_research_findings_summary()
    # full_table_data = asyncio.run(get_table_data())

    # data = get_table_row_data(sample_cell_reference["row_id"])

    # data = get_table_cell_data(
    #     sample_cell_reference["row_id"], sample_cell_reference["column_name"]
    # )

    data = get_data_with_bookmark(sample_bookmark_2, "table")
    vcprint(data, "Data", color="magenta")
