# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l1ll1ll_opy_, bstack11l1l1ll111_opy_
from bstack_utils.bstack1l11lll1l1_opy_ import bstack111l1l1ll11_opy_
class bstack111l1l1lll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l11111ll_opy_=None, bstack1111llll1ll_opy_=True, bstack1l11l1ll1l1_opy_=None, bstack11l1l1l1l1_opy_=None, result=None, duration=None, bstack111l11l111_opy_=None, meta={}):
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111llll1ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l11111ll_opy_ = bstack111l11111ll_opy_
        self.bstack1l11l1ll1l1_opy_ = bstack1l11l1ll1l1_opy_
        self.bstack11l1l1l1l1_opy_ = bstack11l1l1l1l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll11lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lllllll_opy_(self, meta):
        self.meta = meta
    def bstack111lll1ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111lll1lll_opy_(self):
        bstack1111lllllll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ᷈"): bstack1111lllllll_opy_,
            bstack1l1lll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ᷉"): bstack1111lllllll_opy_,
            bstack1l1lll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ᷊"): bstack1111lllllll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1lll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ᷋") + key)
            setattr(self, key, val)
    def bstack1111llllll1_opy_(self):
        return {
            bstack1l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᷌"): self.name,
            bstack1l1lll_opy_ (u"࠭ࡢࡰࡦࡼࠫ᷍"): {
                bstack1l1lll_opy_ (u"ࠧ࡭ࡣࡱ࡫᷎ࠬ"): bstack1l1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᷏"),
                bstack1l1lll_opy_ (u"ࠩࡦࡳࡩ࡫᷐ࠧ"): self.code
            },
            bstack1l1lll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ᷑"): self.scope,
            bstack1l1lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ᷒"): self.tags,
            bstack1l1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᷓ"): self.framework,
            bstack1l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᷔ"): self.started_at
        }
    def bstack111l11111l1_opy_(self):
        return {
         bstack1l1lll_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᷕ"): self.meta
        }
    def bstack1111llll1l1_opy_(self):
        return {
            bstack1l1lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᷖ"): {
                bstack1l1lll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᷗ"): self.bstack111l11111ll_opy_
            }
        }
    def bstack111l1111ll1_opy_(self, bstack111l1111111_opy_, details):
        step = next(filter(lambda st: st[bstack1l1lll_opy_ (u"ࠪ࡭ࡩ࠭ᷘ")] == bstack111l1111111_opy_, self.meta[bstack1l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᷙ")]), None)
        step.update(details)
    def bstack11l1ll1ll_opy_(self, bstack111l1111111_opy_):
        step = next(filter(lambda st: st[bstack1l1lll_opy_ (u"ࠬ࡯ࡤࠨᷚ")] == bstack111l1111111_opy_, self.meta[bstack1l1lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᷛ")]), None)
        step.update({
            bstack1l1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᷜ"): bstack1l1ll1ll_opy_()
        })
    def bstack111llllll1_opy_(self, bstack111l1111111_opy_, result, duration=None):
        bstack1l11l1ll1l1_opy_ = bstack1l1ll1ll_opy_()
        if bstack111l1111111_opy_ is not None and self.meta.get(bstack1l1lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷝ")):
            step = next(filter(lambda st: st[bstack1l1lll_opy_ (u"ࠩ࡬ࡨࠬᷞ")] == bstack111l1111111_opy_, self.meta[bstack1l1lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷟ")]), None)
            step.update({
                bstack1l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᷠ"): bstack1l11l1ll1l1_opy_,
                bstack1l1lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᷡ"): duration if duration else bstack11l1l1ll111_opy_(step[bstack1l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᷢ")], bstack1l11l1ll1l1_opy_),
                bstack1l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᷣ"): result.result,
                bstack1l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᷤ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111llll111_opy_):
        if self.meta.get(bstack1l1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᷥ")):
            self.meta[bstack1l1lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷦ")].append(bstack1111llll111_opy_)
        else:
            self.meta[bstack1l1lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᷧ")] = [ bstack1111llll111_opy_ ]
    def bstack111l1111lll_opy_(self):
        return {
            bstack1l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪᷨ"): self.bstack111ll11lll_opy_(),
            **self.bstack1111llllll1_opy_(),
            **self.bstack1111lll1lll_opy_(),
            **self.bstack111l11111l1_opy_()
        }
    def bstack111l111111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᷩ"): self.bstack1l11l1ll1l1_opy_,
            bstack1l1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᷪ"): self.duration,
            bstack1l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᷫ"): self.result.result
        }
        if data[bstack1l1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᷬ")] == bstack1l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᷭ"):
            data[bstack1l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᷮ")] = self.result.bstack1111ll1111_opy_()
            data[bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᷯ")] = [{bstack1l1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᷰ"): self.result.bstack11l1l1l1ll1_opy_()}]
        return data
    def bstack111l1111l1l_opy_(self):
        return {
            bstack1l1lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᷱ"): self.bstack111ll11lll_opy_(),
            **self.bstack1111llllll1_opy_(),
            **self.bstack1111lll1lll_opy_(),
            **self.bstack111l111111l_opy_(),
            **self.bstack111l11111l1_opy_()
        }
    def bstack111lll1l1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1lll_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᷲ") in event:
            return self.bstack111l1111lll_opy_()
        elif bstack1l1lll_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᷳ") in event:
            return self.bstack111l1111l1l_opy_()
    def bstack111ll11l1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l1ll1l1_opy_ = time if time else bstack1l1ll1ll_opy_()
        self.duration = duration if duration else bstack11l1l1ll111_opy_(self.started_at, self.bstack1l11l1ll1l1_opy_)
        if result:
            self.result = result
class bstack111llll11l_opy_(bstack111l1l1lll_opy_):
    def __init__(self, hooks=[], bstack111llll1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111llll1l1_opy_ = bstack111llll1l1_opy_
        super().__init__(*args, **kwargs, bstack11l1l1l1l1_opy_=bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࠨᷴ"))
    @classmethod
    def bstack1111llll11l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1lll_opy_ (u"ࠫ࡮ࡪࠧ᷵"): id(step),
                bstack1l1lll_opy_ (u"ࠬࡺࡥࡹࡶࠪ᷶"): step.name,
                bstack1l1lll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪ᷷ࠧ"): step.keyword,
            })
        return bstack111llll11l_opy_(
            **kwargs,
            meta={
                bstack1l1lll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ᷸"): {
                    bstack1l1lll_opy_ (u"ࠨࡰࡤࡱࡪ᷹࠭"): feature.name,
                    bstack1l1lll_opy_ (u"ࠩࡳࡥࡹ࡮᷺ࠧ"): feature.filename,
                    bstack1l1lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ᷻"): feature.description
                },
                bstack1l1lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭᷼"): {
                    bstack1l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧ᷽ࠪ"): scenario.name
                },
                bstack1l1lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᷾"): steps,
                bstack1l1lll_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴ᷿ࠩ"): bstack111l1l1ll11_opy_(test)
            }
        )
    def bstack1111lllll11_opy_(self):
        return {
            bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧḀ"): self.hooks
        }
    def bstack111l1111l11_opy_(self):
        if self.bstack111llll1l1_opy_:
            return {
                bstack1l1lll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨḁ"): self.bstack111llll1l1_opy_
            }
        return {}
    def bstack111l1111l1l_opy_(self):
        return {
            **super().bstack111l1111l1l_opy_(),
            **self.bstack1111lllll11_opy_()
        }
    def bstack111l1111lll_opy_(self):
        return {
            **super().bstack111l1111lll_opy_(),
            **self.bstack111l1111l11_opy_()
        }
    def bstack111ll11l1l_opy_(self):
        return bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬḂ")
class bstack111llll111_opy_(bstack111l1l1lll_opy_):
    def __init__(self, hook_type, *args,bstack111llll1l1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111lll1ll1_opy_ = None
        self.bstack111llll1l1_opy_ = bstack111llll1l1_opy_
        super().__init__(*args, **kwargs, bstack11l1l1l1l1_opy_=bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩḃ"))
    def bstack111l1llll1_opy_(self):
        return self.hook_type
    def bstack1111lllll1l_opy_(self):
        return {
            bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨḄ"): self.hook_type
        }
    def bstack111l1111l1l_opy_(self):
        return {
            **super().bstack111l1111l1l_opy_(),
            **self.bstack1111lllll1l_opy_()
        }
    def bstack111l1111lll_opy_(self):
        return {
            **super().bstack111l1111lll_opy_(),
            bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫḅ"): self.bstack1111lll1ll1_opy_,
            **self.bstack1111lllll1l_opy_()
        }
    def bstack111ll11l1l_opy_(self):
        return bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩḆ")
    def bstack11l111ll11_opy_(self, bstack1111lll1ll1_opy_):
        self.bstack1111lll1ll1_opy_ = bstack1111lll1ll1_opy_