# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1ll1l11l11_opy_, bstack11l111l1111_opy_
from bstack_utils.bstack11l11l1lll_opy_ import bstack11111l1llll_opy_
class bstack1111ll1ll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1llllllll11l_opy_=None, bstack11111111111_opy_=True, bstack1l111llll1l_opy_=None, bstack11111l1l_opy_=None, result=None, duration=None, bstack1111lll11l_opy_=None, meta={}):
        self.bstack1111lll11l_opy_ = bstack1111lll11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11111111111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llllllll11l_opy_ = bstack1llllllll11l_opy_
        self.bstack1l111llll1l_opy_ = bstack1l111llll1l_opy_
        self.bstack11111l1l_opy_ = bstack11111l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll1111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1l1l_opy_(self, meta):
        self.meta = meta
    def bstack111llll11l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1llllllllll1_opy_(self):
        bstack1lllllll1l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11ll1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ὎"): bstack1lllllll1l1l_opy_,
            bstack11ll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ὏"): bstack1lllllll1l1l_opy_,
            bstack11ll1l1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ὐ"): bstack1lllllll1l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11ll1l1_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥὑ") + key)
            setattr(self, key, val)
    def bstack1lllllll1lll_opy_(self):
        return {
            bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨὒ"): self.name,
            bstack11ll1l1_opy_ (u"ࠫࡧࡵࡤࡺࠩὓ"): {
                bstack11ll1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪὔ"): bstack11ll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ὕ"),
                bstack11ll1l1_opy_ (u"ࠧࡤࡱࡧࡩࠬὖ"): self.code
            },
            bstack11ll1l1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨὗ"): self.scope,
            bstack11ll1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ὘"): self.tags,
            bstack11ll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ὑ"): self.framework,
            bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ὚"): self.started_at
        }
    def bstack11111111l11_opy_(self):
        return {
         bstack11ll1l1_opy_ (u"ࠬࡳࡥࡵࡣࠪὛ"): self.meta
        }
    def bstack1lllllllll11_opy_(self):
        return {
            bstack11ll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ὜"): {
                bstack11ll1l1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫὝ"): self.bstack1llllllll11l_opy_
            }
        }
    def bstack1llllllll1ll_opy_(self, bstack111111111l1_opy_, details):
        step = next(filter(lambda st: st[bstack11ll1l1_opy_ (u"ࠨ࡫ࡧࠫ὞")] == bstack111111111l1_opy_, self.meta[bstack11ll1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨὟ")]), None)
        step.update(details)
    def bstack1llll1ll_opy_(self, bstack111111111l1_opy_):
        step = next(filter(lambda st: st[bstack11ll1l1_opy_ (u"ࠪ࡭ࡩ࠭ὠ")] == bstack111111111l1_opy_, self.meta[bstack11ll1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪὡ")]), None)
        step.update({
            bstack11ll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩὢ"): bstack1ll1l11l11_opy_()
        })
    def bstack111lll111l_opy_(self, bstack111111111l1_opy_, result, duration=None):
        bstack1l111llll1l_opy_ = bstack1ll1l11l11_opy_()
        if bstack111111111l1_opy_ is not None and self.meta.get(bstack11ll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬὣ")):
            step = next(filter(lambda st: st[bstack11ll1l1_opy_ (u"ࠧࡪࡦࠪὤ")] == bstack111111111l1_opy_, self.meta[bstack11ll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧὥ")]), None)
            step.update({
                bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧὦ"): bstack1l111llll1l_opy_,
                bstack11ll1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬὧ"): duration if duration else bstack11l111l1111_opy_(step[bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨὨ")], bstack1l111llll1l_opy_),
                bstack11ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬὩ"): result.result,
                bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧὪ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllllll1ll1_opy_):
        if self.meta.get(bstack11ll1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭Ὣ")):
            self.meta[bstack11ll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧὬ")].append(bstack1lllllll1ll1_opy_)
        else:
            self.meta[bstack11ll1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨὭ")] = [ bstack1lllllll1ll1_opy_ ]
    def bstack1lllllllllll_opy_(self):
        return {
            bstack11ll1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨὮ"): self.bstack111ll1111l_opy_(),
            **self.bstack1lllllll1lll_opy_(),
            **self.bstack1llllllllll1_opy_(),
            **self.bstack11111111l11_opy_()
        }
    def bstack1111111111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11ll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩὯ"): self.bstack1l111llll1l_opy_,
            bstack11ll1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ὰ"): self.duration,
            bstack11ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ά"): self.result.result
        }
        if data[bstack11ll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧὲ")] == bstack11ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨέ"):
            data[bstack11ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨὴ")] = self.result.bstack11111l1111_opy_()
            data[bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫή")] = [{bstack11ll1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧὶ"): self.result.bstack111llll1111_opy_()}]
        return data
    def bstack1lllllllll1l_opy_(self):
        return {
            bstack11ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪί"): self.bstack111ll1111l_opy_(),
            **self.bstack1lllllll1lll_opy_(),
            **self.bstack1llllllllll1_opy_(),
            **self.bstack1111111111l_opy_(),
            **self.bstack11111111l11_opy_()
        }
    def bstack111l111ll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11ll1l1_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧὸ") in event:
            return self.bstack1lllllllllll_opy_()
        elif bstack11ll1l1_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩό") in event:
            return self.bstack1lllllllll1l_opy_()
    def bstack111l11ll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111llll1l_opy_ = time if time else bstack1ll1l11l11_opy_()
        self.duration = duration if duration else bstack11l111l1111_opy_(self.started_at, self.bstack1l111llll1l_opy_)
        if result:
            self.result = result
class bstack111ll1lll1_opy_(bstack1111ll1ll1_opy_):
    def __init__(self, hooks=[], bstack111ll1l1ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        super().__init__(*args, **kwargs, bstack11111l1l_opy_=bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ὺ"))
    @classmethod
    def bstack1llllllll1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll1l1_opy_ (u"ࠩ࡬ࡨࠬύ"): id(step),
                bstack11ll1l1_opy_ (u"ࠪࡸࡪࡾࡴࠨὼ"): step.name,
                bstack11ll1l1_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬώ"): step.keyword,
            })
        return bstack111ll1lll1_opy_(
            **kwargs,
            meta={
                bstack11ll1l1_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭὾"): {
                    bstack11ll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ὿"): feature.name,
                    bstack11ll1l1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᾀ"): feature.filename,
                    bstack11ll1l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᾁ"): feature.description
                },
                bstack11ll1l1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᾂ"): {
                    bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᾃ"): scenario.name
                },
                bstack11ll1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᾄ"): steps,
                bstack11ll1l1_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᾅ"): bstack11111l1llll_opy_(test)
            }
        )
    def bstack11111111l1l_opy_(self):
        return {
            bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᾆ"): self.hooks
        }
    def bstack111111111ll_opy_(self):
        if self.bstack111ll1l1ll_opy_:
            return {
                bstack11ll1l1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᾇ"): self.bstack111ll1l1ll_opy_
            }
        return {}
    def bstack1lllllllll1l_opy_(self):
        return {
            **super().bstack1lllllllll1l_opy_(),
            **self.bstack11111111l1l_opy_()
        }
    def bstack1lllllllllll_opy_(self):
        return {
            **super().bstack1lllllllllll_opy_(),
            **self.bstack111111111ll_opy_()
        }
    def bstack111l11ll1l_opy_(self):
        return bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᾈ")
class bstack111lllll1l_opy_(bstack1111ll1ll1_opy_):
    def __init__(self, hook_type, *args,bstack111ll1l1ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll111l1111_opy_ = None
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
        super().__init__(*args, **kwargs, bstack11111l1l_opy_=bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᾉ"))
    def bstack111l1l1111_opy_(self):
        return self.hook_type
    def bstack1llllllll111_opy_(self):
        return {
            bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᾊ"): self.hook_type
        }
    def bstack1lllllllll1l_opy_(self):
        return {
            **super().bstack1lllllllll1l_opy_(),
            **self.bstack1llllllll111_opy_()
        }
    def bstack1lllllllllll_opy_(self):
        return {
            **super().bstack1lllllllllll_opy_(),
            bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᾋ"): self.bstack1ll111l1111_opy_,
            **self.bstack1llllllll111_opy_()
        }
    def bstack111l11ll1l_opy_(self):
        return bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᾌ")
    def bstack111lll11ll_opy_(self, bstack1ll111l1111_opy_):
        self.bstack1ll111l1111_opy_ = bstack1ll111l1111_opy_