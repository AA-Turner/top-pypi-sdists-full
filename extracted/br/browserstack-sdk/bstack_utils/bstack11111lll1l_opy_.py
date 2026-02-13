# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11l1lll11_opy_, bstack111l11l1ll1_opy_
from bstack_utils.bstack1ll1ll111_opy_ import bstack1lll1l11l111_opy_
class bstack11111111l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll11l11l11_opy_=None, bstack1lll11l1l111_opy_=True, bstack11l1ll1l111_opy_=None, bstack1l1ll11111_opy_=None, result=None, duration=None, bstack111111llll_opy_=None, meta={}):
        self.bstack111111llll_opy_ = bstack111111llll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll11l1l111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll11l11l11_opy_ = bstack1lll11l11l11_opy_
        self.bstack11l1ll1l111_opy_ = bstack11l1ll1l111_opy_
        self.bstack1l1ll11111_opy_ = bstack1l1ll11111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111111ll1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111l11ll1_opy_(self, meta):
        self.meta = meta
    def bstack1111l1l11l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll111llll1_opy_(self):
        bstack1lll11l1l11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⊞"): bstack1lll11l1l11l_opy_,
            bstack11l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⊟"): bstack1lll11l1l11l_opy_,
            bstack11l11_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⊠"): bstack1lll11l1l11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l11_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦ⊡") + key)
            setattr(self, key, val)
    def bstack1lll11l11111_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⊢"): self.name,
            bstack11l11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⊣"): {
                bstack11l11_opy_ (u"࠭࡬ࡢࡰࡪࠫ⊤"): bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⊥"),
                bstack11l11_opy_ (u"ࠨࡥࡲࡨࡪ࠭⊦"): self.code
            },
            bstack11l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⊧"): self.scope,
            bstack11l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⊨"): self.tags,
            bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⊩"): self.framework,
            bstack11l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊪"): self.started_at
        }
    def bstack1lll11l111l1_opy_(self):
        return {
         bstack11l11_opy_ (u"࠭࡭ࡦࡶࡤࠫ⊫"): self.meta
        }
    def bstack1lll11l11lll_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⊬"): {
                bstack11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⊭"): self.bstack1lll11l11l11_opy_
            }
        }
    def bstack1lll11l11ll1_opy_(self, bstack1lll11l1l1ll_opy_, details):
        step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠩ࡬ࡨࠬ⊮")] == bstack1lll11l1l1ll_opy_, self.meta[bstack11l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⊯")]), None)
        step.update(details)
    def bstack11lll11lll_opy_(self, bstack1lll11l1l1ll_opy_):
        step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠫ࡮ࡪࠧ⊰")] == bstack1lll11l1l1ll_opy_, self.meta[bstack11l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⊱")]), None)
        step.update({
            bstack11l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊲"): bstack11l1lll11_opy_()
        })
    def bstack11111ll11l_opy_(self, bstack1lll11l1l1ll_opy_, result, duration=None):
        bstack11l1ll1l111_opy_ = bstack11l1lll11_opy_()
        if bstack1lll11l1l1ll_opy_ is not None and self.meta.get(bstack11l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⊳")):
            step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠨ࡫ࡧࠫ⊴")] == bstack1lll11l1l1ll_opy_, self.meta[bstack11l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⊵")]), None)
            step.update({
                bstack11l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⊶"): bstack11l1ll1l111_opy_,
                bstack11l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⊷"): duration if duration else bstack111l11l1ll1_opy_(step[bstack11l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊸")], bstack11l1ll1l111_opy_),
                bstack11l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⊹"): result.result,
                bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⊺"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll111ll1ll_opy_):
        if self.meta.get(bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⊻")):
            self.meta[bstack11l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⊼")].append(bstack1lll111ll1ll_opy_)
        else:
            self.meta[bstack11l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⊽")] = [ bstack1lll111ll1ll_opy_ ]
    def bstack1lll11l11l1l_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⊾"): self.bstack111111ll1l_opy_(),
            bstack11l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⊿"): bstack11l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⋀"),
            **self.bstack1lll11l11111_opy_(),
            **self.bstack1lll111llll1_opy_(),
            **self.bstack1lll11l111l1_opy_()
        }
    def bstack1lll111lllll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⋁"): self.bstack11l1ll1l111_opy_,
            bstack11l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⋂"): self.duration,
            bstack11l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⋃"): self.result.result
        }
        if data[bstack11l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋄")] == bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⋅"):
            data[bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⋆")] = self.result.bstack1lll1l11lll_opy_()
            data[bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⋇")] = [{bstack11l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⋈"): self.result.bstack111l1l1ll11_opy_()}]
        return data
    def bstack1lll11l111ll_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⋉"): self.bstack111111ll1l_opy_(),
            **self.bstack1lll11l11111_opy_(),
            **self.bstack1lll111llll1_opy_(),
            **self.bstack1lll111lllll_opy_(),
            **self.bstack1lll11l111l1_opy_()
        }
    def bstack1lllllll1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l11_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪ⋊") in event:
            return self.bstack1lll11l11l1l_opy_()
        elif bstack11l11_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⋋") in event:
            return self.bstack1lll11l111ll_opy_()
    def bstack1111111lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11l1ll1l111_opy_ = time if time else bstack11l1lll11_opy_()
        self.duration = duration if duration else bstack111l11l1ll1_opy_(self.started_at, self.bstack11l1ll1l111_opy_)
        if result:
            self.result = result
