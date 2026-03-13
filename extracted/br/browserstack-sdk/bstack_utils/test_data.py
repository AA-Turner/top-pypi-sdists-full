# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1lll1l11l1_opy_ import bstack1lll11l11lll_opy_
class bstack111111111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll111111l1_opy_=None, bstack1ll1lllll1l1_opy_=True, finished_at=None, bstack111lll11l_opy_=None, result=None, duration=None, bstack1lllll1ll11_opy_=None, meta={}):
        self.bstack1lllll1ll11_opy_ = bstack1lllll1ll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1lllll1l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll111111l1_opy_ = bstack1lll111111l1_opy_
        self.finished_at = finished_at
        self.bstack111lll11l_opy_ = bstack111lll11l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llll1lll11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11111l1l1l_opy_(self, meta):
        self.meta = meta
    def bstack111111ll11_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll111111ll_opy_(self):
        bstack1ll1lllll1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⒐"): bstack1ll1lllll1ll_opy_,
            bstack1111l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⒑"): bstack1ll1lllll1ll_opy_,
            bstack1111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⒒"): bstack1ll1lllll1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1111l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧ⒓") + key)
            setattr(self, key, val)
    def bstack1ll1llllll11_opy_(self):
        return {
            bstack1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⒔"): self.name,
            bstack1111l_opy_ (u"࠭ࡢࡰࡦࡼࠫ⒕"): {
                bstack1111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⒖"): bstack1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⒗"),
                bstack1111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⒘"): self.code
            },
            bstack1111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⒙"): self.scope,
            bstack1111l_opy_ (u"ࠫࡹࡧࡧࡴࠩ⒚"): self.tags,
            bstack1111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⒛"): self.framework,
            bstack1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⒜"): self.started_at
        }
    def bstack1ll1llll1lll_opy_(self):
        return {
         bstack1111l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ⒝"): self.meta
        }
    def bstack1ll1lllll11l_opy_(self):
        return {
            bstack1111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ⒞"): {
                bstack1111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭⒟"): self.bstack1lll111111l1_opy_
            }
        }
    def bstack1ll1llllllll_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭⒠")] == sid, self.meta[bstack1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⒡")]), None)
        step.update(details)
    def bstack1ll1l111l_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1111l_opy_ (u"ࠬ࡯ࡤࠨ⒢")] == sid, self.meta[bstack1111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⒣")]), None)
        step.update({
            bstack1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⒤"): current_time()
        })
    def bstack11111ll11l_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⒥")):
            step = next(filter(lambda st: st[bstack1111l_opy_ (u"ࠩ࡬ࡨࠬ⒦")] == sid, self.meta[bstack1111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⒧")]), None)
            step.update({
                bstack1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⒨"): finished_at,
                bstack1111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⒩"): duration if duration else time_diff(step[bstack1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⒪")], finished_at),
                bstack1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⒫"): result.result,
                bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⒬"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll11111111_opy_):
        if self.meta.get(bstack1111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⒭")):
            self.meta[bstack1111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⒮")].append(bstack1lll11111111_opy_)
        else:
            self.meta[bstack1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⒯")] = [ bstack1lll11111111_opy_ ]
    def bstack1ll1llllll1l_opy_(self):
        return {
            bstack1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⒰"): self.bstack1llll1lll11_opy_(),
            bstack1111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⒱"): bstack1111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⒲"),
            **self.bstack1ll1llllll11_opy_(),
            **self.bstack1lll111111ll_opy_(),
            **self.bstack1ll1llll1lll_opy_()
        }
    def bstack1ll1lllllll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⒳"): self.finished_at,
            bstack1111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⒴"): self.duration,
            bstack1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⒵"): self.result.result
        }
        if data[bstack1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫⒶ")] == bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬⒷ"):
            data[bstack1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬⒸ")] = self.result.bstack1lll11l1l1l_opy_()
            data[bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨⒹ")] = [{bstack1111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫⒺ"): self.result.bstack1111ll11ll1_opy_()}]
        return data
    def bstack1lll11111ll1_opy_(self):
        return {
            bstack1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧⒻ"): self.bstack1llll1lll11_opy_(),
            **self.bstack1ll1llllll11_opy_(),
            **self.bstack1lll111111ll_opy_(),
            **self.bstack1ll1lllllll1_opy_(),
            **self.bstack1ll1llll1lll_opy_()
        }
    def bstack11111111l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1111l_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫⒼ") in event:
            return self.bstack1ll1llllll1l_opy_()
        elif bstack1111l_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ⓗ") in event:
            return self.bstack1lll11111ll1_opy_()
    def bstack1lllllll1ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack111111111l_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111lll11l_opy_=bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࠪⒾ"))
    @classmethod
    def bstack1lll11111l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111l_opy_ (u"࠭ࡩࡥࠩⒿ"): id(step),
                bstack1111l_opy_ (u"ࠧࡵࡧࡻࡸࠬⓀ"): step.name,
                bstack1111l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩⓁ"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1111l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪⓂ"): {
                    bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨⓃ"): feature.name,
                    bstack1111l_opy_ (u"ࠫࡵࡧࡴࡩࠩⓄ"): feature.filename,
                    bstack1111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪⓅ"): feature.description
                },
                bstack1111l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨⓆ"): {
                    bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⓇ"): scenario.name
                },
                bstack1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧⓈ"): steps,
                bstack1111l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫⓉ"): bstack1lll11l11lll_opy_(test)
            }
        )
    def bstack1lll11111l11_opy_(self):
        return {
            bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩⓊ"): self.hooks
        }
    def bstack1lll1111111l_opy_(self):
        if self.integrations:
            return {
                bstack1111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪⓋ"): self.integrations
            }
        return {}
    def bstack1lll11111ll1_opy_(self):
        return {
            **super().bstack1lll11111ll1_opy_(),
            **self.bstack1lll11111l11_opy_()
        }
    def bstack1ll1llllll1l_opy_(self):
        return {
            **super().bstack1ll1llllll1l_opy_(),
            **self.bstack1lll1111111l_opy_()
        }
    def bstack1lllllll1ll_opy_(self):
        return bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧⓌ")
class bstack111111llll_opy_(bstack111111111l_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l11l1l1l_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111lll11l_opy_=bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫⓍ"))
    def bstack1llllll1111_opy_(self):
        return self.hook_type
    def bstack1ll1lllll111_opy_(self):
        return {
            bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪⓎ"): self.hook_type
        }
    def bstack1lll11111ll1_opy_(self):
        return {
            **super().bstack1lll11111ll1_opy_(),
            **self.bstack1ll1lllll111_opy_()
        }
    def bstack1ll1llllll1l_opy_(self):
        return {
            **super().bstack1ll1llllll1l_opy_(),
            bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭Ⓩ"): self.bstack1l1l11l1l1l_opy_,
            **self.bstack1ll1lllll111_opy_()
        }
    def bstack1lllllll1ll_opy_(self):
        return bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫⓐ")
    def bstack111111lll1_opy_(self, bstack1l1l11l1l1l_opy_):
        self.bstack1l1l11l1l1l_opy_ = bstack1l1l11l1l1l_opy_