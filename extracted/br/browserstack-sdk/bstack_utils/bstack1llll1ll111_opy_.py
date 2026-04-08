# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lllllllll_opy_, bstack1lll111lll1_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack1ll1l11ll1ll_opy_
class bstack1lll11ll1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1l1l1l11l1l_opy_=None, bstack1ll11lll1111_opy_=True, bstack1ll1l1ll11l_opy_=None, bstack1l1111ll11_opy_=None, result=None, duration=None, bstack1lll1l11111_opy_=None, meta={}):
        self.bstack1lll1l11111_opy_ = bstack1lll1l11111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11lll1111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1l1l1l11l1l_opy_ = bstack1l1l1l11l1l_opy_
        self.bstack1ll1l1ll11l_opy_ = bstack1ll1l1ll11l_opy_
        self.bstack1l1111ll11_opy_ = bstack1l1111ll11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llll111111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll11ll1l_opy_(self, meta):
        self.meta = meta
    def bstack1llll1l11ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11ll1ll11_opy_(self):
        bstack1ll11ll1lll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⛩"): bstack1ll11ll1lll1_opy_,
            bstack111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⛪"): bstack1ll11ll1lll1_opy_,
            bstack111l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⛫"): bstack1ll11ll1lll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111l_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦ⛬") + key)
            setattr(self, key, val)
    def bstack1ll11lll1l1l_opy_(self):
        return {
            bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⛭"): self.name,
            bstack111l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⛮"): {
                bstack111l_opy_ (u"࠭࡬ࡢࡰࡪࠫ⛯"): bstack111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⛰"),
                bstack111l_opy_ (u"ࠨࡥࡲࡨࡪ࠭⛱"): self.code
            },
            bstack111l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⛲"): self.scope,
            bstack111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⛳"): self.tags,
            bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⛴"): self.framework,
            bstack111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⛵"): self.started_at
        }
    def bstack1ll11ll1l1ll_opy_(self):
        return {
         bstack111l_opy_ (u"࠭࡭ࡦࡶࡤࠫ⛶"): self.meta
        }
    def bstack1ll11ll1ll1l_opy_(self):
        return {
            bstack111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⛷"): {
                bstack111l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⛸"): self.bstack1l1l1l11l1l_opy_
            }
        }
    def bstack1ll11lll1lll_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠩ࡬ࡨࠬ⛹")] == sid, self.meta[bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⛺")]), None)
        step.update(details)
    def bstack111l1l1l1l_opy_(self, sid):
        step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠫ࡮ࡪࠧ⛻")] == sid, self.meta[bstack111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⛼")]), None)
        step.update({
            bstack111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⛽"): bstack1lllllllll_opy_()
        })
    def bstack1llll111lll_opy_(self, sid, result, duration=None):
        bstack1ll1l1ll11l_opy_ = bstack1lllllllll_opy_()
        if sid is not None and self.meta.get(bstack111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⛾")):
            step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠨ࡫ࡧࠫ⛿")] == sid, self.meta[bstack111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✀")]), None)
            step.update({
                bstack111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ✁"): bstack1ll1l1ll11l_opy_,
                bstack111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭✂"): duration if duration else bstack1lll111lll1_opy_(step[bstack111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ✃")], bstack1ll1l1ll11l_opy_),
                bstack111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭✄"): result.result,
                bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ✅"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11lll11ll_opy_):
        if self.meta.get(bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✆")):
            self.meta[bstack111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✇")].append(bstack1ll11lll11ll_opy_)
        else:
            self.meta[bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ✈")] = [ bstack1ll11lll11ll_opy_ ]
    def bstack1ll11ll1l1l1_opy_(self):
        return {
            bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ✉"): self.bstack1llll111111_opy_(),
            bstack111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ✊"): bstack111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ✋"),
            **self.bstack1ll11lll1l1l_opy_(),
            **self.bstack1ll11ll1ll11_opy_(),
            **self.bstack1ll11ll1l1ll_opy_()
        }
    def bstack1ll11lll1ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ✌"): self.bstack1ll1l1ll11l_opy_,
            bstack111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ✍"): self.duration,
            bstack111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ✎"): self.result.result
        }
        if data[bstack111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ✏")] == bstack111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ✐"):
            data[bstack111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ✑")] = self.result.bstack1ll111l1l1l_opy_()
            data[bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ✒")] = [{bstack111l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ✓"): self.result.bstack1llllll1ll11_opy_()}]
        return data
    def bstack1ll11llll111_opy_(self):
        return {
            bstack111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭✔"): self.bstack1llll111111_opy_(),
            **self.bstack1ll11lll1l1l_opy_(),
            **self.bstack1ll11ll1ll11_opy_(),
            **self.bstack1ll11lll1ll1_opy_(),
            **self.bstack1ll11ll1l1ll_opy_()
        }
    def bstack1lll1l1l1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111l_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪ✕") in event:
            return self.bstack1ll11ll1l1l1_opy_()
        elif bstack111l_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ✖") in event:
            return self.bstack1ll11llll111_opy_()
    def bstack1lll1llllll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1l1ll11l_opy_ = time if time else bstack1lllllllll_opy_()
        self.duration = duration if duration else bstack1lll111lll1_opy_(self.started_at, self.bstack1ll1l1ll11l_opy_)
        if result:
            self.result = result
