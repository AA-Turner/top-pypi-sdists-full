# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11l1ll1ll_opy_, bstack1ll1ll111l1_opy_
from bstack_utils.bstack111111111_opy_ import bstack1ll1l11l11ll_opy_
class bstack1lll11l1ll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l11ll11l_opy_=None, bstack1ll11ll11lll_opy_=True, bstack1ll1ll11l1l_opy_=None, bstack1l1l111l1_opy_=None, result=None, duration=None, bstack1llll1111l1_opy_=None, meta={}):
        self.bstack1llll1111l1_opy_ = bstack1llll1111l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11ll11lll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l11ll11l_opy_ = bstack111l11ll11l_opy_
        self.bstack1ll1ll11l1l_opy_ = bstack1ll1ll11l1l_opy_
        self.bstack1l1l111l1_opy_ = bstack1l1l111l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lll1l11l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1l1lll_opy_(self, meta):
        self.meta = meta
    def bstack1llll11lll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11ll1ll1l_opy_(self):
        bstack1ll11lll111l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⛭"): bstack1ll11lll111l_opy_,
            bstack1ll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⛮"): bstack1ll11lll111l_opy_,
            bstack1ll_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⛯"): bstack1ll11lll111l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣ⛰") + key)
            setattr(self, key, val)
    def bstack1ll11ll1lll1_opy_(self):
        return {
            bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⛱"): self.name,
            bstack1ll_opy_ (u"ࠩࡥࡳࡩࡿࠧ⛲"): {
                bstack1ll_opy_ (u"ࠪࡰࡦࡴࡧࠨ⛳"): bstack1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⛴"),
                bstack1ll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⛵"): self.code
            },
            bstack1ll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⛶"): self.scope,
            bstack1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬ⛷"): self.tags,
            bstack1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⛸"): self.framework,
            bstack1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⛹"): self.started_at
        }
    def bstack1ll11lll1111_opy_(self):
        return {
         bstack1ll_opy_ (u"ࠪࡱࡪࡺࡡࠨ⛺"): self.meta
        }
    def bstack1ll11ll11l1l_opy_(self):
        return {
            bstack1ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ⛻"): {
                bstack1ll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ⛼"): self.bstack111l11ll11l_opy_
            }
        }
    def bstack1ll11ll1l1l1_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1ll_opy_ (u"࠭ࡩࡥࠩ⛽")] == sid, self.meta[bstack1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⛾")]), None)
        step.update(details)
    def bstack1l111ll1l1_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1ll_opy_ (u"ࠨ࡫ࡧࠫ⛿")] == sid, self.meta[bstack1ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✀")]), None)
        step.update({
            bstack1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ✁"): bstack11l1ll1ll_opy_()
        })
    def bstack1llll1l111l_opy_(self, sid, result, duration=None):
        bstack1ll1ll11l1l_opy_ = bstack11l1ll1ll_opy_()
        if sid is not None and self.meta.get(bstack1ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✂")):
            step = next(filter(lambda st: st[bstack1ll_opy_ (u"ࠬ࡯ࡤࠨ✃")] == sid, self.meta[bstack1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ✄")]), None)
            step.update({
                bstack1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ✅"): bstack1ll1ll11l1l_opy_,
                bstack1ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ✆"): duration if duration else bstack1ll1ll111l1_opy_(step[bstack1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭✇")], bstack1ll1ll11l1l_opy_),
                bstack1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ✈"): result.result,
                bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ✉"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11ll1l1ll_opy_):
        if self.meta.get(bstack1ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ✊")):
            self.meta[bstack1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ✋")].append(bstack1ll11ll1l1ll_opy_)
        else:
            self.meta[bstack1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭✌")] = [ bstack1ll11ll1l1ll_opy_ ]
    def bstack1ll11lll11l1_opy_(self):
        return {
            bstack1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭✍"): self.bstack1lll1l11l1l_opy_(),
            bstack1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ✎"): bstack1ll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ✏"),
            **self.bstack1ll11ll1lll1_opy_(),
            **self.bstack1ll11ll1ll1l_opy_(),
            **self.bstack1ll11lll1111_opy_()
        }
    def bstack1ll11ll11ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ✐"): self.bstack1ll1ll11l1l_opy_,
            bstack1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭✑"): self.duration,
            bstack1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭✒"): self.result.result
        }
        if data[bstack1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ✓")] == bstack1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ✔"):
            data[bstack1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ✕")] = self.result.bstack1ll111l1lll_opy_()
            data[bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ✖")] = [{bstack1ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ✗"): self.result.bstack1llllll1ll1l_opy_()}]
        return data
    def bstack1ll11ll1l11l_opy_(self):
        return {
            bstack1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪ✘"): self.bstack1lll1l11l1l_opy_(),
            **self.bstack1ll11ll1lll1_opy_(),
            **self.bstack1ll11ll1ll1l_opy_(),
            **self.bstack1ll11ll11ll1_opy_(),
            **self.bstack1ll11lll1111_opy_()
        }
    def bstack1lll1l1ll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧ✙") in event:
            return self.bstack1ll11lll11l1_opy_()
        elif bstack1ll_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ✚") in event:
            return self.bstack1ll11ll1l11l_opy_()
    def bstack1lll1l1ll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1ll11l1l_opy_ = time if time else bstack11l1ll1ll_opy_()
        self.duration = duration if duration else bstack1ll1ll111l1_opy_(self.started_at, self.bstack1ll1ll11l1l_opy_)
        if result:
            self.result = result
class bstack1llll111l11_opy_(bstack1lll11l1ll1_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1l111l1_opy_=bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹ࠭✛"))
    @classmethod
    def bstack1ll11ll11l11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll_opy_ (u"ࠩ࡬ࡨࠬ✜"): id(step),
                bstack1ll_opy_ (u"ࠪࡸࡪࡾࡴࠨ✝"): step.name,
                bstack1ll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ✞"): step.keyword,
            })
        return bstack1llll111l11_opy_(
            **kwargs,
            meta={
                bstack1ll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭✟"): {
                    bstack1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ✠"): feature.name,
                    bstack1ll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ✡"): feature.filename,
                    bstack1ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭✢"): feature.description
                },
                bstack1ll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ✣"): {
                    bstack1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ✤"): scenario.name
                },
                bstack1ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✥"): steps,
                bstack1ll_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧ✦"): bstack1ll1l11l11ll_opy_(test)
            }
        )
    def bstack1ll11ll1l111_opy_(self):
        return {
            bstack1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ✧"): self.hooks
        }
    def bstack1ll11ll1llll_opy_(self):
        if self.integrations:
            return {
                bstack1ll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭✨"): self.integrations
            }
        return {}
    def bstack1ll11ll1l11l_opy_(self):
        return {
            **super().bstack1ll11ll1l11l_opy_(),
            **self.bstack1ll11ll1l111_opy_(),
            **self.bstack1ll11ll1llll_opy_()
        }
    def bstack1ll11lll11l1_opy_(self):
        return {
            **super().bstack1ll11lll11l1_opy_(),
            **self.bstack1ll11ll1llll_opy_()
        }
    def bstack1lll1l1ll1l_opy_(self):
        return bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ✩")
class bstack1llll1ll111_opy_(bstack1lll11l1ll1_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l111111111_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1l111l1_opy_=bstack1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ✪"))
    def bstack1lll11lll1l_opy_(self):
        return self.hook_type
    def bstack1ll11ll1ll11_opy_(self):
        return {
            bstack1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭✫"): self.hook_type
        }
    def bstack1ll11ll1l11l_opy_(self):
        return {
            **super().bstack1ll11ll1l11l_opy_(),
            **self.bstack1ll11ll1ll11_opy_()
        }
    def bstack1ll11lll11l1_opy_(self):
        return {
            **super().bstack1ll11lll11l1_opy_(),
            bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ✬"): self.bstack1l111111111_opy_,
            **self.bstack1ll11ll1ll11_opy_()
        }
    def bstack1lll1l1ll1l_opy_(self):
        return bstack1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ✭")
    def bstack1llll111l1l_opy_(self, bstack1l111111111_opy_):
        self.bstack1l111111111_opy_ = bstack1l111111111_opy_