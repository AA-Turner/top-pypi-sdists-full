# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1ll111ll1l_opy_, bstack111ll1l1l1l_opy_
from bstack_utils.bstack1l1l11111l_opy_ import bstack1lllllll1lll_opy_
class bstack111l111l1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllll11l11l_opy_=None, bstack1lllll1l111l_opy_=True, bstack1l11111ll1l_opy_=None, bstack1llll1111_opy_=None, result=None, duration=None, bstack1111ll11ll_opy_=None, meta={}):
        self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllll1l111l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllll11l11l_opy_ = bstack1lllll11l11l_opy_
        self.bstack1l11111ll1l_opy_ = bstack1l11111ll1l_opy_
        self.bstack1llll1111_opy_ = bstack1llll1111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l11ll11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l1lll1l_opy_(self, meta):
        self.meta = meta
    def bstack111l1lll11_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllll11l1ll_opy_(self):
        bstack1lllll1l1l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ‛"): bstack1lllll1l1l11_opy_,
            bstack1111l1l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ“"): bstack1lllll1l1l11_opy_,
            bstack1111l1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ”"): bstack1lllll1l1l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1111l1l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ„") + key)
            setattr(self, key, val)
    def bstack1lllll1l1l1l_opy_(self):
        return {
            bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ‟"): self.name,
            bstack1111l1l_opy_ (u"࠭ࡢࡰࡦࡼࠫ†"): {
                bstack1111l1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ‡"): bstack1111l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ•"),
                bstack1111l1l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ‣"): self.code
            },
            bstack1111l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ․"): self.scope,
            bstack1111l1l_opy_ (u"ࠫࡹࡧࡧࡴࠩ‥"): self.tags,
            bstack1111l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ…"): self.framework,
            bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ‧"): self.started_at
        }
    def bstack1lllll11ll11_opy_(self):
        return {
         bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ "): self.meta
        }
    def bstack1lllll1l11ll_opy_(self):
        return {
            bstack1111l1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ "): {
                bstack1111l1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭‪"): self.bstack1lllll11l11l_opy_
            }
        }
    def bstack1lllll11l111_opy_(self, bstack1lllll111lll_opy_, details):
        step = next(filter(lambda st: st[bstack1111l1l_opy_ (u"ࠪ࡭ࡩ࠭‫")] == bstack1lllll111lll_opy_, self.meta[bstack1111l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ‬")]), None)
        step.update(details)
    def bstack11ll11l1_opy_(self, bstack1lllll111lll_opy_):
        step = next(filter(lambda st: st[bstack1111l1l_opy_ (u"ࠬ࡯ࡤࠨ‭")] == bstack1lllll111lll_opy_, self.meta[bstack1111l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ‮")]), None)
        step.update({
            bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ "): bstack1ll111ll1l_opy_()
        })
    def bstack111ll1l11l_opy_(self, bstack1lllll111lll_opy_, result, duration=None):
        bstack1l11111ll1l_opy_ = bstack1ll111ll1l_opy_()
        if bstack1lllll111lll_opy_ is not None and self.meta.get(bstack1111l1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ‰")):
            step = next(filter(lambda st: st[bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬ‱")] == bstack1lllll111lll_opy_, self.meta[bstack1111l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ′")]), None)
            step.update({
                bstack1111l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ″"): bstack1l11111ll1l_opy_,
                bstack1111l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ‴"): duration if duration else bstack111ll1l1l1l_opy_(step[bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ‵")], bstack1l11111ll1l_opy_),
                bstack1111l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ‶"): result.result,
                bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ‷"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllll11lll1_opy_):
        if self.meta.get(bstack1111l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ‸")):
            self.meta[bstack1111l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ‹")].append(bstack1lllll11lll1_opy_)
        else:
            self.meta[bstack1111l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ›")] = [ bstack1lllll11lll1_opy_ ]
    def bstack1lllll1l1ll1_opy_(self):
        return {
            bstack1111l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ※"): self.bstack111l11ll11_opy_(),
            **self.bstack1lllll1l1l1l_opy_(),
            **self.bstack1lllll11l1ll_opy_(),
            **self.bstack1lllll11ll11_opy_()
        }
    def bstack1lllll1l1111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1111l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ‼"): self.bstack1l11111ll1l_opy_,
            bstack1111l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ‽"): self.duration,
            bstack1111l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ‾"): self.result.result
        }
        if data[bstack1111l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ‿")] == bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⁀"):
            data[bstack1111l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⁁")] = self.result.bstack111111l1ll_opy_()
            data[bstack1111l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⁂")] = [{bstack1111l1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⁃"): self.result.bstack11l11lll11l_opy_()}]
        return data
    def bstack1lllll1l1lll_opy_(self):
        return {
            bstack1111l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁄"): self.bstack111l11ll11_opy_(),
            **self.bstack1lllll1l1l1l_opy_(),
            **self.bstack1lllll11l1ll_opy_(),
            **self.bstack1lllll1l1111_opy_(),
            **self.bstack1lllll11ll11_opy_()
        }
    def bstack1111lll1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1111l1l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ⁅") in event:
            return self.bstack1lllll1l1ll1_opy_()
        elif bstack1111l1l_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁆") in event:
            return self.bstack1lllll1l1lll_opy_()
    def bstack1111ll1111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11111ll1l_opy_ = time if time else bstack1ll111ll1l_opy_()
        self.duration = duration if duration else bstack111ll1l1l1l_opy_(self.started_at, self.bstack1l11111ll1l_opy_)
        if result:
            self.result = result
class bstack111l1lllll_opy_(bstack111l111l1l_opy_):
    def __init__(self, hooks=[], bstack111lll11ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
        super().__init__(*args, **kwargs, bstack1llll1111_opy_=bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⁇"))
    @classmethod
    def bstack1lllll1l11l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111l1l_opy_ (u"ࠫ࡮ࡪࠧ⁈"): id(step),
                bstack1111l1l_opy_ (u"ࠬࡺࡥࡹࡶࠪ⁉"): step.name,
                bstack1111l1l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ⁊"): step.keyword,
            })
        return bstack111l1lllll_opy_(
            **kwargs,
            meta={
                bstack1111l1l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ⁋"): {
                    bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⁌"): feature.name,
                    bstack1111l1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ⁍"): feature.filename,
                    bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⁎"): feature.description
                },
                bstack1111l1l_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭⁏"): {
                    bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁐"): scenario.name
                },
                bstack1111l1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⁑"): steps,
                bstack1111l1l_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ⁒"): bstack1lllllll1lll_opy_(test)
            }
        )
    def bstack1lllll11ll1l_opy_(self):
        return {
            bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⁓"): self.hooks
        }
    def bstack1lllll11l1l1_opy_(self):
        if self.bstack111lll11ll_opy_:
            return {
                bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⁔"): self.bstack111lll11ll_opy_
            }
        return {}
    def bstack1lllll1l1lll_opy_(self):
        return {
            **super().bstack1lllll1l1lll_opy_(),
            **self.bstack1lllll11ll1l_opy_()
        }
    def bstack1lllll1l1ll1_opy_(self):
        return {
            **super().bstack1lllll1l1ll1_opy_(),
            **self.bstack1lllll11l1l1_opy_()
        }
    def bstack1111ll1111_opy_(self):
        return bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⁕")
class bstack111lll1l11_opy_(bstack111l111l1l_opy_):
    def __init__(self, hook_type, *args,bstack111lll11ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11lll111_opy_ = None
        self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
        super().__init__(*args, **kwargs, bstack1llll1111_opy_=bstack1111l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⁖"))
    def bstack111l1ll1l1_opy_(self):
        return self.hook_type
    def bstack1lllll11llll_opy_(self):
        return {
            bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⁗"): self.hook_type
        }
    def bstack1lllll1l1lll_opy_(self):
        return {
            **super().bstack1lllll1l1lll_opy_(),
            **self.bstack1lllll11llll_opy_()
        }
    def bstack1lllll1l1ll1_opy_(self):
        return {
            **super().bstack1lllll1l1ll1_opy_(),
            bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⁘"): self.bstack1ll11lll111_opy_,
            **self.bstack1lllll11llll_opy_()
        }
    def bstack1111ll1111_opy_(self):
        return bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ⁙")
    def bstack111ll1l111_opy_(self, bstack1ll11lll111_opy_):
        self.bstack1ll11lll111_opy_ = bstack1ll11lll111_opy_