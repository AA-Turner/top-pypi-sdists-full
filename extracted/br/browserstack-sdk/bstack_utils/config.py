# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
conf = {
    bstack111ll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᷻"): False,
    bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ᷼"): True,
    bstack111ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶ᷽ࠫ"): False,
    bstack111ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪ᷾"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111l1lll1_opy_ = conf
    @classmethod
    def bstack1l1l11ll1_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111l1llll_opy_=None):
        return self._11111l1lll1_opy_.get(property_name, bstack11111l1llll_opy_)
    def bstack1l1l1llll1_opy_(self, property_name, bstack11111l1ll1l_opy_):
        self._11111l1lll1_opy_[property_name] = bstack11111l1ll1l_opy_
    def bstack1l1lll1l1_opy_(self, val):
        self._11111l1lll1_opy_[bstack111ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨ᷿ࠫ")] = str(val).lower() == bstack111ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ḁ")
    def bstack1ll1lll11ll_opy_(self):
        return self._11111l1lll1_opy_.get(bstack111ll_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪ࠭ḁ"), False)
    def bstack1ll1l1l111_opy_(self, val):
        self._11111l1lll1_opy_[bstack111ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩḂ")] = str(val).lower() == bstack111ll_opy_ (u"ࠫࡹࡸࡵࡦࠩḃ")
    def bstack1ll1ll1lll1_opy_(self):
        return self._11111l1lll1_opy_.get(bstack111ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫḄ"), False)