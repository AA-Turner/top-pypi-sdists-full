"""Manual integration test for LinkedIn reaction (LIKE) flow.

Tests the Unipile API directly to verify reactions actually work.

Usage:
    # React to a specific post:
    python3.12 scripts/test_reaction_live.py \
        --account-id YOUR_ACCOUNT_ID \
        --post-id POST_ID_TO_LIKE

    # Auto-discover posts from a user and react to the first one:
    python3.12 scripts/test_reaction_live.py \
        --account-id YOUR_ACCOUNT_ID \
        --fetch-posts-from linkedin_username

Set UNIPILE_API_URL and UNIPILE_API_KEY env vars before running.
"""

from __future__ import annotations

import asyncio
import argparse
import os
import sys

# Add src to path for local imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


async def main() -> None:
    from heylead.linkedin.unipile import UnipileClient

    parser = argparse.ArgumentParser(description="Test LinkedIn reaction via Unipile API")
    parser.add_argument("--account-id", required=True, help="Unipile account ID")
    parser.add_argument("--post-id", default="", help="LinkedIn post ID to react to")
    parser.add_argument(
        "--fetch-posts-from", default="",
        help="LinkedIn username/ID to fetch posts from (auto-discovers post-id)",
    )
    parser.add_argument(
        "--reaction-type", default="LIKE",
        help="Reaction type: LIKE, CELEBRATE, SUPPORT, LOVE, INSIGHTFUL, FUNNY",
    )
    parser.add_argument("--dry-run", action="store_true", help="Fetch posts but don't react")
    args = parser.parse_args()

    url = os.environ.get("UNIPILE_API_URL", "")
    key = os.environ.get("UNIPILE_API_KEY", "")
    if not url or not key:
        print("ERROR: Set UNIPILE_API_URL and UNIPILE_API_KEY environment variables")
        sys.exit(1)

    client = UnipileClient(url, key)

    post_id = args.post_id

    # Auto-discover posts if needed
    if not post_id and args.fetch_posts_from:
        print(f"Fetching posts from '{args.fetch_posts_from}'...")
        try:
            posts_resp = await client.get_user_posts(
                args.account_id, args.fetch_posts_from, limit=5
            )
            posts = posts_resp if isinstance(posts_resp, list) else posts_resp.get("items", [])
        except Exception as e:
            print(f"ERROR fetching posts: {e}")
            await client.close()
            sys.exit(1)

        if not posts:
            print("No posts found for this user.")
            await client.close()
            sys.exit(1)

        print(f"\nFound {len(posts)} posts:")
        for i, p in enumerate(posts):
            text = (p.get("text", "") or p.get("body", ""))[:80]
            print(f"  [{i}] ID: {p.get('id', 'N/A')}")
            print(f"      Text: {text}")
            print()

        post_id = posts[0].get("id", "")
        print(f"Using first post: {post_id}")

    if not post_id:
        print("ERROR: No post_id. Use --post-id or --fetch-posts-from")
        await client.close()
        sys.exit(1)

    if args.dry_run:
        print(f"\nDRY RUN: Would send {args.reaction_type} to post {post_id}")
        await client.close()
        return

    # Send reaction
    print(f"\nSending {args.reaction_type} reaction to post {post_id}...")
    try:
        result = await client.send_post_reaction(
            args.account_id, post_id, args.reaction_type,
        )
    except Exception as e:
        print(f"EXCEPTION: {type(e).__name__}: {e}")
        await client.close()
        sys.exit(1)

    print(f"\nResult: {result}")

    if result.get("success"):
        print("\nSUCCESS: Reaction sent! Check LinkedIn to verify it appears.")
    else:
        print(f"\nFAILED: {result.get('error', 'Unknown error')}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
