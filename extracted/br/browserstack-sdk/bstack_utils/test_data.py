# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1ll1111ll_opy_ import bstack1lll1ll111ll_opy_
class bstack1lllllll1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll11ll11l1_opy_=None, bstack1lll11l1lll1_opy_=True, finished_at=None, bstack1l11l11l_opy_=None, result=None, duration=None, bstack11111l111l_opy_=None, meta={}):
        self.bstack11111l111l_opy_ = bstack11111l111l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll11l1lll1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll11ll11l1_opy_ = bstack1lll11ll11l1_opy_
        self.finished_at = finished_at
        self.bstack1l11l11l_opy_ = bstack1l11l11l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11111ll1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111lll111_opy_(self, meta):
        self.meta = meta
    def bstack1111ll1l11_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll11l1ll11_opy_(self):
        bstack1lll11llll11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⊩"): bstack1lll11llll11_opy_,
            bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⊪"): bstack1lll11llll11_opy_,
            bstack11l1l11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⊫"): bstack1lll11llll11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1l11_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣ⊬") + key)
            setattr(self, key, val)
    def bstack1lll11ll11ll_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⊭"): self.name,
            bstack11l1l11_opy_ (u"ࠩࡥࡳࡩࡿࠧ⊮"): {
                bstack11l1l11_opy_ (u"ࠪࡰࡦࡴࡧࠨ⊯"): bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⊰"),
                bstack11l1l11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⊱"): self.code
            },
            bstack11l1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⊲"): self.scope,
            bstack11l1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬ⊳"): self.tags,
            bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⊴"): self.framework,
            bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⊵"): self.started_at
        }
    def bstack1lll11lll1ll_opy_(self):
        return {
         bstack11l1l11_opy_ (u"ࠪࡱࡪࡺࡡࠨ⊶"): self.meta
        }
    def bstack1lll11l1ll1l_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ⊷"): {
                bstack11l1l11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ⊸"): self.bstack1lll11ll11l1_opy_
            }
        }
    def bstack1lll11ll111l_opy_(self, bstack1lll11lll1l1_opy_, details):
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ⊹")] == bstack1lll11lll1l1_opy_, self.meta[bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⊺")]), None)
        step.update(details)
    def bstack1lll11111l_opy_(self, bstack1lll11lll1l1_opy_):
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫ⊻")] == bstack1lll11lll1l1_opy_, self.meta[bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⊼")]), None)
        step.update({
            bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⊽"): current_time()
        })
    def bstack1111l1llll_opy_(self, bstack1lll11lll1l1_opy_, result, duration=None):
        finished_at = current_time()
        if bstack1lll11lll1l1_opy_ is not None and self.meta.get(bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⊾")):
            step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨ⊿")] == bstack1lll11lll1l1_opy_, self.meta[bstack11l1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⋀")]), None)
            step.update({
                bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⋁"): finished_at,
                bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⋂"): duration if duration else time_diff(step[bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⋃")], finished_at),
                bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋄"): result.result,
                bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⋅"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll11ll1111_opy_):
        if self.meta.get(bstack11l1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⋆")):
            self.meta[bstack11l1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⋇")].append(bstack1lll11ll1111_opy_)
        else:
            self.meta[bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⋈")] = [ bstack1lll11ll1111_opy_ ]
    def bstack1lll11lll11l_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⋉"): self.bstack11111ll1l1_opy_(),
            bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⋊"): bstack11l1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⋋"),
            **self.bstack1lll11ll11ll_opy_(),
            **self.bstack1lll11l1ll11_opy_(),
            **self.bstack1lll11lll1ll_opy_()
        }
    def bstack1lll11ll1ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⋌"): self.finished_at,
            bstack11l1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⋍"): self.duration,
            bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⋎"): self.result.result
        }
        if data[bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⋏")] == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⋐"):
            data[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⋑")] = self.result.bstack1lll1ll1l11_opy_()
            data[bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⋒")] = [{bstack11l1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⋓"): self.result.bstack111l1l11lll_opy_()}]
        return data
    def bstack1lll11ll1l1l_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⋔"): self.bstack11111ll1l1_opy_(),
            **self.bstack1lll11ll11ll_opy_(),
            **self.bstack1lll11l1ll11_opy_(),
            **self.bstack1lll11ll1ll1_opy_(),
            **self.bstack1lll11lll1ll_opy_()
        }
    def bstack1llllllll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1l11_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧ⋕") in event:
            return self.bstack1lll11lll11l_opy_()
        elif bstack11l1l11_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⋖") in event:
            return self.bstack1lll11ll1l1l_opy_()
    def bstack1111l11l1l_opy_(self):
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
        super().__init__(*args, **kwargs, bstack1l11l11l_opy_=bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭⋗"))
    @classmethod
    def bstack1lll11ll1l11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l11_opy_ (u"ࠩ࡬ࡨࠬ⋘"): id(step),
                bstack11l1l11_opy_ (u"ࠪࡸࡪࡾࡴࠨ⋙"): step.name,
                bstack11l1l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ⋚"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack11l1l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭⋛"): {
                    bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⋜"): feature.name,
                    bstack11l1l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ⋝"): feature.filename,
                    bstack11l1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⋞"): feature.description
                },
                bstack11l1l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ⋟"): {
                    bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⋠"): scenario.name
                },
                bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⋡"): steps,
                bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧ⋢"): bstack1lll1ll111ll_opy_(test)
            }
        )
    def bstack1lll11ll1lll_opy_(self):
        return {
            bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⋣"): self.hooks
        }
    def bstack1lll11lll111_opy_(self):
        if self.integrations:
            return {
                bstack11l1l11_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭⋤"): self.integrations
            }
        return {}
    def bstack1lll11ll1l1l_opy_(self):
        return {
            **super().bstack1lll11ll1l1l_opy_(),
            **self.bstack1lll11ll1lll_opy_()
        }
    def bstack1lll11lll11l_opy_(self):
        return {
            **super().bstack1lll11lll11l_opy_(),
            **self.bstack1lll11lll111_opy_()
        }
    def bstack1111l11l1l_opy_(self):
        return bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⋥")
class bstack1111l11lll_opy_(bstack1lllllll1ll_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l1lll1ll_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l11l11l_opy_=bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⋦"))
    def bstack11111111l1_opy_(self):
        return self.hook_type
    def bstack1lll11l1llll_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⋧"): self.hook_type
        }
    def bstack1lll11ll1l1l_opy_(self):
        return {
            **super().bstack1lll11ll1l1l_opy_(),
            **self.bstack1lll11l1llll_opy_()
        }
    def bstack1lll11lll11l_opy_(self):
        return {
            **super().bstack1lll11lll11l_opy_(),
            bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⋨"): self.bstack1l1l1lll1ll_opy_,
            **self.bstack1lll11l1llll_opy_()
        }
    def bstack1111l11l1l_opy_(self):
        return bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ⋩")
    def bstack1111ll11l1_opy_(self, bstack1l1l1lll1ll_opy_):
        self.bstack1l1l1lll1ll_opy_ = bstack1l1l1lll1ll_opy_