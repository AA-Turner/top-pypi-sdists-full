import asyncio
import pandas as pd
from flowtask.components.tFilter import tFilter


async def test_filter_equal_str():
    df = pd.DataFrame({
        "column_name": [
            "Apple Pie",
            "Banana Bread",
            "Pear Pie",
            "Cherry Tart",
            "Chocolate Cake",
            "Strawberry Pie",
            "Pineapple Puding"
        ]
    })
    _filter = tFilter(
        operator="&",
        filter=[
            {
                "column": "column_name",
                "value": ["Apple Pie", "Chocolate Cake"],
                "expression": "=="
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component Equal ::')
        result = await comp.run()
        print('Result >', result)

    # repeat the component for equality of strings:
    _filter = tFilter(
        operator="&",
        filter=[
            {
                "column": "column_name",
                "value": "Apple Pie",
                "expression": "=="
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component Equal STR ::')
        result = await comp.run()
        print('Result >', result)

async def test_filter_contains():
    df = pd.DataFrame({
        "column_name": [
            "Apple Pie",
            "Banana Bread",
            "Pear Pie",
            "Cherry Tart",
            "Chocolate Cake",
            "Strawberry Pie",
            "Pineapple Puding"
        ]
    })
    _filter = tFilter(
        operator="&",
        filter=[
            {
                "column": "column_name",
                "value": ["Pie", "Cake"],
                "expression": "contains"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)


async def test_filter_not_contains():
    df = pd.DataFrame({
        "column_name": [
            "Apple Pie",
            "Banana Bread",
            "Pear Pie",
            "Cherry Tart",
            "Chocolate Cake",
            "Strawberry Pie",
            "Pineapple Puding"
        ]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "column_name",
                "value": ["Pie", "Cake"],
                "expression": "not_contains"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)


async def test_filter_regex():
    df = pd.DataFrame({
        "column_name": [
            "Apple Pie",
            "Banana Bread",
            "Pear Pie",
            "Cherry Tart",
            "Chocolate Cake",
            "Strawberry Pie",
            "Pineapple Puding"
        ]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "column_name",
                "value": ".*(Pie|Bread).*",
                "expression": "regex"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)


async def test_filter_not_null():
    df = pd.DataFrame({
        "column_name": [
            "Apple Pie",
            None,
            "Pear Pie",
            "Cherry Tart",
            "",
            "Strawberry Pie",
            "Pineapple Puding"
        ]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "column_name",
                "expression": "not_null"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)

async def test_filter_not_equal():
    df = pd.DataFrame({
        "column_name": ["Apple Pie", "Banana Bread", "Pear Pie", "Cherry Tart"],
        "value": [10, 20, 15, 30]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "column_name",
                "value": ["Banana Bread"],
                "expression": "!="
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)

async def test_filter_equal():
    df = pd.DataFrame({
        "column_name": ["Apple Pie", "Banana Bread", "Pear Pie", "Cherry Tart"],
        "value": [10, 20, 15, 30]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "value",
                "value": [20],
                "expression": "=="
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)


async def test_filter_greater_than():
    df = pd.DataFrame({
        "column_name": ["Apple Pie", "Banana Bread", "Pear Pie", "Cherry Tart"],
        "value": [10, 20, 15, 30]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "value",
                "value": 15,
                "expression": ">"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)


async def test_filter_lesser_than():
    df = pd.DataFrame({
        "column_name": ["Apple Pie", "Banana Bread", "Pear Pie", "Cherry Tart"],
        "value": [10, 20, 15, 30]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "value",
                "value": 20,
                "expression": "<"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Result >', result)


async def test_filter_invalid_emails():
    # Apply regex to find invalid email formats
    df = pd.DataFrame({
        "email": [
            "valid.email@example.com",
            "invalid-email",
            "another.valid+email@domain.org",
            "missing-at-sign.com",
            "valid.email+alias@sub.domain.co",
            "@missing-username.com",
            "plainaddress",
            "valid@domain.com"
        ]
    })
    _filter = tFilter(
        filter=[
            {
                "column": "email",
                "value": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                "expression": "regex"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component for Valid Emails ::')
        result = await comp.run()
        print('Rows matching valid email regex >', result)

    # Invert the regex to find invalid emails
    _filter_invalid = tFilter(
        filter=[
            {
                "column": "email",
                "value": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                "expression": "not_regex"
            }
        ],
        input=df
    )
    async with _filter_invalid as comp_invalid:
        print(':: Starting Component for Invalid Emails ::')
        result_invalid = await comp_invalid.run()
        print(
            'Rows NOT matching valid email regex >', result_invalid
        )

async def test_filter_not_starts():
    df = pd.DataFrame({
        "first_name": ["John", "Jane", "Bob", "Alice", "http://example.com", "https://example.com"],
    })
    print(df)
    _filter = tFilter(
        filter=[
            {
                "column": "first_name",
                "value": ["http", "https"],
                "expression": "not_startswith"
            }
        ],
        input=df
    )
    async with _filter as comp:
        print(':: Starting Component ::')
        result = await comp.run()
        print('Rows Matching >', result)


if __name__ == '__main__':
    asyncio.run(test_filter_equal_str())
    asyncio.run(test_filter_contains())
    asyncio.run(test_filter_not_contains())
    asyncio.run(test_filter_regex())
    asyncio.run(test_filter_not_null())
    asyncio.run(test_filter_not_equal())
    asyncio.run(test_filter_equal())
    asyncio.run(test_filter_greater_than())
    asyncio.run(test_filter_lesser_than())
    asyncio.run(test_filter_invalid_emails())
    asyncio.run(test_filter_not_starts())
