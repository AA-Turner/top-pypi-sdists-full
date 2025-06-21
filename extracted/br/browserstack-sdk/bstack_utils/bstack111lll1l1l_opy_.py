# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lllll1l1l_opy_, bstack11l11ll11l1_opy_
from bstack_utils.bstack1l11lllll_opy_ import bstack11111l1llll_opy_
class bstack111l11l111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllllllll1l_opy_=None, bstack1lllllllllll_opy_=True, bstack1l111lll1l1_opy_=None, bstack11lll1ll11_opy_=None, result=None, duration=None, bstack111l1ll1l1_opy_=None, meta={}):
        self.bstack111l1ll1l1_opy_ = bstack111l1ll1l1_opy_
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
        self.bstack1lllllllll1l_opy_ = bstack1lllllllll1l_opy_
        self.bstack1l111lll1l1_opy_ = bstack1l111lll1l1_opy_
        self.bstack11lll1ll11_opy_ = bstack11lll1ll11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111lll11l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111llll1l1_opy_(self, meta):
        self.meta = meta
    def bstack111llll111_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111111111l_opy_(self):
        bstack111111111ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬἮ"): bstack111111111ll_opy_,
            bstack1l1l1l1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬἯ"): bstack111111111ll_opy_,
            bstack1l1l1l1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩἰ"): bstack111111111ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨἱ") + key)
            setattr(self, key, val)
    def bstack1111111l1ll_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫἲ"): self.name,
            bstack1l1l1l1_opy_ (u"ࠧࡣࡱࡧࡽࠬἳ"): {
                bstack1l1l1l1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ἴ"): bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩἵ"),
                bstack1l1l1l1_opy_ (u"ࠪࡧࡴࡪࡥࠨἶ"): self.code
            },
            bstack1l1l1l1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫἷ"): self.scope,
            bstack1l1l1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪἸ"): self.tags,
            bstack1l1l1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩἹ"): self.framework,
            bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫἺ"): self.started_at
        }
    def bstack1111111l1l1_opy_(self):
        return {
         bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭Ἳ"): self.meta
        }
    def bstack111111111l1_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬἼ"): {
                bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧἽ"): self.bstack1lllllllll1l_opy_
            }
        }
    def bstack1111111l11l_opy_(self, bstack1llllllllll1_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠫ࡮ࡪࠧἾ")] == bstack1llllllllll1_opy_, self.meta[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫἿ")]), None)
        step.update(details)
    def bstack1l11111l_opy_(self, bstack1llllllllll1_opy_):
        step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"࠭ࡩࡥࠩὀ")] == bstack1llllllllll1_opy_, self.meta[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ὁ")]), None)
        step.update({
            bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬὂ"): bstack1lllll1l1l_opy_()
        })
    def bstack111llll1ll_opy_(self, bstack1llllllllll1_opy_, result, duration=None):
        bstack1l111lll1l1_opy_ = bstack1lllll1l1l_opy_()
        if bstack1llllllllll1_opy_ is not None and self.meta.get(bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨὃ")):
            step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭ὄ")] == bstack1llllllllll1_opy_, self.meta[bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪὅ")]), None)
            step.update({
                bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ὆"): bstack1l111lll1l1_opy_,
                bstack1l1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ὇"): duration if duration else bstack11l11ll11l1_opy_(step[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫὈ")], bstack1l111lll1l1_opy_),
                bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨὉ"): result.result,
                bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪὊ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack11111111ll1_opy_):
        if self.meta.get(bstack1l1l1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩὋ")):
            self.meta[bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪὌ")].append(bstack11111111ll1_opy_)
        else:
            self.meta[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫὍ")] = [ bstack11111111ll1_opy_ ]
    def bstack1111111ll11_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ὎"): self.bstack1111lll11l_opy_(),
            **self.bstack1111111l1ll_opy_(),
            **self.bstack1111111111l_opy_(),
            **self.bstack1111111l1l1_opy_()
        }
    def bstack11111111lll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ὏"): self.bstack1l111lll1l1_opy_,
            bstack1l1l1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩὐ"): self.duration,
            bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩὑ"): self.result.result
        }
        if data[bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪὒ")] == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫὓ"):
            data[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫὔ")] = self.result.bstack11111l11ll_opy_()
            data[bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧὕ")] = [{bstack1l1l1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪὖ"): self.result.bstack11l111ll11l_opy_()}]
        return data
    def bstack1111111l111_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ὗ"): self.bstack1111lll11l_opy_(),
            **self.bstack1111111l1ll_opy_(),
            **self.bstack1111111111l_opy_(),
            **self.bstack11111111lll_opy_(),
            **self.bstack1111111l1l1_opy_()
        }
    def bstack111l11111l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l1l1_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪ὘") in event:
            return self.bstack1111111ll11_opy_()
        elif bstack1l1l1l1_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬὙ") in event:
            return self.bstack1111111l111_opy_()
    def bstack1111ll1ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111lll1l1_opy_ = time if time else bstack1lllll1l1l_opy_()
        self.duration = duration if duration else bstack11l11ll11l1_opy_(self.started_at, self.bstack1l111lll1l1_opy_)
        if result:
            self.result = result
