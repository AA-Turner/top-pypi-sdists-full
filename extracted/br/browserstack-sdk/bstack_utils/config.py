# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
conf = {
    bstack111lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ᜔࠭"): False,
    bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯᜕ࠩ"): True,
    bstack111lll_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨ᜖"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11ll1l1111l_opy_ = conf
    @classmethod
    def bstack1ll11lll1l_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11ll1l11111_opy_=None):
        return self._11ll1l1111l_opy_.get(property_name, bstack11ll1l11111_opy_)
    def bstack1lll1llll1_opy_(self, property_name, bstack11ll1l111l1_opy_):
        self._11ll1l1111l_opy_[property_name] = bstack11ll1l111l1_opy_
    def bstack11ll111ll1_opy_(self, val):
        self._11ll1l1111l_opy_[bstack111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ᜗")] = bool(val)
    def bstack1111ll1l1l_opy_(self):
        return self._11ll1l1111l_opy_.get(bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪ᜘"), False)