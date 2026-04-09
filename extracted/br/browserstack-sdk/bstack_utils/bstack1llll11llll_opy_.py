# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l1l111l1l_opy_, bstack1ll1l1llll1_opy_
from bstack_utils.bstack11l1111lll_opy_ import bstack1ll1l11llll1_opy_
class bstack1lll1l1l111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l11lll11_opy_=None, bstack1ll11ll1l11l_opy_=True, bstack1ll1lll1lll_opy_=None, bstack1l11l1l1ll_opy_=None, result=None, duration=None, bstack1lll11lll1l_opy_=None, meta={}):
        self.bstack1lll11lll1l_opy_ = bstack1lll11lll1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11ll1l11l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l11lll11_opy_ = bstack111l11lll11_opy_
        self.bstack1ll1lll1lll_opy_ = bstack1ll1lll1lll_opy_
        self.bstack1l11l1l1ll_opy_ = bstack1l11l1l1ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lll1ll1l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1l1lll_opy_(self, meta):
        self.meta = meta
    def bstack1llll1l1l11_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11ll1ll1l_opy_(self):
        bstack1ll11ll1lll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⛪"): bstack1ll11ll1lll1_opy_,
            bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⛫"): bstack1ll11ll1lll1_opy_,
            bstack11ll11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⛬"): bstack1ll11ll1lll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11ll11_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ⛭") + key)
            setattr(self, key, val)
    def bstack1ll11lll1ll1_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⛮"): self.name,
            bstack11ll11_opy_ (u"࠭ࡢࡰࡦࡼࠫ⛯"): {
                bstack11ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⛰"): bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⛱"),
                bstack11ll11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⛲"): self.code
            },
            bstack11ll11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⛳"): self.scope,
            bstack11ll11_opy_ (u"ࠫࡹࡧࡧࡴࠩ⛴"): self.tags,
            bstack11ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⛵"): self.framework,
            bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⛶"): self.started_at
        }
    def bstack1ll11lll1lll_opy_(self):
        return {
         bstack11ll11_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ⛷"): self.meta
        }
    def bstack1ll11ll1l1ll_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ⛸"): {
                bstack11ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭⛹"): self.bstack111l11lll11_opy_
            }
        }
    def bstack1ll11lll111l_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠪ࡭ࡩ࠭⛺")] == sid, self.meta[bstack11ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⛻")]), None)
        step.update(details)
    def bstack11lll1l1_opy_(self, sid):
        step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠬ࡯ࡤࠨ⛼")] == sid, self.meta[bstack11ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⛽")]), None)
        step.update({
            bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⛾"): bstack1l1l111l1l_opy_()
        })
    def bstack1llll1ll11l_opy_(self, sid, result, duration=None):
        bstack1ll1lll1lll_opy_ = bstack1l1l111l1l_opy_()
        if sid is not None and self.meta.get(bstack11ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⛿")):
            step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬ✀")] == sid, self.meta[bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ✁")]), None)
            step.update({
                bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ✂"): bstack1ll1lll1lll_opy_,
                bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ✃"): duration if duration else bstack1ll1l1llll1_opy_(step[bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ✄")], bstack1ll1lll1lll_opy_),
                bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ✅"): result.result,
                bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ✆"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11lll1l11_opy_):
        if self.meta.get(bstack11ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✇")):
            self.meta[bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ✈")].append(bstack1ll11lll1l11_opy_)
        else:
            self.meta[bstack11ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✉")] = [ bstack1ll11lll1l11_opy_ ]
    def bstack1ll11lll11ll_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ✊"): self.bstack1lll1ll1l1l_opy_(),
            bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭✋"): bstack11ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ✌"),
            **self.bstack1ll11lll1ll1_opy_(),
            **self.bstack1ll11ll1ll1l_opy_(),
            **self.bstack1ll11lll1lll_opy_()
        }
    def bstack1ll11lll11l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭✍"): self.bstack1ll1lll1lll_opy_,
            bstack11ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ✎"): self.duration,
            bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ✏"): self.result.result
        }
        if data[bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ✐")] == bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ✑"):
            data[bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ✒")] = self.result.bstack1ll111ll11l_opy_()
            data[bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ✓")] = [{bstack11ll11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ✔"): self.result.bstack1llllll1l1ll_opy_()}]
        return data
    def bstack1ll11ll1llll_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ✕"): self.bstack1lll1ll1l1l_opy_(),
            **self.bstack1ll11lll1ll1_opy_(),
            **self.bstack1ll11ll1ll1l_opy_(),
            **self.bstack1ll11lll11l1_opy_(),
            **self.bstack1ll11lll1lll_opy_()
        }
    def bstack1lll1l11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11ll11_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫ✖") in event:
            return self.bstack1ll11lll11ll_opy_()
        elif bstack11ll11_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭✗") in event:
            return self.bstack1ll11ll1llll_opy_()
    def bstack1lll11ll11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1lll1lll_opy_ = time if time else bstack1l1l111l1l_opy_()
        self.duration = duration if duration else bstack1ll1l1llll1_opy_(self.started_at, self.bstack1ll1lll1lll_opy_)
        if result:
            self.result = result
