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
from bstack_utils.constants import bstack11l111l1l11_opy_
def bstack11l11lll_opy_(bstack11l111l11ll_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1ll11l1l11_opy_
    host = bstack1ll11l1l11_opy_(cli.config, [bstack11l1l11_opy_ (u"ࠦࡦࡶࡩࡴࠤᥝ"), bstack11l1l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᥞ"), bstack11l1l11_opy_ (u"ࠨࡡࡱ࡫ࠥᥟ")], bstack11l111l1l11_opy_)
    return bstack11l1l11_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᥠ").format(host, bstack11l111l11ll_opy_)