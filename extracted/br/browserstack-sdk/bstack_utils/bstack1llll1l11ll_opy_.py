# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1llllll1l11_opy_, bstack1lll111l11l_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack1ll1l111llll_opy_
class bstack1lll1ll11l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l11l1lll_opy_=None, bstack1ll11l1lll11_opy_=True, bstack1ll1llll111_opy_=None, bstack11l111l11_opy_=None, result=None, duration=None, bstack1lll1ll1ll1_opy_=None, meta={}):
        self.bstack1lll1ll1ll1_opy_ = bstack1lll1ll1ll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11l1lll11_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l11l1lll_opy_ = bstack111l11l1lll_opy_
        self.bstack1ll1llll111_opy_ = bstack1ll1llll111_opy_
        self.bstack11l111l11_opy_ = bstack11l111l11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lll1l111ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll11111l_opy_(self, meta):
        self.meta = meta
    def bstack1llll111ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11ll111l1_opy_(self):
        bstack1ll11ll11111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ✠"): bstack1ll11ll11111_opy_,
            bstack111ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ✡"): bstack1ll11ll11111_opy_,
            bstack111ll11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭✢"): bstack1ll11ll11111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111ll11_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ✣") + key)
            setattr(self, key, val)
    def bstack1ll11l1ll1l1_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ✤"): self.name,
            bstack111ll11_opy_ (u"ࠫࡧࡵࡤࡺࠩ✥"): {
                bstack111ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ✦"): bstack111ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭✧"),
                bstack111ll11_opy_ (u"ࠧࡤࡱࡧࡩࠬ✨"): self.code
            },
            bstack111ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ✩"): self.scope,
            bstack111ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ✪"): self.tags,
            bstack111ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭✫"): self.framework,
            bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ✬"): self.started_at
        }
    def bstack1ll11l1ll111_opy_(self):
        return {
         bstack111ll11_opy_ (u"ࠬࡳࡥࡵࡣࠪ✭"): self.meta
        }
    def bstack1ll11l1llll1_opy_(self):
        return {
            bstack111ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ✮"): {
                bstack111ll11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ✯"): self.bstack111l11l1lll_opy_
            }
        }
    def bstack1ll11l1lll1l_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠨ࡫ࡧࠫ✰")] == sid, self.meta[bstack111ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✱")]), None)
        step.update(details)
    def bstack1lllllll111_opy_(self, sid):
        step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠪ࡭ࡩ࠭✲")] == sid, self.meta[bstack111ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✳")]), None)
        step.update({
            bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ✴"): bstack1llllll1l11_opy_()
        })
    def bstack1llll11ll11_opy_(self, sid, result, duration=None):
        bstack1ll1llll111_opy_ = bstack1llllll1l11_opy_()
        if sid is not None and self.meta.get(bstack111ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ✵")):
            step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠧࡪࡦࠪ✶")] == sid, self.meta[bstack111ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✷")]), None)
            step.update({
                bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ✸"): bstack1ll1llll111_opy_,
                bstack111ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ✹"): duration if duration else bstack1lll111l11l_opy_(step[bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ✺")], bstack1ll1llll111_opy_),
                bstack111ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ✻"): result.result,
                bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ✼"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11ll11l1l_opy_):
        if self.meta.get(bstack111ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭✽")):
            self.meta[bstack111ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✾")].append(bstack1ll11ll11l1l_opy_)
        else:
            self.meta[bstack111ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✿")] = [ bstack1ll11ll11l1l_opy_ ]
    def bstack1ll11ll111ll_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ❀"): self.bstack1lll1l111ll_opy_(),
            bstack111ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ❁"): bstack111ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭❂"),
            **self.bstack1ll11l1ll1l1_opy_(),
            **self.bstack1ll11ll111l1_opy_(),
            **self.bstack1ll11l1ll111_opy_()
        }
    def bstack1ll11ll11l11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ❃"): self.bstack1ll1llll111_opy_,
            bstack111ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ❄"): self.duration,
            bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ❅"): self.result.result
        }
        if data[bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ❆")] == bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ❇"):
            data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ❈")] = self.result.bstack1ll111l1l1l_opy_()
            data[bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭❉")] = [{bstack111ll11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ❊"): self.result.bstack1llllll1ll11_opy_()}]
        return data
    def bstack1ll11l1l1lll_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ❋"): self.bstack1lll1l111ll_opy_(),
            **self.bstack1ll11l1ll1l1_opy_(),
            **self.bstack1ll11ll111l1_opy_(),
            **self.bstack1ll11ll11l11_opy_(),
            **self.bstack1ll11l1ll111_opy_()
        }
    def bstack1lll1l11l1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111ll11_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ❌") in event:
            return self.bstack1ll11ll111ll_opy_()
        elif bstack111ll11_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ❍") in event:
            return self.bstack1ll11l1l1lll_opy_()
    def bstack1lll1ll1lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1llll111_opy_ = time if time else bstack1llllll1l11_opy_()
        self.duration = duration if duration else bstack1lll111l11l_opy_(self.started_at, self.bstack1ll1llll111_opy_)
        if result:
            self.result = result