class bstack1llll1l1l1l_opy_(bstack1lll1l1l111_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l11l1l1ll_opy_=bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪ✘"))
    @classmethod
    def bstack1ll11ll1l1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll11_opy_ (u"࠭ࡩࡥࠩ✙"): id(step),
                bstack11ll11_opy_ (u"ࠧࡵࡧࡻࡸࠬ✚"): step.name,
                bstack11ll11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ✛"): step.keyword,
            })
        return bstack1llll1l1l1l_opy_(
            **kwargs,
            meta={
                bstack11ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ✜"): {
                    bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ✝"): feature.name,
                    bstack11ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩ✞"): feature.filename,
                    bstack11ll11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ✟"): feature.description
                },
                bstack11ll11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ✠"): {
                    bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ✡"): scenario.name
                },
                bstack11ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✢"): steps,
                bstack11ll11_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ✣"): bstack1ll1l11llll1_opy_(test)
            }
        )
    def bstack1ll11lll1111_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ✤"): self.hooks
        }
    def bstack1ll11lll1l1l_opy_(self):
        if self.integrations:
            return {
                bstack11ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ✥"): self.integrations
            }
        return {}
    def bstack1ll11ll1llll_opy_(self):
        return {
            **super().bstack1ll11ll1llll_opy_(),
            **self.bstack1ll11lll1111_opy_(),
            **self.bstack1ll11lll1l1l_opy_()
        }
    def bstack1ll11lll11ll_opy_(self):
        return {
            **super().bstack1ll11lll11ll_opy_(),
            **self.bstack1ll11lll1l1l_opy_()
        }
    def bstack1lll11ll11l_opy_(self):
        return bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ✦")
class bstack1llll1l111l_opy_(bstack1lll1l1l111_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l111l11ll1_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l11l1l1ll_opy_=bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ✧"))
    def bstack1lll1l11ll1_opy_(self):
        return self.hook_type
    def bstack1ll11ll1ll11_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ✨"): self.hook_type
        }
    def bstack1ll11ll1llll_opy_(self):
        return {
            **super().bstack1ll11ll1llll_opy_(),
            **self.bstack1ll11ll1ll11_opy_()
        }
    def bstack1ll11lll11ll_opy_(self):
        return {
            **super().bstack1ll11lll11ll_opy_(),
            bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭✩"): self.bstack1l111l11ll1_opy_,
            **self.bstack1ll11ll1ll11_opy_()
        }
    def bstack1lll11ll11l_opy_(self):
        return bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ✪")
    def bstack1llll1l11l1_opy_(self, bstack1l111l11ll1_opy_):
        self.bstack1l111l11ll1_opy_ = bstack1l111l11ll1_opy_