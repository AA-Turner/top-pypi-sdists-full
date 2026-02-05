# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1ll1llll11_opy_, bstack111l111l11l_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack1llll1111lll_opy_
class bstack1111l11ll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll1l1ll1ll_opy_=None, bstack1lll1ll11l11_opy_=True, bstack11lll1lll1l_opy_=None, bstack1lllll1111_opy_=None, result=None, duration=None, bstack11111lll11_opy_=None, meta={}):
        self.bstack11111lll11_opy_ = bstack11111lll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1ll11l11_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1l1ll1ll_opy_ = bstack1lll1l1ll1ll_opy_
        self.bstack11lll1lll1l_opy_ = bstack11lll1lll1l_opy_
        self.bstack1lllll1111_opy_ = bstack1lllll1111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11111ll111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l111111_opy_(self, meta):
        self.meta = meta
    def bstack1111llllll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll1l1lll11_opy_(self):
        bstack1lll1l1l1ll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ↲"): bstack1lll1l1l1ll1_opy_,
            bstack11l1ll1_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ↳"): bstack1lll1l1l1ll1_opy_,
            bstack11l1ll1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ↴"): bstack1lll1l1l1ll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1ll1_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨ↵") + key)
            setattr(self, key, val)
    def bstack1lll1l1l1lll_opy_(self):
        return {
            bstack11l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ↶"): self.name,
            bstack11l1ll1_opy_ (u"ࠧࡣࡱࡧࡽࠬ↷"): {
                bstack11l1ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭↸"): bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ↹"),
                bstack11l1ll1_opy_ (u"ࠪࡧࡴࡪࡥࠨ↺"): self.code
            },
            bstack11l1ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ↻"): self.scope,
            bstack11l1ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪ↼"): self.tags,
            bstack11l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ↽"): self.framework,
            bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↾"): self.started_at
        }
    def bstack1lll1ll11111_opy_(self):
        return {
         bstack11l1ll1_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭↿"): self.meta
        }
    def bstack1lll1ll111l1_opy_(self):
        return {
            bstack11l1ll1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ⇀"): {
                bstack11l1ll1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧ⇁"): self.bstack1lll1l1ll1ll_opy_
            }
        }
    def bstack1lll1ll1111l_opy_(self, bstack1lll1ll111ll_opy_, details):
        step = next(filter(lambda st: st[bstack11l1ll1_opy_ (u"ࠫ࡮ࡪࠧ⇂")] == bstack1lll1ll111ll_opy_, self.meta[bstack11l1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⇃")]), None)
        step.update(details)
    def bstack11lllll11_opy_(self, bstack1lll1ll111ll_opy_):
        step = next(filter(lambda st: st[bstack11l1ll1_opy_ (u"࠭ࡩࡥࠩ⇄")] == bstack1lll1ll111ll_opy_, self.meta[bstack11l1ll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⇅")]), None)
        step.update({
            bstack11l1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⇆"): bstack1ll1llll11_opy_()
        })
    def bstack1111l1l11l_opy_(self, bstack1lll1ll111ll_opy_, result, duration=None):
        bstack11lll1lll1l_opy_ = bstack1ll1llll11_opy_()
        if bstack1lll1ll111ll_opy_ is not None and self.meta.get(bstack11l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⇇")):
            step = next(filter(lambda st: st[bstack11l1ll1_opy_ (u"ࠪ࡭ࡩ࠭⇈")] == bstack1lll1ll111ll_opy_, self.meta[bstack11l1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⇉")]), None)
            step.update({
                bstack11l1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⇊"): bstack11lll1lll1l_opy_,
                bstack11l1ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⇋"): duration if duration else bstack111l111l11l_opy_(step[bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⇌")], bstack11lll1lll1l_opy_),
                bstack11l1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇍"): result.result,
                bstack11l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⇎"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1l1l1l1l_opy_):
        if self.meta.get(bstack11l1ll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⇏")):
            self.meta[bstack11l1ll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⇐")].append(bstack1lll1l1l1l1l_opy_)
        else:
            self.meta[bstack11l1ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⇑")] = [ bstack1lll1l1l1l1l_opy_ ]
    def bstack1lll1l1l1l11_opy_(self):
        return {
            bstack11l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⇒"): self.bstack11111ll111_opy_(),
            bstack11l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⇓"): bstack11l1ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⇔"),
            **self.bstack1lll1l1l1lll_opy_(),
            **self.bstack1lll1l1lll11_opy_(),
            **self.bstack1lll1ll11111_opy_()
        }
    def bstack1lll1l1llll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⇕"): self.bstack11lll1lll1l_opy_,
            bstack11l1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⇖"): self.duration,
            bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⇗"): self.result.result
        }
        if data[bstack11l1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⇘")] == bstack11l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⇙"):
            data[bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⇚")] = self.result.bstack1llll11111l_opy_()
            data[bstack11l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⇛")] = [{bstack11l1ll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⇜"): self.result.bstack111l1l1l111_opy_()}]
        return data
    def bstack1lll1l1ll111_opy_(self):
        return {
            bstack11l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⇝"): self.bstack11111ll111_opy_(),
            **self.bstack1lll1l1l1lll_opy_(),
            **self.bstack1lll1l1lll11_opy_(),
            **self.bstack1lll1l1llll1_opy_(),
            **self.bstack1lll1ll11111_opy_()
        }
    def bstack1111l11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1ll1_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬ⇞") in event:
            return self.bstack1lll1l1l1l11_opy_()
        elif bstack11l1ll1_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⇟") in event:
            return self.bstack1lll1l1ll111_opy_()
    def bstack11111lll1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11lll1lll1l_opy_ = time if time else bstack1ll1llll11_opy_()
        self.duration = duration if duration else bstack111l111l11l_opy_(self.started_at, self.bstack11lll1lll1l_opy_)
        if result:
            self.result = result
class bstack111l1111ll_opy_(bstack1111l11ll1_opy_):
    def __init__(self, hooks=[], bstack1111l1l1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        super().__init__(*args, **kwargs, bstack1lllll1111_opy_=bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ⇠"))
    @classmethod
    def bstack1lll1l1lll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1ll1_opy_ (u"ࠧࡪࡦࠪ⇡"): id(step),
                bstack11l1ll1_opy_ (u"ࠨࡶࡨࡼࡹ࠭⇢"): step.name,
                bstack11l1ll1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ⇣"): step.keyword,
            })
        return bstack111l1111ll_opy_(
            **kwargs,
            meta={
                bstack11l1ll1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫ⇤"): {
                    bstack11l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⇥"): feature.name,
                    bstack11l1ll1_opy_ (u"ࠬࡶࡡࡵࡪࠪ⇦"): feature.filename,
                    bstack11l1ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⇧"): feature.description
                },
                bstack11l1ll1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ⇨"): {
                    bstack11l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭⇩"): scenario.name
                },
                bstack11l1ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⇪"): steps,
                bstack11l1ll1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬ⇫"): bstack1llll1111lll_opy_(test)
            }
        )
    def bstack1lll1l1ll11l_opy_(self):
        return {
            bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⇬"): self.hooks
        }
    def bstack1lll1l1lllll_opy_(self):
        if self.bstack1111l1l1l1_opy_:
            return {
                bstack11l1ll1_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ⇭"): self.bstack1111l1l1l1_opy_
            }
        return {}
    def bstack1lll1l1ll111_opy_(self):
        return {
            **super().bstack1lll1l1ll111_opy_(),
            **self.bstack1lll1l1ll11l_opy_()
        }
    def bstack1lll1l1l1l11_opy_(self):
        return {
            **super().bstack1lll1l1l1l11_opy_(),
            **self.bstack1lll1l1lllll_opy_()
        }
    def bstack11111lll1l_opy_(self):
        return bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⇮")
class bstack1111lll1l1_opy_(bstack1111l11ll1_opy_):
    def __init__(self, hook_type, *args,bstack1111l1l1l1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1lll111l1_opy_ = None
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        super().__init__(*args, **kwargs, bstack1lllll1111_opy_=bstack11l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⇯"))
    def bstack1llllllll11_opy_(self):
        return self.hook_type
    def bstack1lll1l1ll1l1_opy_(self):
        return {
            bstack11l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⇰"): self.hook_type
        }
    def bstack1lll1l1ll111_opy_(self):
        return {
            **super().bstack1lll1l1ll111_opy_(),
            **self.bstack1lll1l1ll1l1_opy_()
        }
    def bstack1lll1l1l1l11_opy_(self):
        return {
            **super().bstack1lll1l1l1l11_opy_(),
            bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ⇱"): self.bstack1l1lll111l1_opy_,
            **self.bstack1lll1l1ll1l1_opy_()
        }
    def bstack11111lll1l_opy_(self):
        return bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ⇲")
    def bstack1111ll1lll_opy_(self, bstack1l1lll111l1_opy_):
        self.bstack1l1lll111l1_opy_ = bstack1l1lll111l1_opy_