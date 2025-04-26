#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : lifespans
# @Time         : 2024/12/13 10:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from contextlib import asynccontextmanager

from meutils.pipe import *
from meutils.config_utils.manager import ConfigManager


class Resources(BaseModel):
    config_manager: Optional[ConfigManager] = None

    class Config:
        # 允许额外字段，增加灵活性
        extra = 'allow'
        arbitrary_types_allowed = True


# def fake_answer_to_everything_ml_model(x: float):
#     return x * 42
#
#
# ml_models = {}
#
#
# @asynccontextmanager
# async def lifespan(app):
#     # Load the ML model
#     ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
#     yield
#     # Clean up the ML models and release the resources
#     ml_models.clear()


resources = Resources()


@asynccontextmanager
async def nacos_lifespan(app):
    import gc

    logger.debug("Init lifespans")

    config_manager = ConfigManager("test", "testdata")

    resources.config_manager = config_manager

    yield

    # release the resources
    logger.debug("Release the resources")
    del config_manager
    gc.collect()


if __name__ == '__main__':
    from fastapi import FastAPI

    app = FastAPI(lifespan=lifespan)

    app.state.config_manager = ConfigManager("test", "testdata")


    @app.get("/predict")
    async def predict(x: float):
        result = ml_models["answer_to_everything"](x)
        return {"result": result}
