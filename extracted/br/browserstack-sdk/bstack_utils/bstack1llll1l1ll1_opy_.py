# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l111l1ll_opy_, bstack1ll1l1ll1ll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1ll1l111l11l_opy_
class bstack1lll1lllll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l11lllll_opy_=None, bstack1ll11l1ll11l_opy_=True, bstack1lll111l111_opy_=None, bstack111l1l1l_opy_=None, result=None, duration=None, bstack1lll1llll11_opy_=None, meta={}):
        self.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll11l1ll11l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l11lllll_opy_ = bstack111l11lllll_opy_
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
        self.bstack111l1l1l_opy_ = bstack111l1l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lll1l111l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll111111_opy_(self, meta):
        self.meta = meta
    def bstack1llll111ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11l1lll11_opy_(self):
        bstack1ll11l1ll111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ✢"): bstack1ll11l1ll111_opy_,
            bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ✣"): bstack1ll11l1ll111_opy_,
            bstack1l1111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ✤"): bstack1ll11l1ll111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1111l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ✥") + key)
            setattr(self, key, val)
    def bstack1ll11ll11111_opy_(self):
        return {
            bstack1l1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ✦"): self.name,
            bstack1l1111l_opy_ (u"࠭ࡢࡰࡦࡼࠫ✧"): {
                bstack1l1111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ✨"): bstack1l1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ✩"),
                bstack1l1111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ✪"): self.code
            },
            bstack1l1111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ✫"): self.scope,
            bstack1l1111l_opy_ (u"ࠫࡹࡧࡧࡴࠩ✬"): self.tags,
            bstack1l1111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ✭"): self.framework,
            bstack1l1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ✮"): self.started_at
        }
    def bstack1ll11l1l1l1l_opy_(self):
        return {
         bstack1l1111l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ✯"): self.meta
        }
    def bstack1ll11l1ll1l1_opy_(self):
        return {
            bstack1l1111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ✰"): {
                bstack1l1111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭✱"): self.bstack111l11lllll_opy_
            }
        }
    def bstack1ll11l1l1ll1_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1l1111l_opy_ (u"ࠪ࡭ࡩ࠭✲")] == sid, self.meta[bstack1l1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ✳")]), None)
        step.update(details)
    def bstack11l1ll1l1l_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1l1111l_opy_ (u"ࠬ࡯ࡤࠨ✴")] == sid, self.meta[bstack1l1111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ✵")]), None)
        step.update({
            bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ✶"): bstack1l111l1ll_opy_()
        })
    def bstack1llll111l1l_opy_(self, sid, result, duration=None):
        bstack1lll111l111_opy_ = bstack1l111l1ll_opy_()
        if sid is not None and self.meta.get(bstack1l1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ✷")):
            step = next(filter(lambda st: st[bstack1l1111l_opy_ (u"ࠩ࡬ࡨࠬ✸")] == sid, self.meta[bstack1l1111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ✹")]), None)
            step.update({
                bstack1l1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ✺"): bstack1lll111l111_opy_,
                bstack1l1111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ✻"): duration if duration else bstack1ll1l1ll1ll_opy_(step[bstack1l1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ✼")], bstack1lll111l111_opy_),
                bstack1l1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ✽"): result.result,
                bstack1l1111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ✾"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll11ll111ll_opy_):
        if self.meta.get(bstack1l1111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ✿")):
            self.meta[bstack1l1111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ❀")].append(bstack1ll11ll111ll_opy_)
        else:
            self.meta[bstack1l1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ❁")] = [ bstack1ll11ll111ll_opy_ ]
    def bstack1ll11l1llll1_opy_(self):
        return {
            bstack1l1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ❂"): self.bstack1lll1l111l1_opy_(),
            bstack1l1111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭❃"): bstack1l1111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ❄"),
            **self.bstack1ll11ll11111_opy_(),
            **self.bstack1ll11l1lll11_opy_(),
            **self.bstack1ll11l1l1l1l_opy_()
        }
    def bstack1ll11ll111l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭❅"): self.bstack1lll111l111_opy_,
            bstack1l1111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ❆"): self.duration,
            bstack1l1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ❇"): self.result.result
        }
        if data[bstack1l1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ❈")] == bstack1l1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ❉"):
            data[bstack1l1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ❊")] = self.result.bstack1ll111l1l1l_opy_()
            data[bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ❋")] = [{bstack1l1111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ❌"): self.result.bstack1llll1l1l11l_opy_()}]
        return data
    def bstack1ll11ll1111l_opy_(self):
        return {
            bstack1l1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ❍"): self.bstack1lll1l111l1_opy_(),
            **self.bstack1ll11ll11111_opy_(),
            **self.bstack1ll11l1lll11_opy_(),
            **self.bstack1ll11ll111l1_opy_(),
            **self.bstack1ll11l1l1l1l_opy_()
        }
    def bstack1lll1l11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1111l_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫ❎") in event:
            return self.bstack1ll11l1llll1_opy_()
        elif bstack1l1111l_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭❏") in event:
            return self.bstack1ll11ll1111l_opy_()
    def bstack1lll11llll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1lll111l111_opy_ = time if time else bstack1l111l1ll_opy_()
        self.duration = duration if duration else bstack1ll1l1ll1ll_opy_(self.started_at, self.bstack1lll111l111_opy_)
        if result:
            self.result = result
class bstack1llll1l11l1_opy_(bstack1lll1lllll1_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111l1l1l_opy_=bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࠪ❐"))
    @classmethod
    def bstack1ll11l1lll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1111l_opy_ (u"࠭ࡩࡥࠩ❑"): id(step),
                bstack1l1111l_opy_ (u"ࠧࡵࡧࡻࡸࠬ❒"): step.name,
                bstack1l1111l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ❓"): step.keyword,
            })
        return bstack1llll1l11l1_opy_(
            **kwargs,
            meta={
                bstack1l1111l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ❔"): {
                    bstack1l1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ❕"): feature.name,
                    bstack1l1111l_opy_ (u"ࠫࡵࡧࡴࡩࠩ❖"): feature.filename,
                    bstack1l1111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ❗"): feature.description
                },
                bstack1l1111l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ❘"): {
                    bstack1l1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ❙"): scenario.name
                },
                bstack1l1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ❚"): steps,
                bstack1l1111l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ❛"): bstack1ll1l111l11l_opy_(test)
            }
        )
    def bstack1ll11l1l1lll_opy_(self):
        return {
            bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ❜"): self.hooks
        }
    def bstack1ll11l1ll1ll_opy_(self):
        if self.integrations:
            return {
                bstack1l1111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ❝"): self.integrations
            }
        return {}
    def bstack1ll11ll1111l_opy_(self):
        return {
            **super().bstack1ll11ll1111l_opy_(),
            **self.bstack1ll11l1l1lll_opy_(),
            **self.bstack1ll11l1ll1ll_opy_()
        }
    def bstack1ll11l1llll1_opy_(self):
        return {
            **super().bstack1ll11l1llll1_opy_(),
            **self.bstack1ll11l1ll1ll_opy_()
        }
    def bstack1lll11llll1_opy_(self):
        return bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ❞")
class bstack1llll11l1ll_opy_(bstack1lll1lllll1_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack11llllll11l_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111l1l1l_opy_=bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ❟"))
    def bstack1lll1l1ll1l_opy_(self):
        return self.hook_type
    def bstack1ll11l1lllll_opy_(self):
        return {
            bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ❠"): self.hook_type
        }
    def bstack1ll11ll1111l_opy_(self):
        return {
            **super().bstack1ll11ll1111l_opy_(),
            **self.bstack1ll11l1lllll_opy_()
        }
    def bstack1ll11l1llll1_opy_(self):
        return {
            **super().bstack1ll11l1llll1_opy_(),
            bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭❡"): self.bstack11llllll11l_opy_,
            **self.bstack1ll11l1lllll_opy_()
        }
    def bstack1lll11llll1_opy_(self):
        return bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ❢")
    def bstack1llll1111l1_opy_(self, bstack11llllll11l_opy_):
        self.bstack11llllll11l_opy_ = bstack11llllll11l_opy_