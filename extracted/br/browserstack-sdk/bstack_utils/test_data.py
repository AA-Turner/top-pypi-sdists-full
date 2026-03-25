# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack111l1l11l_opy_ import bstack1lll1111l1ll_opy_
class bstack1llll1ll111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1ll1lll111ll_opy_=None, bstack1ll1ll1lll1l_opy_=True, finished_at=None, bstack1l1111111l_opy_=None, result=None, duration=None, bstack1llll1l1l1l_opy_=None, meta={}):
        self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1ll1lll1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1lll111ll_opy_ = bstack1ll1lll111ll_opy_
        self.finished_at = finished_at
        self.bstack1l1111111l_opy_ = bstack1l1111111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llll1llll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llllll111l_opy_(self, meta):
        self.meta = meta
    def bstack1llllll1lll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1lll11111_opy_(self):
        bstack1ll1lll11l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ⓦ"): bstack1ll1lll11l1l_opy_,
            bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ⓧ"): bstack1ll1lll11l1l_opy_,
            bstack1l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪⓨ"): bstack1ll1lll11l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢⓩ") + key)
            setattr(self, key, val)
    def bstack1ll1lll11l11_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⓪"): self.name,
            bstack1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭⓫"): {
                bstack1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⓬"): bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⓭"),
                bstack1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩ⓮"): self.code
            },
            bstack1l1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⓯"): self.scope,
            bstack1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫ⓰"): self.tags,
            bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⓱"): self.framework,
            bstack1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⓲"): self.started_at
        }
    def bstack1ll1lll1l11l_opy_(self):
        return {
         bstack1l1_opy_ (u"ࠩࡰࡩࡹࡧࠧ⓳"): self.meta
        }
    def bstack1ll1ll1lllll_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭⓴"): {
                bstack1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ⓵"): self.bstack1ll1lll111ll_opy_
            }
        }
    def bstack1ll1lll11ll1_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠬ࡯ࡤࠨ⓶")] == sid, self.meta[bstack1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⓷")]), None)
        step.update(details)
    def bstack1lll1ll1_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠧࡪࡦࠪ⓸")] == sid, self.meta[bstack1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⓹")]), None)
        step.update({
            bstack1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⓺"): current_time()
        })
    def bstack1lllll1llll_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⓻")):
            step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠫ࡮ࡪࠧ⓼")] == sid, self.meta[bstack1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⓽")]), None)
            step.update({
                bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⓾"): finished_at,
                bstack1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⓿"): duration if duration else time_diff(step[bstack1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ─")], finished_at),
                bstack1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ━"): result.result,
                bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ│"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1ll1ll1ll_opy_):
        if self.meta.get(bstack1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ┃")):
            self.meta[bstack1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ┄")].append(bstack1ll1ll1ll1ll_opy_)
        else:
            self.meta[bstack1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ┅")] = [ bstack1ll1ll1ll1ll_opy_ ]
    def bstack1ll1lll1l111_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┆"): self.bstack1llll1llll1_opy_(),
            bstack1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ┇"): bstack1l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ┈"),
            **self.bstack1ll1lll11l11_opy_(),
            **self.bstack1ll1lll11111_opy_(),
            **self.bstack1ll1lll1l11l_opy_()
        }
    def bstack1ll1lll111l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ┉"): self.finished_at,
            bstack1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ┊"): self.duration,
            bstack1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ┋"): self.result.result
        }
        if data[bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭┌")] == bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ┍"):
            data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ┎")] = self.result.bstack1ll1llll1ll_opy_()
            data[bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ┏")] = [{bstack1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭┐"): self.result.bstack1111l11l11l_opy_()}]
        return data
    def bstack1ll1lll1111l_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ┑"): self.bstack1llll1llll1_opy_(),
            **self.bstack1ll1lll11l11_opy_(),
            **self.bstack1ll1lll11111_opy_(),
            **self.bstack1ll1lll111l1_opy_(),
            **self.bstack1ll1lll1l11l_opy_()
        }
    def bstack1llll1l1111_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭┒") in event:
            return self.bstack1ll1lll1l111_opy_()
        elif bstack1l1_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ┓") in event:
            return self.bstack1ll1lll1111l_opy_()
    def bstack1lll1llll11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack1llll1ll111_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1111111l_opy_=bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࠬ└"))
    @classmethod
    def bstack1ll1lll11lll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1_opy_ (u"ࠨ࡫ࡧࠫ┕"): id(step),
                bstack1l1_opy_ (u"ࠩࡷࡩࡽࡺࠧ┖"): step.name,
                bstack1l1_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ┗"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1l1_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬ┘"): {
                    bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ┙"): feature.name,
                    bstack1l1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ┚"): feature.filename,
                    bstack1l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ┛"): feature.description
                },
                bstack1l1_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ├"): {
                    bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ┝"): scenario.name
                },
                bstack1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ┞"): steps,
                bstack1l1_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭┟"): bstack1lll1111l1ll_opy_(test)
            }
        )
    def bstack1ll1ll1ll1l1_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ┠"): self.hooks
        }
    def bstack1ll1ll1lll11_opy_(self):
        if self.integrations:
            return {
                bstack1l1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ┡"): self.integrations
            }
        return {}
    def bstack1ll1lll1111l_opy_(self):
        return {
            **super().bstack1ll1lll1111l_opy_(),
            **self.bstack1ll1ll1ll1l1_opy_()
        }
    def bstack1ll1lll1l111_opy_(self):
        return {
            **super().bstack1ll1lll1l111_opy_(),
            **self.bstack1ll1ll1lll11_opy_()
        }
    def bstack1lll1llll11_opy_(self):
        return bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ┢")
class bstack1lllllll11l_opy_(bstack1llll1ll111_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l11ll11ll1_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1111111l_opy_=bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭┣"))
    def bstack1llll1l111l_opy_(self):
        return self.hook_type
    def bstack1ll1ll1llll1_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ┤"): self.hook_type
        }
    def bstack1ll1lll1111l_opy_(self):
        return {
            **super().bstack1ll1lll1111l_opy_(),
            **self.bstack1ll1ll1llll1_opy_()
        }
    def bstack1ll1lll1l111_opy_(self):
        return {
            **super().bstack1ll1lll1l111_opy_(),
            bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ┥"): self.bstack1l11ll11ll1_opy_,
            **self.bstack1ll1ll1llll1_opy_()
        }
    def bstack1lll1llll11_opy_(self):
        return bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭┦")
    def bstack1llllll1ll1_opy_(self, bstack1l11ll11ll1_opy_):
        self.bstack1l11ll11ll1_opy_ = bstack1l11ll11ll1_opy_