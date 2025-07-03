# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack111ll11ll_opy_, bstack11l11lll111_opy_
from bstack_utils.bstack1ll11l1l1_opy_ import bstack111111lllll_opy_
class bstack1111ll1l1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1llllllll1ll_opy_=None, bstack1111111111l_opy_=True, bstack1l11l11111l_opy_=None, bstack1l111111l_opy_=None, result=None, duration=None, bstack111l1ll1ll_opy_=None, meta={}):
        self.bstack111l1ll1ll_opy_ = bstack111l1ll1ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111111111l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llllllll1ll_opy_ = bstack1llllllll1ll_opy_
        self.bstack1l11l11111l_opy_ = bstack1l11l11111l_opy_
        self.bstack1l111111l_opy_ = bstack1l111111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l11l111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1l1l_opy_(self, meta):
        self.meta = meta
    def bstack111ll1l1l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllllll1l11_opy_(self):
        bstack1lllllllll11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᾎ"): bstack1lllllllll11_opy_,
            bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᾏ"): bstack1lllllllll11_opy_,
            bstack1l1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᾐ"): bstack1lllllllll11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦᾑ") + key)
            setattr(self, key, val)
    def bstack1lllllllllll_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᾒ"): self.name,
            bstack1l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᾓ"): {
                bstack1l1_opy_ (u"࠭࡬ࡢࡰࡪࠫᾔ"): bstack1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᾕ"),
                bstack1l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᾖ"): self.code
            },
            bstack1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᾗ"): self.scope,
            bstack1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᾘ"): self.tags,
            bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᾙ"): self.framework,
            bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾚ"): self.started_at
        }
    def bstack1llllllll111_opy_(self):
        return {
         bstack1l1_opy_ (u"࠭࡭ࡦࡶࡤࠫᾛ"): self.meta
        }
    def bstack1llllllll11l_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᾜ"): {
                bstack1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᾝ"): self.bstack1llllllll1ll_opy_
            }
        }
    def bstack1lllllll11ll_opy_(self, bstack1lllllll1l1l_opy_, details):
        step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠩ࡬ࡨࠬᾞ")] == bstack1lllllll1l1l_opy_, self.meta[bstack1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᾟ")]), None)
        step.update(details)
    def bstack11llll11l_opy_(self, bstack1lllllll1l1l_opy_):
        step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠫ࡮ࡪࠧᾠ")] == bstack1lllllll1l1l_opy_, self.meta[bstack1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᾡ")]), None)
        step.update({
            bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᾢ"): bstack111ll11ll_opy_()
        })
    def bstack111llll111_opy_(self, bstack1lllllll1l1l_opy_, result, duration=None):
        bstack1l11l11111l_opy_ = bstack111ll11ll_opy_()
        if bstack1lllllll1l1l_opy_ is not None and self.meta.get(bstack1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᾣ")):
            step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠨ࡫ࡧࠫᾤ")] == bstack1lllllll1l1l_opy_, self.meta[bstack1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾥ")]), None)
            step.update({
                bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᾦ"): bstack1l11l11111l_opy_,
                bstack1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᾧ"): duration if duration else bstack11l11lll111_opy_(step[bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᾨ")], bstack1l11l11111l_opy_),
                bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᾩ"): result.result,
                bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᾪ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llllllll1l1_opy_):
        if self.meta.get(bstack1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᾫ")):
            self.meta[bstack1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᾬ")].append(bstack1llllllll1l1_opy_)
        else:
            self.meta[bstack1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᾭ")] = [ bstack1llllllll1l1_opy_ ]
    def bstack1llllllllll1_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᾮ"): self.bstack111l11l111_opy_(),
            **self.bstack1lllllllllll_opy_(),
            **self.bstack1lllllll1l11_opy_(),
            **self.bstack1llllllll111_opy_()
        }
    def bstack1lllllll1lll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᾯ"): self.bstack1l11l11111l_opy_,
            bstack1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᾰ"): self.duration,
            bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᾱ"): self.result.result
        }
        if data[bstack1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᾲ")] == bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᾳ"):
            data[bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᾴ")] = self.result.bstack111111ll1l_opy_()
            data[bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᾵")] = [{bstack1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᾶ"): self.result.bstack11l111l1111_opy_()}]
        return data
    def bstack1lllllll11l1_opy_(self):
        return {
            bstack1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᾷ"): self.bstack111l11l111_opy_(),
            **self.bstack1lllllllllll_opy_(),
            **self.bstack1lllllll1l11_opy_(),
            **self.bstack1lllllll1lll_opy_(),
            **self.bstack1llllllll111_opy_()
        }
    def bstack111l1111ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨᾸ") in event:
            return self.bstack1llllllllll1_opy_()
        elif bstack1l1_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᾹ") in event:
            return self.bstack1lllllll11l1_opy_()
    def bstack111l1llll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l11111l_opy_ = time if time else bstack111ll11ll_opy_()
        self.duration = duration if duration else bstack11l11lll111_opy_(self.started_at, self.bstack1l11l11111l_opy_)
        if result:
            self.result = result
