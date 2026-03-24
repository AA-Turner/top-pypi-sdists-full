# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1l11ll111l_opy_ import bstack1lll1111l1ll_opy_
class bstack1llll1l11l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1ll1lll11l11_opy_=None, bstack1ll1lll11l1l_opy_=True, finished_at=None, bstack111111ll11_opy_=None, result=None, duration=None, bstack1llll11l111_opy_=None, meta={}):
        self.bstack1llll11l111_opy_ = bstack1llll11l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1lll11l1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1lll11l11_opy_ = bstack1ll1lll11l11_opy_
        self.finished_at = finished_at
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llll11ll11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lllllll11l_opy_(self, meta):
        self.meta = meta
    def bstack1llllll1lll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1lll11lll_opy_(self):
        bstack1ll1lll1l111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨⓡ"): bstack1ll1lll1l111_opy_,
            bstack1ll1lll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨⓢ"): bstack1ll1lll1l111_opy_,
            bstack1ll1lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬⓣ"): bstack1ll1lll1l111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤⓤ") + key)
            setattr(self, key, val)
    def bstack1ll1ll1llll1_opy_(self):
        return {
            bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧⓥ"): self.name,
            bstack1ll1lll_opy_ (u"ࠪࡦࡴࡪࡹࠨⓦ"): {
                bstack1ll1lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩⓧ"): bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬⓨ"),
                bstack1ll1lll_opy_ (u"࠭ࡣࡰࡦࡨࠫⓩ"): self.code
            },
            bstack1ll1lll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⓪"): self.scope,
            bstack1ll1lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⓫"): self.tags,
            bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⓬"): self.framework,
            bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⓭"): self.started_at
        }
    def bstack1ll1lll111l1_opy_(self):
        return {
         bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ⓮"): self.meta
        }
    def bstack1ll1lll111ll_opy_(self):
        return {
            bstack1ll1lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⓯"): {
                bstack1ll1lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ⓰"): self.bstack1ll1lll11l11_opy_
            }
        }
    def bstack1ll1lll1l11l_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪ⓱")] == sid, self.meta[bstack1ll1lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⓲")]), None)
        step.update(details)
    def bstack1l11ll1111_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1ll1lll_opy_ (u"ࠩ࡬ࡨࠬ⓳")] == sid, self.meta[bstack1ll1lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⓴")]), None)
        step.update({
            bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⓵"): current_time()
        })
    def bstack1lllll1ll11_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⓶")):
            step = next(filter(lambda st: st[bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩ⓷")] == sid, self.meta[bstack1ll1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⓸")]), None)
            step.update({
                bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⓹"): finished_at,
                bstack1ll1lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⓺"): duration if duration else time_diff(step[bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⓻")], finished_at),
                bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⓼"): result.result,
                bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⓽"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1ll1lllll_opy_):
        if self.meta.get(bstack1ll1lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⓾")):
            self.meta[bstack1ll1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⓿")].append(bstack1ll1ll1lllll_opy_)
        else:
            self.meta[bstack1ll1lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ─")] = [ bstack1ll1ll1lllll_opy_ ]
    def bstack1ll1ll1lll1l_opy_(self):
        return {
            bstack1ll1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ━"): self.bstack1llll11ll11_opy_(),
            bstack1ll1lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ│"): bstack1ll1lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ┃"),
            **self.bstack1ll1ll1llll1_opy_(),
            **self.bstack1ll1lll11lll_opy_(),
            **self.bstack1ll1lll111l1_opy_()
        }
    def bstack1ll1ll1lll11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ┄"): self.finished_at,
            bstack1ll1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ┅"): self.duration,
            bstack1ll1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ┆"): self.result.result
        }
        if data[bstack1ll1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ┇")] == bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ┈"):
            data[bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ┉")] = self.result.bstack1ll1llll1ll_opy_()
            data[bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ┊")] = [{bstack1ll1lll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ┋"): self.result.bstack11111111ll1_opy_()}]
        return data
    def bstack1ll1lll11111_opy_(self):
        return {
            bstack1ll1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ┌"): self.bstack1llll11ll11_opy_(),
            **self.bstack1ll1ll1llll1_opy_(),
            **self.bstack1ll1lll11lll_opy_(),
            **self.bstack1ll1ll1lll11_opy_(),
            **self.bstack1ll1lll111l1_opy_()
        }
    def bstack1lll1llll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1lll_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ┍") in event:
            return self.bstack1ll1ll1lll1l_opy_()
        elif bstack1ll1lll_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ┎") in event:
            return self.bstack1ll1lll11111_opy_()
    def bstack1lllll1l111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack1llll1l11l1_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111111ll11_opy_=bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࠧ┏"))
    @classmethod
    def bstack1ll1lll11ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭┐"): id(step),
                bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ┑"): step.name,
                bstack1ll1lll_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭┒"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1ll1lll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ┓"): {
                    bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ└"): feature.name,
                    bstack1ll1lll_opy_ (u"ࠨࡲࡤࡸ࡭࠭┕"): feature.filename,
                    bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ┖"): feature.description
                },
                bstack1ll1lll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ┗"): {
                    bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ┘"): scenario.name
                },
                bstack1ll1lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ┙"): steps,
                bstack1ll1lll_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ┚"): bstack1lll1111l1ll_opy_(test)
            }
        )
    def bstack1ll1ll1ll1ll_opy_(self):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭┛"): self.hooks
        }
    def bstack1ll1lll1l1l1_opy_(self):
        if self.integrations:
            return {
                bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ├"): self.integrations
            }
        return {}
    def bstack1ll1lll11111_opy_(self):
        return {
            **super().bstack1ll1lll11111_opy_(),
            **self.bstack1ll1ll1ll1ll_opy_()
        }
    def bstack1ll1ll1lll1l_opy_(self):
        return {
            **super().bstack1ll1ll1lll1l_opy_(),
            **self.bstack1ll1lll1l1l1_opy_()
        }
    def bstack1lllll1l111_opy_(self):
        return bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ┝")
class bstack1llllll11l1_opy_(bstack1llll1l11l1_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l11ll11ll1_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111111ll11_opy_=bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ┞"))
    def bstack1lllll11l11_opy_(self):
        return self.hook_type
    def bstack1ll1lll1111l_opy_(self):
        return {
            bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ┟"): self.hook_type
        }
    def bstack1ll1lll11111_opy_(self):
        return {
            **super().bstack1ll1lll11111_opy_(),
            **self.bstack1ll1lll1111l_opy_()
        }
    def bstack1ll1ll1lll1l_opy_(self):
        return {
            **super().bstack1ll1ll1lll1l_opy_(),
            bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ┠"): self.bstack1l11ll11ll1_opy_,
            **self.bstack1ll1lll1111l_opy_()
        }
    def bstack1lllll1l111_opy_(self):
        return bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ┡")
    def bstack1lllll1lll1_opy_(self, bstack1l11ll11ll1_opy_):
        self.bstack1l11ll11ll1_opy_ = bstack1l11ll11ll1_opy_