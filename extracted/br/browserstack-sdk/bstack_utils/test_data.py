# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1llll11l11l1_opy_
class bstack1lllll1ll11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll1l1lll1l_opy_=None, bstack1lll1ll1l11l_opy_=True, finished_at=None, bstack11l1l1l11l_opy_=None, result=None, duration=None, bstack1lllllll11l_opy_=None, meta={}):
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll1ll1l11l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll1l1lll1l_opy_ = bstack1lll1l1lll1l_opy_
        self.finished_at = finished_at
        self.bstack11l1l1l11l_opy_ = bstack11l1l1l11l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lllll1l1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111111lll1_opy_(self, meta):
        self.meta = meta
    def bstack11111lll11_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll1ll11ll1_opy_(self):
        bstack1lll1ll11l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨἀ"): bstack1lll1ll11l11_opy_,
            bstack1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨἁ"): bstack1lll1ll11l11_opy_,
            bstack1ll111_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬἂ"): bstack1lll1ll11l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll111_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤἃ") + key)
            setattr(self, key, val)
    def bstack1lll1ll11l1l_opy_(self):
        return {
            bstack1ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧἄ"): self.name,
            bstack1ll111_opy_ (u"ࠪࡦࡴࡪࡹࠨἅ"): {
                bstack1ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࠩἆ"): bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬἇ"),
                bstack1ll111_opy_ (u"࠭ࡣࡰࡦࡨࠫἈ"): self.code
            },
            bstack1ll111_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧἉ"): self.scope,
            bstack1ll111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ἂ"): self.tags,
            bstack1ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬἋ"): self.framework,
            bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἌ"): self.started_at
        }
    def bstack1lll1ll11lll_opy_(self):
        return {
         bstack1ll111_opy_ (u"ࠫࡲ࡫ࡴࡢࠩἍ"): self.meta
        }
    def bstack1lll1l1lllll_opy_(self):
        return {
            bstack1ll111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨἎ"): {
                bstack1ll111_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪἏ"): self.bstack1lll1l1lll1l_opy_
            }
        }
    def bstack1lll1ll1111l_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1ll111_opy_ (u"ࠧࡪࡦࠪἐ")] == sid, self.meta[bstack1ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧἑ")]), None)
        step.update(details)
    def bstack111lll1ll1_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1ll111_opy_ (u"ࠩ࡬ࡨࠬἒ")] == sid, self.meta[bstack1ll111_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩἓ")]), None)
        step.update({
            bstack1ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨἔ"): current_time()
        })
    def bstack11111lllll_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫἕ")):
            step = next(filter(lambda st: st[bstack1ll111_opy_ (u"࠭ࡩࡥࠩ἖")] == sid, self.meta[bstack1ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭἗")]), None)
            step.update({
                bstack1ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ἐ"): finished_at,
                bstack1ll111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫἙ"): duration if duration else time_diff(step[bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧἚ")], finished_at),
                bstack1ll111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫἛ"): result.result,
                bstack1ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭Ἔ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll1ll1l1l1_opy_):
        if self.meta.get(bstack1ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬἝ")):
            self.meta[bstack1ll111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭἞")].append(bstack1lll1ll1l1l1_opy_)
        else:
            self.meta[bstack1ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ἟")] = [ bstack1lll1ll1l1l1_opy_ ]
    def bstack1lll1l1lll11_opy_(self):
        return {
            bstack1ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧἠ"): self.bstack1lllll1l1l1_opy_(),
            bstack1ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪἡ"): bstack1ll111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬἢ"),
            **self.bstack1lll1ll11l1l_opy_(),
            **self.bstack1lll1ll11ll1_opy_(),
            **self.bstack1lll1ll11lll_opy_()
        }
    def bstack1lll1l1llll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪἣ"): self.finished_at,
            bstack1ll111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧἤ"): self.duration,
            bstack1ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧἥ"): self.result.result
        }
        if data[bstack1ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨἦ")] == bstack1ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩἧ"):
            data[bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩἨ")] = self.result.bstack1lll11ll1l1_opy_()
            data[bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬἩ")] = [{bstack1ll111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨἪ"): self.result.bstack11l111l1111_opy_()}]
        return data
    def bstack1lll1ll11111_opy_(self):
        return {
            bstack1ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫἫ"): self.bstack1lllll1l1l1_opy_(),
            **self.bstack1lll1ll11l1l_opy_(),
            **self.bstack1lll1ll11ll1_opy_(),
            **self.bstack1lll1l1llll1_opy_(),
            **self.bstack1lll1ll11lll_opy_()
        }
    def bstack111111l11l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll111_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨἬ") in event:
            return self.bstack1lll1l1lll11_opy_()
        elif bstack1ll111_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪἭ") in event:
            return self.bstack1lll1ll11111_opy_()
    def bstack1111111ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack1lllll1ll11_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l1l1l11l_opy_=bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺࠧἮ"))
    @classmethod
    def bstack1lll1ll111l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll111_opy_ (u"ࠪ࡭ࡩ࠭Ἧ"): id(step),
                bstack1ll111_opy_ (u"ࠫࡹ࡫ࡸࡵࠩἰ"): step.name,
                bstack1ll111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ἱ"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1ll111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧἲ"): {
                    bstack1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬἳ"): feature.name,
                    bstack1ll111_opy_ (u"ࠨࡲࡤࡸ࡭࠭ἴ"): feature.filename,
                    bstack1ll111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧἵ"): feature.description
                },
                bstack1ll111_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬἶ"): {
                    bstack1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩἷ"): scenario.name
                },
                bstack1ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫἸ"): steps,
                bstack1ll111_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨἹ"): bstack1llll11l11l1_opy_(test)
            }
        )
    def bstack1lll1ll1l111_opy_(self):
        return {
            bstack1ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Ἲ"): self.hooks
        }
    def bstack1lll1ll111ll_opy_(self):
        if self.integrations:
            return {
                bstack1ll111_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧἻ"): self.integrations
            }
        return {}
    def bstack1lll1ll11111_opy_(self):
        return {
            **super().bstack1lll1ll11111_opy_(),
            **self.bstack1lll1ll1l111_opy_()
        }
    def bstack1lll1l1lll11_opy_(self):
        return {
            **super().bstack1lll1l1lll11_opy_(),
            **self.bstack1lll1ll111ll_opy_()
        }
    def bstack1111111ll1_opy_(self):
        return bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫἼ")
class bstack11111l11ll_opy_(bstack1lllll1ll11_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l1111l11_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l1l1l11l_opy_=bstack1ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨἽ"))
    def bstack1lllll1l1ll_opy_(self):
        return self.hook_type
    def bstack1lll1l1ll1ll_opy_(self):
        return {
            bstack1ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧἾ"): self.hook_type
        }
    def bstack1lll1ll11111_opy_(self):
        return {
            **super().bstack1lll1ll11111_opy_(),
            **self.bstack1lll1l1ll1ll_opy_()
        }
    def bstack1lll1l1lll11_opy_(self):
        return {
            **super().bstack1lll1l1lll11_opy_(),
            bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪἿ"): self.bstack1l1l1111l11_opy_,
            **self.bstack1lll1l1ll1ll_opy_()
        }
    def bstack1111111ll1_opy_(self):
        return bstack1ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨὀ")
    def bstack11111llll1_opy_(self, bstack1l1l1111l11_opy_):
        self.bstack1l1l1111l11_opy_ = bstack1l1l1111l11_opy_