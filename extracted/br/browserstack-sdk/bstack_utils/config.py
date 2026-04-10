# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
conf = {
    bstack1ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᷅"): False,
    bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ᷆"): True,
    bstack1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭᷇"): False,
    bstack1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬ᷈"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11111ll1l1l_opy_ = conf
    @classmethod
    def bstack1l111l1111_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11111ll1lll_opy_=None):
        return self._11111ll1l1l_opy_.get(property_name, bstack11111ll1lll_opy_)
    def bstack11l11l11ll_opy_(self, property_name, bstack11111ll1ll1_opy_):
        self._11111ll1l1l_opy_[property_name] = bstack11111ll1ll1_opy_
    def bstack11l1ll111_opy_(self, val):
        self._11111ll1l1l_opy_[bstack1ll_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪ࠭᷉")] = str(val).lower() == bstack1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ᷊")
    def bstack1ll1ll11l11_opy_(self):
        return self._11111ll1l1l_opy_.get(bstack1ll_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨ᷋"), False)
    def bstack11l1l11ll_opy_(self, val):
        self._11111ll1l1l_opy_[bstack1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫ᷌")] = str(val).lower() == bstack1ll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᷍")
    def bstack1lll111llll_opy_(self):
        return self._11111ll1l1l_opy_.get(bstack1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ᷎࠭"), False)