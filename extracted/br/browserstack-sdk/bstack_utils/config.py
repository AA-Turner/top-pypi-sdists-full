# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
conf = {
    bstack11lll1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᯁ"): False,
    bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᯂ"): True,
    bstack11lll1_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᯃ"): False,
    bstack11lll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠧᯄ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111l1ll111l_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111l1ll11l1_opy_=None):
        return self._111l1ll111l_opy_.get(property_name, bstack111l1ll11l1_opy_)
    def bstack1111l11l1_opy_(self, property_name, bstack111l1ll1111_opy_):
        self._111l1ll111l_opy_[property_name] = bstack111l1ll1111_opy_
    def bstack1ll1l11l1l_opy_(self, val):
        self._111l1ll111l_opy_[bstack11lll1_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨᯅ")] = str(val).lower() == bstack11lll1_opy_ (u"ࠬࡺࡲࡶࡧࠪᯆ")
    def should_skip_session_name(self):
        return self._111l1ll111l_opy_.get(bstack11lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪᯇ"), False)
    def bstack111111ll_opy_(self, val):
        self._111l1ll111l_opy_[bstack11lll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭ᯈ")] = str(val).lower() == bstack11lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᯉ")
    def should_skip_session_status(self):
        return self._111l1ll111l_opy_.get(bstack11lll1_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᯊ"), False)