class bstack1111ll1111_opy_(bstack11111111l1_opy_):
    def __init__(self, hooks=[], bstack1111l111l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        super().__init__(*args, **kwargs, bstack1l1ll11111_opy_=bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⋌"))
    @classmethod
    def bstack1lll111lll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l11_opy_ (u"ࠬ࡯ࡤࠨ⋍"): id(step),
                bstack11l11_opy_ (u"࠭ࡴࡦࡺࡷࠫ⋎"): step.name,
                bstack11l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ⋏"): step.keyword,
            })
        return bstack1111ll1111_opy_(
            **kwargs,
            meta={
                bstack11l11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ⋐"): {
                    bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⋑"): feature.name,
                    bstack11l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ⋒"): feature.filename,
                    bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ⋓"): feature.description
                },
                bstack11l11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ⋔"): {
                    bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⋕"): scenario.name
                },
                bstack11l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⋖"): steps,
                bstack11l11_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪ⋗"): bstack1lll1l11l111_opy_(test)
            }
        )
    def bstack1lll11l1l1l1_opy_(self):
        return {
            bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⋘"): self.hooks
        }
    def bstack1lll11l1111l_opy_(self):
        if self.bstack1111l111l1_opy_:
            return {
                bstack11l11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ⋙"): self.bstack1111l111l1_opy_
            }
        return {}
    def bstack1lll11l111ll_opy_(self):
        return {
            **super().bstack1lll11l111ll_opy_(),
            **self.bstack1lll11l1l1l1_opy_()
        }
    def bstack1lll11l11l1l_opy_(self):
        return {
            **super().bstack1lll11l11l1l_opy_(),
            **self.bstack1lll11l1111l_opy_()
        }
    def bstack1111111lll_opy_(self):
        return bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⋚")
class bstack1111l1lll1_opy_(bstack11111111l1_opy_):
    def __init__(self, hook_type, *args,bstack1111l111l1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1ll1111ll_opy_ = None
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
        super().__init__(*args, **kwargs, bstack1l1ll11111_opy_=bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⋛"))
    def bstack111111l1l1_opy_(self):
        return self.hook_type
    def bstack1lll111lll11_opy_(self):
        return {
            bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⋜"): self.hook_type
        }
    def bstack1lll11l111ll_opy_(self):
        return {
            **super().bstack1lll11l111ll_opy_(),
            **self.bstack1lll111lll11_opy_()
        }
    def bstack1lll11l11l1l_opy_(self):
        return {
            **super().bstack1lll11l11l1l_opy_(),
            bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⋝"): self.bstack1l1ll1111ll_opy_,
            **self.bstack1lll111lll11_opy_()
        }
    def bstack1111111lll_opy_(self):
        return bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ⋞")
    def bstack11111ll1l1_opy_(self, bstack1l1ll1111ll_opy_):
        self.bstack1l1ll1111ll_opy_ = bstack1l1ll1111ll_opy_