# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1111l11l1_opy_, bstack111l1l1l1ll_opy_
from bstack_utils.bstack11l11l11ll_opy_ import bstack1llll11l1l11_opy_
class bstack111111111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll1ll1l1ll_opy_=None, bstack1lll1ll11ll1_opy_=True, bstack11lll1111ll_opy_=None, bstack1ll11l11ll_opy_=None, result=None, duration=None, bstack1111l111ll_opy_=None, meta={}):
        self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1ll11ll1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1ll1l1ll_opy_ = bstack1lll1ll1l1ll_opy_
        self.bstack11lll1111ll_opy_ = bstack11lll1111ll_opy_
        self.bstack1ll11l11ll_opy_ = bstack1ll11l11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111l1l111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111l1ll1l_opy_(self, meta):
        self.meta = meta
    def bstack1111ll1l1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll1l1ll1ll_opy_(self):
        bstack1lll1ll11111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ↮"): bstack1lll1ll11111_opy_,
            bstack1l1111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ↯"): bstack1lll1ll11111_opy_,
            bstack1l1111_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ↰"): bstack1lll1ll11111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1111_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤ↱") + key)
            setattr(self, key, val)
    def bstack1lll1ll11lll_opy_(self):
        return {
            bstack1l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ↲"): self.name,
            bstack1l1111_opy_ (u"ࠪࡦࡴࡪࡹࠨ↳"): {
                bstack1l1111_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ↴"): bstack1l1111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ↵"),
                bstack1l1111_opy_ (u"࠭ࡣࡰࡦࡨࠫ↶"): self.code
            },
            bstack1l1111_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ↷"): self.scope,
            bstack1l1111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭↸"): self.tags,
            bstack1l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ↹"): self.framework,
            bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ↺"): self.started_at
        }
    def bstack1lll1l1llll1_opy_(self):
        return {
         bstack1l1111_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ↻"): self.meta
        }
    def bstack1lll1l1lll1l_opy_(self):
        return {
            bstack1l1111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ↼"): {
                bstack1l1111_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ↽"): self.bstack1lll1ll1l1ll_opy_
            }
        }
    def bstack1lll1ll11l1l_opy_(self, bstack1lll1ll111l1_opy_, details):
        step = next(filter(lambda st: st[bstack1l1111_opy_ (u"ࠧࡪࡦࠪ↾")] == bstack1lll1ll111l1_opy_, self.meta[bstack1l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ↿")]), None)
        step.update(details)
    def bstack1ll1ll11ll_opy_(self, bstack1lll1ll111l1_opy_):
        step = next(filter(lambda st: st[bstack1l1111_opy_ (u"ࠩ࡬ࡨࠬ⇀")] == bstack1lll1ll111l1_opy_, self.meta[bstack1l1111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⇁")]), None)
        step.update({
            bstack1l1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⇂"): bstack1111l11l1_opy_()
        })
    def bstack1111llllll_opy_(self, bstack1lll1ll111l1_opy_, result, duration=None):
        bstack11lll1111ll_opy_ = bstack1111l11l1_opy_()
        if bstack1lll1ll111l1_opy_ is not None and self.meta.get(bstack1l1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⇃")):
            step = next(filter(lambda st: st[bstack1l1111_opy_ (u"࠭ࡩࡥࠩ⇄")] == bstack1lll1ll111l1_opy_, self.meta[bstack1l1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⇅")]), None)
            step.update({
                bstack1l1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⇆"): bstack11lll1111ll_opy_,
                bstack1l1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⇇"): duration if duration else bstack111l1l1l1ll_opy_(step[bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⇈")], bstack11lll1111ll_opy_),
                bstack1l1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⇉"): result.result,
                bstack1l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⇊"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1l1lllll_opy_):
        if self.meta.get(bstack1l1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⇋")):
            self.meta[bstack1l1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⇌")].append(bstack1lll1l1lllll_opy_)
        else:
            self.meta[bstack1l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⇍")] = [ bstack1lll1l1lllll_opy_ ]
    def bstack1lll1ll1l1l1_opy_(self):
        return {
            bstack1l1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⇎"): self.bstack1111l1l111_opy_(),
            bstack1l1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⇏"): bstack1l1111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⇐"),
            **self.bstack1lll1ll11lll_opy_(),
            **self.bstack1lll1l1ll1ll_opy_(),
            **self.bstack1lll1l1llll1_opy_()
        }
    def bstack1lll1ll111ll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⇑"): self.bstack11lll1111ll_opy_,
            bstack1l1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⇒"): self.duration,
            bstack1l1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⇓"): self.result.result
        }
        if data[bstack1l1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇔")] == bstack1l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⇕"):
            data[bstack1l1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⇖")] = self.result.bstack1llll1111l1_opy_()
            data[bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⇗")] = [{bstack1l1111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⇘"): self.result.bstack111l1lll11l_opy_()}]
        return data
    def bstack1lll1ll1111l_opy_(self):
        return {
            bstack1l1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⇙"): self.bstack1111l1l111_opy_(),
            **self.bstack1lll1ll11lll_opy_(),
            **self.bstack1lll1l1ll1ll_opy_(),
            **self.bstack1lll1ll111ll_opy_(),
            **self.bstack1lll1l1llll1_opy_()
        }
    def bstack111111llll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1111_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ⇚") in event:
            return self.bstack1lll1ll1l1l1_opy_()
        elif bstack1l1111_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⇛") in event:
            return self.bstack1lll1ll1111l_opy_()
    def bstack11111ll1l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11lll1111ll_opy_ = time if time else bstack1111l11l1_opy_()
        self.duration = duration if duration else bstack111l1l1l1ll_opy_(self.started_at, self.bstack11lll1111ll_opy_)
        if result:
            self.result = result
class bstack1111llll1l_opy_(bstack111111111l_opy_):
    def __init__(self, hooks=[], bstack1111ll11ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
        super().__init__(*args, **kwargs, bstack1ll11l11ll_opy_=bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺࠧ⇜"))
    @classmethod
    def bstack1lll1ll11l11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1111_opy_ (u"ࠪ࡭ࡩ࠭⇝"): id(step),
                bstack1l1111_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ⇞"): step.name,
                bstack1l1111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭⇟"): step.keyword,
            })
        return bstack1111llll1l_opy_(
            **kwargs,
            meta={
                bstack1l1111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ⇠"): {
                    bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⇡"): feature.name,
                    bstack1l1111_opy_ (u"ࠨࡲࡤࡸ࡭࠭⇢"): feature.filename,
                    bstack1l1111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ⇣"): feature.description
                },
                bstack1l1111_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ⇤"): {
                    bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⇥"): scenario.name
                },
                bstack1l1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⇦"): steps,
                bstack1l1111_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ⇧"): bstack1llll11l1l11_opy_(test)
            }
        )
    def bstack1lll1ll1l11l_opy_(self):
        return {
            bstack1l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⇨"): self.hooks
        }
    def bstack1lll1ll1l111_opy_(self):
        if self.bstack1111ll11ll_opy_:
            return {
                bstack1l1111_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ⇩"): self.bstack1111ll11ll_opy_
            }
        return {}
    def bstack1lll1ll1111l_opy_(self):
        return {
            **super().bstack1lll1ll1111l_opy_(),
            **self.bstack1lll1ll1l11l_opy_()
        }
    def bstack1lll1ll1l1l1_opy_(self):
        return {
            **super().bstack1lll1ll1l1l1_opy_(),
            **self.bstack1lll1ll1l111_opy_()
        }
    def bstack11111ll1l1_opy_(self):
        return bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⇪")
class bstack1111ll1l11_opy_(bstack111111111l_opy_):
    def __init__(self, hook_type, *args,bstack1111ll11ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1ll1l1111_opy_ = None
        self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
        super().__init__(*args, **kwargs, bstack1ll11l11ll_opy_=bstack1l1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⇫"))
    def bstack1111111111_opy_(self):
        return self.hook_type
    def bstack1lll1l1lll11_opy_(self):
        return {
            bstack1l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⇬"): self.hook_type
        }
    def bstack1lll1ll1111l_opy_(self):
        return {
            **super().bstack1lll1ll1111l_opy_(),
            **self.bstack1lll1l1lll11_opy_()
        }
    def bstack1lll1ll1l1l1_opy_(self):
        return {
            **super().bstack1lll1ll1l1l1_opy_(),
            bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⇭"): self.bstack1l1ll1l1111_opy_,
            **self.bstack1lll1l1lll11_opy_()
        }
    def bstack11111ll1l1_opy_(self):
        return bstack1l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ⇮")
    def bstack111l111111_opy_(self, bstack1l1ll1l1111_opy_):
        self.bstack1l1ll1l1111_opy_ = bstack1l1ll1l1111_opy_