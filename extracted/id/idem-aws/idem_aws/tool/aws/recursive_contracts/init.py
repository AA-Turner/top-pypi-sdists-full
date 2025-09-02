import asyncio


def post(hub, ctx):
    if asyncio.iscoroutine(ctx.ret):
        return _averify_list(ctx.ret)
    else:
        return _verify_list(ctx.ret)


async def _averify_list(ret):
    return _verify_list(await ret)


def _verify_list(ret):
    if isinstance(ret, dict) and "comment" in ret:
        if isinstance(ret["comment"], tuple):
            ret["comment"] = list(ret["comment"])
        elif isinstance(ret["comment"], str):
            ret["comment"] = [ret["comment"]]
    return ret
