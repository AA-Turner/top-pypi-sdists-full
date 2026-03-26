# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
conf = {
    bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᯡ"): False,
    bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ᯢ"): True,
    bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬᯣ"): False,
    bstack1ll1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫᯤ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111l1l11l11_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111l1l11l1l_opy_=None):
        return self._111l1l11l11_opy_.get(property_name, bstack111l1l11l1l_opy_)
    def bstack1l1ll1llll_opy_(self, property_name, bstack111l1l11ll1_opy_):
        self._111l1l11l11_opy_[property_name] = bstack111l1l11ll1_opy_
    def bstack1lllll11l_opy_(self, val):
        self._111l1l11l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬᯥ")] = str(val).lower() == bstack1ll1lll_opy_ (u"ࠩࡷࡶࡺ࡫᯦ࠧ")
    def should_skip_session_name(self):
        return self._111l1l11l11_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠧᯧ"), False)
    def bstack1ll11111ll_opy_(self, val):
        self._111l1l11l11_opy_[bstack1ll1lll_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪᯨ")] = str(val).lower() == bstack1ll1lll_opy_ (u"ࠬࡺࡲࡶࡧࠪᯩ")
    def should_skip_session_status(self):
        return self._111l1l11l11_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠬᯪ"), False)