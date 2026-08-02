from agentql.tools.sync_api import query_document


def main():
    QUERY = """
    {
        name
    }
    """
    file_path = "path/to/file.pdf"

    response = query_document(
        file_path,
        query=QUERY,
        timeout=10,
        mode="fast",
    )
    print(f"name: {response['name']}")


if __name__ == "__main__":
    main()