class bstack1llll1l1l1l_opy_(bstack1lll1ll11l1_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l111l11_opy_=bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࠨ❎"))
    @classmethod
    def bstack1ll11l1lllll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111ll11_opy_ (u"ࠫ࡮ࡪࠧ❏"): id(step),
                bstack111ll11_opy_ (u"ࠬࡺࡥࡹࡶࠪ❐"): step.name,
                bstack111ll11_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ❑"): step.keyword,
            })
        return bstack1llll1l1l1l_opy_(
            **kwargs,
            meta={
                bstack111ll11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ❒"): {
                    bstack111ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭❓"): feature.name,
                    bstack111ll11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ❔"): feature.filename,
                    bstack111ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ❕"): feature.description
                },
                bstack111ll11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭❖"): {
                    bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ❗"): scenario.name
                },
                bstack111ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ❘"): steps,
                bstack111ll11_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ❙"): bstack1ll1l111llll_opy_(test)
            }
        )
    def bstack1ll11l1ll11l_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ❚"): self.hooks
        }
    def bstack1ll11ll1111l_opy_(self):
        if self.integrations:
            return {
                bstack111ll11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ❛"): self.integrations
            }
        return {}
    def bstack1ll11l1l1lll_opy_(self):
        return {
            **super().bstack1ll11l1l1lll_opy_(),
            **self.bstack1ll11l1ll11l_opy_(),
            **self.bstack1ll11ll1111l_opy_()
        }
    def bstack1ll11ll111ll_opy_(self):
        return {
            **super().bstack1ll11ll111ll_opy_(),
            **self.bstack1ll11ll1111l_opy_()
        }
    def bstack1lll1ll1lll_opy_(self):
        return bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ❜")
class bstack1llll11l111_opy_(bstack1lll1ll11l1_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l111l11111_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l111l11_opy_=bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ❝"))
    def bstack1lll11ll11l_opy_(self):
        return self.hook_type
    def bstack1ll11l1ll1ll_opy_(self):
        return {
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ❞"): self.hook_type
        }
    def bstack1ll11l1l1lll_opy_(self):
        return {
            **super().bstack1ll11l1l1lll_opy_(),
            **self.bstack1ll11l1ll1ll_opy_()
        }
    def bstack1ll11ll111ll_opy_(self):
        return {
            **super().bstack1ll11ll111ll_opy_(),
            bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ❟"): self.bstack1l111l11111_opy_,
            **self.bstack1ll11l1ll1ll_opy_()
        }
    def bstack1lll1ll1lll_opy_(self):
        return bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ❠")
    def bstack1llll111l11_opy_(self, bstack1l111l11111_opy_):
        self.bstack1l111l11111_opy_ = bstack1l111l11111_opy_