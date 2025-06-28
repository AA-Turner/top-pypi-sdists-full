# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1llllll1l_opy_, bstack11l11ll1l11_opy_
from bstack_utils.bstack111l1l1l_opy_ import bstack11111l1llll_opy_
class bstack111l11ll11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111111111l1_opy_=None, bstack1lllllllllll_opy_=True, bstack1l111lll11l_opy_=None, bstack1111l1ll1_opy_=None, result=None, duration=None, bstack111l1lll11_opy_=None, meta={}):
        self.bstack111l1lll11_opy_ = bstack111l1lll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllllllllll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111111111l1_opy_ = bstack111111111l1_opy_
        self.bstack1l111lll11l_opy_ = bstack1l111lll11l_opy_
        self.bstack1111l1ll1_opy_ = bstack1111l1ll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l11l1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1l1l_opy_(self, meta):
        self.meta = meta
    def bstack111llll11l_opy_(self, hooks):
        self.hooks = hooks
    def bstack11111111ll1_opy_(self):
        bstack1llllllllll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ὎"): bstack1llllllllll1_opy_,
            bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ὏"): bstack1llllllllll1_opy_,
            bstack1l1ll1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ὐ"): bstack1llllllllll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1ll1_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥὑ") + key)
            setattr(self, key, val)
    def bstack1lllllll1lll_opy_(self):
        return {
            bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨὒ"): self.name,
            bstack1l1ll1_opy_ (u"ࠫࡧࡵࡤࡺࠩὓ"): {
                bstack1l1ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪὔ"): bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ὕ"),
                bstack1l1ll1_opy_ (u"ࠧࡤࡱࡧࡩࠬὖ"): self.code
            },
            bstack1l1ll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨὗ"): self.scope,
            bstack1l1ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ὘"): self.tags,
            bstack1l1ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ὑ"): self.framework,
            bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ὚"): self.started_at
        }
    def bstack1lllllll1ll1_opy_(self):
        return {
         bstack1l1ll1_opy_ (u"ࠬࡳࡥࡵࡣࠪὛ"): self.meta
        }
    def bstack1llllllll1l1_opy_(self):
        return {
            bstack1l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ὜"): {
                bstack1l1ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫὝ"): self.bstack111111111l1_opy_
            }
        }
    def bstack11111111111_opy_(self, bstack1llllllll111_opy_, details):
        step = next(filter(lambda st: st[bstack1l1ll1_opy_ (u"ࠨ࡫ࡧࠫ὞")] == bstack1llllllll111_opy_, self.meta[bstack1l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨὟ")]), None)
        step.update(details)
    def bstack111ll11ll_opy_(self, bstack1llllllll111_opy_):
        step = next(filter(lambda st: st[bstack1l1ll1_opy_ (u"ࠪ࡭ࡩ࠭ὠ")] == bstack1llllllll111_opy_, self.meta[bstack1l1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪὡ")]), None)
        step.update({
            bstack1l1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩὢ"): bstack1llllll1l_opy_()
        })
    def bstack111ll1l11l_opy_(self, bstack1llllllll111_opy_, result, duration=None):
        bstack1l111lll11l_opy_ = bstack1llllll1l_opy_()
        if bstack1llllllll111_opy_ is not None and self.meta.get(bstack1l1ll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬὣ")):
            step = next(filter(lambda st: st[bstack1l1ll1_opy_ (u"ࠧࡪࡦࠪὤ")] == bstack1llllllll111_opy_, self.meta[bstack1l1ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧὥ")]), None)
            step.update({
                bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧὦ"): bstack1l111lll11l_opy_,
                bstack1l1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬὧ"): duration if duration else bstack11l11ll1l11_opy_(step[bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨὨ")], bstack1l111lll11l_opy_),
                bstack1l1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬὩ"): result.result,
                bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧὪ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111111111l_opy_):
        if self.meta.get(bstack1l1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ὣ")):
            self.meta[bstack1l1ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧὬ")].append(bstack1111111111l_opy_)
        else:
            self.meta[bstack1l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨὭ")] = [ bstack1111111111l_opy_ ]
    def bstack111111111ll_opy_(self):
        return {
            bstack1l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨὮ"): self.bstack111l11l1l1_opy_(),
            **self.bstack1lllllll1lll_opy_(),
            **self.bstack11111111ll1_opy_(),
            **self.bstack1lllllll1ll1_opy_()
        }
    def bstack11111111l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩὯ"): self.bstack1l111lll11l_opy_,
            bstack1l1ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ὰ"): self.duration,
            bstack1l1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ά"): self.result.result
        }
        if data[bstack1l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧὲ")] == bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨέ"):
            data[bstack1l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨὴ")] = self.result.bstack11111l11l1_opy_()
            data[bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫή")] = [{bstack1l1ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧὶ"): self.result.bstack11l1l111l1l_opy_()}]
        return data
    def bstack1llllllll11l_opy_(self):
        return {
            bstack1l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪί"): self.bstack111l11l1l1_opy_(),
            **self.bstack1lllllll1lll_opy_(),
            **self.bstack11111111ll1_opy_(),
            **self.bstack11111111l1l_opy_(),
            **self.bstack1lllllll1ll1_opy_()
        }
    def bstack111l1l11ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1ll1_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧὸ") in event:
            return self.bstack111111111ll_opy_()
        elif bstack1l1ll1_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩό") in event:
            return self.bstack1llllllll11l_opy_()
    def bstack111l11llll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111lll11l_opy_ = time if time else bstack1llllll1l_opy_()
        self.duration = duration if duration else bstack11l11ll1l11_opy_(self.started_at, self.bstack1l111lll11l_opy_)
        if result:
            self.result = result
class bstack111lll11l1_opy_(bstack111l11ll11_opy_):
    def __init__(self, hooks=[], bstack111ll1l1ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        super().__init__(*args, **kwargs, bstack1111l1ll1_opy_=bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ὺ"))
    @classmethod
    def bstack1lllllllll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1ll1_opy_ (u"ࠩ࡬ࡨࠬύ"): id(step),
                bstack1l1ll1_opy_ (u"ࠪࡸࡪࡾࡴࠨὼ"): step.name,
                bstack1l1ll1_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬώ"): step.keyword,
            })
        return bstack111lll11l1_opy_(
            **kwargs,
            meta={
                bstack1l1ll1_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭὾"): {
                    bstack1l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ὿"): feature.name,
                    bstack1l1ll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᾀ"): feature.filename,
                    bstack1l1ll1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᾁ"): feature.description
                },
                bstack1l1ll1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᾂ"): {
                    bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᾃ"): scenario.name
                },
                bstack1l1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᾄ"): steps,
                bstack1l1ll1_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᾅ"): bstack11111l1llll_opy_(test)
            }
        )
    def bstack11111111l11_opy_(self):
        return {
            bstack1l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᾆ"): self.hooks
        }
    def bstack1lllllllll11_opy_(self):
        if self.bstack111ll1l1ll_opy_:
            return {
                bstack1l1ll1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᾇ"): self.bstack111ll1l1ll_opy_
            }
        return {}
    def bstack1llllllll11l_opy_(self):
        return {
            **super().bstack1llllllll11l_opy_(),
            **self.bstack11111111l11_opy_()
        }
    def bstack111111111ll_opy_(self):
        return {
            **super().bstack111111111ll_opy_(),
            **self.bstack1lllllllll11_opy_()
        }
    def bstack111l11llll_opy_(self):
        return bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᾈ")
class bstack111ll1l111_opy_(bstack111l11ll11_opy_):
    def __init__(self, hook_type, *args,bstack111ll1l1ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1l1l1111_opy_ = None
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        super().__init__(*args, **kwargs, bstack1111l1ll1_opy_=bstack1l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᾉ"))
    def bstack1111ll1ll1_opy_(self):
        return self.hook_type
    def bstack1llllllll1ll_opy_(self):
        return {
            bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᾊ"): self.hook_type
        }
    def bstack1llllllll11l_opy_(self):
        return {
            **super().bstack1llllllll11l_opy_(),
            **self.bstack1llllllll1ll_opy_()
        }
    def bstack111111111ll_opy_(self):
        return {
            **super().bstack111111111ll_opy_(),
            bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᾋ"): self.bstack1ll1l1l1111_opy_,
            **self.bstack1llllllll1ll_opy_()
        }
    def bstack111l11llll_opy_(self):
        return bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᾌ")
    def bstack111ll11lll_opy_(self, bstack1ll1l1l1111_opy_):
        self.bstack1ll1l1l1111_opy_ = bstack1ll1l1l1111_opy_