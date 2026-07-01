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
conf = {
    bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ₧"): False,
    bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ₨"): True,
    bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ₩"): False,
    bstack1l1llll_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨ₪"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111111l1l11_opy_ = conf
    @classmethod
    def bstack1lll1l11_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111111l11l1_opy_=None):
        return self._111111l1l11_opy_.get(property_name, bstack111111l11l1_opy_)
    def bstack1ll11l111l_opy_(self, property_name, bstack111111l11ll_opy_):
        self._111111l1l11_opy_[property_name] = bstack111111l11ll_opy_
    def bstack1ll111l1l1l_opy_(self, val):
        self._111111l1l11_opy_[bstack1l1llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩ₫")] = str(val).lower() == bstack1l1llll_opy_ (u"࠭ࡴࡳࡷࡨࠫ€")
    def bstack11lll1l1_opy_(self):
        return self._111111l1l11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫ₭"), False)
    def bstack1ll111llll1_opy_(self, val):
        self._111111l1l11_opy_[bstack1l1llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ₮")] = str(val).lower() == bstack1l1llll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ₯")
    def bstack11l11l1l_opy_(self):
        return self._111111l1l11_opy_.get(bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ₰"), False)