# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from bstack_utils.constants import bstack11ll1111lll_opy_
def bstack11ll11111_opy_(bstack11ll1111ll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1111lllll_opy_
    host = bstack1111lllll_opy_(cli.config, [bstack1ll11ll_opy_ (u"ࠤࡤࡴ࡮ࡹࠢ᝱"), bstack1ll11ll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᝲ"), bstack1ll11ll_opy_ (u"ࠦࡦࡶࡩࠣᝳ")], bstack11ll1111lll_opy_)
    return bstack1ll11ll_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ᝴").format(host, bstack11ll1111ll1_opy_)