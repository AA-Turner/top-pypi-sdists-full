# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack111111l1l_opy_, bstack1ll1ll1l11l_opy_
from bstack_utils.bstack1111ll11_opy_ import bstack1ll1l11l1l1l_opy_
class bstack1lll1llllll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1l1111l_opy_=None, bstack1ll11ll1l1l1_opy_=True, bstack1ll1ll11l11_opy_=None, bstack1111ll11ll_opy_=None, result=None, duration=None, bstack1lll1l1111l_opy_=None, meta={}):
        self.bstack1lll1l1111l_opy_ = bstack1lll1l1111l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11ll1l1l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1l1111l_opy_ = bstack111l1l1111l_opy_
        self.bstack1ll1ll11l11_opy_ = bstack1ll1ll11l11_opy_
        self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lll1ll1l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll111ll1_opy_(self, meta):
        self.meta = meta
    def bstack1llll1l1lll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11ll11l1l_opy_(self):
        bstack1ll11ll1l11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ✆"): bstack1ll11ll1l11l_opy_,
            bstack1l111l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ✇"): bstack1ll11ll1l11l_opy_,
            bstack1l111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ✈"): bstack1ll11ll1l11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l111l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ✉") + key)
            setattr(self, key, val)
    def bstack1ll11ll1ll1l_opy_(self):
        return {
            bstack1l111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ✊"): self.name,
            bstack1l111l_opy_ (u"࠭ࡢࡰࡦࡼࠫ✋"): {
                bstack1l111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ✌"): bstack1l111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ✍"),
                bstack1l111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ✎"): self.code
            },
            bstack1l111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ✏"): self.scope,
            bstack1l111l_opy_ (u"ࠫࡹࡧࡧࡴࠩ✐"): self.tags,
            bstack1l111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ✑"): self.framework,
            bstack1l111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ✒"): self.started_at
        }
    def bstack1ll11ll1ll11_opy_(self):
        return {
         bstack1l111l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ✓"): self.meta
        }
    def bstack1ll11ll111ll_opy_(self):
        return {
            bstack1l111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ✔"): {
                bstack1l111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭✕"): self.bstack111l1l1111l_opy_
            }
        }
    def bstack1ll11ll11l11_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1l111l_opy_ (u"ࠪ࡭ࡩ࠭✖")] == sid, self.meta[bstack1l111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✗")]), None)
        step.update(details)
    def bstack111lll111_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1l111l_opy_ (u"ࠬ࡯ࡤࠨ✘")] == sid, self.meta[bstack1l111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ✙")]), None)
        step.update({
            bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ✚"): bstack111111l1l_opy_()
        })
    def bstack1llll1l1l11_opy_(self, sid, result, duration=None):
        bstack1ll1ll11l11_opy_ = bstack111111l1l_opy_()
        if sid is not None and self.meta.get(bstack1l111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✛")):
            step = next(filter(lambda st: st[bstack1l111l_opy_ (u"ࠩ࡬ࡨࠬ✜")] == sid, self.meta[bstack1l111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ✝")]), None)
            step.update({
                bstack1l111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ✞"): bstack1ll1ll11l11_opy_,
                bstack1l111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ✟"): duration if duration else bstack1ll1ll1l11l_opy_(step[bstack1l111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ✠")], bstack1ll1ll11l11_opy_),
                bstack1l111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ✡"): result.result,
                bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ✢"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11ll11lll_opy_):
        if self.meta.get(bstack1l111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✣")):
            self.meta[bstack1l111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ✤")].append(bstack1ll11ll11lll_opy_)
        else:
            self.meta[bstack1l111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✥")] = [ bstack1ll11ll11lll_opy_ ]
    def bstack1ll11lll1111_opy_(self):
        return {
            bstack1l111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ✦"): self.bstack1lll1ll1l1l_opy_(),
            bstack1l111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭✧"): bstack1l111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ✨"),
            **self.bstack1ll11ll1ll1l_opy_(),
            **self.bstack1ll11ll11l1l_opy_(),
            **self.bstack1ll11ll1ll11_opy_()
        }
    def bstack1ll11ll1l1ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭✩"): self.bstack1ll1ll11l11_opy_,
            bstack1l111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ✪"): self.duration,
            bstack1l111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ✫"): self.result.result
        }
        if data[bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ✬")] == bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ✭"):
            data[bstack1l111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ✮")] = self.result.bstack1ll111l1l1l_opy_()
            data[bstack1l111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ✯")] = [{bstack1l111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ✰"): self.result.bstack1llll1ll1l11_opy_()}]
        return data
    def bstack1ll11ll1lll1_opy_(self):
        return {
            bstack1l111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ✱"): self.bstack1lll1ll1l1l_opy_(),
            **self.bstack1ll11ll1ll1l_opy_(),
            **self.bstack1ll11ll11l1l_opy_(),
            **self.bstack1ll11ll1l1ll_opy_(),
            **self.bstack1ll11ll1ll11_opy_()
        }
    def bstack1lll11l1l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l111l_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫ✲") in event:
            return self.bstack1ll11lll1111_opy_()
        elif bstack1l111l_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭✳") in event:
            return self.bstack1ll11ll1lll1_opy_()
    def bstack1lll1llll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1ll11l11_opy_ = time if time else bstack111111l1l_opy_()
        self.duration = duration if duration else bstack1ll1ll1l11l_opy_(self.started_at, self.bstack1ll1ll11l11_opy_)
        if result:
            self.result = result
class bstack1llll1111l1_opy_(bstack1lll1llllll_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1111ll11ll_opy_=bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࠪ✴"))
    @classmethod
    def bstack1ll11ll11ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l111l_opy_ (u"࠭ࡩࡥࠩ✵"): id(step),
                bstack1l111l_opy_ (u"ࠧࡵࡧࡻࡸࠬ✶"): step.name,
                bstack1l111l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ✷"): step.keyword,
            })
        return bstack1llll1111l1_opy_(
            **kwargs,
            meta={
                bstack1l111l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ✸"): {
                    bstack1l111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ✹"): feature.name,
                    bstack1l111l_opy_ (u"ࠫࡵࡧࡴࡩࠩ✺"): feature.filename,
                    bstack1l111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ✻"): feature.description
                },
                bstack1l111l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ✼"): {
                    bstack1l111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ✽"): scenario.name
                },
                bstack1l111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✾"): steps,
                bstack1l111l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ✿"): bstack1ll1l11l1l1l_opy_(test)
            }
        )
    def bstack1ll11ll111l1_opy_(self):
        return {
            bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ❀"): self.hooks
        }
    def bstack1ll11ll1llll_opy_(self):
        if self.integrations:
            return {
                bstack1l111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ❁"): self.integrations
            }
        return {}
    def bstack1ll11ll1lll1_opy_(self):
        return {
            **super().bstack1ll11ll1lll1_opy_(),
            **self.bstack1ll11ll111l1_opy_(),
            **self.bstack1ll11ll1llll_opy_()
        }
    def bstack1ll11lll1111_opy_(self):
        return {
            **super().bstack1ll11lll1111_opy_(),
            **self.bstack1ll11ll1llll_opy_()
        }
    def bstack1lll1llll1l_opy_(self):
        return bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ❂")
class bstack1llll11l1ll_opy_(bstack1lll1llllll_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1111ll111_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1111ll11ll_opy_=bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ❃"))
    def bstack1lll11l1ll1_opy_(self):
        return self.hook_type
    def bstack1ll11ll1l111_opy_(self):
        return {
            bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ❄"): self.hook_type
        }
    def bstack1ll11ll1lll1_opy_(self):
        return {
            **super().bstack1ll11ll1lll1_opy_(),
            **self.bstack1ll11ll1l111_opy_()
        }
    def bstack1ll11lll1111_opy_(self):
        return {
            **super().bstack1ll11lll1111_opy_(),
            bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭❅"): self.bstack1l1111ll111_opy_,
            **self.bstack1ll11ll1l111_opy_()
        }
    def bstack1lll1llll1l_opy_(self):
        return bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ❆")
    def bstack1llll111l11_opy_(self, bstack1l1111ll111_opy_):
        self.bstack1l1111ll111_opy_ = bstack1l1111ll111_opy_