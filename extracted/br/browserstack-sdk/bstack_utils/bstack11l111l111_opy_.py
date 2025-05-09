# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11ll11l1ll_opy_, bstack11l1l1ll1l1_opy_
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack111l1l1l1ll_opy_
class bstack111l11l1l1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111llllll1_opy_=None, bstack1111llll1l1_opy_=True, bstack1l111lllll1_opy_=None, bstack1llllllll1_opy_=None, result=None, duration=None, bstack111ll1l1l1_opy_=None, meta={}):
        self.bstack111ll1l1l1_opy_ = bstack111ll1l1l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111llll1l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111llllll1_opy_ = bstack1111llllll1_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.bstack1llllllll1_opy_ = bstack1llllllll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll1llll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111ll1l_opy_(self, meta):
        self.meta = meta
    def bstack111llll1ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l11111l1_opy_(self):
        bstack1111lllll11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ᷌"): bstack1111lllll11_opy_,
            bstack11lll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ᷍"): bstack1111lllll11_opy_,
            bstack11lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬᷎ࠬ"): bstack1111lllll11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11lll_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤ᷏") + key)
            setattr(self, key, val)
    def bstack1111lll1l11_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫᷐ࠧ"): self.name,
            bstack11lll_opy_ (u"ࠪࡦࡴࡪࡹࠨ᷑"): {
                bstack11lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ᷒"): bstack11lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᷓ"),
                bstack11lll_opy_ (u"࠭ࡣࡰࡦࡨࠫᷔ"): self.code
            },
            bstack11lll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᷕ"): self.scope,
            bstack11lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᷖ"): self.tags,
            bstack11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᷗ"): self.framework,
            bstack11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᷘ"): self.started_at
        }
    def bstack1111llll111_opy_(self):
        return {
         bstack11lll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᷙ"): self.meta
        }
    def bstack1111lll1ll1_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᷚ"): {
                bstack11lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᷛ"): self.bstack1111llllll1_opy_
            }
        }
    def bstack1111llll11l_opy_(self, bstack1111lllll1l_opy_, details):
        step = next(filter(lambda st: st[bstack11lll_opy_ (u"ࠧࡪࡦࠪᷜ")] == bstack1111lllll1l_opy_, self.meta[bstack11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷝ")]), None)
        step.update(details)
    def bstack111l1llll_opy_(self, bstack1111lllll1l_opy_):
        step = next(filter(lambda st: st[bstack11lll_opy_ (u"ࠩ࡬ࡨࠬᷞ")] == bstack1111lllll1l_opy_, self.meta[bstack11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷟ")]), None)
        step.update({
            bstack11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᷠ"): bstack11ll11l1ll_opy_()
        })
    def bstack111lllllll_opy_(self, bstack1111lllll1l_opy_, result, duration=None):
        bstack1l111lllll1_opy_ = bstack11ll11l1ll_opy_()
        if bstack1111lllll1l_opy_ is not None and self.meta.get(bstack11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᷡ")):
            step = next(filter(lambda st: st[bstack11lll_opy_ (u"࠭ࡩࡥࠩᷢ")] == bstack1111lllll1l_opy_, self.meta[bstack11lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᷣ")]), None)
            step.update({
                bstack11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᷤ"): bstack1l111lllll1_opy_,
                bstack11lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᷥ"): duration if duration else bstack11l1l1ll1l1_opy_(step[bstack11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᷦ")], bstack1l111lllll1_opy_),
                bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᷧ"): result.result,
                bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᷨ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111lll1lll_opy_):
        if self.meta.get(bstack11lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᷩ")):
            self.meta[bstack11lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᷪ")].append(bstack1111lll1lll_opy_)
        else:
            self.meta[bstack11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷫ")] = [ bstack1111lll1lll_opy_ ]
    def bstack111l111111l_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᷬ"): self.bstack111ll1llll_opy_(),
            **self.bstack1111lll1l11_opy_(),
            **self.bstack111l11111l1_opy_(),
            **self.bstack1111llll111_opy_()
        }
    def bstack111l1111111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᷭ"): self.bstack1l111lllll1_opy_,
            bstack11lll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᷮ"): self.duration,
            bstack11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᷯ"): self.result.result
        }
        if data[bstack11lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᷰ")] == bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᷱ"):
            data[bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᷲ")] = self.result.bstack1111l1llll_opy_()
            data[bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᷳ")] = [{bstack11lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᷴ"): self.result.bstack11ll11l1lll_opy_()}]
        return data
    def bstack1111lll1l1l_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ᷵"): self.bstack111ll1llll_opy_(),
            **self.bstack1111lll1l11_opy_(),
            **self.bstack111l11111l1_opy_(),
            **self.bstack111l1111111_opy_(),
            **self.bstack1111llll111_opy_()
        }
    def bstack111ll11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11lll_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭᷶") in event:
            return self.bstack111l111111l_opy_()
        elif bstack11lll_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᷷") in event:
            return self.bstack1111lll1l1l_opy_()
    def bstack111l11l111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111lllll1_opy_ = time if time else bstack11ll11l1ll_opy_()
        self.duration = duration if duration else bstack11l1l1ll1l1_opy_(self.started_at, self.bstack1l111lllll1_opy_)
        if result:
            self.result = result
class bstack11l1111lll_opy_(bstack111l11l1l1_opy_):
    def __init__(self, hooks=[], bstack11l111111l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        super().__init__(*args, **kwargs, bstack1llllllll1_opy_=bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸ᷸ࠬ"))
    @classmethod
    def bstack1111llll1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lll_opy_ (u"ࠨ࡫ࡧ᷹ࠫ"): id(step),
                bstack11lll_opy_ (u"ࠩࡷࡩࡽࡺ᷺ࠧ"): step.name,
                bstack11lll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ᷻"): step.keyword,
            })
        return bstack11l1111lll_opy_(
            **kwargs,
            meta={
                bstack11lll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬ᷼"): {
                    bstack11lll_opy_ (u"ࠬࡴࡡ࡮ࡧ᷽ࠪ"): feature.name,
                    bstack11lll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ᷾"): feature.filename,
                    bstack11lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲ᷿ࠬ"): feature.description
                },
                bstack11lll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪḀ"): {
                    bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧḁ"): scenario.name
                },
                bstack11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩḂ"): steps,
                bstack11lll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ḃ"): bstack111l1l1l1ll_opy_(test)
            }
        )
    def bstack111l1111l1l_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫḄ"): self.hooks
        }
    def bstack111l1111l11_opy_(self):
        if self.bstack11l111111l_opy_:
            return {
                bstack11lll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬḅ"): self.bstack11l111111l_opy_
            }
        return {}
    def bstack1111lll1l1l_opy_(self):
        return {
            **super().bstack1111lll1l1l_opy_(),
            **self.bstack111l1111l1l_opy_()
        }
    def bstack111l111111l_opy_(self):
        return {
            **super().bstack111l111111l_opy_(),
            **self.bstack111l1111l11_opy_()
        }
    def bstack111l11l111_opy_(self):
        return bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩḆ")
class bstack111lllll1l_opy_(bstack111l11l1l1_opy_):
    def __init__(self, hook_type, *args,bstack11l111111l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111lllllll_opy_ = None
        self.bstack11l111111l_opy_ = bstack11l111111l_opy_
        super().__init__(*args, **kwargs, bstack1llllllll1_opy_=bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ḇ"))
    def bstack111lll11ll_opy_(self):
        return self.hook_type
    def bstack111l11111ll_opy_(self):
        return {
            bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬḈ"): self.hook_type
        }
    def bstack1111lll1l1l_opy_(self):
        return {
            **super().bstack1111lll1l1l_opy_(),
            **self.bstack111l11111ll_opy_()
        }
    def bstack111l111111l_opy_(self):
        return {
            **super().bstack111l111111l_opy_(),
            bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨḉ"): self.bstack1111lllllll_opy_,
            **self.bstack111l11111ll_opy_()
        }
    def bstack111l11l111_opy_(self):
        return bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭Ḋ")
    def bstack111lll1l1l_opy_(self, bstack1111lllllll_opy_):
        self.bstack1111lllllll_opy_ = bstack1111lllllll_opy_