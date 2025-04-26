import asyncio
import typing as t
from functools import wraps

F = t.TypeVar("F")


def run_with_asyncio(f: t.Callable[..., t.Coroutine[t.Any, t.Any, F]]) -> t.Callable[..., F]:
    """
    Decorator to convert an asynchronous function into a synchronous function.

    It wraps an async function and runs it using `asyncio.run()`,
    allowing it to be called synchronously. It is useful when you need to use
    async code in a synchronous context, such as command-line tools or scripts.

    Args:
        f (Callable[..., Coroutine[Any, Any, F]]): An asynchronous function.

    Returns:
        Callable[..., F]: A synchronous function that returns the result of the coroutine.

    Example:
        import psycopg

        @run_with_asyncio
        async def get_user(user_id: int) -> dict:
            async with await psycopg.AsyncConnection.connect("dbname=mydb user=myuser") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT id, name FROM users WHERE id = %s", (user_id,))
                    row = await cur.fetchone()
                    return {"id": row[0], "name": row[1]} if row else None

        user = get_user(1)
        print(user)
    """

    @wraps(f)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> F:
        return asyncio.run(f(*args, **kwargs))

    return wrapper
