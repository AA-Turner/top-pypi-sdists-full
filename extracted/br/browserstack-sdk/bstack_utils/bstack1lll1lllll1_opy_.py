# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1111l1l1l_opy_, bstack1lll11111ll_opy_
from bstack_utils.bstack11l1111l11_opy_ import bstack1ll1l1111111_opy_
class bstack1lll1ll11l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1l11111_opy_=None, bstack1ll11l1l1ll1_opy_=True, bstack1ll1l1l11l1_opy_=None, bstack11l111l1ll_opy_=None, result=None, duration=None, bstack1lll1l111l1_opy_=None, meta={}):
        self.bstack1lll1l111l1_opy_ = bstack1lll1l111l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11l1l1ll1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1l11111_opy_ = bstack111l1l11111_opy_
        self.bstack1ll1l1l11l1_opy_ = bstack1ll1l1l11l1_opy_
        self.bstack11l111l1ll_opy_ = bstack11l111l1ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lll11l1111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1111l1_opy_(self, meta):
        self.meta = meta
    def bstack1llll1l11l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11ll11111_opy_(self):
        bstack1ll11l1ll1l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ❬"): bstack1ll11l1ll1l1_opy_,
            bstack111ll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ❭"): bstack1ll11l1ll1l1_opy_,
            bstack111ll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ❮"): bstack1ll11l1ll1l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111ll_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤ❯") + key)
            setattr(self, key, val)
    def bstack1ll11l1l11ll_opy_(self):
        return {
            bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ❰"): self.name,
            bstack111ll_opy_ (u"ࠪࡦࡴࡪࡹࠨ❱"): {
                bstack111ll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ❲"): bstack111ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ❳"),
                bstack111ll_opy_ (u"࠭ࡣࡰࡦࡨࠫ❴"): self.code
            },
            bstack111ll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ❵"): self.scope,
            bstack111ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭❶"): self.tags,
            bstack111ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ❷"): self.framework,
            bstack111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ❸"): self.started_at
        }
    def bstack1ll11l1l1l11_opy_(self):
        return {
         bstack111ll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ❹"): self.meta
        }
    def bstack1ll11l1ll1ll_opy_(self):
        return {
            bstack111ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ❺"): {
                bstack111ll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ❻"): self.bstack111l1l11111_opy_
            }
        }
    def bstack1ll11l1lllll_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack111ll_opy_ (u"ࠧࡪࡦࠪ❼")] == sid, self.meta[bstack111ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ❽")]), None)
        step.update(details)
    def bstack1l1111ll_opy_(self, sid):
        step = next(filter(lambda st: st[bstack111ll_opy_ (u"ࠩ࡬ࡨࠬ❾")] == sid, self.meta[bstack111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ❿")]), None)
        step.update({
            bstack111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ➀"): bstack1111l1l1l_opy_()
        })
    def bstack1llll111lll_opy_(self, sid, result, duration=None):
        bstack1ll1l1l11l1_opy_ = bstack1111l1l1l_opy_()
        if sid is not None and self.meta.get(bstack111ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ➁")):
            step = next(filter(lambda st: st[bstack111ll_opy_ (u"࠭ࡩࡥࠩ➂")] == sid, self.meta[bstack111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭➃")]), None)
            step.update({
                bstack111ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭➄"): bstack1ll1l1l11l1_opy_,
                bstack111ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ➅"): duration if duration else bstack1lll11111ll_opy_(step[bstack111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ➆")], bstack1ll1l1l11l1_opy_),
                bstack111ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ➇"): result.result,
                bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭➈"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11l1l11l1_opy_):
        if self.meta.get(bstack111ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ➉")):
            self.meta[bstack111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭➊")].append(bstack1ll11l1l11l1_opy_)
        else:
            self.meta[bstack111ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ➋")] = [ bstack1ll11l1l11l1_opy_ ]
    def bstack1ll11l1ll11l_opy_(self):
        return {
            bstack111ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ➌"): self.bstack1lll11l1111_opy_(),
            bstack111ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ➍"): bstack111ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ➎"),
            **self.bstack1ll11l1l11ll_opy_(),
            **self.bstack1ll11ll11111_opy_(),
            **self.bstack1ll11l1l1l11_opy_()
        }
    def bstack1ll11l1l1lll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ➏"): self.bstack1ll1l1l11l1_opy_,
            bstack111ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ➐"): self.duration,
            bstack111ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ➑"): self.result.result
        }
        if data[bstack111ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ➒")] == bstack111ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ➓"):
            data[bstack111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ➔")] = self.result.bstack1ll111l111l_opy_()
            data[bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ➕")] = [{bstack111ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ➖"): self.result.bstack1llll111lll1_opy_()}]
        return data
    def bstack1ll11l1llll1_opy_(self):
        return {
            bstack111ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ➗"): self.bstack1lll11l1111_opy_(),
            **self.bstack1ll11l1l11ll_opy_(),
            **self.bstack1ll11ll11111_opy_(),
            **self.bstack1ll11l1l1lll_opy_(),
            **self.bstack1ll11l1l1l11_opy_()
        }
    def bstack1lll1l111ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111ll_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ➘") in event:
            return self.bstack1ll11l1ll11l_opy_()
        elif bstack111ll_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ➙") in event:
            return self.bstack1ll11l1llll1_opy_()
    def bstack1lll11lll11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1l1l11l1_opy_ = time if time else bstack1111l1l1l_opy_()
        self.duration = duration if duration else bstack1lll11111ll_opy_(self.started_at, self.bstack1ll1l1l11l1_opy_)
        if result:
            self.result = result
class bstack1llll11l1ll_opy_(bstack1lll1ll11l1_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l111l1ll_opy_=bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࠧ➚"))
    @classmethod
    def bstack1ll11l1lll11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭➛"): id(step),
                bstack111ll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ➜"): step.name,
                bstack111ll_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭➝"): step.keyword,
            })
        return bstack1llll11l1ll_opy_(
            **kwargs,
            meta={
                bstack111ll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ➞"): {
                    bstack111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ➟"): feature.name,
                    bstack111ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭➠"): feature.filename,
                    bstack111ll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ➡"): feature.description
                },
                bstack111ll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ➢"): {
                    bstack111ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ➣"): scenario.name
                },
                bstack111ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ➤"): steps,
                bstack111ll_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ➥"): bstack1ll1l1111111_opy_(test)
            }
        )
    def bstack1ll11l1ll111_opy_(self):
        return {
            bstack111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭➦"): self.hooks
        }
    def bstack1ll11l1lll1l_opy_(self):
        if self.integrations:
            return {
                bstack111ll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ➧"): self.integrations
            }
        return {}
    def bstack1ll11l1llll1_opy_(self):
        return {
            **super().bstack1ll11l1llll1_opy_(),
            **self.bstack1ll11l1ll111_opy_(),
            **self.bstack1ll11l1lll1l_opy_()
        }
    def bstack1ll11l1ll11l_opy_(self):
        return {
            **super().bstack1ll11l1ll11l_opy_(),
            **self.bstack1ll11l1lll1l_opy_()
        }
    def bstack1lll11lll11_opy_(self):
        return bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ➨")
class bstack1llll111111_opy_(bstack1lll1ll11l1_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1111ll1ll_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l111l1ll_opy_=bstack111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ➩"))
    def bstack1lll1l1ll1l_opy_(self):
        return self.hook_type
    def bstack1ll11l1l1l1l_opy_(self):
        return {
            bstack111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ➪"): self.hook_type
        }
    def bstack1ll11l1llll1_opy_(self):
        return {
            **super().bstack1ll11l1llll1_opy_(),
            **self.bstack1ll11l1l1l1l_opy_()
        }
    def bstack1ll11l1ll11l_opy_(self):
        return {
            **super().bstack1ll11l1ll11l_opy_(),
            bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ➫"): self.bstack1l1111ll1ll_opy_,
            **self.bstack1ll11l1l1l1l_opy_()
        }
    def bstack1lll11lll11_opy_(self):
        return bstack111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ➬")
    def bstack1llll1111ll_opy_(self, bstack1l1111ll1ll_opy_):
        self.bstack1l1111ll1ll_opy_ = bstack1l1111ll1ll_opy_