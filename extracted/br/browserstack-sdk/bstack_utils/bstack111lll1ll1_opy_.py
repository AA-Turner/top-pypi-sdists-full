# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l11l11ll_opy_, bstack11l1l11l1ll_opy_
from bstack_utils.bstack1l1lllllll_opy_ import bstack11111ll1l11_opy_
class bstack111l111lll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack11111111lll_opy_=None, bstack111111111l1_opy_=True, bstack1l111l1ll1l_opy_=None, bstack1l1ll11l1l_opy_=None, result=None, duration=None, bstack111l11l1ll_opy_=None, meta={}):
        self.bstack111l11l1ll_opy_ = bstack111l11l1ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111111111l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11111111lll_opy_ = bstack11111111lll_opy_
        self.bstack1l111l1ll1l_opy_ = bstack1l111l1ll1l_opy_
        self.bstack1l1ll11l1l_opy_ = bstack1l1ll11l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1ll1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1l1l_opy_(self, meta):
        self.meta = meta
    def bstack111llll1ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack11111111l1l_opy_(self):
        bstack1111111l1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫἭ"): bstack1111111l1ll_opy_,
            bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫἮ"): bstack1111111l1ll_opy_,
            bstack11ll11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨἯ"): bstack1111111l1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11ll11_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧἰ") + key)
            setattr(self, key, val)
    def bstack1111111l1l1_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἱ"): self.name,
            bstack11ll11_opy_ (u"࠭ࡢࡰࡦࡼࠫἲ"): {
                bstack11ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬἳ"): bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨἴ"),
                bstack11ll11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧἵ"): self.code
            },
            bstack11ll11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪἶ"): self.scope,
            bstack11ll11_opy_ (u"ࠫࡹࡧࡧࡴࠩἷ"): self.tags,
            bstack11ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨἸ"): self.framework,
            bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪἹ"): self.started_at
        }
    def bstack111111111ll_opy_(self):
        return {
         bstack11ll11_opy_ (u"ࠧ࡮ࡧࡷࡥࠬἺ"): self.meta
        }
    def bstack1lllllllllll_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫἻ"): {
                bstack11ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭Ἴ"): self.bstack11111111lll_opy_
            }
        }
    def bstack1lllllllll11_opy_(self, bstack1llllllllll1_opy_, details):
        step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠪ࡭ࡩ࠭Ἵ")] == bstack1llllllllll1_opy_, self.meta[bstack11ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪἾ")]), None)
        step.update(details)
    def bstack11l1llll11_opy_(self, bstack1llllllllll1_opy_):
        step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠬ࡯ࡤࠨἿ")] == bstack1llllllllll1_opy_, self.meta[bstack11ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬὀ")]), None)
        step.update({
            bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫὁ"): bstack1l11l11ll_opy_()
        })
    def bstack111ll1ll11_opy_(self, bstack1llllllllll1_opy_, result, duration=None):
        bstack1l111l1ll1l_opy_ = bstack1l11l11ll_opy_()
        if bstack1llllllllll1_opy_ is not None and self.meta.get(bstack11ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧὂ")):
            step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬὃ")] == bstack1llllllllll1_opy_, self.meta[bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩὄ")]), None)
            step.update({
                bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩὅ"): bstack1l111l1ll1l_opy_,
                bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ὆"): duration if duration else bstack11l1l11l1ll_opy_(step[bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ὇")], bstack1l111l1ll1l_opy_),
                bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧὈ"): result.result,
                bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩὉ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llllllll1ll_opy_):
        if self.meta.get(bstack11ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨὊ")):
            self.meta[bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩὋ")].append(bstack1llllllll1ll_opy_)
        else:
            self.meta[bstack11ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪὌ")] = [ bstack1llllllll1ll_opy_ ]
    def bstack1111111l111_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪὍ"): self.bstack111l1ll1l1_opy_(),
            **self.bstack1111111l1l1_opy_(),
            **self.bstack11111111l1l_opy_(),
            **self.bstack111111111ll_opy_()
        }
    def bstack1lllllllll1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ὎"): self.bstack1l111l1ll1l_opy_,
            bstack11ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ὏"): self.duration,
            bstack11ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨὐ"): self.result.result
        }
        if data[bstack11ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩὑ")] == bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪὒ"):
            data[bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪὓ")] = self.result.bstack11111l111l_opy_()
            data[bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ὔ")] = [{bstack11ll11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩὕ"): self.result.bstack111lll1llll_opy_()}]
        return data
    def bstack1111111111l_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬὖ"): self.bstack111l1ll1l1_opy_(),
            **self.bstack1111111l1l1_opy_(),
            **self.bstack11111111l1l_opy_(),
            **self.bstack1lllllllll1l_opy_(),
            **self.bstack111111111ll_opy_()
        }
    def bstack111l1l11ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11ll11_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩὗ") in event:
            return self.bstack1111111l111_opy_()
        elif bstack11ll11_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ὘") in event:
            return self.bstack1111111111l_opy_()
    def bstack111l1ll11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111l1ll1l_opy_ = time if time else bstack1l11l11ll_opy_()
        self.duration = duration if duration else bstack11l1l11l1ll_opy_(self.started_at, self.bstack1l111l1ll1l_opy_)
        if result:
            self.result = result
