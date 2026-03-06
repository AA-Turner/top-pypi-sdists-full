# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1lllllll11_opy_ import bstack1lll11llll11_opy_
class bstack111111l111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1lll111ll11l_opy_=None, bstack1lll111l11ll_opy_=True, finished_at=None, bstack111ll11ll_opy_=None, result=None, duration=None, bstack11111ll111_opy_=None, meta={}):
        self.bstack11111ll111_opy_ = bstack11111ll111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1lll111l11ll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1lll111ll11l_opy_ = bstack1lll111ll11l_opy_
        self.finished_at = finished_at
        self.bstack111ll11ll_opy_ = bstack111ll11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1llllll11ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111l1llll_opy_(self, meta):
        self.meta = meta
    def bstack1111l11ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1lll111l11l1_opy_(self):
        bstack1lll111ll1l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⏑"): bstack1lll111ll1l1_opy_,
            bstack1111_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⏒"): bstack1lll111ll1l1_opy_,
            bstack1111_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⏓"): bstack1lll111ll1l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1111_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥ⏔") + key)
            setattr(self, key, val)
    def bstack1lll111l1lll_opy_(self):
        return {
            bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ⏕"): self.name,
            bstack1111_opy_ (u"ࠫࡧࡵࡤࡺࠩ⏖"): {
                bstack1111_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⏗"): bstack1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⏘"),
                bstack1111_opy_ (u"ࠧࡤࡱࡧࡩࠬ⏙"): self.code
            },
            bstack1111_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⏚"): self.scope,
            bstack1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⏛"): self.tags,
            bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⏜"): self.framework,
            bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⏝"): self.started_at
        }
    def bstack1lll1111lll1_opy_(self):
        return {
         bstack1111_opy_ (u"ࠬࡳࡥࡵࡣࠪ⏞"): self.meta
        }
    def bstack1lll111l1l11_opy_(self):
        return {
            bstack1111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ⏟"): {
                bstack1111_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ⏠"): self.bstack1lll111ll11l_opy_
            }
        }
    def bstack1lll1111llll_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠨ࡫ࡧࠫ⏡")] == sid, self.meta[bstack1111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⏢")]), None)
        step.update(details)
    def bstack11ll1l1l11_opy_(self, sid):
        step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠪ࡭ࡩ࠭⏣")] == sid, self.meta[bstack1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⏤")]), None)
        step.update({
            bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⏥"): current_time()
        })
    def bstack1111l1l11l_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⏦")):
            step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠧࡪࡦࠪ⏧")] == sid, self.meta[bstack1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⏨")]), None)
            step.update({
                bstack1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⏩"): finished_at,
                bstack1111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⏪"): duration if duration else time_diff(step[bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⏫")], finished_at),
                bstack1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⏬"): result.result,
                bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⏭"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1lll111l111l_opy_):
        if self.meta.get(bstack1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⏮")):
            self.meta[bstack1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⏯")].append(bstack1lll111l111l_opy_)
        else:
            self.meta[bstack1111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⏰")] = [ bstack1lll111l111l_opy_ ]
    def bstack1lll111ll111_opy_(self):
        return {
            bstack1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⏱"): self.bstack1llllll11ll_opy_(),
            bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⏲"): bstack1111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⏳"),
            **self.bstack1lll111l1lll_opy_(),
            **self.bstack1lll111l11l1_opy_(),
            **self.bstack1lll1111lll1_opy_()
        }
    def bstack1lll111l1l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⏴"): self.finished_at,
            bstack1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⏵"): self.duration,
            bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⏶"): self.result.result
        }
        if data[bstack1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⏷")] == bstack1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⏸"):
            data[bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⏹")] = self.result.bstack1lll1ll1111_opy_()
            data[bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⏺")] = [{bstack1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⏻"): self.result.bstack1111l1ll1ll_opy_()}]
        return data
    def bstack1lll111ll1ll_opy_(self):
        return {
            bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⏼"): self.bstack1llllll11ll_opy_(),
            **self.bstack1lll111l1lll_opy_(),
            **self.bstack1lll111l11l1_opy_(),
            **self.bstack1lll111l1l1l_opy_(),
            **self.bstack1lll1111lll1_opy_()
        }
    def bstack1llllll1lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1111_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ⏽") in event:
            return self.bstack1lll111ll111_opy_()
        elif bstack1111_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⏾") in event:
            return self.bstack1lll111ll1ll_opy_()
    def bstack1111111111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack111111l111_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111ll11ll_opy_=bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨ⏿"))
    @classmethod
    def bstack1lll1111ll11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111_opy_ (u"ࠫ࡮ࡪࠧ␀"): id(step),
                bstack1111_opy_ (u"ࠬࡺࡥࡹࡶࠪ␁"): step.name,
                bstack1111_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ␂"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ␃"): {
                    bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭␄"): feature.name,
                    bstack1111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ␅"): feature.filename,
                    bstack1111_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ␆"): feature.description
                },
                bstack1111_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭␇"): {
                    bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ␈"): scenario.name
                },
                bstack1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ␉"): steps,
                bstack1111_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ␊"): bstack1lll11llll11_opy_(test)
            }
        )
    def bstack1lll111l1111_opy_(self):
        return {
            bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ␋"): self.hooks
        }
    def bstack1lll1111ll1l_opy_(self):
        if self.integrations:
            return {
                bstack1111_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ␌"): self.integrations
            }
        return {}
    def bstack1lll111ll1ll_opy_(self):
        return {
            **super().bstack1lll111ll1ll_opy_(),
            **self.bstack1lll111l1111_opy_()
        }
    def bstack1lll111ll111_opy_(self):
        return {
            **super().bstack1lll111ll111_opy_(),
            **self.bstack1lll1111ll1l_opy_()
        }
    def bstack1111111111_opy_(self):
        return bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ␍")
class bstack1111l1ll11_opy_(bstack111111l111_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l111l11l_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111ll11ll_opy_=bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ␎"))
    def bstack111111l11l_opy_(self):
        return self.hook_type
    def bstack1lll111l1ll1_opy_(self):
        return {
            bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ␏"): self.hook_type
        }
    def bstack1lll111ll1ll_opy_(self):
        return {
            **super().bstack1lll111ll1ll_opy_(),
            **self.bstack1lll111l1ll1_opy_()
        }
    def bstack1lll111ll111_opy_(self):
        return {
            **super().bstack1lll111ll111_opy_(),
            bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ␐"): self.bstack1l1l111l11l_opy_,
            **self.bstack1lll111l1ll1_opy_()
        }
    def bstack1111111111_opy_(self):
        return bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ␑")
    def bstack1111ll111l_opy_(self, bstack1l1l111l11l_opy_):
        self.bstack1l1l111l11l_opy_ = bstack1l1l111l11l_opy_