class bstack1llll1l1l11_opy_(bstack1lll11ll1ll_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1111ll11_opy_=bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ✗"))
    @classmethod
    def bstack1ll11lll111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l_opy_ (u"ࠬ࡯ࡤࠨ✘"): id(step),
                bstack111l_opy_ (u"࠭ࡴࡦࡺࡷࠫ✙"): step.name,
                bstack111l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ✚"): step.keyword,
            })
        return bstack1llll1l1l11_opy_(
            **kwargs,
            meta={
                bstack111l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ✛"): {
                    bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ✜"): feature.name,
                    bstack111l_opy_ (u"ࠪࡴࡦࡺࡨࠨ✝"): feature.filename,
                    bstack111l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ✞"): feature.description
                },
                bstack111l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ✟"): {
                    bstack111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ✠"): scenario.name
                },
                bstack111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭✡"): steps,
                bstack111l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪ✢"): bstack1ll1l11ll1ll_opy_(test)
            }
        )
    def bstack1ll11lll1l11_opy_(self):
        return {
            bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ✣"): self.hooks
        }
    def bstack1ll11lll11l1_opy_(self):
        if self.integrations:
            return {
                bstack111l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ✤"): self.integrations
            }
        return {}
    def bstack1ll11llll111_opy_(self):
        return {
            **super().bstack1ll11llll111_opy_(),
            **self.bstack1ll11lll1l11_opy_(),
            **self.bstack1ll11lll11l1_opy_()
        }
    def bstack1ll11ll1l1l1_opy_(self):
        return {
            **super().bstack1ll11ll1l1l1_opy_(),
            **self.bstack1ll11lll11l1_opy_()
        }
    def bstack1lll1llllll_opy_(self):
        return bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭✥")
class bstack1llll1l1l1l_opy_(bstack1lll11ll1ll_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack11ll1llllll_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1111ll11_opy_=bstack111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ✦"))
    def bstack1lll1l1l1ll_opy_(self):
        return self.hook_type
    def bstack1ll11ll1llll_opy_(self):
        return {
            bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ✧"): self.hook_type
        }
    def bstack1ll11llll111_opy_(self):
        return {
            **super().bstack1ll11llll111_opy_(),
            **self.bstack1ll11ll1llll_opy_()
        }
    def bstack1ll11ll1l1l1_opy_(self):
        return {
            **super().bstack1ll11ll1l1l1_opy_(),
            bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ✨"): self.bstack11ll1llllll_opy_,
            **self.bstack1ll11ll1llll_opy_()
        }
    def bstack1lll1llllll_opy_(self):
        return bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ✩")
    def bstack1llll11l111_opy_(self, bstack11ll1llllll_opy_):
        self.bstack11ll1llllll_opy_ = bstack11ll1llllll_opy_