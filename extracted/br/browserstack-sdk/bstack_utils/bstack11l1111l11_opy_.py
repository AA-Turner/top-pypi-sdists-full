# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11lll111l1_opy_, bstack11l1l11111l_opy_
from bstack_utils.bstack11lll11l_opy_ import bstack111l1l1ll1l_opy_
class bstack111l1l11ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111lll1lll_opy_=None, bstack111l11111l1_opy_=True, bstack1l11l1l11l1_opy_=None, bstack11l11llll1_opy_=None, result=None, duration=None, bstack111ll11ll1_opy_=None, meta={}):
        self.bstack111ll11ll1_opy_ = bstack111ll11ll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l11111l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111lll1lll_opy_ = bstack1111lll1lll_opy_
        self.bstack1l11l1l11l1_opy_ = bstack1l11l1l11l1_opy_
        self.bstack11l11llll1_opy_ = bstack11l11llll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll1l1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111111l_opy_(self, meta):
        self.meta = meta
    def bstack111lllll1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l11111ll_opy_(self):
        bstack1111llll11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ᷁"): bstack1111llll11l_opy_,
            bstack1l11lll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱ᷂ࠫ"): bstack1111llll11l_opy_,
            bstack1l11lll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ᷃"): bstack1111llll11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l11lll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ᷄") + key)
            setattr(self, key, val)
    def bstack111l1111ll1_opy_(self):
        return {
            bstack1l11lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᷅"): self.name,
            bstack1l11lll_opy_ (u"࠭ࡢࡰࡦࡼࠫ᷆"): {
                bstack1l11lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ᷇"): bstack1l11lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᷈"),
                bstack1l11lll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ᷉"): self.code
            },
            bstack1l11lll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵ᷊ࠪ"): self.scope,
            bstack1l11lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ᷋"): self.tags,
            bstack1l11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᷌"): self.framework,
            bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᷍"): self.started_at
        }
    def bstack111l111111l_opy_(self):
        return {
         bstack1l11lll_opy_ (u"ࠧ࡮ࡧࡷࡥ᷎ࠬ"): self.meta
        }
    def bstack111l1111111_opy_(self):
        return {
            bstack1l11lll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰ᷏ࠫ"): {
                bstack1l11lll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ᷐࠭"): self.bstack1111lll1lll_opy_
            }
        }
    def bstack1111lllllll_opy_(self, bstack111l1111lll_opy_, details):
        step = next(filter(lambda st: st[bstack1l11lll_opy_ (u"ࠪ࡭ࡩ࠭᷑")] == bstack111l1111lll_opy_, self.meta[bstack1l11lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᷒")]), None)
        step.update(details)
    def bstack1l11l1111_opy_(self, bstack111l1111lll_opy_):
        step = next(filter(lambda st: st[bstack1l11lll_opy_ (u"ࠬ࡯ࡤࠨᷓ")] == bstack111l1111lll_opy_, self.meta[bstack1l11lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᷔ")]), None)
        step.update({
            bstack1l11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᷕ"): bstack11lll111l1_opy_()
        })
    def bstack11l111l1ll_opy_(self, bstack111l1111lll_opy_, result, duration=None):
        bstack1l11l1l11l1_opy_ = bstack11lll111l1_opy_()
        if bstack111l1111lll_opy_ is not None and self.meta.get(bstack1l11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷖ")):
            step = next(filter(lambda st: st[bstack1l11lll_opy_ (u"ࠩ࡬ࡨࠬᷗ")] == bstack111l1111lll_opy_, self.meta[bstack1l11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷘ")]), None)
            step.update({
                bstack1l11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᷙ"): bstack1l11l1l11l1_opy_,
                bstack1l11lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᷚ"): duration if duration else bstack11l1l11111l_opy_(step[bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᷛ")], bstack1l11l1l11l1_opy_),
                bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᷜ"): result.result,
                bstack1l11lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᷝ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111lllll1l_opy_):
        if self.meta.get(bstack1l11lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᷞ")):
            self.meta[bstack1l11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷟ")].append(bstack1111lllll1l_opy_)
        else:
            self.meta[bstack1l11lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᷠ")] = [ bstack1111lllll1l_opy_ ]
    def bstack1111llllll1_opy_(self):
        return {
            bstack1l11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪᷡ"): self.bstack111ll1l1l1_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack111l11111ll_opy_(),
            **self.bstack111l111111l_opy_()
        }
    def bstack1111llll1l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᷢ"): self.bstack1l11l1l11l1_opy_,
            bstack1l11lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᷣ"): self.duration,
            bstack1l11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᷤ"): self.result.result
        }
        if data[bstack1l11lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᷥ")] == bstack1l11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᷦ"):
            data[bstack1l11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᷧ")] = self.result.bstack1111l1llll_opy_()
            data[bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᷨ")] = [{bstack1l11lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᷩ"): self.result.bstack11l1l1ll111_opy_()}]
        return data
    def bstack1111lll1ll1_opy_(self):
        return {
            bstack1l11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᷪ"): self.bstack111ll1l1l1_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack111l11111ll_opy_(),
            **self.bstack1111llll1l1_opy_(),
            **self.bstack111l111111l_opy_()
        }
    def bstack111l11l1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l11lll_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᷫ") in event:
            return self.bstack1111llllll1_opy_()
        elif bstack1l11lll_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᷬ") in event:
            return self.bstack1111lll1ll1_opy_()
    def bstack111l1l11l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l1l11l1_opy_ = time if time else bstack11lll111l1_opy_()
        self.duration = duration if duration else bstack11l1l11111l_opy_(self.started_at, self.bstack1l11l1l11l1_opy_)
        if result:
            self.result = result
class bstack111lll1ll1_opy_(bstack111l1l11ll_opy_):
    def __init__(self, hooks=[], bstack11l111ll11_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l111ll11_opy_ = bstack11l111ll11_opy_
        super().__init__(*args, **kwargs, bstack11l11llll1_opy_=bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࠨᷭ"))
    @classmethod
    def bstack111l1111l11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11lll_opy_ (u"ࠫ࡮ࡪࠧᷮ"): id(step),
                bstack1l11lll_opy_ (u"ࠬࡺࡥࡹࡶࠪᷯ"): step.name,
                bstack1l11lll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᷰ"): step.keyword,
            })
        return bstack111lll1ll1_opy_(
            **kwargs,
            meta={
                bstack1l11lll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᷱ"): {
                    bstack1l11lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᷲ"): feature.name,
                    bstack1l11lll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᷳ"): feature.filename,
                    bstack1l11lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᷴ"): feature.description
                },
                bstack1l11lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭᷵"): {
                    bstack1l11lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᷶"): scenario.name
                },
                bstack1l11lll_opy_ (u"࠭ࡳࡵࡧࡳࡷ᷷ࠬ"): steps,
                bstack1l11lll_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴ᷸ࠩ"): bstack111l1l1ll1l_opy_(test)
            }
        )
    def bstack1111llll111_opy_(self):
        return {
            bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰࡹ᷹ࠧ"): self.hooks
        }
    def bstack1111lllll11_opy_(self):
        if self.bstack11l111ll11_opy_:
            return {
                bstack1l11lll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ᷺"): self.bstack11l111ll11_opy_
            }
        return {}
    def bstack1111lll1ll1_opy_(self):
        return {
            **super().bstack1111lll1ll1_opy_(),
            **self.bstack1111llll111_opy_()
        }
    def bstack1111llllll1_opy_(self):
        return {
            **super().bstack1111llllll1_opy_(),
            **self.bstack1111lllll11_opy_()
        }
    def bstack111l1l11l1_opy_(self):
        return bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᷻")
class bstack111lll1lll_opy_(bstack111l1l11ll_opy_):
    def __init__(self, hook_type, *args,bstack11l111ll11_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111l1111l1l_opy_ = None
        self.bstack11l111ll11_opy_ = bstack11l111ll11_opy_
        super().__init__(*args, **kwargs, bstack11l11llll1_opy_=bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ᷼"))
    def bstack111lll11l1_opy_(self):
        return self.hook_type
    def bstack1111llll1ll_opy_(self):
        return {
            bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᷽"): self.hook_type
        }
    def bstack1111lll1ll1_opy_(self):
        return {
            **super().bstack1111lll1ll1_opy_(),
            **self.bstack1111llll1ll_opy_()
        }
    def bstack1111llllll1_opy_(self):
        return {
            **super().bstack1111llllll1_opy_(),
            bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ᷾"): self.bstack111l1111l1l_opy_,
            **self.bstack1111llll1ll_opy_()
        }
    def bstack111l1l11l1_opy_(self):
        return bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯᷿ࠩ")
    def bstack111llll1ll_opy_(self, bstack111l1111l1l_opy_):
        self.bstack111l1111l1l_opy_ = bstack111l1111l1l_opy_