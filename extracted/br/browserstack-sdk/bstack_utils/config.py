# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
conf = {
    bstack11ll11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ᷂"): False,
    bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ᷃"): True,
    bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪ᷄"): False,
    bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩ᷅"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111llll11_opy_ = conf
    @classmethod
    def bstack111llll11_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111lll1ll_opy_=None):
        return self._11111llll11_opy_.get(property_name, bstack11111lll1ll_opy_)
    def bstack1111lll11_opy_(self, property_name, bstack11111lll1l1_opy_):
        self._11111llll11_opy_[property_name] = bstack11111lll1l1_opy_
    def bstack11ll1ll11l_opy_(self, val):
        self._11111llll11_opy_[bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪ᷆")] = str(val).lower() == bstack11ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ᷇")
    def bstack1lll11l111l_opy_(self):
        return self._11111llll11_opy_.get(bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬ᷈"), False)
    def bstack1l1l1ll11l_opy_(self, val):
        self._11111llll11_opy_[bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨ᷉")] = str(val).lower() == bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ᷊")
    def bstack1ll1ll1111l_opy_(self):
        return self._11111llll11_opy_.get(bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪ᷋"), False)