# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1llllllll1_opy_, bstack11l11l11lll_opy_
from bstack_utils.bstack1lll1l1111_opy_ import bstack1111l1lllll_opy_
class bstack111l1l1111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack11111l1llll_opy_=None, bstack11111lll111_opy_=True, bstack1l11l1ll1ll_opy_=None, bstack1ll1111l1l_opy_=None, result=None, duration=None, bstack111l11l111_opy_=None, meta={}):
        self.bstack111l11l111_opy_ = bstack111l11l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11111lll111_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11111l1llll_opy_ = bstack11111l1llll_opy_
        self.bstack1l11l1ll1ll_opy_ = bstack1l11l1ll1ll_opy_
        self.bstack1ll1111l1l_opy_ = bstack1ll1111l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1111ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111ll1ll11_opy_(self, meta):
        self.meta = meta
    def bstack111lll1ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack11111ll1ll1_opy_(self):
        bstack11111lll1l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨἀ"): bstack11111lll1l1_opy_,
            bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨἁ"): bstack11111lll1l1_opy_,
            bstack111lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬἂ"): bstack11111lll1l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111lll_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤἃ") + key)
            setattr(self, key, val)
    def bstack11111ll1l1l_opy_(self):
        return {
            bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧἄ"): self.name,
            bstack111lll_opy_ (u"ࠪࡦࡴࡪࡹࠨἅ"): {
                bstack111lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩἆ"): bstack111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬἇ"),
                bstack111lll_opy_ (u"࠭ࡣࡰࡦࡨࠫἈ"): self.code
            },
            bstack111lll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧἉ"): self.scope,
            bstack111lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ἂ"): self.tags,
            bstack111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬἋ"): self.framework,
            bstack111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἌ"): self.started_at
        }
    def bstack11111lllll1_opy_(self):
        return {
         bstack111lll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩἍ"): self.meta
        }
    def bstack11111llll11_opy_(self):
        return {
            bstack111lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨἎ"): {
                bstack111lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪἏ"): self.bstack11111l1llll_opy_
            }
        }
    def bstack11111llll1l_opy_(self, bstack11111l1ll1l_opy_, details):
        step = next(filter(lambda st: st[bstack111lll_opy_ (u"ࠧࡪࡦࠪἐ")] == bstack11111l1ll1l_opy_, self.meta[bstack111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧἑ")]), None)
        step.update(details)
    def bstack11l11l1l1l_opy_(self, bstack11111l1ll1l_opy_):
        step = next(filter(lambda st: st[bstack111lll_opy_ (u"ࠩ࡬ࡨࠬἒ")] == bstack11111l1ll1l_opy_, self.meta[bstack111lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩἓ")]), None)
        step.update({
            bstack111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨἔ"): bstack1llllllll1_opy_()
        })
    def bstack111ll1l1l1_opy_(self, bstack11111l1ll1l_opy_, result, duration=None):
        bstack1l11l1ll1ll_opy_ = bstack1llllllll1_opy_()
        if bstack11111l1ll1l_opy_ is not None and self.meta.get(bstack111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫἕ")):
            step = next(filter(lambda st: st[bstack111lll_opy_ (u"࠭ࡩࡥࠩ἖")] == bstack11111l1ll1l_opy_, self.meta[bstack111lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭἗")]), None)
            step.update({
                bstack111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ἐ"): bstack1l11l1ll1ll_opy_,
                bstack111lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫἙ"): duration if duration else bstack11l11l11lll_opy_(step[bstack111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἚ")], bstack1l11l1ll1ll_opy_),
                bstack111lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫἛ"): result.result,
                bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭Ἔ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack11111ll111l_opy_):
        if self.meta.get(bstack111lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬἝ")):
            self.meta[bstack111lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭἞")].append(bstack11111ll111l_opy_)
        else:
            self.meta[bstack111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ἟")] = [ bstack11111ll111l_opy_ ]
    def bstack11111ll1lll_opy_(self):
        return {
            bstack111lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧἠ"): self.bstack111l1111ll_opy_(),
            **self.bstack11111ll1l1l_opy_(),
            **self.bstack11111ll1ll1_opy_(),
            **self.bstack11111lllll1_opy_()
        }
    def bstack11111ll1l11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨἡ"): self.bstack1l11l1ll1ll_opy_,
            bstack111lll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬἢ"): self.duration,
            bstack111lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬἣ"): self.result.result
        }
        if data[bstack111lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ἤ")] == bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἥ"):
            data[bstack111lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧἦ")] = self.result.bstack11111lllll_opy_()
            data[bstack111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪἧ")] = [{bstack111lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭Ἠ"): self.result.bstack11l1l1l1111_opy_()}]
        return data
    def bstack11111l1lll1_opy_(self):
        return {
            bstack111lll_opy_ (u"ࠫࡺࡻࡩࡥࠩἩ"): self.bstack111l1111ll_opy_(),
            **self.bstack11111ll1l1l_opy_(),
            **self.bstack11111ll1ll1_opy_(),
            **self.bstack11111ll1l11_opy_(),
            **self.bstack11111lllll1_opy_()
        }
    def bstack111l111l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111lll_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭Ἢ") in event:
            return self.bstack11111ll1lll_opy_()
        elif bstack111lll_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨἫ") in event:
            return self.bstack11111l1lll1_opy_()
    def bstack1111llll11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11l1ll1ll_opy_ = time if time else bstack1llllllll1_opy_()
        self.duration = duration if duration else bstack11l11l11lll_opy_(self.started_at, self.bstack1l11l1ll1ll_opy_)
        if result:
            self.result = result
class bstack111llllll1_opy_(bstack111l1l1111_opy_):
    def __init__(self, hooks=[], bstack111lll1l11_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111lll1l11_opy_ = bstack111lll1l11_opy_
        super().__init__(*args, **kwargs, bstack1ll1111l1l_opy_=bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࠬἬ"))
    @classmethod
    def bstack11111ll11ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111lll_opy_ (u"ࠨ࡫ࡧࠫἭ"): id(step),
                bstack111lll_opy_ (u"ࠩࡷࡩࡽࡺࠧἮ"): step.name,
                bstack111lll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫἯ"): step.keyword,
            })
        return bstack111llllll1_opy_(
            **kwargs,
            meta={
                bstack111lll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬἰ"): {
                    bstack111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἱ"): feature.name,
                    bstack111lll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫἲ"): feature.filename,
                    bstack111lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬἳ"): feature.description
                },
                bstack111lll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪἴ"): {
                    bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧἵ"): scenario.name
                },
                bstack111lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩἶ"): steps,
                bstack111lll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ἷ"): bstack1111l1lllll_opy_(test)
            }
        )
    def bstack11111ll1111_opy_(self):
        return {
            bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫἸ"): self.hooks
        }
    def bstack11111lll11l_opy_(self):
        if self.bstack111lll1l11_opy_:
            return {
                bstack111lll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬἹ"): self.bstack111lll1l11_opy_
            }
        return {}
    def bstack11111l1lll1_opy_(self):
        return {
            **super().bstack11111l1lll1_opy_(),
            **self.bstack11111ll1111_opy_()
        }
    def bstack11111ll1lll_opy_(self):
        return {
            **super().bstack11111ll1lll_opy_(),
            **self.bstack11111lll11l_opy_()
        }
    def bstack1111llll11_opy_(self):
        return bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩἺ")
class bstack111ll1l1ll_opy_(bstack111l1l1111_opy_):
    def __init__(self, hook_type, *args,bstack111lll1l11_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack11111ll11l1_opy_ = None
        self.bstack111lll1l11_opy_ = bstack111lll1l11_opy_
        super().__init__(*args, **kwargs, bstack1ll1111l1l_opy_=bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭Ἳ"))
    def bstack1111llll1l_opy_(self):
        return self.hook_type
    def bstack11111lll1ll_opy_(self):
        return {
            bstack111lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬἼ"): self.hook_type
        }
    def bstack11111l1lll1_opy_(self):
        return {
            **super().bstack11111l1lll1_opy_(),
            **self.bstack11111lll1ll_opy_()
        }
    def bstack11111ll1lll_opy_(self):
        return {
            **super().bstack11111ll1lll_opy_(),
            bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨἽ"): self.bstack11111ll11l1_opy_,
            **self.bstack11111lll1ll_opy_()
        }
    def bstack1111llll11_opy_(self):
        return bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭Ἶ")
    def bstack111llll1l1_opy_(self, bstack11111ll11l1_opy_):
        self.bstack11111ll11l1_opy_ = bstack11111ll11l1_opy_