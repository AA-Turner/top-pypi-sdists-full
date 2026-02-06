# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1lll11lll1_opy_, bstack111ll1l1ll1_opy_
from bstack_utils.bstack11ll1ll11_opy_ import bstack1llll111l111_opy_
class bstack111111llll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll1l1l1lll_opy_=None, bstack1lll1l11lll1_opy_=True, bstack11lll11ll1l_opy_=None, bstack11l11l111l_opy_=None, result=None, duration=None, bstack11111lll11_opy_=None, meta={}):
        self.bstack11111lll11_opy_ = bstack11111lll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1l11lll1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1l1l1lll_opy_ = bstack1lll1l1l1lll_opy_
        self.bstack11lll11ll1l_opy_ = bstack11lll11ll1l_opy_
        self.bstack11l11l111l_opy_ = bstack11l11l111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1111111ll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111ll111l_opy_(self, meta):
        self.meta = meta
    def bstack111l1111l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll1l1lll1l_opy_(self):
        bstack1lll1l1l1l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⇒"): bstack1lll1l1l1l11_opy_,
            bstack11lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⇓"): bstack1lll1l1l1l11_opy_,
            bstack11lllll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⇔"): bstack1lll1l1l1l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11lllll_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ⇕") + key)
            setattr(self, key, val)
    def bstack1lll1l1l111l_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⇖"): self.name,
            bstack11lllll_opy_ (u"ࠫࡧࡵࡤࡺࠩ⇗"): {
                bstack11lllll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⇘"): bstack11lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⇙"),
                bstack11lllll_opy_ (u"ࠧࡤࡱࡧࡩࠬ⇚"): self.code
            },
            bstack11lllll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⇛"): self.scope,
            bstack11lllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⇜"): self.tags,
            bstack11lllll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⇝"): self.framework,
            bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⇞"): self.started_at
        }
    def bstack1lll1l11llll_opy_(self):
        return {
         bstack11lllll_opy_ (u"ࠬࡳࡥࡵࡣࠪ⇟"): self.meta
        }
    def bstack1lll1l1llll1_opy_(self):
        return {
            bstack11lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ⇠"): {
                bstack11lllll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ⇡"): self.bstack1lll1l1l1lll_opy_
            }
        }
    def bstack1lll1l1l11ll_opy_(self, bstack1lll1l1l1l1l_opy_, details):
        step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫ⇢")] == bstack1lll1l1l1l1l_opy_, self.meta[bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⇣")]), None)
        step.update(details)
    def bstack111ll1llll_opy_(self, bstack1lll1l1l1l1l_opy_):
        step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭⇤")] == bstack1lll1l1l1l1l_opy_, self.meta[bstack11lllll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⇥")]), None)
        step.update({
            bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⇦"): bstack1lll11lll1_opy_()
        })
    def bstack1111l1llll_opy_(self, bstack1lll1l1l1l1l_opy_, result, duration=None):
        bstack11lll11ll1l_opy_ = bstack1lll11lll1_opy_()
        if bstack1lll1l1l1l1l_opy_ is not None and self.meta.get(bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⇧")):
            step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠧࡪࡦࠪ⇨")] == bstack1lll1l1l1l1l_opy_, self.meta[bstack11lllll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⇩")]), None)
            step.update({
                bstack11lllll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⇪"): bstack11lll11ll1l_opy_,
                bstack11lllll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⇫"): duration if duration else bstack111ll1l1ll1_opy_(step[bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⇬")], bstack11lll11ll1l_opy_),
                bstack11lllll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⇭"): result.result,
                bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⇮"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1l1lll11_opy_):
        if self.meta.get(bstack11lllll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⇯")):
            self.meta[bstack11lllll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⇰")].append(bstack1lll1l1lll11_opy_)
        else:
            self.meta[bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⇱")] = [ bstack1lll1l1lll11_opy_ ]
    def bstack1lll1l1ll1ll_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⇲"): self.bstack1111111ll1_opy_(),
            bstack11lllll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⇳"): bstack11lllll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⇴"),
            **self.bstack1lll1l1l111l_opy_(),
            **self.bstack1lll1l1lll1l_opy_(),
            **self.bstack1lll1l11llll_opy_()
        }
    def bstack1lll1l1ll11l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11lllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⇵"): self.bstack11lll11ll1l_opy_,
            bstack11lllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⇶"): self.duration,
            bstack11lllll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇷"): self.result.result
        }
        if data[bstack11lllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⇸")] == bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⇹"):
            data[bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⇺")] = self.result.bstack1llll1111ll_opy_()
            data[bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⇻")] = [{bstack11lllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⇼"): self.result.bstack111ll11lll1_opy_()}]
        return data
    def bstack1lll1l1ll111_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⇽"): self.bstack1111111ll1_opy_(),
            **self.bstack1lll1l1l111l_opy_(),
            **self.bstack1lll1l1lll1l_opy_(),
            **self.bstack1lll1l1ll11l_opy_(),
            **self.bstack1lll1l11llll_opy_()
        }
    def bstack11111l11ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11lllll_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ⇾") in event:
            return self.bstack1lll1l1ll1ll_opy_()
        elif bstack11lllll_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⇿") in event:
            return self.bstack1lll1l1ll111_opy_()
    def bstack11111111l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11lll11ll1l_opy_ = time if time else bstack1lll11lll1_opy_()
        self.duration = duration if duration else bstack111ll1l1ll1_opy_(self.started_at, self.bstack11lll11ll1l_opy_)
        if result:
            self.result = result
class bstack1111ll11ll_opy_(bstack111111llll_opy_):
    def __init__(self, hooks=[], bstack1111lllll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
        super().__init__(*args, **kwargs, bstack11l11l111l_opy_=bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࠨ∀"))
    @classmethod
    def bstack1lll1l1ll1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧ∁"): id(step),
                bstack11lllll_opy_ (u"ࠬࡺࡥࡹࡶࠪ∂"): step.name,
                bstack11lllll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ∃"): step.keyword,
            })
        return bstack1111ll11ll_opy_(
            **kwargs,
            meta={
                bstack11lllll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ∄"): {
                    bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭∅"): feature.name,
                    bstack11lllll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ∆"): feature.filename,
                    bstack11lllll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ∇"): feature.description
                },
                bstack11lllll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭∈"): {
                    bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ∉"): scenario.name
                },
                bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ∊"): steps,
                bstack11lllll_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ∋"): bstack1llll111l111_opy_(test)
            }
        )
    def bstack1lll1l1l11l1_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ∌"): self.hooks
        }
    def bstack1lll1l1l1ll1_opy_(self):
        if self.bstack1111lllll1_opy_:
            return {
                bstack11lllll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ∍"): self.bstack1111lllll1_opy_
            }
        return {}
    def bstack1lll1l1ll111_opy_(self):
        return {
            **super().bstack1lll1l1ll111_opy_(),
            **self.bstack1lll1l1l11l1_opy_()
        }
    def bstack1lll1l1ll1ll_opy_(self):
        return {
            **super().bstack1lll1l1ll1ll_opy_(),
            **self.bstack1lll1l1l1ll1_opy_()
        }
    def bstack11111111l1_opy_(self):
        return bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ∎")
class bstack1111ll1lll_opy_(bstack111111llll_opy_):
    def __init__(self, hook_type, *args,bstack1111lllll1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l1ll111l_opy_ = None
        self.bstack1111lllll1_opy_ = bstack1111lllll1_opy_
        super().__init__(*args, **kwargs, bstack11l11l111l_opy_=bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ∏"))
    def bstack111111l1ll_opy_(self):
        return self.hook_type
    def bstack1lll1l1l1111_opy_(self):
        return {
            bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ∐"): self.hook_type
        }
    def bstack1lll1l1ll111_opy_(self):
        return {
            **super().bstack1lll1l1ll111_opy_(),
            **self.bstack1lll1l1l1111_opy_()
        }
    def bstack1lll1l1ll1ll_opy_(self):
        return {
            **super().bstack1lll1l1ll1ll_opy_(),
            bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ∑"): self.bstack1l1l1ll111l_opy_,
            **self.bstack1lll1l1l1111_opy_()
        }
    def bstack11111111l1_opy_(self):
        return bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ−")
    def bstack1111ll1111_opy_(self, bstack1l1l1ll111l_opy_):
        self.bstack1l1l1ll111l_opy_ = bstack1l1l1ll111l_opy_