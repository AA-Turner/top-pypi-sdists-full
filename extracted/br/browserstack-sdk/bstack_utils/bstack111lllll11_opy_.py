# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l11l1l11l_opy_, bstack11l1l1l1ll1_opy_
from bstack_utils.bstack1l11llll1l_opy_ import bstack111l1l1l1l1_opy_
class bstack111lll1l11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1111l1l_opy_=None, bstack111l1111111_opy_=True, bstack1l11ll1ll1l_opy_=None, bstack11ll1llll_opy_=None, result=None, duration=None, bstack111lll11l1_opy_=None, meta={}):
        self.bstack111lll11l1_opy_ = bstack111lll11l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l1111111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1111l1l_opy_ = bstack111l1111l1l_opy_
        self.bstack1l11ll1ll1l_opy_ = bstack1l11ll1ll1l_opy_
        self.bstack11ll1llll_opy_ = bstack11ll1llll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll1l1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1ll1_opy_(self, meta):
        self.meta = meta
    def bstack11l1111l1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111llll1ll_opy_(self):
        bstack1111llll111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1llllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭᷃"): bstack1111llll111_opy_,
            bstack1llllll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭᷄"): bstack1111llll111_opy_,
            bstack1llllll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ᷅"): bstack1111llll111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1llllll_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢ᷆") + key)
            setattr(self, key, val)
    def bstack1111lllllll_opy_(self):
        return {
            bstack1llllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᷇"): self.name,
            bstack1llllll_opy_ (u"ࠨࡤࡲࡨࡾ࠭᷈"): {
                bstack1llllll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ᷉"): bstack1llllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ᷊ࠪ"),
                bstack1llllll_opy_ (u"ࠫࡨࡵࡤࡦࠩ᷋"): self.code
            },
            bstack1llllll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ᷌"): self.scope,
            bstack1llllll_opy_ (u"࠭ࡴࡢࡩࡶࠫ᷍"): self.tags,
            bstack1llllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭᷎ࠪ"): self.framework,
            bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸ᷏ࠬ"): self.started_at
        }
    def bstack1111llll11l_opy_(self):
        return {
         bstack1llllll_opy_ (u"ࠩࡰࡩࡹࡧ᷐ࠧ"): self.meta
        }
    def bstack1111lll1lll_opy_(self):
        return {
            bstack1llllll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭᷑"): {
                bstack1llllll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ᷒"): self.bstack111l1111l1l_opy_
            }
        }
    def bstack111l11111ll_opy_(self, bstack1111llll1l1_opy_, details):
        step = next(filter(lambda st: st[bstack1llllll_opy_ (u"ࠬ࡯ࡤࠨᷓ")] == bstack1111llll1l1_opy_, self.meta[bstack1llllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᷔ")]), None)
        step.update(details)
    def bstack111l1l1ll_opy_(self, bstack1111llll1l1_opy_):
        step = next(filter(lambda st: st[bstack1llllll_opy_ (u"ࠧࡪࡦࠪᷕ")] == bstack1111llll1l1_opy_, self.meta[bstack1llllll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷖ")]), None)
        step.update({
            bstack1llllll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᷗ"): bstack1l11l1l11l_opy_()
        })
    def bstack11l1111l11_opy_(self, bstack1111llll1l1_opy_, result, duration=None):
        bstack1l11ll1ll1l_opy_ = bstack1l11l1l11l_opy_()
        if bstack1111llll1l1_opy_ is not None and self.meta.get(bstack1llllll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷘ")):
            step = next(filter(lambda st: st[bstack1llllll_opy_ (u"ࠫ࡮ࡪࠧᷙ")] == bstack1111llll1l1_opy_, self.meta[bstack1llllll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᷚ")]), None)
            step.update({
                bstack1llllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᷛ"): bstack1l11ll1ll1l_opy_,
                bstack1llllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᷜ"): duration if duration else bstack11l1l1l1ll1_opy_(step[bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᷝ")], bstack1l11ll1ll1l_opy_),
                bstack1llllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᷞ"): result.result,
                bstack1llllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᷟ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111l111111l_opy_):
        if self.meta.get(bstack1llllll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᷠ")):
            self.meta[bstack1llllll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᷡ")].append(bstack111l111111l_opy_)
        else:
            self.meta[bstack1llllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᷢ")] = [ bstack111l111111l_opy_ ]
    def bstack1111llllll1_opy_(self):
        return {
            bstack1llllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᷣ"): self.bstack111ll1l1ll_opy_(),
            **self.bstack1111lllllll_opy_(),
            **self.bstack1111llll1ll_opy_(),
            **self.bstack1111llll11l_opy_()
        }
    def bstack111l1111ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1llllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᷤ"): self.bstack1l11ll1ll1l_opy_,
            bstack1llllll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᷥ"): self.duration,
            bstack1llllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᷦ"): self.result.result
        }
        if data[bstack1llllll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᷧ")] == bstack1llllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᷨ"):
            data[bstack1llllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᷩ")] = self.result.bstack1111l1llll_opy_()
            data[bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᷪ")] = [{bstack1llllll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᷫ"): self.result.bstack11l1l11ll1l_opy_()}]
        return data
    def bstack111l1111l11_opy_(self):
        return {
            bstack1llllll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᷬ"): self.bstack111ll1l1ll_opy_(),
            **self.bstack1111lllllll_opy_(),
            **self.bstack1111llll1ll_opy_(),
            **self.bstack111l1111ll1_opy_(),
            **self.bstack1111llll11l_opy_()
        }
    def bstack111l11l1ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1llllll_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᷭ") in event:
            return self.bstack1111llllll1_opy_()
        elif bstack1llllll_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᷮ") in event:
            return self.bstack111l1111l11_opy_()
    def bstack111l11l11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11ll1ll1l_opy_ = time if time else bstack1l11l1l11l_opy_()
        self.duration = duration if duration else bstack11l1l1l1ll1_opy_(self.started_at, self.bstack1l11ll1ll1l_opy_)
        if result:
            self.result = result
class bstack11l111l11l_opy_(bstack111lll1l11_opy_):
    def __init__(self, hooks=[], bstack11l11111l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
        super().__init__(*args, **kwargs, bstack11ll1llll_opy_=bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࠪᷯ"))
    @classmethod
    def bstack1111lll1ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1llllll_opy_ (u"࠭ࡩࡥࠩᷰ"): id(step),
                bstack1llllll_opy_ (u"ࠧࡵࡧࡻࡸࠬᷱ"): step.name,
                bstack1llllll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᷲ"): step.keyword,
            })
        return bstack11l111l11l_opy_(
            **kwargs,
            meta={
                bstack1llllll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᷳ"): {
                    bstack1llllll_opy_ (u"ࠪࡲࡦࡳࡥࠨᷴ"): feature.name,
                    bstack1llllll_opy_ (u"ࠫࡵࡧࡴࡩࠩ᷵"): feature.filename,
                    bstack1llllll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᷶"): feature.description
                },
                bstack1llllll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ᷷"): {
                    bstack1llllll_opy_ (u"ࠧ࡯ࡣࡰࡩ᷸ࠬ"): scenario.name
                },
                bstack1llllll_opy_ (u"ࠨࡵࡷࡩࡵࡹ᷹ࠧ"): steps,
                bstack1llllll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶ᷺ࠫ"): bstack111l1l1l1l1_opy_(test)
            }
        )
    def bstack111l1111lll_opy_(self):
        return {
            bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᷻"): self.hooks
        }
    def bstack1111lllll11_opy_(self):
        if self.bstack11l11111l1_opy_:
            return {
                bstack1llllll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ᷼"): self.bstack11l11111l1_opy_
            }
        return {}
    def bstack111l1111l11_opy_(self):
        return {
            **super().bstack111l1111l11_opy_(),
            **self.bstack111l1111lll_opy_()
        }
    def bstack1111llllll1_opy_(self):
        return {
            **super().bstack1111llllll1_opy_(),
            **self.bstack1111lllll11_opy_()
        }
    def bstack111l11l11l_opy_(self):
        return bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ᷽ࠧ")
class bstack11l111111l_opy_(bstack111lll1l11_opy_):
    def __init__(self, hook_type, *args,bstack11l11111l1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111lllll1l_opy_ = None
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
        super().__init__(*args, **kwargs, bstack11ll1llll_opy_=bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᷾"))
    def bstack111l111lll_opy_(self):
        return self.hook_type
    def bstack111l11111l1_opy_(self):
        return {
            bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧ᷿ࠪ"): self.hook_type
        }
    def bstack111l1111l11_opy_(self):
        return {
            **super().bstack111l1111l11_opy_(),
            **self.bstack111l11111l1_opy_()
        }
    def bstack1111llllll1_opy_(self):
        return {
            **super().bstack1111llllll1_opy_(),
            bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭Ḁ"): self.bstack1111lllll1l_opy_,
            **self.bstack111l11111l1_opy_()
        }
    def bstack111l11l11l_opy_(self):
        return bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫḁ")
    def bstack11l1111111_opy_(self, bstack1111lllll1l_opy_):
        self.bstack1111lllll1l_opy_ = bstack1111lllll1l_opy_