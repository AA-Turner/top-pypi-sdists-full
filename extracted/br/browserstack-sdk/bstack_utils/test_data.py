# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack11ll1l11ll_opy_ import bstack1lll1l1111l1_opy_
class bstack11111llll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll111ll111_opy_=None, bstack1lll111ll1ll_opy_=True, finished_at=None, bstack11l111l11_opy_=None, result=None, duration=None, bstack11111ll11l_opy_=None, meta={}):
        self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll111ll1ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll111ll111_opy_ = bstack1lll111ll111_opy_
        self.finished_at = finished_at
        self.bstack11l111l11_opy_ = bstack11l111l11_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111111lll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111ll111l_opy_(self, meta):
        self.meta = meta
    def bstack1111l111l1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll111l1lll_opy_(self):
        bstack1lll111l1111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⏐"): bstack1lll111l1111_opy_,
            bstack1lll1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⏑"): bstack1lll111l1111_opy_,
            bstack1lll1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⏒"): bstack1lll111l1111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1lll1l_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤ⏓") + key)
            setattr(self, key, val)
    def bstack1lll111lll1l_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⏔"): self.name,
            bstack1lll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨ⏕"): {
                bstack1lll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⏖"): bstack1lll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⏗"),
                bstack1lll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫ⏘"): self.code
            },
            bstack1lll1l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⏙"): self.scope,
            bstack1lll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⏚"): self.tags,
            bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⏛"): self.framework,
            bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⏜"): self.started_at
        }
    def bstack1lll1111lll1_opy_(self):
        return {
         bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ⏝"): self.meta
        }
    def bstack1lll111l111l_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⏞"): {
                bstack1lll1l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ⏟"): self.bstack1lll111ll111_opy_
            }
        }
    def bstack1lll111ll11l_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"ࠧࡪࡦࠪ⏠")] == sid, self.meta[bstack1lll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⏡")]), None)
        step.update(details)
    def bstack111ll1llll_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬ⏢")] == sid, self.meta[bstack1lll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⏣")]), None)
        step.update({
            bstack1lll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⏤"): current_time()
        })
    def bstack1111ll1ll1_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1lll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⏥")):
            step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"࠭ࡩࡥࠩ⏦")] == sid, self.meta[bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⏧")]), None)
            step.update({
                bstack1lll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⏨"): finished_at,
                bstack1lll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⏩"): duration if duration else time_diff(step[bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⏪")], finished_at),
                bstack1lll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⏫"): result.result,
                bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⏬"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll111l11l1_opy_):
        if self.meta.get(bstack1lll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⏭")):
            self.meta[bstack1lll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⏮")].append(bstack1lll111l11l1_opy_)
        else:
            self.meta[bstack1lll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⏯")] = [ bstack1lll111l11l1_opy_ ]
    def bstack1lll1111llll_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⏰"): self.bstack111111lll1_opy_(),
            bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⏱"): bstack1lll1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⏲"),
            **self.bstack1lll111lll1l_opy_(),
            **self.bstack1lll111l1lll_opy_(),
            **self.bstack1lll1111lll1_opy_()
        }
    def bstack1lll111l1l11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1lll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⏳"): self.finished_at,
            bstack1lll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⏴"): self.duration,
            bstack1lll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⏵"): self.result.result
        }
        if data[bstack1lll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⏶")] == bstack1lll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⏷"):
            data[bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⏸")] = self.result.bstack1lll1ll111l_opy_()
            data[bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⏹")] = [{bstack1lll1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⏺"): self.result.bstack111l11l1l11_opy_()}]
        return data
    def bstack1lll111lll11_opy_(self):
        return {
            bstack1lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⏻"): self.bstack111111lll1_opy_(),
            **self.bstack1lll111lll1l_opy_(),
            **self.bstack1lll111l1lll_opy_(),
            **self.bstack1lll111l1l11_opy_(),
            **self.bstack1lll1111lll1_opy_()
        }
    def bstack1lllllll1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1lll1l_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ⏼") in event:
            return self.bstack1lll1111llll_opy_()
        elif bstack1lll1l_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⏽") in event:
            return self.bstack1lll111lll11_opy_()
    def bstack11111ll111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack11111llll1_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l111l11_opy_=bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺࠧ⏾"))
    @classmethod
    def bstack1lll111l1l1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭⏿"): id(step),
                bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ␀"): step.name,
                bstack1lll1l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭␁"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1lll1l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ␂"): {
                    bstack1lll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ␃"): feature.name,
                    bstack1lll1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭␄"): feature.filename,
                    bstack1lll1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ␅"): feature.description
                },
                bstack1lll1l_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ␆"): {
                    bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ␇"): scenario.name
                },
                bstack1lll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ␈"): steps,
                bstack1lll1l_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ␉"): bstack1lll1l1111l1_opy_(test)
            }
        )
    def bstack1lll111l11ll_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭␊"): self.hooks
        }
    def bstack1lll111ll1l1_opy_(self):
        if self.integrations:
            return {
                bstack1lll1l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ␋"): self.integrations
            }
        return {}
    def bstack1lll111lll11_opy_(self):
        return {
            **super().bstack1lll111lll11_opy_(),
            **self.bstack1lll111l11ll_opy_()
        }
    def bstack1lll1111llll_opy_(self):
        return {
            **super().bstack1lll1111llll_opy_(),
            **self.bstack1lll111ll1l1_opy_()
        }
    def bstack11111ll111_opy_(self):
        return bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ␌")
class bstack1111ll1l11_opy_(bstack11111llll1_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l1l1llll_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack11l111l11_opy_=bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ␍"))
    def bstack1111111ll1_opy_(self):
        return self.hook_type
    def bstack1lll111l1ll1_opy_(self):
        return {
            bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ␎"): self.hook_type
        }
    def bstack1lll111lll11_opy_(self):
        return {
            **super().bstack1lll111lll11_opy_(),
            **self.bstack1lll111l1ll1_opy_()
        }
    def bstack1lll1111llll_opy_(self):
        return {
            **super().bstack1lll1111llll_opy_(),
            bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ␏"): self.bstack1l1l1l1llll_opy_,
            **self.bstack1lll111l1ll1_opy_()
        }
    def bstack11111ll111_opy_(self):
        return bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ␐")
    def bstack1111ll11ll_opy_(self, bstack1l1l1l1llll_opy_):
        self.bstack1l1l1l1llll_opy_ = bstack1l1l1l1llll_opy_