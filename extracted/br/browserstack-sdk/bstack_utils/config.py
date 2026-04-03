# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
conf = {
    bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᷁"): False,
    bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰ᷂ࠪ"): True,
    bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ᷃"): False,
    bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨ᷄"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111llll11_opy_ = conf
    @classmethod
    def bstack1lllllll1_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111llll1l_opy_=None):
        return self._11111llll11_opy_.get(property_name, bstack11111llll1l_opy_)
    def bstack1111ll1l11_opy_(self, property_name, bstack11111lll1ll_opy_):
        self._11111llll11_opy_[property_name] = bstack11111lll1ll_opy_
    def bstack1llllll1l1l_opy_(self, val):
        self._11111llll11_opy_[bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩ᷅")] = str(val).lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ᷆")
    def bstack1lll111ll11_opy_(self):
        return self._11111llll11_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫ᷇"), False)
    def bstack111l1ll111_opy_(self, val):
        self._11111llll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ᷈")] = str(val).lower() == bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᷉")
    def bstack1ll1lll1111_opy_(self):
        return self._11111llll11_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴ᷊ࠩ"), False)