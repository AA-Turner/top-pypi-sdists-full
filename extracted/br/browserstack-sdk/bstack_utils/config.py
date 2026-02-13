# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
conf = {
    bstack11l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᦑ"): False,
    bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᦒ"): True,
    bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᦓ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111lll1llll_opy_ = conf
    @classmethod
    def bstack111l1lll_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111llll1111_opy_=None):
        return self._111lll1llll_opy_.get(property_name, bstack111llll1111_opy_)
    def bstack1ll111ll11_opy_(self, property_name, bstack111lll1lll1_opy_):
        self._111lll1llll_opy_[property_name] = bstack111lll1lll1_opy_
    def bstack11l111lll_opy_(self, val):
        self._111lll1llll_opy_[bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠧᦔ")] = bool(val)
    def bstack1lll11l1ll1_opy_(self):
        return self._111lll1llll_opy_.get(bstack11l11_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨᦕ"), False)
    def bstack1ll1l11ll1_opy_(self, val):
        self._111lll1llll_opy_[bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫᦖ")] = bool(val)
    def bstack1llll11l11l_opy_(self):
        return self._111lll1llll_opy_.get(bstack11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬᦗ"), False)