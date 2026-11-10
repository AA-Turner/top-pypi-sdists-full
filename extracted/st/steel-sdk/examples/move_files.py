from steel import Steel

client = Steel()


def main() -> None:
    session = client.sessions.create()

    try:
        uploaded = client.sessions.files.upload(
            session.id,
            file=("hello.txt", b"Hello from my machine\n"),
            path="hello.txt",
        )
        print(f"Uploaded {uploaded.path} ({uploaded.size} bytes)")

        files = client.sessions.files.list(session.id)
        print([entry.path for entry in files.data])

        download = client.sessions.files.download("hello.txt", session_id=session.id)
        print(download.text())
    finally:
        client.sessions.release(session.id)


if __name__ == "__main__":
    main()
