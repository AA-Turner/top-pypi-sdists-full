import httpx
import pytest
import pytest_asyncio
import concurrent.futures

from mailmanclient.asynclient import AsyncClient
from mailmanclient import Client


if pytest_asyncio.__version__ < '0.17':
    pytest_asyncio.fixture = pytest.fixture


@pytest_asyncio.fixture(autouse=True)
def setup():
    """Setup for testing. Create test data."""
    client = Client('http://localhost:9001/3.1', 'restadmin', 'restpass')
    print('Loading test data...')
    try:
        domain = client.create_domain('example.com')
    except Exception:
        domain = client.get_domain('example.com')
    # Create some lists.
    lists = []
    print('Creating lists...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_id = {
            executor.submit(domain.create_list, f'list{i}'): f'list{i}'
            for i in range(10)}
        for future in concurrent.futures.as_completed(future_to_id):
            lists.append(future.result())

    # Subscribe some addresses.
    print('Creating subscirbers...')
    for i, ml in enumerate(lists):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(
                    ml.subscribe, f'mylist{each}@example.com',
                    pre_verified=True, pre_confirmed=True, pre_approved=True)
                for each in range(i*5)]
            for _future in concurrent.futures.as_completed(futures):
                print('.', end='')
    yield
    # Cleanup after test.
    for ml in lists:
        ml.delete()
    domain.delete()


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient() as conn:
        client = AsyncClient(
            conn, 'http://localhost:9001/3.1', 'restadmin', 'restpass')
        yield client


@pytest.mark.asyncio
async def test_async_client(client):
    domains = await client.domains()
    for each in domains:
        print(f'Domain: {each.mail_host}')


@pytest.mark.asyncio
async def test_get_lists(client):
    lists = await client.lists()
    for ml in lists:
        print(f'Mailinglist: {ml.fqdn_listname}')
        await ml.config()


@pytest.mark.asyncio
async def test_get_members(client):
    members = await client.members()
    for member in members:
        print(f'Member: {member.role} {member.list_id} {member.email} ',
              end='')


@pytest.mark.asyncio
async def test_get_users(client):
    users = await client.users()
    for user in users:
        print(f'User: {user.user_id} ', end='')
        addrs = await user.addresses()
        for addr in addrs:
            print(f'UserAddress: {addr.email}', end='')
        prefs = await user.preferences()
        print('UserPreference: {}'.format(prefs._data), end='')


@pytest.mark.asyncio
async def test_get_addresses(client):
    addresses = await client.addresses()
    for addr in addresses:
        print(f'Address: {addr.email}', end='')
