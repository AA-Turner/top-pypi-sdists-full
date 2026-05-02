import asyncio
from flowtask.interfaces.AzureGraph import AzureGraph
from datetime import datetime, timedelta
from flowtask.conf import (
    MS_TEAMS_DEFAULT_TEAMS_ID,
    MS_TEAMS_TENANT_ID,
    MS_TEAMS_CLIENT_ID,
    MS_TEAMS_CLIENT_SECRET,
    TEAMS_USER,
    TEAMS_PASSWORD
)

async def main():
    az = AzureGraph(
        credentials={
            "tenant_id": "O365_TENANT_ID",
            "client_id": "O365_CLIENT_ID",
            "client_secret": "O365_CLIENT_SECRET"
        }
    )
    az.processing_credentials()
    async with az.open() as client:
        users = await client.list_users(
            max_users=10,
            with_photo=True,
            sort_order='desc'
        )
        print('Users > ', len(users), users[0])


async def get_messages():
    az = AzureGraph(
        credentials={
            "tenant_id": "MS_TEAMS_TENANT_ID",
            "client_id": "MS_TEAMS_CLIENT_ID",
            "client_secret": "MS_TEAMS_CLIENT_SECRET"
        }
    )
    az.processing_credentials()
    async with az.open() as client:
        # getting message chats:
        chat = await client.find_chat_by_name(
            'National HA Team Chat'
        )
        print('Chat Id > ', chat)
        messages = await client.get_chat_messages(
            chat_id=chat.id,
            max_messages=50
        )
        print('Messages > ', len(messages), messages[0])


async def get_user_messages(user: str):
    az = AzureGraph(
        credentials={
            "tenant_id": "MS_TEAMS_TENANT_ID",
            "client_id": "MS_TEAMS_CLIENT_ID",
            "client_secret": "MS_TEAMS_CLIENT_SECRET"
        }
    )
    az.processing_credentials()
    async with az.open() as client:
        # getting message chats:
        chats = await client.list_user_chats(
            user
        )
        usr = await client.get_user(user)
        messages = []
        for chat in chats:
            print('CHAT > ', chat, chat.id, chat.topic)
        #     msg = await client.user_chat_messages(
        #         user=usr,
        #         chat_id=chat.id,
        #         start_time=datetime.utcnow() - timedelta(days=60),
        #         end_time=datetime.utcnow(),
        #         max_messages=10
        #     )
        #     messages.extend(msg)
        # # Test
        # print(len(messages), messages[0])
        # for msg in messages:
        #     print(
        #         {
        #             "id": msg.id,
        #             "body": msg.body.content,
        #             "created": f"{msg.created_date_time}"
        #         }
        #     )


async def get_private_chats(user: str, user2: str):
    az = AzureGraph(
        credentials={
            "tenant_id": "MS_TEAMS_TENANT_ID",
            "client_id": "MS_TEAMS_CLIENT_ID",
            "client_secret": "MS_TEAMS_CLIENT_SECRET"
        }
    )
    az.processing_credentials()
    async with az.open() as client:
        chats = await client.find_one_on_one_chat(
            user, user2
        )
        print(chats)

async def list_chat_for_email(target_email: str):
    # 1) Authenticate 
    graph = AzureGraph(
        tenant_id=MS_TEAMS_TENANT_ID,
        client_id=MS_TEAMS_CLIENT_ID,
        client_secret=MS_TEAMS_CLIENT_SECRET,
        user=TEAMS_USER,
        password=TEAMS_PASSWORD
    ).open()

    # 2) Get your objectId
    me = await graph.get_user_info(TEAMS_USER)
    me_id = me.id.lower()

    # 3) Get the objectId of the target email
    other = await graph.get_user_info(target_email)
    other_id = other.id.lower()

    # 4) List only those one-on-one chats
    all_chats = await graph.list_user_chats(me_id)
    # filtering by those chats whose members include other_id
    chats = []
    for c in all_chats:
        if c.chat_type.lower() != "oneOnOne".lower():
            continue
        # getting members
        mems = (await graph._graph.chats.by_chat_id(c.id).members.get()).value
        member_ids = {
            getattr(m, "user_id", None) or getattr(m.user, "id", "")
            for m in mems
        }
        member_ids = {x.lower() for x in member_ids if x}
        if {me_id, other_id} == member_ids:
            chats.append(c)

    if not chats:
        print(f"No chat found with {target_email}")
        return

    print(f"Chats with {target_email}:")
    for chat in chats:
        print(f"\n— Chat ID: {chat.id}\n")
        messages = await graph.get_chat_messages(chat.id, max_messages=10)
        if not messages:
            print("  (no messages)\n")
            continue
        for msg in messages:
            ts     = msg.last_modified_date_time or msg.created_date_time
            author = msg.from_.user.display_name if msg.from_ and msg.from_.user else "System"
            body   = msg.body.content or "<no content>"
            print(f"  [{ts}] {author}: {body}")
        print()

if __name__ == '__main__':
    asyncio.run(list_chat_for_email(
        'jfrruffato@trocglobal.com'
    ))

