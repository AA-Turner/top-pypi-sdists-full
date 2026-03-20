# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import current_time, time_diff
from bstack_utils.bstack1111l1lll_opy_ import bstack1lll111l11l1_opy_
class bstack1llll1l1l1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1ll1ll1lllll_opy_=None, bstack1ll1lll11l1l_opy_=True, finished_at=None, bstack111l11lll1_opy_=None, result=None, duration=None, bstack1lll1llll11_opy_=None, meta={}):
        self.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1lll11l1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1ll1lllll_opy_ = bstack1ll1ll1lllll_opy_
        self.finished_at = finished_at
        self.bstack111l11lll1_opy_ = bstack111l11lll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lllll1l111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1lllllll11l_opy_(self, meta):
        self.meta = meta
    def bstack1llllll1l1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1lll111ll_opy_(self):
        bstack1ll1lll1l1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩⓛ"): bstack1ll1lll1l1ll_opy_,
            bstack11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩⓜ"): bstack1ll1lll1l1ll_opy_,
            bstack11lll1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ⓝ"): bstack1ll1lll1l1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11lll1_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥⓞ") + key)
            setattr(self, key, val)
    def bstack1ll1ll1llll1_opy_(self):
        return {
            bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨⓟ"): self.name,
            bstack11lll1_opy_ (u"ࠫࡧࡵࡤࡺࠩⓠ"): {
                bstack11lll1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪⓡ"): bstack11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ⓢ"),
                bstack11lll1_opy_ (u"ࠧࡤࡱࡧࡩࠬⓣ"): self.code
            },
            bstack11lll1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨⓤ"): self.scope,
            bstack11lll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧⓥ"): self.tags,
            bstack11lll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ⓦ"): self.framework,
            bstack11lll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨⓧ"): self.started_at
        }
    def bstack1ll1lll111l1_opy_(self):
        return {
         bstack11lll1_opy_ (u"ࠬࡳࡥࡵࡣࠪⓨ"): self.meta
        }
    def bstack1ll1lll11lll_opy_(self):
        return {
            bstack11lll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩⓩ"): {
                bstack11lll1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ⓪"): self.bstack1ll1ll1lllll_opy_
            }
        }
    def bstack1ll1lll11l11_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack11lll1_opy_ (u"ࠨ࡫ࡧࠫ⓫")] == sid, self.meta[bstack11lll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⓬")]), None)
        step.update(details)
    def bstack1ll11ll111_opy_(self, sid):
        step = next(filter(lambda st: st[bstack11lll1_opy_ (u"ࠪ࡭ࡩ࠭⓭")] == sid, self.meta[bstack11lll1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⓮")]), None)
        step.update({
            bstack11lll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⓯"): current_time()
        })
    def bstack1llllll11l1_opy_(self, sid, result, duration=None):
        finished_at = current_time()
        if sid is not None and self.meta.get(bstack11lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⓰")):
            step = next(filter(lambda st: st[bstack11lll1_opy_ (u"ࠧࡪࡦࠪ⓱")] == sid, self.meta[bstack11lll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⓲")]), None)
            step.update({
                bstack11lll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⓳"): finished_at,
                bstack11lll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⓴"): duration if duration else time_diff(step[bstack11lll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⓵")], finished_at),
                bstack11lll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⓶"): result.result,
                bstack11lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⓷"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1lll1ll1l_opy_):
        if self.meta.get(bstack11lll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⓸")):
            self.meta[bstack11lll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⓹")].append(bstack1ll1lll1ll1l_opy_)
        else:
            self.meta[bstack11lll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ⓺")] = [ bstack1ll1lll1ll1l_opy_ ]
    def bstack1ll1lll11111_opy_(self):
        return {
            bstack11lll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⓻"): self.bstack1lllll1l111_opy_(),
            bstack11lll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⓼"): bstack11lll1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⓽"),
            **self.bstack1ll1ll1llll1_opy_(),
            **self.bstack1ll1lll111ll_opy_(),
            **self.bstack1ll1lll111l1_opy_()
        }
    def bstack1ll1lll1111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11lll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⓾"): self.finished_at,
            bstack11lll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⓿"): self.duration,
            bstack11lll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ─"): self.result.result
        }
        if data[bstack11lll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ━")] == bstack11lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ│"):
            data[bstack11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ┃")] = self.result.bstack1ll1lllll11_opy_()
            data[bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭┄")] = [{bstack11lll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ┅"): self.result.bstack11111ll1111_opy_()}]
        return data
    def bstack1ll1lll1l111_opy_(self):
        return {
            bstack11lll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┆"): self.bstack1lllll1l111_opy_(),
            **self.bstack1ll1ll1llll1_opy_(),
            **self.bstack1ll1lll111ll_opy_(),
            **self.bstack1ll1lll1111l_opy_(),
            **self.bstack1ll1lll111l1_opy_()
        }
    def bstack1llll11l1ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11lll1_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩ┇") in event:
            return self.bstack1ll1lll11111_opy_()
        elif bstack11lll1_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ┈") in event:
            return self.bstack1ll1lll1l111_opy_()
    def bstack1llll1l1ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.finished_at = time if time else current_time()
        self.duration = duration if duration else time_diff(self.started_at, self.finished_at)
        if result:
            self.result = result
class TestData(bstack1llll1l1l1l_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111l11lll1_opy_=bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࠨ┉"))
    @classmethod
    def bstack1ll1lll11ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lll1_opy_ (u"ࠫ࡮ࡪࠧ┊"): id(step),
                bstack11lll1_opy_ (u"ࠬࡺࡥࡹࡶࠪ┋"): step.name,
                bstack11lll1_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ┌"): step.keyword,
            })
        return TestData(
            **kwargs,
            meta={
                bstack11lll1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ┍"): {
                    bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭┎"): feature.name,
                    bstack11lll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ┏"): feature.filename,
                    bstack11lll1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ┐"): feature.description
                },
                bstack11lll1_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭┑"): {
                    bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ┒"): scenario.name
                },
                bstack11lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ┓"): steps,
                bstack11lll1_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ└"): bstack1lll111l11l1_opy_(test)
            }
        )
    def bstack1ll1lll1ll11_opy_(self):
        return {
            bstack11lll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ┕"): self.hooks
        }
    def bstack1ll1lll1l11l_opy_(self):
        if self.integrations:
            return {
                bstack11lll1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ┖"): self.integrations
            }
        return {}
    def bstack1ll1lll1l111_opy_(self):
        return {
            **super().bstack1ll1lll1l111_opy_(),
            **self.bstack1ll1lll1ll11_opy_()
        }
    def bstack1ll1lll11111_opy_(self):
        return {
            **super().bstack1ll1lll11111_opy_(),
            **self.bstack1ll1lll1l11l_opy_()
        }
    def bstack1llll1l1ll1_opy_(self):
        return bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ┗")
class bstack1llllll111l_opy_(bstack1llll1l1l1l_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1l1l11l111l_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack111l11lll1_opy_=bstack11lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ┘"))
    def bstack1llll1ll1l1_opy_(self):
        return self.hook_type
    def bstack1ll1lll1l1l1_opy_(self):
        return {
            bstack11lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ┙"): self.hook_type
        }
    def bstack1ll1lll1l111_opy_(self):
        return {
            **super().bstack1ll1lll1l111_opy_(),
            **self.bstack1ll1lll1l1l1_opy_()
        }
    def bstack1ll1lll11111_opy_(self):
        return {
            **super().bstack1ll1lll11111_opy_(),
            bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ┚"): self.bstack1l1l11l111l_opy_,
            **self.bstack1ll1lll1l1l1_opy_()
        }
    def bstack1llll1l1ll1_opy_(self):
        return bstack11lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ┛")
    def bstack1llllll1111_opy_(self, bstack1l1l11l111l_opy_):
        self.bstack1l1l11l111l_opy_ = bstack1l1l11l111l_opy_