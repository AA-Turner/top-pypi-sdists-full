# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lllllllll_opy_, bstack111l1lll1l1_opy_
from bstack_utils.bstack1l1111l1_opy_ import bstack11111l111ll_opy_
class bstack111l11lll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllllll1l11_opy_=None, bstack1lllllll11l1_opy_=True, bstack1l1ll1lll1l_opy_=None, bstack1l1l1l11l_opy_=None, result=None, duration=None, bstack111l1l11ll_opy_=None, meta={}):
        self.bstack111l1l11ll_opy_ = bstack111l1l11ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllllll11l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllllll1l11_opy_ = bstack1lllllll1l11_opy_
        self.bstack1l1ll1lll1l_opy_ = bstack1l1ll1lll1l_opy_
        self.bstack1l1l1l11l_opy_ = bstack1l1l1l11l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111llll11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111ll1111l_opy_(self, meta):
        self.meta = meta
    def bstack111ll111l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllllllll1l_opy_(self):
        bstack1lllllllll11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᾐ"): bstack1lllllllll11_opy_,
            bstack11l1111_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᾑ"): bstack1lllllllll11_opy_,
            bstack11l1111_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᾒ"): bstack1lllllllll11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1111_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨᾓ") + key)
            setattr(self, key, val)
    def bstack1lllllll1l1l_opy_(self):
        return {
            bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᾔ"): self.name,
            bstack11l1111_opy_ (u"ࠧࡣࡱࡧࡽࠬᾕ"): {
                bstack11l1111_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᾖ"): bstack11l1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᾗ"),
                bstack11l1111_opy_ (u"ࠪࡧࡴࡪࡥࠨᾘ"): self.code
            },
            bstack11l1111_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᾙ"): self.scope,
            bstack11l1111_opy_ (u"ࠬࡺࡡࡨࡵࠪᾚ"): self.tags,
            bstack11l1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᾛ"): self.framework,
            bstack11l1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᾜ"): self.started_at
        }
    def bstack1llllllll1ll_opy_(self):
        return {
         bstack11l1111_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᾝ"): self.meta
        }
    def bstack1lllllll1ll1_opy_(self):
        return {
            bstack11l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᾞ"): {
                bstack11l1111_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᾟ"): self.bstack1lllllll1l11_opy_
            }
        }
    def bstack1llllllll1l1_opy_(self, bstack1lllllll111l_opy_, details):
        step = next(filter(lambda st: st[bstack11l1111_opy_ (u"ࠫ࡮ࡪࠧᾠ")] == bstack1lllllll111l_opy_, self.meta[bstack11l1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᾡ")]), None)
        step.update(details)
    def bstack11l11lll1_opy_(self, bstack1lllllll111l_opy_):
        step = next(filter(lambda st: st[bstack11l1111_opy_ (u"࠭ࡩࡥࠩᾢ")] == bstack1lllllll111l_opy_, self.meta[bstack11l1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᾣ")]), None)
        step.update({
            bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᾤ"): bstack1lllllllll_opy_()
        })
    def bstack111ll1lll1_opy_(self, bstack1lllllll111l_opy_, result, duration=None):
        bstack1l1ll1lll1l_opy_ = bstack1lllllllll_opy_()
        if bstack1lllllll111l_opy_ is not None and self.meta.get(bstack11l1111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾥ")):
            step = next(filter(lambda st: st[bstack11l1111_opy_ (u"ࠪ࡭ࡩ࠭ᾦ")] == bstack1lllllll111l_opy_, self.meta[bstack11l1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᾧ")]), None)
            step.update({
                bstack11l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᾨ"): bstack1l1ll1lll1l_opy_,
                bstack11l1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᾩ"): duration if duration else bstack111l1lll1l1_opy_(step[bstack11l1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᾪ")], bstack1l1ll1lll1l_opy_),
                bstack11l1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᾫ"): result.result,
                bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᾬ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllllll1lll_opy_):
        if self.meta.get(bstack11l1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᾭ")):
            self.meta[bstack11l1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᾮ")].append(bstack1lllllll1lll_opy_)
        else:
            self.meta[bstack11l1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᾯ")] = [ bstack1lllllll1lll_opy_ ]
    def bstack11111111111_opy_(self):
        return {
            bstack11l1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᾰ"): self.bstack1111llll11_opy_(),
            **self.bstack1lllllll1l1l_opy_(),
            **self.bstack1lllllllll1l_opy_(),
            **self.bstack1llllllll1ll_opy_()
        }
    def bstack1llllllllll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᾱ"): self.bstack1l1ll1lll1l_opy_,
            bstack11l1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᾲ"): self.duration,
            bstack11l1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᾳ"): self.result.result
        }
        if data[bstack11l1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᾴ")] == bstack11l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᾵"):
            data[bstack11l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᾶ")] = self.result.bstack111111llll_opy_()
            data[bstack11l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᾷ")] = [{bstack11l1111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᾸ"): self.result.bstack111l1ll111l_opy_()}]
        return data
    def bstack1llllllll11l_opy_(self):
        return {
            bstack11l1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ᾱ"): self.bstack1111llll11_opy_(),
            **self.bstack1lllllll1l1l_opy_(),
            **self.bstack1lllllllll1l_opy_(),
            **self.bstack1llllllllll1_opy_(),
            **self.bstack1llllllll1ll_opy_()
        }
    def bstack111l111l1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1111_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪᾺ") in event:
            return self.bstack11111111111_opy_()
        elif bstack11l1111_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬΆ") in event:
            return self.bstack1llllllll11l_opy_()
    def bstack1111llllll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1ll1lll1l_opy_ = time if time else bstack1lllllllll_opy_()
        self.duration = duration if duration else bstack111l1lll1l1_opy_(self.started_at, self.bstack1l1ll1lll1l_opy_)
        if result:
            self.result = result
class bstack111ll1ll11_opy_(bstack111l11lll1_opy_):
    def __init__(self, hooks=[], bstack111lll11ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l11l_opy_=bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᾼ"))
    @classmethod
    def bstack1lllllllllll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1111_opy_ (u"ࠬ࡯ࡤࠨ᾽"): id(step),
                bstack11l1111_opy_ (u"࠭ࡴࡦࡺࡷࠫι"): step.name,
                bstack11l1111_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ᾿"): step.keyword,
            })
        return bstack111ll1ll11_opy_(
            **kwargs,
            meta={
                bstack11l1111_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ῀"): {
                    bstack11l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ῁"): feature.name,
                    bstack11l1111_opy_ (u"ࠪࡴࡦࡺࡨࠨῂ"): feature.filename,
                    bstack11l1111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩῃ"): feature.description
                },
                bstack11l1111_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧῄ"): {
                    bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ῅"): scenario.name
                },
                bstack11l1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ῆ"): steps,
                bstack11l1111_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪῇ"): bstack11111l111ll_opy_(test)
            }
        )
    def bstack1lllllll11ll_opy_(self):
        return {
            bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨῈ"): self.hooks
        }
    def bstack1111111111l_opy_(self):
        if self.bstack111lll11ll_opy_:
            return {
                bstack11l1111_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩΈ"): self.bstack111lll11ll_opy_
            }
        return {}
    def bstack1llllllll11l_opy_(self):
        return {
            **super().bstack1llllllll11l_opy_(),
            **self.bstack1lllllll11ll_opy_()
        }
    def bstack11111111111_opy_(self):
        return {
            **super().bstack11111111111_opy_(),
            **self.bstack1111111111l_opy_()
        }
    def bstack1111llllll_opy_(self):
        return bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ὴ")
class bstack111ll1l1l1_opy_(bstack111l11lll1_opy_):
    def __init__(self, hook_type, *args,bstack111lll11ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l111111lll_opy_ = None
        self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l11l_opy_=bstack11l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪΉ"))
    def bstack1111lll1ll_opy_(self):
        return self.hook_type
    def bstack1llllllll111_opy_(self):
        return {
            bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩῌ"): self.hook_type
        }
    def bstack1llllllll11l_opy_(self):
        return {
            **super().bstack1llllllll11l_opy_(),
            **self.bstack1llllllll111_opy_()
        }
    def bstack11111111111_opy_(self):
        return {
            **super().bstack11111111111_opy_(),
            bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ῍"): self.bstack1l111111lll_opy_,
            **self.bstack1llllllll111_opy_()
        }
    def bstack1111llllll_opy_(self):
        return bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ῎")
    def bstack111ll1l1ll_opy_(self, bstack1l111111lll_opy_):
        self.bstack1l111111lll_opy_ = bstack1l111111lll_opy_