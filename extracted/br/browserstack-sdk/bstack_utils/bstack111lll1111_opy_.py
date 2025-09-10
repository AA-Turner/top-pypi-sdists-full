# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11l1l1l1l1_opy_, bstack11l11l111ll_opy_
from bstack_utils.bstack11lll1l111_opy_ import bstack1lllllll1111_opy_
class bstack1111l1lll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllll111lll_opy_=None, bstack1lllll11l111_opy_=True, bstack1l111lllll1_opy_=None, bstack1ll1l11ll1_opy_=None, result=None, duration=None, bstack111l1111l1_opy_=None, meta={}):
        self.bstack111l1111l1_opy_ = bstack111l1111l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllll11l111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllll111lll_opy_ = bstack1lllll111lll_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.bstack1ll1l11ll1_opy_ = bstack1ll1l11ll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l11lll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll11l1_opy_(self, meta):
        self.meta = meta
    def bstack111lll111l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllll11l1ll_opy_(self):
        bstack1lllll1l1111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll11ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ‚"): bstack1lllll1l1111_opy_,
            bstack1ll11ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ‛"): bstack1lllll1l1111_opy_,
            bstack1ll11ll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ“"): bstack1lllll1l1111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll11ll_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦ”") + key)
            setattr(self, key, val)
    def bstack1lllll11l1l1_opy_(self):
        return {
            bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ„"): self.name,
            bstack1ll11ll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ‟"): {
                bstack1ll11ll_opy_ (u"࠭࡬ࡢࡰࡪࠫ†"): bstack1ll11ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ‡"),
                bstack1ll11ll_opy_ (u"ࠨࡥࡲࡨࡪ࠭•"): self.code
            },
            bstack1ll11ll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ‣"): self.scope,
            bstack1ll11ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ․"): self.tags,
            bstack1ll11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ‥"): self.framework,
            bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ…"): self.started_at
        }
    def bstack1lllll11lll1_opy_(self):
        return {
         bstack1ll11ll_opy_ (u"࠭࡭ࡦࡶࡤࠫ‧"): self.meta
        }
    def bstack1lllll11ll1l_opy_(self):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ "): {
                bstack1ll11ll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ "): self.bstack1lllll111lll_opy_
            }
        }
    def bstack1lllll11llll_opy_(self, bstack1lllll1l11l1_opy_, details):
        step = next(filter(lambda st: st[bstack1ll11ll_opy_ (u"ࠩ࡬ࡨࠬ‪")] == bstack1lllll1l11l1_opy_, self.meta[bstack1ll11ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ‫")]), None)
        step.update(details)
    def bstack11llll1ll_opy_(self, bstack1lllll1l11l1_opy_):
        step = next(filter(lambda st: st[bstack1ll11ll_opy_ (u"ࠫ࡮ࡪࠧ‬")] == bstack1lllll1l11l1_opy_, self.meta[bstack1ll11ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ‭")]), None)
        step.update({
            bstack1ll11ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ‮"): bstack11l1l1l1l1_opy_()
        })
    def bstack111ll1lll1_opy_(self, bstack1lllll1l11l1_opy_, result, duration=None):
        bstack1l111lllll1_opy_ = bstack11l1l1l1l1_opy_()
        if bstack1lllll1l11l1_opy_ is not None and self.meta.get(bstack1ll11ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ ")):
            step = next(filter(lambda st: st[bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫ‰")] == bstack1lllll1l11l1_opy_, self.meta[bstack1ll11ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ‱")]), None)
            step.update({
                bstack1ll11ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ′"): bstack1l111lllll1_opy_,
                bstack1ll11ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭″"): duration if duration else bstack11l11l111ll_opy_(step[bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ‴")], bstack1l111lllll1_opy_),
                bstack1ll11ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭‵"): result.result,
                bstack1ll11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ‶"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllll11ll11_opy_):
        if self.meta.get(bstack1ll11ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ‷")):
            self.meta[bstack1ll11ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ‸")].append(bstack1lllll11ll11_opy_)
        else:
            self.meta[bstack1ll11ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ‹")] = [ bstack1lllll11ll11_opy_ ]
    def bstack1lllll1l1ll1_opy_(self):
        return {
            bstack1ll11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ›"): self.bstack111l11lll1_opy_(),
            **self.bstack1lllll11l1l1_opy_(),
            **self.bstack1lllll11l1ll_opy_(),
            **self.bstack1lllll11lll1_opy_()
        }
    def bstack1lllll1l1l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll11ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ※"): self.bstack1l111lllll1_opy_,
            bstack1ll11ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ‼"): self.duration,
            bstack1ll11ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ‽"): self.result.result
        }
        if data[bstack1ll11ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ‾")] == bstack1ll11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ‿"):
            data[bstack1ll11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⁀")] = self.result.bstack111111l11l_opy_()
            data[bstack1ll11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⁁")] = [{bstack1ll11ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⁂"): self.result.bstack111lll1111l_opy_()}]
        return data
    def bstack1lllll11l11l_opy_(self):
        return {
            bstack1ll11ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⁃"): self.bstack111l11lll1_opy_(),
            **self.bstack1lllll11l1l1_opy_(),
            **self.bstack1lllll11l1ll_opy_(),
            **self.bstack1lllll1l1l1l_opy_(),
            **self.bstack1lllll11lll1_opy_()
        }
    def bstack111l111l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll11ll_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ⁄") in event:
            return self.bstack1lllll1l1ll1_opy_()
        elif bstack1ll11ll_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⁅") in event:
            return self.bstack1lllll11l11l_opy_()
    def bstack1111ll11ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111lllll1_opy_ = time if time else bstack11l1l1l1l1_opy_()
        self.duration = duration if duration else bstack11l11l111ll_opy_(self.started_at, self.bstack1l111lllll1_opy_)
        if result:
            self.result = result
class bstack111l1ll1ll_opy_(bstack1111l1lll1_opy_):
    def __init__(self, hooks=[], bstack111l1lllll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111l1lllll_opy_ = bstack111l1lllll_opy_
        super().__init__(*args, **kwargs, bstack1ll1l11ll1_opy_=bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺࠧ⁆"))
    @classmethod
    def bstack1lllll1l11ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll11ll_opy_ (u"ࠪ࡭ࡩ࠭⁇"): id(step),
                bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ⁈"): step.name,
                bstack1ll11ll_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭⁉"): step.keyword,
            })
        return bstack111l1ll1ll_opy_(
            **kwargs,
            meta={
                bstack1ll11ll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ⁊"): {
                    bstack1ll11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⁋"): feature.name,
                    bstack1ll11ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭⁌"): feature.filename,
                    bstack1ll11ll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ⁍"): feature.description
                },
                bstack1ll11ll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ⁎"): {
                    bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⁏"): scenario.name
                },
                bstack1ll11ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⁐"): steps,
                bstack1ll11ll_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ⁑"): bstack1lllllll1111_opy_(test)
            }
        )
    def bstack1lllll1l1l11_opy_(self):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⁒"): self.hooks
        }
    def bstack1lllll111ll1_opy_(self):
        if self.bstack111l1lllll_opy_:
            return {
                bstack1ll11ll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ⁓"): self.bstack111l1lllll_opy_
            }
        return {}
    def bstack1lllll11l11l_opy_(self):
        return {
            **super().bstack1lllll11l11l_opy_(),
            **self.bstack1lllll1l1l11_opy_()
        }
    def bstack1lllll1l1ll1_opy_(self):
        return {
            **super().bstack1lllll1l1ll1_opy_(),
            **self.bstack1lllll111ll1_opy_()
        }
    def bstack1111ll11ll_opy_(self):
        return bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⁔")
class bstack111l1lll1l_opy_(bstack1111l1lll1_opy_):
    def __init__(self, hook_type, *args,bstack111l1lllll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11lll1ll_opy_ = None
        self.bstack111l1lllll_opy_ = bstack111l1lllll_opy_
        super().__init__(*args, **kwargs, bstack1ll1l11ll1_opy_=bstack1ll11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⁕"))
    def bstack111l111l1l_opy_(self):
        return self.hook_type
    def bstack1lllll1l111l_opy_(self):
        return {
            bstack1ll11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⁖"): self.hook_type
        }
    def bstack1lllll11l11l_opy_(self):
        return {
            **super().bstack1lllll11l11l_opy_(),
            **self.bstack1lllll1l111l_opy_()
        }
    def bstack1lllll1l1ll1_opy_(self):
        return {
            **super().bstack1lllll1l1ll1_opy_(),
            bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⁗"): self.bstack1ll11lll1ll_opy_,
            **self.bstack1lllll1l111l_opy_()
        }
    def bstack1111ll11ll_opy_(self):
        return bstack1ll11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ⁘")
    def bstack111l1lll11_opy_(self, bstack1ll11lll1ll_opy_):
        self.bstack1ll11lll1ll_opy_ = bstack1ll11lll1ll_opy_