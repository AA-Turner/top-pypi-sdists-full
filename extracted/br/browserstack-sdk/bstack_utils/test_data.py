# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1l1l11lll_opy_ import bstack1lll1ll11111_opy_
class bstack1lllllll1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll11l1ll1l_opy_=None, bstack1lll11ll11ll_opy_=True, finished_at=None, bstack11l1l1llll_opy_=None, result=None, duration=None, bstack111111llll_opy_=None, meta={}):
        self.bstack111111llll_opy_ = bstack111111llll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll11ll11ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll11l1ll1l_opy_ = bstack1lll11l1ll1l_opy_
        self.finished_at = finished_at
        self.bstack11l1l1llll_opy_ = bstack11l1l1llll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llllll1lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111lll111_opy_(self, meta):
        self.meta = meta
    def bstack1111l1l1l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll11l1lll1_opy_(self):
        bstack1lll11ll1lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⊦"): bstack1lll11ll1lll_opy_,
            bstack11ll111_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⊧"): bstack1lll11ll1lll_opy_,
            bstack11ll111_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⊨"): bstack1lll11ll1lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11ll111_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ⊩") + key)
            setattr(self, key, val)
    def bstack1lll11ll1111_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⊪"): self.name,
            bstack11ll111_opy_ (u"࠭ࡢࡰࡦࡼࠫ⊫"): {
                bstack11ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⊬"): bstack11ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⊭"),
                bstack11ll111_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⊮"): self.code
            },
            bstack11ll111_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⊯"): self.scope,
            bstack11ll111_opy_ (u"ࠫࡹࡧࡧࡴࠩ⊰"): self.tags,
            bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⊱"): self.framework,
            bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊲"): self.started_at
        }
    def bstack1lll11lll1ll_opy_(self):
        return {
         bstack11ll111_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ⊳"): self.meta
        }
    def bstack1lll11lll1l1_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ⊴"): {
                bstack11ll111_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭⊵"): self.bstack1lll11l1ll1l_opy_
            }
        }
    def bstack1lll11ll111l_opy_(self, bstack1lll11ll1ll1_opy_, details):
        step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭⊶")] == bstack1lll11ll1ll1_opy_, self.meta[bstack11ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⊷")]), None)
        step.update(details)
    def bstack11l11111l_opy_(self, bstack1lll11ll1ll1_opy_):
        step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨ⊸")] == bstack1lll11ll1ll1_opy_, self.meta[bstack11ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⊹")]), None)
        step.update({
            bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⊺"): current_time()
        })
    def bstack1111l11lll_opy_(self, bstack1lll11ll1ll1_opy_, result, duration=None):
        finished_at = current_time()
        if bstack1lll11ll1ll1_opy_ is not None and self.meta.get(bstack11ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⊻")):
            step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬ⊼")] == bstack1lll11ll1ll1_opy_, self.meta[bstack11ll111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⊽")]), None)
            step.update({
                bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⊾"): finished_at,
                bstack11ll111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⊿"): duration if duration else time_diff(step[bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⋀")], finished_at),
                bstack11ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⋁"): result.result,
                bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⋂"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll11l1llll_opy_):
        if self.meta.get(bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⋃")):
            self.meta[bstack11ll111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⋄")].append(bstack1lll11l1llll_opy_)
        else:
            self.meta[bstack11ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⋅")] = [ bstack1lll11l1llll_opy_ ]
    def bstack1lll11ll1l11_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ⋆"): self.bstack1llllll1lll_opy_(),
            bstack11ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⋇"): bstack11ll111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⋈"),
            **self.bstack1lll11ll1111_opy_(),
            **self.bstack1lll11l1lll1_opy_(),
            **self.bstack1lll11lll1ll_opy_()
        }
    def bstack1lll11lll11l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⋉"): self.finished_at,
            bstack11ll111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⋊"): self.duration,
            bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋋"): self.result.result
        }
        if data[bstack11ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⋌")] == bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⋍"):
            data[bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⋎")] = self.result.bstack1lll1ll11ll_opy_()
            data[bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⋏")] = [{bstack11ll111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⋐"): self.result.bstack111l1l111ll_opy_()}]
        return data
    def bstack1lll11ll1l1l_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⋑"): self.bstack1llllll1lll_opy_(),
            **self.bstack1lll11ll1111_opy_(),
            **self.bstack1lll11l1lll1_opy_(),
            **self.bstack1lll11lll11l_opy_(),
            **self.bstack1lll11lll1ll_opy_()
        }
    def bstack1111111111_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11ll111_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫ⋒") in event:
            return self.bstack1lll11ll1l11_opy_()
        elif bstack11ll111_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⋓") in event:
            return self.bstack1lll11ll1l1l_opy_()
    def bstack11111ll11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack1lllllll1ll_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l1l1llll_opy_=bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࠪ⋔"))
    @classmethod
    def bstack1lll11ll11l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll111_opy_ (u"࠭ࡩࡥࠩ⋕"): id(step),
                bstack11ll111_opy_ (u"ࠧࡵࡧࡻࡸࠬ⋖"): step.name,
                bstack11ll111_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ⋗"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack11ll111_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ⋘"): {
                    bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ⋙"): feature.name,
                    bstack11ll111_opy_ (u"ࠫࡵࡧࡴࡩࠩ⋚"): feature.filename,
                    bstack11ll111_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ⋛"): feature.description
                },
                bstack11ll111_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ⋜"): {
                    bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⋝"): scenario.name
                },
                bstack11ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⋞"): steps,
                bstack11ll111_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ⋟"): bstack1lll1ll11111_opy_(test)
            }
        )
    def bstack1lll11lll111_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⋠"): self.hooks
        }
    def bstack1lll11l1ll11_opy_(self):
        if self.integrations:
            return {
                bstack11ll111_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⋡"): self.integrations
            }
        return {}
    def bstack1lll11ll1l1l_opy_(self):
        return {
            **super().bstack1lll11ll1l1l_opy_(),
            **self.bstack1lll11lll111_opy_()
        }
    def bstack1lll11ll1l11_opy_(self):
        return {
            **super().bstack1lll11ll1l11_opy_(),
            **self.bstack1lll11l1ll11_opy_()
        }
    def bstack11111ll11l_opy_(self):
        return bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⋢")
class bstack1111ll11l1_opy_(bstack1lllllll1ll_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l1l111ll_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l1l1llll_opy_=bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⋣"))
    def bstack1111111lll_opy_(self):
        return self.hook_type
    def bstack1lll11l1l1ll_opy_(self):
        return {
            bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⋤"): self.hook_type
        }
    def bstack1lll11ll1l1l_opy_(self):
        return {
            **super().bstack1lll11ll1l1l_opy_(),
            **self.bstack1lll11l1l1ll_opy_()
        }
    def bstack1lll11ll1l11_opy_(self):
        return {
            **super().bstack1lll11ll1l11_opy_(),
            bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭⋥"): self.bstack1l1l1l111ll_opy_,
            **self.bstack1lll11l1l1ll_opy_()
        }
    def bstack11111ll11l_opy_(self):
        return bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ⋦")
    def bstack1111ll11ll_opy_(self, bstack1l1l1l111ll_opy_):
        self.bstack1l1l1l111ll_opy_ = bstack1l1l1l111ll_opy_