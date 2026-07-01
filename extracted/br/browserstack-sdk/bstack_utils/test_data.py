# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
from uuid import uuid4
from bstack_utils.helper import bstack1l1111ll_opy_, bstack1ll1l11ll_opy_
from bstack_utils.bstack111111l11l_opy_ import bstack1ll111lll11l_opy_
class bstack1lll1l1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111llll11l_opy_=None, bstack1l1lllllllll_opy_=True, bstack1ll1ll1ll_opy_=None, bstack1l1lll111_opy_=None, result=None, duration=None, bstack1111l111_opy_=None, meta={}):
        self.bstack1111l111_opy_ = bstack1111l111_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1l1lllllllll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111llll11l_opy_ = bstack1111llll11l_opy_
        self.bstack1ll1ll1ll_opy_ = bstack1ll1ll1ll_opy_
        self.bstack1l1lll111_opy_ = bstack1l1lll111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack1lllll111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1l1ll1ll_opy_(self, meta):
        self.meta = meta
    def bstack11l1l1ll_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll11111111l_opy_(self):
        bstack1l1lllll1l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⫣"): bstack1l1lllll1l1l_opy_,
            bstack1l1llll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⫤"): bstack1l1lllll1l1l_opy_,
            bstack1l1llll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⫥"): bstack1l1lllll1l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1llll_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢ⫦") + key)
            setattr(self, key, val)
    def bstack1l1llllll111_opy_(self):
        return {
            bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⫧"): self.name,
            bstack1l1llll_opy_ (u"ࠨࡤࡲࡨࡾ࠭⫨"): {
                bstack1l1llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⫩"): bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⫪"),
                bstack1l1llll_opy_ (u"ࠫࡨࡵࡤࡦࠩ⫫"): self.code
            },
            bstack1l1llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⫬"): self.scope,
            bstack1l1llll_opy_ (u"࠭ࡴࡢࡩࡶࠫ⫭"): self.tags,
            bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⫮"): self.framework,
            bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⫯"): self.started_at
        }
    def bstack1l1lllllll1l_opy_(self):
        return {
         bstack1l1llll_opy_ (u"ࠩࡰࡩࡹࡧࠧ⫰"): self.meta
        }
    def bstack1l1lllll11ll_opy_(self):
        return {
            bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭⫱"): {
                bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ⫲"): self.bstack1111llll11l_opy_
            }
        }
    def bstack1l1llllll1ll_opy_(self, sid, details):
        step = next(filter(lambda st: st[bstack1l1llll_opy_ (u"ࠬ࡯ࡤࠨ⫳")] == sid, self.meta[bstack1l1llll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⫴")]), None)
        step.update(details)
    def start_step(self, sid):
        step = next(filter(lambda st: st[bstack1l1llll_opy_ (u"ࠧࡪࡦࠪ⫵")] == sid, self.meta[bstack1l1llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ⫶")]), None)
        step.update({
            bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⫷"): bstack1l1111ll_opy_()
        })
    def bstack1l111111_opy_(self, sid, result, duration=None):
        bstack1ll1ll1ll_opy_ = bstack1l1111ll_opy_()
        if sid is not None and self.meta.get(bstack1l1llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ⫸")):
            step = next(filter(lambda st: st[bstack1l1llll_opy_ (u"ࠫ࡮ࡪࠧ⫹")] == sid, self.meta[bstack1l1llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⫺")]), None)
            step.update({
                bstack1l1llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⫻"): bstack1ll1ll1ll_opy_,
                bstack1l1llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⫼"): duration if duration else bstack1ll1l11ll_opy_(step[bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⫽")], bstack1ll1ll1ll_opy_),
                bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⫾"): result.result,
                bstack1l1llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⫿"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1l1lllll1lll_opy_):
        if self.meta.get(bstack1l1llll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ⬀")):
            self.meta[bstack1l1llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ⬁")].append(bstack1l1lllll1lll_opy_)
        else:
            self.meta[bstack1l1llll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ⬂")] = [ bstack1l1lllll1lll_opy_ ]
    def bstack1l1llllll1l1_opy_(self):
        return {
            bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⬃"): self.bstack1lllll111_opy_(),
            bstack1l1llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⬄"): bstack1l1llll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⬅"),
            **self.bstack1l1llllll111_opy_(),
            **self.bstack1ll11111111l_opy_(),
            **self.bstack1l1lllllll1l_opy_()
        }
    def bstack1l1lllll1ll1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⬆"): self.bstack1ll1ll1ll_opy_,
            bstack1l1llll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⬇"): self.duration,
            bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⬈"): self.result.result
        }
        if data[bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⬉")] == bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⬊"):
            data[bstack1l1llll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⬋")] = self.result.failure_type()
            data[bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⬌")] = [{bstack1l1llll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⬍"): self.result.bstack1lll11l11l1l_opy_()}]
            if self.result.exception is not None:
                try:
                    data[bstack1l1llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⬎")] = bstack1l1llll_opy_ (u"ࠧࢁࡽࠣ⬏").format(self.result.exception)
                except Exception:
                    data[bstack1l1llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⬐")] = bstack1l1llll_opy_ (u"ࠧࠨ⬑")
        return data
    def bstack1l1lllllll11_opy_(self):
        return {
            bstack1l1llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⬒"): self.bstack1lllll111_opy_(),
            **self.bstack1l1llllll111_opy_(),
            **self.bstack1ll11111111l_opy_(),
            **self.bstack1l1lllll1ll1_opy_(),
            **self.bstack1l1lllllll1l_opy_()
        }
    def bstack1111l1ll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1llll_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦࠪ⬓") in event:
            return self.bstack1l1llllll1l1_opy_()
        elif bstack1l1llll_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⬔") in event:
            return self.bstack1l1lllllll11_opy_()
    def bstack1lll1l11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1ll1ll_opy_ = time if time else bstack1l1111ll_opy_()
        self.duration = duration if duration else bstack1ll1l11ll_opy_(self.started_at, self.bstack1ll1ll1ll_opy_)
        if result:
            self.result = result
class bstack1l1l1111_opy_(bstack1lll1l1ll_opy_):
    def __init__(self, hooks=[], integrations={}, *args, **kwargs):
        self.hooks = hooks
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1lll111_opy_=bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⬕"))
    @classmethod
    def bstack1l1llllll11l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1llll_opy_ (u"ࠬ࡯ࡤࠨ⬖"): id(step),
                bstack1l1llll_opy_ (u"࠭ࡴࡦࡺࡷࠫ⬗"): step.name,
                bstack1l1llll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ⬘"): step.keyword,
            })
        return bstack1l1l1111_opy_(
            **kwargs,
            meta={
                bstack1l1llll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ⬙"): {
                    bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⬚"): feature.name,
                    bstack1l1llll_opy_ (u"ࠪࡴࡦࡺࡨࠨ⬛"): feature.filename,
                    bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ⬜"): feature.description
                },
                bstack1l1llll_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ⬝"): {
                    bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⬞"): scenario.name
                },
                bstack1l1llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭⬟"): steps,
                bstack1l1llll_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪ⬠"): bstack1ll111lll11l_opy_(test)
            }
        )
    def bstack1ll111111111_opy_(self):
        return {
            bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⬡"): self.hooks
        }
    def bstack1l1llllllll1_opy_(self):
        if self.integrations:
            return {
                bstack1l1llll_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ⬢"): self.integrations
            }
        return {}
    def bstack1l1lllllll11_opy_(self):
        return {
            **super().bstack1l1lllllll11_opy_(),
            **self.bstack1ll111111111_opy_(),
            **self.bstack1l1llllllll1_opy_()
        }
    def bstack1l1llllll1l1_opy_(self):
        return {
            **super().bstack1l1llllll1l1_opy_(),
            **self.bstack1l1llllllll1_opy_()
        }
    def bstack1lll1l11l_opy_(self):
        return bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⬣")
class bstack11ll1l1l_opy_(bstack1lll1l1ll_opy_):
    def __init__(self, hook_type, *args,integrations={}, **kwargs):
        self.hook_type = hook_type
        self.bstack11ll11ll1l1_opy_ = None
        self.integrations = integrations
        super().__init__(*args, **kwargs, bstack1l1lll111_opy_=bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⬤"))
    def bstack1llll1l1l_opy_(self):
        return self.hook_type
    def bstack1l1lllll1l11_opy_(self):
        return {
            bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⬥"): self.hook_type
        }
    def bstack1l1lllllll11_opy_(self):
        return {
            **super().bstack1l1lllllll11_opy_(),
            **self.bstack1l1lllll1l11_opy_()
        }
    def bstack1l1llllll1l1_opy_(self):
        return {
            **super().bstack1l1llllll1l1_opy_(),
            bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⬦"): self.bstack11ll11ll1l1_opy_,
            **self.bstack1l1lllll1l11_opy_()
        }
    def bstack1lll1l11l_opy_(self):
        return bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ⬧")
    def bstack111llll1_opy_(self, bstack11ll11ll1l1_opy_):
        self.bstack11ll11ll1l1_opy_ = bstack11ll11ll1l1_opy_