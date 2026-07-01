from spec_kitty_tracker import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    InMemoryConnector,
    LinkType,
)


async def test_in_memory_connector_crud_and_events() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    ref = ExternalRef(system="jira", workspace="demo", id="DEMO-1", key="DEMO-1")

    issue = CanonicalIssue(
        ref=ref,
        title="First",
        body="Body",
        status=CanonicalStatus.TODO,
        issue_type=CanonicalIssueType.TASK,
    )

    created = await connector.create_issue(issue)
    assert created.title == "First"

    fetched = await connector.get_issue(ref)
    assert fetched.status == CanonicalStatus.TODO

    updated = await connector.update_issue(
        ref,
        {"title": "Updated", "status": CanonicalStatus.IN_PROGRESS},
        idempotency_key="idempotency-1",
    )
    assert updated.title == "Updated"
    assert updated.status == CanonicalStatus.IN_PROGRESS

    await connector.upsert_link(
        ref,
        CanonicalLink(
            type=LinkType.BLOCKS,
            target=ExternalRef(system="jira", workspace="demo", id="DEMO-2", key="DEMO-2"),
        ),
    )
    await connector.add_comment(ref, "Hello")

    events, _ = await connector.list_events(None, 20)
    assert len(events) >= 4


async def test_in_memory_connector_pagination() -> None:
    connector = InMemoryConnector(name="jira", workspace="demo")
    for idx in range(5):
        await connector.create_issue(
            CanonicalIssue(
                ref=ExternalRef(system="jira", workspace="demo", id=f"I-{idx}", key=f"I-{idx}"),
                title=f"Issue {idx}",
                body=None,
                status=CanonicalStatus.TODO,
                issue_type=CanonicalIssueType.TASK,
            )
        )

    page1 = await connector.list_issues(updated_since=None, cursor=None, limit=2, filters=None)
    assert len(page1.items) == 2
    assert page1.next_cursor is not None

    page2 = await connector.list_issues(
        updated_since=None,
        cursor=page1.next_cursor,
        limit=2,
        filters=None,
    )
    assert len(page2.items) == 2
