# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1ll11l1ll1_opy_, bstack11l11l1ll1l_opy_
from bstack_utils.bstack1l1llll111_opy_ import bstack11111111111_opy_
class bstack1111lllll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllll11l1l1_opy_=None, bstack1lllll1l1l1l_opy_=True, bstack1l11111111l_opy_=None, bstack111lllll1l_opy_=None, result=None, duration=None, bstack111l11l111_opy_=None, meta={}):
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllll1l1l1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllll11l1l1_opy_ = bstack1lllll11l1l1_opy_
        self.bstack1l11111111l_opy_ = bstack1l11111111l_opy_
        self.bstack111lllll1l_opy_ = bstack111lllll1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l111lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l1lll11_opy_(self, meta):
        self.meta = meta
    def bstack111lll11ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllll1l11ll_opy_(self):
        bstack1lllll11llll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l11ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ’"): bstack1lllll11llll_opy_,
            bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ‚"): bstack1lllll11llll_opy_,
            bstack1l11ll1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭‛"): bstack1lllll11llll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l11ll1_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ“") + key)
            setattr(self, key, val)
    def bstack1lllll11l1ll_opy_(self):
        return {
            bstack1l11ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ”"): self.name,
            bstack1l11ll1_opy_ (u"ࠫࡧࡵࡤࡺࠩ„"): {
                bstack1l11ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ‟"): bstack1l11ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭†"),
                bstack1l11ll1_opy_ (u"ࠧࡤࡱࡧࡩࠬ‡"): self.code
            },
            bstack1l11ll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ•"): self.scope,
            bstack1l11ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ‣"): self.tags,
            bstack1l11ll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭․"): self.framework,
            bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ‥"): self.started_at
        }
    def bstack1lllll1l1ll1_opy_(self):
        return {
         bstack1l11ll1_opy_ (u"ࠬࡳࡥࡵࡣࠪ…"): self.meta
        }
    def bstack1lllll11l11l_opy_(self):
        return {
            bstack1l11ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ‧"): {
                bstack1l11ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ "): self.bstack1lllll11l1l1_opy_
            }
        }
    def bstack1lllll11lll1_opy_(self, bstack1lllll111lll_opy_, details):
        step = next(filter(lambda st: st[bstack1l11ll1_opy_ (u"ࠨ࡫ࡧࠫ ")] == bstack1lllll111lll_opy_, self.meta[bstack1l11ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ‪")]), None)
        step.update(details)
    def bstack1llll11lll_opy_(self, bstack1lllll111lll_opy_):
        step = next(filter(lambda st: st[bstack1l11ll1_opy_ (u"ࠪ࡭ࡩ࠭‫")] == bstack1lllll111lll_opy_, self.meta[bstack1l11ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ‬")]), None)
        step.update({
            bstack1l11ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ‭"): bstack1ll11l1ll1_opy_()
        })
    def bstack111lll11l1_opy_(self, bstack1lllll111lll_opy_, result, duration=None):
        bstack1l11111111l_opy_ = bstack1ll11l1ll1_opy_()
        if bstack1lllll111lll_opy_ is not None and self.meta.get(bstack1l11ll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ‮")):
            step = next(filter(lambda st: st[bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪ ")] == bstack1lllll111lll_opy_, self.meta[bstack1l11ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ‰")]), None)
            step.update({
                bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ‱"): bstack1l11111111l_opy_,
                bstack1l11ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ′"): duration if duration else bstack11l11l1ll1l_opy_(step[bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ″")], bstack1l11111111l_opy_),
                bstack1l11ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ‴"): result.result,
                bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ‵"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllll11ll11_opy_):
        if self.meta.get(bstack1l11ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭‶")):
            self.meta[bstack1l11ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ‷")].append(bstack1lllll11ll11_opy_)
        else:
            self.meta[bstack1l11ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ‸")] = [ bstack1lllll11ll11_opy_ ]
    def bstack1lllll111ll1_opy_(self):
        return {
            bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ‹"): self.bstack111l111lll_opy_(),
            **self.bstack1lllll11l1ll_opy_(),
            **self.bstack1lllll1l11ll_opy_(),
            **self.bstack1lllll1l1ll1_opy_()
        }
    def bstack1lllll11l111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l11ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ›"): self.bstack1l11111111l_opy_,
            bstack1l11ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭※"): self.duration,
            bstack1l11ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭‼"): self.result.result
        }
        if data[bstack1l11ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ‽")] == bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ‾"):
            data[bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ‿")] = self.result.bstack111111l1l1_opy_()
            data[bstack1l11ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⁀")] = [{bstack1l11ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⁁"): self.result.bstack11l11l1ll11_opy_()}]
        return data
    def bstack1lllll1l111l_opy_(self):
        return {
            bstack1l11ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁂"): self.bstack111l111lll_opy_(),
            **self.bstack1lllll11l1ll_opy_(),
            **self.bstack1lllll1l11ll_opy_(),
            **self.bstack1lllll11l111_opy_(),
            **self.bstack1lllll1l1ll1_opy_()
        }
    def bstack1111l1ll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l11ll1_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧ⁃") in event:
            return self.bstack1lllll111ll1_opy_()
        elif bstack1l11ll1_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⁄") in event:
            return self.bstack1lllll1l111l_opy_()
    def bstack111l1ll11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11111111l_opy_ = time if time else bstack1ll11l1ll1_opy_()
        self.duration = duration if duration else bstack11l11l1ll1l_opy_(self.started_at, self.bstack1l11111111l_opy_)
        if result:
            self.result = result
class bstack111ll11111_opy_(bstack1111lllll1_opy_):
    def __init__(self, hooks=[], bstack111l1lll1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111l1lll1l_opy_ = bstack111l1lll1l_opy_
        super().__init__(*args, **kwargs, bstack111lllll1l_opy_=bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹ࠭⁅"))
    @classmethod
    def bstack1lllll1l1l11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11ll1_opy_ (u"ࠩ࡬ࡨࠬ⁆"): id(step),
                bstack1l11ll1_opy_ (u"ࠪࡸࡪࡾࡴࠨ⁇"): step.name,
                bstack1l11ll1_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ⁈"): step.keyword,
            })
        return bstack111ll11111_opy_(
            **kwargs,
            meta={
                bstack1l11ll1_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭⁉"): {
                    bstack1l11ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁊"): feature.name,
                    bstack1l11ll1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ⁋"): feature.filename,
                    bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⁌"): feature.description
                },
                bstack1l11ll1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ⁍"): {
                    bstack1l11ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ⁎"): scenario.name
                },
                bstack1l11ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⁏"): steps,
                bstack1l11ll1_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧ⁐"): bstack11111111111_opy_(test)
            }
        )
    def bstack1lllll11ll1l_opy_(self):
        return {
            bstack1l11ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⁑"): self.hooks
        }
    def bstack1lllll1l1111_opy_(self):
        if self.bstack111l1lll1l_opy_:
            return {
                bstack1l11ll1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭⁒"): self.bstack111l1lll1l_opy_
            }
        return {}
    def bstack1lllll1l111l_opy_(self):
        return {
            **super().bstack1lllll1l111l_opy_(),
            **self.bstack1lllll11ll1l_opy_()
        }
    def bstack1lllll111ll1_opy_(self):
        return {
            **super().bstack1lllll111ll1_opy_(),
            **self.bstack1lllll1l1111_opy_()
        }
    def bstack111l1ll11l_opy_(self):
        return bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⁓")
class bstack111ll11l11_opy_(bstack1111lllll1_opy_):
    def __init__(self, hook_type, *args,bstack111l1lll1l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11l1l11l_opy_ = None
        self.bstack111l1lll1l_opy_ = bstack111l1lll1l_opy_
        super().__init__(*args, **kwargs, bstack111lllll1l_opy_=bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⁔"))
    def bstack111l111l11_opy_(self):
        return self.hook_type
    def bstack1lllll1l11l1_opy_(self):
        return {
            bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⁕"): self.hook_type
        }
    def bstack1lllll1l111l_opy_(self):
        return {
            **super().bstack1lllll1l111l_opy_(),
            **self.bstack1lllll1l11l1_opy_()
        }
    def bstack1lllll111ll1_opy_(self):
        return {
            **super().bstack1lllll111ll1_opy_(),
            bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⁖"): self.bstack1ll11l1l11l_opy_,
            **self.bstack1lllll1l11l1_opy_()
        }
    def bstack111l1ll11l_opy_(self):
        return bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ⁗")
    def bstack111ll1l11l_opy_(self, bstack1ll11l1l11l_opy_):
        self.bstack1ll11l1l11l_opy_ = bstack1ll11l1l11l_opy_