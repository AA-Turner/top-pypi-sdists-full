# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
conf = {
    bstack1l111l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᷞ"): False,
    bstack1l111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᷟ"): True,
    bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᷠ"): False,
    bstack1l111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩᷡ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111ll11ll_opy_ = conf
    @classmethod
    def bstack1ll11ll111_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111ll1l11_opy_=None):
        return self._11111ll11ll_opy_.get(property_name, bstack11111ll1l11_opy_)
    def bstack1llllll11ll_opy_(self, property_name, bstack11111ll1l1l_opy_):
        self._11111ll11ll_opy_[property_name] = bstack11111ll1l1l_opy_
    def bstack11l1111111_opy_(self, val):
        self._11111ll11ll_opy_[bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪᷢ")] = str(val).lower() == bstack1l111l_opy_ (u"ࠧࡵࡴࡸࡩࠬᷣ")
    def bstack1ll1l1l111l_opy_(self):
        return self._11111ll11ll_opy_.get(bstack1l111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬᷤ"), False)
    def bstack1l1l111ll1_opy_(self, val):
        self._11111ll11ll_opy_[bstack1l111l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᷥ")] = str(val).lower() == bstack1l111l_opy_ (u"ࠪࡸࡷࡻࡥࠨᷦ")
    def bstack1lll111ll11_opy_(self):
        return self._11111ll11ll_opy_.get(bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᷧ"), False)