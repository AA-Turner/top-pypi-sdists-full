# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1ll1ll1l1_opy_, bstack111lll1ll1l_opy_
from bstack_utils.bstack1l1l11111_opy_ import bstack111111lll11_opy_
class bstack1111ll1lll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllllll1l11_opy_=None, bstack1llllllll111_opy_=True, bstack1l111lll1ll_opy_=None, bstack1l1l11l1ll_opy_=None, result=None, duration=None, bstack111l1lll11_opy_=None, meta={}):
        self.bstack111l1lll11_opy_ = bstack111l1lll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llllllll111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllllll1l11_opy_ = bstack1lllllll1l11_opy_
        self.bstack1l111lll1ll_opy_ = bstack1l111lll1ll_opy_
        self.bstack1l1l11l1ll_opy_ = bstack1l1l11l1ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1ll1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111ll111l1_opy_(self, meta):
        self.meta = meta
    def bstack111lll1111_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllllll111l_opy_(self):
        bstack1llllllll1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111l111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᾔ"): bstack1llllllll1ll_opy_,
            bstack111l111_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᾕ"): bstack1llllllll1ll_opy_,
            bstack111l111_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᾖ"): bstack1llllllll1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111l111_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥᾗ") + key)
            setattr(self, key, val)
    def bstack1lllllll1111_opy_(self):
        return {
            bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨᾘ"): self.name,
            bstack111l111_opy_ (u"ࠫࡧࡵࡤࡺࠩᾙ"): {
                bstack111l111_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᾚ"): bstack111l111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᾛ"),
                bstack111l111_opy_ (u"ࠧࡤࡱࡧࡩࠬᾜ"): self.code
            },
            bstack111l111_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᾝ"): self.scope,
            bstack111l111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᾞ"): self.tags,
            bstack111l111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᾟ"): self.framework,
            bstack111l111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᾠ"): self.started_at
        }
    def bstack1lllllll11l1_opy_(self):
        return {
         bstack111l111_opy_ (u"ࠬࡳࡥࡵࡣࠪᾡ"): self.meta
        }
    def bstack1llllllll11l_opy_(self):
        return {
            bstack111l111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᾢ"): {
                bstack111l111_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᾣ"): self.bstack1lllllll1l11_opy_
            }
        }
    def bstack1llllllllll1_opy_(self, bstack1lllllllll1l_opy_, details):
        step = next(filter(lambda st: st[bstack111l111_opy_ (u"ࠨ࡫ࡧࠫᾤ")] == bstack1lllllllll1l_opy_, self.meta[bstack111l111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾥ")]), None)
        step.update(details)
    def bstack1l1l1l11l1_opy_(self, bstack1lllllllll1l_opy_):
        step = next(filter(lambda st: st[bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭ᾦ")] == bstack1lllllllll1l_opy_, self.meta[bstack111l111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᾧ")]), None)
        step.update({
            bstack111l111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾨ"): bstack1ll1ll1l1_opy_()
        })
    def bstack111ll11lll_opy_(self, bstack1lllllllll1l_opy_, result, duration=None):
        bstack1l111lll1ll_opy_ = bstack1ll1ll1l1_opy_()
        if bstack1lllllllll1l_opy_ is not None and self.meta.get(bstack111l111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᾩ")):
            step = next(filter(lambda st: st[bstack111l111_opy_ (u"ࠧࡪࡦࠪᾪ")] == bstack1lllllllll1l_opy_, self.meta[bstack111l111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᾫ")]), None)
            step.update({
                bstack111l111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᾬ"): bstack1l111lll1ll_opy_,
                bstack111l111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᾭ"): duration if duration else bstack111lll1ll1l_opy_(step[bstack111l111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᾮ")], bstack1l111lll1ll_opy_),
                bstack111l111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᾯ"): result.result,
                bstack111l111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᾰ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllllll1ll1_opy_):
        if self.meta.get(bstack111l111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᾱ")):
            self.meta[bstack111l111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᾲ")].append(bstack1lllllll1ll1_opy_)
        else:
            self.meta[bstack111l111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾳ")] = [ bstack1lllllll1ll1_opy_ ]
    def bstack1llllll1llll_opy_(self):
        return {
            bstack111l111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᾴ"): self.bstack111l1ll1l1_opy_(),
            **self.bstack1lllllll1111_opy_(),
            **self.bstack1lllllll111l_opy_(),
            **self.bstack1lllllll11l1_opy_()
        }
    def bstack1lllllllllll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111l111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᾵"): self.bstack1l111lll1ll_opy_,
            bstack111l111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᾶ"): self.duration,
            bstack111l111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᾷ"): self.result.result
        }
        if data[bstack111l111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᾸ")] == bstack111l111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᾹ"):
            data[bstack111l111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᾺ")] = self.result.bstack111111llll_opy_()
            data[bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫΆ")] = [{bstack111l111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᾼ"): self.result.bstack11l1111ll1l_opy_()}]
        return data
    def bstack1lllllll11ll_opy_(self):
        return {
            bstack111l111_opy_ (u"ࠬࡻࡵࡪࡦࠪ᾽"): self.bstack111l1ll1l1_opy_(),
            **self.bstack1lllllll1111_opy_(),
            **self.bstack1lllllll111l_opy_(),
            **self.bstack1lllllllllll_opy_(),
            **self.bstack1lllllll11l1_opy_()
        }
    def bstack111l1l1ll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111l111_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧι") in event:
            return self.bstack1llllll1llll_opy_()
        elif bstack111l111_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ᾿") in event:
            return self.bstack1lllllll11ll_opy_()
    def bstack111l111111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111lll1ll_opy_ = time if time else bstack1ll1ll1l1_opy_()
        self.duration = duration if duration else bstack111lll1ll1l_opy_(self.started_at, self.bstack1l111lll1ll_opy_)
        if result:
            self.result = result
class bstack111ll111ll_opy_(bstack1111ll1lll_opy_):
    def __init__(self, hooks=[], bstack111llll111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111llll111_opy_ = bstack111llll111_opy_
        super().__init__(*args, **kwargs, bstack1l1l11l1ll_opy_=bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹ࠭῀"))
    @classmethod
    def bstack1lllllllll11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l111_opy_ (u"ࠩ࡬ࡨࠬ῁"): id(step),
                bstack111l111_opy_ (u"ࠪࡸࡪࡾࡴࠨῂ"): step.name,
                bstack111l111_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬῃ"): step.keyword,
            })
        return bstack111ll111ll_opy_(
            **kwargs,
            meta={
                bstack111l111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ῄ"): {
                    bstack111l111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ῅"): feature.name,
                    bstack111l111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬῆ"): feature.filename,
                    bstack111l111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ῇ"): feature.description
                },
                bstack111l111_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫῈ"): {
                    bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨΈ"): scenario.name
                },
                bstack111l111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪῊ"): steps,
                bstack111l111_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧΉ"): bstack111111lll11_opy_(test)
            }
        )
    def bstack1lllllll1lll_opy_(self):
        return {
            bstack111l111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬῌ"): self.hooks
        }
    def bstack1llllllll1l1_opy_(self):
        if self.bstack111llll111_opy_:
            return {
                bstack111l111_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭῍"): self.bstack111llll111_opy_
            }
        return {}
    def bstack1lllllll11ll_opy_(self):
        return {
            **super().bstack1lllllll11ll_opy_(),
            **self.bstack1lllllll1lll_opy_()
        }
    def bstack1llllll1llll_opy_(self):
        return {
            **super().bstack1llllll1llll_opy_(),
            **self.bstack1llllllll1l1_opy_()
        }
    def bstack111l111111_opy_(self):
        return bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ῎")
class bstack111ll1ll11_opy_(bstack1111ll1lll_opy_):
    def __init__(self, hook_type, *args,bstack111llll111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1l1111l1_opy_ = None
        self.bstack111llll111_opy_ = bstack111llll111_opy_
        super().__init__(*args, **kwargs, bstack1l1l11l1ll_opy_=bstack111l111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ῏"))
    def bstack111l1111ll_opy_(self):
        return self.hook_type
    def bstack1lllllll1l1l_opy_(self):
        return {
            bstack111l111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ῐ"): self.hook_type
        }
    def bstack1lllllll11ll_opy_(self):
        return {
            **super().bstack1lllllll11ll_opy_(),
            **self.bstack1lllllll1l1l_opy_()
        }
    def bstack1llllll1llll_opy_(self):
        return {
            **super().bstack1llllll1llll_opy_(),
            bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩῑ"): self.bstack1ll1l1111l1_opy_,
            **self.bstack1lllllll1l1l_opy_()
        }
    def bstack111l111111_opy_(self):
        return bstack111l111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧῒ")
    def bstack111ll1l1l1_opy_(self, bstack1ll1l1111l1_opy_):
        self.bstack1ll1l1111l1_opy_ = bstack1ll1l1111l1_opy_