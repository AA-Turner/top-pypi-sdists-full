# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1l1111ll_opy_ import bstack1lll1111111l_opy_
class bstack1lll1llllll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1ll1ll1lll11_opy_=None, bstack1ll1ll1l11l1_opy_=True, finished_at=None, bstack1l1ll111l_opy_=None, result=None, duration=None, bstack1llll1l1111_opy_=None, meta={}):
        self.bstack1llll1l1111_opy_ = bstack1llll1l1111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1ll1l11l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1ll1lll11_opy_ = bstack1ll1ll1lll11_opy_
        self.finished_at = finished_at
        self.bstack1l1ll111l_opy_ = bstack1l1ll111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llll1l1l11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lllll111ll_opy_(self, meta):
        self.meta = meta
    def bstack1llll1lll1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1ll1ll1ll_opy_(self):
        bstack1ll1ll1l1l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ┓"): bstack1ll1ll1l1l1l_opy_,
            bstack1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ└"): bstack1ll1ll1l1l1l_opy_,
            bstack1ll11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭┕"): bstack1ll1ll1l1l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll11_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ┖") + key)
            setattr(self, key, val)
    def bstack1ll1ll1l11ll_opy_(self):
        return {
            bstack1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ┗"): self.name,
            bstack1ll11_opy_ (u"ࠫࡧࡵࡤࡺࠩ┘"): {
                bstack1ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ┙"): bstack1ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭┚"),
                bstack1ll11_opy_ (u"ࠧࡤࡱࡧࡩࠬ┛"): self.code
            },
            bstack1ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ├"): self.scope,
            bstack1ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ┝"): self.tags,
            bstack1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭┞"): self.framework,
            bstack1ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ┟"): self.started_at
        }
    def bstack1ll1ll1l1ll1_opy_(self):
        return {
         bstack1ll11_opy_ (u"ࠬࡳࡥࡵࡣࠪ┠"): self.meta
        }
    def bstack1ll1ll1lllll_opy_(self):
        return {
            bstack1ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ┡"): {
                bstack1ll11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ┢"): self.bstack1ll1ll1lll11_opy_
            }
        }
    def bstack1ll1ll1llll1_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1ll11_opy_ (u"ࠨ࡫ࡧࠫ┣")] == sid, self.meta[bstack1ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ┤")]), None)
        step.update(details)
    def bstack1ll11lll11_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1ll11_opy_ (u"ࠪ࡭ࡩ࠭┥")] == sid, self.meta[bstack1ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ┦")]), None)
        step.update({
            bstack1ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ┧"): current_time()
        })
    def bstack1lllll11lll_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ┨")):
            step = next(filter(lambda st: st[bstack1ll11_opy_ (u"ࠧࡪࡦࠪ┩")] == sid, self.meta[bstack1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ┪")]), None)
            step.update({
                bstack1ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ┫"): finished_at,
                bstack1ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ┬"): duration if duration else time_diff(step[bstack1ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ┭")], finished_at),
                bstack1ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ┮"): result.result,
                bstack1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ┯"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1ll1ll111_opy_):
        if self.meta.get(bstack1ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭┰")):
            self.meta[bstack1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ┱")].append(bstack1ll1ll1ll111_opy_)
        else:
            self.meta[bstack1ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ┲")] = [ bstack1ll1ll1ll111_opy_ ]
    def bstack1ll1ll1ll1l1_opy_(self):
        return {
            bstack1ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ┳"): self.bstack1llll1l1l11_opy_(),
            bstack1ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ┴"): bstack1ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭┵"),
            **self.bstack1ll1ll1l11ll_opy_(),
            **self.bstack1ll1ll1ll1ll_opy_(),
            **self.bstack1ll1ll1l1ll1_opy_()
        }
    def bstack1ll1ll1l1lll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ┶"): self.finished_at,
            bstack1ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ┷"): self.duration,
            bstack1ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ┸"): self.result.result
        }
        if data[bstack1ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ┹")] == bstack1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ┺"):
            data[bstack1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ┻")] = self.result.bstack1ll1lll111l_opy_()
            data[bstack1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭┼")] = [{bstack1ll11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ┽"): self.result.bstack1111l11llll_opy_()}]
        return data
    def bstack1ll1ll1ll11l_opy_(self):
        return {
            bstack1ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┾"): self.bstack1llll1l1l11_opy_(),
            **self.bstack1ll1ll1l11ll_opy_(),
            **self.bstack1ll1ll1ll1ll_opy_(),
            **self.bstack1ll1ll1l1lll_opy_(),
            **self.bstack1ll1ll1l1ll1_opy_()
        }
    def bstack1llll1l1lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll11_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ┿") in event:
            return self.bstack1ll1ll1ll1l1_opy_()
        elif bstack1ll11_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ╀") in event:
            return self.bstack1ll1ll1ll11l_opy_()
    def bstack1llll1l1l1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack1lll1llllll_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1ll111l_opy_=bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࠨ╁"))
    @classmethod
    def bstack1ll1ll1lll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll11_opy_ (u"ࠫ࡮ࡪࠧ╂"): id(step),
                bstack1ll11_opy_ (u"ࠬࡺࡥࡹࡶࠪ╃"): step.name,
                bstack1ll11_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ╄"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1ll11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ╅"): {
                    bstack1ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭╆"): feature.name,
                    bstack1ll11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ╇"): feature.filename,
                    bstack1ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ╈"): feature.description
                },
                bstack1ll11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭╉"): {
                    bstack1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ╊"): scenario.name
                },
                bstack1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ╋"): steps,
                bstack1ll11_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ╌"): bstack1lll1111111l_opy_(test)
            }
        )
    def bstack1ll1ll1l1111_opy_(self):
        return {
            bstack1ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ╍"): self.hooks
        }
    def bstack1ll1ll1l1l11_opy_(self):
        if self.integrations:
            return {
                bstack1ll11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ╎"): self.integrations
            }
        return {}
    def bstack1ll1ll1ll11l_opy_(self):
        return {
            **super().bstack1ll1ll1ll11l_opy_(),
            **self.bstack1ll1ll1l1111_opy_()
        }
    def bstack1ll1ll1ll1l1_opy_(self):
        return {
            **super().bstack1ll1ll1ll1l1_opy_(),
            **self.bstack1ll1ll1l1l11_opy_()
        }
    def bstack1llll1l1l1l_opy_(self):
        return bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ╏")
class bstack1lllll111l1_opy_(bstack1lll1llllll_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l11l1ll111_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1ll111l_opy_=bstack1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ═"))
    def bstack1llll1ll11l_opy_(self):
        return self.hook_type
    def bstack1ll1ll1l111l_opy_(self):
        return {
            bstack1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ║"): self.hook_type
        }
    def bstack1ll1ll1ll11l_opy_(self):
        return {
            **super().bstack1ll1ll1ll11l_opy_(),
            **self.bstack1ll1ll1l111l_opy_()
        }
    def bstack1ll1ll1ll1l1_opy_(self):
        return {
            **super().bstack1ll1ll1ll1l1_opy_(),
            bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ╒"): self.bstack1l11l1ll111_opy_,
            **self.bstack1ll1ll1l111l_opy_()
        }
    def bstack1llll1l1l1l_opy_(self):
        return bstack1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ╓")
    def bstack1llll1ll1ll_opy_(self, bstack1l11l1ll111_opy_):
        self.bstack1l11l1ll111_opy_ = bstack1l11l1ll111_opy_