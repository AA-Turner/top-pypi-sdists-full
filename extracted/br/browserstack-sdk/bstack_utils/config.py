# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
conf = {
    bstack111l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᷁"): False,
    bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰ᷂ࠪ"): True,
    bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ᷃"): False,
    bstack111l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨ᷄"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111lll1ll_opy_ = conf
    @classmethod
    def bstack1lll111ll_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111llll11_opy_=None):
        return self._11111lll1ll_opy_.get(property_name, bstack11111llll11_opy_)
    def bstack1l11ll11_opy_(self, property_name, bstack11111llll1l_opy_):
        self._11111lll1ll_opy_[property_name] = bstack11111llll1l_opy_
    def bstack1lll11l111_opy_(self, val):
        self._11111lll1ll_opy_[bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩ᷅")] = str(val).lower() == bstack111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ᷆")
    def bstack1lll11111ll_opy_(self):
        return self._11111lll1ll_opy_.get(bstack111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫ᷇"), False)
    def bstack1111111111_opy_(self, val):
        self._11111lll1ll_opy_[bstack111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ᷈")] = str(val).lower() == bstack111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᷉")
    def bstack1ll1l1l1l11_opy_(self):
        return self._11111lll1ll_opy_.get(bstack111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴ᷊ࠩ"), False)