class bstack111ll11ll1_opy_(bstack111l111lll_opy_):
    def __init__(self, hooks=[], bstack111lll11l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lll11l1_opy_ = bstack111lll11l1_opy_
        super().__init__(*args, **kwargs, bstack1l1ll11l1l_opy_=bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࠨὙ"))
    @classmethod
    def bstack11111111ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧ὚"): id(step),
                bstack11ll11_opy_ (u"ࠬࡺࡥࡹࡶࠪὛ"): step.name,
                bstack11ll11_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ὜"): step.keyword,
            })
        return bstack111ll11ll1_opy_(
            **kwargs,
            meta={
                bstack11ll11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨὝ"): {
                    bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭὞"): feature.name,
                    bstack11ll11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧὟ"): feature.filename,
                    bstack11ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨὠ"): feature.description
                },
                bstack11ll11_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ὡ"): {
                    bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪὢ"): scenario.name
                },
                bstack11ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬὣ"): steps,
                bstack11ll11_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩὤ"): bstack11111ll1l11_opy_(test)
            }
        )
    def bstack11111111111_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧὥ"): self.hooks
        }
    def bstack11111111l11_opy_(self):
        if self.bstack111lll11l1_opy_:
            return {
                bstack11ll11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨὦ"): self.bstack111lll11l1_opy_
            }
        return {}
    def bstack1111111111l_opy_(self):
        return {
            **super().bstack1111111111l_opy_(),
            **self.bstack11111111111_opy_()
        }
    def bstack1111111l111_opy_(self):
        return {
            **super().bstack1111111l111_opy_(),
            **self.bstack11111111l11_opy_()
        }
    def bstack111l1ll11l_opy_(self):
        return bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬὧ")
class bstack111lll11ll_opy_(bstack111l111lll_opy_):
    def __init__(self, hook_type, *args,bstack111lll11l1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111111ll11_opy_ = None
        self.bstack111lll11l1_opy_ = bstack111lll11l1_opy_
        super().__init__(*args, **kwargs, bstack1l1ll11l1l_opy_=bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩὨ"))
    def bstack111l1111l1_opy_(self):
        return self.hook_type
    def bstack1111111l11l_opy_(self):
        return {
            bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨὩ"): self.hook_type
        }
    def bstack1111111111l_opy_(self):
        return {
            **super().bstack1111111111l_opy_(),
            **self.bstack1111111l11l_opy_()
        }
    def bstack1111111l111_opy_(self):
        return {
            **super().bstack1111111l111_opy_(),
            bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫὪ"): self.bstack1111111ll11_opy_,
            **self.bstack1111111l11l_opy_()
        }
    def bstack111l1ll11l_opy_(self):
        return bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩὫ")
    def bstack111lll1lll_opy_(self, bstack1111111ll11_opy_):
        self.bstack1111111ll11_opy_ = bstack1111111ll11_opy_