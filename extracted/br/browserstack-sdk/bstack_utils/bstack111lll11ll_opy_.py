# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l1l11lll_opy_, bstack111lll11l11_opy_
from bstack_utils.bstack111llll1_opy_ import bstack1111111ll1l_opy_
class bstack111l11ll1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1llllll11lll_opy_=None, bstack1llllll111l1_opy_=True, bstack1l11111ll1l_opy_=None, bstack1l1111ll1_opy_=None, result=None, duration=None, bstack111l11l1l1_opy_=None, meta={}):
        self.bstack111l11l1l1_opy_ = bstack111l11l1l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llllll111l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llllll11lll_opy_ = bstack1llllll11lll_opy_
        self.bstack1l11111ll1l_opy_ = bstack1l11111ll1l_opy_
        self.bstack1l1111ll1_opy_ = bstack1l1111ll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l11111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll1l1l_opy_(self, meta):
        self.meta = meta
    def bstack111ll1llll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1llllll111ll_opy_(self):
        bstack1llllll11ll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ“"): bstack1llllll11ll1_opy_,
            bstack11l1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ”"): bstack1llllll11ll1_opy_,
            bstack11l1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ„"): bstack1llllll11ll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨ‟") + key)
            setattr(self, key, val)
    def bstack1lllll1ll11l_opy_(self):
        return {
            bstack11l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ†"): self.name,
            bstack11l1_opy_ (u"ࠧࡣࡱࡧࡽࠬ‡"): {
                bstack11l1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭•"): bstack11l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ‣"),
                bstack11l1_opy_ (u"ࠪࡧࡴࡪࡥࠨ․"): self.code
            },
            bstack11l1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ‥"): self.scope,
            bstack11l1_opy_ (u"ࠬࡺࡡࡨࡵࠪ…"): self.tags,
            bstack11l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ‧"): self.framework,
            bstack11l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ "): self.started_at
        }
    def bstack1lllll1ll1l1_opy_(self):
        return {
         bstack11l1_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ "): self.meta
        }
    def bstack1llllll11l11_opy_(self):
        return {
            bstack11l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ‪"): {
                bstack11l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧ‫"): self.bstack1llllll11lll_opy_
            }
        }
    def bstack1lllll1lllll_opy_(self, bstack1lllll1lll11_opy_, details):
        step = next(filter(lambda st: st[bstack11l1_opy_ (u"ࠫ࡮ࡪࠧ‬")] == bstack1lllll1lll11_opy_, self.meta[bstack11l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ‭")]), None)
        step.update(details)
    def bstack1l1l111l_opy_(self, bstack1lllll1lll11_opy_):
        step = next(filter(lambda st: st[bstack11l1_opy_ (u"࠭ࡩࡥࠩ‮")] == bstack1lllll1lll11_opy_, self.meta[bstack11l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ ")]), None)
        step.update({
            bstack11l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ‰"): bstack1l1l11lll_opy_()
        })
    def bstack111ll111ll_opy_(self, bstack1lllll1lll11_opy_, result, duration=None):
        bstack1l11111ll1l_opy_ = bstack1l1l11lll_opy_()
        if bstack1lllll1lll11_opy_ is not None and self.meta.get(bstack11l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ‱")):
            step = next(filter(lambda st: st[bstack11l1_opy_ (u"ࠪ࡭ࡩ࠭′")] == bstack1lllll1lll11_opy_, self.meta[bstack11l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ″")]), None)
            step.update({
                bstack11l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ‴"): bstack1l11111ll1l_opy_,
                bstack11l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ‵"): duration if duration else bstack111lll11l11_opy_(step[bstack11l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ‶")], bstack1l11111ll1l_opy_),
                bstack11l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ‷"): result.result,
                bstack11l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ‸"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llllll11l1l_opy_):
        if self.meta.get(bstack11l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ‹")):
            self.meta[bstack11l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ›")].append(bstack1llllll11l1l_opy_)
        else:
            self.meta[bstack11l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ※")] = [ bstack1llllll11l1l_opy_ ]
    def bstack1llllll11111_opy_(self):
        return {
            bstack11l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ‼"): self.bstack111l11111l_opy_(),
            **self.bstack1lllll1ll11l_opy_(),
            **self.bstack1llllll111ll_opy_(),
            **self.bstack1lllll1ll1l1_opy_()
        }
    def bstack1llllll1111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ‽"): self.bstack1l11111ll1l_opy_,
            bstack11l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ‾"): self.duration,
            bstack11l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ‿"): self.result.result
        }
        if data[bstack11l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⁀")] == bstack11l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⁁"):
            data[bstack11l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⁂")] = self.result.bstack11111l111l_opy_()
            data[bstack11l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⁃")] = [{bstack11l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⁄"): self.result.bstack11l11l11lll_opy_()}]
        return data
    def bstack1lllll1lll1l_opy_(self):
        return {
            bstack11l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁅"): self.bstack111l11111l_opy_(),
            **self.bstack1lllll1ll11l_opy_(),
            **self.bstack1llllll111ll_opy_(),
            **self.bstack1llllll1111l_opy_(),
            **self.bstack1lllll1ll1l1_opy_()
        }
    def bstack111l111lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪ⁆") in event:
            return self.bstack1llllll11111_opy_()
        elif bstack11l1_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁇") in event:
            return self.bstack1lllll1lll1l_opy_()
    def bstack1111ll1ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11111ll1l_opy_ = time if time else bstack1l1l11lll_opy_()
        self.duration = duration if duration else bstack111lll11l11_opy_(self.started_at, self.bstack1l11111ll1l_opy_)
        if result:
            self.result = result
class bstack111ll11l11_opy_(bstack111l11ll1l_opy_):
    def __init__(self, hooks=[], bstack111ll11l1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
        super().__init__(*args, **kwargs, bstack1l1111ll1_opy_=bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⁈"))
    @classmethod
    def bstack1lllll1ll1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1_opy_ (u"ࠬ࡯ࡤࠨ⁉"): id(step),
                bstack11l1_opy_ (u"࠭ࡴࡦࡺࡷࠫ⁊"): step.name,
                bstack11l1_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ⁋"): step.keyword,
            })
        return bstack111ll11l11_opy_(
            **kwargs,
            meta={
                bstack11l1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ⁌"): {
                    bstack11l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⁍"): feature.name,
                    bstack11l1_opy_ (u"ࠪࡴࡦࡺࡨࠨ⁎"): feature.filename,
                    bstack11l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ⁏"): feature.description
                },
                bstack11l1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ⁐"): {
                    bstack11l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁑"): scenario.name
                },
                bstack11l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⁒"): steps,
                bstack11l1_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪ⁓"): bstack1111111ll1l_opy_(test)
            }
        )
    def bstack1lllll1l1lll_opy_(self):
        return {
            bstack11l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⁔"): self.hooks
        }
    def bstack1lllll1ll111_opy_(self):
        if self.bstack111ll11l1l_opy_:
            return {
                bstack11l1_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ⁕"): self.bstack111ll11l1l_opy_
            }
        return {}
    def bstack1lllll1lll1l_opy_(self):
        return {
            **super().bstack1lllll1lll1l_opy_(),
            **self.bstack1lllll1l1lll_opy_()
        }
    def bstack1llllll11111_opy_(self):
        return {
            **super().bstack1llllll11111_opy_(),
            **self.bstack1lllll1ll111_opy_()
        }
    def bstack1111ll1ll1_opy_(self):
        return bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⁖")
class bstack111ll1l11l_opy_(bstack111l11ll1l_opy_):
    def __init__(self, hook_type, *args,bstack111ll11l1l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll111l1l1l_opy_ = None
        self.bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_
        super().__init__(*args, **kwargs, bstack1l1111ll1_opy_=bstack11l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⁗"))
    def bstack111l1l1l1l_opy_(self):
        return self.hook_type
    def bstack1lllll1llll1_opy_(self):
        return {
            bstack11l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⁘"): self.hook_type
        }
    def bstack1lllll1lll1l_opy_(self):
        return {
            **super().bstack1lllll1lll1l_opy_(),
            **self.bstack1lllll1llll1_opy_()
        }
    def bstack1llllll11111_opy_(self):
        return {
            **super().bstack1llllll11111_opy_(),
            bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⁙"): self.bstack1ll111l1l1l_opy_,
            **self.bstack1lllll1llll1_opy_()
        }
    def bstack1111ll1ll1_opy_(self):
        return bstack11l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ⁚")
    def bstack111ll1lll1_opy_(self, bstack1ll111l1l1l_opy_):
        self.bstack1ll111l1l1l_opy_ = bstack1ll111l1l1l_opy_