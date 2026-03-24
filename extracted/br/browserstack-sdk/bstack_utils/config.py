# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
conf = {
    bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᯄ"): False,
    bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᯅ"): True,
    bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫᯆ"): False,
    bstack1ll1lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪᯇ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111l1l1lll1_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack111l1l1ll1l_opy_=None):
        return self._111l1l1lll1_opy_.get(property_name, bstack111l1l1ll1l_opy_)
    def bstack11lll11l11_opy_(self, property_name, bstack111l1l1llll_opy_):
        self._111l1l1lll1_opy_[property_name] = bstack111l1l1llll_opy_
    def bstack1l111111_opy_(self, val):
        self._111l1l1lll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫᯈ")] = str(val).lower() == bstack1ll1lll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᯉ")
    def should_skip_session_name(self):
        return self._111l1l1lll1_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪ࠭ᯊ"), False)
    def bstack11lll1llll_opy_(self, val):
        self._111l1l1lll1_opy_[bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩᯋ")] = str(val).lower() == bstack1ll1lll_opy_ (u"ࠫࡹࡸࡵࡦࠩᯌ")
    def should_skip_session_status(self):
        return self._111l1l1lll1_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫᯍ"), False)