# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
conf = {
    bstack1111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᭹"): False,
    bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ᭺"): True,
    bstack1111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭᭻"): False,
    bstack1111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬ᭼"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111ll11l11l_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111ll11l1ll_opy_=None):
        return self._111ll11l11l_opy_.get(property_name, bstack111ll11l1ll_opy_)
    def bstack1ll1111l11_opy_(self, property_name, bstack111ll11l1l1_opy_):
        self._111ll11l11l_opy_[property_name] = bstack111ll11l1l1_opy_
    def bstack1111ll111l_opy_(self, val):
        self._111ll11l11l_opy_[bstack1111l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪ࠭᭽")] = str(val).lower() == bstack1111l_opy_ (u"ࠪࡸࡷࡻࡥࠨ᭾")
    def should_skip_session_name(self):
        return self._111ll11l11l_opy_.get(bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨ᭿"), False)
    def bstack111lllll11_opy_(self, val):
        self._111ll11l11l_opy_[bstack1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫᮀ")] = str(val).lower() == bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫᮁ")
    def should_skip_session_status(self):
        return self._111ll11l11l_opy_.get(bstack1111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭ᮂ"), False)