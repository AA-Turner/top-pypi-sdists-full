# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11l11ll1l1_opy_, bstack111llll1ll1_opy_
from bstack_utils.bstack1ll11l11ll_opy_ import bstack1llllllll11l_opy_
class bstack111l11l111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllll1l11ll_opy_=None, bstack1lllll1l1lll_opy_=True, bstack1l111111111_opy_=None, bstack1lllll111_opy_=None, result=None, duration=None, bstack1111ll1l11_opy_=None, meta={}):
        self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllll1l1lll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllll1l11ll_opy_ = bstack1lllll1l11ll_opy_
        self.bstack1l111111111_opy_ = bstack1l111111111_opy_
        self.bstack1lllll111_opy_ = bstack1lllll111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll11111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111ll1111l_opy_(self, meta):
        self.meta = meta
    def bstack111lll11ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lllll1ll1ll_opy_(self):
        bstack1lllll1l1l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1111lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭‖"): bstack1lllll1l1l1l_opy_,
            bstack1111lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭‗"): bstack1lllll1l1l1l_opy_,
            bstack1111lll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ‘"): bstack1lllll1l1l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1111lll_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢ’") + key)
            setattr(self, key, val)
    def bstack1lllll1l1111_opy_(self):
        return {
            bstack1111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ‚"): self.name,
            bstack1111lll_opy_ (u"ࠨࡤࡲࡨࡾ࠭‛"): {
                bstack1111lll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ“"): bstack1111lll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ”"),
                bstack1111lll_opy_ (u"ࠫࡨࡵࡤࡦࠩ„"): self.code
            },
            bstack1111lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ‟"): self.scope,
            bstack1111lll_opy_ (u"࠭ࡴࡢࡩࡶࠫ†"): self.tags,
            bstack1111lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ‡"): self.framework,
            bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ•"): self.started_at
        }
    def bstack1lllll1ll111_opy_(self):
        return {
         bstack1111lll_opy_ (u"ࠩࡰࡩࡹࡧࠧ‣"): self.meta
        }
    def bstack1lllll11llll_opy_(self):
        return {
            bstack1111lll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭․"): {
                bstack1111lll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ‥"): self.bstack1lllll1l11ll_opy_
            }
        }
    def bstack1lllll1l11l1_opy_(self, bstack1lllll1ll1l1_opy_, details):
        step = next(filter(lambda st: st[bstack1111lll_opy_ (u"ࠬ࡯ࡤࠨ…")] == bstack1lllll1ll1l1_opy_, self.meta[bstack1111lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ‧")]), None)
        step.update(details)
    def bstack11lll1l11l_opy_(self, bstack1lllll1ll1l1_opy_):
        step = next(filter(lambda st: st[bstack1111lll_opy_ (u"ࠧࡪࡦࠪ ")] == bstack1lllll1ll1l1_opy_, self.meta[bstack1111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ ")]), None)
        step.update({
            bstack1111lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭‪"): bstack11l11ll1l1_opy_()
        })
    def bstack111ll11l1l_opy_(self, bstack1lllll1ll1l1_opy_, result, duration=None):
        bstack1l111111111_opy_ = bstack11l11ll1l1_opy_()
        if bstack1lllll1ll1l1_opy_ is not None and self.meta.get(bstack1111lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ‫")):
            step = next(filter(lambda st: st[bstack1111lll_opy_ (u"ࠫ࡮ࡪࠧ‬")] == bstack1lllll1ll1l1_opy_, self.meta[bstack1111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ‭")]), None)
            step.update({
                bstack1111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ‮"): bstack1l111111111_opy_,
                bstack1111lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ "): duration if duration else bstack111llll1ll1_opy_(step[bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ‰")], bstack1l111111111_opy_),
                bstack1111lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ‱"): result.result,
                bstack1111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ′"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lllll1l1ll1_opy_):
        if self.meta.get(bstack1111lll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ″")):
            self.meta[bstack1111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ‴")].append(bstack1lllll1l1ll1_opy_)
        else:
            self.meta[bstack1111lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ‵")] = [ bstack1lllll1l1ll1_opy_ ]
    def bstack1lllll11ll1l_opy_(self):
        return {
            bstack1111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ‶"): self.bstack111ll11111_opy_(),
            **self.bstack1lllll1l1111_opy_(),
            **self.bstack1lllll1ll1ll_opy_(),
            **self.bstack1lllll1ll111_opy_()
        }
    def bstack1lllll11lll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭‷"): self.bstack1l111111111_opy_,
            bstack1111lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ‸"): self.duration,
            bstack1111lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ‹"): self.result.result
        }
        if data[bstack1111lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ›")] == bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ※"):
            data[bstack1111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ‼")] = self.result.bstack111111ll1l_opy_()
            data[bstack1111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ‽")] = [{bstack1111lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ‾"): self.result.bstack111lll11l11_opy_()}]
        return data
    def bstack1lllll1lll11_opy_(self):
        return {
            bstack1111lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ‿"): self.bstack111ll11111_opy_(),
            **self.bstack1lllll1l1111_opy_(),
            **self.bstack1lllll1ll1ll_opy_(),
            **self.bstack1lllll11lll1_opy_(),
            **self.bstack1lllll1ll111_opy_()
        }
    def bstack1111ll11ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1111lll_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫ⁀") in event:
            return self.bstack1lllll11ll1l_opy_()
        elif bstack1111lll_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⁁") in event:
            return self.bstack1lllll1lll11_opy_()
    def bstack111l1l1l1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111111111_opy_ = time if time else bstack11l11ll1l1_opy_()
        self.duration = duration if duration else bstack111llll1ll1_opy_(self.started_at, self.bstack1l111111111_opy_)
        if result:
            self.result = result
class bstack111ll1l1ll_opy_(bstack111l11l111_opy_):
    def __init__(self, hooks=[], bstack111ll11lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        super().__init__(*args, **kwargs, bstack1lllll111_opy_=bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࠪ⁂"))
    @classmethod
    def bstack1lllll11ll11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111lll_opy_ (u"࠭ࡩࡥࠩ⁃"): id(step),
                bstack1111lll_opy_ (u"ࠧࡵࡧࡻࡸࠬ⁄"): step.name,
                bstack1111lll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ⁅"): step.keyword,
            })
        return bstack111ll1l1ll_opy_(
            **kwargs,
            meta={
                bstack1111lll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ⁆"): {
                    bstack1111lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⁇"): feature.name,
                    bstack1111lll_opy_ (u"ࠫࡵࡧࡴࡩࠩ⁈"): feature.filename,
                    bstack1111lll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ⁉"): feature.description
                },
                bstack1111lll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ⁊"): {
                    bstack1111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⁋"): scenario.name
                },
                bstack1111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⁌"): steps,
                bstack1111lll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ⁍"): bstack1llllllll11l_opy_(test)
            }
        )
    def bstack1lllll1l1l11_opy_(self):
        return {
            bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⁎"): self.hooks
        }
    def bstack1lllll1ll11l_opy_(self):
        if self.bstack111ll11lll_opy_:
            return {
                bstack1111lll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⁏"): self.bstack111ll11lll_opy_
            }
        return {}
    def bstack1lllll1lll11_opy_(self):
        return {
            **super().bstack1lllll1lll11_opy_(),
            **self.bstack1lllll1l1l11_opy_()
        }
    def bstack1lllll11ll1l_opy_(self):
        return {
            **super().bstack1lllll11ll1l_opy_(),
            **self.bstack1lllll1ll11l_opy_()
        }
    def bstack111l1l1l1l_opy_(self):
        return bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⁐")
class bstack111ll1ll11_opy_(bstack111l11l111_opy_):
    def __init__(self, hook_type, *args,bstack111ll11lll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1111lll1_opy_ = None
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        super().__init__(*args, **kwargs, bstack1lllll111_opy_=bstack1111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⁑"))
    def bstack1111llll1l_opy_(self):
        return self.hook_type
    def bstack1lllll1l111l_opy_(self):
        return {
            bstack1111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⁒"): self.hook_type
        }
    def bstack1lllll1lll11_opy_(self):
        return {
            **super().bstack1lllll1lll11_opy_(),
            **self.bstack1lllll1l111l_opy_()
        }
    def bstack1lllll11ll1l_opy_(self):
        return {
            **super().bstack1lllll11ll1l_opy_(),
            bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭⁓"): self.bstack1ll1111lll1_opy_,
            **self.bstack1lllll1l111l_opy_()
        }
    def bstack111l1l1l1l_opy_(self):
        return bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ⁔")
    def bstack111lll1l1l_opy_(self, bstack1ll1111lll1_opy_):
        self.bstack1ll1111lll1_opy_ = bstack1ll1111lll1_opy_