# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack11lllll1_opy_, bstack11l11llll1l_opy_
from bstack_utils.bstack11ll1l1lll_opy_ import bstack1111111l11l_opy_
class bstack111l1111ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lllll1l1lll_opy_=None, bstack1lllll1l1ll1_opy_=True, bstack1l111ll11ll_opy_=None, bstack1l1l1ll1_opy_=None, result=None, duration=None, bstack1111ll1l1l_opy_=None, meta={}):
        self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lllll1l1ll1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lllll1l1lll_opy_ = bstack1lllll1l1lll_opy_
        self.bstack1l111ll11ll_opy_ = bstack1l111ll11ll_opy_
        self.bstack1l1l1ll1_opy_ = bstack1l1l1ll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1lllll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lll11l1_opy_(self, meta):
        self.meta = meta
    def bstack111ll111l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1llllll111ll_opy_(self):
        bstack1llllll11l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ "): bstack1llllll11l11_opy_,
            bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ‪"): bstack1llllll11l11_opy_,
            bstack1l1l1ll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ‫"): bstack1llllll11l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l1ll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ‬") + key)
            setattr(self, key, val)
    def bstack1lllll1lllll_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ‭"): self.name,
            bstack1l1l1ll_opy_ (u"࠭ࡢࡰࡦࡼࠫ‮"): {
                bstack1l1l1ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ "): bstack1l1l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ‰"),
                bstack1l1l1ll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ‱"): self.code
            },
            bstack1l1l1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ′"): self.scope,
            bstack1l1l1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩ″"): self.tags,
            bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ‴"): self.framework,
            bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ‵"): self.started_at
        }
    def bstack1lllll1ll1l1_opy_(self):
        return {
         bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ‶"): self.meta
        }
    def bstack1llllll111l1_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ‷"): {
                bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭‸"): self.bstack1lllll1l1lll_opy_
            }
        }
    def bstack1lllll1lll11_opy_(self, bstack1llllll11l1l_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩ࠭‹")] == bstack1llllll11l1l_opy_, self.meta[bstack1l1l1ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ›")]), None)
        step.update(details)
    def bstack11111ll1_opy_(self, bstack1llllll11l1l_opy_):
        step = next(filter(lambda st: st[bstack1l1l1ll_opy_ (u"ࠬ࡯ࡤࠨ※")] == bstack1llllll11l1l_opy_, self.meta[bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ‼")]), None)
        step.update({
            bstack1l1l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ‽"): bstack11lllll1_opy_()
        })
    def bstack111ll1111l_opy_(self, bstack1llllll11l1l_opy_, result, duration=None):
        bstack1l111ll11ll_opy_ = bstack11lllll1_opy_()
        if bstack1llllll11l1l_opy_ is not None and self.meta.get(bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ‾")):
            step = next(filter(lambda st: st[bstack1l1l1ll_opy_ (u"ࠩ࡬ࡨࠬ‿")] == bstack1llllll11l1l_opy_, self.meta[bstack1l1l1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⁀")]), None)
            step.update({
                bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁁"): bstack1l111ll11ll_opy_,
                bstack1l1l1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⁂"): duration if duration else bstack11l11llll1l_opy_(step[bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⁃")], bstack1l111ll11ll_opy_),
                bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁄"): result.result,
                bstack1l1l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⁅"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llllll1111l_opy_):
        if self.meta.get(bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⁆")):
            self.meta[bstack1l1l1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⁇")].append(bstack1llllll1111l_opy_)
        else:
            self.meta[bstack1l1l1ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⁈")] = [ bstack1llllll1111l_opy_ ]
    def bstack1llllll11111_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁉"): self.bstack111l1lllll_opy_(),
            **self.bstack1lllll1lllll_opy_(),
            **self.bstack1llllll111ll_opy_(),
            **self.bstack1lllll1ll1l1_opy_()
        }
    def bstack1lllll1ll111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⁊"): self.bstack1l111ll11ll_opy_,
            bstack1l1l1ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⁋"): self.duration,
            bstack1l1l1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⁌"): self.result.result
        }
        if data[bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⁍")] == bstack1l1l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⁎"):
            data[bstack1l1l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⁏")] = self.result.bstack111111ll1l_opy_()
            data[bstack1l1l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⁐")] = [{bstack1l1l1ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⁑"): self.result.bstack11l1l111ll1_opy_()}]
        return data
    def bstack1lllll1llll1_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁒"): self.bstack111l1lllll_opy_(),
            **self.bstack1lllll1lllll_opy_(),
            **self.bstack1llllll111ll_opy_(),
            **self.bstack1lllll1ll111_opy_(),
            **self.bstack1lllll1ll1l1_opy_()
        }
    def bstack1111lllll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l1ll_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ⁓") in event:
            return self.bstack1llllll11111_opy_()
        elif bstack1l1l1ll_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁔") in event:
            return self.bstack1lllll1llll1_opy_()
    def bstack1111llllll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111ll11ll_opy_ = time if time else bstack11lllll1_opy_()
        self.duration = duration if duration else bstack11l11llll1l_opy_(self.started_at, self.bstack1l111ll11ll_opy_)
        if result:
            self.result = result
class bstack111lll111l_opy_(bstack111l1111ll_opy_):
    def __init__(self, hooks=[], bstack111ll1ll1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111ll1ll1l_opy_ = bstack111ll1ll1l_opy_
        super().__init__(*args, **kwargs, bstack1l1l1ll1_opy_=bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࠨ⁕"))
    @classmethod
    def bstack1lllll1ll1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1ll_opy_ (u"ࠫ࡮ࡪࠧ⁖"): id(step),
                bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡹࡶࠪ⁗"): step.name,
                bstack1l1l1ll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ⁘"): step.keyword,
            })
        return bstack111lll111l_opy_(
            **kwargs,
            meta={
                bstack1l1l1ll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ⁙"): {
                    bstack1l1l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⁚"): feature.name,
                    bstack1l1l1ll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ⁛"): feature.filename,
                    bstack1l1l1ll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⁜"): feature.description
                },
                bstack1l1l1ll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭⁝"): {
                    bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁞"): scenario.name
                },
                bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ "): steps,
                bstack1l1l1ll_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ⁠"): bstack1111111l11l_opy_(test)
            }
        )
    def bstack1lllll1ll11l_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⁡"): self.hooks
        }
    def bstack1lllll1lll1l_opy_(self):
        if self.bstack111ll1ll1l_opy_:
            return {
                bstack1l1l1ll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⁢"): self.bstack111ll1ll1l_opy_
            }
        return {}
    def bstack1lllll1llll1_opy_(self):
        return {
            **super().bstack1lllll1llll1_opy_(),
            **self.bstack1lllll1ll11l_opy_()
        }
    def bstack1llllll11111_opy_(self):
        return {
            **super().bstack1llllll11111_opy_(),
            **self.bstack1lllll1lll1l_opy_()
        }
    def bstack1111llllll_opy_(self):
        return bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⁣")
class bstack111ll1l1l1_opy_(bstack111l1111ll_opy_):
    def __init__(self, hook_type, *args,bstack111ll1ll1l_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11ll1l11_opy_ = None
        self.bstack111ll1ll1l_opy_ = bstack111ll1ll1l_opy_
        super().__init__(*args, **kwargs, bstack1l1l1ll1_opy_=bstack1l1l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⁤"))
    def bstack111l1ll1l1_opy_(self):
        return self.hook_type
    def bstack1lllll1l1l1l_opy_(self):
        return {
            bstack1l1l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⁥"): self.hook_type
        }
    def bstack1lllll1llll1_opy_(self):
        return {
            **super().bstack1lllll1llll1_opy_(),
            **self.bstack1lllll1l1l1l_opy_()
        }
    def bstack1llllll11111_opy_(self):
        return {
            **super().bstack1llllll11111_opy_(),
            bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⁦"): self.bstack1ll11ll1l11_opy_,
            **self.bstack1lllll1l1l1l_opy_()
        }
    def bstack1111llllll_opy_(self):
        return bstack1l1l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ⁧")
    def bstack111llll111_opy_(self, bstack1ll11ll1l11_opy_):
        self.bstack1ll11ll1l11_opy_ = bstack1ll11ll1l11_opy_