class bstack111lllll1l_opy_(bstack111l11l111_opy_):
    def __init__(self, hooks=[], bstack111ll1lll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll1lll1_opy_ = bstack111ll1lll1_opy_
        super().__init__(*args, **kwargs, bstack11lll1ll11_opy_=bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ὚"))
    @classmethod
    def bstack11111111l11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1l1_opy_ (u"ࠬ࡯ࡤࠨὛ"): id(step),
                bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡺࡷࠫ὜"): step.name,
                bstack1l1l1l1_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨὝ"): step.keyword,
            })
        return bstack111lllll1l_opy_(
            **kwargs,
            meta={
                bstack1l1l1l1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ὞"): {
                    bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧὟ"): feature.name,
                    bstack1l1l1l1_opy_ (u"ࠪࡴࡦࡺࡨࠨὠ"): feature.filename,
                    bstack1l1l1l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩὡ"): feature.description
                },
                bstack1l1l1l1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧὢ"): {
                    bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫὣ"): scenario.name
                },
                bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ὤ"): steps,
                bstack1l1l1l1_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪὥ"): bstack11111l1llll_opy_(test)
            }
        )
    def bstack11111111111_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨὦ"): self.hooks
        }
    def bstack1lllllllll11_opy_(self):
        if self.bstack111ll1lll1_opy_:
            return {
                bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩὧ"): self.bstack111ll1lll1_opy_
            }
        return {}
    def bstack1111111l111_opy_(self):
        return {
            **super().bstack1111111l111_opy_(),
            **self.bstack11111111111_opy_()
        }
    def bstack1111111ll11_opy_(self):
        return {
            **super().bstack1111111ll11_opy_(),
            **self.bstack1lllllllll11_opy_()
        }
    def bstack1111ll1ll1_opy_(self):
        return bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ὠ")
class bstack111lll11l1_opy_(bstack111l11l111_opy_):
    def __init__(self, hook_type, *args,bstack111ll1lll1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1llllllll1ll_opy_ = None
        self.bstack111ll1lll1_opy_ = bstack111ll1lll1_opy_
        super().__init__(*args, **kwargs, bstack11lll1ll11_opy_=bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪὩ"))
    def bstack111ll111ll_opy_(self):
        return self.hook_type
    def bstack11111111l1l_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩὪ"): self.hook_type
        }
    def bstack1111111l111_opy_(self):
        return {
            **super().bstack1111111l111_opy_(),
            **self.bstack11111111l1l_opy_()
        }
    def bstack1111111ll11_opy_(self):
        return {
            **super().bstack1111111ll11_opy_(),
            bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬὫ"): self.bstack1llllllll1ll_opy_,
            **self.bstack11111111l1l_opy_()
        }
    def bstack1111ll1ll1_opy_(self):
        return bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪὬ")
    def bstack111ll1l111_opy_(self, bstack1llllllll1ll_opy_):
        self.bstack1llllllll1ll_opy_ = bstack1llllllll1ll_opy_