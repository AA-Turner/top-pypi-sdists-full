# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from bstack_utils.constants import bstack1111l111l1l_opy_
def bstack1lllll1l1_opy_(bstack1111l111ll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1ll11l111l_opy_
    host = bstack1ll11l111l_opy_(cli.config, [bstack1l1111l_opy_ (u"ࠦࡦࡶࡩࡴࠤᶡ"), bstack1l1111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᶢ"), bstack1l1111l_opy_ (u"ࠨࡡࡱ࡫ࠥᶣ")], bstack1111l111l1l_opy_)
    return bstack1l1111l_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᶤ").format(host, bstack1111l111ll1_opy_)