class bstack111lll1111_opy_(bstack1111ll1l1l_opy_):
    def __init__(self, hooks=[], bstack111ll1l1ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        super().__init__(*args, **kwargs, bstack1l111111l_opy_=bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧᾺ"))
    @classmethod
    def bstack1lllllll1ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1_opy_ (u"ࠪ࡭ࡩ࠭Ά"): id(step),
                bstack1l1_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᾼ"): step.name,
                bstack1l1_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭᾽"): step.keyword,
            })
        return bstack111lll1111_opy_(
            **kwargs,
            meta={
                bstack1l1_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧι"): {
                    bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᾿"): feature.name,
                    bstack1l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭῀"): feature.filename,
                    bstack1l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ῁"): feature.description
                },
                bstack1l1_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬῂ"): {
                    bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩῃ"): scenario.name
                },
                bstack1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫῄ"): steps,
                bstack1l1_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ῅"): bstack111111lllll_opy_(test)
            }
        )
    def bstack1lllllllll1l_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ῆ"): self.hooks
        }
    def bstack11111111111_opy_(self):
        if self.bstack111ll1l1ll_opy_:
            return {
                bstack1l1_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧῇ"): self.bstack111ll1l1ll_opy_
            }
        return {}
    def bstack1lllllll11l1_opy_(self):
        return {
            **super().bstack1lllllll11l1_opy_(),
            **self.bstack1lllllllll1l_opy_()
        }
    def bstack1llllllllll1_opy_(self):
        return {
            **super().bstack1llllllllll1_opy_(),
            **self.bstack11111111111_opy_()
        }
    def bstack111l1llll1_opy_(self):
        return bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫῈ")
class bstack111lll111l_opy_(bstack1111ll1l1l_opy_):
    def __init__(self, hook_type, *args,bstack111ll1l1ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11l1lll1_opy_ = None
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        super().__init__(*args, **kwargs, bstack1l111111l_opy_=bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨΈ"))
    def bstack111l111111_opy_(self):
        return self.hook_type
    def bstack1lllllll111l_opy_(self):
        return {
            bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧῊ"): self.hook_type
        }
    def bstack1lllllll11l1_opy_(self):
        return {
            **super().bstack1lllllll11l1_opy_(),
            **self.bstack1lllllll111l_opy_()
        }
    def bstack1llllllllll1_opy_(self):
        return {
            **super().bstack1llllllllll1_opy_(),
            bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪΉ"): self.bstack1ll11l1lll1_opy_,
            **self.bstack1lllllll111l_opy_()
        }
    def bstack111l1llll1_opy_(self):
        return bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨῌ")
    def bstack111ll111ll_opy_(self, bstack1ll11l1lll1_opy_):
        self.bstack1ll11l1lll1_opy_ = bstack1ll11l1lll1_opy_