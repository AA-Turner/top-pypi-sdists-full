#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : database
# @Time         : 2024/11/20 10:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 基础操作 https://mp.weixin.qq.com/s/nbYhmkN05eqnvjGFvzMbXQ

from meutils.pipe import *

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Field, Session, SQLModel, create_engine, select, insert, update

engine = create_async_engine(
    os.getenv("MYSQL_URL"),
    future=True,
    pool_size=64,
    max_overflow=64,
    pool_recycle=3600,
    echo=True,
)


async def create_db_and_tables() -> None:
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        # await conn.run_sync(meta.drop_all) # 清空 慎用
        await conn.run_sync(meta.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


async def get_db():
    async with AsyncSession(engine) as session:
        yield session


async def update_or_insert(entity, filter_kwargs: Optional[dict] = None, update_fn: Optional[Callable] = None,
                           n: int = 1):
    """

    :param entity: TASK 类
    :param filter_kwargs: 查询条件 字典 元组 第一个值是id
    :param update_fn:

        def update_fn(data):
            data.age = 100

    :param n: 轮询次数
    :return:
    """
    if n > 1:  # 一般轮询任务放后台
        for i in range(1, n):
            await asyncio.sleep(n / i, 1)

            logger.debug(f"UPDATE_OR_INSERT: {entity.__name__}-{i}")
            update_flag = await update_or_insert(entity, filter_kwargs, update_fn)
            if update_flag is False:
                logger.debug("提前跳出轮询")
                break

    filter_kwargs = filter_kwargs or {}
    async with AsyncSession(engine) as session:
        statement = select(entity).filter_by(**filter_kwargs)
        result = await session.exec(statement)
        data = result.first()  # result.all()

        if data:  # 主键id查询
            if update_fn:
                logger.debug(f"UPDATE: {data}")

                if inspect.iscoroutinefunction(update_fn):
                    update_flag = await update_fn(data)
                else:
                    update_flag = update_fn(data)

                if update_flag is False: return False  # 跳出轮询

                await session.commit()
                await session.refresh(data)
            return data
        else:
            data = entity(**filter_kwargs)
            logger.debug(f"INSERT: {data}")

            session.add(data)

            await session.commit()
            await session.refresh(data)
            return data


async def select_first(entity, filter_kwargs: Optional[dict] = None):
    async with AsyncSession(engine) as session:
        statement = select(entity).filter_by(**filter_kwargs)

        if result := await session.exec(statement):
            _ = result.first()
            logger.debug(_)
            return _


if __name__ == '__main__':
    pass

    # class Hero(SQLModel, table=True):
    #     id: Optional[int] = Field(default=None, primary_key=True)
    #     name: str
    #     secret_name: str
    #     age: Optional[int] = None
    #
    #
    # hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    # hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    # hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    #
    #
    # async def main():
    #     async with AsyncSession(engine) as session:
    #         session.add(hero_1)
    #         session.add(hero_2)
    #         session.add(hero_3)
    #         await session.commit()
    #
    #
    # # arun(main())
    #
    # arun(create_db_and_tables())

    from meutils.schemas.db.oneapi_types import OneapiTask, OneapiUser, OneapiToken

    # filter_kwargs = {
    #     "task_id": "888",
    # }
    #
    #
    # async def main():
    #     async with AsyncSession(engine) as session:
    #         statement = select(OneapiTask).filter_by(**filter_kwargs)
    #         result = await session.exec(statement)
    #         logger.debug(result)
    #         if result:
    #             logger.debug(result.first())
    #         # await session.commit()
    #
    #
    # arun(update_or_insert(OneapiTask, filter_kwargs))

    filter_kwargs = {
        "id": "1",
    }


    async def main():
        async with AsyncSession(engine) as session:
            # filter_kwargs = {
            #     "id": "1",
            # }
            # statement = select(OneapiUser).filter_by(**filter_kwargs)

            filter_kwargs = {
                "key": "gpoH1z3G6nHovD8MY40i6xx5tsC1vbh7B3Aao2jmejYNoKhv",
            }
            statement = select(OneapiToken).filter_by(**filter_kwargs)

            result = await session.exec(statement)
            if result:
                logger.debug(result.first())
            # await session.commit()


    arun(main())
