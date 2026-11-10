from steel import Steel

client = Steel()


def main() -> None:
    session = client.sessions.create()
    client.sessions.release(session.id)

    finished = client.sessions.retrieve(session.id)
    print(f"Session {finished.id} is {finished.status} after {finished.duration} ms")

    logs = client.sessions.logs(session.id)
    print(f"{logs.total} log events")
    for event in logs.events[:10]:
        print(f"{event.timestamp} {event.type}")

    cost = client.sessions.cost(session.id)
    print(f"The session cost ${cost.total_cost}")


if __name__ == "__main__":
    main()
