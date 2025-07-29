# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lll111111_opy_, bstack11l1111ll1l_opy_
from bstack_utils.bstack1l1l1l111_opy_ import bstack11111l111ll_opy_
class bstack1111ll1l1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllllll11ll_opy_=None, bstack1lllllll11l1_opy_=True, bstack1l1111l111l_opy_=None, bstack1l111ll111_opy_=None, result=None, duration=None, bstack111l111111_opy_=None, meta={}):
        self.bstack111l111111_opy_ = bstack111l111111_opy_
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
        self.bstack1lllllll11ll_opy_ = bstack1lllllll11ll_opy_
        self.bstack1l1111l111l_opy_ = bstack1l1111l111l_opy_
        self.bstack1l111ll111_opy_ = bstack1l111ll111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111lll1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111ll1l111_opy_(self, meta):
        self.meta = meta
    def bstack111lll1l11_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllllll1l11_opy_(self):
        bstack1lllllllll1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᾕ"): bstack1lllllllll1l_opy_,
            bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᾖ"): bstack1lllllllll1l_opy_,
            bstackl_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᾗ"): bstack1lllllllll1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstackl_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦᾘ") + key)
            setattr(self, key, val)
    def bstack1lllllll1111_opy_(self):
        return {
            bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᾙ"): self.name,
            bstackl_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᾚ"): {
                bstackl_opy_ (u"࠭࡬ࡢࡰࡪࠫᾛ"): bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᾜ"),
                bstackl_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᾝ"): self.code
            },
            bstackl_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᾞ"): self.scope,
            bstackl_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᾟ"): self.tags,
            bstackl_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᾠ"): self.framework,
            bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾡ"): self.started_at
        }
    def bstack1llllllll1ll_opy_(self):
        return {
         bstackl_opy_ (u"࠭࡭ࡦࡶࡤࠫᾢ"): self.meta
        }
    def bstack1llllllll1l1_opy_(self):
        return {
            bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᾣ"): {
                bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᾤ"): self.bstack1lllllll11ll_opy_
            }
        }
    def bstack1lllllll1lll_opy_(self, bstack1lllllll111l_opy_, details):
        step = next(filter(lambda st: st[bstackl_opy_ (u"ࠩ࡬ࡨࠬᾥ")] == bstack1lllllll111l_opy_, self.meta[bstackl_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᾦ")]), None)
        step.update(details)
    def bstack1ll1lll1l_opy_(self, bstack1lllllll111l_opy_):
        step = next(filter(lambda st: st[bstackl_opy_ (u"ࠫ࡮ࡪࠧᾧ")] == bstack1lllllll111l_opy_, self.meta[bstackl_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᾨ")]), None)
        step.update({
            bstackl_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᾩ"): bstack1lll111111_opy_()
        })
    def bstack111ll1l11l_opy_(self, bstack1lllllll111l_opy_, result, duration=None):
        bstack1l1111l111l_opy_ = bstack1lll111111_opy_()
        if bstack1lllllll111l_opy_ is not None and self.meta.get(bstackl_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᾪ")):
            step = next(filter(lambda st: st[bstackl_opy_ (u"ࠨ࡫ࡧࠫᾫ")] == bstack1lllllll111l_opy_, self.meta[bstackl_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾬ")]), None)
            step.update({
                bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᾭ"): bstack1l1111l111l_opy_,
                bstackl_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᾮ"): duration if duration else bstack11l1111ll1l_opy_(step[bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾯ")], bstack1l1111l111l_opy_),
                bstackl_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᾰ"): result.result,
                bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᾱ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llllllll11l_opy_):
        if self.meta.get(bstackl_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᾲ")):
            self.meta[bstackl_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾳ")].append(bstack1llllllll11l_opy_)
        else:
            self.meta[bstackl_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᾴ")] = [ bstack1llllllll11l_opy_ ]
    def bstack1llllllll111_opy_(self):
        return {
            bstackl_opy_ (u"ࠫࡺࡻࡩࡥࠩ᾵"): self.bstack1111lll1l1_opy_(),
            **self.bstack1lllllll1111_opy_(),
            **self.bstack1lllllll1l11_opy_(),
            **self.bstack1llllllll1ll_opy_()
        }
    def bstack1llllll1lll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstackl_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᾶ"): self.bstack1l1111l111l_opy_,
            bstackl_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᾷ"): self.duration,
            bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᾸ"): self.result.result
        }
        if data[bstackl_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᾹ")] == bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᾺ"):
            data[bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩΆ")] = self.result.bstack111111ll11_opy_()
            data[bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᾼ")] = [{bstackl_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ᾽"): self.result.bstack111llllllll_opy_()}]
        return data
    def bstack1lllllll1ll1_opy_(self):
        return {
            bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫι"): self.bstack1111lll1l1_opy_(),
            **self.bstack1lllllll1111_opy_(),
            **self.bstack1lllllll1l11_opy_(),
            **self.bstack1llllll1lll1_opy_(),
            **self.bstack1llllllll1ll_opy_()
        }
    def bstack111l111lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstackl_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ᾿") in event:
            return self.bstack1llllllll111_opy_()
        elif bstackl_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ῀") in event:
            return self.bstack1lllllll1ll1_opy_()
    def bstack111l11l11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1111l111l_opy_ = time if time else bstack1lll111111_opy_()
        self.duration = duration if duration else bstack11l1111ll1l_opy_(self.started_at, self.bstack1l1111l111l_opy_)
        if result:
            self.result = result
class bstack111ll111l1_opy_(bstack1111ll1l1l_opy_):
    def __init__(self, hooks=[], bstack111lll1lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lll1lll_opy_ = bstack111lll1lll_opy_
        super().__init__(*args, **kwargs, bstack1l111ll111_opy_=bstackl_opy_ (u"ࠩࡷࡩࡸࡺࠧ῁"))
    @classmethod
    def bstack1lllllll1l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstackl_opy_ (u"ࠪ࡭ࡩ࠭ῂ"): id(step),
                bstackl_opy_ (u"ࠫࡹ࡫ࡸࡵࠩῃ"): step.name,
                bstackl_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ῄ"): step.keyword,
            })
        return bstack111ll111l1_opy_(
            **kwargs,
            meta={
                bstackl_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ῅"): {
                    bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬῆ"): feature.name,
                    bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭ῇ"): feature.filename,
                    bstackl_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧῈ"): feature.description
                },
                bstackl_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬΈ"): {
                    bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩῊ"): scenario.name
                },
                bstackl_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫΉ"): steps,
                bstackl_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨῌ"): bstack11111l111ll_opy_(test)
            }
        )
    def bstack1llllll1llll_opy_(self):
        return {
            bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭῍"): self.hooks
        }
    def bstack1llllllllll1_opy_(self):
        if self.bstack111lll1lll_opy_:
            return {
                bstackl_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ῎"): self.bstack111lll1lll_opy_
            }
        return {}
    def bstack1lllllll1ll1_opy_(self):
        return {
            **super().bstack1lllllll1ll1_opy_(),
            **self.bstack1llllll1llll_opy_()
        }
    def bstack1llllllll111_opy_(self):
        return {
            **super().bstack1llllllll111_opy_(),
            **self.bstack1llllllllll1_opy_()
        }
    def bstack111l11l11l_opy_(self):
        return bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ῏")
class bstack111ll11l1l_opy_(bstack1111ll1l1l_opy_):
    def __init__(self, hook_type, *args,bstack111lll1lll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1l1111ll_opy_ = None
        self.bstack111lll1lll_opy_ = bstack111lll1lll_opy_
        super().__init__(*args, **kwargs, bstack1l111ll111_opy_=bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨῐ"))
    def bstack1111ll1lll_opy_(self):
        return self.hook_type
    def bstack1lllllllll11_opy_(self):
        return {
            bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧῑ"): self.hook_type
        }
    def bstack1lllllll1ll1_opy_(self):
        return {
            **super().bstack1lllllll1ll1_opy_(),
            **self.bstack1lllllllll11_opy_()
        }
    def bstack1llllllll111_opy_(self):
        return {
            **super().bstack1llllllll111_opy_(),
            bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪῒ"): self.bstack1ll1l1111ll_opy_,
            **self.bstack1lllllllll11_opy_()
        }
    def bstack111l11l11l_opy_(self):
        return bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨΐ")
    def bstack111ll111ll_opy_(self, bstack1ll1l1111ll_opy_):
        self.bstack1ll1l1111ll_opy_ = bstack1ll1l1111ll_opy_