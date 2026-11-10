from steel import Steel

client = Steel()


def main() -> None:
    for session in client.sessions.list(status="live"):
        print(f"{session.id} started at {session.created_at}")


if __name__ == "__main__":
    main()
