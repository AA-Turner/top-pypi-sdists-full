# ruff: noqa: E501

import textwrap


def dlt_welcome() -> str:
    """Learn about dlthub Assistant features."""
    return textwrap.dedent(
        """\
        Inform the user of the following:
        - You're the "dlthub Assistant" ([learn more](https://dlthub.com/docs/plus/intro));
        - You can teach about dlt, help write pipelines, and explore data;
        - You can manage and configure dlthub projects;
        - You will ask to use tools to access pipelines & data to accurate and up-to-date information;
        - The user can help you by referencing specific documentation or code in their question
        """
    )


def dlt_new_pipeline() -> str:
    """Instructions to create a new dlthub pipeline."""
    return textwrap.dedent(
        """As an intelligent code assistant, follow step-by-step instructions and use the specified tools to build a new dlt pipeline.

        INSTRUCTIONS

        1. Select a dlthub project
            tool: `select_project(<project_dir>)`
        2. View the available source types.
            tool: `available_sources()`
        3. Ask the user what source to add and add it.
            tool: `add_source(<source_name>, <source_type>)`
        4. View the available destinations. For simple local development, suggest destination type `duckdb` or `filesystem`.
            tool: `available_destinations()`
        5. Ask the user what destination to add and add it.
            tool: `add_destination(<desination_name>, <destination_type>)`
        6. Add the pipeline.
            tool: `add_pipeline(<pipeline_name>, <source_name>, <destination_name>)`
        7. Tell the user to do the following:
            1. Configure the source and destination via `dlt.yml` or `.dlt/config.toml`
            2. Edit the file `${dlt_project_root}/sources/${source_name}.py`
        """
    )


def dlt_select_loading_strategy() -> str:
    """Step-by-step process to select the right loading strategy."""
    return textwrap.dedent(
        """Ask the user a series of questions to select the right loading strategy then provide boilerplate code.

        ## Write dispositions
        REPLACE: All data is removed from destination and is replaced by the data from the source.
        APPEND: The data from the source is appended to the destination.
        MERGE: Add new data to the destination and resolve items already present based on `merge_key` or `primary_key`.

        ## Write dispositions questions
        Ask the questions sequentially in a multi-turn conversation to find the appropriate write disposition.

        1. Is the data stateful?
            If NO: use `APPEND`
            ```python
            @dlt.resource(write_disposition="append")
            ```

            If YES: continue

        2. Do you need to track the history of data changes?
            If YES: use `MERGE - SCD2`
            ```python
            # can use a `merge_key` for incremental loading
            @dlt.resource(write_disposition={"disposition": "merge", "strategy": "scd2"})
            ```
            If NO: continue

        3. Can you request the data incrementally / you don't have to load the full dataset?
            If YES: use `MERGE - DELETE-INSERT`
            ```python
            # use a `primary_key` or `merge_key` to deduplicate data
            @dlt.resource(primary_key="id", write_disposition={"disposition": "merge", "strategy": "delete-insert"})
            ```
            If NO: use `REPLACE`
            ```python
            @dlt.resource(write_disposition="replace")
            ```
        """
    )


__prompts__ = (
    dlt_welcome,
    dlt_new_pipeline,
    dlt_select_loading_strategy,
)
