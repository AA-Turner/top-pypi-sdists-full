# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
conf = {
    bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᦛ"): False,
    bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᦜ"): True,
    bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫᦝ"): False,
    bstack11l1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠪᦞ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._111lllllll1_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11l11111111_opy_=None):
        return self._111lllllll1_opy_.get(property_name, bstack11l11111111_opy_)
    def bstack1l111111ll_opy_(self, property_name, bstack111llllllll_opy_):
        self._111lllllll1_opy_[property_name] = bstack111llllllll_opy_
    def bstack1l1l1111l1_opy_(self, val):
        self._111lllllll1_opy_[bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠫᦟ")] = bool(val)
    def should_skip_session_name(self):
        return self._111lllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠬᦠ"), False)
    def bstack1lllll11l1_opy_(self, val):
        self._111lllllll1_opy_[bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨᦡ")] = bool(val)
    def should_skip_session_status(self):
        return self._111lllllll1_opy_.get(bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩᦢ"), False)