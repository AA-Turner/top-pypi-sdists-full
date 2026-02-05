# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
conf = {
    bstack11l1ll1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩᢩࠬ"): False,
    bstack11l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᢪ"): True,
    bstack11l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ᢫"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11l11l1ll11_opy_ = conf
    @classmethod
    def bstack1l11l11l1_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name, bstack11l11l1l1l1_opy_=None):
        return self._11l11l1ll11_opy_.get(property_name, bstack11l11l1l1l1_opy_)
    def bstack1l1l1111ll_opy_(self, property_name, bstack11l11l1l1ll_opy_):
        self._11l11l1ll11_opy_[property_name] = bstack11l11l1l1ll_opy_
    def bstack11ll1111_opy_(self, val):
        self._11l11l1ll11_opy_[bstack11l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨ᢬")] = bool(val)
    def bstack1lllll1l1ll_opy_(self):
        return self._11l11l1ll11_opy_.get(bstack11l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩ᢭"), False)