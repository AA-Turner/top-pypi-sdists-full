# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
conf = {
    bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᷠ"): False,
    bstack1l1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ᷡ"): True,
    bstack1l1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬᷢ"): False,
    bstack1l1111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫᷣ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111ll11l1_opy_ = conf
    @classmethod
    def bstack111111l1ll_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111ll111l_opy_=None):
        return self._11111ll11l1_opy_.get(property_name, bstack11111ll111l_opy_)
    def bstack11l11lll1l_opy_(self, property_name, bstack11111ll11ll_opy_):
        self._11111ll11l1_opy_[property_name] = bstack11111ll11ll_opy_
    def bstack1ll1111l11_opy_(self, val):
        self._11111ll11l1_opy_[bstack1l1111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬᷤ")] = str(val).lower() == bstack1l1111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᷥ")
    def bstack1ll1l1llll1_opy_(self):
        return self._11111ll11l1_opy_.get(bstack1l1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠧᷦ"), False)
    def bstack11l1l1111l_opy_(self, val):
        self._11111ll11l1_opy_[bstack1l1111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᷧ")] = str(val).lower() == bstack1l1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪᷨ")
    def bstack1ll1l1l11l1_opy_(self):
        return self._11111ll11l1_opy_.get(bstack1l1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬᷩ"), False)