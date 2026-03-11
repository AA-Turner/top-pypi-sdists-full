# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
conf = {
    bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⊍"): False,
    bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭⊎"): True,
    bstack1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬ⊏"): False,
    bstack1ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫ⊐"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._1ll1lll11l11_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack1111l11lll1_opy_=None):
        return self._1ll1lll11l11_opy_.get(property_name, bstack1111l11lll1_opy_)
    def bstack1lll11l111_opy_(self, property_name, bstack1ll1lll11l1l_opy_):
        self._1ll1lll11l11_opy_[property_name] = bstack1ll1lll11l1l_opy_
    def bstack1llll1l1l1_opy_(self, val):
        self._1ll1lll11l11_opy_[bstack1ll111_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬ⊑")] = str(val).lower() == bstack1ll111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⊒")
    def should_skip_session_name(self):
        return self._1ll1lll11l11_opy_.get(bstack1ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠧ⊓"), False)
    def bstack11l1111l1l_opy_(self, val):
        self._1ll1lll11l11_opy_[bstack1ll111_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪ⊔")] = str(val).lower() == bstack1ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪ⊕")
    def should_skip_session_status(self):
        return self._1ll1lll11l11_opy_.get(bstack1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬ⊖"), False)