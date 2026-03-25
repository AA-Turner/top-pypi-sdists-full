# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
conf = {
    bstack1l1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᯉ"): False,
    bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪᯊ"): True,
    bstack1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩᯋ"): False,
    bstack1l1_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠨᯌ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111l1l1ll1l_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111l1l1ll11_opy_=None):
        return self._111l1l1ll1l_opy_.get(property_name, bstack111l1l1ll11_opy_)
    def bstack11l11111ll_opy_(self, property_name, bstack111l1l1lll1_opy_):
        self._111l1l1ll1l_opy_[property_name] = bstack111l1l1lll1_opy_
    def bstack11ll1ll11l_opy_(self, val):
        self._111l1l1ll1l_opy_[bstack1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠩᯍ")] = str(val).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫᯎ")
    def should_skip_session_name(self):
        return self._111l1l1ll1l_opy_.get(bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫᯏ"), False)
    def bstack1l1lll1l1_opy_(self, val):
        self._111l1l1ll1l_opy_[bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧᯐ")] = str(val).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᯑ")
    def should_skip_session_status(self):
        return self._111l1l1ll1l_opy_.get(bstack1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩᯒ"), False)