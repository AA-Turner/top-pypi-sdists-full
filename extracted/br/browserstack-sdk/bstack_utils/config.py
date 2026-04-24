# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
conf = {
    bstack111ll11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᷞ"): False,
    bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᷟ"): True,
    bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᷠ"): False,
    bstack111ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩᷡ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111ll11ll_opy_ = conf
    @classmethod
    def bstack1lllll1lll1_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111ll1l11_opy_=None):
        return self._11111ll11ll_opy_.get(property_name, bstack11111ll1l11_opy_)
    def bstack1l111l1ll1_opy_(self, property_name, bstack11111ll1l1l_opy_):
        self._11111ll11ll_opy_[property_name] = bstack11111ll1l1l_opy_
    def bstack111l11l1l1_opy_(self, val):
        self._11111ll11ll_opy_[bstack111ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪᷢ")] = str(val).lower() == bstack111ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬᷣ")
    def bstack1lll111llll_opy_(self):
        return self._11111ll11ll_opy_.get(bstack111ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬᷤ"), False)
    def bstack1l1lll11l1_opy_(self, val):
        self._11111ll11ll_opy_[bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᷥ")] = str(val).lower() == bstack111ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᷦ")
    def bstack1ll1l1ll1l1_opy_(self):
        return self._11111ll11ll_opy_.get(bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᷧ"), False)